
import os
from playwright.sync_api import sync_playwright

def test_layout_correctness():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{os.getcwd()}/index.html")

        # Test with short lyrics (should be single column)
        title = "Short Song"
        lyrics = "Line 1\nLine 2\nLine 3"
        page.fill("#titleInput", title)
        page.fill("#lyricsInput", lyrics)
        page.click("button:has-text('產生排版')")

        info_text = page.inner_text("#info")
        assert "單欄" in info_text
        assert "歌詞字體: 100px" in info_text

        # Test with long lyrics (should be double column if it fits better)
        long_lyrics = "\n".join([f"Line {i}" for i in range(80)])
        page.fill("#titleInput", "Long Song")
        page.fill("#lyricsInput", long_lyrics)
        page.click("button:has-text('產生排版')")

        info_text = page.inner_text("#info")
        print(f"Long song info: {info_text}")

        # Verify columns
        col1_text = page.inner_text("#col1")
        col2_text = page.inner_text("#col2")

        assert "Long Song" in col1_text
        if "雙欄" in info_text:
            assert len(col2_text.strip()) > 0

        # Verify that scrollHeight <= offsetHeight (no overflow)
        overflow_check = page.evaluate("""() => {
            const col1 = document.getElementById('col1');
            const col2 = document.getElementById('col2');
            return col1.scrollHeight <= col1.offsetHeight && col2.scrollHeight <= col2.offsetHeight;
        }""")
        assert overflow_check is True

        browser.close()

if __name__ == "__main__":
    test_layout_correctness()
    print("Functional test passed!")
