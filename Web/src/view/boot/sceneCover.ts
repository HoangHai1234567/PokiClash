// Ý tưởng C · "Bìa sổ chiến thuật": cuốn sổ bìa giấy kraft trên bàn gỗ; nhãn tên có logo, 5 sticker tướng còn cử động,
// nét bút bi ghi vòng khắc, dấu đỏ "TUYỆT MẬT", dây chun. Chạm thì dây chun bật ra, bìa lật mở: trang đầu chính là sảnh.
import type { Elem } from '../../core/types';
import { ATTACK } from '../aola';
import { h } from '../dom';
import { sfx } from '../sfx';
import { anim, CYCLE, ease, logoSvg, Puppet, STARTERS, tapEl, woodTexture, type Ticker } from './common';
import type { BootScene } from './boot';

const PEN = '#2f4f9a'; // mực bút bi xanh
// sticker: [trái, trên, góc] trong toạ độ bìa 512 × 932
const STK: Record<Elem, [number, number, number]> = {
  thuy: [46, 428, -8],
  hoa: [270, 420, 7],
  kim: [158, 546, -3],
  moc: [40, 602, 6],
  tho: [270, 610, -6],
};
const BEAT: Record<Elem, Elem> = { thuy: 'hoa', hoa: 'kim', kim: 'moc', moc: 'tho', tho: 'thuy' };
const SW = 190, SH = 170;

