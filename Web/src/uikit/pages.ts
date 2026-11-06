// Các trang trưng bày bộ UI Sa Bàn: Thành phần (mọi thành phần, bấm thử được), và 3 màn mẫu: Sảnh, Tướng, Trận.
// Ảnh đảo và nền trận lấy từ Unity (Assets/03 Art qua /unity/), giữ nguyên.
import { POOL } from '../core/data/cards';
import { HERO } from '../core/data/heroes';
import { ELEM_COLOR } from '../core/elements';
import type { Elem } from '../core/types';
import { ATTACK, HIT } from '../view/aola';
import { h } from '../view/dom';
import { icon } from '../view/icons';
import { sfx } from '../view/sfx';
import { deal, flyTo, floatText, phase, pressable, punch, shake, spawn } from './fx';
import {
  bar, button, card, chip, dialog, head, heroTile, HeroPuppet, lvRing, panel, rarity, round, stars, tabs, tag, toast, toggle, topbar,
} from './parts';

const UNITY = '/unity/';
const pick = (ids: string[]) => ids.map((id) => POOL.find((c) => c.id === id)!).filter(Boolean);

// hiện các mục khi cuộn tới (mỗi mục một lần)
function revealOnScroll(root: HTMLElement) {
  const io = new IntersectionObserver((es) => {
    for (const e of es) {
      if (!e.isIntersecting) continue;
      io.unobserve(e.target);
      [...(e.target as HTMLElement).querySelectorAll<HTMLElement>('[data-sp]')].forEach((el, i) => spawn(el, i * 70, (el.dataset.sp as 'pop' | 'up') || 'pop'));
    }
  }, { root, threshold: 0.15 });
  root.querySelectorAll('.k-sec').forEach((s) => io.observe(s));
}

const sp = <T extends HTMLElement>(el: T, how: 'pop' | 'up' = 'pop') => {
  el.dataset.sp = how;
  return el;
};

function sec(title: string, color: '' | 'p' | 'b' | 'g', note: string, ...kids: HTMLElement[]) {
  return h('section', { class: 'k-sec' }, head(title, color), ...kids, note ? h('div', { class: 'k-note' }, note) : null);
}

