// Phát animation tướng xuất từ dự án aola (reskin/<tên>/export/anim.json). CHỈ DÙNG TRONG BẢN THỬ: hình gốc của Baitian.
// Mỗi khung là danh sách hình từ sau ra trước, mỗi hình [sprite, a, b, c, d, tx, ty, alpha, {blend, tint, filters}?]:
// ma trận đi từ điểm ảnh của sprite sang điểm ảnh của clip. Cách vẽ blend / tint / filter theo so_sanh.html của aola.

type Filter = { type: string; bx?: number; by?: number; color?: number[]; strength?: number; angle?: number; dist?: number; inner?: boolean; m?: number[] };
type Fx = { blend?: number; tint?: number[]; filters?: Filter[] };
type Pic = [number, number, number, number, number, number, number, number, Fx?];

export interface Clip {
  name: string;
  size: [number, number];
  frames: Pic[][];
  anchor: [number, number];
  bounds: [number, number, number, number];
  disp: [number, number][]; // dịch chuyển thân so với khung đầu (điểm ảnh clip), đã làm mượt
  peak: number; // khung lao xa nhất
  hit: number; // khung trúng đòn
}

export const IDLE = '1_1', HIT = '1_2', ATTACK = '1_4', SKILL = '1_6';
export const AOLA_BASE = '/aola/';

const BLEND: Record<number, GlobalCompositeOperation> = {
  3: 'multiply', 4: 'screen', 5: 'lighten', 6: 'darken', 7: 'difference', 8: 'lighter', 9: 'difference', 13: 'overlay', 14: 'hard-light',
};

const cache = new Map<string, Promise<AolaAnim | null>>();

export class AolaAnim {
  dir = '';
  fps = 25;
  clips: Record<string, Clip> = {};
  imgs: HTMLImageElement[] = [];
  idleH = 200;
  shadow = -1; // sprite bóng dưới chân (mảnh đầu của dáng đứng)

  static load(dir: string): Promise<AolaAnim | null> {
    let p = cache.get(dir);
    if (!p) {
      p = AolaAnim.fetch(dir).catch((e) => {
        console.warn('[aola] không tải được', dir, e);
        return null;
      });
      cache.set(dir, p);
    }
    return p;
  }

  private static async fetch(dir: string): Promise<AolaAnim | null> {
    const res = await fetch(`${AOLA_BASE}${dir}/export/anim.json`);
    if (!res.ok) return null;
    const j = await res.json();
    const a = new AolaAnim();
    a.dir = dir;
    a.fps = j.fps || 25;
    a.imgs = (j.sprites as string[]).map((s) => {
      const im = new Image();
      im.src = `${AOLA_BASE}${dir}/${s}`;
      return im;
    });
    await Promise.all(a.imgs.map((im) => (im.complete ? Promise.resolve() : new Promise<void>((r) => { im.onload = () => r(); im.onerror = () => r(); }))));
    for (const [name, c] of Object.entries(j.clips as Record<string, { size: [number, number]; frames: Pic[][] }>))
      a.clips[name] = { name, size: c.size, frames: c.frames, anchor: [0, 0], bounds: [0, 0, 0, 0], disp: [], peak: 0, hit: 0 };
    if (!a.clips[IDLE]) return null;
    a.prepare();
    return a;
  }

  private corners(p: Pic): [number, number][] {
    const im = this.imgs[p[0]];
    const w = im?.naturalWidth || 0, h = im?.naturalHeight || 0;
    return [[0, 0], [w, 0], [0, h], [w, h]].map(([x, y]) => [p[1] * x + p[3] * y + p[5], p[2] * x + p[4] * y + p[6]]);
  }

