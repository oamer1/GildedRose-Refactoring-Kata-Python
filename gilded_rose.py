# -*- coding: utf-8 -*-


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_backstage_passes_item(self, item):
        """Handle the logic of "Backstage passes to a TAFKAL80ETC concert" """

        if item.sell_in < 11 and item.quality < 50:
            item.quality = item.quality + 2
        if item.sell_in < 6 and item.quality < 50:
            item.quality = item.quality + 1
        if item.sell_in < 0:
            item.quality = 0

    def update_quality(self):
        special_items = [
            "Aged Brie",
            "Backstage passes to a TAFKAL80ETC concert",
            "Sulfuras, Hand of Ragnaros",
        ]
        for item in self.items:
            if item.name not in special_items and item.quality > 0:
                item.quality = item.quality - 1

            if item.name == "Backstage passes to a TAFKAL80ETC concert":
                self.update_backstage_passes_item(item)

            if item.name == "Aged Brie":
                if item.quality < 50:
                    item.quality = item.quality + 1

            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name not in special_items and item.quality > 0:
                    item.quality = item.quality - 1

                if item.name == "Aged Brie":
                    if item.quality < 50:
                        item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
