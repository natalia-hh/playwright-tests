import pytest
from playwright.sync_api import expect

from config import Config, logger
from locators import RouletteLocators
from pages.roulette_page import RoulettePage
from utils import Translations


def set_language(roulette_page, language):
    """Helper function to set language and reload the page."""
    roulette_page.page.evaluate(
        """(lang) => {{
        localStorage.setItem('userChosenLocale', lang);
        localStorage.setItem('userHasChosenLocal', 'true');
    }}""",
        language,
    )
    roulette_page.page.reload()
    Translations.LANGUAGE = language
    logger.info(f"[{language}] Language set successfully")


@pytest.mark.regression
@pytest.mark.parametrize("language", Config.SUPPORTED_LANGUAGES)
def test_webpage_labels(roulette_page: RoulettePage, language):
    """
    Verifies that the page title and bet input placeholder are correctly translated.
    """
    set_language(roulette_page, language)

    logger.info(
        f'[{language}] Checking Page Title: {Translations.get_label("roulette_page", "title")}'
    )
    expect(roulette_page.page).to_have_title(
        Translations.get_label("roulette_page", "title")
    )

    logger.info(
        f'[{language}] Bet Input field placeholder: {Translations.get_label("bet_input_field", "placeholder")}'
    )
    expect(
        roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)
    ).to_have_attribute(
        "placeholder", Translations.get_label("bet_input_field", "placeholder")
    )


@pytest.mark.regression
@pytest.mark.parametrize("language", Config.SUPPORTED_LANGUAGES)
def test_adjust_bet_buttons_labels(roulette_page: RoulettePage, language):
    """
    Validates the translation of 'Adjust Bet' button labels for supported languages.
    Ensures each button is visible and displays the correct localized text.
    """
    set_language(roulette_page, language)

    translations = Translations.get_group("adjust_bet_buttons")
    for key, locator in RouletteLocators.ADJUST_BET_LOCATORS.items():
        expected_label = translations.get(key, "no label found")
        logger.info(
            f"[{language}] Checking Adjust Bet Button: {key} to have label: {expected_label}"
        )
        expect(roulette_page.page.locator(locator)).to_be_visible()
        expect(roulette_page.page.locator(locator)).to_have_text(expected_label)


@pytest.mark.regression
@pytest.mark.parametrize("language", Config.SUPPORTED_LANGUAGES)
def test_place_bet_buttons_labels(roulette_page: RoulettePage, language):
    """
    Validates the translation of 'Place Bet' button labels for supported languages.
    Ensures each button is visible and displays the correct localized text.
    """
    set_language(roulette_page, language)

    translations = Translations.get_group("place_bet_buttons")
    for key, locator in RouletteLocators.PLACE_BET_LOCATORS.items():
        expected_label = translations.get(key, "no label found")
        logger.info(
            f"[{language}] Checking Place Bet Button: {key} to have label: {expected_label}"
        )
        expect(roulette_page.page.locator(locator)).to_be_visible()
        expect(roulette_page.page.locator(locator)).to_contain_text(
            expected_label
        )  # contain_text, because there are Win 2x, W14x texts, need to cover later
