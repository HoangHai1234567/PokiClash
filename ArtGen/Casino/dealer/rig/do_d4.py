# Đo clip D4 của Lão Mực bằng chính động cơ nướng (dong_co.Sim, 60 bước/giây): vị trí cổ tay và góc thế giới của hai bàn tay ở
# từng bước, bước dời và bước xoay lớn nhất giữa hai bước liền nhau (dấu hiệu giật / quay ngược vòng), toạ độ ở các mốc sự kiện.
# Ghi nhớ rig-kiem-goc-nhay: tờ khung tĩnh không lộ lỗi giật, phải đo. (Góc nhảy của khoá đã xuất: kiem.py.)
# Chạy: py -3 -I do_d4.py [clip ...]
import math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hoat_anh as H  # noqa: E402
from dong_co import simulate, DT, base_pose  # noqa: E402
import clip_d4 as D4  # noqa: E402

MARK = {
    "rl_spin": [("đập xuống mâm", D4.T_HIT), ("quay", D4.T_QUAY), ("hết quất", D4.T_WHIP1), ("tha_bi − 1 khung", D4.T_THA - D4.F),
                ("tha_bi", D4.T_THA), ("tha_bi + 1 khung", D4.T_THA + D4.F)],
    "rl_point": [("chi", 0.5), ("giữ", 0.8)],
    "rl_no_more": [("lấy đà", 0.26), ("hết xua", 0.42)],
    "rl_invite": [("đầu cung quạt", 0.42), ("giữa", 0.62), ("cuối", 0.82)],
    "rl_watch": [("t 0 (40°)", 0.0), ("t 0,72 (270°)", 0.7222), ("t 1,22 (180°)", 1.2222), ("t 1,72 (90°)", 1.7222)],
}


def measure(name):
    dur, loop, fn = H.CLIPS[name]
    idle = H.CLIPS["idle"][2]
    rec = []

    def pose(t):
        p = base_pose()
        if t < 0 and not loop:
            idle(t % H.IDLE_DUR, p)
        else:
            fn(t % dur if loop else t, p)
        old = p.get("xao")

        def grab(hw, t=t, old=old):
            rec.append((t, {s: (hw[s][0], hw[s][1]) for s in "tp"}))
            return old(hw) if old else []

        p["xao"] = grab
        return p

    simulate(pose, -2.0, dur)
    rec = [r for r in rec if r[0] >= -1e-9]
    print(f"== {name} ({dur} s)")
    for s in "tp":
        worst_d, worst_a = (0.0, 0.0), (0.0, 0.0)
        for (t0, a), (t1, b) in zip(rec, rec[1:]):
            d = math.hypot(b[s][0][0] - a[s][0][0], b[s][0][1] - a[s][0][1])
            da = abs(b[s][1] - a[s][1])
            if d > worst_d[0]:
                worst_d = (d, t1)
            if da > worst_a[0]:
                worst_a = (da, t1)
        print(f"  tay {s}: bước dời cổ tay lớn nhất {worst_d[0]:.0f} px / bước 1/60 s (t {worst_d[1]:.3f}); "
              f"bước xoay bàn tay lớn nhất {worst_a[0]:.1f} độ / bước (t {worst_a[1]:.3f})")
    for label, tm in MARK.get(name, []):
        r = min(rec, key=lambda q: abs(q[0] - tm))
        out = []
        for s in "tp":
            (x, y), ang = r[1][s]
            out.append(f"{s}: cổ tay ({x:.0f}, {y:.0f}) hướng ngón {((ang + 180) % 360) - 180:.0f}°")
        print(f"  {label:18s} t {r[0]:.3f}  " + " | ".join(out))
    return rec


if __name__ == "__main__":
    for n in (sys.argv[1:] or ["rl_invite", "rl_no_more", "rl_spin", "rl_watch", "rl_point"]):
        measure(n)
