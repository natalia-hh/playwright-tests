import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://csgoempire.com/roulette")
    page.get_by_placeholder("Enter bet amount...").click()
    expect(page.locator("div").filter(has_text=re.compile(r"^Clear$"))).to_be_visible()
    expect(page.get_by_role("button", name="Clear")).to_be_visible()
    expect(page.get_by_role("button", name="+ 0.01")).to_be_visible()
    expect(page.get_by_role("button", name="+ 0.1")).to_be_visible()
    expect(page.get_by_role("button", name="+ 1", exact=True)).to_be_visible()
    expect(page.get_by_role("button", name="+ 10", exact=True)).to_be_visible()
    expect(page.get_by_role("button", name="+ 100")).to_be_visible()
    expect(page.get_by_role("button", name="/ 2")).to_be_visible()
    expect(page.get_by_role("button", name="x 2")).to_be_visible()
    expect(page.get_by_role("button", name="Max")).to_be_visible()
    expect(page.get_by_placeholder("Enter bet amount...")).to_be_empty();
    page.get_by_role("button", name="Clear").click()
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("0.00");
    page.get_by_placeholder("Enter bet amount...").click()
    page.get_by_placeholder("Enter bet amount...").fill("10.00")
    page.get_by_placeholder("Enter bet amount...").press("Enter")
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("10.00");
    page.get_by_role("button", name="Clear").click()
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("0.00");

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
