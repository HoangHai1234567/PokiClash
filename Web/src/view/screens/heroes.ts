// Tướng: lưới tướng (có và chưa có), chi tiết tướng với hoạt cảnh, chỉ số, 3 thẻ nội tại, nâng thẻ, tiến hóa sao.
import { heroStats } from '../../core/battle';
import { CARD } from '../../core/data/cards';
import { HERO, HEROES } from '../../core/data/heroes';
import { STAGES } from '../../core/data/stages';
import { ELEM_COLOR, RARITY_COLOR, RARITY_NAME } from '../../core/elements';
import { canEvolve, canUpCard, cardReq, cardSum, CARD_MAX, evolve, formOf, MAX_STAR, SLOTS, starNeed, upCard, type CardSlot } from '../../core/progression';
import { app, type Screen } from '../app';
import { AolaAnim, ATTACK, HIT, IDLE, SKILL, Sticker } from '../aola';
import { clear, h } from '../dom';
import { icon } from '../icons';
import { sfx } from '../sfx';
import { cardEl, elemTag, heroImg, stars } from '../ui';

export function heroesScreen(): Screen {
  const grid = h('div', { class: 'row gap12', style: 'flex-wrap:wrap;justify-content:center;padding:6px 10px 110px' });
  const scroller = h('div', { class: 'scroll', style: 'position:absolute;left:0;right:0;top:84px;bottom:0;overflow-y:auto' }, grid);
  const el = h(
    'div',
    { class: 'screen' },
    scroller,
  );

  function render() {
    clear(grid);
    const s = app.save;
    const list = [...HEROES].sort((a, b) => Number(s.heroes[b.id].owned) - Number(s.heroes[a.id].owned));
    list.forEach((hero, i) => {
      const p = s.heroes[hero.id];
      const alert = p.owned && (canEvolve(s, hero.id) || SLOTS.some((k) => canUpCard(s, hero.id, k)));
      const card = h(
        'div',
        {
          class: 'sk center',
          style: `width:154px;height:206px;flex-direction:column;justify-content:flex-end;padding:8px 6px;cursor:pointer;--fill:${p.owned ? '#fffaf0' : '#efe6d2'};transform:rotate(${((i * 37) % 5) - 2}deg);position:relative`,
          onclick: () => {
            sfx.click();
            openHero(hero.id, render);
          },
        },
        h('div', { style: `position:absolute;left:3px;right:3px;top:3px;height:56px;background:${ELEM_COLOR[hero.elem]};opacity:.35;border-radius:12px 5px 0 0` }),
        h('div', { class: 'tape', style: 'top:-9px;left:46px' }),
        heroImg(hero.id, 112, !p.owned),
        h('div', { class: 'title', style: 'font-size:16px;line-height:1;text-align:center;margin-top:4px' }, hero.name),
        h('div', { class: 'row gap4' }, elemTag(hero.elem), h('span', { class: 'small', style: `font-weight:bold;color:${RARITY_COLOR[hero.rarity]}` }, RARITY_NAME[hero.rarity])),
        p.owned
          ? stars(p.star)
          : h('div', { class: 'bar', style: 'width:120px;height:14px;margin-top:3px' }, h('i', { style: `width:${(p.shards / hero.shards) * 100}%;--c:#7ee0d0` }), h('b', null, `${p.shards}/${hero.shards} mảnh`)),
        alert ? h('div', { class: 'badge', style: 'position:absolute;top:-8px;right:-6px;width:26px;height:26px;border-radius:50%;background:var(--red);border:2.5px solid var(--ink);color:#fff;font-family:"Baloo 2";font-weight:800;display:flex;align-items:center;justify-content:center', html: '!' }) : null,
        s.team.includes(hero.id) && p.owned ? h('div', { class: 'label-tag sk thin', style: 'position:absolute;top:8px;left:6px;font-size:11px;--fill:var(--green);color:#fff;-webkit-text-stroke:2.5px var(--ink);paint-order:stroke fill' }, 'TRONG ĐỘI') : null,
      );
      grid.append(card);
    });
  }

  return { el, top: 'back', title: 'Tướng', enter: render };
}

