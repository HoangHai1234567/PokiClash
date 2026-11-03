// Máy tự chơi đo cân bằng, chạy trong Node: npm run sim -- [pachinko|battle|badges|island|all] [số trận]
import { runBattle, SIM_TEAMS, simSave, zoneTable } from '../src/core/sim';
import { createBattle } from '../src/core/battle';
import { badgeCount, badgeSeed, badgeStage } from '../src/core/badges';
import { BADGE, badgeBonus } from '../src/core/data/badges';
import { HERO } from '../src/core/data/heroes';
import { TAG_NAME } from '../src/core/data/islands';
import { MEASURED_RATES } from '../src/core/data/measured';
import { claimZoneChest, enemyTeam, playerTeam, stageBalls, STAR_LEVEL } from '../src/core/progression';
import { STAGES, V2_ZONES, ZONE, ZONE_CHESTS, ZONES, zoneStages } from '../src/core/data/stages';
import { Board, BW, openChest, SLOT_INFO, SWING, type SlotKind } from '../src/core/pachinko';
import { expToNext, newSave, type SaveData } from '../src/core/progression';
import { Rng } from '../src/core/rng';

const mode = process.argv[2] ?? 'all';
const N = Number(process.argv[3] ?? 200);

function pachinko() {
  const board = new Board(7);
  const rng = new Rng(3);
  const count: Record<string, number> = {};
  let landed = 0;
  const total = 6000;
  let dropped = 0, t = 0;
  while (landed < total) {
    if (dropped < total && t % 6 === 0) {
      // máng thả đung đưa: vị trí theo hình sin, gần như đều
      board.drop(BW / 2 + Math.sin(t * 0.37) * SWING, 1);
      dropped++;
    }
    for (const e of board.step(1 / 60)) {
      if (e.t !== 'land') continue;
      landed++;
      const k = e.cup ? `cốc:${e.reward}` : `ô${e.slot}:${e.reward}`;
      count[k] = (count[k] ?? 0) + 1;
    }
    t++;
  }
  const rows = Object.entries(count).sort();
  console.log(`\nMáy bi: ${total} bi, ${(t / 60).toFixed(0)} giây máy`);
  for (const [k, v] of rows) console.log(`  ${k.padEnd(20)} ${((v / total) * 100).toFixed(2)}%`);
  // giá trị kỳ vọng mỗi bi (x1): EXP và bi hoàn lại; rương mở thử 20000 lần
  const s = newSave(0);
  const chestEv: Record<string, { exp: number; balls: number; cards: number }> = {};
  for (const kind of ['chest_wood', 'chest_silver', 'chest_gold'] as const) {
    let exp = 0, balls = 0, cards = 0;
    for (let i = 0; i < 20000; i++) {
      const s2: SaveData = JSON.parse(JSON.stringify(s));
      for (const r of openChest(s2, kind, 1, rng)) {
        if (r.k === 'exp') exp += r.n;
        if (r.k === 'balls') balls += r.n;
        if (r.k === 'card') cards++;
      }
    }
    chestEv[kind] = { exp: exp / 20000, balls: balls / 20000, cards: cards / 20000 };
  }
  let ev = 0, back = 0, cards = 0;
  for (const [k, v] of rows) {
    const kind = k.split(':')[1] as SlotKind;
    const p = v / total;
    const info = SLOT_INFO[kind];
    if (info.exp) ev += p * info.exp;
    else if (info.balls) back += p * info.balls;
    else {
      const c = chestEv[kind];
      ev += p * c.exp;
      back += p * c.balls;
      cards += p * c.cards;
    }
  }
  console.log(`  rương:`, chestEv);
  console.log(`  mỗi bi (x1): ${ev.toFixed(2)} EXP, hoàn ${back.toFixed(3)} bi, ${cards.toFixed(3)} thẻ`);
  console.log(`  bi để lên cấp 2/5/10: ${[1, 4, 9].map((l) => (expToNext(l) / ev).toFixed(1)).join(' / ')}`);
}


