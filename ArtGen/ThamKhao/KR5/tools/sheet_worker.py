# Tiến trình con: gói khung của một hoạt ảnh thành một tấm png (cắt sát theo hộp chung).
import os, re


def safe(k):
    return re.sub(r'[^A-Za-z0-9_.-]', '_', k)[:150]


def job_sheet(args):
    key, kind, info, SHEETS, MAXW = args
    from PIL import Image
    try:
        out_png = os.path.join(SHEETS, safe(key) + '.png')
        if kind in ('a', 's'):
            files = info['files']
            ims = []
            for fp in files:
                im = Image.open(fp).convert('RGBA')
                bb = im.getbbox()
                ims.append((im, bb))
            # ô cắt sát: lấy hộp chung lớn nhất cho mọi khung
            cw = max(((bb[2] - bb[0]) if bb else 1) for _, bb in ims)
            ch = max(((bb[3] - bb[1]) if bb else 1) for _, bb in ims)
            # chỉ gói khung khác nhau
            uniq = {}; fidx = []
            for fp, (im, bb) in zip(files, ims):
                if fp not in uniq: uniq[fp] = len(uniq)
                fidx.append(uniq[fp])
            n = len(uniq)
            cols = max(1, min(n, MAXW // max(cw, 1)))
            rows = (n + cols - 1) // cols
            sheet = Image.new('RGBA', (cols * cw, rows * ch), (0, 0, 0, 0))
            meta = [None] * n
            for fp, i in uniq.items():
                im, bb = ims[files.index(fp)]
                x, y = (i % cols) * cw, (i // cols) * ch
                if bb:
                    sheet.paste(im.crop(bb), (x, y))
                    meta[i] = [x, y, bb[2] - bb[0], bb[3] - bb[1], bb[0], bb[1], im.width, im.height]
                else:
                    meta[i] = [x, y, 0, 0, 0, 0, im.width, im.height]
            if sheet.width * sheet.height > 0:
                sheet.save(out_png, optimize=False, compress_level=6)
            return key, {'img': safe(key) + '.png', 'cells': meta, 'seq': fidx}
        else:   # exo: gói các sprite mảnh
            names = info['names']
            ims = []
            for nm, fp in names:
                im = Image.open(fp).convert('RGBA'); ims.append((nm, im, im.getbbox()))
            # xếp theo hàng đơn giản
            x = y = rowh = 0; places = []
            W = 0
            for nm, im, bb in ims:
                w = (bb[2] - bb[0]) if bb else 1; h = (bb[3] - bb[1]) if bb else 1
                if x + w > MAXW: x = 0; y += rowh; rowh = 0
                places.append((x, y)); x += w; rowh = max(rowh, h); W = max(W, x)
            Hh = y + rowh
            sheet = Image.new('RGBA', (max(W, 1), max(Hh, 1)), (0, 0, 0, 0))
            meta = {}
            for (nm, im, bb), (px, py) in zip(ims, places):
                if bb:
                    sheet.paste(im.crop(bb), (px, py))
                    meta[nm] = [px, py, bb[2] - bb[0], bb[3] - bb[1], bb[0], bb[1], im.width, im.height]
                else:
                    meta[nm] = [px, py, 0, 0, 0, 0, im.width, im.height]
            sheet.save(out_png, optimize=False, compress_level=6)
            return key, {'img': safe(key) + '.png', 'parts': meta}
    except Exception as ex:
        return key, {'err': str(ex)}


