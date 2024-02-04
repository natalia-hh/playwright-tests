# This is an alternative version of the test that:
# runs test_webpage_check as a serapate test instead of executing it before each test

import re
from playwright.sync_api import expect, Playwright, sync_playwright

def test_webpage_check(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    # verify that CSGO/Roulette/'Enter bet amount...' presented and 'Page not found' is not visible
    page.goto('https://csgoempire.com/roulette',wait_until='load')
    expect(page).to_have_title(re.compile('CSGOEmpire'))
    expect(page.get_by_role('heading', name='Page not found')).not_to_be_visible()
    expect(page.get_by_role('heading', name='Roulette')).to_be_visible()
    expect(page.get_by_placeholder('Enter bet amount...')).to_be_visible()
    print('CHECK: Webpage initial check')
    context.close()
    browser.close()
with sync_playwright() as playwright:
    test_webpage_check(playwright)

def test_allcontrols_initial_check(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://csgoempire.com/roulette")
    
    # Verify that all required elememts (input field and all input controls) are visible:
    expect(page.get_by_placeholder("Enter bet amount...")).to_be_visible()
    print('CHECK: Input field is visible')
    control_button_names = ['Clear','+ 0.01','+ 0.1','+ 1','+ 10','+ 100','1/ 2','x 2','Max']
    for x in control_button_names:
        expect(page.get_by_role("button", name=x, exact=True)).to_be_visible()
        print('CHECK: Input Controls button is visible: ', x)

    # Verify that there is an exact number of input controls (9):
    expect(page.locator('.bet-input__controls-inner.-ml-md button')).to_have_count(9) #not nice locating solution
    print('CHECK: Input field and 9 controls found')
    context.close()
    browser.close()
with sync_playwright() as playwright:
    test_allcontrols_initial_check(playwright)
 
def test_input_field_check(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://csgoempire.com/roulette")
    # Data cases for Input Field - Positives
    # ..null
    expect(page.get_by_placeholder("Enter bet amount...")).to_be_empty()
    page.get_by_placeholder("Enter bet amount...").click()
    page.click('body')
    print('CHECK: Null => ', page.get_by_placeholder("Enter bet amount...").input_value())
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("0.00")
    # ..empty
    page.get_by_placeholder("Enter bet amount...").fill("")
    page.click('body')
    print('CHECK: Empty => ', page.get_by_placeholder("Enter bet amount...").input_value())
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("0.00")
    # ..no decimals
    page.get_by_placeholder("Enter bet amount...").fill("10")
    page.click('body')
    print('CHECK: no decimals => ', page.get_by_placeholder("Enter bet amount...").input_value())
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("10.00")
    # ..with descimals
    page.get_by_placeholder("Enter bet amount...").fill("10.00")
    page.click('body')
    print('CHECK: with decimals => ', page.get_by_placeholder("Enter bet amount...").input_value())
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("10.00")
    # ..comma separator
    page.get_by_placeholder("Enter bet amount...").fill("10,00")
    page.click('body')
    print('CHECK: commma separator => ',page.get_by_placeholder("Enter bet amount...").input_value())
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("10.00")
    # ..rounded
    page.get_by_placeholder("Enter bet amount...").fill("10.006")
    page.click('body')
    print('CHECK: Rounded => ', page.get_by_placeholder("Enter bet amount...").input_value())
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("10.01")
    # ..big number
    page.get_by_placeholder("Enter bet amount...").fill("1000000000000000005")
    page.click('body')
    print('CHECK: Big number => ', page.get_by_placeholder("Enter bet amount...").input_value())
  # expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("1000000000000000005.00")
    # Data cases for Input Field - Negatives
    # ..negavite value
    page.get_by_placeholder("Enter bet amount...").fill("-10.00")
    page.click('body')
    print('CHECK: Negative value => ', page.get_by_placeholder("Enter bet amount...").input_value())
  # expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("0.00")
    # ..text
    page.get_by_placeholder("Enter bet amount...").fill("Text")
    page.click('body')
    print('CHECK: Text => ', page.get_by_placeholder("Enter bet amount...").input_value())
  #  expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("0.00")
    # ..with symbols
    page.get_by_placeholder("Enter bet amount...").fill("10.0±!@#$%^*")
    page.click('body')
    print('CHECK: With symbols => ', page.get_by_placeholder("Enter bet amount...").input_value())
  #  expect(page.get_by_placeholder("Enter bet amount...")).to_have_value("0.00")
    context.close()
    browser.close()
with sync_playwright() as playwright:
    test_input_field_check(playwright)

def test_input_controls_check(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://csgoempire.com/roulette")
    # Data cases for Input Controls (buttons)
    input_value = 1.00
    control_button_names = ['Clear','+ 0.01','+ 0.1','+ 1','+ 10','+ 100','1/ 2','x 2','Max']
    
    # ..Scenario 1 - positive check
    calculated_input_value = [0,input_value+0.01,input_value+0.1,input_value+1,input_value+10,input_value+100,input_value/2,input_value*2,input_value]
    for x in control_button_names:
        page.reload()
        page.get_by_placeholder("Enter bet amount...").fill(str(input_value))
        expect(page.get_by_placeholder("Enter bet amount...")).to_have_value(str(input_value))
        page.get_by_role("button", name=x, exact=True).click()
        expected_value = '%.2f' % calculated_input_value[control_button_names.index(x)]
        print('CHECK: Entered:', '%.2f' % input_value,'Clicked Button=',x, 'Exp Result=','%.2f' % calculated_input_value[control_button_names.index(x)])
        expect(page.get_by_placeholder("Enter bet amount...")).to_have_value(expected_value)
        
    # ..Scenario 2 - all controls used, except Clear and Max
    page.reload()
    page.get_by_placeholder("Enter bet amount...").fill(str(input_value))
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value(str(input_value))
    for x in control_button_names[1:8]: # this excludes Clear and Max buttons
        page.get_by_role("button", name=x, exact=True).click()
    expected_calc_value = '%.2f' % (input_value+0.01+0.1+1+10+100)
    print('CHECK: Entered:', '%.2f' % input_value,'Clicked All buttons', 'Exp Result=','%.2f' % (input_value+0.01+0.1+1+10+100))
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value(expected_calc_value)

    # ..Scenario 3 - each control clicked multiple times
    # <not implemented>
    # ..Scenario 4 - combinations with Input field
    # <not implemented>
    context.close()
    browser.close()
with sync_playwright() as playwright:
    test_input_controls_check(playwright)
