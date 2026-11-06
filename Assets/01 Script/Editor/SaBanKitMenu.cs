// Bộ UI Sa Bàn vào Unity (GD_Claude/17_BoUI.md; bản web Web/uikit.html). Menu "PokiClash/Prefab/Bộ UI Sa Bàn: hiệu ứng, nút sticker,
// chỉ khâu" (chạy lại được, không nhân đôi):
// - Kit/NetBung: nét bung khi nhả nút (InkBurst, 5 gạch mực), gán UiKit.burst;
// - nút tròn (Kit/Nut_Tron) thành sticker: nền giấy viền mực làm viền trắng, thêm lõi màu "loi" (SketchButton.SetCore);
// - khung giấy lớn trong mọi prefab (ảnh sk_Panel từ 260 × 160, sk_PanelThin từ 300 × 200) thêm đường chỉ khâu "chi_khau" bên trong;
// - nút chính thở (UiMotion.breath): Lên cấp, Giới thiệu, Huyền thoại, Rương đảo, Chọn tướng khởi đầu, Đánh (đảo),
//   Máy Bi (sảnh); chấm đỏ thở nhanh (hàng nút sảnh, thẻ tướng, nút AFK);
// - bảng tên vùng ở sảnh nhún tại chỗ;
// - thông báo (Dialogs/ThongBao) thành giấy nhớ vàng có băng keo hồng.
// Xuất trận (hộp chuẩn bị) thở theo code khi bấm được; ô tướng và thẻ chia bài nhún theo code (HeroesScene, BattleView).
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class SaBanKitMenu
    {
        const string Prefabs = "Assets/04 Prefabs";
        const string BurstPath = Prefabs + "/Kit/NetBung.prefab";
        const string RoundPath = Prefabs + "/Kit/Nut_Tron.prefab";
        const string StitchPath = "Assets/03 Art/Kit/ui_chi_khau.png";
        static readonly Color StitchColor = new Color(0.17f, 0.13f, 0.09f, 0.3f);
        const float InsetPanel = 16, InsetThin = 12; // viền mực Unity dày hơn web: chỉ khâu cách viền rõ
        static readonly Color StickyYellow = new Color(1f, 0.914f, 0.541f, 1f);
        static readonly Color TapePink = new Color(1f, 0.77f, 0.84f, 0.94f);
        static readonly Vector2 C = new Vector2(0.5f, 0.5f);

        [MenuItem("PokiClash/Prefab/Bộ UI Sa Bàn: hiệu ứng, nút sticker, chỉ khâu", priority = 70)]
        static void Build()
        {
            var assets = Load<UiAssets>();
            Theme.Init(assets);
            var kit = assets.prefabs;
            BuildBurst(kit);
            StickerRound();
            var stitch = StitchSprite();
            int stitched = AddStitches(stitch);
            Unstitch(Prefabs + "/Items/TranVsMat.prefab");
            stitched += Uncover(stitch);
            int breaths = Breaths();
            int zones = HubZonesIdle();
            StickyToast();
            AssetDatabase.SaveAssets();
            Debug.Log($"[Bộ UI] Nét bung, nút tròn sticker, {stitched} khung có chỉ khâu, {breaths} nút/chấm thở, {zones} bảng tên vùng nhún, giấy nhớ.");
        }

        // ---------- nét bung ----------

        static void BuildBurst(UiKit kit)
        {
            var root = new GameObject("NetBung", typeof(RectTransform), typeof(CanvasGroup), typeof(InkBurst));
            try
            {
                var rt = (RectTransform)root.transform;
                rt.sizeDelta = new Vector2(140, 140);
                var cg = root.GetComponent<CanvasGroup>();
                cg.interactable = false;
                cg.blocksRaycasts = false;
                root.GetComponent<InkBurst>().Setup(cg);
                for (int i = 0; i < 5; i++)
                {
                    float a = i * Mathf.PI * 2 / 5;
                    var dir = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                    var go = new GameObject("gach_" + i, typeof(RectTransform), typeof(InkPath));
                    go.transform.SetParent(rt, false);
                    ((RectTransform)go.transform).Place(C, Vector2.zero, Vector2.zero);
                    var ink = go.GetComponent<InkPath>();
                    ink.Setup(new[] { dir * 40, dir * 68 }, 7);
                    ink.color = Theme.Ink;
                    ink.raycastTarget = false;
                }
                PrefabUtility.SaveAsPrefabAsset(root, BurstPath);
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
            kit.burst = AssetDatabase.LoadAssetAtPath<InkBurst>(BurstPath);
            EditorUtility.SetDirty(kit);
        }

        // ---------- nút tròn sticker ----------

        static void StickerRound()
        {
            var root = PrefabUtility.LoadPrefabContents(RoundPath);
            try
            {
                var btn = root.GetComponent<SketchButton>();
                var t = root.transform.Find("loi");
                Image core;
                if (t) core = t.GetComponent<Image>();
                else
                {
                    var go = new GameObject("loi", typeof(RectTransform), typeof(Image), typeof(LayoutElement));
                    go.transform.SetParent(root.transform, false);
                    go.GetComponent<LayoutElement>().ignoreLayout = true;
                    core = go.GetComponent<Image>();
                }
                core.transform.SetAsFirstSibling();
                var crt = (RectTransform)core.transform;
                crt.anchorMin = new Vector2(0.13f, 0.13f);
                crt.anchorMax = new Vector2(0.87f, 0.87f);
                crt.offsetMin = crt.offsetMax = Vector2.zero;
                Theme.SetSprite(core, Sketch.Round);
                core.type = Image.Type.Simple;
                core.preserveAspect = true;
                core.raycastTarget = false;
                btn.SetCore(core);
                PrefabUtility.SaveAsPrefabAsset(root, RoundPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // ---------- chỉ khâu ----------

        static Sprite StitchSprite()
        {
            var ti = AssetImporter.GetAtPath(StitchPath) as TextureImporter;
            if (!ti) return null;
            var border = new Vector4(32, 32, 32, 32);
            if (ti.spriteBorder != border)
            {
                ti.spriteBorder = border;
                ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Sprite>(StitchPath);
        }

        static int AddStitches(Sprite stitch)
        {
            if (!stitch) return 0;
            var panel = Sketch.Panel;
            var thin = Sketch.PanelThin;
            int count = 0;
            foreach (var path in AllPrefabs())
            {
                if (path == BurstPath || path.EndsWith("/BootTitle.prefab") || path.EndsWith("/TranVsMat.prefab")) continue;
                bool kitPanel = path.EndsWith("/Kit/Khung.prefab"); // khung gốc của kit: gắn luôn, bản lồng ở mọi nơi có theo
                var root = PrefabUtility.LoadPrefabContents(path);
                bool changed = false;
                try
                {
                    foreach (var img in root.GetComponentsInChildren<Image>(true))
                    {
                        bool isPanel = img.sprite == panel, isThin = img.sprite == thin;
                        if (!isPanel && !isThin) continue;
                        if (img.type != Image.Type.Sliced) continue;
                        // khung nằm trong prefab lồng khác: để prefab gốc của nó lo
                        var inst = PrefabUtility.GetNearestPrefabInstanceRoot(img.gameObject);
                        if (inst && inst != root) continue;
                        var size = ((RectTransform)img.transform).rect.size;
                        if (!kitPanel && (isPanel ? size.x < 260 || size.y < 160 : size.x < 300 || size.y < 200)) continue;
                        var old = img.transform.Find("chi_khau");
                        GameObject go;
                        if (old) go = old.gameObject;
                        else
                        {
                            go = new GameObject("chi_khau", typeof(RectTransform), typeof(Image), typeof(LayoutElement));
                            go.transform.SetParent(img.transform, false);
                            go.transform.SetAsFirstSibling();
                            go.GetComponent<LayoutElement>().ignoreLayout = true;
                        }
                        float inset = isPanel ? InsetPanel : InsetThin;
                        ((RectTransform)go.transform).Stretch(inset, inset, inset, inset);
                        var s = go.GetComponent<Image>();
                        Theme.SetSprite(s, stitch);
                        s.type = Image.Type.Tiled;
                        s.fillCenter = false;
                        s.color = StitchColor;
                        s.raycastTarget = false;
                        changed = true;
                        count++;
                    }
                    if (changed) PrefabUtility.SaveAsPrefabAsset(root, path);
                }
                finally
                {
                    PrefabUtility.UnloadPrefabContents(root);
                }
            }
            return count;
        }

        // ---------- nút chính thở, chấm đỏ ----------

        // (prefab, kiểu component, đường dẫn trường, chấm đỏ?)
        static readonly (string type, string field, bool dot)[] DialogBreaths =
        {
            ("LevelUpDialog", "ok", false), ("IntroDialog", "start", false), ("LegendMilestoneDialog", "ok", false),
            ("ZoneChestDialog", "ok", false), ("StarterDialog", "pick", false),
        };

        static int Breaths()
        {
            int n = 0;
            foreach (var path in AllPrefabs().Where(p => p.Contains("/Dialogs/")))
                n += Mark(path, DialogBreaths);
            // Máy bi: nút thả bi, thả liền, nút cược đang được pokiwar-9a vẽ lại (2026-11-06): không gắn
            n += Mark(Prefabs + "/Screens/Zone.prefab", "ZoneScene", "p.fight", false);
            n += Mark(Prefabs + "/Screens/Hub.prefab", "HubScene", "bottom.Array.data[2].button", false);
            for (int i = 0; i < 5; i++) n += Mark(Prefabs + "/Screens/Hub.prefab", "HubScene", $"bottom.Array.data[{i}].badge", true);
            n += Mark(Prefabs + "/App/App.prefab", "TopBars", "afkDot", true);
            // chấm đỏ trên thẻ tướng (Items/TheTuong)
            var tt = Prefabs + "/Items/TheTuong.prefab";
            if (File.Exists(tt))
            {
                var root = PrefabUtility.LoadPrefabContents(tt);
                try
                {
                    var dot = root.GetComponentsInChildren<Transform>(true).FirstOrDefault(x => x.name == "cham_do");
                    if (dot)
                    {
                        SetBreath(dot.gameObject, true);
                        PrefabUtility.SaveAsPrefabAsset(root, tt);
                        n++;
                    }
                }
                finally
                {
                    PrefabUtility.UnloadPrefabContents(root);
                }
            }
            return n;
        }

        static int Mark(string path, string type, string field, bool dot) => Mark(path, new[] { (type, field, dot) });

        // gắn thở cho đối tượng mà trường field của component type trong prefab path trỏ tới (mở prefab một lần cho cả danh sách)
        static int Mark(string path, (string type, string field, bool dot)[] list)
        {
            if (!File.Exists(path)) return 0;
            var root = PrefabUtility.LoadPrefabContents(path);
            int n = 0;
            try
            {
                foreach (var comp in root.GetComponentsInChildren<MonoBehaviour>(true))
                {
                    if (!comp) continue;
                    foreach (var (type, field, dot) in list)
                    {
                        if (comp.GetType().Name != type) continue;
                        var prop = new SerializedObject(comp).FindProperty(field);
                        if (prop == null || prop.propertyType != SerializedPropertyType.ObjectReference) continue;
                        var obj = prop.objectReferenceValue;
                        var go = obj is Component c ? c.gameObject : obj as GameObject;
                        if (!go) continue;
                        SetBreath(go, dot);
                        n++;
                    }
                }
                if (n > 0) PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            return n;
        }

        static void SetBreath(GameObject go, bool dot)
        {
            var m = go.GetComponent<UiMotion>() ?? go.AddComponent<UiMotion>();
            m.breath = true;
            m.breathAmount = dot ? 0.16f : 0.045f;
            m.breathPeriod = dot ? 1.6f : 2.2f;
        }

        // ---------- bảng tên vùng ở sảnh nhún ----------

        static int HubZonesIdle()
        {
            var path = Prefabs + "/Screens/Hub.prefab";
            var root = PrefabUtility.LoadPrefabContents(path);
            int n = 0;
            try
            {
                foreach (var z in root.GetComponentsInChildren<HubZone>(true))
                {
                    var prop = new SerializedObject(z).FindProperty("p.plaque");
                    var img = prop?.objectReferenceValue as Image;
                    if (!img) continue;
                    var m = img.GetComponent<UiMotion>() ?? img.gameObject.AddComponent<UiMotion>();
                    m.idle = true;
                    m.idleLift = 6;
                    m.idleTilt = 0.5f;
                    m.idlePeriod = 3.6f;
                    n++;
                }
                if (n > 0) PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            return n;
        }

        // ---------- giấy nhớ ----------

        static void StickyToast()
        {
            var path = Prefabs + "/Dialogs/ThongBao.prefab";
            if (!File.Exists(path)) return;
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                var bg = root.GetComponent<Image>();
                if (bg) bg.color = StickyYellow;
                var t = root.transform.Find("bang_keo");
                if (!t)
                {
                    var go = new GameObject("bang_keo", typeof(RectTransform), typeof(Image), typeof(LayoutElement));
                    go.transform.SetParent(root.transform, false);
                    go.GetComponent<LayoutElement>().ignoreLayout = true;
                    t = go.transform;
                }
                var rt = (RectTransform)t;
                rt.Place(new Vector2(0.5f, 1), new Vector2(0, 6), new Vector2(130, 36));
                rt.localEulerAngles = new Vector3(0, 0, -3);
                var img = t.GetComponent<Image>();
                Theme.SetSprite(img, Sketch.Tape);
                img.color = TapePink;
                img.raycastTarget = false;
                PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // ---------- tiện ích ----------

        // chỉ khâu bị lớp lưới kẻ ô phủ kín (tờ giấy hộp thoại: to_giay/luoi): đặt bản mới làm con của lớp lưới (vẽ ngay trên lưới,
        // dưới nội dung), tắt bản bị che (bản từ prefab Khung lồng bên trong thì chỉ tắt được)
        static readonly string[] Covers = { "luoi", "o_ke", "giay", "ke" };

        static int Uncover(Sprite stitch)
        {
            if (!stitch) return 0;
            int n = 0;
            foreach (var path in AllPrefabs())
            {
                var root = PrefabUtility.LoadPrefabContents(path);
                bool changed = false;
                try
                {
                    foreach (var st in root.GetComponentsInChildren<Transform>(true).Where(t => t.name == "chi_khau").ToList())
                    {
                        var parent = st.parent;
                        if (!parent || Covers.Contains(parent.name)) continue;
                        RectTransform cover = null;
                        for (int i = st.GetSiblingIndex() + 1; i < parent.childCount; i++)
                        {
                            var c = parent.GetChild(i) as RectTransform;
                            if (c && Covers.Contains(c.name) && c.GetComponent<Image>() && c.anchorMin == Vector2.zero && c.anchorMax == Vector2.one)
                            {
                                cover = c;
                                break;
                            }
                        }
                        if (!cover) continue;
                        if (st.gameObject.activeSelf)
                        {
                            st.gameObject.SetActive(false);
                            changed = true;
                        }
                        var src = st.GetComponent<Image>();
                        var srt = (RectTransform)st;
                        var existing = cover.Find("chi_khau");
                        GameObject go;
                        if (existing) go = existing.gameObject;
                        else
                        {
                            go = new GameObject("chi_khau", typeof(RectTransform), typeof(Image), typeof(LayoutElement));
                            go.transform.SetParent(cover, false);
                            go.GetComponent<LayoutElement>().ignoreLayout = true;
                        }
                        var rt = (RectTransform)go.transform;
                        // cùng chỗ với bản cũ (so với khung cha), đổi sang toạ độ của lớp lưới
                        rt.anchorMin = Vector2.zero;
                        rt.anchorMax = Vector2.one;
                        rt.offsetMin = srt.offsetMin - cover.offsetMin;
                        rt.offsetMax = srt.offsetMax - cover.offsetMax;
                        var img = go.GetComponent<Image>();
                        Theme.SetSprite(img, stitch);
                        img.type = Image.Type.Tiled;
                        img.fillCenter = false;
                        img.color = StitchColor;
                        img.raycastTarget = false;
                        changed = true;
                        n++;
                    }
                    // biến thể chạy trước tờ giấy gốc (thứ tự tên) từng tự thêm một bản: chỉ giữ một bản dưới mỗi lớp lưới,
                    // ưu tiên bản kế thừa từ prefab gốc
                    foreach (var cover in root.GetComponentsInChildren<Transform>(true).Where(t => Covers.Contains(t.name)).ToList())
                    {
                        var dups = cover.Cast<Transform>().Where(t => t.name == "chi_khau").ToList();
                        if (dups.Count < 2) continue;
                        bool Own(Transform t) => !PrefabUtility.IsPartOfPrefabInstance(t.gameObject) || PrefabUtility.IsAddedGameObjectOverride(t.gameObject);
                        var keep = dups.FirstOrDefault(t => !Own(t)) ?? dups[0];
                        foreach (var t in dups)
                            if (t != keep && Own(t))
                            {
                                Object.DestroyImmediate(t.gameObject);
                                changed = true;
                            }
                    }
                    if (changed) PrefabUtility.SaveAsPrefabAsset(root, path);
                }
                finally
                {
                    PrefabUtility.UnloadPrefabContents(root);
                }
            }
            return n;
        }

        // khung truyện tranh màn VS: không khâu (đã gắn ở lần chạy trước thì gỡ)
        static void Unstitch(string path)
        {
            if (!File.Exists(path)) return;
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                var all = root.GetComponentsInChildren<Transform>(true).Where(t => t.name == "chi_khau").ToList();
                foreach (var t in all) Object.DestroyImmediate(t.gameObject);
                if (all.Count > 0) PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static IEnumerable<string> AllPrefabs() =>
            AssetDatabase.FindAssets("t:Prefab", new[] { Prefabs }).Select(AssetDatabase.GUIDToAssetPath).Where(p => !p.Contains("/Heroes/")).OrderBy(p => p);

        static T Load<T>() where T : Object =>
            AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:" + typeof(T).Name)[0]));
    }
}
