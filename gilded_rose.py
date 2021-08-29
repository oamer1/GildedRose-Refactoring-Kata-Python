# -*- coding: utf-8 -*-

# Don't touch me
"""
do not alter the Item class or Items property as those belong to the
goblin in the corner who will insta-rage and one-shot you as he doesn't believe in shared code
ownership
"""


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):  # pragma: no cover
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


# It we are allowed to change Item class , this class is not necessary
# Since we can add this method into Item, but the whole point of this exercise
# to add feature to the legacy code of the goblin !
class Normal(Item):
    max_quality = 50
    unit_delta = -1

    def increment_quality(self, increment_unit):
        """Handles quality increments and ensures quality >0 and <50 , invarient"""
        if self.quality > 0 and self.quality < self.max_quality:
            self.quality = self.quality + increment_unit
        return self.quality

    def day_tick(self):
        # Advance day
        self.sell_in -= 1

    def update(self):
        # if -ve sell in quality degrades twice
        if self.sell_in <= 0:
            self.quality = self.increment_quality(2 * self.unit_delta)
        else:
            self.quality = self.increment_quality(self.unit_delta)
        self.day_tick()


class AgedBrie(Normal):
    """
    "Aged Brie" actually increases in Quality the older it gets
    """

    unit_delta = 1

    def update(self):
        self.quality = self.increment_quality(self.unit_delta)
        self.day_tick()


class Sulfuras(Normal):
    """
    Sulfuras, Hand of Ragnaros
    "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
    """

    def update(self):
        pass


class Conjured(Normal):
    """
    "Conjured" items degrade in Quality twice as fast as normal items
    """

    unit_delta = 2 * Normal.unit_delta


class Backstage(Normal):
    """
    Backstage passes", like aged brie, increases in Quality as its SellIn value approaches;
    Quality increases by 2 when there are 10 days or less and by 3 when there are 5 days or less but
    Quality drops to 0 after the concert
    """

    def update(self):
        if self.sell_in < 0:
            self.quality = 0
        elif self.sell_in < 6:
            self.quality = self.increment_quality(3)
        elif self.sell_in < 11:
            self.quality = self.increment_quality(2)

        self.day_tick()


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    @staticmethod
    def item_factory(item):
        special_items = {
            "Backstage passes to a TAFKAL80ETC concert": Backstage,
            "Aged Brie": AgedBrie,
            "Sulfuras, Hand of Ragnaros": Sulfuras,
            "Conjured": Conjured,
        }
        item_class = special_items.get(item.name, Normal)
        return item_class(item.name, item.sell_in, item.quality)

    def update(self):
        for item in self.items:
            gilded_item = self.item_factory(item)
            gilded_item.update()
            self.update_item_attrs(item, gilded_item)

    def update_item_attrs(self, item, gilded_item):
        """
        Update item attrs so I dont have to change all of tests since
        tests assume GildedRose directly update item attrs.
        ** Also since this is a legacy code , returning gilded items, instead of
        directly manipulating items as in original code might break any existing code ! **
        Can be avoided if gilded classes initialised with item object instead of item attrs.
        """
        for attr, value in gilded_item.__dict__.items():
            setattr(item, attr, value)
