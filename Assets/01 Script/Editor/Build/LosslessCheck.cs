// Soát các cách bớt dung lượng "không đổi chất lượng hình" (người dùng 2026-11-21: "đừng để ảnh hưởng tới chất lượng hình ảnh game").
// Không đổi cách nhập ảnh nào, chỉ đo và ghi ảnh so vào Temp/PokiShots/:
//  - "Soát atlas hạt": từng ảnh hạt trong atlas Fx/hat.spriteatlasv2 dựng lại đúng như Image vẽ (phần cắt viền bù bằng
//    DataUtility.GetPadding, vùng ảnh lấy theo GetOuterUV như Image Simple) rồi so với ảnh gốc và với bản nén lẻ ASTC 6x6 như bản build
//    trước atlas. Hai bản cùng mức nén nên độ lệch so với ảnh gốc phải ngang nhau; lệch chỗ (bù cắt viền sai) thì sai số vọt lên.
//  - "Đo sai số _dist khi nén EAC RG": giải nén EAC thành số thực, so kênh khoảng cách (R, mỗi bậc 0,25 px ảnh gốc) và mặt nạ sóng
//    (G); mô phỏng lại công thức bọt sóng, mực của UIInkWater ở vài thời điểm, đo độ đổi màu nước.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using UnityEditor;
using UnityEngine;
using UnityEngine.Experimental.Rendering;
using UnityEngine.Sprites;
using UnityEngine.U2D;

namespace PokiClash.EditorTools
{
    public static class LosslessCheck
    {
        const string HatAtlasPath = "Assets/03 Art/Fx/hat.spriteatlasv2";

        // Lệnh qua file cho agent (2026-11-21: menu mới thêm không gọi được qua MCP khi cửa sổ Unity không được focus, Unity chưa dựng lại
        // thanh menu): ghi một tên lệnh trong danh sách dưới vào Library/PokiBuild/lenh.txt; Unity đọc trong khoảng 1 giây (không khi
        // đang biên dịch, nhập, build, Play), xoá file rồi chạy. Chỉ chạy các lệnh có tên ở đây.
        const string CommandFile = "Library/PokiBuild/lenh.txt";
        static readonly Dictionary<string, System.Action> Commands = new Dictionary<string, System.Action>
        {
            ["atlas_hat"] = AtlasMenu.BuildHat,
            ["soat_hat"] = CheckHat,
            ["dist_eac"] = CheckDist,
            ["build_android"] = () => PokiBuild.Run(PokiBuild.Kind.AndroidTest),
        };
        static double nextPoll;

        [InitializeOnLoadMethod]
        static void HookCommands() => EditorApplication.update += PollCommand;

