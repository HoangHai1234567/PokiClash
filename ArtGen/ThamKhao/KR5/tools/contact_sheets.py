# Tờ khung để học: mỗi hiệu ứng một tờ, mọi khung xếp lưới, đánh số, trên nền xám giữa (thấy rõ mép mềm / mép cứng).
#   py -3 -I tools/contact_sheets.py [no,lua,nuoc,khoi]
# Đọc ../fx_viewer/data.json + sheets/ + exo/ (chạy build_fx_viewer.py trước). Ghi ../to_khung/<nhóm>__<tên>.jpg và so_lieu.json
import os, sys, json, math
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FV = os.path.join(BASE, 'fx_viewer')
OUT = os.path.join(BASE, 'to_khung')
os.makedirs(OUT, exist_ok=True)
D = json.load(open(os.path.join(FV, 'data.json'), encoding='utf-8'))
A = D['assets']
RS = 0.5
BG = (112, 114, 106, 255)

PICK = {
    'no': ['a:explosion_big', 'a:explosion_KR5_big', 'a:explosion_air', 'a:explode_big', 'a:fireball_explosion', 'a:explosion_fragment',
           'a:tower_dwarf_skill_main_explosion_idle', 'a:cluster_bomb_main_explosion_idle', 'a:dwarven_flamespitter_tower_blazing_trail_explosion_idle',
           'a:ballista_tower_bomb_explotion_idle', 'a:hero_lava_ultimate_hit', 'a:veznan_wrath_explosion_fx_idle',
           'a:rocket_gunners_tower_phosphoric_coating_explosion_idle', 'a:hermit_toad_tower_explosion2_idle', 'x:explosionDef|idle',
           'x:boss_gator_lvl3_explosionDef|run', 'a:hero_dragon_bone_plague_explosion_idle', 'a:elven_stargazers_tower_rising_star_explosion_idle'],
    'lua': ['a:fire_small', 'a:fire_medium', 'a:fire_large', 'a:tower_dwarf_fire_modifier_big', 'a:dwarven_flamespitter_tower_scorching_torches_fx_idle',
            'a:dwarven_flamespitter_tower_blazing_trail_path_fx_idle', 'a:dwarven_flamespitter_tower_blazing_trail_projectile_idle',
            'a:hero_evil_dragon_breath_idle', 'a:hero_dragon_bone_breath_idle', 'a:gryph_skillproy_fire_run', 'a:tricannon_tower_overheat_fire_fx',
            'a:hero_lava_ultimate_projectile_idle', 'x:BonfireDef|loop', 'x:DLCDwarfFireDef|loop', 'a:dwarven_flamespitter_tower_scorching_torches_particle_idle',
            'a:hero_lava_skill_4_hit'],
    'nuoc': ['a:hermit_toad_tower_splash_run', 'a:hermit_toad_tower_bubbles_run', 'a:hero_dragon_arborean_water_projectile_run',
             'a:hero_dragon_arborean_water_hit_fx_idle', 'a:hero_dragon_arborean_water_ground_fx_idle', 'a:hero_dragon_arborean_water_projectile_trail_idle',
             'x:WaterSparksDef|loop', 'x:WavesRiverDef|loop', 'a:demon_pit_tower_lvl4_tower_front_splash', 'a:noxious_horror_projectile_splash',
             'a:barrel_tower_lvl4_bad_barrel_bubbles_fx_loop', 'x:RockRipplesDef|loop', 'a:fx_water_splash_big', 'a:fx_water_splash_small',
             'a:fx_water_bubble_big', 'a:enemy_water_splash_small', 'a:DLC_stage_03_missile_water_splash', 'a:decal_water_splash_play'],
    'khoi': ['a:tower_build_dust', 'a:tower_sell_dust', 'a:desintegrate_enemy_big', 'a:Blaze_skill2humo_loop', 'a:rocket_gunners_tower_take_off_fx_idle',
             'a:rocket_gunners_tower_sting_missiles_floor_decal_smoke_idle', 'a:dust_cryptid_dust_fx_loop', 'a:anya_mist_run_in',
             'a:ballista_tower_missed_arrow_dust', 'x:SmokeBonfireDef|loop', 'x:DLCDwarfSmokeDef|loop', 'x:VaporCraterDef|loop',
             'a:cutthroat_rat_attack_2_smokeFX', 'a:hero_dragon_bone_cloud_idle', 'a:Blaze_skill1humito_run'],
}
# tên anim chung có thể khác: dò theo tiền tố
ALIASES = {}
for k in list(A):
    ALIASES.setdefault(k.lower(), k)

try:
    FONT = ImageFont.truetype('arial.ttf', 22)
    FONT_S = ImageFont.truetype('arial.ttf', 18)
