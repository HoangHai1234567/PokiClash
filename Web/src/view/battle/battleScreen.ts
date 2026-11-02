// Màn trận: điều khiển lượt, phát lại sự kiện của core/battle kèm hoạt cảnh.
import './battle.css';
import { aiInnate, aiPickIndex, aiSwapChoice } from '../../core/ai';
import {
  activeOf, advance, canSwap, createBattle, execute, fighterName, forceSwap, innateBlock, innateCard, pick, startBattle, swap, useInnate,
  type Battle, type Ev, type FSnap, type SideId, type Snap,
} from '../../core/battle';
import { CARD } from '../../core/data/cards';
import { CFG } from '../../core/data/config';
import { HERO } from '../../core/data/heroes';
import { STAGE, ZONE, zoneStages } from '../../core/data/stages';
import { cardText, costText, pct } from '../../core/cardtext';
import { ELEM_NAME, elemMult, RARITY_COLOR } from '../../core/elements';
import { enemyTeam, playerTeam, teamSlots, winStage, type StageReward } from '../../core/progression';
import { Rng, randomSeed } from '../../core/rng';
import type { Stat } from '../../core/types';
import { app, type Screen } from '../app';
import { ATTACK, SKILL } from '../aola';
import { clear, h, wait } from '../dom';
import { icon } from '../icons';
import { sfx } from '../sfx';
import { bar, cardEl, elemTag, heroImg, posIn } from '../ui';
import { Stage } from './stage';

const STAT_VN: Record<Stat, string> = { atk: 'Công', def: 'Thủ', crit: 'Chí mạng', lifesteal: 'Hút máu', dodge: 'Né', dmgTaken: 'Sát thương nhận' };

interface Plate {
  el: HTMLElement;
  name: HTMLElement;
  meta: HTMLElement;
  hp: ReturnType<typeof bar>;
  mana: ReturnType<typeof bar>;
  rage: ReturnType<typeof bar>;
  chips: HTMLElement;
  bench: HTMLElement;
}

export interface BattleParams {
  stageId: number;
  team: string[];
}

export function battleScreen(): Screen {
  return new BattleScreen();
}

class BattleScreen implements Screen {
  el: HTMLElement;
  top = 'none' as const;
  private b!: Battle;
  private stage!: Stage;
  private stageId = 1;
  private team: string[] = [];
  private alive = true;
  private speed = 1;
  private auto = false;
  private busy = false;
  private plates!: [Plate, Plate];
  private roundLbl!: HTMLElement;
  private turnChip!: HTMLElement;
  private speedBtn!: HTMLButtonElement;
  private autoBtn!: HTMLButtonElement;
  private panel!: HTMLElement;
  private qHead!: HTMLElement;
  private qRow!: HTMLElement;
  private offer!: HTMLElement;
  private bottom!: HTMLElement;
  private overlay!: HTMLElement;
  private snap: Snap | null = null;
  private pending: Promise<void> = Promise.resolve();
  private execIdx = -1;
  private pickDone: (() => void) | null = null;
  private hinted = new Set<string>();

  constructor() {
    this.el = h('div', { class: 'screen' });
  }

  enter(params?: unknown) {
    const p = params as BattleParams;
    this.stageId = p.stageId;
    this.team = p.team.slice(0, teamSlots(app.save)); // chỉ mang đủ số ô đội đã mở
    this.speed = app.save.settings.speed || 1;
    const st = STAGE[this.stageId];
    const unlock = app.save.level;
    this.b = createBattle([playerTeam(app.save, this.team), enemyTeam(st)], randomSeed(), [unlock, Math.max(unlock, st.enemies[0].level)]);
    this.stage = new Stage(ZONE[st.zone], () => app.scale);
    this.stage.speed = this.speed;
    this.build();
    void this.run();
  }

  leave() {
    this.alive = false;
    this.stage?.destroy();
    this.pickDone?.();
  }

  // ---------- dựng giao diện ----------
  private build() {
    clear(this.el);
    this.roundLbl = h('div', { class: 'round-lbl' }, 'Hiệp 1');
    this.turnChip = h('div', { class: 'turn-chip sk thin' }, '...');
    this.speedBtn = h('button', { class: 'btn small paper', onclick: () => this.toggleSpeed() }, `×${this.speed}`) as HTMLButtonElement;
    this.autoBtn = h('button', { class: 'btn small paper', onclick: () => this.toggleAuto() }, 'Tự chơi') as HTMLButtonElement;
    const top = h(
      'div',
      { class: 'bt-top' },
      h('button', { class: 'btn round paper', style: 'width:42px;height:42px', html: icon('pause', 24), onclick: () => this.menu() }),
      this.roundLbl,
      this.turnChip,
      h('div', { class: 'grow' }),
      this.speedBtn,
      this.autoBtn,
    );
    this.plates = [this.makePlate(0), this.makePlate(1)];
    this.qHead = h('div', { class: 'q-head' });
    this.qRow = h('div', { class: 'q-row' });
    this.offer = h('div', { class: 'offer' });
    this.bottom = h('div', { class: 'bt-bottom' });
    this.panel = h('div', { class: 'bt-panel' }, this.qHead, this.qRow, this.offer, this.bottom);
    this.overlay = h('div', { class: 'layer', style: 'z-index:20' });
    this.el.append(this.stage.canvas, top, this.plates[0].el, this.plates[1].el, this.panel, this.overlay);
  }

