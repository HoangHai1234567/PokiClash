# -*- coding: utf-8 -*-
"""Gói GPT vẽ ba tờ mảnh DẠNG 2 của xương rồng tròn (xuong_rong, cùng rig monster_3229 với dạng 1). Concept dạng 2 đã duyệt
2026-11-12 (`inbox/xuong_rong_2/tai_ve/L1_duyet.png`: lục sẫm, gai nhỏ nhọn trên múi, nanh dài lởm chởm, vành hoa lưỡi dao; gai lớn kem
trơn vì người dùng dặn "bỏ màu hồng ở gai dạng 2 đi"). Gai lớn, gai dài, ụ đất dùng lại của dạng 1: không có tờ gai.

    XR_DANG=2 py -3 -I ArtGen/Spine/xuong_rong.py nhom_part
    py -3 -I ArtGen/Spine/build_xuong_rong_2.py
    py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/xuong_rong_2/luot_2_manh_<A|B|C>.txt
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_xuong_rong as B1  # noqa: E402

K = 2
Wp = B1.Wp
MAU2 = ("COLOURS (exactly as on image 1): dark cactus green skin #259B51; rib lines very dark green #034B26; small spikes, fangs and "
        "toe nubs warm cream #FEE79B; flower petals crimson pink #F02565 with a darker #8E1840 centre line; inside of the mouth dark "
        "wine red #940D36; ink #2B2118.")


def _o(khung, ten):
    v = khung[ten]
    return f"centre at about x = {v['x'] + v['w'] // 2}, y = {v['y'] + v['h'] // 2}, about {v['w']} px wide and {v['h']} px tall"


def main():
    duyet = os.path.join(B1.save_dir(K), "L1_duyet.png")
    if not os.path.exists(duyet):
        raise SystemExit("chưa có concept dạng 2 đã duyệt")
    Kh = {to: json.load(open(os.path.join(B1.mau_dir(K), f"part_{to}.json"), encoding="utf-8")) for to in "ABC"}
    A, B, C = Kh["A"], Kh["B"], Kh["C"]
    noi = {
        "A": ("three big parts of the head-body: the ball, the skin ring around the mouth, the inside of the mouth", 4, True,
              ["- THE BALL (left; " + _o(A, "P_shenti") + "): the COMPLETE round barrel-cactus body as if the mouth, the arms, the "
               "legs, the big thorns and the flower had all been taken off: one even DARK cactus green ball; bold very-dark-green "
               "RIB lines (about 5 px) run from the top of the ball to the bottom like lines of longitude, exactly where the guide "
               "shows them; at each small cream triangle of the guide draw one tiny SHARP cream spike (a little cone about 20 px "
               "long with a thin ink outline) pointing the way the guide shows. There is NO mouth, no hole and no empty patch on "
               "this ball: the ribs and the green cover all of it. A closed ink outline all around the ball.",
               "- THE SKIN RING (middle; " + _o(A, "P_zuichun") + "): a ring of the same dark green skin with a big empty hole (the "
               "mouth opening); the hole stays PURE WHITE. Draw a bold ink line ONLY along the edge of the hole, all the way "
               "around it. The OUTER edge of the ring has NO ink outline at all: there the green, with its crayon hatching, simply "
               "ends at the silhouette edge (this ring will be laid on the ball and must melt into it; it is not a lip). No rib "
               "lines, no spikes on the ring.",
               "- THE INSIDE OF THE MOUTH (right; " + _o(A, "P_kouqiang") + "): one flat blob of dark wine red with crayon hatching, "
               "filling its silhouette. No ink outline needed, no teeth, no tongue, no throat, no darker area."]),
        "B": ("three parts: the upper row of fangs, the lower row of fangs and the flower crown", 6, False,
              ["- UPPER FANGS (top left; " + _o(B, "P_shangya") + "): the guide shows the SHORT fangs of the first stage. Keep the "
               "cream band (its upper, wavy edge and its two ends) exactly where it is and at the same size, and REDRAW THE FANGS "
               "that hang down from it LONGER, SHARPER and more jagged, as on image 1: five pointed fangs, each about 40 px longer "
               "than on the guide (they grow DOWNWARD into the white space under the band, never sideways beyond the ends of the "
               "band and never upward), the second and the fourth long like tusks, every fang ending in a sharp point. Flat cream; "
               "closed ink outline around the whole shape.",
               "- LOWER FANGS (top right; " + _o(B, "P_xiaya") + "): the same for the lower row: keep the cream crescent band "
               "(its lower, round edge and its two ends) exactly where it is, and redraw the fangs that rise from it LONGER and "
               "SHARPER: five pointed fangs, each about 40 px longer than on the guide (they grow UPWARD into the white space above "
               "the band), two of them long like tusks. Flat cream; closed ink outline around the whole shape.",
               "- FLOWER CROWN (bottom left; " + _o(B, "P_toufa") + "): SEVEN long, narrow, pointed petals like blades, standing "
               "side by side in a fan exactly as on the guide (the middle petals in front of the outer ones), crimson pink, each "
               "with its own ink outline and one darker centre line; the curved lower edge is the base of the crown. Keep every "
               "petal where the guide puts it (same base point, same direction, same length); all seven petals are whole, none "
               "is cut off."]),
        "C": ("nine green limb parts: arm segments, fists, thighs and feet", 6, True,
              ["- SEVEN PLAIN GREEN PARTS: each is ONE plain rounded segment of an arm or a leg (upper arm, forearm, round fist, "
               "thigh), exactly its silhouette: flat DARK cactus green, closed ink outline, nothing on it: no thorns, no ribs, no "
               "spikes, no fingers.",
               "- TWO FEET (the two parts with small cream shapes; " + _o(C, "P_tuiL2") + " and " + _o(C, "P_tuiR2") + "): a "
               "small dark green foot with TWO little cream toe nubs at its bottom edge, where the guide shows them, each nub "
               "with a thin ink outline; closed ink outline around the foot."]),
    }
    out = []
    for to, (gi, net, sat, ds) in noi.items():
        luu = os.path.join(B1.save_dir(K), f"N_{to}.png")
        p = os.path.join(B1.pk(K), f"luot_2_manh_{to}.txt")
        luat = B1.PART_RULE if sat else (
            "HOW TO DRAW THE PARTS: image 2 is a stiff computer-made sheet: each part lies in its exact place. Redraw the sheet "
            "cleanly in the hand-drawn style of image 1. Keep every part in the SAME POSITION, at the same size and in the same "
            "orientation on the canvas; do NOT move, rotate, resize, merge, add or remove parts; do not assemble them into a "
            "creature; keep the white gaps between the parts. Change the shapes only where a part below says so. Take from image "
            "1 the look: the wobbly dark-brown ink pen line (#2B2118), the loose diagonal crayon hatching, the exact colours.")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(duyet)}: the APPROVED creature (second evolution stage), 1536x1024, white background: a round "
             "dark-green cactus-ball monster with no face, a huge grin full of long cream fangs with a dark wine-red inside, a "
             "crown of seven blade-like crimson-pink petals, two arms with spiked fists, two short legs, small cream spikes on the "
             "ball. It gives the design, the colours, the ink line and the crayon hatching.",
             f"image 2 = {Wp(os.path.join(B1.mau_dir(K), f'part_{to}.png'))}: PART SHEET GUIDE, 1536x1024, white background: {gi}, "
             "each lying in its exact place on the canvas. It gives, for every part, the size, the orientation and the position.",
             "", f"SAVE: save it as a PNG to {Wp(luu)}",
             f"If a file with that name already exists, save as N_{to}_2.png, N_{to}_3.png ... in the same folder. Do not edit, "
             "move or delete any other file.", "",
             "TASK: draw ONE part sheet, landscape 1536x1024: the SEPARATE body parts of the creature of image 1, laid out exactly "
             "as on image 2, for a 2D cut-out animation rig.", "",
             luat, "",
             f"INK OUTLINE: about {net} px thick on this canvas for every outline on this sheet (the parts are drawn enlarged), "
             "closed all the way around each part, except where a part below says it has no outline.", "",
             "THE PARTS:"] + ds + ["", MAU2, B1.PART_FLAT]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        out.append(p)
    gd = ["", "## Lượt 2: ba tờ mảnh dạng 2 theo khung part (2026-11-12, sau khi người dùng duyệt `L1_duyet.png`)", "",
          "Ảnh 1 là concept dạng 2 đã duyệt, ảnh 2 là tờ hướng dẫn (`XR_DANG=2 py -3 -I ArtGen/Spine/xuong_rong.py nhom_part`). Codex "
          f"lưu `N_A.png`, `N_B.png`, `N_C.png` vào `{Wp(B1.save_dir(K))}`. Gai lớn, gai dài, ụ đất dùng lại của dạng 1.", "",
          "| Tờ | File prompt | Tờ hướng dẫn (1536 × 1024, nền trắng) trông như thế nào |", "|---|---|---|",
          f"| A | `{Wp(out[0])}` | Quả cầu lục sẫm có múi dọc và các tam giác kem nhỏ (chỗ gai nhỏ), vành da quanh lỗ miệng chỉ viền mực "
          "ở mép lỗ, khối đỏ rượu sẫm lòng miệng |",
          f"| B | `{Wp(out[1])}` | Hai dải nanh kem của dạng 1 (nanh còn ngắn, quanh có khoảng trắng để vẽ nanh dài ra), vành hoa bảy "
          "cánh nhọn như lưỡi dao hồng đỏ |",
          f"| C | `{Wp(out[2])}` | Chín khúc tay chân lục sẫm, hai bàn chân có ngón kem |",
          "", "Kiểm (Claude tự làm): `XR_DANG=2 xuong_rong.py cat_part` in IoU (tờ A, C dưới 0,9 thì gen lại; tờ B vẽ tự do: soi "
          "dải lợi còn đúng chỗ, nanh dài ra đúng phía)."]
    hd = os.path.join(B1.pk(K), "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 2:")[0].rstrip("\n")
    open(hd, "w", encoding="utf-8", newline="\n").write(cu + "\n" + "\n".join(gd) + "\n")
    for p in out:
        print(p)


if __name__ == "__main__":
    main()
