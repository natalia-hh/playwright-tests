from typing import Any
import pytest
from playwright.sync_api import expect
from pages.roulette_page import RoulettePage
from locators import RouletteLocators
from utils import load_json_test_data_comment
from config import Config
from config import logger

    # Рекомендация: Добавить сюда визуальные проверки или проверки кросс-браузерности (если это планируется).

bet_input_field_values_test_data = load_json_test_data_comment('bet_input_field_valid.json')
@pytest.mark.smoke
@pytest.mark.parametrize('input_value, expected_value, comment', bet_input_field_values_test_data,ids=[case[2] for case in bet_input_field_values_test_data])
def test_bet_input_field_valid(roulette_page: RoulettePage, input_value: tuple[Any, Any, Any], expected_value: tuple[Any, Any, Any], comment: tuple[Any, Any, Any]):
    """Bet Input field Validation"""
    roulette_page.clear_bet_value()
    roulette_page.enter_bet_keyboard(input_value)
    logger.info(f'Checking Bet Input Case: {comment}; Test value {input_value}; Expected value: {expected_value}')
    expect(roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)).to_have_value(expected_value)

bet_input_field_values_test_data = load_json_test_data_comment('bet_input_field_invalid.json')
@pytest.mark.smoke
@pytest.mark.parametrize('input_value, expected_value, comment', bet_input_field_values_test_data,ids=[case[2] for case in bet_input_field_values_test_data])
def test_bet_input_field_invalid(roulette_page: RoulettePage, input_value: tuple[Any, Any, Any], expected_value: tuple[Any, Any, Any], comment: tuple[Any, Any, Any]):
    """Bet Input field - Ensure invalid characters cannot be entered"""
    roulette_page.clear_bet_value()
    logger.info(f'Checking Bet Input Case: {comment}; Test value: {input_value}')
    roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD).press_sequentially(input_value, delay=100)
    expect(roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)).to_have_value(expected_value)
    border_locator = roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD).locator('..')
    logger.info(f'Checking if the border is highlighted in red')
    expect(border_locator).to_have_class(Config.ERROR_BORDER_STYLE)
    