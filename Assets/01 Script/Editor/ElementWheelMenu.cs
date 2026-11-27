// Hộp Tương khắc và nút icon vòng 5 chấm ở ô tướng (người dùng dặn 2026-11-27: FTUE phải cho người chơi biết khắc hệ quan trọng với
// chiến thuật; ô tướng có icon chạm mở popup tương khắc). Menu "PokiClash/Prefab/Hộp thoại và màn/Tương khắc: hộp và icon ô tướng", hoặc
// cờ Temp/tuong_khac_build.flag (dựng khi Unity không Play, biên dịch xong). Chạy lại thì dựng lại, giữ đường dẫn nên GUID và chỗ trỏ trong
// UiKit.dialogs giữ nguyên.
// - Dialogs/TuongKhac (ElementWheelDialog) = bản sao tờ giấy gốc Dialogs/HopThoai rộng 980, cỡ cố định: băng tiêu đề nâu sẫm chữ kem viền
//   mực, dòng tướng; vòng 5 hệ (đĩa tròn màu hệ, icon hệ, vòng sáng, tên hệ) và 5 mũi tên cung (nét mực dưới, nét màu trên); hai dòng
//   KHẮC / BỊ KHẮC (nền, viên nhãn, icon hệ → icon hệ, chữ hệ số); câu chiến thuật; nút "Hiểu rồi!" (chỉ hiện ở bài học).
// - Nút tròn giấy "nut_tuong_khac" (kit.buttonRound, icon Fallback/Icons/tuong_khac.png) vào: Items/TheTuong (góc trên phải),
//   Items/OChonDoi (đáy phải dải hệ), Dialogs/ChiTietTuong (bên phải nhãn hệ, sau huy hiệu), Dialogs/ChonTuongKhoiDau (cuối hàng tên).
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
    public static class ElementWheelMenu
    {
        const string SheetBase = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string DialogPath = "Assets/04 Prefabs/Dialogs/TuongKhac.prefab";
        const string IconPath = "Assets/03 Art/Fallback/Icons/tuong_khac.png";
        const string TilePath = "Assets/04 Prefabs/Items/TheTuong.prefab";
        const string CellPath = "Assets/04 Prefabs/Items/OChonDoi.prefab";
        const string DetailPath = "Assets/04 Prefabs/Dialogs/ChiTietTuong.prefab";
        const string StarterPath = "Assets/04 Prefabs/Dialogs/ChonTuongKhoiDau.prefab";
        const string BtnName = "nut_tuong_khac";

        // tờ giấy: rộng, cao khi có nút "Hiểu rồi!" và khi không; vòng: tâm (từ đỉnh tờ), bán kính, cỡ đĩa
        // (2026-11-27 sửa sau khi người dùng soi: câu chiến thuật lòi ra dưới tờ giấy khi không có nút; tên hệ hai bên bị mũi tên đè)
        const float SheetW = 980, FullH = 1472, OkH = 146;
        const float WheelY = -585, R = 245, Disk = 116, RingSize = 146, IconSize = 78, LabelOut = 46;
        const float RowW = 880, RowH = 124, Row1Y = -912, Row2Y = -1050, TipY = -1190, TipH = 100, OkY = -1312;

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Tương khắc: hộp và icon ô tướng", priority = 68)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            var art = Load<ArtLibrary>();
            if (!assets || !art)
            {
                Debug.LogError("[Tương khắc] thiếu UiAssets / ArtLibrary");
                return;
            }
            Theme.Init(assets);
            var kit = assets.prefabs;
            if (!kit.buttonRound || !kit.buttonBig)
            {
                Debug.LogError("[Tương khắc] UiKit thiếu nút tròn / nút to");
                return;
            }
            var icon = AssetDatabase.LoadAssetAtPath<Sprite>(IconPath);
            if (!icon)
            {
                Debug.LogError("[Tương khắc] chưa nhập icon " + IconPath);
                return;
            }
            BuildDialog(kit, art);
            Edit(TilePath, root => PatchTile(root, kit, icon));
            Edit(CellPath, root => PatchCell(root, kit, icon));
            Edit(DetailPath, root => PatchDetail(root, kit, icon));
            Edit(StarterPath, root => PatchStarter(root, kit, icon));
            AssetDatabase.SaveAssets();
            Debug.Log($"[Tương khắc] Đã dựng {DialogPath} (UiKit.dialogs) và nút {BtnName} ở TheTuong, OChonDoi, ChiTietTuong, ChonTuongKhoiDau.");
        }

        // ---------- hộp ----------

        static void BuildDialog(UiKit kit, ArtLibrary art)
        {
            var title = Theme.Outlined(Theme.Title, 0.22f);
            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetBase));
            try
            {
                root.name = "TuongKhac";
                var view = root.GetComponent<ModalSheet>();
                view.Configure(SheetW, false, false);
                var sheet = view.Sheet;
                foreach (var f in sheet.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(f);
                foreach (var l in sheet.GetComponents<LayoutGroup>()) Object.DestroyImmediate(l);
                sheet.anchorMin = sheet.anchorMax = new Vector2(0.5f, 0.5f);
                sheet.pivot = new Vector2(0.5f, 0.5f);
                sheet.anchoredPosition = Vector2.zero;
                sheet.sizeDelta = new Vector2(SheetW, FullH - OkH);
                var page = HomeSceneMenu.Fill(HomeSceneMenu.Node(sheet, "noi_dung"));
                page.SetAsLastSibling();
                var top = new Vector2(0.5f, 1);

                // băng tiêu đề: viên nâu sẫm, chữ kem viền mực (không dùng chữ mực đậm làm tiêu đề, người dùng dặn 2026-11-27)
                var band = HomeSceneMenu.Img(page, "bang_tieu_de", Sketch.Pill, Theme.Ink2, false, true);
                band.pixelsPerUnitMultiplier = 1.4f;
                HomeSceneMenu.At(band.rectTransform, top, new Vector2(0, -30), new Vector2(560, 100), top);
                var titleText = T(band.transform, "chu", 60, Theme.Paper, new Vector2(0.5f, 0.5f), new Vector2(0, 2), new Vector2(520, 90),
                    new Vector2(0.5f, 0.5f), TextAlignmentOptions.Center);
                titleText.font = Theme.Title;
                if (title) titleText.fontSharedMaterial = title;
                titleText.text = "Tương khắc";
                var sub = T(page, "dong_tuong", 38, Theme.Ink2, top, new Vector2(0, -142), new Vector2(860, 50), top, TextAlignmentOptions.Center);
                sub.font = Theme.Body;
                sub.fontSharedMaterial = Theme.Body ? Theme.Body.material : sub.fontSharedMaterial;
                sub.text = ""; // chữ điền lúc chạy; chữ mẫu trong prefab cũng phải có bản dịch (LocTests) nên để trống

                // vòng 5 hệ: mũi tên nằm dưới đĩa
                var wheel = HomeSceneMenu.Node(page, "vong");
                HomeSceneMenu.At(wheel, top, new Vector2(0, WheelY), new Vector2(2 * R + RingSize, 2 * R + RingSize), new Vector2(0.5f, 0.5f));
                var order = ElementWheelDialog.Order;
                int n = order.Length;
                var arrows = new ElementWheelDialog.Arrow[n];
                var arrowRoot = HomeSceneMenu.Node(wheel, "mui_ten");
                HomeSceneMenu.Fill(arrowRoot);
                for (int i = 0; i < n; i++) arrows[i] = Arrow(arrowRoot, i, n);
                var nodes = new ElementWheelDialog.Node[n];
                for (int i = 0; i < n; i++) nodes[i] = WheelNode(wheel, art, order[i], i, n);

                // hai dòng quan hệ và câu chiến thuật (hiện sau khi vẽ xong vòng)
                var rowsGo = HomeSceneMenu.Node(page, "dong_quan_he", typeof(CanvasGroup));
                HomeSceneMenu.Fill(rowsGo);
                var beat = RelRow(rowsGo, "dong_khac", Row1Y, title);
                var beaten = RelRow(rowsGo, "dong_bi_khac", Row2Y, title);
                var tip = T(rowsGo, "cau_chien_thuat", 36, Theme.Ink2, top, new Vector2(0, TipY), new Vector2(880, TipH), top,
                    TextAlignmentOptions.Center);
                tip.font = Theme.Body;
                tip.fontSharedMaterial = Theme.Body ? Theme.Body.material : tip.fontSharedMaterial;
                tip.enableAutoSizing = true;
                tip.fontSizeMin = 26;
                tip.textWrappingMode = TextWrappingModes.Normal;
                tip.text = "";

                var ok = Btn(kit.buttonBig, page, "nut_hieu_roi", "", BtnColor.Green, top, new Vector2(0, OkY), new Vector2(440, 124), top);

                var dlg = root.AddComponent<ElementWheelDialog>();
                dlg.Setup(new ElementWheelDialog.Parts
                {
                    title = titleText, sub = sub, tip = tip, nodes = nodes, arrows = arrows, beat = beat, beaten = beaten,
                    rows = rowsGo.GetComponent<CanvasGroup>(), ok = ok, sheet = sheet, fullH = FullH, shortH = FullH - OkH,
                });
                var saved = PrefabUtility.SaveAsPrefabAsset(root, DialogPath).GetComponent<ElementWheelDialog>();
                if (!kit.dialogs.Any(x => x is ElementWheelDialog))
                {
                    kit.dialogs.Add(saved);
                    EditorUtility.SetDirty(kit);
                }
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        // góc của hệ thứ i trên vòng (độ, 0 = phải, tăng ngược chiều kim đồng hồ): hệ 0 ở đỉnh, các hệ sau theo chiều kim đồng hồ
        static float Angle(int i, int n) => 90f - 360f / n * i;

        static Vector2 OnRing(float deg, float r) => new Vector2(r * Mathf.Cos(deg * Mathf.Deg2Rad), r * Mathf.Sin(deg * Mathf.Deg2Rad));

        static ElementWheelDialog.Node WheelNode(RectTransform wheel, ArtLibrary art, Elem e, int i, int n)
        {
            var c = new Vector2(0.5f, 0.5f);
            var root = HomeSceneMenu.Node(wheel, "he_" + Keys.Of(e));
            HomeSceneMenu.At(root, c, OnRing(Angle(i, n), R), new Vector2(Disk, Disk), c);
            var ring = HomeSceneMenu.Img(root, "vong_sang", Sketch.Ring360 ? Sketch.Ring360 : Sketch.Ring, Theme.Yellow);
            HomeSceneMenu.At(ring.rectTransform, c, Vector2.zero, new Vector2(RingSize, RingSize), c);
            var disk = HomeSceneMenu.Img(root, "dia", Sketch.Round, Color.Lerp(Theme.Of(e), Color.white, 0.55f));
            HomeSceneMenu.At(disk.rectTransform, c, Vector2.zero, new Vector2(Disk, Disk), c);
            var ic = HomeSceneMenu.Img(root, "icon", art.Icon(ElementWheelDialog.IconOf(e)), Color.white);
            ic.preserveAspect = true;
            HomeSceneMenu.At(ic.rectTransform, c, new Vector2(0, 2), new Vector2(IconSize, IconSize), c);
            // tên hệ nằm phía ngoài vòng theo hướng từ tâm ra (mũi tên chạy trên vòng nên không đè chữ)
            var dir = OnRing(Angle(i, n), 1);
            var label = T(root, "ten", 34, Theme.Ink, c, dir * (RingSize / 2 + LabelOut), new Vector2(160, 44), c, TextAlignmentOptions.Center);
            label.text = Elements.NameVi(e);
            return new ElementWheelDialog.Node { root = root, disk = disk, icon = ic, ring = ring, label = label };
        }

        // mũi tên cung từ hệ i tới hệ i + 1 (chiều kim đồng hồ): thân cung tránh hai đĩa, đầu chữ V ở cuối; nét mực to dưới, nét màu trên
        static ElementWheelDialog.Arrow Arrow(RectTransform parent, int i, int n)
        {
            float gap = (RingSize / 2 + 10) / R * Mathf.Rad2Deg; // độ bỏ ra ở mỗi đầu để không đè đĩa (kể cả vòng sáng)
            float a0 = Angle(i, n) - gap, a1 = Angle(i + 1, n) + gap;
            const int steps = 18;
            var pts = new System.Collections.Generic.List<Vector2>();
            for (int k = 0; k <= steps; k++) pts.Add(OnRing(Mathf.Lerp(a0, a1, k / (float)steps), R));
            // đầu chữ V: hai cánh dài 34 lệch ±34° so với hướng ngược tiếp tuyến ở mũi
            var tip = pts[pts.Count - 1];
            var dir = (tip - pts[pts.Count - 2]).normalized;
            float head = 34, spread = 34 * Mathf.Deg2Rad;
            Vector2 back = -dir;
            Vector2 W(float s) => tip + head * new Vector2(back.x * Mathf.Cos(s) - back.y * Mathf.Sin(s), back.x * Mathf.Sin(s) + back.y * Mathf.Cos(s));
            pts.Add(W(spread));
            pts.Add(tip);
            pts.Add(W(-spread));
            var go = HomeSceneMenu.Node(parent, "mui_" + i);
            HomeSceneMenu.Fill(go);
            var ink = Path(go, "muc", pts.ToArray(), 22, Theme.Ink);
            var fill = Path(go, "mau", pts.ToArray(), 11, ElementWheelDialog.Other);
            return new ElementWheelDialog.Arrow { ink = ink, fill = fill };
        }

        static InkPath Path(RectTransform parent, string name, Vector2[] pts, float w, Color c)
        {
            var p = HomeSceneMenu.Node(parent, name, typeof(CanvasRenderer), typeof(InkPath)).GetComponent<InkPath>();
            HomeSceneMenu.Fill(p.rectTransform);
            p.Setup(pts, w);
            p.color = c;
            p.raycastTarget = false;
            return p;
        }

        // một dòng KHẮC / BỊ KHẮC: nền giấy mỏng, viên nhãn chữ trắng viền mực, icon hệ → icon hệ, chữ hệ số hai dòng
        static ElementWheelDialog.Row RelRow(RectTransform parent, string name, float y, Material outline)
        {
            var top = new Vector2(0.5f, 1);
            var left = new Vector2(0, 0.5f);
            var bg = HomeSceneMenu.Img(parent, name, Sketch.PanelThin, Theme.Paper2, false, true);
            HomeSceneMenu.At(bg.rectTransform, top, new Vector2(0, y), new Vector2(RowW, RowH), top);
            var pill = HomeSceneMenu.Img(bg.transform, "nhan", Sketch.Pill, ElementWheelDialog.Good, false, true);
            pill.pixelsPerUnitMultiplier = 1.8f;
            HomeSceneMenu.At(pill.rectTransform, left, new Vector2(24, 0), new Vector2(214, 62), left);
            var tag = T(pill.transform, "chu", 36, Color.white, new Vector2(0.5f, 0.5f), new Vector2(0, 1), new Vector2(196, 56),
                new Vector2(0.5f, 0.5f), TextAlignmentOptions.Center);
            tag.font = Theme.Title;
            if (outline) tag.fontSharedMaterial = outline;
            tag.text = "";
            var from = HomeSceneMenu.Img(bg.transform, "he_trai", null, Color.white);
            from.preserveAspect = true;
            HomeSceneMenu.At(from.rectTransform, left, new Vector2(258, 0), new Vector2(80, 80), left);
            // mũi tên nhỏ giữa hai icon
            var arrow = HomeSceneMenu.Node(bg.transform, "mui_ten");
            HomeSceneMenu.At(arrow, left, new Vector2(346, 0), new Vector2(64, 40), left);
            var pts = new[] { new Vector2(-24, 0), new Vector2(22, 0), new Vector2(8, 13), new Vector2(22, 0), new Vector2(8, -13) };
            Path(arrow, "muc", pts, 9, Theme.Ink);
            var to = HomeSceneMenu.Img(bg.transform, "he_phai", null, Color.white);
            to.preserveAspect = true;
            HomeSceneMenu.At(to.rectTransform, left, new Vector2(418, 0), new Vector2(80, 80), left);
            var text = T(bg.transform, "he_so", 38, Theme.Ink, left, new Vector2(522, 0), new Vector2(RowW - 540, RowH - 12), left,
                TextAlignmentOptions.MidlineLeft);
            text.font = Theme.Body;
            text.fontSharedMaterial = Theme.Body ? Theme.Body.material : text.fontSharedMaterial;
            text.textWrappingMode = TextWrappingModes.Normal;
            text.richText = true;
            text.lineSpacing = -6;
            text.text = "";
            return new ElementWheelDialog.Row { bg = bg, pill = pill, from = from, to = to, tag = tag, text = text };
        }

        // ---------- nút ở ô tướng ----------

        // nút tròn giấy có icon vòng 5 chấm; size: cạnh nút, icon chiếm 74%
        static SketchButton Wheel(UiKit kit, Transform parent, Sprite icon, float size)
        {
            var old = parent.Find(BtnName);
            if (old) Object.DestroyImmediate(old.gameObject);
            var b = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonRound.gameObject, parent)).GetComponent<SketchButton>();
            b.name = BtnName;
            b.SetRole(BtnColor.Paper);
            b.SetText("");
            b.Rect.sizeDelta = new Vector2(size, size);
            var img = HomeSceneMenu.Img(b.transform, "icon", icon, Color.white);
            img.preserveAspect = true;
            var c = new Vector2(0.5f, 0.5f);
            HomeSceneMenu.At(img.rectTransform, c, Vector2.zero, new Vector2(size * 0.74f, size * 0.74f), c);
            return b;
        }

        // thẻ màn Tướng (308 x 412): góc trên phải trong giấy, dưới chấm đỏ góc thẻ
        static void PatchTile(GameObject root, UiKit kit, Sprite icon)
        {
            var tile = root.GetComponent<HeroTile>();
            var so = new SerializedObject(tile);
            var card = (Image)so.FindProperty("p.card").objectReferenceValue;
            var parent = card ? card.transform : root.transform;
            var b = Wheel(kit, parent, icon, 68);
            HomeSceneMenu.At(b.Rect, new Vector2(1, 1), new Vector2(-60, -64), new Vector2(68, 68), new Vector2(0.5f, 0.5f));
            b.transform.SetAsLastSibling();
            // chấm đỏ (nếu có) vẫn trên cùng
            var alert = (Image)so.FindProperty("p.alert").objectReferenceValue;
            if (alert && alert.transform.parent == b.transform.parent) alert.transform.SetAsLastSibling();
            tile.SetupWheel(b);
            EditorUtility.SetDirty(tile);
        }

        // ô hộp chọn đội (154 x 222): đáy phải của dải hệ, dưới mũi tên khắc ở góc
        static void PatchCell(GameObject root, UiKit kit, Sprite icon)
        {
            var cell = root.GetComponent<PrepRosterCell>();
            var b = Wheel(kit, root.transform, icon, 48);
            HomeSceneMenu.At(b.Rect, new Vector2(1, 1), new Vector2(-28, -106), new Vector2(48, 48), new Vector2(0.5f, 0.5f));
            b.transform.SetAsLastSibling();
            var arrow = root.transform.Find("khac");
            if (arrow) arrow.SetAsLastSibling();
            cell.SetupWheel(b);
            EditorUtility.SetDirty(cell);
        }

        // hộp chi tiết tướng: con của nhãn hệ, bên phải (chừa chỗ huy hiệu hệ cạnh nhãn)
        static void PatchDetail(GameObject root, UiKit kit, Sprite icon)
        {
            var dlg = root.GetComponent<HeroDetailDialog>();
            var so = new SerializedObject(dlg);
            var tag = (UiElemTag)so.FindProperty("p.elemTag").objectReferenceValue;
            if (!tag)
            {
                Debug.LogError("[Tương khắc] ChiTietTuong thiếu nhãn hệ");
                return;
            }
            var b = Wheel(kit, tag.transform, icon, 56);
            HomeSceneMenu.At(b.Rect, new Vector2(1, 0.5f), new Vector2(64, 0), new Vector2(56, 56), new Vector2(0.5f, 0.5f));
            dlg.SetupWheel(b);
            EditorUtility.SetDirty(dlg);
        }

        // hộp chọn tướng khởi đầu: cuối hàng tên (hàng ngang căn giữa: icon hệ, tên, nút)
        static void PatchStarter(GameObject root, UiKit kit, Sprite icon)
        {
            var dlg = root.GetComponent<StarterDialog>();
            var so = new SerializedObject(dlg);
            var name = (TextMeshProUGUI)so.FindProperty("p.name").objectReferenceValue;
            if (!name)
            {
                Debug.LogError("[Tương khắc] ChonTuongKhoiDau thiếu chữ tên");
                return;
            }
            var row = name.transform.parent;
            var b = Wheel(kit, row, icon, 72);
            if (!b.TryGetComponent<LayoutElement>(out var le)) le = b.gameObject.AddComponent<LayoutElement>();
            le.preferredWidth = le.preferredHeight = 72;
            le.minWidth = le.minHeight = 72;
            b.transform.SetAsLastSibling();
            dlg.SetupWheel(b);
            EditorUtility.SetDirty(dlg);
        }

        // ---------- chung ----------

        static void Edit(string path, System.Action<GameObject> patch)
        {
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                patch(root);
                PrefabUtility.SaveAsPrefabAsset(root, path);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static TextMeshProUGUI T(Transform p, string n, float size, Color c, Vector2 anchor, Vector2 pos, Vector2 box, Vector2 pivot,
            TextAlignmentOptions align = TextAlignmentOptions.MidlineLeft)
        {
            var t = HomeSceneMenu.Text(p, n, size, c, align);
            HomeSceneMenu.At(t.rectTransform, anchor, pos, box, pivot);
            t.enableAutoSizing = true;
            t.fontSizeMin = size * 0.6f;
            t.fontSizeMax = size;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            return t;
        }

        static SketchButton Btn(SketchButton prefab, Transform parent, string name, string label, BtnColor color, Vector2 anchor, Vector2 pos,
            Vector2 size, Vector2 pivot)
        {
            var b = ((GameObject)PrefabUtility.InstantiatePrefab(prefab.gameObject, parent)).GetComponent<SketchButton>();
            b.name = name;
            b.SetRole(color);
            b.SetText(label);
            HomeSceneMenu.At(b.Rect, anchor, pos, size, pivot);
            if (b.Label)
            {
                b.Label.enableAutoSizing = true;
                b.Label.fontSizeMax = b.Label.fontSize;
                b.Label.fontSizeMin = b.Label.fontSize * 0.6f;
                b.Label.textWrappingMode = TextWrappingModes.NoWrap;
            }
            return b;
        }

        // ---------- cờ ----------

        static double nextPoll;
        static string Flag(string n) => System.IO.Path.GetFullPath(System.IO.Path.Combine(Application.dataPath, "../Temp/" + n));

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            var build = Flag("tuong_khac_build.flag");
            if (!File.Exists(build)) return;
            File.Delete(build);
            Build();
        }
    }
}
