from collections.abc import Iterator

import pytest
from playwright.sync_api import Browser, Page, sync_playwright


BASE_URL = "https://rahulshettyacademy.com/AutomationPractice/"


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=500)
        yield browser
        browser.close()


@pytest.fixture()
def page(browser: Browser) -> Iterator[Page]:
    context = browser.new_context(viewport={"width": 1366, "height": 768})
    page = context.new_page()
    page.goto(BASE_URL, wait_until="domcontentloaded")
    yield page
    page.wait_for_timeout(1000)
    context.close()
