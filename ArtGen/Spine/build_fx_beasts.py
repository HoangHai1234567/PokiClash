# -*- coding: utf-8 -*-
"""Tờ hiệu ứng riêng cho từng dòng thú đảo Thủy (beast.py), 2026-11-08. Người dùng dặn: animation đơn giản, hiệu ứng bù vào
là chính, càng gần boss cuối hiệu ứng càng đẹp; tham khảo cách làm của pixelfx (đà, khựng, hạt văng có biến thiên) nhưng hình là
ảnh vẽ tay tô phẳng theo luật game (không glow, không gradient).

Mỗi tờ: ảnh 1536x1024 chia lưới vô hình 3 cột x 2 hàng (ô 512x512), mỗi ô một hình hiệu ứng nằm trọn trong ô. Cắt theo ô
(--cat) ra inbox/fx/<id>_<tên>.png (nền trong, cắt sát).

    py -3 -I ArtGen/Spine/build_fx_beasts.py [id ...]          sinh file prompt gui_gpt/fx_<id>/luot_1_lien.txt
    py -3 -I ArtGen/Spine/build_fx_beasts.py --cat [id ...]    cắt tờ đã gen
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import W, WORLD_STYLE, ART, FLAT  # noqa: E402

REF = W(ART, "Heroes", "inbox", "giot_suong_fx", "tai_ve")
OUT = W(HERE, "inbox", "fx")

# id -> [(tên, mô tả tiếng Anh)] đúng 6 ô theo thứ tự: hàng trên trái -> phải, rồi hàng dưới
SHEETS = {
    "tieu_y": [
        ("claw", "three parallel curved water claw-slash streaks (a paw swipe made of water), slanting down to the right, foam edges, a few drops"),
        ("orb", "a round water bubble orb with a small spiral current inside and three tiny bubbles around it"),
        ("tornado", "a small upright water tornado (a narrow twisting water spout), wide at the top, thin at the bottom, foam rings and flying drops"),
        ("burst", "a round splash burst of water seen from the front: a ring of water petals with foam, drops flying outward"),
        ("foam", "a small cluster of white foam bubbles with a blue outline, like sea foam"),
        ("curl", "a single curling ocean wave crest with white foam, moving to the right"),
    ],
    "canh_cut": [
        ("smash", "an ice impact burst: a star-shaped burst of pale blue ice chunks and frost flakes radiating from the centre"),
        ("orb", "a round frosty ice orb with a snowflake pattern inside and small ice crystals orbiting it"),
        ("block", "a big cracked block of clear blue ice falling, with frost on its edges"),
        ("shards", "a spray of seven sharp pale-blue ice shards flying to the right in a fan"),
        ("flake", "one simple six-pointed snowflake"),
        ("fish", "a small frozen fish encased in a cube of ice, cartoon style"),
    ],
    "mi_nhi": [
        ("notes", "a cluster of three musical notes made of flowing water, with small drops, floating to the right"),
        ("sound", "three curved sound-wave arcs (crescents) of pale aqua water, opening to the right, getting bigger outward"),
        ("ribbon", "a long swirling ribbon of water forming a loose spiral, with foam tips"),
        ("pearl", "a round pearl orb with a soft pink rim inside a ring of tiny water drops"),
        ("feather", "a single lavender-blue feather with a turquoise tip"),
        ("note", "one small musical note made of water"),
    ],
    "ma_ket": [
        ("ram", "a curved double shock-wave of water shaped like two spiral ram horns hitting forward to the right, foam edges"),
        ("orb", "a round sea-foam orb, aqua water with white foam curls swirling around it"),
        ("tide", "a tall tidal wave rising up and curling forward to the right, its foam crest shaped like a ram's spiral horn"),
        ("burst", "a round splash burst of water with foam, drops flying outward"),
        ("bubble", "a small group of three round bubbles with blue outlines"),
        ("shell", "a small spiral seashell, cream and coral, silver rim"),
    ],
    "vay_lam": [
        ("bite", "a big biting jaw made of water: two curved rows of white shark teeth closing (upper and lower arcs) with splashing foam"),
        ("fin", "a shark fin cutting through a low wave, leaving a foam trail to the left, moving to the right"),
        ("geyser", "a tall upright water geyser with a pair of water shark jaws opening at its top"),
        ("burst", "a round splash burst of deep blue water with foam, drops flying outward"),
        ("drop", "one single blue water droplet"),
        ("tooth", "one white triangular shark tooth with a blue outline"),
    ],
    "kuba": [
        ("smash", "a crystal impact burst: aquamarine and white faceted crystal shards exploding outward from the centre"),
        ("orb", "a round aquamarine crystal orb with facets, small crystal chips orbiting it"),
        ("spikes", "a cluster of big pointed aquamarine crystals erupting upward from the ground, with rock chips flying"),
        ("shards", "a spray of seven small faceted crystal shards flying to the right in a fan"),
        ("gem", "one small faceted diamond gem, ice-white with aquamarine facets"),
        ("shield", "a round hexagon-pattern crystal shield, pale aqua, seen from the front"),
    ],
    "thuong_lam": [
        ("breath", "a cone of frost breath blowing to the right: icy wind streaks, snowflakes and ice crystals, wide at the right end"),
        ("orb", "a round ice orb with crystal spikes, a snowflake core"),
        ("icicles", "a burst of big icicles erupting upward from the ground in a ring, pale blue crystal ice"),
        ("nova", "a flat ring of frost and ice crystals spreading on the ground, seen in perspective (a wide ellipse)"),
        ("flake", "one ornate six-pointed snowflake"),
        ("shard", "one sharp ice shard crystal"),
    ],
    "huyen_vu": [
        ("slam", "a heavy shock-wave splash: a wide crescent of water bursting outward to both sides from a ground impact, rocks and foam"),
        ("orb", "a round jade-green orb with a golden hexagon rune pattern and swirling water around it"),
        ("serpent", "a huge water serpent (a sea snake made of water) rising up and striking forward to the right, mouth open, foam mane"),
        ("runes", "a flat golden rune circle with a hexagon turtle-shell pattern, seen in perspective on the ground (a wide ellipse), jade and gold"),
        ("spark", "one small four-pointed jade-green sparkle star"),
        ("wave", "a big dark-blue tidal wave with a white foam crest, curling forward to the right"),
    ],
    "lam_quan": [
        ("toll", "three concentric bronze-gold sound shock rings (a bell toll), seen in perspective as ellipses, with small music-note sparks"),
        ("orb", "a small bronze temple bell glowing with swirling water around it, coral-red tassel"),
        ("bell", "a huge ornate bronze temple bell with wave reliefs and a coral-red rope on top, seen from the side, falling down"),
        ("whirl", "a flat whirlpool of deep blue water spiralling, seen in perspective on the ground (a wide ellipse), foam spiral arms"),
        ("note", "one small golden music-note spark"),
        ("trident", "a big curling wave rising forward to the right with a golden trident shape inside its foam crest"),
    ],
    # tờ thứ hai cho dạng cuối của hai boss cuối đảo (ải 60, 70): hiệu ứng lớn, đẹp nhất
    "huyen_vu_b": [
        ("barrier", "a big half-dome shield made of jade hexagon tiles (a turtle-shell pattern) with a golden rim, seen from the front"),
        ("serpent", "a giant water serpent coiling up in a spiral and rising, mouth open, golden eyes, white foam mane"),
        ("pillar", "a pillar of black-jade stone with golden runes erupting from the ground, water splashing around its base"),
        ("tsunami", "a huge wide dark-blue tidal wave wall with a curling white foam crest, moving to the right"),
        ("orb", "a black-jade orb wrapped in a thin golden rune ring, small water swirls around it"),
        ("rain", "a cluster of falling water drops mixed with small jade-green sparkles"),
    ],
    "lam_quan_b": [
        ("shock", "a huge golden-bronze shockwave ring cracking the ground, seen in perspective as a wide ellipse, rock chips and water splashes flying"),
        ("toll", "a vertical fan of big bronze-gold sound-wave arcs expanding to the right, with three tiny bells among them"),
        ("spout", "a tall twisting whirlpool water column with a golden trident rising out of its top"),
        ("dragon", "a lion-dragon head made of water, roaring and charging to the right, foam mane flowing back"),
        ("feathers", "a swirling burst of black feathers with indigo tips"),
        ("halo", "a ring of small golden bells and golden sparkles, like a charm halo"),
    ],
    # đảo Mộc (2026-11-08 tối): lá, hoa, dây leo, gió, pha lê lục; sét vẽ vàng phẳng (không glow)
    "tien_la": [
        ("slash", "a crescent slash made of sharp green leaves flying to the right"),
        ("orb", "a round green seed orb with a small leaf swirl around it"),
        ("storm", "an upright whirl of green leaves spinning like a small tornado"),
        ("burst", "a round burst of green leaves flying outward from the centre"),
        ("leaf", "one single green leaf"),
        ("seed", "one small golden round seed pod with a short stem"),
    ],
    "hoa_nhuy": [
        ("petals", "a crescent stream of red and white flower petals flying to the right"),
        ("orb", "a round yellow pollen orb surrounded by red petals"),
        ("bloom", "a giant red-and-white flower bursting open upward from the ground, with leaves at its base"),
        ("burst", "a round burst of red petals and yellow pollen dots"),
        ("petal", "one single red flower petal"),
        ("pollen", "a small cluster of yellow pollen dots and tiny sparkles"),
    ],
    "de_hoa": [
        ("ram", "a curved shock-wave shaped like two wooden antler branches hitting forward to the right, with small yellow flowers"),
        ("orb", "a round wreath orb of yellow flowers and green leaves"),
        ("roots", "a burst of brown wooden roots and branches erupting upward from the ground, little leaves on them"),
        ("burst", "a round burst of yellow flowers and green leaves"),
        ("flower", "one small yellow five-petal flower"),
        ("chip", "one small brown wood chip"),
    ],
    "bom_la": [
        ("claw", "three parallel curved claw-slash streaks made of green leaves, slanting down to the right"),
        ("orb", "a round brown pinecone orb with green fern leaves around it"),
        ("vines", "a cluster of green vines whipping upward from the ground, curling at the tips, with leaves"),
        ("burst", "a round burst of green fern leaves"),
        ("cone", "one small brown pinecone"),
        ("fern", "one single green fern leaf"),
    ],
    "phong_linh": [
        ("gust", "a crescent gust of pale green wind streaks with small leaves, blowing to the right"),
        ("orb", "a spinning maple-seed propeller orb: two winged seeds circling a pale green wind ball"),
        ("whirl", "an upright whirlwind of pale green wind with leaves caught in it"),
        ("ring", "a flat ring of wind swirls seen in perspective on the ground (a wide ellipse)"),
        ("seed", "one maple seed with its single wing"),
        ("feather", "one single green owl feather"),
    ],
    "gio_loc": [
        ("blade", "a sharp crescent wind blade of pale teal air with white swirl lines, flying to the right"),
        ("orb", "a round teal wind orb with a white spiral symbol inside, small air swirls around it"),
        ("tornado", "a big upright teal tornado, wide at the top, with white swirl lines and leaves"),
        ("ring", "a flat ring of teal wind seen in perspective on the ground (a wide ellipse) with leaves"),
        ("swirl", "one small white-and-teal wind swirl"),
        ("wing", "one translucent-looking green dragonfly wing piece, flat pale green with dark green veins"),
    ],
    "long_vuot": [
        ("claw", "three parallel curved red claw-slash streaks with small green leaves, slanting down to the right"),
        ("orb", "a round amber orb with a leaf pattern inside and little leaves around it"),
        ("thorns", "a burst of thorny green vines and red thorns erupting upward from the ground"),
        ("burst", "a round burst of green leaves and small red thorns"),
        ("acorn", "one small orange-brown acorn"),
        ("talon", "one curved red claw tip"),
    ],
    "tho_hoang": [
        ("slash", "a long crescent slash made of jade-green bamboo leaves, flying to the right"),
        ("orb", "a round jade-green bamboo charm orb with a golden ring and small bamboo leaves around it"),
        ("spikes", "a ring of sharp jade bamboo stalks erupting upward from the ground"),
        ("burst", "a round burst of jade bamboo leaves and golden sparks"),
        ("leaf", "one single bamboo leaf"),
        ("wheel", "a round wooden shield-wheel with green carvings, seen from the front"),
    ],
    "moc_tinh": [
        ("claw", "three parallel curved claw-slash streaks made of bright green crystal, slanting down to the right"),
        ("orb", "a round faceted bright green crystal orb with small crystal chips orbiting it"),
        ("spikes", "a cluster of big pointed bright green crystals erupting upward from the ground with rock chips"),
        ("burst", "a round burst of bright green crystal shards"),
        ("gem", "one small faceted bright green gem"),
        ("leaf", "one leaf-shaped green crystal"),
    ],
    "thanh_long": [
        ("claw", "three parallel curved jade-green dragon claw streaks with small leaves, slanting down to the right"),
        ("orb", "a round jade pearl orb with a flat yellow zig-zag lightning ring around it"),
        ("dragon", "a long green dragon made of wind and leaves rising upward in an S-curve, mouth open"),
        ("strike", "a flat yellow lightning strike hitting the ground with a burst of green leaves at its base"),
        ("bolt", "one small flat yellow zig-zag lightning bolt"),
        ("cloud", "one small round grey-and-white cloud swirl"),
    ],
    "thanh_long_b": [
        ("storm", "a big storm cloud ring seen in perspective on the ground (a wide ellipse) with flat yellow lightning bolts"),
        ("roar", "a vertical fan of big jade-green wind arcs expanding to the right, with leaves"),
        ("pillar", "a tall twisting pillar of green wind and leaves with a flat yellow lightning bolt down its centre"),
        ("head", "a green dragon head made of wind and leaves, roaring and charging to the right, white whiskers flowing back"),
        ("leaves", "a swirling burst of green and golden leaves"),
        ("halo", "a ring of small jade pearls and flat yellow sparkles, like a halo"),
    ],
    # đảo Hỏa (2026-11-09): tờ lửa chung thay bộ NƯỚC mặc định của beast.py (vòng dưới chân, lốc tụ lực, tiến hóa, sóng cuối),
    # rồi mỗi dòng một tờ riêng; Lân Hỏa (boss cuối) thêm tờ thứ hai
    "hoa_chung": [
        ("ring", "a flat ring of small flames seen in perspective on the ground (a wide ellipse, about three times wider than tall)"),
        ("whirl", "a fire whirl seen from the front: a wide ring of curling flame tongues swirling around an empty centre"),
        ("wave", "a low wave of flames rolling along the ground to the right, its crest curling forward"),
        ("burst", "a round fire burst seen from the front: a ring of flame petals radiating outward from the centre"),
        ("pillar", "a tall upright pillar of flames rising from the ground, wide at the base, flame tongues twisting up"),
        ("ember", "one small flame-shaped ember"),
    ],
    "su_tu_lua": [
        ("claw", "three parallel curved claw-slash streaks made of flame, slanting down to the right"),
        ("fist", "a big star-shaped punch impact burst with flame tongues around it"),
        ("orb", "a round fire orb with a curling lion-mane flame pattern around it"),
        ("burst", "a round burst of orange and yellow flame tufts flying outward"),
        ("lion", "a lion head made of flames, roaring and charging to the right, mane of flame flowing back"),
        ("ember", "one small orange flame tuft"),
    ],
    "khong_lo": [
        ("crack", "a long low crack in the ground running to the right, with flames bursting up out of the crack along its length"),
        ("smash", "an impact burst of black coal chunks and orange flames radiating from the centre"),
        ("orb", "a round glowing-coal orb: a black charcoal ball with flat orange cracks and a small flame on top"),
        ("geyser", "a tall upright geyser of flames and coal chunks erupting from a cracked ground"),
        ("chunk", "one small black coal chunk with an orange crack"),
        ("boulder", "a big flaming charcoal boulder with orange cracks, a short flame trail behind it to the upper left"),
    ],
    "kim_su": [
        ("roar", "three curved sound-wave arcs made of crimson-and-gold flame, opening to the right, getting bigger outward"),
        ("orb", "a round golden fire orb with a crimson swirl inside, like the curl of a lion's mane"),
        ("pillar", "a tall upright pillar of crimson and gold curling flame swirls erupting from the ground"),
        ("burst", "a round burst of crimson and golden flame curls radiating outward"),
        ("swirl", "one small crimson flame curl with a gold tip"),
        ("medal", "a round golden medallion with a lion face, rimmed with small crimson flames"),
    ],
    "nham_than": [
        ("meteor", "a big falling lava rock: dark basalt with flat orange cracks, a flame trail streaming up behind it"),
        ("splash", "a round lava splash burst: blobs of flat orange and yellow lava and rock chips flying outward"),
        ("orb", "a round molten lava orb inside a cracked basalt shell, small flame on top"),
        ("fist", "a big rock-fist punch impact: basalt chunks and lava spatter bursting forward to the right"),
        ("rock", "one small basalt rock with an orange crack"),
        ("pool", "a flat pool of lava seen in perspective on the ground (a wide ellipse) with a basalt rim"),
    ],
    "nguu_quyen": [
        ("horn", "a double shock-wave shaped like two curved bull horns hitting forward to the right, with flames"),
        ("glove", "a big star-shaped punch impact burst with a red boxing-glove print in the middle and flames around"),
        ("orb", "a round orb made of curling fire clouds"),
        ("trail", "a long horizontal trail of fire clouds streaming to the left, like the dust behind a charging bull"),
        ("burst", "a round burst of curling fire clouds"),
        ("cloud", "one small curling fire cloud puff"),
    ],
    "hong_lien": [
        ("breath", "a cone of flame petals blown to the right, widening outward"),
        ("petal", "one big lotus-petal-shaped flame flying to the right, pink and red with a yellow base"),
        ("lotus", "a big blooming lotus flower made of pink and red flames, opening upward from the ground"),
        ("orb", "a round lotus-bud orb of flame, pink and red petals closed around a yellow core"),
        ("burst", "a round burst of pink and red lotus petals of flame flying outward"),
        ("spark", "one small pink petal-shaped ember"),
    ],
    "giap_long": [
        ("ram", "a steel-horn impact: a star-shaped burst of white-hot sparks and steel shards hitting forward to the right"),
        ("ball", "an armoured dragon curled into a spiky steel ball, red-hot spike tips, rolling to the right with a flame trail"),
        ("burst", "a round burst of grey steel shards and orange flames radiating outward"),
        ("orb", "a round red-hot steel orb with riveted bands and a flame crest"),
        ("shard", "one small grey steel shard with a red-hot tip"),
        ("spikes", "a ring of big grey steel spikes with red-hot tips erupting upward from the ground"),
    ],
    "huyen_viem": [
        ("claw", "three parallel curved claw-slash streaks made of violet and pink flame, slanting down to the right"),
        ("foxfire", "one foxfire wisp: a teardrop flame of violet and pink with a curling tail, flying to the right"),
        ("pillar", "a tall upright pillar of violet and pink foxfire flames erupting from the ground, golden crescent moons in it"),
        ("orb", "a round violet foxfire orb with a golden crescent moon inside"),
        ("burst", "a round burst of violet and pink flame tongues radiating outward"),
        ("moon", "one small golden crescent moon"),
    ],
    "hoa_tinh": [
        ("bite", "a big biting jaw made of coral-red flame: two curved rows of white fangs closing, with flame tongues"),
        ("crystal", "a cluster of big pointed ruby crystals erupting upward from the ground with coral flames between them"),
        ("orb", "a round faceted ruby orb wrapped in a ring of coral flame"),
        ("burst", "a round burst of ruby shards and coral flame tongues"),
        ("gem", "one small faceted ruby gem"),
        ("howl", "three curved sound-wave arcs of coral-pink flame opening to the right"),
    ],
    "lan_hoa": [
        ("tail", "a big crescent arc of red and gold flame swept by a tail, curving down to the right"),
        ("orb", "a round golden flame pearl with red cloud curls around it"),
        ("qilin", "a fire qilin spirit made of red and golden flames leaping down to the right, antlers and flowing mane"),
        ("burst", "a round burst of red and golden flames with small cloud curls"),
        ("cloud", "one small curling cloud of red and gold flame"),
        ("ring", "a flat ring of golden flames and red cloud curls seen in perspective on the ground (a wide ellipse)"),
    ],
    "lan_hoa_b": [
        ("pillar", "a tall pillar of holy golden and white-gold flame pouring down from the sky onto the ground"),
        ("feathers", "a swirling burst of long flame feathers in red, orange and gold"),
        ("halo", "a ring of golden flames with small jade-green gems, like a halo"),
        ("roar", "a vertical fan of big red-and-gold flame arcs expanding to the right with cloud curls"),
        ("meteor", "a big golden fireball falling with a long red flame trail streaming up behind it"),
        ("seal", "a round golden seal of flame with a cloud pattern, seen in perspective on the ground (a wide ellipse)"),
    ],
    # đảo Kim (2026-11-09, build_kim.py): tờ kim loại chung thay bộ NƯỚC mặc định, mỗi dòng một tờ, Kim Nghê thêm tờ thứ hai
    "kim_chung": [
        # lần đầu (lưỡi thép, gai) bị công cụ vẽ ảnh của Codex chặn: tả bằng tấm kim loại, dải bạc, tia lửa
        ("ring", "a flat ring of small silver metal plates and gold rivets seen in perspective on the ground (a wide ellipse, about "
                 "three times wider than tall)"),
        ("whirl", "a whirl seen from the front: a wide ring of curved silver ribbons and small gold stars swirling around an "
                  "empty centre"),
        ("wave", "a low rolling wave of silver metal plates and gold chips moving along the ground to the right, its crest "
                 "curling forward"),
        ("burst", "a round burst seen from the front: a ring of small silver diamond-shaped chips and four-pointed yellow stars "
                  "radiating outward from an empty centre"),
        ("pillar", "a tall upright column of silver ribbons and gold chips spiralling up from the ground, wide at the base"),
        ("spark", "one small four-pointed yellow star"),
    ],
    "bo_cap": [
        ("pinch", "a pincer-snap burst: two thick curved arcs of bronze closing on a star-shaped burst, turquoise crystal chips"),
        ("sting", "a narrow star burst pointing down-right with turquoise crystal chips"),
        ("crystals", "a cluster of big pointed turquoise crystal spikes in bronze rims erupting upward from a cracked ground"),
        ("orb", "a round faceted turquoise crystal orb set in a bronze ring"),
        ("burst", "a round burst of turquoise crystal shards and bronze chips flying outward"),
        ("shard", "one small faceted turquoise crystal shard"),
    ],
    "doc_giac": [
        ("horn", "a drill-like spiral cone of silver and gold pointing to the right, a star burst at its tip"),
        ("charge", "a long horizontal charge trail streaming to the left: crimson ribbons like a flowing mane and silver streaks"),
        ("burst", "a round burst of silver armour shards and crimson ribbon strands flying outward"),
        ("orb", "a round golden orb with a turquoise gem in the middle and a spiral horn pattern around it"),
        ("crest", "a big royal crest shield of silver and gold with a unicorn head, rimmed with crimson ribbons"),
        ("star", "one small four-pointed gold star"),
    ],
    "bo_ngua": [
        ("slash", "one big crescent-moon swoosh arc of steel blue and silver, curving down to the right"),
        ("cross", "an X-shaped pair of crossing steel-blue crescent swoosh arcs with small green leaf shards"),
        ("orb", "a round jade-green orb with a crescent moon shape inside and a ruby dot"),
        ("burst", "a round burst of jade-green and steel shards flying outward"),
        ("whirl", "a whirlwind of many silver crescent swooshes spinning around an empty centre, seen from the front"),
        ("blade", "one small silver crescent moon shape"),
    ],
    "phi_thuong": [
        ("lance", "a giant long faceted sapphire-blue crystal shard pointing straight DOWN with a gold band, falling from above"),
        ("thrust", "a long straight speed streak to the right, steel-blue, ending in a star-shaped burst at its tip"),
        ("quill", "one long steel-blue porcupine quill with a gold tip, flying to the right"),
        ("orb", "a round crystal orb, its left half sapphire blue and its right half ruby red, in a gold ring"),
        ("burst", "a round burst of steel-blue quills radiating outward"),
        ("crater", "a round crater seen in perspective on the ground (a wide ellipse) with crystal shards and quills "
                   "sticking out of it"),
    ],
    "khien_bac": [
        ("bash", "a shield-bash impact: a big arrowhead-shaped shield outline of sky blue with radiating impact lines"),
        ("wave", "a low wave of sky-blue and silver shield plates rolling along the ground to the right"),
        ("wall", "a row of three big tall sky-blue kite shields with green gems erupting upward from the ground like a wall"),
        ("orb", "a round sky-blue shield emblem orb with a green gem and a small gold cross"),
        ("burst", "a round burst of silver-blue armour shards flying outward"),
        ("gem", "one small faceted green gem"),
    ],
    "chien_than": [
        ("shell", "a big golden cannon shell with sky-blue bands falling DOWN steeply, a short sky-blue trail streaming up behind"),
        ("blast", "a cannon muzzle-blast: a star-shaped burst of gold and sky-blue petals opening to the right"),
        ("rings", "three golden shock rings opening to the right, getting bigger outward"),
        ("orb", "a round golden orb with an emerald gem in the middle like an owl eye, sky-blue rim"),
        ("burst", "a round burst of golden feathers and sky-blue shards flying outward"),
        ("feather", "one small golden feather"),
    ],
    "thiet_phu": [
        ("axe", "one big crescent swoosh arc of grey steel with a red edge, curving down to the right"),
        ("whirl", "a horizontal whirlwind of grey and red crescent arcs spinning around an empty centre"),
        ("crack", "a ground smash: a round crater in perspective with rock chips, brass rivets and yellow sparks flying up"),
        ("orb", "a round red iron orb with brass rivets and a white plume on top"),
        ("burst", "a round burst of red iron chunks, brass rivets and yellow sparks"),
        ("bolt", "one small brass rivet bolt"),
    ],
    "tam_kiem": [
        ("slash_b", "one big crescent swoosh arc of sapphire blue, curving down to the right"),
        ("slash_r", "one big crescent swoosh arc of ruby red, curving up to the right"),
        ("cross", "three crossing crescent swoosh arcs, sapphire blue, ruby red and gold, meeting in a star burst"),
        ("orb", "a round golden orb with a V-shaped crest on it and three tiny gold stars around"),
        ("burst", "a round burst of white and gold diamond chips and small blue and red chips"),
        ("seal", "a round golden seal with a three-pointed crown pattern, seen in perspective on the ground (a wide ellipse)"),
    ],
    "ung_thep": [
        ("talon", "three parallel curved claw-mark streaks of mint crystal and silver, slanting down to the right"),
        ("feather", "one long mint crystal feather flying to the right"),
        ("gust", "a horizontal gust of curved wind arcs with small mint crystal feathers in it, blowing to the right"),
        ("orb", "a round mint crystal orb inside an orange ring"),
        ("burst", "a round burst of mint crystal shards and silver feathers"),
        ("whirl", "a whirl of six long mint crystal feathers spinning around an empty centre, seen from the front"),
    ],
    "kim_nghe": [
        ("bite", "a big chomp shape made of sapphire-blue flame: two curved rows of white teeth closing, gold chips"),
        ("claw", "three parallel curved claw-slash streaks of sapphire-blue flame, slanting down to the right"),
        ("spirit", "a nghe guardian spirit (a fox-lion beast) made of sapphire-blue flames with golden armour pieces, leaping "
                   "down to the right"),
        ("orb", "a round sapphire-blue flame orb inside a golden ring engraved with clouds"),
        ("burst", "a round burst of sapphire-blue flame tongues and gold shards"),
        ("flame", "one small sapphire-blue flame tuft"),
    ],
    "kim_nghe_b": [
        ("pillar", "a tall pillar of sapphire-blue and pale-blue flame pouring down from the sky onto the ground"),
        ("seal", "a round golden seal with a cloud pattern and blue gems, seen in perspective on the ground (a wide ellipse)"),
        ("halo", "a ring of golden armour plates and sapphire gems, like a halo"),
        ("roar", "a vertical fan of big sapphire-blue flame arcs expanding to the right with golden cloud curls"),
        ("meteor", "a big golden meteor falling with a long sapphire-blue flame trail streaming up behind it"),
        ("blades", "a swirling burst of golden crescents and sapphire-blue flame tongues"),
    ],
    # đảo Thổ (2026-11-10, build_tho.py): tờ đất đá chung thay bộ NƯỚC mặc định, mỗi dòng một tờ, Giáp Nham thêm tờ thứ hai
    "tho_chung": [
        ("ring", "a flat ring of small brown and grey pebbles and dust puffs seen in perspective on the ground (a wide ellipse, "
                 "about three times wider than tall)"),
        ("whirl", "a whirl seen from the front: a wide ring of curved sand-coloured dust ribbons and small pebbles swirling "
                  "around an empty centre"),
        ("wave", "a low rolling wave of brown earth and grey rock chunks moving along the ground to the right, its crest "
                 "curling forward"),
        ("burst", "a round burst seen from the front: a ring of small grey rock chips and sand-coloured dust puffs radiating "
                  "outward from an empty centre"),
        ("pillar", "a tall upright column of brown earth and grey rock chunks erupting up from the ground, wide at the base"),
        ("spark", "one small grey pebble"),
    ],
    "thach_nhan": [
        ("fist", "a punch impact: a big star-shaped burst of olive-grey stone chips and moss-green bits"),
        ("boulder", "one round mossy grey-olive boulder with a moss tuft on top, flying to the right"),
        ("spikes", "a cluster of big square-topped olive-grey stone pillars with moss and a green spiral carving erupting upward "
                   "from a cracked ground"),
        ("orb", "a round olive-grey stone orb with a green spiral carved on it and a moss tuft"),
        ("burst", "a round burst of olive-grey rock chunks and green moss bits flying outward"),
        ("pebble", "one small mossy grey stone"),
    ],
    "lung_vuong": [
        ("claw", "three parallel curved claw-mark streaks of gold, slanting down to the right"),
        ("dig", "a mound of brown earth bursting up from the ground with flying dirt clods and a few blue crystal chips"),
        ("whirl", "a whirlwind of brown dust ribbons and golden crescent claw arcs spinning around an empty centre, seen from "
                  "the front"),
        ("orb", "a round sapphire-blue crystal orb inside a golden ring"),
        ("burst", "a round burst of brown dirt clods and blue crystal chips flying outward"),
        ("crystal", "one small faceted blue crystal"),
    ],
    "cao_da": [
        ("claw", "three parallel curved claw-mark streaks of emerald green, slanting down to the right"),
        ("spikes", "a cluster of big pointed emerald-green stone spikes erupting upward from a cracked ground"),
        ("shard", "one long pointed emerald-green stone shard flying to the right"),
        ("orb", "a round emerald-green stone orb with a deep-blue gem in the middle"),
        ("burst", "a round burst of emerald-green stone shards flying outward"),
        ("ring", "a ring made of a twisted red-and-white rope, seen in perspective on the ground (a wide ellipse)"),
    ],
    "ho_khoan": [
        ("drill", "a spiral ruby-red crystal drill cone pointing to the right, a star burst of rock chips at its tip"),
        ("cracker", "a popping firecracker burst: small red paper scraps, gold curls and four-pointed yellow stars flying out"),
        ("crystals", "a cluster of big jagged emerald-green crystals erupting upward from a cracked ground"),
        ("orb", "a round red gem orb set in a golden lion-dance mount with curly cloud trims"),
        ("burst", "a round burst of emerald crystal shards and small red paper scraps flying outward"),
        ("shard", "one small jagged emerald crystal"),
    ],
    "phu_van": [
        ("seal", "a round stone seal carved with teal square rune glyphs, seen in perspective on the ground (a wide ellipse)"),
        ("crack", "a ground stomp: a round crater in perspective with blue-grey rock slabs tilting up and dust puffs"),
        ("obelisk", "a tall blue-grey stone obelisk carved with teal rune glyphs rising up from a cracked ground"),
        ("orb", "a round blue-grey stone orb carved with one teal square rune glyph"),
        ("burst", "a round burst of blue-grey rock chunks with teal rune marks flying outward"),
        ("glyph", "one small square blue-grey stone with a teal rune carved on it"),
    ],
    "hat_de": [
        ("acorn", "one big brown acorn with a crosshatched cap flying to the right, short speed lines behind it"),
        ("bash", "a shield-bash impact: a big round acorn-shell shield outline with radiating impact lines"),
        ("fall", "a big brown acorn falling DOWN steeply, a short trail of brown leaves streaming up behind it"),
        ("orb", "a round golden acorn orb with a sky-blue band"),
        ("burst", "a round burst of acorn shell bits and small brown leaves flying outward"),
        ("leaf", "one small brown oak leaf"),
    ],
    "rua_nui": [
        ("quake", "a wide ground crack seen in perspective (a wide ellipse) with brown rock slabs tilting up around it"),
        ("peak", "a small rocky brown mountain peak with green grassy ledges erupting up from the ground"),
        ("boulder", "a big brown boulder falling DOWN steeply, a short trail of dust puffs streaming up behind it"),
        ("orb", "a round mossy pebble orb with a little two-leaf sprout on top"),
        ("burst", "a round burst of brown rocks and green leaves flying outward"),
        ("crystal", "one small ice-blue crystal"),
    ],
    "ho_kim_cuong": [
        ("diamond", "a giant long faceted pale-violet diamond crystal pointing straight DOWN, falling from above"),
        ("drill", "a long spiral ruby-red crystal drill cone pointing to the right with gold bands"),
        ("storm", "a whirl of many long pale-violet diamond crystal blades spinning around an empty centre, seen from the front"),
        ("orb", "a round pale-violet faceted diamond orb in a golden ring with emerald dots"),
        ("burst", "a round burst of pale-violet diamond shards and gold chips flying outward"),
        ("shard", "one small faceted pale-violet diamond"),
    ],
    "cu_phu": [
        ("axe", "one big crescent swoosh arc of violet steel with a golden edge, curving down to the right"),
        ("crack", "a ground smash: a round crater in perspective with golden-sand crystal chunks flying up"),
        ("whirl", "a horizontal whirlwind of violet and gold crescent arcs spinning around an empty centre"),
        ("orb", "a round golden-sand crystal orb with a teal gem and a small red-orange crystal plume"),
        ("burst", "a round burst of golden-sand crystal chunks and red-orange crystal chips"),
        ("gem", "one small faceted teal gem"),
    ],
    "giap_nham": [
        ("punch", "a punch impact: a big star burst of sharp angular golden rays with lime-green trims"),
        ("scales", "a spray of angular golden scales flying to the right in a fan"),
        ("pillar", "a tall column of angular golden crystal slabs rising up from a cracked ground"),
        ("orb", "a round golden orb with a green gem in the middle and angular gold rays around it"),
        ("burst", "a round burst of angular golden shards and small crimson ribbon strands"),
        ("scale", "one small angular golden scale"),
    ],
    "giap_nham_b": [
        ("meteor", "a big angular golden boulder falling with a long crimson ribbon trail streaming up behind it"),
        ("seal", "a round golden seal with an angular scale pattern and a green gem, seen in perspective on the ground (a wide "
                 "ellipse)"),
        ("halo", "a ring of angular golden scale plates and green gems, like a halo"),
        ("roar", "a vertical fan of big angular golden arcs expanding to the right with crimson ribbon curls"),
        ("quake", "a wide ring of golden rock slabs tilting up out of the ground, seen in perspective (a wide ellipse)"),
        ("blades", "a swirling burst of golden crescents and crimson ribbons"),
    ],
}
KIM = {"kim_chung", "bo_cap", "doc_giac", "bo_ngua", "phi_thuong", "khien_bac", "chien_than", "thiet_phu", "tam_kiem",
       "ung_thep", "kim_nghe", "kim_nghe_b"}
HOA = {"hoa_chung", "su_tu_lua", "khong_lo", "kim_su", "nham_than", "nguu_quyen", "hong_lien", "giap_long", "huyen_viem",
       "hoa_tinh", "lan_hoa", "lan_hoa_b"}
THO = {"tho_chung", "thach_nhan", "lung_vuong", "cao_da", "ho_khoan", "phu_van", "hat_de", "rua_nui", "ho_kim_cuong",
       "cu_phu", "giap_nham", "giap_nham_b"}


def paths(hid):
    out_dir = W(HERE, "gui_gpt", "fx_" + hid)
    save_dir = W(HERE, "inbox", "fx", hid, "tai_ve")
    return out_dir, save_dir, W(save_dir, "sheet.png")


def luot_1(hid):
    out_dir, save_dir, save = paths(hid)
    items = SHEETS[hid]
    refs = [(W(REF, "FX03.png"), "an approved effect of the same game (a water splash burst), 1024x1024: match EXACTLY its hand-drawn "
                                 "line, crayon texture and flat colouring"),
            (W(REF, "FX07.png"), "another approved effect of the same game (a wave), 1024x1024: same style reference"),
            (WORLD_STYLE, "the game's hand-drawn map, 1024x1536; use ONLY its line and colouring style, nothing of its content")]
    img = "\n".join(f"image {i + 1} = {p}: {d}." for i, (p, d) in enumerate(refs))
    cells = ["top-left", "top-middle", "top-right", "bottom-left", "bottom-middle", "bottom-right"]
    lst = "\n".join(f"{j + 1}. {cells[j]} cell: {d}." for j, (_n, d) in enumerate(items))
    boss = ""
    if hid.split("_b")[0] in ("kuba", "huyen_vu", "lam_quan", "thuong_lam", "gio_loc", "tho_hoang", "thanh_long", "hong_lien",
                              "giap_long", "huyen_viem", "hoa_tinh", "lan_hoa", "chien_than", "thiet_phu", "tam_kiem",
                              "ung_thep", "kim_nghe", "hat_de", "rua_nui", "ho_kim_cuong", "cu_phu",
                              "giap_nham") or hid.endswith("_b"):
        boss = ("\nThese effects belong to one of the island's last bosses: make them especially rich and beautiful (more "
                "layered shapes, elegant curls and details), still flat-coloured and readable.")
    fire = ""
    if hid in HOA:
        fire = ("\nFIRE: every flame is a flat shape with a closed dark-brown ink outline, filled with flat crayon colours in at "
                "most three clear bands (red outer, orange middle, yellow inner, or the colours stated for that effect), never "
                "left as white paper; lava is flat orange and yellow. Nothing glows: no light, no halo, no bright edges, no "
                "smoke or heat haze.")
    if hid in KIM:
        fire = ("\nMETAL: steel, gold, bronze, crystal and gems are flat shapes with a closed dark-brown ink outline, each one "
                "flat crayon colour (plus a few darker facet or edge lines); no shine spots, no white highlights, no "
                "reflections, no metallic gradients; sparks are flat yellow four-pointed stars with a dark outline; flames (if "
                "any) are flat shapes in at most three colour bands. Nothing glows: no light, no halo, no bright edges.")
    if hid in THO:
        fire = ("\nEARTH: rocks, stones, earth, sand, crystals and gems are flat shapes with a closed dark-brown ink outline, "
                "each one flat crayon colour (plus a few darker crack or facet lines); dust puffs are flat sand-coloured "
                "cloud shapes with an outline; no shine spots, no white highlights, no reflections, no gradients; carved "
                "runes are flat colour lines. Nothing glows: no light, no halo, no bright edges.")
    t = f"""IMAGES (attached in this order; open each from its path):
{img}

