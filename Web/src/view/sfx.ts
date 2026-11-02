// Âm thanh tổng hợp bằng WebAudio (không có file âm thanh): tiếng "bụp", "keng", "soạt" kiểu đồ chơi.
let ctx: AudioContext | null = null;
let on = true;
let lastPeg = 0;

export function setSound(v: boolean) {
  on = v;
}

function ac(): AudioContext | null {
  if (!on) return null;
  try {
    if (!ctx) ctx = new AudioContext();
    if (ctx.state === 'suspended') void ctx.resume();
    return ctx;
  } catch {
    return null;
  }
}

function tone(freq: number, dur: number, type: OscillatorType = 'sine', vol = 0.12, slide = 0, delay = 0) {
  const a = ac();
  if (!a) return;
  const t = a.currentTime + delay;
  const o = a.createOscillator();
  const g = a.createGain();
  o.type = type;
  o.frequency.setValueAtTime(freq, t);
  if (slide) o.frequency.exponentialRampToValueAtTime(Math.max(30, freq + slide), t + dur);
  g.gain.setValueAtTime(0.0001, t);
  g.gain.exponentialRampToValueAtTime(vol, t + 0.01);
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  o.connect(g).connect(a.destination);
  o.start(t);
  o.stop(t + dur + 0.02);
}

function noise(dur: number, vol = 0.1, freq = 1200, q = 0.8, delay = 0) {
  const a = ac();
  if (!a) return;
  const t = a.currentTime + delay;
  const len = Math.floor(a.sampleRate * dur);
  const buf = a.createBuffer(1, len, a.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / len);
  const src = a.createBufferSource();
  src.buffer = buf;
  const f = a.createBiquadFilter();
  f.type = 'bandpass';
  f.frequency.value = freq;
  f.Q.value = q;
  const g = a.createGain();
  g.gain.value = vol;
  src.connect(f).connect(g).connect(a.destination);
  src.start(t);
}

export const sfx = {
  click: () => tone(660, 0.07, 'triangle', 0.08, 200),
  pick: () => { noise(0.12, 0.12, 2400, 1.2); tone(520, 0.08, 'triangle', 0.05, 300); },
  deal: () => noise(0.08, 0.06, 3200, 1.5),
  card: () => { tone(440, 0.09, 'square', 0.04, 220); noise(0.06, 0.05, 1800); },
  hit: (crit = false) => { noise(0.18, crit ? 0.32 : 0.22, 500, 0.7); tone(crit ? 180 : 140, 0.18, 'sine', 0.22, -80); },
  whoosh: () => noise(0.25, 0.1, 900, 0.5),
  heal: () => { tone(660, 0.12, 'sine', 0.07); tone(880, 0.16, 'sine', 0.07, 0, 0.08); },
  buff: () => { tone(500, 0.08, 'triangle', 0.06, 300); tone(750, 0.1, 'triangle', 0.06, 300, 0.07); },
  debuff: () => tone(400, 0.2, 'sawtooth', 0.04, -200),
  shield: () => { tone(300, 0.15, 'square', 0.04, 200); noise(0.1, 0.05, 4000); },
  miss: () => tone(900, 0.15, 'sine', 0.05, -500),
  coin: () => { tone(988, 0.07, 'square', 0.05); tone(1319, 0.14, 'square', 0.05, 0, 0.06); },
  peg: (speed: number) => {
    const now = performance.now();
    if (now - lastPeg < 35) return;
    lastPeg = now;
    tone(1100 + Math.random() * 500, 0.04, 'triangle', Math.min(0.06, speed / 9000));
  },
  land: () => tone(330, 0.12, 'triangle', 0.08, -100),
  chest: () => { noise(0.2, 0.12, 700); [523, 659, 784, 1047].forEach((f, i) => tone(f, 0.18, 'triangle', 0.07, 0, 0.12 + i * 0.07)); },
  level: () => [523, 659, 784, 1047, 1319].forEach((f, i) => tone(f, 0.22, 'square', 0.05, 0, i * 0.09)),
  win: () => [392, 523, 659, 784, 1047].forEach((f, i) => tone(f, 0.25, 'triangle', 0.08, 0, i * 0.11)),
  lose: () => [392, 349, 311, 262].forEach((f, i) => tone(f, 0.3, 'triangle', 0.07, 0, i * 0.16)),
  ult: () => { noise(0.5, 0.18, 300, 0.5); tone(110, 0.6, 'sawtooth', 0.08, 220); },
  swap: () => { noise(0.15, 0.08, 1500); tone(380, 0.12, 'triangle', 0.06, 380); },
  error: () => tone(160, 0.15, 'square', 0.05),
  stamp: () => { noise(0.12, 0.3, 300, 0.6); tone(90, 0.2, 'sine', 0.25, -40); },
};
