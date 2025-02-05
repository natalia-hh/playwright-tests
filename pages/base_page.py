from playwright.sync_api import Page
from config import logger


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def click(self, locator: str, element_name: str = "Element"):
        try:
            self.page.locator(locator).click()
            logger.info(f"Clicked on '{element_name}'")
        except Exception as e:
            logger.error(f"Failed to click on '{element_name}': {e}")

    def fill(self, locator: str, value: str, element_name: str = "Input Field"):
        try:
            self.page.locator(locator).fill(value)
            logger.info(f"Filled '{element_name}' with value: '{value}'")
        except Exception as e:
            logger.error(f"Failed to fill '{element_name}' with value '{value}': {e}")

    def get_input_value(self, locator: str, element_name: str = "Input Field") -> str:
        try:
            value = self.page.locator(locator).input_value()
            logger.info(f"Retrieved value from '{element_name}': '{value}'")
            return value
        except Exception as e:
            logger.error(f"Failed to get input value from '{element_name}': {e}")
            return ""

    def wait_for_element(self, locator: str, state: str = "visible", timeout: int = 3000, element_name: str = "Element"):
        try:
            self.page.locator(locator).wait_for(state=state, timeout=timeout)
            logger.info(f"'{element_name}' is now {state}")
        except Exception as e:
            logger.warning(f"Timeout waiting for '{element_name}' to be {state}: {e}")
