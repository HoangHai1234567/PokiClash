// Hiệu ứng của bộ UI Sa Bàn: nhấn lún rồi nảy (punch), nét mực bung quanh chỗ chạm, hiện ra (spawn), chia bài (deal), đếm số,
// lắc khi lỗi. Đứng tại chỗ (idle) và thở (breath) là animation CSS (kit.css); punch chạy trên phần tử con để không giẫm lên
// transform của idle/breath ở phần tử bọc ngoài.
import { sfx } from '../view/sfx';

const OUT = 'cubic-bezier(.2,.8,.2,1)';
const BACK = 'cubic-bezier(.34,1.56,.64,1)';

export function punch(el: Element, k = 1) {
  el.animate(
    [
      { transform: 'scale(1)' },
      { transform: `scale(${1 - 0.1 * k}) rotate(-1.5deg)`, offset: 0.25 },
      { transform: `scale(${1 + 0.12 * k}) rotate(1deg)`, offset: 0.6 },
      { transform: `scale(${1 - 0.03 * k})`, offset: 0.82 },
      { transform: 'scale(1)' },
    ],
    { duration: 360, easing: 'ease-out' },
  );
}

// gắn nhấn: lún khi đè, nảy + nét bung khi thả; root là nơi vẽ nét bung (toạ độ trong khung điện thoại)
export function pressable(el: HTMLElement, onTap?: (e: PointerEvent) => void, opts: { burst?: boolean; sound?: () => void } = {}) {
  let down: Animation | null = null;
  el.addEventListener('pointerdown', () => {
    down = el.animate([{ transform: 'scale(1)' }, { transform: 'scale(0.9) rotate(-1deg)' }], { duration: 90, easing: OUT, fill: 'forwards' });
  });
  const release = () => {
    down?.cancel();
    down = null;
  };
  el.addEventListener('pointerleave', release);
  el.addEventListener('pointercancel', release);
  el.addEventListener('pointerup', (e) => {
    release();
    punch(el);
    if (opts.burst !== false) burst(el, e);
    (opts.sound ?? sfx.click)();
    onTap?.(e);
  });
}

// 5 gạch mực ngắn toả ra từ chỗ chạm rồi tan
export function burst(el: HTMLElement, e: PointerEvent) {
  const phone = el.closest('#phone') as HTMLElement | null;
  if (!phone) return;
  const r = phone.getBoundingClientRect();
  const s = r.width / 540;
  const x = (e.clientX - r.left) / s, y = (e.clientY - r.top) / s;
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('class', 'k-burst');
  svg.setAttribute('width', '120');
  svg.setAttribute('height', '120');
  svg.setAttribute('viewBox', '-60 -60 120 120');
  svg.style.left = `${x - 60}px`;
  svg.style.top = `${y - 60}px`;
  const n = 5, a0 = Math.random() * Math.PI;
  for (let i = 0; i < n; i++) {
    const a = a0 + (i / n) * Math.PI * 2;
    const p = document.createElementNS(ns, 'path');
    p.setAttribute('d', `M${Math.cos(a) * 20},${Math.sin(a) * 20} L${Math.cos(a) * 34},${Math.sin(a) * 34}`);
    svg.appendChild(p);
  }
  phone.appendChild(svg);
  svg.animate(
    [
      { transform: 'scale(.5)', opacity: 1 },
      { transform: 'scale(1.25)', opacity: 0 },
    ],
    { duration: 380, easing: OUT },
  ).finished.then(() => svg.remove());
}

// hiện ra: nảy từ nhỏ, hơi xoay, rồi đứng yên (fill backwards: trước giờ hiện thì ẩn)
export function spawn(el: Element, delay = 0, from: 'pop' | 'drop' | 'up' = 'pop') {
  const start =
    from === 'drop' ? 'translateY(-60px) rotate(-6deg) scale(1.1)' : from === 'up' ? 'translateY(70px) rotate(4deg) scale(.9)' : 'scale(.5) rotate(-8deg)';
  return el.animate(
    [
      { opacity: 0, transform: start },
      { opacity: 1, transform: 'scale(1.07) rotate(2deg)', offset: 0.65 },
      { opacity: 1, transform: 'none' },
    ],
    { duration: 440, delay, easing: OUT, fill: 'backwards' },
  );
}