  private makePlate(side: SideId): Plate {
    const name = h('span', { class: 'pname' });
    const meta = h('span', { class: 'row gap4' });
    const hp = bar('hp');
    const mana = bar('thin mana', false);
    const rage = bar('thin rage', false);
    const chips = h('div', { class: 'chips' });
    const bench = h('div', { class: 'bench' });
    const el = h(
      'div',
      { class: 'plate sk', style: side === 0 ? 'left:10px;top:404px;transform:rotate(0.6deg)' : 'right:10px;top:66px;transform:rotate(-0.8deg)' },
      h('div', { class: 'row gap6' }, name, meta),
      hp.el,
      h('div', { class: 'bars2' }, mana.el, rage.el),
      chips,
      bench,
    );
    return { el, name, meta, hp, mana, rage, chips, bench };
  }

  private fillPlate(side: SideId) {
    const p = this.plates[side];
    const f = activeOf(this.b, side);
    p.name.textContent = fighterName(f);
    clear(p.meta);
    p.meta.append(elemTag(f.hero.elem), h('span', { class: 'lv' }, `Lv${f.level}`), f.boss ? h('span', { class: 'boss-tag' }, 'BOSS') : '');
  }

  private applySnap(s: Snap) {
    this.snap = s;
    for (const side of [0, 1] as SideId[]) {
      const f: FSnap = s.f[side][s.active[side]];
      const p = this.plates[side];
      p.hp.set(f.hp, f.maxHp, f.shield, `${f.hp}/${f.maxHp}${f.shield ? ` +${f.shield}🛡` : ''}`);
      p.mana.set(f.mana, CFG.maxMana);
      p.rage.set(f.rage, CFG.maxRage);
      clear(p.chips);
      if (f.atkB) p.chips.append(h('span', { class: f.atkB > 0 ? 'up' : 'down' }, `Công ${f.atkB > 0 ? '+' : '−'}${pct(Math.abs(f.atkB))}`));
      if (f.defB) p.chips.append(h('span', { class: f.defB > 0 ? 'up' : 'down' }, `Thủ ${f.defB > 0 ? '+' : '−'}${pct(Math.abs(f.defB))}`));
      for (const [id, left] of f.st) p.chips.append(h('span', { class: id === 'burn' || id === 'stun' ? 'down' : 'up' }, `${{ burn: 'Bỏng', stun: 'Choáng', regen: 'Hồi', evade: 'Né' }[id]}${id === 'burn' || id === 'regen' ? ' ' + left : ''}`));
      clear(p.bench);
      if (s.f[side].length > 1)
        s.f[side].forEach((x, i) => p.bench.append(h('i', { class: `${x.dead ? 'dead' : ''} ${i === s.active[side] ? 'act' : ''}` })));
      this.stage.setStatuses(side, f.st);
    }
    this.renderBottom();
  }

  // ---------- vòng trận ----------
  private async run() {
    await document.fonts.ready;
    const b = this.b;
    await Promise.all([
      this.stage.setActor(0, activeOf(b, 0).hero.id, false, true, activeOf(b, 0).form),
      this.stage.setActor(1, activeOf(b, 1).hero.id, activeOf(b, 1).boss, true, activeOf(b, 1).form),
    ]);
    this.fillPlate(0);
    this.fillPlate(1);
    await this.intro();
    if (!this.alive) return;
    await this.playEvs(startBattle(b));
    while (this.alive && b.phase !== 'over') {
      if (b.phase === 'forceSwap') {
        if (b.turn.side === 0) {
          const idx = this.auto ? aiForced(b) : await this.chooseForced();
          if (!this.alive) return;
          await this.playEvs(forceSwap(b, idx));
        } else await this.playEvs(advance(b));
        continue;
      }
      if (b.phase === 'picking') {
        if (b.turn.side === 0 && !this.auto) await this.playerPicking();
        else await this.aiPicking();
        if (!this.alive) return;
        this.renderOffer();
        await this.playEvs(execute(b));
        continue;
      }
      if (b.phase === 'ready') {
        await this.playEvs(execute(b));
        continue;
      }
      await this.playEvs(advance(b));
    }
    if (this.alive) await this.finish();
  }

  private async intro() {
    const t = (side: SideId) =>
      h('div', { class: 'team' }, ...this.b.sides[side].fighters.map((f, i) => h('div', { style: `animation-delay:${i * 0.08}s` }, heroImg(f.hero.id, side === 1 && f.boss ? 120 : 96))));
    const st = STAGE[this.stageId];
    const v = h(
      'div',
      { class: 'vs' },
      h('div', { class: 'nm' }, `${ZONE[st.zone].name} · Ải ${st.idx} · ${st.name}`),
      t(1),
      h('div', { class: 'vsword' }, 'VS'),
      t(0),
      h('div', { class: 'nm', style: 'font-size:18px' }, 'Đội bạn'),
    );
    this.overlay.appendChild(v);
    sfx.whoosh();
    await wait(1500);
    v.classList.add('out');
    await wait(300);
    v.remove();
  }