  private prepare() {
    const idle = this.clips[IDLE];
    const shadow = idle.frames[0][0][0];
    this.shadow = shadow;
    const center = (p: Pic): [number, number] => {
      const im = this.imgs[p[0]];
      const x = (im?.naturalWidth || 0) / 2, y = (im?.naturalHeight || 0) / 2;
      return [p[1] * x + p[3] * y + p[5], p[2] * x + p[4] * y + p[6]];
    };
    const sh0 = idle.frames[0].find((p) => p[0] === shadow)!;
    idle.anchor = center(sh0);
    for (const c of Object.values(this.clips)) {
      // điểm khớp: tâm bóng dưới chân; không có bóng thì dời theo các mảnh chung với dáng đứng
      if (c !== idle) {
        const s = c.frames[0]?.find((p) => p[0] === shadow);
        if (s) c.anchor = center(s);
        else {
          const offs: [number, number][] = [];
          for (const p of c.frames[0] ?? []) {
            const q = idle.frames[0].find((x) => x[0] === p[0]);
            if (q) offs.push([p[5] - q[5], p[6] - q[6]]);
          }
          if (offs.length) {
            offs.sort((u, v) => u[0] - v[0]);
            const m = offs[Math.floor(offs.length / 2)];
            c.anchor = [idle.anchor[0] + m[0], idle.anchor[1] + m[1]];
          } else c.anchor = [c.size[0] / 2, c.size[1] * 0.9];
        }
      }
      let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
      const raw: ([number, number] | null)[] = [];
      for (const f of c.frames) {
        let sx = 0, sy = 0, n = 0;
        for (const p of f) {
          for (const [x, y] of this.corners(p)) {
            x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y);
          }
          if (p[0] !== shadow) { sx += p[5]; sy += p[6]; n++; }
        }
        raw.push(n ? [sx / n, sy / n] : null);
      }
      c.bounds = isFinite(x0) ? [x0, y0, x1, y1] : [0, 0, c.size[0], c.size[1]];
      // dịch chuyển thân theo khung, làm mượt
      const base = raw.find((r) => r) ?? [0, 0];
      let last: [number, number] = [0, 0];
      const d = raw.map((r) => (last = r ? [r[0] - base[0], r[1] - base[1]] : last));
      c.disp = d.map((_, i) => {
        let sx = 0, sy = 0, n = 0;
        for (let k = Math.max(0, i - 2); k <= Math.min(d.length - 1, i + 2); k++) { sx += d[k][0]; sy += d[k][1]; n++; }
        return [sx / n, sy / n];
      });
      let best = 0, bi = 0;
      c.disp.forEach(([x, y], i) => { const m = Math.hypot(x, y); if (m > best) { best = m; bi = i; } });
      c.peak = bi;
      c.hit = best > 60 ? bi : Math.floor(c.frames.length * (c.name === SKILL ? 0.55 : 0.6));
    }
    const ib = idle.bounds;
    this.idleH = Math.max(40, idle.anchor[1] - ib[1]);
  }

  clip(name: string): Clip {
    return this.clips[name] ?? this.clips[IDLE];
  }
  duration(name: string): number {
    return this.clip(name).frames.length / this.fps;
  }
  frameAt(name: string, t: number, loop: boolean): number {
    const n = this.clip(name).frames.length;
    const i = Math.floor(t * this.fps);
    return loop ? ((i % n) + n) % n : Math.min(n - 1, Math.max(0, i));
  }

  // vẽ một khung, gốc toạ độ ở điểm khớp (bóng dưới chân); ctx đã đặt sẵn biến đổi ngoài
  drawFrame(ctx: CanvasRenderingContext2D, name: string, fi: number, scale: number, noShadow = false) {
    const c = this.clip(name);
    const frame = c.frames[fi] ?? c.frames[0];
    const base = ctx.getTransform();
    for (const p of frame) {
      if (noShadow && p[0] === this.shadow) continue;
      let im: CanvasImageSource = this.imgs[p[0]];
      const el = this.imgs[p[0]];
      if (!el || !el.complete || !el.naturalWidth) continue;
      const fx = p[8];
      let pad = 0;
      if (fx?.tint) im = tinted(el, p[0], this.dir, fx.tint);
      if (fx?.filters && fx.filters.length && canFilter) {
        const r = filtered(im, `${this.dir}|${p[0]}|${fx.tint?.join(',') ?? ''}`, fx.filters, Math.hypot(p[1], p[2]) * scale);
        im = r.c;
        pad = r.pad;
      }
      ctx.setTransform(base);
      ctx.scale(scale, scale);
      ctx.translate(-c.anchor[0], -c.anchor[1]);
      ctx.transform(p[1], p[2], p[3], p[4], p[5], p[6]);
      if (pad) ctx.translate(-pad, -pad);
      ctx.globalAlpha = p[7];
      ctx.globalCompositeOperation = (fx?.blend && BLEND[fx.blend]) || 'source-over';
      ctx.drawImage(im, 0, 0);
    }
    ctx.setTransform(base);
    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = 'source-over';
  }
}

