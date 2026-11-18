# Phần chính của build_fx_viewer.py (nạp khi chạy, không nạp trong tiến trình con)
# Đọc: lua_src (animation db, template qua luamini, exoskeleton), images/sprites (sprite đã cắt đúng cỡ gốc),
#      apk_unpacked/.../ipadhd/*.lua (atlas: size, trim, alias).
# Ghi: fx_viewer/data.json (template, hoạt ảnh, chiêu) + fx_viewer/sheets/*.png (mỗi hoạt ảnh một tấm, khung cắt sát).
import os, sys, re, json, math, glob
from multiprocessing import Pool
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from luamini import Interp, LTab, make_stdlib
from kr5_templates import load_templates, to_py

HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2 or not os.path.isdir(os.path.join(sys.argv[1], 'lua_src')):
    sys.exit('Cần đường dẫn tới bản rút Kingdom Rush 5 (thư mục có lua_src, images/sprites, apk_unpacked), '
             'vd. py -3 -I tools/build_fx_viewer.py D:/Ripper/KingdomRush5')
ROOT = os.path.abspath(sys.argv[1])   # bản rút (nguồn), chỉ đọc
LUA = os.path.join(ROOT, 'lua_src')
ATL = os.path.join(ROOT, 'apk_unpacked', 'assets', 'kr5-phone', 'images', 'ipadhd')
SPR = os.path.join(ROOT, 'images', 'sprites')
EXOD = os.path.join(LUA, 'kr5', 'data', 'exoskeletons')
OUT = os.path.join(os.path.dirname(HERE), 'fx_viewer')   # ghi cạnh thư mục tools/
SHEETS = os.path.join(OUT, 'sheets')
RS = 0.5            # ảnh ipadhd = 2 lần toạ độ game
MAXW = 4096

# ------------------------------------------------------------ nhóm hệ (theo từ khoá trong tên)
TAGS = [
    ('no', 'Nổ', r'explo|explot|blast|boom|burst|deton|kaboom|bomb|nuke|impact|shockwave|shock_wave|crater|grenade|missile|dynamite|cannon_explo|rocket'),
    ('lua', 'Lửa', r'fire|flam|burn|lava|magma|ember|inferno|blaz|heat|molten|scorch|pyro|meteor|napalm|torch|bonfire|candle|hellfire|ignit|incinerat|spark_fire|dragon_breath|breath'),
    ('nuoc', 'Nước', r'water|splash|wave|bubbl|drip|rain|tide|_sea|sea_|aqua|river|puddle|geyser|torrent|ripple|drown|foam|liquid|wet|droplet|tsunami|whirlpool|fish'),
    ('khoi', 'Khói / bụi', r'smoke|dust|steam|vapo|cloud|fog|mist|puff|gas|fume|_ash|ash_|soot|poof|smog|haze|dirt'),
    ('set', 'Sét / điện', r'lightn|thunder|electr|spark|shock|coil|tesla|zap|energy|beam|laser|plasma|ray_|_ray|rayo|bolt|static'),
    ('bang', 'Băng', r'ice|frost|freez|frozen|snow|winter|cold|glaci|blizz|chill'),
    ('doc', 'Độc / axit', r'poison|venom|acid|toxic|plague|blight|goo|slime|corrupt|ooze|sludge|bile|spit'),
    ('phep', 'Phép / ánh sáng', r'arcane|magic|holy|light(?!n)|heal|star(?!t|gazer)|glow|rune|spell|teleport|portal|bless|celest|divine|mana|soul|ghost|spirit|void|necro|curse|aura|halo|sparkle|shine|radian|judgement|crystal|summon|ritual'),
    ('dat', 'Đất / đá', r'rock|stone|earth|ground|crack|quake|debris|dirt|sand|boulder|rubble|tremor|fissure|mud|scrap|wood'),
    ('mau', 'Máu', r'blood|bleed|gore'),
    ('gio', 'Gió', r'wind|tornado|whirl|cyclone|gust|vortex|storm|twister|air_|_air'),
]
TAG_RE = [(k, re.compile(p)) for k, _, p in TAGS]
FXWORD = re.compile(r'fx|hit|decal|particle|trail|projectile|proy|bullet|aura|spawn|effect|impact|explo|smoke|fire|flame|'
                    r'splash|spark|glow|ray|beam|bolt|bomb|blast|dust|cloud|mod_|_mod|ps_|bubble|wave|'
                    r'teleport|heal|death_fx|smoke|steam|lava|poison|venom|acid|frost|lightning')


