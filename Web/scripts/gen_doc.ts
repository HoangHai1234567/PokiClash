// In bảng markdown từ dữ liệu thật của game (tướng, thẻ, ải, tiến trình) để dán vào tài liệu: npx tsx scripts/gen_doc.ts
import { heroStats } from '../src/core/battle';
import { cardText, costText } from '../src/core/cardtext';
import { CARD, POOL } from '../src/core/data/cards';
import { HERO, HEROES } from '../src/core/data/heroes';
import { STAGES, ZONE } from '../src/core/data/stages';
import { ELEM_NAME, RARITY_NAME } from '../src/core/elements';
import { TREES } from '../src/core/data/trees';
import { expToNext, newSave, stageBalls, X_STEPS } from '../src/core/progression';

const out: string[] = [];
const p = (s = '') => out.push(s);

p('### Tướng (chỉ số ở cấp 1, 1 sao)');
p();
p('| Tướng | Hệ | Độ hiếm | Máu | Công | Thủ | Tốc | Mảnh mở | Chiêu | Tuyệt kỹ | Bị động |');
p('|---|---|---|---|---|---|---|---|---|---|---|');
for (const h of HEROES) {
  const s = heroStats(h, 1, 1);
  const c = (id: string) => `**${CARD[id].name}** (${costText(CARD[id]) || RARITY_NAME[CARD[id].rarity]}): ${cardText(CARD[id])}`;
  p(`| ${h.name} | ${ELEM_NAME[h.elem]} | ${RARITY_NAME[h.rarity]} | ${s.hp} | ${s.atk} | ${s.def} | ${s.spd} | ${h.shards} | ${c(h.skill)} | ${c(h.ult)} | **${CARD[h.passive].name}**: ${cardText(CARD[h.passive])} |`);
}
p();
p('### Thẻ chung');
p();
p('| Thẻ | Độ hiếm | Mở ở cấp | Tác dụng |');
p('|---|---|---|---|');
for (const c of POOL) p(`| ${c.name} | ${RARITY_NAME[c.rarity]} | ${c.unlock ?? 1} | ${cardText(c)} |`);
p();
p('### Ải');
p();
p('| Đảo | Ải | Tên | Loại | Địch (cấp) | Bi (lần đầu / đánh lại) | Thưởng mảnh (lần đầu) |');
p('|---|---|---|---|---|---|---|');
for (const st of STAGES) {
  const foes = st.enemies.map((e) => `${HERO[e.hero].name} ${e.level}${e.boss ? ' (boss)' : ''}`).join(', ');
  const drops = st.drops.map((d) => (d.gift ? `${HERO[d.hero].name} gia nhập` : `${HERO[d.hero].name} ${d.min}–${d.max} (${Math.round(d.chance * 100)}%)`)).join(', ') || '—';
  p(`| ${ZONE[st.zone].name} | ${st.idx} | ${st.name} | ${st.kind === 'boss' ? 'Boss' : st.kind === 'mini' ? 'Mini boss' : 'Thường'} | ${foes} | ${stageBalls(st, true)} / ${stageBalls(st, false)} | ${drops} |`);
}
p();
p('### Cấp người chơi');
p();
p('| Cấp | EXP lên cấp sau |');
p('|---|---|');
for (const lv of [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20]) p(`| ${lv} | ${expToNext(lv)} |`);
p();
p(`Nút cược máy bi mở theo cấp: ${X_STEPS.map((x) => `×${x.x} ở cấp ${x.lv}`).join(', ')}.`);
p(`Cây bi: mỗi cây ${TREES.perHour} bi/giờ, chứa tối đa ${TREES.cap}; cây 1 mở khi qua ải 1, cây 2–5 khi qua boss Đảo Thủy, Hỏa, Kim, Mộc. AFK chỉ ra mảnh tướng và rương AFK.`);
console.log(out.join('\n'));
