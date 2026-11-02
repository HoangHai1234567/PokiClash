// Ảnh nền scene (đảo lớn, 5 đảo hệ). Có ảnh ở public/art/<tên>.png|jpg|webp thì dùng ảnh; chưa có thì tự vẽ
// bản đồ nét tay bằng roughjs (cùng toạ độ vùng và ải, nên thay ảnh vào là khớp).
import { WORLD_VILLAGE, ZONES, type ZoneDef } from '../core/data/stages';
import { ELEM_COLOR } from '../core/elements';
import type { Elem } from '../core/types';
import { INK, roughOf, type RoughCanvas } from './art';
import { icon } from './icons';
import { Rng } from '../core/rng';

export const SW = 540, SH = 960;

const imgCache = new Map<string, Promise<HTMLImageElement | null>>();
export function loadArt(name: string): Promise<HTMLImageElement | null> {
  let p = imgCache.get(name);
  if (!p) {
    p = (async () => {
      for (const ext of ['png', 'jpg', 'jpeg', 'webp']) {
        const im = new Image();
        im.src = `/art/${name}.${ext}`;
        const ok = await new Promise<boolean>((r) => {
          im.onload = () => r(true);
          im.onerror = () => r(false);
        });
        if (ok && im.naturalWidth > 0) return im;
      }
      return null;
    })();
    imgCache.set(name, p);
  }
  return p;
}

// nền scene: ảnh nếu có, không thì canvas vẽ tay
export async function sceneBackdrop(name: string, fallback: () => HTMLCanvasElement): Promise<HTMLElement> {
  const im = await loadArt(name);
  if (im) {
    const el = im.cloneNode() as HTMLImageElement;
    el.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;object-fit:cover';
    return el;
  }
  const c = fallback();
  c.style.cssText = 'position:absolute;inset:0;width:100%;height:100%';
  return c;
}

// ---------- vẽ tay ----------

const iconImg = new Map<string, HTMLImageElement>();
function iconImage(name: string): HTMLImageElement {
  let im = iconImg.get(name);
  if (!im) {
    im = new Image();
    im.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(icon(name, 96).replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '));
    iconImg.set(name, im);
  }
  return im;
}
export function preloadIcons(): Promise<void> {
  // bỏ trùng tên: cùng một ảnh mà gán onload hai lần thì lời hứa đầu không bao giờ xong
  const names = [...new Set(Object.values(LANDMARKS).flat().concat(['machine', 'boss', 'crownSm']))];
  return Promise.all(names.map((n) => new Promise<void>((r) => {
    const im = iconImage(n);
    if (im.complete) r();
    else {
      im.addEventListener('load', () => r(), { once: true });
      im.addEventListener('error', () => r(), { once: true });
    }
  }))).then(() => undefined);
}

const LANDMARKS: Record<Elem, string[]> = {
  thuy: ['wave', 'drop', 'bubble', 'trident', 'wave'],
  hoa: ['flame', 'torch', 'phoenix', 'flame', 'sun'],
  kim: ['bell', 'helmet', 'hammer', 'bell', 'e_kim'],
  moc: ['leaf', 'seed', 'feather', 'lotus', 'leaf'],
  tho: ['e_tho', 'rock', 'incense', 'e_tho', 'crownSm'],
};
const LIGHT: Record<Elem, string> = { thuy: '#bfe4f5', hoa: '#ffc7a0', kim: '#e4e9ee', moc: '#c9ecb0', tho: '#f6dca0' };

function canvas(px: number): [HTMLCanvasElement, CanvasRenderingContext2D, RoughCanvas] {
  const c = document.createElement('canvas');
  c.width = Math.round(SW * px);
  c.height = Math.round(SH * px);
  const g = c.getContext('2d')!;
  g.scale(px, px);
  return [c, g, roughOf(c)];
}

// khối tròn méo mềm (cộng vài sóng sin), trông như bờ đảo vẽ tay
function blob(cx: number, cy: number, rx: number, ry: number, rng: Rng, n = 18): [number, number][] {
  const pts: [number, number][] = [];
  const p1 = rng.range(0, 6), p2 = rng.range(0, 6), p3 = rng.range(0, 6);
  const m = Math.max(n, 40);
  for (let i = 0; i < m; i++) {
    const a = (i / m) * Math.PI * 2;
    const k = 1 + 0.09 * Math.sin(3 * a + p1) + 0.05 * Math.sin(5 * a + p2) + 0.03 * Math.sin(9 * a + p3);
    pts.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]);
  }
  return pts;
}

function sea(g: CanvasRenderingContext2D, rc: RoughCanvas, top: string, bottom: string, seed: number) {
  const gr = g.createLinearGradient(0, 0, 0, SH);
  gr.addColorStop(0, top);
  gr.addColorStop(1, bottom);
  g.fillStyle = gr;
  g.fillRect(0, 0, SW, SH);
  const rng = new Rng(seed);
  for (let i = 0; i < 46; i++) {
    const x = rng.range(-20, SW), y = rng.range(0, SH);
    rc.arc(x, y, 34, 12, Math.PI, Math.PI * 2, false, { stroke: 'rgba(255,255,255,0.55)', strokeWidth: 1.6, roughness: 1.2, seed: i + seed });
  }
}

