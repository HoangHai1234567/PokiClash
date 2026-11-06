// Thành phần của bộ UI Sa Bàn, dựng bằng DOM. Mỗi thành phần cử động: bọc ngoài chạy idle/breath (CSS), phần tử trong nhận punch.
import { cardText } from '../core/cardtext';
import { ELEM_COLOR, ELEM_NAME, RARITY_COLOR, RARITY_NAME } from '../core/elements';
import { HERO } from '../core/data/heroes';
import type { CardDef, Elem } from '../core/types';
import { AolaAnim, IDLE, portrait, Sticker } from '../view/aola';
import { h } from '../view/dom';
import { icon } from '../view/icons';
import { sfx } from '../view/sfx';
import { countTo, phase, pressable, punch, shake, spawn } from './fx';

export const kit = { scale: 1 }; // tỉ lệ khung điện thoại trên màn (main.ts đặt)

type Color = 'red' | 'green' | 'blue' | 'yellow' | 'purple' | 'orange' | 'paper';

// ---------- nút ----------
export function button(label: string, opts: { color?: Color; size?: 'big' | 'small' | 'tiny'; icon?: string; cost?: string; breath?: boolean; disabled?: boolean; onTap?: () => void } = {}) {
  const b = h('button', { class: `k-btn ${opts.color ?? 'red'} ${opts.size ?? ''}` },
    opts.icon ? h('span', { html: icon(opts.icon, opts.size === 'big' ? 34 : 26) }) : null,
    label,
    opts.cost ? h('span', { class: 'k-cost' }, opts.cost) : null);
  if (opts.disabled) b.setAttribute('disabled', '');
  pressable(b, () => opts.onTap?.());
  const w = h('span', { class: opts.breath ? 'k-breath' : '', style: 'display:inline-block' }, b);
  return w;
}

// nút tròn sticker (viền trắng + viền mực, lõi màu), có nhãn băng keo bên dưới và chấm đỏ
export function round(iconName: string, opts: { color?: string; size?: 'big' | 'small'; label?: string; dot?: number | string; breath?: boolean; onTap?: () => void } = {}) {
  const sz = opts.size === 'big' ? 54 : opts.size === 'small' ? 28 : 36;
  const b = h('button', { class: `k-round ${opts.size ?? ''}`, style: `--c:${opts.color ?? '#fffaf0'}` }, h('i', { html: icon(iconName, sz) }));
  if (opts.dot !== undefined) {
    const dot = h('span', { class: 'k-dot k-breath', style: '--bs:1.18;--bd:1.6s' }, String(opts.dot));
    b.appendChild(dot);
  }
  pressable(b, () => opts.onTap?.());
  const col = h('div', { class: 'col', style: 'align-items:center' }, h('span', { class: opts.breath ? 'k-breath' : '', style: 'display:inline-block;--bs:1.06' }, b));
  if (opts.label) col.appendChild(h('span', { class: 'k-navlabel' }, opts.label));
  return col;
}

// ---------- chip tài nguyên, vòng cấp ----------
export function chip(iconName: string, value: number) {
  const num = h('span', { class: 'k-num' }, value.toLocaleString('vi-VN'));
  const el = h('div', { class: 'k-chip', html: icon(iconName, 50) }, num);
  let v = value;
  return {
    el,
    set(nv: number) {
      countTo(num, v, nv);
      punch(el, 0.6);
      v = nv;
    },
  };
}

export function lvRing(level: number, progress: number) {
  const C = 2 * Math.PI * 23;
  const el = h('div', { class: 'k-lv', html: `<svg viewBox="0 0 62 62"><circle cx="31" cy="31" r="28" fill="#fffaf0" stroke="#2b2118" stroke-width="3"/>
    <circle cx="31" cy="31" r="20" fill="#ffe9a8" stroke="#2b2118" stroke-width="2.5"/>
    <circle class="arc" cx="31" cy="31" r="23" fill="none" stroke="#b783e6" stroke-width="5" stroke-linecap="round" transform="rotate(-90 31 31)" stroke-dasharray="${C * progress} ${C}"/></svg>` },
  h('b', {}, h('small', {}, 'CẤP'), String(level)));
  return el;
}

