import pytest
from pages.roulette_page import RoulettePage

VALID_BROWSERS = ("chromium", "firefox", "webkit")

def pytest_addoption(parser):
    parser.addoption("--custom-browser", action="store", choices=VALID_BROWSERS, default="chromium", help="Browser to run tests on")
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode")

@pytest.fixture(scope="session")
def browser_type_launch_args(request):
    return {
        "headless": request.config.getoption("--headless")
    }

@pytest.fixture(scope="session")
def browser_context_args():
    return {
#        "record_video_dir": "test-results/videos", 
#        "record_har_path": "test-results/har"
    }

@pytest.fixture(scope='session')
def browser_session(playwright, request):
    browser_name = request.config.getoption("--custom-browser")
    headless = request.config.getoption("--headless")
    browser = getattr(playwright, browser_name).launch(headless=headless)
    yield browser
    browser.close()

@pytest.fixture(scope='function')
def browser_instance(browser_session):
    context = browser_session.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()

@pytest.fixture(scope='function')
def roulette_page(browser_instance) -> RoulettePage:
    roulette_page = RoulettePage(browser_instance)
    roulette_page.goto_page()
    roulette_page.accept_cookies()
    return roulette_page

@pytest.mark.skip
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.failed:
        page = item.funcargs.get("roulette_page").page
        screenshot_name = f"test-results/screenshots/failed_{item.name}.png"
        import os
        os.makedirs("test-results/screenshots", exist_ok=True)

        print(f"📸 Saving screenshot for failed test: {screenshot_name}")
        page.screenshot(path=screenshot_name)