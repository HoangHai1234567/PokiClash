# Tính chính xác hoàn trả máy quả (3 cuộn x 3 hàng, 5 đường) trên mọi tổ hợp dừng, để chọn dải cuộn / bảng trả.
import itertools, json, sys

W, CH = 7, 8  # Sao (thay mọi biểu tượng trừ Rương), Rương
LINES = [(1, 1, 1), (0, 0, 0), (2, 2, 2), (0, 1, 2), (2, 1, 0)]


def line_win(a, b, c, pays, wild_pays):
    s = (a, b, c)
    if CH in s:
        return 0, None
    if all(x == W for x in s):
        return wild_pays, W
    base = next(x for x in s if x != W)
    if all(x == base or x == W for x in s):
        return pays.get(base, 0), base
    return 0, None


def rtp(reels, pays, wild_pays, scatter2, free):
    L = [len(r) for r in reels]
    tot_line = tot_scat = 0.0
    p3 = 0.0
    hit = 0
    badge = 0.0
    n = 0
    for i in range(L[0]):
        for j in range(L[1]):
            for k in range(L[2]):
                cols = []
                for r, st in zip(reels, (i, j, k)):
                    ln = len(r)
                    cols.append((r[(st - 1) % ln], r[st], r[(st + 1) % ln]))
                lw = 0
                for ln_ in LINES:
                    w, sym = line_win(cols[0][ln_[0]], cols[1][ln_[1]], cols[2][ln_[2]], pays, wild_pays)
                    lw += w
                    if sym == 6:
                        badge += 1
                nch = sum(1 for col in cols for x in col if x == CH)
                sc = scatter2 * 5 if nch == 2 else 0  # x tổng cược = 5 cược đường
                if nch >= 3:
                    p3 += 1
                if lw + sc > 0 or nch >= 3:
                    hit += 1
                tot_line += lw
                tot_scat += sc
                n += 1
    B = (tot_line + tot_scat) / n / 5.0
    p3 /= n
    V = B / (1 - free * p3)
    return V, B, p3, hit / n, badge / n


if __name__ == "__main__":
    # dải cuộn: mỗi ngọc 3, bi 2, huy hiệu 1, Sao 1, Rương 1 = 20 ô; xếp xen để không dồn cụm
    def strip(seed):
        import random
        rnd = random.Random(seed)
        base = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6, 7, 8]
        for _ in range(2000):
            rnd.shuffle(base)
            ok = all(base[x] != base[(x + 1) % len(base)] for x in range(len(base)))
            if ok:
                return list(base)
        return base

    reels = [strip(11), strip(23), strip(37)]
    pays = {0: 8, 1: 8, 2: 8, 3: 8, 4: 8, 5: 15, 6: 60}
    for gem in [6, 7, 8, 9, 10, 12]:
        for bi in [12, 15, 20]:
            pays2 = dict(pays)
            for g in range(5):
                pays2[g] = gem
            pays2[5] = bi
            V, B, p3, hitr, badge = rtp(reels, pays2, 100, 1, 5)
            print("gem", gem, "bi", bi, "RTP %.4f base %.4f p3 %.5f hit %.3f badge/spin %.5f" % (V, B, p3, hitr, badge))
    print(json.dumps(reels))
