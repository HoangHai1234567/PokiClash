// Sân đấu: nền vẽ bút sáp, hai tướng dạng sticker, hiệu ứng chữ tượng thanh, số sát thương, rung màn.
// Địch đứng trên trái (mặt trước, như clip gốc), phe mình dưới phải (lật ngang). Clip đánh lao sang phải-xuống,
// nên quãng lao được nắn lại cho trúng đối thủ.
import { HERO } from '../../core/data/heroes';
import type { ZoneDef } from '../../core/data/stages';
import type { StatusId } from '../../core/types';
import { AolaAnim, ATTACK, HIT, IDLE, SKILL, Sticker } from '../aola';
import { cloud, hill, INK, roughOf, tuft } from '../art';

export const STAGE_W = 540, STAGE_H = 464;
export const POS: [[number, number], [number, number]] = [
  [392, 418], // phe mình (dưới phải)
  [158, 236], // địch (trên trái)
];
const HEIGHT = [176, 150];

interface Actor {
  side: 0 | 1;
  heroId: string;
  size: number; // cỡ của dạng đang hiện (theo sao)
  anim: AolaAnim | null;
  sticker: Sticker;
  clip: string;
  t: number;
  loop: boolean;
  flash: number;
  alpha: number;
  dead: number; // 0 sống; >0 thời gian từ lúc gục
  enter: number; // thời gian từ lúc ra sân
  exit: number; // >0 đang rút lui
  hop: number;
  lunge: number; // cho tướng không lao trong clip: tự nhảy tới
  statuses: [StatusId, number][];
  boss: boolean;
  done?: () => void;
  hitCb?: () => void;
  hitFired: boolean;
}

type Fx =
  | { k: 'text'; x: number; y: number; t: number; life: number; text: string; color: string; size: number; vy: number; rot: number; side?: 0 | 1; lift?: number }
  | { k: 'burst'; x: number; y: number; t: number; life: number; text: string; color: string; size: number; rot: number; seed: number }
  | { k: 'ring'; x: number; y: number; t: number; life: number; color: string; r: number }
  | { k: 'spark'; x: number; y: number; t: number; life: number; color: string; parts: { a: number; v: number; s: number }[] }
  | { k: 'flash'; t: number; life: number; color: string };

const WORDS_HIT = ['BỐP!', 'CHÁT!', 'BỤP!', 'HỰ!', 'BINH!'];
const WORDS_BIG = ['ẦM!!', 'RẦM!!', 'OÀNH!!'];

export class Stage {
  canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private bg: HTMLCanvasElement | null = null;
  private actors: [Actor | null, Actor | null] = [null, null];
  private fx: Fx[] = [];
  private shake = 0;
  private raf = 0;
  private last = 0;
  speed = 1;
  private px = 1; // điểm ảnh thật trên mỗi đơn vị
  private chapter: ZoneDef;

  constructor(chapter: ZoneDef, getScale: () => number) {
    this.chapter = chapter;
    this.canvas = document.createElement('canvas');
    this.canvas.style.cssText = `position:absolute;left:0;top:56px;width:${STAGE_W}px;height:${STAGE_H}px`;
    this.ctx = this.canvas.getContext('2d')!;
    const resize = () => {
      this.px = getScale() * (window.devicePixelRatio || 1);
      this.canvas.width = Math.round(STAGE_W * this.px);
      this.canvas.height = Math.round(STAGE_H * this.px);
      this.bg = null;
    };
    resize();
    window.addEventListener('pc-fit', resize);
    const loop = (now: number) => {
      const dt = Math.min(0.05, (now - (this.last || now)) / 1000);
      this.last = now;
      this.update(dt * this.speed);
      this.draw();
      this.raf = requestAnimationFrame(loop);
    };
    this.raf = requestAnimationFrame(loop);
  }

  destroy() {
    cancelAnimationFrame(this.raf);
  }

