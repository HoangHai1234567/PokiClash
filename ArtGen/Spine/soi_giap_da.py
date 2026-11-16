# -*- coding: utf-8 -*-
"""Sói giáp sắt (soi_giap, rig monster_3428 do người dùng chỉ): concept THEO CON GỐC (sói to cơ bắp, mặt nạ + mũ giáp gỗ, giáp vai có sừng
cong, ngực trần, khiên gỗ cao gấp đôi người, búa gỗ đai sắt), đổi sang sói mặc GIÁP SẮT, cầm khiên sắt và búa sắt. Tướng thứ 6 đảo Kim.

    soi_giap_da.py ca_con     hình cả con gốc ở khung 0 idle trên nền trắng → inbox/soi_giap_1/mau/goc_ca_con.png (+ .json: khung từng part)
    soi_giap_da.py concept    ba file prompt concept (ba hướng) → gui_gpt/soi_giap_1/luot_1_concept_<A|B|C>.txt + HUONG_DAN.md
    soi_giap_da.py so_goc     chồng viền hình bóng con gốc lên từng concept, in độ khớp → inbox/soi_giap_1/mau/_so_goc.png
Ảnh con gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai."""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import soi_giap as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
GUI = os.path.join(HERE, "gui_gpt", "soi_giap_1")
CHIEN_SAT = os.path.join(HERE, "inbox", "chien_sat_1", "tai_ve", "L1_duyet.png")
KIEM_SI = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")
MUC = "#2B2118"


def Wp(p):
    return os.path.normpath(p)


def ghi(p, lines):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")


def luu(ten):
    out = os.path.join(G.TAI, ten + ".png")
    return out, [f"SAVE: save it as a PNG to {Wp(out)}",
                 f"If a file with that name already exists, save as {ten}_2.png, {ten}_3.png ... in the same folder. Do not edit, move or "
                 "delete any other file."]


def khung_ca_con(atts, cao=800.0):
    """phép đổi toạ độ rig → ảnh 1536 × 1024: cả con cao ~cao px, đặt giữa khung."""
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    s = min(cao / (y1 - y0), 1250.0 / (x1 - x0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return s, cx, cy, (lambda V: np.stack([W / 2 + (V[:, 0] - cx) * s, H / 2 - (V[:, 1] - cy) * s], 1))


def ca_con():
    """cả con gốc ở khung 0 idle, nền trắng, khung 1536 × 1024; ghi khung bao từng part trên ảnh."""
    _, imgs, atts = G.nap("att_idle0.json")
    atts = [a for a in atts if a.get("region")]
    s, cx, cy, T = khung_ca_con(atts)
    S = 2
    can = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))
    hop = {}
    for a in atts:
        im = G.part_goc(a)
        uv, tr = G.luoi(a)
        lay = Image.new("RGBa", (W * S, H * S), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), T(np.array(a["xy"], float).reshape(-1, 2)) * S, uv, tr)
        lay = lay.convert("RGBA")
        al = np.asarray(lay)[..., 3] > 60
        if al.any():
            ys, xs = np.nonzero(al)
            hop[a["slot"]] = [int(xs.min() / S), int(ys.min() / S), int(xs.max() / S), int(ys.max() / S)]
        can.alpha_composite(lay)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, "goc_ca_con.png")
    can.convert("RGB").resize((W, H), Image.LANCZOS).save(p)
    json.dump(dict(s=s, cx=cx, cy=cy, hop=hop), open(p[:-4] + ".json", "w"), indent=1)
    print(p, f"tỉ lệ {s:.3f} px / đơn vị")
    for k, v in hop.items():
        print(k, v)