export function sceneCover(tk: Ticker): BootScene {
  const el = h('div', { class: 'bt-scene bt-cover' });
  const desk = h('div', { class: 'cv-desk', style: `background-image:url(${woodTexture()})` });
  const front = h('div', { class: 'cv-face cv-front' });
  const back = h('div', { class: 'cv-face cv-back' },
    h('div', { style: "position:absolute;left:40px;right:40px;top:380px;text-align:center;font:400 22px Pangolin;color:#5a4636;line-height:1.5" },
      'Nhặt được sổ này', h('br'), 'xin trả lại cho chủ sổ!', h('br'), h('span', { style: 'font-size:34px' }, '☺')));
  const cover = h('div', { class: 'cv-cover' }, front, back);
  const wrap = h('div', { class: 'cv-wrap' }, cover);
  el.append(desk, wrap);

  // gáy vải, góc bọc
  front.append(
    h('div', { class: 'cv-spine' }),
    h('div', { class: 'cv-corner', style: 'left:478px;top:-34px;transform:rotate(45deg)' }),
    h('div', { class: 'cv-corner', style: 'left:478px;top:900px;transform:rotate(45deg)' }),
  );

  // nét bút bi: vòng khắc giữa các sticker
  const center = (e: Elem) => [STK[e][0] + SW / 2, STK[e][1] + SH * 0.55] as const;
  const doodles = CYCLE.map((s, i) => {
    const [x0, y0] = center(s), [x1, y1] = center(BEAT[s]);
    const L = Math.hypot(x1 - x0, y1 - y0), dx = (x1 - x0) / L, dy = (y1 - y0) / L;
    const ax = x0 + dx * 64, ay = y0 + dy * 58, bx = x1 - dx * 66, by = y1 - dy * 60;
    const bend = 26 * (i % 2 ? 1 : -1);
    const mx = (ax + bx) / 2 - dy * bend, my = (ay + by) / 2 + dx * bend;
    const tx = bx - mx, ty = by - my, tl = Math.hypot(tx, ty), ux = tx / tl, uy = ty / tl;
    const head = `M${bx - ux * 13 - uy * 8},${by - uy * 13 + ux * 8} L${bx},${by} L${bx - ux * 13 + uy * 8},${by - uy * 13 - ux * 8}`;
    return `<path class="cv-pen" d="M${ax},${ay} Q${mx},${my} ${bx},${by}" pathLength="1"/><path class="cv-pen-h" d="${head}"/>`;
  }).join('');
  const doodle = h('div', {
    class: 'bt-fill',
    html: `<svg class="cv-doodle boil-self" viewBox="0 0 512 932" width="512" height="932">
      ${doodles}
      <g class="cv-notes" font-family="Pangolin" fill="${PEN}">
        <text x="204" y="497" font-size="23" transform="rotate(-4 228 497)">khắc!</text>
        <text x="408" y="606" font-size="22" transform="rotate(8 408 606)">×1,5</text>
        <text x="58" y="612" font-size="19" transform="rotate(-10 58 612)">nhớ nha</text>
        <path d="M0 -15l5 10 11 2-8 7 2 11-10-5-10 5 2-11-8-7 11-2z" fill="none" stroke="${PEN}" stroke-width="2.4" stroke-linejoin="round" transform="translate(90 444) rotate(-12)"/>
        <path d="M238 770l14 14M252 770l-14 14" stroke="${PEN}" stroke-width="3" stroke-linecap="round"/>
      </g>
    </svg>`,
  });
  front.append(doodle);

  // nhãn tên
  const owner = h('b', {}, 'Bạn');
  const label = h('div', { class: 'cv-label' },
    h('div', { html: logoSvg('cvl', 320) }),
    h('div', { class: 'cv-sub' }, 'SỔ TAY CHIẾN THUẬT'),
    h('div', { class: 'cv-owner' }, 'Chủ sổ:', owner),
    h('div', { class: 'ta-tape', style: 'left:-24px;top:-10px;transform:rotate(-28deg)' }),
    h('div', { class: 'ta-tape', style: 'left:330px;top:-8px;transform:rotate(24deg);background:rgba(170,214,255,.85)' }),
  );
  front.append(label);

  // sticker tướng
  const stickers: Record<string, { box: HTMLElement; pup: Puppet }> = {};
  for (const e of CYCLE) {
    const [x, y, r] = STK[e];
    const pup = new Puppet(STARTERS[e].aola, SW, SH, { flip: x > 200, body: 0.62, foot: 0.86 });
    const box = h('div', { class: 'cv-sticker', style: `left:${x}px;top:${y}px;width:${SW}px;height:${SH}px;transform:rotate(${r}deg)` }, pup.el);
    front.append(box);
    stickers[e] = { box, pup };
    tk.add((dt) => pup.tick(dt));
  }

  const stamp = h('div', { class: 'cv-stamp', style: 'left:244px;top:384px;transform:rotate(-13deg)' }, 'TUYỆT MẬT');
  const band = h('div', { class: 'cv-band', style: 'left:468px' });
  const bottom = h('div', { class: 'bt-bottom' });
  const postit = h('div', { class: 'cv-postit' }, h('div', { class: 'ta-tape', style: 'left:158px;top:-12px;transform:rotate(-3deg)' }), bottom);
  front.append(stamp, band, postit);
  const tap = tapEl('Chạm để mở sổ');

  const pens = [...doodle.querySelectorAll('.cv-pen')] as SVGPathElement[];
  const heads = [...doodle.querySelectorAll('.cv-pen-h')] as SVGPathElement[];
  const notes = doodle.querySelector('.cv-notes') as SVGGElement;
  for (const x of [label, stamp, notes, ...heads, ...Object.values(stickers).map((v) => v.box)]) (x as unknown as HTMLElement).style.opacity = '0';
  owner.style.clipPath = 'inset(0 100% 0 0)';

  async function intro() {
    void anim(cover, [{ transform: 'translateY(70px) scale(1.05)', opacity: 0 }, { transform: 'translateY(0) scale(1)', opacity: 1 }], { duration: 450, easing: ease.out });
    setTimeout(() => sfx.land(), 380);
    void anim(postit, [{ transform: 'translateX(-50%) translateY(170px) rotate(1.5deg)' }, { transform: 'translateX(-50%) translateY(0) rotate(1.5deg)' }], { duration: 450, delay: 350, easing: ease.back });
    void anim(label, [{ opacity: 0, transform: 'rotate(-6deg) scale(1.25)' }, { opacity: 1, transform: 'rotate(-1.2deg) scale(1)' }], { duration: 320, delay: 550, easing: ease.out });
    CYCLE.forEach((e, i) => {
      const [, , r] = STK[e], d = 950 + i * 170;
      void anim(stickers[e].box, [
        { opacity: 0, transform: `rotate(${r - 18}deg) scale(1.7)` },
        { opacity: 1, transform: `rotate(${r + 3}deg) scale(.94)`, offset: 0.7 },
        { opacity: 1, transform: `rotate(${r}deg) scale(1)` },
      ], { duration: 340, delay: d, easing: ease.out });
      setTimeout(() => sfx.pick(), d + 200);
    });
    pens.forEach((p, i) => {
      const d = 2000 + i * 230;
      void anim(p, [{ strokeDashoffset: 1 }, { strokeDashoffset: 0 }], { duration: 260, delay: d, easing: ease.inOut });
      void anim(heads[i], [{ opacity: 0 }, { opacity: 1 }], { duration: 60, delay: d + 240 });
    });
    void anim(notes, [{ opacity: 0 }, { opacity: 1 }], { duration: 400, delay: 3100 });
    void anim(owner, [{ clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)' }], { duration: 450, delay: 3200, easing: 'linear' });
    await anim(stamp, [
      { opacity: 0, transform: 'rotate(-30deg) scale(2.6)' },
      { opacity: 1, transform: 'rotate(-11deg) scale(.92)', offset: 0.75 },
      { opacity: 1, transform: 'rotate(-13deg) scale(1)' },
    ], { duration: 300, delay: 3750, easing: ease.in });
    sfx.stamp();
    void anim(cover, [{ transform: 'translate(0,0)' }, { transform: 'translate(3px,-3px)' }, { transform: 'translate(-2px,2px)' }, { transform: 'translate(0,0)' }], { duration: 200 });
    el.classList.add('idle');
  }

  return {
    el,
    bottom,
    intro,
    showTap() {
      bottom.replaceChildren(tap);
      void anim(tap, [{ opacity: 0, transform: 'translateY(10px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 300, easing: ease.out });
    },
    async exit() {
      // dây chun bật ra
      sfx.swap();
      await anim(band, [{ transform: 'translateX(0) rotate(0)' }, { transform: 'translateX(-14px) rotate(-2deg)', offset: 0.3 }, { transform: 'translateX(90px) rotate(10deg)', opacity: 0 }], { duration: 300, easing: ease.in });
      for (const e of CYCLE) {
        stickers[e].pup.play(ATTACK);
        const r = STK[e][2];
        void anim(stickers[e].box, [{ transform: `rotate(${r}deg)` }, { transform: `rotate(${r - 6}deg) translateY(-10px)` }, { transform: `rotate(${r}deg)` }], { duration: 300 });
      }
      await new Promise((r) => setTimeout(r, 260));
      // lật bìa
      sfx.whoosh();
      void anim(desk, [{ opacity: 1 }, { opacity: 0 }], { duration: 400, delay: 650 });
      await anim(cover, [{ transform: 'rotateY(0deg)' }, { transform: 'rotateY(-178deg)' }], { duration: 1050, easing: ease.inOut });
    },
  };
}
