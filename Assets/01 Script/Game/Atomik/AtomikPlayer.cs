// Phát một rig .atomik: tính xương từng khung, biến dạng lưới có trọng số trên CPU, vẽ bằng một Mesh (một lần vẽ, tam giác
// theo thứ tự slot). GameObject, MeshFilter, MeshRenderer dựng sẵn trong scene/prefab; ở đây chỉ sinh Mesh (luật PrefabOnly).
// Khoá animation theo cách Spine 4.2: xoay cộng vào góc gốc, dời cộng vào vị trí gốc, tỉ lệ nhân; đường cong bezier tuyệt đối.
using System;
using UnityEngine;

namespace PokiClash.Game
{
    [ExecuteAlways]
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
    public sealed class AtomikPlayer : MonoBehaviour
    {
        public AtomikAsset asset;
        public string clip = "idle";
        public bool loop = true;
        public float speed = 1f;
        public float mixTime = 0.12f;   // trộn tư thế khi đổi clip

        public float Time01 => cur >= 0 && asset.anims[cur].dur > 0 ? Mathf.Repeat(time, asset.anims[cur].dur) / asset.anims[cur].dur : 0;
        public bool Done => cur >= 0 && !loop && time >= asset.anims[cur].dur;

        Mesh mesh;
        AtomikAsset built;
        int cur = -1;
        float time, mixLeft;
        float[] lx, ly, lr, lsx, lsy;           // tư thế cục bộ
        float[] px, py, pr, psx, psy;           // tư thế lúc bắt đầu trộn
        float[] wa, wb, wc, wd, wx, wy;         // ma trận thế giới 2x3
        int[] slotAtt, lastAtt;
        Vector3[] verts;
        Vector2[] uvs;
        Color32[] cols;
        int[] tris;

        public void Play(string name, bool loopClip = true)
        {
            if (!Ready()) return;
            int i = asset.FindClip(name);
            if (i < 0) { Debug.LogWarning($"[Atomik] {asset.rigName}: không có clip {name}"); return; }
            if (cur >= 0 && mixTime > 0)
            {
                Array.Copy(lx, px, lx.Length); Array.Copy(ly, py, ly.Length); Array.Copy(lr, pr, lr.Length);
                Array.Copy(lsx, psx, lsx.Length); Array.Copy(lsy, psy, lsy.Length);
                mixLeft = mixTime;
            }
            cur = i;
            clip = name;
            loop = loopClip;
            time = 0;
            Apply();
        }

        // Dựng đúng một thời điểm (Editor chụp khung, kiểm so với khung Python).
        public void Sample(string name, float t)
        {
            if (!Ready()) return;
            cur = asset.FindClip(name);
            clip = name;
            time = t;
            mixLeft = 0;
            Apply();
        }

        void OnEnable()
        {
            if (!Ready()) return;
            cur = asset.FindClip(clip);
            time = 0;
            Apply();
        }

        void OnDisable()
        {
            if (mesh == null) return;
            if (Application.isPlaying) Destroy(mesh); else DestroyImmediate(mesh);
            mesh = null;
            built = null;
        }

        void Update()
        {
            if (!Ready()) return;
            if (Application.isPlaying)
            {
                float dt = UnityEngine.Time.deltaTime * speed;
                time += dt;
                if (mixLeft > 0) mixLeft = Mathf.Max(0, mixLeft - dt);
            }
            else if (cur < 0 || asset.anims[cur].name != clip) cur = asset.FindClip(clip);
            Apply();
        }