  // ---------- người chơi chọn ----------
  private playerPicking(): Promise<void> {
    return new Promise<void>((resolve) => {
      this.pickDone = () => {
        this.pickDone = null;
        resolve();
      };
      this.renderQueue();
      this.renderOffer();
      this.renderBottom();
      this.hint('pick');
    });
  }

  private async onPick(i: number, cardEl?: HTMLElement) {
    const b = this.b;
    if (this.busy || b.phase !== 'picking' || b.turn.side !== 0) return;
    this.busy = true;
    sfx.pick();
    const slot = this.qRow.querySelector('.tile.empty') as HTMLElement | null;
    if (cardEl && slot) await this.flyCard(cardEl, slot);
    pick(b, i);
    this.renderQueue();
    this.renderOffer();
    this.renderBottom();
    this.busy = false;
    if ((b.phase as string) === 'ready') {
      await wait(350 / this.speed);
      this.pickDone?.();
    }
  }

  private async flyCard(from: HTMLElement, to: HTMLElement) {
    const a = posIn(app.root, from), z = posIn(app.root, to);
    const clone = from.cloneNode(true) as HTMLElement;
    from.classList.add('gone');
    clone.style.cssText = `position:absolute;left:${a[0] - 80}px;top:${a[1] - 116}px;z-index:70;transition:transform .26s cubic-bezier(.5,-0.2,.6,1);pointer-events:none;animation:none`;
    app.flyLayer.appendChild(clone);
    await wait(16);
    clone.style.transform = `translate(${z[0] - a[0]}px, ${z[1] - a[1]}px) scale(0.32) rotate(-12deg)`;
    await wait(270);
    clone.remove();
  }

  private onInnate(which: 'skill' | 'ult', btn: HTMLElement) {
    const b = this.b;
    if (b.turn.side !== 0 || this.auto || this.busy) return;
    const why = innateBlock(b, which);
    if (why) {
      sfx.error();
      btn.classList.remove('shake');
      void btn.offsetWidth;
      btn.classList.add('shake');
      app.toast(why, 'info');
      return;
    }
    const evs = useInnate(b, which);
    const last = evs[evs.length - 1];
    if (last) this.applySnap(last.snap);
    sfx.buff();
    if (which === 'ult') {
      sfx.ult();
      this.stage.text(0, 'Tuyệt kỹ sẵn sàng!', '#ff8fb3', 22);
    }
    this.renderQueue();
    this.renderBottom();
  }

  private async onSwap(idx: number) {
    const b = this.b;
    if (b.turn.side !== 0 || this.auto || this.busy) return;
    if (idx === b.sides[0].active) return;
    if (!canSwap(b, idx)) {
      sfx.error();
      const f = b.sides[0].fighters[idx];
      app.toast(f.dead ? `${f.hero.name} đã gục` : 'Chỉ đổi tướng đầu lượt, trước khi chọn thẻ', 'info');
      return;
    }
    this.busy = true;
    await this.playEvs(swap(b, idx));
    this.busy = false;
    this.renderQueue();
    this.renderOffer();
    this.renderBottom();
  }

  private chooseForced(): Promise<number> {
    return new Promise((resolve) => {
      const b = this.b;
      const box = h('div', { class: 'col center gap12' }, h('h2', null, 'Chọn tướng ra sân'), h('div', { class: 'muted' }, 'Tướng đang đánh đã gục.'));
      const row = h('div', { class: 'row gap12' });
      const foe = activeOf(b, 1);
      b.sides[0].fighters.forEach((f, i) => {
        if (f.dead) return;
        const em = elemMult(f.hero.elem, foe.hero.elem), bad = elemMult(foe.hero.elem, f.hero.elem);
        row.append(
          h(
            'div',
            { class: 'mate sk', style: 'width:110px;height:140px;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:8px', onclick: () => { m.close(); resolve(i); } },
            heroImg(f.hero.id, 80),
            h('div', { class: 'title', style: 'font-size:14px' }, f.hero.name),
            h('div', { class: 'small' }, `${f.hp}/${f.maxHp}`),
            em > 1 ? h('div', { class: 'small', style: 'color:var(--green-d)' }, 'Khắc địch') : bad > 1 ? h('div', { class: 'small', style: 'color:var(--red)' }, 'Bị khắc') : null,
          ),
        );
      });
      box.append(row);
      const m = app.modal(box, { closable: false, width: 440 });
    });
  }