// ---------- thanh ----------
export function bar(color: '' | 'blue' | 'orange' | 'purple', value: number, max: number, showText = true) {
  const ghost = h('i', { class: 'ghost' });
  const fill = h('i', { class: 'fill' });
  const txt = h('span', {});
  const el = h('div', { class: `k-bar ${color}` }, ghost, fill, txt);
  let cur = value;
  const set = (v: number) => {
    const p = Math.max(0, Math.min(1, v / max)) * 100;
    fill.style.width = `${p}%`;
    if (v < cur) ghost.style.width = `${p}%`;
    else {
      ghost.style.transition = 'none';
      ghost.style.width = `${p}%`;
      void ghost.offsetWidth;
      ghost.style.transition = '';
    }
    txt.textContent = showText ? `${Math.round(v)}/${max}` : '';
    cur = v;
  };
  // lần đầu: vệt vàng theo luôn
  fill.style.width = ghost.style.width = `${(value / max) * 100}%`;
  txt.textContent = showText ? `${value}/${max}` : '';
  return { el, set, get value() { return cur; } };
}

// ---------- nhãn ----------
export function tag(e: Elem) {
  return h('span', { class: 'k-tag', style: `--c:${ELEM_COLOR[e]}` }, h('span', { html: icon(`e_${e}`, 20) }), ELEM_NAME[e]);
}

export function rarity(r: CardDef['rarity']) {
  return h('span', { class: 'k-rar', style: `color:${RARITY_COLOR[r]}` }, RARITY_NAME[r]);
}

// sao: hiện lần lượt, sao sáng nảy
export function stars(n: number, max = 5, size = 22, animate = true) {
  const el = h('span', { class: 'k-stars' });
  for (let i = 0; i < max; i++) {
    const s = h('span', { html: icon(i < n ? 'star' : 'starOff', size), style: 'display:inline-block' });
    el.appendChild(s);
    if (animate && i < n) spawn(s, 120 + i * 110);
  }
  return el;
}

// ---------- khung, tiêu đề mục, băng keo ----------
export function panel(kids: (Node | null)[], opts: { kraft?: boolean; tapes?: ('y' | 'p' | 'b' | 'g')[]; style?: string } = {}) {
  const el = h('div', { class: `k-panel ${opts.kraft ? 'kraft' : ''}`, style: opts.style ?? '' }, ...kids);
  (opts.tapes ?? ['y']).forEach((t, i) => {
    const left = i === 0 ? -18 : undefined;
    el.appendChild(h('i', { class: `k-tape ${t === 'y' ? '' : t}`, style: `${left !== undefined ? `left:${left}px;` : 'right:-18px;'}top:-10px;transform:rotate(${i === 0 ? -24 : 22}deg)` }));
  });
  return el;
}

export function head(text: string, color: '' | 'p' | 'b' | 'g' = '', small?: string) {
  return h('div', { class: `k-head ${color}` }, text, small ? h('small', {}, small) : null);
}

// ---------- thẻ bài ----------
export function card(c: CardDef, kind: 'pool' | 'skill' | 'ult' = 'pool') {
  const inner = h('div', { class: `k-card ${kind === 'pool' ? c.rarity : kind}` },
    h('div', { class: 'band' }),
    h('div', { class: 'ico', html: icon(c.icon, 46) }),
    h('div', { class: 'nm' }, c.name),
    h('div', { class: 'tx' }, cardText(c)),
    h('div', { class: 'rr' }, kind === 'pool' ? RARITY_NAME[c.rarity] : kind === 'skill' ? 'Chiêu' : 'Tuyệt kỹ'));
  const w = phase(h('div', { class: 'k-cardw k-idle', style: '--iy:-6px;--ir:1deg' }, inner), 3.4, 1);
  return { el: w, inner };
}

