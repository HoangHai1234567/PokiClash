// Máy bi và thanh trên (2026-11-27, người dùng: "chưa thấy có max số bi người chơi có thể có 1 lúc, thanh fill giống trong clash of critters";
// "ô level để nhất quán 1 kiểu ô tròn level ở màn đảo chính thôi"). Menu "PokiClash/Prefab/Máy bi: thanh túi bi, ô cấp tròn" (chạy lại được):
// - Screens/Machine: "tui_bi" (vùng chữ đếm trong khung_dem, thu vào cho vừa lòng thanh) + "lap" (ảnh bo tròn, neo phải = bi / trần túi, đặt
//   lúc chạy) nằm trên khung_dem, dưới chữ đếm; gán MachineScene.p.bagFill / bagFillImg. Học thanh "10/30" dưới nút thả của Critters.
// - Screens/Machine: thanh kinh nghiệm to hơn (người dùng 2026-11-27: "bỏ nút ra đảo đi, làm thanh kinh nghiệm kia to lên"): rãnh khung_thanh
//   cao 55 → 82, rộng 585 → 600 (ảnh rãnh pk_ranh_exp chia 9 mảnh để viền không dày ra), thanh trong trải theo rãnh, chữ số to hơn;
// - App.prefab: chép ô cấp tròn của sảnh (Hud/vong_cap) vào thanh "Quay lai" (bọc "o_cap" trong hàng layout, đúng chỗ chip "Cấp N"), ẩn chip
//   cũ; gán TopBars backBadge / backArc / backLvNum. Máy bi ẩn ô này (đã có vòng cấp to trên thanh kinh nghiệm).
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class MachineBagBarMenu
    {
        const string MachinePath = "Assets/04 Prefabs/Screens/Machine.prefab";
        const string AppPath = "Assets/04 Prefabs/App/App.prefab";
        const float BadgeScale = 0.62f, BadgeW = 112;

        [MenuItem("PokiClash/Prefab/Máy bi: thanh túi bi, ô cấp tròn", priority = 67)]
        public static void Build()
        {
            if (!BakedArt.Current)
            {
                var g = AssetDatabase.FindAssets("t:BakedArt").FirstOrDefault();
                if (g != null) BakedArt.Current = AssetDatabase.LoadAssetAtPath<BakedArt>(AssetDatabase.GUIDToAssetPath(g));
            }
            if (!Theme.Kit)
            {
                var g = AssetDatabase.FindAssets("t:UiAssets").FirstOrDefault();
                if (g != null) Theme.Init(AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(g)));
            }
            bool a = BagBar(), b = BackBadge(), c = ExpBar();
            AssetDatabase.SaveAssets();
            Debug.Log($"[Máy bi] Thanh túi bi: {(a ? "xong" : "LỖI")}; ô cấp tròn thanh màn con: {(b ? "xong" : "LỖI")}; thanh kinh nghiệm: {(c ? "xong" : "LỖI")}.");
        }

        static bool BagBar()
        {
            var root = PrefabUtility.LoadPrefabContents(MachinePath);
            try
            {
                var scene = root.GetComponent<MachineScene>();
                var so = new SerializedObject(scene);
                var counter = so.FindProperty("p.counter").objectReferenceValue as TextMeshProUGUI;
                var parent = counter ? counter.transform.parent : null;
                var pill = parent ? parent.Find("khung_dem") : null;
                if (!counter || !pill)
                {
                    Debug.LogError("[Máy bi] Không thấy chữ đếm / khung_dem (chạy menu bố cục bản 2 trước).");
                    return false;
                }
                var old = parent.Find("tui_bi");
                if (old) Object.DestroyImmediate(old.gameObject);
                var holder = (RectTransform)new GameObject("tui_bi", typeof(RectTransform)).transform;
                holder.gameObject.layer = counter.gameObject.layer;
                holder.SetParent(parent, false);
                // lòng thanh: cả khung đếm thu vào InX hai bên, InY trên dưới (khung vẽ có viền vàng dày); chữ đếm trải cùng vùng cho số nằm giữa
                var kr = (RectTransform)pill;
                const float InX = 16, InY = 10;
                holder.anchorMin = kr.anchorMin;
                holder.anchorMax = kr.anchorMax;
                holder.pivot = kr.pivot;
                holder.sizeDelta = kr.sizeDelta - new Vector2(2 * InX, 2 * InY);
                holder.anchoredPosition = kr.anchoredPosition + new Vector2(InX * (1 - 2 * kr.pivot.x), -InY * (2 * kr.pivot.y - 1));
                var cr = counter.rectTransform;
                cr.anchorMin = holder.anchorMin;
                cr.anchorMax = holder.anchorMax;
                cr.pivot = holder.pivot;
                cr.sizeDelta = holder.sizeDelta;
                cr.anchoredPosition = holder.anchoredPosition;
                holder.SetSiblingIndex(counter.transform.GetSiblingIndex()); // trên khung, dưới chữ
                var fillGo = new GameObject("lap", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                fillGo.layer = counter.gameObject.layer;
                var fill = (RectTransform)fillGo.transform;
                fill.SetParent(holder, false);
                fill.anchorMin = Vector2.zero;
                fill.anchorMax = new Vector2(0.5f, 1);
                fill.pivot = new Vector2(0, 0.5f);
                fill.offsetMin = fill.offsetMax = Vector2.zero;
                var img = fillGo.GetComponent<Image>();
                Theme.SetSprite(img, Sketch.Pill);
                img.type = Image.Type.Sliced;
                img.color = Theme.Hex("#ff8fc0");
                img.raycastTarget = false;
                so.FindProperty("p.bagFill").objectReferenceValue = fill;
                so.FindProperty("p.bagFillImg").objectReferenceValue = img;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(root, MachinePath);
                return true;
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // ---------- chụp thử (đang Play): máy bi túi đầy / lưng chừng, màn Tướng (ô cấp tròn trên thanh màn con) → Temp/PokiShots/tui_bi/ ----------

        [MenuItem("PokiClash/Thử/Máy bi/thanh túi bi, ô cấp tròn (chụp)", priority = 121)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Máy bi] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(RunTour());
        }

        static IEnumerator RunTour()
        {
            var dir = Path.Combine(PlayTour.ShotDir, "tui_bi");
            if (Directory.Exists(dir)) Directory.Delete(dir, true);
            Directory.CreateDirectory(dir);
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            int n = 0;
            IEnumerator Shot(string name, float wait)
            {
                yield return new WaitForSecondsRealtime(wait);
                yield return new WaitForEndOfFrame();
                var tex = ScreenCapture.CaptureScreenshotAsTexture();
                File.WriteAllBytes(Path.Combine(dir, $"{n++:00}_{name}.jpg"), tex.EncodeToJPG(88));
                Object.Destroy(tex);
            }
            IEnumerator Go(string scene)
            {
                App.Modals.CloseAll();
                App.Router.Go(scene);
                yield return new WaitForSecondsRealtime(0.3f);
                for (float t = 0; (App.Router.Busy || App.Router.Current != scene) && t < 20; t += Time.unscaledDeltaTime) yield return null;
                App.Modals.CloseAll();
            }
            try
            {
                var s = App.Save.Data;
                int cap = BallBag.Cap(s, App.Data.Cfg, PokiClash.Game.SaveService.Now());
                yield return Go(SceneIds.Machine);
                foreach (var (balls, name) in new[] { (cap + 5, "may_bi_tui_day"), (cap * 2 / 5, "may_bi_lung_chung") })
                {
                    s.balls = balls;
                    App.Bars.Refresh();
                    App.Router.CurrentRoot?.Refresh();
                    yield return Shot(name, 1.0f);
                }
                yield return Go(SceneIds.Heroes);
                yield return Shot("man_tuong_o_cap", 1.0f);
                yield return Go(SceneIds.Hub);
                yield return Shot("sanh", 1.0f);
                Debug.Log("[Máy bi] Xong chụp thanh túi bi, ô cấp: " + dir);
            }
            finally
            {
                App.Modals.CloseAll();
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
        }

        const string RanhPath = "Assets/03 Art/Pachinko/pk_ranh_exp.png";
        static readonly Vector2 ExpSize = new Vector2(600, 82);
        const float ExpCenterX = 405.6f, ExpLabel = 38;

        static bool ExpBar()
        {
            // ảnh rãnh: viên thuốc 585 × 55, chia 9 mảnh theo bán kính đầu tròn để kéo cao không dày viền
            var ti = AssetImporter.GetAtPath(RanhPath) as TextureImporter;
            if (ti && ti.spriteBorder.sqrMagnitude < 1)
            {
                ti.spriteBorder = new Vector4(27, 27, 27, 27);
                ti.SaveAndReimport();
            }
            var root = PrefabUtility.LoadPrefabContents(MachinePath);
            try
            {
                var bar = root.GetComponentInChildren<MachineExpBar>(true);
                var khung = bar ? bar.transform.Find("khung_thanh") as RectTransform : null;
                var ranh = khung ? khung.Find("ranh")?.GetComponent<Image>() : null;
                var thanh = khung ? khung.Find("thanh_exp") as RectTransform : null;
                if (!khung || !ranh || !thanh)
                {
                    Debug.LogError("[Máy bi] Không thấy khung_thanh / ranh / thanh_exp của thanh kinh nghiệm.");
                    return false;
                }
                khung.sizeDelta = ExpSize;
                khung.anchoredPosition = new Vector2(ExpCenterX, khung.anchoredPosition.y);
                ranh.type = Image.Type.Sliced;
                // thanh trong lòng rãnh (cách viền 9 ngang, 8 dọc)
                thanh.anchorMin = Vector2.zero;
                thanh.anchorMax = Vector2.one;
                thanh.pivot = new Vector2(0, 0.5f);
                thanh.offsetMin = new Vector2(9, 8);
                thanh.offsetMax = new Vector2(-9, -8);
                var ui = thanh.GetComponent<UiBar>();
                var label = ui ? ui.Label : thanh.GetComponentInChildren<TextMeshProUGUI>(true);
                if (label)
                {
                    label.enableAutoSizing = true;
                    label.fontSizeMin = 18;
                    label.fontSizeMax = ExpLabel;
                    label.fontSize = ExpLabel;
                }
                PrefabUtility.SaveAsPrefabAsset(root, MachinePath);
                return true;
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // đường đi theo thứ tự con từ gốc tới t (hai chữ cùng tên "chu" trong vòng cấp nên không tra theo tên)
        static List<int> PathTo(Transform root, Transform t)
        {
            var path = new List<int>();
            for (; t && t != root; t = t.parent) path.Insert(0, t.GetSiblingIndex());
            return t == root ? path : null;
        }

        static Transform Follow(Transform root, List<int> path)
        {
            if (path == null) return null;
            var t = root;
            foreach (int i in path) t = t && i < t.childCount ? t.GetChild(i) : null;
            return t;
        }

        static bool BackBadge()
        {
            var app = PrefabUtility.LoadPrefabContents(AppPath);
            try
            {
                var top = app.GetComponentInChildren<TopBars>(true);
                var ring = top ? top.transform.Find("Hud/vong_cap") : null;
                var back = top ? top.transform.Find("Quay lai") : null;
                if (!ring || !back)
                {
                    Debug.LogError("[Thanh trên] Không thấy Hud/vong_cap hoặc Quay lai trong " + AppPath);
                    return false;
                }
                var so = new SerializedObject(top);
                var backLv = so.FindProperty("backLv").objectReferenceValue as TextMeshProUGUI;
                var lv = so.FindProperty("lvText").objectReferenceValue as TextMeshProUGUI;
                var arc = so.FindProperty("expArc").objectReferenceValue as Image;
                var chip = backLv ? backLv.transform.parent : null;
                if (!chip || chip.parent != back)
                {
                    Debug.LogError("[Thanh trên] Không thấy chip cấp của thanh Quay lai.");
                    return false;
                }
                var lvPath = lv ? PathTo(ring, lv.transform) : null;
                var arcPath = arc ? PathTo(ring, arc.transform) : null;

                var old = back.Find("o_cap");
                if (old) Object.DestroyImmediate(old.gameObject);
                var wrap = (RectTransform)new GameObject("o_cap", typeof(RectTransform), typeof(LayoutElement)).transform;
                wrap.gameObject.layer = chip.gameObject.layer;
                wrap.SetParent(back, false);
                wrap.SetSiblingIndex(chip.GetSiblingIndex());
                wrap.sizeDelta = new Vector2(BadgeW, 124);
                var le = wrap.GetComponent<LayoutElement>();
                le.preferredWidth = BadgeW;
                le.preferredHeight = 124;

                var badge = (RectTransform)Object.Instantiate(ring.gameObject, wrap).transform;
                badge.name = "vong_cap";
                foreach (var l in badge.GetComponents<LayoutElement>()) Object.DestroyImmediate(l);
                // tâm vòng tròn (ảnh "dia") về giữa ô
                var dia = badge.Find("dia") as RectTransform;
                float cy = dia ? dia.anchoredPosition.y : -34;
                badge.anchorMin = badge.anchorMax = badge.pivot = new Vector2(0.5f, 0.5f);
                badge.anchoredPosition = new Vector2(0, -cy * BadgeScale);
                badge.localScale = Vector3.one * BadgeScale;
                var num = Follow(badge, lvPath)?.GetComponent<TextMeshProUGUI>();
                var arcCopy = Follow(badge, arcPath)?.GetComponent<Image>();
                if (!num || !arcCopy) Debug.LogWarning("[Thanh trên] Ô cấp chép thiếu chữ số hoặc cung EXP");
                foreach (var g in badge.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
                chip.gameObject.SetActive(false);

                so.FindProperty("backBadge").objectReferenceValue = wrap.gameObject;
                so.FindProperty("backArc").objectReferenceValue = arcCopy;
                so.FindProperty("backLvNum").objectReferenceValue = num;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(app, AppPath);
                return true;
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(app);
            }
        }
    }
}