  // ---------- máy chọn (địch, hoặc tự chơi) ----------
  private async aiPicking() {
    const b = this.b;
    const side = b.turn.side;
    this.renderQueue();
    this.renderBottom();
    if (side === 1) this.renderFoeThinking();
    else this.renderOffer();
    await wait(420 / this.speed);
    const sw = aiSwapChoice(b);
    if (sw >= 0) await this.playEvs(swap(b, sw));
    while (this.alive && b.phase === 'picking') {
      const inn = aiInnate(b);
      if (inn) {
        const evs = useInnate(b, inn);
        if (evs.length) this.applySnap(evs[evs.length - 1].snap);
        const c = innateCard(activeOf(b, side), inn).card;
        this.stage.text(side, `${inn === 'ult' ? 'Tuyệt kỹ' : 'Chiêu'}: ${c.name}`, inn === 'ult' ? '#ff8fb3' : '#8ec5ff', 20);
        sfx.buff();
        this.renderQueue();
        await wait(380 / this.speed);
      }
      // địch ở các ải đầu chọn kém hơn (nhiễu cao), về sau chọn kỹ
      const i = aiPickIndex(b, side === 1 ? Math.max(0.12, 0.6 - this.stageId * 0.05) : 0.12);
      if (side === 0) {
        const cardNode = this.offer.children[i] as HTMLElement | undefined;
        if (cardNode) {
          cardNode.style.transform = 'translateY(-14px) scale(1.05)';
          await wait(260 / this.speed);
          sfx.pick();
          const slot = this.qRow.querySelector('.tile.empty') as HTMLElement | null;
          if (slot) await this.flyCard(cardNode, slot);
        }
        pick(b, i);
        this.renderQueue();
        this.renderOffer();
      } else {
        const backs = this.offer.querySelectorAll('.back-card');
        const chosen = backs[i] as HTMLElement | undefined;
        if (chosen) {
          chosen.style.transform = 'translateY(-16px) rotate(-4deg)';
          await wait(200 / this.speed);
        }
        sfx.deal();
        pick(b, i);
        this.renderQueue();
        this.renderFoeThinking();
        await wait(260 / this.speed);
      }
    }
  }

  // ---------- vẽ hàng thẻ, thẻ chọn, nút ----------
  private renderQueue() {
    const b = this.b, t = b.turn;
    const mine = t.side === 0;
    clear(this.qHead);
    this.qHead.append(
      h('span', { html: icon(mine ? 'cards' : 'skull', 24) }),
      mine ? 'Hàng thẻ của bạn' : `Hàng thẻ của ${fighterName(activeOf(b, 1))}`,
      h('span', { class: 'cnt sk thin' }, b.phase === 'picking' ? `Chọn ${t.picksTotal - t.picksLeft + 1}/${t.picksTotal}` : 'Ra đòn!'),
    );
    clear(this.qRow);
    const items = t.queue;
    items.forEach((q, i) => {
      const c = CARD[q.card];
      this.qRow.append(
        h(
          'div',
          { class: `tile sk thin ${q.kind === 'skill' ? 'skill' : ''} ${i < this.execIdx ? 'done' : ''} ${i === this.execIdx ? 'now' : ''}`, style: `--rc:${RARITY_COLOR[c.rarity]}`, title: `${c.name}: ${cardText(c, q.lv)}` },
          h('span', { html: icon(c.icon, 38) }),
          h('div', { class: 'tn' }, c.name),
        ),
      );
    });
    const pickedPool = items.filter((q) => q.kind === 'pool').length;
    for (let i = pickedPool; i < t.picksTotal; i++) this.qRow.append(h('div', { class: 'tile sk thin empty' }));
    this.qRow.append(h('div', { class: 'q-arrow' }, '➜'));
    const ult = t.ult ? CARD[t.ult.card] : null;
    this.qRow.append(
      h(
        'div',
        { class: `tile sk thin final ${ult ? 'ult' : ''} ${this.execIdx >= items.length ? 'now' : ''}` },
        h('span', { html: icon(ult ? ult.icon : t.stunned ? 'bolt' : 'fist', 38) }),
        h('div', { class: 'tn' }, ult ? ult.name : t.stunned ? 'Choáng' : 'Đánh thường'),
      ),
    );
  }

  private renderOffer() {
    const b = this.b, t = b.turn;
    clear(this.offer);
    this.offer.className = 'offer';
    if (t.side !== 0 || b.phase !== 'picking') {
      if (b.phase === 'over') return;
      const who = fighterName(activeOf(b, t.side));
      this.offer.append(h('div', { class: 'foe-think', style: 'padding-top:60px' }, h('div', { class: 'lbl' }, t.side === 0 ? `${who} ra đòn!` : `${who} (địch) ra đòn!`)));
      return;
    }
    t.offer.forEach((id, i) => {
      const el = cardEl(id, 1, { onclick: () => void this.onPick(i, el) });
      if (this.auto) el.style.pointerEvents = 'none';
      this.offer.append(el);
    });
    sfx.deal();
  }

  private renderFoeThinking() {
    const b = this.b, t = b.turn;
    // lá úp chỉ chia một lần mỗi lượt; các lần sau chỉ trả lá vừa chọn về chỗ
    const old = this.offer.querySelector('.foe-think');
    if (old && b.phase === 'picking' && old.querySelectorAll('.back-card').length) {
      old.querySelectorAll<HTMLElement>('.back-card').forEach((c) => (c.style.transform = ''));
      return;
    }
    clear(this.offer);
    const box = h('div', { class: 'foe-think' }, h('div', { class: 'lbl' }, b.phase === 'picking' ? `${fighterName(activeOf(b, 1))} đang chọn thẻ...` : 'Địch ra đòn!'));
    if (b.phase === 'picking') box.append(h('div', { class: 'row gap12' }, ...t.offer.map(() => h('div', { class: 'back-card sk', html: icon('dice', 70) }))));
    this.offer.append(box);
  }

