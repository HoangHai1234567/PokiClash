// Màn mở game "Sa bàn giấy" (BootTitle; người dùng chọn ý tưởng A ngày 2026-11-06, GD_Claude/16_ManBoot.md).
// Menu "PokiClash/Prefab/Màn mở game: sa bàn" dựng (chạy lại thì dựng lại):
// - Assets/04 Prefabs/Screens/BootTitle.prefab:
//   + canvas màn boot: bàn gỗ (nhận chạm), thẻ úp và bút chì, ảnh sa bàn (RawImage), logo, băng keo chữ, giấy ghi chú có thanh tải
//     và lời nhắc chạm;
//   + sa bàn: canvas thế giới ở xa và camera phối cảnh (tắt sẵn, BootTitle bật khi đã có RenderTexture); tấm bản đồ nghiêng, đảo,
//     mũi tên khắc, vòng "Xuất phát!", đế, tấm dựng tướng, cờ hệ. Toạ độ chép từ Web/src/view/boot/sceneTable.ts, nhân 2;
// - gán App.bootTitle trong prefab App.
// Ảnh ở Assets/03 Art/Boot, xuất từ bản web: node Web/scripts/export_boot_art.mjs (cần npm run dev).
// Thêm: công tắc "PokiClash/Thử/Bỏ màn mở game" và vòng chụp "PokiClash/Thử/Màn mở game: chụp từng nhịp (đang Play)".
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
    public static class BootTitleMenu
    {
        const string PrefabPath = "Assets/04 Prefabs/Screens/BootTitle.prefab";
        const string AppPath = "Assets/04 Prefabs/App/App.prefab";
        const string ArtDir = "Assets/03 Art/Boot/";
        const string IslandPath = "Assets/03 Art/Islands/world.png";
        const string SkipMenu = "PokiClash/Thử/Bỏ màn mở game (Play vào thẳng sảnh)";

        // tấm bản đồ trên web: 480 × 690, gốc trên trái; chỗ đứng của tướng (POS trong sceneTable.ts)
        const float SheetW = 480, SheetH = 690;
        static readonly Dictionary<Elem, Vector2> Pos = new Dictionary<Elem, Vector2>
        {
            [Elem.Thuy] = new Vector2(141, 504),
            [Elem.Hoa] = new Vector2(297, 182),
            [Elem.Kim] = new Vector2(385, 297),
            [Elem.Moc] = new Vector2(123, 257),
            [Elem.Tho] = new Vector2(354, 504),
        };

        // camera sa bàn: perspective 980 px, perspective-origin (270, 60) của CSS, nhân 2, gốc giữa khung 1080 × 1920
        static readonly Vector3 Eye = new Vector3(0, 840, -1960);
        // vùng ảnh sa bàn trên khung (đủ chứa tấm bản đồ, băng keo góc và tướng đứng ở mép xa)
        static readonly Rect Region = new Rect(-540, -840, 1080, 1300);

        static readonly Vector2 C = new Vector2(0.5f, 0.5f);

        // toạ độ web trên tấm bản đồ → toạ độ cục bộ của tấm trong Unity (gốc giữa cạnh dưới, y lên, nhân 2)
        static Vector2 S(float x, float y) => new Vector2(2 * (x - SheetW / 2), 2 * (SheetH - y));
        static Vector2 S(Vector2 v) => S(v.x, v.y);

        static ArtLibrary art;

        [MenuItem("PokiClash/Prefab/Màn mở game: sa bàn (BootTitle)", priority = 68)]
        static void Build()
        {
            var assets = Load<UiAssets>();
            art = Load<ArtLibrary>();
            Theme.Init(assets); // phông, sprite giấy, viền chữ nướng sẵn
            var root = new GameObject("BootTitle");
            try
            {
                var bt = root.AddComponent<BootTitle>();
                bt.p = new BootTitle.Parts();
                BuildScreen(root.transform, assets.prefabs, bt.p);
                BuildWorld(root.transform, bt.p);
                Folder(Path.GetDirectoryName(PrefabPath).Replace('\\', '/'));
                PrefabUtility.SaveAsPrefabAsset(root, PrefabPath);
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
            var prefab = AssetDatabase.LoadAssetAtPath<BootTitle>(PrefabPath);
            var appRoot = PrefabUtility.LoadPrefabContents(AppPath);
            try
            {
                var app = appRoot.GetComponentInChildren<App>(true);
                app.bootTitle = prefab;
                PrefabUtility.SaveAsPrefabAsset(appRoot, AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(appRoot);
            }
            AssetDatabase.SaveAssets();
            Debug.Log($"[Màn mở game] Đã dựng {PrefabPath} và gán vào {AppPath}.");
        }

        // ---------- canvas màn boot ----------

        static void BuildScreen(Transform root, UiKit kit, BootTitle.Parts p)
        {
            var view = Ui.Spawn(kit.canvas, root);
            view.name = "Canvas";
            view.Canvas.sortingOrder = 15; // trên thanh trên (10), dưới canvas phủ có mây và hộp thoại (20)
            p.view = view;

            // bàn gỗ phủ kín màn, nhận chạm (chặn chạm xuống sảnh bên dưới)
            var desk = Img(view.Bg, "ban_go", Spr("boot_ban_go"), raycast: true);
            desk.rectTransform.Stretch();
            p.catcher = desk.gameObject.AddComponent<ClickCatcher>();

            var stage = Node(view.Frame, "san_khau");
            stage.Place(C, Vector2.zero, new Vector2(PokiCanvas.RefW, PokiCanvas.RefH));
            p.stage = stage;

            // thẻ úp (chọn 1 trong 3) và bút chì trên bàn
            var props = Node(stage, "do_tren_ban", typeof(CanvasGroup));
            props.Stretch();
            p.props = props.GetComponent<CanvasGroup>();
            p.props.blocksRaycasts = false;
            Img(props, "the_up", Spr("boot_the_up")).rectTransform.Place(C, new Vector2(-428, -4), new Vector2(400, 440));
            var pencil = Img(props, "but_chi", Spr("boot_but_chi")).rectTransform;
            pencil.Place(C, new Vector2(510, 66), new Vector2(356, 84));
            pencil.localEulerAngles = new Vector3(0, 0, -62);

            // ảnh camera sa bàn
            var raw = new GameObject("sa_ban", typeof(RectTransform), typeof(RawImage)).GetComponent<RawImage>();
            raw.transform.SetParent(stage, false);
            raw.raycastTarget = false;
            raw.color = new Color(1, 1, 1, 1);
            raw.rectTransform.Place(C, Region.center, Region.size);
            p.saBan = raw;

            // logo (gốc ở cạnh dưới để bật lên)
            var logo = Img(stage, "logo", Spr("boot_logo")).rectTransform;
            logo.Place(C, new Vector2(0, 449), Native(logo), new Vector2(0.5f, 0));
            logo.localEulerAngles = new Vector3(0, 0, 2);
            p.logo = logo;

            // băng keo chữ
            var tag = Node(stage, "bang_keo", typeof(CanvasGroup));
            tag.Place(C, new Vector2(0, 458), new Vector2(406, 76));
            tag.localEulerAngles = new Vector3(0, 0, 3);
            p.tagline = tag;
            p.taglineGroup = tag.GetComponent<CanvasGroup>();
            p.taglineGroup.blocksRaycasts = false;
            Img(tag, "nen", Spr("boot_bang_keo")).rectTransform.Stretch();
            Text(tag, "chu", Theme.Body, 42, Theme.Ink, "Sổ Tay Phiêu Lưu").rectTransform.Stretch(0, 0, 0, 4);

            // giấy ghi chú dưới: thanh tải, rồi lời nhắc chạm
            var note = Img(stage, "giay_ghi", Spr("boot_giay_ghi")).rectTransform;
            note.Place(C, new Vector2(0, -814), new Vector2(812, 248));
            note.localEulerAngles = new Vector3(0, 0, 1);
            p.note = note;

            var loading = Node(note, "dang_tai");
            loading.Stretch();
            p.loading = loading.gameObject;
            var bar = Img(loading, "khung", Spr("boot_thanh_tai")).rectTransform;
            bar.Place(C, new Vector2(0, 37), new Vector2(608, 56));
            var fill = Img(bar, "loi", Spr("boot_thanh_tai_loi"));
            fill.rectTransform.Place(C, Vector2.zero, new Vector2(588, 36));
            fill.type = Image.Type.Filled;
            fill.fillMethod = Image.FillMethod.Horizontal;
            fill.fillOrigin = (int)Image.OriginHorizontal.Left;
            p.barFill = fill;
            var pen = Img(bar, "but", art ? art.Icon("pencil") : null).rectTransform;
            pen.Place(C, new Vector2(-276, 50), new Vector2(68, 68));
            pen.localEulerAngles = new Vector3(0, 0, -8);
            p.barPencil = pen;
            p.pct = Text(loading, "phan_tram", Theme.Bold, 30, Theme.Ink2, "0%");
            p.pct.rectTransform.Place(C, new Vector2(0, -10), new Vector2(200, 40));
            p.tip = Text(loading, "meo", Theme.Body, 27, Theme.Ink2, "Mẹo");
            p.tip.rectTransform.Place(C, new Vector2(0, -68), new Vector2(720, 76));
            p.tip.textWrappingMode = TextWrappingModes.Normal;
            p.tip.lineSpacing = -12;

            var tap = Node(note, "cham");
            tap.Stretch();
            p.tap = tap.gameObject;
            var tapText = Text(tap, "chu", Theme.Title, 72, Color.white, "Chạm để bắt đầu", 0.3f);
            tapText.rectTransform.Place(C, new Vector2(0, 14), new Vector2(760, 100));
            p.tapText = tapText.rectTransform;
            Img(tapText.rectTransform, "gach", Spr("boot_gach_chan")).rectTransform.Place(C, new Vector2(0, -50), new Vector2(572, 40));
            tap.gameObject.SetActive(false);
        }

        // ---------- sa bàn: canvas thế giới ở xa, camera phối cảnh ----------

        static void BuildWorld(Transform root, BootTitle.Parts p)
        {
            var wgo = new GameObject("SaBan", typeof(RectTransform), typeof(Canvas));
            var world = (RectTransform)wgo.transform;
            world.SetParent(root, false);
            world.sizeDelta = new Vector2(PokiCanvas.RefW, PokiCanvas.RefH);
            world.localPosition = new Vector3(-20000, 0, 0); // xa mọi thứ khác (tướng aola ở x = 10000+)
            world.localScale = Vector3.one;
            var canvas = wgo.GetComponent<Canvas>();
            canvas.renderMode = RenderMode.WorldSpace;
            p.world = world;

            var camGo = new GameObject("cam", typeof(Camera));
            camGo.transform.SetParent(world, false);
            camGo.transform.localPosition = Eye;
            var cam = camGo.GetComponent<Camera>();
            cam.orthographic = false;
            cam.clearFlags = CameraClearFlags.SolidColor;
            // nền trong suốt màu gỗ: mép mờ của băng keo, nét viền hoà vào mặt bàn chứ không viền đen
            cam.backgroundColor = new Color(0.49f, 0.31f, 0.19f, 0);
            cam.depth = -10;
            cam.nearClipPlane = 20;
            cam.farClipPlane = 6000;
            cam.allowHDR = false;
            cam.useOcclusionCulling = false;
            cam.enabled = false; // BootTitle bật khi đã gắn RenderTexture
            canvas.worldCamera = cam;
            p.cam = cam;
            p.eye = Eye;
            p.region = Region;

            var sheet = Node(world, "to_ban_do", typeof(CanvasGroup));
            sheet.Place(C, new Vector2(0, -756), new Vector2(2 * SheetW, 2 * SheetH), new Vector2(0.5f, 0));
            sheet.localEulerAngles = new Vector3(BootTitle.Tilt, 0, 0);
            p.sheet = sheet;
            p.sheetGroup = sheet.GetComponent<CanvasGroup>();
            p.sheetGroup.blocksRaycasts = false;
            // giấy kẻ ô, biển, băng keo góc, la bàn (ảnh có lề 30 px web quanh tấm)
            Img(sheet, "giay", Spr("boot_ban_do")).rectTransform.Place(C, Vector2.zero, new Vector2(1080, 1500));
            var island = Img(sheet, "dao", AssetDatabase.LoadAssetAtPath<Sprite>(IslandPath));
            island.rectTransform.Place(C, new Vector2(0, 0.3f), new Vector2(880, 880 * 2320f / 1480f));
            island.type = Image.Type.Filled;
            island.fillMethod = Image.FillMethod.Horizontal;
            island.fillOrigin = (int)Image.OriginHorizontal.Left;
            p.island = island;

            // kế hoạch: mũi tên đứt nét theo vòng khắc (viền mực + lõi màu hệ), đầu mũi tên
            var plan = Node(sheet, "ke_hoach");
            plan.Place(new Vector2(0.5f, 0), Vector2.zero, Vector2.zero, new Vector2(0.5f, 0));
            var cyc = BootTitle.Cycle;
            p.arrowInk = new InkPath[cyc.Length];
            p.arrowColor = new InkPath[cyc.Length];
            p.arrowHead = new InkPath[cyc.Length];
            for (int i = 0; i < cyc.Length; i++)
            {
                var from = Pos[cyc[i]];
                var to = Pos[cyc[(i + 1) % cyc.Length]];
                Arrow(from, to, i % 2 == 1 ? 34 : -34, out var pts, out var head);
                p.arrowInk[i] = Ink(plan, $"mui_ten_{i}_muc", pts, 22, Theme.Ink, 26, 24);
                p.arrowColor[i] = Ink(plan, $"mui_ten_{i}_mau", pts, 11, Theme.Of(cyc[i]), 26, 24);
                p.arrowHead[i] = Ink(plan, $"mui_ten_{i}_dau", head, 10, Theme.Ink);
            }

            // khoanh "Xuất phát!" quanh đảo Thủy
            var startRt = Node(sheet, "xuat_phat", typeof(CanvasGroup));
            startRt.Place(new Vector2(0.5f, 0), Vector2.zero, Vector2.zero, new Vector2(0.5f, 0));
            p.start = startRt.GetComponent<CanvasGroup>();
            p.start.blocksRaycasts = false;
            var sp = Pos[Elem.Thuy];
            var ringPts = new Vector2[64];
            float th = -8 * Mathf.Deg2Rad;
            for (int k = 0; k < ringPts.Length; k++)
            {
                float t = k * Mathf.PI * 2 / ringPts.Length;
                float ex = 70 * Mathf.Cos(t), ey = -4 + 52 * Mathf.Sin(t); // so với tâm (sx, sy), y xuống như SVG
                float rx = ex * Mathf.Cos(th) - ey * Mathf.Sin(th), ry = ex * Mathf.Sin(th) + ey * Mathf.Cos(th);
                ringPts[k] = S(sp.x + rx, sp.y + ry);
            }
            p.ring = Ink(startRt, "vong", ringPts, 8, Theme.Hex("#c0392b"), 0, 0, true);
            var go = Text(startRt, "chu", Theme.Body, 60, Theme.Hex("#c0392b"), "Xuất phát!");
            go.rectTransform.Place(C, S(sp.x + 2, sp.y + 74), new Vector2(340, 90));
            go.rectTransform.localEulerAngles = new Vector3(0, 0, 6);

            // tướng (đế, tấm dựng) và cờ: vẽ từ xa tới gần; cờ trước tướng để cán cờ nằm sau người tướng
            p.standees = new BootTitle.Standee[cyc.Length];
            foreach (var e in cyc.OrderBy(e => Pos[e].y).ThenBy(e => Pos[e].x))
            {
                int i = System.Array.IndexOf(cyc, e);
                var at = Pos[e];
                string n = ElemFile(e);
                // cờ cắm cạnh tướng (bên phải bản đồ thì cờ bên phải), gốc ở chân cán
                float fx = at.x > SheetW / 2 ? 46 : -62;
                var flag = Img(sheet, "co_" + n, Spr("boot_co_" + n)).rectTransform;
                flag.Place(new Vector2(0.5f, 0), S(at.x + fx, at.y - 22), new Vector2(156, 232), new Vector2(23f / 156, 1 - 218f / 232));
                flag.localEulerAngles = new Vector3(-BootTitle.Tilt, 0, 0);
                var spot = Node(sheet, "dung_" + n);
                spot.Place(new Vector2(0.5f, 0), S(at), Vector2.zero);
                var bases = Node(spot, "de");
                bases.Place(C, Vector2.zero, new Vector2(168, 72));
                Img(bases, "nen", Spr("boot_de_nen"), Theme.Of(e)).rectTransform.Stretch();
                Img(bases, "vien", Spr("boot_de_vien")).rectTransform.Stretch();
                var up = Node(spot, "len");
                up.Place(C, Vector2.zero, new Vector2(440, 380), new Vector2(0.5f, 0));
                up.localEulerAngles = new Vector3(-BootTitle.Tilt, 0, 0);
                p.standees[i] = new BootTitle.Standee { up = up, flag = flag, bases = bases, flip = at.x > SheetW / 2 };
            }
        }

        // mũi tên cong từ chỗ đứng này tới chỗ đứng kia (như sceneTable.ts): bỏ 42 px đầu, 48 px cuối, cong theo bend
        static void Arrow(Vector2 a0, Vector2 a1, float bend, out Vector2[] pts, out Vector2[] head)
        {
            var d = a1 - a0;
            float L = d.magnitude;
            var u = d / L;
            var a = a0 + u * 42;
            var b = a1 - u * 48;
            var m = (a + b) / 2 + new Vector2(-u.y, u.x) * bend;
            pts = new Vector2[25];
            for (int k = 0; k < pts.Length; k++)
            {
                float t = k / (float)(pts.Length - 1);
                var q = (1 - t) * (1 - t) * a + 2 * (1 - t) * t * m + t * t * b;
                pts[k] = S(q);
            }
            var tg = (b - m).normalized;
            head = new[]
            {
                S(b - tg * 18 - new Vector2(tg.y, -tg.x) * 11),
                S(b),
                S(b - tg * 18 + new Vector2(tg.y, -tg.x) * 11),
            };
        }

        // ---------- tiện ích ----------

        static string ElemFile(Elem e) => e switch
        {
            Elem.Kim => "kim",
            Elem.Moc => "moc",
            Elem.Thuy => "thuy",
            Elem.Hoa => "hoa",
            _ => "tho",
        };

        static T Load<T>() where T : Object =>
            AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:" + typeof(T).Name)[0]));

        static Sprite Spr(string name)
        {
            var s = AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + name + ".png");
            if (!s) Debug.LogError($"[Màn mở game] Thiếu ảnh {ArtDir}{name}.png: chạy node Web/scripts/export_boot_art.mjs");
            return s;
        }

        static Vector2 Native(RectTransform rt)
        {
            var img = rt.GetComponent<Image>();
            return img && img.sprite ? img.sprite.rect.size : rt.sizeDelta;
        }

        static void Folder(string path)
        {
            if (AssetDatabase.IsValidFolder(path)) return;
            var parent = Path.GetDirectoryName(path).Replace('\\', '/');
            Folder(parent);
            AssetDatabase.CreateFolder(parent, Path.GetFileName(path));
        }

        static RectTransform Node(Transform parent, string name, params System.Type[] extra)
        {
            var go = new GameObject(name, new[] { typeof(RectTransform) }.Concat(extra).ToArray());
            go.transform.SetParent(parent, false);
            return (RectTransform)go.transform;
        }

        static Image Img(Transform parent, string name, Sprite s, Color? color = null, bool raycast = false)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            var img = go.GetComponent<Image>();
            Theme.SetSprite(img, s);
            img.color = color ?? Color.white;
            img.raycastTarget = raycast;
            return img;
        }

        static TextMeshProUGUI Text(Transform parent, string name, TMP_FontAsset font, float size, Color color, string text, float outline = 0)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(TextMeshProUGUI));
            go.transform.SetParent(parent, false);
            var t = go.GetComponent<TextMeshProUGUI>();
            t.font = font;
            if (outline > 0)
            {
                var m = Theme.Outlined(font, outline);
                if (m) t.fontSharedMaterial = m;
            }
            t.fontSize = size;
            t.color = color;
            t.alignment = TextAlignmentOptions.Center;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
            t.raycastTarget = false;
            t.text = text;
            return t;
        }

        static InkPath Ink(Transform parent, string name, Vector2[] pts, float width, Color color, float dash = 0, float gap = 0, bool closed = false)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(InkPath));
            go.transform.SetParent(parent, false);
            var rt = (RectTransform)go.transform;
            rt.Place(new Vector2(0.5f, 0.5f), Vector2.zero, Vector2.zero);
            var ink = go.GetComponent<InkPath>();
            ink.Setup(pts, width, dash, gap, closed);
            ink.color = color;
            ink.raycastTarget = false;
            return ink;
        }

        // ---------- công tắc và vòng chụp ----------

        [MenuItem(SkipMenu, priority = 98)]
        static void ToggleSkip()
        {
            bool v = !EditorPrefs.GetBool(App.SkipBootPref, false);
            EditorPrefs.SetBool(App.SkipBootPref, v);
            Menu.SetChecked(SkipMenu, v);
        }

        [MenuItem(SkipMenu, true)]
        static bool ToggleSkipCheck()
        {
            Menu.SetChecked(SkipMenu, EditorPrefs.GetBool(App.SkipBootPref, false));
            return true;
        }

        // diễn lại màn mở game trên sảnh, chụp từng nhịp vào Temp/PokiShots/boot_*.png, chạm, chụp đoạn lao vào đảo
        [MenuItem("PokiClash/Thử/Màn mở game: chụp từng nhịp (đang Play)", priority = 120)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Màn mở game] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(RunTour());
        }

        static IEnumerator RunTour()
        {
            BootTitle.Dismiss();
            yield return null;
            while (App.Router.Busy) yield return null;
            App.Modals.CloseAll();
            BootTitle.Spawn(App.I.bootTitle);
            float t0 = Time.realtimeSinceStartup;
            foreach (var at in new[] { 0.3f, 1.2f, 2.0f, 2.9f, 3.9f, 4.8f })
            {
                while (Time.realtimeSinceStartup - t0 < at) yield return null;
                yield return Shot($"{Mathf.RoundToInt(at * 10):00}");
            }
            var bt = BootTitle.Current;
            if (!bt)
            {
                Debug.LogError("[Màn mở game] Màn tắt giữa chừng.");
                yield break;
            }
            bt.p.catcher.OnClick?.Invoke();
            float c0 = Time.realtimeSinceStartup;
            foreach (var at in new[] { 0.35f, 0.9f, 1.5f })
            {
                while (Time.realtimeSinceStartup - c0 < at) yield return null;
                yield return Shot($"x{Mathf.RoundToInt(at * 10):00}");
            }
            while (BootTitle.Current && Time.realtimeSinceStartup - c0 < 6) yield return null;
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("x_sanh");
            Debug.Log($"[Màn mở game] Chụp xong: {PlayTour.ShotDir}/boot_*.png");
        }

        static IEnumerator Shot(string name)
        {
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(PlayTour.ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(PlayTour.ShotDir, $"boot_{name}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
        }
    }
}

