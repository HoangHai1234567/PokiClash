import type { Elem, HeroDef, HeroForm, Rarity } from '../types';

// 40 tướng, 8 mỗi hệ (2 Thường, 2 Khá, 2 Hiếm, 1 Sử thi, 1 Huyền thoại), chốt ở GD_Claude/13_DanhSachTuong.md.
// Mỗi tướng là một dòng tiến hóa của aola: lên sao thì đổi dạng (FORM_STARS ở progression.ts). Dạng lấy theo
// reskin/pokiclash_lines.json của AolaRipper. CHỈ DÙNG TRONG BẢN THỬ: hình và chuyển động gốc của Baitian.
// Chỉ số gốc là 6 chỉ số aola của dạng 1 (pmDataMap cột 4–9: công, thủ, công phép, thủ phép, máu, tốc); 4 thầy tu, Tiểu Y,
// Lam Quân giữ số cũ. Thẻ: 6 tướng giữ bộ thẻ riêng (vs, bd, pl, cs, ty, lq), 34 tướng mới tạm mượn bộ thẻ của tướng cùng
// hệ (cards.ts, BORROW), thiết kế thẻ riêng sau.

const SHARDS: Record<Rarity, number> = { common: 10, uncommon: 15, rare: 20, epic: 30, legend: 50 };
// cỡ trên sân theo số dạng của dòng: dạng sau to hơn
const SIZES = [[1], [0.92, 1.1], [0.9, 1.02, 1.14]];

// forms: [tên dạng, thư mục aola]; kit: tiền tố id 3 thẻ riêng (<kit>_skill, <kit>_ult, <kit>_pas)
function hero(
  id: string, name: string, title: string, elem: Elem, rarity: Rarity, stats: HeroDef['stats'], kit: string,
  forms: [string, string][], sizes = SIZES[forms.length - 1], line = `Dòng ${name}`,
): HeroDef {
  const fs: HeroForm[] = forms.map(([n, aola], i) => ({ name: n, aola, size: sizes[i] }));
  return {
    id, name, title, aola: fs[0].aola, elem, rarity, stats,
    skill: `${kit}_skill`, ult: `${kit}_ult`, passive: `${kit}_pas`,
    shards: SHARDS[rarity], line, size: fs[0].size, forms: fs,
  };
}

