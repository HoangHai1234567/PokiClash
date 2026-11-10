// Hàng nút đáy sảnh làm lại (người dùng 2026-11-10: "thiết kế lại bộ UI này, hơi xấu"). Trước: 5 nút tròn trôi trên biển, nhãn chữ trắng.
// Nay theo bộ UI "Sa Bàn" (GD_Claude/17_BoUI.md), chỉ dùng ảnh kit đã duyệt:
// - kệ gỗ: mép bàn gỗ (boot_ban_go xoay ngang) chạy suốt đáy màn, viền mực trên, tràn xuống quá mép an toàn;
// - 4 nút phụ (Tướng, Sổ thẻ, Đánh tiếp, Sổ tay): thẻ giấy ghi chú (boot_giay_ghi, 9 mảnh) nghiêng nhẹ so le, băng keo màu dán
//   mép trên, icon to, nhãn chữ mực in trên thẻ; là SketchButton (lún, nảy, nét mực bung như mọi nút);
// - Máy Bi: nút tròn sticker cũ, phóng to, nhô lên khỏi mép bàn, vẫn thở; nhãn là mảnh băng keo vàng đè dưới;
// - chấm số đỏ: góc trên phải mỗi nút.
// Menu "PokiClash/Prefab/Sảnh: hàng nút đáy (kệ gỗ, thẻ giấy)" chạy lại được: lấy icon và chấm số từ HubScene.bottom rồi dựng lại.
using System.Collections.Generic;
using System.Linq;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HubDockMenu
    {
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string WoodPath = "Assets/03 Art/Boot/boot_ban_go.png";
        const string CardPath = "Assets/03 Art/Boot/boot_giay_ghi.png";
        const string TapePath = UiRefreshMenu.TapePath; // băng keo trắng gạch chéo, tô màu được

        const float WoodH = 196, Bleed = 160, Card = 176, Big = 236;
        static readonly string[] Names = { "Tướng", "Sổ thẻ", "Máy Bi", "Đánh tiếp", "Sổ tay" };
        static readonly float[] X = { -412, -214, 0, 214, 412 };
        static readonly float[] Tilt = { 3f, -2f, 0, 2f, -3f };

        // Temp/hub_dock.flag: biên dịch xong và không Play thì dựng một lần rồi xoá cờ (Unity dùng chung nhiều session)
        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += () =>
        {
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            var f = System.IO.Path.GetFullPath(System.IO.Path.Combine(Application.dataPath, "../Temp/hub_dock.flag"));
            if (!System.IO.File.Exists(f)) return;
            System.IO.File.Delete(f);
            Build();
        };

        [MenuItem("PokiClash/Prefab/Sảnh: hàng nút đáy (kệ gỗ, thẻ giấy)", priority = 64)]
        public static void Build()
        {
            var assets = AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiAssets")[0]));
            Theme.Init(assets);
            var wood = AssetDatabase.LoadAssetAtPath<Sprite>(WoodPath);
            var card = Sliced(CardPath, new Vector4(30, 30, 30, 30));
            var tape = AssetDatabase.LoadAssetAtPath<Sprite>(TapePath);
            if (!wood || !card || !tape)
            {
                Debug.LogError("[Sảnh] Thiếu ảnh kit: boot_ban_go, boot_giay_ghi hoặc băng keo tiêu đề.");
                return;
            }
            var root = PrefabUtility.LoadPrefabContents(HubPath);
            try
            {
                var hub = root.GetComponent<HubScene>();
                var so = new SerializedObject(hub);
                var arr = so.FindProperty("bottom");
                var row = root.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == "hang_nut");
                if (!row || arr.arraySize != 5)
                {
                    Debug.LogError("[Sảnh] Không thấy hang_nut hoặc HubScene.bottom không đủ 5 nút.");
                    return;
                }
                var kitButton = Theme.Prefabs.buttonNormal;
                var kitSo = new SerializedObject(kitButton);
                var outlined = (Material)kitSo.FindProperty("labelOutlined").objectReferenceValue;
                var plain = (Material)kitSo.FindProperty("labelPlain").objectReferenceValue;

                // giữ lại: icon, chấm số, nút Máy Bi
                var icons = new Sprite[5];
                var badges = new RectTransform[5];
                var badgeTexts = new TextMeshProUGUI[5];
                SketchButton center = null;
                var keep = Node(root.transform, "giu_tam");
                for (int i = 0; i < 5; i++)
                {
                    var e = arr.GetArrayElementAtIndex(i);
                    var b = (SketchButton)e.FindPropertyRelative("button").objectReferenceValue;
                    badges[i] = (RectTransform)e.FindPropertyRelative("badge").objectReferenceValue;
                    badgeTexts[i] = (TextMeshProUGUI)e.FindPropertyRelative("badgeText").objectReferenceValue;
                    var ic = b ? b.GetComponentsInChildren<Image>(true).FirstOrDefault(x => x.name == "icon") : null;
                    icons[i] = ic ? ic.sprite : null;
                    if (badges[i]) badges[i].SetParent(keep, false);
                    if (i == 2)
                    {
                        center = b;
                        b.transform.SetParent(keep, false);
                    }
                }

                // dựng lại hàng
                foreach (var c in row.GetComponents<HorizontalLayoutGroup>()) Object.DestroyImmediate(c);
                for (int i = row.childCount - 1; i >= 0; i--) Object.DestroyImmediate(row.GetChild(i).gameObject);
                row.anchorMin = new Vector2(0, 0);
                row.anchorMax = new Vector2(1, 0);
                row.pivot = new Vector2(0.5f, 0);
                row.anchoredPosition = Vector2.zero;
                row.sizeDelta = new Vector2(0, WoodH + 90);

                Shelf(row, wood);
                var tapes = new[] { Theme.TapeBlue, Theme.TapePink, Theme.TapeYellow, Theme.TapeGreen, Theme.TapeYellow };
                for (int i = 0; i < 5; i++)
                {
                    SketchButton btn;
                    RectTransform slot;
                    if (i == 2)
                    {
                        slot = Node(row, "nut_" + Names[i]);
                        slot.anchorMin = slot.anchorMax = new Vector2(0.5f, 0);
                        slot.pivot = new Vector2(0.5f, 0.5f);
                        slot.anchoredPosition = new Vector2(X[i], WoodH - 42);
                        float w = ((RectTransform)center.transform).rect.width;
                        slot.sizeDelta = new Vector2(Big, Big);
                        center.transform.SetParent(slot, false);
                        var crt = (RectTransform)center.transform;
                        crt.anchorMin = crt.anchorMax = crt.pivot = new Vector2(0.5f, 0.5f);
                        crt.anchoredPosition = Vector2.zero;
                        crt.localRotation = Quaternion.identity;
                        float k = Big / Mathf.Max(1, w);
                        slot.localScale = new Vector3(k, k, 1);
                        // tên trên băng keo vàng đè mép dưới
                        var ribbon = Img(row, "bang_keo_Máy Bi", tape, new Color(1f, 0.86f, 0.36f, 1f), true);
                        At(ribbon.rectTransform, new Vector2(0.5f, 0), new Vector2(0, WoodH - 42 - Big / 2 + 6), new Vector2(208, 54));
                        ribbon.rectTransform.localEulerAngles = new Vector3(0, 0, -2);
                        var rl = Text(ribbon.transform, "chu", Theme.Bold, 30, Theme.Ink, null);
                        Fill(rl.rectTransform);
                        rl.text = "Máy Bi";
                        btn = center;
                    }
                    else
                    {
                        btn = CardButton(row, Names[i], icons[i], card, tape, tapes[i], Tilt[i], outlined, plain, out slot);
                        slot.anchoredPosition = new Vector2(X[i], WoodH / 2 + 6);
                    }
                    // chấm số: góc trên phải
                    if (badges[i])
                    {
                        badges[i].SetParent(slot, false);
                        badges[i].anchorMin = badges[i].anchorMax = new Vector2(1, 1);
                        badges[i].pivot = new Vector2(0.5f, 0.5f);
                        badges[i].anchoredPosition = i == 2 ? new Vector2(-30, -26) : new Vector2(-14, -12);
                        badges[i].localScale = i == 2 ? Vector3.one / slot.localScale.x : Vector3.one;
                        badges[i].localRotation = Quaternion.identity;
                        badges[i].SetAsLastSibling();
                    }
                    var e = arr.GetArrayElementAtIndex(i);
                    e.FindPropertyRelative("button").objectReferenceValue = btn;
                    e.FindPropertyRelative("badge").objectReferenceValue = badges[i];
                    e.FindPropertyRelative("badgeText").objectReferenceValue = badgeTexts[i];
                }
                so.ApplyModifiedPropertiesWithoutUndo();
                Object.DestroyImmediate(keep.gameObject);
                PrefabUtility.SaveAsPrefabAsset(root, HubPath);
                Debug.Log("[Sảnh] Đã dựng lại hàng nút đáy: kệ gỗ, 4 thẻ giấy, nút Máy Bi nhô lên.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // mép bàn gỗ: ảnh ván dọc xoay ngang trong khung cắt, viền mực trên
        static void Shelf(RectTransform row, Sprite wood)
        {
            var clip = Node(row, "ke_go", typeof(RectMask2D));
            clip.anchorMin = new Vector2(0, 0);
            clip.anchorMax = new Vector2(1, 0);
            clip.pivot = new Vector2(0.5f, 0);
            clip.anchoredPosition = new Vector2(0, -Bleed);
            clip.sizeDelta = new Vector2(240, WoodH + Bleed); // rộng hơn khung 120 mỗi bên (máy rộng)
            var img = Img(clip, "go", wood, Color.white, false);
            img.preserveAspect = false;
            var rt = img.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = new Vector2(WoodH + Bleed + 40, 1600); // xoay 90°: rộng thành cao
            rt.localEulerAngles = new Vector3(0, 0, 90);
            var bg = Img(clip, "phu_toi", null, new Color(0.23f, 0.16f, 0.11f, 0.12f), true); // tối nhẹ cho thẻ nổi
            Fill(bg.rectTransform);
            var ink = Img(clip, "vien_muc", null, Theme.Ink, false);
            var irt = ink.rectTransform;
            irt.anchorMin = new Vector2(0, 1);
            irt.anchorMax = new Vector2(1, 1);
            irt.pivot = new Vector2(0.5f, 1);
            irt.anchoredPosition = Vector2.zero;
            irt.sizeDelta = new Vector2(0, 7);
            // nhận chạm trên kệ (khỏi kéo bản đồ khi chạm hụt nút)
            bg.raycastTarget = true;
        }

        static SketchButton CardButton(RectTransform row, string name, Sprite icon, Sprite card, Sprite tape, Color tapeColor, float tilt,
            Material outlined, Material plain, out RectTransform slot)
        {
            slot = Node(row, "o_" + name);
            slot.anchorMin = slot.anchorMax = new Vector2(0.5f, 0);
            slot.pivot = new Vector2(0.5f, 0.5f);
            slot.sizeDelta = new Vector2(Card, Card);
            slot.localEulerAngles = new Vector3(0, 0, tilt);

            var img = Img(slot, "nut_" + name, card, Theme.CardFill, true, true);
            Fill(img.rectTransform);
            var go = img.gameObject;
            var icn = Img(go.transform, "icon", icon, Color.white, false);
            At(icn.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, 16), new Vector2(104, 104));
            var label = Text(go.transform, "chu", Theme.Bold, 30, Theme.Ink, null);
            At(label.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 30), new Vector2(Card - 12, 40));
            label.text = name;
            var btn = go.AddComponent<SketchButton>();
            btn.Setup(img, label, false, card, card, outlined, plain);
            btn.SetColor(Theme.CardFill);

            var t = Img(slot, "bang_keo", tape, tapeColor, false);
            t.preserveAspect = false;
            At(t.rectTransform, new Vector2(0.5f, 1), new Vector2(0, 2), new Vector2(92, 30));
            t.rectTransform.localEulerAngles = new Vector3(0, 0, -tilt * 2.5f - 4);
            return btn;
        }

        static Sprite Sliced(string path, Vector4 border)
        {
            var ti = AssetImporter.GetAtPath(path) as TextureImporter;
            if (ti && ti.spriteBorder != border)
            {
                ti.spriteBorder = border;
                ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }

        static RectTransform Node(Transform parent, string name, params System.Type[] types)
        {
            var go = new GameObject(name, new[] { typeof(RectTransform) }.Concat(types).ToArray());
            go.layer = LayerMask.NameToLayer("UI");
            var rt = (RectTransform)go.transform;
            rt.SetParent(parent, false);
            return rt;
        }

        static void At(RectTransform rt, Vector2 anchor, Vector2 pos, Vector2 size)
        {
            rt.anchorMin = rt.anchorMax = anchor;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = pos;
            rt.sizeDelta = size;
        }

        static void Fill(RectTransform rt)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
        }

        static Image Img(Transform parent, string name, Sprite s, Color c, bool raycast, bool sliced = false)
        {
            var img = Node(parent, name, typeof(CanvasRenderer), typeof(Image)).GetComponent<Image>();
            Theme.SetSprite(img, s);
            img.color = c;
            img.type = sliced ? Image.Type.Sliced : Image.Type.Simple;
            img.preserveAspect = !sliced && s;
            img.raycastTarget = raycast;
            return img;
        }

        static TextMeshProUGUI Text(Transform parent, string name, TMP_FontAsset font, float size, Color color, Material mat)
        {
            var t = Node(parent, name, typeof(CanvasRenderer), typeof(TextMeshProUGUI)).GetComponent<TextMeshProUGUI>();
            t.font = font;
            if (mat) t.fontSharedMaterial = mat;
            t.fontSize = size;
            t.color = color;
            t.alignment = TextAlignmentOptions.Center;
            t.textWrappingMode = TextWrappingModes.NoWrap;
            t.overflowMode = TextOverflowModes.Overflow;
            t.raycastTarget = false;
            return t;
        }
    }
}
