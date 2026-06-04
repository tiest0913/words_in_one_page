import pytest
from playwright.sync_api import sync_playwright
import os

def test_empty_lyrics_no_change():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Get absolute path to index.html
        path = os.path.abspath("index.html")
        page.goto(f"file://{path}")

        # Set a title but keep lyrics empty
        page.fill("#titleInput", "Test Title")
        page.fill("#lyricsInput", "")

        # Verify initial state
        col1 = page.locator("#col1")
        col2 = page.locator("#col2")
        assert col1.inner_html() == ""
        assert col2.inner_html() == ""

        # Click the generate button
        page.get_by_role("button", name="🚀 產生排版").click()

        # Verify that the columns remain empty
        assert col1.inner_html() == ""
        assert col2.inner_html() == ""

        browser.close()
