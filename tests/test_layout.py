import os
import pytest
from playwright.sync_api import Page, expect

def test_empty_lyrics_no_layout_change(page: Page):
    # Load the local index.html
    path = os.path.abspath("index.html")
    page.goto(f"file://{path}")

    # Ensure col1 and col2 are empty initially
    col1 = page.locator("#col1")
    col2 = page.locator("#col2")
    expect(col1).to_be_empty()
    expect(col2).to_be_empty()

    # Fill title but leave lyrics empty
    page.fill("#titleInput", "Test Title")
    page.click("text=🚀 產生排版")

    # Verify col1 and col2 are still empty
    # If the early return is working, these should remain empty.
    expect(col1).to_be_empty()
    expect(col2).to_be_empty()

def test_happy_path(page: Page):
    path = os.path.abspath("index.html")
    page.goto(f"file://{path}")

    page.fill("#titleInput", "Test Title")
    page.fill("#lyricsInput", "Line 1\nLine 2\nLine 3")
    page.click("text=🚀 產生排版")

    col1 = page.locator("#col1")
    expect(col1).not_to_be_empty()
    expect(col1).to_contain_text("Test Title")
    expect(col1).to_contain_text("Line 1")

    info = page.locator("#info")
    expect(info).to_contain_text("排版")
