import pytest
from playwright.sync_api import sync_playwright
import os
import re

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    path = os.path.abspath("index.html")
    page.goto(f"file://{path}")
    yield page
    page.close()

def test_initial_state(page):
    """Verify the initial state of the application."""
    info = page.inner_text("#info")
    assert info == ""
    assert page.inner_text("#col1") == ""
    assert page.inner_text("#col2") == ""

def test_calculate_layout_basic(page):
    """Test layout calculation with basic lyrics."""
    page.fill("#titleInput", "Test Song")
    page.fill("#lyricsInput", "Line 1\nLine 2\nLine 3")
    page.click("button:has-text('🚀 產生排版')")

    info = page.inner_text("#info")
    assert "單欄" in info or "雙欄" in info
    assert "歌詞字體" in info

    col1_content = page.inner_html("#col1")
    assert "Test Song" in col1_content
    assert "Line 1" in col1_content
    assert 'class="lyrics-title"' in col1_content

def test_empty_lyrics_does_nothing(page):
    """Verify that clicking the button with empty lyrics does not change the state."""
    page.fill("#titleInput", "Test Song")
    page.fill("#lyricsInput", "")
    page.click("button:has-text('🚀 產生排版')")

    info = page.inner_text("#info")
    assert info == ""
    assert page.inner_text("#col1") == ""

def test_font_size_limit(page):
    """Verify that font size is within the expected range (10-100)."""
    page.fill("#titleInput", "Small")
    page.fill("#lyricsInput", "Short")
    page.click("button:has-text('🚀 產生排版')")

    info = page.inner_text("#info")
    match = re.search(r"歌詞字體: (\d+)px", info)
    assert match
    font_size = int(match.group(1))
    assert 10 <= font_size <= 100

def test_layout_switching(page):
    """Verify that the layout can switch between single and double column."""
    # Short lyrics should be single column
    page.fill("#titleInput", "Short Song")
    page.fill("#lyricsInput", "Line 1\nLine 2")
    page.click("button:has-text('🚀 產生排版')")
    assert "單欄" in page.inner_text("#info")
    assert page.inner_text("#col2") == ""

    # Long lyrics should trigger double column
    # Use many lines to ensure it doesn't fit in one column easily
    long_lyrics = "\n".join([f"Line {i}" for i in range(1, 100)])
    page.fill("#titleInput", "Long Song")
    page.fill("#lyricsInput", long_lyrics)
    page.click("button:has-text('🚀 產生排版')")

    info = page.inner_text("#info")
    assert "雙欄" in info
    col2_content = page.inner_text("#col2")
    assert len(col2_content.strip()) > 0

def test_title_font_size_logic(page):
    """Verify the title font size is font_size + 5."""
    page.fill("#titleInput", "Title")
    page.fill("#lyricsInput", "Lyrics")
    page.click("button:has-text('🚀 產生排版')")

    info = page.inner_text("#info")
    match = re.search(r"歌詞字體: (\d+)px", info)
    assert match
    font_size = int(match.group(1))

    title_element = page.query_selector(".lyrics-title")
    title_style = title_element.get_attribute("style")
    assert f"font-size:{font_size+5}px" in title_style.replace(" ", "")
