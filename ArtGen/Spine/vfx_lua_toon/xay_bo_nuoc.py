# -*- coding: utf-8 -*-
"""Dựng trang xem BỘ NƯỚC (artifact xem trên điện thoại): chép khung frames/<tên> vào <thư_mục>/frames, ghi <thư_mục>/bo_nuoc.html
(cấu hình lấy từ frames/manifest.json) và <thư_mục>/files.json (bản đồ tệp để đăng).
    py -3 -I xay_bo_nuoc.py <thư_mục_ra>
"""
import json
import os
import shutil
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
MAN = json.load(open(os.path.join(HERE, "frames", "manifest.json"), encoding="utf-8"))
G = 70   # px: điểm trúng cao hơn mặt đất (vũng đặt dưới chân đích); trong game đặt vũng ở chân đích
# (mã, nhãn, các bộ khung, mô tả); bộ khung: tên, hoặc dict(s=tên, label, dx, dy = neo bộ này so với neo bộ đầu (px), d = trễ (khung))
FX = [
    # ---- BỘ NƯỚC v2 (người dùng 2026-11-24: "dựa theo shader của họ rồi tự build cầu nước, tia nước,... tất cả theo ý mình, lốc nước ok
    # rồi"): chất nước chung lam nhạt + bọt trắng, khối cel 3 dải + mép lam sâu, cầu / thương bằng metaball (đuôi liền thân), tan theo
    # ngưỡng × mặt nạ mềm, dải hai ngưỡng dọc ống (học shader repo abitofgamedev/water_vfx). Vũng dưới chân đích ghép trễ.
    ("cau", "Cầu nước", ["cau_nem"], "Lặp 1 s. n_cau, n_dan, n_ngoc. Cầu nước metaball rung như thạch (cục nhỏ chạy vòng trong lòng làm mặt cầu phồng xẹp), bay sang phải; ĐUÔI LIỀN THÂN thon dần, chót tự thắt thành giọt. Lam nhạt, khối cel 3 dải, mép lam sâu, vệt bọt trắng xoay. Neo tâm cầu."),
    ("cauvo", "Cầu vỡ", [dict(s="cau_vo2", label="Toé"), dict(s="vung_nuoc", label="Vũng", dx=10, dy=G, d=2)],
     "Một lượt 1 s. Cầu / đạn nước trúng: cầu metaball bẹp lại rồi vỡ lấm tấm, vương miện ngửa về người đánh, chấm toé, vệt, giọt; vũng dưới chân đích."),
    ("tia", "Tia nước", [dict(s="tia_nuoc2", label="Tia"), dict(s="vung_nuoc", label="Vũng", dx=493, dy=G, d=3)],
     "Một lượt 1,6 s. n_tia. Ống nước thẳng hơi gợn: đầu tia tới đích trong 0,1 s rồi PHÌNH (vượt cỡ, phập phồng), vệt nước chảy nhanh dọc ống, đuôi tan rách từ miệng (dải hai ngưỡng); đích toé ngược về người bắn liên tục; vũng dưới chân đích. Neo miệng, điểm chạm 493 px."),
    ("tong", "Tia ống", [dict(s="tia_ong", label="Ống"), dict(s="vung_nuoc", label="Vũng", dx=493, dy=90, d=7)],
     "Một lượt 1,6 s. Ống nước vòng cung từ miệng sang đích: hiện từ miệng (0–0,3 s), giữ, tan rách từ miệng (1,0–1,38 s); đích toé lặp; vũng dưới chân đích."),
    ("roi", "Roi nước", [dict(s="roi_nuoc", label="Roi"), dict(s="vung_nuoc", label="Vũng", dx=493, dy=90, d=8)],
     "Một lượt 1 s. Một đoạn nước chạy dọc vòng cung tới đích (0,34 s) rồi toé; vũng dưới chân đích."),
    ("toe", "Toé nước", [dict(s="toe_nuoc2", label="Toé"), dict(s="vung_nuoc", label="Vũng", dx=10, dy=G, d=1)],
     "Một lượt 1 s. n_va (lao, húc, quật), đạn trúng thân: chớp sao, 2 vương miện ngửa ngược về người đánh (ngón nước mảnh dần rồi đứt thành giọt), chấm toé, vệt, giọt; vũng dưới chân đích. Neo điểm trúng."),
    ("tdat", "Toé đất", ["toe_dat"], "Một lượt 1 s. Đòn nện / cầu rơi xuống đất: 2 vành vương miện thấp loang trên đất tan theo ngưỡng, chấm toé, vệt, giọt, 2 vũng. Neo tâm trên đất."),
    ("thuong", "Thương nước", ["thuong_nuoc2"], "Lặp 0,5 s. n_thuong. Mũi nước metaball vuốt nhọn về phải, vệt bọt xoắn quanh trục, đuôi liền thân xoắn nhẹ thon dần, giọt văng sau. Neo gốc mũi."),
    ("song", "Sóng", ["song_cuon"], "Một lượt 1,1 s. n_song. Tấm nước cong chân thon, mặt lõm có vệt nước quay về đích (phải), mào bọt trắng cuộn úp lên mặt sóng; tan từ chân lên thành răng giọt, mào tan sau cùng rồi rơi giọt. Lam nhạt + bọt trắng. Neo chân sóng (phía đích)."),
    ("loc", "Lốc nước", ["loc_nuoc"], "Một lượt 2 s. n_loc / n_voi. Giữ nguyên (người dùng: lốc nước ok rồi)."),
    ("phun", "Mạch phun", ["mach_phun2"], "Một lượt 1,6 s. n_xoay. Vành toé + vũng ở chân, cột nước dựng từ đất (phình rồi phập phồng, vệt nước chảy lên), đỉnh vương miện toé ngửa lên + giọt rơi quanh cột, rồi cột sụp từ trên xuống. Neo chân cột."),
]
UPP, HX = 15.2 / 750, 10.0 - 0.12
DX = round(HX / UPP)
os.makedirs(os.path.join(OUT, "frames"), exist_ok=True)
files, cfg = {}, []
for code, label, sets, desc in FX:
    ss = []
    for it in sets:
        it = dict(s=it) if isinstance(it, str) else dict(it)
        s_ = it["s"]
        m = MAN[s_]
        # gộp cả bộ thành MỘT tờ khung (lưới ≤ 4096 px mỗi cạnh): ít tệp, điện thoại tải nhanh; trang cắt khung theo ô
        cols = max(1, min(m["count"], 4000 // m["w"]))
        rows = (m["count"] + cols - 1) // cols
        nm = f"{s_}.png"
        if "frames/" + nm not in files:
            sheet = Image.new("RGBA", (cols * m["w"], rows * m["h"]), (0, 0, 0, 0))
            for i in range(m["count"]):
                im = Image.open(os.path.join(HERE, "frames", s_, f"{s_}_{i:02d}.png")).convert("RGBA")
                sheet.paste(im, ((i % cols) * m["w"], (i // cols) * m["h"]))
            sheet.save(os.path.join(OUT, "frames", nm), optimize=True)
            files["frames/" + nm] = "frames/" + nm
        dx = DX if it.get("dx") == "DX" else it.get("dx", 0)
        ss.append(dict(sheet=nm, cols=cols, n=m["count"], w=m["w"], h=m["h"], ax=m["anchor"][0], ay=m["anchor"][1], loop=m["loop"],
                       label=it.get("label", label), dx=dx, dy=it.get("dy", 0), d=it.get("d", 0)))
    # khung chung bao mọi bộ (neo bộ đầu = gốc), mỗi bộ vẽ tại (ox + dx − ax, oy + dy − ay)
    x0 = min(t["dx"] - t["ax"] for t in ss)
    x1 = max(t["dx"] - t["ax"] + t["w"] for t in ss)
    y0 = min(t["dy"] - t["ay"] for t in ss)
    y1 = max(t["dy"] - t["ay"] + t["h"] for t in ss)
    canvas = dict(w=x1 - x0, h=y1 - y0, ox=-x0, oy=-y0)
    for t in ss:
        t["px"], t["py"] = canvas["ox"] + t["dx"] - t["ax"], canvas["oy"] + t["dy"] - t["ay"]
    cfg.append(dict(code=code, label=label, desc=desc, sets=ss, canvas=canvas, n=max(t["n"] + t["d"] for t in ss), loop=ss[0]["loop"]))
tpl = open(os.path.join(HERE, "bo_nuoc_tpl.html"), encoding="utf-8").read()
open(os.path.join(OUT, "bo_nuoc.html"), "w", encoding="utf-8").write(tpl.replace("/*CFG*/[]", json.dumps(cfg, ensure_ascii=False)))
json.dump(files, open(os.path.join(OUT, "files.json"), "w"))
print("ok", len(files), "khung")
