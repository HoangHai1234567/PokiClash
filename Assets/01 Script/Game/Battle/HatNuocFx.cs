// Lưới uGUI vẽ hiệu ứng nước bằng shader PokiClash/UIWaterFx (người dùng 2026-11-24 chọn "c": toàn bộ bộ nước trong trận chạy bằng
// shader thay khung vẽ sẵn; lốc nước giữ khung). Mỗi lớp hạt (HatDat / HatSau / HatTruoc) có một thành phần này, đặt sẵn trong prefab
// ngay sau "Mang" (menu "PokiClash/Prefab/Trận/Sàn đấu: nước shader", NuocFxMenu.cs) — không tạo GameObject hay Material lúc chạy.
// HatLua (HatNuocShader.cs) gọi Begin, các hàm hình (Ball, Strip, Sprite, Fan, Ring, Dot) mỗi khung rồi End: mỗi hình là một "mảnh" có
// lớp; End xếp mảnh theo lớp (ổn định) và ghép chỉ số theo thứ tự đó nên hình lớp cao vẽ sau. Mọi tham số của hình đi theo đỉnh
// (TEXCOORD1, TEXCOORD2: Canvas của lớp hạt phải bật hai kênh này). Toạ độ là toạ độ UI của lớp hạt (StageView.P đã đổi).
// Khung của thành phần đặt rộng 8000 quanh gốc như HatMang (RectMask2D của ô xem tướng không loại cả lưới).
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    [RequireComponent(typeof(CanvasRenderer))]
    public sealed class HatNuocFx : MaskableGraphic
    {
        public const float Ball_ = 0, Strip_ = 1, Mask_ = 2, Fan_ = 3, Ring_ = 4, Dot_ = 5, Fb_ = 6, Tube_ = 7, Glow_ = 8;
        // bảng màu của flipbook / ống tia (shader: TEXCOORD1.x = loại + 16 × bảng; 2026-11-25 tia năng lượng Mộc / Kim / Thổ theo tia Water Laser)
        public const int PalNuoc = 0, PalMoc = 1, PalHoPhach = 2, PalLua = 3, PalKim = 4, PalTho = 5, PalMa = 6; // 6: nước ma thuật xanh ngọc (cầu ma thủy)
        const float FbTexel = 0.5f / 2048; // co uv nửa điểm ảnh vào trong ô atlas (không lấy lẫn ô bên)

        [SerializeField] Texture2D noise; // nhiễu lặp (Assets/03 Art/Fx/Nuoc/nuoc_nhieu.png)

        struct Chunk
        {
            public float layer;
            public int i0, n;
        }

        readonly List<UIVertex> verts = new List<UIVertex>(4096);
        readonly List<int> raw = new List<int>(8192);
        readonly List<int> idx = new List<int>(8192);
        readonly List<Chunk> chunks = new List<Chunk>(256);
        static readonly System.Comparison<Chunk> ByLayer = (a, b) => a.layer.CompareTo(b.layer);
        bool had;

        public override Texture mainTexture => noise ? noise : s_WhiteTexture;

        // tham số hình đi theo đỉnh qua TEXCOORD1, TEXCOORD2: bật hai kênh này trên Canvas chứa lớp hạt (menu cũng bật sẵn trong prefab)
        protected override void OnEnable()
        {
            base.OnEnable();
            var c = canvas;
            if (c) c.additionalShaderChannels |= AdditionalCanvasShaderChannels.TexCoord1 | AdditionalCanvasShaderChannels.TexCoord2;
        }

        public void Begin()
        {
            verts.Clear();
            raw.Clear();
            chunks.Clear();
        }

        public bool Any => chunks.Count > 0;

        public void End()
        {
            for (int i = 0; i < chunks.Count; i++)
            {
                var c = chunks[i];
                c.layer += i * 1e-6f;
                chunks[i] = c;
            }
            chunks.Sort(ByLayer);
            idx.Clear();
            foreach (var c in chunks)
                for (int k = 0; k < c.n; k++) idx.Add(raw[c.i0 + k]);
            if (chunks.Count > 0 || had) SetVerticesDirty();
            had = chunks.Count > 0;
        }

        protected override void OnPopulateMesh(VertexHelper vh)
        {
            vh.Clear();
            if (verts.Count > 0 && idx.Count > 0) vh.AddUIVertexStream(verts, idx);
        }

        int V(Vector2 pos, Vector2 uv, Vector4 u1, Vector4 u2, Color32 col)
        {
            verts.Add(new UIVertex { position = pos, color = col, uv0 = new Vector4(uv.x, uv.y, 0, 0), uv1 = u1, uv2 = u2 });
            return verts.Count - 1;
        }

        void Close(float layer, int i0) => chunks.Add(new Chunk { layer = layer, i0 = i0, n = raw.Count - i0 });

        // tứ giác tâm c, trục ax (nửa rộng), ay (nửa cao); uv góc (u0,v0)..(u1,v1)
        void Quad(float layer, Vector2 c, Vector2 ax, Vector2 ay, Vector2 uvMin, Vector2 uvMax, Vector4 u1, Vector4 u2, Color32 col)
        {
            int i0 = raw.Count;
            int a = V(c - ax - ay, new Vector2(uvMin.x, uvMin.y), u1, u2, col);
            int b = V(c + ax - ay, new Vector2(uvMax.x, uvMin.y), u1, u2, col);
            int d = V(c + ax + ay, new Vector2(uvMax.x, uvMax.y), u1, u2, col);
            int e = V(c - ax + ay, new Vector2(uvMin.x, uvMax.y), u1, u2, col);
            raw.Add(a); raw.Add(b); raw.Add(d);
            raw.Add(a); raw.Add(d); raw.Add(e);
            Close(layer, i0);
        }

        static Vector2 Rot(float deg)
        {
            float r = deg * Mathf.Deg2Rad;
            return new Vector2(Mathf.Cos(r), Mathf.Sin(r));
        }

        // cầu bán kính r (UI); thr > 0 = tan lấm tấm; wob = độ rung mép; spin = tốc xoay vệt; sx: giãn theo hướng ang (bay)
        public void Ball(float layer, Vector2 c, float r, Color32 col, float thr, float wob, float spin, float time, float seed, float ang = 0, float sx = 1,
            int pal = 0)
        {
            var ux = Rot(ang);
            var uy = new Vector2(-ux.y, ux.x);
            float pad = 1 + wob + 0.04f;
            Quad(layer, c, ux * r * sx * pad, uy * r * pad, new Vector2(-pad, -pad), new Vector2(pad, pad), new Vector4(Ball_ + 16 * pal, thr, wob, spin),
                new Vector4(time, seed, 0, 0), col);
        }

        // dải theo đường pts (UI), nửa bề rộng hw[i]; head / tail: ngưỡng hai đầu theo quãng 0..1 (hiện khi tail < m < head)
        public void Strip(float layer, List<Vector2> pts, List<float> hw, Color32 col, float head, float tail, float time, float seed, Vector2 lightXY,
            float foam = 0)
        {
            int n = pts.Count;
            if (n < 2) return;
            int i0 = raw.Count;
            float tot = 0;
            for (int i = 1; i < n; i++) tot += (pts[i] - pts[i - 1]).magnitude;
            tot = Mathf.Max(tot, 1e-3f);
            float s = 0;
            int prev = -1;
            for (int i = 0; i < n; i++)
            {
                if (i > 0) s += (pts[i] - pts[i - 1]).magnitude;
                var tg = pts[Mathf.Min(n - 1, i + 1)] - pts[Mathf.Max(0, i - 1)];
                tg = tg.sqrMagnitude > 1e-6f ? tg.normalized : Vector2.right;
                var nm = new Vector2(-tg.y, tg.x);
                float w = Mathf.Max(0.01f, hw[i]);
                float side = Vector2.Dot(nm, lightXY);
                var u2 = new Vector4(time, seed, s / tot, side);
                var u1 = new Vector4(Strip_, foam, head, tail); // foam > 0,5: dải bọt trắng rách
                int l = V(pts[i] + nm * w, new Vector2(s / 100f, 1), u1, u2, col);
                int r = V(pts[i] - nm * w, new Vector2(s / 100f, -1), u1, u2, col);
                if (prev >= 0)
                {
                    raw.Add(prev); raw.Add(prev + 1); raw.Add(r);
                    raw.Add(prev); raw.Add(r); raw.Add(l);
                }
                prev = l;
            }
            Close(layer, i0);
        }

        // sprite mặt nạ mềm (ô atlas mask), cỡ w × h, xoay ang; thr ngưỡng tan, band dải mép bọt, flat: không vòm; ns cỡ nhiễu
        public void Sprite(float layer, Vector2 c, float w, float h, float ang, int mask, float thr, float band, bool flat, float ns, Color32 col,
            float time, float seed)
        {
            var ux = Rot(ang);
            var uy = new Vector2(-ux.y, ux.x);
            Quad(layer, c, ux * (w * 0.5f), uy * (h * 0.5f), Vector2.zero, Vector2.one, new Vector4(Mask_, thr, mask, band),
                new Vector4(time, seed, flat ? 1 : 0, ns), col);
        }

        // quạt (vương miện ngửa): gốc o, hướng ang (độ, 90 = lên), bán kính R, nửa góc mở half (rad), bán kính trong r0 (0..1)
        public void Fan(float layer, Vector2 o, float ang, float R, float half, float r0, int mask, float tiles, float thr, Color32 col, float time,
            float seed, float squash = 1)
        {
            var uy = Rot(ang);                     // trục quạt
            var ux = new Vector2(uy.y, -uy.x);     // ngang quạt (phải của trục)
            float sw = Mathf.Max(Mathf.Sin(Mathf.Min(half, 1.5f)), 0.2f);
            // ô bao quạt: x ∈ [-sw, sw] (toạ độ quạt đã chuẩn hoá theo R), y ∈ [0, 1]
            var c = o + uy * (R * 0.5f);
            Quad(layer, c, ux * (R * sw * squash), uy * (R * 0.5f), new Vector2(-sw, 0), new Vector2(sw, 1), new Vector4(Fan_, thr, mask, half),
                new Vector4(time, seed, tiles, r0), col);
        }

        // vành loang trên đất (elip rx × ry), bán kính trong r0 (0..1), half: +1 nửa trước, −1 nửa sau, 0 cả vành
        public void Ring(float layer, Vector2 c, float rx, float ry, float r0, int mask, float tiles, float thr, int half, Color32 col, float time,
            float seed)
        {
            Quad(layer, c, new Vector2(rx, 0), new Vector2(0, ry), new Vector2(-1, -1), new Vector2(1, 1), new Vector4(Ring_, thr, mask, r0),
                new Vector4(time, seed, tiles, half), col);
        }

        // FLIPBOOK của gói mẫu (atlas nuoc_fb, bảng NuocFbBang): tâm c, cỡ w × h (UI; h ≤ 0 → theo tỉ lệ khung gốc), xoay ang (độ),
        // frame: chỉ số khung thực (lẻ = chồng mờ sang khung sau); cut: ngưỡng mép (0,2–0,5); lift: nâng giá trị (+ sáng hơn);
        // kind 0 thường, 1 nền đất (phẳng, tối hơn), 2 toàn bọt trắng; flipX: lật ngang (hướng toé)
        public void Fb(float layer, Vector2 c, float w, float h, float ang, NFb fb, float frame, float cut, Color32 col, float time, float seed,
            float lift = 0, int kind = 0, bool flipX = false, int pal = 0)
        {
            var d = NuocFbBang.Get(fb);
            if (h <= 0) h = w / Mathf.Max(0.05f, d.aspect);
            float f = Mathf.Clamp(frame, 0, d.frames - 1);
            int i0 = (int)f, i1 = Mathf.Min(i0 + 1, d.frames - 1);
            float t = f - i0;
            Vector2 a0 = d.Min(i0), b0 = d.Min(i1);
            float du = d.cu - 2 * FbTexel, dv = d.cv - 2 * FbTexel;
            a0 += new Vector2(FbTexel, FbTexel);
            b0 += new Vector2(FbTexel, FbTexel);
            var ux = Rot(ang);
            var uy = new Vector2(-ux.y, ux.x);
            var ax = ux * (w * 0.5f);
            var ay = uy * (h * 0.5f);
            var u1 = new Vector4(Fb_ + 16 * pal, t, cut, d.pair);
            var u2 = new Vector4(time, seed, lift, kind);
            float l = flipX ? 1 : 0, r = flipX ? 0 : 1;
            int i00 = raw.Count;
            int p = VF(c - ax - ay, new Vector4(a0.x + du * l, a0.y, b0.x + du * l, b0.y), u1, u2, col);
            int q = VF(c + ax - ay, new Vector4(a0.x + du * r, a0.y, b0.x + du * r, b0.y), u1, u2, col);
            int s = VF(c + ax + ay, new Vector4(a0.x + du * r, a0.y + dv, b0.x + du * r, b0.y + dv), u1, u2, col);
            int e = VF(c - ax + ay, new Vector4(a0.x + du * l, a0.y + dv, b0.x + du * l, b0.y + dv), u1, u2, col);
            raw.Add(p); raw.Add(q); raw.Add(s);
            raw.Add(p); raw.Add(s); raw.Add(e);
            Close(layer, i00);
        }

        int VF(Vector2 pos, Vector4 uv, Vector4 u1, Vector4 u2, Color32 col)
        {
            verts.Add(new UIVertex { position = pos, color = col, uv0 = uv, uv1 = u1, uv2 = u2 });
            return verts.Count - 1;
        }

        // ỐNG TIA kiểu Water Laser theo đường pts, nửa bề rộng hw[i]; kind 0 vỏ ngoài, 1 lõi sáng, 2 vệt bọt trôi, 3 vỏ mỏng rách;
        // scroll: tốc trôi vân (quãng / giây, theo hướng tia); cut: ngưỡng vỡ / tan (0 = liền)
        public void Tube(float layer, List<Vector2> pts, List<float> hw, Color32 col, int kind, float scroll, float cut, float time, float seed,
            Vector2 lightXY, int pal = 0)
        {
            int n = pts.Count;
            if (n < 2) return;
            int i0 = raw.Count;
            float tot = 0;
            for (int i = 1; i < n; i++) tot += (pts[i] - pts[i - 1]).magnitude;
            tot = Mathf.Max(tot, 1e-3f);
            float s = 0;
            int prev = -1;
            var u1 = new Vector4(Tube_ + 16 * pal, cut, scroll, kind);
            for (int i = 0; i < n; i++)
            {
                if (i > 0) s += (pts[i] - pts[i - 1]).magnitude;
                var tg = pts[Mathf.Min(n - 1, i + 1)] - pts[Mathf.Max(0, i - 1)];
                tg = tg.sqrMagnitude > 1e-6f ? tg.normalized : Vector2.right;
                var nm = new Vector2(-tg.y, tg.x);
                float w = Mathf.Max(0.01f, hw[i]);
                var u2 = new Vector4(time, seed, s / tot, Vector2.Dot(nm, lightXY));
                int l = V(pts[i] + nm * w, new Vector2(s / 100f, 1), u1, u2, col);
                int r = V(pts[i] - nm * w, new Vector2(s / 100f, -1), u1, u2, col);
                if (prev >= 0)
                {
                    raw.Add(prev); raw.Add(prev + 1); raw.Add(r);
                    raw.Add(prev); raw.Add(r); raw.Add(l);
                }
                prev = l;
            }
            Close(layer, i0);
        }

        // QUẦNG mềm (NGOẠI LỆ luật không quầng sáng, chỉ cầu ma thủy Thôn Kình — người dùng 2026-11-25): đĩa bán kính r, hard = mũ độ hiện (lớn:
        // gọn tâm), tone 0 sáng / 1 tối, noise: mép chập chờn; sx giãn theo góc ang (quầng dẹt trên đất)
        public void Glow(float layer, Vector2 c, float r, float hard, int tone, float noise, Color32 col, float time, float seed, int pal = 0, float sx = 1,
            float ang = 0)
        {
            var ux = Rot(ang);
            var uy = new Vector2(-ux.y, ux.x);
            Quad(layer, c, ux * (r * sx), uy * r, new Vector2(-1, -1), new Vector2(1, 1), new Vector4(Glow_ + 16 * pal, 0, hard, tone),
                new Vector4(time, seed, noise, 0), col);
        }

        // giọt tròn bán kính r; tone 0 lam sâu, 1 lam sáng, 2 bọt
        public void Dot(float layer, Vector2 c, float r, int tone, Color32 col, float sx = 1, float ang = 0, int pal = 0)
        {
            var ux = Rot(ang);
            var uy = new Vector2(-ux.y, ux.x);
            Quad(layer, c, ux * (r * sx * 1.05f), uy * (r * 1.05f), new Vector2(-1.05f, -1.05f), new Vector2(1.05f, 1.05f),
                new Vector4(Dot_ + 16 * pal, 0, tone, 0), Vector4.zero, col);
        }
    }
}
