# -*- coding: utf-8 -*-
"""Vá một trường của khối `game` trong file .atomik ĐÃ XUẤT (và <mã>_game.json cạnh nó) mà không dựng lại rig. Dùng khi chỉ thêm cờ
cho game (ví dụ farAim) còn xương, lưới, clip, atlas không đổi. Script rig vẫn phải khai cùng giá trị để lần xuất sau ra y hệt.

    py -3 -I ArtGen/Spine/quai/va_game.py <thư mục rig> <mã> <khoá> '<json giá trị>' [khoá đứng trước]
    py -3 -I ArtGen/Spine/quai/va_game.py ArtGen/Spine/inbox/chim_la_1/rig chim_la_1 farAim '["cast"]' far
"""
import gzip
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8")


def chen(g, khoa, gia_tri, sau):
    if khoa in g or sau not in g:
        g[khoa] = gia_tri
        return g
    g2 = {}
    for k, v in g.items():
        g2[k] = v
        if k == sau:
            g2[khoa] = gia_tri
    return g2


def va(thu_muc, ma, khoa, gia_tri, sau):
    path = os.path.join(thu_muc, ma + ".atomik")
    raw = open(path, "rb").read()
    if raw[:4] != b"ATMK":
        raise SystemExit("không phải .atomik: " + path)
    body = gzip.decompress(raw[6:])
    n = struct.unpack("<I", body[:4])[0]
    js = json.loads(body[4:4 + n].decode("utf-8"))
    if js.get("game", {}).get(khoa) == gia_tri:
        print(f"{path}: {khoa} đã đúng, không đổi")
    else:
        js["game"] = chen(js.get("game") or {}, khoa, gia_tri, sau)
        out = json.dumps(js, ensure_ascii=False, separators=(",", ":")).encode("utf-8")      # như atomik.convert
        with open(path, "wb") as f:
            f.write(raw[:6] + gzip.compress(struct.pack("<I", len(out)) + out + body[4 + n:], 9))
        print(f"{path}: đã vá game.{khoa} = {gia_tri} ({len(raw)} -> {os.path.getsize(path)} byte)")
    gp = os.path.join(thu_muc, ma + "_game.json")
    if os.path.exists(gp):
        g = json.load(open(gp, encoding="utf-8"))
        if g.get(khoa) != gia_tri:
            with open(gp, "w", encoding="utf-8") as f:
                f.write(json.dumps(chen(g, khoa, gia_tri, sau), ensure_ascii=False, indent=1))
            print(f"{gp}: đã vá")


if __name__ == "__main__":
    a = sys.argv[1:]
    va(a[0], a[1], a[2], json.loads(a[3]), a[4] if len(a) > 4 else "")
