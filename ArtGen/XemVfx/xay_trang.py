# Dựng trang so sánh hiệu ứng từng tướng (bản TRƯỚC / SAU một đợt sửa VFX).
#   py -3 -I ArtGen/XemVfx/xay_trang.py
# Đọc ảnh tour ArtGen/XemVfx/chup/<đợt>/<tướng>/<danh|mana|ult>_NN.jpg (menu "PokiClash/Thử/Hiệu ứng mọi tướng: chụp bản
# TRƯỚC / SAU"; trước 2026-11-19 tour ghi vào Temp/PokiShots/vfx_all, Unity xoá Temp khi tắt), cắt vùng sân, gói mỗi đòn thành một
# tấm lưới vào anh/<đợt>/<tướng>_<đòn>.jpg, ghi data.json. Tướng nào không còn ảnh gốc mà đã có tấm từ lần dựng trước thì giữ tấm cũ
# (số khung lấy ở data.json cũ). Kèm báo cáo agent từng hệ (bao_cao/<hệ>.md). Chỉ lấy tướng có rig .atomik / Spine.
# Ảnh là hình trong game (rig gốc của game khác, aola): chỉ xem trên máy, anh/ và data.json đã .gitignore.
import os, sys, json, glob, re
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
SHOTS = os.path.join(HERE, 'chup')
HEROES = os.path.join(ROOT, 'Assets', '02 Data', 'Json', 'heroes.json')
RES = os.path.join(ROOT, 'Assets', '03 Art', 'Heroes', 'Resources')
OUT = os.path.join(HERE, 'anh')
CROP = (0, 75, 720, 865)      # vùng sân trong ảnh dọc 720 x 1441
W, H = 360, 395               # cỡ mỗi khung trên trang
COLS = 10
MOVES = [('danh', 'Đòn thường'), ('mana', 'Chiêu mana'), ('ult', 'Chiêu cuối')]
DOTS = ['truoc', 'sau']
ELEMS = [('hoa', 'Hỏa'), ('thuy', 'Thủy'), ('moc', 'Mộc'), ('kim', 'Kim'), ('tho', 'Thổ')]


def heroes():
    H_ = json.load(open(HEROES, encoding='utf-8'))
    H_ = [h for h in (H_ if isinstance(H_, list) else H_.get('heroes', [])) if isinstance(h, dict)]
    out = []
    for h in H_:
        forms = h.get('forms') or []
        ok = bool(forms) and all(any(glob.glob(os.path.join(RES, f.get('aola') or '_', p)) for p in ('*.atomik', '*.skel', '*.json'))
                                 for f in forms)
        if not ok: continue
        out.append({'id': h['id'], 'name': h['name'], 'elem': h['elem'], 'forms': [f.get('name') for f in forms],
                    'skill': h.get('skill'), 'ult': h.get('ult')})
    return out


def strip(src_dir, move, dst):
    files = sorted(glob.glob(os.path.join(src_dir, move + '_*.jpg')))
    if not files: return 0
    n = len(files); rows = (n + COLS - 1) // COLS
    sheet = Image.new('RGB', (COLS * W, rows * H), (20, 20, 20))
    for i, f in enumerate(files):
        im = Image.open(f).convert('RGB').crop(CROP).resize((W, H), Image.LANCZOS)
        sheet.paste(im, ((i % COLS) * W, (i // COLS) * H))
    sheet.save(dst, quality=84)
    return n


def notes():
    """báo cáo agent: tách theo tiêu đề có id tướng"""
    res = {}
    for f in glob.glob(os.path.join(HERE, 'bao_cao', '*.md')):
        t = open(f, encoding='utf-8').read()
        parts = re.split(r'^(#{2,3} .*)$', t, flags=re.M)
        for i in range(1, len(parts), 2):
            head, body = parts[i], parts[i + 1]
            for hid in re.findall(r'\b([a-z]+_[a-z_]+)\b', head):
                res.setdefault(hid, []).append((head.strip('# ').strip() + '\n' + body.strip())[:6000])
    return res


def main():
    hs = heroes()
    nt = notes()
    # số khung từ lần dựng trước: tướng không còn ảnh gốc thì giữ tấm cũ trong anh/<đợt>/
    old = {}
    try:
        for e in json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8')).get('heroes', []):
            old[e['id']] = e.get('n', {})
    except Exception:
        pass
    data = {'cols': COLS, 'w': W, 'h': H, 'moves': MOVES, 'elems': ELEMS, 'dots': [], 'heroes': []}
    for d in DOTS:
        if os.path.exists(os.path.join(SHOTS, d, 'ds.json')) or glob.glob(os.path.join(OUT, d, '*.jpg')): data['dots'].append(d)
    for h in hs:
        e = dict(h); e['n'] = {}
        for d in data['dots']:
            src = os.path.join(SHOTS, d, h['id'])
            os.makedirs(os.path.join(OUT, d), exist_ok=True)
            for m, _ in MOVES:
                dst = os.path.join(OUT, d, '%s_%s.jpg' % (h['id'], m))
                n = strip(src, m, dst) if os.path.isdir(src) else 0
                if not n and os.path.exists(dst): n = (old.get(h['id'], {}).get(m) or {}).get(d, 0)
                if n: e['n'].setdefault(m, {})[d] = n
        if h['id'] in nt: e['note'] = '\n\n'.join(nt[h['id']])
        data['heroes'].append(e)
        print(h['id'], e['n'])
    json.dump(data, open(os.path.join(HERE, 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print('xong:', len(data['heroes']), 'tướng, đợt', data['dots'])


if __name__ == '__main__':
    main()
