# CS:GO Empire Roulette Web Tests
This project contains automated web tests for the Roulette page on CS:GO Empire, using Python and Playwright framework. It was designed to verify the Bet Input field and Bet Controls functionality as part of a **Skill Assessment for the CSGOEmpire team**.

[!IMPORTANT]
## Important notes for the Assessors (CSGOEmpire team):
- **Test coverage**: the tests aren't exhaustive. They aim to showcase coding techniques for the Skill Assessment, completed under the tight schedule and without prior knowledge of the Playwright framework.
- **No Authentication**: following assessment guidelines, no user login is required for these tests.
- **Pytest Integration**: test scripts in `tests` folder utilise Pytest library to perform an initial webpage check before each test. See tests scrips in `tests_alternative` folder for an atlernative version, where no Pytest library is used.
- **Output Visibility**: tests are designed to print intermediate results to terminal for clarity during manual execution. These prints are optional and can be omitted once integrated with a test execution reporting system.
- **Test Execution Strategy**: the `test_roulette_pw.py` test script includes intentionally commented expectations within `test_input_field_check` test to enable full test runs for the demonstration.
- **Test Code Structure**: there is an illustration of two approaches in the code structure (it depends on the accepted code practices insuring readability and maintainability which one should be used in a real-life scenario):
    - Sequential execution in `test_input_field_check`.
    - Loop-based execution in `test_input_controls_check`.

## Project Structure
- `tests`: final test scripts
  - `test_roulette_pw.py`: tests scripts without using the pytest-check library, meaning it does not allow for soft assertions.
  - `test_roulette_pw_pytest-check.py`: the same test as `test_roulette_pw.py` but utilises the pytest-check library allowing soft assertions.
- `tests_alternative`: additional tests for internal use.

## Installation
To run these tests, you need to have Python and Playwright installed in your environment. Follow these steps to set up:

### 1. **Clone the repository:**
```Shell
git clone https://github.com/natalia-hh/playwright-tests.git
cd playwright-tests
```

### 2. **Install required packages:**
Make sure you have Python installed, then use pip to install Playwright, Pytest and pytest-check (if you plan to run `test_roulette_pw_pytest-check.py` with soft assertions):
```Shell
pip install playwright pytest pytest-check
```

## Execution
To run the tests, navigate to the project directory and use the pytest command. You can run tests from a specific folder or run a specific test file. 
- **To run all tests in the `tests` folder:**
```Shell
pytest tests/
```

- **To run a specific test file:**
```Shell
pytest tests/test_roulette_pw.py
```

- **To view intermediate test data in terminal, include -s:**
```Shell
pytest -s tests/test_roulette_pw.py
```

## License
This project is licensed under the GNU Affero General Public License v3.0 License. See the LICENSE file for more details.