        static void PollCommand()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || BuildPipeline.isBuildingPlayer
                || EditorApplication.isPlayingOrWillChangePlaymode || !File.Exists(CommandFile)) return;
            string cmd;
            try
            {
                cmd = File.ReadAllText(CommandFile).Trim();
                File.Delete(CommandFile);
            }
            catch (IOException)
            {
                return;
            }
            if (!Commands.TryGetValue(cmd, out var run))
            {
                Debug.LogWarning($"[Lệnh] Không có lệnh \"{cmd}\" ({string.Join(", ", Commands.Keys)})");
                return;
            }
            Debug.Log("[Lệnh] Chạy " + cmd);
            run();
        }

        struct Row
        {
            public string name;
            public double dbOld, dbNew, dbNewOld;
            public Color32[] src, old, nw;
            public int w, h;
        }

        [MenuItem("PokiClash/Build/Soát atlas hạt (so với ảnh lẻ, không đổi gì)", priority = 41)]
        static void CheckHat()
        {
            var atlas = AssetDatabase.LoadAssetAtPath<SpriteAtlas>(HatAtlasPath);
            if (!atlas)
            {
                Debug.LogError("[Soát] Chưa có " + HatAtlasPath + ": chạy PokiClash/Tối ưu/Sprite Atlas hạt hiệu ứng (dựng lại)");
                return;
            }
            var paths = AssetDatabase.FindAssets("t:Texture2D", new[] { AtlasMenu.HatDir }).Select(AssetDatabase.GUIDToAssetPath)
                .Where(AtlasMenu.InHatAtlas).OrderBy(p => p).ToList();
            var pages = new HashSet<Texture2D>();
            var pageFill = new Dictionary<Texture2D, long>();
            long rectArea = 0, packedArea = 0, oldBytes = 0;
            int trimmed = 0, fullBad = 0, missing = 0, compressedSrc = 0;
            var rows = new List<Row>();
            int step = Mathf.Max(1, paths.Count / 150);
            padMismatch = logged = 0;
            try
            {
                for (int i = 0; i < paths.Count; i++)
                {
                    string p = paths[i];
                    if (i % 20 == 0 && EditorUtility.DisplayCancelableProgressBar("Soát atlas hạt", p, i / (float)paths.Count)) break;
                    var src = AssetDatabase.LoadAssetAtPath<Sprite>(p);
                    if (!src) continue;
                    if (AssetImporter.GetAtPath(p) is TextureImporter ti && (ti.textureCompression != TextureImporterCompression.Uncompressed
                            || ti.GetPlatformTextureSettings("Android").overridden)) compressedSrc++;
                    var pk = atlas.GetSprite(src.name);
                    if (!pk)
                    {
                        missing++;
                        continue;
                    }
                    pages.Add(pk.texture);
                    pageFill.TryGetValue(pk.texture, out long pf);
                    pageFill[pk.texture] = pf + (long)(pk.textureRect.width * pk.textureRect.height);
                    int W = Mathf.RoundToInt(src.rect.width), H = Mathf.RoundToInt(src.rect.height);
                    oldBytes += (long)((W + 5) / 6) * ((H + 5) / 6) * 16;
                    var tr = pk.textureRect;
                    rectArea += (long)W * H;
                    packedArea += (long)(tr.width * tr.height);
                    bool trim = tr.width < W - 0.5f || tr.height < H - 0.5f;
                    if (trim) trimmed++;
                    if (trim && AtlasMenu.HatFullRect(p)) fullBad++;
                    if (i % step == 0 || AtlasMenu.HatFullRect(p) && i % 4 == 0) rows.Add(Compare(p, pk, W, H));
                    Object.DestroyImmediate(pk);
                }
            }
            finally
            {
                EditorUtility.ClearProgressBar();
            }
            long pageBytes = pages.Sum(t => (long)((t.width + 5) / 6) * ((t.height + 5) / 6) * 16);
            var sb = new StringBuilder();
            sb.AppendLine($"Atlas hạt: {paths.Count} ảnh, thiếu trong atlas {missing}, nguồn còn nén {compressedSrc} (phải 0: nguồn nén thì gói lại mờ)");
            sb.AppendLine($"Trang atlas: {pages.Count} ({string.Join(", ", pages.Select(t => $"{t.width}x{t.height} {t.format}"))})");
            sb.AppendLine("Độ đầy từng trang (phần hình, chưa tính lề): " +
                          string.Join(" ", pageFill.Select(kv => $"{100.0 * kv.Value / ((long)kv.Key.width * kv.Key.height):0}%")));
            sb.AppendLine($"Diện tích: khung ảnh {rectArea / 1e6:0.0} Mpx → phần giữ trong atlas {packedArea / 1e6:0.0} Mpx ({100.0 * packedArea / rectArea:0}%); " +
                          $"cắt viền {trimmed} ảnh; ảnh Filled bị cắt viền (phải 0): {fullBad}; chỗ Image đặt (padding) khác chỗ cắt (phải 0): {padMismatch}");
            sb.AppendLine($"Dung lượng ASTC 6x6: ảnh lẻ {oldBytes / 1048576.0:0.0} MB → atlas {pageBytes / 1048576.0:0.0} MB (bớt {(oldBytes - pageBytes) / 1048576.0:0.0} MB)");
            if (rows.Count > 0)
            {
                double mo = rows.Average(r => r.dbOld), mn = rows.Average(r => r.dbNew);
                var worse = rows.Where(r => r.dbNew < r.dbOld - 1).ToList();
                var geo = rows.Where(r => r.dbNew < 30).ToList();
                sb.AppendLine($"So {rows.Count} ảnh mẫu với ảnh gốc (PSNR trên nền xám, càng cao càng giống; trùng hẳn = 99):");
                sb.AppendLine($"  ảnh lẻ nén (bản build trước) trung bình {mo:0.0} dB, thấp nhất {rows.Min(r => r.dbOld):0.0}");
                sb.AppendLine($"  atlas (bản mới)                trung bình {mn:0.0} dB, thấp nhất {rows.Min(r => r.dbNew):0.0}");
                sb.AppendLine($"  atlas kém ảnh lẻ hơn 1 dB: {worse.Count} ảnh {string.Join(", ", worse.Take(10).Select(r => $"{r.name} {r.dbOld:0.0}→{r.dbNew:0.0}"))}");
                sb.AppendLine($"  nghi lệch chỗ (dưới 30 dB): {geo.Count} {string.Join(", ", geo.Take(10).Select(r => r.name))}");
                string shot = Sheet(rows);
                sb.AppendLine("Ảnh so (gốc | ảnh lẻ nén | atlas | chênh atlas − ảnh lẻ × 8): " + shot);
            }
            string dir = Path.Combine(PlayTour.ShotDir, "hat_atlas");
            Directory.CreateDirectory(dir);
            File.WriteAllText(Path.Combine(dir, "bao_cao.txt"), sb.ToString());
            Debug.Log("[Soát] " + sb);
        }

        static int padMismatch, logged;

        static Row Compare(string path, Sprite pk, int W, int H)
        {
            // ảnh gốc đọc thẳng từ file: trong Editor bật Sprite Atlas V2 thì sprite của file đã trỏ vào trang atlas
            var st = new Texture2D(2, 2, TextureFormat.RGBA32, false, false);
            st.LoadImage(File.ReadAllBytes(path));
            W = st.width;
            H = st.height;
            var s = st.GetPixels32();
            Object.DestroyImmediate(st);
            // bản build trước: ảnh lẻ nén ASTC 6x6 mức Normal (như cách nhập cũ)
            var t = new Texture2D(W, H, TextureFormat.RGBA32, false, false);
            t.SetPixels32(s);
            t.Apply(false);
            EditorUtility.CompressTexture(t, TextureFormat.ASTC_6x6, TextureCompressionQuality.Normal);
            t.Apply(false);
            var o = Read(t, W, H, false, Vector2.one, Vector2.zero);
            Object.DestroyImmediate(t);
            // bản mới: phần giữ lại trong trang atlas (textureRect) đặt về đúng chỗ trong khung (textureRectOffset); Image Simple đặt
            // theo DataUtility.GetPadding: hai số phải trùng (đếm padMismatch)
            var tex = pk.texture;
            var tr = pk.textureRect;
            var off = pk.textureRectOffset;
            var pad = DataUtility.GetPadding(pk);
            if (Mathf.Abs(pad.x - off.x) > 0.5f || Mathf.Abs(pad.y - off.y) > 0.5f
                || Mathf.Abs(W - pad.x - pad.z - tr.width) > 0.5f || Mathf.Abs(H - pad.y - pad.w - tr.height) > 0.5f) padMismatch++;
            if (logged++ < 3)
                Debug.Log($"[Soát] {pk.name}: khung {W}x{H}, trang {tex.name} {tex.width}x{tex.height}, textureRect {tr}, offset {off}, padding {pad}, " +
                          $"outerUV {DataUtility.GetOuterUV(pk)}");
            int px = Mathf.RoundToInt(off.x), py = Mathf.RoundToInt(off.y), rw = Mathf.RoundToInt(tr.width), rh = Mathf.RoundToInt(tr.height);
            var n = new Color32[W * H];
            if (rw > 0 && rh > 0)
            {
                var reg = Read(tex, rw, rh, false, new Vector2(tr.width / tex.width, tr.height / tex.height), new Vector2(tr.x / tex.width, tr.y / tex.height));
                for (int y = 0; y < rh && py + y < H; y++)
                    for (int x = 0; x < rw && px + x < W; x++)
                        n[(py + y) * W + px + x] = reg[y * rw + x];
            }
            return new Row { name = Path.GetFileNameWithoutExtension(path), src = s, old = o, nw = n, w = W, h = H, dbOld = Psnr(s, o), dbNew = Psnr(s, n), dbNewOld = Psnr(o, n) };
        }

        static Color32 OnGray(Color32 c)
        {
            int a = c.a;
            byte M(byte v) => (byte)((v * a + 150 * (255 - a)) / 255);
            return new Color32(M(c.r), M(c.g), M(c.b), 255);
        }

        static double Psnr(Color32[] a, Color32[] b)
        {
            double se = 0;
            for (int i = 0; i < a.Length; i++)
            {
                Color32 x = OnGray(a[i]), y = OnGray(b[i]);
                se += (x.r - y.r) * (x.r - y.r) + (x.g - y.g) * (x.g - y.g) + (x.b - y.b) * (x.b - y.b);
            }
            double mse = se / (3.0 * a.Length);
            return mse < 1e-9 ? 99 : 10 * System.Math.Log10(255.0 * 255.0 / mse);
        }

        // 10 ảnh: 6 ảnh atlas lệch ảnh lẻ nhiều nhất, 4 ảnh lớn nhất; mỗi hàng gốc | ảnh lẻ | atlas | chênh × 8, đúng cỡ, nền xám
        static string Sheet(List<Row> rows)
        {
            var pick = rows.OrderBy(r => r.dbNewOld).Take(6).Concat(rows.OrderByDescending(r => r.w * r.h).Take(4)).Distinct().ToList();
            const int gap = 8;
            int cw = pick.Max(r => r.w), W = 4 * cw + 3 * gap, H = pick.Sum(r => r.h) + gap * (pick.Count - 1);
            var canvas = Enumerable.Repeat(new Color32(255, 255, 255, 255), W * H).ToArray();
            int oy = H;
            foreach (var r in pick)
            {
                oy -= r.h;
                for (int y = 0; y < r.h; y++)
                    for (int x = 0; x < r.w; x++)
                    {
                        int i = y * r.w + x, o = (oy + y) * W;
                        canvas[o + x] = OnGray(r.src[i]);
                        canvas[o + cw + gap + x] = OnGray(r.old[i]);
                        canvas[o + 2 * (cw + gap) + x] = OnGray(r.nw[i]);
                        Color32 a = OnGray(r.old[i]), b = OnGray(r.nw[i]);
                        int d = Mathf.Min(255, 8 * Mathf.Max(Mathf.Abs(a.r - b.r), Mathf.Max(Mathf.Abs(a.g - b.g), Mathf.Abs(a.b - b.b))));
                        canvas[o + 3 * (cw + gap) + x] = new Color32((byte)d, (byte)d, (byte)d, 255);
                    }
                oy -= gap;
            }
            var tex = new Texture2D(W, H, TextureFormat.RGBA32, false);
            tex.SetPixels32(canvas);
            tex.Apply(false);
            string dir = Path.Combine(PlayTour.ShotDir, "hat_atlas");
            Directory.CreateDirectory(dir);
            string file = Path.Combine(dir, "so_atlas_hat.png");
            File.WriteAllBytes(file, tex.EncodeToPNG());
            Object.DestroyImmediate(tex);
            return file;
        }

        // vẽ (một vùng của) texture ra w x h bằng GPU (giải nén ASTC/EAC) rồi đọc về
        static Color32[] Read(Texture tex, int w, int h, bool linear, Vector2 scale, Vector2 offset)
        {
            var rt = RenderTexture.GetTemporary(w, h, 0, RenderTextureFormat.ARGB32, linear ? RenderTextureReadWrite.Linear : RenderTextureReadWrite.sRGB);
            var prev = RenderTexture.active;
            Graphics.Blit(tex, rt, scale, offset);
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

        // đọc về số thực (EAC giải ra 11 bit: đọc qua 8 bit thì lẫn sai số làm tròn của chính lúc đọc)
        static Color[] ReadF(Texture tex, int w, int h)
        {
            var rt = RenderTexture.GetTemporary(w, h, 0, RenderTextureFormat.ARGBFloat, RenderTextureReadWrite.Linear);
            var prev = RenderTexture.active;
            Graphics.Blit(tex, rt);
            RenderTexture.active = rt;
            var t = new Texture2D(w, h, TextureFormat.RGBAFloat, false, true);
            t.ReadPixels(new Rect(0, 0, w, h), 0, 0, false);
            t.Apply(false);
            RenderTexture.active = prev;
            RenderTexture.ReleaseTemporary(rt);
            var px = t.GetPixels();
            Object.DestroyImmediate(t);
            return px;
        }

        // ---------- _dist: EAC RG ----------
        [MenuItem("PokiClash/Build/Đo sai số ảnh khoảng cách dist khi nén EAC RG (không đổi gì)", priority = 42)]
        static void CheckDist()
        {
            var sb = new StringBuilder("Ảnh _dist RG16 → EAC RG (R: khoảng cách tới bờ, 1 bậc = 0,25 px ảnh gốc ≈ 0,8 điểm màn; G: mặt nạ sóng)\n");
            foreach (var f in Directory.GetFiles("Assets/03 Art/Baked/Islands", "land_*_dist.png"))
            {
                string path = f.Replace('\\', '/');
                string isl = Path.GetFileNameWithoutExtension(path).Substring(5).Replace("_dist", "");
                var mat = AssetDatabase.LoadAssetAtPath<Material>($"Assets/03 Art/Islands/land_water_{isl}.mat");
                var src = new Texture2D(2, 2, TextureFormat.RGBA32, false, true);
                src.LoadImage(File.ReadAllBytes(path));
                int w = src.width, h = src.height;
                var s32 = src.GetPixels32();
                foreach (var q in new[] { TextureCompressionQuality.Normal, TextureCompressionQuality.Best })
                {
                    var t = new Texture2D(w, h, TextureFormat.RGBA32, false, true);
                    t.SetPixels32(s32);
                    t.Apply(false);
                    EditorUtility.CompressTexture(t, TextureFormat.EAC_RG, q);
                    t.Apply(false);
                    var e = ReadF(t, w, h);
                    Object.DestroyImmediate(t);
                    sb.AppendLine($"{isl} {w}x{h} mức {q}: {Stats(s32, e, w, mat)}");
                }
                Object.DestroyImmediate(src);
            }
            string dir = Path.Combine(PlayTour.ShotDir, "nen_thu");
            Directory.CreateDirectory(dir);
            File.WriteAllText(Path.Combine(dir, "dist_eac.txt"), sb.ToString());
            Debug.Log("[Soát] " + sb);
        }

        static string Stats(Color32[] s, Color[] e, int w, Material mat)
        {
            float period = mat ? mat.GetFloat("_Period") : 22, speed = mat ? mat.GetFloat("_Speed") : 9;
            float reachMax = mat ? mat.GetFloat("_Reach") : 46, washK = mat ? mat.GetFloat("_Wash") : 14, foamK = mat ? mat.GetFloat("_Foam") : 0.92f;
            int water = 0, flips = 0, over1 = 0, over2 = 0;
            double sumErr = 0, maxErr = 0;
            int vis10 = 0, vis25 = 0, samples = 0;
            double maxVis = 0;
            float[] times = { 0f, 0.37f, 1.1f, 2.3f, 4.9f };
            for (int i = 0; i < s.Length; i++)
            {
                bool m0 = s[i].g > 127, m1 = e[i].g > 0.5f;
                if (m0 != m1) flips++;
                if (!m0) continue;
                water++;
                float r0 = s[i].r / 255f, r1 = e[i].r;
                double lv = System.Math.Abs(r1 - r0) * 255;
                sumErr += lv;
                if (lv > maxErr) maxErr = lv;
                if (lv > 1) over1++;
                if (lv > 2) over2++;
                if (!m1 || (i & 3) != 0) continue; // màu nước: mỗi 4 điểm một điểm cho nhanh
                var p = new Vector2(i % w + 0.5f, i / w + 0.5f);
                foreach (float t in times)
                {
                    Water(r0 * 64, p, t, period, speed, reachMax, washK, out float f0, out float k0);
                    Water(r1 * 64, p, t, period, speed, reachMax, washK, out float f1, out float k1);
                    double d = System.Math.Max(System.Math.Abs(f1 - f0) * foamK, System.Math.Abs(k1 - k0) * 0.45);
                    samples++;
                    if (d > 0.10) vis10++;
                    if (d > 0.25) vis25++;
                    if (d > maxVis) maxVis = d;
                }
            }
            return $"lệch R trung bình {sumErr / Mathf.Max(1, water):0.00} bậc, lớn nhất {maxErr:0.0} bậc, quá 1 bậc {100.0 * over1 / Mathf.Max(1, water):0.00}%, " +
                   $"quá 2 bậc {100.0 * over2 / Mathf.Max(1, water):0.000}%; mặt nạ đổi {flips} điểm; màu nước đổi quá 10% ở {100.0 * vis10 / Mathf.Max(1, samples):0.00}% " +
                   $"điểm, quá 25% ở {100.0 * vis25 / Mathf.Max(1, samples):0.000}%, lớn nhất {maxVis * 100:0}%";
        }

        // bọt sóng, mực của UIInkWater (cùng công thức, số của material đảo) tại khoảng cách d (px), điểm p (px ảnh gốc), giờ t
        static void Water(float d, Vector2 p, float t, float period, float speed, float reachMax, float washK, out float foam, out float ink)
        {
            float n = (Vn(p * 0.018f + new Vector2(t * 0.04f, 0)) - 0.5f) * 14f;
            float f = Frac((d + n + t * speed) / period);
            float line = Ss(0f, 0.04f, f) * (1 - Ss(0.11f, 0.19f, f));
            ink = Ss(0.19f, 0.22f, f) * (1 - Ss(0.22f, 0.28f, f));
            float fade = 1 - Ss(5f, reachMax, d);
            float br = (Vn(p * 0.006f) - 0.5f) * 0.6f;
            float wv = 0.5f + 0.5f * Mathf.Sin(t * 1.3f + Vn(p * 0.009f) * 6.283f);
            float reach = 3f + wv * (washK - 3f);
            float wash = 1 - Ss(reach - 1.5f, reach + 1.5f, d);
            float washEdge = 1 - Ss(1f, 3.2f, Mathf.Abs(d - reach));
            float hatch = 0.72f + 0.28f * (Frac((p.x + p.y) * 0.22f) >= 0.5f ? 1 : 0);
            foam = Mathf.Clamp01(Mathf.Max(line * fade * (0.9f + br), Mathf.Max(wash * 0.72f * hatch, washEdge)));
            ink *= fade;
        }

        static float Frac(float x) => x - Mathf.Floor(x);
        static float Ss(float a, float b, float x)
        {
            float k = Mathf.Clamp01((x - a) / (b - a));
            return k * k * (3 - 2 * k);
        }
        static float H21(Vector2 q) => Frac(Mathf.Sin(q.x * 127.1f + q.y * 311.7f) * 43758.5453f);
        static float Vn(Vector2 q)
        {
            float ix = Mathf.Floor(q.x), iy = Mathf.Floor(q.y), fx = q.x - ix, fy = q.y - iy;
            fx = fx * fx * (3 - 2 * fx);
            fy = fy * fy * (3 - 2 * fy);
            float a = H21(new Vector2(ix, iy)), b = H21(new Vector2(ix + 1, iy)), c = H21(new Vector2(ix, iy + 1)), d = H21(new Vector2(ix + 1, iy + 1));
            return Mathf.Lerp(Mathf.Lerp(a, b, fx), Mathf.Lerp(c, d, fx), fy);
        }
    }
}
