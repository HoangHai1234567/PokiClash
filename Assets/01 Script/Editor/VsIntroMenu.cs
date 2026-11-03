// Màn VS đầu trận kiểu trang truyện tranh (người dùng chốt 2026-11-03). Menu "PokiClash/Prefab/Trận: màn VS truyện tranh" dựng
// (chạy lại thì dựng lại):
// - Items/TranVsMat (VsFace): ô mặt 300 × 300: khung giấy viền mực, mặt hoặc chân dung trong ô có mặt nạ, nhãn BOSS, ô tên đè mép dưới;
// - Screens/Battle: dựng lại con của nút VS (BattleIntro, trong lớp phủ, tắt sẵn): nền giấy (khe giữa hai khung, nhận chạm bỏ qua),
//   phe địch và phe mình (viền mực, lòng khung có mặt nạ chứa nền ảnh và tia, hàng mặt, viên lực chiến), khung lời dẫn (phe địch),
//   khối VS (hình nổ, chữ, ảnh vẽ tay). Hình khung và chỗ đặt BattleIntro tính lúc chạy theo cỡ màn;
// - Screens/Battle: nút "tuyet_ky" (UltCutIn) cạnh màn VS: khung truyện cắt thành dải hình bình hành ngang sân khi ra tuyệt kỹ (giấy,
//   viền mực, lòng khung có mặt nạ chứa nền, tia, mặt tướng; lời dẫn, tên tuyệt kỹ); gán BattleView.p.ultCut;
// - đo hộp phần có hình của mọi chân dung aola (PortraitBoxes, Resources/BattleIntro/khung_chan_dung): ô mặt và dải tuyệt kỹ phóng
//   chân dung theo đó khi tướng chưa có ảnh mặt. Nhập thêm tướng thì chạy lại menu.
using System.IO;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class VsIntroMenu
    {
        const string FacePath = "Assets/04 Prefabs/Items/TranVsMat.prefab";
        const string BattlePath = "Assets/04 Prefabs/Screens/Battle.prefab";
        const string BoxesDir = "Assets/03 Art/BattleIntro/Resources/BattleIntro";

        static ArtLibrary art;

        [MenuItem("PokiClash/Prefab/Trận: màn VS truyện tranh", priority = 67)]
        static void Build()
        {
            var assets = Load<UiAssets>();
            art = Load<ArtLibrary>();
            Theme.Init(assets); // phông, sprite giấy, viền chữ nướng sẵn
            BakeBoxes();
            var face = BuildFace(assets.prefabs);
            var root = PrefabUtility.LoadPrefabContents(BattlePath);
            try
            {
                var intro = root.GetComponentInChildren<BattleIntro>(true);
                if (!intro)
                {
                    Debug.LogError("[VS] Không thấy BattleIntro trong " + BattlePath);
                    return;
                }
                BuildIntro(intro, face);
                var ult = BuildUlt(intro.transform.parent, assets.prefabs);
                var view = root.GetComponentInChildren<BattleView>(true);
                var so = new SerializedObject(view);
                so.FindProperty("p.ultCut").objectReferenceValue = ult;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(root, BattlePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            AssetDatabase.SaveAssets();
            Debug.Log($"[VS] Đã dựng {FacePath} và màn VS trong {BattlePath}.");
        }

        static T Load<T>() where T : Object =>
            AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:" + typeof(T).Name)[0]));

        // ---------- hộp hình chân dung ----------

        // đo hộp phần có hình (alpha ≥ 40) của mọi chân dung aola, 0..1 theo khung ảnh, gốc dưới trái
        static void BakeBoxes()
        {
            Folder(BoxesDir);
            var path = $"{BoxesDir}/{Path.GetFileName(PortraitBoxes.Res)}.asset";
            var asset = AssetDatabase.LoadAssetAtPath<PortraitBoxes>(path);
            if (!asset)
            {
                asset = ScriptableObject.CreateInstance<PortraitBoxes>();
                AssetDatabase.CreateAsset(asset, path);
            }
            asset.entries.Clear();
            var tex = new Texture2D(2, 2);
            foreach (var file in Directory.GetFiles(AolaImport.ResDir, "*_portrait.png", SearchOption.AllDirectories))
            {
                tex.LoadImage(File.ReadAllBytes(file));
                var px = tex.GetPixels32();
                int w = tex.width, h = tex.height, x0 = w, y0 = h, x1 = -1, y1 = -1;
                for (int y = 0; y < h; y++)
                for (int x = 0; x < w; x++)
                {
                    if (px[y * w + x].a < 40) continue;
                    x0 = Mathf.Min(x0, x);
                    x1 = Mathf.Max(x1, x);
                    y0 = Mathf.Min(y0, y);
                    y1 = Mathf.Max(y1, y);
                }
                if (x1 < 0) continue;
                asset.entries.Add(new PortraitBoxes.Entry
                {
                    aola = Path.GetFileName(Path.GetDirectoryName(file)),
                    box = Rect.MinMaxRect(x0 / (float)w, y0 / (float)h, (x1 + 1) / (float)w, (y1 + 1) / (float)h),
                });
            }
            Object.DestroyImmediate(tex);
            EditorUtility.SetDirty(asset);
            AssetDatabase.SaveAssets();
            Debug.Log($"[VS] Đo hộp hình {asset.entries.Count} chân dung -> {path}");
        }

        static void Folder(string path)
        {
            if (AssetDatabase.IsValidFolder(path)) return;
            var parent = Path.GetDirectoryName(path).Replace('\\', '/');
            Folder(parent);
            AssetDatabase.CreateFolder(parent, Path.GetFileName(path));
        }

        // ---------- ô mặt ----------

        static VsFace BuildFace(UiKit kit)
        {
            var root = new GameObject("TranVsMat", typeof(RectTransform));
            try
            {
                var rt = (RectTransform)root.transform;
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(VsFace.Size, VsFace.Size);

                var frame = Img(rt, "vien", Sketch.PanelThin, Theme.CardFill, true);
                frame.rectTransform.Stretch();
                var mask = Node(rt, "khung", typeof(RectMask2D));
                mask.Stretch(12, 12, 12, 12);
                var hinh = Node(mask, "hinh");
                hinh.Stretch();
                var face = Img(hinh, "mat", null, Color.white);
                face.rectTransform.Stretch();
                face.gameObject.SetActive(false);
                var por = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, hinh)).GetComponent<HeroPortrait>();
                por.name = "chan_dung";
                var prt = por.Rect;
                prt.anchorMin = prt.anchorMax = new Vector2(0.5f, 0);
                prt.pivot = new Vector2(0.5f, 0); // gốc ở chân
                foreach (var g in por.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;

                // nhãn BOSS góc trên trái, nghiêng
                var boss = Img(rt, "boss", Sketch.Pill, Theme.Red, true);
                boss.rectTransform.Place(new Vector2(0, 1), new Vector2(-14, 18), new Vector2(124, 52), new Vector2(0, 1));
                boss.rectTransform.localEulerAngles = new Vector3(0, 0, 8);
                var bt = Text(boss.rectTransform, "chu", Theme.Title, 32, Color.white, TextAlignmentOptions.Center, 0.28f);
                bt.rectTransform.Stretch();
                bt.text = "BOSS";
                boss.gameObject.SetActive(false);

                // ô tên đè mép dưới khung, tự co theo chữ
                var cap = Img(rt, "ten", Sketch.PanelThin, Theme.CardFill, true);
                var crt = cap.rectTransform;
                crt.Place(new Vector2(0.5f, 0), new Vector2(0, 24), new Vector2(200, 52), new Vector2(0.5f, 1));
                var hl = cap.gameObject.AddComponent<HorizontalLayoutGroup>();
                hl.padding = new RectOffset(18, 18, 6, 9);
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = true;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                var fit = cap.gameObject.AddComponent<ContentSizeFitter>();
                fit.horizontalFit = fit.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
                var label = Text(crt, "chu", Theme.Bold, 32, Theme.Ink, TextAlignmentOptions.Center);
                label.text = "Tên Lv1";

                var vf = root.AddComponent<VsFace>();
                vf.Setup(frame, hinh, face, por, boss.gameObject, label);
                var saved = PrefabUtility.SaveAsPrefabAsset(root, FacePath).GetComponent<VsFace>();
                Debug.Log("[VS] Dựng " + FacePath);
                return saved;
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // ---------- màn VS ----------

        static void BuildIntro(BattleIntro intro, VsFace face)
        {
            var rt = (RectTransform)intro.transform;
            for (int i = rt.childCount - 1; i >= 0; i--) Object.DestroyImmediate(rt.GetChild(i).gameObject);
            rt.Stretch();
            var cg = intro.GetComponent<CanvasGroup>();
            if (!cg) cg = intro.gameObject.AddComponent<CanvasGroup>();

            var page = Img(rt, "giay", null, Theme.Paper);
            page.rectTransform.Stretch();
            page.raycastTarget = true; // chạm để bỏ qua (BattleIntro.OnPointerClick)

            var foe = BuildSide(rt, "phe_dich", new Vector2(1, 1));
            var mine = BuildSide(rt, "phe_ta", new Vector2(0, 0));

            // khung lời dẫn vàng góc trên trái (đi theo phe địch): đảo · ải, tên ải
            var cap = Img(foe.root, "loi_dan", Sketch.PanelThin, Theme.Yellow, true);
            var crt = cap.rectTransform;
            crt.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(400, 120), new Vector2(0, 1));
            crt.localEulerAngles = new Vector3(0, 0, 1.5f);
            var vl = cap.gameObject.AddComponent<VerticalLayoutGroup>();
            vl.padding = new RectOffset(26, 30, 12, 16);
            vl.spacing = -4;
            vl.childAlignment = TextAnchor.UpperLeft;
            vl.childControlWidth = vl.childControlHeight = true;
            vl.childForceExpandWidth = vl.childForceExpandHeight = false;
            var fit = cap.gameObject.AddComponent<ContentSizeFitter>();
            fit.horizontalFit = fit.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            var title = Text(crt, "dao_ai", Theme.Bold, 34, Theme.Ink2, TextAlignmentOptions.Left);
            title.text = "Đảo Thủy · Ải 5";
            var sub = Text(crt, "ten_ai", Theme.Title, 54, Theme.Ink, TextAlignmentOptions.Left);
            sub.text = "Vũng San Hô";

            // khối VS giữa khe
            var vs = Node(rt, "vs");
            vs.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(420, 294));
            var burst = Img(vs, "no", Sketch.Burst, Theme.Yellow);
            burst.preserveAspect = false;
            burst.rectTransform.Stretch();
            var vsText = Text(vs, "chu", Theme.Title, 150, Theme.Red, TextAlignmentOptions.Center, 0.3f);
            vsText.rectTransform.Stretch(0, 0, 0, 16);
            vsText.characterSpacing = -6;
            vsText.text = "VS";
            var vsArt = Img(vs, "anh", null, Color.white);
            vsArt.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(430, 430)); // ảnh vẽ tay: to cỡ hình nổ tạm
            vsArt.gameObject.SetActive(false);

            intro.Setup(cg, page, mine, foe, crt, title, sub, vs, burst, vsText, vsArt, face);
            intro.gameObject.SetActive(false);
        }

        // ---------- dải tuyệt kỹ ----------

        // nút "tuyet_ky" (UltCutIn) trong lớp phủ, cạnh màn VS: dải (giấy, viền mực, lòng khung có mặt nạ chứa nền, tia, mặt), chữ
        static UltCutIn BuildUlt(Transform overlay, UiKit kit)
        {
            var old = overlay.GetComponentInChildren<UltCutIn>(true);
            if (old) Object.DestroyImmediate(old.gameObject);
            var root = Node(overlay, "tuyet_ky");
            root.Stretch();
            var band = Node(root, "dai");
            band.Place(new Vector2(0.5f, 0.5f), Vector2.zero, Vector2.zero);
            var paper = Poly(band, "giay", Theme.Paper);
            var ink = Poly(band, "vien", Theme.Ink);
            var panel = Poly(band, "khung", Color.white);
            panel.gameObject.AddComponent<Mask>().showMaskGraphic = true;
            var rays = Node(panel.transform, "tia", typeof(RayGraphic)).GetComponent<RayGraphic>();
            rays.raycastTarget = false;
            var art = Img(panel.transform, "nen", null, Color.white);
            art.preserveAspect = false;
            art.gameObject.SetActive(false);
            var faceBox = Node(panel.transform, "mat");
            faceBox.Place(new Vector2(0.5f, 0.5f), Vector2.zero, Vector2.zero);
            var face = Img(faceBox, "anh", null, Color.white);
            face.preserveAspect = true;
            face.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(470, 470));
            face.gameObject.SetActive(false);
            var por = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, faceBox)).GetComponent<HeroPortrait>();
            por.name = "chan_dung";
            por.Rect.anchorMin = por.Rect.anchorMax = new Vector2(0.5f, 0);
            por.Rect.pivot = new Vector2(0.5f, 0); // gốc ở chân
            foreach (var g in por.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;

            // chữ: khung lời dẫn vàng "Tuyệt kỹ · tên tướng" trên, tên tuyệt kỹ chữ to viền mực dưới
            var text = Node(band, "chu");
            text.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(560, 240));
            text.localEulerAngles = new Vector3(0, 0, 3);
            var cap = Img(text, "loi_dan", Sketch.PanelThin, Theme.Yellow, true);
            var crt = cap.rectTransform;
            crt.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 26), new Vector2(300, 56), new Vector2(0.5f, 0));
            var hl = cap.gameObject.AddComponent<HorizontalLayoutGroup>();
            hl.padding = new RectOffset(20, 22, 6, 9);
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.childControlWidth = hl.childControlHeight = true;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            var fit = cap.gameObject.AddComponent<ContentSizeFitter>();
            fit.horizontalFit = fit.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            var caption = Text(crt, "chu", Theme.Bold, 34, Theme.Ink, TextAlignmentOptions.Center);
            caption.text = "Tuyệt kỹ · Tên tướng";
            var skill = Text(text, "ten_chieu", Theme.Title, 84, Color.white, TextAlignmentOptions.Center, 0.32f);
            skill.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, 16), new Vector2(560, 120), new Vector2(0.5f, 1));
            skill.enableAutoSizing = true;
            skill.fontSizeMin = 44;
            skill.fontSizeMax = 84;
            skill.text = "Tên Tuyệt Kỹ";

            var u = root.gameObject.AddComponent<UltCutIn>();
            u.Setup(band, paper, ink, panel, art, rays, faceBox, face, por, text, crt, caption, skill);
            root.gameObject.SetActive(false);
            return u;
        }

        static PolyGraphic Poly(Transform parent, string name, Color color)
        {
            var g = Node(parent, name, typeof(PolyGraphic)).GetComponent<PolyGraphic>();
            g.color = color;
            g.raycastTarget = false;
            return g;
        }

        // một phe: viền mực, lòng khung (Mask) chứa nền ảnh và tia, hàng mặt, viên lực chiến (pivot theo góc đặt)
        static BattleIntro.Side BuildSide(RectTransform parent, string name, Vector2 powerPivot)
        {
            var s = new BattleIntro.Side { root = Node(parent, name) };
            s.root.Stretch();
            s.ink = Node(s.root, "vien", typeof(PolyGraphic)).GetComponent<PolyGraphic>();
            s.ink.color = Theme.Ink;
            s.ink.raycastTarget = false;
            s.panel = Node(s.root, "khung", typeof(PolyGraphic), typeof(Mask)).GetComponent<PolyGraphic>();
            s.panel.raycastTarget = false;
            s.panel.GetComponent<Mask>().showMaskGraphic = true;
            s.rays = Node(s.panel.transform, "tia", typeof(RayGraphic)).GetComponent<RayGraphic>();
            s.rays.raycastTarget = false;
            s.art = Img(s.panel.transform, "nen", null, Color.white);
            s.art.preserveAspect = false;
            s.art.gameObject.SetActive(false);
            s.row = Node(s.root, "hang");
            s.row.Place(new Vector2(0.5f, 0.5f), Vector2.zero, Vector2.zero);
            s.powerText = PowerPill(s.root, out s.power);
            s.power.pivot = powerPivot;
            return s;
        }

        // viên lực chiến: icon kiếm + số, tự co theo số
        static TextMeshProUGUI PowerPill(Transform parent, out RectTransform row)
        {
            var bg = Img(parent, "luc_chien", Sketch.PanelThin, Theme.CardFill, true);
            row = bg.rectTransform;
            row.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(200, 70));
            var hl = bg.gameObject.AddComponent<HorizontalLayoutGroup>();
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.spacing = 8;
            hl.padding = new RectOffset(16, 22, 6, 8);
            hl.childControlWidth = hl.childControlHeight = true;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;
            var fit = bg.gameObject.AddComponent<ContentSizeFitter>();
            fit.horizontalFit = fit.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            var ic = Img(row, "icon", art ? art.Icon("sword") : null, Color.white);
            var le = ic.gameObject.AddComponent<LayoutElement>();
            le.preferredWidth = le.preferredHeight = 48;
            var t = Text(row, "so", Theme.Title, 48, Theme.Ink, TextAlignmentOptions.MidlineLeft);
            t.text = "0";
            return t;
        }

        // ---------- dựng nút ----------

        static RectTransform Node(Transform parent, string name, params System.Type[] comps)
        {
            var go = new GameObject(name, typeof(RectTransform));
            foreach (var c in comps) go.AddComponent(c);
            go.transform.SetParent(parent, false);
            return (RectTransform)go.transform;
        }

        static Image Img(Transform parent, string name, Sprite sprite, Color color, bool sliced = false)
        {
            var img = Node(parent, name, typeof(Image)).GetComponent<Image>();
            Theme.SetSprite(img, sprite);
            img.type = sliced ? Image.Type.Sliced : Image.Type.Simple;
            img.preserveAspect = !sliced && sprite;
            img.color = color;
            img.raycastTarget = false;
            return img;
        }

        // outline: độ dày viền mực (0,2..0,32, theo material nướng sẵn), 0 là không viền
        static TextMeshProUGUI Text(Transform parent, string name, TMP_FontAsset font, float size, Color color, TextAlignmentOptions align,
            float outline = 0)
        {
            var t = Node(parent, name, typeof(TextMeshProUGUI)).GetComponent<TextMeshProUGUI>();
            t.font = font;
            if (outline > 0)
            {
                var m = Theme.Outlined(font, outline);
                if (m) t.fontSharedMaterial = m;
            }
            t.fontSize = size;
            t.color = color;
            t.alignment = align;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
            t.raycastTarget = false;
            t.text = "";
            return t;
        }
    }
}
