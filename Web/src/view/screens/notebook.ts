// Sổ tay: cài đặt, bảng thử (tua nhanh), chỉnh số cân bằng, máy tự chơi đo tỉ lệ thắng.
import { afkTravel } from '../../core/afk';
import { CFG, CFG_DEFAULT } from '../../core/data/config';
import { HEROES } from '../../core/data/heroes';
import { STAGES, ZONE, ZONES, zoneSize } from '../../core/data/stages';
import { addExp, SLOTS } from '../../core/progression';
import { simulateStage } from '../../core/sim';
import { app, type Screen } from '../app';
import { clear, h } from '../dom';
import { icon } from '../icons';
import { sfx } from '../sfx';

const CFG_LABEL: Partial<Record<keyof typeof CFG, string>> = {
  picks: 'Số lần chọn mỗi lượt',
  manaPerTurn: 'Mana mỗi lượt',
  benchMana: 'Mana tướng dự bị',
  rageOnAttack: 'Nộ khi đánh trúng',
  rageOnHit: 'Nộ khi bị đánh (× phần máu mất)',
  critBase: 'Tỉ lệ chí mạng gốc',
  critMult: 'Hệ số chí mạng',
  defK: 'Hằng số thủ',
  hpBase: 'Máu gốc',
  atkBase: 'Công gốc',
  defBase: 'Thủ gốc',
  lvStep: 'Tăng mỗi cấp',
  starStep: 'Tăng mỗi sao',
  bossHp: 'Máu boss ×',
  bossAtk: 'Công boss ×',
  bossEvoHp: 'Boss tiến hóa: tổng máu các dạng ×',
  bossEvoAtk: 'Boss tiến hóa: Công kém mỗi dạng',
  cardLvStep: 'Tăng mỗi cấp thẻ',
};