def tags_of(*names):
    s = ' '.join(n.lower() for n in names if n)
    return [k for k, rx in TAG_RE if rx.search(s)]


# ------------------------------------------------------------ atlas: tên sprite -> (thư mục atlas, tên file gốc, size, trim)
sprites = {}
for f in glob.glob(os.path.join(ATL, '*.lua')):
    base = os.path.splitext(os.path.basename(f))[0]
    t = open(f, encoding='utf-8').read()
    for m in re.finditer(r'\["([^"]+)"\]=\{size=\{(\d+),(\d+)\}, trim=\{(-?\d+),(-?\d+),(-?\d+),(-?\d+)\}, a_name="([^"]+)", a_size=\{\d+,\d+\}, f_quad=\{(\d+),(\d+),(\d+),(\d+)\}, alias=\{([^}]*)\}', t):
        g = m.groups()
        rec = (base, g[0], (int(g[1]), int(g[2])))
        sprites.setdefault(g[0], rec)
        for al in re.findall(r'"([^"]+)"', g[12]):
            sprites.setdefault(al, rec)
print('sprite trong atlas:', len(sprites))


def spr_file(name):
    r = sprites.get(name)
    if not r: return None
    p = os.path.join(SPR, r[0], r[1] + '.png')
    return p if os.path.exists(p) else None


def src_group(atlas):
    a = atlas or ''
    m = re.match(r'go_hero_(\w+)', a)
    if m: return 'hero:' + m.group(1)
    m = re.match(r'go_towers_(\w+)', a)
    if m: return 'tower:' + m.group(1)
    if a == 'go_towers': return 'tower:_chung'
    m = re.match(r'go_enemies_(\w+)', a)
    if m: return 'enemy:' + m.group(1)
    m = re.match(r'go_stage(\d+)', a)
    if m: return 'stage:' + m.group(1)
    if a.startswith('go_stages_'): return 'stage:' + a[len('go_stages_'):]
    m = re.match(r'go_items_(\w+)', a)
    if m: return 'item:' + m.group(1)
    if a.startswith('go_relics'): return 'item:relics'
    if a in ('go_commons', 'go_decals'): return 'common:' + a[3:]
    return 'other:' + a


# ------------------------------------------------------------ animation db
def load_anim_file(path, unwrap=True):
    it = Interp(); make_stdlib(it)
    v = it.run(open(path, encoding='utf-8').read(), path)
    if unwrap and isinstance(v, LTab) and isinstance(v.get('animations'), LTab) and v.get('fps') is None: v = v.get('animations')
    return to_py(v) if isinstance(v, LTab) else {}


anims = {}
for p in [os.path.join(LUA, 'kr5', 'data', 'game_animations.lua')] + sorted(glob.glob(os.path.join(LUA, 'kr5', 'data', 'animations', '*.lua'))):
    for k, a in load_anim_file(p).items():
        if not isinstance(a, dict): continue
        if a.get('layer_from') is not None and a.get('layer_prefix'):
            for i in range(int(a['layer_from']), int(a['layer_to']) + 1):
                nk = k.replace('layerX', 'layer%d' % i)
                b = dict(a); b['prefix'] = a['layer_prefix'] % i if '%' in a['layer_prefix'] else a['layer_prefix']
                anims.setdefault(nk, b)
            continue
        anims.setdefault(k, a)


def anim_frames(a):
    if isinstance(a.get('frames'), list): return [int(x) for x in a['frames']]
    fr = []
    if isinstance(a.get('ranges'), list):
        for r in a['ranges']:
            if isinstance(r, list) and len(r) == 2:
                s, e = int(r[0]), int(r[1]); fr += list(range(s, e + 1) if e >= s else range(s, e - 1, -1))
            elif isinstance(r, list): fr += [int(x) for x in r]
        return fr
    if isinstance(a.get('pre'), list): fr += [int(x) for x in a['pre']]
    if a.get('from') is not None and a.get('to') is not None:
        s, e = int(a['from']), int(a['to']); fr += list(range(s, e + 1) if e >= s else range(s, e - 1, -1))
    if isinstance(a.get('post'), list): fr += [int(x) for x in a['post']]
    return fr


