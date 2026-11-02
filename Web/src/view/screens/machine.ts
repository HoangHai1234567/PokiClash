// Máy bi: thả bi qua đinh, rơi vào ô EXP / hoàn bi / rương. Nút ×N là mức cược: tốn N bi mỗi lần thả, thưởng ×N.
import { HERO } from '../../core/data/heroes';
import { MEASURED_BALLS, MEASURED_RATES } from '../../core/data/measured';
import { RARITY_COLOR } from '../../core/elements';
import {
  Board, BALL_R, BH, BW, CHEST_NAME, CHESTS, DROP_Y, FLOOR, LEFT, maxPerDrop, openChest, RIGHT, SLOT_TOP, slotReward, spendBall, SWING,
  type Reward, type SlotKind,
} from '../../core/pachinko';
import { LEGEND_HERO, LEGEND_MILESTONE, X_STEPS, xAllowed } from '../../core/progression';
import { Rng, randomSeed } from '../../core/rng';
import { app, type Screen } from '../app';
import { INK, roughOf } from '../art';
import { clear, h, wait } from '../dom';
import { icon } from '../icons';
import { sfx } from '../sfx';
import { cardEl, heroImg, posIn } from '../ui';

type ChestKind = 'chest_wood' | 'chest_silver' | 'chest_gold';
const CHEST_COLOR: Record<ChestKind, string> = { chest_wood: '#c98a4a', chest_silver: '#c9d3dc', chest_gold: '#f7c948' };
const K = 0.86; // cỡ máy trên màn so với toạ độ máy
const MX = (540 - BW * K) / 2, MY = 112;

interface FloatText { x: number; y: number; t: number; text: string; color: string }

