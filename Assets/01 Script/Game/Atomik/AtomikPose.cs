// Tư thế của một rig .atomik ở một thời điểm và lưới dựng từ tư thế đó (CPU), dùng chung cho AtomikPlayer (scene thử) và
// AolaActor (dạng tướng là .atomik). Khoá theo cách Spine 4.2: xoay cộng vào góc gốc, dời cộng vào vị trí gốc, tỉ lệ nhân;
// đường cong bezier điểm điều khiển tuyệt đối. Bản 2 thêm độ đậm slot (hiệu ứng hiện, tan). Không sinh đối tượng Unity nào.
using System;
using UnityEngine;

namespace PokiClash.Game
{
    public sealed class AtomikPose
    {
        public readonly AtomikAsset asset;
        public readonly int maxVerts;
        readonly float[] lx, ly, lr, lsx, lsy;     // tư thế cục bộ
        readonly float[] px, py, pr, psx, psy;     // tư thế giữ lại để trộn (Snapshot)
        readonly float[] wa, wb, wc, wd, wx, wy;   // ma trận thế giới 2x3
        readonly int[] slotAtt;
        readonly float[] slotAlpha;

        // một lần dựng lưới (một Mesh): nhớ hình từng slot lần trước để biết có phải dựng lại tam giác không. Dựng nhiều Mesh từ cùng
        // tư thế (AolaActor: thân có viền sticker, hạt lá không viền) thì mỗi Mesh một pass riêng.
        public sealed class SkinPass
        {
            internal int[] lastAtt;
            internal int used;       // rig có mặt nạ cắt: số chỉ số tam giác đang dùng (phần sau là tam giác rỗng 0, 0, 0)
            public int[] Tris = new int[0];
        }

        // mặt nạ cắt (bản 3): slot nào thuộc mặt nạ nào, chỗ dư cho đỉnh sinh ra khi cắt, bộ đệm cắt một tam giác
        readonly AtomikMask[] masks;
        readonly int[] slotMask, slotStart;
        readonly int extraVerts;
        readonly float[] mpx, mpy;
        float[] clipA = new float[4 * 40], clipB = new float[4 * 40];

        readonly SkinPass main;

        public int[] Tris => main.Tris;

        public AtomikPose(AtomikAsset a)
        {
            asset = a;
            int nb = a.bones.Length, ns = a.slots.Length;
            lx = new float[nb]; ly = new float[nb]; lr = new float[nb]; lsx = new float[nb]; lsy = new float[nb];
            px = new float[nb]; py = new float[nb]; pr = new float[nb]; psx = new float[nb]; psy = new float[nb];
            wa = new float[nb]; wb = new float[nb]; wc = new float[nb]; wd = new float[nb]; wx = new float[nb]; wy = new float[nb];
            slotAtt = new int[ns];
            slotAlpha = new float[ns];
            main = NewPass();
            foreach (var att in a.atts) maxVerts += att.uvs.Length / 2;
            attsRef = a.atts;
            masks = a.masks;
            if (masks != null && masks.Length > 0)
            {
                slotMask = new int[ns];
                slotStart = new int[ns];
                for (int s = 0; s < ns; s++) slotMask[s] = -1;
                int mv = 3;
                for (int m = 0; m < masks.Length; m++)
                {
                    if (masks[m].verts == null || masks[m].verts.Length < 6) continue;
                    mv = Mathf.Max(mv, masks[m].verts.Length / 2);
                    for (int s = Mathf.Max(0, masks[m].slot); s <= masks[m].end && s < ns; s++) slotMask[s] = m;
                }
                mpx = new float[mv]; mpy = new float[mv];
                if (4 * (mv + 8) > clipA.Length) { clipA = new float[4 * (mv + 8)]; clipB = new float[4 * (mv + 8)]; }
                // tam giác bị mép cắt xén sinh thêm đỉnh: chừa chỗ theo số tam giác nằm trong vùng cắt (thường chỉ vài chục cái bị xén)
                int clipTris = 0;
                foreach (var att in a.atts)
                    if (att.slot >= 0 && att.slot < ns && slotMask[att.slot] >= 0) clipTris += att.tris.Length / 3;
                extraVerts = Mathf.Min(clipTris * 3, 12000);
                maxVerts += extraVerts;
            }
        }

