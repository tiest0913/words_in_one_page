import pytest
import os
from playwright.sync_api import Page, expect

# We use the built-in 'page' fixture provided by pytest-playwright

@pytest.fixture(autouse=True)
def setup(page: Page):
    # Get absolute path to index.html
    path = os.path.abspath("index.html")
    page.goto(f"file://{path}")

def test_basic_layout_generation(page: Page):
    """Test that filling title and lyrics and clicking generate updates the info display."""
    page.fill("#titleInput", "Test Song")
    page.fill("#lyricsInput", "Line 1\nLine 2\nLine 3")
    page.click("#calculateBtn")

    # Check if info text is updated
    expect(page.locator("#info")).to_contain_text("目前狀態")
    expect(page.locator("#info")).to_contain_text("歌詞字體")

    # Check if title is rendered in col1
    expect(page.locator("#col1")).to_contain_text("Test Song")
    expect(page.locator("#col1")).to_contain_text("Line 1")

def test_empty_lyrics_handling(page: Page):
    """Test that clicking generate with empty lyrics does not update the info display."""
    page.fill("#titleInput", "Test Song")
    page.fill("#lyricsInput", "")
    page.click("#calculateBtn")

    expect(page.locator("#info")).to_have_text("")

def test_single_column_layout(page: Page):
    """Test that short lyrics result in a single column layout."""
    page.fill("#titleInput", "Short Song")
    page.fill("#lyricsInput", "Only one line")
    page.click("#calculateBtn")

    expect(page.locator("#info")).to_contain_text("單欄")
    expect(page.locator("#col2")).to_have_text("")

def test_double_column_layout(page: Page):
    """Test that long lyrics result in a double column layout."""
    page.fill("#titleInput", "Long Song")
    # Generate 100 lines of lyrics to ensure it triggers double column
    long_lyrics = "\n".join([f"Line {i}" for i in range(1, 101)])
    page.fill("#lyricsInput", long_lyrics)
    page.click("#calculateBtn")

    expect(page.locator("#info")).to_contain_text("雙欄")
    # Should be split into two columns
    expect(page.locator("#col2")).not_to_have_text("")

def test_print_button_triggers_window_print(page: Page):
    """Test that clicking the print button triggers window.print."""
    # Mock window.print
    page.evaluate("window.print = () => { window.printCalled = true; }")

    page.click("#printBtn")

    print_called = page.evaluate("window.printCalled")
    assert print_called is True