SAVE: save it as a PNG to {save}
If a file with that name already exists, save as sheet_2.png, sheet_3.png ... in the same folder. Do not edit, move or delete any other file.

TASK: draw a SHEET OF SIX SEPARATE GAME EFFECT SPRITES in the hand-drawn style of images 1 and 2.

LAYOUT (very important, the sheet is cut automatically): landscape 1536x1024, pure-white background, divided into an invisible grid of 3 columns x 2 rows of 512x512 cells. Draw exactly ONE effect in each cell, centred, filling about 75% of the cell, every part (drops and sparks included) at least 40 px inside its cell: nothing crosses into a neighbouring cell. No grid lines, no numbers, no labels.
{lst}{boss}

STYLE: drawn by hand on paper with a dark-brown ink pen (#2B2118) outline about 6 px thick, slightly wobbly; coloured with coloured pencils and wax crayons, visible diagonal hatching. Colours exactly as described for each effect (water blue and aqua with white foam; ice pale blue and white; leaves and vines green; flowers as stated; crystals as stated; lightning flat yellow with a dark outline, never glowing).{fire}
{FLAT}
Plain pure-white background (#FFFFFF), no creature, no character, no text.
"""
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(save_dir, exist_ok=True)
    p = W(out_dir, "luot_1_lien.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)
    return p


# hình vòng (vòng lửa dưới đất, lốc, nổ hở giữa, vòng gai): lòng giấy trắng khép kín phải trong suốt, không thì lên sân thành
# đĩa trắng đục (fg_mask chỉ bỏ nền trắng nối mép ô)
HOLLOW = {"hoa_chung_ring", "hoa_chung_whirl", "hoa_chung_burst", "lan_hoa_ring", "lan_hoa_b_halo", "giap_long_spikes",
          "kim_chung_ring", "kim_chung_whirl", "kim_chung_burst", "bo_ngua_whirl", "thiet_phu_whirl", "ung_thep_whirl",
          "kim_nghe_b_halo", "chien_than_rings",
          "tho_chung_ring", "tho_chung_whirl", "tho_chung_burst", "lung_vuong_whirl", "ho_kim_cuong_storm", "cu_phu_whirl",
          "giap_nham_b_halo", "giap_nham_b_quake", "cao_da_ring"}


def clear_holes(cell, m, min_area=400):
    """bỏ khỏi mặt nạ các mảng trắng (giấy, mọi kênh >= 238) khép kín rộng hơn min_area px."""
    import cv2
    import numpy as np
    white = (cell.min(2) >= 238).astype(np.uint8) & m.astype(np.uint8)
    n, cl, st, _ = cv2.connectedComponentsWithStats(white, connectivity=4)
    out = m.copy()
    for c in range(1, n):
        if st[c, cv2.CC_STAT_AREA] >= min_area:
            out[cl == c] = False
    return out


def cat(hid):
    """cắt tờ theo ô 3x2: nền trắng nối mép thành trong suốt (giữ trắng bên trong như bọt), cắt sát, lưu inbox/fx/<id>_<tên>.png."""
    import numpy as np
    from PIL import Image
    sys.path.insert(0, HERE)
    import rig as riglib
    _o, save_dir, save = paths(hid)
    cands = sorted([f for f in os.listdir(save_dir) if f.lower().endswith(".png")],
                   key=lambda f: os.path.getmtime(os.path.join(save_dir, f)))
    if not cands:
        print("chưa có tờ:", hid)
        return
    im = Image.open(os.path.join(save_dir, cands[-1])).convert("RGB")
    im = im.resize((1536, 1024), Image.LANCZOS) if im.size != (1536, 1024) else im
    a = np.array(im)
    for j, (name, _d) in enumerate(SHEETS[hid]):
        cx, cy = (j % 3) * 512, (j // 3) * 512
        cell = a[cy + 6:cy + 506, cx + 6:cx + 506]
        m = riglib.fg_mask(cell)
        if not m.any():
            print("  ô trống:", name)
            continue
        if f"{hid}_{name}" in HOLLOW:
            m = clear_holes(cell, m)
        rgba = riglib.to_rgba(cell, m)
        ys, xs = np.nonzero(m)
        out = Image.fromarray(rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
        os.makedirs(OUT, exist_ok=True)
        p = os.path.join(OUT, f"{hid}_{name}.png")
        out.save(p, optimize=True)
        print(" ", p, out.size)


def main(argv):
    if argv and argv[0] == "--cat":
        for hid in argv[1:] or list(SHEETS):
            cat(hid)
        return
    for hid in argv or list(SHEETS):
        print(luot_1(hid))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