// chia bài: bay từ chồng bài (dưới giữa màn) tới chỗ, xoay nhẹ, lật mặt
export function deal(el: HTMLElement, delay = 0, fromX = 0, fromY = 320) {
  return el.animate(
    [
      { opacity: 0, transform: `translate(${fromX}px, ${fromY}px) rotate(-24deg) scale(.55) rotateY(80deg)` },
      { opacity: 1, transform: 'translate(0, -14px) rotate(3deg) scale(1.06) rotateY(0deg)', offset: 0.7 },
      { opacity: 1, transform: 'none' },
    ],
    { duration: 520, delay, easing: OUT, fill: 'backwards' },
  );
}

// bay đi (thẻ đã dùng, quà vào túi): tới đích rồi thu nhỏ biến mất
export function flyTo(el: HTMLElement, dx: number, dy: number, dur = 420) {
  return el.animate(
    [
      { transform: 'none', opacity: 1 },
      { transform: `translate(${dx * 0.4}px, ${dy * 0.4 - 30}px) rotate(-8deg) scale(1.08)`, opacity: 1, offset: 0.4 },
      { transform: `translate(${dx}px, ${dy}px) rotate(6deg) scale(.35)`, opacity: 0 },
    ],
    { duration: dur, easing: 'cubic-bezier(.5,0,.75,0)', fill: 'forwards' },
  ).finished;
}

// lắc ngang (bấm khi chưa đủ điều kiện)
export function shake(el: Element) {
  el.animate(
    [{ transform: 'translateX(0)' }, { transform: 'translateX(-7px)' }, { transform: 'translateX(6px)' }, { transform: 'translateX(-4px)' }, { transform: 'translateX(0)' }],
    { duration: 300 },
  );
  sfx.error();
}

// đếm số lên/xuống rồi nảy
export function countTo(el: HTMLElement, from: number, to: number, dur = 600) {
  const t0 = performance.now();
  const fmt = (v: number) => Math.round(v).toLocaleString('vi-VN');
  const step = (now: number) => {
    const k = Math.min(1, (now - t0) / dur);
    el.textContent = fmt(from + (to - from) * (1 - Math.pow(1 - k, 3)));
    if (k < 1) requestAnimationFrame(step);
    else punch(el, 0.8);
  };
  requestAnimationFrame(step);
}

// chữ "+12" bay lên rồi tan (thưởng, sát thương)
export function floatText(host: HTMLElement, text: string, x: number, y: number, color = '#fff') {
  const t = document.createElement('div');
  t.textContent = text;
  t.className = 'k-stk';
  t.style.cssText = `position:absolute;left:${x}px;top:${y}px;transform:translate(-50%,-50%);font:800 30px 'Baloo 2';color:${color};pointer-events:none;z-index:55`;
  host.appendChild(t);
  t.animate(
    [
      { transform: 'translate(-50%,-50%) scale(.4)', opacity: 0 },
      { transform: 'translate(-50%,-80%) scale(1.15)', opacity: 1, offset: 0.25 },
      { transform: 'translate(-50%,-160%) scale(1)', opacity: 0 },
    ],
    { duration: 900, easing: OUT },
  ).finished.then(() => t.remove());
}

export const ease = { OUT, BACK };

// pha ngẫu nhiên cho idle/breath để các phần tử không nhún đồng loạt
export function phase(el: HTMLElement, base = 3.2, spread = 0.8) {
  el.style.setProperty('--dur', `${(base + (Math.random() - 0.5) * spread).toFixed(2)}s`);
  el.style.setProperty('--ph', `${(-Math.random() * base).toFixed(2)}s`);
  return el;
}
