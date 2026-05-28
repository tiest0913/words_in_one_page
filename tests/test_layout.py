import os
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        browser.close()

def load_page(context):
    page = context.new_page()
    path = os.path.abspath("index.html")
    page.goto(f"file://{path}")
    return page

def test_empty_lyrics(browser_context):
    page = load_page(browser_context)
    page.fill("#titleInput", "Empty Song")
    page.fill("#lyricsInput", "")
    page.click("button:has-text('🚀 產生排版')")

    # Info should not be updated if lyrics are empty
    info_text = page.inner_text("#info")
    assert info_text == ""
    page.close()

def test_single_column_layout(browser_context):
    page = load_page(browser_context)
    page.fill("#titleInput", "Short Song")
    # A few lines should fit in a single column with a large font
    page.fill("#lyricsInput", "Line 1\nLine 2\nLine 3")
    page.click("button:has-text('🚀 產生排版')")

    info_text = page.inner_text("#info")
    assert "單欄排版" in info_text
    # Check if title is present in col1
    assert page.locator("#col1 .lyrics-title").text_content() == "Short Song"
    # col2 should be empty
    assert page.inner_text("#col2") == ""
    page.close()

def test_double_column_layout(browser_context):
    page = load_page(browser_context)
    page.fill("#titleInput", "Long Song")
    # Many lines to force double column or at least test it
    # We'll use 50 lines to make sure it's long
    long_lyrics = "\n".join([f"Lyric Line {i}" for i in range(1, 61)])
    page.fill("#lyricsInput", long_lyrics)
    page.click("button:has-text('🚀 產生排版')")

    info_text = page.inner_text("#info")
    # For 60 lines, it's very likely to use double column to get a better font size
    # unless the font size difference is less than 4px, but with 60 lines,
    # single column would have very small font.
    assert "雙欄排版" in info_text

    # col1 and col2 should both have content
    assert page.inner_text("#col1") != ""
    assert page.inner_text("#col2") != ""
    page.close()

def test_xss_protection(browser_context):
    page = load_page(browser_context)
    page.fill("#titleInput", "<img src=x onerror=alert(1)>")
    page.fill("#lyricsInput", "Normal Line")
    page.click("button:has-text('🚀 產生排版')")

    # If textContent/replaceChildren is used, the title should be exactly the input string
    title_element = page.locator("#col1 .lyrics-title")
    assert title_element.text_content() == "<img src=x onerror=alert(1)>"

    # Ensure no img element was created
    assert page.locator("#col1 .lyrics-title img").count() == 0
    page.close()

def test_very_long_title(browser_context):
    page = load_page(browser_context)
    long_title = "A" * 1000
    page.fill("#titleInput", long_title)
    page.fill("#lyricsInput", "Short lyrics")
    page.click("button:has-text('🚀 產生排版')")

    assert page.locator("#col1 .lyrics-title").text_content() == long_title
    page.close()
