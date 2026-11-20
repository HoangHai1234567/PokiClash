# -*- coding: utf-8 -*-
"""Gói prompt concept quái lính (NPC không thu thập, 1 dạng) cho 4 đảo còn lại: gui_gpt/quai_<đảo>/luot_1_concept.txt.

    py -3 -I ArtGen/Spine/build_quai_npc.py            # sinh 4 file prompt + HUONG_DAN.md
Mẫu: gui_gpt/quai_thuy/luot_1_concept.txt (tôm tít đấm bốc, thay Cua Kìm). Đường dẫn tính từ chỗ đặt script (hai máy khác ổ).
Người dùng 2026-11-20: "Bạn tự quyết, làm xong 4 đảo còn lại" -> Claude tự chọn thiết kế, mỗi đảo một con, thay lính loại 1 của đảo.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
INBOX = os.path.join(HERE, "inbox")
GUI = os.path.join(HERE, "gui_gpt")
REF1 = os.path.join(INBOX, "ca_den_1", "tai_ve", "L1_duyet.png")
REF2 = os.path.join(INBOX, "ech_xanh_1", "tai_ve", "L1_duyet.png")

STYLE = (
    "DRAWING STYLE (very important): hand-drawn on paper like the approved heroes of our game (images 1 and 2): a wobbly "
    "dark-brown INK outline (#2B2118, about 7 px) running all the way round every piece exactly on its silhouette, thinner ink "
    "lines (about 4 px) for the few inner lines, and every area filled with ONE flat colour with visible coloured-pencil / "
    "wax-crayon hatching. No shading, no highlights, no white shine streaks, no gradients, no glow, no shadows, no gloss, no "
    "sparkles: flat colour only; a darker tone only on the far-side pieces listed. VERY SIMPLE DESIGN, FEW DETAILS: no extra "
    "spikes, patterns, spots, scars, badges or decorations beyond what is listed.")

CANVAS = (
    "CANVAS: landscape 1536x1024, pure-white background (#FFFFFF), no ground line, no cast shadow; the character centred, about "
    "820 px tall from its highest point to the feet, the feet about 90 px above the bottom edge. No sparkles, no glints, no dust, "
    "no glow, no aura round the character, no fire, smoke, leaves or particles flying off it, no speed lines, no labels, no frame.")

READ = (
    "READABLE FOR ANIMATION: the limbs, tail, wings and head pieces are clearly separate shapes joined to the body (no white gaps "
    "where they join), not crossing over the body silhouette more than described, nothing held in the hands, no weapon.")

QUAI = {
    "quai_hoa": dict(
        dao="FIRE", island="the volcano island",
        what="a FIGHTING ROOSTER BRAWLER: a cocky little gamecock whose comb and tail are made of fire, ready to kick",
        design=[
            "HEAD (upper right, about 35% of the character's height, big and chunky like a chibi): a round head with a short "
            "strong hooked BEAK (closed, pointing right); one big round fierce EYE (white with a dark pupil and one small white "
            "dot) under a heavy slanted angry brow; on top a big COMB shaped like three rounded flame tongues leaning back; one "
            "small round wattle hanging under the beak.",
            "BODY: a plump round body with a big puffed-out chest pushed forward, leaning forward a little, standing tall.",
            "WINGS: two short wings like little arms: the NEAR wing (in front) bent at the side of the body with its tip pointing "
            "back and down, three big feather tips; the FAR wing raised up behind the back, only its upper half visible above the "
            "back. Leave a clear gap between the far wing and the head.",
            "TAIL: a big tail of four long curved feathers shaped like flame tongues, sweeping up and back to the LEFT, behind the "
            "body; the tips do not touch the head.",
            "LEGS: two strong scaly legs, wide apart (near leg forward and straight, far leg back), each with a sharp spur at the "
            "back of the shin and a three-toed foot with short claws flat on the ground; both legs fully visible, not crossing.",
            "COLOURS (flat): body, head and near wing orange #F39A2D, a darker orange #D9771C on the far wing and the far leg; "
            "chest cream #F3E3C0; comb, wattle and tail feathers red #E5483A with yellow #F7C948 tips; beak, legs and feet "
            "yellow #F7C948 with darker yellow #E0A91E on the far leg; claws dark brown.",
        ],
        mood="a hot-headed, cocky little fighting cock (an enemy of the game): eye narrowed and angry, chest out, ready to kick"),
    "quai_moc": dict(
        dao="WOOD", island="the forest island",
        what=("a SQUIRREL SCRAPPER: a tough little squirrel wearing the spiky shell of a chestnut as a helmet, with a huge "
              "bushy tail made of big leaves"),
        design=[
            "HEAD (upper right, about 40% of the character's height, big and round like a chibi), turned to the right: a round "
            "squirrel face with a short muzzle, a small dark nose, two big front buck teeth showing, big round fierce EYES "
            "(yellow iris #F7C948, dark pupil, one small white dot) under heavy slanted angry brows; on top a HELMET: the open "
            "half-shell of a chestnut burr, a rounded cap covered with about ten short thick spikes; two short pointed ears "
            "poking out under the helmet's rim.",
            "BODY: a small chubby body standing upright on its hind legs, pale belly.",
            "ARMS: two short arms with small four-finger paws: the NEAR arm (in front) raised as a fist in front of the chest, "
            "NOT covering the face; the FAR arm raised a bit higher behind, fist up. Leave a clear gap between the arms and the "
            "head.",
            "TAIL: a very big bushy TAIL made of three big overlapping leaves in a column, growing from the lower back, curving up "
            "behind the body to the LEFT, its top leaf curling back at the height of the helmet; a clear gap between the tail and "
            "the head.",
            "LEGS: two short strong hind legs with big flat feet, standing apart, both fully visible.",
            "COLOURS (flat): fur chestnut brown #B8733A, a darker brown #8E5527 on the far arm and the far leg; belly, muzzle "
            "and inner ears cream #F3E3C0; helmet spiky shell yellow-green #A8C64A with its spikes the same colour; tail leaves "
            "green #6DBE45 with a darker green #4E9A33 middle vein line; teeth white; small pink #F07FA6 inside the mouth.",
        ],
        mood="a scrappy, short-tempered little squirrel (an enemy of the game): eyes narrowed and angry, teeth bared, fists up"),
    "quai_kim": dict(
        dao="METAL", island="the metal island",
        what=("a STEEL HEDGEHOG FIGHTER: a stocky little hedgehog whose quills are big flat steel blades, standing upright "
              "with metal claws"),
        design=[
            "HEAD (upper right, about 40% of the character's height, big and round like a chibi), turned to the right: a round "
            "face with a short pointed SNOUT ending in a round black nose; big round fierce EYES (yellow iris #F7C948, dark pupil, "
            "one small white dot) under heavy slanted angry brows; a small mouth with one tiny fang; small round ears.",
            "QUILLS (the most important pieces): a mantle of about nine big flat triangular STEEL BLADES covering the back of the "
            "head and the back of the body, fanning out behind to the LEFT and up like a spiky crest; each blade a simple long "
            "triangle with one thin inner line; they never cover the face.",
            "BODY: a round chubby body standing upright on two short legs, with a pale round belly.",
            "ARMS: two short arms, each ending in three short curved metal CLAWS: the NEAR arm (in front) held forward at chest "
            "height with claws spread, ready to slash; the FAR arm raised higher behind, claws up. Leave a clear gap between each "
            "arm and the head.",
            "LEGS: two short legs with small feet, standing apart, both fully visible.",
            "COLOURS (flat): fur dark slate blue #4B5A78, a darker slate #38445C on the far arm and the far leg; face, snout and "
            "belly cream-tan #E8C9A0; steel blades silver-grey #B7C0CC with a darker grey #8A95A5 on the blades of the far side; "
            "claws gold #E3B341; nose dark brown.",
        ],
        mood="a prickly, grumpy little hedgehog warrior (an enemy of the game): eyes narrowed and angry, claws ready"),
    "quai_tho": dict(
        dao="EARTH", island="the earth island",
        what="a STONE RAM BRUISER: a stocky little mountain ram with huge curled horns of rock, ready to charge and headbutt",
        design=[
            "HEAD (front right, about 35% of the character's height, big like a chibi), lowered a little and turned to the right, "
            "ready to charge: a short broad face with a blunt muzzle and two nostrils, a small goatee beard, big round fierce EYES "
            "(yellow iris #F7C948, dark pupil, one small white dot) under heavy slanted angry brows; two MASSIVE curled HORNS of "
            "stone, each one a thick spiral curling back and down around the side of the head, with two or three crack lines; "
            "small ears under the horns.",
            "BODY: a chunky barrel body seen from the side, covered with a thick wool coat made of big rounded cloud-like puffs; "
            "three flat rounded stone plates sitting on top of the wool along the back.",
            "LEGS: four short sturdy legs with hooves, all four visible and separate: the near front leg forward, the near back "
            "leg back, the far front leg and the far back leg a little behind and offset from the near ones so they do not "
            "overlap them; hooves flat on the ground.",
            "TAIL: a small stubby wool tail at the back on the LEFT.",
            "COLOURS (flat): face, ears and legs earthy brown #A8743F, a darker brown #85592E on the two far legs; wool sand "
            "#E6D3A8; horns and back plates stone grey-brown #9C8B76 with a darker #7A6B5A on the far horn; hooves and nose "
            "dark brown #5A4632; beard sand.",
        ],
        mood="a stubborn, hot-headed little ram (an enemy of the game): eyes narrowed and angry, head lowered, ready to charge"),
}


def prompt(ma, q):
    save = os.path.join(INBOX, ma, "tai_ve", "L1.png")
    lines = [
        "IMAGES (attached in this order; open each from its path):",
        f"image 1 = {REF1}: an approved hero of our game (a blue anglerfish beast with a lantern), 1536x1024, white background: "
        "match EXACTLY its wobbly dark-brown pen line, its crayon hatching and its completely flat colouring. Do NOT copy its "
        "design or its colours.",
        f"image 2 = {REF2}: an approved hero of our game (a green frog beast with its tongue out), 1536x1024, white background: "
        "match EXACTLY the same drawing style (pen line, crayon hatching, flat colours, the fierce slanted eyes). Do NOT copy its "
        "design or its colours.",
        "",
        f"SAVE: save it as a PNG to {save}",
        "If a file with that name already exists, save as L1_2.png, L1_3.png ... in the same folder. Do not edit, move or delete "
        "any other file.",
        "",
        f"TASK: DESIGN A NEW CHARACTER. One picture of a new enemy creature of our game: a {q['dao']} monster that players fight "
        f"on {q['island']} (it is not collected). It is {q['what']}. Draw ONE character, whole, in the pose described below, in "
        "our hand-drawn style (images 1 and 2).",
        "",
        "DESIGN, PIECE BY PIECE (three-quarter view turned to the RIGHT, standing on the ground, ready to fight):",
    ] + [f"- {d}" for d in q["design"]] + [
        "",
        READ,
        "",
        STYLE,
        "",
        f"Mood: {q['mood']}; chunky and appealing but not a cute mascot, not horror.",
        "",
        CANVAS,
    ]
    return "\n".join(lines) + "\n"


HD = """# Quái lính 4 đảo (Claude tự gen bằng Magnific, người dùng không phải gửi GPT)

