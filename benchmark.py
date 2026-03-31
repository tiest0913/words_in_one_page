
import time
from playwright.sync_api import sync_playwright

def run_benchmark():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Use a local file path
        import os
        path = "file://" + os.path.abspath("index.html")
        page.goto(path)

        # Long lyrics to make it work harder
        lyrics = "\n".join([f"Line {i}: This is some lyrics text to fill the page and trigger layout calculations." for i in range(100)])
        title = "Benchmark Song Title"

        page.fill("#titleInput", title)
        page.fill("#lyricsInput", lyrics)

        # Warm up
        for _ in range(5):
            page.click("button:has-text('🚀 產生排版')")

        iterations = 50
        start_time = time.time()
        for _ in range(iterations):
            page.click("button:has-text('🚀 產生排版')")
        end_time = time.time()

        avg_time = (end_time - start_time) / iterations
        print(f"Average time per layout calculation: {avg_time:.4f} seconds")

        browser.close()
        return avg_time

if __name__ == "__main__":
    run_benchmark()
