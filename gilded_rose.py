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
class Normal:
    def __init__(self, item) -> None:
        self.item = item

    # Properties so we dont have to use self.item.quality, self.item.sell_in
    @property
    def quality(self):
        return self.item.quality

    @quality.setter
    def quality(self, value):
        self.item.quality = value

    @property
    def sell_in(self):
        return self.item.sell_in

    @sell_in.setter
    def sell_in(self, value):
        self.item.sell_in = value

    max_quality = 50
    min_quality = 0
    deadline_sell_in = 0
    unit_delta = -1

    def increment_quality(self, increment_unit):
        """Handles quality increments and ensures quality >0 and <50 , invariant"""
        if self.quality > self.min_quality and self.quality < self.max_quality:
            self.quality = self.quality + increment_unit
        return self.quality

    def day_tick(self):
        # Advance day
        self.sell_in -= 1

    def update(self):
        # if -ve sell in quality degrades twice
        if self.sell_in <= self.deadline_sell_in:
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
        return item_class(item)

    def update(self):
        for item in self.items:
            gilded_item = self.item_factory(item)
            gilded_item.update()
