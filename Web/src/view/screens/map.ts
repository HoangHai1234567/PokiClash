// Hộp AFK (cây bi, mảnh tướng, rương AFK) và màn giới thiệu lần đầu (bản đồ ải nay là scene đảo: world.ts, zone.ts).
// Unity để cây bi thành công trình riêng trên sảnh; bản web gộp vào hộp này cho gọn.
import { HERO } from '../../core/data/heroes';
import {
  AFK, afkBoost, afkBoosting, afkChestTimes, afkPending, afkSlots, claimAfk, localDay, openAfkChest,
} from '../../core/afk';
import { TREES } from '../../core/data/trees';
import { treeCap, treeRate, treesHarvest, treesOf, treesOpen, treesStock } from '../../core/trees';
import { AFK_CAP_H, totalCleared } from '../../core/progression';
import { adLeft, adUse } from '../../core/ads';
import { Rng, randomSeed } from '../../core/rng';
import { app } from '../app';
import { clear, h, wait } from '../dom';
import { icon } from '../icons';
import { sfx } from '../sfx';

// ---------- AFK ----------
const tz = () => -new Date().getTimezoneOffset();
const hm = (ms: number) => {
  const m = Math.max(0, Math.ceil(ms / 60000));
  return m >= 60 ? `${Math.floor(m / 60)} giờ ${m % 60} phút` : `${m} phút`;
};

