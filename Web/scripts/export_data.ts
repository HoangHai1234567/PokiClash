// Xuất dữ liệu game (tướng, thẻ, đảo, ải, cấu hình) ra JSON cho Unity: npx tsx scripts/export_data.ts [thư mục đích]
// Mặc định ghi vào ../Assets/02 Data/Json. Một nguồn: sửa số ở web rồi chạy lại, Unity không sửa tay.
import { TREES } from '../src/core/data/trees';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { AFK, AFK_CHEST } from '../src/core/afk';
import { SIM_TEAMS } from '../src/core/sim';
import { BADGE } from '../src/core/data/badges';
import { CAVE, POTENTIAL } from '../src/core/data/potential';
import { FARM, FARM_SPOTS } from '../src/core/data/farm';
import { AD_LIMITS, PASS, PRODUCTS } from '../src/core/data/ads';
import { CFG } from '../src/core/data/config';
import { INNATE, POOL, POOL_WEIGHT } from '../src/core/data/cards';
import { HEROES, LEGEND_MILESTONE_HERO, STARTERS } from '../src/core/data/heroes';
import { STAGES, WORLD_VILLAGE, ZONES } from '../src/core/data/stages';
import { Board, BW, CHESTS, LEGEND_COPIES, MAX_PER_DROP, MAX_PER_DROP_HIGH, MAX_PER_DROP_LEVEL, SWING, type SlotKind } from '../src/core/pachinko';
import {
  AFK_CAP_H, CARD_MAX, CARD_REQ, EXP_BASE, EXP_POW, FORM_STARS, LEGEND_MILESTONE, MAX_LEVEL, MAX_STAR, SAVE_VERSION, STAR_CARDS,
  STAR_LEVEL, X_STEPS,
} from '../src/core/progression';

const out = resolve(process.argv[2] ?? join(import.meta.dirname, '../../Assets/02 Data/Json'));
mkdirSync(out, { recursive: true });

// tỉ lệ từng loại ô của máy bi: mô phỏng 6.000 bi thả đều (bảng "Tỉ lệ" trong game đọc số này)
function pachinkoRates() {
  const board = new Board(7);
  const count: Partial<Record<SlotKind, number>> = {};
  let landed = 0, dropped = 0, frame = 0;
  const total = 6000;
  while (landed < total && frame < 200000) {
    if (dropped < total && frame % 6 === 0) {
      board.drop(BW / 2 + ((((dropped * 0.6180339887498949) % 1) * 2) - 1) * SWING, 1);
      dropped++;
    }
    for (const e of board.step(1 / 60)) if (e.t === 'land') {
      landed++;
      count[e.reward] = (count[e.reward] ?? 0) + 1;
    }
    frame++;
  }
  const out: Record<string, number> = {};
  for (const [k, v] of Object.entries(count)) out[k] = Math.round((v / total) * 10000) / 10000;
  return { balls: total, rates: out };
}

const measured = pachinkoRates();
// bảng "Tỉ lệ" của web đọc cùng số đo (file sinh tự động, đừng sửa tay)
writeFileSync(
  join(import.meta.dirname, '../src/core/data/measured.ts'),
  '// Sinh bởi scripts/export_data.ts: tỉ lệ từng loại ô của máy bi, mô phỏng ' + measured.balls + ' bi thả đều. Đừng sửa tay.\n' +
    'export const MEASURED_BALLS = ' + measured.balls + ';\n' +
    'export const MEASURED_RATES: Record<string, number> = ' + JSON.stringify(measured.rates) + ';\n',
  'utf8',
);

const files: Record<string, unknown> = {
  'heroes.json': { heroes: HEROES, starters: STARTERS, legendMilestoneHero: LEGEND_MILESTONE_HERO },
  'cards.json': { pool: POOL, innate: INNATE },
  'zones.json': { zones: ZONES, village: WORLD_VILLAGE },
  'stages.json': { stages: STAGES },
  'balance.json': {
    cfg: CFG,
    progression: {
      saveVersion: SAVE_VERSION, maxLevel: MAX_LEVEL, expBase: EXP_BASE, expPow: EXP_POW, afkCapH: AFK_CAP_H, legendMilestone: LEGEND_MILESTONE,
      cardMax: CARD_MAX, maxStar: MAX_STAR, xSteps: X_STEPS, cardReq: CARD_REQ, starCards: STAR_CARDS, starLevel: STAR_LEVEL,
      formStars: FORM_STARS,
    },
    poolWeight: POOL_WEIGHT,
    pachinko: {
      maxPerDrop: MAX_PER_DROP, maxPerDropHigh: MAX_PER_DROP_HIGH, maxPerDropLevel: MAX_PER_DROP_LEVEL, legendCopies: LEGEND_COPIES,
      chests: CHESTS,
      measured,
    },
    afk: { ...AFK, chest: AFK_CHEST },
    simTeams: SIM_TEAMS,
    badges: BADGE,
    potential: POTENTIAL,
    cave: CAVE,
    farm: { ...FARM, spots: FARM_SPOTS },
    trees: TREES,
    ads: { limits: AD_LIMITS, pass: PASS, products: PRODUCTS },
  },
};

for (const [name, data] of Object.entries(files)) {
  writeFileSync(join(out, name), JSON.stringify(data, null, 1) + '\n', 'utf8');
  console.log('ghi', join(out, name));
}
console.log(`tướng ${HEROES.length}, thẻ chung ${POOL.length}, thẻ riêng ${INNATE.length}, đảo ${ZONES.length}, ải ${STAGES.length}`);
