// Xuất ảnh thay thế cho Unity từ code vẽ của bản web: icon SVG (256 px), bản đồ nét tay (đảo lớn, 5 đảo hệ, 1080 × 1920)
// và nền sân đấu theo hệ (1080 × 928).
// Cần dev server đang chạy (npm run dev, cổng 5180). Chạy: node scripts/export_fallback.mjs [thư mục đích]
// Mặc định ghi vào ../Assets/03 Art/Fallback. Unity chỉ dùng các ảnh này khi chưa có ảnh gen cùng tên.
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const here = dirname(fileURLToPath(import.meta.url));
const out = resolve(process.argv[2] ?? join(here, '../../Assets/03 Art/Fallback'));
const url = process.env.PC_URL ?? 'http://localhost:5180/';
const chrome = process.env.CHROME ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe';
mkdirSync(join(out, 'Icons'), { recursive: true });

// tên icon lấy thẳng từ bảng P trong icons.ts
const src = readFileSync(join(here, '../src/view/icons.ts'), 'utf8');
const names = [...src.matchAll(/^ {2}([A-Za-z_0-9]+):/gm)].map((m) => m[1]);

const browser = await puppeteer.launch({ executablePath: chrome, headless: true, args: ['--no-sandbox'] });
const page = await browser.newPage();
await page.goto(url, { waitUntil: 'networkidle0' });

const result = await page.evaluate(async (names) => {
  const icons = await import('/src/view/icons.ts');
  const scenery = await import('/src/view/scenery.ts');
  const stages = await import('/src/core/data/stages.ts');
  const battleStage = await import('/src/view/battle/stage.ts');
  await scenery.preloadIcons();
  const toPng = async (svg, size) => {
    const im = new Image();
    im.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '));
    await im.decode();
    const c = document.createElement('canvas');
    c.width = c.height = size;
    c.getContext('2d').drawImage(im, 0, 0, size, size);
    return c.toDataURL('image/png');
  };
  const res = { icons: {}, maps: {} };
  for (const n of names) res.icons[n] = await toPng(icons.icon(n, 256), 256);
  res.maps.world = scenery.drawWorldFallback(2).toDataURL('image/png');
  for (const z of stages.ZONES) res.maps['zone_' + z.id] = scenery.drawZoneFallback(z, 2).toDataURL('image/png');
  // nền sân đấu theo hệ (540 × 464, nhân 2)
  for (const z of stages.ZONES) {
    const st = new battleStage.Stage(z, () => 2);
    res.maps['battle_' + z.id] = st.paintBg().toDataURL('image/png');
    st.destroy();
  }
  return res;
}, names);
await browser.close();

const save = (file, dataUrl) => writeFileSync(file, Buffer.from(dataUrl.split(',')[1], 'base64'));
for (const [n, d] of Object.entries(result.icons)) save(join(out, 'Icons', `${n}.png`), d);
for (const [n, d] of Object.entries(result.maps)) save(join(out, `${n}.png`), d);
console.log(`ghi ${Object.keys(result.icons).length} icon và ${Object.keys(result.maps).length} bản đồ vào ${out}`);
