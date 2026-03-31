import os
from playwright.sync_api import sync_playwright, expect

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        file_path = "file://" + os.path.abspath("index.html")

        # Test Case 1: Empty lyrics input
        page.goto(file_path)
        page.fill("#titleInput", "Test Title")
        page.fill("#lyricsInput", "")
        page.click("button:has-text('🚀 產生排版')")
        expect(page.locator("#col1")).to_be_empty()
        expect(page.locator("#info")).to_be_empty()
        print("✓ Test 1: Empty lyrics handled correctly.")

        # Test Case 2: Whitespace-only lyrics
        page.goto(file_path)
        page.fill("#lyricsInput", "   \n   ")
        page.click("button:has-text('🚀 產生排版')")
        expect(page.locator("#col1")).to_be_empty()
        expect(page.locator("#info")).to_be_empty()
        print("✓ Test 2: Whitespace-only lyrics handled correctly.")

        # Test Case 3: Valid input
        page.goto(file_path)
        page.fill("#titleInput", "Song Title")
        page.fill("#lyricsInput", "Line 1\nLine 2")
        page.click("button:has-text('🚀 產生排版')")
        expect(page.locator("#col1")).not_to_be_empty()
        expect(page.locator("#info")).to_contain_text("目前狀態")
        print("✓ Test 3: Valid input generates layout correctly.")

        browser.close()

if __name__ == "__main__":
    run_tests()