print('hoạt ảnh trong animation db:', len(anims))

# ------------------------------------------------------------ exoskeleton
exo_names = {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(EXOD, '*.lua'))}
exo_anim = {}   # "<exo>_<anim>" -> (exo, anim)
_exo_cache = {}


def load_exo(name):
    if name in _exo_cache: return _exo_cache[name]
    p = os.path.join(EXOD, name + '.lua')
    try:
        d = load_anim_file(p, unwrap=False)
        if not isinstance(d, dict): d = None
    except Exception as ex:
        print('  ! exo', name, ex); d = None
    _exo_cache[name] = d
    return d


for en in exo_names:
    d = load_exo(en)
    if not d: continue
    for a in d.get('animations') or []:
        if isinstance(a, dict) and a.get('name'):
            exo_anim[en + '_' + a['name']] = (en, a['name'])
print('exoskeleton:', len(exo_names), ' hoạt ảnh exo:', len(exo_anim))

# ------------------------------------------------------------ template
ents, order, comps, G = load_templates(ROOT, verbose=True)
T = {n: to_py(ents[n]) for n in order if n in ents}
Z = {k: v for k, v in G.items() if k.startswith('Z_') and isinstance(v, (int, float))}

# kế thừa: tìm base gần nhất bằng cách so khớp tên template_name được copy -> ghi lại lúc chạy? dùng câu register_t trong mã
BASE = {}
for path in [os.path.join(LUA, 'all', 'templates.lua'), os.path.join(LUA, 'kr5', 'game_templates.lua')]:
    for m in re.finditer(r'(?:E:register_t|RT)\("([^"]+)"(?:,\s*"([^"]+)")?\)', open(path, encoding='utf-8').read()):
        BASE.setdefault(m.group(1), m.group(2))


def chain(n):
    out = []; seen = set()
    while n and n not in seen:
        seen.add(n); out.append(n); n = BASE.get(n)
    return out


def kind_of(n, t):
    ch = chain(n)
    if t.get('particle_system') and not t.get('render'): return 'ps'
    for c in ch:
        if c in ('fx', 'fx_fade') or c.startswith('fx_'): return 'fx'
        if c.startswith('decal'): return 'decal'
        if c in ('bullet', 'bomb', 'arrow', 'bolt', 'shotgun') : return 'bullet'
        if c.startswith('aura'): return 'aura'
        if c.startswith('mod_') or c == 'modifier': return 'mod'
    if 'bullet' in t: return 'bullet'
    if 'aura' in t: return 'aura'
    if 'modifier' in t: return 'mod'
    if 'particle_system' in t: return 'ps'
    if 'hero' in t: return 'hero'
    if 'tower' in t: return 'tower'
    if 'enemy' in t: return 'enemy'
    if 'soldier' in t: return 'soldier'
    return 'other'


used_assets = {}      # key -> dict(kind='a'|'s'|'x', ...)


def resolve_sprite(s):
    """sprite của render -> khoá tài sản ('a:tên anim' | 's:tên sprite' | 'x:exo|anim')"""
    if not isinstance(s, dict): return None
    nm = s.get('name'); pf = s.get('prefix')
    if s.get('exo'):
        full = (pf + '_' + nm) if pf else nm
        if full in exo_anim:
            en, an = exo_anim[full]; k = 'x:' + en + '|' + an
            used_assets[k] = ('x', en, an); return k
        return None
    if s.get('animation') and isinstance(s['animation'], str):
        nm = s['animation']; pf = None
    if s.get('animated', True) and nm is not None:
        full = (pf + '_' + nm) if pf else nm
        if full in anims:
            used_assets['a:' + full] = ('a', full); return 'a:' + full
        if full in exo_anim:
            en, an = exo_anim[full]; k = 'x:' + en + '|' + an
            used_assets[k] = ('x', en, an); return k
        return None
    if isinstance(nm, str) and nm in sprites:
        used_assets['s:' + nm] = ('s', nm); return 's:' + nm
    return None


