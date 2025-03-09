from typing import List

from src.item import Item

ITEM_NAME_AGED_BRIE = "Aged Brie"
ITEM_NAME_PASSES = "Backstage passes to a TAFKAL80ETC concert"
ITEM_NAME_SULFURAS = "Sulfuras, Hand of Ragnaros"
ITEM_NAME_CONJURED = "Conjured"

PASSES_SELL_IN_THRESHOLD_1 = 10
PASSES_SELL_IN_THRESHOLD_2 = 5

MIN_QUALITY = 0
MAX_QUALITY = 50


class GildedRose(object):
    def __init__(self, items: List[Item]) -> None:
        self.items = items

    @staticmethod
    def __get_item_updated_quality(
        sell_in: int, previous_quality: int, increase_quality: bool = False, double_quality_change: bool = False
    ) -> int:
        factor = 2 if sell_in < 0 else 1

        if double_quality_change:
            factor *= 2

        if increase_quality:
            return previous_quality + factor

        return previous_quality - factor

    @staticmethod
    def __get_passes_updated_quality(sell_in: int, previous_quality: int) -> int:
        if sell_in < 0:
            return 0

        factor = 1 if sell_in > PASSES_SELL_IN_THRESHOLD_1 else 2 if sell_in > PASSES_SELL_IN_THRESHOLD_2 else 3
        return previous_quality + factor

    def update_quality(self) -> None:
        for item in self.items:
            if item.name == ITEM_NAME_SULFURAS:
                continue

            item.sell_in = item.sell_in - 1

            if item.name == ITEM_NAME_PASSES:
                item.quality = self.__get_passes_updated_quality(
                    item.sell_in,
                    item.quality,
                )
            else:
                item.quality = self.__get_item_updated_quality(
                    item.sell_in,
                    item.quality,
                    increase_quality=(item.name == ITEM_NAME_AGED_BRIE),
                    double_quality_change=(item.name == ITEM_NAME_CONJURED),
                )

            item.quality = max(min(item.quality, MAX_QUALITY), MIN_QUALITY)