export const HEROES: HeroDef[] = [
  // ---------- Kim ----------
  hero('bu_long', 'Bu Lông', 'Người máy tí hon', 'kim', 'common', [60, 42, 90, 10, 90, 10], 'bu_long',
    [['Bu Lông', 'goc_76'], ['Bu Lông', 'goc_77'], ['Bu Lông', 'goc_78']]),
  hero('phao_hop', 'Pháo Hộp', 'Hộp sắt bắn đạn', 'kim', 'common', [48, 50, 98, 40, 46, 20], 'phao_hop',
    [['Pháo Hộp', 'goc_1889'], ['Pháo Hộp', 'goc_1890']]),
  hero('kiem_linh', 'Kiếm Linh', 'Thanh kiếm biết bay', 'kim', 'uncommon', [70, 40, 70, 40, 45, 75], 'kiem_linh',
    [['Kiếm Linh', 'goc_1617']]),  // chỉ số tạm: aola để cả 6 chỉ số là 1
  hero('meo_quyen', 'Mèo Quyền Sắt', 'Nắm đấm nghìn cân', 'kim', 'uncommon', [50, 40, 30, 80, 30, 70], 'meo_quyen',
    [['Mèo Quyền Sắt', 'goc_1176'], ['Mèo Quyền Sắt', 'goc_1177']]),
  hero('bo_cap', 'Bọ Cạp Đồng', 'Đuôi pha lê cát đỏ', 'kim', 'rare', [40, 70, 40, 30, 60, 70], 'bo_cap',
    [['Bọ Cạp Đồng', 'goc_676'], ['Bọ Cạp Đồng', 'goc_677'], ['Bọ Cạp Đồng', 'goc_678']]),
  hero('bo_ngua', 'Bọ Ngựa Liềm Thép', 'Song liềm kiếm khách', 'kim', 'rare', [60, 40, 50, 70, 40, 60], 'bo_ngua',
    [['Bọ Ngựa Liềm Thép', 'goc_683'], ['Bọ Ngựa Liềm Thép', 'goc_684'], ['Bọ Ngựa Liềm Thép', 'goc_685']]),
  hero('soi_linh', 'Sói Linh Thép', 'Lửa lạnh giáp xanh', 'kim', 'epic', [60, 25, 55, 90, 55, 92], 'soi_linh',
    [['Sói Linh Thép', 'goc_2176'], ['Sói Linh Thép', 'goc_2177']]),
  hero('bach_ho', 'Bạch Hổ', 'Thần thú phương Tây', 'kim', 'legend', [120, 65, 96, 140, 98, 102], 'bach_ho',
    [['Bạch Hổ', 'goc_1911']]),
  // ---------- Mộc ----------
  hero('mam_go', 'Mầm Gỗ', 'Hạt giống nhút nhát', 'moc', 'common', [55, 80, 40, 40, 40, 90], 'mam_go',
    [['Mầm Gỗ', 'goc_2373'], ['Mầm Gỗ', 'goc_2374']]),
  hero('nu_hoa', 'Nụ Hoa', 'Bông nở lăn tròn', 'moc', 'common', [40, 40, 50, 30, 30, 30], 'nu_hoa',
    [['Nụ Hoa', 'goc_22'], ['Nụ Hoa', 'goc_23'], ['Nụ Hoa', 'goc_24']]),
  hero('kien_binh', 'Kiến Binh', 'Lính gác giáo lá', 'moc', 'uncommon', [90, 100, 80, 100, 80, 90], 'kien_binh',
    [['Kiến Binh', 'goc_216']]),
  hero('banh_tet', 'Hiệp Sĩ Bánh Tét', 'Hiệp khách gói lá', 'moc', 'uncommon', [50, 50, 50, 50, 50, 50], 'banh_tet',
    [['Hiệp Sĩ Bánh Tét', 'goc_494'], ['Hiệp Sĩ Bánh Tét', 'goc_495'], ['Hiệp Sĩ Bánh Tét', 'goc_496']]),
  hero('de_hoa', 'Dê Hoa', 'Sừng gỗ vương miện hoa', 'moc', 'rare', [100, 60, 30, 40, 30, 70], 'de_hoa',
    [['Dê Hoa', 'goc_866'], ['Dê Hoa', 'goc_867'], ['Dê Hoa', 'goc_868']]),
  hero('giac_long', 'Giác Long Gỗ', 'Sừng vỏ cây xung trận', 'moc', 'rare', [55, 40, 60, 70, 60, 40], 'giac_long',
    [['Giác Long Gỗ', 'goc_2392'], ['Giác Long Gỗ', 'goc_2393']]),
  hero('phong_linh', 'Phong Linh', 'Linh tướng gió lá', 'moc', 'epic', [130, 60, 30, 30, 30, 30], 'phong_linh',
    [['Phong Linh', 'goc_943'], ['Phong Linh', 'goc_944']]),
  hero('thanh_long', 'Thanh Long', 'Thần thú phương Đông', 'moc', 'legend', [50, 40, 50, 80, 40, 60], 'thanh_long',
    [['Thanh Long', 'goc_1219'], ['Thanh Long', 'goc_1220']]),
  // ---------- Thủy ----------
  hero('tieu_y', 'Tiểu Y', 'Bé con sóng nước', 'thuy', 'common', [80, 30, 70, 80, 35, 40], 'ty',
    [['Tiểu Y', 'goc_1319'], ['Y Trạch', 'goc_1320']], [0.85, 1.12], 'Dòng Y Trạch'),
  hero('canh_cut', 'Cánh Cụt', 'Đầu bếp xứ băng', 'thuy', 'common', [85, 40, 50, 55, 50, 20], 'canh_cut',
    [['Cánh Cụt Con', 'goc_1691'], ['Đầu Bếp Cánh Cụt', 'goc_1692']]),
  hero('giot_suong', 'Giọt Sương', 'Giọt nước hóa rồng', 'thuy', 'uncommon', [50, 50, 50, 50, 50, 50], 'giot_suong',
    [['Giọt Nước', 'thuy_7'], ['Tiên Sương', 'goc_8'], ['Sương Long', 'goc_9']]),
  hero('tam_tay', 'Tám Tay', 'Pháo thủ bong bóng', 'thuy', 'uncommon', [80, 60, 60, 30, 30, 30], 'tam_tay',
    [['Tám Tay Bong Bóng', 'goc_1053'], ['Tám Tay Pháo Thủ', 'goc_1054']]),
  hero('ca_ngua', 'Cá Ngựa', 'Lính gác rạn san hô', 'thuy', 'rare', [80, 40, 60, 60, 40, 40], 'ca_ngua',
    [['Cá Ngựa Tân Binh', 'goc_181'], ['Cá Ngựa Song Đao', 'goc_182'], ['Cá Ngựa Tướng Quân', 'goc_183']]),
  hero('map_rang', 'Mập Răng Cưa', 'Răng cưa biển sâu', 'thuy', 'rare', [40, 50, 40, 40, 40, 90], 'map_rang',
    [['Cá Mập Con', 'goc_31'], ['Mập Răng Cưa', 'goc_32'], ['Vua Cá Mập', 'goc_33']]),
  hero('lam_quan', 'Lam Quân', 'Tiểu tướng chuông đồng', 'thuy', 'epic', [72, 30, 57, 77, 57, 48], 'lq',
    [['Lam Quân', 'goc_1831'], ['Vạn Quân', 'goc_1832'], ['Hắc Dực Vạn Quân', 'goc_2955']], [0.95, 1.12, 1.16], 'Dòng Vạn Quân'),
  hero('huyen_vu', 'Huyền Vũ', 'Thần thú phương Bắc', 'thuy', 'legend', [80, 60, 40, 40, 50, 40], 'huyen_vu',
    [['Rùa Ngọc', 'goc_713'], ['Rùa Biển Ngọc', 'goc_714'], ['Huyền Vũ', 'goc_715']]),
  // ---------- Hỏa ----------
  hero('heo_lua', 'Heo Lửa', 'Bờm lửa húc liều', 'hoa', 'common', [90, 90, 40, 30, 40, 30], 'heo_lua',
    [['Heo Lửa', 'goc_205'], ['Heo Lửa', 'goc_206'], ['Heo Lửa', 'goc_207']]),
  hero('dom_lua', 'Đốm Lửa', 'Ngọn lửa tươi cười', 'hoa', 'common', [55, 89, 62, 60, 61, 82], 'dom_lua',
    [['Đốm Lửa', 'goc_2419'], ['Đốm Lửa', 'goc_2420']]),
  hero('phao_tet', 'Pháo Tết', 'Ba đầu nổ đùng', 'hoa', 'uncommon', [40, 80, 30, 80, 30, 20], 'phao_tet',
    [['Pháo Tết', 'goc_1370'], ['Pháo Tết', 'goc_1371']]),
  hero('su_tu_lua', 'Sư Tử Lửa', 'Bờm lửa nhỏ', 'hoa', 'uncommon', [45, 60, 40, 60, 40, 55], 'su_tu_lua',
    [['Sư Tử Lửa', 'goc_4'], ['Sư Tử Lửa', 'goc_5'], ['Sư Tử Lửa', 'goc_6']]),
  hero('bo_de', 'Võ Tăng Bồ Đề', 'Cánh lửa liên hoa', 'hoa', 'rare', [130, 30, 95, 135, 95, 125], 'bd',
    [['Võ Tăng Bồ Đề', 'monk_500']], [1.08], 'Dòng Thỏ Võ'),
  hero('ho_lua', 'Hồ Lửa', 'Ba đuôi hỏa hồ', 'hoa', 'rare', [100, 100, 100, 100, 100, 100], 'ho_lua',
    [['Hồ Lửa', 'goc_307']]),
  hero('phap_luan', 'Thiền Sư Pháp Luân', 'Người xoay bánh xe pháp', 'hoa', 'epic', [110, 70, 90, 140, 90, 130], 'pl',
    [['Thiền Sư Pháp Luân', 'monk_2010']], [1.12], 'Dòng Thỏ Võ'),
  hero('chu_tuoc', 'Chu Tước', 'Thần thú phương Nam', 'hoa', 'legend', [120, 150, 90, 30, 90, 150], 'chu_tuoc',
    [['Chu Tước', 'goc_506']]),
  // ---------- Thổ ----------
  hero('vo_su', 'Võ Sư', 'Quyền thủ áo vải', 'tho', 'common', [45, 45, 60, 45, 60, 45], 'vs',
    [['Võ Sư', 'monk_boxer']], [1], 'Dòng Thỏ Võ'),
  hero('gau_mo', 'Gấu Thợ Mỏ', 'Thợ đào hầm', 'tho', 'common', [90, 130, 150, 50, 50, 80], 'gau_mo',
    [['Gấu Thợ Mỏ', 'goc_373']]),
  hero('soc_da', 'Sóc Đá', 'Má phồng đầy sỏi', 'tho', 'uncommon', [70, 60, 40, 60, 40, 20], 'soc_da',
    [['Sóc Đá', 'goc_825'], ['Sóc Đá', 'goc_826']]),
  hero('bo_hung', 'Bọ Hung Cát', 'Lăn cầu cát vàng', 'tho', 'uncommon', [200, 100, 150, 100, 150, 90], 'bo_hung',
    [['Bọ Hung Cát', 'goc_210']]),
  hero('thach_nhan', 'Thạch Nhân', 'Núi đá biết đi', 'tho', 'rare', [80, 85, 95, 30, 30, 25], 'thach_nhan',
    [['Thạch Nhân', 'goc_34'], ['Thạch Nhân', 'goc_35'], ['Thạch Nhân', 'goc_36']]),
  hero('sa_than', 'Sa Thần', 'Hộ vệ sa mạc', 'tho', 'rare', [250, 100, 200, 100, 200, 180], 'sa_than',
    [['Sa Thần', 'goc_1000']]),
  hero('ky_lan', 'Kỳ Lân Cát', 'Bờm cát hoàng kim', 'tho', 'epic', [50, 70, 50, 40, 50, 40], 'ky_lan',
    [['Kỳ Lân Cát', 'goc_88'], ['Kỳ Lân Cát', 'goc_89'], ['Kỳ Lân Cát', 'goc_90']]),
  hero('ca_sa', 'Đại Sư Cà Sa', 'Kim cang hộ pháp', 'tho', 'legend', [110, 70, 95, 136, 95, 124], 'cs',
    [['Đại Sư Cà Sa', 'monk_2217']], [1.18], 'Dòng Thỏ Võ'),
];

export const HERO: Record<string, HeroDef> = Object.fromEntries(HEROES.map((h) => [h.id, h]));
// người chơi mới chỉ có Giọt Sương (người dùng chốt 2026-11-01); đảo Thủy tặng thêm Võ Sư (ải 3) và Nụ Hoa (ải 6)
export const STARTERS = ['giot_suong'];
export const LEGEND_MILESTONE_HERO = 'ca_sa';
