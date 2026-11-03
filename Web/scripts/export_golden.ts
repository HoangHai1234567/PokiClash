// Xuất bộ đối chiếu (golden) cho EditMode test của Unity: npx tsx scripts/export_golden.ts [thư mục đích]
// Mặc định ghi vào ../Assets/02 Data/Golden. Unity chạy lại cùng hạt giống và so từng giá trị.
import '../src/core/data/stages_v1'; // Unity chưa có hệ thống 70 ải: đối chiếu bộ 8 ải cũ (phải đứng đầu)
import { mkdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { aiTurn } from '../src/core/ai';
import { advance, aiForcedChoice, createBattle, execute, forceSwap, heroStats, startBattle, type Battle, type Ev } from '../src/core/battle';
import { cardText, costText } from '../src/core/cardtext';
import { INNATE, POOL } from '../src/core/data/cards';
import { HERO, HEROES } from '../src/core/data/heroes';
import {
  addShards, claimZoneChest, enemyFormStar, enemyTeam, formIndex, memberOf, migrateRosterV3, newSave, playerTeam, rollCardDrop, SLOTS,
  stageLead, winStage,
} from '../src/core/progression';
import { afkBoost, afkChestTimes, afkPending, afkSlots, afkTick, afkTravel, claimAfk, openAfkChest } from '../src/core/afk';
import { adLeft, adUse, buyProduct, migrateAdsV2, passActive } from '../src/core/ads';
import { treeCap, treesHarvest, treesOpen, treesStock, treesTick, treesTravel } from '../src/core/trees';
import { Board, BW, openChest, spendBall, SWING, type Reward } from '../src/core/pachinko';
import { Rng } from '../src/core/rng';
import { runBattle, zoneTable } from '../src/core/sim';
import { badgeCount, badgeCurrent, badgeSeed, badgeStage, lineOpen, templeOpen, winBadge } from '../src/core/badges';
import { STAGE, STAGES, ZONES } from '../src/core/data/stages';
import { potentialTotals, type PotLine } from '../src/core/data/potential';
import { farmAuto, farmBoost, farmHarvest, farmHours, farmOf, farmPlace, farmRate, farmRemove, farmRestMin, farmTick, farmTravel, spotsOpen } from '../src/core/farm';
import { caveElem, caveLeft, cavePick, caveStage, keepPotential, spinCost, spinPotential, weekdayOf, winCave } from '../src/core/potential';
import { RARITIES, type Elem, type TeamSetup } from '../src/core/types';

const out = resolve(process.argv[2] ?? join(import.meta.dirname, '../../Assets/02 Data/Golden'));
mkdirSync(out, { recursive: true });

function write(name: string, data: unknown, pretty = true) {
  writeFileSync(join(out, name), JSON.stringify(data, null, pretty ? 1 : 0) + '\n', 'utf8');
  console.log('ghi', join(out, name));
}

// 1.000 số đầu của mỗi hạt giống, kèm vài phép dẫn xuất (int, chance) để bắt lỗi làm tròn
const SEEDS = [1, 42, 123456];
write('rng.json', {
  seeds: SEEDS.map((seed) => {
    const r = new Rng(seed);
    const next = Array.from({ length: 1000 }, () => r.next());
    const r2 = new Rng(seed);
    const ints = Array.from({ length: 200 }, () => r2.int(0, 9));
    return { seed, next, ints };
  }),
});

// mô tả mọi thẻ ở cấp 1 và cấp 5
write('cardtext.json', {
  cards: [...POOL, ...INNATE].map((c) => ({ id: c.id, lv1: cardText(c, 1), lv5: cardText(c, 5), cost: costText(c) })),
});

// ---------- trận: 200 trận, đội ngẫu nhiên theo hạt giống, bên 0 là người (đổi tướng bằng hộp chọn), bên 1 là máy ----------

function randomTeam(r: Rng, name: string, ai: boolean): TeamSetup {
  const n = r.int(1, 3);
  const members = [];
  for (let i = 0; i < n; i++) {
    const h = HEROES[r.int(0, HEROES.length - 1)];
    const m = {
      heroId: h.id, level: r.int(1, 30), star: r.int(1, 5),
      cardLv: { skill: r.int(1, 5), ult: r.int(1, 5), passive: r.int(1, 5) },
      boss: r.chance(0.15),
    };
    // boss ải 8: thẻ Tiến Hóa (gồm cả dòng 1 dạng, không tiến hóa nhưng gánh máu cả dòng)
    members.push(m.boss && r.chance(0.6) ? { ...m, evo: true } : m);
  }
  return { name, ai, members };
}

// vòng chơi giống sim.ts nhưng giữ lại mọi sự kiện
function play(b: Battle): Ev[] {
  const evs: Ev[] = [...startBattle(b)];
  let guard = 0;
  while (b.phase !== 'over' && guard++ < 2000) {
    if (b.phase === 'forceSwap') {
      evs.push(...forceSwap(b, aiForcedChoice(b, b.turn.side)));
      continue;
    }
    if (b.phase === 'picking') {
      evs.push(...aiTurn(b, 0.15));
      evs.push(...execute(b));
      continue;
    }
    evs.push(...advance(b));
  }
  return evs;
}

const DETAIL = 12; // số trận ghi đủ từng sự kiện (cả ảnh chụp)
const battles = [];
const detail = [];
const gen = new Rng(2026);
for (let i = 0; i < 200; i++) {
  const seed = gen.int(1, 2 ** 31 - 2);
  const teams: [TeamSetup, TeamSetup] = [randomTeam(gen, 'Bạn', false), randomTeam(gen, 'Địch', true)];
  const unlock: [number, number] = [gen.int(1, 12), gen.int(1, 12)];
  const b = createBattle(teams, seed, unlock);
  const evs = play(b);
  const entry = {
    seed, unlock, teams,
    winner: b.winner, round: b.round, turns: b.turns, dmg: b.dmgDealt, events: evs.length,
    kinds: evs.map((e) => e.t).join(','),
    last: evs[evs.length - 1]?.snap ?? null,
  };
  battles.push(entry);
  if (i < DETAIL) detail.push({ seed, evs });
}
write('battles.json', { battles }, false);
write('battle_events.json', { battles: detail }, false);
const revives = battles.filter((x) => x.kinds.includes('revive')).length;
const evolves = battles.filter((x) => x.kinds.includes('evolve')).length;
console.log(`200 trận: bên 0 thắng ${battles.filter((x) => x.winner === 0).length}, có hồi sinh ${revives}, có tiến hóa ${evolves}, ` +
  `dài nhất ${Math.max(...battles.map((x) => x.round))} hiệp`);

// ---------- tiến trình: chỉ số tướng, thẻ rơi từ rương, mảnh tướng ----------

const stats = HEROES.flatMap((h) => [1, 10, 20, 30].flatMap((lv) => [1, 3, 5].flatMap((st) =>
  [false, true].map((boss) => ({ id: h.id, lv, st, boss, ...heroStats(h, lv, st, boss) })))));

const dropSave = newSave(0);
for (const id of ['vo_su', 'ca_ngua', 'phap_luan', 'ca_sa']) dropSave.heroes[id].owned = true;
const dr = new Rng(77);
const drops = Array.from({ length: 300 }, () => {
  const d = rollCardDrop(dropSave, RARITIES[dr.int(0, 4)], dr);
  return d ? [d.hero, d.slot, d.card, d.rarity] : null;
});

const shardSave = newSave(0);
const sr = new Rng(5);
const shards = Array.from({ length: 80 }, () => {
  const hero = HEROES[sr.int(0, HEROES.length - 1)].id;
  const n = sr.int(1, 6);
  const r = addShards(shardSave, hero, n, sr);
  return [hero, n, r.unlocked, r.converted];
});
const shardEnd = HEROES.map((h) => {
  const p = shardSave.heroes[h.id];
  return [h.id, p.owned, p.shards, ...SLOTS.map((k) => p.cards[k].copies)];
});
write('progression.json', { stats, drops, shards, shardEnd });

// ---------- đảo: thưởng ải (lần đầu, đánh lại, tặng tướng) và rương mốc ----------

const zs = newSave(0);
const zr = new Rng(9);
const steps: unknown[] = [];
const win = (id: number) => {
  const r = winStage(zs, id, zr);
  steps.push({ t: 'win', id, balls: r.balls, first: r.first, shards: r.shards.map((x) => [x.hero, x.n, x.unlocked, x.converted]) });
};
const chest = (z: 'thuy' | 'hoa') => {
  const r = claimZoneChest(zs, z, zr);
  steps.push({ t: 'chest', z, r: r ? { balls: r.balls, big: r.big, cards: r.cards.map((c) => [c.hero, c.slot, c.card, c.rarity]) } : null });
};
for (let id = 1; id <= 4; id++) win(id);
chest('thuy');
chest('thuy'); // chưa đủ 8 ải: null
for (let id = 5; id <= 8; id++) win(id);
chest('thuy');
for (let k = 0; k < 6; k++) win(8); // đánh lại boss
win(3); // đánh lại ải tặng: không tặng nữa
for (let id = 9; id <= 12; id++) win(id);
chest('hoa');
write('zones.json', {
  steps,
  end: { zones: zs.zones, zoneChests: zs.zoneChests, clears: zs.clears, balls: zs.balls,
    owned: Object.entries(zs.heroes).filter(([, p]) => p.owned).map(([k]) => k) },
});

// ---------- máy bi: thả 6.000 bi (vị trí thả theo dãy tỉ lệ vàng, không dùng lượng giác), mở rương, mốc Huyền thoại ----------

const board = new Board(7);
const landCount: Record<string, number> = {};
const firstLands: string[] = [];
let landed = 0, dropped = 0, frame = 0, pegHits = 0;
const TOTAL = 6000;
while (landed < TOTAL && frame < 200000) {
  if (dropped < TOTAL && frame % 6 === 0) {
    board.drop(BW / 2 + ((((dropped * 0.6180339887498949) % 1) * 2) - 1) * SWING, 1);
    dropped++;
  }
  for (const e of board.step(1 / 60)) {
    if (e.t === 'peg') {
      pegHits++;
      continue;
    }
    landed++;
    const k = e.cup ? `cup:${e.reward}` : `slot${e.slot}:${e.reward}`;
    landCount[k] = (landCount[k] ?? 0) + 1;
    if (firstLands.length < 400) firstLands.push(k);
  }
  frame++;
}

const cs = newSave(0);
for (const id of ['vo_su', 'nu_hoa', 'ca_ngua']) cs.heroes[id].owned = true;
cs.zones.thuy = 8;
const cr = new Rng(11);
const kinds = ['chest_wood', 'chest_silver', 'chest_gold'] as const;
const chestOpens = Array.from({ length: 600 }, (_, i) => {
  const kind = kinds[i % 3];
  const x = [1, 3, 5][Math.floor(i / 3) % 3];
  return {
    kind, x,
    r: openChest(cs, kind, x, cr).map((r) =>
      r.k === 'card' ? ['card', r.drop.hero, r.drop.slot, r.drop.card, r.drop.rarity]
        : r.k === 'shards' ? ['shards', r.res.hero, r.res.n, r.res.unlocked, r.res.converted]
        : r.k === 'exp' ? ['exp', r.n, r.ups] : r.k === 'balls' ? ['balls', r.n] : [r.k]),
  };
});

const legend = (owned: boolean) => {
  const s = newSave(0);
  s.balls = 1000;
  if (owned) s.heroes.ca_sa.owned = true;
  let at = -1, reward: unknown = null;
  for (let i = 0; i < 120 && at < 0; i++) {
    const r = spendBall(s, 3);
    if (r) {
      at = s.ballsSpent;
      reward = r;
    }
  }
  return { at, reward, ballsSpent: s.ballsSpent, copies: owned ? s.heroes.ca_sa.cards : null };
};

write('pachinko.json', {
  drop: { total: TOTAL, frames: frame, pegHits, landCount, firstLands },
  chest: { save: { level: cs.level, exp: cs.exp, balls: cs.balls }, opens: chestOpens },
  legend: { fresh: legend(false), owned: legend(true) },
}, false);
console.log('máy bi:', landCount, 'khung', frame);

// ---------- AFK: đồng hồ theo đoạn, tăng tốc, rương AFK, lùi giờ, lượt quảng cáo; Unity chạy lại từng bước và so trạng thái ----------

const T0 = 1_700_000_000_000, HR = 3600000;
const as = newSave(T0);
for (const id of ['vo_su', 'nu_hoa']) as.heroes[id].owned = true;
const ar = new Rng(21);
const rw = (rs: Reward[] | null) => rs && rs.map((r) =>
  r.k === 'card' ? ['card', r.drop.hero, r.drop.slot, r.drop.card, r.drop.rarity]
    : r.k === 'exp' ? ['exp', r.n, r.ups] : r.k === 'balls' ? ['balls', r.n] : [r.k]);
type AfkOp =
  | { op: 'tick' | 'pending' | 'boost'; t: number }
  | { op: 'claim'; t: number; mult: number }
  | { op: 'open'; t: number; early: boolean }
  | { op: 'ad'; day: number; kind: 'open' | 'boost' }
  | { op: 'travel'; ms: number }
  | { op: 'zone'; zone: 'thuy' | 'hoa'; n: number };
const afkOps: AfkOp[] = [
  { op: 'tick', t: T0 + 2 * HR },
  { op: 'zone', zone: 'thuy', n: 8 },
  { op: 'pending', t: T0 + 2.5 * HR },
  { op: 'pending', t: T0 + 7 * HR },
  { op: 'boost', t: T0 + 7 * HR },
  { op: 'boost', t: T0 + 8 * HR },
  { op: 'pending', t: T0 + 12 * HR },
  { op: 'pending', t: T0 + 20 * HR },
  { op: 'open', t: T0 + 6 * HR, early: false },
  { op: 'open', t: T0 + 20 * HR, early: false },
  { op: 'open', t: T0 + 20 * HR, early: false },
  { op: 'open', t: T0 + 20 * HR, early: false },
  { op: 'open', t: T0 + 20 * HR, early: false },
  { op: 'open', t: T0 + 20 * HR, early: false },
  { op: 'claim', t: T0 + 20 * HR, mult: 1 },
  { op: 'tick', t: T0 + 15 * HR },
  { op: 'pending', t: T0 + 18 * HR },
  { op: 'open', t: T0 + 18.5 * HR, early: false },
  { op: 'open', t: T0 + 18.5 * HR, early: true },
  ...Array.from({ length: 5 }, () => ({ op: 'ad' as const, day: 100, kind: 'open' as const })),
  ...Array.from({ length: 4 }, () => ({ op: 'ad' as const, day: 100, kind: 'boost' as const })),
  { op: 'ad', day: 101, kind: 'open' },
  { op: 'travel', ms: 8 * HR },
  { op: 'pending', t: T0 + 18.5 * HR },
  { op: 'claim', t: T0 + 18.5 * HR, mult: 2 },
  { op: 'zone', zone: 'hoa', n: 8 },
  { op: 'boost', t: T0 + 19 * HR },
  { op: 'pending', t: T0 + 24 * HR },
  { op: 'pending', t: T0 + 40 * HR },
  ...Array.from({ length: 5 }, (_, i) => ({ op: 'open' as const, t: T0 + (40 + i) * HR, early: false })),
  { op: 'claim', t: T0 + 45 * HR, mult: 1 },
];
const afkSteps = afkOps.map((o) => {
  let r: unknown = null;
  switch (o.op) {
    case 'tick': r = afkTick(as, o.t); break;
    case 'pending': r = afkPending(as, o.t); break;
    case 'boost': r = afkBoost(as, o.t); break;
    case 'claim': {
      const c = claimAfk(as, o.t, o.mult, ar);
      r = { hours: c.hours, shards: c.shards.map((x) => [x.hero, x.n, x.unlocked, x.converted]) };
      break;
    }
    case 'open': r = rw(openAfkChest(as, o.t, ar, o.early)); break;
    case 'ad': {
      const p = o.kind === 'open' ? 'afk_chest_open' : 'afk_boost';
      r = [adUse(as, o.day, p), adLeft(as, o.day, p)];
      break;
    }
    case 'travel': afkTravel(as, o.ms); break;
    case 'zone': as.zones[o.zone] = o.n; break;
  }
  return { ...o, r, afk: structuredClone(as.afk), times: afkChestTimes(as, o.op === 'travel' || o.op === 'ad' || o.op === 'zone' ? 0 : o.t), balls: as.balls, exp: as.exp, level: as.level, afkSince: as.afkSince };
});
write('afk.json', { t0: T0, steps: afkSteps });
console.log('AFK:', afkSteps.length, 'bước');

// ---------- bảng 40 ải × 5 mức cấp như npm run sim -- battle (6 trận mỗi ô): cửa sổ Cân bằng của Unity phải ra đúng số này ----------
const SIM_N = 6;
write('sim.json', { n: SIM_N, zones: zoneTable(SIM_N) }, false);
console.log('bảng 40 ải:', SIM_N, 'trận mỗi ô');

// ---------- Đền Huy Hiệu: đội địch của cả 200 trận thử thách, chỉ số có phần cộng huy hiệu, vài trận đánh thật, một đoạn tiến độ ----------

const bzones = ZONES.map((z) => z.id);
const badgeStages = bzones.flatMap((z) => [1, 2, 3, 4, 5].flatMap((tier) =>
  Array.from({ length: badgeCount(tier) }, (_, k) => {
    const st = badgeStage(z, tier, k + 1);
    return { zone: z, tier, i: k + 1, id: st.id, seed: badgeSeed(z, tier, k + 1), kind: st.kind, enemies: st.enemies.map((e) => [e.hero, e.level, e.boss]) };
  })));
const bs = newSave(0);
for (const id of ['vo_su', 'nu_hoa', 'ca_ngua', 'phap_luan']) bs.heroes[id].owned = true;
bs.badges.thuy.tier = 2;
bs.badges.hoa.tier = 5;
const badgeStats = ['giot_suong', 'ca_ngua', 'phap_luan', 'vo_su'].map((h) => {
  const m = memberOf(bs, h);
  return { hero: h, mods: m.mods ?? null, stats: heroStats(HERO[h], 9, 2, false, m.mods) };
});
bs.level = 9;
bs.team = ['giot_suong', 'ca_ngua', 'phap_luan'];
const badgeFights = [1, 2, 3, 4, 5].map((i) => {
  const st = badgeStage('thuy', 1, i);
  const b = runBattle(createBattle([{ ...playerTeam(bs), ai: true }, enemyTeam(st)], badgeSeed('thuy', 1, i), [9, Math.max(9, st.enemies[0].level)]));
  return { i, winner: b.winner, round: b.round };
});
// tiến độ: mở đền, thua (không mất tiến độ), thắng hết bậc Đồng hệ Thủy, rương bạc
const ps = newSave(0);
ps.zones.thuy = 8;
ps.zones.kim = 4;
const pr = new Rng(31);
const badgeSteps: unknown[] = [];
const snap = () => ({ balls: ps.balls, exp: ps.exp, level: ps.level, badges: structuredClone(ps.badges) });
badgeSteps.push({ op: 'open', temple: templeOpen(ps), lines: bzones.map((z) => lineOpen(ps, z)), cur: badgeCurrent(ps, 'thuy'), ...snap() });
for (let i = 0; i < 12; i++) {
  const z: Elem = i < 6 ? 'thuy' : 'kim';
  const r = winBadge(ps, z, pr);
  badgeSteps.push({
    op: 'win', zone: z, gain: r?.balls ?? 0, tierDone: r?.tierDone ?? 0, chest: r?.chest ?? null,
    rewards: (r?.rewards ?? []).map((x) => x.k === 'card' ? ['card', x.drop.hero, x.drop.card] : x.k === 'exp' ? ['exp', x.n] : x.k === 'balls' ? ['balls', x.n] : [x.k]),
    cur: badgeCurrent(ps, z), ...snap(),
  });
}
write('badges.json', { stages: badgeStages, stats: badgeStats, fights: badgeFights, steps: badgeSteps });
console.log('huy hiệu:', badgeStages.length, 'trận; Thủy bậc 1:', badgeFights.map((f) => (f.winner === 0 ? 'thắng' : 'thua') + ' ' + f.round).join(', '));

// ---------- Tiềm năng: khai phá có khoá ô, giữ mới / giữ cũ, trần tổng, trận có hiệu ứng đầu trận, Hang theo ngày ----------

const pts = newSave(0);
pts.heroes.giot_suong.star = 4;
pts.heroes.vo_su.owned = true;
pts.heroes.vo_su.star = 2;
pts.potentialStones = 300;
const prng = new Rng(41);
const lockSets = [[], [true], [true, false, true], [false, true, false, true], [true, true, true], [], [false, false, true]];
const potSpins = Array.from({ length: 60 }, (_, i) => {
  const hero = i % 5 === 4 ? 'vo_su' : 'giot_suong';
  const locks = lockSets[i % lockSets.length];
  const cost = spinCost(pts, hero, locks);
  const res = spinPotential(pts, hero, locks, prng);
  const keepNew = i % 3 !== 1;
  if (res) keepPotential(pts, hero, keepNew);
  return { hero, locks, cost, res, keepNew, stones: pts.potentialStones, pot: structuredClone(pts.heroes[hero].potential) };
});
const capLines = [{ k: 'atk', r: 4 }, { k: 'atk', r: 4 }, { k: 'atk', r: 4 }, { k: 'mana', r: 4 }] as PotLine[];
const potTotals = { lines: capLines, totals: potentialTotals(capLines) };
// trận: Tiểu Y và Võ Sư có tiềm năng đủ loại, đánh ải 3 và 5 của Đảo Thủy
const pf = newSave(0);
pf.level = 6;
pf.heroes.vo_su.owned = true;
pf.team = ['giot_suong', 'vo_su'];
pf.heroes.giot_suong.potential = [{ k: 'rage', r: 3 }, { k: 'crit', r: 4 }, { k: 'atk', r: 2 }, null];
pf.heroes.vo_su.potential = [{ k: 'mana', r: 2 }, { k: 'lifesteal', r: 3 }, null, null];
const potMembers = playerTeam(pf).members;
const potFights = [3, 5].flatMap((id) => [11, 12, 13].map((seed) => {
  const b = createBattle([{ ...playerTeam(pf), ai: true }, enemyTeam(STAGE[id])], seed, [6, 6]);
  const f0 = b.sides[0].fighters[0];
  const startState = { mana: f0.mana, rage: f0.rage, buffs: f0.buffs.map((x) => [x.stat, x.v, x.left]) };
  runBattle(b);
  return { stage: id, seed, winner: b.winner, round: b.round, start: startState };
}));
// Hang: đội địch mọi hệ × tầng, thứ trong tuần, lượt và đá
const caveStages = ZONES.flatMap((z) => [0, 1, 2, 3].map((tier) => {
  const st = caveStage(z.id, tier);
  return { zone: z.id, tier, id: st.id, enemies: st.enemies.map((e) => [e.hero, e.level, e.boss]) };
}));
const cs2 = newSave(0);
cs2.zones.hoa = 4;
const caveDays = Array.from({ length: 9 }, (_, i) => 20000 + i).map((day) => ({ day, weekday: weekdayOf(day), elem: caveElem(cs2, day) }));
const caveSteps: unknown[] = [];
const day0 = 20003; // Chủ nhật? xem weekday trong caveDays
for (const [op, arg] of [['win', 0], ['win', 3], ['pick', 'moc'], ['win', 1], ['win', 2], ['ad', 0], ['ad', 0], ['win', 2], ['win', 2]] as const) {
  let r: unknown = null;
  if (op === 'win') r = winCave(cs2, day0, arg as number);
  else if (op === 'ad') r = adUse(cs2, day0, 'cave_extra');
  else r = cavePick(cs2, day0, arg as Elem);
  caveSteps.push({ op, arg, r, left: caveLeft(cs2, day0), stones: cs2.potentialStones, elem: caveElem(cs2, day0) });
}
write('potential.json', {
  spins: potSpins, totals: potTotals,
  members: potMembers.map((m) => ({ hero: m.heroId, mods: m.mods ?? null, start: m.start ?? null })),
  fights: potFights, caveStages, caveDays, caveDay: day0, caveSteps,
});
console.log('tiềm năng:', potSpins.filter((x) => x.res).length, 'lần quay; trận', potFights.map((f) => f.winner).join(''));

// ---------- Trang trại: công thức, đặt, rút, nghỉ, tự xếp, tăng tốc, thu hoạch, lùi giờ, tua ----------

const fs0 = newSave(0);
for (const id of ['vo_su', 'nu_hoa', 'ca_ngua', 'bo_de']) fs0.heroes[id].owned = true;
fs0.level = 9;
fs0.heroes.ca_ngua.star = 3;
const FT0 = 1_800_000_000_000, FH = 3600000;
const farmFormula = ['giot_suong', 'vo_su', 'nu_hoa', 'ca_ngua', 'bo_de'].map((h) => ({
  hero: h, hours: farmHours(fs0, h), rest: farmRestMin(fs0, h), rates: [0, 1, 2, 3, 4, 5, 6, 7].map((i) => farmRate(fs0, h, i)),
}));
type FarmOp = [string, number, ...(string | number)[]];
const farmOps: FarmOp[] = [
  ['tick', 0], ['place', 0, 0, 'giot_suong'], ['place', 0, 1, 'giot_suong'], ['place', 0, 1, 'vo_su'], ['place', 0, 3, 'bo_de'],
  ['tick', 1.5], ['boost', 1.5, 100], ['boost', 2, 100], ['tick', 3], ['harvest', 3], ['remove', 3, 0], ['place', 3.2, 0, 'giot_suong'],
  ['auto', 3.2], ['tick', 2], ['tick', 9], ['harvest', 9], ['remove', 9, 1], ['remove', 9, 2], ['auto', 9.1], ['travel', 0, 30],
  ['harvest', 9.1], ['auto', 40], ['tick', 70], ['harvest', 70],
];
const farmSteps = farmOps.map(([op, t, a, b]) => {
  const now = FT0 + t * FH;
  let r: unknown = null;
  if (op === 'tick') r = farmTick(fs0, now);
  else if (op === 'place') r = farmPlace(fs0, now, a as number, b as string);
  else if (op === 'remove') r = farmRemove(fs0, now, a as number);
  else if (op === 'harvest') r = farmHarvest(fs0, now);
  else if (op === 'auto') r = farmAuto(fs0, now);
  else if (op === 'boost') r = farmBoost(fs0, now);
  else if (op === 'travel') farmTravel(fs0, (a as number) * FH);
  return { op, t, a: a ?? null, b: b ?? null, r, farm: structuredClone(farmOf(fs0, now)), balls: fs0.balls };
});
write('farm.json', { t0: FT0, open: spotsOpen(fs0.level), formula: farmFormula, steps: farmSteps });
console.log('trang trại:', farmSteps.length, 'bước, chỗ mở', spotsOpen(fs0.level));

// ---------- Quảng cáo và gói: giới hạn mỗi chỗ, qua ngày, lùi ngày không mở lại lượt; Thẻ Phiêu Lưu (AFK ×1,5, 5 ô, mở 1 giờ) ----------

const ads0 = newSave(0);
type AdOp = [string, number, string?];
const adOps: AdOp[] = [
  ['use', 10, 'afk_boost'], ['use', 10, 'afk_boost'], ['use', 10, 'afk_boost'], ['use', 10, 'afk_boost'], ['use', 10, 'tree_double'],
  ['use', 10, 'cave_extra'], ['use', 10, 'cave_extra'], ['use', 9, 'afk_boost'], ['use', 11, 'afk_boost'], ['use', 11, 'farm_boost'],
  ['use', 11, 'nope'],
];
const adSteps = adOps.map(([op, day, p]) => ({ op, day, p, r: adUse(ads0, day, p!), left: adLeft(ads0, day, p!), state: structuredClone(ads0.ads) }));
const pas = newSave(0);
pas.zones.thuy = 8;
const PT0 = 1_900_000_000_000;
pas.afk.lastTick = PT0;
const passSteps: unknown[] = [];
const snapP = (t: number) => {
  const stock = treesStock(pas, t);
  return { slots: afkSlots(pas, t), times: afkChestTimes(pas, t), chests: [...pas.afk.chests], hours: pas.afk.hours, balls: pas.balls, pass: passActive(pas, t), stock, cap: treeCap(pas, t), trees: [...pas.trees!.stock] };
};
passSteps.push({ op: 'start', ...snapP(PT0) });
passSteps.push({ op: 'buy', r: buyProduct(pas, 'adventure_pass', PT0), until: pas.ent!.passUntil, ...snapP(PT0) });
passSteps.push({ op: 'buy', r: buyProduct(pas, 'adventure_pass', PT0 + 1000), until: pas.ent!.passUntil, ...snapP(PT0 + 1000) });
const t15 = PT0 + 15 * 3600000;
passSteps.push({ op: 'pending', r: afkPending(pas, t15), ...snapP(t15) });
passSteps.push({ op: 'harvest', r: treesHarvest(pas, t15), ...snapP(t15) });
passSteps.push({ op: 'noads', r: [buyProduct(pas, 'no_ads', t15), buyProduct(pas, 'no_ads', t15)], noAds: pas.ent!.noAds, ...snapP(t15) });
const tEnd = pas.ent!.passUntil + 3600000;
passSteps.push({ op: 'expired', r: afkPending(pas, tEnd), ...snapP(tEnd) });
// di chuyển bản lưu v2 -> v3: bộ đếm cũ (afk, farm, cave) dồn về ads
const migIn = [
  { afk: { adDay: 20500, adOpen: 2, adBoost: 1 }, farm: { adDay: 20500, adCount: 3 }, cave: { day: 20500, wins: 1, ad: true } },
  { afk: { adDay: 20499, adOpen: 4, adBoost: 3 }, farm: { adDay: 20500, adCount: 1 }, cave: { day: 20498, wins: 0, ad: true } },
  { afk: { adDay: 0, adOpen: 0, adBoost: 0 }, cave: { day: 20500, wins: 2, ad: false } },
];
const migrate = migIn.map((x) => {
  const o = structuredClone(x) as Record<string, unknown>;
  migrateAdsV2(o);
  return { in: x, out: o };
});
write('ads.json', { steps: adSteps, pass: passSteps, migrate, t0: PT0 });

// ---------- Cây bi: mở theo tiến độ, ra đều, đầy thì ngừng, hái giữ phần lẻ, lùi giờ, tua, Thẻ Phiêu Lưu ----------

const ts = newSave(0);
const TT0 = 1_800_000_000_000;
type TreeOp = [op: 'tick' | 'stock' | 'harvest' | 'harvest2' | 'travel' | 'zone' | 'pass', t: number, arg?: string | number];
const treeOps: TreeOp[] = [
  ['tick', 0], ['stock', 5], ['zone', 5, 'clear1'], ['stock', 6], ['stock', 8.5], ['harvest', 8.5], ['stock', 20], ['zone', 20, 'thuy'],
  ['stock', 21], ['harvest2', 21], ['stock', 23.25], ['tick', 22], ['stock', 24], ['travel', 24, 30], ['stock', 24], ['zone', 24, 'hoa'],
  ['pass', 24], ['stock', 30], ['stock', 50], ['harvest', 50], ['zone', 50, 'kim'], ['zone', 50, 'moc'], ['stock', 60],
  ['travel', 60, 24 * 30], ['stock', 60], ['harvest', 60], ['stock', 70],
];
const treeSteps = treeOps.map(([op, h, arg]) => {
  const t = TT0 + h * HR;
  let r: unknown = null;
  switch (op) {
    case 'tick': r = treesTick(ts, t); break;
    case 'stock': r = treesStock(ts, t); break;
    case 'harvest': r = treesHarvest(ts, t); break;
    case 'harvest2': r = treesHarvest(ts, t, 2); break;
    case 'travel': treesTravel(ts, (arg as number) * HR); break;
    case 'zone':
      if (arg === 'clear1') ts.zones.thuy = 1;
      else ts.zones[arg as Elem] = 8;
      break;
    case 'pass': r = buyProduct(ts, 'adventure_pass', t); break;
  }
  return { op, h, arg: arg ?? null, r, open: treesOpen(ts), cap: treeCap(ts, t), trees: structuredClone(ts.trees ?? null), balls: ts.balls };
});
write('trees.json', { t0: TT0, steps: treeSteps });
console.log('cây bi:', treeSteps.length, 'bước');
console.log('quảng cáo:', adSteps.length, 'bước; gói:', passSteps.length, 'bước');

// ---------- 40 tướng: dạng theo sao, bản lưu v3 -> v4 (gộp và đổi tướng cũ) ----------
const forms = HEROES.map((h) => ({ id: h.id, n: h.forms.length, idx: [1, 2, 3, 4, 5].map((st) => formIndex(h, st)) }));
const hp = (owned: boolean, shards: number, star: number, lv: number[], copies: number[], pot: unknown[] = [null, null, null, null]) => ({
  owned, shards, star, potential: pot,
  cards: { skill: { lv: lv[0], copies: copies[0] }, ult: { lv: lv[1], copies: copies[1] }, passive: { lv: lv[2], copies: copies[2] } },
});
const rosterIn = [
  // Y Trạch gộp vào Tiểu Y (cả hai đã có), Gia Bỉ đổi thành Nụ Hoa (chưa có Nụ Hoa), đội và trang trại đổi id
  {
    heroes: {
      tieu_y: hp(true, 0, 2, [2, 1, 1], [1, 0, 3]), y_trach: hp(true, 4, 3, [1, 3, 2], [2, 5, 0], [{ k: 'atk', r: 2 }, null, null, null]),
      gia_bi: hp(true, 0, 1, [1, 1, 1], [0, 0, 0]), vo_su: hp(true, 0, 1, [1, 1, 1], [0, 0, 0]),
    },
    team: ['y_trach', 'tieu_y', 'gia_bi'],
    farm: { lastTick: 0, boostUntil: 0, spots: [{ hero: 'tieu_y', energy: 3, stock: 1 }, { hero: 'y_trach', energy: 5, stock: 2 }, { hero: 'gia_bi', energy: 1, stock: 0 }], rest: { y_trach: 900, tieu_y: 500, gia_bi: 100 } },
  },
  // Vạn Quân và Hắc Dực cùng gộp vào Lam Quân (Lam Quân chưa có, chỉ có mảnh); Sứ Giả chưa có, chỉ có mảnh
  {
    heroes: {
      lam_quan: hp(false, 3, 1, [1, 1, 1], [0, 0, 0]), van_quan: hp(true, 0, 2, [2, 2, 1], [1, 1, 1]),
      hac_duc: hp(false, 7, 1, [1, 1, 1], [0, 0, 0]), su_gia: hp(false, 5, 1, [1, 1, 1], [0, 0, 0]),
    },
    team: ['van_quan', 'hac_duc'],
  },
];
const rosterMigrate = rosterIn.map((x) => {
  const o = structuredClone(x) as Record<string, unknown>;
  migrateRosterV3(o);
  return { in: x, out: o };
});
// tướng chính đứng trên nút ải (màn đảo) và sao chọn hình của nó
const leads = STAGES.map((st) => ({ id: st.id, hero: stageLead(st).hero, star: enemyFormStar(stageLead(st)) }));
write('roster.json', { forms, migrate: rosterMigrate, leads });
console.log('40 tướng:', forms.length, 'tướng,', rosterMigrate.length, 'bản lưu nâng v4');
