import pytest
from playwright.sync_api import expect

from config import logger
from locators import RouletteLocators
from pages.roulette_page import RoulettePage


@pytest.mark.regression
@pytest.mark.parametrize(
    ("adjust_bet_button_label", "initial_value"),
    [
        (button, value)
        for button in RouletteLocators.ADJUST_BET_LOCATORS.keys()
        for value in [0.01, 0, 10, 100.05, 9999]
    ],
)
def test_adjust_bet_buttons(
    roulette_page: RoulettePage, adjust_bet_button_label, initial_value
):
    """
    Verifies the functionality of 'Adjust Bet' buttons with various initial bet values.
    Ensures each button correctly adjusts the bet value based on predefined logic
    for different scenarios, including edge cases like zero and large numbers.
    """
    # ..scenario 1 - positive check all buttons:
    roulette_page.clear_bet_value()
    roulette_page.enter_bet_keyboard(initial_value)
    roulette_page.click_adjust_bet_button(adjust_bet_button_label)
    expected_value = roulette_page.calculate_bet(
        float(initial_value), adjust_bet_button_label
    )
    logger.info(
        f"Checking that initial value {initial_value} adjusted by {adjust_bet_button_label}; Expected value: {expected_value}"
    )
    expect(roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)).to_have_value(
        expected_value
    )

    # ..scenario 2 - combination of multiple similar adjustements

    # ..scenario 3 - combination of multiple different adjustements
