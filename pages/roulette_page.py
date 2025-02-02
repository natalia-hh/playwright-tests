from playwright.sync_api import Page
from locators import RouletteLocators
from utils import format_number
from config import Config
from config import logger

class RoulettePage:
    def __init__(self, page: Page):
        self.page = page
    
    def goto_page(self):
        self.page.goto(Config.ROULETTE_LANDING_PAGE)
        self.page.wait_for_load_state("domcontentloaded")
        
    def accept_cookies(self):
        try:
            cookie_button = self.page.locator(RouletteLocators.COOKIE_BANNER_BUTTON)
            if cookie_button.is_visible(timeout=2000):
                cookie_button.click()
                logger.info("Cookie banner accepted.")
                self.page.locator(RouletteLocators.COOKIE_BANNER).wait_for(state="hidden", timeout=3000)
            else:
                logger.info("Cookie banner already accepted or not visible.")
        except Exception as e:
            logger.warning(f"Cookie banner handling skipped: {e}")
        
    def enter_bet_keyboard(self, bet_value):
        self.page.locator(RouletteLocators.BET_INPUT_FIELD).fill(str(bet_value))
        
    def clear_bet_value(self):
        self.page.locator(RouletteLocators.BET_INPUT_FIELD).fill('')
        self.page.click('body')

    def get_bet_input_value(self):
        return self.page.locator(RouletteLocators.BET_INPUT_FIELD).input_value()

    def find_adjust_bet_button(self, bet_button: str): # not(.button-pill) excluded as its Clear is for Mobile
        return self.page.locator(f'[data-testid^="roulette-bet-input"] button:not(.button-pill) >> text="{bet_button}"')
    
    def click_adjust_bet_button(self, bet_adjust_button_label: str):
        if bet_adjust_button_label not in RouletteLocators.ADJUST_BET_LOCATORS:
            logger.error(f"Unknown Adjust Bet button: {bet_adjust_button_label}")
            raise ValueError(f"Unknown Adjust Bet button: {bet_adjust_button_label}")
        try:
            self.page.locator(RouletteLocators.ADJUST_BET_LOCATORS[bet_adjust_button_label]).click()
        except Exception as e:
            logger.error(f"Failed to click Adjust Bet '{bet_adjust_button_label}': {e}")
    
    def click_place_bet_button(self, placebet_button: str):
        if placebet_button not in RouletteLocators.PLACE_BET_LOCATORS:
            logger.error(f"Invalid Place Bet button: {placebet_button}. Choose from: {list(RouletteLocators.PLACE_BET_LOCATORS.keys())}")
            raise ValueError(f"Invalid Place Bet button: {placebet_button}. Choose from: {list(RouletteLocators.PLACE_BET_LOCATORS.keys())}")
        try:
            self.page.locator(RouletteLocators.PLACE_BET_LOCATORS[placebet_button]).click()
        except Exception as e:
            logger.error(f"Failed to click '{placebet_button}' Place Bet button: {e}")
    
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
            raise ValueError(f"Unknown Ajdust Bet button: {button}") 
        return format_number(result)   