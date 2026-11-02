// Chỉnh mặt máy bi cho tỉ lệ từng loại ô giữ như mặt máy cũ: npx tsx scripts/tune_pachinko.ts [vòng ô, mặc định 4] [vòng cốc, mặc định 3]
// Bước 1: cỡ cốc bạc và khe két vàng (tỉ lệ cốc gần như không phụ thuộc độ rộng ô).
// Bước 2: độ rộng ô đối xứng. Tỉ lệ một loại ô ≈ mật độ × (độ rộng − 18), vì tâm bi chỉ lọt phần ô trừ hai nửa bi ở
// hai vách. Mỗi vòng nhân phần hiệu dụng (w − 18) theo mục tiêu / đo (giảm chấn), co giãn chung cho tổng đúng 432,
// ô tối thiểu 22. Tỉ lệ dao động khoảng ±0,5 điểm giữa các lần chạy do bi va bi; đạt khi mọi loại lệch dưới 1 điểm.
// In số đề xuất để chép vào src/core/pachinko.ts (SLOT_W, CUPS.silverR, VAULT.slit) và Core/Pachinko.cs.
import { Board, BW, CUPS, LEFT, RIGHT, SLOT_LAYOUT, SLOT_W, SWING, VAULT, type SlotKind } from '../src/core/pachinko';

// tỉ lệ của mặt máy cũ (scripts/export_data.ts, 6.000 bi): giữ nguyên kinh tế mỗi bi
export const TARGET: Record<SlotKind, number> = {
  chest_gold: 0.0343, chest_silver: 0.0597, chest_wood: 0.0747, exp15: 0.22, exp10: 0.2275, exp5: 0.296, ball: 0.0878,
};
// phần vàng đến từ ô khuất dưới đáy két; phần còn lại do két
export const GOLD_HIDDEN = 0.011;
const MIN_W = 22;

export type Run = { cup: Record<string, number>; slot: Record<string, number>; total: number; flight: number[]; frames: number };

// cùng cách thả với export_data.ts (dãy tỉ lệ vàng)
export function run(widths: readonly number[], total = 6000, seed = 7): Run {
  const board = new Board(seed, widths);
  const cup: Record<string, number> = {}, slot: Record<string, number> = {};
  const flight: number[] = [];
  let landed = 0, dropped = 0, frame = 0;
  while (landed < total && frame < 200000) {
    if (dropped < total && frame % 6 === 0) {
      board.drop(BW / 2 + ((((dropped * 0.6180339887498949) % 1) * 2) - 1) * SWING, 1);
      dropped++;
    }
    for (const e of board.step(1 / 60)) if (e.t === 'land') {
      landed++;
      flight.push(e.ball.age);
      if (e.cup) cup[e.reward] = (cup[e.reward] ?? 0) + 1;
      else slot[e.reward] = (slot[e.reward] ?? 0) + 1;
    }
    frame++;
  }
  return { cup, slot, total, flight, frames: frame };
}

const rate = (r: Run, m: Record<string, number>, k: string) => (m[k] ?? 0) / r.total;
const round = (x: number) => Math.round(x * 4) / 4;

function report(tag: string, r: Run) {
  const fl = [...r.flight].sort((a, b) => a - b);
  console.log(`\n${tag}\n  ${r.total} bi, bay trung vị ${fl[fl.length >> 1].toFixed(2)} s, p90 ${fl[Math.floor(fl.length * 0.9)].toFixed(2)} s, max ${fl[fl.length - 1].toFixed(2)} s`);
  for (const k of Object.keys(TARGET) as SlotKind[]) {
    const v = rate(r, r.cup, k) + rate(r, r.slot, k);
    console.log(`  ${k.padEnd(13)} ${(v * 100).toFixed(2).padStart(6)}%  (mục tiêu ${(TARGET[k] * 100).toFixed(2)}%)` +
      (k === 'chest_gold' ? `  két ${(rate(r, r.cup, k) * 100).toFixed(2)}%, ô khuất ${(rate(r, r.slot, k) * 100).toFixed(2)}%` : ''));
  }
}

if (process.argv[1]?.replace(/\\/g, '/').endsWith('scripts/tune_pachinko.ts')) {
  const loops = Number(process.argv[2] ?? 4), cupLoops = Number(process.argv[3] ?? 3);
  const HALF = (RIGHT - LEFT) / 2;
  console.log('bố cục:', SLOT_LAYOUT.join(' '));
  let r = run(SLOT_W, 3000);
  report(`bắt đầu: ${JSON.stringify(SLOT_W)} bạc r ${CUPS.silverR} khe ${VAULT.slit}`, r);

  // bước 1: cốc bạc (tỉ lệ gần tỉ lệ thuận với bán kính) và khe két (theo phần khe trống cho tâm bi: khe − 2R)
  for (let i = 0; i < cupLoops; i++) {
    CUPS.silverR = round(CUPS.silverR * TARGET.chest_silver / Math.max(0.001, rate(r, r.cup, 'chest_silver')));
    const vaultWant = TARGET.chest_gold - GOLD_HIDDEN, vaultGot = Math.max(0.001, rate(r, r.cup, 'chest_gold'));
    VAULT.slit = round(18 + (VAULT.slit - 18) * Math.pow(vaultWant / vaultGot, 0.8));
    r = run(SLOT_W, 3000);
    report(`cốc vòng ${i + 1}: bạc r ${CUPS.silverR}, khe ${VAULT.slit}`, r);
  }

  // bước 2: độ rộng ô (một nửa máy từ ngoài vào: gỗ, 15, 5, bi, 10; rồi ô khuất ở giữa)
  const SIDE: SlotKind[] = ['chest_wood', 'exp15', 'exp5', 'ball', 'exp10'];
  const want: Record<string, number> = { ...TARGET, mid: GOLD_HIDDEN };
  let w = [...SLOT_W];
  for (let i = 0; i < loops; i++) {
    r = run(w, 6000);
    report(`ô vòng ${i + 1}: ${JSON.stringify(w)} (tổng ${w.reduce((a, b) => a + b, 0)})`, r);
    const eff: Record<string, number> = { mid: w[5] - 18 };
    SIDE.forEach((k, j) => (eff[k] = w[j] - 18));
    const got: Record<string, number> = { mid: rate(r, r.slot, 'chest_gold') };
    for (const k of SIDE) got[k] = rate(r, r.slot, k);
    for (const k of Object.keys(eff)) eff[k] = Math.max(MIN_W - 18, eff[k] * Math.pow(want[k] / Math.max(0.0005, got[k]), 0.7));
    const sumEff = eff.mid + 2 * SIDE.reduce((a, k) => a + eff[k], 0);
    const room = 2 * HALF - 18 * 11;
    for (const k of Object.keys(eff)) eff[k] *= room / sumEff;
    const side = SIDE.map((k) => round(eff[k] + 18));
    w = [...side, round(eff.mid + 18), ...[...side].reverse()];
    w[0] = w[10] = round((2 * HALF - w.slice(1, 10).reduce((a, b) => a + b, 0)) / 2);
  }
  console.log(`\nchép vào pachinko.ts: SLOT_W = ${JSON.stringify(w)}; CUPS.silverR = ${CUPS.silverR}; VAULT.slit = ${VAULT.slit}`);
}