        bool Ready()
        {
            if (asset == null || asset.bones == null || asset.bones.Length == 0) return false;
            if (built == asset && mesh != null) return true;
            int nb = asset.bones.Length, ns = asset.slots.Length;
            lx = new float[nb]; ly = new float[nb]; lr = new float[nb]; lsx = new float[nb]; lsy = new float[nb];
            px = new float[nb]; py = new float[nb]; pr = new float[nb]; psx = new float[nb]; psy = new float[nb];
            wa = new float[nb]; wb = new float[nb]; wc = new float[nb]; wd = new float[nb]; wx = new float[nb]; wy = new float[nb];
            slotAtt = new int[ns];
            lastAtt = new int[ns];
            for (int i = 0; i < ns; i++) lastAtt[i] = int.MinValue;
            int maxV = 0;
            foreach (var a in asset.atts) maxV += a.uvs.Length / 2;
            verts = new Vector3[maxV];
            uvs = new Vector2[maxV];
            cols = new Color32[maxV];
            for (int i = 0; i < maxV; i++) cols[i] = new Color32(255, 255, 255, 255);
            if (mesh == null)
            {
                mesh = new Mesh { name = "atomik_" + asset.rigName, hideFlags = HideFlags.DontSave };
                mesh.MarkDynamic();
            }
            GetComponent<MeshFilter>().sharedMesh = mesh;
            var r = GetComponent<MeshRenderer>();
            if (asset.material != null && r.sharedMaterial != asset.material) r.sharedMaterial = asset.material;
            built = asset;
            cur = -1;
            return true;
        }

        void Apply()
        {
            var bones = asset.bones;
            int nb = bones.Length;
            for (int i = 0; i < nb; i++)
            {
                var b = bones[i];
                lx[i] = b.x; ly[i] = b.y; lr[i] = b.rot; lsx[i] = b.sx; lsy[i] = b.sy;
            }
            for (int s = 0; s < asset.slots.Length; s++) slotAtt[s] = asset.slots[s].att;
            if (cur >= 0)
            {
                var c = asset.anims[cur];
                float t = c.dur <= 0 ? 0 : loop ? Mathf.Repeat(time, c.dur) : Mathf.Min(time, c.dur);
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
            }
            if (mixLeft > 0 && mixTime > 0)
            {
                float w = 1 - mixLeft / mixTime;
                for (int i = 0; i < nb; i++)
                {
                    lx[i] = Mathf.Lerp(px[i], lx[i], w); ly[i] = Mathf.Lerp(py[i], ly[i], w);
                    lr[i] = Mathf.LerpAngle(pr[i], lr[i], w);
                    lsx[i] = Mathf.Lerp(psx[i], lsx[i], w); lsy[i] = Mathf.Lerp(psy[i], lsy[i], w);
                }
            }
            // ma trận thế giới (cha luôn đứng trước con)
            for (int i = 0; i < nb; i++)
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
            // da: đỉnh = tổng có trọng số (ma trận xương x vị trí gắn)
            float inv = 1f / Mathf.Max(1e-3f, asset.ppu);
            int nv = 0;
            bool trisDirty = false;
            for (int s = 0; s < asset.slots.Length; s++)
            {
                if (slotAtt[s] != lastAtt[s]) { trisDirty = true; lastAtt[s] = slotAtt[s]; }
                if (slotAtt[s] < 0) continue;
                var att = asset.atts[slotAtt[s]];
                var w = att.wInfo;
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
                    verts[nv] = new Vector3(x * inv, y * inv, 0);
                    uvs[nv] = new Vector2(att.uvs[2 * v], att.uvs[2 * v + 1]);
                    nv++;
                }
            }
            if (trisDirty || tris == null)
            {
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
                mesh.Clear();
                mesh.SetVertices(verts, 0, nv);
                mesh.SetUVs(0, uvs, 0, nv);
                mesh.SetColors(cols, 0, nv);
                mesh.SetTriangles(tris, 0, true);
            }
            else
            {
                mesh.SetVertices(verts, 0, nv);
                mesh.RecalculateBounds();
            }
        }

        // ---- khoá
        static float Sample1(float[] k, float t)
        {
            const int S = 7;
            int n = k.Length / S;
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

        static void Sample2(float[] k, float t, out float x, out float y)
        {
            const int S = 12;
            int n = k.Length / S;
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
