import logging
import re

class Config:
    BASE_URL = 'https://csgoempire.com'
    ROULETTE_LANDING_PAGE = f'{BASE_URL}/roulette'
    PAGE_TITLE_REGEX = re.compile('.*CSGOEmpire.*')
    SUPPORTED_LANGUAGES = ["en", "es"]
    ERROR_BORDER_STYLE = re.compile('.*border-red-2.*')

class LoggerConfig:
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOG_FILE = 'test-results/logs/test_log.log'

    @staticmethod
    def setup_logging():
        logger = logging.getLogger(__name__)
        logger.setLevel(LoggerConfig.LOG_LEVEL)

        if logger.hasHandlers():
            logger.handlers.clear()

        # file_handler = logging.FileHandler(LoggerConfig.LOG_FILE)
        # file_handler.setFormatter(logging.Formatter(LoggerConfig.LOG_FORMAT))
        # logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LoggerConfig.LOG_FORMAT))
        logger.addHandler(console_handler)

        return logger

logger = LoggerConfig.setup_logging()