  private renderBottom() {
    const b = this.b;
    if (!b) return;
    clear(this.bottom);
    const side = b.sides[0];
    const t = b.turn;
    const myTurn = t.side === 0 && b.phase === 'picking' && !this.auto;
    side.fighters.forEach((f, i) => {
      const can = myTurn && canSwap(b, i);
      const el = h(
        'div',
        { class: `mate sk thin ${i === side.active ? 'act' : ''} ${f.dead ? 'dead' : ''} ${can ? 'can' : ''}`, title: `${f.hero.name}${can ? ' · bấm để đổi ra sân' : ''}`, onclick: () => void this.onSwap(i) },
        heroImg(f.hero.id, 54),
        h('div', { class: 'mhp' }, h('i', { style: `width:${(f.hp / f.maxHp) * 100}%` })),
      );
      this.bottom.append(el);
    });
    const me = activeOf(b, 0);
    for (const which of ['skill', 'ult'] as const) {
      const { card, lv } = innateCard(me, which);
      const why = t.side === 0 ? innateBlock(b, which) : 'Lượt địch';
      const used = which === 'skill' ? t.side === 0 && t.skillUsed : t.side === 0 && !!t.ult;
      const el = h(
        'div',
        { class: `inn sk thin ${which === 'ult' ? 'ult' : ''} ${!why && myTurn ? 'ready' : ''} ${why && !used ? 'off' : ''} ${used ? 'used' : ''}`, title: `${card.name}: ${cardText(card, lv)}` },
        h('span', { html: icon(card.icon, 42) }),
        h('div', { class: 'col', style: 'min-width:0' }, h('div', { class: 't' }, which === 'ult' ? 'Tuyệt kỹ' : 'Chiêu'), h('div', { class: 's' }, card.name), h('div', { class: 's' }, used ? 'Đã xếp' : costText(card))),
        which === 'ult' ? h('div', { class: 'meter' }, h('i', { style: `width:${Math.min(100, me.rage)}%` })) : null,
      );
      el.addEventListener('click', () => this.onInnate(which, el));
      this.bottom.append(el);
      if (!why && myTurn && which === 'skill') this.hint('skill', el);
      if (!why && myTurn && which === 'ult') this.hint('ult', el);
    }
  }

  // ---------- phát sự kiện ----------
  private async playEvs(evs: Ev[]) {
    for (const e of evs) {
      if (!this.alive) return;
      await this.playEv(e);
    }
    await this.pending;
  }