function battles() {
  console.log(`
Trận theo đảo, ${N} trận mỗi ô (máy chơi cả hai bên)`);
  const table = zoneTable(N);
  for (const z of ZONES) {
    const zt = SIM_TEAMS[z.id];
    const t = table.find((x) => x.zone === z.id)!;
    console.log(`
${z.name} (đề nghị cấp ${z.level[0]}–${z.level[1]}), đội ${zt.team.join(', ')}, sao ${zt.star}, thẻ cấp ${zt.card}`);
    console.log('  ải'.padEnd(28) + t.levels.map((l) => `cấp ${l}`.padStart(14)).join(''));
    for (const row of t.stages) {
      const st = STAGES.find((x) => x.id === row.id)!;
      const cells = row.cells.map((c) => `${Math.round((c.win / N) * 100)}% ${(c.rounds / N).toFixed(1)}h`.padStart(14));
      console.log(`  ${String(st.idx)} ${st.name.padEnd(24)}${cells.join('')}`);
    }
  }
}

// Đền Huy Hiệu: tỉ lệ thắng từng bậc (trung bình các trận của bậc, và trận cuối) với đội mẫu của đảo cùng hệ,
// cấp người chơi = cấp địch trận 1 của bậc + {−2, 0, +3}; rồi bảng đảo khi mọi tướng có huy hiệu bậc 0 / 3 / 5.
function badges() {
  console.log(`
Đền Huy Hiệu, ${N} trận mỗi trận thử thách`);
  for (const z of ZONES) {
    const zt = SIM_TEAMS[z.id];
    console.log(`
Dãy ${z.name} · đội ${zt.team.join(', ')}, sao ${zt.star}, thẻ ${zt.card}`);
    for (let tier = 1; tier <= 5; tier++) {
      const base = badgeStage(z.id, tier, 1).enemies[0].level;
      const cells = [-2, 0, 3].map((dl) => {
        const lv = Math.max(1, base + dl);
        const s = simSave(zt.team, lv, zt.star, zt.card);
        let win = 0, total = 0, last = 0;
        const n = badgeCount(tier);
        for (let i = 1; i <= n; i++) {
          const st = badgeStage(z.id, tier, i);
          for (let k = 0; k < N; k++) {
            const b = runBattle(createBattle([{ ...playerTeam(s), ai: true }, enemyTeam(st)], badgeSeed(z.id, tier, i) + k * 7919, [lv, Math.max(lv, st.enemies[0].level)]));
            if (b.winner === 0) {
              win++;
              if (i === n) last++;
            }
            total++;
          }
        }
        return `cấp ${lv}: ${Math.round((win / total) * 100)}% (cuối ${Math.round((last / N) * 100)}%)`.padEnd(30);
      });
      console.log(`  ${BADGE.tiers[tier - 1].padEnd(10)}${cells.join('')}`);
    }
  }
  console.log(`
Ảnh hưởng lên đảo: tỉ lệ thắng trung bình 8 ải ở cấp đề nghị thấp nhất, mọi tướng có huy hiệu bậc 0 / 3 / 5`);
  for (const z of ZONES) {
    const zt = SIM_TEAMS[z.id];
    const cells = [0, 3, 5].map((tier) => {
      const s = simSave(zt.team, z.level[0], zt.star, zt.card);
      for (const e of Object.keys(s.badges) as (keyof typeof s.badges)[]) s.badges[e].tier = tier;
      let win = 0, total = 0;
      for (const st of STAGES.filter((x) => x.zone === z.id))
        for (let k = 0; k < N; k++) {
          const b = runBattle(createBattle([{ ...playerTeam(s), ai: true }, enemyTeam(st)], 1000 + k * 7919, [z.level[0], z.level[0]]));
          if (b.winner === 0) win++;
          total++;
        }
      return `bậc ${tier} (+${Math.round(badgeBonus(tier) * 100)}%): ${Math.round((win / total) * 100)}%`.padEnd(22);
    });
    console.log(`  ${z.name.padEnd(10)} cấp ${z.level[0]}: ${cells.join('')}`);
  }
}