MO_TA_CON = (
    "PIECE BY PIECE (as in image 1: a BIG, HEAVY, MUSCULAR WOLF warrior standing on two legs in a deep crouching ready stance, seen from the "
    "side and turned three-quarters to the viewer's RIGHT, his head held LOW and pushed forward between his shoulders, a HUGE SHIELD standing "
    "behind his right arm, a big HAMMER held low on the left): "
    "THE HEAD (upper middle-right, low between the shoulders): a wolf head turned three-quarters to the right and a little down. A FACE MASK "
    "covers the upper part of the head and the top of the muzzle and comes down to a blunt point just above the nose; ONLY ONE EYE shows, as "
    "a small narrow slit just under the lower-left edge of the mask (the other eye is hidden); under the mask the lower muzzle shows, pale, "
    "with a black nose at its lower-right tip, and pale cheek fur on its left. TWO pointed EARS stick out to the RIGHT almost horizontally: "
    "the near ear (bigger, pale inside) just above the face at the left edge of the mask, the far ear (small) behind the right side of the "
    "mask. A CROWN PLATE covers the top of the head above the mask. Behind the head a tall BACK PLATE rises from the upper back over the "
    "nape (in image 1 rough plates with hooked tips). A big shaggy fur MANE flows back from the back of the head, over the near shoulder, to "
    "the left. "
    "THE NEAR SHOULDER (viewer's left, in front of the body): a BIG SHOULDER PAD covers the whole shoulder, with a big HORN-like spike rising "
    "from its top and curving up (in image 1 a dark curved horn with dark crystals). "
    "THE CHEST: a broad chest under the head (in image 1 bare, pale, muscled fur); a leather strap goes round the neck; a small PENDANT hangs "
    "on the chest; a leather strap comes down from the near shoulder across the chest. "
    "THE WAIST: a rope belt with a knot at the left side, and a long ragged dark cloth flap hanging down in front between the legs. "
    "NEAR ARM (viewer's left, in front of the body): a big muscular upper arm under the shoulder pad, the forearm going down to the left with "
    "a dark wrist band, the FIST at the lower left gripping the HAMMER handle; the end of the handle sticks out up to the left above the fist; "
    "the big HAMMER HEAD hangs down below the fist at the lower left, near the ground, in front of the near leg. "
    "FAR ARM (viewer's right): the arm reaches forward to the right in front of the shield; a thick bracer on the forearm is the shield "
    "strap; the big paw at the right, its claws curled. "
    "THE SHIELD: a HUGE tall shield standing upright behind the far arm on the right, seen from the side (its front face narrow, its thick "
    "edge showing on its right), its top higher than the top of the head, its bottom down near the ground. "
    "LEGS: two short, very thick wolf legs bent in a deep squat, wide apart: the near leg on the left behind the hammer head, the far leg on "
    "the right under the far arm; paws with dark claws. "
    "TAIL: a small bushy tail tip sticking out to the left behind the hips, with a pale tip.")

