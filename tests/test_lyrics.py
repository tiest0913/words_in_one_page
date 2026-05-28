from playwright.sync_api import sync_playwright
import os

def test_empty_lyrics():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the local index.html
        path = os.path.abspath("index.html")
        page.goto(f"file://{path}")

        # Initial state: col1 and col2 should be empty
        col1 = page.locator("#col1")
        col2 = page.locator("#col2")

        assert col1.inner_text() == ""
        assert col2.inner_text() == ""

        # 1. Fill title but leave lyrics empty and click Generate
        page.fill("#titleInput", "Test Title")
        page.click("button:has-text('產生排版')")

        # Should still be empty because it returned early
        assert col1.inner_text() == ""
        assert col2.inner_text() == ""

        # 2. Fill both lyrics and title and click Generate
        page.fill("#lyricsInput", "Line 1\nLine 2")
        page.click("button:has-text('產生排版')")

        # Should now have content
        content_after = col1.inner_text()
        assert "Test Title" in content_after
        assert "Line 1" in content_after

        # 3. Clear lyrics and click Generate again
        page.fill("#lyricsInput", "")
        page.click("button:has-text('產生排版')")

        # Should NOT have changed (should still have the previous content because of the early return)
        assert col1.inner_text() == content_after

        browser.close()
        print("Test passed successfully!")

if __name__ == "__main__":
    test_empty_lyrics()