export function notebookScreen(): Screen {
  const content = h('div', { class: 'col gap12', style: 'padding:6px 16px 110px' });
  const el = h(
    'div',
    { class: 'screen' },
    h('div', { class: 'scroll', style: 'position:absolute;left:0;right:0;top:74px;bottom:0;overflow-y:auto' }, content),
  );

  const section = (title: string, ic: string, ...kids: (Node | null)[]) =>
    h('div', { class: 'sk thin col gap8', style: 'padding:12px 14px;--fill:#fff' }, h('div', { class: 'row gap8' }, h('span', { html: icon(ic, 30) }), h('h3', null, title)), ...kids);

  function toggle(label: string, get: () => boolean, set: (v: boolean) => void) {
    const t = h('div', { class: `toggle ${get() ? 'on' : ''}` });
    t.addEventListener('click', () => {
      set(!get());
      t.classList.toggle('on', get());
      app.applySettings();
      app.persist();
      sfx.click();
    });
    return h('div', { class: 'row gap8', style: 'justify-content:space-between' }, h('span', null, label), t);
  }

  function render() {
    clear(content);
    const s = app.save;
    content.append(
      section(
        'Cài đặt',
        'gear',
        toggle('Nét vẽ rung (tắt nếu máy chậm)', () => s.settings.boil, (v) => (s.settings.boil = v)),
        toggle('Âm thanh', () => s.settings.sound, (v) => (s.settings.sound = v)),
        toggle('Bong bóng gợi ý trong trận', () => s.settings.hints, (v) => (s.settings.hints = v)),
      ),
    );
    const dbg = (label: string, fn: () => void, cls = 'paper') =>
      h('button', { class: `btn small ${cls}`, onclick: () => { fn(); app.persist(); sfx.coin(); render(); } }, label);
    content.append(
      section(
        'Bảng thử (tua nhanh)',
        'dice',
        h('div', { class: 'small muted' }, 'Chỉ có trong bản thử, để xem nhanh các phần sau.'),
        h(
          'div',
          { class: 'row gap6', style: 'flex-wrap:wrap' },
          dbg('+50 bi', () => (s.balls += 50)),
          dbg('+500 XP', () => {
            const b = s.level;
            addExp(s, 500);
            if (s.level > b) app.levelUp(b, s.level);
          }),
          dbg('Tua AFK 1 giờ', () => afkTravel(s, 3600000)),
          dbg('Tua AFK 8 giờ', () => afkTravel(s, 8 * 3600000)),
          dbg('Mở hết tướng', () => HEROES.forEach((x) => (s.heroes[x.id].owned = true))),
          dbg('Mở hết ải', () => { for (const z of ZONES) s.zones[z.id] = zoneSize(z.id); }),
          dbg('+5 bản sao mọi thẻ', () => HEROES.forEach((x) => SLOTS.forEach((k) => (s.heroes[x.id].cards[k].copies += 5)))),
          h('button', { class: 'btn small red', onclick: () => confirmReset() }, 'Xoá dữ liệu'),
        ),
      ),
    );
    // chỉnh số
    const grid = h('div', { style: 'display:grid;grid-template-columns:1fr 1fr;gap:6px 10px' });
    for (const k of Object.keys(CFG_LABEL) as (keyof typeof CFG)[]) {
      const inp = h('input', { type: 'number', step: 'any', value: String(CFG[k]) }) as HTMLInputElement;
      inp.addEventListener('change', () => {
        const v = Number(inp.value);
        if (Number.isFinite(v)) (CFG as Record<string, number>)[k] = v;
      });
      grid.append(h('label', { class: 'field' }, inp, h('span', { class: 'small' }, CFG_LABEL[k]!)));
    }
    content.append(
      section(
        'Chỉnh số cân bằng',
        'pencil',
        h('div', { class: 'small muted' }, 'Sửa xong có hiệu lực ở trận sau. Tải lại trang thì về số gốc.'),
        grid,
        h('button', { class: 'btn small paper', onclick: () => { Object.assign(CFG, CFG_DEFAULT); render(); } }, 'Về số gốc'),
      ),
    );
    // máy tự chơi
    const sel = h('select', { style: 'font-family:"Baloo 2";font-size:15px;border:2px solid var(--ink);border-radius:6px;padding:2px 4px;background:#fffaf0' }) as HTMLSelectElement;
    for (const st of STAGES) sel.append(h('option', { value: String(st.id) }, `${ZONE[st.zone].name} ${st.idx}: ${st.name}`));
    sel.value = String((STAGES.find((st) => st.idx === s.zones[st.zone] + 1) ?? STAGES[0]).id);
    const out = h('div', { class: 'title', style: 'font-size:17px' });
    content.append(
      section(
        'Máy tự chơi',
        'cards',
        h('div', { class: 'small muted' }, `Máy chơi cả hai bên 100 trận với đội hiện tại (${s.team.join(', ') || 'trống'}) ở cấp ${s.level}. Người thật thường chơi tốt hơn máy.`),
        h('div', { class: 'row gap8' }, sel, h('button', {
          class: 'btn small blue',
          onclick: () => {
            out.textContent = 'Đang chạy...';
            setTimeout(() => {
              const r = simulateStage(s, Number(sel.value), s.team.filter((t) => s.heroes[t]?.owned), 100, Date.now() % 100000);
              out.textContent = `Thắng ${Math.round(r.win * 100)}% · trung bình ${r.rounds.toFixed(1)} hiệp`;
            }, 30);
          },
        }, 'Chạy 100 trận')),
        out,
      ),
    );
    content.append(
      section(
        'Về bản thử',
        'info',
        h('div', { style: 'font-size:15px;line-height:1.2' }, 'PokiClash, bản web thử vòng lõi: đánh ải bằng thẻ → nhận bi → máy bi → lên cấp, nâng thẻ, tiến hóa → ải khó hơn.'),
        h('div', { class: 'small muted' }, 'Hình và chuyển động tướng lấy từ dự án aola (gốc của Baitian), chỉ dùng trong bản thử, không đưa vào bản phát hành.'),
        h('div', { class: 'small muted' }, `Đã đánh ${s.stats.battles} trận, thắng ${s.stats.wins}. Đã thả ${s.ballsSpent} bi.`),
      ),
    );
  }

  function confirmReset() {
    const m = app.modal(
      h('div', { class: 'col center gap12', style: 'text-align:center' }, h('h2', null, 'Xoá hết dữ liệu?'), h('div', null, 'Cấp, tướng, thẻ, ải đã qua sẽ về như mới.'),
        h('div', { class: 'row gap8' }, h('button', { class: 'btn red', onclick: () => { m.close(); app.reset(); } }, 'Xoá'), h('button', { class: 'btn paper', onclick: () => m.close() }, 'Thôi'))),
      { width: 380 },
    );
  }

  return { el, top: 'back', title: 'Sổ tay', enter: render };
}
