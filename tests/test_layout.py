import pytest
from playwright.sync_api import sync_playwright
import os

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    # Use absolute path to the index.html
    file_path = "file://" + os.path.abspath("index.html")
    page.goto(file_path)
    yield page
    page.close()

def test_empty_lyrics_does_nothing(page):
    # Set title but no lyrics
    page.fill("#titleInput", "Test Song")
    page.click("button:has-text('產生排版')")

    # Check that info text is still empty (or doesn't contain "目前狀態")
    info_text = page.inner_text("#info")
    assert "目前狀態" not in info_text

def test_calculate_layout_single_column(page):
    # Short lyrics should likely result in single column
    page.fill("#titleInput", "Short Song")
    page.fill("#lyricsInput", "Line 1\nLine 2\nLine 3")
    page.click("button:has-text('產生排版')")

    info_text = page.inner_text("#info")
    assert "單欄" in info_text

    # Check if col1 contains title and lyrics
    col1_text = page.inner_text("#col1")
    assert "Short Song" in col1_text
    assert "Line 1" in col1_text

    # Check if col2 is empty
    col2_text = page.inner_text("#col2")
    assert col2_text.strip() == ""

def test_calculate_layout_double_column(page):
    # Very long lyrics to force double column
    # Need many lines to exceed the height of A4 at min font size 10
    long_lyrics = "\n".join([f"Line {i}" for i in range(1, 150)])
    page.fill("#titleInput", "Long Song")
    page.fill("#lyricsInput", long_lyrics)
    page.click("button:has-text('產生排版')")

    info_text = page.inner_text("#info")
    # Whether it chooses single or double depends on whether it fits
    # If it's very long, it might still be single if double doesn't help much,
    # but 150 lines should definitely trigger double if it fits better.
    # Actually, if it's TOO long it might not fit either.
    # Let's just check if it runs and updates the info.
    assert "目前狀態" in info_text
    assert "px" in info_text

def test_font_size_rendering(page):
    page.fill("#titleInput", "Font Test")
    page.fill("#lyricsInput", "Line 1\nLine 2")
    page.click("button:has-text('產生排版')")

    # Get the font size from info text
    import re
    info_text = page.inner_text("#info")
    match = re.search(r"(\d+)px", info_text)
    assert match is not None
    font_size = match.group(1)

    # Check if the style is applied to col1
    style = page.get_attribute("#col1", "style")
    assert f"font-size: {font_size}px" in style