  // ---------- tướng ----------
  // form: dạng đang hiện trong dòng tiến hóa (Fighter.form: theo sao, boss tiến hóa thì theo trận), chọn hình và cỡ
  async setActor(side: 0 | 1, heroId: string, boss = false, entering = true, form = 0) {
    const forms = HERO[heroId].forms;
    const fm = forms[Math.min(form, forms.length - 1)];
    const a: Actor = {
      side, heroId, size: fm.size, anim: null, sticker: new Sticker(), clip: IDLE, t: Math.random() * 2, loop: true,
      flash: 0, alpha: 1, dead: 0, enter: entering ? 0 : 9, exit: 0, hop: 0, lunge: 0, statuses: [], boss, hitFired: false,
    };
    this.actors[side] = a;
    a.anim = await AolaAnim.load(fm.aola);
  }

  retreat(side: 0 | 1): Promise<void> {
    const a = this.actors[side];
    if (!a) return Promise.resolve();
    a.exit = 0.0001;
    return new Promise((r) => setTimeout(r, 280 / this.speed));
  }

  setStatuses(side: 0 | 1, st: [StatusId, number][]) {
    const a = this.actors[side];
    if (a) a.statuses = st;
  }

  // chạy clip; onHit gọi lúc trúng đòn; trả về lúc clip xong
  play(side: 0 | 1, clip: string, onHit?: () => void): Promise<void> {
    const a = this.actors[side];
    if (!a || !a.anim || a.dead) {
      onHit?.();
      return new Promise((r) => setTimeout(r, 300 / this.speed));
    }
    a.done?.();
    a.clip = clip;
    a.t = 0;
    a.loop = false;
    a.hitCb = onHit;
    a.hitFired = !onHit;
    a.lunge = 0;
    return new Promise((r) => {
      a.done = r;
    });
  }

  hurt(side: 0 | 1, big = false) {
    const a = this.actors[side];
    if (!a || a.dead) return;
    a.flash = 0.16;
    this.shake = Math.max(this.shake, big ? 12 : 6);
    if (a.clip === IDLE || a.clip === HIT) {
      a.clip = HIT;
      a.t = 0;
      a.loop = false;
    }
  }

  dodge(side: 0 | 1) {
    const a = this.actors[side];
    if (a) a.hop = 0.0001;
  }

  die(side: 0 | 1) {
    const a = this.actors[side];
    if (a) a.dead = 0.0001;
  }

  head(side: 0 | 1): [number, number] {
    const [x, y] = POS[side];
    const a = this.actors[side];
    const hh = HEIGHT[side] * (a ? a.size : 1);
    return [x, y - hh * 0.85];
  }
  body(side: 0 | 1): [number, number] {
    const [x, y] = POS[side];
    const a = this.actors[side];
    const hh = HEIGHT[side] * (a ? a.size : 1);
    return [x, y - hh * 0.45];
  }

  // ---------- hiệu ứng ----------
  // chữ ra liền nhau thì xếp tầng xuống dưới, không chồng lên nhau
  text(side: 0 | 1, text: string, color: string, size = 26, dy = 0) {
    const [x, y] = this.head(side);
    // dòng tin: chữ mới hiện ở chỗ cũ, chữ trước bị đẩy lên một dòng
    for (const f of this.fx) if (f.k === 'text' && f.side === side) f.lift = (f.lift ?? 0) + size + 6;
    const sx = side === 1 ? Math.min(x, 200) : Math.max(x, 330);
    this.fx.push({ k: 'text', x: sx, y: y + dy + 20, t: 0, life: 1.25, text, color, size, vy: -18, rot: (Math.random() - 0.5) * 0.08, side, lift: 0 });
  }
  number(side: 0 | 1, n: number, color: string, big = false) {
    const [x, y] = this.body(side);
    this.fx.push({ k: 'text', x: x + (Math.random() - 0.5) * 60, y: y - 10, t: 0, life: 1.0, text: String(n), color, size: big ? 46 : 34, vy: -70, rot: (Math.random() - 0.5) * 0.3 });
  }
  burst(side: 0 | 1, big: boolean, word?: string) {
    const [x, y] = this.body(side);
    const w = word ?? (big ? WORDS_BIG : WORDS_HIT)[Math.floor(Math.random() * (big ? WORDS_BIG.length : WORDS_HIT.length))];
    this.fx.push({ k: 'burst', x: x + (Math.random() - 0.5) * 30, y: y - 20, t: 0, life: 0.6, text: w, color: big ? '#ffd24a' : '#fff6c8', size: big ? 1.35 : 1, rot: (Math.random() - 0.5) * 0.5, seed: Math.random() * 100 });
    this.spark(side, big ? '#ffd24a' : '#fff');
  }
  ring(side: 0 | 1, color: string) {
    const [x, y] = this.body(side);
    this.fx.push({ k: 'ring', x, y, t: 0, life: 0.6, color, r: 70 });
  }
  spark(side: 0 | 1, color: string) {
    const [x, y] = this.body(side);
    this.fx.push({ k: 'spark', x, y, t: 0, life: 0.45, color, parts: Array.from({ length: 9 }, () => ({ a: Math.random() * Math.PI * 2, v: 120 + Math.random() * 160, s: 6 + Math.random() * 8 })) });
  }
  flash(color = '#fff') {
    this.fx.push({ k: 'flash', t: 0, life: 0.35, color });
  }

