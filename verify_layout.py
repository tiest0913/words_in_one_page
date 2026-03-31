
from playwright.sync_api import sync_playwright, expect
import os

def verify_layout():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="/home/jules/verification/video")
        page = context.new_page()

        path = "file://" + os.path.abspath("index.html")
        page.goto(path)
        page.wait_for_timeout(500)

        # Test with some lyrics
        title = "Optimized Title"
        lyrics = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6"

        page.fill("#titleInput", title)
        page.fill("#lyricsInput", lyrics)
        page.wait_for_timeout(500)

        page.click("button:has-text('🚀 產生排版')")
        page.wait_for_timeout(500)

        # Verify title and lyrics are present
        expect(page.locator(".lyrics-title")).to_have_text(title)
        expect(page.locator("#col1")).to_contain_text("Line 1")

        page.screenshot(path="/home/jules/verification/verification.png")
        page.wait_for_timeout(1000)

        context.close()
        browser.close()

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/video", exist_ok=True)
    verify_layout()
