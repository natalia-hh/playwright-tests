import pytest
from playwright.sync_api import expect

from config import Config, logger
from locators import RouletteLocators
from pages.roulette_page import RoulettePage


@pytest.mark.smoke
def test_webpage_healthcheck(roulette_page: RoulettePage):
    """
    Verifies the Roulette page loads correctly with all key UI elements visible.
    Checks the page URL, title, bet input field, adjust/place bet buttons,
    and validates the count of adjust bet buttons.
    """
    logger.info("Checking Page Title - CSGOEmpire text")
    expect(roulette_page.page).to_have_url(Config.ROULETTE_LANDING_PAGE)
    expect(roulette_page.page).to_have_title(Config.PAGE_TITLE_REGEX)
    logger.info("Checking Bet Input field")
    expect(roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)).to_be_visible()
    for label, locator in RouletteLocators.ADJUST_BET_LOCATORS.items():
        logger.info(f"Checking Adjust Bet Button: {label}")
        expect(roulette_page.page.locator(locator)).to_be_visible()
    for label, locator in RouletteLocators.PLACE_BET_LOCATORS.items():
        logger.info(f"Checking Place Bet Button: {label}")
        expect(roulette_page.page.locator(locator)).to_be_visible()
    expected_buttons_count = len(RouletteLocators.ADJUST_BET_LOCATORS)
    logger.info(
        f"Checking Total Number of Adjust Bet buttons: {expected_buttons_count}"
    )
    expect(
        roulette_page.page.locator(
            f"{RouletteLocators.BET_SECTION} button:not(.button-pill)"
        )
    ).to_have_count(expected_buttons_count)
