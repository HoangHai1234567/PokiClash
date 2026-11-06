// Phần dùng chung của màn boot: 5 tướng khởi đầu, tướng cử động (aola), logo sticker, thanh tải bút chì, lời nhắc chạm, nạp trước.
import { HERO } from '../../core/data/heroes';
import { ELEM_COLOR } from '../../core/elements';
import type { Elem } from '../../core/types';
import { AolaAnim, IDLE, Sticker } from '../aola';
import { app } from '../app';
import { h } from '../dom';
import { icon } from '../icons';

export const UNITY = '/unity/'; // Assets/03 Art của Unity (vite.config.ts)
export const INK = '#2b2118';

// thứ tự khắc: Thủy → Hỏa → Kim → Mộc → Thổ → Thủy (cũng là thứ tự đảo)
export const CYCLE: Elem[] = ['thuy', 'hoa', 'kim', 'moc', 'tho'];
const STARTER_ID: Record<Elem, string> = { thuy: 'giot_suong', hoa: 'su_tu_lua', kim: 'bu_long', moc: 'nu_hoa', tho: 'thach_nhan' };
export interface Starter { elem: Elem; id: string; name: string; aola: string; color: string }
export const STARTERS: Record<Elem, Starter> = Object.fromEntries(
  CYCLE.map((e) => {
    const hd = HERO[STARTER_ID[e]];
    return [e, { elem: e, id: hd.id, name: hd.name, aola: hd.forms[0].aola, color: ELEM_COLOR[e] }];
  }),
) as Record<Elem, Starter>;

export const PEDESTAL = (e: Elem) => `${UNITY}Islands/be_${e}.png`;
export const WORLD_IMG = `${UNITY}Islands/world.png`;

export const TIPS = [
  'Thủy khắc Hỏa, Hỏa khắc Kim, Kim khắc Mộc, Mộc khắc Thổ, Thổ khắc Thủy.',
  'Đánh vào hệ mình khắc: sát thương ×1,5. Bị khắc thì chỉ còn ×0,75.',
  'Mỗi lượt chọn 5 lần, mỗi lần 1 trong 3 thẻ.',
  'Chiêu và Tuyệt kỹ không tốn lần chọn, chỉ tốn mana và nộ.',
  'Ải đã qua tự đánh ra bi khi bạn vắng mặt.',
  'Cấp người chơi cũng là cấp của mọi tướng.',
  'Gom đủ mảnh để thu phục tướng mới.',
];

// ---------- tướng cử động: vẽ clip aola vào canvas, viền sticker ----------
export class Puppet {
  el: HTMLCanvasElement;
  anim: AolaAnim | null = null;
  private st = new Sticker();
  private clip = IDLE;
  private t = Math.random() * 3;
  private after: (() => void) | null = null;
  constructor(
    public dir: string,
    public w: number,
    public hgt: number,
    public opt: { flip?: boolean; body?: number; foot?: number; className?: string } = {},
  ) {
    this.el = h('canvas', { class: `bt-puppet ${opt.className ?? ''}`, style: `width:${w}px;height:${hgt}px` }) as HTMLCanvasElement;
    void AolaAnim.load(dir).then((a) => (this.anim = a));
  }
  play(clip: string, then?: () => void) {
    if (!this.anim) return then?.();
    this.clip = clip;
    this.t = 0;
    this.after = then ?? null;
  }
  tick(dt: number) {
    this.t += dt;
    const pr = (window.devicePixelRatio || 1) * app.scale;
    const W = Math.round(this.w * pr), H = Math.round(this.hgt * pr);
    const cv = this.el;
    if (cv.width !== W || cv.height !== H) {
      cv.width = W;
      cv.height = H;
    }
    const g = cv.getContext('2d')!;
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.clearRect(0, 0, W, H);
    const a = this.anim;
    if (!a) return;
    const c = a.clip(this.clip);
    const loop = this.clip === IDLE;
    const fi = a.frameAt(this.clip, this.t, loop);
    if (!loop && fi >= c.frames.length - 1) {
      this.clip = IDLE;
      this.t = 0;
      const f = this.after;
      this.after = null;
      f?.();
    }
    const px = (H * (this.opt.body ?? 0.8)) / a.idleH;
    this.st.render(a, this.clip, fi, px, !!this.opt.flip, true, false, true); // UI không vẽ bóng dưới chân
    g.drawImage(this.st.canvas, W / 2 - this.st.ox, H * (this.opt.foot ?? 0.93) - this.st.oy);
  }
}

