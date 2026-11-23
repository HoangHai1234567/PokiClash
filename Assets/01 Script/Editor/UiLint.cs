// Soát giao diện tự động (đang Play, 2026-11-23; người dùng: "kiểm tra tất cả mọi màn / popup / panel... căn chỉnh text / button / UI còn lỗi
// không, icon nào bị lệch, không căn giữa, bị khuyết mất thì sửa hết"). Duyệt mọi Graphic đang hiện trên các canvas (màn đang mở, khung app,
// hộp thoại) và ghi các lỗi nghi ngờ:
// - TRAN: chữ TMP tràn khung (isTextOverflowing; chữ một dòng không co mà rộng hơn khung; chữ tự co đã co nhỏ nhất vẫn tràn);
// - NHO: cỡ chữ hiện trên màn (theo khung 1080) dưới 16 px;
// - LOI_KHUNG: chữ (khung chữ thật) lòi ra ngoài nền chứa nó (Image cha gần nhất) quá 6 px;
// - CHONG: hai chữ đang hiện chồng lên nhau quá 35 % diện tích chữ nhỏ hơn;
// - NGOAI_MAN: nút hoặc chữ lòi ra ngoài màn quá 4 px (trừ thứ nằm trong khung cuộn, bản đồ kéo);
// - MAT_HINH: ảnh tên icon / hinh / anh / chan_dung đang bật mà không có sprite (ô trắng);
// - LECH: icon trong nút chỉ có icon (không chữ) lệch tâm nút quá 12 % cỡ nút.
// Menu "PokiClash/Thử/Khác/Giao diện∕Soát UI: quét màn đang mở (đang Play)" ghi Temp/PokiShots/lint/<tên>.txt; tour UiFullAudit gọi Scan sau mỗi ảnh.
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class UiLint
    {
        public const float RefW = 1080, MinFont = 16, EdgeTol = 4, PanelTol = 8, OverlapK = 0.35f, CenterTol = 0.12f;
        static readonly string[] IconNames = { "icon", "hinh", "anh", "chan_dung", "body" };

        public static string Dir => Path.Combine(Application.dataPath, "..", "Temp", "PokiShots", "lint");

        [MenuItem("PokiClash/Thử/Khác/Giao diện∕Soát UI: quét màn đang mở (đang Play)", priority = 147)]
        static void ScanNow()
        {
            if (!EditorApplication.isPlaying)
            {
                Debug.LogWarning("[Soát UI] Bấm Play trước");
                return;
            }
            var list = Scan("thu_cong");
            Debug.Log($"[Soát UI] {list.Count} lỗi nghi ngờ, xem {Path.GetFullPath(Path.Combine(Dir, "thu_cong.txt"))}");
        }

        // quét, ghi báo cáo <name>.txt, trả danh sách dòng lỗi
        public static List<string> Scan(string name)
        {
            Directory.CreateDirectory(Dir);
            var issues = new List<string>();
            var canvases = Object.FindObjectsByType<Canvas>(FindObjectsSortMode.None).Where(c => c.isRootCanvas && c.isActiveAndEnabled).ToList();
            var texts = new List<(TextMeshProUGUI t, Rect r)>();
            foreach (var cv in canvases)
            {
                var cam = cv.renderMode == RenderMode.ScreenSpaceOverlay ? null : cv.worldCamera;
                float k = RefW / Mathf.Max(1, Screen.width); // điểm ảnh màn → px khung 1080
                foreach (var g in cv.GetComponentsInChildren<Graphic>(false))
                {
                    if (!Visible(g)) continue;
                    var sr = ScreenRect(g.rectTransform, cam);
                    if (g is TextMeshProUGUI t && !string.IsNullOrWhiteSpace(t.text))
                    {
                        var tr = TextScreenRect(t, cam, sr);
                        texts.Add((t, tr));
                        CheckText(t, sr, tr, cam, k, issues);
                    }
                    else if (g is Image img) CheckImage(img, sr, cam, issues);
                    if ((g is TextMeshProUGUI || g.GetComponent<SketchButton>()) && !Scrolled(g.transform))
                    {
                        var r = g is TextMeshProUGUI tt ? TextScreenRect(tt, cam, sr) : sr;
                        float o = Mathf.Max(0, -r.xMin, r.xMax - Screen.width, -r.yMin, r.yMax - Screen.height) * k;
                        if (o > EdgeTol) issues.Add($"NGOAI_MAN\t{NodePath(g.transform)}\tlòi {o:0} px{Txt(g)}");
                    }
                }
            }
            // chữ chồng chữ
            for (int i = 0; i < texts.Count; i++)
            for (int j = i + 1; j < texts.Count; j++)
            {
                var (a, ra) = texts[i];
                var (b, rb) = texts[j];
                if (a.transform.IsChildOf(b.transform) || b.transform.IsChildOf(a.transform)) continue;
                if (a.canvas && b.canvas && a.canvas.rootCanvas != b.canvas.rootCanvas) continue; // hộp thoại trên màn nền: không tính
                var inter = Intersect(ra, rb);
                if (inter <= 0) continue;
                float small = Mathf.Min(ra.width * ra.height, rb.width * rb.height);
                if (small > 1 && inter / small > OverlapK)
                    issues.Add($"CHONG\t{NodePath(a.transform)} ↔ {NodePath(b.transform)}\t\"{Short(a.text)}\" / \"{Short(b.text)}\"");
            }
            File.WriteAllText(Path.Combine(Dir, name + ".txt"), $"{name}: {issues.Count} lỗi nghi ngờ\n" + string.Join("\n", issues), Encoding.UTF8);
            return issues;
        }

        static void CheckText(TextMeshProUGUI t, Rect sr, Rect tr, Camera cam, float k, List<string> issues)
        {
            t.ForceMeshUpdate();
            var rt = t.rectTransform;
            var size = rt.rect.size;
            bool over = t.isTextOverflowing;
            if (!over && t.textWrappingMode == TextWrappingModes.NoWrap && !t.enableAutoSizing && t.preferredWidth > size.x + 4 &&
                t.overflowMode != TextOverflowModes.Overflow)
                over = true;
            if (t.enableAutoSizing && t.fontSize <= t.fontSizeMin + 0.01f && (t.preferredWidth > size.x + 2 || t.preferredHeight > size.y + 2))
                over = true;
            // chỉ báo tràn thấy được: rộng hơn khung, hay cao hơn hẳn (chữ Việt có dấu luôn "cao" hơn khung một dòng vài px)
            if (over && !(t.preferredWidth > size.x + 6 || t.preferredHeight > size.y + Mathf.Max(16, 0.4f * size.y))) over = false;
            if (over) issues.Add($"TRAN\t{NodePath(t.transform)}\tcỡ {t.fontSize:0} khung {size.x:0}x{size.y:0} cần {t.preferredWidth:0}x{t.preferredHeight:0}\t\"{Short(t.text)}\"");
            // cỡ chữ hiện trên màn
            float px = t.fontSize * (sr.height / Mathf.Max(1, size.y)) * k;
            if (size.y > 1 && px < MinFont) issues.Add($"NHO\t{NodePath(t.transform)}\t{px:0.#} px\t\"{Short(t.text)}\"");
            // lòi ra ngoài nền chứa nó
            var panel = ParentPanel(t.transform);
            if (panel && !Scrolled(t.transform))
            {
                var pr = ScreenRect(panel.rectTransform, cam);
                float o = Mathf.Max(0, pr.xMin - tr.xMin, tr.xMax - pr.xMax, pr.yMin - tr.yMin, tr.yMax - pr.yMax) * k;
                if (o > PanelTol) issues.Add($"LOI_KHUNG\t{NodePath(t.transform)}\tlòi {o:0} px khỏi {panel.name}\t\"{Short(t.text)}\"");
            }
        }

        static void CheckImage(Image img, Rect sr, Camera cam, List<string> issues)
        {
            string n = img.name.ToLowerInvariant();
            bool iconLike = IconNames.Any(x => n == x || n.StartsWith(x + "_") || n.EndsWith("_" + x));
            if (iconLike && !img.sprite && img.color.a > 0.05f)
                issues.Add($"MAT_HINH\t{NodePath(img.transform)}\tảnh bật mà không có sprite ({sr.width:0}x{sr.height:0})");
            // icon trong nút chỉ có icon: lệch tâm
            if (n != "icon" || !img.sprite) return;
            var parent = img.transform.parent as RectTransform;
            if (!parent || !parent.GetComponent<SketchButton>() && !parent.GetComponent<Button>()) return;
            if (parent.GetComponentsInChildren<TextMeshProUGUI>(false).Any(x => !string.IsNullOrWhiteSpace(x.text) && x.transform.parent == parent)) return;
            var pr = ScreenRect(parent, cam);
            var c = sr.center - pr.center;
            if (Mathf.Abs(c.x) > pr.width * CenterTol || Mathf.Abs(c.y) > pr.height * CenterTol)
                issues.Add($"LECH\t{NodePath(img.transform)}\tlệch ({c.x / pr.width:P0}, {c.y / pr.height:P0}) so với nút");
        }

        static bool Visible(Graphic g)
        {
            if (!g.enabled || !g.gameObject.activeInHierarchy) return false;
            if (g.color.a < 0.05f) return false;
            float a = 1;
            for (var t = g.transform; t; t = t.parent)
            {
                var cg = t.GetComponent<CanvasGroup>();
                if (cg) a *= cg.alpha;
            }
            if (a < 0.05f) return false;
            var s = g.transform.lossyScale;
            return Mathf.Abs(s.x) > 1e-4f && Mathf.Abs(s.y) > 1e-4f;
        }

        // nằm trong khung cuộn / bản đồ kéo / mặt nạ: lòi ra ngoài là bình thường
        static bool Scrolled(Transform t)
        {
            for (var p = t.parent; p; p = p.parent)
                if (p.GetComponent<ScrollRect>() || p.GetComponent<RectMask2D>() || p.GetComponent<Mask>() || p.GetComponent<LandView>())
                    return true;
            return false;
        }

        // nền chứa chữ: Image cha gần nhất (bỏ qua ảnh trong suốt, ảnh nhỏ hơn chữ nhiều lần thì vẫn tính)
        static Image ParentPanel(Transform t)
        {
            for (var p = t.parent; p; p = p.parent)
            {
                var img = p.GetComponent<Image>();
                if (img && img.enabled && img.color.a > 0.2f && img.sprite) return img;
                if (p.GetComponent<Canvas>()) return null;
            }
            return null;
        }

        static Rect ScreenRect(RectTransform rt, Camera cam)
        {
            var c = new Vector3[4];
            rt.GetWorldCorners(c);
            Vector2 a = RectTransformUtility.WorldToScreenPoint(cam, c[0]), b = RectTransformUtility.WorldToScreenPoint(cam, c[2]);
            return Rect.MinMaxRect(Mathf.Min(a.x, b.x), Mathf.Min(a.y, b.y), Mathf.Max(a.x, b.x), Mathf.Max(a.y, b.y));
        }

        // khung chữ thật (textBounds) trên màn; chữ rỗng thì khung RectTransform
        static Rect TextScreenRect(TextMeshProUGUI t, Camera cam, Rect fallback)
        {
            var b = t.textBounds;
            if (b.size.x <= 0 || b.size.y <= 0) return fallback;
            var rt = t.rectTransform;
            Vector2 a = RectTransformUtility.WorldToScreenPoint(cam, rt.TransformPoint(b.min)), c = RectTransformUtility.WorldToScreenPoint(cam, rt.TransformPoint(b.max));
            return Rect.MinMaxRect(Mathf.Min(a.x, c.x), Mathf.Min(a.y, c.y), Mathf.Max(a.x, c.x), Mathf.Max(a.y, c.y));
        }

        static float Intersect(Rect a, Rect b)
        {
            float w = Mathf.Min(a.xMax, b.xMax) - Mathf.Max(a.xMin, b.xMin), h = Mathf.Min(a.yMax, b.yMax) - Mathf.Max(a.yMin, b.yMin);
            return w > 0 && h > 0 ? w * h : 0;
        }

        static string NodePath(Transform t)
        {
            var parts = new List<string>();
            for (int i = 0; t && i < 5; i++, t = t.parent) parts.Add(t.name);
            parts.Reverse();
            return string.Join("/", parts);
        }

        static string Txt(Graphic g) => g is TextMeshProUGUI t ? $"\t\"{Short(t.text)}\"" : "";
        static string Short(string s) => (s ?? "").Replace("\n", " ⏎ ").Length > 50 ? s.Replace("\n", " ⏎ ").Substring(0, 50) + "…" : (s ?? "").Replace("\n", " ⏎ ");
    }
}
