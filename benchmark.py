
import time
from playwright.sync_api import sync_playwright

def run_benchmark():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///app/index.html")

        # Sample lyrics (approx 100 lines)
        lyrics = "\n".join([f"Line {i}: This is a sample lyric line for performance testing purposes." for i in range(100)])
        title = "Performance Test Title"

        page.fill("#titleInput", title)
        page.fill("#lyricsInput", lyrics)

        # Measure calculateLayout execution time
        # We'll run it multiple times to get an average
        iterations = 10
        total_time = 0

        for _ in range(iterations):
            start = page.evaluate("performance.now()")
            page.evaluate("calculateLayout()")
            end = page.evaluate("performance.now()")
            total_time += (end - start)

        avg_time = total_time / iterations
        print(f"Average calculateLayout time: {avg_time:.4f} ms")

        browser.close()

if __name__ == "__main__":
    run_benchmark()
