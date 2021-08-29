# -*- coding: utf-8 -*-


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def increment_quality(self, quality, increment_unit):
        """Handles quality increments and ensures quality >0 and <50"""
        if quality > 0 and quality < 50:
            quality = quality + increment_unit
        return quality

    def update_ordinary_item(self, item):
        """Handle the logic of ordinary item"""
        # if -ve sell in quality degrades twice
        if item.sell_in <= 0:
            item.quality = self.increment_quality(item.quality, -2)
        else:
            item.quality = self.increment_quality(item.quality, -1)
        item.sell_in = item.sell_in - 1

    def update_backstage_passes_item(self, item):
        """Handle the logic of "Backstage passes to a TAFKAL80ETC concert" """

        if item.sell_in < 11:
            item.quality = self.increment_quality(item.quality, 2)
        if item.sell_in < 6:
            item.quality = self.increment_quality(item.quality, 1)
        if item.sell_in < 0:
            item.quality = 0
        item.sell_in = item.sell_in - 1

    def update_sulfuras_item(self, item):
        """Handle the logic of salfurus, do nothing"""
        return item

    def update_aged_brie(self, item):
        """Handle the logic of "Aged Brie" """
        item.quality = self.increment_quality(item.quality, 1)
        item.sell_in = item.sell_in - 1

    def update_conjured_item(self, item):
        """Handle the logic of Conjured item"""
        # if -ve sell in quality degrades twice
        if item.sell_in <= 0:
            item.quality = self.increment_quality(item.quality, -4)
        else:
            item.quality = self.increment_quality(item.quality, -2)
        item.sell_in = item.sell_in - 1

    def update_quality(self):

        for item in self.items:
            update_factory = {
                "Backstage passes to a TAFKAL80ETC concert": self.update_backstage_passes_item,
                "Aged Brie": self.update_aged_brie,
                "Sulfuras, Hand of Ragnaros": self.update_sulfuras_item,
                "Conjured": self.update_conjured_item,
            }
            update_func = update_factory.get(item.name, self.update_ordinary_item)
            return update_func(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):  # pragma: no cover
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
