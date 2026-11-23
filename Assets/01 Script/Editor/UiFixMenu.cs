// Sửa căn chỉnh sau đợt soát UI tự động 2026-11-23 (người dùng: "kiểm tra tất cả mọi màn / popup / panel... căn chỉnh text / button /
// UI còn lỗi không, icon nào bị lệch, không căn giữa, bị khuyết mất thì sửa hết"; tour UiFullAudit + UiLint, ảnh Temp/PokiShots/soat).
// Menu "PokiClash/Prefab/Giao diện chung/Giao diện chung∕Soát UI 11-23: sửa căn chỉnh prefab" vá thẳng các prefab (chạy lại được, giá trị đặt tuyệt đối):
// 1. sảnh: nhãn thẻ công trình bên phải hai dòng, chữ không dưới 16 ("Đền Huy Hiệu", "Hang Tiềm Năng" một dòng co còn 15 px);
// 2. Nhà: hàng nút dưới nhấc lên (chữ dưới nút bị cắt ở đáy màn), tấm xây và dòng gợi ý nhấc theo;
// 3. hộp chọn đội: ô tướng cao thêm, lực chiến nhấc khỏi viền khung độ hiếm (số bị viền dưới cắt);
// 4. con dấu (Thắng / Thua / Lên cấp / Huyền thoại): chữ tự co, chừa lề trong vòng mực ("HUYỀN THOẠI!" chạm, lòi khỏi vòng);
// 5. Trang trại: bảng tên khu nằm trong khung ảnh ("Xưởng nông cụ" cắt mép phải);
// 6. Máy bi: số "+8" của ô quà nhấc vào trong (lòi khỏi đáy màn).
using System;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class UiFixMenu
    {
        const string P = "Assets/04 Prefabs/";

        [MenuItem("PokiClash/Prefab/Giao diện chung/Giao diện chung∕Soát UI 11-23: sửa căn chỉnh prefab", priority = 160)]
        static void Run()
        {
            int n = 0;

            // 1. sảnh: thẻ công trình 132 x 132: icon nhấc lên, chữ hai dòng ở đáy
            n += Edit("Screens/Hub.prefab", root =>
            {
                foreach (var hb in root.GetComponentsInChildren<HubBuilding>(true))
                {
                    var so = new SerializedObject(hb);
                    if (so.FindProperty("icon").objectReferenceValue is Image icon)
                    {
                        icon.rectTransform.anchoredPosition = new Vector2(0, 22);
                        icon.rectTransform.sizeDelta = new Vector2(60, 60);
                    }
                    if (so.FindProperty("label").objectReferenceValue is TextMeshProUGUI label)
                    {
                        label.textWrappingMode = TextWrappingModes.Normal;
                        label.enableAutoSizing = true;
                        label.fontSizeMax = 22;
                        label.fontSizeMin = 16;
                        label.lineSpacing = -22;
                        label.margin = new Vector4(2, 0, 2, 0);
                        label.alignment = TextAlignmentOptions.Center;
                        var r = label.rectTransform;
                        r.anchorMin = r.anchorMax = new Vector2(0.5f, 0);
                        r.pivot = new Vector2(0.5f, 0.5f);
                        r.anchoredPosition = new Vector2(0, 31);
                        r.sizeDelta = new Vector2(122, 54);
                    }
                }
            });

            // 2. Nhà: đáy hàng nút 62 → 100, tấm xây 196 → 234, gợi ý trên tấm xây (khớp HomeCrittersMenu.HudY / SheetY)
            n += Edit("Screens/Home.prefab", root =>
            {
                SetY(root, "hang_nut_nha", 100);
                SetY(root, "tam_xay", 234);
                SetY(root, "goi_y", 234 + 520 + 6);
            });

            // 3. chọn đội: ô 154 x 210 → 154 x 222, lực chiến 6 → 12 từ đáy; lưới hộp chọn đội theo cỡ ô mới
            n += Edit("Items/OChonDoi.prefab", root =>
            {
                var rt = (RectTransform)root.transform;
                rt.sizeDelta = new Vector2(rt.sizeDelta.x, 222);
                var pw = root.transform.Find("luc_chien") as RectTransform;
                if (pw) pw.anchoredPosition = new Vector2(pw.anchoredPosition.x, 12);
            });
            n += Edit("Dialogs/ChonDoi.prefab", root =>
            {
                foreach (var g in root.GetComponentsInChildren<GridLayoutGroup>(true))
                    if (Mathf.Approximately(g.cellSize.x, 154) && Mathf.Approximately(g.cellSize.y, 210))
                        g.cellSize = new Vector2(154, 222);
            });

            // 4. con dấu: chữ trong vòng mực tự co, lề trong
            foreach (var path in new[] { "Kit/ConDau.prefab", "Dialogs/TranKetQua.prefab", "Dialogs/HuyenThoai.prefab", "Dialogs/LenCap.prefab" })
                n += Edit(path, root =>
                {
                    foreach (var t in root.GetComponentsInChildren<Transform>(true))
                    {
                        bool stamp = t.GetComponent<UiStamp>() || t.name == "con_dau";
                        if (!stamp) continue;
                        foreach (var label in t.GetComponentsInChildren<TextMeshProUGUI>(true))
                        {
                            if (label.transform.parent != t) continue;
                            float max = Mathf.Max(label.fontSize, label.enableAutoSizing ? label.fontSizeMax : 0);
                            label.enableAutoSizing = true;
                            label.fontSizeMax = max;
                            label.fontSizeMin = Mathf.Round(max * 0.55f);
                            label.textWrappingMode = TextWrappingModes.NoWrap;
                            label.margin = new Vector4(40, 10, 40, 10);
                        }
                    }
                });

            // 4b. kết quả trận: con dấu là con trực tiếp của cột tờ giấy nên bị kéo ngang hết tờ (~820) và cao theo ô, nghiêng 9° thì góc dưới
            //    cắt dòng tên ải (nới ô chỉ làm dấu to theo). Đặt dấu vào ô riêng "o_con_dau" cao 265 (ô chịu layout), dấu bỏ qua layout:
            //    cỡ theo chữ (UiStamp.Set), nghiêng 6°.
            n += Edit("Dialogs/TranKetQua.prefab", root =>
            {
                var stamp = root.GetComponentInChildren<UiStamp>(true);
                if (!stamp) return;
                var t = stamp.Rect;
                RectTransform cell = t.parent.name == "o_con_dau" ? (RectTransform)t.parent : null;
                if (!cell)
                {
                    cell = new GameObject("o_con_dau", typeof(RectTransform), typeof(LayoutElement)).GetComponent<RectTransform>();
                    cell.SetParent(t.parent, false);
                    cell.SetSiblingIndex(t.GetSiblingIndex());
                    t.SetParent(cell, false);
                }
                var cle = cell.GetComponent<LayoutElement>();
                cle.preferredHeight = 265;
                cle.minHeight = 265;
                if (t.GetComponent<LayoutElement>() is LayoutElement le) le.ignoreLayout = true;
                t.anchorMin = t.anchorMax = t.pivot = new Vector2(0.5f, 0.5f);
                t.anchoredPosition = Vector2.zero;
                t.sizeDelta = new Vector2(600, 190);
                t.localScale = Vector3.one;
                t.localEulerAngles = new Vector3(0, 0, -6);
            });

            // 4c. tiềm năng: chip đá tinh chép đè đúng chỗ chip đá (menu Tiềm năng: 6 ô...), che mất số đá → dời sang trái chip đá,
            //     tiêu đề co lại trước chip
            n += Edit("Dialogs/TiemNang.prefab", root =>
            {
                RectTransform Find(string name)
                {
                    foreach (var t in root.GetComponentsInChildren<RectTransform>(true))
                        if (t.name == name) return t;
                    return null;
                }
                RectTransform chip = Find("chip"), tinh = Find("chip_tinh");
                if (!chip || !tinh || tinh.parent != chip.parent) return;
                tinh.anchorMin = chip.anchorMin;
                tinh.anchorMax = chip.anchorMax;
                tinh.pivot = chip.pivot;
                tinh.sizeDelta = chip.sizeDelta;
                tinh.anchoredPosition = chip.anchoredPosition - new Vector2(chip.rect.width + 18, 0);
                var parent = (RectTransform)chip.parent;
                float LeftOf(RectTransform r)
                {
                    var c = new Vector3[4];
                    r.GetWorldCorners(c);
                    return Mathf.Min(parent.InverseTransformPoint(c[0]).x, parent.InverseTransformPoint(c[2]).x);
                }
                float RightOf(RectTransform r)
                {
                    var c = new Vector3[4];
                    r.GetWorldCorners(c);
                    return Mathf.Max(parent.InverseTransformPoint(c[0]).x, parent.InverseTransformPoint(c[2]).x);
                }
                float limit = LeftOf(tinh) - 14;
                foreach (var title in parent.GetComponentsInChildren<TextMeshProUGUI>(true))
                {
                    if (title.transform.parent != parent) continue;
                    // lề phải của chữ chừa chỗ hai chip (đặt bằng margin nên không phụ thuộc neo của khung chữ)
                    float over = RightOf(title.rectTransform) - limit;
                    var m = title.margin;
                    title.margin = new Vector4(m.x, m.y, Mathf.Max(0, over), m.w);
                    float max = Mathf.Max(title.fontSize, title.enableAutoSizing ? title.fontSizeMax : 0);
                    title.enableAutoSizing = true;
                    title.fontSizeMax = max;
                    title.fontSizeMin = Mathf.Round(max * 0.55f);
                    title.textWrappingMode = TextWrappingModes.NoWrap;
                }
            });

            // 5. Trang trại: ảnh nền 1024 rộng phủ màn nên hai bên bị cắt ~8%; bảng "Xưởng nông cụ" (x 870) lòi mép phải → x 790
            //    (khớp FarmSceneMenu.Signs)
            n += Edit("Screens/Farm.prefab", root =>
            {
                foreach (var t in root.GetComponentsInChildren<RectTransform>(true))
                    if (t.name == "bang_smithy" && t.parent && t.parent.name == "bang_khu")
                    {
                        t.anchorMin = new Vector2(790f / 1024f, t.anchorMin.y);
                        t.anchorMax = new Vector2(790f / 1024f, t.anchorMax.y);
                        t.anchoredPosition = new Vector2(0, t.anchoredPosition.y);
                    }
            });

            // 6. Máy bi: số trong ô quà
            n += Edit("Screens/Machine.prefab", root =>
            {
                foreach (var t in root.GetComponentsInChildren<Transform>(true))
                    if (t.name == "o_qua" && t.Find("so") is RectTransform so)
                        so.anchoredPosition = new Vector2(so.anchoredPosition.x, 44);
            });

            AssetDatabase.SaveAssets();
            Debug.Log($"[Soát UI] Đã vá {n} prefab (sảnh, Nhà, chọn đội, con dấu, Trang trại, Máy bi).");
        }

        static void SetY(GameObject root, string name, float y)
        {
            foreach (var t in root.GetComponentsInChildren<RectTransform>(true))
                if (t.name == name)
                {
                    t.anchoredPosition = new Vector2(t.anchoredPosition.x, y);
                    return;
                }
            Debug.LogWarning($"[Soát UI] Không thấy {name} trong {root.name}");
        }

        static int Edit(string rel, Action<GameObject> edit)
        {
            string path = P + rel;
            if (!AssetDatabase.LoadAssetAtPath<GameObject>(path))
            {
                Debug.LogWarning("[Soát UI] Không có " + path);
                return 0;
            }
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                edit(root);
                PrefabUtility.SaveAsPrefabAsset(root, path);
                return 1;
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }
    }
}