  // ---------- cập nhật ----------
  private update(dt: number) {
    for (const a of this.actors) {
      if (!a) continue;
      a.t += dt;
      a.flash = Math.max(0, a.flash - dt);
      if (a.enter < 9) a.enter += dt;
      if (a.exit > 0) a.exit += dt;
      if (a.hop > 0) a.hop = a.hop > 0.5 ? 0 : a.hop + dt;
      if (a.dead > 0) a.dead += dt;
      if (a.anim && !a.loop) {
        const c = a.anim.clip(a.clip);
        const fi = Math.floor(a.t * a.anim.fps);
        if (!a.hitFired && fi >= c.hit) {
          a.hitFired = true;
          a.hitCb?.();
        }
        if (fi >= c.frames.length) {
          if (!a.hitFired) {
            a.hitFired = true;
            a.hitCb?.();
          }
          a.clip = IDLE;
          a.t = 0;
          a.loop = true;
          const d = a.done;
          a.done = undefined;
          d?.();
        }
      }
    }
    this.shake = Math.max(0, this.shake - dt * 40);
    this.fx = this.fx.filter((f) => (f.t += dt) < f.life);
  }

  // ---------- vẽ ----------
  private draw() {
    const g = this.ctx, px = this.px;
    g.setTransform(1, 0, 0, 1, 0, 0);
    if (!this.bg) this.bg = this.paintBg();
    const sx = (Math.random() - 0.5) * this.shake * px, sy = (Math.random() - 0.5) * this.shake * px;
    g.clearRect(0, 0, this.canvas.width, this.canvas.height);
    g.drawImage(this.bg, sx, sy);
    g.setTransform(px, 0, 0, px, sx, sy);
    // địch vẽ trước (xa hơn)
    for (const side of [1, 0] as const) this.drawActor(side);
    for (const f of this.fx) this.drawFx(f);
  }