except Exception:
    FONT = FONT_S = ImageFont.load_default()

_img = {}
def sheet(name):
    if name not in _img: _img[name] = Image.open(os.path.join(FV, 'sheets', name)).convert('RGBA')
    return _img[name]


def frames_a(a):
    """trả list ảnh khung (cùng cỡ, căn theo toạ độ ảnh đầy đủ)"""
    im = sheet(a['img'])
    cells = a['cells']
    x0 = min(c[4] for c in cells if c[2]); y0 = min(c[5] for c in cells if c[2])
    x1 = max(c[4] + c[2] for c in cells if c[2]); y1 = max(c[5] + c[3] for c in cells if c[2])
    out = []
    for i in a['seq']:
        c = cells[i]; fr = Image.new('RGBA', (x1 - x0, y1 - y0), (0, 0, 0, 0))
        if c[2]: fr.paste(im.crop((c[0], c[1], c[0] + c[2], c[1] + c[3])), (c[4] - x0, c[5] - y0))
        out.append(fr)
    return out


def loveM(x, y, r, sx, sy, ox, oy, kx, ky):
    c, s = math.cos(r), math.sin(r)
    a = c * sx - ky * s * sy; b = s * sx + ky * c * sy; cc = kx * c * sx - s * sy; d = kx * s * sx + c * sy
    return [a, b, cc, d, x - ox * a - oy * cc, y - ox * b - oy * d]


def mul(m, n):
    a, b, c, d, e, f = m; A_, B, C, D_, E, F = n
    return [a * A_ + c * B, b * A_ + d * B, a * C + c * D_, b * C + d * D_, a * E + c * F + e, b * E + d * F + f]


def inv(m):
    a, b, c, d, e, f = m; det = a * d - b * c
    if abs(det) < 1e-12: return None
    ia, ib, ic, id_ = d / det, -b / det, -c / det, a / det
    return [ia, ib, ic, id_, -(ia * e + ic * f), -(ib * e + id_ * f)]


def frames_x(a, scale=2.0):
    meta = D['exos'][a['exo']]
    ex = json.load(open(os.path.join(FV, meta['f']), encoding='utf-8'))
    im = sheet(ex['img'])
    frs = ex['anims'][a['anim']]
    # hộp bao
    pts = []
    for fr in frs:
        for p in fr:
            pm = ex['parts'][p[0]]
            if not pm or not pm[2] or p[8] <= 0: continue
            po = ex['po'][p[0]]; x, y, w, h, dx, dy, W, H = pm
            m = loveM(p[1], p[2], p[3], p[4] * RS, p[5] * RS, 0.5 * W - po[0] / RS, 0.5 * H - po[1] / RS, p[6], p[7])
            for u, v in ((dx, dy), (dx + w, dy), (dx, dy + h), (dx + w, dy + h)):
                pts.append((m[0] * u + m[2] * v + m[4], m[1] * u + m[3] * v + m[5]))
    if not pts: return []
    bx0 = min(p[0] for p in pts); by0 = min(p[1] for p in pts); bx1 = max(p[0] for p in pts); by1 = max(p[1] for p in pts)
    Wd, Hd = int((bx1 - bx0) * scale) + 2, int((by1 - by0) * scale) + 2
    V = [scale, 0, 0, scale, -bx0 * scale, -by0 * scale]
    out = []
    for fr in frs:
        canvas = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0))
        for p in fr:
            pm = ex['parts'][p[0]]
            if not pm or not pm[2] or p[8] <= 0: continue
            po = ex['po'][p[0]]; x, y, w, h, dx, dy, W, H = pm
            m = mul(V, loveM(p[1], p[2], p[3], p[4] * RS, p[5] * RS, 0.5 * W - po[0] / RS, 0.5 * H - po[1] / RS, p[6], p[7]))
            m = mul(m, [1, 0, 0, 1, dx, dy])
            # chỉ biến đổi trong hộp bao của mảnh
            cs = [(m[0] * u + m[2] * v + m[4], m[1] * u + m[3] * v + m[5]) for u, v in ((0, 0), (w, 0), (0, h), (w, h))]
            qx0 = max(0, int(math.floor(min(c[0] for c in cs)))); qy0 = max(0, int(math.floor(min(c[1] for c in cs))))
            qx1 = min(Wd, int(math.ceil(max(c[0] for c in cs))) + 1); qy1 = min(Hd, int(math.ceil(max(c[1] for c in cs))) + 1)
            if qx1 <= qx0 or qy1 <= qy0: continue
            m = mul([1, 0, 0, 1, -qx0, -qy0], m)
            iv = inv(m)
            if not iv: continue
            part = im.crop((x, y, x + w, y + h))
            if p[8] < 1:
                al = part.getchannel('A').point(lambda v, k=p[8]: int(v * k)); part.putalpha(al)
            layer = part.transform((qx1 - qx0, qy1 - qy0), Image.AFFINE, (iv[0], iv[2], iv[4], iv[1], iv[3], iv[5]), resample=Image.BILINEAR)
            canvas.alpha_composite(layer, (qx0, qy0))
        out.append(canvas)
    return out