// ---------- ô tướng ----------
export function heroTile(id: string, opts: { star?: number; power?: number; locked?: boolean; dot?: boolean; onTap?: () => void } = {}) {
  const hd = HERO[id];
  const img = h('img', { alt: '' }) as HTMLImageElement;
  void portrait(hd.forms[0].aola, 220, !!opts.locked).then((src) => { if (src) img.src = src; });
  const tile = h('div', { class: `k-hero ${opts.locked ? 'locked' : ''}`, style: `--c:${ELEM_COLOR[hd.elem]}` },
    h('div', { class: 'band' }),
    img,
    h('div', { class: 'nm k-stk-sm' }, hd.name),
    h('div', { class: 'meta' }, tag(hd.elem), opts.locked ? h('span', { class: 'k-note', style: 'margin:0' }, '0/10 mảnh') : h('span', { class: 'pw' }, `⚔ ${opts.power ?? 1000}`)),
    opts.locked ? null : h('div', { style: 'margin-top:4px' }, stars(opts.star ?? 1, 5, 18, false)));
  if (opts.dot) tile.appendChild(h('span', { class: 'k-dot k-wiggle', style: 'transform-origin:50% 100%' }, '!'));
  pressable(tile, () => (opts.locked ? shake(tile) : opts.onTap?.()), { burst: !opts.locked });
  return phase(h('div', { class: 'k-herow k-idle', style: '--iy:-3px;--ir:.5deg' }, tile), 3.8, 1.2);
}

// tướng cử động (clip aola) trên canvas, viền sticker; chạy bằng vòng rAF chung
const puppets = new Set<HeroPuppet>();
let raf = 0, last = 0;
function loop(now: number) {
  const dt = Math.min(0.05, (now - (last || now)) / 1000);
  last = now;
  for (const p of puppets) {
    if (!p.el.isConnected) puppets.delete(p);
    else p.tick(dt);
  }
  raf = puppets.size ? requestAnimationFrame(loop) : 0;
}
export class HeroPuppet {
  el: HTMLCanvasElement;
  private anim: AolaAnim | null = null;
  private st = new Sticker();
  private t = Math.random() * 3;
  private clip = IDLE;
  constructor(dir: string, public w: number, public hgt: number, public flip = false) {
    this.el = h('canvas', { style: `width:${w}px;height:${hgt}px;display:block;pointer-events:none` }) as HTMLCanvasElement;
    void AolaAnim.load(dir).then((a) => (this.anim = a));
    puppets.add(this);
    if (!raf) raf = requestAnimationFrame(loop);
  }
  play(clip: string) {
    this.clip = clip;
    this.t = 0;
  }
  tick(dt: number) {
    this.t += dt;
    const pr = (window.devicePixelRatio || 1) * kit.scale;
    const W = Math.round(this.w * pr), H = Math.round(this.hgt * pr);
    if (this.el.width !== W || this.el.height !== H) {
      this.el.width = W;
      this.el.height = H;
    }
    const g = this.el.getContext('2d')!;
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.clearRect(0, 0, W, H);
    const a = this.anim;
    if (!a) return;
    const c = a.clip(this.clip);
    const loopClip = this.clip === IDLE;
    const fi = a.frameAt(this.clip, this.t, loopClip);
    if (!loopClip && fi >= c.frames.length - 1) {
      this.clip = IDLE;
      this.t = 0;
    }
    this.st.render(a, this.clip, fi, (H * 0.78) / a.idleH, this.flip, true, false, true);
    g.drawImage(this.st.canvas, W / 2 - this.st.ox, H * 0.94 - this.st.oy);
  }
}

