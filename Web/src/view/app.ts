// Khung ứng dụng: co giãn khung 540 × 960, lưu trữ, scene (không có thanh tab), màn mây chuyển scene, hộp thoại.
// Học theo Clash of Critters: mỗi chức năng là một scene riêng (đảo lớn, đảo hệ, máy bi, tướng, trận),
// vào bằng nút trên đảo hoặc hàng nút dưới sảnh, ra bằng nút quay lại.
import { POOL } from '../core/data/cards';
import { HEROES } from '../core/data/heroes';
import { migrateAdsV2 } from '../core/ads';
import { afkChestTimes, afkPending } from '../core/afk';
import { treesStock } from '../core/trees';
import {
  canEvolve, canUpCard, expToNext, migrateRosterV3, newSave, SAVE_VERSION, SLOTS, totalCleared, X_STEPS, type SaveData,
} from '../core/progression';
import { installArt, setBoil } from './art';
import { h, fmt, wait } from './dom';
import { icon } from './icons';
import { setSound, sfx } from './sfx';
import { modal, toast, type ModalOpts } from './ui';

export interface Screen {
  el: HTMLElement;
  top: 'hud' | 'back' | 'none';
  title?: string;
  back?: () => void;
  enter?(params?: unknown): void;
  leave?(): void;
}

const KEY = 'pokiclash.save';

// mây chuyển scene: hai khối mây vẽ tay khép vào rồi tách ra
function cloudSvg(flip: boolean): string {
  const puffs: string[] = [];
  for (let i = 0; i < 16; i++) {
    const y = -40 + i * 72;
    const x = 560 + Math.sin(i * 1.7) * 60;
    puffs.push(`<circle cx="${x}" cy="${y}" r="${110 + (i % 3) * 22}"/>`);
  }
  return `<svg viewBox="0 0 760 1100" width="760" height="1100" style="${flip ? 'transform:scaleX(-1)' : ''}">
    <g fill="#fffaf0" stroke="#2b2118" stroke-width="7">${puffs.join('')}<rect x="0" y="-60" width="560" height="1220" stroke="none"/></g>
    <g fill="#fffaf0">${puffs.join('')}<rect x="0" y="-60" width="560" height="1220"/></g>
  </svg>`;
}

export class App {
  root: HTMLElement;
  screenLayer: HTMLElement;
  hudEl: HTMLElement;
  backEl: HTMLElement;
  modalLayer: HTMLElement;
  toastLayer: HTMLElement;
  flyLayer: HTMLElement;
  cloudEl: HTMLElement;
  save: SaveData;
  scale = 1;
  screens: Record<string, () => Screen> = {};
  private built: Record<string, Screen> = {};
  current: Screen | null = null;
  currentName = '';
  private moving = false;
  private queued: [string, unknown] | null = null;
  private hudParts!: { ring: SVGCircleElement; lv: HTMLElement; balls: HTMLElement; afk: HTMLElement; afkN: HTMLElement };
  private backParts!: { title: HTMLElement; balls: HTMLElement; lv: HTMLElement };

  constructor(root: HTMLElement) {
    this.root = root;
    installArt(root);
    this.save = this.load();
    this.screenLayer = h('div', { class: 'layer', style: 'pointer-events:auto' });
    this.hudEl = h('div', { class: 'hud' });
    this.backEl = h('div', { class: 'backbar' });
    this.modalLayer = h('div', { class: 'layer', style: 'z-index:40' });
    this.flyLayer = h('div', { class: 'layer', style: 'z-index:70' });
    this.toastLayer = h('div', { class: 'toast-layer' });
    this.cloudEl = h('div', { class: 'clouds' }, h('div', { class: 'c l', html: cloudSvg(false) }), h('div', { class: 'c r', html: cloudSvg(true) }));
    root.append(this.screenLayer, this.hudEl, this.backEl, this.modalLayer, this.flyLayer, this.toastLayer, this.cloudEl);
    this.buildHud();
    this.buildBack();
    this.applySettings();
    window.addEventListener('resize', () => this.fit());
    this.fit();
    setInterval(() => this.refreshHud(), 5000);
  }

