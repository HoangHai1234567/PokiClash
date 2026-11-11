"""so_sanh.md cho dạng 1, 2 của dòng Hải Long (tm10_<k>): số xương, slot, đỉnh, tam giác, khoá, MB so với con gốc monster_3705 và
dạng 3 bản 4 (đọc stat.json + .atomik đã xuất).

    py -3 -I ArtGen/Spine/tm10_so_sanh.py 2
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import hai_long_soi as S  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")


def main(k):
    name = f"tm10_{k}"
    rig = os.path.join(HERE, "inbox", name, "rig")
    st = json.load(open(os.path.join(rig, "stat.json"), encoding="utf-8"))
    new = S.read_atomik(os.path.join(rig, name + ".atomik"))
    g = json.load(open(os.path.join(rig, name + "_game.json"), encoding="utf-8"))
    st3 = json.load(open(os.path.join(HERE, "inbox", "hai_long", "rig", "stat.json"), encoding="utf-8"))
    a3 = S.read_atomik(os.path.join(HERE, "inbox", "hai_long", "rig", "hai_long.atomik"))
    ref = json.load(open(os.path.join(S.SCAN, "info.json"), encoding="utf-8"))
    rmesh = [a for a in ref["skins"][0]["atts"] if a["type"] == "_MeshAttachment"]
    rkeys = sum(t.get("frames", 0) for a in ref["anims"] for t in a["tls"])
    mb = lambda n: f"{n / 1e6:.2f} MB"
    nb_own = sum(1 for b in json.load(open(os.path.join(rig, name + ".json"), encoding="utf-8"))["bones"] if not b["name"].startswith("n_") and b["name"] != "evo")
    ten = {2: "Hải Long Tam Thủ (dạng 2)", 1: "Hải Long Nhi (dạng 1)"}[k]
    L = [f"# {ten}: so với con gốc (monster_3705) và dạng 3 bản 4 (2026-11-11)", "",
         "Rig dựng bằng `tm10.py` trên bộ máy `hai_long.py` (giải cổ, dải lưới B-spline, râu dây mềm, băng chuyền sóng, aura); mảnh thân "
         "từ tờ M01, M02 của dạng này, hình nước dùng chung với dạng 3. **Rig gộp tiến hóa**: chứa luôn dạng sau (xương `n_*` dưới `evo` co "
         f"{g['_evolve']['tiB']}, slot ẩn mặc định) nên số dưới đây là của rig gộp; phần riêng của dạng này ghi trong ngoặc.", "",
         "| | monster_3705 (gốc) | Hải Long dạng 3 bản 4 | " + ten + " (rig gộp) |", "|---|---|---|---|",
         f"| Xương | {len(ref['bones'])} | {st3['bones']} | {st['bones']} (riêng {nb_own}) |",
         f"| Slot | {len(ref['slots'])} | {st3['slots']} | {st['slots']} (riêng {st['slots'] - st3['slots']}) |",
         f"| Đỉnh / tam giác | {sum(a['verts'] for a in rmesh)} / {sum(a['tris'] for a in rmesh)} | {st3['verts']} / {st3['tris']} | {st['verts']} / {st['tris']} (riêng {st['verts'] - st3['verts']} / {st['tris'] - st3['tris']}) |",
         f"| Clip | {len(ref['anims'])} | {st3['clips']} | {st['clips']} (7 + aura + evolve) |",
         f"| Khoá | {rkeys:,} | {st3['keys']:,} | {st['keys']:,} |",
         f"| .atomik | 3,71 MB (skel + atlas) | {mb(a3['file'])} | **{mb(new['file'])}** (json {mb(new['json'])} + png {mb(new['png'])} trước nén) |",
         f"| Atlas | 2048 × 1228 | {st3['atlas'][0]} × {st3['atlas'][1]} | {st['atlas'][0]} × {st['atlas'][1]} (gồm cả mảnh thân dạng 3) |",
         "", "## Clip", "", "| Clip | Dài (s) | Khoá |", "|---|---|---|"]
    for cn, dur in st["durs"].items():
        L.append(f"| {cn} | {dur:.2f} | {new['clips'][cn][1]:,} |")
    kh = {}
    kp = os.path.join(rig, "khop.json")
    if os.path.exists(kp):
        kh = json.load(open(kp, encoding="utf-8"))
    if k == 1:   # rig dạng 1 gộp dạng 2 (phần riêng của dạng 2 = stat dạng 2 − stat dạng 3)
        st2 = json.load(open(os.path.join(HERE, "inbox", "tm10_2", "rig", "stat.json"), encoding="utf-8"))
        own_v = st["verts"] - (st2["verts"] - st3["verts"])
    else:
        own_v = st["verts"] - st3["verts"]
    per = 5 if k == 2 else 4
    step = 1104 * 0.9 / 14 / per
    L += ["", "## Mật độ lưới theo chiều cao, khớp concept", "",
          f"- Chiều cao dáng đứng {g['height']}; đỉnh riêng của dạng {own_v} → **{own_v / g['height']:.2f} đỉnh / đơn vị cao** "
          f"(dạng 3 bản 4: {st3['verts']} / 1099,5 = {st3['verts'] / 1099.5:.2f}); cột lưới dải cổ {per}/đốt (bước ≈ {step:.0f} đơn vị ≈ "
          f"{step / g['height'] * 100:.1f}% chiều cao); mọi mảnh phủ kín (lưới ô chữ nhật trùm cả khung ảnh mảnh: hở 0 px).",
          f"- Khớp concept bằng dò tự động (`tm10_khop.py khop {k}`): đầu theo bản đồ lớp màu (tỉ lệ, góc, vị trí), chân cổ + hướng mọc "
          f"từ mặt nạ thân trên mặt nước, cổ dò (dirE, arr, ka, kb) phủ đúng thân, vòng thân / đuôi từ mặt nạ; "
          f"**IoU thân khung 0 idle vs concept (bỏ nước) = {kh.get('iou', float('nan')):.3f}**, dáng gốc không animation "
          f"{kh.get('iou_setup', float('nan')):.3f} (đích ≥ 0,9; ảnh `so_concept_iou.png`; idle giây 0 = dáng gốc từ 2026-11-11).",
          ]
    lp = os.path.join(HERE, "inbox", f"tm10_{k}", "manh_lai", "lai.json")
    if os.path.exists(lp):
        lai = json.load(open(lp, encoding="utf-8"))
        pcs = lai["pieces"]
        L += ["", "## Cách lai (2026-11-11): mảnh cắt thẳng từ concept", "",
              f"- `tm10_lai.py cat {k}`: {len(pcs)} mảnh cắt từ `tai_ve/L1_duyet.png` theo mặt nạ + hình học dò (khop.json): "
              + ", ".join(sorted(pcs)) + f". Mọi điểm thân trên mặt nước gán cho mảnh gần nhất (phủ {lai['phu']:.3f}).",
              "- Đầu: vùng mảnh đầu GPT nới xuống (hàm, họng); hàm dưới = phần dưới đường giữa khe miệng (cụm hồng lòng miệng), bản lề = mép "
              "sau khe, xương hàm dời tới bản lề, lưới hai xương (họng sát bản lề theo đầu); lòng miệng = mảng hồng phẳng đúng khe, bám đầu "
              "(hé thì lộ, khép thì hàm che). Vệt kem dính mép môi là môi (đi với hàm), râu dây chỉ tách khi là sợi rời mỏng dài.",
              "- Cổ: lưới vùng dày (`quai.luoi.luoi_vung`, bước viền 1,5% / trong 2% chiều cao con) trên hình cổ concept, trọng số B-spline "
              "chiếu lên chuỗi xương n<hid>* (đường tâm Dijkstra); slot `cc<hid>` nằm TRÊN dải cổ GPT `c<hid>` (đoạn chìm dưới mặt nước, "
              "clip appear trồi lên); cổ sau mọc thêm 32 px dưới đầu / cổ trước / mặt nước, vẽ bù inpaint.",
              "- Đuôi: chuỗi tail* dọc trục PCA của mảnh cắt; vòng thân: lưới vùng + 5 điểm điều khiển Gauss như dạng 3. Nước dùng chung dạng 3.",
              f"- Atlas chỉ chứa mảnh còn dùng; chiều cao dáng đứng = đỉnh thân concept ({lai['height_rig']}) + 60."]
    L += ["", "## Ghi chú", "",
          f"- Chiều cao dáng đứng {g['height']} (dạng sau {g['_evolve']['next']}: {g['_evolve']['height_next']}); `evo` = {g['_evolve']['tiB']}.",
          "- Dung lượng vượt đích 0,6 MB của dạng 1–2 vì rig gộp mang cả dạng sau (dạng 3 một mình 1,08 MB) để tiến hóa nối liền; phần riêng "
          "của dạng này ước ~0,45 MB (atlas thân + khoá 8 clip).",
          ("- Khung trúng: attack 0,45 (đầu d) / 0,68 (thủ lĩnh), cast 1,0 (phun, so le 0,06), skill 1,32 (gầm)." if k == 2 else
           "- Khung trúng: attack 0,45 (mổ một nhát), cast 1,0 (phun), skill 1,32 (gầm)."),
          "- Lệch nối clip đo trên ĐỈNH LƯỚI (`hai_long_soi.py lech_dinh`, mọi slot kể cả râu dây mềm): ≤ 4,4 px so với khung 0 idle; "
          "evolve kết thúc đúng dáng giây 0 idle + aura của dạng sau (khoá hằng), sai khác chỉ ở pha aura lúc game đổi sticker."]
    p = os.path.join(rig, "so_sanh.md")
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(p)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