  private async playEv(e: Ev) {
    const st = this.stage, sp = () => this.speed;
    const W = (ms: number) => wait(ms / sp());
    if (['card', 'turn', 'ult', 'attack', 'round', 'swap'].includes(e.t)) await this.pending;
    switch (e.t) {
      case 'start':
        break;
      case 'round':
        this.roundLbl.textContent = `Hiệp ${e.round}`;
        await this.banner(`Hiệp ${e.round}`, "Bạn đi trước");
        break;
      case 'turn': {
        this.execIdx = -1;
        this.turnChip.textContent = e.side === 0 ? 'Lượt bạn' : 'Lượt địch';
        this.turnChip.classList.toggle('foe', e.side === 1);
        this.renderQueue();
        if (e.side === 1) this.renderFoeThinking();
        break;
      }
      case 'card': {
        if (e.rep === 0) this.execIdx++;
        this.renderQueue();
        const c = CARD[e.card];
        sfx.card();
        this.flyTile(e.side);
        st.text(e.side, c.name, e.kind === 'skill' ? '#8ec5ff' : '#fff6c8', 22);
        if (e.kind === 'skill') {
          let hit!: () => void;
          const hp = new Promise<void>((r) => (hit = r));
          this.pending = st.play(e.side, SKILL, () => hit());
          await hp;
        } else await W(420);
        break;
      }
      case 'innate':
        break;
      case 'buff': {
        const up = e.stat === 'dmgTaken' ? e.v < 0 : e.v > 0;
        const v = e.stat === 'dmgTaken' ? `${STAT_VN[e.stat]} ${e.v > 0 ? '+' : '−'}${pct(Math.abs(e.v))}` : `${e.v > 0 ? '+' : '−'}${pct(Math.abs(e.v))} ${STAT_VN[e.stat]}`;
        st.text(e.side, `${up ? '▲' : '▼'} ${v}`, up ? '#9be36a' : '#ff8a7a', 21);
        if (up) sfx.buff();
        else sfx.debuff();
        await W(230);
        break;
      }
      case 'heal':
        st.number(e.side, e.amount, '#7be36a');
        st.ring(e.side, '#6cbf4f');
        sfx.heal();
        await W(260);
        break;
      case 'maxhp':
        st.text(e.side, `+${e.amount} máu tối đa`, '#7be36a', 21);
        st.ring(e.side, '#f7c948');
        sfx.heal();
        await W(260);
        break;
      case 'shield':
        st.text(e.side, `+${e.amount} khiên`, '#8ec5ff', 22);
        st.ring(e.side, '#4a90d9');
        sfx.shield();
        await W(260);
        break;
      case 'mana':
        st.text(e.side, `${e.v > 0 ? '+' : ''}${e.v} mana`, '#8ec5ff', 19);
        await W(160);
        break;
      case 'rage':
        st.text(e.side, `${e.v > 0 ? '+' : ''}${e.v} nộ`, '#ffb070', 19);
        await W(160);
        break;
      case 'status': {
        const name = { burn: 'Bỏng!', stun: 'Choáng!', regen: 'Hồi phục', evade: 'Sẵn sàng né' }[e.id];
        st.text(e.side, name, e.id === 'burn' ? '#ffb070' : e.id === 'stun' ? '#ffe14a' : '#bfe8a0', 26);
        if (e.id === 'stun' || e.id === 'burn') sfx.debuff();
        else sfx.buff();
        await W(300);
        break;
      }
      case 'resist':
        st.text(e.side, 'Trượt hiệu ứng', '#ddd', 20);
        await W(200);
        break;
      case 'cleanse':
        st.text(e.side, 'Sạch hiệu ứng xấu', '#bfe8ff', 21);
        st.ring(e.side, '#bfe8ff');
        await W(240);
        break;
      case 'double':
        st.text(e.side, 'Thẻ sau ×2!', '#ffe14a', 24);
        await W(240);
        break;
      case 'stunned':
        st.text(e.side, 'Choáng: mất lượt', '#ffe14a', 20);
        sfx.debuff();
        await W(700);
        break;
      case 'passive': {
        const c = CARD[e.card];
        if (this.snap && this.snap.active[e.side] !== e.idx) break;
        st.text(e.side, `✦ ${c.name}`, '#e3c4ff', 20);
        await W(260);
        break;
      }
      case 'attack': {
        this.execIdx = this.b.turn.queue.length;
        this.renderQueue();
        sfx.whoosh();
        let hit!: () => void;
        const hp = new Promise<void>((r) => (hit = r));
        this.pending = st.play(e.side, ATTACK, () => hit());
        await hp;
        break;
      }
      case 'ult': {
        this.execIdx = this.b.turn.queue.length;
        this.renderQueue();
        const c = CARD[e.card];
        sfx.ult();
        st.flash('#fff3c4');
        void this.banner(c.name, `Tuyệt kỹ của ${fighterName(activeOf(this.b, e.side))}`, true);
        let hit!: () => void;
        const hp = new Promise<void>((r) => (hit = r));
        this.pending = st.play(e.side, SKILL, () => hit());
        await hp;
        break;
      }
      case 'dmg': {
        if (e.kind === 'self') {
          st.number(e.to, e.amount, '#ff8a7a');
          sfx.debuff();
          await W(240);
          break;
        }
        if (e.dodged) {
          st.dodge(e.to);
          st.text(e.to, 'Né!', '#e3c4ff', 30);
          sfx.miss();
          await W(260);
          break;
        }
        if (e.kind === 'burn') {
          st.number(e.to, e.amount, '#ffb070');
          st.hurt(e.to);
          sfx.hit(false);
          await W(360);
          break;
        }
        const big = e.crit || e.kind === 'ult';
        st.hurt(e.to, big);
        st.burst(e.to, big);
        st.number(e.to, e.amount, e.crit ? '#ffe14a' : '#ff6a5a', big);
        if (e.crit) st.text(e.to, 'CHÍ MẠNG!', '#ffe14a', 28);
        if (e.elem > 1) st.text(e.to, 'Khắc hệ ×1,5', '#9be36a', 18);
        if (e.elem < 1) st.text(e.to, 'Bị khắc ×0,75', '#c9c0b0', 18);
        if (e.blocked) st.text(e.to, `Khiên đỡ ${e.blocked}`, '#8ec5ff', 18);
        sfx.hit(big);
        this.plates[e.to].el.classList.remove('shake');
        void this.plates[e.to].el.offsetWidth;
        this.plates[e.to].el.classList.add('shake');
        await W(big ? 330 : 240);
        break;
      }
      case 'revive':
        await this.pending;
        st.text(e.side, 'Hồi sinh!', '#ffe08a', 30);
        st.ring(e.side, '#f7c948');
        st.flash('#fff6c9');
        sfx.level();
        await W(700);
        break;
      case 'evolve': {
        // boss lên dạng sau: hiệu ứng như hồi sinh, đổi hình và tên dạng (thanh máu đổi theo ảnh chụp)
        await this.pending;
        const f = this.b.sides[e.side].fighters[e.idx];
        const name = f.hero.forms[e.form].name;
        st.text(e.side, 'Tiến hóa!', '#ffe08a', 34);
        st.ring(e.side, '#f7c948');
        st.flash('#fff6c9');
        sfx.level();
        await st.setActor(e.side, f.hero.id, f.boss, false, e.form);
        this.plates[e.side].name.textContent = name;
        st.text(e.side, name, '#fff6c8', 22);
        await W(900);
        break;
      }
      case 'death': {
        await this.pending;
        st.die(e.side);
        st.text(e.side, 'Gục!', '#c9c0b0', 34);
        sfx.lose();
        await W(900);
        break;
      }
      case 'swap': {
        sfx.swap();
        await st.retreat(e.side);
        const f = this.b.sides[e.side].fighters[e.to];
        await st.setActor(e.side, f.hero.id, f.boss, true, f.form);
        this.fillPlate(e.side);
        st.text(e.side, e.side === 0 ? `${f.hero.name}, ra sân!` : `${f.hero.name} ra sân`, '#fff6c8', 22);
        await W(480);
        break;
      }
      case 'end':
        break;
    }
    this.applySnap(e.snap);
  }