// một vòng requestAnimationFrame cho mọi thứ cử động trong màn boot
export class Ticker {
  private fns = new Set<(dt: number, t: number) => void>();
  private raf = 0;
  private last = 0;
  private t0 = 0;
  add(f: (dt: number, t: number) => void) {
    this.fns.add(f);
    return () => this.fns.delete(f);
  }
  start() {
    this.t0 = performance.now();
    const loop = (now: number) => {
      const dt = Math.min(0.05, (now - (this.last || now)) / 1000);
      this.last = now;
      for (const f of this.fns) f(dt, (now - this.t0) / 1000);
      this.raf = requestAnimationFrame(loop);
    };
    this.raf = requestAnimationFrame(loop);
  }
  stop() {
    cancelAnimationFrame(this.raf);
    this.fns.clear();
  }
}

// ---------- logo: chữ sticker, viền trắng giấy xé, chữ CLASH tô 5 màu hệ theo vòng khắc ----------
export function logoSvg(id: string, width = 400): string {
  const W = 420, H = 236;
  const torn = `${id}-torn`, hatch = `${id}-hatch`;
  const clashCol = CYCLE.map((e) => ELEM_COLOR[e]);
  const row = (txt: string, x: number, y: number, size: number, rot: number[], dy: number[], fills: string[], ls: number) => {
    const spans = (fill: (i: number) => string) =>
      [...txt].map((ch, i) => `<tspan fill="${fill(i)}">${ch}</tspan>`).join('');
    const base = `x="${x}" y="${y}" font-size="${size}" rotate="${rot.join(' ')}" dy="${dy.join(' ')}" letter-spacing="${ls}" text-anchor="middle" font-family="'Baloo 2', sans-serif" font-weight="800" stroke-linejoin="round" stroke-linecap="round"`;
    return `
      <g filter="url(#${torn})">
        <text ${base} stroke="${INK}" stroke-width="${size * 0.36}" fill="${INK}">${spans(() => INK)}</text>
        <text ${base} stroke="#fffaf0" stroke-width="${size * 0.3}" fill="#fffaf0">${spans(() => '#fffaf0')}</text>
      </g>
      <text ${base} stroke="${INK}" stroke-width="${size * 0.13}" paint-order="stroke fill" fill="${INK}">${spans((i) => fills[i % fills.length])}</text>
      <text ${base} fill="url(#${hatch})">${spans(() => `url(#${hatch})`)}</text>`;
  };
  return `<svg class="bt-logo" viewBox="0 0 ${W} ${H}" width="${width}" height="${(width * H) / W}" overflow="visible">
    <defs>
      <filter id="${torn}" x="-10%" y="-10%" width="120%" height="120%">
        <feTurbulence type="fractalNoise" baseFrequency="0.09" numOctaves="2" seed="7"/>
        <feDisplacementMap in="SourceGraphic" scale="6" xChannelSelector="R" yChannelSelector="G"/>
      </filter>
      <pattern id="${hatch}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(-55)">
        <rect width="2.4" height="7" fill="rgba(255,255,255,.3)"/>
      </pattern>
    </defs>
    ${row('Poki', 150, 82, 74, [-9, 4, -6, 8], [0, -3, 5, -6], ['#f7c948', '#f7c948', '#f7c948', '#f7c948'], -1)}
    ${row('CLASH', 222, 200, 118, [-6, 3, -3, 5, -4], [0, -5, 8, -6, 5], clashCol, -3)}
    <g fill="none" stroke="${INK}" stroke-width="4.5" stroke-linecap="round">
      <path d="M34 120l-18-9M38 141l-24 2M44 100l-12-17"/>
      <path d="M392 108l20-12M398 132l24 1M386 86l12-18"/>
    </g>
  </svg>`;
}

// ---------- thanh tải: khung vẽ tay, tô sáp 5 màu, bút chì chạy theo ----------
export function loaderEl() {
  const fill = h('i', { class: 'bt-bar-fill' });
  const pencil = h('span', { class: 'bt-bar-pencil', html: icon('pencil', 34) });
  const pct = h('span', { class: 'bt-bar-pct' }, '0%');
  const tip = h('div', { class: 'bt-tip' });
  const el = h('div', { class: 'bt-load' }, h('div', { class: 'bt-bar' }, fill, pencil), h('div', { class: 'row', style: 'gap:8px;justify-content:center' }, pct), tip);
  let ti = Math.floor(Math.random() * TIPS.length);
  const showTip = () => {
    tip.innerHTML = `<b>Mẹo:</b> ${TIPS[ti % TIPS.length]}`;
    ti++;
  };
  showTip();
  const tipTimer = window.setInterval(showTip, 2600);
  return {
    el,
    set(p: number) {
      const v = Math.max(0, Math.min(1, p));
      fill.style.width = `${v * 100}%`;
      pencil.style.left = `${v * 100}%`;
      pct.textContent = `${Math.round(v * 100)}%`;
    },
    done() {
      clearInterval(tipTimer);
    },
  };
}

export function tapEl(text = 'Chạm để bắt đầu') {
  return h('div', { class: 'bt-tap' }, h('span', { class: 'bt-tap-t' }, text));
}

// ---------- nạp trước: tướng, ảnh, phông ----------
export function preload(): { progress: () => number; done: Promise<void> } {
  let n = 0;
  const jobs: Promise<unknown>[] = [];
  const add = (p: Promise<unknown>) => jobs.push(p.catch(() => null).finally(() => n++));
  for (const e of CYCLE) add(AolaAnim.load(STARTERS[e].aola));
  for (const src of [WORLD_IMG, ...CYCLE.map(PEDESTAL)]) add(loadImg(src));
  add(document.fonts.load('800 40px "Baloo 2"'));
  add(document.fonts.load('400 20px "Pangolin"'));
  const total = jobs.length;
  return { progress: () => n / total, done: Promise.all(jobs).then(() => undefined) };
}

export function loadImg(src: string): Promise<HTMLImageElement> {
  return new Promise((res, rej) => {
    const im = new Image();
    im.onload = () => res(im);
    im.onerror = rej;
    im.src = src;
  });
}

// ---------- vân gỗ mặt bàn (canvas, sinh một lần) ----------
const woodUrl: Record<number, string> = {};
export function woodTexture(scale = 1): string {
  if (woodUrl[scale]) return woodUrl[scale];
  const c = document.createElement('canvas');
  c.width = 540 * scale;
  c.height = 960 * scale;
  const g = c.getContext('2d')!;
  g.scale(scale, scale);
  const planks = [0, 128, 262, 400, 540];
  const tones = ['#8a5a36', '#7d5031', '#93613a', '#83552f'];
  for (let i = 0; i < planks.length - 1; i++) {
    const x0 = planks[i], x1 = planks[i + 1];
    g.fillStyle = tones[i % tones.length];
    g.fillRect(x0, 0, x1 - x0, 960);
    // vân gỗ: đường lượn sóng dọc tấm
    for (let k = 0; k < 26; k++) {
      const bx = x0 + Math.random() * (x1 - x0);
      g.strokeStyle = `rgba(${Math.random() < 0.5 ? '60,34,18' : '170,120,80'},${0.12 + Math.random() * 0.16})`;
      g.lineWidth = 1 + Math.random() * 2.2;
      g.beginPath();
      const ph = Math.random() * 6, amp = 2 + Math.random() * 6, fr = 0.004 + Math.random() * 0.01;
      for (let y = -10; y <= 970; y += 12) {
        const x = bx + Math.sin(y * fr + ph) * amp;
        if (y === -10) g.moveTo(x, y);
        else g.lineTo(x, y);
      }
      g.stroke();
    }
    // mắt gỗ
    if (Math.random() < 0.9) {
      const kx = x0 + 20 + Math.random() * (x1 - x0 - 40), ky = 80 + Math.random() * 800;
      for (let r = 4; r < 22; r += 4) {
        g.strokeStyle = `rgba(60,34,18,${0.28 - r * 0.01})`;
        g.lineWidth = 1.6;
        g.beginPath();
        g.ellipse(kx, ky, r * 0.6, r * 1.6, 0, 0, Math.PI * 2);
        g.stroke();
      }
    }
    // khe giữa hai tấm: nét mực
    g.fillStyle = 'rgba(43,33,24,0.85)';
    g.fillRect(x1 - 2, 0, 3, 960);
  }
  woodUrl[scale] = c.toDataURL(scale === 1 ? 'image/jpeg' : 'image/png', 0.85);
  return woodUrl[scale];
}

// chạy chuỗi Web Animations rồi chờ xong
export function anim(el: Element, frames: Keyframe[], opt: KeyframeAnimationOptions): Promise<void> {
  const a = el.animate(frames, { fill: 'both', ...opt });
  return a.finished.then(() => undefined).catch(() => undefined);
}

export const ease = {
  out: 'cubic-bezier(.2,.8,.2,1)',
  back: 'cubic-bezier(.34,1.56,.64,1)',
  in: 'cubic-bezier(.6,0,.8,.4)',
  inOut: 'cubic-bezier(.65,0,.35,1)',
};
