// Giấy, mực, nét rung: vân giấy sinh bằng canvas, 3 filter SVG lệch nhau đổi lần lượt để nét "sôi" như hoạt hình vẽ tay.
import rough from 'roughjs';

export function installArt(root: HTMLElement) {
  root.style.setProperty('--grain', `url(${grain()})`);
  root.style.setProperty('--stamp-mask', `url(${stampMask()})`);
  const defs = [0, 1, 2]
    .map(
      (i) => `<filter id="boil${i}" x="-6%" y="-6%" width="112%" height="112%">
        <feTurbulence type="fractalNoise" baseFrequency="0.032" numOctaves="2" seed="${i * 11 + 3}" result="n"/>
        <feDisplacementMap in="SourceGraphic" in2="n" scale="3.4" xChannelSelector="R" yChannelSelector="G"/></filter>`,
    )
    .join('');
  document.body.insertAdjacentHTML(
    'beforeend',
    `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>${defs}
      <filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="5"/><feDisplacementMap in="SourceGraphic" scale="5" xChannelSelector="R" yChannelSelector="G"/></filter>
    </defs></svg>`,
  );
}

let boilTimer = 0;
export function setBoil(root: HTMLElement, on: boolean) {
  clearInterval(boilTimer);
  if (!on) {
    delete root.dataset.boil;
    return;
  }
  let n = 0;
  root.dataset.boil = '0';
  boilTimer = window.setInterval(() => {
    n = (n + 1) % 3;
    root.dataset.boil = String(n);
  }, 160);
}

function grain(): string {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d')!;
  const img = g.createImageData(256, 256);
  for (let i = 0; i < img.data.length; i += 4) {
    const v = Math.random();
    img.data[i] = 120;
    img.data[i + 1] = 95;
    img.data[i + 2] = 60;
    img.data[i + 3] = v < 0.5 ? v * 18 : 0;
  }
  g.putImageData(img, 0, 0);
  // xơ giấy
  g.strokeStyle = 'rgba(140,110,70,0.07)';
  g.lineWidth = 1;
  for (let i = 0; i < 60; i++) {
    const x = Math.random() * 256, y = Math.random() * 256, a = Math.random() * Math.PI;
    g.beginPath();
    g.moveTo(x, y);
    g.quadraticCurveTo(x + Math.cos(a) * 8 + 3, y + Math.sin(a) * 8 - 3, x + Math.cos(a) * 16, y + Math.sin(a) * 16);
    g.stroke();
  }
  return c.toDataURL();
}

function stampMask(): string {
  const c = document.createElement('canvas');
  c.width = c.height = 200;
  const g = c.getContext('2d')!;
  g.fillStyle = '#000';
  g.fillRect(0, 0, 200, 200);
  g.globalCompositeOperation = 'destination-out';
  for (let i = 0; i < 900; i++) {
    g.fillStyle = `rgba(0,0,0,${Math.random() * 0.7})`;
    const r = Math.random() * 2.6;
    g.beginPath();
    g.arc(Math.random() * 200, Math.random() * 200, r, 0, Math.PI * 2);
    g.fill();
  }
  return c.toDataURL();
}

// ---------- vẽ nguệch ngoạc lên canvas bằng roughjs ----------
export type RoughCanvas = ReturnType<typeof rough.canvas>;
export function roughOf(c: HTMLCanvasElement): RoughCanvas {
  return rough.canvas(c);
}

export const INK = '#2b2118';

// mây bông kiểu bút sáp
export function cloud(rc: RoughCanvas, x: number, y: number, s: number, seed: number) {
  const pts: [number, number][] = [];
  const bumps = 7;
  for (let i = 0; i <= bumps; i++) {
    const a = Math.PI + (i / bumps) * Math.PI;
    pts.push([x + Math.cos(a) * 60 * s, y + Math.sin(a) * 26 * s - (i % 2 ? 10 * s : 0)]);
  }
  rc.curve([...pts, [x + 60 * s, y + 8 * s], [x - 60 * s, y + 8 * s], pts[0]], {
    stroke: INK, strokeWidth: 2.2, fill: '#ffffff', fillStyle: 'solid', roughness: 1.4, seed,
  });
}

export function hill(rc: RoughCanvas, w: number, y: number, amp: number, color: string, seed: number, h: number) {
  const pts: [number, number][] = [];
  for (let x = -20; x <= w + 20; x += 40) pts.push([x, y + Math.sin(x / 90 + seed) * amp + Math.sin(x / 37 + seed * 2) * amp * 0.3]);
  rc.polygon([...pts, [w + 20, h + 20], [-20, h + 20]], {
    stroke: INK, strokeWidth: 2.4, fill: color, fillStyle: 'hachure', hachureGap: 7, fillWeight: 2.2, hachureAngle: -50, roughness: 1.3, seed,
  });
}

export function tuft(rc: RoughCanvas, x: number, y: number, seed: number, color = '#3f8f33') {
  for (let i = -2; i <= 2; i++)
    rc.line(x + i * 4, y, x + i * 7, y - 12 - Math.abs(i) * -2, { stroke: color, strokeWidth: 2, roughness: 1.2, seed: seed + i });
}
