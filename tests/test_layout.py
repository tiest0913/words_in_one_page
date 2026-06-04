import os
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    # Load the index.html file
    path = os.path.abspath("index.html")
    page.goto(f"file://{path}")
    yield page
    page.close()

def test_test_layout_direct(page):
    """Test the testLayout helper function directly."""
    # Define test data
    title = "Test Title"
    lines = ["Line 1", "Line 2", "Line 3", "Line 4"]

    # Run testLayout for single column
    page.evaluate("""([title, lines]) => {
        const col1 = document.getElementById('col1');
        const col2 = document.getElementById('col2');
        return testLayout(20, false, title, lines, col1, col2);
    }""", [title, lines])

    # Verify DOM state for single column
    col1_content = page.text_content("#col1")
    col2_content = page.text_content("#col2")
    assert title in col1_content
    assert "Line 1" in col1_content
    assert "Line 4" in col1_content
    assert col2_content == ""

    # Run testLayout for double column
    page.evaluate("""([title, lines]) => {
        const col1 = document.getElementById('col1');
        const col2 = document.getElementById('col2');
        return testLayout(20, true, title, lines, col1, col2);
    }""", [title, lines])

    # Verify DOM state for double column
    col1_content = page.text_content("#col1")
    col2_content = page.text_content("#col2")
    assert title in col1_content
    assert "Line 1" in col1_content
    assert "Line 2" in col1_content
    assert "Line 3" in col2_content
    assert "Line 4" in col2_content

def test_calculate_layout_single_column(page):
    """Test E2E layout calculation for single column."""
    page.fill("#titleInput", "Small Song")
    page.fill("#lyricsInput", "Line 1\nLine 2\nLine 3")
    page.click("#calculateBtn")

    info_text = page.text_content("#info")
    assert "單欄排版" in info_text

    col1_content = page.text_content("#col1")
    assert "Small Song" in col1_content
    assert "Line 1" in col1_content
    assert page.text_content("#col2") == ""

def test_calculate_layout_double_column(page):
    """Test E2E layout calculation for double column."""
    # Use many lines to force double column
    lyrics = "\n".join([f"Line {i}" for i in range(1, 100)])
    page.fill("#titleInput", "Long Song")
    page.fill("#lyricsInput", lyrics)
    page.click("#calculateBtn")

    info_text = page.text_content("#info")
    # It should favor double column if it allows for significantly larger font
    # or if single column just doesn't fit (which is likely here)
    assert "排版" in info_text

    col1_content = page.text_content("#col1")
    col2_content = page.text_content("#col2")
    assert "Long Song" in col1_content
    assert col1_content != ""
    assert col2_content != ""

def test_empty_lyrics_early_return(page):
    """Test that the function returns early if lyrics are empty."""
    page.fill("#titleInput", "No Lyrics")
    page.fill("#lyricsInput", "")
    page.click("#calculateBtn")

    assert page.text_content("#info") == ""
    assert page.text_content("#col1") == ""
    assert page.text_content("#col2") == ""