        readonly AtomikAtt[] attsRef;

        // rig vừa được nhập lại (sửa file .atomik lúc Editor đang Play): mảng xương, slot, đỉnh đã đổi, nơi dùng phải dựng lại
        public bool Stale => !asset || !ReferenceEquals(asset.atts, attsRef) || asset.bones.Length != lx.Length ||
                             asset.slots.Length != slotAtt.Length;

        // Tư thế cục bộ ở clip ci, giây t (nơi gọi tự lặp hay kẹp t). ci < 0: dáng gốc.
        public void Sample(int ci, float t)
        {
            var bones = asset.bones;
            for (int i = 0; i < bones.Length; i++)
            {
                var b = bones[i];
                lx[i] = b.x; ly[i] = b.y; lr[i] = b.rot; lsx[i] = b.sx; lsy[i] = b.sy;
            }
            for (int s = 0; s < asset.slots.Length; s++)
            {
                slotAtt[s] = asset.slots[s].att;
                slotAlpha[s] = 1 - Mathf.Clamp01(asset.slots[s].fade);
            }
            if (ci < 0 || ci >= asset.anims.Length) return;
            var c = asset.anims[ci];
            if (c.tls != null)
                foreach (var tl in c.tls)
                {
                    int i = tl.bone;
                    if (tl.type == 0) lr[i] += Sample1(tl.keys, t);
                    else
                    {
                        Sample2(tl.keys, t, out float vx, out float vy);
                        if (tl.type == 1) { lx[i] += vx; ly[i] += vy; }
                        else { lsx[i] *= vx; lsy[i] *= vy; }
                    }
                }
            if (c.sk != null)
                foreach (var k in c.sk)
                    for (int j = 0; j < k.times.Length; j++)
                        if (k.times[j] <= t + 1e-5f) slotAtt[k.slot] = k.atts[j];
            if (c.sa != null)
                foreach (var k in c.sa)
                    slotAlpha[k.slot] = Mathf.Clamp01(Sample1(k.keys, t));
        }

        // Phủ thêm clip lặp ci ở giây t lên tư thế vừa Sample (clip "aura": mây bay vòng quanh Thanh Long...). Clip này chạy theo
        // đồng hồ riêng của nơi gọi, liền qua mọi lần đổi clip chính, nên các clip chính không khoá xương, slot của nó. Xương: xoay,
        // dời cộng thêm, tỉ lệ nhân (như Sample); hình trong slot: đặt theo khoá; độ đậm slot: nhân vào (clip chính vẫn làm mờ được,
        // vd. dạng cũ tan khi tiến hóa).
        public void Overlay(int ci, float t)
        {
            if (ci < 0 || ci >= asset.anims.Length) return;
            var c = asset.anims[ci];
            if (c.tls != null)
                foreach (var tl in c.tls)
                {
                    int i = tl.bone;
                    if (tl.type == 0) lr[i] += Sample1(tl.keys, t);
                    else
                    {
                        Sample2(tl.keys, t, out float vx, out float vy);
                        if (tl.type == 1) { lx[i] += vx; ly[i] += vy; }
                        else { lsx[i] *= vx; lsy[i] *= vy; }
                    }
                }
            if (c.sk != null)
                foreach (var k in c.sk)
                    for (int j = 0; j < k.times.Length; j++)
                        if (k.times[j] <= t + 1e-5f) slotAtt[k.slot] = k.atts[j];
            if (c.sa != null)
                foreach (var k in c.sa)
                    slotAlpha[k.slot] *= Mathf.Clamp01(Sample1(k.keys, t));
        }