def resolve_ps(ps):
    out = []
    names = ps.get('names') if isinstance(ps.get('names'), list) else [ps.get('name')]
    for nm in names:
        if not isinstance(nm, str): out.append(None); continue
        if ps.get('animated'):
            if nm in anims: used_assets['a:' + nm] = ('a', nm); out.append('a:' + nm); continue
            if nm in exo_anim:
                en, an = exo_anim[nm]; k = 'x:' + en + '|' + an; used_assets[k] = ('x', en, an); out.append(k); continue
        if nm in sprites: used_assets['s:' + nm] = ('s', nm); out.append('s:' + nm); continue
        if nm in anims: used_assets['a:' + nm] = ('a', nm); out.append('a:' + nm); continue
        out.append(None)
    return out


def r5(x):
    return round(x, 4) if isinstance(x, float) else x


def vec(v, d=(0, 0)):
    if isinstance(v, dict): return [r5(v.get('x', d[0]) or 0), r5(v.get('y', d[1]) or 0)]
    return list(d)


def strings_in(v, acc):
    if isinstance(v, str): acc.add(v)
    elif isinstance(v, dict):
        for x in v.values(): strings_in(x, acc)
    elif isinstance(v, list):
        for x in v: strings_in(x, acc)


PS_KEYS = ['alphas', 'anchor', 'animated', 'animation_fps', 'cycle_names', 'emission_rate', 'emit_area_spread', 'emit_direction',
           'emit_duration', 'emit_offset', 'emit_rotation', 'emit_rotation_spread', 'emit_speed', 'emit_spread', 'loop',
           'particle_lifetime', 'scale_same_aspect', 'scale_var', 'scales_x', 'scales_y', 'sort_y_offset', 'sort_y_offsets',
           'source_lifetime', 'spin', 'track_rotation', 'ts_offset', 'z', 'name', 'names', 'track_offset']
BUL_KEYS = ['flight_time', 'g', 'rotation_speed', 'align_with_trajectory', 'hit_fx', 'hit_fx_air', 'hit_decal', 'particles_name',
            'start_fx', 'miss_fx', 'miss_decal', 'hit_payload', 'damage_radius', 'acceleration_factor', 'min_speed', 'max_speed',
            'hit_blood_fx', 'arrive_fx', 'ignore_rotation', 'hide_radius', 'mod', 'mods', 'speed', 'fixed_height', 'hit_time', 'ray_duration']