// ---------- Thành phần ----------
export function pageParts(phone: HTMLElement) {
  const el = h('div', { class: 'k-fill' });
  const page = h('div', { class: 'k-page' });
  const scroll = h('div', { class: 'k-scroll' });
  page.appendChild(scroll);
  const tb = topbar('Bộ UI');
  el.append(tb.el, page);

  // nút
  const dlg = () => levelDialog(phone);
  scroll.append(sec('Nút', '', 'Nhấn: lún rồi nảy, nét mực bung quanh ngón tay. Nút chính thở nhẹ để mời bấm.',
    sp(h('div', { class: 'row gap12 wrap' }, button('Xuất trận!', { color: 'red', size: 'big', breath: true, onTap: dlg }))),
    sp(h('div', { class: 'row gap8 wrap', style: 'margin-top:12px' },
      button('Nhận', { color: 'green' }), button('Đổi đội', { color: 'blue' }), button('Nâng', { color: 'yellow', cost: '×3' }))),
    sp(h('div', { class: 'row gap8 wrap', style: 'margin-top:12px' },
      button('Huỷ', { color: 'paper' }), button('Tiến hoá', { color: 'purple', size: 'small' }), button('Khoá', { color: 'orange', size: 'small', disabled: true }), button('Xem', { color: 'paper', size: 'tiny' }))),
    sp(h('div', { class: 'row gap12 wrap', style: 'margin-top:14px;align-items:flex-start' },
      round('back'), round('gear'), round('close', { color: '#ffd6cc' }), round('play', { color: '#c9ecb0' }), round('chest', { color: '#ffe08a', dot: 3 }))),
  ));

  // tài nguyên
  const balls = chip('ball', 186);
  const shards = chip('shard', 7);
  const plus = button('+12 bi', { color: 'green', size: 'small', onTap: () => {
    balls.set(Number(balls.el.textContent?.replace(/\D/g, '') || 186) + 12);
    const r = balls.el.getBoundingClientRect(), pr = phone.getBoundingClientRect(), s = pr.width / 540;
    floatText(phone, '+12', (r.left + r.width / 2 - pr.left) / s, (r.top - pr.top) / s, '#ff8fb3');
  } });
  scroll.append(sec('Tài nguyên', 'b', 'Số đổi thì đếm chạy rồi nảy; chữ thưởng bay lên.',
    sp(h('div', { class: 'row gap16 wrap', style: 'padding-left:12px' }, lvRing(15, 0.62), balls.el, shards.el)),
    sp(h('div', { style: 'margin-top:12px' }, plus))));

  // thanh
  const hp = bar('', 640, 827);
  const mana = bar('blue', 18, 25);
  const rage = bar('orange', 60, 100);
  const xp = bar('purple', 532, 675);
  const hit = button('−120', { color: 'red', size: 'tiny', onTap: () => hp.set(Math.max(0, hp.value - 120)) });
  const heal = button('+80', { color: 'green', size: 'tiny', onTap: () => hp.set(Math.min(827, hp.value + 80)) });
  scroll.append(sec('Thanh', 'p', 'Vạch sáp chạy chậm cho thanh "sống"; mất máu thì vệt vàng lùi theo sau.',
    sp(h('div', { class: 'col gap8', style: 'width:380px' },
      h('div', { class: 'row gap8' }, h('span', { html: icon('heart', 26) }), h('div', { class: 'grow' }, hp.el)),
      h('div', { class: 'row gap8' }, h('span', { html: icon('drop', 26) }), h('div', { class: 'grow' }, mana.el)),
      h('div', { class: 'row gap8' }, h('span', { html: icon('rage', 26) }), h('div', { class: 'grow' }, rage.el)),
      h('div', { class: 'row gap8' }, h('span', { html: icon('exp', 26) }), h('div', { class: 'grow' }, xp.el)))),
    sp(h('div', { class: 'row gap8', style: 'margin-top:10px' }, hit, heal))));

  // nhãn
  scroll.append(sec('Nhãn', 'g', '',
    sp(h('div', { class: 'row gap6 wrap' }, ...(['thuy', 'hoa', 'kim', 'moc', 'tho'] as Elem[]).map(tag))),
    sp(h('div', { class: 'row gap12 wrap', style: 'margin-top:10px' }, rarity('common'), rarity('uncommon'), rarity('rare'), rarity('epic'), rarity('legend'))),
    sp(h('div', { style: 'margin-top:8px' }, stars(3, 5, 30)))));

  // khung giấy
  const panels = () => h('div', { class: 'col gap16' },
    sp(panel([h('div', { class: 'k-title', style: 'font-size:20px' }, 'Giấy có chỉ khâu'), h('div', { style: 'font-size:16px;margin-top:4px' }, 'Viền mực, đường chỉ khâu đứt nét bên trong, băng keo giữ hai góc.')], { tapes: ['y', 'b'] })),
    sp(panel([h('div', { class: 'k-title', style: 'font-size:20px' }, 'Giấy kraft'), h('div', { style: 'font-size:16px;margin-top:4px' }, 'Cho ô phụ, gợi ý, nền bảng thưởng.')], { kraft: true, tapes: ['p'] })));
  let pbox = panels();
  const again = button('Hiện lại', { color: 'paper', size: 'small', onTap: () => {
    const n = panels();
    pbox.replaceWith(n);
    pbox = n;
    [...n.querySelectorAll<HTMLElement>('[data-sp]')].forEach((e, i) => spawn(e, i * 90, 'drop'));
  } });
  scroll.append(sec('Khung giấy', '', '', pbox, sp(h('div', { style: 'margin-top:12px' }, again))));

  // thẻ bài
  const hand = h('div', { class: 'row gap12', style: 'height:210px;align-items:flex-end;padding-bottom:6px' });
  const dealHand = () => {
    hand.replaceChildren();
    pick(['mai_vuot', 'giap_go', 'bang_gac']).forEach((c, i) => {
      const cd = card(c);
      cd.el.addEventListener('click', () => {
        const on = !cd.el.classList.contains('sel');
        hand.querySelectorAll('.k-cardw').forEach((x) => x.classList.remove('sel'));
        cd.el.classList.toggle('sel', on);
      });
      pressable(cd.inner, undefined, { burst: false, sound: sfx.pick });
      hand.appendChild(cd.el);
      deal(cd.el, i * 110, (1 - i) * 140, 260);
      setTimeout(() => sfx.deal(), i * 110);
    });
  };
  dealHand();
  scroll.append(sec('Thẻ bài', 'b', 'Chia ra rồi đứng nhún tại chỗ, mỗi lá một nhịp. Chạm để chọn: thẻ nhấc lên, có dấu tích.',
    hand, sp(h('div', { style: 'margin-top:6px' }, button('Chia lại', { color: 'blue', size: 'small', onTap: dealHand })))));

  // ô tướng
  scroll.append(sec('Ô tướng', 'p', 'Chạm tướng chưa có: ô lắc. Chấm "!" lắc lư khi có việc chờ.',
    sp(h('div', { class: 'row gap12', style: 'align-items:flex-start;margin-left:-8px' },
      heroTile('giot_suong', { star: 2, power: 1421, dot: true, onTap: () => heroDialog(phone, 'giot_suong') }),
      heroTile('huyen_vu', { locked: true }))),
  ));

  // công tắc, tab
  scroll.append(sec('Công tắc và tab', 'g', '',
    sp(h('div', { class: 'row gap16' }, h('span', { style: 'font-size:18px;width:120px' }, 'Âm thanh'), toggle(true))),
    sp(h('div', { class: 'row gap16', style: 'margin-top:10px' }, h('span', { style: 'font-size:18px;width:120px' }, 'Rung'), toggle(false))),
    sp(h('div', { style: 'margin-top:16px' }, tabs(['Đội hình', 'Thẻ', 'Mảnh', 'Huy hiệu'], 0)))));

  // hộp thoại, thông báo
  scroll.append(sec('Hộp thoại và giấy nhớ', '', 'Hộp mở nảy ra, con dấu đóng xuống, sao hiện lần lượt. Giấy nhớ trượt xuống rồi tự đi.',
    sp(h('div', { class: 'row gap8 wrap' },
      button('Lên cấp', { color: 'purple', onTap: dlg }),
      button('Giấy nhớ', { color: 'yellow', onTap: () => toast(phone, 'Đội tự đi ải mang về 12 bi!') }))),
  ));

  revealOnScroll(scroll);
  return el;
}