// Đảo 70 ải (islands.ts): tỉ lệ thắng từng ải. Người chơi mang 1 tướng (ô đội 2 mở khi xong đảo), cấp = cấp địch cao nhất của ải
// −1 / 0 / +1; sao theo cấp như người chơi theo kịp (sao n khi đủ cấp STAR_LEVEL[n]), cấp thẻ = sao. Hai tướng: tướng khởi đầu
// (cùng hệ đảo) và tướng tặng ở ải 3 (hệ khắc đảo). Cuối bảng: bi lần đầu qua cả đảo và cấp lên được nếu thả hết vào máy bi.
const TWO = process.argv[4] === 'two'; // npm run sim -- island 60 two: thử đội 2 tướng (giot_suong + vo_su)
function island() {
  for (const z of V2_ZONES) {
    const picks = TWO ? [['giot_suong', 'vo_su']] : [['giot_suong'], ['vo_su']];
    console.log(`\n${ZONE[z].name}: ${zoneStages(z).length} ải, ${N} trận mỗi ô; cột: ${picks.map((p) => p.map((x) => HERO[x].name).join('+')).join(' | ')} ở cấp −1 / 0 / +1`);
    const stats = new Map<string, number[][]>(); // kiểu ải -> [cột tướng][ải]
    for (const st of zoneStages(z)) {
      const rec = Math.max(...st.enemies.map((e) => e.level));
      const cells = picks.map((team) => [-1, 0, 1].map((dl) => {
        const lv = Math.max(1, rec + dl);
        let star = 1;
        while (star < 5 && STAR_LEVEL[star + 1] <= lv) star++;
        const s = simSave(team, lv, star, star);
        let win = 0;
        for (let i = 0; i < N; i++) if (runBattle(createBattle([{ ...playerTeam(s), ai: true }, enemyTeam(st)], 1000 + i * 7919, [lv, lv])).winner === 0) win++;
        return Math.round((win / N) * 100);
      }));
      const key = st.kind !== 'normal' ? st.kind : st.tag!;
      const row = stats.get(key) ?? picks.map(() => [] as number[]);
      cells.forEach((c, i) => row[i].push(c[1]));
      stats.set(key, row);
      const foes = st.enemies.map((e) => `${HERO[e.hero].name}${e.boss ? '*' : ''}${e.buff ? (e.buff > 0 ? '+' : '') + Math.round(e.buff * 100) + '%' : ''}`).join(', ');
      console.log(`  ${String(st.idx).padStart(2)} ${(st.kind !== 'normal' ? st.kind : TAG_NAME[st.tag!]).padEnd(14)} cấp ${String(rec).padEnd(2)} ${foes.padEnd(46).slice(0, 46)} ${cells.map((c) => c.map((v) => `${v}%`.padStart(5)).join('')).join('  |')}`);
    }
    console.log(`  Trung bình ở cấp đề nghị theo kiểu ải (${picks.map((p) => p.map((x) => HERO[x].name).join('+')).join(' | ')}):`);
    const avg = (v: number[]) => Math.round(v.reduce((a, b) => a + b, 0) / v.length);
    for (const [k, v] of stats) console.log(`    ${(TAG_NAME[k as keyof typeof TAG_NAME] ?? k).padEnd(16)} ${v.map((c) => `${avg(c)}%`.padStart(5)).join(' |')}  (${v[0].length} ải)`);
    // bi lần đầu qua đảo, rương mốc; EXP mỗi bi (×1) theo tỉ lệ ô đo được và rương mở thử
    const firstBalls = zoneStages(z).reduce((a, st) => a + stageBalls(st, true), 0);
    const s = newSave(0);
    s.zones[z] = zoneStages(z).length;
    let chestBalls = 0;
    const rng = new Rng(5);
    while (true) {
      const r = claimZoneChest(s, z, rng);
      if (!r) break;
      chestBalls += r.balls;
    }
    let ev = 0;
    for (const [k, p] of Object.entries(MEASURED_RATES)) {
      const info = SLOT_INFO[k as SlotKind];
      if (info.exp) ev += p * info.exp;
      else if (!info.balls) {
        let exp = 0;
        for (let i = 0; i < 4000; i++) for (const r of openChest(newSave(0), k as 'chest_wood', 1, rng)) if (r.k === 'exp') exp += r.n;
        ev += (p * exp) / 4000;
      }
    }
    let lv = 1, exp = (firstBalls + chestBalls) * ev;
    while (exp >= expToNext(lv)) exp -= expToNext(lv++);
    console.log(`  Bi lần đầu qua: ${firstBalls} (ải) + ${chestBalls} (${ZONE_CHESTS[z].length} rương) ≈ ${Math.round((firstBalls + chestBalls) * ev)} EXP (${ev.toFixed(1)} EXP/bi) → cấp ${lv}, chưa tính cây bi, trang trại, đánh lại`);
    const rep = zoneStages(z).map((st) => stageBalls(st, false));
    console.log(`  Bi đánh lại một ải: ${Math.min(...rep)}–${Math.max(...rep)}`);
  }
}

if (mode === 'pachinko' || mode === 'all') pachinko();
if (mode === 'badges' || mode === 'all') badges();
if (mode === 'battle' || mode === 'all') battles();
if (mode === 'island' || mode === 'all') island();