// ---------- công tắc, tab ----------
export function toggle(on: boolean, onChange?: (v: boolean) => void) {
  const el = h('button', { class: `k-toggle ${on ? 'on' : ''}` }, h('i', {}));
  pressable(el, () => {
    on = !on;
    el.classList.toggle('on', on);
    onChange?.(on);
  }, { burst: false, sound: sfx.pick });
  return el;
}

export function tabs(labels: string[], active: number, onChange?: (i: number) => void) {
  const el = h('div', { class: 'k-tabs' });
  const btns = labels.map((l, i) => {
    const b = h('button', { class: `k-tab ${i === active ? 'on' : ''}` }, l);
    pressable(b, () => {
      btns.forEach((x, k) => x.classList.toggle('on', k === i));
      onChange?.(i);
    }, { burst: false, sound: sfx.pick });
    return b;
  });
  el.append(...btns);
  return el;
}

// ---------- hộp thoại ----------
export function dialog(host: HTMLElement, title: string, body: HTMLElement, opts: { headColor?: '' | 'p' | 'b' | 'g' } = {}) {
  const sheet = h('div', { class: 'k-sheet' }, h('div', { class: `k-head ${opts.headColor ?? ''}` }, title), body);
  const modal = h('div', { class: 'k-modal' }, sheet);
  const close = () => {
    sfx.whoosh();
    modal.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 220, fill: 'forwards' });
    sheet.animate([{ transform: 'none' }, { transform: 'scale(.85) rotate(3deg) translateY(30px)' }], { duration: 220, easing: 'ease-in', fill: 'forwards' })
      .finished.then(() => modal.remove());
  };
  const x = round('close', { size: 'small', onTap: close });
  x.classList.add('k-x');
  sheet.appendChild(x);
  modal.addEventListener('pointerdown', (e) => { if (e.target === modal) close(); });
  host.appendChild(modal);
  modal.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 200 });
  sheet.animate([
    { transform: 'scale(.6) rotate(-6deg) translateY(60px)', opacity: 0 },
    { transform: 'scale(1.05) rotate(1deg)', opacity: 1, offset: 0.65 },
    { transform: 'none', opacity: 1 },
  ], { duration: 420, easing: 'cubic-bezier(.2,.8,.2,1)' });
  sfx.card();
  return { close, sheet };
}

// ---------- giấy nhớ thông báo ----------
export function toast(host: HTMLElement, text: string, iconName = 'ball') {
  const el = h('div', { class: 'k-toast' }, h('i', { class: 'k-tape p' }), h('span', { html: icon(iconName, 34) }), h('span', {}, text));
  host.appendChild(el);
  el.animate([
    { transform: 'translate(-50%, -160px) rotate(-8deg)' },
    { transform: 'translate(-50%, 10px) rotate(2deg)', offset: 0.7 },
    { transform: 'translate(-50%, 0) rotate(-1deg)' },
  ], { duration: 460, easing: 'cubic-bezier(.2,.8,.2,1)', fill: 'forwards' });
  sfx.coin();
  setTimeout(() => {
    el.animate([{ transform: 'translate(-50%, 0) rotate(-1deg)' }, { transform: 'translate(-50%, -170px) rotate(6deg)' }], { duration: 360, easing: 'ease-in', fill: 'forwards' })
      .finished.then(() => el.remove());
  }, 2200);
}

// ---------- thanh trên (màn con) ----------
export function topbar(title: string, onBack?: () => void) {
  const lv = h('div', { class: 'k-chip', style: 'height:40px;font-size:19px;padding-left:44px', html: icon('exp', 46) }, 'Cấp 15');
  const balls = chip('ball', 186);
  balls.el.style.cssText = 'height:40px;font-size:19px';
  return {
    el: h('div', { class: 'k-topbar' },
      round('back', { size: 'small', onTap: onBack }),
      h('div', { class: 'k-titletape' }, title),
      h('div', { class: 'grow' }),
      lv, balls.el),
    balls,
  };
}
