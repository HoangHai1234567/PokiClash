// Dựng prefab đoạn cốt truyện mở đầu (App/StoryIntro.cs, GD_Claude/25_FTUE.md mục 11): Assets/04 Prefabs/Screens/CotTruyen.prefab,
// gán App.storyPrefab trong App.prefab. Trang truyện tranh tràn màn hình (người dùng 2026-11-23): nền mực, hai trang giấy phủ kín màn,
// mỗi trang 3 ô tranh tứ giác vách xiên (ComicPanel), viền mực (InkPath), khung lời dẫn vàng nhạt viền mực ở góc ô. Hình ô, viền, chỗ
// khung lời dẫn do StoryIntro.Layout tính lúc chạy theo cỡ màn; prefab chỉ giữ các vật.
// Tranh lấy ở Assets/03 Art/Story/khung_1..6.png (gói GPT ArtGen/Story/build_story.py --nhap; cách nhập do ArtPostprocessor); ô nào chưa có tranh thì gắn tạm
// một nền trận / bản đồ có sẵn. Có tranh mới thì chạy lại menu.
// Dòng "Cốt truyện mở đầu" ở Sổ tay: menu "PokiClash/Prefab/Khác/Hộp thoại và màn∕Sổ tay: thêm dòng Cốt truyện" (dựng prefab cũng gọi). Xem trong Editor:
// "PokiClash/Thử/Khác/Người chơi mới∕Cốt truyện mở đầu: xem lại" (chưa Play thì tự vào Play từ Boot.unity rồi mở).
using System.IO;
using System.Linq;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class StoryIntroMenu
    {
        const string PrefabPath = "Assets/04 Prefabs/Screens/CotTruyen.prefab";
        const string AppPath = "Assets/04 Prefabs/App/App.prefab";
        const string ArtDir = "Assets/03 Art/Story";

        // ảnh tạm khi chưa có tranh GPT (không có chữ trong ảnh)
        static readonly string[] Temp =
        {
            "Assets/03 Art/BattleBG/battle_thuy_c01.png",
            "Assets/03 Art/BattleBG/battle_thuy_c02.png",
            "Assets/03 Art/BattleBG/battle_moc_c01.png",
            "Assets/03 Art/BattleBG/battle_moc_c03.png",
            "Assets/03 Art/BattleBG/battle_hoa_s70.png",
            "Assets/03 Art/BattleBG/battle_thuy_c06.png",
        };

        static readonly Color CaptionFill = new Color(1f, 0.93f, 0.66f); // vàng nhạt kiểu ô lời dẫn truyện tranh

        static UiKit Kit => AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));

        [MenuItem("PokiClash/Prefab/Khác/Hộp thoại và màn∕Cốt truyện mở đầu (CotTruyen)", priority = 68)]
        public static void Build()
        {
            var kit = Kit;
            var root = new GameObject("CotTruyen");
            try
            {
                var view = Ui.Spawn(kit.canvas, root.transform);
                view.name = "Canvas";
                view.Canvas.sortingOrder = 25; // trên mây và hộp thoại (20), dưới lớp phủ hướng dẫn
                var bgArea = view.Bg;
                var cg = bgArea.gameObject.AddComponent<CanvasGroup>();

                // nền mực dưới các trang (lộ ra lúc sang trang)
                Img(bgArea, "nen", null, Theme.Ink).rectTransform.Stretch();

                // chạm khắp màn (dưới nút Bỏ qua)
                var catcher = Img(bgArea, "cham", null, new Color(1, 1, 1, 0), true);
                catcher.rectTransform.Stretch();
                var tap = catcher.gameObject.AddComponent<ClickCatcher>();

                var labelTpl = kit.hint.Label;
                var pages = new RectTransform[2];
                var panels = new StoryIntro.Panel[6];
                for (int p = 0; p < 2; p++)
                {
                    // trang giấy phủ kín màn: khe giữa các ô và lề ngoài là màu giấy
                    var page = Img(bgArea, "trang_" + (p + 1), null, Theme.Paper).rectTransform;
                    page.Stretch();
                    pages[p] = page;
                    for (int k = 0; k < StoryIntro.PerPage; k++)
                    {
                        int i = p * StoryIntro.PerPage + k;
                        panels[i] = Panel(page, i, labelTpl);
                    }
                }

                // nhắc chạm: giữa đáy vùng an toàn, chữ giấy viền mực (đọc được trên tranh)
                var hint = Object.Instantiate(labelTpl.gameObject, view.Safe, false).GetComponent<TextMeshProUGUI>();
                hint.name = "cham_tiep";
                StripLayout(hint);
                hint.text = "Chạm để tiếp tục";
                hint.color = Theme.Paper;
                var hintMat = AssetDatabase.LoadAssetAtPath<Material>($"Assets/03 Art/Baked/Fonts/{hint.font.name} vien 25.mat");
                if (hintMat) hint.fontSharedMaterial = hintMat;
                else Debug.LogWarning($"[Cốt truyện] Không thấy material viền cho phông {hint.font.name}: chữ nhắc chạm không viền");
                hint.fontSize = 38;
                hint.alignment = TextAlignmentOptions.Center;
                hint.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 70), new Vector2(720, 64), new Vector2(0.5f, 0.5f));

                // Bỏ qua: góc trên phải vùng an toàn
                var skip = Ui.Spawn(kit.buttonSmall, view.Safe);
                skip.name = "nut_bo_qua";
                skip.SetRole(BtnColor.Paper);
                skip.SetText("Bỏ qua");
                var srt = (RectTransform)skip.transform;
                srt.anchorMin = srt.anchorMax = srt.pivot = new Vector2(1, 1);
                srt.anchoredPosition = new Vector2(-40, -40);

                // chỉ nền chạm và nút nhận chạm
                foreach (var gr in bgArea.GetComponentsInChildren<Graphic>(true))
                    if (gr != catcher && !gr.transform.IsChildOf(skip.transform)) gr.raycastTarget = false;
                foreach (var gr in view.Safe.GetComponentsInChildren<Graphic>(true))
                    if (!gr.transform.IsChildOf(skip.transform)) gr.raycastTarget = false;

                var st = root.AddComponent<StoryIntro>();
                st.Setup(cg, pages, panels, tap, skip, hint);
                PrefabUtility.SaveAsPrefabAsset(root, PrefabPath);
            }
            finally
            {
                Object.DestroyImmediate(root);
            }

            var prefab = AssetDatabase.LoadAssetAtPath<StoryIntro>(PrefabPath);
            var appRoot = PrefabUtility.LoadPrefabContents(AppPath);
            try
            {
                var app = appRoot.GetComponentInChildren<App>(true);
                var so = new SerializedObject(app);
                so.FindProperty("storyPrefab").objectReferenceValue = prefab;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(appRoot, AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(appRoot);
            }
            AddNotebookRow();
            AssetDatabase.SaveAssets();
            int real = Enumerable.Range(1, 6).Count(k => File.Exists(ArtPath(k)));
            Debug.Log($"[Cốt truyện] Đã dựng {PrefabPath} ({real}/6 ô có tranh, còn lại ảnh tạm) và gán App.storyPrefab.");
        }

        // một ô: vật phủ kín trang (CanvasGroup), tranh tứ giác, viền mực, khung lời dẫn; hình và chỗ đặt tính lúc chạy (StoryIntro.Layout)
        static StoryIntro.Panel Panel(RectTransform page, int i, TextMeshProUGUI labelTpl)
        {
            var frame = new GameObject("o_" + (i + 1), typeof(RectTransform), typeof(CanvasGroup)).GetComponent<RectTransform>();
            frame.gameObject.layer = LayerMask.NameToLayer("UI");
            frame.SetParent(page, false);
            frame.Stretch();

            var artGo = new GameObject("tranh", typeof(RectTransform), typeof(CanvasRenderer), typeof(ComicPanel));
            artGo.layer = LayerMask.NameToLayer("UI");
            artGo.transform.SetParent(frame, false);
            ((RectTransform)artGo.transform).Stretch();
            var art = artGo.GetComponent<ComicPanel>();
            art.Sprite = ArtSprite(i);
            art.raycastTarget = false;

            var border = Ink(frame, "vien", StoryIntro.BorderWidth);

            // khung lời dẫn (ô không có chữ thì ẩn)
            var caption = Img(frame, "loi_dan", null, CaptionFill).rectTransform;
            caption.Place(Vector2.zero, Vector2.zero, new Vector2(400, 80), new Vector2(0.5f, 0.5f));
            var text = Object.Instantiate(labelTpl.gameObject, caption, false).GetComponent<TextMeshProUGUI>();
            text.name = "chu";
            StripLayout(text);
            text.rectTransform.Stretch(StoryIntro.CaptionPadX, StoryIntro.CaptionPadY, StoryIntro.CaptionPadX, StoryIntro.CaptionPadY);
            text.alignment = TextAlignmentOptions.Center;
            text.color = Theme.Ink;
            text.enableAutoSizing = false;
            text.fontSize = 38;
            text.textWrappingMode = TextWrappingModes.Normal;
            text.text = StoryIntro.Caption(i);
            var capBorder = Ink(caption, "vien", 4);
            caption.gameObject.SetActive(!string.IsNullOrEmpty(text.text));
            return new StoryIntro.Panel { frame = frame, art = art, border = border, caption = caption, captionBorder = capBorder, captionText = text };
        }

        // nét mực phủ kín cha, gốc toạ độ góc dưới trái (điểm do StoryIntro.Layout đặt)
        static InkPath Ink(RectTransform parent, string name, float width)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(InkPath));
            go.layer = LayerMask.NameToLayer("UI");
            go.transform.SetParent(parent, false);
            var rt = ((RectTransform)go.transform).Stretch();
            rt.pivot = Vector2.zero;
            var ink = go.GetComponent<InkPath>();
            ink.color = Theme.Ink;
            ink.raycastTarget = false;
            ink.Setup(new Vector2[0], width, 0, 0, true);
            return ink;
        }

        static void StripLayout(TextMeshProUGUI t)
        {
            foreach (var c in t.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
            foreach (var c in t.GetComponents<LayoutElement>()) Object.DestroyImmediate(c);
            t.gameObject.SetActive(true);
        }

        static Image Img(Transform parent, string name, Sprite s, Color c, bool raycast = false)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
            go.layer = LayerMask.NameToLayer("UI");
            go.transform.SetParent(parent, false);
            var img = go.GetComponent<Image>();
            Theme.SetSprite(img, s);
            img.color = c;
            img.raycastTarget = raycast;
            ((RectTransform)go.transform).Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(100, 100));
            return img;
        }

        // ---------- dòng "Cốt truyện mở đầu" ở Sổ tay ----------

        const string NotebookPath = "Assets/04 Prefabs/Screens/Notebook.prefab";

        // nhân bản dòng Cách chơi (không có thì Ngôn ngữ / Giảm nhấp nháy / Âm thanh) ngay dưới nó, nút ghi "Xem", gán NotebookScene.p.story.
        // Đã có thì không làm gì. Dựng prefab cốt truyện cũng gọi.
        [MenuItem("PokiClash/Prefab/Khác/Hộp thoại và màn∕Sổ tay: thêm dòng Cốt truyện", priority = 69)]
        public static void AddNotebookRow()
        {
            var contents = PrefabUtility.LoadPrefabContents(NotebookPath);
            try
            {
                var scene = contents.GetComponentInChildren<NotebookScene>(true);
                var so = new SerializedObject(scene);
                var prop = so.FindProperty("p.story");
                if (prop.objectReferenceValue) return;
                var src = new[] { "p.howTo", "p.language", "p.lowFlash", "p.sound" }
                    .Select(n => (SketchButton)so.FindProperty(n).objectReferenceValue).FirstOrDefault(b => b);
                if (!src)
                {
                    Debug.LogError("[Sổ tay] Không thấy dòng nào để nhân bản cho dòng Cốt truyện.");
                    return;
                }
                var row = src.transform.parent;
                var copy = Object.Instantiate(row.gameObject, row.parent, false);
                copy.name = "hang_CotTruyen";
                copy.transform.SetSiblingIndex(row.GetSiblingIndex() + 1);
                // con là prefab kit: thay bản sao (đã mất liên kết) bằng bản dựng từ prefab nguồn với cùng chỉnh sửa (như NotebookLanguageMenu)
                for (int i = 0; i < row.childCount; i++)
                {
                    var orig = row.GetChild(i).gameObject;
                    if (!PrefabUtility.IsAnyPrefabInstanceRoot(orig)) continue;
                    var source = PrefabUtility.GetCorrespondingObjectFromSource(orig);
                    var cloned = copy.transform.GetChild(i).gameObject;
                    var fresh = (GameObject)PrefabUtility.InstantiatePrefab(source, copy.transform);
                    PrefabUtility.SetPropertyModifications(fresh, PrefabUtility.GetPropertyModifications(orig));
                    fresh.transform.SetSiblingIndex(i);
                    fresh.name = cloned.name;
                    Object.DestroyImmediate(cloned);
                }
                foreach (var t in copy.GetComponentsInChildren<TextMeshProUGUI>(true))
                    if (!t.GetComponentInParent<SketchButton>()) t.text = "Cốt truyện mở đầu";
                var btn = copy.GetComponentInChildren<SketchButton>(true);
                btn.name = "nut_CotTruyen";
                btn.SetText("Xem");
                btn.SetRole(BtnColor.Blue);
                prop.objectReferenceValue = btn;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, NotebookPath);
                Debug.Log($"[Sổ tay] Thêm dòng Cốt truyện mở đầu dưới dòng {row.name}");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // ---------- xem lại trong Editor ----------

        // chưa Play thì mở Boot.unity, vào Play, tắt màn mở game, chờ màn tải xong rồi mở cốt truyện (bản lưu mới thì App tự mở)
        const string ReplayFlag = "StoryReplay";

        [MenuItem("PokiClash/Thử/Khác/Người chơi mới∕Cốt truyện mở đầu: xem lại", priority = 145)]
        static void Replay()
        {
            if (Application.isPlaying)
            {
                if (App.I) App.I.StartCoroutine(OpenWhenReady());
                return;
            }
            if (!UnityEditor.SceneManagement.EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo()) return;
            const string boot = "Assets/00 Scenes/Boot.unity";
            if (UnityEngine.SceneManagement.SceneManager.GetActiveScene().path != boot)
                UnityEditor.SceneManagement.EditorSceneManager.OpenScene(boot);
            SessionState.SetBool(ReplayFlag, true);
            EditorApplication.isPlaying = true;
        }

        [InitializeOnLoadMethod]
        static void HookReplay()
        {
            EditorApplication.update += PollReplay;
            // thoát Play trước khi kịp mở thì bỏ cờ (không xoá theo isPlayingOrWillChangePlaymode: lúc đang chuyển sang Play nó còn false)
            EditorApplication.playModeStateChanged += s =>
            {
                if (s == PlayModeStateChange.EnteredEditMode) SessionState.SetBool(ReplayFlag, false);
            };
        }

        static void PollReplay()
        {
            if (!SessionState.GetBool(ReplayFlag, false)) return;
            if (!EditorApplication.isPlaying || App.I == null || App.Router == null || App.Router.CurrentRoot == null) return;
            SessionState.SetBool(ReplayFlag, false);
            BootTitle.Dismiss(); // màn mở game chỉ tắt khi chạm
            App.I.StartCoroutine(OpenWhenReady());
        }

        static System.Collections.IEnumerator OpenWhenReady()
        {
            float t0 = Time.realtimeSinceStartup;
            while (!StoryIntro.Current && App.Booting && Time.realtimeSinceStartup - t0 < 30) yield return null;
            if (StoryIntro.Current) yield break;
            if (!StoryIntro.Replay()) Debug.LogWarning("[Cốt truyện] Không mở được (App.storyPrefab trống?).");
        }

        [MenuItem("PokiClash/Thử/Khác/Người chơi mới∕Cốt truyện mở đầu: chạm hết và chụp từng khung (đang Play)", priority = 146)]
        static void Tour()
        {
            if (!Application.isPlaying || !App.I)
            {
                Debug.LogWarning("[Cốt truyện] Cần đang Play.");
                return;
            }
            App.I.StartCoroutine(RunTour());
        }

        static string Dir => Path.Combine(PlayTour.ShotDir, "cot_truyen");

        static System.Collections.IEnumerator RunTour()
        {
            if (Directory.Exists(Dir)) Directory.Delete(Dir, true);
            Directory.CreateDirectory(Dir);
            var st = StoryIntro.Current ? StoryIntro.Current : StoryIntro.Replay();
            if (!st)
            {
                Debug.LogWarning("[Cốt truyện] Không mở được (App.storyPrefab trống?).");
                yield break;
            }
            int n = 0;
            yield return new WaitForSecondsRealtime(0.3f);
            // chụp giữa lúc khung đầu đang đập xuống, rồi mỗi khung sau khi chữ chạy xong
            yield return Shot(n++, "dang_hien");
            for (int i = 0; i < 6 && st; i++)
            {
                yield return new WaitForSecondsRealtime(1.6f);
                yield return Shot(n++, "khung_" + (i + 1));
                if (!st) break;
                st.DebugTap();
                if (i == 2)
                {
                    yield return new WaitForSecondsRealtime(0.25f);
                    yield return Shot(n++, "lat_trang");
                }
            }
            yield return new WaitForSecondsRealtime(0.15f);
            yield return Shot(n++, "mo_dan");
            while (st) yield return null;
            HowToDialog.Open();
            yield return new WaitForSecondsRealtime(0.8f);
            yield return Shot(n++, "hop_cach_choi");
            App.Modals.CloseAll();
            Debug.Log($"[Cốt truyện] Đã chụp {n} ảnh vào {Dir}");
        }

        static System.Collections.IEnumerator Shot(int n, string name)
        {
            yield return new WaitForEndOfFrame();
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(Dir, $"{n:00}_{name}.jpg"), tex.EncodeToJPG(85));
            Object.Destroy(tex);
        }

        static string ArtPath(int k) => $"{ArtDir}/khung_{k}.png";

        static Sprite ArtSprite(int i)
        {
            var real = Sprite(ArtPath(i + 1));
            if (real) return real;
            var tmp = Sprite(Temp[i]);
            if (!tmp) Debug.LogWarning($"[Cốt truyện] Khung {i + 1}: không có tranh lẫn ảnh tạm {Temp[i]}");
            return tmp;
        }

        static Sprite Sprite(string path) => File.Exists(path) ? AssetDatabase.LoadAllAssetsAtPath(path).OfType<Sprite>().FirstOrDefault() : null;

        // chân dung bán thân nhân vật chính (nền trong suốt, build_story.py --nhap) cho lời dẫn của lớp phủ hướng dẫn (GuideMenu);
        // chưa có thì null
        public const string HeroPath = ArtDir + "/nhan_vat.png";

        // cách nhập (sprite, không mipmap, ASTC trên điện thoại) do ArtPostprocessor đặt cho mọi ảnh trong Assets/03 Art
        public static Sprite HeroSprite() => Sprite(HeroPath);
    }
}
