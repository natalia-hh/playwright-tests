from playwright.sync_api import Page
from locators import RouletteLocators
from utils import format_number
from config import Config, logger
from pages.base_page import BasePage


class RoulettePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
    
    def goto_page(self):
        self.page.goto(Config.ROULETTE_LANDING_PAGE)
        self.page.wait_for_load_state("domcontentloaded")
        self.wait_for_element(RouletteLocators.BET_INPUT_FIELD, element_name='Bet Input field')
        
    def accept_cookies(self):
        try:
            cookie_button = self.page.locator(RouletteLocators.COOKIE_BANNER_BUTTON)
            if cookie_button.is_visible(timeout=2000):
                self.click(RouletteLocators.COOKIE_BANNER_BUTTON, element_name='Accept Cookie button')
                self.wait_for_element(RouletteLocators.COOKIE_BANNER, state='hidden', element_name='Accept Cookie banner')
            else:
                logger.info("Cookie banner already accepted or not visible.")
        except Exception as e:
            logger.warning(f"Cookie banner handling skipped: {e}")

    def clear_bet_value(self):
        self.fill(RouletteLocators.BET_INPUT_FIELD, '', element_name='Bet Input field')

    def enter_bet_keyboard(self, bet_value):
        self.fill(RouletteLocators.BET_INPUT_FIELD, str(bet_value), element_name='Bet Input field')

    def get_bet_input_value(self):
        return self.get_input_value(RouletteLocators.BET_INPUT_FIELD, element_name='Bet Input field')

    def find_adjust_bet_button(self, bet_button: str):
        return self.page.locator(f'[data-testid^="roulette-bet-input"] button:not(.button-pill) >> text="{bet_button}"')
            
    def click_adjust_bet_button(self, adjust_bet_button_label: str):
        if adjust_bet_button_label not in RouletteLocators.ADJUST_BET_LOCATORS:
            logger.error(f"Unknown Adjust Bet button: {adjust_bet_button_label}")
            raise ValueError(f"Unknown Adjust Bet button: {adjust_bet_button_label}")
        self.click(RouletteLocators.ADJUST_BET_LOCATORS[adjust_bet_button_label], element_name=f'Adjust Bet Button {adjust_bet_button_label}')
    
    def click_place_bet_button(self, place_bet_button: str):
        if place_bet_button not in RouletteLocators.PLACE_BET_LOCATORS:
            logger.error(f"Unknown Place Bet button: {place_bet_button}")
            raise ValueError(f"Unknown Place Bet button: {place_bet_button}")
        self.click(RouletteLocators.PLACE_BET_LOCATORS[place_bet_button], element_name=f'Place Bet Button {place_bet_button}')    
    
    def calculate_bet(self, initial_value, button: str) -> str:
        if button == 'clear':
            result = '0'
        elif button.startswith('plus_'):
            increment = float(button.strip('plus_'))
            result = round(initial_value + increment + 1e-9, 2)
        elif button == 'half':
            result = round(initial_value / 2 + 1e-9, 2)
        elif button == 'double':
            result = round(initial_value * 2 + 1e-9, 2)
        elif button == 'max':
            result = initial_value # Correct for non-signed-in users only; a different scenario is required for the signed-in precondition
        else:
            raise ValueError(f"Unknown Adjust Bet button: {button}")
        return format_number(result)
    