def compact_template(n, t):
    o = {'k': kind_of(n, t), 'b': chain(n)[1:4]}
    rd = t.get('render') or {}
    sps = rd.get('sprites') if isinstance(rd.get('sprites'), list) else []
    sl = []
    for s in sps:
        if not isinstance(s, dict): continue
        key = resolve_sprite(s)
        e = {'a': key, 'loop': s.get('loop', True), 'an': vec(s.get('anchor'), (0.5, 0.5)), 'of': vec(s.get('offset'))}
        if s.get('scale') is not None: e['sc'] = vec(s.get('scale'), (1, 1))
        for k2, k3 in (('r', 'r'), ('alpha', 'al'), ('z', 'z'), ('sort_y_offset', 'sy'), ('fps', 'fps'), ('hidden', 'hid'),
                       ('draw_order', 'do'), ('flip_x', 'fx'), ('time_offset', 'to'), ('random_ts', 'rts'), ('hide_after_runs', 'har'),
                       ('ignore_start', 'ign')):
            v = s.get(k2)
            if v not in (None, False, 0) or (k2 == 'alpha' and v != 255 and v is not None): e[k3] = r5(v)
        if e.get('al') == 255: e.pop('al')
        if s.get('color'): e['col'] = s['color']
        if s.get('shader'): e['sh'] = s['shader']
        if not key: e['miss'] = ((s.get('prefix') or '') + '|' + str(s.get('name')))
        sl.append(e)
    if sl: o['sp'] = sl
    tw = t.get('tween')
    if isinstance(tw, dict) and isinstance(tw.get('props'), list):
        props = []
        for p in tw['props']:
            if not isinstance(p, dict) or not p.get('keys'): continue
            keys = []
            for kk in p['keys']:
                if not isinstance(kk, list) or len(kk) < 2: continue
                v = kk[1]
                v = vec(v) if isinstance(v, dict) else r5(v)
                keys.append([r5(kk[0]), v] + ([kk[2]] if len(kk) > 2 else []))
            if keys:
                props.append({k: v for k, v in dict(n=p.get('name', 'alpha'), k=keys, l=p.get('loop') or None, s=p.get('sprite_id', 1),
                                                    m=p.get('multiply') or None, i=p.get('interp'), to=r5(p.get('time_offset'))).items() if v is not None})
        if props:
            o['tw'] = {k: v for k, v in dict(p=props, rm=tw.get('remove'), rev=tw.get('reverse') or None, dis=tw.get('disabled') or None,
                                             rts=tw.get('random_ts')).items() if v is not None}
    ps = t.get('particle_system')
    if isinstance(ps, dict):
        pe = {k: ps[k] for k in PS_KEYS if ps.get(k) is not None}
        pe['assets'] = resolve_ps(ps)
        o['ps'] = pe
    bl = t.get('bullet')
    if isinstance(bl, dict):
        o['bl'] = {k: (vec(bl[k]) if isinstance(bl[k], dict) and k == 'speed' else bl[k]) for k in BUL_KEYS if bl.get(k) is not None}
    for comp in ('aura', 'modifier', 'timed'):
        c = t.get(comp)
        if isinstance(c, dict):
            o[comp[:3]] = {k: v for k, v in c.items() if isinstance(v, (int, float, str, bool)) and k in
                           ('duration', 'cycle_time', 'radius', 'runs', 'sprite_id', 'duration_var', 'damage_radius', 'track_source', 'use_mod_offset')}
    ray = {k: t.get(k) for k in ('image_width', 'ray_duration', 'track_target', 'dist_offset') if isinstance(t.get(k), (int, float, bool))}
    if 'image_width' in ray or 'ray_duration' in ray: o['ray'] = ray
    acc = set(); strings_in(t, acc)
    refs = sorted(x for x in acc if x != n and x in T)
    if refs: o['ref'] = refs
    return o


# chọn template hiệu ứng
FX_KINDS = {'fx', 'decal', 'bullet', 'aura', 'mod', 'ps'}
TPL = {}
for n in order:
    t = T.get(n)
    if not isinstance(t, dict): continue
    k = kind_of(n, t)
    if k in FX_KINDS or re.search(r'^(fx|decal|ps|aura|mod|bullet|bolt|bomb|arrow|ray|controller)_', n):
        TPL[n] = compact_template(n, t)
print('template hiệu ứng:', len(TPL))

# ------------------------------------------------------------ chiêu của tướng / tháp / quái
ATK_KEYS = ['animation', 'animations', 'bullet', 'bullets', 'shoot_time', 'shoot_times', 'hit_time', 'hit_times', 'spawn_time', 'hit_fx',
            'hit_decal', 'start_fx', 'mod', 'mods', 'entity', 'aura', 'bullet_start_offset', 'spawn_offset', 'spawn_pos_offset',
            'bullet_count', 'count', 'type', 'cooldown', 'range', 'max_range', 'damage_radius', 'xp_from_skill', 'fx', 'hit_offset',
            'payload', 'decal', 'cast_time', 'sound', 'loops', 'duration', 'hit_fx_offset']


