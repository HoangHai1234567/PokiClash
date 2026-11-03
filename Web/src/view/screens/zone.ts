// Scene đảo một hệ: ảnh đảo to, các ải dọc đường mòn từ bãi dưới lên hang boss, thanh tiến độ có rương mốc,
// khung "ải tiếp theo" ở dưới. Trong một đảo, ải mở lần lượt.
// Đảo 8 ải (hệ thống cũ): mỗi ải một nút. Đảo 70 ải (islands.ts): 10 ải tướng là mốc lớn, ải xen giữa là chấm nhỏ trên đường;
// chạm mốc hoặc chấm thì mở bảng chặng (các ải từ ải tướng đó tới trước ải tướng sau).
import { BOSS_EVO } from '../../core/data/cards';
import { CFG } from '../../core/data/config';
import { HERO, HEROES, STARTERS } from '../../core/data/heroes';
import { TAG_NAME } from '../../core/data/islands';
import { isMinion } from '../../core/data/minions';
import { STAGE, V2_ZONES, ZONE, ZONE_CHESTS, zoneSize, zoneStages, type StageDef, type StageEnemy, type ZoneDef } from '../../core/data/stages';
import { ELEM_COLOR, ELEM_NAME, elemMult, BEATS } from '../../core/elements';
import {
  claimZoneChest, enemyFormStar, FORM_STARS, nextStage, stageBalls, stageCleared, stageLead, stageOpen, TEAM_SLOT_ZONES, teamSlots, zoneChestReady,
} from '../../core/progression';
import { cardText } from '../../core/cardtext';
import { Rng, randomSeed } from '../../core/rng';
import type { Elem } from '../../core/types';
import { app, type Screen } from '../app';
import { clear, h } from '../dom';
import { icon } from '../icons';
import { drawZoneFallback, preloadIcons, sceneBackdrop, SH, SW } from '../scenery';
import { sfx } from '../sfx';
import { cardEl, elemTag, heroImg, stars } from '../ui';
import { difficulty } from './world';

// hệ khắc hệ z (để gợi ý)
const counterOf = (z: Elem): Elem => (Object.keys(BEATS) as Elem[]).find((k) => BEATS[k] === z)!;

// bản đồ đảo phóng to và cuộn dọc, để ải ở hai đầu không bị khung trên dưới che; đảo 70 ải phóng to hơn cho đủ chỗ chấm ải
const MK1 = 1.27, MK2 = 2.2, PAD_T = 110, PAD_B = 150;
const isV2 = (z: Elem) => V2_ZONES.includes(z);
const dims = (z: Elem) => {
  const mk = isV2(z) ? MK2 : MK1;
  return { mk, MW: Math.round(SW * mk), MH: Math.round(SH * mk) };
};
const pathSvg = (d: string, w: number, hh: number) =>
  `<svg width="${w}" height="${hh}" class="boil-self"><path d="${d}" fill="none" stroke="#2b2118" stroke-width="9" stroke-linecap="round" stroke-dasharray="14 12" opacity=".5"/><path d="${d}" fill="none" stroke="#ffe08a" stroke-width="5" stroke-linecap="round" stroke-dasharray="14 12"/></svg>`;
const nodeSize = (st: StageDef) => (st.kind === 'boss' ? 86 : st.kind === 'mini' ? 72 : 58);
// nhãn dưới hình địch: cấp, BOSS, cường hóa (+%) hoặc yếu đi (−%)
function enemyLabel(e: StageEnemy) {
  const b = e.buff ? ` ${e.buff > 0 ? '+' : '−'}${Math.round(Math.abs(e.buff) * 100)}%` : '';
  return `Lv${e.level}${e.boss ? ' BOSS' : ''}${b}`;
}
const TAG_FILL = { hero: '#ffd9a0', minion: '#dfe9f3', buff: '#ffc9bd', group: '#e7dcf5', pair: '#e7dcf5', elite: '#ffc9bd', gate: '#ffb3a3' };
// nhãn kiểu ải (đảo 70 ải)
function tagChip(st: StageDef) {
  const text = st.kind === 'boss' ? 'Boss đảo' : st.kind === 'mini' ? 'Mini boss' : TAG_NAME[st.tag!];
  return h('span', { class: 'chip sk thin', style: `font-size:12px;padding:0 6px;--fill:${TAG_FILL[st.tag!]};white-space:nowrap;align-self:flex-start` }, text);
}