function levelDialog(phone: HTMLElement) {
  const stamp = h('div', { class: 'k-stamp' }, 'LÊN CẤP!');
  const lvTxt = h('div', { class: 'k-title k-stk', style: 'font-size:64px;line-height:1;margin-top:14px' }, 'Cấp 16');
  const ok = button('Tuyệt!', { color: 'green', breath: true, onTap: () => d.close() });
  const body = h('div', { class: 'col', style: 'align-items:center;text-align:center;gap:8px' },
    stamp, lvTxt,
    h('div', { style: 'font-size:18px' }, 'Mọi tướng mạnh thêm. Cấp người chơi cũng là cấp của tướng.'),
    stars(3, 3, 40), h('div', { style: 'margin-top:8px' }, ok));
  const d = dialog(phone, 'Phần thưởng', body, { headColor: 'p' });
  stamp.animate([
    { transform: 'rotate(-30deg) scale(2.6)', opacity: 0 },
    { transform: 'rotate(-6deg) scale(.92)', opacity: 1, offset: 0.75 },
    { transform: 'rotate(-8deg) scale(1)', opacity: 1 },
  ], { duration: 320, delay: 260, easing: 'ease-in', fill: 'backwards' });
  setTimeout(() => sfx.stamp(), 520);
  spawn(lvTxt, 520);
}

function heroDialog(phone: HTMLElement, id: string) {
  const hd = HERO[id];
  const pup = new HeroPuppet(hd.forms[0].aola, 240, 220);
  const body = h('div', { class: 'col', style: 'align-items:center;gap:6px' },
    h('div', { class: 'row gap8' }, tag(hd.elem), h('span', { class: 'k-title', style: 'font-size:26px' }, hd.name)),
    stars(2, 5, 26),
    h('div', { style: `position:relative;width:240px;height:220px;border:3px dashed ${ELEM_COLOR[hd.elem]};border-radius:50% 50% 14px 14px` }, pup.el),
    h('div', { class: 'row gap8', style: 'margin-top:4px' },
      button('Đánh', { color: 'paper', size: 'tiny', onTap: () => pup.play(ATTACK) }),
      button('Trúng', { color: 'paper', size: 'tiny', onTap: () => pup.play(HIT) })),
    h('div', { class: 'row gap8', style: 'margin-top:10px' }, button('Tiềm năng', { color: 'blue', size: 'small' }), button('Tiến hoá', { color: 'purple', size: 'small', breath: true })));
  dialog(phone, 'Tướng', body, { headColor: 'b' });
}

