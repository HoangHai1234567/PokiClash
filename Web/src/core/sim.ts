// Máy tự chơi cả trận (cả hai bên do máy chọn), dùng cho script đo và bảng thử trong game.
import { aiTurn } from './ai';
import { advance, aiForcedChoice, createBattle, execute, forceSwap, startBattle, type Battle } from './battle';
import { STAGE, STAGES, ZONES } from './data/stages';
import { enemyTeam, newSave, playerTeam, type SaveData } from './progression';
import type { Elem } from './types';

export function runBattle(b: Battle): Battle {
  startBattle(b);
  let guard = 0;
  while (b.phase !== 'over' && guard++ < 2000) {
    if (b.phase === 'forceSwap') {
      forceSwap(b, aiForcedChoice(b, b.turn.side));
      continue;
    }
    if (b.phase === 'picking') {
      aiTurn(b, 0.15);
      execute(b);
      continue;
    }
    advance(b);
  }
  return b;
}

export function simulateStage(s: SaveData, stageId: number, team: string[], n: number, seed = 1) {
  let win = 0, rounds = 0;
  for (let i = 0; i < n; i++) {
    const b = runBattle(createBattle([{ ...playerTeam(s, team), ai: true }, enemyTeam(STAGE[stageId])], seed + i * 7919, [s.level, s.level]));
    if (b.winner === 0) win++;
    rounds += b.round;
  }
  return { win: win / n, rounds: rounds / n };
}

// ---------- bảng đo theo đảo (npm run sim -- battle, cửa sổ Cân bằng của Unity) ----------

// mỗi đảo một đội hợp lý (tướng khắc hệ đảo), sao và cấp thẻ theo độ sâu của đảo
export const SIM_TEAMS: Record<Elem, { team: string[]; star: number; card: number }> = {
  // 40 tướng (2026-11-02): đội cũ đổi sang tướng thay cùng hệ, cùng độ hiếm; Đảo Thủy là tướng khởi đầu và 2 tướng tặng
  thuy: { team: ['giot_suong', 'vo_su', 'nu_hoa'], star: 1, card: 1 },
  hoa: { team: ['ca_ngua', 'giot_suong', 'vo_su'], star: 2, card: 2 },
  kim: { team: ['phap_luan', 'bo_de', 'ca_ngua'], star: 2, card: 2 },
  moc: { team: ['soi_linh', 'bo_cap', 'bu_long'], star: 3, card: 3 },
  tho: { team: ['de_hoa', 'nu_hoa', 'soi_linh'], star: 3, card: 3 },
};

// 5 mức cấp quanh khoảng đề nghị của đảo
export const simLevels = (lv: [number, number]) =>
  [lv[0] - 2, lv[0], Math.round((lv[0] + lv[1]) / 2), lv[1], lv[1] + 2].map((l) => Math.max(1, l));

// bản lưu giả cho một ô của bảng: đội, cấp, sao, cấp cả 3 thẻ
export function simSave(team: string[], level: number, star: number, card: number): SaveData {
  const s = newSave(0);
  s.level = level;
  s.team = team;
  for (const h of team) {
    const hp = s.heroes[h];
    hp.owned = true;
    hp.star = star;
    hp.cards.skill.lv = hp.cards.ult.lv = hp.cards.passive.lv = card;
  }
  return s;
}

// N trận mỗi ô; hạt giống 1000 + i × 7919 như script đo
export function zoneTable(n: number) {
  return ZONES.map((z) => {
    const zt = SIM_TEAMS[z.id];
    const lvls = simLevels(z.level);
    return {
      zone: z.id, levels: lvls,
      stages: STAGES.filter((x) => x.zone === z.id).map((st) => ({
        id: st.id,
        cells: lvls.map((lv) => {
          const s = simSave(zt.team, lv, zt.star, zt.card);
          let win = 0, rounds = 0;
          for (let i = 0; i < n; i++) {
            const b = runBattle(createBattle([{ ...playerTeam(s), ai: true }, enemyTeam(st)], 1000 + i * 7919, [lv, lv]));
            if (b.winner === 0) win++;
            rounds += b.round;
          }
          return { win, rounds };
        }),
      })),
    };
  });
}
