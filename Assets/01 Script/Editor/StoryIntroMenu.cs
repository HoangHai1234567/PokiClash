// Dựng prefab đoạn cốt truyện mở đầu (App/StoryIntro.cs, GD_Claude/25_FTUE.md mục 11): Assets/04 Prefabs/Screens/CotTruyen.prefab,
// gán App.storyPrefab trong App.prefab. Bàn gỗ, một tờ sổ, hai trang × 3 khung tranh (trang 1: khung ngang trên, hai khung dọc dưới;
// trang 2: hai khung dọc trên, khung ngang dưới), mỗi khung là tranh in trên giấy viền mực, băng keo trên, băng chữ dưới.
// Tranh lấy ở Assets/03 Art/Story/khung_1..6.png (gói GPT ArtGen/Story/build_story.py --nhap; cách nhập do ArtPostprocessor); khung nào chưa có tranh thì gắn tạm
// một nền trận / bản đồ có sẵn. Có tranh mới thì chạy lại menu.
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
        const string DeskPath = "Assets/03 Art/Boot/boot_ban_go.png";

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

        // khung trên trang (toạ độ trong tờ 1010 × 1700, gốc giữa tờ): tâm, cỡ, độ nghiêng. Cả cụm hạ 45 cho cân với dòng nhắc chạm dưới.
        const float LW = 900, LH = 600, PW = 430, PH = 645;
        static readonly (Vector2 pos, Vector2 size, float tilt)[] Layout =
        {
            (new Vector2(0, 425), new Vector2(LW, LH), -1.5f),
            (new Vector2(-225, -275), new Vector2(PW, PH), 2f),
            (new Vector2(225, -275), new Vector2(PW, PH), -2.5f),
            (new Vector2(-225, 395), new Vector2(PW, PH), 1.5f),
            (new Vector2(225, 395), new Vector2(PW, PH), -2f),
            (new Vector2(0, -335), new Vector2(LW, LH), 1f),
        };

        static UiKit Kit => AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));

        [MenuItem("PokiClash/Prefab/Cốt truyện mở đầu (CotTruyen)", priority = 68)]
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

                // bàn gỗ phủ kín màn (giữ tỉ lệ ảnh, tràn mép)
                var desk = Img(bgArea, "ban_go", Sprite(DeskPath), Color.white);
                desk.rectTransform.Stretch();
                var fit = desk.gameObject.AddComponent<AspectRatioFitter>();
                fit.aspectMode = AspectRatioFitter.AspectMode.EnvelopeParent;
                fit.aspectRatio = desk.sprite ? desk.sprite.rect.width / desk.sprite.rect.height : 0.5625f;
                if (!desk.sprite) desk.color = new Color(0.45f, 0.3f, 0.18f);

                // chạm khắp màn (dưới nút Bỏ qua)
                var catcher = Img(bgArea, "cham", null, new Color(1, 1, 1, 0), true);
                catcher.rectTransform.Stretch();
                var tap = catcher.gameObject.AddComponent<ClickCatcher>();

                // sổ: chứa hai trang (co lại trên máy thấp), trong khung 1080
                var book = new GameObject("so", typeof(RectTransform)).GetComponent<RectTransform>();
                book.gameObject.layer = LayerMask.NameToLayer("UI");
                book.SetParent(view.Frame, false);
                book.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -10), new Vector2(1010, 1700));

                var labelTpl = kit.hint.Label;
                var pages = new RectTransform[2];
                var panels = new StoryIntro.Panel[6];
                for (int p = 0; p < 2; p++)
                {
                    var page = Object.Instantiate(kit.panel.gameObject, book, false).GetComponent<RectTransform>();
                    page.name = "trang_" + (p + 1);
                    foreach (Transform ch in page) Object.DestroyImmediate(ch.gameObject);
                    page.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(1010, 1700));
                    page.GetComponent<Image>().raycastTarget = false;
                    pages[p] = page;
                    for (int k = 0; k < StoryIntro.PerPage; k++)
                    {
                        int i = p * StoryIntro.PerPage + k;
                        panels[i] = Panel(kit, page, i, labelTpl);
                    }
                }

                // nhắc chạm (dưới đáy tờ đang mở, mực trên giấy)
                var hint = Object.Instantiate(labelTpl.gameObject, book, false).GetComponent<TextMeshProUGUI>();
                hint.name = "cham_tiep";
                StripLayout(hint);
                hint.text = "Chạm để tiếp tục";
                hint.color = Theme.Ink2;
                hint.fontSize = 34;
                hint.alignment = TextAlignmentOptions.Center;
                hint.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -760), new Vector2(720, 60));

                // Bỏ qua: góc trên phải vùng an toàn
                var skip = Ui.Spawn(kit.buttonSmall, view.Safe);
                skip.name = "nut_bo_qua";
                skip.SetRole(BtnColor.Paper);
                skip.SetText("Bỏ qua");
                var srt = (RectTransform)skip.transform;
                srt.anchorMin = srt.anchorMax = srt.pivot = new Vector2(1, 1);
                srt.anchoredPosition = new Vector2(-28, -28);

                // chỉ nền chạm và nút nhận chạm
                foreach (var gr in bgArea.GetComponentsInChildren<Graphic>(true))
                    if (gr != catcher && !gr.transform.IsChildOf(skip.transform)) gr.raycastTarget = false;
                foreach (var gr in view.Safe.GetComponentsInChildren<Graphic>(true))
                    if (!gr.transform.IsChildOf(skip.transform)) gr.raycastTarget = false;

                var st = root.AddComponent<StoryIntro>();
                st.Setup(cg, book, pages, panels, tap, skip, hint);
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
            AssetDatabase.SaveAssets();
            int real = Enumerable.Range(1, 6).Count(k => File.Exists(ArtPath(k)));
            Debug.Log($"[Cốt truyện] Đã dựng {PrefabPath} ({real}/6 khung có tranh, còn lại ảnh tạm) và gán App.storyPrefab.");
        }

        static StoryIntro.Panel Panel(UiKit kit, RectTransform page, int i, TextMeshProUGUI labelTpl)
        {
            var (pos, size, tilt) = Layout[i];
            var frame = Img(page, "khung_" + (i + 1), null, Theme.Paper).rectTransform;
            frame.Place(new Vector2(0.5f, 0.5f), pos, size);
            frame.localEulerAngles = new Vector3(0, 0, tilt);
            frame.gameObject.AddComponent<CanvasGroup>();
            Border(frame, "vien_ngoai", size, 0, 5);

            const float inset = 16;
            // cắt tranh bằng Mask (stencil): RectMask2D cắt theo hộp thẳng nên khung nghiêng bị tràn mép
            var window = Img(frame, "tranh_khung", null, Color.white).rectTransform;
            window.Stretch(inset, inset, inset, inset);
            window.gameObject.AddComponent<Mask>().showMaskGraphic = false;
            var art = Img(window, "tranh", ArtSprite(i), Color.white);
            art.preserveAspect = false;
            var asp = art.sprite ? art.sprite.rect.width / art.sprite.rect.height : size.x / size.y;
            var inner = size - new Vector2(inset, inset) * 2;
            float w = Mathf.Max(inner.x, inner.y * asp);
            art.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(w, w / asp) * 1.12f);
            Border(frame, "vien_trong", size, inset, 4);

            // băng keo trên mép
            var tape = Object.Instantiate(kit.tape.gameObject, frame, false).GetComponent<RectTransform>();
            tape.name = "bang_keo";
            tape.Place(new Vector2(0.5f, 1), new Vector2(i % 2 == 0 ? -size.x * 0.18f : size.x * 0.2f, 6), new Vector2(170, 54), new Vector2(0.5f, 0.5f));
            tape.localEulerAngles = new Vector3(0, 0, i % 2 == 0 ? -6 : 5);

            // băng chữ dưới mép (khung không có chữ thì ẩn lúc chạy)
            var caption = Img(frame, "bang_chu", null, Theme.Paper2).rectTransform;
            float cw = Mathf.Min(size.x - 40, size.x > size.y ? 640 : 400);
            caption.Place(new Vector2(0.5f, 0), new Vector2(0, -6), new Vector2(cw, 78), new Vector2(0.5f, 0.5f));
            caption.localEulerAngles = new Vector3(0, 0, -tilt * 0.6f + (i % 2 == 0 ? 1 : -1));
            Border(caption, "vien", new Vector2(cw, 78), 0, 4);
            var text = Object.Instantiate(labelTpl.gameObject, caption, false).GetComponent<TextMeshProUGUI>();
            text.name = "chu";
            StripLayout(text);
            text.rectTransform.Stretch(14, 6, 14, 6);
            text.alignment = TextAlignmentOptions.Center;
            text.color = Theme.Ink;
            text.enableAutoSizing = true;
            text.fontSizeMin = 22;
            text.fontSizeMax = 38;
            text.textWrappingMode = TextWrappingModes.Normal;
            text.text = StoryIntro.Caption(i);
            caption.gameObject.SetActive(!string.IsNullOrEmpty(text.text));
            return new StoryIntro.Panel { frame = frame, window = window, art = art, caption = caption, captionText = text, tilt = tilt };
        }

        // viền mực tay quanh hình chữ nhật (lệch nhẹ từng điểm cho có vẻ vẽ tay)
        static void Border(RectTransform parent, string name, Vector2 size, float inset, float width)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(InkPath));
            go.layer = LayerMask.NameToLayer("UI");
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.Place(new Vector2(0.5f, 0.5f), Vector2.zero, size);
            var ink = go.GetComponent<InkPath>();
            ink.color = Theme.Ink;
            ink.raycastTarget = false;
            float hx = size.x / 2 - inset, hy = size.y / 2 - inset;
            var rnd = new System.Random(name.GetHashCode() ^ (int)(size.x * 7 + size.y));
            float J() => (float)(rnd.NextDouble() * 2 - 1) * 1.6f;
            var pts = new[]
            {
                new Vector2(-hx, hy), new Vector2(0, hy + J()), new Vector2(hx, hy),
                new Vector2(hx + J(), 0), new Vector2(hx, -hy),
                new Vector2(0, -hy + J()), new Vector2(-hx, -hy), new Vector2(-hx + J(), 0),
            };
            ink.Setup(pts, width, 0, 0, true);
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

        // ---------- thử khi đang Play ----------

        [MenuItem("PokiClash/Thử/Cốt truyện mở đầu: xem lại (đang Play)", priority = 145)]
        static void Replay()
        {
            if (!Application.isPlaying || !App.I)
            {
                Debug.LogWarning("[Cốt truyện] Cần đang Play.");
                return;
            }
            StoryIntro.Replay();
        }

        [MenuItem("PokiClash/Thử/Cốt truyện mở đầu: chạm hết và chụp từng khung (đang Play)", priority = 146)]
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