        // giữ tư thế cục bộ hiện tại làm điểm đầu trộn (đổi clip)
        public void Snapshot()
        {
            Array.Copy(lx, px, lx.Length); Array.Copy(ly, py, ly.Length); Array.Copy(lr, pr, lr.Length);
            Array.Copy(lsx, psx, lsx.Length); Array.Copy(lsy, psy, lsy.Length);
        }

        // trộn từ tư thế đã giữ (w = 0) tới tư thế vừa Sample (w = 1)
        public void Mix(float w)
        {
            for (int i = 0; i < lx.Length; i++)
            {
                lx[i] = Mathf.Lerp(px[i], lx[i], w); ly[i] = Mathf.Lerp(py[i], ly[i], w);
                lr[i] = Mathf.LerpAngle(pr[i], lr[i], w);
                lsx[i] = Mathf.Lerp(psx[i], lsx[i], w); lsy[i] = Mathf.Lerp(psy[i], lsy[i], w);
            }
        }

        // dời thêm xương b (cục bộ, sau Sample, trước World): hiệu ứng ở xa kéo tới chỗ đối thủ (AolaActor)
        public void Nudge(int b, float x, float y)
        {
            if (b < 0 || b >= lx.Length) return;
            lx[b] += x;
            ly[b] += y;
        }

        public float LocalX(int b) => b >= 0 && b < lx.Length ? lx[b] : 0;

        // ma trận thế giới (cha luôn đứng trước con)
        public void World()
        {
            var bones = asset.bones;
            for (int i = 0; i < bones.Length; i++)
            {
                float rad = lr[i] * Mathf.Deg2Rad, cs = Mathf.Cos(rad), sn = Mathf.Sin(rad);
                float a = cs * lsx[i], b = -sn * lsy[i], c = sn * lsx[i], d = cs * lsy[i];
                int p = bones[i].parent;
                if (p < 0) { wa[i] = a; wb[i] = b; wc[i] = c; wd[i] = d; wx[i] = lx[i]; wy[i] = ly[i]; continue; }
                float pa = wa[p], pb = wb[p], pc = wc[p], pd = wd[p];
                if (bones[i].noScale)
                {
                    float n0 = Mathf.Sqrt(pa * pa + pc * pc), n1 = Mathf.Sqrt(pb * pb + pd * pd);
                    if (n0 > 1e-6f) { pa /= n0; pc /= n0; }
                    if (n1 > 1e-6f) { pb /= n1; pd /= n1; }
                }
                wa[i] = pa * a + pb * c; wb[i] = pa * b + pb * d;
                wc[i] = pc * a + pd * c; wd[i] = pc * b + pd * d;
                wx[i] = wa[p] * lx[i] + wb[p] * ly[i] + wx[p];
                wy[i] = wc[p] * lx[i] + wd[p] * ly[i] + wy[p];
            }
        }

        // vị trí thế giới của xương (pixel rig, y lên), sau World()
        public Vector2 BonePos(int b) => b >= 0 && b < wx.Length ? new Vector2(wx[b], wy[b]) : Vector2.zero;

        public SkinPass NewPass()
        {
            var p = new SkinPass { lastAtt = new int[asset.slots.Length] };
            for (int i = 0; i < p.lastAtt.Length; i++) p.lastAtt[i] = int.MinValue;
            return p;
        }

        // Dựng đỉnh theo slot (sau World): toạ độ = pixel rig x scale, lật ngang nếu flipX; hideSlot: slot vẽ trong suốt (-1: không).
        // Trả số đỉnh; trisChanged: hình trong slot đổi nên Tris đã dựng lại (nơi gọi đặt lại tam giác của Mesh).
        public int Skin(Vector3[] verts, Vector2[] uvs, Color32[] cols, float scale, bool flipX, int hideSlot, out bool trisChanged) =>
            Skin(main, null, false, verts, uvs, cols, scale, flipX, hideSlot, out trisChanged);