  // ô thẻ đang chạy bay từ hàng thẻ lên đầu tướng rồi tan
  private flyTile(side: SideId) {
    const tile = this.qRow.querySelector<HTMLElement>('.tile.now');
    if (!tile) return;
    const a = posIn(app.root, tile);
    const [hx, hy] = this.stage.head(side);
    const clone = tile.cloneNode(true) as HTMLElement;
    clone.classList.remove('now', 'done');
    const sp = this.speed;
    clone.style.cssText += `;position:absolute;left:${a[0] - 28}px;top:${a[1] - 35}px;z-index:70;pointer-events:none;transition:transform ${0.32 / sp}s cubic-bezier(.3,1.4,.5,1), opacity ${0.2 / sp}s ${0.3 / sp}s`;
    app.flyLayer.appendChild(clone);
    requestAnimationFrame(() => {
      clone.style.transform = `translate(${hx - a[0]}px, ${hy + 56 - 40 - a[1]}px) scale(1.4) rotate(${side === 0 ? -8 : 8}deg)`;
      clone.style.opacity = '0';
    });
    setTimeout(() => clone.remove(), 600 / sp);
  }

  private async banner(title: string, sub: string, ult = false) {
    const el = h('div', { class: `banner sk ${ult ? 'ult' : ''}` }, h('h2', null, title), h('div', { class: 'sub' }, sub));
    this.overlay.appendChild(el);
    await wait((ult ? 900 : 750) / this.speed);
    el.classList.add('out');
    await wait(250);
    el.remove();
  }

  private hint(key: string, anchor?: HTMLElement) {
    if (!app.save.settings.hints || this.hinted.has(key) || app.save.stats.battles > 1) return;
    this.hinted.add(key);
    const text: Record<string, string> = {
      pick: 'Chọn 1 trong 3 thẻ, 5 lần. Thẻ chạy lần lượt rồi tướng đánh thường.',
      skill: 'Đủ mana: bấm Chiêu để xen chiêu vào hàng thẻ. Không tốn lần chọn!',
      ult: 'Đủ nộ: bật Tuyệt kỹ, nó thay cú đánh thường cuối lượt.',
    };
    const pos = anchor ? posIn(app.root, anchor) : [180, 690];
    const bubble = h('div', { class: 'speech sk', style: `left:${Math.min(220, Math.max(10, pos[0] - 150))}px;top:${pos[1] - 120}px` }, text[key]);
    this.overlay.appendChild(bubble);
    setTimeout(() => bubble.remove(), 4200);
  }

  // ---------- nút trên ----------
  private toggleSpeed() {
    this.speed = this.speed >= 3 ? 1 : this.speed + 1;
    this.stage.speed = this.speed;
    this.speedBtn.textContent = `×${this.speed}`;
    app.save.settings.speed = this.speed;
    app.persist();
    sfx.click();
  }

  private toggleAuto() {
    this.auto = !this.auto;
    this.autoBtn.style.setProperty('--fill', this.auto ? 'var(--green)' : 'var(--paper)');
    this.autoBtn.textContent = this.auto ? 'Đang tự chơi' : 'Tự chơi';
    sfx.click();
    // đang tới lượt mình chọn thì để máy chọn nốt
    if (this.auto && this.pickDone && this.b.turn.side === 0 && this.b.phase === 'picking') {
      const done = this.pickDone;
      this.pickDone = null;
      void this.aiPicking().then(done);
    }
    this.renderOffer();
    this.renderBottom();
  }

  private menu() {
    sfx.click();
    const st = STAGE[this.stageId];
    const m = app.modal(
      h(
        'div',
        { class: 'col center gap12', style: 'text-align:center' },
        h('h2', null, 'Tạm dừng'),
        h('div', { class: 'muted' }, `${ZONE[st.zone].name} · Ải ${st.idx}: ${st.name}`),
        h('div', { style: 'font-size:15px;max-width:360px' }, 'Mẹo: thẻ chạy theo thứ tự xếp. Xếp thẻ tăng Công trước chiêu để chiêu đánh mạnh hơn. Hệ khắc: Kim → Mộc → Thổ → Thủy → Hỏa → Kim.'),
        h('button', { class: 'btn green', onclick: () => m.close() }, 'Đánh tiếp'),
        h('button', { class: 'btn paper small', onclick: () => { m.close(); app.save.stats.battles++; app.persist(); app.go('zone', { zone: st.zone }); } }, 'Bỏ trận (tính thua)'),
      ),
      { width: 420 },
    );
  }

