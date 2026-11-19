# Tách nền XÁM PHẲNG của tờ khung gen (GPT vẽ nền "plain flat light gray") ngay tại máy, thay cho Magnific remove_background
# (công cụ đó vài lần coi cả tờ là chủ thể, giữ nguyên nền: lốc cát trùm, va chạm tia lá 2026-11-19).
#   py -3 -I ArtGen/Spine/vfx_gen/tach_xam.py tia_lua_doan tia_vang_trung ...
# Đọc tho/<tên>.png, ghi trong/<tên>.png (RGBA). Màu nền lấy trung vị bốn góc; điểm nào gần màu nền (Lab, nặng phần sắc: nền xám trung
# tính, hình VFX luôn có sắc) thì trong suốt, chuyển mềm trong khoảng 7..16. Không cần nối ra mép (vùng nền bị vòng / lốc bao kín vẫn tách).
# Màu trắng tinh / xám trong hình (sao lấp lánh trắng, khói xám) có thể bị mờ bớt: tờ có khói xám thì đừng dùng script này.
import os, sys
import numpy as np, cv2
from PIL import Image
from scipy import ndimage

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def tach(name, lo=7.0, hi=16.0):
    raw = np.asarray(Image.open(os.path.join(HERE, 'tho', name + '.png')).convert('RGB'))
    lab = cv2.cvtColor(raw, cv2.COLOR_RGB2LAB).astype(np.float32)
    c = np.concatenate([lab[:20, :20].reshape(-1, 3), lab[:20, -20:].reshape(-1, 3), lab[-20:, :20].reshape(-1, 3), lab[-20:, -20:].reshape(-1, 3)])
    bg = np.median(c, axis=0)
    d = np.sqrt((((lab - bg) * np.array([0.6, 1.6, 1.6])) ** 2).sum(-1))
    a = np.clip((d - lo) / (hi - lo), 0, 1)
    a = ndimage.gaussian_filter(a, 0.6)
    Image.fromarray(np.dstack([raw, (a * 255).astype(np.uint8)]), 'RGBA').save(os.path.join(HERE, 'trong', name + '.png'))
    sach = os.path.join(HERE, 'trong', name + '_sach.png')
    if os.path.exists(sach): os.remove(sach)
    print(name, 'nền', bg.astype(int), 'trong suốt %.0f %%' % (100 * (a < 0.02).mean()))


if __name__ == '__main__':
    for n in sys.argv[1:]: tach(n)
