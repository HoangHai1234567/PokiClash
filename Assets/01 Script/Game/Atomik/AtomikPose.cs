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
        readonly int[] slotAtt, lastAtt;
        readonly float[] slotAlpha;
        int[] tris = new int[0];

        public int[] Tris => tris;

        public AtomikPose(AtomikAsset a)
        {
            asset = a;
            int nb = a.bones.Length, ns = a.slots.Length;
            lx = new float[nb]; ly = new float[nb]; lr = new float[nb]; lsx = new float[nb]; lsy = new float[nb];
            px = new float[nb]; py = new float[nb]; pr = new float[nb]; psx = new float[nb]; psy = new float[nb];
            wa = new float[nb]; wb = new float[nb]; wc = new float[nb]; wd = new float[nb]; wx = new float[nb]; wy = new float[nb];
            slotAtt = new int[ns];
            lastAtt = new int[ns];
            slotAlpha = new float[ns];
            for (int i = 0; i < ns; i++) lastAtt[i] = int.MinValue;
            foreach (var att in a.atts) maxVerts += att.uvs.Length / 2;
            attsRef = a.atts;
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
                slotAlpha[s] = 1;
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

        // Dựng đỉnh theo slot (sau World): toạ độ = pixel rig x scale, lật ngang nếu flipX; hideSlot: slot vẽ trong suốt (-1: không).
        // Trả số đỉnh; trisChanged: hình trong slot đổi nên Tris đã dựng lại (nơi gọi đặt lại tam giác của Mesh).
        public int Skin(Vector3[] verts, Vector2[] uvs, Color32[] cols, float scale, bool flipX, int hideSlot, out bool trisChanged)
        {
            trisChanged = false;
            int nv = 0;
            float fx = flipX ? -scale : scale;
            for (int s = 0; s < asset.slots.Length; s++)
            {
                if (slotAtt[s] != lastAtt[s]) { trisChanged = true; lastAtt[s] = slotAtt[s]; }
                if (slotAtt[s] < 0) continue;
                var att = asset.atts[slotAtt[s]];
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
            if (trisChanged || tris.Length == 0)
            {
                trisChanged = true;
                int nt = 0;
                for (int s = 0; s < asset.slots.Length; s++)
                    if (slotAtt[s] >= 0) nt += asset.atts[slotAtt[s]].tris.Length;
                tris = new int[nt];
                int off = 0, ti = 0;
                for (int s = 0; s < asset.slots.Length; s++)
                {
                    if (slotAtt[s] < 0) continue;
                    var att = asset.atts[slotAtt[s]];
                    foreach (var tv in att.tris) tris[ti++] = tv + off;
                    off += att.uvs.Length / 2;
                }
            }
            return nv;
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
