# -*- coding: utf-8 -*-
"""Đổi HÌNH suất 8 đảo Thổ (id `ho_kim_cuong`, ải 50 "Vách Kim Cương", có bản boss) sang QUÁI BÙN (mã làm việc quai_bun, rig monster_3668 của
game tham khảo; ghi chú ArtGen/Spine/inbox/quai_bun_ghichu.md). Người dùng 2026-11-17 duyệt rig: "ok cho vào game"; tên: "đặt dễ hiểu là được".

Giữ id tướng, id thẻ, chỉ số, hiệu ứng thẻ (không đổi bản lưu), như tiền lệ 5 tướng Thổ đầu (doi_tho5.py). Đổi:
    tên     Hổ Kim Cương -> Bùn Ngoạm; danh hiệu "Quái bùn nuốt chửng"; dòng "Dòng Bùn Ngoạm"
    dạng    MỘT dạng (bảng DANG). Dạng 1 "Bùn Ngoạm Nhi" do phiên khác làm: có rig thì thêm một dòng vào đầu DANG (mã, cỡ) + gộp clip
            tiến hoá như doi_tho5_dang2.th (TIEN_HOA = True), chạy lại `lam`
    thẻ     Vuốt Kim Cương -> Đấm Bùn Trồi (claw -> fist); Kim Cương Bạo Phá -> Nuốt Chửng (crack -> fang);
            Giáp Kim Cương -> Thân Bùn (helmet -> shield); thẻ boss Kim Cương Bất Khuất -> Bùn Tái Tạo (crown -> crown)
Hiệu ứng: Assets/01 Script/Game/Battle/HatBun.cs (n_bun_danh / n_bun_troi / n_bun_ngoam), StageView.ThoFx / ThoAtk; cơ chế nuốt / nhổ đối
thủ StageViewNuot.cs (đọc sự kiện ngoam / nho + xương mieng_to của rig).

Sửa `Assets/02 Data/Json/heroes.json`, `cards.json` (từng khối: các phiên khác cũng sửa hai file này). Rồi trong Unity: "PokiClash/Nhập dữ
liệu", "PokiClash/Tướng/Gắn dạng .atomik vào prefab tướng", golden. Chạy lại không đổi gì thêm.

    py -3 -I ArtGen/Spine/quai/doi_quai_bun.py [--kiem]     heroes.json + cards.json (--kiem: chỉ báo, không ghi)
    py -3 -I ArtGen/Spine/quai/doi_quai_bun.py chep          chép rig + chân dung vào Resources/<mã>/ (<mã>.atomik, <mã>_portrait.png)
    py -3 -I ArtGen/Spine/quai/doi_quai_bun.py lam           chep + heroes.json + cards.json
    py -3 -I ArtGen/Spine/quai/doi_quai_bun.py xoa_cu [--kiem]  xoá Resources/ho_kim_cuong_1 (hình cũ) nếu không còn gì tham chiếu GUID
                                                             của nó (chạy SAU khi Unity "Gắn dạng" đã dựng lại prefab)
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doi_phap_lua as D  # noqa: E402  (khoi_tuong, dat_dang, heroes, cards, chep)

INBOX = os.path.normpath(D.INBOX)
ID = "ho_kim_cuong"
TEN = "Bùn Ngoạm"
KHAC = [("name", "Hổ Kim Cương", TEN), ("title", "Hổ vương giáp kim cương", "Quái bùn nuốt chửng"),
        ("line", "Dòng Hổ Khoan", "Dòng Bùn Ngoạm")]
THE = {"ho_kim_cuong_skill": ("Vuốt Kim Cương", "Đấm Bùn Trồi", "claw", "fist"),
       "ho_kim_cuong_ult": ("Kim Cương Bạo Phá", "Nuốt Chửng", "crack", "fang"),
       "ho_kim_cuong_pas": ("Giáp Kim Cương", "Thân Bùn", "helmet", "shield"),
       "ho_kim_cuong_boss": ("Kim Cương Bất Khuất", "Bùn Tái Tạo", "crown", "crown")}
# các dạng theo thứ tự tiến hoá: (tên dạng, mã rig = thư mục inbox/<mã>/rig và Resources/<mã>, tên file .atomik trong rig, cỡ).
# Cỡ: các tướng Thổ trước 0,88 → 1,14 theo ải (dạng cuối ải 20 Sơn Viên 1,14, ải 40 Sa Trùng 1,1); ải 50 lớn hơn. Soi trong trận 2026-11-17.
DANG = [
    (TEN, "quai_bun_1", "quai_bun.atomik", 1.16),
]
TIEN_HOA = False          # True khi DANG có từ hai rig: gộp clip evolve vào rig dạng 1 (doi_tho5_dang2.th) trước khi chép
CU = "ho_kim_cuong_1"     # hình cũ (Resources/<CU>/), bỏ hẳn sau khi prefab không còn trỏ tới
# Khối game của bản trong Resources (không sửa rig ở inbox, không xuất lại): soi trong trận 2026-11-17 thấy quả bóng + gai của chiêu cuối bị
# khung camera sticker cắt dọc (rig khai span 3,6 = ±1,8 chiều cao quanh chân; cú lao trong rig 1,23 + bóng 0,47 + gai tới 2,19 chiều cao).
# Đo mọi clip (khung bao mỗi 0,02 s): skill x tới 2,19, cast 2,25 (cast có far: sân dời khung camera theo đích nên không cần). span 4,6.
# Chỉ đổi JSON, giữ nguyên ảnh atlas từng byte. Lần xuất rig sau nên khai luôn span này trong quai_bun_game.json.
GAME = {"span": 4.6}


def sua_game(b):
    """bytes .atomik → bytes với khối game đã đè GAME (atlas giữ nguyên)."""
    import gzip
    import struct
    assert b[:4] == b"ATMK"
    d = gzip.decompress(b[6:])
    n = struct.unpack("<I", d[:4])[0]
    J = json.loads(d[4:4 + n].decode("utf-8"))
    if all(J.get("game", {}).get(k) == v for k, v in GAME.items()):
        return b
    J.setdefault("game", {}).update(GAME)
    js = json.dumps(J, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    body = struct.pack("<I", len(js)) + js + d[4 + n:]
    return b[:6] + gzip.compress(body, 9)


def chep_rig(ma, tep):
    """chép rig (đã đè GAME) + chân dung vào Resources/<ma>/ như doi_phap_lua.chep; chạy lại không đổi thêm."""
    rig = os.path.join(INBOX, ma, "rig")
    d = os.path.join(D.RES, ma)
    os.makedirs(d, exist_ok=True)
    moi = sua_game(open(os.path.join(rig, tep), "rb").read())
    q = os.path.join(d, f"{ma}.atomik")
    giong = os.path.exists(q) and open(q, "rb").read() == moi
    if not giong:
        open(q, "wb").write(moi)
    print(f"  {os.path.relpath(q, D.ROOT)}: {'giữ' if giong else 'chép'} ({len(moi) // 1024} KB, game {GAME})")
    p, q = os.path.join(rig, "chan_dung.png"), os.path.join(d, f"{ma}_portrait.png")
    giong = os.path.exists(q) and open(p, "rb").read() == open(q, "rb").read()
    if not giong:
        shutil.copyfile(p, q)
    print(f"  {os.path.relpath(q, D.ROOT)}: {'giữ' if giong else 'chép'} ({os.path.getsize(q) // 1024} KB)")


def kiem_ten():
    h = json.load(open(os.path.join(D.DATA, "Json", "heroes.json"), encoding="utf-8"))
    H = h if isinstance(h, list) else h.get("heroes", [])
    ten = {x["name"]: x["id"] for x in H}
    assert ten.get(TEN, ID) == ID, f"tên {TEN} trùng tướng {ten.get(TEN)}"


def kiem_icon():
    """biểu tượng thẻ mới có trong bộ ảnh thẻ (Editor/ArtImporter.cs) không."""
    p = os.path.join(D.ROOT, "Assets", "01 Script", "Editor", "ArtImporter.cs")
    t = open(p, encoding="utf-8").read()
    for cid, (_, _, _, ic) in THE.items():
        assert f'"{ic}"' in t, f"thẻ {cid}: không thấy biểu tượng {ic} trong ArtImporter.cs"


def dat():
    D.ID, D.KHAC, D.THE = ID, KHAC, THE


def du_lieu():
    kiem_ten()
    kiem_icon()
    dat()
    D.heroes([(ten, ma, co) for ten, ma, _, co in DANG])
    D.cards()


def chep():
    if TIEN_HOA and len(DANG) > 1:
        import doi_tho5_dang2 as T2
        (_, ma1, _, co1), (ten2, ma2, _, co2) = DANG[0], DANG[-1]
        T2.TUONG2[ID] = (ma1, ma2, ten2, co1, co2)
        T2.th(ID)
        T2.chep(ID)
        return
    for _, ma, tep, _ in DANG:
        chep_rig(ma, tep)


def guid(meta):
    for ln in open(meta, encoding="utf-8"):
        if ln.startswith("guid:"):
            return ln.split()[1]
    return None


def xoa_cu():
    """xoá Resources/<CU> nếu không prefab / asset / scene nào (ngoài chính thư mục đó) trỏ GUID của nó, heroes.json không còn tên đó."""
    d = os.path.join(D.RES, CU)
    if not os.path.isdir(d):
        print(f"  {os.path.relpath(d, D.ROOT)}: không còn (đã xoá)")
        return
    gs = {guid(os.path.join(d, f)): f[:-5] for f in os.listdir(d) if f.endswith(".meta")}
    gs.pop(None, None)
    hj = open(os.path.join(D.DATA, "Json", "heroes.json"), encoding="utf-8").read()
    assert f'"{CU}"' not in hj, f"heroes.json còn trỏ {CU}: chạy doi_quai_bun.py trước"
    con = []
    for goc, _, files in os.walk(os.path.join(D.ROOT, "Assets")):
        if os.path.normpath(goc).startswith(os.path.normpath(d)):
            continue
        for f in files:
            if not f.endswith((".prefab", ".asset", ".unity", ".mat", ".controller")):
                continue
            p = os.path.join(goc, f)
            try:
                t = open(p, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for g, ten in gs.items():
                if g in t:
                    con.append((os.path.relpath(p, D.ROOT), ten))
    if con:
        print(f"  {os.path.relpath(d, D.ROOT)}: CÒN tham chiếu, giữ lại:")
        for p, ten in con:
            print(f"    {p} -> {ten}")
        return
    print(f"  {os.path.relpath(d, D.ROOT)}: không còn tham chiếu ({len(gs)} GUID) " + ("(chỉ kiểm)" if D.KIEM else "-> xoá"))
    if not D.KIEM:
        shutil.rmtree(d)
        if os.path.exists(d + ".meta"):
            os.remove(d + ".meta")


if __name__ == "__main__":
    D.KIEM = "--kiem" in sys.argv
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[:1] == ["chep"]:
        chep()
    elif a[:1] == ["lam"]:
        chep()
        du_lieu()
    elif a[:1] == ["xoa_cu"]:
        xoa_cu()
    else:
        du_lieu()
