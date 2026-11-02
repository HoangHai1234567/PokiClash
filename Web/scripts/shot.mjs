// Chụp màn hình bằng Chrome không giao diện, để soi giao diện mà không cần mở trình duyệt.
// node scripts/shot.mjs --go "screen=map&skipintro" --wait 1500 --click ".tab" --shot ten [--eval "js"] ...
import puppeteer from 'puppeteer-core';
import fs from 'node:fs';

const BASE = process.env.PC_URL || 'http://localhost:5180/';
const OUT = process.env.PC_SHOTS || 'shots';
fs.mkdirSync(OUT, { recursive: true });
const CHROME = ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'].find((p) => fs.existsSync(p));

const args = process.argv.slice(2);
const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: true,
  args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
  defaultViewport: { width: Number(process.env.PC_W || 540), height: Number(process.env.PC_H || 960), deviceScaleFactor: 1 },
});
const page = await browser.newPage();
// PC_ART_DIR: trả ảnh /art/<tên> từ thư mục khác (thử ảnh mà không chép vào public/)
if (process.env.PC_ART_DIR) {
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    const m = req.url().match(/\/art\/([\w-]+)\.png/);
    const f = m && `${process.env.PC_ART_DIR}/${m[1]}.png`;
    if (f && fs.existsSync(f)) req.respond({ status: 200, contentType: 'image/png', body: fs.readFileSync(f) });
    else req.continue();
  });
}
const errors = [];
page.on('console', (m) => {
  if (m.type() === 'error' || m.type() === 'warning') errors.push(`[${m.type()}] ${m.text()}`);
});
page.on('pageerror', (e) => errors.push(`[pageerror] ${e.message}`));

for (let i = 0; i < args.length; i += 2) {
  const k = args[i], v = args[i + 1];
  try {
    if (k === '--go') await page.goto(BASE + '?' + v, { waitUntil: 'networkidle0', timeout: 30000 });
    else if (k === '--wait') await new Promise((r) => setTimeout(r, Number(v)));
    else if (k === '--click') {
      await page.waitForSelector(v, { timeout: 8000 });
      await page.click(v);
    } else if (k === '--eval') console.log('eval:', JSON.stringify(await page.evaluate(v)));
    else if (k === '--shot') {
      await page.screenshot({ path: `${OUT}/${v}.png` });
      console.log('shot', `${OUT}/${v}.png`);
    }
  } catch (e) {
    console.log(`step ${k} ${v} failed: ${e.message}`);
  }
}
if (errors.length) console.log('CONSOLE:\n' + errors.slice(0, 30).join('\n'));
await browser.close();
