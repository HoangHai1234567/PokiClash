// Mọi con số cân bằng ở một chỗ. Bảng chỉnh số trong game sửa thẳng object này (mất khi tải lại trang).
export const CFG = {
  // lượt
  picks: 5,
  offer: 3,
  // tài nguyên
  manaPerTurn: 20,
  benchMana: 10,
  maxMana: 100,
  maxRage: 100,
  rageOnAttack: 10,
  rageOnHit: 80, // nộ nhận thêm = phần máu mất / máu tối đa × số này
  // sát thương
  critBase: 0.05,
  critMult: 1.6,
  defK: 100, // sát thương × defK / (defK + thủ)
  dmgVar: 0.08,
  shieldCap: 0.6, // khiên tối đa so với máu tối đa
  // chỉ số tướng theo cấp và sao
  hpBase: 600,
  atkBase: 180,
  defBase: 55,
  lvStep: 0.1,
  starStep: 0.08,
  bossHp: 1.8,
  bossAtk: 1.1,
  cardLvStep: 0.15, // mỗi cấp thẻ tăng số của thẻ thêm 15 %
  // giới hạn an toàn: quá số hiệp này thì bên có tổng phần trăm máu cao hơn thắng (hoà thì địch thắng)
  maxRounds: 60,
};

export type Cfg = typeof CFG;
export const CFG_DEFAULT: Cfg = { ...CFG };