# ba hướng (Claude đề xuất, chờ người dùng chọn). Mỗi hướng: (tên Việt, mô tả Việt, các dòng CHANGE tiếng Anh)
HUONG = {
    "A": ("sói xám tro, giáp thép xám + đỏ thẫm",
          "lông xám tro, ngực mõm kem; mắt hổ phách; mặt nạ + mũ ĐỔI DÁNG thành mũ thép tròn một sống dọc, mặt nạ mõm nhọn; tấm gáy thành cổ "
          "áo thép hai lớp; giáp vai ba lá thép + gai nón thẳng (bỏ sừng cong, bỏ tinh thể); THÊM giáp ngực thép; mặt dây nanh thép; đai vải đỏ, "
          "vạt đỏ thẫm; búa đầu trống tròn đai sắt; khiên tháp thép đỉnh vòm, viền đinh",
          ["FUR: ash grey #8C8E97 on the mane, the arms, the legs and the tail; the muzzle, the cheeks, the chest fur showing at the neck, the "
           "inner side of the near ear, the paws and the tail tip pale cream #EEE9E0. One flat colour each, no shading. Claws dark #3A3236.",
           "EYE: the one narrow eye under the mask edge, flat amber #F2B33D with a dark pupil dot (no glow, no light rays).",
           "ARMOUR colours (everything made of metal below): steel #9BA1AB on the main faces, darker steel #6E747F on the faces turned away; "
           "cloth crimson #A8323A; leather dark brown #5A3C2A.",
           "HELMET (a NEW SHAPE for the mask and the crown plate together): a smooth rounded steel helmet with ONE raised ridge running from "
           "front to back over its top, and a steel snout MASK over the top of the muzzle ending in a blunt point above the nose, with a "
           "narrow eye slit edge. No hooked plates, no crystals, no gold marks, no rivets.",
           "BACK PLATE: a NEW SHAPE: a tall steel COLLAR behind the head made of TWO overlapping curved plates (a neck guard), plain.",
           "SHOULDER PAD: a NEW SHAPE: a big pauldron of THREE overlapping curved steel plates, with ONE short straight conical steel SPIKE "
           "rising from its top (no curved horn, no crystals).",
           "CHEST ARMOUR (new, it makes him an armoured wolf): a steel BREASTPLATE covering the chest and the belly, following the chest's "
           "outline, with one vertical ridge line down its middle; the neck strap and the shoulder strap stay dark leather over it.",
           "PENDANT: a small steel wolf-FANG token on the neck strap.",
           "FOREARMS: a plain steel bracer on each forearm (the far one is the shield strap). The thighs and the upper arms stay fur.",
           "WAIST: a crimson cloth sash knotted at the left side; the long front flap dark crimson #7E2A30 with a ragged lower edge.",
           "THE HAMMER: a NEW SHAPE in the same place and at the same size as the old head: a steel war hammer whose head is a thick DRUM (a "
           "short fat cylinder lying across the handle, two round flat striking faces) with a dark iron band round each end; a dark iron "
           "handle with crimson grip wraps under the fist.",
           "THE SHIELD: a NEW SHAPE in the same place and at the same size: a tall steel TOWER shield seen from the side, its top edge "
           "ROUNDED, its front face plain steel with a raised darker rim, a row of round rivets along the rim, its thick edge darker steel. "
           "No wood, no crystals, no emblem."]),
    "B": ("sói đen than, giáp gang sẫm + đồng thau",
          "lông đen than, ngực mõm xám nhạt; mắt cam; mặt nạ + mũ ĐỔI DÁNG thành mũ gang đỉnh bằng, mặt nạ có khe mắt ngang viền đồng, hai vây "
          "sắt vuốt ra sau; tấm gáy thành tấm gang vuông; giáp vai vòm tròn viền đồng + ba gai ngắn (bỏ sừng); THÊM giáp ngực gang ba đinh đồng; "
          "mặt dây đĩa đồng; thắt lưng da khoá đồng; búa khối có mỏ nhọn; khiên gang tám cạnh, đinh đồng",
          ["FUR: charcoal #4A4A55 on the mane, the arms, the legs and the tail; the muzzle, the cheeks, the chest fur showing at the neck, the "
           "inner side of the near ear, the paws and the tail tip pale grey #D9D8DE. One flat colour each, no shading. Claws dark #2C2A30.",
           "EYE: the one narrow eye under the mask edge, flat orange #F08A3A with a dark pupil dot (no glow).",
           "ARMOUR colours: blackened iron #4B4F58 on the main faces, darker iron #363940 on the faces turned away, a thin BRASS trim #C99A3E "
           "only where listed; leather dark brown #5A3C2A.",
           "HELMET (a NEW SHAPE for the mask and the crown plate together): a blackened iron helmet with a FLAT top, and a mask over the top "
           "of the muzzle whose lower edge is a straight horizontal eye slit edged with brass; two short iron FINS sweep back from the sides "
           "of the helmet top. No hooked plates, no crystals, no gold marks.",
           "BACK PLATE: a NEW SHAPE: a tall SQUARE blackened iron plate behind the head with a brass rim along its top edge.",
           "SHOULDER PAD: a NEW SHAPE: one big ROUND dome pauldron of blackened iron with a brass rim, and a row of THREE short iron spikes "
           "along its top (no curved horn, no crystals).",
           "CHEST ARMOUR (new): a blackened iron BREASTPLATE covering the chest and the belly, following the chest's outline, a brass rim "
           "along its top edge and three round brass rivets in a row across it; the neck strap and the shoulder strap dark leather over it.",
           "PENDANT: a small round brass disc on the neck strap.",
           "FOREARMS: blackened iron bracers with brass edges. The thighs and the upper arms stay fur.",
           "WAIST: a wide dark leather belt with a square brass buckle; the long front flap dark leather with a ragged lower edge.",
           "THE HAMMER: a NEW SHAPE in the same place and at the same size as the old head: a blackened iron WAR HAMMER: a squared block head "
           "with a flat striking face on its lower end and a short curved SPIKE (a beak) on its upper end, a brass band round its middle; a "
           "dark iron handle with two brass rings.",
           "THE SHIELD: a NEW SHAPE in the same place and at the same size: a tall blackened iron shield seen from the side with its CORNERS "
           "CUT OFF (straight slanted top corners), a raised vertical RIDGE down its front face and round brass rivets at its corners. No "
           "wood, no crystals, no emblem."]),
    "C": ("sói nâu đỏ, giáp bạc + xanh lam",
          "lông nâu đỏ, ngực mõm kem; mắt vàng chanh; mặt nạ + mũ ĐỔI DÁNG thành mũ bạc chóp nhọn, mặt nạ hình mõm sói có thanh che mũi; tấm "
          "gáy thành ba lá bạc xoè như vây; giáp vai vuông ba lá + vây lưỡi cong ra sau (bỏ sừng); THÊM giáp ngực bạc hai lớp; mặt dây đá xanh; "
          "đai vải xanh; búa tạ đầu vuông vát cạnh; khiên bạc hình diều đáy nhọn, viền sắt",
          ["FUR: russet brown #A65E3A on the mane, the arms, the legs and the tail; the muzzle, the cheeks, the chest fur showing at the neck, "
           "the inner side of the near ear, the paws and the tail tip cream #F1E3C8. One flat colour each, no shading. Claws dark #3A3236.",
           "EYE: the one narrow eye under the mask edge, flat lime yellow #C9D84A with a dark pupil dot (no glow).",
           "ARMOUR colours: bright silver steel #B9C0CA on the main faces, darker steel #858C98 on the faces turned away, dark iron #4A4B52 "
           "where listed; cloth royal blue #34508F.",
           "HELMET (a NEW SHAPE for the mask and the crown plate together): a silver helmet whose top rises to a POINT, and a mask shaped like "
           "a wolf snout over the top of the muzzle with a straight NOSE BAR down its middle. No hooked plates, no crystals, no gold marks.",
           "BACK PLATE: a NEW SHAPE: THREE silver plates fanned out behind the head like a fin.",
           "SHOULDER PAD: a NEW SHAPE: a square-cornered pauldron of THREE stacked overlapping silver plates, with a curved silver BLADE-fin "
           "sweeping up and back from its top (no horn, no crystals).",
           "CHEST ARMOUR (new): a silver BREASTPLATE covering the chest and the belly, following the chest's outline, one curved line across "
           "its lower part (two overlapping plates); the neck strap and the shoulder strap dark iron-grey leather over it.",
           "PENDANT: a small blue stone in a silver frame on the neck strap.",
           "FOREARMS: silver bracers. The thighs and the upper arms stay fur.",
           "WAIST: a blue cloth sash knotted at the left side; the long front flap dark blue #26386A with a ragged lower edge.",
           "THE HAMMER: a NEW SHAPE in the same place and at the same size as the old head: a silver steel MAUL: a big squared block head with "
           "a bevelled edge round each striking face and a dark iron band round its middle; a dark iron handle with blue grip wraps.",
           "THE SHIELD: a NEW SHAPE in the same place and at the same size: a tall silver KITE shield seen from the side: a straight top edge, "
           "the sides tapering down to a rounded POINT at the bottom, a dark iron rim all the way round and one dark iron band across its "
           "upper third. No wood, no crystals, no emblem."]),
}

