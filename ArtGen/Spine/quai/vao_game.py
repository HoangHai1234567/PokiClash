"""Đưa các dạng tướng .atomik đã NHẬN của lô 10 tướng mới đảo Thủy vào Assets (bước vào game, 2026-11-11).

Đọc ArtGen/Spine/quai/da_nhan.json, mảng "nhan" (Claude điều phối thêm dòng khi rig đạt). Mỗi dòng:
    {"id": "ti_tach", "dang": [
        {"nguon": "ArtGen/Spine/inbox/tm01_1/rig", "atomik": "tm01_1.atomik", "dich": "ti_tach_1"},
        {"nguon": "ArtGen/Spine/inbox/tm01_2/rig", "atomik": "tm01_2.atomik", "dich": "ti_tach_2"}]}
  - nguon: thư mục rig (tương đối gốc repo); atomik: tên file trong đó (bỏ trống: file .atomik duy nhất trong thư mục);
    chan_dung: tên ảnh chân dung (mặc định chan_dung.png); dich: tên dạng = khoá "aola" trong heroes.json (<id>_<k>).
Với mỗi dạng: chép <nguon>/<atomik> -> Assets/03 Art/Heroes/Resources/<dich>/<dich>.atomik và chân dung ->
<dich>_portrait.png (vuông 512; khác cỡ thì thu vào khung 512 trong suốt). Chỉ ghi hai file đó; file khác trong thư mục đích
(<dich>.asset do menu Unity dựng, .meta) không đụng. Đích đã có và giống hệt thì giữ; khác thì ghi đè đúng file đó (báo "cập nhật").
Kiểm .atomik: đầu "ATMK", giải gzip, JSON có khối `game` (fps, height, hitClips/hitTimes, muzzle, move, shadow...), đủ clip
(idle, attack, cast, skill, hit, appear, die; evolve trừ dạng cuối; aura tuỳ), xương move / slot shadow có thật. Dạng lỗi nặng
(không đọc được, thiếu `game`, thiếu idle) thì không chép.

    py -3 -I ArtGen/Spine/quai/vao_game.py            kiểm rồi chép các dạng trong "nhan"
    py -3 -I ArtGen/Spine/quai/vao_game.py --kiem     chỉ kiểm, không chép
    py -3 -I ArtGen/Spine/quai/vao_game.py --vi-du    kiểm mục "_vi_du" (luôn chỉ kiểm)

Sau khi chép (trong Unity, Claude điều phối): menu "PokiClash/Nhập dữ liệu" rồi "PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng"
(dựng <dich>.asset, prefab tướng mới), soi bằng "PokiClash/Tướng/Chụp thử dạng .atomik (mọi clip)". Xem VAO_GAME.md.
"""
import gzip
import io
import json
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
RES = os.path.join(ROOT, "Assets", "03 Art", "Heroes", "Resources")
HEROES = os.path.join(ROOT, "Assets", "02 Data", "Json", "heroes.json")
DA_NHAN = os.path.join(HERE, "da_nhan.json")
LO = ["ti_tach", "thach_giai", "ca_den", "ha_ba", "so_ngoc", "giong_bao", "lien_kinh", "uyen_xa", "han_ngac", "hai_long"]
NEED_CLIPS = ["idle", "attack", "cast", "skill", "hit", "appear", "die"]
PORTRAIT = 512


def read_atomik(path):
    """trả (json rig, số byte PNG atlas, (rộng, cao) atlas, phiên bản file)"""
    raw = open(path, "rb").read()
    if raw[:4] != b"ATMK":
        raise ValueError("không có đầu ATMK")
    ver = struct.unpack("<H", raw[4:6])[0]
    body = gzip.decompress(raw[6:])
    n = struct.unpack("<I", body[:4])[0]
    rig = json.loads(body[4:4 + n].decode("utf-8"))
    m = struct.unpack("<I", body[4 + n:8 + n])[0]
    png = body[8 + n:8 + n + m]
    wh = struct.unpack(">II", png[16:24]) if png[:8] == b"\x89PNG\r\n\x1a\n" else (0, 0)
    return rig, len(png), wh, ver


def png_size(path):
    b = open(path, "rb").read(24)
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", b[16:24])


