# Xuất khung VFX vào game. Từ 2026-11-19 (người dùng so trang xem khung: "tôi nhìn thấy bản cũ đẹp hơn", "có thể dùng bản gốc luôn
# cũng được") lấy BẢN GỐC đã cắt + tách nền (khung/<tên>/, cat_khung.py), đủ màu RGBA, không làm phẳng / vân chì (khung_chi/ chỉ còn để
# so). Giảm 255 màu làm lấm tấm chỗ mờ dần nên bỏ; Unity nén lại khi build. Ghi:
#   Assets/03 Art/Fx/Hat/hat_fb_<tên>_NN.png   (HatLua.Fb… tra bằng S("fb_<tên>_NN"))
#   py -3 -I ArtGen/Spine/vfx_gen/xuat_fb.py            (mọi hiệu ứng)
#   py -3 -I ArtGen/Spine/vfx_gen/xuat_fb.py no khoi    (vài hiệu ứng)
# Giảm còn 255 màu (PNG bảng màu có alpha): vân chì làm PNG đầy đủ màu nặng ~125 KB / khung; Unity nén lại khi build nên không mất gì
# thấy được. Sau khi xuất: Unity refresh, chạy menu "PokiClash/Prefab/Sàn đấu: hạt lửa (bộ Hỏa)" và "Hộp chi tiết tướng: hạt lửa + nút Mana".
import os, sys, glob
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'Assets', '03 Art', 'Fx', 'Hat')
NAMES = ['no', 'trung_lua', 'lua_lap', 'cau_lua', 'nham', 'khoi', 'nuoc_toe', 'song_nuoc', 'trung_nuoc', 'cau_nuoc', 'loc',
         'gai_la', 'gai_bang', 'gai_sat', 'loc_nuoc', 'loc_lua', 'loc_cat', 'cau_tu', 'cau_bay', 'loc_nuoc_bao', 'loc_lua_bao', 'loc_cat_bao',
         'tia_moc_doan', 'tia_moc_nong', 'tia_moc_trung', 'tia_nuoc_doan', 'tia_nuoc_trung',
         'tia_lua_doan', 'tia_lua_nong', 'tia_lua_trung', 'tia_vang_doan', 'tia_vang_nong', 'tia_vang_trung',
         'long_la', 'quat_dat', 'chem_kg', 'trung_trang', 'set_danh']


def main():
    names = sys.argv[1:] or NAMES
    tot = 0
    for n in names:
        files = sorted(glob.glob(os.path.join(HERE, 'khung', n, n + '_*.png')))
        if not files:
            print('thiếu', n); continue
        for f in files:
            im = Image.open(f).convert('RGBA')
            dst = os.path.join(OUT, 'hat_fb_' + os.path.basename(f))
            im.save(dst, optimize=True)
            tot += os.path.getsize(dst)
        print(n, len(files), 'khung')
    print('tổng %.1f MB vào %s' % (tot / 1048576, OUT))


if __name__ == '__main__':
    main()
