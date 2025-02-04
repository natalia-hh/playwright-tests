class RouletteLocators:
    COOKIE_BANNER_BUTTON = '#cookiebanner a.c-button-primary'
    COOKIE_BANNER = '#cookiebanner'
      
    BET_SECTION = 'div[data-testid="roulette-bet-input"]'
    BET_INPUT_FIELD = '[data-testid="roulette-bet-input"] >> input'
    BET_INPUT_FIELD_ICON = '[data-testid="roulette-bet-input"] >> svg'
    
    ADJUST_BET_LOCATORS = {
        "clear": f'{BET_SECTION} [data-testid="roulette-bet-input-clearundefined"]',
        "plus_0.01": f'{BET_SECTION} [data-testid="roulette-bet-input-+0.01"]',
        "plus_0.1": f'{BET_SECTION} [data-testid="roulette-bet-input-+0.1"]',
        "plus_1": f'{BET_SECTION} [data-testid="roulette-bet-input-+1"]',
        "plus_10": f'{BET_SECTION} [data-testid="roulette-bet-input-+10"]',
        "plus_100": f'{BET_SECTION} [data-testid="roulette-bet-input-+100"]',
        "half": f'{BET_SECTION} [data-testid="roulette-bet-input-1/2"]',
        "double": f'{BET_SECTION} [data-testid="roulette-bet-input-x2"]',
        "max": f'{BET_SECTION} [data-testid="roulette-bet-input-maxundefined"]'
    }
    
    PLACE_BET_LOCATORS = {
        "ct": "[data-testid='bet-button-ct']",
        "bonus": "[data-testid='bet-button-bonus']",
        "t": "[data-testid='bet-button-t']"
    }
    
    