export function machineScreen(): Screen {
  const canvas = h('canvas', { style: `position:absolute;left:${MX}px;top:${MY}px;width:${BW * K}px;height:${BH * K}px;touch-action:none` }) as HTMLCanvasElement;
  const ctx = canvas.getContext('2d')!;
  const xCol = h('div', { class: 'col gap8', style: 'position:absolute;left:6px;top:150px;width:62px' });
  const tray = h('div', { class: 'col gap6 center', style: 'position:absolute;right:4px;top:140px;width:66px' });
  const counter = h('div', { class: 'title', style: 'font-size:16px' });
  const dropBtn = h('button', { class: 'btn red big', style: 'width:220px;touch-action:none' }, h('span', { html: icon('ball', 32) }), 'Thả bi') as HTMLButtonElement;
  const autoBtn = h('button', { class: 'btn orange' }, 'Thả liền 20') as HTMLButtonElement;
  const legend = h('div', { style: 'width:300px' });
  const header = h(
    'div',
    { class: 'row gap8', style: 'position:absolute;left:12px;right:12px;top:72px;height:38px' },
    h('div', { class: 'grow' }),
    h('button', { class: 'btn small paper', onclick: () => rates() }, h('span', { html: icon('info', 20) }), 'Tỉ lệ'),
  );
  const controls = h(
    'div',
    { class: 'col center gap6', style: `position:absolute;left:0;right:0;top:${MY + BH * K + 6}px` },
    h('div', { class: 'row gap12' }, dropBtn, autoBtn),
    h('div', { class: 'row gap12' }, counter, legend),
  );
  const el = h('div', { class: 'screen' }, header, canvas, xCol, tray, controls);

  let board = new Board(randomSeed());
  let staticBg: HTMLCanvasElement | null = null;
  let px = 1;
  let raf = 0, last = 0, acc = 0, time = 0;
  let x = 1;
  let holding = false, holdTimer = 0;
  let session = 0; // số bi đã thả trong đợt này
  let autoLeft = 0;
  const chests: { kind: ChestKind; x: number }[] = [];
  const floats: FloatText[] = [];
  const glow = new Map<number, number>(); // ô đáy sáng lên
  const pegFlash = new Map<number, number>();
  let levelBefore = 0;
  let bigReward: Reward | null = null;
  let active = false;
  const rng = new Rng(randomSeed());

  function resize() {
    px = app.scale * K * (window.devicePixelRatio || 1);
    canvas.width = Math.round(BW * px);
    canvas.height = Math.round(BH * px);
    staticBg = null;
  }
  window.addEventListener('pc-fit', resize);

  const launcherX = () => BW / 2 + Math.sin(time * 1.25) * SWING;

  // ---------- thả ----------
  function canDrop() {
    return app.save.balls >= x && session < maxPerDrop(app.save.level);
  }
  function dropOne(): boolean {
    if (!canDrop()) return false;
    if (session === 0) levelBefore = app.save.level;
    const r = spendBall(app.save, x);
    if (r) bigReward = r;
    board.drop(launcherX() + (Math.random() - 0.5) * 4, x);
    session++;
    sfx.click();
    refreshUi();
    return true;
  }
  function startHold() {
    if (!canDrop()) {
      sfx.error();
      app.toast(app.save.balls < x ? `Cần ${x} bi cho mỗi lần thả ×${x}` : `Tối đa ${maxPerDrop(app.save.level)} bi một đợt, chờ bi rơi hết`, 'ball');
      return;
    }
    holding = true;
    dropOne();
    holdTimer = 0;
  }
  dropBtn.addEventListener('pointerdown', (e) => {
    e.preventDefault();
    startHold();
  });
  window.addEventListener('pointerup', () => (holding = false));
  autoBtn.addEventListener('click', () => {
    if (autoLeft) return;
    autoLeft = Math.min(maxPerDrop(app.save.level) - session, Math.floor(app.save.balls / x));
    if (!autoLeft) {
      sfx.error();
      app.toast('Không đủ bi', 'ball');
    }
  });
  canvas.addEventListener('pointerdown', (e) => {
    e.preventDefault();
    startHold();
  });

  // ---------- bi rơi ----------
  function onLand(kind: SlotKind, slot: number, cup: boolean, bx: number, by: number, mult: number) {
    const s = app.save;
    const r = slotReward(s, kind, mult);
    if (slot >= 0) glow.set(slot, 0.5);
    if (r.k === 'exp') {
      floats.push({ x: bx, y: by - 20, t: 0, text: `+${r.n} XP`, color: '#c18cf0' });
      sfx.land();
    } else if (r.k === 'balls') {
      floats.push({ x: bx, y: by - 20, t: 0, text: `+${r.n} bi`, color: '#ff8fb3' });
      sfx.coin();
    } else if (r.k === 'chest') {
      chests.push({ kind: r.kind, x: mult });
      floats.push({ x: bx, y: by - 26, t: 0, text: CHEST_NAME[r.kind] + '!', color: CHEST_COLOR[r.kind] });
      sfx.chest();
      const from: [number, number] = [MX + bx * K, MY + by * K];
      const to = posIn(app.root, tray);
      const fly = h('div', { class: 'fly', style: `left:${from[0] - 22}px;top:${from[1] - 22}px;--chest:${CHEST_COLOR[r.kind]}`, html: icon('chest', 44) });
      app.flyLayer.appendChild(fly);
      setTimeout(() => (fly.style.transform = `translate(${to[0] - from[0]}px, ${to[1] - from[1]}px) scale(.8)`), 20);
      setTimeout(() => {
        fly.remove();
        drawTray();
      }, 640);
    }
    void cup;
    app.persist();
  }

  async function sessionEnd() {
    session = 0;
    refreshUi();
    if (bigReward && bigReward.k === 'legendCopies') {
      app.toast(`Mốc ${LEGEND_MILESTONE} bi: +${bigReward.n} bản sao thẻ Huyền thoại của ${HERO[bigReward.hero].name}`, 'star');
      bigReward = null;
    }
    if (bigReward && bigReward.k === 'hero') {
      const hero = HERO[bigReward.hero];
      bigReward = null;
      sfx.level();
      const m = app.modal(
        h(
          'div',
          { class: 'col center gap12', style: 'text-align:center' },
          h('div', { class: 'stamp', style: 'color:var(--orange);border-color:var(--orange);font-size:40px' }, 'Huyền thoại!'),
          heroImg(hero.id, 200),
          h('h2', null, hero.name),
          h('div', null, `Thả đủ ${LEGEND_MILESTONE} bi: chắc chắn nhận tướng Huyền thoại đầu tiên.`),
          h('button', { class: 'btn green', onclick: () => m.close() }, 'Vào đội!'),
        ),
        { width: 440 },
      );
    }
    // mở hết rương rồi mới báo lên cấp, để hộp thoại không chồng nhau
    if (chests.length) await openChests(levelBefore);
    else if (app.save.level > levelBefore) app.levelUp(levelBefore, app.save.level);
  }

  // ---------- rương ----------
  function drawTray() {
    clear(tray);
    tray.append(h('div', { class: 'title', style: 'font-size:12px;text-align:center;line-height:1' }, 'Rương chờ'));
    const counts: Partial<Record<ChestKind, number>> = {};
    for (const c of chests) counts[c.kind] = (counts[c.kind] ?? 0) + 1;
    for (const k of ['chest_gold', 'chest_silver', 'chest_wood'] as ChestKind[]) {
      if (!counts[k]) continue;
      tray.append(
        h(
          'div',
          { class: 'sk thin center', style: `width:60px;height:58px;--fill:#fff;position:relative;cursor:pointer;--chest:${CHEST_COLOR[k]}`, onclick: () => void openChests() },
          h('span', { html: icon('chest', 44), class: 'wob' }),
          h('div', { class: 'title', style: 'position:absolute;right:2px;bottom:-4px;font-size:15px' }, `×${counts[k]}`),
        ),
      );
    }
  }

  let opening = false;
  async function openChests(lvFrom = app.save.level) {
    if (opening || !chests.length) return;
    opening = true;
    while (chests.length && active) {
      const c = chests.shift()!;
      drawTray();
      const box = h('div', { class: 'col center gap12', style: 'text-align:center;min-height:300px' });
      const chestIc = h('div', { class: 'shake', style: `--chest:${CHEST_COLOR[c.kind]}`, html: icon('chest', 120) });
      box.append(h('h2', null, `${CHEST_NAME[c.kind]}${c.x > 1 ? ` ×${c.x}` : ''}`), chestIc);
      let next!: () => void;
      const done = new Promise<void>((r) => (next = r));
      const m = app.modal(box, { width: 470, onClose: () => next() });
      sfx.whoosh();
      await wait(650);
      chestIc.classList.remove('shake');
      void chestIc.offsetWidth;
      chestIc.classList.add('pop');
      sfx.chest();
      const rewards = openChest(app.save, c.kind, c.x, rng);
      app.persist();
      const list = h('div', { class: 'row gap8', style: 'flex-wrap:wrap;justify-content:center;max-height:520px;overflow-y:auto' });
      for (const r of rewards) list.append(rewardEl(r));
      box.append(list);
      box.append(
        h(
          'div',
          { class: 'row gap8' },
          h('button', { class: 'btn green', onclick: () => m.close() }, chests.length ? `Mở tiếp (${chests.length})` : 'Nhận'),
        ),
      );
      await done;
    }
    opening = false;
    drawTray();
    if (app.save.level > lvFrom) app.levelUp(lvFrom, app.save.level);
  }

  function rewardEl(r: Reward): HTMLElement {
    switch (r.k) {
      case 'exp':
        return h('div', { class: 'chip sk thin pop', style: 'font-size:22px' }, h('span', { html: icon('exp', 34) }), `+${r.n} XP`);
      case 'balls':
        return h('div', { class: 'chip sk thin pop', style: 'font-size:22px' }, h('span', { html: icon('ball', 34) }), `+${r.n} bi`);
      case 'card': {
        const p = app.save.heroes[r.drop.hero];
        const wrap = h('div', { class: 'col center pop', style: 'gap:2px' });
        wrap.append(cardEl(r.drop.card, p.cards[r.drop.slot].lv, { mini: true }));
        wrap.append(h('div', { class: 'small', style: `font-weight:bold;color:${RARITY_COLOR[r.drop.rarity]}` }, `${HERO[r.drop.hero].name}`));
        return wrap;
      }
      case 'stones':
        return h('div', { class: 'chip sk thin pop', style: 'font-size:22px' }, h('span', { html: icon('rock', 34) }), `+${r.n} đá tiềm năng`);
      case 'shards':
        return h('div', { class: 'chip sk thin pop' }, heroImg(r.res.hero, 40), r.res.unlocked ? `Mở khóa ${HERO[r.res.hero].name}!` : `${HERO[r.res.hero].name} +${r.res.n} mảnh`);
      default:
        return h('div');
    }
  }

  function rates() {
    // số đo do scripts/export_data.ts ghi (cùng số với bảng của Unity)
    const pct = (k: string) => `≈ ${((MEASURED_RATES[k] ?? 0) * 100).toFixed(1).replace('.', ',')} %`;
    const rows: [string, string, string][] = [
      ['chest_gold', 'Rương vàng (két giữa máy và ô khuất dưới két)', pct('chest_gold')],
      ['chest_silver', 'Rương bạc (2 cốc hai bên)', pct('chest_silver')],
      ['chest_wood', 'Rương gỗ (2 ô mép)', pct('chest_wood')],
      ['exp', 'EXP 15 (2 ô)', pct('exp15')],
      ['exp', 'EXP 10 (2 ô cạnh ô vàng)', pct('exp10')],
      ['exp', 'EXP 5 (2 ô)', pct('exp5')],
      ['ball', 'Hoàn 1 bi (2 ô)', pct('ball')],
    ];
    const table = h('div', { class: 'col gap4' });
    for (const [ic, name, p] of rows)
      table.append(h('div', { class: 'row gap8', style: `--chest:${CHEST_COLOR[ic as ChestKind] ?? ''}` }, h('span', { html: icon(ic.startsWith('chest') ? 'chest' : ic, 26) }), h('div', { class: 'grow' }, name), h('b', null, p)));
    const chestInfo = h('div', { class: 'col gap4', style: 'font-size:14px' });
    for (const k of ['chest_wood', 'chest_silver', 'chest_gold'] as ChestKind[]) {
      const tot = CHESTS[k].reduce((a, r) => a + r.w, 0);
      chestInfo.append(
        h('div', null, h('b', null, CHEST_NAME[k] + ': '), CHESTS[k].map((r) => `${Math.round((r.w / tot) * 100)}% ${({ balls: 'bi', exp: 'EXP', cards: 'thẻ', shards: 'mảnh tướng', stones: 'đá tiềm năng' })[r.k]} ${r.min}${r.max > r.min ? '–' + r.max : ''}`).join(', ')),
      );
    }
    chestInfo.append(h('div', { class: 'muted' }, `Thẻ trong rương là bản sao thẻ nội tại của tướng bạn đã có. Thẻ Huyền thoại trong Rương vàng: 0,01 % mỗi thẻ. Thả đủ ${LEGEND_MILESTONE} bi: chắc chắn ra tướng Huyền thoại đầu tiên.`));
    app.modal(
      h('div', { class: 'col gap8' }, h('h2', null, 'Tỉ lệ của máy'), h('div', { class: 'small muted' }, `Đo bằng mô phỏng ${MEASURED_BALLS.toLocaleString('vi-VN')} bi với máng thả đung đưa đều. Nút ×N nhân mọi thưởng, kể cả số thẻ trong rương.`), table, h('h3', { style: 'margin-top:8px' }, 'Trong rương'), chestInfo),
      { width: 480 },
    );
  }

  // ---------- giao diện ----------
  function refreshUi() {
    const s = app.save;
    clear(xCol);
    xCol.append(h('div', { class: 'title', style: 'font-size:12px;text-align:center;line-height:1' }, 'Cược'));
    const allowed = xAllowed(s);
    if (!allowed.includes(x)) x = 1;
    for (const st of X_STEPS) {
      const ok = allowed.includes(st.x);
      xCol.append(
        h(
          'button',
          {
            class: `btn small ${x === st.x ? 'orange' : 'paper'} ${ok ? '' : 'off'}`,
            style: 'width:60px;padding:8px 0 6px;flex-direction:column;gap:0',
            title: ok ? `Mỗi lần thả tốn ${st.x} bi, thưởng ×${st.x}` : `Mở ở cấp ${st.lv}`,
            onclick: () => {
              if (!ok || session) return;
              x = st.x;
              sfx.click();
              refreshUi();
            },
          },
          `×${st.x}`,
          ok ? null : h('span', { style: 'font-size:10px' }, `Cấp ${st.lv}`),
        ),
      );
    }
    counter.textContent = session ? `Đợt này: ${session}/${maxPerDrop(s.level)}` : `${s.balls} bi · tốn ${x}/lần`;
    autoBtn.textContent = `Thả liền ${maxPerDrop(s.level)}`;
    clear(legend);
    if (!s.legendDone) {
      const p = Math.min(1, s.ballsSpent / LEGEND_MILESTONE);
      legend.append(h('div', { class: 'bar', style: 'height:18px;--c:var(--orange)' }, h('i', { style: `width:${p * 100}%;--c:var(--orange)` }), h('b', null, `Huyền thoại chắc chắn: ${s.ballsSpent}/${LEGEND_MILESTONE}`)));
    } else legend.append(h('div', { class: 'small muted' }, `Đã nhận ${HERO[LEGEND_HERO].name}. Từ giờ Huyền thoại rất hiếm.`));
    dropBtn.classList.toggle('off', !canDrop());
  }

  // ---------- vẽ ----------
  function paintStatic(): HTMLCanvasElement {
    const c = document.createElement('canvas');
    c.width = canvas.width;
    c.height = canvas.height;
    const g = c.getContext('2d')!;
    g.scale(px, px);
    const rc = roughOf(c);
    // thân máy
    g.fillStyle = '#fff4d6';
    g.fillRect(0, 0, BW, BH);
    rc.rectangle(4, 4, BW - 8, BH - 8, { stroke: INK, strokeWidth: 4, fill: '#ffe9b0', fillStyle: 'solid', roughness: 1.6, seed: 2 });
    rc.rectangle(LEFT, 60, RIGHT - LEFT, BH - 64, { stroke: INK, strokeWidth: 2.5, fill: '#fffaf0', fillStyle: 'solid', roughness: 1.2, seed: 3 });
    // chấm bi trang trí
    g.fillStyle = 'rgba(232,85,63,.12)';
    for (let y = 80; y < SLOT_TOP - 10; y += 22)
      for (let xx = LEFT + 12 + ((y / 22) % 2) * 11; xx < RIGHT - 6; xx += 22) {
        g.beginPath();
        g.arc(xx, y, 2.2, 0, Math.PI * 2);
        g.fill();
      }
    // vai nghiêng
    for (const sg of board.segs.filter((s) => s.kind === 'shoulder')) rc.line(sg.x1, sg.y1, sg.x2, sg.y2, { stroke: INK, strokeWidth: 4, roughness: 1, seed: 5 });
    // ô đáy
    board.slots.forEach((sl, i) => {
      const kind = sl.reward;
      const color = kind === 'chest_gold' ? '#ffe27a' : kind.startsWith('chest') ? '#ffe0b0' : kind === 'ball' ? '#ffd2e2' : kind === 'exp15' ? '#e6d2ff' : kind === 'exp10' ? '#efe2ff' : '#f6efff';
      rc.rectangle(sl.x0 + 1, SLOT_TOP, sl.x1 - sl.x0 - 2, BH - SLOT_TOP - 8, { stroke: 'none', fill: color, fillStyle: 'hachure', hachureGap: 5, fillWeight: 2, roughness: 1, seed: 20 + i });
    });
    for (const sg of board.segs.filter((s) => s.kind === 'divider')) rc.line(sg.x1, sg.y1, sg.x2, sg.y2 - 8, { stroke: INK, strokeWidth: 3, roughness: 0.8, seed: 7 });
    // két vàng: thân tô vàng nhạt giữa mái và đáy, nét mái và đáy dày
    const roof = board.segs.filter((s) => s.kind === 'roof');
    const floor = board.segs.filter((s) => s.kind === 'floor');
    if (roof.length === 2 && floor.length === 2) {
      g.fillStyle = 'rgba(255,210,74,.35)';
      g.beginPath();
      g.moveTo(roof[0].x1, roof[0].y1);
      g.lineTo(roof[0].x2, roof[0].y2);
      g.lineTo(roof[1].x2, roof[1].y2);
      g.lineTo(roof[1].x1, roof[1].y1);
      g.lineTo(floor[1].x1, floor[1].y1);
      g.lineTo(floor[1].x2, floor[1].y2);
      g.lineTo(floor[0].x1, floor[0].y1);
      g.closePath();
      g.fill();
      for (const sg of [...roof, ...floor]) rc.line(sg.x1, sg.y1, sg.x2, sg.y2, { stroke: INK, strokeWidth: 4.5, roughness: 0.9, seed: 11 });
      drawChest(g, (floor[0].x2 + floor[1].x2) / 2, (roof[0].y2 + floor[0].y2) / 2 + 2, 0.4, '#f39a2d');
    }
    rc.line(LEFT, BH - 8, RIGHT, BH - 8, { stroke: INK, strokeWidth: 3, roughness: 1, seed: 8 });
    // nhãn ô
    board.slots.forEach((sl) => {
      const cx = (sl.x0 + sl.x1) / 2, w = sl.x1 - sl.x0;
      g.font = `800 ${w < 30 ? 13 : 17}px "Baloo 2"`;
      g.textAlign = 'center';
      g.lineWidth = 4;
      g.strokeStyle = INK;
      g.lineJoin = 'round';
      const k = sl.reward;
      const text = k === 'exp5' ? '5' : k === 'exp10' ? '10' : k === 'exp15' ? '15' : k === 'ball' ? '+1' : '';
      if (text) {
        g.fillStyle = k === 'ball' ? '#ff8fb3' : '#c18cf0';
        g.strokeText(text, cx, FLOOR + 6);
        g.fillText(text, cx, FLOOR + 6);
        g.font = `800 10px "Baloo 2"`;
        g.lineWidth = 3;
        const sub = k === 'ball' ? 'bi' : 'XP';
        g.strokeText(sub, cx, FLOOR + 18);
        g.fillStyle = '#fff';
        g.fillText(sub, cx, FLOOR + 18);
      } else drawChest(g, cx, FLOOR + 4, 0.38, k === 'chest_gold' ? '#f39a2d' : k === 'chest_silver' ? '#9aa6b2' : '#c98a4a');
    });
    // đinh
    board.pegs.forEach((p) => {
      if (p.kind === 'bumper') {
        // nấm chấm bi
        g.fillStyle = '#e8553f';
        g.strokeStyle = INK;
        g.lineWidth = 3;
        g.beginPath();
        g.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        g.fill();
        g.stroke();
        g.fillStyle = '#fff';
        for (const [dx, dy, rr] of [[-6, -5, 3.5], [5, -7, 2.6], [6, 4, 3], [-3, 6, 2.2]])
          {
            g.beginPath();
            g.arc(p.x + dx, p.y + dy, rr, 0, Math.PI * 2);
            g.fill();
          }
      } else if (p.kind === 'post' && p.r > 6) {
        g.fillStyle = '#c98a4a';
        g.strokeStyle = INK;
        g.lineWidth = 2.5;
        g.beginPath();
        g.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        g.fill();
        g.stroke();
      } else {
        g.fillStyle = INK;
        g.beginPath();
        g.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        g.fill();
        g.fillStyle = '#fff';
        g.beginPath();
        g.arc(p.x - 1.4, p.y - 1.4, p.r * 0.35, 0, Math.PI * 2);
        g.fill();
      }
    });
    // cốc hứng tròn (két vàng đã vẽ ở trên)
    for (const cup of board.cups) {
      if (cup.r <= 0) continue;
      const gold = cup.reward === 'chest_gold';
      const w = gold ? 26 : 30;
      g.fillStyle = gold ? '#ffd24a' : '#dfe6ee';
      g.strokeStyle = INK;
      g.lineWidth = 3;
      g.beginPath();
      g.moveTo(cup.x - w / 2, cup.y - 8);
      g.lineTo(cup.x - w / 2 + 5, cup.y + 12);
      g.lineTo(cup.x + w / 2 - 5, cup.y + 12);
      g.lineTo(cup.x + w / 2, cup.y - 8);
      g.closePath();
      g.fill();
      g.stroke();
      drawChest(g, cup.x, cup.y + 2, 0.28, gold ? '#f39a2d' : '#9aa6b2');
    }
    // ray máng thả
    rc.line(LEFT + 8, DROP_Y - 22, RIGHT - 8, DROP_Y - 22, { stroke: INK, strokeWidth: 3, roughness: 1.4, seed: 9 });
    g.font = '800 15px "Baloo 2"';
    g.textAlign = 'center';
    g.fillStyle = INK;
    g.fillText('chạm hoặc giữ để thả bi', BW / 2, 24);
    return c;
  }

  function drawChest(g: CanvasRenderingContext2D, x: number, y: number, s: number, color: string) {
    g.save();
    g.translate(x - 24 * s, y - 24 * s);
    g.scale(s, s);
    g.fillStyle = color;
    g.strokeStyle = INK;
    g.lineWidth = 4;
    g.beginPath();
    g.rect(7, 20, 34, 20);
    g.fill();
    g.stroke();
    g.beginPath();
    g.moveTo(7, 20);
    g.quadraticCurveTo(7, 7, 24, 7);
    g.quadraticCurveTo(41, 7, 41, 20);
    g.closePath();
    g.fill();
    g.stroke();
    g.fillStyle = '#ffd24a';
    g.fillRect(20, 21, 8, 10);
    g.strokeRect(20, 21, 8, 10);
    g.restore();
  }

  function draw() {
    if (!staticBg) staticBg = paintStatic();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.drawImage(staticBg, 0, 0);
    ctx.setTransform(px, 0, 0, px, 0, 0);
    // ô sáng
    for (const [i, t] of glow) {
      const sl = board.slots[i];
      ctx.fillStyle = `rgba(255,230,120,${t})`;
      ctx.fillRect(sl.x0, SLOT_TOP, sl.x1 - sl.x0, BH - SLOT_TOP - 8);
    }
    for (const [i, t] of pegFlash) {
      const p = board.pegs[i];
      ctx.fillStyle = `rgba(255,210,74,${t * 2})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r + 5, 0, Math.PI * 2);
      ctx.fill();
    }
    // máng thả: đám mây cầm bi
    const lx = launcherX();
    ctx.save();
    ctx.translate(lx, DROP_Y - 20);
    ctx.fillStyle = '#fff';
    ctx.strokeStyle = INK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    for (const [dx, dy, r] of [[-16, 2, 11], [-4, -6, 13], [10, -3, 12], [18, 4, 9]]) ctx.moveTo(dx + r, dy), ctx.arc(dx, dy, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = INK;
    ctx.beginPath();
    ctx.arc(-4, -2, 1.8, 0, Math.PI * 2);
    ctx.arc(6, -2, 1.8, 0, Math.PI * 2);
    ctx.fill();
    if (canDrop()) {
      ctx.fillStyle = '#ff8fb3';
      ctx.beginPath();
      ctx.arc(0, 20, BALL_R, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    }
    ctx.restore();
    // bi
    for (const b of board.balls) {
      ctx.fillStyle = 'rgba(255,143,179,.25)';
      ctx.beginPath();
      ctx.arc(b.x - b.vx * 0.02, b.y - b.vy * 0.02, BALL_R * 0.85, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = b.mult >= 5 ? '#ffd24a' : b.mult > 1 ? '#8ec5ff' : '#ff8fb3';
      ctx.strokeStyle = INK;
      ctx.lineWidth = 2.6;
      ctx.beginPath();
      ctx.arc(b.x, b.y, BALL_R, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = '#fff';
      ctx.beginPath();
      ctx.arc(b.x - 3, b.y - 3, 2.6, 0, Math.PI * 2);
      ctx.fill();
    }
    // chữ nổi
    for (const f of floats) {
      const k = f.t / 1.1;
      ctx.save();
      ctx.globalAlpha = k > 0.6 ? 1 - (k - 0.6) / 0.4 : 1;
      ctx.font = '800 22px "Baloo 2"';
      ctx.textAlign = 'center';
      ctx.lineWidth = 5;
      ctx.lineJoin = 'round';
      ctx.strokeStyle = INK;
      ctx.strokeText(f.text, f.x, f.y - f.t * 50);
      ctx.fillStyle = f.color;
      ctx.fillText(f.text, f.x, f.y - f.t * 50);
      ctx.restore();
    }
  }

  function frame(now: number) {
    const dt = Math.min(0.05, (now - (last || now)) / 1000);
    last = now;
    time += dt;
    acc += dt;
    while (acc >= 1 / 120) {
      acc -= 1 / 120;
      for (const e of board.step(1 / 120)) {
        if (e.t === 'peg') {
          pegFlash.set(e.peg, 0.25);
          sfx.peg(e.speed);
        } else onLand(e.reward, e.slot, e.cup, e.ball.x, Math.min(e.ball.y, FLOOR), e.ball.mult);
      }
    }
    if (holding || autoLeft) {
      holdTimer += dt;
      if (holdTimer > 0.16) {
        holdTimer = 0;
        if (!dropOne()) {
          holding = false;
          autoLeft = 0;
        } else if (autoLeft) autoLeft--;
      }
    }
    for (const [k, v] of glow) v - dt <= 0 ? glow.delete(k) : glow.set(k, v - dt);
    for (const [k, v] of pegFlash) v - dt <= 0 ? pegFlash.delete(k) : pegFlash.set(k, v - dt);
    for (let i = floats.length - 1; i >= 0; i--) if ((floats[i].t += dt) > 1.1) floats.splice(i, 1);
    if (session && !board.balls.length && !holding && !autoLeft) void sessionEnd();
    draw();
    raf = requestAnimationFrame(frame);
  }

  return {
    el,
    top: 'back',
    title: 'Máy Bi',
    enter() {
      active = true;
      board = new Board(randomSeed());
      resize();
      refreshUi();
      drawTray();
      last = 0;
      cancelAnimationFrame(raf);
      void document.fonts.ready.then(() => {
        staticBg = null;
      });
      raf = requestAnimationFrame(frame);
    },
    leave() {
      active = false;
      cancelAnimationFrame(raf);
      // bi đang rơi khi rời màn: tính luôn như ô EXP 10
      for (const b of board.balls) onLand('exp10', 4, false, b.x, b.y, b.mult);
      board.balls = [];
      if (session) void sessionEnd();
      holding = false;
      autoLeft = 0;
    },
  };
}