// ---------- tint: colour transform của SWF, làm một lần rồi giữ ----------
const tintCache = new Map<string, HTMLCanvasElement>();
function tinted(im: HTMLImageElement, idx: number, dir: string, x: number[]): HTMLCanvasElement | HTMLImageElement {
  const key = `${dir}|${idx}|${x.join(',')}`;
  const hit = tintCache.get(key);
  if (hit) return hit;
  const c = document.createElement('canvas');
  c.width = im.naturalWidth;
  c.height = im.naturalHeight;
  const g = c.getContext('2d')!;
  const [mr, mg, mb, ar, ag, ab] = x;
  const k = (mr + mg + mb) / 3;
  if (Math.abs(k - 1) > 0.004 && canFilter) g.filter = `brightness(${k})`;
  g.drawImage(im, 0, 0);
  g.filter = 'none';
  for (const [op, r, gg, b, none] of [
    ['lighter', Math.max(0, ar), Math.max(0, ag), Math.max(0, ab), 0],
    ['multiply', 255 + Math.min(0, ar), 255 + Math.min(0, ag), 255 + Math.min(0, ab), 255],
  ] as [GlobalCompositeOperation, number, number, number, number][]) {
    if (r === none && gg === none && b === none) continue;
    const s = document.createElement('canvas');
    s.width = c.width;
    s.height = c.height;
    const sg = s.getContext('2d')!;
    sg.drawImage(im, 0, 0);
    sg.globalCompositeOperation = 'source-in';
    sg.fillStyle = `rgb(${r},${gg},${b})`;
    sg.fillRect(0, 0, s.width, s.height);
    g.globalCompositeOperation = op;
    g.drawImage(s, 0, 0);
    g.globalCompositeOperation = 'source-over';
  }
  g.globalCompositeOperation = 'destination-in';
  g.drawImage(im, 0, 0);
  tintCache.set(key, c);
  return c;
}

// ---------- filter của SWF (glow, shadow, blur, colour matrix) thành filter SVG cho canvas ----------
export const canFilter = typeof document !== 'undefined' && 'filter' in (document.createElement('canvas').getContext('2d') ?? {});
const filterDefs = new Map<string, string>();
function filterUrl(list: Filter[], scale: number): string {
  const key = JSON.stringify(list) + '@' + scale.toFixed(2);
  const hit = filterDefs.get(key);
  if (hit) return hit;
  let host = document.getElementById('swf-filters');
  if (!host) {
    host = document.createElementNS('http://www.w3.org/2000/svg', 'svg') as unknown as HTMLElement;
    host.id = 'swf-filters';
    host.setAttribute('width', '0');
    host.setAttribute('height', '0');
    host.style.position = 'absolute';
    document.body.appendChild(host);
  }
  const id = 'swf' + filterDefs.size;
  const dev = (w = 0) => Math.max(0.01, 0.35 * w * scale).toFixed(2);
  let body = '', last = 'SourceGraphic', n = 0;
  for (const f of list) {
    const out = 'r' + n++;
    if (f.type === 'blur') body += `<feGaussianBlur in="${last}" stdDeviation="${dev(f.bx)} ${dev(f.by)}" result="${out}"/>`;
    else if (f.type === 'matrix' && f.m) {
      const v = f.m.map((x, i) => (i % 5 === 4 ? x / 255 : x)).join(' ');
      body += `<feColorMatrix in="${last}" type="matrix" values="${v}" result="${out}"/>`;
    } else if ((f.type === 'glow' || f.type === 'shadow') && !f.inner && f.color) {
      const [r, g, b, a] = f.color, s = Math.min(f.strength ?? 1, 6);
      let dx = 0, dy = 0;
      if (f.type === 'shadow') {
        dx = Math.cos(f.angle ?? 0) * (f.dist ?? 0) * scale;
        dy = Math.sin(f.angle ?? 0) * (f.dist ?? 0) * scale;
      }
      body += `<feGaussianBlur in="${last}" stdDeviation="${dev(f.bx)} ${dev(f.by)}" result="${out}b"/>` +
        `<feOffset in="${out}b" dx="${dx.toFixed(2)}" dy="${dy.toFixed(2)}" result="${out}o"/>` +
        `<feFlood flood-color="rgb(${r},${g},${b})" flood-opacity="${a}" result="${out}c"/>` +
        `<feComposite in="${out}c" in2="${out}o" operator="in" result="${out}g"/>` +
        `<feComponentTransfer in="${out}g" result="${out}s"><feFuncA type="linear" slope="${s}"/></feComponentTransfer>` +
        `<feMerge result="${out}"><feMergeNode in="${out}s"/><feMergeNode in="${last}"/></feMerge>`;
    } else continue;
    last = out;
  }
  host.insertAdjacentHTML('beforeend', `<filter id="${id}" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB">${body}</filter>`);
  const url = body ? `url(#${id})` : 'none';
  filterDefs.set(key, url);
  return url;
}
const fxCache = new Map<string, { c: HTMLCanvasElement; pad: number }>();
function filtered(im: CanvasImageSource, key0: string, list: Filter[], sObj: number) {
  const k = 1 / Math.max(0.05, sObj);
  const kq = Math.round(k * 4) / 4;
  const key = key0 + '|' + JSON.stringify(list) + '|' + kq;
  const hit = fxCache.get(key);
  if (hit) return hit;
  let pad = 0;
  for (const f of list) if (f.bx !== undefined) pad = Math.max(pad, (Math.max(f.bx, f.by ?? 0) + (f.dist ?? 0)) * kq);
  pad = Math.ceil(pad * 1.2) + 2;
  const w = (im as HTMLImageElement).naturalWidth || (im as HTMLCanvasElement).width;
  const h = (im as HTMLImageElement).naturalHeight || (im as HTMLCanvasElement).height;
  const c = document.createElement('canvas');
  c.width = w + 2 * pad;
  c.height = h + 2 * pad;
  const g = c.getContext('2d')!;
  g.filter = filterUrl(list, kq);
  g.drawImage(im, pad, pad);
  const r = { c, pad };
  fxCache.set(key, r);
  return r;
}

