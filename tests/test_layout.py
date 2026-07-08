import os
import pathlib
import pytest
import re
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    path = pathlib.Path("index.html").absolute()
    page.goto(path.as_uri())

def test_empty_lyrics(page: Page):
    page.fill("#titleInput", "Test Title")
    page.click("#calculateBtn")
    # If lyrics are empty, the function returns early and info is not updated.
    # Initially info is empty.
    expect(page.locator("#info")).to_be_empty()

def test_single_column_layout(page: Page):
    page.fill("#titleInput", "Short Song")
    page.fill("#lyricsInput", "Line 1\nLine 2\nLine 3")
    page.click("#calculateBtn")

    expect(page.locator("#info")).to_contain_text("單欄排版")
    expect(page.locator("#col1")).to_contain_text("Short Song")
    expect(page.locator("#col1")).to_contain_text("Line 1")
    expect(page.locator("#col2")).to_be_empty()

def test_double_column_layout(page: Page):
    page.fill("#titleInput", "Long Song")
    # Generate many lines to force double column
    lyrics = "\n".join([f"Line {i}" for i in range(1, 100)])
    page.fill("#lyricsInput", lyrics)
    page.click("#calculateBtn")

    # Check if col2 is not empty
    expect(page.locator("#col2")).not_to_be_empty()
    expect(page.locator("#info")).to_contain_text("雙欄排版")

def test_font_size_calculation(page: Page):
    page.fill("#titleInput", "Font Size Test")
    page.fill("#lyricsInput", "Just a few lines")
    page.click("#calculateBtn")

    info_text = page.locator("#info").inner_text()
    assert "歌詞字體" in info_text

    match = re.search(r"(\d+)px", info_text)
    assert match is not None
    font_size = int(match.group(1))
    assert 10 <= font_size <= 100

    # Check if the style is actually applied
    col1_font_size = page.evaluate("window.getComputedStyle(document.getElementById('col1')).fontSize")
    assert col1_font_size == f"{font_size}px"
