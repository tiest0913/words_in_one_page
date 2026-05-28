import unittest
import os
from playwright.sync_api import sync_playwright

class TestLayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(headless=True)
        cls.context = cls.browser.new_context()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def setUp(self):
        self.page = self.context.new_page()
        # Load the local index.html
        path = os.path.abspath("index.html")
        self.page.goto(f"file://{path}")

    def tearDown(self):
        self.page.close()

    def test_very_long_lyrics(self):
        """Test layout behavior with very long lyrics that exceed page capacity."""
        # Provide a very long list of lyrics
        long_lyrics = "\n".join([f"Line {i}" for i in range(1, 500)])

        self.page.fill("#titleInput", "Long Song")
        self.page.fill("#lyricsInput", long_lyrics)

        # Click the generate button
        self.page.click("button[onclick='calculateLayout()']")

        # Wait for info to update
        info_text = self.page.inner_text("#info")
        print(f"Info text: {info_text}")

        # Verify that it handled it (likely by falling back to 10px)
        self.assertIn("10px", info_text)

        # Check if the content is actually there
        col1_text = self.page.inner_text("#col1")
        self.assertIn("Line 1", col1_text)

        # Verify the columns overflow or are handled
        col1_scroll_height = self.page.eval_on_selector("#col1", "el => el.scrollHeight")
        col1_offset_height = self.page.eval_on_selector("#col1", "el => el.offsetHeight")

        print(f"Col1 ScrollHeight: {col1_scroll_height}, OffsetHeight: {col1_offset_height}")
        # When lyrics are too long even at 10px, scrollHeight will exceed offsetHeight
        self.assertGreater(col1_scroll_height, col1_offset_height)

if __name__ == "__main__":
    unittest.main()
