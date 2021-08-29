# -*- coding: utf-8 -*-
import pytest

from gilded_rose import AgedBrie, Item, GildedRose


# DRY easy to type constants
AGED_BRIE = "Aged Brie"
SULFURES = "Sulfuras, Hand of Ragnaros"
BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"
CONJURED = "Conjured"

test_items = [
    Item("Bar", 10, 0),
    Item(AGED_BRIE, 10, 0),
    Item(SULFURES, 10, 0),
    Item(BACKSTAGE, 10, 0),
    Item(CONJURED, 10, 0),
]
# Exlude Sulfuras
test_items_except_sulfuras = [item for item in test_items if item.name != SULFURES]


class TestCommonTraits:
    MAX_QUALITY = 50
    # The Quality of an item is never negative
    @pytest.mark.parametrize("item", test_items)
    def test_quality_never_negative(self, item):
        GildedRose([item]).update()
        assert item.quality >= 0

    @pytest.mark.parametrize("item", test_items_except_sulfuras)
    def test_end_of_day_lower_sell_in(self, item):
        """Lower sell in except for Sulfuras"""
        prev_sell_in = item.sell_in
        GildedRose([item]).update()
        assert item.sell_in == prev_sell_in - 1

    # The Quality of an item is never more than 50
    @pytest.mark.parametrize("item", test_items)
    def test_quality_never_greater_than_max_quality(self, item):
        item.quality = self.MAX_QUALITY
        GildedRose([item]).update()
        assert item.quality <= self.MAX_QUALITY


class TestNormalItems:
    """Test Normal items"""

    normal_rate = -1

    @pytest.fixture
    def valid_item(self):
        return Item("Foo", 10, 10)

    @pytest.fixture
    def passed_date_item(self):
        return Item("Foo", 0, 10)

    # At the end of each day our system lowers both values for every item
    def test_end_of_day(self, valid_item):
        """For Normal item lower sell_in and quality"""
        item = valid_item
        initial_quality = item.quality
        GildedRose([item]).update()
        assert item.sell_in == 9
        assert item.quality == initial_quality + self.normal_rate

    # Once the sell by date has passed, Quality degrades twice as fast
    def test_quality_item_passed_date_degrades_twice(self, passed_date_item):
        item = passed_date_item
        initial_quality = item.quality
        GildedRose([item]).update()
        assert item.quality == initial_quality + 2 * self.normal_rate


class TestAgedBrie:

    # "Aged Brie" actually increases in Quality the older it gets
    def test_aged_brie_gets_older_quality_increase(self):
        item = Item(AGED_BRIE, 10, 10)
        initial_quality = item.quality
        GildedRose([item]).update()
        assert item.quality == initial_quality + 1


class TestSulfuras:
    # "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
    # "Sulfuras" is a legendary item and as such its Quality is 80 and it never alters.
    # This is a bit ambigous should the client code maintain the invarient quality=80 or GildedRose ?!
    # Ask the goblin !!
    def test_Sulfuras_const_quality_and_sellin(self):
        item = Item(SULFURES, 10, 80)
        initial_sell_in = item.sell_in
        initial_quality = item.quality
        GildedRose([item]).update()
        assert item.quality == initial_quality
        assert item.sell_in == initial_sell_in


class TestBackstagePasses:
    days_range_10_to_6_inc = range(6, 11)
    days_range_5_to_0_inc = range(0, 6)
    days_sample_less_than_0 = range(-10, 0)

    # "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches;
    def test_backstage_passes_gets_older_quality_increase(self):
        item = Item(BACKSTAGE, 10, 10)
        initial_quality = item.quality
        GildedRose([item]).update()
        assert item.quality > initial_quality

    # Quality increases by 2 when there are 10 days or less
    @pytest.mark.parametrize("day", days_range_10_to_6_inc)
    def test_backstage_passes_10_days_or_less_increase_quality_by_2(self, day):
        item = Item(BACKSTAGE, day, 10)
        initial_quality = item.quality
        GildedRose([item]).update()
        assert item.quality == initial_quality + 2

    # Quality increase by 3 when there are 5 days or less but
    @pytest.mark.parametrize("day", days_range_5_to_0_inc)
    def test_backstage_passes_5_days_or_less_increase_quality_by_3(self, day):
        item = Item(BACKSTAGE, day, 5)
        initial_quality = item.quality
        GildedRose([item]).update()
        assert item.quality == initial_quality + 3

    # Quality drops to 0 after the concert
    @pytest.mark.parametrize("day", days_sample_less_than_0)
    def test_backstage_concert_finished_quality_0(self, day):
        item = Item(BACKSTAGE, day, 5)
        GildedRose([item]).update()
        assert item.quality == 0


class TestConjured(TestNormalItems):
    """Test Conjured items"""

    normal_rate = 2 * TestNormalItems.normal_rate

    @pytest.fixture
    def valid_item(self):
        return Item(CONJURED, 10, 10)

    @pytest.fixture
    def passed_date_item(self):
        return Item(CONJURED, 0, 10)