  private drawActor(side: 0 | 1) {
    const a = this.actors[side];
    if (!a) return;
    const g = this.ctx, px = this.px;
    const hero = HERO[a.heroId];
    let [x, y] = POS[side];
    // ra sân: rơi từ trên xuống, nảy nhẹ
    if (a.enter < 0.45) {
      const k = a.enter / 0.45;
      y -= (1 - k) * (1 - k) * 260;
    }
    let alpha = 1;
    if (a.exit > 0) {
      alpha = Math.max(0, 1 - a.exit / 0.28);
      x += (side === 0 ? 1 : -1) * a.exit * 500;
    }
    if (a.hop > 0) y -= Math.sin((a.hop / 0.5) * Math.PI) * 40;
    let rot = 0;
    if (a.dead > 0) {
      const k = Math.min(1, a.dead / 0.7);
      alpha = 1 - k * 0.85;
      rot = (side === 0 ? 1 : -1) * k * 1.25;
      y += k * 12;
    }
    if (a.dead > 1.4) return;
    // bóng
    g.save();
    g.globalAlpha = 0.35 * alpha;
    g.fillStyle = INK;
    g.beginPath();
    g.ellipse(x, POS[side][1] + 2, 46 * a.size * (side === 0 ? 1.15 : 1), 11 * a.size, 0, 0, Math.PI * 2);
    g.fill();
    g.restore();
    if (!a.anim) {
      g.save();
      g.fillStyle = '#ddd';
      g.strokeStyle = INK;
      g.lineWidth = 3;
      g.beginPath();
      g.ellipse(x, y - 60, 40, 60, 0, 0, Math.PI * 2);
      g.fill();
      g.stroke();
      g.restore();
      return;
    }
    const anim = a.anim;
    const flip = side === 0;
    const scale = (HEIGHT[side] * a.size * (a.boss ? 1.18 : 1)) / anim.idleH;
    const fi = anim.frameAt(a.clip, a.t, a.loop);
    a.sticker.render(anim, a.clip, fi, scale * px, flip, true, false);
    // quãng lao: thay chuyển động trong clip bằng đường tới đối thủ
    let ox = 0, oy = 0;
    if (a.clip === ATTACK) {
      const c = anim.clip(ATTACK);
      const other = POS[side === 0 ? 1 : 0];
      const tx = (other[0] - POS[side][0]) * 0.72, ty = (other[1] - POS[side][1]) * 0.72;
      const d = c.disp[fi] ?? [0, 0], pk = c.disp[c.peak] ?? [0, 0];
      const mx = (flip ? -d[0] : d[0]) * scale, my = d[1] * scale;
      const Mx = (flip ? -pk[0] : pk[0]) * scale, My = pk[1] * scale;
      const M = Math.hypot(Mx, My);
      if (M > 30) {
        const k = Math.hypot(tx, ty) / M;
        const ang = Math.atan2(ty, tx) - Math.atan2(My, Mx);
        const cs = Math.cos(ang) * k, sn = Math.sin(ang) * k;
        ox = mx * cs - my * sn - mx;
        oy = mx * sn + my * cs - my;
      } else {
        // clip bắn từ xa: tự nhún tới một đoạn
        const n = c.frames.length;
        const u = Math.min(1, fi / Math.max(1, c.hit));
        const back = fi > c.hit ? Math.min(1, (fi - c.hit) / Math.max(1, n - c.hit)) : 0;
        const lunge = Math.sin(u * Math.PI * 0.5) * (1 - back) * 0.35;
        ox = tx * lunge;
        oy = ty * lunge;
      }
    }
    const cv = a.sticker.canvas;
    g.save();
    g.globalAlpha = alpha;
    g.translate(x + ox, y + oy);
    if (rot) g.rotate(rot);
    if (a.dead > 0) g.filter = 'grayscale(1)';
    g.drawImage(cv, -a.sticker.ox / px, -a.sticker.oy / px, cv.width / px, cv.height / px);
    g.filter = 'none';
    if (a.flash > 0) {
      g.globalCompositeOperation = 'lighter';
      g.globalAlpha = Math.min(1, a.flash * 5) * 0.65;
      g.drawImage(cv, -a.sticker.ox / px, -a.sticker.oy / px, cv.width / px, cv.height / px);
      g.globalCompositeOperation = 'source-over';
    }
    g.restore();
    // trạng thái trên đầu
    if (!a.dead && a.statuses.length) this.drawStatuses(a, x, y - HEIGHT[side] * a.size * (a.boss ? 1.18 : 1) - 8);
  }

  private drawStatuses(a: Actor, x: number, y: number) {
    const g = this.ctx;
    const t = performance.now() / 1000;
    for (const [id] of a.statuses) {
      if (id === 'stun') {
        for (let i = 0; i < 3; i++) {
          const ang = t * 3 + (i * Math.PI * 2) / 3;
          this.star(x + Math.cos(ang) * 30, y + Math.sin(ang) * 8, 8, '#ffd24a');
        }
      }
      if (id === 'burn') {
        for (let i = 0; i < 3; i++) {
          const fx = x - 26 + i * 26, fy = y + 30 + Math.sin(t * 8 + i) * 3;
          g.save();
          g.fillStyle = '#f58a2e';
          g.strokeStyle = INK;
          g.lineWidth = 2;
          g.beginPath();
          g.moveTo(fx, fy - 14);
          g.quadraticCurveTo(fx + 9, fy - 2, fx + 6, fy + 4);
          g.quadraticCurveTo(fx, fy + 9, fx - 6, fy + 4);
          g.quadraticCurveTo(fx - 9, fy - 2, fx, fy - 14);
          g.fill();
          g.stroke();
          g.restore();
        }
      }
      if (id === 'regen') {
        g.save();
        g.font = `800 18px "Baloo 2"`;
        g.fillStyle = '#6cbf4f';
        g.strokeStyle = INK;
        g.lineWidth = 4;
        g.textAlign = 'center';
        const yy = y + 20 - ((t * 30) % 30);
        g.strokeText('+', x + 34, yy);
        g.fillText('+', x + 34, yy);
        g.restore();
      }
      if (id === 'evade') {
        g.save();
        g.globalAlpha = 0.5 + Math.sin(t * 6) * 0.2;
        g.strokeStyle = '#9a6ad6';
        g.lineWidth = 3;
        g.setLineDash([6, 6]);
        g.beginPath();
        g.ellipse(x, y + 80, 60, 90, 0, 0, Math.PI * 2);
        g.stroke();
        g.restore();
      }
    }
  }