def unit_attacks(n, t):
    out = []
    groups = []
    for g in ('melee', 'ranged'):
        if isinstance(t.get(g), dict) and isinstance(t[g].get('attacks'), list): groups.append((g, t[g]['attacks']))
    for g in ('timed_attacks', 'area_attacks', 'custom_attack'):
        v = t.get(g)
        if isinstance(v, dict) and isinstance(v.get('list'), list): groups.append((g, v['list']))
        elif isinstance(v, dict) and g == 'custom_attack': groups.append((g, [v]))
    if isinstance(t.get('attacks'), dict) and isinstance(t['attacks'].get('list'), list):
        groups.append(('attacks', t['attacks']['list']))
    for g, lst in groups:
        for i, a in enumerate(lst):
            if not isinstance(a, dict): continue
            e = {k: a[k] for k in ATK_KEYS if a.get(k) is not None}
            if not any(k in e for k in ('animation', 'bullet', 'mod', 'entity', 'aura', 'hit_fx', 'start_fx', 'bullets')): continue
            e['g'] = g; e['i'] = i + 1
            for k in ('bullet_start_offset', 'spawn_offset', 'spawn_pos_offset', 'hit_offset', 'hit_fx_offset'):
                if isinstance(e.get(k), dict): e[k] = vec(e[k])
                elif isinstance(e.get(k), list) and e[k] and isinstance(e[k][0], dict): e[k] = [vec(x) for x in e[k]]
            out.append(e)
    return out


UNITS = {}
for n in order:
    t = T.get(n)
    if not isinstance(t, dict): continue
    k = kind_of(n, t)
    if k not in ('hero', 'tower', 'enemy', 'soldier', 'other'): continue
    atks = unit_attacks(n, t)
    if not atks: continue
    rd = t.get('render') or {}
    sps = rd.get('sprites') if isinstance(rd.get('sprites'), list) else []
    body = []
    for s in sps:
        if isinstance(s, dict):
            body.append({'pf': s.get('prefix'), 'nm': s.get('name'), 'an': vec(s.get('anchor'), (0.5, 0.5)), 'of': vec(s.get('offset')),
                         'z': s.get('z'), 'anim': bool(s.get('animated', True)), 'exo': bool(s.get('exo')),
                         'sc': vec(s.get('scale'), (1, 1)) if s.get('scale') else None, 'do': s.get('draw_order'),
                         'ang': s.get('angles')})
    # nạp sẵn hoạt ảnh thân cho từng đòn
    for a in atks:
        al = a.get('animations') if isinstance(a.get('animations'), list) else [a.get('animation')]
        keys = []
        for an in al:
            ks = []
            for b in body:
                if not isinstance(an, str): ks.append(None); continue
                nm = an
                if b['ang'] and isinstance(b['ang'], dict) and isinstance(b['ang'].get(an), list) and b['ang'][an]:
                    nm = b['ang'][an][0]
                if b['exo']:
                    ks.append(resolve_sprite({'exo': True, 'prefix': b['pf'], 'name': nm}))
                elif b['anim']:
                    ks.append(resolve_sprite({'animated': True, 'prefix': b['pf'], 'name': nm}))
                else:
                    ks.append(None)
            keys.append(ks)
        a['body'] = keys
    idle = []
    for b in body:
        if b['exo']: idle.append(resolve_sprite({'exo': True, 'prefix': b['pf'], 'name': b['nm'] or 'idle'}))
        elif b['anim']:
            nm = b['nm']
            if b['ang'] and isinstance(b['ang'], dict) and isinstance(b['ang'].get('idle'), list): nm = b['ang']['idle'][0]
            idle.append(resolve_sprite({'animated': True, 'prefix': b['pf'], 'name': nm}) or resolve_sprite({'animated': True, 'prefix': b['pf'], 'name': 'idle'}))
        else: idle.append(resolve_sprite({'animated': False, 'name': b['nm']}))
    UNITS[n] = {'k': k, 'body': [{kk: vv for kk, vv in b.items() if kk in ('an', 'of', 'z', 'sc', 'do') and vv is not None} for b in body],
                'idle': idle, 'atk': atks}
    # các template được nhắc tới trong đòn cũng phải có mặt
    acc = set(); strings_in(atks, acc)
    for x in acc:
        if x in T and x not in TPL: TPL[x] = compact_template(x, T[x])
print('đơn vị có đòn:', len(UNITS))

# kéo theo template được tham chiếu (hit_fx, particles_name ...) cho đủ
changed = True
while changed:
    changed = False
    for n in list(TPL):
        for r in TPL[n].get('ref', []):
            if r not in TPL and kind_of(r, T[r]) in FX_KINDS:
                TPL[r] = compact_template(r, T[r]); changed = True

