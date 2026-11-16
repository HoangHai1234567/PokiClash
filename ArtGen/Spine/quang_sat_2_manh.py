# -*- coding: utf-8 -*-
"""Tinh linh quặng sắt DẠNG 2 (quang_sat_2): mảnh "đúng chỗ, đúng cỡ" từ concept đã duyệt (inbox/quang_sat_2/tai_ve/L1_duyet.png = L1_B,
người dùng chọn 2026-11-16: đá bazan có mạch quặng cam, mày đá, chùm năm gai hematit đỏ gỉ, tay là tinh thể hematit to). Cùng khung với dạng 1
(cùng rig monster_3371) nên dùng lại các hàm của quang_sat_manh.py, chỉ đổi nhóm mảnh và thư mục.

Mảnh: longdan_9 thân (KHÔNG mắt) M1; longdan_4 gai giữa, gai_t / gai_p gai ngoài trái / phải, longdan_1 / longdan_0 tay trái / phải M2;
longdan_3 / longdan_2 gai trong trái / phải M3; mắt mở cắt thẳng từ concept; mắt nhắm, mắt ngủ, gò, hố lấy của dạng 1 (cùng chỗ).

    quang_sat_2_manh.py prompt | mat | cat [nhóm] | chep1 | ghep
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quang_sat_manh as M  # noqa: E402

BASE2 = os.path.join(HERE, "inbox", "quang_sat_2")
TAI2 = os.path.join(BASE2, "tai_ve")
M.CONCEPT = os.path.join(TAI2, "L1_duyet.png")
M.MANH = os.path.join(BASE2, "manh")
M.GUI = os.path.join(HERE, "gui_gpt", "quang_sat_2")
M.ANH1 = ("the APPROVED picture of our character, 1536x1024, white background: a heavy round dark BASALT dome spirit with three thin flat "
          "orange ore seams, a thick rock brow ridge over a dark face band with two upright cyan oval eyes, two small rusty-red nubs above "
          "the brow, a cluster of FIVE rusty-red hematite crystal spikes with steel-grey ridge lines on its head (a tall one in the middle, "
          "two on each side) and two floating rusty-red crystals as its hands (a long one at the lower left, a shorter one at the lower "
          "right). Hand-drawn: wobbly dark-brown ink line, crayon hatching, flat colours.")
M.NHOM = {
    "M1": [("longdan_9", "the dark basalt dome BODY with its orange seams, its thick rock brow ridge, the two rusty-red nubs and the dark face band",
            "the parts of the dome covered by the five red spikes and the two red hands must be drawn: a complete smooth round dome with its "
            "full outline (the top of the dome under the spikes, the lower left edge under the long left crystal, the lower right edge under "
            "the right crystal), the orange seams continuing where they were hidden; the dark face band keeps exactly its shape but WITHOUT "
            "the two eyes: where the eyes were, the band is plain flat dark charcoal like the rest of the band")],
    "M2": [("longdan_4", "the TALL red spike in the MIDDLE of the head", "complete it into ONE closed shape: its lower end ends where it meets "
                                                                          "the dome, as in image 1"),
           ("gai_t", "the SMALL red spike at the far LEFT edge of the head (the outermost left one)", "complete it into one closed shape"),
           ("gai_p", "the SMALL red spike at the far RIGHT edge of the head (the outermost right one)", "complete it into one closed shape"),
           ("longdan_1", "the LONG red crystal floating at the lower LEFT (a hand)", "complete it into one closed double-pointed shape"),
           ("longdan_0", "the red crystal floating at the lower RIGHT (a hand)", "complete it into one closed double-pointed shape")],
    "M3": [("longdan_3", "the red spike on the upper LEFT of the head, between the middle spike and the far-left spike",
            "complete it into one closed shape"),
           ("longdan_2", "the red spike on the upper RIGHT of the head, between the middle spike and the far-right spike",
            "complete it into one closed shape")],
}
M.PHU = {}
M.DAT = {}
M.THU_TU = ["longdan_0", "longdan_9", "longdan_8", "longdan_7", "longdan_4", "longdan_3", "longdan_2", "gai_t", "gai_p", "longdan_1"]
# hộp từng mảnh trên concept dạng 2 (px) để cắt gán cụm (đo trên L1_B)
HOP2 = {"longdan_4": (735, 30, 970, 480), "longdan_3": (525, 195, 695, 430), "longdan_2": (995, 195, 1170, 430),
        "gai_t": (380, 365, 550, 535), "gai_p": (1130, 380, 1280, 535), "longdan_1": (230, 610, 520, 925), "longdan_0": (1185, 640, 1350, 925)}
_hop = M.hop_goc


def hop_goc():
    h = _hop()
    h.update({k: list(map(float, v)) for k, v in HOP2.items()})
    return h


M.hop_goc = hop_goc


def moi_nhat(ten):
    fs = sorted([f for f in os.listdir(TAI2) if (f == ten + ".png" or f.startswith(ten + "_")) and f.endswith(".png")],
                key=lambda f: os.path.getmtime(os.path.join(TAI2, f)))
    return os.path.join(TAI2, fs[-1]) if fs else None


def luu(ten):
    out = os.path.join(TAI2, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {M.Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


M.moi_nhat, M.luu = moi_nhat, luu


def chep1():
    """mắt nhắm, mắt ngủ, gò, hố của dạng 1 (cùng chỗ trên cùng khung) chép sang manh dạng 2."""
    os.makedirs(M.MANH, exist_ok=True)
    m1 = os.path.join(HERE, "inbox", "quang_sat_1", "manh")
    D1 = json.load(open(os.path.join(m1, "dat.json")))
    D2 = M.nap_dat()
    for t in ("longdan_5", "longdan_6", "ngu_t", "ngu_p", "go_dat", "ho"):
        shutil.copy(os.path.join(m1, t + ".png"), os.path.join(M.MANH, t + ".png"))
        D2[t] = dict(D1[t], nguon="dạng 1")
    M.ghi_dat(D2)
    print("chép từ dạng 1:", "longdan_5 longdan_6 ngu_t ngu_p go_dat ho")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "prompt":
        M.prompt()
    elif cmd == "mat":
        M.mat()
    elif cmd == "cat":
        M.cat(sys.argv[2:] or None)
    elif cmd == "chep1":
        chep1()
    elif cmd == "ghep":
        M.ghep()
    else:
        print(__doc__)
