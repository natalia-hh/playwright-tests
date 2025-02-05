# 🎯 CS:GO Empire Roulette Automated Tests
## 📋 Overview
This project contains automated web tests for the **Roulette page** on CS:GO Empire using **Python, Pytest, and Playwright**. The goal is to demonstrate examples of validating the functionality, usability, and reliability of key UI elements and user interactions across different browsers.

### 🚀 Key Features
- **Bet Input Field Validation:** Verifies correct input handling, including valid and invalid scenarios.
- **Bet Control Buttons Testing:** Ensures all bet adjustment and placement buttons function as expected.
- **Multi-Language Support:** Validates UI translations (English and Spanish by parameterized tests).
- **Cross-Browser Compatibility:** Tests can be executed on Chromium, Firefox, and WebKit using CLI options.

## ❗️ Important Notes for Assessors (CSGOEmpire Team)
> - **Test Сoverage**: This suite is not exhaustive. It showcases coding practices and testing approaches for the Skill Assessment, focusing specifically on the selected section of the Roulette page: bet input field, bet adjustment buttons, and the bet placement button.
> - **Authentication**: User login is not required, in accordance with the assessment guidelines.
> - **Security Consideration**: Tests may fail in **headless mode** due to Cloudflare’s human verification checks. No bypass mechanisms have been implemented in this project.
> - **Test Execution Strategy**: Tests are designed with reusability in mind, leveraging fixtures, parameterization, and a modular structure to facilitate easy expansion, maintenance, and CI/CD integration.
> - **Tests Structure**: Tests are organized into separate files based on categories (e.g., UI, translations, logic, E2E) with tagging (`smoke`, `regression`) for efficient management. Keep in mind that this organization is for demonstration purposes only and typically depends on the existing project structure and practices.
> - **Localization**: Language switching is implemented via **Local Storage Manipulation** for speed and simplicity. For comprehensive localization testing, additional UI-level verification should be implemented.

## 🗂️ Project Structure
```plaintext
├── tests/                           # Test scripts
│   ├── test_roulette_health.py       # Health check for Roulette page
│   ├── test_roulette_logic.py        # Tests for betting logic and calculations
│   ├── test_roulette_translations.py # UI translations validation
│   └── test_roulette_ui.py           # Visual and UI interaction tests
│
├── pages/                           # Page Object Model (POM) classes
│   ├── __init__.py                   # Marks the directory as a Python package
│   ├── base_page.py                  # Base class with common page actions
│   └── roulette_page.py              # POM for Roulette page interactions
│
├── data/                            # Test data
│   ├── bet_input_field_valid.json    # Valid bet input test cases
│   ├── bet_input_field_invalid.json  # Invalid bet input test cases
│   ├── translations.json             # Language translation data
│   └── /images                       # Screenshots for visual tests
│       └── bet_input_icon.png        # Baseline image for icon comparison
│
├── config.py                        # Configuration settings (base URL, languages)
├── conftest.py                      # Pytest fixtures
├── locators.py                      # Element locators for UI tests
├── utils.py                         # Utility functions for tests
├── requirements.txt                 # Project dependencies
├── .gitignore                       # Specifies files/folders to ignore in Git
└── README.md                        # Project documentation
```

## Installation
```sh
git clone https://github.com/your_repo/playwright-tests.git -b code-level-up
cd playwright-tests
pip install -r requirements.txt
playwright install
```

## Running Tests
```sh
pytest -s               # Run all tests with console logging enabled
pytest --headed         # Run tests in headed mode (with visible browser UI)
pytest --custom-browser chromium  # Run on a specific browser: chromium, firefox, webkit
pytest -m smoke         # Run by a specific marker: smoke, regression
```
Note: The `--custom-browser` option is a custom CLI argument added to avoid conflicts with Playwright's VSCode Plugin `--browser` parameter.

## Reporting
To generate **Allure Report**:
```sh
pytest --alluredir=test-results/allure-results
allure serve test-results/allure-results
```

## CI/CD Integration

### 🚀 GitHub Actions Example

To run Playwright tests in a GitHub Actions workflow, use the following configuration:

```yml
name: Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          playwright install

      - name: Run Playwright Tests
        run: pytest --headless --custom-browser=chromium -m smoke
```

## License
This project is licensed under the GNU Affero General Public License v3.0.
