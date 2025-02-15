import os

import pytest
from PIL import Image, ImageChops
from playwright.sync_api import expect

from config import Config, logger
from locators import RouletteLocators
from pages.roulette_page import RoulettePage
from utils import load_json_test_data_comment


bet_input_field_values_test_data = load_json_test_data_comment(
    "bet_input_field_valid.json"
)


@pytest.mark.smoke
@pytest.mark.parametrize(
    "input_value, expected_value, comment",
    bet_input_field_values_test_data,
    ids=[case[2] for case in bet_input_field_values_test_data],
)
def test_bet_input_field_valid(
    roulette_page: RoulettePage, input_value, expected_value, comment
):
    """
    Validates that the bet input field accepts valid numeric values.
    Ensures correct formatting and value display after input for different valid cases.
    """
    roulette_page.clear_bet_value()
    roulette_page.enter_bet_keyboard(input_value)
    logger.info(
        f"Checking Bet Input Case: {comment}; Test value {input_value}; Expected value: {expected_value}"
    )
    expect(roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)).to_have_value(
        expected_value
    )


bet_input_field_values_test_data = load_json_test_data_comment(
    "bet_input_field_invalid.json"
)


@pytest.mark.smoke
@pytest.mark.parametrize(
    "input_value, expected_value, comment",
    bet_input_field_values_test_data,
    ids=[case[2] for case in bet_input_field_values_test_data],
)
def test_bet_input_field_invalid(
    roulette_page: RoulettePage, input_value, expected_value, comment
):
    """
    Ensures the bet input field rejects invalid characters and highlights errors.
    Verifies that invalid inputs are ignored and the field is visually marked with an error style.
    """
    roulette_page.clear_bet_value()
    logger.info(f"Checking Bet Input Case: {comment}; Test value: {input_value}")
    roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD).press_sequentially(
        input_value, delay=100
    )
    expect(roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)).to_have_value(
        expected_value
    )
    border_locator = roulette_page.page.locator(
        RouletteLocators.BET_INPUT_FIELD
    ).locator("..")
    logger.info(f"Checking if the border is red for {input_value}")
    expect(border_locator).to_have_class(Config.ERROR_BORDER_STYLE)


@pytest.mark.regression
def test_bet_input_icon_visibility(roulette_page: RoulettePage):
    """
    Verifies the visibility, size, structure, and image of the bet input icon.
    """
    icon_locator = roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD_ICON)

    logger.info("Checking if the bet input icon is visible.")
    expect(icon_locator).to_be_visible()

    bounding_box = icon_locator.bounding_box()
    logger.info(
        f"Checking icon dimensions: {bounding_box['width']}x{bounding_box['height']}"
    )
    assert bounding_box["width"] == 14, "Icon width should be 14px"
    assert bounding_box["height"] == 14, "Icon height should be 14px"

    logger.info("Checking if the SVG icon contains a <path> element.")
    path_element = icon_locator.locator("path")
    expect(path_element).to_be_visible()

    logger.info(
        "Capturing a screenshot of the bet input icon and comparing it with the baseline."
    )
    current_screenshot = "test-results/snapshots/bet_input_icon.png"
    baseline_screenshot = "data/images/bet_input_icon.png"

    icon_locator.screenshot(path=current_screenshot)

    if not os.path.exists(baseline_screenshot):
        logger.warning(
            "Baseline screenshot not found. Creating one for future comparisons."
        )
        icon_locator.screenshot(path=baseline_screenshot)
    else:
        with Image.open(current_screenshot) as current, Image.open(
            baseline_screenshot
        ) as baseline:
            diff = ImageChops.difference(current, baseline)
            if diff.getbbox():
                diff.save("snapshots/diff_bet_input_icon.png")
                raise AssertionError(
                    "The current screenshot does not match the baseline."
                )
