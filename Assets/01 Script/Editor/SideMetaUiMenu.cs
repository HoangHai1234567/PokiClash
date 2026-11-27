// Dựng phần giao diện mới của side meta (2026-11-17, tăng dày nội dung Đền Huy Hiệu và Tiềm năng, GD_Claude/20_TangDayNoiDung.md) vào
// prefab có sẵn. Chạy lại được nhiều lần: phần đã dựng thì giữ (hàng sao, nút bậc, thanh mốc sao dựng lại).
// - "Tiềm năng: 6 ô, bộ, đá tinh": Dialogs/TiemNang thêm ô 5, 6 (chép ô 4, đổi tên o_4, o_5, khoa_4, khoa_5), chip đá tinh (chip_tinh, chép
//   chip đá, icon tô màu đá tinh), dòng bộ (bo, chép dòng tổng), nút khai phá bằng đá tinh (khai_pha_tinh, cạnh khai_pha); gán các trường
//   mới của PotentialDialog. Dialogs/TiemNangSoSanh thêm dòng 5, 6 (chép dòng 4) và gán vào PotentialCompareDialog.rows.
// - "Đền Huy Hiệu: sao trận, chọn bậc, mốc sao": Items/TranHuyHieu thêm hàng sao kit (sao, 3 sao, cạnh nút đánh) vào BadgeStageRow.stars;
//   Dialogs/DanhSachTranHuyHieu thêm nút kit nhỏ "«" / "»" (bac_truoc, bac_sau) góc phải đầu hộp vào BadgeListDialog.prev / next;
//   Screens/Badges thêm thanh kit (thanh_moc_sao) đáy khung giới thiệu, gán BadgesScene.intro (gioi_thieu/chu) và starBar.
//   Bệ Items/BenHuyHieu: tên, phần cộng, tiến độ, "Đã đạt bậc cao nhất" tự co chữ, không đè nút; hộp danh sách trận: đầu hộp cao hơn, tên một
//   dòng tự co, nút bậc nhỏ không đè tên; hàng trận: chữ dừng trước hàng sao.
// - (Bỏ 2026-11-27) "Hang Tiềm Năng: hàng tầng gọn": màn Hang thành sân khấu (Editor/CaveStageMenu.cs), không còn Items/TangHang.
// Ô chép bằng Object.Instantiate (không giữ liên kết prefab con KhungMong / Nut_Ti của ô gốc); số ô (chữ số đầu dòng) đặt lại theo thứ tự;
// phần kit mới gắn bằng InstantiatePrefab.
// Sau khi dựng, chỉnh vị trí và cỡ trong Editor như mọi prefab khác.
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class SideMetaUiMenu
    {
        const string PotPath = "Assets/04 Prefabs/Dialogs/TiemNang.prefab";
        const string ComparePath = "Assets/04 Prefabs/Dialogs/TiemNangSoSanh.prefab";
        const string RowPath = "Assets/04 Prefabs/Items/TranHuyHieu.prefab";
        const string ListPath = "Assets/04 Prefabs/Dialogs/DanhSachTranHuyHieu.prefab";
        const string TemplePath = "Assets/04 Prefabs/Screens/Badges.prefab";
        const string PedestalPath = "Assets/04 Prefabs/Items/BenHuyHieu.prefab";
        static readonly Color CrystalTint = new Color32(0x4f, 0xd8, 0xe8, 0xff); // như PotentialPanel.CrystalTint

        // ---------- tiện ích ----------

        static UiKit Kit()
        {
            var g = AssetDatabase.FindAssets("t:UiKit");
            return g.Length == 0 ? null : AssetDatabase.LoadAssetAtPath<UiKit>(AssetDatabase.GUIDToAssetPath(g[0]));
        }

        // đường đi theo chỉ số con từ root tới t ("2/0"); "" nếu t là root; null nếu t không nằm dưới root
        static string RelPath(Transform root, Transform t)
        {
            var parts = new List<string>();
            for (var x = t; x != root; x = x.parent)
            {
                if (!x) return null;
                parts.Insert(0, x.GetSiblingIndex().ToString());
            }
            return string.Join("/", parts);
        }

        static Transform At(Transform root, string path)
        {
            if (string.IsNullOrEmpty(path)) return root;
            var t = root;
            foreach (var p in path.Split('/')) t = t.GetChild(int.Parse(p));
            return t;
        }

        // chép một đồ vật ngay sau nó (cùng cha), đặt tên
        static GameObject Dup(GameObject src, string name)
        {
            var c = Object.Instantiate(src, src.transform.parent);
            c.name = name;
            c.transform.SetSiblingIndex(src.transform.GetSiblingIndex() + 1);
            return c;
        }

        // ánh xạ một tham chiếu (component hoặc GameObject) trong bản gốc sang bản chép theo cùng đường đi
        static Object Map(Object src, Transform srcRoot, Transform dstRoot)
        {
            if (!src) return null;
            var t = src is GameObject go ? go.transform : ((Component)src).transform;
            var path = RelPath(srcRoot, t);
            if (path == null) return null;
            var dt = At(dstRoot, path);
            return src is GameObject ? dt.gameObject : (Object)dt.GetComponent(src.GetType());
        }

        // tổ tiên của t là con trực tiếp của cột có VerticalLayoutGroup (một "hàng" của hộp)
        static Transform RowOf(Transform t)
        {
            while (t.parent && !t.parent.GetComponent<VerticalLayoutGroup>()) t = t.parent;
            return t;
        }

        static void Rename(Transform root, string from, string to)
        {
            foreach (var t in root.GetComponentsInChildren<Transform>(true))
                if (t.name == from) t.name = to;
        }

        // chép thêm phần tử cho mảng struct rows tới đủ n, mỗi phần tử mới chép hàng của phần tử cuối; fields: tên trường của struct;
        // rootField: trường là gốc của hàng (null: hàng là tổ tiên của trường đầu nằm ngay dưới cột VerticalLayoutGroup)
        static int GrowRows(SerializedProperty rows, int n, string[] fields, string rowName, string lockName = null, string rootField = null)
        {
            int have = rows.arraySize, added = 0;
            if (have == 0 || have >= n) return 0;
            var last = rows.GetArrayElementAtIndex(have - 1);
            Transform srcRoot;
            if (rootField != null) srcRoot = ((GameObject)last.FindPropertyRelative(rootField).objectReferenceValue).transform;
            else
            {
                var anyRef = fields.Select(f => last.FindPropertyRelative(f).objectReferenceValue).First(o => o);
                srcRoot = RowOf(anyRef is GameObject g0 ? g0.transform : ((Component)anyRef).transform);
            }
            if (!srcRoot.parent)
            {
                Debug.LogError($"[Side meta] Không tìm được hàng để chép ({rowName}).");
                return 0;
            }
            var prev = srcRoot.gameObject;
            var srcRefs = fields.ToDictionary(f => f, f => last.FindPropertyRelative(f).objectReferenceValue);
            for (int i = have; i < n; i++)
            {
                var clone = Dup(prev, rowName + i);
                if (lockName != null) Rename(clone.transform, lockName + (have - 1), lockName + i);
                rows.arraySize = i + 1;
                var el = rows.GetArrayElementAtIndex(i);
                foreach (var f in fields) el.FindPropertyRelative(f).objectReferenceValue = Map(srcRefs[f], srcRoot, clone.transform);
                prev = clone;
                added++;
            }
            return added;
        }

        // chữ tự co trong khung: cỡ tối đa max, tối thiểu min; wrap: cho xuống dòng
        static void Fit(TextMeshProUGUI t, float max, float min, bool wrap)
        {
            if (!t) return;
            t.enableAutoSizing = true;
            t.fontSizeMax = max;
            t.fontSizeMin = min;
            t.fontSize = max;
            t.textWrappingMode = wrap ? TextWrappingModes.Normal : TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
        }

        // khung neo góc trên trái: cách trái x, cách trên y, rộng w, cao h
        static void TopLeft(Component c, float x, float y, float w, float h)
        {
            if (!c) return;
            var r = (RectTransform)c.transform;
            r.anchorMin = r.anchorMax = new Vector2(0, 1);
            r.pivot = new Vector2(0, 1);
            r.anchoredPosition = new Vector2(x, -y);
            r.sizeDelta = new Vector2(w, h);
        }

        // khung giãn theo chiều ngang của cha, neo mép trên: lề trái l, lề phải r, cách trên y, cao h
        static void TopStretch(Component c, float l, float r, float y, float h)
        {
            if (!c) return;
            var t = (RectTransform)c.transform;
            t.anchorMin = new Vector2(0, 1);
            t.anchorMax = new Vector2(1, 1);
            t.pivot = new Vector2(0.5f, 1);
            t.sizeDelta = new Vector2(-(l + r), h);
            t.anchoredPosition = new Vector2((l - r) / 2, -y);
        }

        // đặt lại chữ số thứ tự đầu mỗi hàng (chữ không thuộc trường nào của hàng, không nằm trong nút, đang là một số): 1, 2, 3...
        static void Renumber(SerializedProperty rows, string[] fields, string rootField = null)
        {
            for (int i = 0; i < rows.arraySize; i++)
            {
                var el = rows.GetArrayElementAtIndex(i);
                var refs = new HashSet<Object>(fields.Select(f => el.FindPropertyRelative(f).objectReferenceValue).Where(o => o));
                if (refs.Count == 0) continue;
                Transform root;
                if (rootField != null) root = ((GameObject)el.FindPropertyRelative(rootField).objectReferenceValue).transform;
                else
                {
                    var any = refs.First();
                    root = RowOf(any is GameObject g ? g.transform : ((Component)any).transform);
                }
                foreach (var t in root.GetComponentsInChildren<TextMeshProUGUI>(true))
                    if (!refs.Contains(t) && !t.GetComponentInParent<SketchButton>() && int.TryParse(t.text.Trim(), out _))
                        t.text = (i + 1).ToString();
            }
        }

        static void Width(Component c, float w)
        {
            var rt = (RectTransform)c.transform;
            rt.sizeDelta = new Vector2(w, rt.sizeDelta.y);
            var le = c.GetComponent<LayoutElement>();
            if (le) le.preferredWidth = w;
        }

        // ---------- Tiềm năng ----------

        [MenuItem("PokiClash/Prefab/Nhà và side meta/Tiềm năng: 6 ô, bộ, đá tinh", priority = 61)]
        static void BuildPotential()
        {
            var contents = PrefabUtility.LoadPrefabContents(PotPath);
            try
            {
                var dlg = contents.GetComponentInChildren<PotentialDialog>(true);
                var so = new SerializedObject(dlg);
                var potFields = new[] { "bg", "text", "rarity", "lockButton", "lockButtonIcon", "lockIcon" };
                int added = GrowRows(so.FindProperty("rows"), Potential.Slots, potFields, "o_", "khoa_");
                Renumber(so.FindProperty("rows"), potFields);

                var stones = (TextMeshProUGUI)so.FindProperty("stones").objectReferenceValue;
                var crystals = so.FindProperty("crystals");
                if (!crystals.objectReferenceValue && stones)
                {
                    var chip = stones.GetComponentInParent<UiChip>();
                    var src = chip ? chip.gameObject : stones.gameObject;
                    var c = Dup(src, "chip_tinh");
                    var cc = c.GetComponent<UiChip>();
                    if (cc && cc.Icon) cc.Icon.color = CrystalTint;
                    crystals.objectReferenceValue = cc ? cc.Value : c.GetComponent<TextMeshProUGUI>();
                }

                var totals = (TextMeshProUGUI)so.FindProperty("totals").objectReferenceValue;
                var sets = so.FindProperty("sets");
                if (!sets.objectReferenceValue && totals)
                {
                    var b = Dup(totals.gameObject, "bo").GetComponent<TextMeshProUGUI>();
                    b.fontSize = totals.fontSize * 0.85f;
                    b.text = "Bộ: chưa có";
                    sets.objectReferenceValue = b;
                }

                var spin = (SketchButton)so.FindProperty("spin").objectReferenceValue;
                var spinC = so.FindProperty("spinCrystal");
                if (!spinC.objectReferenceValue && spin)
                {
                    var bc = Dup(spin.gameObject, "khai_pha_tinh").GetComponent<SketchButton>();
                    bc.SetRole(BtnColor.Blue);
                    bc.SetText("Đá tinh (1)");
                    Width(spin, 340);
                    Width(bc, 300);
                    spinC.objectReferenceValue = bc;
                }
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, PotPath);
                Debug.Log($"[Tiềm năng] {PotPath}: thêm {added} ô (đủ {Potential.Slots}), chip đá tinh, dòng bộ, nút đá tinh.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }

            contents = PrefabUtility.LoadPrefabContents(ComparePath);
            try
            {
                var dlg = contents.GetComponentInChildren<PotentialCompareDialog>(true);
                var so = new SerializedObject(dlg);
                var cmpFields = new[] { "root", "oldBg", "newBg", "oldText", "newText", "arrow" };
                int added = GrowRows(so.FindProperty("rows"), Potential.Slots, cmpFields, "o_", null, "root");
                Renumber(so.FindProperty("rows"), cmpFields, "root");
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, ComparePath);
                Debug.Log($"[Tiềm năng] {ComparePath}: thêm {added} dòng (đủ {Potential.Slots}).");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // ---------- Đền Huy Hiệu ----------

        [MenuItem("PokiClash/Prefab/Nhà và side meta/Đền Huy Hiệu: sao trận, chọn bậc, mốc sao", priority = 62)]
        static void BuildTemple()
        {
            var kit = Kit();
            if (!kit)
            {
                Debug.LogError("[Đền] Không thấy asset UiKit.");
                return;
            }

            // hàng sao của mỗi trận
            var contents = PrefabUtility.LoadPrefabContents(RowPath);
            try
            {
                var row = contents.GetComponentInChildren<BadgeStageRow>(true);
                var so = new SerializedObject(row);
                var sp = so.FindProperty("stars");
                if (sp.objectReferenceValue) Object.DestroyImmediate(((Component)sp.objectReferenceValue).gameObject);
                var fight = (SketchButton)so.FindProperty("fight").objectReferenceValue;
                var parent = fight ? fight.transform.parent : row.transform;
                var stars = ((GameObject)PrefabUtility.InstantiatePrefab(kit.stars.gameObject, parent)).GetComponent<UiStars>();
                stars.name = "sao";
                stars.SetSize(30);
                stars.Set(3, 3);
                var rt = stars.Rect;
                rt.anchorMin = rt.anchorMax = new Vector2(1, 0.5f);
                rt.pivot = new Vector2(1, 0.5f);
                rt.anchoredPosition = new Vector2(-214, 4); // bên trái nút đánh (rộng 180, cách mép 24)
                sp.objectReferenceValue = stars;
                // chữ dừng trước hàng sao (sao rộng 3 × 30 × 0,9)
                var label = (TextMeshProUGUI)so.FindProperty("text").objectReferenceValue;
                if (label)
                {
                    var lr = label.rectTransform;
                    lr.offsetMax = new Vector2(-(214 + 3 * 30 * 0.9f + 12), lr.offsetMax.y);
                    Fit(label, 30, 18, false);
                }
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, RowPath);
                Debug.Log($"[Đền] {RowPath}: hàng sao.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }

            // nút xem bậc trước / sau
            contents = PrefabUtility.LoadPrefabContents(ListPath);
            try
            {
                var dlg = contents.GetComponentInChildren<BadgeListDialog>(true);
                var so = new SerializedObject(dlg);
                var title = (TextMeshProUGUI)so.FindProperty("title").objectReferenceValue;
                var head = title ? title.transform.parent : dlg.transform;
                const float NavW = 84, NavH = 60;
                SketchButton Make(string prop, string name, string label, float x)
                {
                    var p = so.FindProperty(prop);
                    if (p.objectReferenceValue) Object.DestroyImmediate(((Component)p.objectReferenceValue).gameObject);
                    var b = ((GameObject)PrefabUtility.InstantiatePrefab(kit.buttonTiny.gameObject, head)).GetComponent<SketchButton>();
                    b.name = name;
                    b.SetText(label);
                    b.SetRole(BtnColor.Paper);
                    var r = b.Rect;
                    r.anchorMin = r.anchorMax = new Vector2(1, 1);
                    r.pivot = new Vector2(1, 1);
                    r.anchoredPosition = new Vector2(x, -8);
                    r.sizeDelta = new Vector2(NavW, NavH);
                    var le = b.GetComponent<LayoutElement>();
                    if (le)
                    {
                        le.preferredWidth = NavW;
                        le.preferredHeight = NavH;
                    }
                    p.objectReferenceValue = b;
                    return b;
                }
                Make("next", "bac_sau", "»", -8);
                Make("prev", "bac_truoc", "«", -16 - NavW);
                // đầu hộp: tên một dòng tự co, không chui dưới nút bậc; dòng phụ (2–3 dòng) tự co, không đè tên
                var headLe = head.GetComponent<LayoutElement>();
                if (headLe) headLe.preferredHeight = 200;
                var sub = (TextMeshProUGUI)so.FindProperty("sub").objectReferenceValue;
                TopStretch(title, 140, 2 * NavW + 32, 6, 78);
                Fit(title, 60, 34, false);
                TopStretch(sub, 140, 20, 86, 110);
                Fit(sub, 26, 17, true);
                if (sub) sub.verticalAlignment = VerticalAlignmentOptions.Top;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, ListPath);
                Debug.Log($"[Đền] {ListPath}: nút bậc trước / sau.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }

            // bệ: chữ tự co, không đè nút "Thử thách" (nút rộng 290 ở góc dưới phải, cao 30..130)
            contents = PrefabUtility.LoadPrefabContents(PedestalPath);
            try
            {
                var ped = contents.GetComponentInChildren<BadgePedestal>(true);
                var so = new SerializedObject(ped);
                TextMeshProUGUI T(string f) => (TextMeshProUGUI)so.FindProperty("p." + f).objectReferenceValue;
                Fit(T("title"), 50, 30, false);
                TopLeft(T("bonus"), 250, 96, 690, 66);
                Fit(T("bonus"), 28, 17, true);
                var prog = T("progress");
                if (prog)
                {
                    prog.rectTransform.sizeDelta = new Vector2(410, prog.rectTransform.sizeDelta.y);
                    Fit(prog, 32, 18, false);
                }
                var done = T("done");
                if (done)
                {
                    done.rectTransform.sizeDelta = new Vector2(400, done.rectTransform.sizeDelta.y);
                    Fit(done, 40, 22, false);
                }
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, PedestalPath);
                Debug.Log($"[Đền] {PedestalPath}: chữ tự co, không đè nút.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }

            // thanh mốc sao đáy khung giới thiệu
            contents = PrefabUtility.LoadPrefabContents(TemplePath);
            try
            {
                var scene = contents.GetComponentInChildren<BadgesScene>(true);
                var so = new SerializedObject(scene);
                var list = (RectTransform)so.FindProperty("list").objectReferenceValue;
                var intro = list ? list.Find("gioi_thieu") : null;
                if (!intro)
                {
                    Debug.LogError("[Đền] Không thấy khung gioi_thieu trong cột của màn Đền.");
                    return;
                }
                var text = intro.Find("chu") ? intro.Find("chu").GetComponent<TextMeshProUGUI>() : intro.GetComponentInChildren<TextMeshProUGUI>(true);
                so.FindProperty("intro").objectReferenceValue = text;
                var bp = so.FindProperty("starBar");
                const float BarH = 26, Room = 44;
                if (bp.objectReferenceValue) Object.DestroyImmediate(((Component)bp.objectReferenceValue).gameObject);
                else
                {
                    // lần đầu: nới khung và chừa chỗ dưới chữ cho thanh
                    var le = intro.GetComponent<LayoutElement>();
                    if (le) le.preferredHeight += Room;
                    var irt = (RectTransform)intro;
                    if (!le) irt.sizeDelta = new Vector2(irt.sizeDelta.x, irt.sizeDelta.y + Room);
                    if (text) text.rectTransform.offsetMin = new Vector2(text.rectTransform.offsetMin.x, text.rectTransform.offsetMin.y + Room);
                }
                var bar = ((GameObject)PrefabUtility.InstantiatePrefab(kit.bar.gameObject, intro)).GetComponent<UiBar>();
                bar.name = "thanh_moc_sao";
                bar.SetKind(UiBar.Kind.Exp);
                var brt = (RectTransform)bar.transform;
                brt.anchorMin = new Vector2(0, 0);
                brt.anchorMax = new Vector2(1, 0);
                brt.pivot = new Vector2(0.5f, 0);
                brt.sizeDelta = new Vector2(-80, BarH);
                brt.anchoredPosition = new Vector2(0, 16);
                bp.objectReferenceValue = bar;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, TemplePath);
                Debug.Log($"[Đền] {TemplePath}: thanh mốc sao, chữ giới thiệu.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

    }
}
