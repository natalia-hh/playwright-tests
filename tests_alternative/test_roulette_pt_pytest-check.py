# This is an alternative version of the test that:
# doesn't utilise Playwright class
# utilise pytest_check library for soft assertions

import re
from playwright.sync_api import expect, Page
from pytest_check import check

def test_webpage_check(page: Page):
    # Verify that the page is loaded, 'Page not found' is not displayed:
    page.goto('https://csgoempire.com/roulette',wait_until='load')
    expect(page).to_have_title(re.compile("CSGOEmpire"))
    expect(page.get_by_role("heading", name="Page not found")).to_be_hidden()
    print('CHECK: Webpage initial check')

def test_allcontrols_initial_check(page: Page) -> None:
    page.goto("https://csgoempire.com/roulette")
    
    # Verify that all required elememts (input field and all input controls) are visible:
    expect(page.get_by_placeholder("Enter bet amount...")).to_be_visible()
    print('CHECK: Input field is visible')

    control_button_names = ['Clear','+ 0.01','+ 0.1','+ 1','+ 10','+ 100','1/ 2','x 2','Max']
    for x in control_button_names:
        expect(page.get_by_role("button", name=x, exact=True)).to_be_visible()
        print('CHECK: Input Controls button is visible: ', x)

    # Verify that there are no more input controls than expected (9):
    check.equal(page.locator('.bet-input__controls-inner.-ml-md button').count(), 9, 'FALSE for controls amount')
    print('CHECK: Input field and 9 controls found')
 
def test_input_field_check(page: Page) -> None:
    page.goto("https://csgoempire.com/roulette")
    # Positives
    #null
    expect(page.get_by_placeholder("Enter bet amount...")).to_be_empty()
    page.get_by_placeholder("Enter bet amount...").click()
    page.click('body')
    print('CHECK: Null => ', page.get_by_placeholder("Enter bet amount...").input_value())
    check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), '0.00','FALSE for null')
    #empty
    page.get_by_placeholder("Enter bet amount...").fill("")
    page.click('body')
    print('CHECK: Empty => ', page.get_by_placeholder("Enter bet amount...").input_value())
    check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), '0.00','FALSE for empty')
    #no decimals
    page.get_by_placeholder("Enter bet amount...").fill("10")
    page.click('body')
    print('CHECK: no decimals => ', page.get_by_placeholder("Enter bet amount...").input_value())
    check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), '10.00','FALSE for no decimals')
    #with descimals
    page.get_by_placeholder("Enter bet amount...").fill("10.00")
    page.click('body')
    print('CHECK: with decimals => ', page.get_by_placeholder("Enter bet amount...").input_value())
    check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), '10.00','FALSE for with decimals')
    #comma separator
    page.get_by_placeholder("Enter bet amount...").fill("10,00")
    page.click('body')
    print('CHECK: commma separator => ',page.get_by_placeholder("Enter bet amount...").input_value())
    check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), '10.00','FALSE for comma')
    #rounded
    page.get_by_placeholder("Enter bet amount...").fill("10.006")
    page.click('body')
    print('CHECK: Rounded => ', page.get_by_placeholder("Enter bet amount...").input_value())
    check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), '10.01','FALSE for rounded')
    #big number
    page.get_by_placeholder("Enter bet amount...").fill("1000000000000000005")
    page.click('body')
    print('CHECK: Big number => ', page.get_by_placeholder("Enter bet amount...").input_value())
    check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), '1000000000000000005.05','FALSE for big number')
    # Negatives
    #negavite value
    page.get_by_placeholder("Enter bet amount...").fill("-10.00")
    page.click('body')
    print('CHECK: Negative value => ', page.get_by_placeholder("Enter bet amount...").input_value())
    check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), '0.00','FALSE for negative value')
    #text
    page.get_by_placeholder("Enter bet amount...").fill("Text")
    page.click('body')
    print('CHECK: Text => ', page.get_by_placeholder("Enter bet amount...").input_value())
    check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), '0.00','FALSE for text')
    #with symbols
    page.get_by_placeholder("Enter bet amount...").fill("10.0±!@#$%^*")
    page.click('body')
    print('CHECK: With symbols => ', page.get_by_placeholder("Enter bet amount...").input_value())
    check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), '0.00','FALSE for symbols')

def test_input_controls_check(page: Page) -> None:
    page.goto("https://csgoempire.com/roulette")
    control_button_names = ['Clear','+ 0.01','+ 0.1','+ 1','+ 10','+ 100','1/ 2','x 2','Max']
    input_value = 1.00

    # Scenario 1 - positive check
    calculated_input_value = [0,input_value+0.01,input_value+0.1,input_value+1,input_value+10,input_value+100,input_value/2,input_value*2,input_value]
    for x in control_button_names:
        page.reload()
        page.get_by_placeholder("Enter bet amount...").fill(str(input_value))
        expect(page.get_by_placeholder("Enter bet amount...")).to_have_value(str(input_value))
        page.get_by_role("button", name=x, exact=True).click()
        expected_value = '%.2f' % calculated_input_value[control_button_names.index(x)]
        print('CHECK: Entered:', '%.2f' % input_value,'Clicked Button=',x, 'Exp Result=','%.2f' % calculated_input_value[control_button_names.index(x)])
        check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), expected_value, 'FALSE for button'+ x)
        
    # Scenario 2 - all controls used, except Clear and Max
    page.reload()
    page.get_by_placeholder("Enter bet amount...").fill(str(input_value))
    expect(page.get_by_placeholder("Enter bet amount...")).to_have_value(str(input_value))
    for x in control_button_names[1:8]: # this excludes Clear and Max buttons
        page.get_by_role("button", name=x, exact=True).click()
    expected_calc_value = '%.2f' % (input_value+0.01+0.1+1+10+100)
    print('CHECK: Entered:', '%.2f' % input_value,'Clicked All buttons', 'Exp Result=','%.2f' % (input_value+0.01+0.1+1+10+100))
    check.equal(page.get_by_placeholder("Enter bet amount...").input_value(), expected_calc_value, 'FALSE')

    # Scenario 3 - each control clicked multiple times
    #<not implemented>
    
    
    # Scenario 4 - combinations with Input field
     #<not implemented>


