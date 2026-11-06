// Trang trưng bày bộ UI Sa Bàn (http://localhost:5180/uikit.html): khung điện thoại 540 × 960 co theo màn,
// thanh chọn trang trên cùng: Thành phần, Sảnh, Tướng, Trận. ?p=parts|hub|heroes|battle để mở thẳng một trang.
import '@fontsource/baloo-2/700.css';
import '@fontsource/baloo-2/800.css';
import '@fontsource/pangolin/400.css';
import './kit.css';
import { h } from '../view/dom';
import { woodTexture } from '../view/boot/common';
import { kit } from './parts';
import { pageBattle, pageHeroes, pageHub, pageParts } from './pages';

const phone = document.getElementById('phone')!;
phone.style.backgroundImage = `url(${woodTexture()})`;

function fit() {
  const W = window.innerWidth, H = window.innerHeight;
  const s = Math.min(W / 546, H / 966);
  kit.scale = s;
  phone.style.transform = `scale(${s})`;
  phone.style.left = `${(W - 540 * s) / 2}px`;
  phone.style.top = `${(H - 960 * s) / 2}px`;
}
window.addEventListener('resize', fit);
fit();

const PAGES: Record<string, [string, (p: HTMLElement) => HTMLElement]> = {
  parts: ['Thành phần', pageParts],
  hub: ['Sảnh', pageHub],
  heroes: ['Tướng', pageHeroes],
  battle: ['Trận', pageBattle],
};
const stage = h('div', { class: 'k-fill' });
const btns: Record<string, HTMLElement> = {};
const sw = h('div', { class: 'k-switch' },
  ...Object.entries(PAGES).map(([k, [name]]) => (btns[k] = h('button', { onclick: () => show(k) }, name))));
phone.append(stage, sw);

function show(k: string) {
  if (!(k in PAGES)) k = 'parts';
  for (const [n, b] of Object.entries(btns)) b.classList.toggle('on', n === k);
  // gỡ hộp thoại, giấy nhớ, nét bung còn sót của trang trước
  phone.querySelectorAll('.k-modal,.k-toast,.k-burst').forEach((e) => e.remove());
  stage.replaceChildren(PAGES[k][1](phone));
  history.replaceState(null, '', `?p=${k}`);
}
show(new URLSearchParams(location.search).get('p') ?? 'parts');