def portrait_bytes(path):
    """ảnh chân dung vuông 512 (giữ nguyên byte nếu đã đúng cỡ)"""
    wh = png_size(path)
    if wh == (PORTRAIT, PORTRAIT):
        return open(path, "rb").read(), "512"
    from PIL import Image  # chỉ cần khi phải đổi cỡ
    im = Image.open(path).convert("RGBA")
    im.thumbnail((PORTRAIT, PORTRAIT), Image.LANCZOS)
    out = Image.new("RGBA", (PORTRAIT, PORTRAIT), (0, 0, 0, 0))
    out.paste(im, ((PORTRAIT - im.width) // 2, PORTRAIT - im.height))  # chân sát đáy như khung gốc, giữa ngang
    buf = io.BytesIO()
    out.save(buf, "PNG", optimize=True)
    return buf.getvalue(), f"{wh[0]}x{wh[1]}->512" if wh else "đổi về 512"


def check_rig(rig, last_form):
    """trả (lỗi nặng[], cảnh báo[], tóm tắt)"""
    err, warn = [], []
    clips = [a.get("name") for a in rig.get("anims", [])]
    bones = {b.get("name") for b in rig.get("bones", [])}
    slots = {s.get("name") for s in rig.get("slots", [])}
    g = rig.get("game")
    if "idle" not in clips:
        err.append("thiếu clip idle")
    for c in NEED_CLIPS:
        if c != "idle" and c not in clips:
            warn.append(f"thiếu clip {c}")
    if not last_form and "evolve" not in clips:
        warn.append("thiếu clip evolve (không phải dạng cuối)")
    if last_form and "evolve" in clips:
        warn.append("dạng cuối có clip evolve (thừa)")
    if not g:
        err.append("thiếu khối game")
        g = {}
    else:
        if not g.get("height") or g["height"] <= 0:
            err.append("game.height trống")
        hc, ht = g.get("hitClips") or [], g.get("hitTimes") or []
        if len(hc) != len(ht):
            err.append(f"hitClips {len(hc)} khác hitTimes {len(ht)}")
        for c in ("attack", "cast", "skill"):
            if c not in hc:
                warn.append(f"game.hitClips thiếu {c}")
        for c, t in zip(hc, ht):
            a = next((x for x in rig.get("anims", []) if x.get("name") == c), None)
            if a is None:
                warn.append(f"hitClips có {c} nhưng rig không có clip đó")
            elif not (0 < t < a.get("dur", 0)):
                warn.append(f"khung trúng {c} {t}s ngoài clip ({a.get('dur')}s)")
        mv = g.get("move") or "move"
        if mv not in bones:
            warn.append(f"game.move '{mv}' không có xương đó")
        sh = g.get("shadow")
        if sh and sh not in slots:
            warn.append(f"game.shadow '{sh}' không có slot đó")
        mz = g.get("muzzle") or []
        if len(mz) not in (0, 2):
            warn.append(f"game.muzzle {mz} phải 2 số")
    n_ev = sum(len(a.get("ev") or []) for a in rig.get("anims", []))
    summary = {
        "xương": len(bones), "slot": len(slots), "hình": len(rig.get("atts", [])), "mặt nạ": len(rig.get("masks") or []),
        "clip": ",".join(clips), "sự kiện": n_ev, "fps": g.get("fps"), "cao": g.get("height"),
        "trúng": dict(zip(g.get("hitClips") or [], g.get("hitTimes") or [])), "miệng bắn": g.get("muzzle"),
        "move": g.get("move"), "shadow": g.get("shadow"), "va chạm": g.get("impactClips"),
    }
    return err, warn, summary


def same(path, data):
    return os.path.exists(path) and open(path, "rb").read() == data


def main():
    kiem = "--kiem" in sys.argv or "--vi-du" in sys.argv
    key = "_vi_du" if "--vi-du" in sys.argv else "nhan"
    cfg = json.load(open(DA_NHAN, encoding="utf-8"))
    rows = cfg.get(key) or []
    if isinstance(rows, dict):
        rows = [rows]
    heroes = {h["id"]: h for h in json.load(open(HEROES, encoding="utf-8"))["heroes"]}
    print(f"da_nhan.json [{key}]: {len(rows)} dòng{' (chỉ kiểm)' if kiem else ''}")
    table, bad = [], 0
    for row in rows:
        hid = row.get("id")
        h = heroes.get(hid)
        forms = [f["aola"] for f in h["forms"]] if h else []
        if not h:
            print(f"  ! {hid}: không có trong heroes.json (chạy tuong_moi_thuy.py trước)")
            bad += 1
            continue
        for d in row.get("dang", []):
            dich = d.get("dich", "")
            src_dir = os.path.normpath(os.path.join(ROOT, d.get("nguon", "")))
            status, notes = "", []
            if not re.fullmatch(re.escape(hid) + r"_\d", dich) or dich not in forms:
                print(f"  ! {hid} -> {dich}: tên đích phải là một dạng của {hid} trong heroes.json ({', '.join(forms)})")
                bad += 1
                continue
            last = dich == forms[-1]
            name = d.get("atomik")
            if not name and os.path.isdir(src_dir):
                cand = [f for f in os.listdir(src_dir) if f.endswith(".atomik")]
                name = cand[0] if len(cand) == 1 else None
                if len(cand) > 1:
                    notes.append(f"nhiều .atomik ({', '.join(cand)}): ghi rõ 'atomik'")
            src = os.path.join(src_dir, name) if name else None
            por = os.path.join(src_dir, d.get("chan_dung", "chan_dung.png"))
            if not src or not os.path.exists(src):
                table.append((dich, d.get("nguon"), "-", "-", "THIẾU .atomik"))
                bad += 1
                continue
            try:
                rig, png_n, atlas_wh, ver = read_atomik(src)
            except Exception as e:  # noqa: BLE001
                table.append((dich, d.get("nguon"), "-", "-", f"HỎNG .atomik: {e}"))
                bad += 1
                continue
            err, warn, summ = check_rig(rig, last)
            kb = os.path.getsize(src) / 1024
            if not os.path.exists(por):
                err.append(f"thiếu chân dung {os.path.basename(por)}")
            print(f"  {dich} <- {os.path.relpath(src, ROOT)} ({kb:.0f} KB, ATMK v{ver}, atlas {atlas_wh[0]}x{atlas_wh[1]})")
            print("     " + "; ".join(f"{k} {v}" for k, v in summ.items()))
            for w in warn:
                print(f"     cảnh báo: {w}")
            for e in err:
                print(f"     LỖI: {e}")
            if err:
                table.append((dich, d.get("nguon"), f"{kb:.0f} KB", "-", "BỎ QUA (lỗi)"))
                bad += 1
                continue
            data = open(src, "rb").read()
            pdata, pnote = portrait_bytes(por)
            out_dir = os.path.join(RES, dich)
            out_a = os.path.join(out_dir, f"{dich}.atomik")
            out_p = os.path.join(out_dir, f"{dich}_portrait.png")
            st = []
            for path, blob, label in ((out_a, data, "atomik"), (out_p, pdata, "chân dung")):
                if same(path, blob):
                    st.append(f"{label} giữ")
                    continue
                verb = "cập nhật" if os.path.exists(path) else "thêm"
                if not kiem:
                    os.makedirs(out_dir, exist_ok=True)
                    with open(path, "wb") as f:
                        f.write(blob)
                st.append(f"{label} {verb}{' (sẽ)' if kiem else ''}")
            table.append((dich, d.get("nguon"), f"{kb:.0f} KB", pnote, ", ".join(st) + (f"; {len(warn)} cảnh báo" if warn else "")))
    if table:
        print("\n  dạng | nguồn | .atomik | chân dung | trạng thái")
        for r in table:
            print("  " + " | ".join(str(x) for x in r))
    # tiến độ cả lô: dạng nào của 10 tướng mới đã có trong Resources
    have, miss = [], []
    for hid in LO:
        for f in (heroes[hid]["forms"] if hid in heroes else []):
            ok = os.path.exists(os.path.join(RES, f["aola"], f"{f['aola']}.atomik"))
            (have if ok else miss).append(f["aola"])
    print(f"\n  lô Thủy trong Resources: {len(have)}/{len(have) + len(miss)} dạng" + (f"; còn thiếu: {', '.join(miss)}" if miss else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