// ---------- đường mòn của đảo 70 ải ----------
// Đường cong qua các điểm ải của ảnh đảo (như rc.curve của bản đồ nét tay: Catmull-Rom, hai đầu lặp điểm), lấy mẫu dày để
// đo chiều dài. Mốc (ải tướng) cách nhau theo số ải xen giữa của chặng, chấm ải rải đều giữa hai mốc.
interface TrailPt { x: number; y: number; d: number }
function trailPolyline(z: ZoneDef, MW: number, MH: number): TrailPt[] {
  const P = z.nodes.map(([x, y]) => [x * MW, y * MH]);
  const Q = [P[0], ...P, P[P.length - 1]];
  const out: TrailPt[] = [{ x: P[0][0], y: P[0][1], d: 0 }];
  for (let i = 1; i + 2 < Q.length; i++) {
    const [p0, p1, p2, p3] = [Q[i - 1], Q[i], Q[i + 1], Q[i + 2]];
    const b1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const b2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    for (let k = 1; k <= 24; k++) {
      const t = k / 24, u = 1 - t;
      const x = u * u * u * p1[0] + 3 * u * u * t * b1[0] + 3 * u * t * t * b2[0] + t * t * t * p2[0];
      const y = u * u * u * p1[1] + 3 * u * u * t * b1[1] + 3 * u * t * t * b2[1] + t * t * t * p2[1];
      const last = out[out.length - 1];
      out.push({ x, y, d: last.d + Math.hypot(x - last.x, y - last.y) });
    }
  }
  return out;
}
function pointAt(poly: TrailPt[], d: number): TrailPt {
  let i = 1;
  while (i < poly.length - 1 && poly[i].d < d) i++;
  const a = poly[i - 1], b = poly[i], t = b.d > a.d ? Math.min(1, Math.max(0, (d - a.d) / (b.d - a.d))) : 0;
  return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t, d };
}
// vị trí từng ải (theo idx - 1) trên đường; mỗi chặng chiếm phần đường tỉ lệ với (số chấm + 3)
function trailLayout(z: ZoneDef, stages: StageDef[], MW: number, MH: number) {
  const poly = trailPolyline(z, MW, MH);
  const len = poly[poly.length - 1].d;
  const heads = stages.filter((st) => st.tag === 'hero');
  const gaps = heads.slice(0, -1).map((st, c) => heads[c + 1].idx - st.idx - 1 + 3);
  const total = gaps.reduce((a, b) => a + b, 0);
  const D = [0];
  gaps.forEach((g) => D.push(D[D.length - 1] + (len * g) / total));
  const at: TrailPt[] = [];
  heads.forEach((st, c) => {
    at[st.idx - 1] = pointAt(poly, D[c]);
    if (c + 1 >= heads.length) return;
    const n = heads[c + 1].idx - st.idx - 1;
    const a = D[c] + nodeSize(st) / 2 + 10, b = D[c + 1] - nodeSize(heads[c + 1]) / 2 - 10;
    for (let j = 1; j <= n; j++) at[st.idx - 1 + j] = pointAt(poly, a + ((b - a) * (j - 0.5)) / n);
  });
  return { poly, at };
}

