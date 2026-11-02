// Scene đảo một hệ: ảnh đảo to, 8 ải dọc đường mòn từ bãi dưới lên hang boss, thanh tiến độ có 2 rương mốc,
// khung "ải tiếp theo" ở dưới. Trong một đảo, ải mở lần lượt.
import { HERO, HEROES, STARTERS } from '../../core/data/heroes';
import { STAGE, ZONE, zoneStages, type StageDef } from '../../core/data/stages';
import { ELEM_COLOR, ELEM_NAME, elemMult, BEATS } from '../../core/elements';
import {
  claimZoneChest, nextStage, stageBalls, stageCleared, stageOpen, ZONE_CHEST_AT, zoneChestReady,
} from '../../core/progression';
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

// bản đồ đảo phóng to và cuộn dọc, để ải ở hai đầu không bị khung trên dưới che
const MK = 1.27, MW = Math.round(SW * MK), MH = Math.round(SH * MK), PAD_T = 110, PAD_B = 150;

export function zoneScreen(): Screen {
  const bg = h('div', { class: 'fill' });
  const pathLayer = h('div', { class: 'fill', style: 'pointer-events:none' });
  const nodes = h('div', { class: 'fill' });
  const map = h('div', { style: `position:absolute;left:${(SW - MW) / 2}px;top:${PAD_T}px;width:${MW}px;height:${MH}px` }, bg, pathLayer, nodes);
  const scroller = h('div', { class: 'scroll', style: 'position:absolute;inset:0;overflow-y:auto;overflow-x:hidden' }, h('div', { style: `position:relative;height:${PAD_T + MH + PAD_B}px` }, map));
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
    const node = await sceneBackdrop(z.art, () => drawZoneFallback(z, app.scale * MK * (window.devicePixelRatio || 1)));
    if (loadedFor === zone) bg.replaceChildren(node);
  }

  function render() {
    const z = ZONE[zone];
    const s = app.save;
    const stages = zoneStages(zone);
    const prog = s.zones[zone];
    // đường đã đi: nét đỏ đứt qua các ải đã qua
    const P = z.nodes.map(([x, y]) => [x * MW, y * MH]);
    let d = '';
    for (let i = 0; i <= Math.min(prog, 7); i++) d += `${i ? 'L' : 'M'}${P[i][0]},${P[i][1]}`;
    pathLayer.innerHTML = prog
      ? `<svg width="${MW}" height="${MH}" class="boil-self"><path d="${d}" fill="none" stroke="#2b2118" stroke-width="9" stroke-linecap="round" stroke-dasharray="14 12" opacity=".5"/><path d="${d}" fill="none" stroke="#ffe08a" stroke-width="5" stroke-linecap="round" stroke-dasharray="14 12"/></svg>`
      : '';
    // ải
    clear(nodes);
    const lead = s.team.find((t) => s.heroes[t]?.owned) ?? STARTERS[0];
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
      if (cleared) nodes.append(h('div', { style: `position:absolute;left:${x + size / 2 - 20}px;top:${y - size / 2 - 10}px;pointer-events:none;z-index:3`, html: icon('check', 28) }));
      if (current) {
        const side = x > MW / 2 ? -1 : 1;
        nodes.append(h('div', { class: 'bob', style: `position:absolute;left:${x + side * 56 - 36}px;top:${y - 92}px;pointer-events:none;z-index:3` }, heroImg(lead, 80)));
      }
    });
    // cuộn tới ải đang đánh
    const cur = Math.min(7, prog);
    requestAnimationFrame(() => (scroller.scrollTop = Math.max(0, PAD_T + P[cur][1] - 480)));
    // thông tin đảo + rương mốc
    clear(info);
    const df = difficulty(z, s.level, prog >= 8);
    const ready = zoneChestReady(s, zone);
    const bar = h('div', { class: 'zprog', style: `--zc:${ELEM_COLOR[zone]};margin:10px 22px 4px 4px` }, h('i', { style: `width:${(prog / 8) * 100}%` }));
    ZONE_CHEST_AT.forEach((at, n) => {
      const got = s.zoneChests[zone] > n;
      const can = ready === n;
      bar.append(
        h('div', {
          class: `mk ${can ? 'wob' : ''}`,
          style: `left:${(at / 8) * 100}%;--chest:${n ? '#f7c948' : '#c9d3dc'};${got ? 'opacity:.45;filter:grayscale(1)' : ''}`,
          title: got ? 'Đã nhận' : `Qua ${at} ải để mở`,
          html: icon('chest', 40),
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
        h('span', { class: 'small muted' }, `${prog}/8 ải`),
      ),
      bar,
      h('div', { class: 'small', style: 'line-height:1.15' }, `${z.sub}. Địch hệ ${ELEM_NAME[zone]}: dùng tướng hệ ${ELEM_NAME[counterOf(zone)]} để khắc.`),
    );
    // ải tiếp theo
    clear(bottom);
    const next = nextStage(s, zone);
    if (next) {
      const gift = next.drops.find((x) => x.gift);
      bottom.append(
        h(
          'div',
          { class: 'col grow', style: 'gap:3px;min-width:0' },
          h('div', { class: 'title', style: 'font-size:19px;line-height:1' }, `Ải ${next.idx}/8 · ${next.name}`),
          h('div', { class: 'row gap4' }, ...next.enemies.map((e) => h('div', { class: 'col center', style: 'width:52px' }, heroImg(e.hero, e.boss ? 48 : 40), h('span', { class: 'small title', style: 'font-size:11px' }, `Lv${e.level}${e.boss ? ' BOSS' : ''}`)))),
          h('div', { class: 'small' }, `+${stageBalls(next, true)} bi${gift ? ` · ${HERO[gift.hero].name} gia nhập đội!` : next.drops.length ? ` · rơi mảnh ${next.drops.map((x) => HERO[x.hero].name).join(', ')}` : ''}`),
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

  function claim(n: number) {
    const s = app.save;
    if (zoneChestReady(s, zone) !== n) {
      sfx.error();
      app.toast(s.zoneChests[zone] > n ? 'Đã nhận rương này' : `Qua ${ZONE_CHEST_AT[n]} ải của đảo để mở`, 'chest');
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
      h('div', { class: 'col center gap12', style: 'text-align:center' }, h('h2', null, r.big ? 'Rương chinh phục!' : 'Rương nửa đảo'), h('div', { class: 'pop', style: `--chest:${r.big ? '#f7c948' : '#c9d3dc'}`, html: icon('chest', 110) }), list, h('button', { class: 'btn green', onclick: () => m.close() }, 'Nhận')),
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
  const team = s.team.filter((t) => s.heroes[t]?.owned).slice(0, 3);
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
        st.kind !== 'normal' ? h('span', { class: 'diff wall', style: 'font-size:13px' }, st.kind === 'boss' ? 'BOSS ĐẢO' : 'MINI BOSS') : null,
      ),
      h('div', { class: 'title', style: 'font-size:20px;margin-top:-6px' }, st.name),
    );
    if (s.level < maxLv - 2)
      body.append(h('div', { class: 'sk thin', style: '--fill:#ffd2c8;padding:6px 10px;font-size:15px' }, `Cảnh báo: địch cấp ${maxLv}, bạn mới cấp ${s.level}. Đảo này đang quá mạnh, nên nuôi tướng thêm.`));
    const foes = h('div', { class: 'row gap8 sk thin', style: 'padding:8px;--fill:#fff2ec;justify-content:center;flex-wrap:wrap' });
    for (const e of st.enemies) {
      const hero = HERO[e.hero];
      foes.append(
        h(
          'div',
          { class: 'col center', style: 'width:120px' },
          heroImg(e.hero, e.boss ? 84 : 66),
          h('div', { class: 'title', style: 'font-size:15px;text-align:center;line-height:1' }, hero.name),
          h('div', { class: 'row gap4' }, elemTag(hero.elem), h('span', { class: 'title', style: 'font-size:13px' }, `Lv${e.level}`)),
          e.boss ? h('div', { class: 'small', style: 'color:var(--red);font-weight:bold' }, 'Boss: máu ×1,8') : null,
        ),
      );
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
      slots.append(
        h(
          'div',
          { class: 'sk center', style: `width:112px;height:100px;--fill:${id2 ? '#eaf6df' : '#f6efdc'};flex-direction:column;cursor:pointer;${id2 ? '' : '--shadow:none'}`, onclick: () => { if (id2) { team.splice(i, 1); sfx.click(); draw(); } } },
          id2 ? heroImg(id2, 64) : h('div', { class: 'muted title', style: 'font-size:14px' }, 'Trống'),
          id2 ? h('div', { class: 'title', style: 'font-size:13px' }, `${i === 0 ? 'Ra trước · ' : ''}${HERO[id2].name}`) : null,
        ),
      );
    }
    body.append(h('div', { class: 'row', style: 'justify-content:space-between' }, h('div', { class: 'title', style: 'font-size:15px' }, 'Đội của bạn (tối đa 3, tướng đầu ra trước)'), h('span', { class: 'small muted' }, 'chạm để bỏ')), slots);
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
              else if (team.length < 3) team.push(hero.id);
              else app.toast('Đội tối đa 3 tướng', 'team');
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
