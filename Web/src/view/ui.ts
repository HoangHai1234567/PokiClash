// Thành phần giao diện dùng chung: thẻ, thanh, tag hệ, sao, chân dung, hộp thoại, thông báo, bay icon.
import { CARD } from '../core/data/cards';
import { HERO } from '../core/data/heroes';
import { cardText, costText, KIND_NAME } from '../core/cardtext';
import { formOf } from '../core/progression';
import { ELEM_COLOR, ELEM_NAME, RARITY_COLOR, RARITY_NAME } from '../core/elements';
import type { Elem } from '../core/types';
import { portrait } from './aola';
import { h } from './dom';
import { icon } from './icons';
import { sfx } from './sfx';

export function cardEl(id: string, lv = 1, opts: { mini?: boolean; locked?: string; onclick?: () => void; showKind?: boolean } = {}) {
  const c = CARD[id];
  const el = h(
    'div',
    {
      class: `card sk r-${c.rarity}${opts.mini ? ' mini' : ''}${opts.locked ? ' locked' : ''}`,
      style: `--rc:${RARITY_COLOR[c.rarity]}`,
      onclick: opts.onclick,
    },
    h('div', { class: `tape ${c.kind === 'ult' ? 'pink' : c.kind === 'skill' ? 'blue' : c.kind === 'passive' ? 'green' : ''}` }),
    c.cost && (c.cost.mana || c.cost.rage) ? h('div', { class: 'cost sk thin', style: c.cost.rage ? '--fill:var(--rage)' : '' }, costText(c)) : null,
    h('div', { class: 'cname' }, c.name),
    h('div', { class: 'art', html: icon(c.icon, opts.mini ? 46 : 74) }),
    h('div', { class: 'desc' }, cardText(c, lv)),
    h(
      'div',
      { class: 'rar' },
      h('i'),
      opts.showKind || c.kind !== 'pool' ? `${KIND_NAME[c.kind]} · ` : '',
      RARITY_NAME[c.rarity],
      lv > 1 ? ` · cấp ${lv}` : '',
    ),
    opts.locked ? h('div', { class: 'lock', html: `${icon('lock', 44)}<div>${opts.locked}</div>` }) : null,
  );
  return el;
}

export function bar(cls: string, label = true) {
  const el = h('div', { class: `bar ${cls}` }, h('i', { class: 'ghost' }), h('i', { class: 'main' }), h('i', { class: 'shield' }), label ? h('b') : null);
  const ghost = el.children[0] as HTMLElement, main = el.children[1] as HTMLElement, sh = el.children[2] as HTMLElement;
  const txt = el.querySelector('b');
  return {
    el,
    set(v: number, max: number, shield = 0, text?: string) {
      const p = Math.max(0, Math.min(1, v / Math.max(1, max)));
      main.style.width = `${p * 100}%`;
      ghost.style.width = `${p * 100}%`;
      sh.style.width = `${Math.min(1, shield / Math.max(1, max)) * 100}%`;
      if (txt) txt.textContent = text ?? `${Math.round(v)}/${Math.round(max)}`;
      el.classList.toggle('full', v >= max);
    },
    // vệt vàng lùi chậm sau khi mất máu
    hold() {
      ghost.style.transition = 'none';
      void ghost.offsetWidth;
      ghost.style.transition = '';
    },
  };
}

export function elemTag(e: Elem) {
  return h('span', { class: 'elem-tag', style: `--ec:${ELEM_COLOR[e]}`, html: `${icon('e_' + e, 18)}${ELEM_NAME[e]}` });
}

export function stars(n: number, max = 5) {
  return h('span', { class: 'stars', html: Array.from({ length: max }, (_, i) => icon(i < n ? 'star' : 'starOff', 16)).join('') });
}

// star: chọn dạng trong dòng tiến hóa (mặc định dạng 1)
export function heroImg(heroId: string, height: number, silhouette = false, star = 1) {
  const img = h('img', { style: `height:${height}px;opacity:0;transition:opacity .25s` }) as HTMLImageElement;
  void portrait(formOf(HERO[heroId], star).aola, height * 2, silhouette).then((src) => {
    if (src) {
      img.src = src;
      img.style.opacity = '1';
    } else {
      img.replaceWith(h('div', { class: 'center', style: `height:${height}px`, html: icon('e_' + HERO[heroId].elem, height * 0.6) }));
    }
  });
  return img;
}

// ---------- hộp thoại ----------
export interface ModalOpts {
  onClose?: () => void;
  closable?: boolean;
  top?: boolean;
  width?: number;
  tape?: boolean;
}
export function modal(layer: HTMLElement, content: Node, opts: ModalOpts = {}) {
  const sheet = h('div', { class: 'sheet sk', style: opts.width ? `width:${opts.width}px` : '' }, opts.tape === false ? null : h('div', { class: 'tape' }), content);
  const back = h('div', { class: `modal-back${opts.top ? ' top' : ''}` }, sheet);
  const close = () => {
    back.remove();
    opts.onClose?.();
  };
  if (opts.closable !== false) {
    sheet.appendChild(h('button', { class: 'btn round paper x', html: icon('close', 26), onclick: () => { sfx.click(); close(); } }));
    back.addEventListener('pointerdown', (e) => {
      if (e.target === back) close();
    });
  }
  layer.appendChild(back);
  return { close, sheet, back };
}

export function toast(layer: HTMLElement, text: string, iconName?: string) {
  const t = h('div', { class: 'toast sk thin', html: `${iconName ? icon(iconName, 24, 'style="vertical-align:-6px;margin-right:4px"') : ''}${text}` });
  layer.appendChild(t);
  setTimeout(() => t.remove(), 2700);
}

// bay một icon từ điểm này tới điểm kia (toạ độ trong #root)
export function flyIcon(layer: HTMLElement, name: string, from: [number, number], to: [number, number], size = 34, delay = 0) {
  const el = h('div', { class: 'fly', html: icon(name, size), style: `left:${from[0] - size / 2}px;top:${from[1] - size / 2}px` });
  layer.appendChild(el);
  setTimeout(() => {
    el.style.transform = `translate(${to[0] - from[0]}px, ${to[1] - from[1]}px) scale(0.7) rotate(25deg)`;
  }, 20 + delay);
  setTimeout(() => el.remove(), 650 + delay);
}

// vị trí phần tử trong hệ toạ độ #root (khung 540 × 960)
export function posIn(root: HTMLElement, el: Element): [number, number] {
  const r = el.getBoundingClientRect(), b = root.getBoundingClientRect();
  const k = b.width / 540;
  return [(r.left + r.width / 2 - b.left) / k, (r.top + r.height / 2 - b.top) / k];
}
