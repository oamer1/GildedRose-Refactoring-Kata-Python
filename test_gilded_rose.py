# -*- coding: utf-8 -*-
import pytest

from gilded_rose import Item, GildedRose

# At the end of each day our system lowers both values for every item
def test_end_of_day_ordinary_item():
    """For ordinary item lower sell_in and quality"""
    item = Item("Foo", 10, 10)
    GildedRose([item]).update_quality()
    assert item.sell_in == 9
    assert item.quality == 9


# The Quality of an item is never negative
test_items = [
    Item("Bar", 10, 0),
    Item("Aged Brie", 10, 0),
    Item("Sulfuras, Hand of Ragnaros", 10, 0),
    Item("Backstage passes to a TAFKAL80ETC concert", 10, 0),
]


@pytest.mark.parametrize("item", test_items)
def test_quality_never_negative(item):
    GildedRose([item]).update_quality()
    assert item.quality >= 0


test_items_end_day = [
    item for item in test_items if item.name != "Sulfuras, Hand of Ragnaros"
]


@pytest.mark.parametrize("item", test_items_end_day)
def test_end_of_day_lower_sell_in(item):
    """Lower sell in except for Sulfuras"""
    prev_sell_in = item.sell_in
    GildedRose([item]).update_quality()
    assert item.sell_in == prev_sell_in - 1


# "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
def test_quality_never_negative():
    item = Item("Aged Brie", 10, 30)
    GildedRose([item]).update_quality()
    assert item.quality >= 0


# The Quality of an item is never more than 50
@pytest.mark.parametrize("item", test_items)
def test_quality_never_greater_50(item):
    item.quality = 50
    GildedRose([item]).update_quality()
    assert item.quality <= 50


# Once the sell by date has passed, Quality degrades twice as fast
def test_quality_non_special_item_passed_date_degrades_twice():
    item = Item("Foo", 0, 10)
    initial_quality = item.quality
    GildedRose([item]).update_quality()
    assert item.quality == initial_quality - 2


# "Aged Brie" actually increases in Quality the older it gets
def test_aged_brie_gets_older_quality_increase():
    item = Item("Aged Brie", 10, 10)
    initial_quality = item.quality
    GildedRose([item]).update_quality()
    assert item.quality > initial_quality


# "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
def test_Sulfuras_const_quality_and_sellin():
    item = Item("Sulfuras, Hand of Ragnaros", 10, 10)
    initial_sell_in = item.sell_in
    initial_quality = item.quality
    GildedRose([item]).update_quality()
    assert item.quality == initial_quality
    assert item.sell_in == initial_sell_in


# "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches;
def test_backstage_passes_gets_older_quality_increase():
    item = Item("Backstage passes to a TAFKAL80ETC concert", 10, 10)
    initial_quality = item.quality
    GildedRose([item]).update_quality()
    assert item.quality > initial_quality


days_range_10_to_6_inc = range(6, 11)
# Quality increases by 2 when there are 10 days or less
@pytest.mark.parametrize("day", days_range_10_to_6_inc)
def test_backstage_passes_10_days_increase_quality_by_2(day):
    item = Item("Backstage passes to a TAFKAL80ETC concert", day, 10)
    initial_quality = item.quality
    GildedRose([item]).update_quality()
    assert item.quality == initial_quality + 2


days_range_5_to_0_inc = range(0, 6)
# Quality increase by 3 when there are 5 days or less but
@pytest.mark.parametrize("day", days_range_10_to_6_inc)
def test_backstage_passes_5_days_less_increase_quality_by_3(day):
    item = Item("Backstage passes to a TAFKAL80ETC concert", day, 5)
    initial_quality = item.quality
    GildedRose([item]).update_quality()
    assert item.quality == initial_quality + 2


days_sample_less_than_0 = range(-10, 0)
# Quality drops to 0 after the concert
@pytest.mark.parametrize("day", days_sample_less_than_0)
def test_backstage_concert_finished_quality_0(day):
    item = Item("Backstage passes to a TAFKAL80ETC concert", day, 5)
    GildedRose([item]).update_quality()
    assert item.quality == 0