STYLE = (
    f"DRAWING STYLE (very important): hand-drawn on paper like the approved heroes of our game (images 2 and 3): a wobbly dark-brown INK "
    f"outline ({MUC}, about 7 px) running all the way round every piece exactly on its silhouette, thinner ink lines (about 4 px) for the "
    "few inner lines (plate edges, the eye, a few fur tufts, the chest line), and every area filled with ONE flat colour with visible "
    "coloured-pencil / wax-crayon hatching. Image 1 is painted in a soft digital style with light and dark planes, mauve-grey fur, brown "
    "wood-and-leather armour, dark purple and red crystals and a glowing red eye: do NOT copy that painting style, its colours or its "
    "crystals: no shading, no highlights, no white shine streaks, no gradients, no blush, no glow, no shadows, no gloss, no sparkles: flat "
    "colour only. A different tone appears only where a different face (front face / side face) or material is listed. SIMPLE DESIGN, FEW "
    "DETAILS: no extra rivets, engravings, scratches, cracks, dents, skulls, badges, emblems, flames or patterns beyond what is listed.")


def prompt_concept():
    mau = os.path.join(G.MAU, "goc_ca_con.png")
    R = [(mau, "the REFERENCE character, 1536x1024, white background: a big heavy muscular wolf warrior in a deep crouch, head low, wearing "
               "a brown face mask and rough brown helmet plates with a red crystal, a big brown shoulder pad with a dark curved horn, a bare "
               "muscled chest with a strap and a small pendant, a rope belt and a long dark cloth flap, a huge brown wooden shield standing "
               "behind his right arm and a wood-and-iron block hammer held low on the left. It is painted in a soft digital style. Keep "
               "its POSE, its BUILD, its PIECES and their PLACES; change its LOOK and the shapes listed.",
          "Hình cả con gốc ở dáng nghỉ (1536 × 1024, nền trắng): sói to cơ bắp ngồi thụp, đầu cúi, mặt nạ + mũ giáp gỗ nâu có tinh thể đỏ, "
          "giáp vai nâu sừng cong đen, ngực trần có dây da và mặt dây, đai thừng + vạt vải dài, khiên gỗ cao gấp đôi người sau tay phải, búa gỗ "
          "đai sắt thõng tay trái. Giữ dáng, khối người và từng mảnh, đổi hình"),
         (CHIEN_SAT, "an approved hero of our game from the same metal island (a chubby armoured knight with a shield), 1536x1024, white "
                     "background: match EXACTLY its wobbly dark-brown pen line, its visible crayon hatching and its completely flat "
                     "colouring of metal plates (front faces and darker side faces). Do NOT copy its design, its proportions or its "
                     "colours.",
          "Chiến binh sắt Thiết Vệ (tướng 2 đảo Kim) đã duyệt: lấy nét bút rung, vân sáp, cách tô giáp phẳng (mặt trước + mặt bên sẫm)"),
         (KIEM_SI, "another approved hero of our game (a sturdy armoured monkey samurai), 1536x1024, white background: see how a sturdy animal "
                   "warrior's fur, fur tufts and armour plates are drawn flat with few details. Do NOT copy its design, its leaves or its "
                   "colours.",
          "Voọc samurai (tướng đảo Mộc) đã duyệt: xem cách vẽ thú chiến binh chắc nịch: lông, chỏm lông, giáp tô phẳng, ít chi tiết")]
    hd = ["# Gói GPT: sói giáp sắt (soi_giap), tướng 6 đảo Kim", "",
          "Con gốc của rig: `monster_3428` (sói to cơ bắp, mặt nạ + mũ giáp gỗ, giáp vai sừng cong, khiên gỗ lớn, búa gỗ đai sắt; game tham "
          "khảo; người dùng chỉ). Ảnh mẫu 1 là hình con gốc: chỉ dùng trong máy, không đăng công khai.", "",
          "## Lượt 1: concept theo con gốc, ba hướng (2026-11-16)", "",
          "Người dùng: \"concept sói humanoid mặc giáp sắt, cầm khiên sắt và búa sắt\". Ba file, mỗi file một hướng; giữ dáng ngồi thụp, khối "
          "người to, chỗ và cỡ từng mảnh của con gốc (để lắp lên đúng xương); đổi hẳn dáng các mảnh nhận diện (mặt nạ + mũ, tấm gáy, giáp vai "
          "sừng, đầu búa, khiên), thêm giáp ngực sắt, đổi màu lông, chất giáp.", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
    hd += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
    hd += [""]
    for k, (vi, vi2, doi) in HUONG.items():
        out, save = luu(f"L1_{k}")
        p = os.path.join(GUI, f"luot_1_concept_{k}.txt")
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {e}" for i, (r, e, _) in enumerate(R, 1)]
        t += [""] + save + ["",
              "TASK: REDESIGN ON THE SAME POSE. Redraw the wolf of image 1 as ONE picture of OUR OWN character, a BIG WOLF WARRIOR IN IRON "
              "ARMOUR with an iron shield and an iron hammer: the SAME pose and the SAME big heavy muscular build, with EVERY piece in the "
              "same place, at the same size and with the same overlaps (if the new picture were laid over image 1, every piece must sit on "
              "its old place), but with the NEW shapes, new materials, new colours and our hand-drawn drawing style described below. Do not "
              "add pieces other than the armour listed, do not remove, merge or move pieces. Do NOT make him chibi, small-bodied or "
              "big-headed: keep the head low and small between the big shoulders, as in image 1.", "",
              MO_TA_CON, "",
              "CHANGE:"] + [f"- {d}" for d in doi] + ["",
              STYLE, "",
              "Mood: a tough, heavy, determined wolf warrior ready to fight (a game hero), strong and a little stocky, not a cute mascot, not "
              "scary. Both arms, both legs and the tail must stay attached to the body exactly as in image 1; the near fist really grips "
              "the hammer handle; the shield is strapped to the far forearm.",
              "",
              "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character at the same "
              "place and size as in image 1. No sparkles, no glints, no dust, no glow, no fire, no speed lines, no labels, no frame."]
        ghi(p, t)
        hd += [f"- **Hướng {k}** ({vi}: {vi2}): chỉ gửi GPT đường dẫn `{Wp(p)}`; ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…)."]
        print(p)
    hd += ["", "Bản được chọn chép thành `L1_duyet.png` cùng thư mục.", "",
           "Kiểm: đúng dáng ngồi thụp, khối người to, đúng chỗ và cỡ từng mảnh như ảnh 1 (chồng lên phải trùng, trừ mũ, tấm gáy, gai vai, đầu "
           "búa, khiên đổi dáng); đầu cúi thấp giữa hai vai, nghiêng ¾ phải, chỉ lộ MỘT khe mắt dưới mép mặt nạ, hai tai chĩa ngang sang phải; "
           "tay gần nắm cán búa, khiên buộc vào cẳng tay xa; hai chân, đuôi dính thân; nét bút mực rung, vân sáp, tô phẳng, không bóng, mắt không "
           "phát sáng, không tinh thể; nền trắng tinh.", "",
           "Câu sửa nhanh: \"remove the shading / highlights, flat colour only\"; \"keep every piece at the same place and size as in image "
           "1\"; \"keep the big heavy build, the head low between the shoulders\"; \"the fist must grip the hammer handle\"."]
    ghi(os.path.join(GUI, "HUONG_DAN.md"), hd)


def _mat_na(p):
    """mặt nạ hình (khác nền trắng), lấp kín lỗ."""
    import cv2
    a = np.asarray(Image.open(p).convert("RGB").resize((W, H)), np.int16)
    m = ((255 - a).max(2) > 28).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    k = np.zeros_like(m)
    cv2.drawContours(k, [c for c in cs if cv2.contourArea(c) > 400], -1, 1, -1)
    return k.astype(bool)


def so_goc(ks="ABC"):
    """chồng viền hình bóng con gốc (đỏ) lên từng concept, in độ khớp IoU → mau/_so_goc.png."""
    import cv2
    g = _mat_na(os.path.join(G.MAU, "goc_ca_con.png"))
    cs, _ = cv2.findContours(g.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    o = []
    for k in ks:
        p = os.path.join(G.TAI, f"L1_{k}.png")
        if not os.path.exists(p):
            continue
        m = _mat_na(p)
        iou = (m & g).sum() / max(1, (m | g).sum())
        im = np.asarray(Image.open(p).convert("RGB").resize((W, H))).copy()
        cv2.drawContours(im, cs, -1, (230, 30, 30), 3)
        cv2.putText(im, f"{k}  IoU {iou:.3f}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (230, 30, 30), 4)
        o.append(Image.fromarray(im).resize((W // 2, H // 2), Image.LANCZOS))
        print(k, f"IoU {iou:.3f}")
    if o:
        c = Image.new("RGB", (W // 2 * len(o), H // 2), "white")
        for i, im in enumerate(o):
            c.paste(im, (i * W // 2, 0))
        c.save(os.path.join(G.MAU, "_so_goc.png"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "so_goc":
        so_goc(*(sys.argv[2:3] or ["ABC"]))
    elif cmd == "ca_con":
        ca_con()
    elif cmd == "concept":
        prompt_concept()
    else:
        print(__doc__)