Mỗi đảo một con, một dạng, thay lính loại 1 của đảo (bậc 1 và bậc 2 dùng chung hình, bậc 2 to hơn):

| đảo | file prompt | thay | con mới | ảnh mẫu | lưu |
|---|---|---|---|---|---|
""" + "\n".join(
    f"| {d} | gui_gpt/{m}/luot_1_concept.txt | {t} | {n} | ca_den_1, ech_xanh_1 (L1_duyet.png, 1536x1024, nền trắng: chỉ học nét vẽ) | inbox/{m}/tai_ve/L1.png |"
    for d, m, t, n in [("Hỏa", "quai_hoa", "Lò Lửa / Lò Quái", "gà chọi lửa"),
                       ("Mộc", "quai_moc", "Bọ Sừng / Bọ Sừng Gỗ", "sóc đội vỏ hạt dẻ gai, đuôi lá"),
                       ("Kim", "quai_kim", "Giáp Vệ / Chiến Giáp", "nhím lông lưỡi thép"),
                       ("Thổ", "quai_tho", "Chuột Khoan / Khoan Giáp", "dê núi sừng đá")]) + """

Kiểm: một con trọn vẹn, nền trắng, viền mực nâu, tô phẳng không bóng; tay chân đuôi tách rõ khỏi thân (để cắt mảnh, rig).
Sửa nhanh: "keep everything, only <chỗ cần sửa>".
"""


def main():
    for ma, q in QUAI.items():
        d = os.path.join(GUI, ma)
        os.makedirs(d, exist_ok=True)
        os.makedirs(os.path.join(INBOX, ma, "tai_ve"), exist_ok=True)
        p = os.path.join(d, "luot_1_concept.txt")
        open(p, "w", encoding="utf-8", newline="\n").write(prompt(ma, q))
        print(p)
    p = os.path.join(GUI, "quai_hoa", "..", "HUONG_DAN_quai_npc.md")
    open(os.path.normpath(p), "w", encoding="utf-8", newline="\n").write(HD)
    print(os.path.normpath(p))


if __name__ == "__main__":
    main()
