# Vẽ phần tĩnh của mặt máy bi cho Unity (Assets/03 Art/Baked/Machine/may_tinh.png, 920 × 1360 = 2 lần khung 460 × 680),
# cùng nét với ảnh nướng cũ: nền trong suốt, mực nâu đen, đinh có chấm sáng, u tường nâu, cốc bạc, két vàng (mái ^, đáy V),
# ô gạch chéo hai mức đậm nhạt, vách có đầu tròn. Chữ số trên ô (TMP), rương nhỏ trong ô, cốc, két (prefab kit Ruong) và nấm
# (ảnh pk_bumper, phồng xẹp khi bị chạm; vẽ bằng draw_machine_fx.py) do MachineBoard đặt lúc chạy, không vẽ ở đây.
#   npx tsx scripts/export_board.ts > board.json
#   py -3 -I scripts/draw_machine.py board.json "../Assets/03 Art/Baked/Machine/may_tinh.png"
import json
import math
import sys

from PIL import Image, ImageDraw

OUT_K = 2  # px ảnh mỗi đơn vị máy
SS = 4  # vẽ to gấp SS rồi thu nhỏ cho mượt cạnh
K = OUT_K * SS

INK = (43, 33, 24, 255)
WHITE = (255, 255, 255, 255)
POST = (201, 138, 74, 255)
DOT = (232, 85, 63, 31)
SILVER = (223, 230, 238, 255)
GOLD = (255, 210, 74, 255)
VAULT_FILL = (255, 210, 74, 95)
SLOT_COLOR = {
    'chest_wood': (255, 224, 176), 'chest_gold': (255, 226, 122), 'chest_silver': (223, 230, 238),
    'ball': (255, 210, 226), 'exp15': (230, 210, 255), 'exp10': (239, 226, 255), 'exp5': (246, 239, 255),
}


def P(x, y):
    return (x * K, y * K)


def circle(d, x, y, r, fill=None, outline=None, width=0):
    d.ellipse([(x - r) * K, (y - r) * K, (x + r) * K, (y + r) * K], fill=fill, outline=outline, width=int(round(width * K)))


def line(d, x1, y1, x2, y2, w, color=INK):
    d.line([P(x1, y1), P(x2, y2)], fill=color, width=int(round(w * K)))
    # đầu nét tròn
    circle(d, x1, y1, w / 2, fill=color)
    circle(d, x2, y2, w / 2, fill=color)


def peg(d, x, y, r):
    circle(d, x, y, r, fill=INK)
    circle(d, x - 1.4 * r / 5, y - 1.4 * r / 5, r * 0.35, fill=WHITE)



def hatch(img, x0, y0, x1, y1, rgb):
    # gạch chéo 45°: sọc đậm (đục) xen sọc nhạt (alpha 89), chu kỳ 5 đơn vị
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([P(x0, y0), P(x1, y1)], fill=rgb + (89,))
    period = 5
    span = int((x1 - x0) + (y1 - y0)) + period
    for t in range(-span, span, period):
        # đường x - y = c qua khung
        c = x0 + t
        d.line([P(c, y1), P(c + (y1 - y0), y0)], fill=rgb + (255,), width=int(round(2 * K)))
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).rectangle([P(x0, y0), P(x1, y1)], fill=255)
    clipped = Image.new('RGBA', img.size, (0, 0, 0, 0))
    clipped.paste(layer, (0, 0), mask)
    img.alpha_composite(clipped)


def main(src, dst):
    b = json.load(open(src, encoding='utf-8'))
    BW, BH, LEFT, RIGHT, SLOT_TOP, DROP_Y = b['BW'], b['BH'], b['LEFT'], b['RIGHT'], b['SLOT_TOP'], b['DROP_Y']
    img = Image.new('RGBA', (int(BW * K), int(BH * K)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # chấm bi trang trí trên mặt chơi
    y = 80
    while y < SLOT_TOP - 10:
        x = LEFT + 12 + ((y / 22) % 2) * 11
        while x < RIGHT - 6:
            circle(d, x, y, 2.2, fill=DOT)
            x += 22
        y += 22

    segs = b['segs']
    # ô đáy (gạch chéo) rồi vách, đáy máy
    for sl in b['slots']:
        hatch(img, sl['x0'] + 1, SLOT_TOP, sl['x1'] - 1, BH - 8, SLOT_COLOR[sl['reward']])
    d = ImageDraw.Draw(img)
    for sg in segs:
        if sg['kind'] == 'divider':
            line(d, sg['x1'], sg['y1'], sg['x2'], sg['y2'] - 8, 3)
    line(d, LEFT, BH - 8, RIGHT, BH - 8, 3)

    # ray máng thả, vai nghiêng
    for sg in segs:
        if sg['kind'] == 'ceiling':
            line(d, sg['x1'] + 8, sg['y1'], sg['x2'] - 8, sg['y2'], 3)
        if sg['kind'] == 'shoulder':
            line(d, sg['x1'], sg['y1'], sg['x2'], sg['y2'], 4)

    # két vàng: thân tô vàng nhạt giữa mái và đáy, mái và đáy nét dày
    roof = [s for s in segs if s['kind'] == 'roof']
    floor = [s for s in segs if s['kind'] == 'floor']
    if len(roof) == 2 and len(floor) == 2:
        poly = [(roof[0]['x1'], roof[0]['y1']), (roof[0]['x2'], roof[0]['y2']), (roof[1]['x2'], roof[1]['y2']), (roof[1]['x1'], roof[1]['y1']),
                (floor[1]['x1'], floor[1]['y1']), (floor[1]['x2'], floor[1]['y2']), (floor[0]['x1'], floor[0]['y1'])]
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).polygon([P(x, y) for x, y in poly], fill=VAULT_FILL)
        img.alpha_composite(layer)
        d = ImageDraw.Draw(img)
        for s in roof + floor:
            line(d, s['x1'], s['y1'], s['x2'], s['y2'], 4.5)

    # đinh, u tường, cọc (nấm là ảnh động)
    for p in b['pegs']:
        x, y, r, kind = p['x'], p['y'], p['r'], p['kind']
        if kind == 'bumper':
            continue
        if kind == 'post' and r > 6:
            circle(d, x, y, r, fill=POST, outline=INK, width=2.5)
        else:
            peg(d, x, y, r)

    # cốc bạc (cốc tròn): hình thang
    for c in b['cups']:
        if c['r'] <= 0:
            continue
        w = 30
        x, y = c['x'], c['y']
        pts = [P(x - w / 2, y - 8), P(x - w / 2 + 5, y + 12), P(x + w / 2 - 5, y + 12), P(x + w / 2, y - 8)]
        d.polygon(pts, fill=SILVER if c['reward'] == 'chest_silver' else GOLD, outline=INK, width=int(round(3 * K)))

    img = img.resize((int(BW * OUT_K), int(BH * OUT_K)), Image.LANCZOS)
    img.save(dst)
    print('ghi', dst, img.size)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