        // như trên nhưng chỉ các slot có mask[s] == want (mask null: mọi slot), theo pass riêng (Tris của pass đó)
        public int Skin(SkinPass pass, bool[] mask, bool want, Vector3[] verts, Vector2[] uvs, Color32[] cols, float scale, bool flipX,
                        int hideSlot, out bool trisChanged)
        {
            trisChanged = false;
            int nv = 0;
            float fx = flipX ? -scale : scale;
            var lastAtt = pass.lastAtt;
            for (int s = 0; s < asset.slots.Length; s++)
            {
                int att0 = mask == null || mask[s] == want ? slotAtt[s] : -1;
                if (att0 != lastAtt[s]) { trisChanged = true; lastAtt[s] = att0; }
                if (slotStart != null) slotStart[s] = nv;
                if (att0 < 0) continue;
                var att = asset.atts[att0];
                var w = att.wInfo;
                byte alpha = s == hideSlot ? (byte)0 : (byte)Mathf.RoundToInt(slotAlpha[s] * 255);
                var col = new Color32(255, 255, 255, alpha);
                int n = att.uvs.Length / 2, k = 0;
                for (int v = 0; v < n; v++)
                {
                    int cnt = (int)w[k++];
                    float x = 0, y = 0;
                    for (int j = 0; j < cnt; j++, k += 4)
                    {
                        int bi = (int)w[k];
                        float bx = w[k + 1], by = w[k + 2], ww = w[k + 3];
                        x += (wa[bi] * bx + wb[bi] * by + wx[bi]) * ww;
                        y += (wc[bi] * bx + wd[bi] * by + wy[bi]) * ww;
                    }
                    verts[nv] = new Vector3(x * fx, y * scale, 0);
                    uvs[nv] = new Vector2(att.uvs[2 * v], att.uvs[2 * v + 1]);
                    cols[nv] = col;
                    nv++;
                }
            }
            if (slotMask != null)
            {
                trisChanged = true;   // lưới đổi mỗi khung: nơi gọi đặt lại cả đỉnh lẫn tam giác
                return ClipTris(pass, verts, uvs, cols, nv, fx, scale);
            }
            if (trisChanged || pass.Tris.Length == 0)
            {
                trisChanged = true;
                int nt = 0;
                for (int s = 0; s < asset.slots.Length; s++)
                    if (lastAtt[s] >= 0) nt += asset.atts[lastAtt[s]].tris.Length;
                var tris = pass.Tris = new int[nt];
                int off = 0, ti = 0;
                for (int s = 0; s < asset.slots.Length; s++)
                {
                    if (lastAtt[s] < 0) continue;
                    var att = asset.atts[lastAtt[s]];
                    foreach (var tv in att.tris) tris[ti++] = tv + off;
                    off += att.uvs.Length / 2;
                }
            }
            return nv;
        }

