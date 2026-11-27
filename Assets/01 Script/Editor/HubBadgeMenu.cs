// Nút sảnh kiểu huy hiệu (người dùng 2026-11-27: ba icon bánh răng, Hang Tiềm Năng, Sổ Phép "bị chìm vào phần back, không đẹp và nhỏ
// quá. Gen lại cho nổi bật hơn"). Ảnh: ArtGen/Hud/nut_sanh (Magnific GPT 2.6 nền trong, cat_nut.py) -> 03 Art/Hud/nut_so_tay,
// nut_hang, nut_so_phep.png: vành vàng đinh tán, lòng màu đậm (xanh than, tím, xanh lục) để nổi trên nền tuyết / giấy sáng.
// Menu "PokiClash/Prefab/Sảnh và đảo/Nút sảnh: huy hiệu" hoặc cờ Temp/hub_badge_build.flag (chạy khi Unity không Play, không biên dịch):
// - App.prefab, nút Sổ tay của thanh Hud (TopBars.notebookBtn): nền thành huy hiệu bánh răng (sprite thường = sprite nhấn, nút vẫn
//   lún / nảy), tắt lõi màu và icon bánh răng cũ, to thành TopSize; giữ mép phải chỗ cũ (nút neo phải, ngoài hàng layout);
// - App.prefab (giao diện sảnh chung LobbyDock, 2026-11-27; trước ở Screens/Hub), cột công trình: thẻ Hang Tiềm Năng, Sổ Phép thành huy hiệu BadgeSize (HubBuilding kiểu badge: khung giấy trong suốt
//   giữ làm vùng chạm), tên chữ sáng trên băng tối đè mép dưới huy hiệu, tắt băng keo; các thẻ giãn ra Pitch cho băng tên khỏi đè
//   huy hiệu dưới. Thẻ chưa có ảnh huy hiệu (Đền Huy Hiệu) giữ thẻ giấy.
// Chạy lại được. Menu dựng lại cột (HubMapMenu "Sảnh bản đồ thế giới") tạo lại thẻ giấy: chạy menu này sau nó.
using System.IO;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HubBadgeMenu
    {
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string AppPath = "Assets/04 Prefabs/App/App.prefab";
        const string Dir = "Assets/03 Art/Hud/";
        const float TopSize = 120, BadgeSize = 128, Pitch = 172;
        static readonly Color Band = Theme.Hex("#2e1f45"); // băng tên: tím than như lòng huy hiệu
        static readonly (string icon, string sprite)[] Cards = { ("rock", "nut_hang"), ("pencil", "nut_so_phep") };

        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/hub_badge_build.flag"));
        static double nextPoll;

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            if (!File.Exists(Flag)) return;
            File.Delete(Flag);
            Build();
        }

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Nút sảnh: huy hiệu")]
        static void Build()
        {
            var guids = AssetDatabase.FindAssets("t:UiAssets");
            if (guids.Length > 0) Theme.Init(AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(guids[0])));
            Notebook();
            Side();
            AssetDatabase.SaveAssets();
            Debug.Log("[Nút sảnh] Xong");
        }

        static Sprite Load(string name)
        {
            var s = AssetDatabase.LoadAssetAtPath<Sprite>(Dir + name + ".png");
            if (!s) Debug.LogError("[Nút sảnh] Thiếu ảnh " + Dir + name + ".png (chạy ArtGen/Hud/nut_sanh/cat_nut.py)");
            return s;
        }

        static void Notebook()
        {
            var badge = Load("nut_so_tay");
            if (!badge) return;
            var contents = PrefabUtility.LoadPrefabContents(AppPath);
            try
            {
                var bars = contents.GetComponentInChildren<TopBars>(true);
                var btn = bars ? new SerializedObject(bars).FindProperty("notebookBtn").objectReferenceValue as SketchButton : null;
                if (!btn)
                {
                    Debug.LogError("[Nút sảnh] App.prefab không có TopBars.notebookBtn");
                    return;
                }
                var so = new SerializedObject(btn);
                var bg = so.FindProperty("bg").objectReferenceValue as Image;
                var core = so.FindProperty("core").objectReferenceValue as Image;
                so.FindProperty("normal").objectReferenceValue = badge;
                so.FindProperty("pressed").objectReferenceValue = badge;
                so.ApplyModifiedPropertiesWithoutUndo();
                Theme.SetSprite(bg, badge);
                bg.type = Image.Type.Simple;
                bg.preserveAspect = true;
                if (core && core != bg) core.gameObject.SetActive(false);
                foreach (var img in btn.GetComponentsInChildren<Image>(true))
                    if (img != bg && img != core) img.gameObject.SetActive(false); // icon bánh răng cũ
                var rt = btn.Rect;
                var old = rt.sizeDelta;
                rt.sizeDelta = new Vector2(TopSize, TopSize);
                // nút neo phải: giữ mép phải chỗ cũ, to thêm về bên trái và đều trên dưới
                rt.anchoredPosition += new Vector2(-(TopSize - old.x) * (1 - rt.pivot.x), 0);
                var le = btn.GetComponent<LayoutElement>();
                if (le && !le.ignoreLayout)
                {
                    le.preferredWidth = TopSize;
                    le.preferredHeight = TopSize;
                }
                EditorUtility.SetDirty(btn);
                Debug.Log($"[Nút sảnh] Sổ tay: {old} -> {rt.sizeDelta}, neo {rt.anchorMin}, chỗ {rt.anchoredPosition}");
                PrefabUtility.SaveAsPrefabAsset(contents, AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // cột công trình nằm trong App.prefab (giao diện sảnh chung LobbyDock, 2026-11-27)
        static void Side()
        {
            var contents = PrefabUtility.LoadPrefabContents(LobbyDockMenu.AppPath);
            try
            {
                var hub = contents.GetComponentInChildren<LobbyDock>(true);
                if (!hub)
                {
                    Debug.LogError("[Nút sảnh] App.prefab chưa có LobbyDock (menu \"Sảnh chung: dời ...\")");
                    return;
                }
                var arr = new SerializedObject(hub).FindProperty("buildings");
                var items = HubScene.Buildings;
                for (int i = 0; i < arr.arraySize && i < items.Length; i++)
                {
                    var b = arr.GetArrayElementAtIndex(i).objectReferenceValue as HubBuilding;
                    // cột đã đổi sang ô vuông (HubTileMenu, 2026-11-27): không dựng lại huy hiệu + băng tên tối đè lên
                    if (!b || b.Tile) continue;
                    var slot = (RectTransform)b.transform;
                    slot.anchoredPosition = new Vector2(slot.anchoredPosition.x, -i * Pitch);
                    string sprite = null;
                    foreach (var (icon, s) in Cards)
                        if (items[i].icon == icon) sprite = s;
                    if (sprite == null) continue;
                    var badge = Load(sprite);
                    if (!badge) continue;
                    Card(b, slot, badge);
                    EditorUtility.SetDirty(b);
                    Debug.Log("[Nút sảnh] thẻ " + items[i].name + " -> " + sprite);
                }
                PrefabUtility.SaveAsPrefabAsset(contents, LobbyDockMenu.AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        static void Card(HubBuilding b, RectTransform slot, Sprite badge)
        {
            var bg = b.Bg;
            var icon = b.Icon;
            var label = b.Label;
            b.SetBadge(true);
            bg.color = Color.clear; // Bind cũng đặt trong suốt; vẫn nhận chạm
            Theme.SetSprite(icon, badge);
            icon.type = Image.Type.Simple;
            icon.preserveAspect = true;
            icon.color = Color.white;
            var irt = icon.rectTransform;
            irt.anchorMin = irt.anchorMax = new Vector2(0.5f, 1);
            irt.pivot = new Vector2(0.5f, 1);
            irt.anchoredPosition = new Vector2(0, 6);
            irt.sizeDelta = new Vector2(BadgeSize, BadgeSize);
            // băng tên tối đè mép dưới huy hiệu (dựng lại nếu đã có)
            var band = bg.transform.Find("bang_ten") as RectTransform;
            if (!band)
            {
                var go = new GameObject("bang_ten", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                go.layer = LayerMask.NameToLayer("UI");
                band = (RectTransform)go.transform;
                band.SetParent(bg.transform, false);
            }
            band.SetAsLastSibling();
            var bi = band.GetComponent<Image>();
            Theme.SetSprite(bi, Sketch.Pill);
            bi.type = bi.sprite && bi.sprite.border != Vector4.zero ? Image.Type.Sliced : Image.Type.Simple;
            bi.color = Band;
            bi.raycastTarget = false;
            band.anchorMin = band.anchorMax = new Vector2(0.5f, 0);
            band.pivot = new Vector2(0.5f, 0.5f);
            band.anchoredPosition = new Vector2(0, 2);
            band.sizeDelta = new Vector2(150, 40);
            var lrt = label.rectTransform;
            lrt.SetParent(band, false);
            lrt.anchorMin = Vector2.zero;
            lrt.anchorMax = Vector2.one;
            lrt.pivot = new Vector2(0.5f, 0.5f);
            lrt.offsetMin = new Vector2(10, 3);
            lrt.offsetMax = new Vector2(-10, -3);
            lrt.localEulerAngles = Vector3.zero;
            label.font = Theme.Bold;
            if (Theme.Bold) label.fontSharedMaterial = Theme.Bold.material;
            label.fontStyle = FontStyles.Normal;
            label.enableAutoSizing = true;
            label.fontSizeMin = 14;
            label.fontSizeMax = 22;
            label.alignment = TextAlignmentOptions.Center;
            label.color = HubBuilding.BadgeLabel;
            label.raycastTarget = false;
            // băng keo của thẻ giấy: tắt; chấm báo: góc trên phải huy hiệu
            var tape = slot.Find("bang_keo");
            if (tape) tape.gameObject.SetActive(false);
            var drt = b.Dot.rectTransform;
            drt.anchorMin = drt.anchorMax = new Vector2(1, 1);
            drt.anchoredPosition = new Vector2(-14, -8);
        }
    }
}
