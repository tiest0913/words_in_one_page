import os
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    path = os.path.abspath('index.html')
    page.goto(f'file://{path}')
    yield page
    page.close()

def test_happy_path(page):
    # Set title and lyrics
    page.fill('#titleInput', 'Test Song')
    page.fill('#lyricsInput', 'Line 1\nLine 2\nLine 3\nLine 4')

    # Click the generate button
    page.click('button:has-text("🚀 產生排版")')

    # Check if info text is updated
    info_text = page.inner_text('#info')
    assert '目前狀態' in info_text
    assert 'px' in info_text

    # Check if col1 has content
    col1_content = page.inner_text('#col1')
    assert 'Test Song' in col1_content
    assert 'Line 1' in col1_content

def test_empty_lyrics(page):
    # Set title but no lyrics
    page.fill('#titleInput', 'Empty Song')
    page.fill('#lyricsInput', '')

    # Click the generate button
    page.click('button:has-text("🚀 產生排版")')

    # Info text should remain empty (or default)
    info_text = page.inner_text('#info')
    assert info_text == ''

    # Columns should be empty
    assert page.inner_text('#col1') == ''
    assert page.inner_text('#col2') == ''

def test_long_lyrics_double_column(page):
    # Generate long lyrics
    long_lyrics = '\n'.join([f'Line {i}' for i in range(1, 101)])
    page.fill('#titleInput', 'Long Song')
    page.fill('#lyricsInput', long_lyrics)

    # Click the generate button
    page.click('button:has-text("🚀 產生排版")')

    # Should likely be double column
    info_text = page.inner_text('#info')
    assert '雙欄' in info_text

    # Check if col2 is not empty
    col2_content = page.inner_text('#col2')
    assert len(col2_content) > 0

def test_title_rendering(page):
    page.fill('#titleInput', 'Unique Title')
    page.fill('#lyricsInput', 'Some lyrics')
    page.click('button:has-text("🚀 產生排版")')

    # Title should be in col1 with class lyrics-title
    title_element = page.query_selector('#col1 .lyrics-title')
    assert title_element is not None
    assert title_element.inner_text() == 'Unique Title'
