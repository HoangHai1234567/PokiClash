// Kiểu dữ liệu dùng chung của phần logic. Không phụ thuộc trình duyệt: chạy được cả trong Node (máy tự chơi).

export type Elem = 'kim' | 'moc' | 'thuy' | 'hoa' | 'tho';
export type Rarity = 'common' | 'uncommon' | 'rare' | 'epic' | 'legend';
export const RARITIES: Rarity[] = ['common', 'uncommon', 'rare', 'epic', 'legend'];

// atk, def: cộng phần trăm vào chỉ số; crit: cộng tỉ lệ chí mạng; lifesteal: phần sát thương hút thành máu;
// dodge: tỉ lệ né đòn đánh thường; dmgTaken: phần sát thương nhận thêm (âm là giảm)
export type Stat = 'atk' | 'def' | 'crit' | 'lifesteal' | 'dodge' | 'dmgTaken';
export type StatusId = 'burn' | 'stun' | 'regen' | 'evade';
export type Target = 'self' | 'foe';

// until 'end': hết khi kết thúc lượt của chủ (buff đánh); 'start': hết khi bắt đầu lượt sau của chủ (buff thủ, che lượt địch)
export type Effect =
  | { k: 'buff'; stat: Stat; v: number; turns: number; until?: 'end' | 'start'; on?: Target }
  | { k: 'heal'; pct: number }
  | { k: 'maxhp'; pct: number }
  | { k: 'selfdmg'; pctCur: number }
  | { k: 'mana'; v: number; on?: Target }
  | { k: 'rage'; v: number; on?: Target }
  | { k: 'dmg'; mult: number; hits?: number; pierce?: number; lifesteal?: number }
  | { k: 'shield'; pct: number }
  | { k: 'status'; id: StatusId; turns: number; v?: number; chance?: number; on: Target }
  | { k: 'cleanse' }
  | { k: 'double' }
  | { k: 'extra'; mult: number }
  | { k: 'trueStrike'; mult: number }
  | { k: 'ifLow'; below: number; then: Effect[]; else?: Effect[] }
  | { k: 'revive'; pct: number } // chỉ dùng cho bị động 'death': lần đầu gục thì sống lại với pct máu tối đa
  | { k: 'evolve'; pct: number }; // chỉ dùng cho thẻ Tiến Hóa của boss: lên dạng sau, hồi tới pct máu tối đa của dạng mới

export type CardKind = 'pool' | 'skill' | 'ult' | 'passive';
export type PassiveTrigger = 'start' | 'turnStart' | 'lowHp' | 'onAttack' | 'onHit' | 'death';

export interface CardDef {
  id: string;
  name: string;
  rarity: Rarity;
  kind: CardKind;
  icon: string;
  effects: Effect[];
  cost?: { mana?: number; rage?: number };
  trigger?: PassiveTrigger;
  chance?: number; // bị động: tỉ lệ kích hoạt
  below?: number; // bị động lowHp: ngưỡng máu
  unlock?: number; // thẻ chung: cấp người chơi để mở
  flavor?: string;
  owner?: string; // thẻ nội tại: id tướng
}

// một dạng trong dòng tiến hóa của tướng: lên sao thì đổi dạng (mốc ở CFG.formStars)
export interface HeroForm {
  name: string;
  aola: string; // thư mục trong reskin
  size: number; // hệ số cỡ trên sân
}

export interface HeroDef {
  id: string;
  name: string;
  title: string;
  aola: string; // = forms[0].aola (chỗ chưa biết sao, như mặc định)
  elem: Elem;
  rarity: Rarity;
  // 6 chỉ số gốc của Aola (dạng 1): công, thủ, công phép, thủ phép, máu, tốc
  stats: [number, number, number, number, number, number];
  skill: string;
  ult: string;
  passive: string;
  shards: number; // số mảnh để mở
  line: string; // dòng tiến hóa (để hiển thị)
  size: number; // = forms[0].size
  forms: HeroForm[]; // 1–3 dạng, dạng 1 trước
}

// phần cộng của side meta (huy hiệu, đá tiềm năng): phần trăm Máu, Công, Thủ và cộng thẳng Tốc
export interface StatMods {
  hpPct: number;
  atkPct: number;
  defPct: number;
  spd: number;
}

// hiệu ứng đầu trận của tiềm năng: mana, nộ cộng lúc dựng tướng; chí mạng, hút máu thành buff cả trận
export interface BattleStart {
  mana: number;
  rage: number;
  crit: number;
  lifesteal: number;
}

export interface Member {
  heroId: string;
  level: number;
  star: number;
  cardLv: { skill: number; ult: number; passive: number };
  boss?: boolean;
  evo?: boolean; // boss có thẻ Tiến Hóa (BOSS_EVO): vào trận ở dạng 1, gần chết thì lên dạng sau
  mods?: StatMods;
  start?: BattleStart;
}

export interface TeamSetup {
  name: string;
  ai: boolean;
  members: Member[];
}
