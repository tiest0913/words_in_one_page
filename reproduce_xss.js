const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('file://' + process.cwd() + '/index.html');

  // Set an XSS payload in the title input
  await page.fill('#titleInput', '<img src=x onerror="window.xssDetected=true">');
  await page.fill('#lyricsInput', 'Some lyrics');

  // Click the button to trigger calculateLayout
  await page.click('button:has-text("產生排版")');

  // Check if the XSS was executed
  const xssDetected = await page.evaluate(() => window.xssDetected);

  if (xssDetected) {
    console.log('XSS Detected!');
  } else {
    console.log('XSS NOT Detected.');
  }

  await browser.close();
})();