def stats(frames):
    soft = solid = 0; cols = {}
    for fr in frames[::max(1, len(frames) // 6)]:
        sm = fr.resize((max(1, fr.width // 3), max(1, fr.height // 3)))
        for r, g, b, al in (sm.get_flattened_data() if hasattr(sm, 'get_flattened_data') else sm.getdata()):
            if al < 8: continue
            if al < 230: soft += 1
            else: solid += 1
            k = (r >> 4, g >> 4, b >> 4); cols[k] = cols.get(k, 0) + al / 255
    tot = max(1, soft + solid)
    top = sorted(cols.items(), key=lambda kv: -kv[1])[:10]
    return {'soft_pct': round(100 * soft / tot), 'top_colors': ['#%02x%02x%02x' % (c[0] * 17, c[1] * 17, c[2] * 17) for c, _ in top]}


def contact(key, frames, title, path, maxw=2200):
    n = len(frames)
    fw, fh = frames[0].size
    sc = min(1.0, 260 / max(fw, fh)) if max(fw, fh) > 260 else 1.0
    cw, ch = max(60, int(fw * sc)), max(60, int(fh * sc))
    cols = max(1, min(n, maxw // (cw + 8)))
    rows = (n + cols - 1) // cols
    W = cols * (cw + 8) + 8; H = rows * (ch + 30) + 46
    out = Image.new('RGBA', (W, H), (40, 42, 46, 255))
    dr = ImageDraw.Draw(out)
    dr.text((10, 10), title, fill=(240, 230, 210, 255), font=FONT)
    for i, fr in enumerate(frames):
        x = 8 + (i % cols) * (cw + 8); y = 46 + (i // cols) * (ch + 30)
        cell = Image.new('RGBA', (cw, ch), BG)
        f2 = fr.resize((max(1, int(fw * sc)), max(1, int(fh * sc))), Image.LANCZOS) if sc != 1 else fr
        cell.alpha_composite(f2, ((cw - f2.width) // 2, (ch - f2.height) // 2))
        out.paste(cell, (x, y))
        dr.text((x + 3, y + ch + 3), str(i + 1), fill=(200, 200, 190, 255), font=FONT_S)
    out.convert('RGB').save(path, quality=90)


def main():
    only = set(sys.argv[1].split(',')) if len(sys.argv) > 1 else None
    res = json.load(open(os.path.join(OUT, 'so_lieu.json'), encoding='utf-8')) if os.path.exists(os.path.join(OUT, 'so_lieu.json')) else {}
    for grp, keys in PICK.items():
        if only and grp not in only: continue
        for key in keys:
            k = key if key in A else ALIASES.get(key.lower())
            if not k:
                cand = [x for x in A if x.lower().startswith(key.lower())]
                k = cand[0] if cand else None
            if not k: print('  thiếu', key); continue
            a = A[k]
            try:
                frs = frames_x(a) if a['t'] == 'x' else frames_a(a)
            except Exception as ex:
                print('  lỗi', k, ex); continue
            if not frs: continue
            st = stats(frs)
            nm = k[2:].replace('|', '_')
            fps = D['exos'][a['exo']]['fps'] if a['t'] == 'x' else 30
            info = {'grp': grp, 'n': len(frs), 'dur': round(len(frs) / fps, 2), 'size_game': [round(frs[0].width * (RS if a['t'] != 'x' else 0.5)), round(frs[0].height * (RS if a['t'] != 'x' else 0.5))],
                    'used': a.get('used', [])[:6], **st}
            if a['t'] != 'x' and len(a['seq']) != len(a['cells']): info['seq'] = [x + 1 for x in a['seq']]
            res[k] = info
            title = '%s  ·  %d khung · %.2f s · vùng hình %dx%d px ảnh · mép mềm %d%%' % (nm, len(frs), info['dur'], frs[0].width, frs[0].height, st['soft_pct'])
            contact(k, frs, title, os.path.join(OUT, '%s__%s.jpg' % (grp, nm[:90])))
            print('ok', grp, nm, len(frs), flush=True)
            json.dump(res, open(os.path.join(OUT, 'so_lieu.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(res, open(os.path.join(OUT, 'so_lieu.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