# ------------------------------------------------------------ hoạt ảnh hiệu ứng không gắn template (vẫn cho vào thư viện)
lib_extra = 0
for k, a in anims.items():
    if 'a:' + k in used_assets: continue
    if FXWORD.search(k.lower()) or tags_of(k, a.get('prefix')):
        fr = anim_frames(a)
        if fr and spr_file('%s_%04d' % (a.get('prefix'), fr[0])):
            used_assets['a:' + k] = ('a', k); lib_extra += 1
for k, (en, an) in exo_anim.items():
    kk = 'x:' + en + '|' + an
    if kk in used_assets: continue
    if not en.startswith('Card') and (FXWORD.search(k.lower()) or tags_of(k)):
        used_assets[kk] = ('x', en, an); lib_extra += 1
print('thêm hoạt ảnh hiệu ứng lẻ:', lib_extra, ' tổng tài sản:', len(used_assets))


# ------------------------------------------------------------ gói tấm khung (mỗi tài sản một png)
def safe(k):
    return re.sub(r'[^A-Za-z0-9_.-]', '_', k)[:150]


from sheet_worker import job_sheet


def main():
    os.makedirs(SHEETS, exist_ok=True)
    for x in os.listdir(SHEETS): os.remove(os.path.join(SHEETS, x))
    jobs = []
    ASSETS = {}
    exo_pack = {}   # exo -> set(sprite)
    for key, rec in used_assets.items():
        if key.endswith('_shadow') or '_shadow_' in key: continue
        if rec[0] == 'a':
            a = anims[rec[1]]; fr = anim_frames(a)
            names = ['%s_%04d' % (a.get('prefix'), i) for i in fr]
            files = [spr_file(nm) for nm in names]
            if not files or any(f is None for f in files):
                files = [f for f in files if f]
                if not files: continue
            first = sprites.get(names[0])
            ASSETS[key] = {'t': 'a', 'n': len(names), 'src': src_group(first[0] if first else ''),
                           'tags': tags_of(rec[1], a.get('prefix')), 'sz': list(first[2]) if first else None}
            jobs.append((key, 'a', {'files': files}, SHEETS, MAXW))
        elif rec[0] == 's':
            f = spr_file(rec[1])
            if not f: continue
            first = sprites.get(rec[1])
            ASSETS[key] = {'t': 's', 'n': 1, 'src': src_group(first[0]), 'tags': tags_of(rec[1]), 'sz': list(first[2])}
            jobs.append((key, 's', {'files': [f]}, SHEETS, MAXW))
        else:
            exo_pack.setdefault(rec[1], set()).add(rec[2])
    # exo: mỗi exo một tấm, các anim dùng chung
    EXOS = {}
    for en, an_set in exo_pack.items():
        d = load_exo(en)
        if not d: continue
        offs = {}
        for pk, pv in (d.get('parts') or {}).items():
            if isinstance(pv, dict): offs[pk] = [pv.get('offsetX') or 0, pv.get('offsetY') or 0]
        anims_out = {}; partnames = {}
        for a in d.get('animations') or []:
            if not isinstance(a, dict): continue
            frames = []
            for fr in a.get('frames') or []:
                pl = []
                for p in (fr.get('parts') if isinstance(fr, dict) else None) or []:
                    nm = p.get('name'); xf = p.get('xform') or {}
                    fp = spr_file(nm)
                    if not fp: continue
                    if nm not in partnames: partnames[nm] = (len(partnames), fp)
                    pl.append([partnames[nm][0], r5(xf.get('x', 0)), r5(xf.get('y', 0)), r5(xf.get('r', 0)), r5(xf.get('sx', 1)),
                               r5(xf.get('sy', 1)), r5(xf.get('kx', 0)), r5(xf.get('ky', 0)),
                               r5(p.get('alpha') if p.get('alpha') is not None else 1)])
                frames.append(pl)
            anims_out[a.get('name')] = frames
        plist = sorted(partnames.items(), key=lambda kv: kv[1][0])
        EXOS[en] = {'fps': d.get('fps') or 30, 'anims': anims_out, 'pn': [nm for nm, _ in plist],
                    'po': [offs.get(nm, [0, 0]) for nm, _ in plist]}
        jobs.append(('exo:' + en, 'x', {'names': [(nm, fp) for nm, (i, fp) in plist]}, SHEETS, MAXW))
        for an in an_set:
            key = 'x:' + en + '|' + an
            fr0 = anims_out.get(an) or []
            first_part = None
            for f in fr0:
                if f: first_part = plist[f[0][0]][0]; break
            atlas = sprites.get(first_part, ('',))[0] if first_part else ''
            ASSETS[key] = {'t': 'x', 'exo': en, 'anim': an, 'n': len(fr0), 'src': src_group(atlas), 'tags': tags_of(en, an)}
    body_keys = set()
    for u in UNITS.values():
        for a in u['atk']:
            for ks in a.get('body') or []:
                for k in ks:
                    if k: body_keys.add(k)
        for k in u['idle']:
            if k: body_keys.add(k)
    for k in body_keys:
        if k in ASSETS: ASSETS[k]['body'] = 1
    # gán thẻ hệ theo template dùng tài sản (vd. fx_fire_x dùng anim tên trung tính)
    users = {}
    for n, o in TPL.items():
        ks = [s.get('a') for s in o.get('sp', [])] + (o.get('ps', {}).get('assets') or [])
        for k in ks:
            if k: users.setdefault(k, set()).add(n)
    for k, us in users.items():
        if k in ASSETS:
            extra = tags_of(*us)
            ASSETS[k]['tags'] = sorted(set(ASSETS[k]['tags']) | set(extra))
            ASSETS[k]['used'] = sorted(us)[:40]
    print('gói tấm khung:', len(jobs))
    sheets = {}
    with Pool(max(2, os.cpu_count() - 1)) as pool:
        for i, (key, res) in enumerate(pool.imap_unordered(job_sheet, jobs, chunksize=8)):
            sheets[key] = res
            if (i + 1) % 500 == 0: print('  ', i + 1)
    bad = 0
    for key, a in list(ASSETS.items()):
        if a['t'] in ('a', 's'):
            r = sheets.get(key)
            if not r or 'err' in r: bad += 1; ASSETS.pop(key); continue
            a.update(r)
    for en, e in EXOS.items():
        r = sheets.get('exo:' + en)
        if not r or 'err' in r: continue
        e['img'] = r['img']; e['parts'] = [r['parts'].get(nm) for nm in e['pn']]
    print('lỗi gói:', bad)
    # gỡ template trỏ tài sản không gói được
    for o in TPL.values():
        for s in o.get('sp', []):
            if s.get('a') and s['a'] not in ASSETS: s['miss'] = s['a']; s['a'] = None
        if o.get('ps'):
            o['ps']['assets'] = [k if k in ASSETS else None for k in o['ps']['assets']]
    for k, o in TPL.items():
        names = [k] + [s.get('a') or '' for s in o.get('sp', [])] + [x or '' for x in (o.get('ps', {}).get('assets') or [])]
        o['tags'] = tags_of(*names)
    os.makedirs(os.path.join(OUT, 'exo'), exist_ok=True)
    EXMETA = {}
    for en, e in EXOS.items():
        if 'img' not in e: continue
        with open(os.path.join(OUT, 'exo', safe(en) + '.json'), 'w', encoding='utf-8') as f:
            json.dump(e, f, ensure_ascii=False, separators=(',', ':'))
        EXMETA[en] = {'f': 'exo/' + safe(en) + '.json', 'fps': e['fps'], 'anims': {k: len(v) for k, v in e['anims'].items()}}
    data = {'rs': RS, 'fps': 30, 'z': Z, 'tags': [[k, v] for k, v, _ in TAGS], 'assets': ASSETS, 'exos': EXMETA, 'tpl': TPL, 'units': UNITS}
    with open(os.path.join(OUT, 'data.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print('ghi data.json: %.1f MB' % (os.path.getsize(os.path.join(OUT, 'data.json')) / 1e6))
    tot = sum(os.path.getsize(os.path.join(SHEETS, x)) for x in os.listdir(SHEETS))
    print('tấm khung: %d file, %.0f MB' % (len(os.listdir(SHEETS)), tot / 1e6))

