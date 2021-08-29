# -*- coding: utf-8 -*-
import pytest

from gilded_rose import Item, GildedRose

test_items = [
    Item("Bar", 10, 0),
    Item("Aged Brie", 10, 0),
    Item("Sulfuras, Hand of Ragnaros", 10, 0),
    Item("Backstage passes to a TAFKAL80ETC concert", 10, 0),
    Item("Conjured", 10, 0),
]
# Exlude Sulfuras
test_items_except_sulfuras = [
    item for item in test_items if item.name != "Sulfuras, Hand of Ragnaros"
]


class TestCommonTraits:
    # The Quality of an item is never negative
    @pytest.mark.parametrize("item", test_items)
    def test_quality_never_negative(self, item):
        GildedRose([item]).update_quality()
        assert item.quality >= 0

    @pytest.mark.parametrize("item", test_items_except_sulfuras)
    def test_end_of_day_lower_sell_in(self, item):
        """Lower sell in except for Sulfuras"""
        prev_sell_in = item.sell_in
        GildedRose([item]).update_quality()
        assert item.sell_in == prev_sell_in - 1

    # The Quality of an item is never more than 50
    @pytest.mark.parametrize("item", test_items)
    def test_quality_never_greater_50(self, item):
        item.quality = 50
        GildedRose([item]).update_quality()
        assert item.quality <= 50


class TestNormalItems:
    """Test Normal items"""

    # At the end of each day our system lowers both values for every item
    def test_end_of_day_Normal_item(self):
        """For Normal item lower sell_in and quality"""
        item = Item("Foo", 10, 10)
        initial_quality = item.quality
        GildedRose([item]).update_quality()
        assert item.sell_in == 9
        assert item.quality == initial_quality - 1

    # Once the sell by date has passed, Quality degrades twice as fast
    def test_quality_Normal_item_passed_date_degrades_twice(self):
        item = Item("Foo", 0, 10)
        initial_quality = item.quality
        GildedRose([item]).update_quality()
        assert item.quality == initial_quality - 2


class TestAgedBrie:

    # "Aged Brie" actually increases in Quality the older it gets
    def test_aged_brie_gets_older_quality_increase(self):
        item = Item("Aged Brie", 10, 10)
        initial_quality = item.quality
        GildedRose([item]).update_quality()
        assert item.quality > initial_quality


class TestSulfuras:
    # "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
    def test_Sulfuras_const_quality_and_sellin(self):
        item = Item("Sulfuras, Hand of Ragnaros", 10, 10)
        initial_sell_in = item.sell_in
        initial_quality = item.quality
        GildedRose([item]).update_quality()
        assert item.quality == initial_quality
        assert item.sell_in == initial_sell_in


class TestBackstagePasses:
    days_range_10_to_6_inc = range(6, 11)
    days_range_5_to_0_inc = range(0, 6)
    days_sample_less_than_0 = range(-10, 0)

    # "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches;
    def test_backstage_passes_gets_older_quality_increase(self):
        item = Item("Backstage passes to a TAFKAL80ETC concert", 10, 10)
        initial_quality = item.quality
        GildedRose([item]).update_quality()
        assert item.quality > initial_quality

    # Quality increases by 2 when there are 10 days or less
    @pytest.mark.parametrize("day", days_range_10_to_6_inc)
    def test_backstage_passes_10_days_increase_quality_by_2(self, day):
        item = Item("Backstage passes to a TAFKAL80ETC concert", day, 10)
        initial_quality = item.quality
        GildedRose([item]).update_quality()
        assert item.quality == initial_quality + 2

    # Quality increase by 3 when there are 5 days or less but
    @pytest.mark.parametrize("day", days_range_10_to_6_inc)
    def test_backstage_passes_5_days_less_increase_quality_by_3(self, day):
        item = Item("Backstage passes to a TAFKAL80ETC concert", day, 5)
        initial_quality = item.quality
        GildedRose([item]).update_quality()
        assert item.quality == initial_quality + 2

    # Quality drops to 0 after the concert
    @pytest.mark.parametrize("day", days_sample_less_than_0)
    def test_backstage_concert_finished_quality_0(self, day):
        item = Item("Backstage passes to a TAFKAL80ETC concert", day, 5)
        GildedRose([item]).update_quality()
        assert item.quality == 0


class TestConjured:
    """Test Conjured items"""

    # At the end of each day our system lowers both values for every item
    def test_end_of_day_Normal_item(self):
        """For Normal item lower sell_in and quality"""
        item = Item("Conjured", 10, 10)
        initial_quality = item.quality
        GildedRose([item]).update_quality()
        assert item.sell_in == 9
        assert item.quality == initial_quality - 2

    # Once the sell by date has passed, Quality degrades twice as fast as Normal
    def test_quality_Conjured_item_passed_date_degrades_twice_as_Normal(self):
        item = Item("Conjured", 0, 10)
        initial_quality = item.quality
        GildedRose([item]).update_quality()
        assert item.quality == initial_quality - 4
