# CS:GO Empire Roulette Web Tests
This project contains automated web tests for the CS:GO Empire Roulette page (https://csgoempire.com/roulette), written in Python using the Playwright framework. The purpose of these tests is showcase the automation of the Bet controls verification on the CS:GO Empire Roulette webpage as part of the Skill Assessement work. The project is structured into two main directories, `tests` and `tests_alternative`, to showcase different testing strategies.

## Important notest for the Assessors (CSGOEmpire team):
  - none of tests include user authothorisation, since the skill assessement stated that: "Creating an account and signing in is not required."
  - final test scripts ( `tests` folder) additionally unilise Pytest library, that allows to run the initial webpage check before each test.
  - all tests do Print intermediate test data to improve test execution visibility due to the nature of the test scripts execution (manual run in terminal), none of the Prints are nessesary and can be removed once the tests are integrated to any reporting systems
  - `test_roulette_pw.py` test script contain commented out 4 expectations in the test_input_field_check test, this was made on purpose to allow to showcase the full test executing without breaking it in the middle. In the real case scenario, they shouldn't be commented out: the test script should stop after the first failed expectation.
  - the main `test_input_field_check` and `test_input_controls_check` tests represent different approaches to structuring test data and actions (it depends on the accepted code practices for readability, maintainability which one should be maily used):
    - `test_input_field_check` - sequential execution
    - `test_input_controls_check` - loop execution

## Structure
The project is organised as follows:
- `tests`: contains the finalised tests.
  - `test_roulette_pw.py`: executes tests without using the pytest-check library, meaning it does not allow for soft assertions.
  - `test_roulette_pw_pytest-check.py`: the same test as `test_roulette_pw.py` but utilises the pytest-check library to enable soft assertions.
- `tests_alternative`: An alternative set of tests, do not require Assessors's attention.
  
## Installation
To run these tests, you need to have Python and Playwright installed in your environment. Follow these steps to set up:

1. **Clone the repository:**
git clone https://github.com/natalia-hh/playwright-tests.git
cd playwright-tests

2. **Install dependencies:**
Make sure you have Python installed, then use pip to install Playwright, Pytest and pytest-check (if you plan to use soft assertions):

pip install playwright pytest pytest-check


## Usage
To run the tests, navigate to the project directory and use the pytest command. You can run tests from a specific folder or run a specific test file. 
- **To run all tests in the `tests` folder:**
pytest tests/

- **To run a specific test file:**
pytest tests/test_roulette_pw.py

- **To display intermediate test data in terminal:**
pytest -s tests/test_roulette_pw.py


## License

This project is open-sourced under the GNU Affero General Public License v3.0 License. See the LICENSE file for more details.
