// Icon vẽ tay: viewBox 48 × 48, nét mực dày, tô màu bút sáp. Lớp "ic" làm nét rung theo nhịp của cả trang.
const INK = '#2b2118';
const S = `stroke="${INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"`;
const s2 = `stroke="${INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"`;
const shine = (d: string) => `<path d="${d}" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".75"/>`;

const P: Record<string, string> = {
  // ----- chỉ số, tài nguyên -----
  heart: `<path d="M24 41C10 31 5 24 6 16c1-6 6-9 10-9 4 0 7 2 8 6 1-4 4-6 8-6 5 0 10 4 10 10 0 8-6 15-18 24z" fill="#f05a5a" ${S}/>${shine('M12 15c1-3 3-4 5-4')}`,
  drop: `<path d="M24 5c6 9 13 16 13 24a13 13 0 0 1-26 0C11 21 18 14 24 5z" fill="#5aa8f0" ${S}/>${shine('M17 28c0 4 2 6 5 7')}`,
  flame: `<path d="M24 43c-9 0-14-6-14-13 0-8 7-11 7-19 4 3 6 6 6 10 2-3 3-7 2-12 8 5 13 13 13 21 0 8-5 13-14 13z" fill="#f58a2e" ${S}/><path d="M24 40c-4 0-6-3-6-6 0-4 4-6 4-9 4 3 8 6 8 10 0 3-2 5-6 5z" fill="#ffd24a" ${s2}/>`,
  sword: `<path d="M39 6l3 3-21 23-5-5z" fill="#e2e8ee" ${S}/><path d="M10 27l11 11M14 31l-7 7M7 34l7 7" fill="none" ${S}/>${shine('M36 10L22 26')}`,
  shield: `<path d="M24 5l16 5c0 15-5 26-16 33C13 36 8 25 8 10z" fill="#7fb4e8" ${S}/><path d="M24 11v26M15 16c3 1 6 1 9 0 3 1 6 1 9 0" fill="none" ${s2}/>`,
  speed: `<path d="M27 4L11 27h11l-4 17 19-25H25z" fill="#ffd24a" ${S}/>`,
  star: `<path d="M24 5l5.5 11.5 12.5 1.5-9.2 8.6 2.5 12.4L24 32.8 12.7 39l2.5-12.4L6 18l12.5-1.5z" fill="#ffd24a" ${S}/>`,
  starOff: `<path d="M24 5l5.5 11.5 12.5 1.5-9.2 8.6 2.5 12.4L24 32.8 12.7 39l2.5-12.4L6 18l12.5-1.5z" fill="#e6d8b8" ${S}/>`,
  ball: `<circle cx="24" cy="24" r="16" fill="#ff8fb3" ${S}/><path d="M9 21c8 4 22 4 30 0" fill="none" ${s2}/><circle cx="24" cy="23" r="4.5" fill="#fff" ${s2}/>${shine('M15 14c3-3 6-4 9-4')}`,
  exp: `<path d="M24 4l6 13 14 2-10 10 3 14-13-7-13 7 3-14L4 19l14-2z" fill="#c18cf0" ${S}/><text x="24" y="31" font-family="Baloo 2" font-weight="800" font-size="13" text-anchor="middle" fill="#fff" stroke="${INK}" stroke-width="3" paint-order="stroke">XP</text>`,
  shard: `<path d="M24 4l12 10-5 26-7 4-7-4-5-26z" fill="#7ee0d0" ${S}/><path d="M24 4v40M12 14h24M17 40l7-26 7 26" fill="none" ${s2} opacity=".7"/>`,
  coin: `<circle cx="24" cy="24" r="17" fill="#ffd24a" ${S}/><circle cx="24" cy="24" r="10" fill="none" ${s2}/>`,
  clock: `<circle cx="24" cy="25" r="17" fill="#fff6dc" ${S}/><path d="M24 14v12l8 5" fill="none" ${S}/><path d="M17 5h14" ${S}/>`,
  chest: `<path d="M7 20h34v20H7z" fill="var(--chest,#c98a4a)" ${S}/><path d="M7 20c0-9 6-13 17-13s17 4 17 13z" fill="var(--chest,#c98a4a)" ${S}/><path d="M7 25h34" ${S}/><rect x="20" y="21" width="8" height="10" rx="2" fill="#ffd24a" ${s2}/><path d="M14 10v30M34 10v30" fill="none" ${s2} opacity=".55"/>`,
  // ----- giao diện -----
  map: `<path d="M5 11l12-5 14 5 12-5v31l-12 5-14-5-12 5z" fill="#f3e2b0" ${S}/><path d="M17 6v31M31 11v31" fill="none" ${s2}/><path d="M9 26c4-3 6 2 10 0s5-6 9-4 6 3 10 1" fill="none" stroke="#e8553f" stroke-width="2.5" stroke-dasharray="3 3"/>`,
  cards: `<rect x="6" y="11" width="22" height="30" rx="3" transform="rotate(-12 17 26)" fill="#7fb4e8" ${S}/><rect x="19" y="8" width="22" height="30" rx="3" transform="rotate(8 30 23)" fill="#ffd24a" ${S}/><path d="M28 18l2 5 5 1-4 3 1 5-4-3-4 3 1-5-4-3 5-1z" fill="#fff" ${s2} transform="rotate(8 30 23)"/>`,
  team: `<circle cx="17" cy="16" r="7" fill="#ffcf9e" ${S}/><path d="M5 40c0-9 5-14 12-14s12 5 12 14z" fill="#6cbf4f" ${S}/><circle cx="33" cy="18" r="6" fill="#ffcf9e" ${S}/><path d="M27 40c0-7 2-12 7-12 5 0 9 4 9 12z" fill="#4a90d9" ${S}/>`,
  machine: `<path d="M9 6h30v30H9z" fill="#f7c948" ${S}/><circle cx="16" cy="14" r="2" fill="${INK}"/><circle cx="24" cy="19" r="2" fill="${INK}"/><circle cx="32" cy="14" r="2" fill="${INK}"/><circle cx="20" cy="25" r="2" fill="${INK}"/><circle cx="28" cy="25" r="2" fill="${INK}"/><circle cx="24" cy="11" r="4" fill="#ff8fb3" ${s2}/><path d="M9 36l-3 7h36l-3-7" fill="#e8553f" ${S}/><path d="M17 36v7M24 36v7M31 36v7" ${s2}/>`,
  gear: `<path d="M24 6l4 1 1 5 4 2 4-3 3 3-3 4 2 4 5 1 1 4-1 4-5 1-2 4 3 4-3 3-4-3-4 2-1 5-4 1-4-1-1-5-4-2-4 3-3-3 3-4-2-4-5-1-1-4 1-4 5-1 2-4-3-4 3-3 4 3 4-2 1-5z" fill="#c9d3dc" ${S}/><circle cx="24" cy="24" r="6" fill="#fffaf0" ${S}/>`,
  swap: `<path d="M8 17h28l-6-7M40 31H12l6 7" fill="none" ${S}/>`,
  lock: `<rect x="10" y="21" width="28" height="21" rx="4" fill="#c9b48a" ${S}/><path d="M16 21v-6a8 8 0 0 1 16 0v6" fill="none" ${S}/><circle cx="24" cy="31" r="3" fill="${INK}"/>`,
  play: `<path d="M14 8l26 16-26 16z" fill="#6cbf4f" ${S}/>`,
  pause: `<path d="M13 9h8v30h-8zM27 9h8v30h-8z" fill="#fff6dc" ${S}/>`,
  close: `<path d="M12 12l24 24M36 12L12 36" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`,
  check: `<path d="M8 25l10 10L40 11" fill="none" stroke="#3f8f33" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>`,
  up: `<path d="M24 6l14 16h-8v20H18V22h-8z" fill="#6cbf4f" ${S}/>`,
  down: `<path d="M24 42L10 26h8V6h12v20h8z" fill="#e8553f" ${S}/>`,
  info: `<circle cx="24" cy="24" r="17" fill="#7fb4e8" ${S}/><path d="M24 22v12" ${S}/><circle cx="24" cy="15" r="2.4" fill="${INK}"/>`,
  back: `<path d="M28 9L13 24l15 15" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>`,
  boss: `<path d="M24 6c10 0 16 7 16 16 0 6-3 10-6 12v6H14v-6c-3-2-6-6-6-12 0-9 6-16 16-16z" fill="#f3f0e8" ${S}/><circle cx="17" cy="22" r="4.5" fill="${INK}"/><circle cx="31" cy="22" r="4.5" fill="${INK}"/><path d="M24 27l-2 4h4z" fill="${INK}"/><path d="M19 40v-5M24 40v-5M29 40v-5" ${s2}/>`,
  crownSm: `<path d="M8 36l-2-22 10 8 8-13 8 13 10-8-2 22z" fill="#ffd24a" ${S}/><path d="M8 36h32" ${S}/>`,
  tv: `<rect x="5" y="12" width="38" height="26" rx="4" fill="#9ad0f0" ${S}/><path d="M16 4l8 8 8-8" fill="none" ${S}/><path d="M20 20v11l9-5.5z" fill="#fff" ${s2}/>`,
  sound: `<path d="M8 19h8l10-8v26l-10-8H8z" fill="#fff6dc" ${S}/><path d="M32 17c3 3 3 11 0 14M36 13c5 5 5 17 0 22" fill="none" ${S}/>`,
  pencil: `<path d="M8 40l3-10 22-22 7 7-22 22z" fill="#f7c948" ${S}/><path d="M8 40l3-10 7 7z" fill="#ffe2b8" ${s2}/><path d="M29 12l7 7" ${s2}/>`,
  dice: `<rect x="8" y="8" width="32" height="32" rx="6" fill="#fff" ${S} transform="rotate(-8 24 24)"/><circle cx="17" cy="18" r="2.6" fill="${INK}"/><circle cx="24" cy="24" r="2.6" fill="${INK}"/><circle cx="31" cy="30" r="2.6" fill="${INK}"/>`,
  // ----- thẻ chung -----
  claw: `<path d="M9 40c6-12 10-22 11-34M19 41c4-11 7-21 8-33M29 41c3-9 5-17 6-28" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round"/><path d="M9 40c6-12 10-22 11-34M19 41c4-11 7-21 8-33M29 41c3-9 5-17 6-28" fill="none" stroke="#e8553f" stroke-width="3" stroke-linecap="round"/>`,
  bandage: `<rect x="5" y="17" width="38" height="14" rx="7" fill="#ffe0b8" transform="rotate(-35 24 24)" ${S}/><rect x="17" y="17" width="14" height="14" fill="#fff6e6" transform="rotate(-35 24 24)" ${s2}/><path d="M21 23h.1M25 25h.1M23 27h.1M27 21h.1" ${S} transform="rotate(-35 24 24)"/>`,
  rock: `<path d="M8 33l4-14 10-8 13 3 6 12-4 11-15 3z" fill="#b5a99a" ${S}/><path d="M17 22l6 4M27 30l5-3" fill="none" ${s2}/>${shine('M14 22l5-6')}`,
  potion: `<path d="M19 5h10v6h-2v6c7 3 11 8 11 14a14 14 0 0 1-28 0c0-6 4-11 11-14v-6h-2z" fill="#f06d8a" ${S}/><path d="M12 30c6-2 18 2 24-1" fill="none" ${s2}/>${shine('M16 33c0 3 2 5 4 6')}`,
  bun: `<path d="M6 32c0-12 8-20 18-20s18 8 18 20c0 5-8 8-18 8S6 37 6 32z" fill="#fff3dc" ${S}/><path d="M18 15c2 4 2 7 0 10M24 13v12M30 15c-2 4-2 7 0 10" fill="none" ${s2}/>`,
  skull: `<path d="M24 5c10 0 16 7 16 16 0 5-2 9-5 11v7H13v-7c-3-2-5-6-5-11 0-9 6-16 16-16z" fill="#f3f0e8" ${S}/><circle cx="17" cy="21" r="4.5" fill="#e8553f" ${s2}/><circle cx="31" cy="21" r="4.5" fill="#e8553f" ${s2}/><path d="M24 26l-2.5 5h5z" fill="${INK}"/>`,
  bubble: `<circle cx="24" cy="24" r="17" fill="#bfe4ff" fill-opacity=".85" ${S}/>${shine('M14 18c2-5 6-7 10-7')}<circle cx="31" cy="31" r="2.5" fill="#fff"/>`,
  lotus: `<path d="M24 38c-8 0-14-4-17-9 5-1 10 0 13 3-3-7-2-14 4-21 6 7 7 14 4 21 3-3 8-4 13-3-3 5-9 9-17 9z" fill="#f7a8c8" ${S}/><path d="M24 11v26" fill="none" ${s2}/><path d="M8 41h32" ${S}/>`,
  fist: `<path d="M12 18c0-4 3-6 6-6h14c4 0 6 3 6 7v10c0 7-5 12-12 12h-4c-6 0-10-4-10-10z" fill="#ffcf9e" ${S}/><path d="M18 12v9M25 12v9M32 13v8M12 24c4-2 9-1 12 2" fill="none" ${s2}/>`,
  fist2: `<g transform="translate(-6 2) scale(.8)"><path d="M12 18c0-4 3-6 6-6h14c4 0 6 3 6 7v10c0 7-5 12-12 12h-4c-6 0-10-4-10-10z" fill="#ffcf9e" ${S}/><path d="M18 12v9M25 12v9M32 13v8" fill="none" ${s2}/></g><g transform="translate(16 6) scale(.8)"><path d="M12 18c0-4 3-6 6-6h14c4 0 6 3 6 7v10c0 7-5 12-12 12h-4c-6 0-10-4-10-10z" fill="#ffb07a" ${S}/><path d="M18 12v9M25 12v9M32 13v8" fill="none" ${s2}/></g>`,
  rage: `<path d="M8 10l8 6M40 10l-8 6" ${S}/><circle cx="24" cy="28" r="15" fill="#f05a3a" ${S}/><path d="M15 23l7 3M33 23l-7 3" ${S}/><path d="M17 35c4-4 10-4 14 0" fill="none" ${S}/><path d="M36 6l3 5 5-1-3 5" fill="none" stroke="#e8553f" stroke-width="2.6" stroke-linecap="round"/>`,
  fang: `<path d="M6 14c6 5 30 5 36 0v6c-2 4-6 6-10 6l-3 13-5-12h-0l-5 12-3-13c-4 0-8-2-10-6z" fill="#fff" ${S}/><path d="M18 26c0 6-2 9-4 11M30 26c0 6 2 9 4 11" fill="none" stroke="#e8553f" stroke-width="2.4" stroke-linecap="round"/>`,
  crack: `<path d="M24 5l16 5c0 15-5 26-16 33C13 36 8 25 8 10z" fill="#c9d3dc" ${S}/><path d="M22 6l4 10-6 6 7 7-4 13" fill="none" stroke="#e8553f" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>`,
  torch: `<path d="M20 25h8l-2 18h-4z" fill="#a8743f" ${S}/><path d="M24 26c-7 0-10-4-10-9 0-6 5-8 5-13 3 2 5 4 5 7 1-2 2-4 1-7 6 3 9 8 9 13 0 5-3 9-10 9z" fill="#f58a2e" ${S}/>`,
  mirror: `<ellipse cx="24" cy="20" rx="13" ry="15" fill="#bfe4ff" ${S}/><path d="M24 35v8M17 43h14" ${S}/>${shine('M16 16c1-4 4-6 7-7')}${shine('M27 27l4-4')}`,
  eye: `<path d="M4 24c6-9 12-13 20-13s14 4 20 13c-6 9-12 13-20 13S10 33 4 24z" fill="#fff" ${S}/><circle cx="24" cy="24" r="8" fill="#f7c948" ${S}/><circle cx="24" cy="24" r="3.5" fill="${INK}"/>`,
  bolt: `<path d="M28 3L10 27h12l-5 18 21-26H26z" fill="#ffe14a" ${S}/>`,
  yinyang: `<circle cx="24" cy="24" r="18" fill="#fff" ${S}/><path d="M24 6a9 9 0 0 1 0 18 9 9 0 0 0 0 18 18 18 0 0 1 0-36z" fill="#5aa8f0" ${s2}/><circle cx="24" cy="15" r="3" fill="#fff" ${s2}/><circle cx="24" cy="33" r="3" fill="#5aa8f0" ${s2}/>`,
  ghost: `<path d="M10 42V21c0-9 6-15 14-15s14 6 14 15v21l-5-4-4 4-5-4-5 4-4-4z" fill="#ece6ff" ${S}/><circle cx="19" cy="21" r="2.6" fill="${INK}"/><circle cx="29" cy="21" r="2.6" fill="${INK}"/><path d="M21 29c2 1 4 1 6 0" fill="none" ${s2}/>`,
  phoenix: `<path d="M24 40c-6-6-6-14 0-20 6 6 6 14 0 20z" fill="#f58a2e" ${S}/><path d="M22 24C14 23 7 16 5 7c8 2 14 6 19 13 5-7 11-11 19-13-2 9-9 16-17 17" fill="#ffcc3a" ${S}/><circle cx="24" cy="15" r="4" fill="#e8553f" ${s2}/>`,
  crown: `<path d="M7 36l-3-23 11 9 9-15 9 15 11-9-3 23z" fill="#ffd24a" ${S}/><path d="M7 36h34v6H7z" fill="#f39a2d" ${S}/><circle cx="24" cy="27" r="3.5" fill="#e8553f" ${s2}/>`,
  // ----- thẻ nội tại -----
  wheel: `<circle cx="24" cy="24" r="17" fill="#ffcf6a" ${S}/><circle cx="24" cy="24" r="5" fill="#f58a2e" ${s2}/><path d="M24 7v12M24 29v12M7 24h12M29 24h12M12 12l8 8M28 28l8 8M36 12l-8 8M20 28l-8 8" ${s2}/>`,
  sun: `<circle cx="24" cy="24" r="9" fill="#ffd24a" ${S}/><path d="M24 4v7M24 37v7M4 24h7M37 24h7M10 10l5 5M33 33l5 5M38 10l-5 5M15 33l-5 5" ${S}/>`,
  incense: `<path d="M12 42h24l-3-9H15z" fill="#c98a4a" ${S}/><path d="M24 33V18" ${S}/><path d="M24 17c-4-3-4-7 0-9 4-2 4-5 1-7" fill="none" stroke="#9aa6b2" stroke-width="2.6" stroke-linecap="round"/><path d="M18 18c-3-3-2-6 1-8M30 18c3-3 2-6-1-8" fill="none" stroke="#9aa6b2" stroke-width="2.2" stroke-linecap="round"/>`,
  seed: `<path d="M24 42c-8 0-12-6-12-12 0-8 6-12 12-12s12 4 12 12c0 6-4 12-12 12z" fill="#b5875a" ${S}/><path d="M24 18c0-6 3-10 9-12-1 6-4 9-9 12zM24 18c-1-5-4-8-9-9 1 5 4 8 9 9z" fill="#6cbf4f" ${s2}/>`,
  leaf: `<path d="M8 40C8 20 20 8 41 7c0 21-12 33-33 33z" fill="#6cbf4f" ${S}/><path d="M8 40L32 16M18 30l-1-8M24 24l7 1" fill="none" ${s2}/>`,
  wind: `<path d="M5 17h24a6 6 0 1 0-6-6M5 26h32a6 6 0 1 1-6 6M5 35h16" fill="none" ${S}/>`,
  feather: `<path d="M38 6C24 8 12 18 10 38c14-3 26-14 28-32z" fill="#bfe8d0" ${S}/><path d="M6 42L30 15M16 31h8M21 25h7" fill="none" ${s2}/>`,
  bell: `<path d="M24 6c-8 0-12 6-12 14v9l-5 6h34l-5-6v-9c0-8-4-14-12-14z" fill="#e8b84a" ${S}/><circle cx="24" cy="39" r="4" fill="#c98a4a" ${S}/><path d="M17 20c0-4 2-7 6-8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".7"/>`,
  hammer: `<path d="M9 9h20v14H9z" fill="#c9d3dc" ${S} transform="rotate(-30 19 16)"/><path d="M22 21l16 20" stroke="${INK}" stroke-width="8" stroke-linecap="round"/><path d="M22 21l16 20" stroke="#c98a4a" stroke-width="4" stroke-linecap="round"/>`,
  helmet: `<path d="M8 33c0-13 7-23 16-23s16 10 16 23z" fill="#c9d3dc" ${S}/><path d="M5 33h38v6H5z" fill="#a9b6c2" ${S}/><path d="M24 10v23" ${s2}/><path d="M24 4l3 6h-6z" fill="#e8553f" ${s2}/>`,
  wing: `<path d="M6 38C10 20 22 9 42 6c-3 6-6 9-11 11 4 0 7-1 9-2-3 6-8 10-14 11 3 1 6 0 8-1-5 8-14 12-28 13z" fill="#6a5a8a" ${S}/><path d="M12 33c8-6 15-12 22-20" fill="none" stroke="#c7b8f0" stroke-width="2" stroke-linecap="round"/>`,
  moon: `<path d="M30 5a19 19 0 1 0 13 26A15 15 0 0 1 30 5z" fill="#6a5a8a" ${S}/><path d="M12 12l1 3 3 1-3 1-1 3-1-3-3-1 3-1z" fill="#ffd24a" ${s2}/>`,
  wave: `<path d="M4 30c5-10 12-14 20-12-6 4-6 10 0 12 6 2 12-1 16-6 3 7-2 16-14 16C14 40 6 37 4 30z" fill="#5aa8f0" ${S}/><path d="M10 20c4-8 12-12 20-10" fill="none" ${s2}/>`,
  trident: `<path d="M24 14v30" stroke="${INK}" stroke-width="6" stroke-linecap="round"/><path d="M24 14v30" stroke="#e8b84a" stroke-width="2.5" stroke-linecap="round"/><path d="M12 6v8c0 4 5 6 12 6s12-2 12-6V6M24 4v16" fill="none" ${S}/><path d="M10 9l2-5 2 5M22 7l2-5 2 5M34 9l2-5 2 5" fill="#e8b84a" ${s2}/>`,
  // ----- Ngũ hành -----
  e_kim: `<path d="M6 34l6-16h24l6 16z" fill="#d6dee6" ${S}/><path d="M12 18l4-8h16l4 8" fill="#eef2f6" ${S}/>${shine('M15 28l3-7')}`,
  e_moc: `<path d="M8 40C8 20 20 8 41 7c0 21-12 33-33 33z" fill="#6cbf4f" ${S}/><path d="M8 40L32 16" fill="none" ${s2}/>`,
  e_thuy: `<path d="M24 5c6 9 13 16 13 24a13 13 0 0 1-26 0C11 21 18 14 24 5z" fill="#4a90d9" ${S}/><path d="M17 30c3 3 8 3 12-1" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>`,
  e_hoa: `<path d="M24 43c-9 0-14-6-14-13 0-8 7-11 7-19 4 3 6 6 6 10 2-3 3-7 2-12 8 5 13 13 13 21 0 8-5 13-14 13z" fill="#e8553f" ${S}/><path d="M24 40c-4 0-6-3-6-6 0-4 4-6 4-9 4 3 8 6 8 10 0 3-2 5-6 5z" fill="#ffd24a" ${s2}/>`,
  e_tho: `<path d="M4 40l13-24 7 10 6-14 14 28z" fill="#e2a93b" ${S}/><path d="M26 18l4 6 3-3" fill="none" ${s2}/>`,
};

export function icon(name: string, size = 40, extra = ''): string {
  const body = P[name] ?? P.star;
  return `<svg class="ic" viewBox="0 0 48 48" width="${size}" height="${size}" ${extra}>${body}</svg>`;
}

export function iconEl(name: string, size = 40, extra = ''): SVGElement {
  const t = document.createElement('template');
  t.innerHTML = icon(name, size, extra);
  return t.content.firstElementChild as SVGElement;
}

export const hasIcon = (n: string) => n in P;