// ---------- màn mẫu: Sảnh (đảo giữ nguyên) ----------
export function pageHub(phone: HTMLElement) {
  const el = h('div', { class: 'k-fill', style: 'background:#8fd0ea' });
  const map = h('img', { src: `${UNITY}Islands/world.png`, style: 'position:absolute;left:50%;top:60px;width:560px;transform:translateX(-50%);pointer-events:none' });
  el.appendChild(map);
  // bảng tên vùng: giấy ghim, nhún nhẹ
  const zone = (name: string, e: Elem, lvl: string, x: number, y: number, hint: string, hintC: string) => {
    const t = h('div', { class: 'k-panel', style: 'padding:8px 12px 8px 10px;display:flex;align-items:center;gap:8px;border-radius:12px 6px 14px 6px' },
      h('span', { html: icon(`e_${e}`, 30) }),
      h('div', { class: 'col' }, h('b', { class: 'k-title', style: 'font-size:18px;line-height:1' }, name), h('span', { style: 'font-size:13px;color:#5a4636' }, lvl)),
      h('span', { class: 'k-tag', style: `--c:${hintC};height:22px;font-size:12px;padding:0 6px` }, hint));
    pressable(t, undefined, { sound: sfx.pick });
    const w = phase(h('div', { class: 'k-idle', style: `position:absolute;left:${x}px;top:${y}px;--iy:-4px;--ir:.6deg` }, t), 3.6, 1);
    return w;
  };
  el.append(
    zone('Đảo Hỏa', 'hoa', 'Ải kế cấp 1 · 0/70', 210, 230, 'Dễ', '#6cbf4f'),
    zone('Đảo Mộc', 'moc', 'Ải kế cấp 1', 24, 340, 'Dễ', '#6cbf4f'),
    zone('Đảo Kim', 'kim', 'Ải kế cấp 1', 330, 400, 'Dễ', '#6cbf4f'),
    zone('Đảo Thủy', 'thuy', 'Ải kế cấp 29 · 7/70', 40, 620, 'Khó', '#e8553f'),
    zone('Đảo Thổ', 'tho', 'Ải kế cấp 1', 320, 650, 'Dễ', '#6cbf4f'),
  );
  // mũi tên chỉ đảo nên đánh
  el.appendChild(h('div', { class: 'k-idle', style: 'position:absolute;left:92px;top:560px;--iy:-10px;--ir:0deg;--dur:1.1s', html: icon('down', 46) }));
  // thanh trên sảnh
  const balls = chip('ball', 186);
  const afk = h('button', { class: 'k-chip', style: 'cursor:pointer;height:44px', html: icon('clock', 50) }, '+50');
  pressable(afk, () => toast(phone, 'Đội tự đi ải mang về 50 bi!', 'clock'));
  el.appendChild(h('div', { class: 'k-topbar' }, lvRing(15, 0.62), balls.el, afk, h('div', { class: 'grow' }), round('gear', { size: 'small' })));
  // hàng nút dưới
  el.appendChild(h('div', { style: 'position:absolute;left:0;right:0;bottom:18px;display:flex;justify-content:space-around;align-items:flex-end;padding:0 10px' },
    round('team', { color: '#c9ecb0', label: 'Tướng', dot: 3 }),
    round('cards', { color: '#bcd8f5', label: 'Sổ thẻ' }),
    round('machine', { color: '#ffe08a', size: 'big', label: 'Máy Bi', dot: '99+', breath: true }),
    round('map', { color: '#ffb3a3', label: 'Đánh tiếp' }),
    round('pencil', { color: '#e3d2ff', label: 'Sổ tay' })));
  setTimeout(() => el.isConnected && toast(phone, 'Chào mừng trở lại! +12 bi', 'ball'), 900);
  return el;
}

