# Playwright Automation Practice Tests

This project automates the Rahul Shetty Automation Practice page with Python,
pytest, and Playwright.

Target page:

```text
https://rahulshettyacademy.com/AutomationPractice/
```

## Scenario Coverage

- 10 positive scenarios
- 10 negative scenarios
- 5 edge cases

## Run

```bash
.venv/bin/python -m pytest
```

Or run the helper script:

```bash
.venv/bin/python main.py
```

The tests run in a visible Chromium browser with a small delay between actions.
An HTML report is generated at:

```text
reports/automation-practice-report.html
```
