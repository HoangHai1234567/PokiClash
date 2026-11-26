// Kết xuất khung duyệt với KHUNG NHÌN CỐ ĐỊNH (như camera trong game) bằng lõi AtomSpine (renderFrame nhận hộp thế giới; lệnh
// `atom sheet` thì tự co theo hình nên clip có tay vươn ra ngoài khung sẽ bị thu nhỏ). Chỉ dùng để xem, không sửa project.
// Chạy (xem_d2.py gọi, đặt biến ATOMSPINE_DIR): node <AtomSpine>/node_modules/tsx/dist/cli.mjs khung.mts <thư mục project> <thư mục ra> <fps>
//                        <minX,minY,maxX,maxY> <rộng> <cao> <cột> <clip,clip,...> [bg RRGGBB]
// Ra: <thư mục ra>/<clip>_sheet.png (các khung xếp lưới, ô rộng x cao) + in "<clip> <số khung> <dur>".
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const AS = process.env.ATOMSPINE_DIR ?? 'D:/AtomSpine';
const { parseProject, renderFrame, encodePng } = await import(pathToFileURL(join(AS, 'packages/core/src/index.ts')).href);
const { projectImages } = await import(pathToFileURL(join(AS, 'packages/cli/src/images.ts')).href);

const [dir, out, fpsS, boxS, wS, hS, colsS, clipsS, bgS] = process.argv.slice(2);
const fps = Number(fpsS);
const [minX, minY, maxX, maxY] = boxS.split(',').map(Number);
const w = Number(wS), h = Number(hS), cols = Number(colsS);
const bgHex = bgS ?? 'EFE5D2';
const bg: [number, number, number, number] = [parseInt(bgHex.slice(0, 2), 16), parseInt(bgHex.slice(2, 4), 16), parseInt(bgHex.slice(4, 6), 16), 255];
const project = parseProject(readFileSync(join(dir, 'atomspine.json'), 'utf8'));
const images = projectImages(dir, project, []);
for (const name of clipsS.split(',')) {
  const anim = project.anims.find((a: any) => a.name === name);
  if (!anim) { console.log(`${name} MISSING`); continue; }
  const dur = (anim as any).dur ?? (anim as any).duration ?? 1;
  const n = Math.round(dur * fps) + 1;
  const rows = Math.ceil(n / cols);
  const sheet = new Uint8Array(cols * w * rows * h * 4);
  for (let k = 0; k < n; k++) {
    const img: any = renderFrame(project, images, { anim: name, t: Math.min(dur, k / fps), width: w, height: h, bg, fit: { minX, minY, maxX, maxY }, padding: 0 });
    const data: Uint8Array = img.data ?? img.rgba ?? img.pixels;
    const x0 = (k % cols) * w, y0 = Math.floor(k / cols) * h;
    for (let y = 0; y < h; y++) sheet.set(data.subarray(y * w * 4, (y + 1) * w * 4), ((y0 + y) * cols * w + x0) * 4);
  }
  const first: any = renderFrame(project, images, { anim: name, t: 0, width: 4, height: 4, bg, fit: { minX, minY, maxX, maxY }, padding: 0 });
  const key = first.data ? 'data' : first.rgba ? 'rgba' : 'pixels';
  writeFileSync(join(out, `${name}_sheet.png`), encodePng({ w: cols * w, h: rows * h, [key]: sheet } as any));
  console.log(`${name} ${n} ${dur}`);
}
