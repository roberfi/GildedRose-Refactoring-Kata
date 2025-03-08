from src.item import Item

ITEM_NAME_AGED_BRIE = "Aged Brie"
ITEM_NAME_PASSES = "Backstage passes to a TAFKAL80ETC concert"
ITEM_NAME_SULFURAS = "Sulfuras, Hand of Ragnaros"

MIN_QUALITY = 0
MAX_QUALITY = 50


class GildedRose(object):
    def __init__(self, items: list[Item]) -> None:
        self.items = items

    @staticmethod
    def __get_item_quality(
        sell_in: int, previous_quality: int, increase_quality: bool = False
    ) -> int:
        factor = 2 if sell_in < 0 else 1

        if increase_quality:
            return previous_quality + factor

        return previous_quality - factor

    @staticmethod
    def __get_passes_quality(sell_in: int, previous_quality: int) -> int:
        if sell_in < 0:
            return 0

        factor = 1 if sell_in > 10 else 2 if sell_in > 5 else 3
        return previous_quality + factor

    def update_quality(self) -> None:
        for item in self.items:
            if item.name == ITEM_NAME_SULFURAS:
                continue

            item.sell_in = item.sell_in - 1

            if item.name == ITEM_NAME_PASSES:
                item.quality = self.__get_passes_quality(
                    item.sell_in,
                    item.quality,
                )
            else:
                item.quality = self.__get_item_quality(
                    item.sell_in,
                    item.quality,
                    increase_quality=(item.name == ITEM_NAME_AGED_BRIE),
                )

            item.quality = max(min(item.quality, MAX_QUALITY), MIN_QUALITY)