// ---------- sticker: tướng vẽ vào canvas riêng, viền trắng rồi viền mực ----------
export const OUTLINE = canFilter
  ? 'drop-shadow(2.5px 0 0 #fff) drop-shadow(-2.5px 0 0 #fff) drop-shadow(0 2.5px 0 #fff) drop-shadow(0 -2.5px 0 #fff) ' +
    'drop-shadow(2px 0 0 #2b2118) drop-shadow(-2px 0 0 #2b2118) drop-shadow(0 2px 0 #2b2118) drop-shadow(0 -2px 0 #2b2118)'
  : 'none';

export class Sticker {
  a: CanvasRenderingContext2D;
  b: CanvasRenderingContext2D;
  ox = 0; // vị trí điểm khớp trong canvas b
  oy = 0;
  private key = '';
  constructor() {
    this.a = document.createElement('canvas').getContext('2d')!;
    this.b = document.createElement('canvas').getContext('2d')!;
  }
  // vẽ lại khi khung, clip hay cỡ đổi; px = cỡ thật trên màn (đã nhân tỉ lệ màn và dpr)
  render(anim: AolaAnim, clip: string, fi: number, px: number, flip: boolean, outline = true, silhouette = false, noShadow = false) {
    const key = `${anim.dir}|${clip}|${fi}|${px.toFixed(3)}|${flip}|${outline}|${silhouette}|${noShadow}`;
    if (key === this.key) return;
    this.key = key;
    const c = anim.clip(clip);
    const [x0, y0, x1, y1] = c.bounds;
    const pad = 12;
    const w = Math.ceil((x1 - x0) * px) + pad * 2, h = Math.ceil((y1 - y0) * px) + pad * 2;
    for (const g of [this.a, this.b]) {
      if (g.canvas.width !== w || g.canvas.height !== h) {
        g.canvas.width = w;
        g.canvas.height = h;
      } else g.clearRect(0, 0, w, h);
    }
    const ax = (c.anchor[0] - x0) * px + pad, ay = (c.anchor[1] - y0) * px + pad;
    this.oy = ay;
    this.ox = flip ? w - ax : ax;
    const g = this.a;
    g.setTransform(1, 0, 0, 1, 0, 0);
    if (flip) {
      g.translate(w, 0);
      g.scale(-1, 1);
    }
    g.translate(ax, ay);
    anim.drawFrame(g, clip, fi, px, noShadow);
    g.setTransform(1, 0, 0, 1, 0, 0);
    if (silhouette) {
      g.globalCompositeOperation = 'source-in';
      g.fillStyle = '#4a3c30';
      g.fillRect(0, 0, w, h);
      g.globalCompositeOperation = 'source-over';
    }
    const b = this.b;
    b.filter = outline ? OUTLINE : 'none';
    b.drawImage(this.a.canvas, 0, 0);
    b.filter = 'none';
  }
  get canvas() {
    return this.b.canvas;
  }
}

// ảnh chân dung tĩnh (khung đứng đầu), có viền sticker; giữ lại theo cỡ
const portraitCache = new Map<string, Promise<string>>();
export function portrait(dir: string, height: number, silhouette = false): Promise<string> {
  const key = `${dir}|${height}|${silhouette}`;
  let p = portraitCache.get(key);
  if (!p) {
    p = AolaAnim.load(dir).then((a) => {
      if (!a) return '';
      const st = new Sticker();
      const px = (height * 0.86) / a.idleH;
      st.render(a, IDLE, 0, px, false, true, silhouette);
      return st.canvas.toDataURL();
    });
    portraitCache.set(key, p);
  }
  return p;
}