// ---------- màn mẫu: Tướng ----------
export function pageHeroes(phone: HTMLElement) {
  const el = h('div', { class: 'k-fill' });
  const page = h('div', { class: 'k-page' });
  const scroll = h('div', { class: 'k-scroll', style: 'padding:22px 16px 120px 16px' });
  page.appendChild(scroll);
  el.append(topbar('Tướng').el, page);

  const lead = new HeroPuppet(HERO.giot_suong.forms[0].aola, 220, 210);
  const leadBox = h('div', { style: 'position:relative;width:220px;height:210px;cursor:pointer' }, lead.el);
  pressable(leadBox, () => lead.play(ATTACK), { burst: false, sound: sfx.pick });
  const slot = (need: string) => h('div', { class: 'k-slot', style: 'width:96px;height:128px' }, h('div', { class: 'col', style: 'align-items:center' }, h('span', { html: icon('lock', 30) }), h('span', { style: 'font:800 13px Baloo\\ 2;color:#8a7560' }, need)));
  const team = panel([
    h('div', { class: 'row' }, h('span', { class: 'k-title', style: 'font-size:24px' }, 'Đội hình'), h('div', { class: 'grow' }), button('Đổi đội', { color: 'blue', size: 'small' })),
    h('div', { class: 'row', style: 'justify-content:space-around;align-items:flex-end;margin-top:6px' }, slot('cấp 60'), leadBox, slot('cấp 200')),
    h('div', { class: 'row gap6', style: 'justify-content:center;margin-top:4px' }, tag('thuy'), h('span', { class: 'k-title', style: 'font-size:22px' }, 'Giọt Sương'), h('span', { class: 'k-rar', style: 'color:#6cbf4f' }, 'Khá')),
    h('div', { class: 'row', style: 'justify-content:space-around;margin-top:8px;font:800 20px Baloo\\ 2' },
      h('span', { class: 'row gap4', html: `${icon('heart', 26)} 827` }), h('span', { class: 'row gap4', html: `${icon('sword', 26)} 375` }),
      h('span', { class: 'row gap4', html: `${icon('shield', 26)} 95` }), h('span', { class: 'row gap4', html: `${icon('speed', 26)} 55` })),
  ], { tapes: ['y', 'p'] });
  scroll.appendChild(team);
  spawn(team, 80, 'drop');

  scroll.appendChild(h('div', { style: 'margin:22px 0 12px' }, tabs(['Của bạn', 'Chưa có'], 0)));
  const grid = h('div', { style: 'display:grid;grid-template-columns:repeat(3,148px);gap:14px 12px;justify-content:center' });
  const owned: [string, number, number, boolean?][] = [['giot_suong', 2, 1421, true], ['su_tu_lua', 1, 1180], ['bu_long', 1, 1093], ['nu_hoa', 1, 1012], ['thach_nhan', 1, 1240]];
  const locked = ['huyen_vu', 'thanh_long', 'bach_ho', 'ca_ngua'];
  const tiles = [
    ...owned.map(([id, st, pw, dot]) => heroTile(id, { star: st, power: pw, dot, onTap: () => heroDialog(phone, id) })),
    ...locked.map((id) => heroTile(id, { locked: true })),
  ];
  tiles.forEach((t, i) => {
    t.style.width = '148px';
    grid.appendChild(t);
    spawn(t, 260 + i * 70, 'up');
  });
  scroll.appendChild(grid);
  return el;
}

