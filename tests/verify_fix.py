import os
import pytest
from playwright.sync_api import Page, expect

def test_title_rendering(page: Page):
    # Get the absolute path to index.html
    current_dir = os.getcwd()
    file_path = f"file://{current_dir}/index.html"

    page.goto(file_path)

    # Fill in title and lyrics
    title = "Test Song Title"
    lyrics = "Line 1\nLine 2\nLine 3\nLine 4"

    page.fill("#titleInput", title)
    page.fill("#lyricsInput", lyrics)

    # Click the generate button
    page.click("button:has-text('產生排版')")

    # Verify title in col1
    col1_title = page.locator("#col1 .lyrics-title")
    expect(col1_title).to_have_text(title)

    # Change to a longer lyrics to potentially trigger double column or just verify it's still there
    # The logic for double column depends on font size fitting.
    # Let's just verify it works with some input.

    # Check if font size is applied (it should be fontSize + 5)
    # Since we don't know the exact fontSize calculated, we just check if it exists and has some size.
    font_size = col1_title.evaluate("el => el.style.fontSize")
    assert font_size.endswith("px")
    assert int(font_size.replace("px", "")) > 5

def test_double_column_title(page: Page):
    current_dir = os.getcwd()
    file_path = f"file://{current_dir}/index.html"

    page.goto(file_path)

    title = "Double Column Title"
    # Use many lines to encourage double column
    lyrics = "\n".join([f"Line {i}" for i in range(1, 50)])

    page.fill("#titleInput", title)
    page.fill("#lyricsInput", lyrics)

    page.click("button:has-text('產生排版')")

    # Verify title in col1 even in double column
    col1_title = page.locator("#col1 .lyrics-title")
    expect(col1_title).to_have_text(title)

    # Check the 'info' text to see if it says '雙欄'
    info = page.locator("#info")
    expect(info).to_contain_text("雙欄")
