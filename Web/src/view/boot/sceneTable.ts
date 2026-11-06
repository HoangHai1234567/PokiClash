// Ý tưởng A · "Sa bàn giấy": tấm bản đồ đảo đặt nghiêng trên bàn gỗ như sa bàn; 5 tướng khởi đầu bật dựng lên
// như sách pop-up ở đảo cùng hệ, mũi tên kế hoạch tác chiến vẽ theo vòng khắc, logo gấp bật lên.
import { ELEM_COLOR } from '../../core/elements';
import type { Elem } from '../../core/types';
import { ATTACK, HIT } from '../aola';
import { h } from '../dom';
import { icon } from '../icons';
import { sfx } from '../sfx';
import { anim, CYCLE, ease, INK, logoSvg, Puppet, STARTERS, tapEl, woodTexture, WORLD_IMG, type Ticker } from './common';
import type { BootScene } from './boot';

const TILT = 46;
// chỗ đứng của từng tướng trên tấm bản đồ (480 × 690), cạnh mốc của vùng hệ trong world.png
const POS: Record<Elem, [number, number]> = {
  thuy: [141, 504],
  hoa: [297, 182],
  kim: [385, 297],
  moc: [123, 257],
  tho: [354, 504],
};
const BEAT: Record<Elem, Elem> = { thuy: 'hoa', hoa: 'kim', kim: 'moc', moc: 'tho', tho: 'thuy' };