  // ---------- lưu ----------
  private load(): SaveData {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) {
        const s = JSON.parse(raw) as SaveData;
        if (s.v === 2) {
          migrateAdsV2(s);
          s.v = 3;
        }
        if (s.v === 3) {
          migrateRosterV3(s);
          s.v = 4;
        }
        if (s.v === SAVE_VERSION) {
          const fresh = newSave(Date.now());
          for (const hh of HEROES) if (!s.heroes[hh.id]) s.heroes[hh.id] = fresh.heroes[hh.id];
          return s;
        }
      }
    } catch {
      /* lưu hỏng thì làm mới */
    }
    return newSave(Date.now());
  }
  persist() {
    try {
      localStorage.setItem(KEY, JSON.stringify(this.save));
    } catch {
      /* hết chỗ */
    }
    this.refreshHud();
  }
  reset() {
    localStorage.removeItem(KEY);
    this.save = newSave(Date.now());
    this.persist();
    this.built = {};
    this.go('world', undefined, false);
  }

  applySettings() {
    setBoil(this.root, this.save.settings.boil);
    setSound(this.save.settings.sound);
  }

  fit() {
    const W = window.innerWidth, H = window.innerHeight;
    this.scale = Math.min(W / 540, H / 960);
    this.root.style.transform = `scale(${this.scale})`;
    this.root.style.left = `${(W - 540 * this.scale) / 2}px`;
    this.root.style.top = `${(H - 960 * this.scale) / 2}px`;
    window.dispatchEvent(new Event('pc-fit'));
  }

  // ---------- scene ----------
  go(name: string, params?: unknown, transition = true) {
    if (this.moving) {
      this.queued = [name, params];
      return;
    }
    void this.move(name, params, transition && !!this.current);
  }

  private async move(name: string, params: unknown, transition: boolean) {
    const make = this.screens[name];
    if (!make) return;
    this.moving = true;
    if (transition) {
      sfx.whoosh();
      this.cloudEl.classList.add('cover');
      await wait(380);
    }
    this.current?.leave?.();
    let s = this.built[name];
    if (!s || name === 'battle') {
      s = make();
      if (name !== 'battle') this.built[name] = s;
    }
    this.screenLayer.replaceChildren(s.el);
    this.current = s;
    this.currentName = name;
    this.hudEl.classList.toggle('hidden', s.top !== 'hud');
    this.backEl.classList.toggle('hidden', s.top !== 'back');
    this.backParts.title.textContent = s.title ?? '';
    s.enter?.(params);
    this.refreshHud();
    if (transition) {
      await wait(60);
      this.cloudEl.classList.remove('cover');
      await wait(380);
    }
    this.moving = false;
    const q = this.queued;
    this.queued = null;
    if (q) this.go(q[0], q[1]);
  }

  setTitle(t: string) {
    this.backParts.title.textContent = t;
  }

  modal(content: Node, opts?: ModalOpts) {
    return modal(this.modalLayer, content, opts);
  }
  toast(text: string, iconName?: string) {
    toast(this.toastLayer, text, iconName);
  }

  // ---------- thanh trên của sảnh ----------
  private buildHud() {
    const ring = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    const ringSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    ringSvg.setAttribute('viewBox', '0 0 58 58');
    ringSvg.setAttribute('class', 'ring');
    ringSvg.innerHTML = `<circle cx="29" cy="29" r="25" fill="#fffaf0" stroke="#2b2118" stroke-width="3"/>
      <circle cx="29" cy="29" r="19.5" fill="#ffe9a8" stroke="#2b2118" stroke-width="2.5"/>`;
    ring.setAttribute('cx', '29');
    ring.setAttribute('cy', '29');
    ring.setAttribute('r', '22.3');
    ring.setAttribute('fill', 'none');
    ring.setAttribute('stroke', '#b783e6');
    ring.setAttribute('stroke-width', '5');
    ring.setAttribute('stroke-linecap', 'round');
    ring.setAttribute('transform', 'rotate(-90 29 29)');
    ringSvg.appendChild(ring);
    const lv = h('div', { class: 'n' });
    const balls = h('span', { class: 'num' });
    const afkN = h('span', { class: 'num' });
    const afk = h(
      'button',
      { class: 'chip sk thin', style: '--fill:#e9f6ff;cursor:pointer;border:0;background:none', onclick: () => { sfx.click(); this.openAfk(); } },
      h('span', { html: icon('clock', 28) }),
      afkN,
    );
    this.hudParts = { ring, lv, balls, afk, afkN };
    this.hudEl.append(
      h('div', { class: 'lvbadge', title: 'Cấp người chơi = cấp mọi tướng' }, ringSvg, lv),
      h('div', { class: 'chip sk thin', title: 'Bi: thả vào máy bi' }, h('span', { html: icon('ball', 28) }), balls),
      afk,
      h('div', { class: 'grow' }),
      h('button', { class: 'btn round paper', title: 'Sổ tay', html: icon('gear', 30), onclick: () => { sfx.click(); this.go('notebook'); } }),
    );
  }

  // ---------- thanh quay lại của scene con ----------
  private buildBack() {
    const title = h('h2', { class: 'bb-title sk' });
    const balls = h('span', { class: 'num' });
    const lv = h('span', { class: 'num' });
    this.backParts = { title, balls, lv };
    this.backEl.append(
      h('button', { class: 'btn round paper bb-back', title: 'Quay lại', html: icon('back', 30), onclick: () => { sfx.click(); (this.current?.back ?? (() => this.go('world')))(); } }),
      title,
      h('div', { class: 'grow' }),
      h('div', { class: 'chip sk thin', style: 'font-size:16px' }, h('span', { html: icon('exp', 24) }), lv),
      h('div', { class: 'chip sk thin', style: 'font-size:16px' }, h('span', { html: icon('ball', 24) }), balls),
    );
  }

  openAfk: () => void = () => {};

  refreshHud() {
    if (!this.hudParts) return;
    const s = this.save;
    const p = s.level >= 30 ? 1 : s.exp / expToNext(s.level);
    const C = 2 * Math.PI * 22.3;
    this.hudParts.ring.setAttribute('stroke-dasharray', `${C * p} ${C}`);
    this.hudParts.lv.innerHTML = `<small>CẤP</small>${s.level}`;
    this.hudParts.balls.textContent = fmt(s.balls);
    const afk = afkPending(s, Date.now());
    const tree = treesStock(s, Date.now());
    this.hudParts.afkN.textContent = totalCleared(s) ? (tree ? `+${tree}` : `${Math.floor(afk.hours * 60)}′`) : 'AFK';
    this.hudParts.afk.classList.toggle('pulse', tree >= 5);
    this.hudParts.afk.classList.toggle('dot', afkChestTimes(s, Date.now()).some((t) => t.ready <= Date.now()));
    this.backParts.balls.textContent = fmt(s.balls);
    this.backParts.lv.textContent = `Cấp ${s.level}`;
  }

  // số việc chờ ở mục Tướng (nâng thẻ, tiến hóa), để hiện chấm đỏ trên nút
  heroAlerts(): number {
    const s = this.save;
    let n = 0;
    for (const hh of HEROES) {
      if (!s.heroes[hh.id].owned) continue;
      if (canEvolve(s, hh.id)) n++;
      for (const k of SLOTS) if (canUpCard(s, hh.id, k)) n++;
    }
    return n;
  }

  // ---------- lên cấp ----------
  levelUp(from: number, to: number) {
    if (to <= from) return;
    sfx.level();
    const newCards = POOL.filter((c) => (c.unlock ?? 1) > from && (c.unlock ?? 1) <= to);
    const newX = X_STEPS.filter((x) => x.lv > from && x.lv <= to);
    const body = h(
      'div',
      { class: 'col center gap8', style: 'text-align:center' },
      h('div', { class: 'stamp', style: 'color:var(--purple);border-color:var(--purple);font-size:48px' }, 'Lên cấp!'),
      h('h1', { class: 'outline-text', style: 'font-size:64px;margin-top:8px' }, `Cấp ${to}`),
      h('div', { style: 'font-size:18px' }, `Mọi tướng mạnh thêm. Cấp người chơi cũng là cấp của tướng.`),
      newX.length ? h('div', { class: 'label-tag sk thin' }, `Mở nút ${newX.map((x) => '×' + x.x).join(', ')} ở máy bi`) : null,
      newCards.length ? h('div', { style: 'font-size:16px' }, `Thẻ mới vào bộ rút: ${newCards.map((c) => c.name).join(', ')}`) : null,
      h('button', { class: 'btn green', onclick: () => m.close() }, 'Tuyệt!'),
    );
    const m = this.modal(body, { width: 420 });
  }
}

export let app: App;
export function setApp(a: App) {
  app = a;
}
