# -*- coding: utf-8 -*-


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def increment_quality(self, quality, increment_unit):
        """Handles quality increments and ensures quality >0 and <50"""
        if quality > 0 and quality < 50:
            quality = quality + increment_unit
        return quality

    def update_backstage_passes_item(self, item):
        """Handle the logic of "Backstage passes to a TAFKAL80ETC concert" """

        if item.sell_in < 11:
            item.quality = self.increment_quality(item.quality, 2)
        if item.sell_in < 6:
            item.quality = self.increment_quality(item.quality, 1)
        if item.sell_in < 0:
            item.quality = 0

    def update_quality(self):
        special_items = [
            "Aged Brie",
            "Backstage passes to a TAFKAL80ETC concert",
            "Sulfuras, Hand of Ragnaros",
        ]
        for item in self.items:
            if item.name not in special_items:
                item.quality = item.quality - 1

            if item.name == "Backstage passes to a TAFKAL80ETC concert":
                self.update_backstage_passes_item(item)

            if item.name == "Aged Brie":
                item.quality = self.increment_quality(item.quality, 1)

            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name not in special_items:
                    item.quality = self.increment_quality(item.quality, -1)

                if item.name == "Aged Brie":
                    item.quality = self.increment_quality(item.quality, 1)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
