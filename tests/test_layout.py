import pytest
from playwright.sync_api import sync_playwright
import os

def test_layout_calculation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the local index.html
        abs_path = os.path.abspath("index.html")
        page.goto(f"file://{abs_path}")

        # Fill in title and lyrics
        page.fill("#titleInput", "Test Song")
        page.fill("#lyricsInput", "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nLine 8\nLine 9\nLine 10")

        # Click the generate button
        page.click("button:has-text('🚀 產生排版')")

        # Check if info text is updated
        info = page.inner_text("#info")
        assert "目前狀態" in info
        assert "歌詞字體" in info

        # Verify font size is within expected range
        import re
        match = re.search(r"(\d+)px", info)
        assert match
        font_size = int(match.group(1))
        assert 10 <= font_size <= 100

        browser.close()

if __name__ == "__main__":
    test_layout_calculation()
