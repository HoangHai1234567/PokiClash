# -*- coding: utf-8 -*-
"""Tướng 7 đảo Thổ (ải 40, id game hiện `rua_nui`), mã làm việc `sau_dat`: SÂU ĐẤT KHỔNG LỒ trên rig `monster_3643` (game tham khảo,
người dùng chỉ 2026-11-17 bằng ảnh chụp trang xem). Lời dặn: "concept sâu đất khổng lồ như ảnh, tham khảo baron trong lol và sâu cát trong
dune; animation xuất hiện chui từ dưới đất lên; các chiêu còn lại tự sáng tạo dựa theo con gốc, độc đáo, lạ, epic, đẹp"; gen qua Magnific
(dưới 100 credit / ảnh, quá thì hỏi). Xương, lưới, chuyển động gốc là của nhà phát hành game đó: dùng nội bộ, không đăng công khai.

    sau_dat.py ca_con          hình cả con gốc khung 0 idle → inbox/sau_dat_1/mau/goc_ca_con.png (+ .json khung từng slot)
    sau_dat.py slot            bảng slot (thứ tự vẽ, ảnh, xương, khung trên ảnh ca_con)
    sau_dat.py concept         file prompt concept từng hướng → gui_gpt/sau_dat_1/luot_1_concept_<k>.txt + HUONG_DAN.md
    sau_dat.py so_goc [ks]     chồng viền hình bóng con gốc lên từng concept, in IoU → inbox/sau_dat_1/mau/_so_goc.png
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tho5  # noqa: E402

CODE = "sau_dat"
tho5.CON[CODE] = ("monster_3643", 7, 40)
_I = os.path.join(HERE, "inbox")
RONG = os.path.join(_I, "rong_cat_1", "tai_ve", "L1_duyet.png")
QUY = os.path.join(_I, "quy_nui_1", "tai_ve", "L1_duyet.png")

GOC_EN = ("the ORIGINAL rig character from another game (a pale serpent-dragon rising out of a cocoon of tall purple petals, dark tentacles "
          "on its head, 1536x1024, white background). It is painted in a smooth digital cel style. Use it ONLY for the pose, the body plan "
          "and where each big piece sits; do NOT copy its shapes, its face, its crest, its petals, its details or its colours.")
GOC_VI = ("Con gốc `monster_3643` khung 0 idle (rồng rắn trắng trồi lên giữa kén cánh tím, tua đen trên đầu, đế pha lê lam), 1536 × 1024 nền "
          "trắng: chỉ lấy DÁNG, bố cục và chỗ từng mảnh to")
REFS = [
    (RONG, "an approved EARTH hero of our game (a sandstone-armoured drake), 1536x1024, white background: match EXACTLY its wobbly dark-brown "
           "pen line, its crayon hatching, its completely flat earth colours (sand, ochre, cream, brown) and its fierce narrow eye. Do NOT "
           "copy its design.",
     "Rồng giáp sa thạch (tướng 4 đảo Thổ) đã duyệt: lấy nét bút mực rung, vân sáp, màu đất phẳng, mắt hẹp dữ"),
    (QUY, "an approved EARTH hero of our game (a four-armed rock ape), 1536x1024, white background: match EXACTLY how big heavy rock is drawn "
          "in our style (flat front-face tone, darker side-face tone, nothing else) and its flat amber crystal vein. Do NOT copy its design.",
     "Vượn núi đá bốn tay (tướng 5 đảo Thổ) đã duyệt: lấy cách vẽ đá nặng (hai tông mặt trước / mặt bên) và mạch hổ phách phẳng"),
]

TASK = ("TASK: DESIGN A NEW CHARACTER, LOOSELY BASED ON image 1: a COLOSSAL BURROWING WORM, a mini-boss of the earth island, bursting up "
        "out of the ground (a giant earthworm crossed with a desert sandworm and a jungle baron beast). Image 1 is ONLY a guide for the POSE "
        "and the BODY PLAN (the new character will be animated with the same skeleton): keep its pose, its facing, its size and place on "
        "the canvas, and roughly where the head, the jaw, the body, the crest, the feelers, the tall slabs behind, the plates in front, the "
        "small tendrils and the rubble at the bottom are and which way they point. EVERYTHING ELSE IS OUR OWN NEW DESIGN, described below. "
        "The result must NOT look like a recolour or a trace of image 1: someone who knows image 1 must see a DIFFERENT creature in the "
        "same pose. The head, the crest, the feelers and the tendrils stay joined to the body (no white gaps).")

PLAN = ("BODY PLAN (from image 1, positions on the 1536x1024 canvas): the creature fills x 420-1110, y 130-910. A low pile of broken rock "
        "lies across the bottom (y 750-910). Out of the middle of that pile rises the THICK WORM BODY in a gentle S-curve (lower body about "
        "x 680-940, y 550-880), its belly side turned to the viewer. The HEAD is at the upper right (about x 840-1060, y 450-660), seen from "
        "the side and a little from the front, POINTING RIGHT AND SLIGHTLY DOWN, ONE eye visible; it has an upper head piece and a separate "
        "hinged LOWER JAW under it, the mouth slightly open at the right end. A CREST of plates sweeps back and up from the top of the head "
        "toward the upper left (x 670-990, y 300-550). About TEN long thin FEELERS grow from the back of the head and fan up and to the right "
        "(their tips up to y 130). Behind the body FIVE TALL POINTED SLABS stand up round it like a half-open bud (x 460-1100, y 290-870). In "
        "front of the lower body FOUR DARK CURVED PLATES rise out of the rubble. About a DOZEN short curved TENDRILS sprout from the ground "
        "and the lower body and curl outwards to the left and the right; THREE short tendrils grow from the back of the head pointing left.")

MOOD = ("MOOD: a colossal, ancient, menacing worm: fierce and epic like a boss monster, heavy and powerful, mature proportions (NOT chibi, NOT "
        "a cute mascot, no smile), but stylised and clean for a family game: no gore, no slime, no drool, no blood.")

HUONG = {
    "A": ("sâu cát (nghiêng Dune)",
          "đầu húc bằng sa thạch ba vòng giáp, miệng tròn có nhiều vòng răng kem hướng vào trong, lòng miệng đỏ đất nung; thân vòng đốt vàng "
          "cát; mào sau đầu ba tấm quạt sa thạch tròn; mười râu roi nâu sẫm đầu ngạnh hổ phách; năm phiến sau lưng là ĐÁ PHÂN TẦNG (vằn kem, "
          "son, gỉ) dựng lên như đất nứt; bốn tảng đất nâu sẫm có khe hổ phách; tua nhỏ hồng đất như giun con; đế là gò cát, đá vụn, hổ phách",
          ["BODY: a giant SANDWORM body made of many RING SEGMENTS like an earthworm, each ring a sand-ochre band #D3A866 with a thin darker "
           "groove #9C7444 between rings; the belly side cream sand #EAD7AE.",
           "HEAD (new, not a dragon skull): a blunt, heavy ARMOURED WORM HEAD like a battering ram, wrapped in THREE overlapping sandstone "
           "ARMOUR RINGS #C99A57 (darker #9E7442 on the faces turned away). At the right end a WIDE ROUND MOUTH, slightly open, lined with "
           "RINGS OF MANY SMALL INWARD-POINTING TEETH #F1E6CB; inside of the mouth deep terracotta red #A2412E. One small FIERCE NARROW EYE "
           "on the side of the head (amber iris #F6C443, black slit pupil, one small white dot) under a heavy stone brow ridge.",
           "LOWER JAW: a thick armoured plate #C99A57 under the mouth with two short tusks #F1E6CB pointing up and forward.",
           "CREST: behind the head THREE broad rounded FAN-SHAPED sandstone plates stacked like a collar #D9B677, each with one flat ochre "
           "band #BF8443 along its edge (no long pointed ear spikes).",
           "FEELERS: about ten long thin whip feelers, dark brown #4E3726, each ending in a small AMBER crystal barb #EFA330.",
           "SLABS BEHIND: FIVE tall upturned slabs of LAYERED ROCK (sandstone strata: flat horizontal bands of cream #EAD7AE, ochre #C99A57 "
           "and rust #A85F3A), jagged pointed tops, as if the ground split and tilted up round the worm (no smooth petals, no cell pattern).",
           "PLATES IN FRONT: four angular broken EARTH CHUNKS, dark brown #5A4030 (side faces #3F2D22), each with one thin amber crack "
           "#EFA330.",
           "TENDRILS: short curved fleshy feelers, dusty rose #C98B78 with darker rings, like little earthworms.",
           "RUBBLE: a low SAND MOUND #E2C48C with sandstone rocks #C99A57 / #9E7442 and a few small flat amber crystals #EFA330 (no blue "
           "crystals)."]),
    "B": ("Baron đất (nghiêng Baron)",
          "đầu thú giáp mai nâu tím đất, vương miện sừng kem vuốt ra sau, hàm dưới to có hai NGÀ lớn vểnh lên, mắt hổ phách dữ; thân vòng đốt "
          "đỏ đất nung, bụng tấm kem; mười gai roi nâu tím đầu móc; năm phiến sau lưng là NỬA HỐC ĐÁ: vỏ đá nâu xù, lòng lởm chởm pha lê hổ "
          "phách; bốn tảng bazan đen nâu; tua nhỏ như gai xương kem; đế đá vụn + pha lê hổ phách",
          ["BODY: a huge segmented worm body, terracotta red-brown rings #A65A3C with thin dark grooves #6E3524, a column of broad cream belly "
           "plates #E8D3A8 down the side turned to the viewer.",
           "HEAD (new, not a dragon skull): a massive ARMOURED BEAST-WORM HEAD with a thick plated carapace, dusky earthy plum-brown #6E4A5C "
           "(darker #4E3242 on the faces turned away); a heavy brow over ONE FIERCE NARROW EYE (amber iris #F6C443, black slit pupil, one "
           "small white dot); the mouth slightly open showing a row of strong teeth #F1E6CB.",
           "LOWER JAW: big and heavy #6E4A5C, carrying TWO LARGE CURVED TUSKS #F1E6CB jutting up past the upper lip.",
           "CREST: a CROWN of four thick cream horns #E9DCC0 curving back from the top of the head, each with a dark tip band #4E3242 (thick "
           "curved horns, not flat ear blades).",
           "FEELERS: about ten long spiny whip feelers, plum-brown #6E4A5C, each ending in a hooked cream spike #E9DCC0.",
           "SLABS BEHIND: FIVE tall halves of a split GEODE ROCK: the outer rim rough brown rock #7A5A44, the inner face packed with flat "
           "AMBER CRYSTAL facets #EFA330 / #D88A22 (flat colour, no glow), pointed tops.",
           "PLATES IN FRONT: four curved basalt plates, dark brown-black #3E3030 (side faces #2A2020), one ochre crack each #C4964F.",
           "TENDRILS: short curved cream BONE SPIKES #E9DCC0 with brown tips #7A5A44 sprouting from the ground.",
           "RUBBLE: broken brown rocks #8E6E52 / #6E533D with a few flat amber crystals #EFA330 (no blue crystals)."]),
    "C": ("giun đất giáp đá",
          "thân thịt hồng đất nung vòng đốt, một đai yên sáng ở giữa như giun đất, vài vảy đá phiến; đầu mõm XẺNG ĐÁ dẹt to để đào, mắt hổ "
          "phách nhỏ dữ; hàm dưới hồng có hàng răng đá cùn; mào ba vảy đá phiến chồng ngói; mười râu đất son có đốt, đầu hạt hổ phách; năm "
          "phiến sau lưng là TẢNG ĐẤT VỠ lật lên (mặt cắt nhiều lớp đất + sỏi); bốn mảnh đá phiến sẫm; tua nhỏ hồng như giun con; đế gò đất "
          "nâu + cuội + hổ phách",
          ["BODY: a fleshy giant EARTHWORM body, rosy terracotta #C9735A rings with darker grooves #8E4A38, ONE wider pale SADDLE BAND #E3B39A "
           "round the middle of the body like a real earthworm; armoured here and there with a few flat slate-stone scales #7F7468.",
           "HEAD (new, not a dragon skull): a tapering worm head ending in a big flat SHOVEL-SHAPED STONE SNOUT for digging, slate grey-brown "
           "#8A7B6B (darker #625548 on the faces turned away); ONE small FIERCE NARROW EYE (amber iris #F6C443, black slit pupil, one small "
           "white dot) under a stone brow.",
           "LOWER JAW: a strong rosy terracotta jaw #C9735A lined with a row of blunt stone teeth #E9DCC0; the mouth slightly open, inside "
           "dark red-brown #6E2E26.",
           "CREST: THREE overlapping slate-stone SCALES #8A7B6B stacked like roof tiles behind the head, rounded tips (no long pointed "
           "spikes).",
           "FEELERS: about ten long thin segmented feelers, ochre #C4964F with darker rings #8C6A48, rounded tips with a tiny amber bead "
           "#EFA330.",
           "SLABS BEHIND: FIVE tall upturned CLODS of BROKEN GROUND: cross-sections of layered soil (dark brown #5E4232, red-brown #8E5A3E, "
           "ochre #C4964F bands) with a few pebbles, ragged pointed tops.",
           "PLATES IN FRONT: four flat dark slate shards #4E4640 (side faces #36302C).",
           "TENDRILS: short curved pink-terracotta feelers #D08A72 like little earthworms.",
           "RUBBLE: a mound of brown earth #7E5A3E with round pebbles #A89884 and a few flat amber crystals #EFA330 (no blue crystals)."]),
}

def concept():
    G = tho5.dat(CODE)
    gui = os.path.join(HERE, "gui_gpt", f"{CODE}_1")
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, GOC_EN, GOC_VI)] + REFS
    Wp = tho5.Wp
    hd = ["# Gói GPT: Sâu đất khổng lồ (`sau_dat`), tướng 7 đảo Thổ (ải 40)", "",
          "Con gốc của rig: `monster_3643` (game tham khảo, người dùng chỉ). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy, không đăng "
          "công khai. Gen qua Magnific (GPT 2.6, 1k high, 95 credit / ảnh; trần người dùng 100 credit / ảnh).", "",
          "## Lượt 1: concept, ba hướng (2026-11-17)", "",
          "Người dùng: \"concept sâu đất khổng lồ như ảnh, tham khảo baron trong lol và sâu cát trong dune\". Giữ dáng, hướng, chỗ các mảnh "
          "to của con gốc (để lắp lên đúng xương); đầu, mào, râu, phiến sau lưng, tảng trước, tua, đế là thiết kế mới theo hệ đất.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out = os.path.join(G.TAI, f"L1_{k}.png")
        p = os.path.join(gui, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as L1_{k}_2.png, L1_{k}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.",
              "", TASK, "", PLAN, "", "DESIGN:"] + [f"- {d}" for d in doi] + ["", tho5.style(),
              "", MOOD, "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at about the same "
              "place and size as in image 1. No sparkles, no glints, no dust cloud, no flying debris, no glow, no aura round the character, no "
              "smoke, no speed lines, no labels, no frame."]
        tho5.ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): file prompt `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: cùng dáng, cùng hướng (đầu bên phải chĩa phải hơi xuống, một mắt), cùng chỗ các mảnh to như ảnh 1 nhưng nhìn ra con KHÁC; "
           "thân là sâu vòng đốt; mắt có chấm trắng; nét bút mực rung, vân sáp, tô phẳng, không bóng, không quầng sáng; nền trắng tinh.", "",
           "Câu sửa nhanh: \"it still looks like image 1: change the head, the crest and the slabs more\"; \"remove the shading / highlights "
           "/ glow, flat colour only\"; \"head, crest, feelers and tendrils joined to the body, no white gap\"."]
    tho5.ghi(os.path.join(gui, "HUONG_DAN.md"), hd)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "ca_con":
        tho5.ca_con(CODE)
    elif a[0] == "slot":
        tho5.slot(CODE)
    elif a[0] == "concept":
        concept()
    elif a[0] == "so_goc":
        tho5.so_goc(CODE, a[1] if len(a) > 1 else "ABC")
