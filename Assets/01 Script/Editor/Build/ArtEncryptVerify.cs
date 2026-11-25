// Menu KIỂM mã hoá ảnh (Lớp 1, cách B) — chạy trong Unity để xác nhận vòng bóc-raw → gói → mã hoá → giải mã → dựng lại Texture2D
// cho RA ĐÚNG ảnh, TRƯỚC khi làm bước build strip ảnh gốc. Chọn một texture trong Project rồi menu PokiClash/Bảo mật/Kiểm mã hoá ảnh
// (không chọn thì tự lấy một atlas tướng). Báo: format, cỡ, raw có khớp từng byte sau vòng tròn không (khớp = ảnh dựng lại y hệt),
// và mở cửa sổ so ảnh gốc / ảnh dựng lại. Lưu ý: trên Editor Windows active target là Standalone nên format thường là DXT/RGBA, không
// phải ASTC của Android; vòng tròn đúng ở đây chứng minh cơ chế chạy. Việc bản Android bóc ra ASTC sẽ do bước build in format từng
// ảnh để xác nhận.
using System.IO;
using System.Linq;
using PokiClash.Game;
using PokiClash.Security;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class ArtEncryptVerify
    {
        [MenuItem("PokiClash/Bảo mật/Kiểm mã hoá ảnh", priority = 200)]
        public static void Verify()
        {
            var tex = Selection.activeObject as Texture2D;
            string path = tex ? AssetDatabase.GetAssetPath(tex) : DefaultAtlas();
            if (string.IsNullOrEmpty(path))
            {
                EditorUtility.DisplayDialog("Kiểm mã hoá ảnh", "Chọn một texture trong Project rồi chạy lại (không tìm thấy atlas tướng mặc định).", "OK");
                return;
            }

            var importer = AssetImporter.GetAtPath(path) as TextureImporter;
            bool wasReadable = importer != null && importer.isReadable;
            if (importer != null && !wasReadable)
            {
                importer.isReadable = true;
                importer.SaveAndReimport();
            }
            tex = AssetDatabase.LoadAssetAtPath<Texture2D>(path);
            if (!tex)
            {
                Debug.LogError("[Bảo mật] Không nạp được texture: " + path);
                return;
            }

            byte[] raw;
            try { raw = tex.GetRawTextureData(); }
            catch (System.Exception e)
            {
                Debug.LogError("[Bảo mật] GetRawTextureData lỗi (" + tex.format + "): " + e.Message);
                if (importer != null && !wasReadable) { importer.isReadable = false; importer.SaveAndReimport(); }
                return;
            }

            bool linear = importer != null && !importer.sRGBTexture;
            var blob = new TexBlob
            {
                kind = TexBlob.KindTexture,
                format = (int)tex.format,
                width = tex.width,
                height = tex.height,
                mipCount = tex.mipmapCount,
                filterMode = (byte)tex.filterMode,
                wrapMode = (byte)tex.wrapMode,
                linear = (byte)(linear ? 1 : 0),
                raw = raw,
            };

            // vòng tròn thật: Pack -> mã hoá -> giải mã -> Unpack -> dựng Texture2D
            byte[] enc = PokiCrypt.Encrypt(blob.Pack(), "texture");
            byte[] plain = PokiCrypt.TryDecrypt(enc, "texture");
            var back = plain == null ? null : TexBlob.Unpack(plain);
            bool ok = back != null;
            bool rawEqual = ok && back.raw.Length == raw.Length && !back.raw.Where((t, i) => t != raw[i]).Any();

            Texture2D recon = null;
            if (ok)
            {
                try { recon = PokiArt.FromBlob(back, tex.name + "_recon"); }
                catch (System.Exception e) { Debug.LogError("[Bảo mật] Dựng lại Texture2D lỗi: " + e.Message); }
            }

            float overhead = raw.Length > 0 ? 100f * (enc.Length - raw.Length) / raw.Length : 0;
            string report =
                $"[Bảo mật] Kiểm mã hoá ảnh: {Path.GetFileName(path)}\n" +
                $"  format={tex.format}  cỡ={tex.width}x{tex.height}  mip={tex.mipmapCount}  linear={linear}\n" +
                $"  raw={raw.Length:n0}B  blob mã hoá={enc.Length:n0}B  (+{overhead:0.0}% overhead)\n" +
                $"  giải mã OK={ok}  raw khớp từng byte={rawEqual}  dựng lại Texture2D={(recon ? "OK" : "LỖI")}";
            if (rawEqual && recon) Debug.Log(report + "\n  => ĐẠT: ảnh dựng lại y hệt ảnh gốc.");
            else Debug.LogError(report + "\n  => CHƯA ĐẠT: xem lại (format lạ? GetRawTextureData trả khác?).");

            if (importer != null && !wasReadable) { importer.isReadable = false; importer.SaveAndReimport(); }

            if (recon)
                ArtVerifyWindow.Show(AssetDatabase.LoadAssetAtPath<Texture2D>(path), recon, report, rawEqual);
        }

        static string DefaultAtlas()
        {
            var g = AssetDatabase.FindAssets("t:Texture2D _atlas", new[] { "Assets/03 Art/Heroes/Resources" });
            foreach (var id in g)
            {
                var p = AssetDatabase.GUIDToAssetPath(id);
                if (p.EndsWith("_atlas.png") || p.Contains("_atlas")) return p;
            }
            return null;
        }
    }

    // Cửa sổ so ảnh gốc / ảnh dựng lại bằng mắt.
    public sealed class ArtVerifyWindow : EditorWindow
    {
        Texture2D a, b;
        string report;
        bool ok;

        public static void Show(Texture2D orig, Texture2D recon, string report, bool ok)
        {
            var w = GetWindow<ArtVerifyWindow>(true, "Kiểm mã hoá ảnh");
            w.a = orig; w.b = recon; w.report = report; w.ok = ok;
            w.minSize = new Vector2(680, 420);
            w.Show();
        }

        void OnGUI()
        {
            EditorGUILayout.HelpBox(ok ? "ĐẠT: ảnh dựng lại y hệt ảnh gốc." : "CHƯA ĐẠT: so bằng mắt xem có méo/sai màu không.",
                ok ? MessageType.Info : MessageType.Warning);
            EditorGUILayout.LabelField(report, EditorStyles.wordWrappedMiniLabel, GUILayout.Height(60));
            var r = GUILayoutUtility.GetRect(position.width, position.height - 100);
            float w = (r.width - 20) / 2;
            var ra = new Rect(r.x, r.y, w, r.height);
            var rb = new Rect(r.x + w + 20, r.y, w, r.height);
            GUI.Label(new Rect(ra.x, ra.y, w, 16), "Gốc");
            GUI.Label(new Rect(rb.x, rb.y, w, 16), "Dựng lại từ blob mã hoá");
            if (a) EditorGUI.DrawPreviewTexture(new Rect(ra.x, ra.y + 18, w, r.height - 18), a);
            if (b) EditorGUI.DrawPreviewTexture(new Rect(rb.x, rb.y + 18, w, r.height - 18), b);
        }
    }
}