// ---------- màn mẫu: Trận (hàng thẻ) ----------
export function pageBattle(phone: HTMLElement) {
  const el = h('div', { class: 'k-fill' });
  // sân: nền trận đảo Thủy (giữ nguyên ảnh), hai tướng
  const arena = h('div', { style: `position:absolute;left:0;right:0;top:0;height:470px;background:url(${UNITY}BattleBG/battle_thuy_c01.png) center 70% / cover;border-bottom:3px solid #2b2118;overflow:hidden` });
  const me = new HeroPuppet(HERO.giot_suong.forms[0].aola, 200, 190);
  const foe = new HeroPuppet(HERO.su_tu_lua.forms[0].aola, 190, 180, true);
  const meBox = h('div', { style: 'position:absolute;left:60px;top:190px' }, me.el);
  const foeBox = h('div', { style: 'position:absolute;right:50px;top:130px' }, foe.el);
  const foeHp = bar('', 900, 900);
  const meHp = bar('', 827, 827);
  const plate = (name: string, e: Elem, b: ReturnType<typeof bar>, style: string) =>
    h('div', { class: 'k-panel', style: `position:absolute;${style};width:230px;padding:8px 12px 10px` },
      h('div', { class: 'row gap6', style: 'margin-bottom:4px' }, h('b', { class: 'k-title', style: 'font-size:17px' }, name), h('div', { class: 'grow' }), tag(e)), b.el);
  arena.append(foeBox, meBox, plate('Sư Tử Lửa', 'hoa', foeHp, 'right:16px;top:52px'), plate('Giọt Sương', 'thuy', meHp, 'left:16px;bottom:14px'));
  el.appendChild(arena);
  // trang dưới: hàng thẻ
  const page = h('div', { class: 'k-page', style: 'top:482px' });
  el.appendChild(page);
  const inner = h('div', { class: 'col', style: 'position:absolute;inset:0;padding:14px 16px 0' });
  page.appendChild(inner);
  const slots = Array.from({ length: 5 }, () => h('div', { class: 'k-slot' }));
  const pickTxt = h('span', { class: 'k-btn paper tiny', style: 'pointer-events:none' }, 'Chọn 0/5');
  const fightW = h('span', { style: 'display:none' });
  inner.appendChild(h('div', { class: 'row gap6' }, head('Hàng thẻ', 'b'), h('div', { class: 'grow' }), pickTxt));
  inner.appendChild(h('div', { class: 'row gap8', style: 'margin-top:10px;justify-content:center' }, ...slots, fightW));
  const hand = h('div', { class: 'row', style: 'gap:14px;justify-content:center;margin-top:18px;height:200px;align-items:flex-end' });
  inner.appendChild(hand);
  // chiêu, tuyệt kỹ, mana, nộ
  const mana = bar('blue', 25, 25, false);
  const rage = bar('orange', 40, 100, false);
  const skill = round('drop', { color: '#8fc3f0', breath: true, onTap: () => { me.play(ATTACK); hitFoe(90); mana.set(0); setTimeout(() => mana.set(25), 2500); } });
  const ult = round('wave', { color: '#ffb3a3', onTap: () => shake(ult) });
  inner.appendChild(h('div', { class: 'row gap12', style: 'margin-top:8px' },
    skill, h('div', { class: 'col gap6 grow' }, mana.el, rage.el), ult));

  let queued = 0;
  const pool = pick(['mai_vuot', 'giap_go', 'bang_gac', 'hit_tho', 'gam_gu', 'nem_da', 'binh_thuoc', 'dam_kep', 'cuong_no', 'hut_mau']);
  let k = 0;
  const nextCard = () => pool[k++ % pool.length];
  const fight = button('Đánh!', { color: 'red', breath: true, onTap: () => {
    me.play(ATTACK);
    sfx.hit();
    setTimeout(() => hitFoe(160 + Math.round(Math.random() * 60)), 380);
    queued = 0;
    slots.forEach((s, i) => setTimeout(() => { s.classList.remove('on'); s.replaceChildren(); punch(s, 0.6); }, i * 60));
    pickTxt.textContent = 'Chọn 0/5';
    fightW.style.display = 'none';
  } });
  fightW.appendChild(fight);
  function hitFoe(dmg: number) {
    foe.play(HIT);
    sfx.hit();
    foeHp.set(Math.max(0, foeHp.value - dmg));
    floatText(phone, `−${dmg}`, 400, 150, '#ff7b62');
    foeBox.animate([{ transform: 'translateX(0)' }, { transform: 'translateX(10px)' }, { transform: 'translateX(-6px)' }, { transform: 'translateX(0)' }], { duration: 260 });
    if (foeHp.value <= 0) setTimeout(() => foeHp.set(900), 1200);
  }
  const addCard = (i: number, delay: number) => {
    const c = nextCard();
    const cd = card(c);
    cd.el.addEventListener('click', () => {
      if (queued >= 5) return shake(cd.el);
      if (!cd.el.classList.contains('sel')) {
        hand.querySelectorAll('.k-cardw').forEach((x) => x.classList.remove('sel'));
        cd.el.classList.add('sel');
        return;
      }
      // chạm lần hai: bay vào ô kế tiếp
      const slot = slots[queued++];
      const a = cd.el.getBoundingClientRect(), b = slot.getBoundingClientRect(), s = phone.getBoundingClientRect().width / 540;
      cd.el.classList.remove('k-idle');
      sfx.pick();
      void flyTo(cd.el, (b.left + b.width / 2 - (a.left + a.width / 2)) / s, (b.top + b.height / 2 - (a.top + a.height / 2)) / s).then(() => {
        slot.classList.add('on');
        slot.replaceChildren(h('span', { html: icon(c.icon, 40) }));
        punch(slot);
        const idx = [...hand.children].indexOf(cd.el);
        cd.el.remove();
        addCard(idx, 0);
        pickTxt.textContent = `Chọn ${queued}/5`;
        if (queued >= 5) {
          fightW.style.display = '';
          spawn(fight, 0);
        }
      });
    });
    pressable(cd.inner, undefined, { burst: false, sound: sfx.pick });
    const ref = hand.children[i] ?? null;
    hand.insertBefore(cd.el, ref);
    deal(cd.el, delay, 0, 300);
    setTimeout(() => sfx.deal(), delay);
  };
  for (let i = 0; i < 3; i++) addCard(i, 300 + i * 120);
  return el;
}