export function openAfk() {
  const s = app.save;
  const body = h('div', { class: 'col center gap12', style: 'text-align:center' });
  const m = app.modal(body, { width: 460 });
  function draw() {
    clear(body);
    body.append(h('span', { html: icon('clock', 64) }), h('h2', null, 'Đội tự đi ải'));
    if (!totalCleared(s)) {
      body.append(h('div', null, 'Qua ải 1 để mở. Cây bi ra bi và đội tự đánh các ải đã qua, cả khi bạn tắt game.'));
      return;
    }
    const now = Date.now();
    const day = localDay(now, tz());
    const p = afkPending(s, now);
    const a = s.afk;
    // cây bi
    const stock = treesStock(s, now), cap = treeCap(s, now);
    const trees = h('div', { class: 'row gap8' });
    treesOf(s, now).stock.forEach((x) =>
      trees.append(h('div', { class: 'col center', style: 'gap:2px' }, h('span', { html: icon('ball', 34), class: x >= cap ? 'wob' : '' }), h('div', { class: 'small', style: 'font-weight:bold' }, `${Math.floor(x)}/${cap}`))),
    );
    const tleft = adLeft(s, day, 'tree_double');
    body.append(
      h('h3', null, `Cây bi (${treesOpen(s)}/${TREES.unlockZones.length + 1})`),
      h('div', { class: 'small muted' }, `Mỗi cây ${treeRate(s, now)} bi/giờ, chứa tối đa ${cap}; đầy thì ngừng. Cây mới mở khi qua boss các đảo.`),
      trees,
      h('div', { class: 'row gap8' },
        h('button', { class: `btn green ${stock ? '' : 'off'}`, onclick: () => stock && harvest(1) }, `Hái +${stock}`),
        h('button', { class: `btn purple ${stock && tleft ? '' : 'off'}`, onclick: () => stock && tleft && void fakeAd().then((ok) => ok && adUse(s, day, 'tree_double') && harvest(2)) },
          h('span', { html: icon('tv', 26) }), tleft ? `Hái ×2 (${tleft})` : 'Hết lượt hôm nay')),
      h('h3', null, `Đội tự đánh ${totalCleared(s)} ải đã qua`),
      h('div', { class: 'bar exp', style: 'width:100%;height:20px' }, h('i', { style: `width:${(p.hours / AFK_CAP_H) * 100}%` }), h('b', null, `${p.hours.toFixed(1)} / ${AFK_CAP_H} giờ`)),
      h('div', { class: 'small muted' }, `Mỗi giờ có ${AFK.shardChance * 100}% cơ hội nhặt mảnh tướng boss đã gặp; giữ tối đa ${AFK_CAP_H} giờ.`),
    );
    // khay rương AFK
    const times = afkChestTimes(s, now);
    const tray = h('div', { class: 'row gap8' });
    for (let i = 0; i < afkSlots(s, now); i++) {
      const t = times[i];
      if (!t) {
        tray.append(h('div', { class: 'sk thin center', style: 'width:84px;height:96px;--fill:#f3e7c9;opacity:.6' }));
        continue;
      }
      const ready = t.ready <= now;
      const cell = h(
        'div',
        { class: 'sk thin col center', style: `width:84px;height:96px;--fill:#fff;--chest:#8fd3c8;gap:0;cursor:${ready ? 'pointer' : 'default'}` },
        h('span', { html: icon('chest', 48), class: ready ? 'wob' : '' }),
        h('div', { class: 'small', style: 'font-weight:bold' }, ready ? 'Mở được' : t.start <= now ? hm(t.ready - now) : 'Chờ'),
      );
      if (ready) cell.onclick = () => openChestNow(false);
      tray.append(cell);
    }
    body.append(h('h3', null, 'Rương AFK'), tray);
    body.append(h('div', { class: 'small muted' }, a.chests.length >= afkSlots(s, now) ? 'Khay đầy, mở bớt rương' : `Rương tiếp: ${a.chestAcc.toFixed(1)} / ${AFK.chestEveryH} giờ AFK`));
    const row2 = h('div', { class: 'row gap8' });
    if (times[0] && times[0].ready > now) {
      const left = adLeft(s, day, 'afk_chest_open');
      row2.append(
        h('button', { class: `btn small purple ${left ? '' : 'off'}`, onclick: () => left && void fakeAd().then((ok) => ok && adUse(s, day, 'afk_chest_open') && openChestNow(true)) },
          h('span', { html: icon('tv', 22) }), `Mở ngay (${left})`),
      );
    }
    if (afkBoosting(s, now)) row2.append(h('div', { class: 'small', style: 'font-weight:bold' }, `Tăng tốc ×2: còn ${hm(a.boostUntil - now)}`));
    else {
      const left = p.full ? 0 : adLeft(s, day, 'afk_boost'); // đầy giờ thì AFK dừng: nhận trước rồi mới tăng tốc
      row2.append(
        h('button', {
          class: `btn small orange ${left ? '' : 'off'}`,
          onclick: () => left && void fakeAd().then((ok) => {
            if (ok && adUse(s, day, 'afk_boost') && afkBoost(s, Date.now())) {
              app.persist();
              draw();
            }
          }),
        }, h('span', { html: icon('tv', 22) }), `Tăng tốc ×2 (${left})`),
      );
    }
    body.append(row2);
    body.append(
      h(
        'div',
        { class: 'row gap8' },
        h('button', { class: `btn green ${p.hours >= 1 ? '' : 'off'}`, onclick: () => claim() }, 'Nhận mảnh'),
      ),
      h('div', { class: 'small muted' }, 'Nút có hình TV giả lập xem quảng cáo (bản thử không có quảng cáo thật).'),
    );
  }
  function claim() {
    const r = claimAfk(s, Date.now(), 1, new Rng(randomSeed()));
    app.persist();
    app.toast(r.shards.length ? `Nhặt ${r.shards.reduce((a, x) => a + x.n, 0)} mảnh tướng` : 'Lần này chưa nhặt được mảnh tướng', 'star');
    for (const sh of r.shards) if (sh.unlocked) app.toast(`Mở khóa ${HERO[sh.hero].name}!`, 'star');
    draw();
  }
  function harvest(mult: number) {
    const n = treesHarvest(s, Date.now(), mult);
    app.persist();
    sfx.coin();
    app.toast(`Hái ${n} bi`, 'ball');
    draw();
  }
  function openChestNow(early: boolean) {
    const lv = s.level;
    const rs = openAfkChest(s, Date.now(), new Rng(randomSeed()), early);
    if (!rs) return;
    app.persist();
    sfx.chest();
    for (const r of rs)
      app.toast(
        r.k === 'exp' ? `Rương AFK: +${r.n} XP` : r.k === 'balls' ? `Rương AFK: +${r.n} bi` : r.k === 'card' ? `Rương AFK: thẻ của ${HERO[r.drop.hero].name}` : r.k === 'stones' ? `Rương AFK: +${r.n} đá tiềm năng` : 'Rương AFK',
        r.k === 'card' ? 'cards' : r.k === 'exp' ? 'exp' : 'ball',
      );
    if (s.level > lv) app.levelUp(lv, s.level);
    draw();
  }
  // quảng cáo giả lập 3 giây; "Bỏ qua" thì không nhận thưởng
  function fakeAd(): Promise<boolean> {
    return new Promise((done) => {
      let ok = false, cancelled = false;
      const n = h('div', { class: 'title', style: 'font-size:40px' }, '3');
      const box = h('div', { class: 'col center gap12', style: 'text-align:center' }, h('span', { html: icon('tv', 80) }), h('h2', null, 'Quảng cáo giả lập'), n);
      const ad = app.modal(box, { closable: false, width: 360, onClose: () => done(ok) });
      box.append(h('button', { class: 'btn small paper', onclick: () => { cancelled = true; ad.close(); } }, 'Bỏ qua'));
      void (async () => {
        for (let i = 3; i > 0 && !cancelled; i--) {
          n.textContent = String(i);
          await wait(1000);
        }
        if (!cancelled) {
          ok = true;
          ad.close();
        }
      })();
    });
  }
  draw();
}

