// Ý tưởng B · "Ấn Ngũ Hành": trang sổ kẻ ô, bút mực tự vẽ vòng ấn; 5 tướng khởi đầu đứng trên bệ ở 5 đỉnh,
// mũi tên khắc vẽ thành ngôi sao năm cánh theo thứ tự đảo (Thủy → Hỏa → Kim → Mộc → Thổ), logo đóng dấu.
import { ELEM_COLOR, ELEM_NAME } from '../../core/elements';
import type { Elem } from '../../core/types';
import { ATTACK, HIT } from '../aola';
import { h } from '../dom';
import { icon } from '../icons';
import { sfx } from '../sfx';
import { anim, CYCLE, ease, INK, logoSvg, PEDESTAL, Puppet, STARTERS, tapEl, type Ticker } from './common';
import type { BootScene } from './boot';

const CX = 270, CY = 592, RV = 160; // tâm ấn, bán kính đỉnh
const LAYOUT: Elem[] = ['hoa', 'tho', 'kim', 'thuy', 'moc']; // theo chiều kim đồng hồ từ đỉnh trên: khắc = nhảy 2 đỉnh
const vert = (e: Elem) => {
  const a = ((-90 + 72 * LAYOUT.indexOf(e)) * Math.PI) / 180;
  return [CX + RV * Math.cos(a), CY + RV * Math.sin(a)] as const;
};
const BEAT: Record<Elem, Elem> = { thuy: 'hoa', hoa: 'kim', kim: 'moc', moc: 'tho', tho: 'thuy' };