function stamp(g: CanvasRenderingContext2D, name: string, x: number, y: number, size: number, rot = 0) {
  const im = iconImage(name);
  if (!im.complete) return;
  g.save();
  g.translate(x, y);
  g.rotate(rot);
  g.drawImage(im, -size / 2, -size / 2, size, size);
  g.restore();
}

export function drawWorldFallback(px: number): HTMLCanvasElement {
  const [c, g, rc] = canvas(px);
  sea(g, rc, '#7fd0e0', '#3fa8c4', 3);
  const rng = new Rng(11);
  // bóng đảo
  rc.polygon(blob(270, 470, 250, 400, rng, 24), { stroke: 'none', fill: 'rgba(30,60,80,0.25)', fillStyle: 'solid', roughness: 2, seed: 2 });
  // mỗi vùng một khối, vẽ từ trên xuống
  const order = [...ZONES].sort((a, b) => a.world[1] - b.world[1]);
  for (const z of order) {
    const [fx, fy] = z.world;
    const cx = fx * SW, cy = fy * SH;
    const pts = blob(cx, cy, 165, 190, rng, 16);
    rc.polygon(pts, { stroke: INK, strokeWidth: 3, fill: LIGHT[z.id], fillStyle: 'solid', roughness: 1.6, seed: z.order + 5 });
    rc.polygon(pts, { stroke: 'none', fill: ELEM_COLOR[z.id], fillStyle: 'hachure', hachureGap: 8, fillWeight: 2.2, hachureAngle: -40 + z.order * 20, roughness: 1.4, seed: z.order + 9 });
  }
  for (const z of ZONES) {
    const [fx, fy] = z.world;
    const lm = LANDMARKS[z.id];
    for (let i = 0; i < 7; i++) {
      const a = rng.range(0, Math.PI * 2), r = rng.range(30, 110);
      stamp(g, lm[i % lm.length], fx * SW + Math.cos(a) * r, fy * SH + Math.sin(a) * r * 1.1, rng.range(30, 48), rng.range(-0.3, 0.3));
    }
  }
  // làng giữa
  const [vx, vy] = WORLD_VILLAGE;
  rc.circle(vx * SW, vy * SH, 120, { stroke: INK, strokeWidth: 3, fill: '#f3e2b0', fillStyle: 'solid', roughness: 1.4, seed: 21 });
  rc.circle(vx * SW, vy * SH, 120, { stroke: 'none', fill: '#d9c48e', fillStyle: 'cross-hatch', hachureGap: 9, roughness: 1.2, seed: 22 });
  stamp(g, 'machine', vx * SW, vy * SH - 6, 76);
  return c;
}

export function drawZoneFallback(z: ZoneDef, px: number): HTMLCanvasElement {
  const [c, g, rc] = canvas(px);
  sea(g, rc, z.sky[0], z.sea, z.order + 30);
  const rng = new Rng(100 + z.order);
  rc.polygon(blob(270, 500, 250, 440, rng, 26), { stroke: 'none', fill: 'rgba(30,40,50,0.25)', fillStyle: 'solid', roughness: 2, seed: 3 });
  const pts = blob(270, 480, 245, 430, rng, 26);
  rc.polygon(pts, { stroke: INK, strokeWidth: 3.5, fill: LIGHT[z.id], fillStyle: 'solid', roughness: 1.6, seed: 4 });
  rc.polygon(pts, { stroke: 'none', fill: z.ground, fillStyle: 'hachure', hachureGap: 9, fillWeight: 2.4, hachureAngle: -50, roughness: 1.4, seed: 5 });
  // đường mòn qua các ải
  const P = z.nodes.map(([x, y]) => [x * SW, y * SH] as [number, number]);
  rc.curve(P, { stroke: '#a8865a', strokeWidth: 18, roughness: 1, seed: 6 });
  rc.curve(P, { stroke: '#f3e2b0', strokeWidth: 11, roughness: 1, seed: 7 });
  // cảnh vật hai bên đường
  const lm = LANDMARKS[z.id];
  for (let i = 0; i < 26; i++) {
    const x = rng.range(70, 470), y = rng.range(120, 880);
    if (P.some(([px2, py2]) => Math.hypot(px2 - x, py2 - y) < 70)) continue;
    stamp(g, lm[i % lm.length], x, y, rng.range(30, 56), rng.range(-0.3, 0.3));
  }
  // hang boss
  const [bx, by] = P[P.length - 1];
  stamp(g, lm[0], bx - 60, by - 20, 70, -0.2);
  stamp(g, lm[1], bx + 62, by - 10, 70, 0.2);
  return c;
}