        // Rig có mặt nạ cắt: dựng lại danh sách tam giác mỗi khung. Slot ngoài vùng cắt chép nguyên; slot trong vùng cắt: tam giác
        // nằm hẳn trong đa giác giữ nguyên, nằm hẳn ngoài một cạnh thì bỏ, bị xén thì cắt (Sutherland–Hodgman) và thêm đỉnh mới vào
        // cuối mảng đỉnh. Tris có sức chứa cố định, phần chưa dùng là tam giác rỗng (0, 0, 0) để nơi gọi không phải đổi cách nạp
        // và không sinh rác mỗi khung. Trả số đỉnh sau khi thêm.
        int ClipTris(SkinPass pass, Vector3[] verts, Vector2[] uvs, Color32[] cols, int nv, float fx, float scale)
        {
            var lastAtt = pass.lastAtt;
            int cap = extraVerts * 3;
            for (int s = 0; s < lastAtt.Length; s++)
                if (lastAtt[s] >= 0) cap += asset.atts[lastAtt[s]].tris.Length;
            if (pass.Tris.Length != cap) { pass.Tris = new int[cap]; pass.used = 0; }
            var tris = pass.Tris;
            int ti = 0, curMask = -1, np = 0;
            float orient = 1;
            for (int s = 0; s < lastAtt.Length; s++)
            {
                if (lastAtt[s] < 0) continue;
                var at = asset.atts[lastAtt[s]].tris;
                int off = slotStart[s], m = slotMask[s];
                if (m < 0)
                {
                    for (int q = 0; q < at.Length; q++) tris[ti++] = at[q] + off;
                    continue;
                }
                if (m != curMask)
                {
                    // đa giác cắt trong cùng hệ với đỉnh (đã nhân scale, đã lật); chiều quay quyết định bên nào là "trong"
                    var mk = masks[m];
                    int b = mk.bone;
                    np = mk.verts.Length / 2;
                    float area = 0;
                    for (int i = 0; i < np; i++)
                    {
                        float bx = mk.verts[2 * i], by = mk.verts[2 * i + 1];
                        mpx[i] = (wa[b] * bx + wb[b] * by + wx[b]) * fx;
                        mpy[i] = (wc[b] * bx + wd[b] * by + wy[b]) * scale;
                    }
                    for (int i = 0; i < np; i++)
                    {
                        int j = (i + 1) % np;
                        area += mpx[i] * mpy[j] - mpx[j] * mpy[i];
                    }
                    orient = area >= 0 ? 1 : -1;
                    curMask = m;
                }
                for (int q = 0; q + 2 < at.Length; q += 3)
                {
                    int i0 = at[q] + off, i1 = at[q + 1] + off, i2 = at[q + 2] + off;
                    Vector3 v0 = verts[i0], v1 = verts[i1], v2 = verts[i2];
                    bool allIn = true, gone = false;
                    for (int e = 0; e < np; e++)
                    {
                        int f = (e + 1) % np;
                        float ex = mpx[e], ey = mpy[e], dx = (mpx[f] - ex) * orient, dy = (mpy[f] - ey) * orient;
                        float d0 = dx * (v0.y - ey) - dy * (v0.x - ex);
                        float d1 = dx * (v1.y - ey) - dy * (v1.x - ex);
                        float d2 = dx * (v2.y - ey) - dy * (v2.x - ex);
                        if (d0 < 0 && d1 < 0 && d2 < 0) { gone = true; break; }
                        if (d0 < 0 || d1 < 0 || d2 < 0) allIn = false;
                    }
                    if (gone) continue;
                    if (allIn)
                    {
                        tris[ti++] = i0; tris[ti++] = i1; tris[ti++] = i2;
                        continue;
                    }
                    float[] src = clipA, dst = clipB;
                    Put(src, 0, v0, uvs[i0]); Put(src, 1, v1, uvs[i1]); Put(src, 2, v2, uvs[i2]);
                    int n = 3;
                    for (int e = 0; e < np && n >= 3; e++)
                    {
                        int f = (e + 1) % np;
                        n = ClipEdge(src, n, dst, mpx[e], mpy[e], (mpx[f] - mpx[e]) * orient, (mpy[f] - mpy[e]) * orient);
                        var sw = src; src = dst; dst = sw;
                    }
                    if (n < 3 || nv + n > verts.Length || ti + (n - 2) * 3 > tris.Length) continue;
                    int bs = nv;
                    var col = cols[i0];
                    for (int k = 0; k < n; k++)
                    {
                        verts[nv] = new Vector3(src[4 * k], src[4 * k + 1], 0);
                        uvs[nv] = new Vector2(src[4 * k + 2], src[4 * k + 3]);
                        cols[nv] = col;
                        nv++;
                    }
                    for (int k = 1; k < n - 1; k++) { tris[ti++] = bs; tris[ti++] = bs + k; tris[ti++] = bs + k + 1; }
                }
            }
            int end = ti;
            for (; ti < pass.used; ti++) tris[ti] = 0;
            pass.used = end;
            return nv;
        }

        static void Put(float[] a, int i, Vector3 v, Vector2 uv)
        {
            a[4 * i] = v.x; a[4 * i + 1] = v.y; a[4 * i + 2] = uv.x; a[4 * i + 3] = uv.y;
        }

