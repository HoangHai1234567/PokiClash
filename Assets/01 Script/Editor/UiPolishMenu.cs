// Soi và sửa giao diện một lượt (người dùng 2026-11-21: "chụp lại các màn xem UI phần nào còn xấu hoặc text quá to so với nút hoặc
// căn chỉnh lệch thì sửa lại hết 1 lượt"). Ảnh soi: menu "PokiClash/Thử/Chụp mọi màn để soi giao diện" (Temp/PokiShots/ui).
// Menu dò ghi cấu trúc chữ, băng dính của các prefab cần sửa vào Logs/ui_polish_dump.txt.
using System.Collections.Generic;
using System.IO;
using System.Text;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class UiPolishMenu
    {
        static readonly string[] DumpPrefabs =
        {
            "Assets/04 Prefabs/Screens/Notebook.prefab",
            "Assets/04 Prefabs/Screens/Badges.prefab",
            "Assets/04 Prefabs/Screens/Farm.prefab",
            "Assets/04 Prefabs/Dialogs/GioiThieu.prefab",
            "Assets/04 Prefabs/Dialogs/ChuanBiTran.prefab",
            "Assets/04 Prefabs/Dialogs/ChonTuongKhoiDau.prefab",
        };

        [MenuItem("PokiClash/Prefab/Giao diện chung/Soi giao diện: ghi cấu trúc chữ, băng dính (Logs)", priority = 90)]
        static void Dump()
        {
            var sb = new StringBuilder();
            foreach (var path in DumpPrefabs)
            {
                var root = PrefabUtility.LoadPrefabContents(path);
                try
                {
                    sb.AppendLine("== " + path);
                    foreach (var t in root.GetComponentsInChildren<TextMeshProUGUI>(true))
                    {
                        var r = t.rectTransform.rect;
                        string txt = t.text.Replace("\n", "\\n");
                        if (txt.Length > 40) txt = txt.Substring(0, 40) + "…";
                        sb.AppendLine($"  T {Path(t.transform, root.transform)}  [{r.width:0}x{r.height:0}] size {t.fontSize:0.#} auto {t.enableAutoSizing} {t.fontSizeMin:0.#}-{t.fontSizeMax:0.#} wrap {t.enableWordWrapping} \"{txt}\"");
                    }
                    foreach (var im in root.GetComponentsInChildren<Image>(true))
                    {
                        var r = im.rectTransform.rect;
                        if (r.width >= 400 && r.height <= 90 || im.name.Contains("bang") || im.name.Contains("tape"))
                            sb.AppendLine($"  I {Path(im.transform, root.transform)}  [{r.width:0}x{r.height:0}] sprite {(im.sprite ? im.sprite.name : "-")} rot {im.rectTransform.localEulerAngles.z:0.#}");
                    }
                }
                finally
                {
                    PrefabUtility.UnloadPrefabContents(root);
                }
            }
            var outp = System.IO.Path.Combine(Application.dataPath, "..", "Logs", "ui_polish_dump.txt");
            File.WriteAllText(outp, sb.ToString());
            Debug.Log("[Soi giao diện] Ghi " + System.IO.Path.GetFullPath(outp));
        }

        // Sửa một lượt theo ảnh soi 2026-11-21 (chỉ cỡ, lề, màu, hình; không đổi chữ nên bảng dịch tiếng Anh không lệch). Chạy lại không sao.
        [MenuItem("PokiClash/Prefab/Giao diện chung/Sửa giao diện một lượt (2026-11-21)", priority = 91)]
        static void Apply()
        {
            // 1. nút kit: lề nhãn rộng hơn (chữ không chạm viền vẽ tay), co chữ được tới ~42% khi nhãn dài (bản cũ 60%: chữ dài vẫn tràn)
            foreach (var (rel, padX, minK) in new[]
                     {
                         ("Kit/Nut_Nho.prefab", 22f, 0.45f), ("Kit/Nut_Ti.prefab", 16f, 0.45f),
                         ("Kit/Nut_Vua.prefab", 26f, 0.42f), ("Kit/Nut_To.prefab", 30f, 0.42f),
                     })
                Edit(rel, root =>
                {
                    var l = root.GetComponentInChildren<UI.SketchButton>(true).Label;
                    var r = l.rectTransform;
                    r.sizeDelta = new Vector2(-2 * padX, r.sizeDelta.y);
                    l.enableAutoSizing = true;
                    l.fontSizeMin = Mathf.Round(l.fontSizeMax * minK);
                });

            // 2. sảnh: nhãn công trình bên phải co theo nút ("Đền Huy Hiệu", "Hang Tiềm Năng" tràn), chấm báo tròn viền trắng (bản cũ ô vuông)
            var knob = AssetDatabase.GetBuiltinExtraResource<Sprite>("UI/Skin/Knob.psd");
            Edit("Screens/Hub.prefab", root =>
            {
                foreach (var hb in root.GetComponentsInChildren<HubBuilding>(true))
                {
                    var so = new SerializedObject(hb);
                    if (so.FindProperty("label").objectReferenceValue is TextMeshProUGUI label)
                    {
                        if (!label.enableAutoSizing) label.fontSizeMax = label.fontSize;
                        label.enableAutoSizing = true;
                        label.fontSizeMin = Mathf.Round(label.fontSizeMax * 0.5f);
                        label.enableWordWrapping = false;
                        label.margin = new Vector4(6, 0, 6, 0);
                    }
                    if (so.FindProperty("dot").objectReferenceValue is Image dot)
                    {
                        dot.sprite = knob;
                        dot.type = Image.Type.Simple;
                        dot.rectTransform.sizeDelta = new Vector2(30, 30);
                        var o = dot.GetComponent<Outline>();
                        if (!o) o = dot.gameObject.AddComponent<Outline>();
                        o.effectColor = Color.white;
                        o.effectDistance = new Vector2(2.5f, -2.5f);
                    }
                }
            });

            // 3. chuẩn bị trận: tên tướng trong ô đội ("Ra trước · Bạch Viêm Hổ") nằm gọn trong ô, co chữ nhỏ hơn được
            Edit("Dialogs/ChuanBiTran.prefab", root =>
            {
                foreach (var t in root.GetComponentsInChildren<TextMeshProUGUI>(true))
                {
                    if (t.transform.parent == null || !t.transform.parent.name.StartsWith("o_doi_") || !t.enableAutoSizing) continue;
                    var r = t.rectTransform;
                    float y0 = r.offsetMin.y, y1 = r.offsetMax.y;
                    var aMin = r.anchorMin;
                    var aMax = r.anchorMax;
                    var pos = r.anchoredPosition;
                    var size = r.sizeDelta;
                    r.anchorMin = new Vector2(0, aMin.y);
                    r.anchorMax = new Vector2(1, aMax.y);
                    r.sizeDelta = new Vector2(-52, size.y); // khung tím của ô hẹp hơn ô: chừa 26 px mỗi bên
                    r.anchoredPosition = new Vector2(0, pos.y);
                    t.fontSizeMin = 11;
                    t.enableWordWrapping = false;
                }
            });

            // 4. chọn tướng khởi đầu: nút "CHỌN <TÊN>" lề rộng, co chữ được
            Edit("Dialogs/ChonTuongKhoiDau.prefab", root => FixButtonLabel(root, "nut_Chon", 34, 20));

            // 5. đền huy hiệu: dòng giới thiệu đầu trang tự co chữ cho vừa khung (bản cũ dính viền trên)
            Edit("Screens/Badges.prefab", root =>
            {
                foreach (var t in root.GetComponentsInChildren<TextMeshProUGUI>(true))
                    if (t.transform.parent && t.transform.parent.name == "gioi_thieu" && t.name == "chu")
                    {
                        t.fontSizeMax = t.fontSize;
                        t.enableAutoSizing = true;
                        t.fontSizeMin = 18;
                        t.margin = new Vector4(10, 8, 10, 8);
                    }
            });

            // 6. sổ tay phiêu lưu (giới thiệu): tiêu đề và đoạn chữ từng ô tự co (bản cũ dính viền dưới)
            Edit("Dialogs/GioiThieu.prefab", root =>
            {
                foreach (var t in root.GetComponentsInChildren<TextMeshProUGUI>(true))
                {
                    if (t.transform.parent == null || !t.transform.parent.name.StartsWith("o_")) continue;
                    t.fontSizeMax = t.fontSize;
                    t.enableAutoSizing = true;
                    t.fontSizeMin = Mathf.Round(t.fontSize * 0.62f);
                }
            });

            // 7. trang trại: nút "×2 NĂNG SUẤT" chữ bắt đầu sau icon TV
            Edit("Screens/Farm.prefab", root => FixButtonLabel(root, "farm_x2", 22, 22));

            // 8. màn Nhà: dòng gợi ý được hai dòng, chữ to hơn (bản cũ một dòng co tới 16); khay và bảng chọn nhích lên cho khỏi chồng
            Edit("Screens/Home.prefab", root =>
            {
                var home = root.GetComponentInChildren<HomeScene>(true);
                var so = new SerializedObject(home);
                if (so.FindProperty("hint").objectReferenceValue is TextMeshProUGUI hint)
                {
                    var bg = hint.transform.parent as RectTransform;
                    if (bg && bg.sizeDelta.y < 80) bg.sizeDelta = new Vector2(bg.sizeDelta.x, 84);
                    hint.enableAutoSizing = true;
                    hint.enableWordWrapping = true;
                    hint.fontSizeMin = 17;
                    hint.fontSizeMax = 24;
                }
                foreach (var key in new[] { "tray", "panel" })
                    if (so.FindProperty(key).objectReferenceValue is RectTransform rt && rt.anchoredPosition.y < 240)
                        rt.anchoredPosition = new Vector2(rt.anchoredPosition.x, 248);
            });
            // 9. khay Xây màn Nhà: tên công trình được xuống dòng, cỡ chữ đều giữa các nút (bản cũ mỗi nút co một cỡ, nhiều nút chữ li ti)
            Edit("Items/NutKhayNha.prefab", root =>
            {
                var l = root.GetComponentInChildren<UI.SketchButton>(true).Label;
                l.enableWordWrapping = true;
                l.enableAutoSizing = true;
                l.fontSizeMax = 20;
                l.fontSizeMin = 12;
                // icon nhỏ lại cho chữ rộng thêm (bản 80 px: tên + "NHÀ CẤP 4" phải xuống 3 dòng, chạm đáy nút)
                var icon = root.transform.Find("icon") as RectTransform;
                if (icon) icon.sizeDelta = new Vector2(68, 68);
                l.rectTransform.offsetMin = new Vector2(80, l.rectTransform.offsetMin.y);
            });
            AssetDatabase.SaveAssets();
            Debug.Log("[Sửa giao diện] Xong một lượt");
        }

        // nút tên `name`: nhãn chừa lề hai bên (và chừa chỗ icon con nằm bên trái nếu có), co chữ tới minSize
        static void FixButtonLabel(GameObject root, string name, float pad, float minSize)
        {
            foreach (var b in root.GetComponentsInChildren<UI.SketchButton>(true))
            {
                if (b.name != name) continue;
                var l = b.Label;
                var lr = l.rectTransform;
                float left = pad;
                var br = (RectTransform)b.transform;
                foreach (var im in b.GetComponentsInChildren<Image>(true))
                {
                    if (im.transform == b.transform || im.transform.IsChildOf(lr) || im == b.Core) continue;
                    var corners = new Vector3[4];
                    im.rectTransform.GetWorldCorners(corners);
                    float right = br.InverseTransformPoint(corners[2]).x - br.rect.xMin;
                    if (right < br.rect.width * 0.45f) left = Mathf.Max(left, right + 8); // icon ở nửa trái
                }
                lr.anchorMin = new Vector2(0, lr.anchorMin.y);
                lr.anchorMax = new Vector2(1, lr.anchorMax.y);
                lr.offsetMin = new Vector2(left, lr.offsetMin.y);
                lr.offsetMax = new Vector2(-pad, lr.offsetMax.y);
                l.enableAutoSizing = true;
                l.fontSizeMin = minSize;
                Debug.Log($"[Sửa giao diện] {name}: lề trái {left:0}, phải {pad:0}");
            }
        }

        static void Edit(string rel, System.Action<GameObject> fix)
        {
            string path = "Assets/04 Prefabs/" + rel;
            var root = PrefabUtility.LoadPrefabContents(path);
            try
            {
                fix(root);
                PrefabUtility.SaveAsPrefabAsset(root, path);
                Debug.Log("[Sửa giao diện] " + rel);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        static string Path(Transform t, Transform root)
        {
            var parts = new List<string>();
            for (var x = t; x && x != root; x = x.parent) parts.Add(x.name);
            parts.Reverse();
            return string.Join("/", parts);
        }
    }
}