export function zoneScreen(): Screen {
  const bg = h('div', { class: 'fill' });
  const pathLayer = h('div', { class: 'fill', style: 'pointer-events:none' });
  const nodes = h('div', { class: 'fill' });
  const map = h('div', { style: 'position:absolute' }, bg, pathLayer, nodes);
  const holder = h('div', { style: 'position:relative' }, map);
  const scroller = h('div', { class: 'scroll', style: 'position:absolute;inset:0;overflow-y:auto;overflow-x:hidden' }, holder);
  const info = h('div', { class: 'zinfo sk' });
  const bottom = h('div', { class: 'zbottom sk' });
  const el = h('div', { class: 'screen' }, scroller, info, bottom);
  let zone: Elem = 'thuy';
  let loadedFor = '';

  async function loadBg() {
    const z = ZONE[zone];
    if (loadedFor === zone) return;
    loadedFor = zone;
    bg.replaceChildren();
    await preloadIcons();
    scroller.style.background = z.sea;
    const node = await sceneBackdrop(z.art, () => drawZoneFallback(z, app.scale * dims(zone).mk * (window.devicePixelRatio || 1)));
    if (loadedFor === zone) bg.replaceChildren(node);
  }

  function render() {
    const { MW, MH } = dims(zone);
    map.style.cssText = `position:absolute;left:${(SW - MW) / 2}px;top:${PAD_T}px;width:${MW}px;height:${MH}px`;
    holder.style.height = `${PAD_T + MH + PAD_B}px`;
    if (isV2(zone)) renderTrail(MW, MH);
    else renderNodes(MW, MH);
    renderInfo();
  }

  // đảo 70 ải: mốc ải tướng, chấm ải xen giữa, đường đã đi tới ải đang đánh
  function renderTrail(MW: number, MH: number) {
    const z = ZONE[zone];
    const s = app.save;
    const stages = zoneStages(zone);
    const prog = s.zones[zone];
    const { poly, at } = trailLayout(z, stages, MW, MH);
    const cur = Math.min(prog, stages.length - 1); // vị trí (idx - 1) của ải đang đánh, hoặc ải cuối khi đã xong
    const end = at[cur];
    let d = '';
    for (const p of poly) {
      if (p.d >= end.d) break;
      d += `${d ? 'L' : 'M'}${p.x.toFixed(1)},${p.y.toFixed(1)}`;
    }
    pathLayer.innerHTML = prog && d ? pathSvg(`${d}L${end.x.toFixed(1)},${end.y.toFixed(1)}`, MW, MH) : '';
    clear(nodes);
    const leader = s.team.find((t) => s.heroes[t]?.owned) ?? STARTERS[0];
    stages.forEach((st, i) => {
      const { x, y } = at[i];
      const cleared = stageCleared(s, st), open = stageOpen(s, st), current = open && !cleared;
      const tap = () => {
        sfx.click();
        openChapter(st.chapter ?? 0);
      };
      if (st.tag === 'hero') {
        const size = nodeSize(st);
        const fill = !open ? '#d9d2c2' : cleared ? '#c9eab8' : st.kind === 'boss' ? '#ffb3a3' : st.kind === 'mini' ? '#ffd9a0' : '#fff3c4';
        nodes.append(h(
          'div',
          { class: `znode sk ${open ? '' : 'locked'} ${current ? 'pulse' : ''}`, style: `left:${x - size / 2}px;top:${y - size / 2}px;width:${size}px;height:${size}px;--fill:${fill}`, title: st.name, onclick: tap },
          st.kind !== 'normal' ? h('span', { html: icon(st.kind === 'boss' ? 'boss' : 'crownSm', st.kind === 'boss' ? 42 : 32) }) : null,
          h('div', { class: 'num', style: `font-size:${st.kind === 'normal' ? 22 : 15}px` }, String(st.idx)),
        ));
        const lead = stageLead(st);
        const lh = st.kind === 'boss' ? 78 : st.kind === 'mini' ? 64 : 52;
        nodes.append(h('div', {
          style: `position:absolute;left:${x}px;top:${y - size / 2 + 12}px;transform:translateX(-50%) translateY(-100%);pointer-events:none;z-index:2;${open ? '' : 'filter:grayscale(.7);opacity:.75'}`,
        }, heroImg(lead.hero, lh, false, enemyFormStar(lead))));
        if (cleared) nodes.append(h('div', { style: `position:absolute;left:${x + size / 2 - 20}px;top:${y - size / 2 - 10}px;pointer-events:none;z-index:3`, html: icon('check', 28) }));
      } else {
        const size = current ? 18 : 12;
        const fill = cleared ? '#ffe08a' : current ? '#ff8a6a' : '#d9d2c2';
        nodes.append(h('div', {
          class: current ? 'pulse' : '',
          style: `position:absolute;left:${x - size / 2}px;top:${y - size / 2}px;width:${size}px;height:${size}px;border-radius:50%;background:${fill};border:2.5px solid #2b2118;cursor:pointer;z-index:1`,
          title: `Ải ${st.idx}`,
          onclick: tap,
        }));
      }
      if (current) {
        const side = x > MW / 2 ? -1 : 1;
        const off = st.tag === 'hero' ? nodeSize(st) / 2 + 50 : 46;
        nodes.append(h('div', { class: 'bob', style: `position:absolute;left:${x + side * off - 36}px;top:${y - 92}px;pointer-events:none;z-index:3` }, heroImg(leader, 80)));
      }
    });
    requestAnimationFrame(() => (scroller.scrollTop = Math.max(0, PAD_T + end.y - 480)));
  }

  // đảo 8 ải: mỗi ải một nút tại điểm ải của ảnh đảo
  function renderNodes(MW: number, MH: number) {
    const z = ZONE[zone];
    const s = app.save;
    const stages = zoneStages(zone);
    const prog = s.zones[zone];
    // đường đã đi: nét đỏ đứt qua các ải đã qua
    const P = z.nodes.map(([x, y]) => [x * MW, y * MH]);
    let d = '';
    for (let i = 0; i <= Math.min(prog, 7); i++) d += `${i ? 'L' : 'M'}${P[i][0]},${P[i][1]}`;
    pathLayer.innerHTML = prog ? pathSvg(d, MW, MH) : '';
    // ải
    clear(nodes);
    const leader = s.team.find((t) => s.heroes[t]?.owned) ?? STARTERS[0];
    stages.forEach((st, i) => {
      const [x, y] = P[i];
      const cleared = stageCleared(s, st), open = stageOpen(s, st), current = open && !cleared;
      const size = st.kind === 'boss' ? 86 : st.kind === 'mini' ? 72 : 58;
      const fill = !open ? '#d9d2c2' : cleared ? '#c9eab8' : st.kind === 'boss' ? '#ffb3a3' : st.kind === 'mini' ? '#ffd9a0' : '#fff3c4';
      const node = h(
        'div',
        {
          class: `znode sk ${open ? '' : 'locked'} ${current ? 'pulse' : ''}`,
          style: `left:${x - size / 2}px;top:${y - size / 2}px;width:${size}px;height:${size}px;--fill:${fill}`,
          title: st.name,
          onclick: () => {
            if (!open) {
              sfx.error();
              app.toast(`Qua ải ${st.idx - 1} của ${z.name} trước đã`, 'lock');
              return;
            }
            sfx.click();
            openPrep(st.id);
          },
        },
        st.kind !== 'normal' ? h('span', { html: icon(st.kind === 'boss' ? 'boss' : 'crownSm', st.kind === 'boss' ? 42 : 32) }) : null,
        h('div', { class: 'num', style: `font-size:${st.kind === 'normal' ? 24 : 15}px` }, open ? String(st.idx) : ''),
        !open ? h('span', { html: icon('lock', 26) }) : null,
      );
      nodes.append(node);
      // tướng chính của ải đứng trên nút, chân khuất sau mép nút (boss tiến hóa hiện dạng 1); ải chưa mở thì mờ
      const lead = stageLead(st);
      const lh = st.kind === 'boss' ? 78 : st.kind === 'mini' ? 64 : 52;
      nodes.append(h('div', {
        style: `position:absolute;left:${x}px;top:${y - size / 2 + 12}px;transform:translateX(-50%) translateY(-100%);pointer-events:none;z-index:2;${open ? '' : 'filter:grayscale(.7);opacity:.75'}`,
      }, heroImg(lead.hero, lh, false, enemyFormStar(lead))));
      if (cleared) nodes.append(h('div', { style: `position:absolute;left:${x + size / 2 - 20}px;top:${y - size / 2 - 10}px;pointer-events:none;z-index:3`, html: icon('check', 28) }));
      if (current) {
        const side = x > MW / 2 ? -1 : 1;
        nodes.append(h('div', { class: 'bob', style: `position:absolute;left:${x + side * (size / 2 + 50) - 36}px;top:${y - 92}px;pointer-events:none;z-index:3` }, heroImg(leader, 80)));
      }
    });
    // cuộn tới ải đang đánh
    const cur = Math.min(7, prog);
    requestAnimationFrame(() => (scroller.scrollTop = Math.max(0, PAD_T + P[cur][1] - 480)));
  }

  // thông tin đảo, rương mốc, ải tiếp theo
  function renderInfo() {
    const z = ZONE[zone];
    const s = app.save;
    const prog = s.zones[zone], size = zoneSize(zone), chests = ZONE_CHESTS[zone];
    clear(info);
    const df = difficulty(z, s.level, prog >= size);
    const ready = zoneChestReady(s, zone);
    const bar = h('div', { class: 'zprog', style: `--zc:${ELEM_COLOR[zone]};margin:10px 22px 4px 4px` }, h('i', { style: `width:${(prog / size) * 100}%` }));
    chests.forEach((at, n) => {
      const got = s.zoneChests[zone] > n;
      const can = ready === n;
      const big = n === chests.length - 1;
      bar.append(
        h('div', {
          class: `mk ${can ? 'wob' : ''}`,
          style: `left:${(at / size) * 100}%;--chest:${big ? '#f7c948' : '#c9d3dc'};${got ? 'opacity:.45;filter:grayscale(1)' : ''}`,
          title: got ? 'Đã nhận' : `Qua ${at} ải để mở`,
          html: icon('chest', chests.length > 2 ? (big ? 36 : 28) : 40),
          onclick: () => claim(n),
        }),
      );
    });
    info.append(
      h(
        'div',
        { class: 'row gap6' },
        elemTag(zone),
        h('span', { class: 'title', style: 'font-size:15px' }, `Cấp đề nghị ${z.level[0]}–${z.level[1]}`),
        h('span', { class: `diff ${df.cls}` }, df.text),
        h('div', { class: 'grow' }),
        h('span', { class: 'small muted' }, `${prog}/${size} ải`),
      ),
      bar,
      h('div', { class: 'small', style: 'line-height:1.15' }, `${z.sub}. Địch hệ ${ELEM_NAME[zone]}: dùng tướng hệ ${ELEM_NAME[counterOf(zone)]} để khắc.`),
    );
    // ải tiếp theo
    clear(bottom);
    const next = nextStage(s, zone);
    if (next) {
      const gift = next.drops.find((x) => x.gift);
      const shards = [...new Set(next.drops.filter((x) => !x.gift).map((x) => HERO[x.hero].name))];
      bottom.append(
        h(
          'div',
          { class: 'col grow', style: 'gap:3px;min-width:0' },
          h('div', { class: 'row gap6', style: 'min-width:0' },
            h('div', { class: 'title', style: 'font-size:19px;line-height:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis' }, `Ải ${next.idx}/${size} · ${next.name}`),
            next.tag ? tagChip(next) : null),
          h('div', { class: 'row gap4' }, ...next.enemies.map((e) => h('div', { class: 'col center', style: 'width:52px' }, heroImg(e.hero, e.boss ? 48 : 40, false, enemyFormStar(e)), h('span', { class: 'small title', style: 'font-size:11px;white-space:nowrap' }, enemyLabel(e))))),
          h('div', { class: 'small' }, `+${stageBalls(next, true)} bi${gift ? ` · ${HERO[gift.hero].name} gia nhập đội!` : shards.length ? ` · rơi mảnh ${shards.join(', ')}` : ''}`),
        ),
        h('button', { class: 'btn red big', onclick: () => { sfx.click(); openPrep(next.id); } }, 'Đánh!'),
      );
    } else {
      bottom.append(
        h('span', { html: icon('crownSm', 48) }),
        h('div', { class: 'col grow' }, h('div', { class: 'title', style: 'font-size:19px' }, `Đã chinh phục ${z.name}!`), h('div', { class: 'small' }, 'Đánh lại ải bất kỳ để kiếm thêm bi và mảnh tướng; boss rơi mảnh khi AFK.')),
      );
    }
  }

  // bảng chặng (đảo 70 ải): các ải từ ải tướng tới trước ải tướng sau; chạm ải đã mở thì vào chuẩn bị trận
  function openChapter(ch: number) {
    const s = app.save;
    const list = zoneStages(zone).filter((st) => st.chapter === ch);
    const head = list[0];
    const body = h('div', { class: 'col gap6' });
    const m = app.modal(body, { width: 510 });
    body.append(
      h('h2', null, head.name),
      h('div', { class: 'small', style: 'margin-top:-6px' }, `Ải ${head.idx}–${list[list.length - 1].idx} · ra mắt ${HERO[head.enemies[0].hero].name}`),
    );
    const rows = h('div', { class: 'col gap4', style: 'max-height:600px;overflow-y:auto;padding:2px' });
    for (const st of list) {
      const cleared = stageCleared(s, st), open = stageOpen(s, st), current = open && !cleared;
      rows.append(h(
        'div',
        {
          class: `sk thin row gap6 ${current ? 'pulse' : ''}`,
          style: `padding:4px 8px;align-items:center;cursor:pointer;--fill:${!open ? '#e2dccd' : cleared ? '#eaf6df' : '#fff3c4'};${open ? '' : 'opacity:.8'}`,
          onclick: () => {
            if (!open) {
              sfx.error();
              app.toast(`Qua ải ${st.idx - 1} trước đã`, 'lock');
              return;
            }
            sfx.click();
            m.close();
            openPrep(st.id);
          },
        },
        h('div', { class: 'title', style: 'font-size:22px;width:34px;text-align:center' }, String(st.idx)),
        h('div', { class: 'col', style: 'width:104px;gap:1px' }, tagChip(st), h('div', { class: 'small muted', style: 'font-size:11px' }, `+${stageBalls(st, !cleared)} bi`)),
        h('div', { class: 'row gap4 grow', style: `${open ? '' : 'filter:grayscale(.7)'}` }, ...st.enemies.map((e) => h('div', { class: 'col center', style: 'width:50px' }, heroImg(e.hero, e.boss ? 44 : 38, false, enemyFormStar(e)), h('span', { class: 'small title', style: 'font-size:10px;white-space:nowrap' }, enemyLabel(e))))),
        h('span', { html: icon(cleared ? 'check' : open ? 'play' : 'lock', 26) }),
      ));
    }
    body.append(rows, h('div', { class: 'center' }, h('button', { class: 'btn paper', onclick: () => m.close() }, 'Đóng')));
    requestAnimationFrame(() => {
      const i = list.findIndex((st) => stageOpen(s, st) && !stageCleared(s, st));
      if (i > 3) rows.scrollTop = (rows.children[i] as HTMLElement).offsetTop - 120;
    });
  }

  function claim(n: number) {
    const s = app.save;
    if (zoneChestReady(s, zone) !== n) {
      sfx.error();
      app.toast(s.zoneChests[zone] > n ? 'Đã nhận rương này' : `Qua ${ZONE_CHESTS[zone][n]} ải của đảo để mở`, 'chest');
      return;
    }
    const r = claimZoneChest(s, zone, new Rng(randomSeed()));
    if (!r) return;
    app.persist();
    sfx.chest();
    const list = h('div', { class: 'row gap8', style: 'flex-wrap:wrap;justify-content:center' });
    list.append(h('div', { class: 'chip sk thin pop', style: 'font-size:22px' }, h('span', { html: icon('ball', 34) }), `+${r.balls} bi`));
    for (const c of r.cards) list.append(h('div', { class: 'col center pop' }, cardEl(c.card, s.heroes[c.hero].cards[c.slot].lv, { mini: true }), h('div', { class: 'small title' }, HERO[c.hero].name)));
    const m = app.modal(
      h('div', { class: 'col center gap12', style: 'text-align:center' }, h('h2', null, r.big ? 'Rương chinh phục!' : ZONE_CHESTS[zone].length > 2 ? `Rương ải ${ZONE_CHESTS[zone][n]}` : 'Rương nửa đảo'), h('div', { class: 'pop', style: `--chest:${r.big ? '#f7c948' : '#c9d3dc'}`, html: icon('chest', 110) }), list, h('button', { class: 'btn green', onclick: () => m.close() }, 'Nhận')),
      { width: 470 },
    );
    render();
  }

  return {
    el,
    top: 'back',
    title: 'Đảo',
    back: () => app.go('world'),
    enter(params) {
      const p = (params ?? {}) as { zone?: Elem; prep?: number };
      if (p.zone) zone = p.zone;
      app.setTitle(ZONE[zone].name);
      void loadBg();
      render();
      if (p.prep) setTimeout(() => openPrep(p.prep!), 250);
    },
  };
}

