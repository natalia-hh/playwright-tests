import re
import pytest
from playwright.sync_api import expect
from pages.roulette_page import RoulettePage
from locators import RouletteLocators
from utils import load_json_test_data_comment
from utils import Translations
from config import Config
from config import logger

@pytest.fixture(scope='function', autouse=True)
def roulette_page(browser_instance) -> RoulettePage:
    roulette_page = RoulettePage(browser_instance)
    roulette_page.goto_page()
    roulette_page.accept_cookies()
    return roulette_page

def test_webpage_healthcheck(roulette_page: RoulettePage):
    """Verify CSGO/Roulette UI and Bet elements exist."""
    logger.info('Checking Page Title - CSGOEmpire text')
    expect(roulette_page.page).to_have_url(Config.ROULETTE_LANDING_PAGE)
    expect(roulette_page.page).to_have_title(Config.PAGE_TITLE_REGEX)
    logger.info('Checking Bet Input field')
    expect(roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)).to_be_visible()
    for label, locator in RouletteLocators.ADJUST_BET_LOCATORS.items():
        logger.info(f'Checking Adjust Bet Button: {label}')
        expect(roulette_page.page.locator(locator)).to_be_visible()
    for label, locator in RouletteLocators.PLACE_BET_LOCATORS.items():
        logger.info(f'Checking Place Bet Button: {label}')
        expect(roulette_page.page.locator(locator)).to_be_visible()
    expected_buttons_count = len(RouletteLocators.ADJUST_BET_LOCATORS)
    logger.info(f'Checking Total Number of Adjust Bet buttons: {expected_buttons_count}')
    expect(roulette_page.page.locator(f'{RouletteLocators.BET_SECTION} button:not(.button-pill)')).to_have_count(expected_buttons_count)

# @pytest.mark.translations
@pytest.mark.parametrize('language', Config.SUPPORTED_LANGUAGES)
def test_webpage_labels(roulette_page: RoulettePage, language):
    """Verify CSGO/Roulette UI and Bet elements translations"""

    roulette_page.page.evaluate(f"""(lang) => {{
        localStorage.setItem('userChosenLocale', lang);  
        localStorage.setItem('userHasChosenLocal', 'true'); 
    }}""", language)
    roulette_page.page.reload()
    
    Translations.LANGUAGE = language
    
    logger.info(f'[{language}] Checking Page Title: {Translations.get_label('roulette_page','title')}')
    expect(roulette_page.page).to_have_title(Translations.get_label('roulette_page','title'))
    logger.info(f'[{language}] Bet Input field placeholder: {Translations.get_label('bet_input_field','placeholder')}')
    expect(roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)).to_have_attribute('placeholder', Translations.get_label('bet_input_field','placeholder'))

    translations = Translations.get_group("adjust_bet_buttons")
    for key, locator in RouletteLocators.ADJUST_BET_LOCATORS.items():
        expected_label = translations.get(key, 'no label found')
        logger.info(f'[{language}] Checking Adjust Bet Button: {key} to have label: {expected_label}')
        expect(roulette_page.page.locator(locator)).to_be_visible()   
        expect(roulette_page.page.locator(locator)).to_have_text(expected_label)
    
    translations = Translations.get_group("place_bet_buttons")      
    for key, locator in RouletteLocators.PLACE_BET_LOCATORS.items():
        expected_label = translations.get(key, 'no label found')
        logger.info(f'[{language}] Checking Place Bet Button: {key} to have label: {expected_label}')
        expect(roulette_page.page.locator(locator)).to_be_visible()   
        expect(roulette_page.page.locator(locator)).to_contain_text(expected_label) # contain_text, because there are Win 2x, W14x texts, need to cover later
    
bet_input_field_values_test_data = load_json_test_data_comment('bet_input_field_valid.json')
@pytest.mark.parametrize('input_value, expected_value, comment', bet_input_field_values_test_data,ids=[case[2] for case in bet_input_field_values_test_data])
def test_bet_input_field_valid(roulette_page: RoulettePage, input_value, expected_value, comment):
    """Bet Input field Validation"""
    roulette_page.clear_bet_value()
    roulette_page.enter_bet_keyboard(input_value)
    roulette_page.page.click('body')
    logger.info(f'Checking Bet Input Case: {comment}; Test value {input_value}; Expected value: {expected_value}')
    expect(roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)).to_have_value(expected_value)

bet_input_field_values_test_data = load_json_test_data_comment('bet_input_field_invalid.json')
@pytest.mark.parametrize('input_value, expected_value, comment', bet_input_field_values_test_data,ids=[case[2] for case in bet_input_field_values_test_data])
def test_bet_input_field_invalid(roulette_page: RoulettePage, input_value, expected_value, comment):
    """Bet Input field - Ensure invalid characters cannot be entered"""
    roulette_page.clear_bet_value()
    logger.info(f'Checking Bet Input Case: {comment}; Test value: {input_value}')
    typed_so_far = ""
    for char in input_value:
        roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD).type(char)
        typed_so_far += char
        # optional to debug
        # current_val = roulette_page.get_bet_input_value()
        # print(f"After typing {typed_so_far}: {current_val}")
    expect(roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)).to_have_value(expected_value)
    border_locator = roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD).locator('..')
    logger.info(f'Checking if the border is highlighted in red')
    expect(border_locator).to_have_class(Config.ERROR_BORDER_STYLE)

@pytest.mark.parametrize(
    ('adjust_bet_button', 'initial_value'), 
    [(button, value) for button in RouletteLocators.ADJUST_BET_LOCATORS.keys() for value in [0.01, 0, 10, 100.05, 9999]])
def test_adjust_bet_buttons(roulette_page: RoulettePage, adjust_bet_button, initial_value):
    """Adjust Bet Buttons Verification"""
         # ..scenario 1 - positive check all buttons:
    # initial_value = 10
    roulette_page.clear_bet_value() 
    roulette_page.enter_bet_keyboard(initial_value)
    roulette_page.click_adjust_bet_button(adjust_bet_button)
    expected_value = roulette_page.calculate_bet(float(initial_value), adjust_bet_button)
    logger.info(f'Checking that initial value {initial_value} adjusted by {adjust_bet_button}; Expected value: {expected_value}')
    expect(roulette_page.page.locator(RouletteLocators.BET_INPUT_FIELD)).to_have_value(expected_value)
         
         # ..scenario 2 - combination of multiple similar adjustements     
            
         # ..scenario 3 - combination of multiple different adjustements     
         