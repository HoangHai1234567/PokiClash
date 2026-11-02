// Đổi hiệu ứng của thẻ ra chữ tiếng Việt, theo cấp thẻ, để mô tả luôn khớp với số thật.
import { CFG } from './data/config';
import type { CardDef, Effect, Stat } from './types';

const r2 = (x: number) => Math.round(x * 100) / 100;

export function lvFactor(lv: number): number {
  return 1 + CFG.cardLvStep * (lv - 1);
}

export function scaleEffects(effects: Effect[], lv: number): Effect[] {
  if (lv <= 1) return effects;
  const f = lvFactor(lv);
  return effects.map((e): Effect => {
    switch (e.k) {
      case 'buff':
        return { ...e, v: r2(e.v * f) };
      case 'heal':
        return { ...e, pct: r2(e.pct * f) };
      case 'maxhp':
        return { ...e, pct: r2(e.pct * f) };
      case 'selfdmg':
        return { ...e, pctCur: r2(e.pctCur / f) };
      case 'mana':
      case 'rage':
        return { ...e, v: Math.round(e.v * f) };
      case 'dmg':
        return { ...e, mult: r2(e.mult * f), lifesteal: e.lifesteal ? r2(e.lifesteal * f) : undefined };
      case 'shield':
        return { ...e, pct: r2(e.pct * f) };
      case 'status':
        return {
          ...e,
          v: e.v ? r2(e.v * f) : e.v,
          chance: e.chance ? Math.min(1, r2(e.chance * f)) : e.chance,
        };
      case 'extra':
        return { ...e, mult: r2(e.mult * f) };
      case 'trueStrike':
        return { ...e, mult: r2(e.mult * f) };
      case 'ifLow':
        return { ...e, then: scaleEffects(e.then, lv), else: e.else ? scaleEffects(e.else, lv) : undefined };
      case 'revive':
        return { ...e, pct: Math.min(1, r2(e.pct * f)) };
      default:
        return e;
    }
  });
}

export const pct = (x: number) => `${Math.round(x * 100)}%`;
const lowFirst = (t: string) => t.charAt(0).toLowerCase() + t.slice(1);

const STAT_NAME: Record<Stat, string> = {
  atk: 'Công',
  def: 'Thủ',
  crit: 'chí mạng',
  lifesteal: 'hút máu',
  dodge: 'né',
  dmgTaken: 'sát thương nhận',
};

function turnsText(turns: number, until: 'end' | 'start', foe: boolean): string {
  if (turns >= 99) return ' cả trận';
  if (foe) return turns === 1 ? ' 1 lượt' : ` ${turns} lượt`;
  if (until === 'start') return turns === 1 ? ' tới lượt sau' : ` trong ${turns} lượt địch`;
  return turns === 1 ? ' lượt này' : ` trong ${turns} lượt`;
}