        // cắt đa giác src (n đỉnh, mỗi đỉnh x, y, u, v) theo một cạnh: giữ phần bên trái của vectơ (dx, dy) đặt tại (ex, ey)
        static int ClipEdge(float[] src, int n, float[] dst, float ex, float ey, float dx, float dy)
        {
            int m = 0;
            for (int i = 0; i < n; i++)
            {
                int a = 4 * i, b = 4 * ((i + 1) % n);
                float da = dx * (src[a + 1] - ey) - dy * (src[a] - ex);
                float db = dx * (src[b + 1] - ey) - dy * (src[b] - ex);
                if (da >= 0)
                {
                    dst[4 * m] = src[a]; dst[4 * m + 1] = src[a + 1]; dst[4 * m + 2] = src[a + 2]; dst[4 * m + 3] = src[a + 3];
                    m++;
                }
                if ((da >= 0) != (db >= 0))
                {
                    float t = da / (da - db);
                    for (int c = 0; c < 4; c++) dst[4 * m + c] = src[a + c] + (src[b + c] - src[a + c]) * t;
                    m++;
                }
            }
            return m;
        }

        // ---- khoá
        public static float Sample1(float[] k, float t)
        {
            const int S = 7;
            int n = k.Length / S;
            if (n == 0) return 0;
            if (t <= k[0]) return k[1];
            if (t >= k[(n - 1) * S]) return k[(n - 1) * S + 1];
            int i = 0;
            while (i < n - 2 && t >= k[(i + 1) * S]) i++;
            int o = i * S, q = o + S;
            float t0 = k[o], v0 = k[o + 1], t1 = k[q], v1 = k[q + 1];
            switch ((int)k[o + 2])
            {
                case 1: return v0;
                case 2: return Bezier(t0, v0, k[o + 3], k[o + 4], k[o + 5], k[o + 6], t1, v1, t);
                default: return v0 + (v1 - v0) * (t - t0) / Mathf.Max(1e-6f, t1 - t0);
            }
        }

        public static void Sample2(float[] k, float t, out float x, out float y)
        {
            const int S = 12;
            int n = k.Length / S;
            if (n == 0) { x = y = 0; return; }
            if (t <= k[0]) { x = k[1]; y = k[2]; return; }
            if (t >= k[(n - 1) * S]) { x = k[(n - 1) * S + 1]; y = k[(n - 1) * S + 2]; return; }
            int i = 0;
            while (i < n - 2 && t >= k[(i + 1) * S]) i++;
            int o = i * S, q = o + S;
            float t0 = k[o], t1 = k[q];
            switch ((int)k[o + 3])
            {
                case 1: x = k[o + 1]; y = k[o + 2]; return;
                case 2:
                    x = Bezier(t0, k[o + 1], k[o + 4], k[o + 5], k[o + 6], k[o + 7], t1, k[q + 1], t);
                    y = Bezier(t0, k[o + 2], k[o + 8], k[o + 9], k[o + 10], k[o + 11], t1, k[q + 2], t);
                    return;
                default:
                    float u = (t - t0) / Mathf.Max(1e-6f, t1 - t0);
                    x = k[o + 1] + (k[q + 1] - k[o + 1]) * u;
                    y = k[o + 2] + (k[q + 2] - k[o + 2]) * u;
                    return;
            }
        }

        // bezier bậc ba (t0,v0) (cx1,cy1) (cx2,cy2) (t1,v1): tìm s để x(s) = t rồi trả y(s)
        static float Bezier(float t0, float v0, float cx1, float cy1, float cx2, float cy2, float t1, float v1, float t)
        {
            float lo = 0, hi = 1, s = 0.5f;
            for (int it = 0; it < 22; it++)
            {
                s = (lo + hi) * 0.5f;
                float u = 1 - s;
                float xs = u * u * u * t0 + 3 * u * u * s * cx1 + 3 * u * s * s * cx2 + s * s * s * t1;
                if (xs < t) lo = s; else hi = s;
            }
            float m = 1 - s;
            return m * m * m * v0 + 3 * m * m * s * cy1 + 3 * m * s * s * cy2 + s * s * s * v1;
        }
    }
}
