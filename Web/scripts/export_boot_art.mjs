// Xuất ảnh màn boot "Sa bàn giấy" (ý tưởng A, người dùng chọn 2026-11-06) cho Unity, vẽ bằng đúng code của bản web, nhân 2:
// logo, tấm bản đồ giấy (giấy kẻ ô, biển, băng keo, la bàn; đảo dùng Islands/world.png có sẵn), mặt bàn gỗ, 3 lá thẻ úp,
// bút chì, cờ 5 hệ, khung và lõi thanh tải, giấy ghi chú, băng keo chữ, nét gạch chân, đế tướng.
// Cần dev server đang chạy (npm run dev, cổng 5180). Chạy: node scripts/export_boot_art.mjs [thư mục đích]
// Mặc định ghi vào ../Assets/03 Art/Boot (tên boot_*, không trùng ảnh thay thế trong Fallback).
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const here = dirname(fileURLToPath(import.meta.url));
const out = resolve(process.argv[2] ?? join(here, '../../Assets/03 Art/Boot'));
const url = process.env.PC_URL ?? 'http://localhost:5180/';
const chrome = process.env.CHROME ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe';
mkdirSync(out, { recursive: true });

const browser = await puppeteer.launch({ executablePath: chrome, headless: true, args: ['--no-sandbox'], defaultViewport: { width: 1400, height: 1800, deviceScaleFactor: 2 } });
const page = await browser.newPage();
await page.goto(url + '?skipboot', { waitUntil: 'networkidle0' });

const wood = await page.evaluate(async () => {
  const common = await import('/src/view/boot/common.ts');
  const table = await import('/src/view/boot/sceneTable.ts');
  const icons = await import('/src/view/icons.ts');
  await document.fonts.ready;
  const root = document.getElementById('root');
  document.getElementById('desk').style.display = 'none';
  document.documentElement.style.background = 'transparent';
  document.body.style.background = 'transparent';
  const bx = document.createElement('div');
  bx.id = 'bx';
  bx.style.cssText = 'position:absolute;left:0;top:0;display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start;width:1380px';
  bx.style.setProperty('--grain', getComputedStyle(root).getPropertyValue('--grain'));
  document.body.append(bx);
  const add = (id, html, style = '') => {
    const d = document.createElement('div');
    d.id = id;
    d.style.cssText = `position:relative;display:inline-block;${style}`;
    d.innerHTML = html;
    bx.append(d);
  };
  const INK = '#2b2118';
  add('logo', common.logoSvg('xl', 360), 'padding:14px');
  const tapes = [[-22, -12, -8], [428, -10, 7], [-24, 672, 6], [430, 670, -9]]
    .map(([x, y, r]) => `<div class="ta-tape" style="left:${x}px;top:${y}px;transform:rotate(${r}deg)"></div>`).join('');
  const compass = `<svg style="position:absolute;left:0;top:0" viewBox="0 0 480 690" width="480" height="690"><g transform="translate(424 628)">
      <circle r="26" fill="#fffaf0" stroke="${INK}" stroke-width="3"/>
      <path d="M0 -22 L7 0 L0 22 L-7 0 Z" fill="#e8553f" stroke="${INK}" stroke-width="2.4" stroke-linejoin="round"/>
      <path d="M0 0 L7 0 L0 22 Z" fill="#fffaf0" stroke="${INK}" stroke-width="2.4" stroke-linejoin="round"/>
      <text y="-31" text-anchor="middle" font-family="'Baloo 2'" font-weight="800" font-size="17" fill="${INK}">B</text></g></svg>`;
  add('sheet', `<div class="ta-sheet" style="position:relative;left:0;top:0;transform:none"><div class="ta-sheet-bg bt-paper"></div><div class="ta-sea"></div>${tapes}${compass}</div>`, 'padding:30px');
  const cards = [[-14, 392, -22], [8, 408, -6], [30, 428, 10]]
    .map(([x, y, r]) => `<div class="ta-card" style="left:${x + 44}px;top:${y - 372}px;transform:rotate(${r}deg)">${icons.icon('star', 30)}</div>`).join('');
  add('cards', cards, 'width:200px;height:220px');
  add('pencil', table.pencilSvg(), 'padding:4px;line-height:0');
  for (const e of ['thuy', 'hoa', 'kim', 'moc', 'tho']) add('flag_' + e, table.flagSvg(e), 'padding:4px;line-height:0');
  add('bar', '<div class="bt-bar" style="margin:0"></div>', 'padding:2px');
  add('barfill', '<div class="bt-bar-fill" style="position:relative;width:294px;height:18px;transition:none"></div>', 'line-height:0');
  add('note', '<div class="ta-note" style="position:relative;left:0;bottom:auto;transform:none"></div>', 'padding:3px');
  add('tagline', '<div class="bt-tagline" style="position:relative;left:0;transform:none;color:transparent">Sổ Tay Phiêu Lưu</div>', 'padding:2px');
  add('underline', `<svg viewBox="0 0 200 14" width="280" height="14" preserveAspectRatio="none"><path d="M3 9c40-6 90-7 194-3M20 12c50-4 100-4 150-2" fill="none" stroke="#e8553f" stroke-width="3.4" stroke-linecap="round"/></svg>`, 'padding:3px;line-height:0');
  add('de_nen', '<div style="width:84px;height:36px;border-radius:50%;background:#fff"></div>', 'line-height:0');
  add('de_vien', `<div style="width:84px;height:36px;border-radius:50%;border:3px solid ${INK}"></div>`, 'line-height:0');
  // chữ ô ghi chú và băng keo đo để Unity đặt cỡ
  return common.woodTexture(2);
});

const names = {
  logo: 'boot_logo', sheet: 'boot_ban_do', cards: 'boot_the_up', pencil: 'boot_but_chi',
  flag_thuy: 'boot_co_thuy', flag_hoa: 'boot_co_hoa', flag_kim: 'boot_co_kim', flag_moc: 'boot_co_moc', flag_tho: 'boot_co_tho',
  bar: 'boot_thanh_tai', barfill: 'boot_thanh_tai_loi', note: 'boot_giay_ghi', tagline: 'boot_bang_keo', underline: 'boot_gach_chan',
  de_nen: 'boot_de_nen', de_vien: 'boot_de_vien',
};
const sizes = {};
for (const [id, name] of Object.entries(names)) {
  const el = await page.$('#' + id);
  const box = await el.boundingBox();
  sizes[name] = [Math.round(box.width * 2), Math.round(box.height * 2)];
  await el.screenshot({ path: join(out, name + '.png'), omitBackground: true });
}
writeFileSync(join(out, 'boot_ban_go.png'), Buffer.from(wood.split(',')[1], 'base64'));
await browser.close();
console.log('ghi', Object.keys(names).length + 1, 'ảnh vào', out);
console.log(JSON.stringify(sizes));