// ---------- giới thiệu lần đầu ----------
export function intro() {
  const s = app.save;
  const panel = (ic: string, title: string, text: string, rot: number) =>
    h('div', { class: 'row gap12 sk thin', style: `padding:10px 12px;--fill:#fff;transform:rotate(${rot}deg);text-align:left` }, h('span', { html: icon(ic, 56) }), h('div', { class: 'col' }, h('div', { class: 'title', style: 'font-size:19px' }, title), h('div', { style: 'font-size:15px;line-height:1.15' }, text)));
  const body = h(
    'div',
    { class: 'col gap12' },
    h('h1', { style: 'text-align:center' }, 'Sổ Tay Phiêu Lưu'),
    h('div', { class: 'muted', style: 'text-align:center;margin-top:-6px' }, 'Bản thử PokiClash: đánh ải, thả bi, nuôi tướng'),
    panel('map', '1. Năm đảo, năm hệ', 'Đảo nào cũng vào được, nhưng đảo sau mạnh hơn hẳn. Bạn có Giọt Sương hệ Thủy: bắt đầu ở Đảo Thủy, qua ải sẽ có thêm tướng.', 1),
    panel('cards', '2. Đánh bằng thẻ', 'Mỗi lượt chọn 5 lần, mỗi lần 1 trong 3 thẻ. Xen Chiêu và Tuyệt kỹ vào hàng thẻ. Thẻ chạy xong thì tướng đánh.', -1),
    panel('ball', '3. Thắng thì nhận bi', 'Ải đã qua còn tự đánh khi bạn vắng (AFK). Boss rơi mảnh tướng mới.', 0.8),
    panel('machine', '4. Thả bi vào máy', 'Bi ra kinh nghiệm (cấp người chơi = cấp tướng), rương thẻ để nâng chiêu và tiến hóa sao.', -0.6),
    h('div', { class: 'center' }, h('button', { class: 'btn red big', onclick: () => { s.intro = true; app.persist(); m.close(); } }, 'Bắt đầu!')),
  );
  const m = app.modal(body, { width: 470, closable: false });
}