export function effectText(e: Effect): string {
  switch (e.k) {
    case 'buff': {
      const foe = e.on === 'foe';
      const until = e.until ?? (e.stat === 'def' || e.stat === 'dmgTaken' || e.stat === 'dodge' ? 'start' : 'end');
      const sign = e.v >= 0 ? '+' : '−';
      const t = turnsText(e.turns, until, foe);
      if (e.stat === 'lifesteal') return `Hút ${pct(e.v)} sát thương thành máu${t}`;
      if (e.stat === 'dodge') return `${pct(e.v)} né đòn đánh thường${t}`;
      if (e.stat === 'dmgTaken') return `${e.v < 0 ? 'Giảm' : 'Nhận thêm'} ${pct(Math.abs(e.v))} sát thương${t}`;
      return `${foe ? 'Địch ' : ''}${sign}${pct(Math.abs(e.v))} ${STAT_NAME[e.stat]}${t}`;
    }
    case 'heal':
      return `Hồi ${pct(e.pct)} máu`;
    case 'maxhp':
      return `+${pct(e.pct)} máu tối đa cả trận`;
    case 'selfdmg':
      return `Mất ${pct(e.pctCur)} máu đang có`;
    case 'mana':
      if (e.on === 'foe') return `Hút ${Math.abs(e.v)} mana của địch`;
      return `+${e.v} mana`;
    case 'rage':
      if (e.on === 'foe') return `Hút ${Math.abs(e.v)} nộ của địch`;
      return `+${e.v} nộ`;
    case 'dmg': {
      let s = e.hits && e.hits > 1 ? `Đánh ${e.hits} lần, mỗi lần ${pct(e.mult)} Công` : `Gây ${pct(e.mult)} Công sát thương`;
      if (e.pierce) s += `, xuyên ${pct(e.pierce)} Thủ`;
      if (e.lifesteal) s += `, hút ${pct(e.lifesteal)} thành máu`;
      return s;
    }
    case 'shield':
      return `Khiên bằng ${pct(e.pct)} máu tối đa`;
    case 'status': {
      const c = e.chance && e.chance < 1 ? `${pct(e.chance)} cơ hội: ` : '';
      if (e.id === 'burn') return `${c}Đốt địch ${e.turns} lượt (${pct(e.v ?? 0)} máu mỗi lượt)`;
      if (e.id === 'regen') return `${c}Hồi ${pct(e.v ?? 0)} máu đầu mỗi lượt, ${e.turns} lượt`;
      if (e.id === 'stun') return `${c}Làm địch choáng`;
      if (e.id === 'evade') return `${c}Né trọn đòn đánh kế tiếp`;
      return '';
    }
    case 'cleanse':
      return 'Xoá hiệu ứng xấu';
    case 'double':
      return 'Thẻ kế tiếp chạy 2 lần';
    case 'extra':
      return `Cuối lượt đánh thêm một cú ${pct(e.mult)} Công`;
    case 'trueStrike':
      return `Đòn đánh lượt này bỏ qua Thủ, ×${String(e.mult).replace('.', ',')}`;
    case 'ifLow':
      return `Máu dưới ${pct(e.below)}: ${lowFirst(e.then.map(effectText).join(', '))}` +
        (e.else ? `. Không thì: ${lowFirst(e.else.map(effectText).join(', '))}` : '');
    case 'revive':
      return `Hồi sinh với ${pct(e.pct)} máu`;
    case 'evolve':
      return `Tiến hóa, hồi ${e.pct >= 1 ? 'đầy' : `tới ${pct(e.pct)}`} máu, máu và Công tăng`;
  }
}

export function cardText(c: CardDef, lv = 1): string {
  const body = scaleEffects(c.effects, lv).map(effectText).join('. ');
  if (c.kind !== 'passive') return body + '.';
  if (c.effects[0]?.k === 'evolve') return `Khi máu dưới ${pct(c.below ?? 0.25)}, nếu còn dạng sau: ${lowFirst(body)}.`;
  switch (c.trigger) {
    case 'start':
      return `Vào trận: ${body.charAt(0).toLowerCase()}${body.slice(1)}.`;
    case 'turnStart':
      return `Đầu mỗi lượt: ${body.charAt(0).toLowerCase()}${body.slice(1)}.`;
    case 'lowHp':
      return `Lần đầu máu dưới ${pct(c.below ?? 0.3)}: ${body.charAt(0).toLowerCase()}${body.slice(1)}.`;
    case 'onAttack': {
      const ch = Math.min(1, (c.chance ?? 1) * lvFactor(lv));
      return `Mỗi đòn đánh thường: ${pct(ch)} cơ hội ${body.charAt(0).toLowerCase()}${body.slice(1)}.`;
    }
    case 'onHit':
      return `Mỗi lần bị đánh: ${body.charAt(0).toLowerCase()}${body.slice(1)}.`;
    case 'death':
      return `Lần đầu gục: ${body.charAt(0).toLowerCase()}${body.slice(1)}.`;
  }
  return body + '.';
}

export function costText(c: CardDef): string {
  const parts: string[] = [];
  if (c.cost?.rage) parts.push(`${c.cost.rage} nộ`);
  if (c.cost?.mana) parts.push(`${c.cost.mana} mana`);
  return parts.join(' + ');
}

export const KIND_NAME = { pool: 'Thẻ chung', skill: 'Chiêu', ult: 'Tuyệt kỹ', passive: 'Bị động' } as const;
