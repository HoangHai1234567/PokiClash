// Nén thử (hướng 2 của việc giảm dung lượng build, người dùng 2026-11-21): so hình đang vào game với mức nén đề xuất cho các nhóm ảnh
// nặng mà người dùng chưa chốt mức nén: nền đảo, nền trận, nền Nhà, ảnh khoảng cách _dist, hạt hiệu ứng. KHÔNG đổi cách nhập ảnh nào:
// chỉ ghi ảnh so vào Temp/PokiShots/nen_thu (cột trái là bản đang vào game, các cột sau là bản đề xuất; hàng trên đúng cỡ điểm ảnh,
// hàng dưới phóng 3 lần chỗ nhiều nét nhất) và ước dung lượng cả nhóm nếu áp (bao_cao.txt).
// Không đụng: máy bi (ASTC 4x4, người dùng chê 6x6 bết 2026-11-20), chân dung (5x5, chê 8x8 vỡ khối 2026-11-04).
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class CompressTrial
    {
        sealed class Variant
        {
            public string label;
            public TextureFormat fmt;
            public int cap; // cạnh tối đa (0: giữ cỡ đang nhập)
        }

        sealed class Sample
        {
            public string path;
            public Variant[] variants;
        }

        static Variant V(string label, TextureFormat fmt, int cap = 0) => new Variant { label = label, fmt = fmt, cap = cap };

        static readonly Sample[] Samples =
        {
            new Sample { path = "Assets/03 Art/Islands/land_thuy.png", variants = new[] { V("ASTC 8x8", TextureFormat.ASTC_8x8) } },
            new Sample { path = "Assets/03 Art/Islands/zone_thuy.png", variants = new[] { V("ASTC 8x8", TextureFormat.ASTC_8x8) } },
            new Sample { path = "Assets/03 Art/BattleBG/battle_hoa_c01.png", variants = new[] { V("ASTC 8x8", TextureFormat.ASTC_8x8) } },
            new Sample { path = "Assets/03 Art/Home/home_base.png", variants = new[] { V("ASTC 8x8", TextureFormat.ASTC_8x8) } },
            new Sample { path = "Assets/03 Art/Baked/Islands/land_thuy_dist.png", variants = new[] { V("EAC RG", TextureFormat.EAC_RG) } },
            new Sample
            {
                path = "Assets/03 Art/Fx/Hat/hat_arc_0.png",
                variants = new[] { V("ASTC 8x8", TextureFormat.ASTC_8x8), V("ASTC 6x6 cạnh 256", TextureFormat.ASTC_6x6, 256) },
            },
        };

        static string OutDir => Path.Combine(PlayTour.ShotDir, "nen_thu");

        [MenuItem("PokiClash/Dung lượng: nén thử nền to + hạt (ảnh so, không đổi gì)", priority = 91)]
        static void Run()
        {
            Directory.CreateDirectory(OutDir);
            var sb = new StringBuilder();
            sb.AppendLine($"Nén thử {System.DateTime.Now:yyyy-MM-dd HH:mm}, nền {EditorUserBuildSettings.activeBuildTarget}. Cột trái: đang vào game; cột sau: đề xuất.");
            sb.AppendLine();
            foreach (var s in Samples)
            {
                try { sb.AppendLine(Compare(s)); }
                catch (System.Exception e) { sb.AppendLine($"{s.path}: lỗi {e.Message}"); }
            }
            sb.AppendLine();
            sb.AppendLine("Ước cả nhóm nếu áp (cỡ trong gói dữ liệu, trước nén LZ4HC):");
            Estimate(sb, "Nền to (Islands, BattleBG, Home/home_base, cạnh từ 1024, đang ASTC 5x5/6x6) → ASTC 8x8",
                p => (p.StartsWith("Assets/03 Art/Islands/") || p.StartsWith("Assets/03 Art/BattleBG/") || p.StartsWith("Assets/03 Art/Home/home_base")),
                t => Mathf.Max(t.width, t.height) >= 1024 && (t.format == TextureFormat.ASTC_6x6 || t.format == TextureFormat.ASTC_5x5),
                TextureFormat.ASTC_8x8, 0);
            Estimate(sb, "Ảnh khoảng cách _dist (Baked/Islands) RG16 → EAC RG",
                p => p.StartsWith("Assets/03 Art/Baked/Islands/") && p.EndsWith("_dist.png"), t => t.format == TextureFormat.RG16, TextureFormat.EAC_RG, 0);
            Estimate(sb, "Hạt hiệu ứng Fx/Hat → ASTC 8x8", p => p.StartsWith("Assets/03 Art/Fx/Hat/"), t => t.format == TextureFormat.ASTC_6x6,
                TextureFormat.ASTC_8x8, 0);
            Estimate(sb, "Hạt hiệu ứng Fx/Hat → ASTC 6x6, cạnh tối đa 256", p => p.StartsWith("Assets/03 Art/Fx/Hat/"),
                t => t.format == TextureFormat.ASTC_6x6 && Mathf.Max(t.width, t.height) > 256, TextureFormat.ASTC_6x6, 256);
            File.WriteAllText(Path.Combine(OutDir, "bao_cao.txt"), sb.ToString());
            Debug.Log("[Nén thử] " + Path.Combine(OutDir, "bao_cao.txt") + "\n" + sb);
        }

        static string Compare(Sample s)
        {
            var ti = (TextureImporter)AssetImporter.GetAtPath(s.path);
            var cur = AssetDatabase.LoadAssetAtPath<Texture2D>(s.path);
            if (!ti || !cur) return $"{s.path}: không thấy";
            bool linear = !ti.sRGBTexture;
            bool data = s.path.EndsWith("_dist.png"); // ảnh số liệu: xem cả hai kênh, bỏ alpha
            int w = cur.width, h = cur.height;
            var cols = new List<Color32[]> { Read(cur, w, h, linear) };
            var line = new StringBuilder($"{Path.GetFileName(s.path)} {w}x{h}: đang {cur.format} {Kb(Storage(cur))}");

            var src = new Texture2D(2, 2, TextureFormat.RGBA32, false, linear);
            src.LoadImage(File.ReadAllBytes(s.path));
            foreach (var v in s.variants)
            {
                int tw = w, th = h;
                if (v.cap > 0 && Mathf.Max(w, h) > v.cap)
                {
                    float k = v.cap / (float)Mathf.Max(w, h);
                    tw = Mathf.Max(1, Mathf.RoundToInt(w * k));
                    th = Mathf.Max(1, Mathf.RoundToInt(h * k));
                }
                var t = new Texture2D(tw, th, TextureFormat.RGBA32, false, linear);
                t.SetPixels32(Read(src, tw, th, linear));
                t.Apply(false);
                EditorUtility.CompressTexture(t, v.fmt, TextureCompressionQuality.Normal);
                t.Apply(false);
                cols.Add(Read(t, w, h, linear)); // hiện ở cỡ cũ (bản thu nhỏ thì phóng lại như GPU vẽ)
                line.Append($" | {v.label}{(v.cap > 0 ? $" ({tw}x{th})" : "")} {Kb(Bytes(v.fmt, tw, th))}");
                Object.DestroyImmediate(t);
            }
            Object.DestroyImmediate(src);

            var crop = Busy(cols[0], w, h, 512, 512);
            int zs = Mathf.Min(160, crop.width, crop.height);
            var zc = Busy(cols[0], w, h, zs, zs, crop);
            const int gap = 12, zoom = 3;
            int cw = Mathf.Max(crop.width, zs * zoom), W = cols.Count * cw + (cols.Count - 1) * gap, H = crop.height + gap + zs * zoom;
            var canvas = new Color32[W * H];
            for (int i = 0; i < canvas.Length; i++) canvas[i] = new Color32(255, 255, 255, 255);
            for (int c = 0; c < cols.Count; c++)
            {
                int ox = c * (cw + gap);
                // hàng dưới: phóng 3 lần (điểm vuông, thấy rõ khối nén); hàng trên: đúng cỡ (ảnh ghi từ dưới lên)
                for (int y = 0; y < zs * zoom; y++)
                    for (int x = 0; x < zs * zoom; x++)
                        canvas[y * W + ox + x] = Show(cols[c][(zc.y + y / zoom) * w + zc.x + x / zoom], data);
                int oy = zs * zoom + gap;
                for (int y = 0; y < crop.height; y++)
                    for (int x = 0; x < crop.width; x++)
                        canvas[(oy + y) * W + ox + x] = Show(cols[c][(crop.y + y) * w + crop.x + x], data);
            }
            var outTex = new Texture2D(W, H, TextureFormat.RGBA32, false);
            outTex.SetPixels32(canvas);
            outTex.Apply(false);
            string file = Path.Combine(OutDir, Path.GetFileNameWithoutExtension(s.path) + "_so.png");
            File.WriteAllBytes(file, outTex.EncodeToPNG());
            Object.DestroyImmediate(outTex);
            return line + $" → {Path.GetFileName(file)}";
        }

        // điểm ảnh trên nền xám (thấy mép trong suốt); ảnh số liệu: kênh R, G thành màu, đặc
        static Color32 Show(Color32 c, bool data)
        {
            if (data) return new Color32(c.r, c.g, 0, 255);
            int a = c.a;
            byte M(byte v) => (byte)((v * a + 150 * (255 - a)) / 255);
            return new Color32(M(c.r), M(c.g), M(c.b), 255);
        }

        // vẽ texture ra w x h (GPU giải nén, lọc song tuyến khi đổi cỡ) rồi đọc về
        static Color32[] Read(Texture tex, int w, int h, bool linear)
        {
            var rt = RenderTexture.GetTemporary(w, h, 0, RenderTextureFormat.ARGB32, linear ? RenderTextureReadWrite.Linear : RenderTextureReadWrite.sRGB);
            var prev = RenderTexture.active;
            Graphics.Blit(tex, rt);
            RenderTexture.active = rt;
            var t = new Texture2D(w, h, TextureFormat.RGBA32, false, linear);
            t.ReadPixels(new Rect(0, 0, w, h), 0, 0, false);
            t.Apply(false);
            RenderTexture.active = prev;
            RenderTexture.ReleaseTemporary(rt);
            var px = t.GetPixels32();
            Object.DestroyImmediate(t);
            return px;
        }

        // khung cw x ch nhiều nét nhất (độ chênh sáng giữa các điểm cách 4), trong vùng within (mặc định cả ảnh)
        static RectInt Busy(Color32[] px, int w, int h, int cw, int ch, RectInt? within = null)
        {
            var r = within ?? new RectInt(0, 0, w, h);
            cw = Mathf.Min(cw, r.width);
            ch = Mathf.Min(ch, r.height);
            const int step = 4;
            int gw = r.width / step, gh = r.height / step;
            var g = new float[gw * gh];
            for (int gy = 0; gy < gh - 1; gy++)
                for (int gx = 0; gx < gw - 1; gx++)
                {
                    int x = r.x + gx * step, y = r.y + gy * step;
                    float L(int xx, int yy)
                    {
                        var c = px[yy * w + xx];
                        return (c.r + c.g + c.b) * c.a / 765f;
                    }
                    float l = L(x, y);
                    g[gy * gw + gx] = Mathf.Abs(l - L(x + step, y)) + Mathf.Abs(l - L(x, y + step));
                }
            int ww = cw / step, wh = ch / step, best = -1;
            float bestV = -1;
            var bestPos = new Vector2Int(0, 0);
            for (int gy = 0; gy + wh <= gh; gy += Mathf.Max(1, wh / 8))
                for (int gx = 0; gx + ww <= gw; gx += Mathf.Max(1, ww / 8))
                {
                    float sum = 0;
                    for (int y = 0; y < wh; y++)
                        for (int x = 0; x < ww; x++)
                            sum += g[(gy + y) * gw + gx + x];
                    if (sum > bestV)
                    {
                        bestV = sum;
                        bestPos = new Vector2Int(gx, gy);
                        best = 1;
                    }
                }
            if (best < 0) return new RectInt(r.x, r.y, cw, ch);
            return new RectInt(r.x + bestPos.x * step, r.y + bestPos.y * step, cw, ch);
        }

        static void Estimate(StringBuilder sb, string label, System.Func<string, bool> pathOk, System.Func<Texture2D, bool> texOk, TextureFormat fmt, int cap)
        {
            long now = 0, after = 0;
            int n = 0;
            foreach (var guid in AssetDatabase.FindAssets("t:Texture2D", new[] { "Assets/03 Art" }))
            {
                string p = AssetDatabase.GUIDToAssetPath(guid);
                if (!pathOk(p) || AtlasMenu.InAtlas(p)) continue;
                var t = AssetDatabase.LoadAssetAtPath<Texture2D>(p);
                if (!t || !texOk(t)) continue;
                int tw = t.width, th = t.height;
                if (cap > 0 && Mathf.Max(tw, th) > cap)
                {
                    float k = cap / (float)Mathf.Max(tw, th);
                    tw = Mathf.Max(1, Mathf.RoundToInt(tw * k));
                    th = Mathf.Max(1, Mathf.RoundToInt(th * k));
                }
                now += Storage(t);
                after += Bytes(fmt, tw, th);
                n++;
            }
            sb.AppendLine($"  {label}: {n} ảnh, {now / 1048576.0:0.0} MB → {after / 1048576.0:0.0} MB (bớt {(now - after) / 1048576.0:0.0} MB)");
        }

        static string Kb(long b) => $"{b / 1024.0:0} KB";

        static long Bytes(TextureFormat f, int w, int h)
        {
            int b = f == TextureFormat.ASTC_4x4 ? 4 : f == TextureFormat.ASTC_5x5 ? 5 : f == TextureFormat.ASTC_6x6 ? 6
                : f == TextureFormat.ASTC_8x8 ? 8 : f == TextureFormat.ASTC_10x10 ? 10 : f == TextureFormat.ASTC_12x12 ? 12 : 0;
            if (b > 0) return (long)((w + b - 1) / b) * ((h + b - 1) / b) * 16;
            if (f == TextureFormat.EAC_RG || f == TextureFormat.ETC2_RGBA8) return (long)((w + 3) / 4) * ((h + 3) / 4) * 16;
            if (f == TextureFormat.RG16) return (long)w * h * 2;
            return (long)w * h * 4;
        }

        static MethodInfo storage;

        // cỡ lưu thật của ảnh đã nhập ở nền đang chọn (như BuildSizeMenu)
        static long Storage(Texture2D t)
        {
            storage ??= typeof(Editor).Assembly.GetType("UnityEditor.TextureUtil")?.GetMethod("GetStorageMemorySizeLong", BindingFlags.Static | BindingFlags.Public);
            return storage != null ? (long)storage.Invoke(null, new object[] { t }) : UnityEngine.Profiling.Profiler.GetRuntimeMemorySizeLong(t);
        }
    }
}
