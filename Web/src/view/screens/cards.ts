// Sổ thẻ: bộ thẻ chung (mở theo cấp) và cách xếp thẻ.
import { POOL, POOL_WEIGHT } from '../../core/data/cards';
import { RARITY_COLOR, RARITY_NAME } from '../../core/elements';
import { RARITIES } from '../../core/types';
import { app, type Screen } from '../app';
import { clear, h } from '../dom';
import { icon } from '../icons';
import { cardEl } from '../ui';

export function cardsScreen(): Screen {
  const content = h('div', { class: 'col gap12', style: 'padding:6px 14px 110px;align-items:center' });
  const el = h(
    'div',
    { class: 'screen' },
    h('div', { class: 'scroll', style: 'position:absolute;left:0;right:0;top:74px;bottom:0;overflow-y:auto' }, content),
  );

  function render() {
    clear(content);
    const lv = app.save.level;
    const tot = POOL.filter((c) => (c.unlock ?? 1) <= lv).reduce((a, c) => a + POOL_WEIGHT[c.rarity], 0);
    content.append(
      h(
        'div',
        { class: 'sk thin', style: 'padding:10px 14px;--fill:#fff;font-size:15.5px;line-height:1.2;transform:rotate(-.6deg)' },
        h('div', { class: 'title', style: 'font-size:18px' }, 'Cách xếp thẻ'),
        h('div', null, 'Mỗi lượt chọn 5 lần, mỗi lần 1 trong 3 thẻ dưới đây. Thẻ chạy theo đúng thứ tự xếp, rồi tướng đánh thường.'),
        h('div', null, 'Chiêu (tốn mana) và Tuyệt kỹ (đủ nộ + mana) là thẻ riêng của tướng, xen vào hàng lúc đang chọn, không tốn lần chọn. Tuyệt kỹ thay cú đánh thường cuối lượt.'),
        h('div', null, 'Mẹo: xếp thẻ tăng Công trước Chiêu. "Lượt này" là tới hết lượt mình; "tới lượt sau" là che cả lượt địch.'),
      ),
    );
    const legend = h('div', { class: 'row gap8', style: 'flex-wrap:wrap;justify-content:center' });
    for (const r of RARITIES) {
      const own = POOL.filter((c) => c.rarity === r && (c.unlock ?? 1) <= lv);
      const w = own.length ? (POOL_WEIGHT[r] * own.length) / Math.max(1, tot) : 0;
      void w;
      legend.append(h('span', { class: 'chip sk thin', style: 'font-size:14px' }, h('i', { style: `width:14px;height:14px;border-radius:50%;background:${RARITY_COLOR[r]};border:2px solid var(--ink);display:inline-block` }), `${RARITY_NAME[r]} · nặng ${POOL_WEIGHT[r]}`));
    }
    content.append(legend);
    const grid = h('div', { class: 'row gap12', style: 'flex-wrap:wrap;justify-content:center' });
    for (const c of POOL) {
      const locked = (c.unlock ?? 1) > lv;
      grid.append(cardEl(c.id, 1, { locked: locked ? `Mở ở cấp ${c.unlock}` : undefined }));
    }
    content.append(grid);
    content.append(h('div', { class: 'small muted', style: 'text-align:center', html: `${icon('info', 18, 'style="vertical-align:-4px"')} Thẻ riêng của tướng xem ở mục Tướng.` }));
  }

  return { el, top: 'back', title: 'Sổ thẻ', enter: render };
}
