// Màn boot (màn mở game): nạp trước, diễn cảnh mở, "Chạm để bắt đầu", rồi vào sảnh.
// 3 ý tưởng để so (người dùng chọn): A Sa bàn giấy, B Ấn Ngũ Hành, C Bìa sổ. Đổi bằng ?boot=a|b|c hoặc nút trên cùng.
import { app } from '../app';
import { h, wait } from '../dom';
import { sfx } from '../sfx';
import { loaderEl, preload, Ticker } from './common';
import { sceneCover } from './sceneCover';
import { sceneSeal } from './sceneSeal';
import { sceneTable } from './sceneTable';
import './boot.css';

export interface BootScene {
  el: HTMLElement;
  bottom: HTMLElement; // chỗ đặt thanh tải, rồi lời nhắc chạm
  intro(): Promise<void>;
  showTap(): void;
  exit(): Promise<void>; // xong thì sảnh phải lộ ra (tự mở mây hoặc lật bìa)
  usesClouds?: boolean; // true: bộ điều khiển kéo mây che rồi mở ra sảnh
}

export type BootVariant = 'a' | 'b' | 'c';
const MAKERS: Record<BootVariant, [string, (tk: Ticker) => BootScene]> = {
  a: ['Sa bàn', sceneTable],
  b: ['Ấn Ngũ Hành', sceneSeal],
  c: ['Bìa sổ', sceneCover],
};
const KEY = 'pokiclash.boot';

export function bootVariant(q: URLSearchParams): BootVariant {
  const v = (q.get('boot') || localStorage.getItem(KEY) || 'a') as BootVariant;
  return v in MAKERS ? v : 'a';
}

export async function runBoot(first: BootVariant, opts: { switcher?: boolean } = {}): Promise<void> {
  const layer = h('div', { class: 'boot-layer' });
  app.root.append(layer);
  const loading = preload();
  let variant = first;
  let tk: Ticker | null = null;
  let scene: BootScene | null = null;
  let token = 0;
  let canTap = false;
  let resolveTap: () => void = () => {};
  const tapped = new Promise<void>((r) => (resolveTap = r));

  const chips: Record<string, HTMLElement> = {};
  const switcher = h('div', { class: 'bt-switch', onpointerdown: (e: Event) => e.stopPropagation() },
    h('span', { class: 'bt-switch-l' }, 'Ý tưởng'),
    ...(Object.keys(MAKERS) as BootVariant[]).map((v) =>
      (chips[v] = h('button', { class: 'bt-chip', onclick: () => { sfx.click(); void start(v); } }, `${v.toUpperCase()} · ${MAKERS[v][0]}`))),
  );

  async function start(v: BootVariant) {
    const my = ++token;
    variant = v;
    localStorage.setItem(KEY, v);
    for (const [k, c] of Object.entries(chips)) c.classList.toggle('on', k === v);
    canTap = false;
    tk?.stop();
    scene?.el.remove();
    tk = new Ticker();
    scene = MAKERS[v][1](tk);
    layer.prepend(scene.el);
    tk.start();
    const bar = loaderEl();
    scene.bottom.replaceChildren(bar.el);
    const t0 = performance.now();
    const minT = 4300; // cảnh mở dài chừng này: thanh tải không chạy nhanh hơn cảnh
    const upd = window.setInterval(() => bar.set(Math.min(loading.progress(), (performance.now() - t0) / minT)), 60);
    await Promise.all([scene.intro(), loading.done, wait(minT)]);
    clearInterval(upd);
    bar.set(1);
    bar.done();
    if (my !== token) return;
    await wait(250);
    if (my !== token) return;
    scene.showTap();
    canTap = true;
  }

  const stopTicker = () => (tk as Ticker | null)?.stop();
  layer.addEventListener('pointerdown', () => {
    if (!canTap) return;
    canTap = false;
    resolveTap();
  });
  if (opts.switcher !== false) layer.append(switcher);
  void start(variant);
  await tapped;
  switcher.remove();
  const s = scene!;
  if (s.usesClouds) {
    await s.exit();
    sfx.whoosh();
    app.cloudEl.classList.add('cover');
    await wait(420);
    stopTicker();
    layer.remove();
    await wait(60);
    app.cloudEl.classList.remove('cover');
    await wait(380);
  } else {
    await s.exit();
    stopTicker();
    layer.remove();
  }
}
