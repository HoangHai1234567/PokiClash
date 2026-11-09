# -*- coding: utf-8 -*-
"""Đổi mã hình 10 dòng tướng đảo Hỏa (hoặc đảo Kim với --kim) trong heroes.json sang dạng .atomik <id>_<k> (2026-11-09), chỉ
dạng đã có file Assets/03 Art/Heroes/Resources/<id>_<k>/<id>_<k>.atomik. Giữ nguyên định dạng file (indent 1, kiểu xuống dòng,
dòng cuối).

    py -3 -I ArtGen/Spine/hoa_json.py [--kim] [--dry]
Sau đó trong Unity: PokiClash/Nhập dữ liệu, rồi PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
JSON = os.path.join(ROOT, "Assets", "02 Data", "Json", "heroes.json")
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
IDS = ["su_tu_lua", "khong_lo", "kim_su", "nham_than", "nguu_quyen", "hong_lien", "giap_long", "huyen_viem", "hoa_tinh",
       "lan_hoa"]
KIM = ["bo_cap", "doc_giac", "bo_ngua", "phi_thuong", "khien_bac", "chien_than", "thiet_phu", "tam_kiem", "ung_thep",
       "kim_nghe"]
if "--kim" in sys.argv:
    IDS = KIM


def main(dry):
    d = json.load(open(JSON, encoding="utf-8"))
    changed = []
    for h in d["heroes"]:
        if h["id"] not in IDS:
            continue
        for k, f in enumerate(h["forms"], 1):
            code = f"{h['id']}_{k}"
            if not os.path.isfile(os.path.join(RES, code, code + ".atomik")):
                print("  chưa có .atomik:", code)
                continue
            if f["aola"] != code:
                changed.append(f"{f['aola']} -> {code}")
                f["aola"] = code
            if k == 1:
                h["aola"] = code
    print("\n".join(changed) or "không đổi gì")
    if not dry and changed:
        nl = "\r\n" if b"\r\n" in open(JSON, "rb").read(4096) else "\n"  # giữ kiểu xuống dòng của file (máy này CRLF)
        with open(JSON, "w", encoding="utf-8", newline=nl) as fh:
            fh.write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main("--dry" in sys.argv)
