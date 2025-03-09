import pytest

from src.gilded_rose import GildedRose
from src.item import Item


class TestGildedRose:
    @staticmethod
    def assert_item_sell_in_value(item: Item, *, expected_value: int) -> None:
        assert item.sell_in == expected_value, (
            f"sell_in value of item {item.name} is wrong. "
            f"Expected value: {expected_value}, actual value: {item.sell_in}"
        )

    @staticmethod
    def assert_item_quality_value(item: Item, *, expected_value: int) -> None:
        assert item.quality == expected_value, (
            f"quality value of item {item.name} is wrong. "
            f"Expected value: {expected_value}, actual value: {item.quality}"
        )

    @pytest.mark.parametrize(
        ("name", "sell_in", "quality", "updated_sell_in", "updated_quality"),
        (
            pytest.param(
                "Any Name",
                10,
                10,
                9,
                9,
                id="quality_degraded_normal_behavior",
            ),
            pytest.param(
                "Any Name",
                0,
                10,
                -1,
                8,
                id="quality_degraded_twice_after_sell_in",
            ),
            pytest.param(
                "Any Name",
                10,
                0,
                9,
                0,
                id="quality_not_lower_than_zero",
            ),
            pytest.param(
                "Aged Brie",
                10,
                10,
                9,
                11,
                id="quality_increased_for_aged_brie",
            ),
            pytest.param(
                "Aged Brie",
                0,
                10,
                -1,
                12,
                id="quality_increased_twice_for_aged_brie",
            ),
            pytest.param(
                "Aged Brie",
                10,
                50,
                9,
                50,
                id="quality_not_greater_than_fifty",
            ),
            pytest.param(
                "Sulfuras, Hand of Ragnaros",
                1,
                80,
                1,
                80,
                id="sulfuras_not_changed",
            ),
            pytest.param(
                "Backstage passes to a TAFKAL80ETC concert",
                15,
                1,
                14,
                2,
                id="quality_increased_for_passes",
            ),
            pytest.param(
                "Backstage passes to a TAFKAL80ETC concert",
                10,
                5,
                9,
                7,
                id="quality_increased_twice_for_passes",
            ),
            pytest.param(
                "Backstage passes to a TAFKAL80ETC concert",
                5,
                10,
                4,
                13,
                id="quality_increased_three_times_for_passes",
            ),
            pytest.param(
                "Backstage passes to a TAFKAL80ETC concert",
                0,
                20,
                -1,
                0,
                id="quality_to_zero_after_sell_in_for_passes",
            ),
            pytest.param(
                "Conjured",
                10,
                10,
                9,
                8,
                id="quality_degraded_twice_faster_for_conjured",
            ),
            pytest.param(
                "Conjured",
                0,
                10,
                -1,
                6,
                id="quality_degraded_four_times_faster_for_conjured_after_sell_in",
            ),
        ),
    )
    def test_gilded_rose(
        self,
        name: str,
        sell_in: int,
        quality: int,
        updated_sell_in: int,
        updated_quality: int,
    ) -> None:
        item = Item(name, sell_in, quality)

        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()

        self.assert_item_sell_in_value(item, expected_value=updated_sell_in)
        self.assert_item_quality_value(item, expected_value=updated_quality)
