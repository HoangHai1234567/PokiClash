// Dựng phần màn Đảo của đảo 70 ải (chạy lại thì dựng lại):
// - Items/ChamAi (ZonePip): vùng chạm trong suốt, chấm là nút tròn kit (Nut_Tron) không nhận chạm, nhịp ở chấm;
// - Items/DongChang (ZoneChapterRow): khung mỏng kit, số ải, kiểu ải, bi, 3 ô địch (chân dung kit, nhãn), dấu trạng thái;
// - Dialogs/BangChang (ZoneChapterDialog): biến thể tờ giấy gốc HopThoai, tên chặng, dòng phụ, danh sách cuộn, nút Đóng;
// - Screens/Zone: gán pipPrefab, chapterPrefab; thêm rương mốc ruong_2..ruong_6 (chép ruong_1) cho 7 rương của đảo 70 ải.
// Chữ chép phông và viền từ hộp Chuẩn bị trận (ChuanBiTran).
using System.Collections.Generic;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class ZoneLongMenu
    {
        const string ZonePath = "Assets/04 Prefabs/Screens/Zone.prefab";
        const string PrepPath = "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab";
        const string SheetPath = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string PipPath = "Assets/04 Prefabs/Items/ChamAi.prefab";
        const string RowPath = "Assets/04 Prefabs/Items/DongChang.prefab";
        const string ChapterPath = "Assets/04 Prefabs/Dialogs/BangChang.prefab";
        const int Chests = 7;

        [MenuItem("PokiClash/Prefab/Đảo 70 ải (ChamAi, DongChang, BangChang)", priority = 65)]
        static void Build()
        {
            var kit = AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiKit")[0]));
            var pso = new SerializedObject(AssetDatabase.LoadAssetAtPath<GameObject>(PrepPath).GetComponent<StagePrepDialog>());
            var titleTpl = (TextMeshProUGUI)pso.FindProperty("p.title").objectReferenceValue;
            var subTpl = (TextMeshProUGUI)pso.FindProperty("p.sub").objectReferenceValue;
            var hintTpl = (TextMeshProUGUI)pso.FindProperty("p.hint").objectReferenceValue;

            var pip = BuildPip(kit);
            var row = BuildRow(kit, titleTpl, hintTpl);
            var chapter = BuildChapter(kit, titleTpl, subTpl, row);

            var contents = PrefabUtility.LoadPrefabContents(ZonePath);
            try
            {
                var zone = contents.GetComponent<ZoneScene>();
                var so = new SerializedObject(zone);
                so.FindProperty("pipPrefab").objectReferenceValue = pip;
                so.FindProperty("chapterPrefab").objectReferenceValue = chapter;
                // rương mốc: chép ruong_1 tới đủ 7 (vị trí, cỡ đặt lúc chạy theo số ải)
                var chests = so.FindProperty("p.chests");
                var first = chests.GetArrayElementAtIndex(chests.arraySize - 1).FindPropertyRelative("image").objectReferenceValue as Image;
                for (int i = chests.arraySize; i < Chests; i++)
                {
                    var go = Object.Instantiate(first.gameObject, first.transform.parent, false);
                    go.name = "ruong_" + i;
                    chests.InsertArrayElementAtIndex(i);
                    var el = chests.GetArrayElementAtIndex(i);
                    el.FindPropertyRelative("image").objectReferenceValue = go.GetComponent<Image>();
                    el.FindPropertyRelative("click").objectReferenceValue = go.GetComponent<ClickCatcher>();
                    el.FindPropertyRelative("wobble").objectReferenceValue = go.GetComponent<Wobble>();
                }
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, ZonePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
            Debug.Log($"[Đảo] Đã dựng {PipPath}, {RowPath}, {ChapterPath}; gán vào {ZonePath} ({Chests} rương mốc).");
        }

        static ZonePip BuildPip(UiKit kit)
        {
            var root = new GameObject("cham_ai", typeof(RectTransform), typeof(Image), typeof(ClickCatcher), typeof(ZonePip));
            try
            {
                var hit = root.GetComponent<Image>();
                hit.color = new Color(1, 1, 1, 0);
                hit.raycastTarget = true;
                var dot = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonRound.gameObject, root.transform)).GetComponent<SketchButton>();
                dot.name = "cham";
                foreach (var g in dot.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
                dot.SetText("");
                var pulse = dot.gameObject.AddComponent<Pulse>();
                pulse.amount = 0.3f;
                pulse.period = 1.1f;
                pulse.enabled = false;
                root.GetComponent<ZonePip>().Setup(dot, root.GetComponent<ClickCatcher>(), pulse);
                ((RectTransform)root.transform).sizeDelta = new Vector2(ZonePip.Hit, ZonePip.Hit);
                dot.Rect.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(ZonePip.Size, ZonePip.Size));
                return PrefabUtility.SaveAsPrefabAsset(root, PipPath).GetComponent<ZonePip>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        static ZoneChapterRow BuildRow(UiKit kit, TextMeshProUGUI titleTpl, TextMeshProUGUI smallTpl)
        {
            var root = (GameObject)PrefabUtility.InstantiatePrefab(kit.panelThin.gameObject);
            try
            {
                root.name = "dong_chang";
                var bg = root.GetComponent<Image>();
                bg.raycastTarget = true;
                var click = root.AddComponent<ClickCatcher>();
                var le = root.AddComponent<LayoutElement>();
                le.preferredHeight = ZoneChapterRow.Height;
                var rt = (RectTransform)root.transform;
                rt.sizeDelta = new Vector2(880, ZoneChapterRow.Height);

                var idx = Text(titleTpl, root.transform, "so_ai", 56);
                idx.alignment = TextAlignmentOptions.Center;
                idx.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(18, 0), new Vector2(84, 90), new Vector2(0, 0.5f));
                var tag = Text(titleTpl, root.transform, "kieu_ai", 32);
                tag.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(112, 22), new Vector2(230, 46), new Vector2(0, 0.5f));
                var balls = Text(smallTpl, root.transform, "bi", 26);
                balls.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(112, -28), new Vector2(230, 38), new Vector2(0, 0.5f));

                var foes = new List<ZoneChapterRow.Foe>();
                for (int i = 0; i < 3; i++)
                {
                    var f = new GameObject("dich_" + i, typeof(RectTransform)).GetComponent<RectTransform>();
                    f.SetParent(root.transform, false);
                    f.Place(new Vector2(0, 0.5f), new Vector2(420 + i * 138, 0), new Vector2(134, ZoneChapterRow.Height - 8), new Vector2(0.5f, 0.5f));
                    var por = ((GameObject)PrefabUtility.InstantiatePrefab(kit.portrait.gameObject, f)).GetComponent<HeroPortrait>();
                    por.name = "chan_dung";
                    foreach (var g in por.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
                    por.Rect.Place(new Vector2(0.5f, 0), new Vector2(0, 30), new Vector2(90, 104), new Vector2(0.5f, 0));
                    var label = Text(smallTpl, f, "nhan", 22);
                    label.alignment = TextAlignmentOptions.Center;
                    label.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 0), new Vector2(150, 30), new Vector2(0.5f, 0));
                    foes.Add(new ZoneChapterRow.Foe { root = f.gameObject, portrait = por, label = label });
                }

                var state = new GameObject("trang_thai", typeof(RectTransform), typeof(Image)).GetComponent<Image>();
                state.transform.SetParent(root.transform, false);
                state.raycastTarget = false;
                state.preserveAspect = true;
                state.rectTransform.Place(new Vector2(1, 0.5f), new Vector2(-22, 0), new Vector2(60, 60), new Vector2(1, 0.5f));

                var comp = root.AddComponent<ZoneChapterRow>();
                comp.Setup(new ZoneChapterRow.Parts { bg = bg, state = state, click = click, idx = idx, tag = tag, balls = balls, foes = foes.ToArray() });
                return PrefabUtility.SaveAsPrefabAsset(root, RowPath).GetComponent<ZoneChapterRow>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        static ZoneChapterDialog BuildChapter(UiKit kit, TextMeshProUGUI titleTpl, TextMeshProUGUI subTpl, ZoneChapterRow row)
        {
            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetPath));
            try
            {
                root.name = "BangChang";
                root.GetComponent<ModalSheet>().Configure(980, false, false);
                var sheet = Find(root.transform, "to_giay");
                var content = new GameObject("noi_dung", typeof(RectTransform), typeof(VerticalLayoutGroup)).transform;
                content.SetParent(sheet, false);
                var vl = content.GetComponent<VerticalLayoutGroup>();
                vl.spacing = 12;
                vl.childControlWidth = vl.childControlHeight = true;
                vl.childForceExpandWidth = true;
                vl.childForceExpandHeight = false;

                var title = LayoutText(titleTpl, content, "tieu_de", 70, 60);
                title.alignment = TextAlignmentOptions.Center;
                var sub = LayoutText(subTpl, content, "dong_phu", 44, 32);
                sub.alignment = TextAlignmentOptions.Center;

                // danh sách cuộn dọc: khung nhìn cắt mép, nội dung giãn theo số dòng
                var listGo = new GameObject("danh_sach", typeof(RectTransform), typeof(ScrollRect), typeof(LayoutElement));
                listGo.transform.SetParent(content, false);
                listGo.GetComponent<LayoutElement>().preferredHeight = 1120;
                var view = new GameObject("khung_nhin", typeof(RectTransform), typeof(RectMask2D), typeof(Image)).GetComponent<RectTransform>();
                view.SetParent(listGo.transform, false);
                view.anchorMin = Vector2.zero;
                view.anchorMax = Vector2.one;
                view.offsetMin = view.offsetMax = Vector2.zero;
                var viewImg = view.GetComponent<Image>();
                viewImg.color = new Color(1, 1, 1, 0);
                viewImg.raycastTarget = true;
                var list = new GameObject("cac_ai", typeof(RectTransform), typeof(VerticalLayoutGroup), typeof(ContentSizeFitter)).GetComponent<RectTransform>();
                list.SetParent(view, false);
                list.anchorMin = new Vector2(0, 1);
                list.anchorMax = new Vector2(1, 1);
                list.pivot = new Vector2(0.5f, 1);
                list.offsetMin = list.offsetMax = Vector2.zero;
                var lv = list.GetComponent<VerticalLayoutGroup>();
                lv.spacing = 10;
                lv.padding = new RectOffset(6, 6, 4, 4);
                lv.childControlWidth = lv.childControlHeight = true;
                lv.childForceExpandWidth = true;
                lv.childForceExpandHeight = false;
                list.GetComponent<ContentSizeFitter>().verticalFit = ContentSizeFitter.FitMode.PreferredSize;
                var scroll = listGo.GetComponent<ScrollRect>();
                scroll.viewport = view;
                scroll.content = list;
                scroll.horizontal = false;
                scroll.vertical = true;
                scroll.movementType = ScrollRect.MovementType.Clamped;
                scroll.scrollSensitivity = 40;

                var btnRow = new GameObject("hang_nut", typeof(RectTransform), typeof(HorizontalLayoutGroup), typeof(LayoutElement));
                btnRow.transform.SetParent(content, false);
                var hl = btnRow.GetComponent<HorizontalLayoutGroup>();
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                btnRow.GetComponent<LayoutElement>().preferredHeight = 120;
                var close = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonNormal.gameObject, btnRow.transform)).GetComponent<SketchButton>();
                close.name = "nut_Dong";
                close.SetText("Đóng");
                close.SetRole(BtnColor.Paper);

                root.AddComponent<ZoneChapterDialog>().Setup(title, sub, scroll, list, close, row);
                return PrefabUtility.SaveAsPrefabAsset(root, ChapterPath).GetComponent<ZoneChapterDialog>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        static Transform Find(Transform t, string name)
        {
            foreach (var c in t.GetComponentsInChildren<Transform>(true))
                if (c.name == name) return c;
            return null;
        }

        // chữ một dòng, canh trái, chép phông và viền từ chữ có sẵn (đặt chỗ bằng Place)
        static TextMeshProUGUI Text(TextMeshProUGUI from, Transform parent, string name, float size)
        {
            var t = Object.Instantiate(from.gameObject, parent, false).GetComponent<TextMeshProUGUI>();
            t.name = name;
            foreach (var c in t.GetComponents<LayoutElement>()) Object.DestroyImmediate(c);
            foreach (var c in t.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
            t.gameObject.SetActive(true);
            t.enableAutoSizing = true;
            t.fontSizeMax = size;
            t.fontSizeMin = size * 0.6f;
            t.alignment = TextAlignmentOptions.MidlineLeft;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
            t.raycastTarget = false;
            t.text = "";
            return t;
        }

        // chữ trong cột dọc, cao h
        static TextMeshProUGUI LayoutText(TextMeshProUGUI from, Transform parent, string name, float h, float size)
        {
            var t = Text(from, parent, name, size);
            t.gameObject.AddComponent<LayoutElement>().preferredHeight = h;
            return t;
        }
    }
}
