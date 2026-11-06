// Sảnh: đảo lớn chia 5 vùng hệ, làng máy bi ở giữa. Không khoá vùng nào: vùng nào cũng vào được,
// bảng tên ghi cấp đề nghị và độ khó so với cấp người chơi. Chạm vùng thì sang scene đảo của hệ đó.
import { WORLD_VILLAGE, ZONES, zoneSize, type ZoneDef } from '../../core/data/stages';
import { ELEM_COLOR } from '../../core/elements';
import { app, type Screen } from '../app';
import { clear, h } from '../dom';
import { icon } from '../icons';
import { drawWorldFallback, preloadIcons, sceneBackdrop, SH, SW } from '../scenery';
import { sfx } from '../sfx';
import { intro } from './map';

export function difficulty(z: ZoneDef, level: number, done: boolean): { cls: string; text: string } {
  if (done) return { cls: 'done', text: 'Đã chinh phục' };
  if (level >= z.level[1]) return { cls: 'easy', text: 'Dễ' };
  if (level >= z.level[0]) return { cls: 'fit', text: 'Vừa sức' };
  if (level >= z.level[0] - 3) return { cls: 'hard', text: 'Khó' };
  return { cls: 'wall', text: 'Quá mạnh!' };
}

// vùng nên đánh: vùng chưa xong dễ nhất mà người chơi theo được
export function recommendedZone(level: number, zones: Record<string, number>): ZoneDef {
  return ZONES.find((z) => zones[z.id] < zoneSize(z.id) && level >= z.level[0] - 3) ?? ZONES.find((z) => zones[z.id] < zoneSize(z.id)) ?? ZONES[0];
}

export function worldScreen(): Screen {
  const bg = h('div', { class: 'fill' });
  const sky = h('div', { class: 'world-sky' });
  const over = h('div', { class: 'fill' });
  const bottom = h('div', { class: 'world-bottom' });
  const el = h('div', { class: 'screen' }, bg, sky, over, bottom);
  let bgReady = false;
  let shownIntro = false;

  // mây trôi ngang trên đảo
  for (let i = 0; i < 3; i++)
    sky.append(h('div', {
      class: 'drift',
      style: `top:${130 + i * 250}px;animation-duration:${70 + i * 25}s;animation-delay:-${i * 23}s`,
      html: `<svg width="${200 - i * 30}" height="${80 - i * 10}" viewBox="0 0 200 80"><path d="M20 62c-14 0-16-20-2-24 0-18 22-26 34-14 6-16 34-18 42-2 12-10 34-4 34 12 18-2 26 24 8 28z" fill="#fff" stroke="#2b2118" stroke-width="3" opacity=".9"/></svg>`,
    }));

  async function loadBg() {
    if (bgReady) return;
    await preloadIcons();
    const node = await sceneBackdrop('world', () => drawWorldFallback(app.scale * (window.devicePixelRatio || 1)));
    bg.replaceChildren(node);
    bgReady = true;
  }

  function render() {
    clear(over);
    const s = app.save;
    const reco = recommendedZone(s.level, s.zones);
    for (const z of ZONES) {
      const [fx, fy] = z.world;
      const x = fx * SW, y = fy * SH;
      const done = s.zones[z.id] >= zoneSize(z.id);
      const df = difficulty(z, s.level, done);
      const open = () => {
        sfx.click();
        app.go('zone', { zone: z.id });
      };
      over.append(h('div', { class: 'zhit', style: `left:${x - 95}px;top:${y - 95}px;width:190px;height:190px`, onclick: open }));
      const pw = 200;
      const left = Math.max(8, Math.min(SW - pw - 8, x - pw / 2));
      const plaque = h(
        'div',
        { class: 'zplaque sk', style: `left:${left}px;top:${y + 34}px;width:${pw}px;--fill:#fffaf0;transform:rotate(${(z.order % 2 ? 1 : -1) * 1.5}deg)`, onclick: open },
        h('span', { html: icon('e_' + z.id, 38) }),
        h(
          'div',
          { class: 'col grow', style: 'min-width:0;gap:2px' },
          h('div', { class: 'row gap4', style: 'justify-content:space-between' }, h('div', { class: 'zn', style: 'white-space:nowrap' }, z.name), h('span', { class: `diff ${df.cls}` }, df.text)),
          h('div', { class: 'zl', style: 'white-space:nowrap' }, `Cấp ${z.level[0]}–${z.level[1]} · ${s.zones[z.id]}/${zoneSize(z.id)} ải`),
          h('div', { class: 'zprog', style: `height:8px;border-width:2px;--zc:${ELEM_COLOR[z.id]}` }, h('i', { style: `width:${(s.zones[z.id] / zoneSize(z.id)) * 100}%` })),
        ),
      );
      over.append(plaque);
      if (z === reco) over.append(h('div', { class: 'reco bob', style: `left:${x - 22}px;top:${y - 30}px`, html: icon('down', 44) }));
    }
    // làng máy bi
    const [vx, vy] = WORLD_VILLAGE;
    over.append(
      h(
        'div',
        { class: 'zplaque sk', style: `left:${vx * SW - 74}px;top:${vy * SH + 38}px;width:148px;--fill:#ffe9a0;justify-content:center`, onclick: () => { sfx.click(); app.go('machine'); } },
        h('span', { html: icon('machine', 34) }),
        h('div', { class: 'col' }, h('div', { class: 'zn', style: 'font-size:16px' }, 'Làng Máy Bi'), h('div', { class: 'zl' }, `${s.balls} bi đang có`)),
      ),
    );
    // hàng nút dưới
    clear(bottom);
    const mb = (ic: string, label: string, color: string, go: () => void, dot = 0, big = false) =>
      h(
        'div',
        { class: `mbtn ${big ? 'big' : ''}`, onclick: () => { sfx.click(); go(); } },
        h('div', { class: 'disc sk', style: `--mc:${color}`, html: icon(ic, big ? 64 : 50) }),
        h('div', { class: 'lbl' }, label),
        dot ? h('div', { class: 'dot' }, dot > 99 ? '99+' : dot) : null,
      );
    bottom.append(
      mb('team', 'Tướng', '#c9ecb0', () => app.go('heroes'), app.heroAlerts()),
      mb('cards', 'Sổ thẻ', '#bcd8f5', () => app.go('cards')),
      mb('machine', 'Máy Bi', '#ffe08a', () => app.go('machine'), s.balls, true),
      mb('map', 'Đánh tiếp', '#ffb3a3', () => app.go('zone', { zone: reco.id })),
      mb('pencil', 'Sổ tay', '#e3d2ff', () => app.go('notebook')),
    );
  }

  return {
    el,
    top: 'hud',
    enter() {
      void loadBg();
      render();
      if (!shownIntro && !app.save.intro) {
        shownIntro = true;
        app.afterBoot(() => setTimeout(() => intro(), 500));
      }
    },
  };
}