  // ---------- kết thúc ----------
  private async finish() {
    const win = this.b.winner === 0;
    await wait(500);
    const s = app.save;
    const before = s.level;
    let rw: StageReward | null = null;
    if (win) rw = winStage(s, this.stageId, new Rng(randomSeed()));
    else s.stats.battles++;
    app.persist();
    if (win) sfx.win();
    else sfx.lose();
    const st = STAGE[this.stageId];
    const next = zoneStages(st.zone).find((x) => x.idx === st.idx + 1);
    const body = h('div', { class: 'col center gap12', style: 'text-align:center' });
    body.append(h('div', { class: `stamp ${win ? '' : 'lose'}` }, win ? 'Thắng!' : 'Thua rồi'));
    body.append(h('div', { class: 'title', style: 'font-size:20px;margin-top:6px' }, `${ZONE[st.zone].name} · Ải ${st.idx} · ${st.name}`));
    body.append(h('div', { class: 'small muted' }, `${this.b.round} hiệp · gây ${this.b.dmgDealt[0]} sát thương`));
    if (rw) {
      const list = h('div', { class: 'col gap8', style: 'width:100%;align-items:stretch' });
      list.append(h('div', { class: 'row gap8 sk thin', style: 'padding:8px 12px;--fill:#fff' }, h('span', { html: icon('ball', 36) }), h('div', { class: 'title', style: 'font-size:22px' }, `+${rw.balls} bi`), rw.first ? h('span', { class: 'label-tag sk thin', style: 'margin-left:auto' }, 'Lần đầu qua ải') : null));
      for (const sh of rw.shards) {
        const hero = HERO[sh.hero];
        const prog = s.heroes[sh.hero];
        list.append(
          h(
            'div',
            { class: 'row gap8 sk thin', style: `padding:6px 12px;--fill:${sh.unlocked ? '#fff3c4' : '#fff'}` },
            heroImg(sh.hero, 52),
            h(
              'div',
              { class: 'col', style: 'align-items:flex-start' },
              h('div', { class: 'title', style: 'font-size:18px' }, sh.unlocked ? `Mở khóa ${hero.name}!` : `${hero.name} +${sh.n} mảnh`),
              h('div', { class: 'small muted' }, sh.unlocked ? 'Tướng mới đã vào đội hình' : sh.converted ? `Đã có tướng: đổi thành ${sh.converted} bản sao thẻ` : `${prog.shards}/${hero.shards} mảnh`),
            ),
          ),
        );
        if (sh.unlocked) sfx.chest();
      }
      body.append(list);
    } else {
      body.append(
        h(
          'div',
          { class: 'col gap6', style: 'font-size:16px;text-align:left' },
          h('div', null, '• Thả bi ở Máy bi để lên cấp: mọi tướng mạnh lên.'),
          h('div', null, '• Nâng thẻ và tiến hóa ở mục Tướng.'),
          h('div', null, `• Chọn tướng khắc hệ địch (${ELEM_NAME[HERO[st.enemies[0].hero].elem]} bị ${ELEM_NAME[khac(HERO[st.enemies[0].hero].elem)]} khắc).`),
        ),
      );
    }
    const btns = h('div', { class: 'row gap8', style: 'flex-wrap:wrap;justify-content:center' });
    if (win && s.balls > 0) btns.append(h('button', { class: 'btn orange', onclick: () => { m.close(); app.go('machine'); } }, h('span', { html: icon('machine', 26) }), `Máy bi (${s.balls})`));
    if (win && next && next.idx <= s.zones[st.zone] + 1) btns.append(h('button', { class: 'btn green', onclick: () => { m.close(); app.go('zone', { zone: st.zone, prep: next.id }); } }, 'Ải tiếp ➜'));
    btns.append(h('button', { class: 'btn paper', onclick: () => { m.close(); app.go('battle', { stageId: this.stageId, team: this.team }); } }, 'Đánh lại'));
    btns.append(h('button', { class: 'btn paper', onclick: () => { m.close(); app.go('zone', { zone: st.zone }); } }, ZONE[st.zone].name));
    body.append(btns);
    const m = app.modal(body, { closable: false, width: 460 });
    setTimeout(() => sfx.stamp(), 120);
    if (s.level > before) app.levelUp(before, s.level);
  }
}

function aiForced(b: Battle): number {
  return b.sides[0].fighters.findIndex((f) => !f.dead);
}

function khac(e: keyof typeof ELEM_NAME): keyof typeof ELEM_NAME {
  const by: Record<string, keyof typeof ELEM_NAME> = { moc: 'kim', tho: 'moc', thuy: 'tho', hoa: 'thuy', kim: 'hoa' };
  return by[e];
}