// ---------- chi tiết tướng ----------
export function openHero(id: string, onChange?: () => void) {
  const s = app.save;
  const hero = HERO[id];
  const body = h('div', { class: 'col gap8' });
  let anim: AolaAnim | null = null;
  let clip = IDLE, t = 0, raf = 0, last = 0;
  const cv = h('canvas', { style: 'width:220px;height:220px' }) as HTMLCanvasElement;
  const st = new Sticker();
  const m = app.modal(body, { width: 500, onClose: () => cancelAnimationFrame(raf) });
  void AolaAnim.load(formOf(hero, s.heroes[id].star).aola).then((a) => (anim = a)); // dạng theo sao

  const loop = (now: number) => {
    const dt = Math.min(0.05, (now - (last || now)) / 1000);
    last = now;
    t += dt;
    const g = cv.getContext('2d')!;
    const dpr = (window.devicePixelRatio || 1) * app.scale;
    const W = Math.round(220 * dpr);
    if (cv.width !== W) cv.width = cv.height = W;
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.clearRect(0, 0, W, W);
    if (anim) {
      const owned = s.heroes[id].owned;
      const c = anim.clip(clip);
      const fi = anim.frameAt(clip, t, clip === IDLE);
      if (clip !== IDLE && fi >= c.frames.length - 1) {
        clip = IDLE;
        t = 0;
      }
      // giữ cỡ dáng đứng cho mọi clip; vệt đòn bay xa thì bị cắt ở mép ô
      const fit = (W * (clip === IDLE ? 0.7 : 0.6)) / anim.idleH;
      st.render(anim, clip, fi, fit, false, true, !owned);
      g.drawImage(st.canvas, (clip === IDLE ? W / 2 : W * 0.32) - st.ox, W * (clip === IDLE ? 0.94 : 0.8) - st.oy);
      void c;
    }
    raf = requestAnimationFrame(loop);
  };
  raf = requestAnimationFrame(loop);

  function draw() {
    clear(body);
    const p = s.heroes[id];
    const stats = heroStats(hero, s.level, p.star);
    body.append(
      h(
        'div',
        { class: 'row gap8' },
        h(
          'div',
          { class: 'sk center', style: `width:226px;height:236px;--fill:${ELEM_COLOR[hero.elem]}33;flex-direction:column;flex:none` },
          cv,
          h(
            'div',
            { class: 'row gap4', style: 'margin-top:-4px' },
            ...([[IDLE, 'Đứng'], [ATTACK, 'Đánh'], [SKILL, 'Chiêu'], [HIT, 'Trúng']] as [string, string][]).map(([c, n]) =>
              h('button', { class: 'btn tiny paper', onclick: () => { clip = c; t = 0; sfx.click(); } }, n),
            ),
          ),
        ),
        h(
          'div',
          { class: 'col gap4', style: 'flex:1;min-width:0' },
          h('h2', null, hero.name),
          h('div', { class: 'muted', style: 'margin-top:-4px' }, hero.title),
          h('div', { class: 'row gap4' }, elemTag(hero.elem), h('span', { class: 'title', style: `font-size:14px;color:${RARITY_COLOR[hero.rarity]}` }, RARITY_NAME[hero.rarity])),
          p.owned ? stars(p.star) : null,
          h('div', { class: 'small muted' }, hero.line),
          h(
            'div',
            { class: 'sk thin col gap4', style: 'padding:8px 10px;--fill:#fff;margin-top:4px' },
            statRow('heart', 'Máu', stats.hp),
            statRow('sword', 'Công', stats.atk),
            statRow('shield', 'Thủ', stats.def),
            statRow('speed', 'Tốc', stats.spd),
            h('div', { class: 'small muted' }, `Ở cấp ${s.level}, sao ${p.star}`),
          ),
        ),
      ),
    );
    if (!p.owned) {
      const from = STAGES.filter((st) => st.drops.some((d) => d.hero === id)).map((st) => `ải ${st.id}`);
      body.append(
        h(
          'div',
          { class: 'sk thin col gap6', style: 'padding:10px;--fill:#f3fbf9' },
          h('div', { class: 'title', style: 'font-size:17px' }, `Chưa có: cần ${hero.shards} mảnh`),
          h('div', { class: 'bar', style: 'height:18px' }, h('i', { style: `width:${(p.shards / hero.shards) * 100}%;--c:#7ee0d0` }), h('b', null, `${p.shards}/${hero.shards}`)),
          h('div', { class: 'small' }, from.length ? `Mảnh rơi ở ${from.join(', ')}; ải boss đã qua còn rơi khi AFK, và đôi khi trong rương máy bi.` : hero.rarity === 'legend' ? 'Thả đủ 300 bi ở máy bi để nhận chắc chắn.' : 'Mảnh rơi trong rương máy bi.'),
        ),
      );
    }
    // 3 thẻ
    const row = h('div', { class: 'row gap8', style: 'justify-content:center;align-items:flex-start' });
    for (const slot of SLOTS) {
      const cid = slot === 'skill' ? hero.skill : slot === 'ult' ? hero.ult : hero.passive;
      const cp = p.cards[slot];
      const col = h('div', { class: 'col center gap4' });
      col.append(cardEl(cid, cp.lv, { mini: false }));
      (col.firstChild as HTMLElement).style.cssText += ';width:148px;height:224px;cursor:default';
      if (p.owned) {
        const req = cardReq(cp.lv);
        col.append(
          cp.lv >= CARD_MAX
            ? h('div', { class: 'small title' }, 'Cấp tối đa')
            : h('div', { class: 'bar', style: 'width:140px;height:15px' }, h('i', { style: `width:${Math.min(1, cp.copies / req) * 100}%;--c:var(--blue)` }), h('b', null, `${cp.copies}/${req} bản sao`)),
        );
        if (canUpCard(s, id, slot))
          col.append(h('button', { class: 'btn small green pulse', onclick: () => doUp(slot) }, `Lên cấp ${cp.lv + 1}`));
      }
      row.append(col);
    }
    body.append(h('div', { class: 'title', style: 'font-size:16px' }, 'Thẻ riêng của tướng'), row);
    // tiến hóa
    if (p.owned) {
      if (p.star < MAX_STAR) {
        const need = starNeed(p.star + 1);
        const ok = canEvolve(s, id);
        body.append(
          h(
            'div',
            { class: 'sk thin row gap8', style: 'padding:8px 12px;--fill:#fff8e0' },
            h('span', { html: icon('star', 40) }),
            h(
              'div',
              { class: 'col grow' },
              h('div', { class: 'title', style: 'font-size:17px' }, `Tiến hóa lên ${p.star + 1} sao: +8% mọi chỉ số`),
              h('div', { class: 'small' }, `Tổng cấp 3 thẻ ${cardSum(s, id)}/${need.cards} · Cấp người chơi ${s.level}/${need.level}`),
            ),
            h('button', { class: `btn orange ${ok ? 'pulse' : 'off'}`, onclick: () => doEvolve() }, 'Tiến hóa'),
          ),
        );
      } else body.append(h('div', { class: 'title center', style: 'font-size:16px' }, 'Đã tiến hóa tối đa'));
      const inTeam = s.team.includes(id);
      body.append(
        h(
          'div',
          { class: 'center' },
          h(
            'button',
            {
              class: `btn ${inTeam ? 'paper' : 'blue'}`,
              onclick: () => {
                sfx.click();
                if (inTeam) s.team = s.team.filter((x) => x !== id);
                else if (s.team.length >= 3) {
                  app.toast('Đội đã đủ 3 tướng: bỏ bớt một tướng trước', 'team');
                  return;
                } else s.team.push(id);
                app.persist();
                draw();
                onChange?.();
              },
            },
            inTeam ? 'Bỏ khỏi đội' : 'Cho vào đội',
          ),
        ),
      );
    }
  }

  function doUp(slot: CardSlot) {
    if (upCard(s, id, slot)) {
      sfx.level();
      app.toast(`${CARD[slot === 'skill' ? hero.skill : slot === 'ult' ? hero.ult : hero.passive].name} lên cấp!`, 'up');
      app.persist();
      draw();
      onChange?.();
    }
  }
  function doEvolve() {
    if (evolve(s, id)) {
      sfx.level();
      clip = SKILL;
      t = 0;
      app.toast(`${hero.name} tiến hóa ${s.heroes[id].star} sao!`, 'star');
      app.persist();
      draw();
      onChange?.();
    }
  }
  draw();
  return m;
}

function statRow(ic: string, name: string, v: number) {
  return h('div', { class: 'row gap6' }, h('span', { html: icon(ic, 22) }), h('span', { class: 'grow' }, name), h('b', { class: 'title', style: 'font-size:17px' }, String(v)));
}
