// Lớp 1 (cách B) phía Editor. Hiện có: THU danh sách ảnh hero đích + mã hoá-thử TOÀN BỘ (không strip, không đổi asset) để xác nhận
// vòng tròn bóc-raw → gói → mã hoá → giải → dựng lại chạy đúng trên cả bộ ảnh thật, kèm format (biết có giữ ASTC không) và dung
// lượng. EncodeReadable dùng lại cho bước build strip (ArtEncryptStrip). Ảnh đích: *_atlas.png, *_portrait.png dưới Heroes/Resources
// (loaded bằng Resources.Load theo chuỗi qua PokiArt).
// Bật/tắt "readable" theo ĐỢT (SetReadable/RestoreReadable, gộp trong StartAssetEditing) thay vì toggle từng ảnh: 2 đợt nhập lại cho
// cả bộ thay vì 2×N lần (góp ý của assets-3e). Không dùng hộp thoại modal (treo Unity/MCP khi không có người bấm).
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Game;
using PokiClash.Security;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class ArtEncryptBuild
    {
        public const string HeroRes = "Assets/03 Art/Heroes/Resources";

        public struct Target
        {
            public string path;  // đường dẫn asset
            public string key;   // key Resources, không đuôi
            public bool sprite;  // chân dung = Sprite; atlas = Texture2D
        }

        public static List<Target> Collect()
        {
            var res = new List<Target>();
            foreach (var guid in AssetDatabase.FindAssets("t:Texture2D", new[] { HeroRes }))
            {
                string p = AssetDatabase.GUIDToAssetPath(guid);
                if (p.Contains("/enc/")) continue;
                string file = Path.GetFileNameWithoutExtension(p);
                bool atlas = file.EndsWith("_atlas");
                bool portrait = file.EndsWith("_portrait");
                if (!atlas && !portrait) continue;
                string key = p.Substring(HeroRes.Length + 1);
                key = key.Substring(0, key.Length - Path.GetExtension(key).Length);
                res.Add(new Target { path = p, key = key, sprite = portrait });
            }
            return res;
        }

        // Bật/tắt readable hàng loạt trong một đợt nhập lại. Trả về trạng thái cũ để khôi phục.
        public static Dictionary<string, bool> SetReadable(IEnumerable<Target> targets, bool on)
        {
            var prev = new Dictionary<string, bool>();
            try
            {
                AssetDatabase.StartAssetEditing();
                foreach (var t in targets)
                {
                    if (AssetImporter.GetAtPath(t.path) is TextureImporter imp)
                    {
                        prev[t.path] = imp.isReadable;
                        if (imp.isReadable != on) { imp.isReadable = on; imp.SaveAndReimport(); }
                    }
                }
            }
            finally { AssetDatabase.StopAssetEditing(); AssetDatabase.Refresh(); }
            return prev;
        }

        public static void RestoreReadable(Dictionary<string, bool> prev)
        {
            if (prev == null || prev.Count == 0) return;
            try
            {
                AssetDatabase.StartAssetEditing();
                foreach (var kv in prev)
                    if (AssetImporter.GetAtPath(kv.Key) is TextureImporter imp && imp.isReadable != kv.Value)
                    {
                        imp.isReadable = kv.Value; imp.SaveAndReimport();
                    }
            }
            finally { AssetDatabase.StopAssetEditing(); AssetDatabase.Refresh(); }
        }

        // Mã hoá một ảnh (GIẢ ĐỊNH đã readable — người gọi bật trước theo đợt). Trả null + err nếu không bóc được.
        public static byte[] EncodeReadable(Target t, out TexBlob meta, out int rawLen, out string err)
        {
            meta = null; rawLen = 0; err = null;
            var tex = AssetDatabase.LoadAssetAtPath<Texture2D>(t.path);
            if (!tex) { err = "không nạp được Texture2D"; return null; }
            byte[] raw;
            try { raw = tex.GetRawTextureData(); }
            catch (System.Exception e) { err = "GetRawTextureData lỗi (" + tex.format + "): " + e.Message; return null; }
            if (raw == null || raw.Length == 0) { err = "raw rỗng (chưa readable?)"; return null; }
            rawLen = raw.Length;
            var importer = AssetImporter.GetAtPath(t.path) as TextureImporter;
            bool linear = importer != null && !importer.sRGBTexture;
            var b = new TexBlob
            {
                kind = t.sprite ? TexBlob.KindSprite : TexBlob.KindTexture,
                format = (int)tex.format, width = tex.width, height = tex.height, mipCount = tex.mipmapCount,
                filterMode = (byte)tex.filterMode, wrapMode = (byte)tex.wrapMode, linear = (byte)(linear ? 1 : 0),
                raw = raw,
            };
            if (t.sprite)
            {
                var spr = AssetDatabase.LoadAssetAtPath<Sprite>(t.path);
                if (!spr) { err = "chân dung không nạp được dạng Sprite"; return null; }
                var r = spr.rect;
                b.rectX = r.x; b.rectY = r.y; b.rectW = r.width; b.rectH = r.height;
                b.pivotX = r.width > 0 ? spr.pivot.x / r.width : 0.5f;
                b.pivotY = r.height > 0 ? spr.pivot.y / r.height : 0.5f;
                b.ppu = spr.pixelsPerUnit;
                var bd = spr.border;
                b.borderL = bd.x; b.borderB = bd.y; b.borderR = bd.z; b.borderT = bd.w;
            }
            meta = b;
            return PokiCrypt.Encrypt(b.Pack(), "texture");
        }

        [MenuItem("PokiClash/Bảo mật/Thử mã hoá toàn bộ ảnh hero (không strip)", priority = 201)]
        public static void DryRunAll()
        {
            var targets = Collect();
            if (targets.Count == 0)
            {
                Debug.LogWarning("[Bảo mật] Không thấy ảnh đích (*_atlas, *_portrait) dưới " + HeroRes);
                return;
            }

            int ok = 0, fail = 0;
            long rawTotal = 0, encTotal = 0;
            var fmt = new Dictionary<string, int>();
            var fails = new List<string>();
            Dictionary<string, bool> prev = null;
            try
            {
                prev = SetReadable(targets, true); // một đợt nhập lại cho cả bộ
                for (int i = 0; i < targets.Count; i++)
                {
                    var t = targets[i];
                    if (EditorUtility.DisplayCancelableProgressBar("Thử mã hoá ảnh hero",
                            $"{i + 1}/{targets.Count}: {t.key}", (float)(i + 1) / targets.Count))
                        break;

                    byte[] enc = EncodeReadable(t, out var meta, out int rawLen, out string err);
                    if (enc == null) { fail++; fails.Add(t.key + " — " + err); continue; }

                    byte[] plain = PokiCrypt.TryDecrypt(enc, "texture");
                    var back = plain == null ? null : TexBlob.Unpack(plain);
                    bool rawEqual = back != null && back.raw.Length == meta.raw.Length
                                    && !back.raw.Where((x, k) => x != meta.raw[k]).Any();
                    Texture2D recon = null;
                    if (back != null) { try { recon = PokiArt.FromBlob(back, "recon"); } catch { } }
                    bool built = recon != null;          // chốt TRƯỚC khi huỷ (Unity coi object đã huỷ là null)
                    if (recon) Object.DestroyImmediate(recon);

                    if (rawEqual && built)
                    {
                        ok++;
                        rawTotal += rawLen; encTotal += enc.Length;
                        string f = ((TextureFormat)meta.format).ToString();
                        fmt[f] = fmt.TryGetValue(f, out var c) ? c + 1 : 1;
                    }
                    else { fail++; fails.Add(t.key + " — raw khớp=" + rawEqual + " dựng=" + built); }
                }
            }
            finally
            {
                EditorUtility.ClearProgressBar();
                RestoreReadable(prev);
            }

            string fmtStr = string.Join(", ", fmt.OrderByDescending(kv => kv.Value).Select(kv => $"{kv.Key}×{kv.Value}"));
            string report =
                $"[Bảo mật] Thử mã hoá ảnh hero: {ok} ĐẠT / {fail} LỖI / {targets.Count} tổng\n" +
                $"  format: {fmtStr}\n" +
                $"  dung lượng raw {rawTotal / 1024f / 1024f:0.0} MB -> blob mã hoá {encTotal / 1024f / 1024f:0.0} MB";
            if (fails.Count > 0) report += "\n  LỖI (tối đa 10):\n   - " + string.Join("\n   - ", fails.Take(10));
            if (fail == 0) Debug.Log(report + "\n  => ĐẠT TOÀN BỘ: an toàn để bật bước build strip.");
            else Debug.LogError(report);
        }
    }
}