export function sceneTable(tk: Ticker): BootScene {
  const el = h('div', { class: 'bt-scene bt-desk bt-table', style: `background-image:url(${woodTexture()})` });

  // đồ trên bàn: 3 lá thẻ úp (chọn 1 trong 3) và cây bút chì
  const cards = h('div', { class: 'bt-fill' },
    ...[[-14, -18, 392, -22], [8, 2, 404, -6], [30, 22, 420, 10]].map(([x, , y, r], i) =>
      h('div', { class: 'ta-card', style: `left:${x}px;top:${y + i * 4}px;transform:rotate(${r}deg)`, html: icon('star', 30) })),
    h('div', { class: 'ta-pencil', style: 'left:440px;top:430px;transform:rotate(62deg)', html: pencilSvg() }),
  );
  el.append(cards);

  // ---- sa bàn 3D ----
  const sheet = h('div', { class: 'ta-sheet' });
  const stage = h('div', { class: 'ta-stage' }, sheet);
  el.append(stage);
  sheet.append(
    h('div', { class: 'ta-sheet-bg bt-paper' }),
    h('div', { class: 'ta-sea' }),
    h('img', { class: 'ta-island', src: WORLD_IMG, draggable: 'false' }),
    ...[[-22, -12, -8], [428, -10, 7], [-24, 672, 6], [430, 670, -9]].map(([x, y, r]) =>
      h('div', { class: 'ta-tape', style: `left:${x}px;top:${y}px;transform:rotate(${r}deg)` })),
  );

  // kế hoạch: mũi tên đứt nét theo vòng khắc, vòng tròn "Xuất phát!", la bàn
  const arrows = CYCLE.map((s, i) => {
    const [x0, y0] = POS[s], [x1, y1] = POS[BEAT[s]];
    const L = Math.hypot(x1 - x0, y1 - y0), dx = (x1 - x0) / L, dy = (y1 - y0) / L;
    const ax = x0 + dx * 42, ay = y0 + dy * 42, bx = x1 - dx * 48, by = y1 - dy * 48;
    const bend = 34 * (i % 2 ? 1 : -1);
    const mx = (ax + bx) / 2 - dy * bend, my = (ay + by) / 2 + dx * bend;
    // hướng mũi tên = tiếp tuyến cuối đường cong
    const tx = bx - mx, ty = by - my, tl = Math.hypot(tx, ty), ux = tx / tl, uy = ty / tl;
    const d = `M${ax},${ay} Q${mx},${my} ${bx},${by}`;
    const head = `M${bx - ux * 18 - uy * 11},${by - uy * 18 + ux * 11} L${bx},${by} L${bx - ux * 18 + uy * 11},${by - uy * 18 - ux * 11}`;
    return `<mask id="taM${i}" maskUnits="userSpaceOnUse" x="0" y="0" width="480" height="690"><path class="ta-mask" d="${d}" pathLength="1"/></mask>
      <g class="ta-arrow" data-i="${i}">
        <path class="ta-dash-ink" d="${d}" mask="url(#taM${i})"/>
        <path class="ta-dash" d="${d}" stroke="${ELEM_COLOR[s]}" mask="url(#taM${i})"/>
        <path class="ta-head" d="${head}"/>
      </g>`;
  }).join('');
  const [sx, sy] = POS.thuy;
  const plan = h('div', {
    class: 'bt-fill',
    html: `<svg class="ta-plan boil-self" viewBox="0 0 480 690" width="480" height="690">
      ${arrows}
      <g class="ta-start">
        <ellipse class="ta-ring" cx="${sx}" cy="${sy - 4}" rx="70" ry="52" pathLength="1" transform="rotate(-8 ${sx} ${sy})"/>
        <text x="${sx - 64}" y="${sy + 82}" font-family="Pangolin" font-size="30" fill="#c0392b" transform="rotate(-6 ${sx} ${sy + 80})">Xuất phát!</text>
      </g>
      <g class="ta-compass" transform="translate(424 628)">
        <circle r="26" fill="#fffaf0" stroke="${INK}" stroke-width="3"/>
        <path d="M0 -22 L7 0 L0 22 L-7 0 Z" fill="#e8553f" stroke="${INK}" stroke-width="2.4" stroke-linejoin="round"/>
        <path d="M0 0 L7 0 L0 22 Z" fill="#fffaf0" stroke="${INK}" stroke-width="2.4" stroke-linejoin="round"/>
        <text y="-31" text-anchor="middle" font-family="'Baloo 2'" font-weight="800" font-size="17" fill="${INK}">B</text>
      </g>
    </svg>`,
  });
  sheet.append(plan);
  const q = (s: string) => plan.querySelector(s) as SVGElement;
  const arrowEls = [...plan.querySelectorAll('.ta-arrow')] as SVGGElement[];

  // tướng dựng đứng và cờ hiệu
  const heroes: Record<string, { up: HTMLElement; flag: HTMLElement; base: HTMLElement; pup: Puppet }> = {};
  for (const e of CYCLE) {
    const [x, y] = POS[e];
    const pup = new Puppet(STARTERS[e].aola, 220, 190, { flip: x > 240, body: 0.7 });
    const base = h('div', { class: 'ta-base', style: `background:${ELEM_COLOR[e]}` });
    const up = h('div', { class: 'ta-up' }, pup.el);
    const flag = h('div', { class: 'ta-flag', html: flagSvg(e) });
    const fx = x > 240 ? 46 : -62;
    sheet.append(
      h('div', { class: 'ta-std', style: `left:${x}px;top:${y}px` }, base, up),
      h('div', { class: 'ta-std', style: `left:${x + fx}px;top:${y - 22}px` }, flag),
    );
    heroes[e] = { up, flag, base, pup };
    tk.add((dt) => pup.tick(dt));
  }

  // ---- logo, băng keo, giấy ghi chú dưới ----
  const logo = h('div', { class: 'ta-logo', html: logoSvg('tal', 360) });
  const tape = h('div', { class: 'bt-tagline' }, 'Sổ Tay Phiêu Lưu');
  const bottom = h('div', { class: 'bt-bottom' });
  const note = h('div', { class: 'ta-note' }, bottom);
  const tap = tapEl();
  el.append(logo, tape, note);

  for (const x of [logo, tape, q('.ta-start'), ...Object.values(heroes).flatMap((v) => [v.up, v.flag, v.base])]) (x as HTMLElement).style.opacity = '0';
  for (const a of arrowEls) a.style.opacity = '0';
  const island = sheet.querySelector('.ta-island') as HTMLElement;
  island.style.clipPath = 'inset(0 100% 0 0)';

  async function intro() {
    void anim(sheet, [
      { transform: `translateY(420px) rotateX(${TILT + 20}deg)`, opacity: 0 },
      { transform: `translateY(0) rotateX(${TILT}deg)`, opacity: 1 },
    ], { duration: 700, delay: 50, easing: ease.out });
    void anim(note, [{ transform: 'translateX(-50%) translateY(160px) rotate(-1deg)' }, { transform: 'translateX(-50%) translateY(0) rotate(-1deg)' }], { duration: 500, delay: 200, easing: ease.back });
    void anim(island, [{ clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)' }], { duration: 750, delay: 650, easing: ease.inOut });
    CYCLE.forEach((e, i) => {
      const v = heroes[e], d = 1450 + i * 200;
      void anim(v.base, [{ opacity: 0, transform: 'scale(.2)' }, { opacity: 1, transform: 'scale(1)' }], { duration: 220, delay: d, easing: ease.back });
      void anim(v.up, [
        { opacity: 1, transform: 'rotateX(0deg)' },
        { opacity: 1, transform: `rotateX(${-TILT - 22}deg)`, offset: 0.65 },
        { opacity: 1, transform: `rotateX(${-TILT}deg)` },
      ], { duration: 480, delay: d + 60, easing: ease.out });
      void anim(v.flag, [
        { opacity: 1, transform: 'rotateX(0deg)' },
        { opacity: 1, transform: `rotateX(${-TILT - 18}deg)`, offset: 0.65 },
        { opacity: 1, transform: `rotateX(${-TILT}deg)` },
      ], { duration: 420, delay: d + 200, easing: ease.out });
      setTimeout(() => sfx.pick(), d + 120);
    });
    CYCLE.forEach((s, i) => {
      const a = arrowEls[i], d = 2550 + i * 280;
      void anim(a, [{ opacity: 0 }, { opacity: 1 }], { duration: 1, delay: d });
      void anim(plan.querySelector(`#taM${i} path`)!, [{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }], { duration: 300, delay: d, easing: ease.inOut });
      void anim(a.querySelector('.ta-head')!, [{ opacity: 0, transform: 'scale(.3)' }, { opacity: 1, transform: 'scale(1)' }], { duration: 120, delay: d + 280 });
      setTimeout(() => {
        sfx.card();
        heroes[BEAT[s]].pup.play(HIT);
      }, d + 300);
    });
    void anim(q('.ta-start'), [{ opacity: 0 }, { opacity: 1 }], { duration: 1, delay: 4000 });
    void anim(q('.ta-ring'), [{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }], { duration: 420, delay: 4000, easing: ease.inOut });
    await anim(logo, [
      { opacity: 1, transform: 'translateX(-50%) perspective(700px) rotateX(88deg)' },
      { opacity: 1, transform: 'translateX(-50%) perspective(700px) rotateX(-16deg) rotate(-2deg)', offset: 0.6 },
      { opacity: 1, transform: 'translateX(-50%) perspective(700px) rotateX(0deg) rotate(-2deg)' },
    ], { duration: 560, delay: 3700, easing: ease.out });
    sfx.stamp();
    await anim(tape, [{ opacity: 0, transform: 'translateX(-50%) rotate(-3deg) scaleX(.2)' }, { opacity: 1, transform: 'translateX(-50%) rotate(-3deg) scaleX(1)' }], { duration: 260, easing: ease.out });
    el.classList.add('idle');
  }

  return {
    el,
    bottom,
    intro,
    usesClouds: true,
    showTap() {
      bottom.replaceChildren(tap);
      void anim(tap, [{ opacity: 0, transform: 'translateY(10px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 300, easing: ease.out });
    },
    async exit() {
      sfx.whoosh();
      el.classList.remove('idle');
      for (const e of CYCLE) heroes[e].pup.play(ATTACK);
      void anim(logo, [{ transform: 'translateX(-50%) rotate(-2deg)' }, { transform: 'translateX(-50%) translateY(-260px) rotate(-8deg)' }], { duration: 700, delay: 150, easing: ease.in });
      void anim(tape, [{ opacity: 1 }, { opacity: 0 }], { duration: 300 });
      void anim(note, [{ transform: 'translateX(-50%) rotate(-1deg)' }, { transform: 'translateX(-50%) translateY(200px) rotate(-1deg)' }], { duration: 500, delay: 150, easing: ease.in });
      void anim(cards, [{ opacity: 1 }, { opacity: 0 }], { duration: 400 });
      stage.style.transformOrigin = '27% 68%'; // lao vào đảo Thủy, chỗ xuất phát
      await anim(stage, [{ transform: 'scale(1)' }, { transform: 'scale(2.8)' }], { duration: 1000, delay: 250, easing: ease.in });
    },
  };
}

export function flagSvg(e: Elem): string {
  return `<svg viewBox="0 0 56 86" width="70" height="108" overflow="visible">
    <path d="M6 84V6" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>
    <path d="M6 84V6" stroke="#c98a4a" stroke-width="2.4" stroke-linecap="round"/>
    <path class="ta-cloth" d="M7 8 Q30 4 52 20 Q30 30 7 38 Z" fill="${ELEM_COLOR[e]}" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/>
    <g transform="translate(13 11) scale(.4)">${icon(`e_${e}`, 48).replace(/<svg[^>]*>|<\/svg>/g, '')}</g>
  </svg>`;
}

export function pencilSvg(): string {
  return `<svg viewBox="0 0 170 34" width="170" height="34">
    <path d="M30 4h120l14 5v16l-14 5H30z" fill="#f7c948" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M30 13h134M30 21h134" stroke="${INK}" stroke-width="1.6" opacity=".35"/>
    <path d="M150 4v26" stroke="${INK}" stroke-width="3"/><path d="M150 4h6v26h-6z" fill="#f07fa6" stroke="${INK}" stroke-width="3"/>
    <path d="M30 4L4 17l26 13z" fill="#f3d7a8" stroke="${INK}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M12 13L4 17l8 4z" fill="${INK}"/>
  </svg>`;
}