export function sceneSeal(tk: Ticker): BootScene {
  const el = h('div', { class: 'bt-scene bt-paper bt-seal' });

  // lề đỏ và lỗ bấm giấy
  el.append(h('div', { class: 'bt-margin' }), ...[150, 480, 810].map((y) => h('div', { class: 'bt-hole', style: `top:${y}px` })));

  // ---- vòng ấn (SVG phủ cả trang, toạ độ = toạ độ màn) ----
  const ring = `M${CX},${CY} m-209,0 a209,209 0 1,1 418,0 a209,209 0 1,1 -418,0`;
  const rule = CYCLE.map((e) => `${ELEM_NAME[e].toUpperCase()} KHẮC ${ELEM_NAME[BEAT[e]].toUpperCase()}`).join('  ✦  ') + '  ✦';
  const pent = LAYOUT.map((e) => vert(e).join(',')).join(' ');
  const arrows = CYCLE.map((s, i) => {
    const [x0, y0] = vert(s), [x1, y1] = vert(BEAT[s]);
    const L = Math.hypot(x1 - x0, y1 - y0), dx = (x1 - x0) / L, dy = (y1 - y0) / L;
    const ax = x0 + dx * 46, ay = y0 + dy * 46, bx = x1 - dx * 54, by = y1 - dy * 54;
    // hơi cong như nét tay
    const mx = (ax + bx) / 2 - dy * 10, my = (ay + by) / 2 + dx * 10;
    const nx = -dy, ny = dx;
    const head = `M${bx - dx * 17 + nx * 9},${by - dy * 17 + ny * 9} L${bx},${by} L${bx - dx * 17 - nx * 9},${by - dy * 17 - ny * 9}`;
    return `<g class="bs-arrow" data-i="${i}">
      <path class="bs-hl" d="M${ax},${ay} Q${mx},${my} ${bx},${by}" stroke="${ELEM_COLOR[s]}" pathLength="1"/>
      <path class="bs-ink" d="M${ax},${ay} Q${mx},${my} ${bx},${by}" pathLength="1"/>
      <path class="bs-flow" d="M${ax},${ay} Q${mx},${my} ${bx},${by}"/>
      <path class="bs-head" d="${head}"/>
    </g>`;
  }).join('');
  const svg = h('div', {
    class: 'bt-fill',
    html: `<svg class="bs-svg boil-self" viewBox="0 0 540 960" width="540" height="960">
      <g class="bs-spin">
        <circle class="bs-c1" cx="${CX}" cy="${CY}" r="226" pathLength="1"/>
        <circle class="bs-c2" cx="${CX}" cy="${CY}" r="193" pathLength="1"/>
        <g class="bs-text"><path id="bsRing" d="${ring}" fill="none"/>
          <text font-size="14.5" font-family="'Baloo 2'" font-weight="800" fill="#5a4636" letter-spacing="1">
            <textPath href="#bsRing" textLength="1300" lengthAdjust="spacing">${rule}</textPath></text></g>
        <polygon class="bs-pent" points="${pent}"/>
        ${arrows}
      </g>
      <g class="bs-core">
        <circle cx="${CX}" cy="${CY}" r="38" fill="#fffaf0" stroke="${INK}" stroke-width="3.5"/>
        <circle cx="${CX}" cy="${CY}" r="31" fill="none" stroke="#e8553f" stroke-width="2.5" stroke-dasharray="5 4"/>
        <g transform="translate(${CX - 20},${CY - 20}) scale(.85)">${swords()}</g>
      </g>
    </svg>`,
  });
  el.append(svg);
  const q = (s: string) => svg.querySelector(s) as SVGElement;
  const arrowEls = [...svg.querySelectorAll('.bs-arrow')] as SVGGElement[];

  // ---- bệ và tướng ở 5 đỉnh ----
  const heroes: Record<string, { box: HTMLElement; ped: HTMLElement; pup: Puppet }> = {};
  for (const e of CYCLE) {
    const [vx, vy] = vert(e);
    const ped = h('div', { class: 'bs-ped', style: `left:${vx - 60}px;top:${vy - 26}px` },
      h('img', { src: PEDESTAL(e), width: 120, draggable: 'false' }),
      h('span', { class: 'bs-badge', html: icon(`e_${e}`, 26) }));
    const pup = new Puppet(STARTERS[e].aola, 160, 136, { flip: vx > CX + 4, body: 0.76 });
    const box = h('div', { class: 'bs-hero', style: `left:${vx - 80}px;top:${vy - 127}px` }, pup.el);
    el.append(ped, box);
    heroes[e] = { box, ped, pup };
    tk.add((dt) => pup.tick(dt));
  }

  // ---- logo, băng keo, chỗ tải ----
  const logo = h('div', { class: 'bs-logo', html: logoSvg('bsl', 370) });
  const tape = h('div', { class: 'bt-tagline' }, 'Sổ Tay Phiêu Lưu');
  const bottom = h('div', { class: 'bt-bottom' });
  const tap = tapEl();
  el.append(logo, tape, bottom);

  const hide = [logo, tape, ...Object.values(heroes).flatMap((x) => [x.box, x.ped]), q('.bs-core'), q('.bs-text'), q('.bs-pent')];
  for (const x of hide) (x as HTMLElement).style.opacity = '0';
  for (const a of arrowEls) a.style.opacity = '0';

  async function intro() {
    void anim(q('.bs-c1'), [{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }], { duration: 900, delay: 100, easing: ease.inOut });
    void anim(q('.bs-c2'), [{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }], { duration: 800, delay: 350, easing: ease.inOut });
    void anim(q('.bs-text'), [{ opacity: 0 }, { opacity: 1 }], { duration: 500, delay: 900 });
    void anim(q('.bs-pent'), [{ opacity: 0 }, { opacity: 1 }], { duration: 400, delay: 800 });
    CYCLE.forEach((e, i) => {
      const x = heroes[e], d = 950 + i * 190;
      void anim(x.ped, [{ opacity: 0, transform: 'translateY(-36px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 380, delay: d, easing: ease.back });
      void anim(x.box, [
        { opacity: 0, transform: 'scale(1.7) rotate(-14deg)' },
        { opacity: 1, transform: 'scale(.92) rotate(3deg)', offset: 0.7 },
        { opacity: 1, transform: 'scale(1) rotate(0)' },
      ], { duration: 360, delay: d + 140, easing: ease.out });
      setTimeout(() => sfx.land(), d + 260);
    });
    // mũi tên khắc
    CYCLE.forEach((s, i) => {
      const a = arrowEls[i], d = 2050 + i * 300;
      void anim(a, [{ opacity: 0 }, { opacity: 1 }], { duration: 1, delay: d });
      void anim(a.querySelector('.bs-ink')!, [{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }], { duration: 300, delay: d, easing: ease.inOut });
      void anim(a.querySelector('.bs-hl')!, [{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }], { duration: 340, delay: d + 40, easing: ease.inOut });
      void anim(a.querySelector('.bs-head')!, [{ opacity: 0 }, { opacity: 1 }], { duration: 60, delay: d + 290 });
      setTimeout(() => {
        const t = heroes[BEAT[s]];
        sfx.card();
        t.pup.play(HIT);
        void anim(t.box, [{ transform: 'translateX(0)' }, { transform: 'translateX(-6px)' }, { transform: 'translateX(5px)' }, { transform: 'translateX(0)' }], { duration: 260 });
      }, d + 300);
    });
    void anim(q('.bs-core'), [
      { opacity: 0, transform: 'scale(2.4) rotate(-30deg)' },
      { opacity: 1, transform: 'scale(.9) rotate(4deg)', offset: 0.75 },
      { opacity: 1, transform: 'scale(1) rotate(0)' },
    ], { duration: 320, delay: 3600, easing: ease.in });
    setTimeout(() => sfx.stamp(), 3850);
    await anim(logo, [
      { opacity: 0, transform: 'translateX(-50%) scale(1.6) rotate(-10deg)' },
      { opacity: 1, transform: 'translateX(-50%) scale(.94) rotate(-1deg)', offset: 0.7 },
      { opacity: 1, transform: 'translateX(-50%) scale(1) rotate(-2deg)' },
    ], { duration: 420, delay: 3950, easing: ease.in });
    sfx.stamp();
    el.animate([{ transform: 'translate(0,0)' }, { transform: 'translate(3px,-4px)' }, { transform: 'translate(-3px,3px)' }, { transform: 'translate(0,0)' }], { duration: 200 });
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
      for (const e of CYCLE) {
        const x = heroes[e];
        x.pup.play(ATTACK);
        void anim(x.box, [{ transform: 'translateY(0)' }, { transform: 'translateY(-18px)' }, { transform: 'translateY(0)' }], { duration: 380, easing: ease.out });
      }
      void anim(q('.bs-spin'), [{ transform: 'rotate(0)' }, { transform: 'rotate(144deg)' }], { duration: 900, easing: ease.inOut });
      void anim(q('.bs-core'), [{ transform: 'scale(1)' }, { transform: 'scale(1.35) rotate(90deg)' }, { transform: 'scale(1) rotate(144deg)' }], { duration: 900, easing: ease.inOut });
      await anim(tap, [{ transform: 'scale(1)' }, { transform: 'scale(1.15)' }, { transform: 'scale(0)', opacity: 0 }], { duration: 380 });
      await new Promise((r) => setTimeout(r, 380));
    },
  };
}

// hai thanh kiếm bắt chéo (48 × 48)
function swords(): string {
  const S = `stroke="${INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"`;
  const one = `<path d="M39 6l3 3-19 21-5-5z" fill="#e2e8ee" ${S}/><path d="M13 27l8 8M16 32l-7 7" fill="none" ${S}/><path d="M11 33l4 4" ${S} stroke-width="6"/>`;
  return `<svg viewBox="0 0 48 48" width="48" height="48">${one}<g transform="translate(48,0) scale(-1,1)">${one}</g></svg>`;
}