// ---------- chuẩn bị trận: xem địch, thưởng, chọn đội ----------
export function openPrep(id: number) {
  const st: StageDef = STAGE[id];
  const s = app.save;
  const slotsOpen = teamSlots(s);
  const team = s.team.filter((t) => s.heroes[t]?.owned).slice(0, slotsOpen);
  const body = h('div', { class: 'col gap8' });
  const m = app.modal(body, { width: 500 });
  const lead = HERO[st.enemies.find((e) => e.boss)?.hero ?? st.enemies[0].hero];
  const maxLv = Math.max(...st.enemies.map((e) => e.level));

  function draw() {
    clear(body);
    body.append(
      h(
        'div',
        { class: 'row gap8' },
        h('h2', null, `${ZONE[st.zone].name} · Ải ${st.idx}`),
        st.kind !== 'normal' ? h('span', { class: 'diff wall', style: 'font-size:13px' }, st.kind === 'boss' ? 'BOSS ĐẢO' : 'MINI BOSS') : st.tag ? tagChip(st) : null,
      ),
      h('div', { class: 'title', style: 'font-size:20px;margin-top:-6px' }, st.name),
    );
    // ải 1 của đảo 70 ải: đấu với bóng của tướng khởi đầu
    if (st.tag === 'hero' && STARTERS.includes(st.enemies[0].hero))
      body.append(h('div', { class: 'small', style: 'margin-top:-4px' }, `Mặt nước in bóng ${HERO[st.enemies[0].hero].name} của bạn. Thắng chính mình trước đã!`));
    if (s.level < maxLv - 2)
      body.append(h('div', { class: 'sk thin', style: '--fill:#ffd2c8;padding:6px 10px;font-size:15px' }, `Cảnh báo: địch cấp ${maxLv}, bạn mới cấp ${s.level}. Đảo này đang quá mạnh, nên nuôi tướng thêm.`));
    const foes = h('div', { class: 'row gap8 sk thin', style: 'padding:8px;--fill:#fff2ec;justify-content:center;flex-wrap:wrap' });
    for (const e of st.enemies) {
      const hero = HERO[e.hero];
      const evo = e.evo && hero.forms.length > 1;
      foes.append(
        h(
          'div',
          { class: 'col center', style: 'width:120px' },
          heroImg(e.hero, e.boss ? 84 : 66, false, enemyFormStar(e)),
          h('div', { class: 'title', style: 'font-size:15px;text-align:center;line-height:1' }, evo ? hero.forms[0].name : hero.name),
          h('div', { class: 'row gap4' }, elemTag(hero.elem), h('span', { class: 'title', style: 'font-size:13px' }, `Lv${e.level}`)),
          e.boss ? h('div', { class: 'small', style: 'color:var(--red);font-weight:bold' }, evo ? `Boss tiến hóa ${hero.forms.length} dạng` : `Boss: máu ×${String(Math.round(CFG.bossHp * (e.evo ? CFG.bossEvoHp : 1) * 10) / 10).replace('.', ',')}`) : null,
          e.buff ? h('div', { class: 'small', style: `font-weight:bold;color:${e.buff > 0 ? 'var(--red)' : 'var(--green, #3a8a3a)'}` }, e.buff > 0 ? `Cường hóa +${Math.round(e.buff * 100)}%` : `Yếu hơn ${Math.round(-e.buff * 100)}%`) : null,
          isMinion(e.hero) ? h('div', { class: 'small muted', style: 'text-align:center;line-height:1.1' }, 'Lính, không thu phục') : null,
        ),
      );
      // boss tiến hóa: cả dòng dạng (dạng sau to hơn) và thẻ Tiến Hóa
      if (evo) {
        const line = h('div', { class: 'row gap4', style: 'align-items:flex-end' });
        hero.forms.forEach((fm, i) => {
          if (i) line.append(h('span', { class: 'title', style: 'font-size:20px;padding-bottom:18px' }, '›'));
          line.append(h('div', { class: 'col center', style: 'width:76px' }, heroImg(e.hero, 46 + i * 10, false, i ? FORM_STARS[i - 1] : 1), h('div', { class: 'small title', style: 'font-size:11px;text-align:center;line-height:1' }, fm.name)));
        });
        foes.append(h('div', { class: 'col center gap4', style: 'width:100%' }, line, h('div', { class: 'small', style: 'text-align:center;line-height:1.2' }, h('b', null, `${BOSS_EVO.name}: `), cardText(BOSS_EVO))));
      }
    }
    body.append(h('div', { class: 'title', style: 'font-size:15px' }, 'Đối thủ'), foes);
    const first = !stageCleared(s, st);
    const rw = h('div', { class: 'row gap8', style: 'flex-wrap:wrap' }, h('span', { class: 'chip sk thin' }, h('span', { html: icon('ball', 26) }), `+${stageBalls(st, first)} bi${first ? ' (lần đầu)' : ''}`));
    for (const dr of st.drops) {
      if (dr.gift) {
        if (first) rw.append(h('span', { class: 'chip sk thin', style: '--fill:#fff3c4' }, heroImg(dr.hero, 30), `${HERO[dr.hero].name} gia nhập!`));
        continue;
      }
      const ch = first ? dr.chance : dr.chance * (dr.chance >= 1 ? 0.5 : 0.8);
      rw.append(h('span', { class: 'chip sk thin', title: s.heroes[dr.hero].owned ? 'Đã có tướng: mảnh đổi thành bản sao thẻ' : '' }, heroImg(dr.hero, 30), `${dr.min}–${dr.max} mảnh · ${Math.round(ch * 100)}%`));
    }
    body.append(h('div', { class: 'title', style: 'font-size:15px' }, 'Phần thưởng'), rw);
    const slots = h('div', { class: 'row gap8', style: 'justify-content:center' });
    for (let i = 0; i < 3; i++) {
      const id2 = team[i];
      if (i >= slotsOpen) {
        slots.append(h('div', { class: 'sk center', style: 'width:112px;height:100px;--fill:#e2dccd;flex-direction:column;--shadow:none', html: icon('lock', 28) }, h('div', { class: 'small muted' }, `Xong ${TEAM_SLOT_ZONES[i]} đảo`)));
        continue;
      }
      slots.append(
        h(
          'div',
          { class: 'sk center', style: `width:112px;height:100px;--fill:${id2 ? '#eaf6df' : '#f6efdc'};flex-direction:column;cursor:pointer;${id2 ? '' : '--shadow:none'}`, onclick: () => { if (id2) { team.splice(i, 1); sfx.click(); draw(); } } },
          id2 ? heroImg(id2, 64) : h('div', { class: 'muted title', style: 'font-size:14px' }, 'Trống'),
          id2 ? h('div', { class: 'title', style: 'font-size:13px' }, `${i === 0 ? 'Ra trước · ' : ''}${HERO[id2].name}`) : null,
        ),
      );
    }
    body.append(h('div', { class: 'row', style: 'justify-content:space-between' }, h('div', { class: 'title', style: 'font-size:15px' }, `Đội của bạn (${slotsOpen}/3 ô, tướng đầu ra trước)`), h('span', { class: 'small muted' }, 'chạm để bỏ')), slots);
    const roster = h('div', { class: 'row gap6', style: 'flex-wrap:wrap;justify-content:center' });
    for (const hero of HEROES) {
      const p = s.heroes[hero.id];
      if (!p.owned) continue;
      const inTeam = team.includes(hero.id);
      const adv = elemMult(hero.elem, lead.elem), bad = elemMult(lead.elem, hero.elem);
      roster.append(
        h(
          'div',
          {
            class: 'sk thin center',
            style: `width:68px;height:80px;flex-direction:column;cursor:pointer;--fill:${inTeam ? '#ffe9a0' : '#fff'};position:relative`,
            onclick: () => {
              sfx.click();
              if (inTeam) team.splice(team.indexOf(hero.id), 1);
              else if (team.length < slotsOpen) team.push(hero.id);
              else app.toast(slotsOpen < 3 ? `Đang mở ${slotsOpen} ô đội: xong thêm đảo để mở ô mới` : 'Đội tối đa 3 tướng', 'team');
              draw();
            },
          },
          heroImg(hero.id, 52),
          h('div', { class: 'title', style: 'font-size:10px;line-height:1;text-align:center;max-width:64px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis' }, hero.name),
          adv > 1 ? h('div', { style: 'position:absolute;top:-8px;right:-6px', html: icon('up', 24) }) : bad > 1 ? h('div', { style: 'position:absolute;top:-8px;right:-6px', html: icon('down', 24) }) : null,
        ),
      );
    }
    body.append(roster);
    body.append(h('div', { class: 'small muted', style: 'text-align:center' }, `Mũi tên xanh: khắc ${ELEM_NAME[lead.elem]} của ${lead.name}. Mũi tên đỏ: bị khắc.`));
    void stars;
    body.append(
      h(
        'div',
        { class: 'center' },
        h(
          'button',
          {
            class: `btn red big ${team.length ? '' : 'off'}`,
            onclick: () => {
              if (!team.length) return;
              sfx.click();
              s.team = [...team];
              app.persist();
              m.close();
              app.go('battle', { stageId: id, team: [...team] });
            },
          },
          'Xuất trận!',
        ),
      ),
    );
  }
  draw();
}