  private star(x: number, y: number, r: number, color: string) {
    const g = this.ctx;
    g.save();
    g.fillStyle = color;
    g.strokeStyle = INK;
    g.lineWidth = 2;
    g.beginPath();
    for (let i = 0; i < 10; i++) {
      const rr = i % 2 ? r * 0.45 : r;
      const a = -Math.PI / 2 + (i * Math.PI) / 5;
      g.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr);
    }
    g.closePath();
    g.fill();
    g.stroke();
    g.restore();
  }

  private drawFx(f: Fx) {
    const g = this.ctx;
    const k = f.t / f.life;
    g.save();
    switch (f.k) {
      case 'text': {
        const pop = k < 0.15 ? 0.5 + (k / 0.15) * 0.7 : k < 0.25 ? 1.2 - ((k - 0.15) / 0.1) * 0.2 : 1;
        g.globalAlpha = k > 0.7 ? 1 - (k - 0.7) / 0.3 : 1;
        g.translate(f.x, f.y + f.vy * f.t - (f.lift ?? 0));
        g.rotate(f.rot);
        g.scale(pop, pop);
        g.font = `800 ${f.size}px "Baloo 2"`;
        g.textAlign = 'center';
        g.textBaseline = 'middle';
        g.lineJoin = 'round';
        g.lineWidth = f.size / 5;
        g.strokeStyle = INK;
        g.strokeText(f.text, 0, 0);
        g.fillStyle = f.color;
        g.fillText(f.text, 0, 0);
        break;
      }
      case 'burst': {
        const pop = k < 0.2 ? 0.3 + (k / 0.2) * 0.9 : 1.2 - Math.min(0.2, (k - 0.2) * 0.5);
        g.globalAlpha = k > 0.75 ? 1 - (k - 0.75) / 0.25 : 1;
        g.translate(f.x, f.y);
        g.rotate(f.rot);
        g.scale(pop * f.size, pop * f.size);
        // ngôi sao răng cưa kiểu truyện tranh
        g.beginPath();
        const n = 13;
        for (let i = 0; i < n * 2; i++) {
          const r = i % 2 ? 28 + ((i * 7 + f.seed) % 9) : 52 + ((i * 13 + f.seed) % 14);
          const a = (i * Math.PI) / n;
          g.lineTo(Math.cos(a) * r * 1.25, Math.sin(a) * r * 0.85);
        }
        g.closePath();
        g.fillStyle = f.color;
        g.strokeStyle = INK;
        g.lineWidth = 3.5;
        g.lineJoin = 'round';
        g.fill();
        g.stroke();
        g.font = `800 26px "Baloo 2"`;
        g.textAlign = 'center';
        g.textBaseline = 'middle';
        g.lineWidth = 6;
        g.strokeText(f.text, 0, 2);
        g.fillStyle = '#e8553f';
        g.fillText(f.text, 0, 2);
        break;
      }
      case 'ring': {
        g.globalAlpha = 1 - k;
        g.strokeStyle = f.color;
        g.lineWidth = 6 * (1 - k) + 1;
        g.setLineDash([10, 7]);
        g.beginPath();
        g.ellipse(f.x, f.y, f.r * (0.3 + k), f.r * 0.6 * (0.3 + k), 0, 0, Math.PI * 2);
        g.stroke();
        break;
      }
      case 'spark': {
        g.globalAlpha = 1 - k;
        g.strokeStyle = INK;
        g.lineCap = 'round';
        for (const p of f.parts) {
          const d = p.v * f.t;
          const x = f.x + Math.cos(p.a) * d, y = f.y + Math.sin(p.a) * d;
          g.lineWidth = 5;
          g.beginPath();
          g.moveTo(x, y);
          g.lineTo(x + Math.cos(p.a) * p.s, y + Math.sin(p.a) * p.s);
          g.stroke();
          g.strokeStyle = f.color;
          g.lineWidth = 2.5;
          g.stroke();
          g.strokeStyle = INK;
        }
        break;
      }
      case 'flash': {
        g.globalAlpha = (1 - k) * 0.7;
        g.fillStyle = f.color;
        g.fillRect(0, 0, STAGE_W, STAGE_H);
        break;
      }
    }
    g.restore();
  }

  // ---------- nền ----------
  private paintBg(): HTMLCanvasElement {
    const c = document.createElement('canvas');
    c.width = this.canvas.width;
    c.height = this.canvas.height;
    const g = c.getContext('2d')!;
    const px = this.px;
    g.scale(px, px);
    const ch = this.chapter;
    const sky = g.createLinearGradient(0, 0, 0, STAGE_H);
    sky.addColorStop(0, ch.sky[0]);
    sky.addColorStop(0.75, ch.sky[1]);
    g.fillStyle = sky;
    g.fillRect(0, 0, STAGE_W, STAGE_H);
    // vệt màu nước
    for (let i = 0; i < 14; i++) {
      const x = Math.random() * STAGE_W, y = Math.random() * 220, r = 30 + Math.random() * 80;
      const rg = g.createRadialGradient(x, y, 0, x, y, r);
      rg.addColorStop(0, 'rgba(255,255,255,0.35)');
      rg.addColorStop(1, 'rgba(255,255,255,0)');
      g.fillStyle = rg;
      g.fillRect(x - r, y - r, r * 2, r * 2);
    }
    const tmp = document.createElement('canvas');
    tmp.width = c.width;
    tmp.height = c.height;
    const tg = tmp.getContext('2d')!;
    tg.scale(px, px);
    const rc = roughOf(tmp);
    // mặt trời
    rc.circle(486, 52, 56, { stroke: INK, strokeWidth: 2.2, fill: '#ffe08a', fillStyle: 'solid', roughness: 1.3, seed: 3 });
    for (let i = 0; i < 10; i++) {
      const a = (i / 10) * Math.PI * 2;
      rc.line(486 + Math.cos(a) * 36, 52 + Math.sin(a) * 36, 486 + Math.cos(a) * 48, 52 + Math.sin(a) * 48, { stroke: INK, strokeWidth: 2, roughness: 1.2, seed: i + 5 });
    }
    cloud(rc, 300, 70, 0.75, 11);
    cloud(rc, 60, 120, 0.55, 17);
    cloud(rc, 420, 150, 0.45, 23);
    const sea = ch.id === 'thuy' || ch.id === 'kim';
    hill(rc, STAGE_W, 230, 22, sea ? '#b9a6e6' : '#b8dca0', 2, STAGE_H);
    if (sea) {
      for (let y = 270; y < STAGE_H; y += 26)
        for (let x = (y / 26) % 2 ? 10 : 40; x < STAGE_W; x += 70)
          rc.arc(x, y, 36, 16, Math.PI, Math.PI * 2, false, { stroke: '#5a7fb8', strokeWidth: 1.8, roughness: 1, seed: x + y });
    }
    hill(rc, STAGE_W, 300, 14, ch.ground, 7, STAGE_H);
    // bệ đứng
    rc.ellipse(POS[1][0], POS[1][1] + 4, 210, 50, { stroke: INK, strokeWidth: 2.4, fill: sea ? '#e9e0c8' : '#d9c48e', fillStyle: 'cross-hatch', hachureGap: 6, roughness: 1.4, seed: 31 });
    rc.ellipse(POS[0][0], POS[0][1] + 6, 270, 64, { stroke: INK, strokeWidth: 2.6, fill: sea ? '#e9e0c8' : '#d9c48e', fillStyle: 'cross-hatch', hachureGap: 6, roughness: 1.4, seed: 37 });
    for (let i = 0; i < 9; i++) tuft(rc, 20 + Math.random() * 500, 320 + Math.random() * 140, i * 7, sea ? '#4b7aa8' : '#3f8f33');
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.drawImage(tmp, 0, 0);
    return c;
  }
}
