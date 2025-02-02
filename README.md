# CS:GO Empire Roulette Web Tests
## Overview
This project contains automated web tests for the **Roulette page** on CS:GO Empire using **Python, Pytest, and Playwright**. The goal is to display examplles of validation of the functionality, usability, and reliability of key UI elements and user interactions across different environments.

### Key Features
- **Bet Input Field Validation:** Verifies correct input handling, including valid and invalid scenarios.
- **Bet Control Buttons Testing:** Ensures all bet adjustment and placement buttons function as expected.
- **Multi-Language Support:** Validates UI translations (English and Spanish with parameterized test: test_webpage_labels).
- **Cross-Browser Compatibility:** Tests can be executed on Chromium, Firefox, and WebKit using CLI options.

## Important notes for the Assessors (CSGOEmpire team):
> - **Test Сoverage**: This suite is not exhaustive. It showcases coding practices and testing approaches for the Skill Assessment, focusing specifically on the selected section of the Roulette page: bet input field, bet adjustment buttons, and the bet placement button.
> - **Authentication**: User login is not required, in accordance with the assessment guidelines.
> - **Security Consideration**: Tests may fail in **headless mode** due to Cloudflare’s human verification checks. No bypass mechanisms have been implemented in this project.
> - **Test Execution Strategy**: Tests are designed with reusability in mind, leveraging fixtures, parameterization, and a modular structure to facilitate easy expansion, maintenance, and CI/CD integration.
> - **Tests Structure**: All tests are currently written in a single test_ file. As the project scales, it’s recommended to organize tests into separate files and categories (e.g., UI, translations, logic, E2E) and implement tagging (e.g., smoke, regression) for better management. It heavily relies on the existing project structure and practices.
> - **Localization**: Language switching is implemented via **Local Storage Manipulation** for speed and simplicity. For comprehensive localization testing, additional UI-level verification should be implemented.

## Project Structure
- `tests/`: Test scripts
  - `test_roulette_page.py`: main test file for UI validation
- `pages/`: Page Object Model (POM) classes
  - `roulette_page.py`: Roulette page interactions
- `data/`: Test data in JSON format
  - `bet_input_field_valid.json`: valid input test cases
  - `bet_input_field_invalid.json`: invalid input test cases
  - `translations.json`: language support data
- `config.py`: Configuration settings (base url, languages)
- `conftest.py`: Pytest fixtures
- `locators.py`: Element locators
- `README.md`
- `utils.py`: Helper functions

## Installation
```sh
git clone https://github.com/your_repo/playwright-tests.git
cd playwright-tests
pip install -r requirements.txt
playwright install
```

## Running Tests
```sh
pytest -s               # Run all tests with logging
pytest --headed         # Run tests in headed mode
pytest --custom-browser chromium  # Run on a specific browser: chromium, firefox, webkit
```

## CI/CD Integration
For GitHub Actions, use the following command:
```yml
- name: Run Playwright Tests
  run: pytest --headless
```

## Reporting
To generate **Allure Report**:
```sh
pytest --alluredir=allure-results
allure serve allure-results
```

## License
This project is licensed under the GNU Affero General Public License v3.0.
