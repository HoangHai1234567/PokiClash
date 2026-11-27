// Hai cột icon ở sảnh kiểu ô vuông (người dùng 2026-11-27, gửi ảnh cột icon màn máy bi Clash of Critters: "các icon gói 2 bên đều rất to
// rõ ràng, hình vuông bo tròn và có viền trắng, tôi muốn bạn làm y hệt"). Mỗi icon là ô vuông bo tròn cạnh ShopMenu.HubTileSize: viền
// trắng giấy + viền mực tay (Shop/v3/o_san_vien), lòng ô tô màu tươi có nét chì, caro thoi mờ (o_san_nen; ArtGen/Shop/v3/ve_ui.py
// hub_tile), hình to tràn mép trên và thở, tên / đồng hồ chữ trắng viền mực ở đáy ô, chấm đỏ góc trên phải.
// Hai cột nằm trong App.prefab (giao diện sảnh chung LobbyDock, 2026-11-27: sống qua sảnh, Nhà, đảo Casino; trước ở Screens/Hub):
// - Cột trái (Lọ Bi + 3 ưu đãi, HubShop): ShopMenu.BuildHub dựng lại nhóm "cua_hang_san".
// - Cột phải (cot_cong_trinh, HubBuilding kiểu ô): Đền Huy Hiệu, Hang Tiềm Năng, Sổ Phép đổi từ huy hiệu vành vàng (HubBadgeMenu) sang
//   ô vuông; hình riêng không vành Assets/03 Art/Icons/san_den, san_hang, san_so_phep (GPT 2.6, ArtGen/Hud/o_san/cat_hinh.py).
// Menu "PokiClash/Prefab/Sảnh và đảo/Nút sảnh: ô vuông hai cột" hoặc cờ Temp/hub_tile_build.flag (chạy khi Unity không Play, không biên
// dịch). Chạy lại được. Menu "Nút sảnh: huy hiệu" dựng lại cột phải kiểu cũ: chạy menu này sau nó.
using System.IO;
using System.Linq;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HubTileMenu
    {
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string AppPath = "Assets/04 Prefabs/App/App.prefab";
        // nút AFK thanh trên (TopBars.afkBtn; người dùng 2026-11-27 "ô thời gian afk kia quá nhỏ"): 200 × 76, đồng hồ 68 -> 260 × 96, 96
        const float AfkW = 260, AfkH = 96, AfkClock = 96;
        const string Dir = "Assets/03 Art/Icons/";

        // icon công trình (HubScene.Buildings) -> hình trong ô, màu lòng ô (tương phản với hình: đền đỏ kem -> trời, hang nâu -> nho,
        // sổ đỏ -> lá)
        static readonly (string icon, string sprite, Color hue)[] Cards =
        {
            ("crown", "san_den", ShopHue.Sky.fill), ("rock", "san_hang", ShopHue.Grape.fill), ("pencil", "san_so_phep", ShopHue.Mint.fill),
        };

        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/hub_tile_build.flag"));
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

        [MenuItem("PokiClash/Prefab/Sảnh và đảo/Nút sảnh: ô vuông hai cột")]
        static void Build()
        {
            if (!BakedArt.Current)
            {
                var guid = AssetDatabase.FindAssets("t:BakedArt").FirstOrDefault();
                if (guid != null) BakedArt.Current = AssetDatabase.LoadAssetAtPath<BakedArt>(AssetDatabase.GUIDToAssetPath(guid));
            }
            var ua = AssetDatabase.FindAssets("t:UiAssets").FirstOrDefault();
            if (ua != null) Theme.Init(AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(ua)));
            ShopMenu.BuildHub();
            Side();
            Afk();
            AssetDatabase.SaveAssets();
            Debug.Log("[Nút sảnh ô vuông] Xong");
        }

        static void Side()
        {
            var (tpl, _) = ShopMenu.Templates();
            var (nenS, vienS, dayS) = ShopMenu.HubTileSprites();
            float T = ShopMenu.HubTileSize, over = ShopMenu.HubTileOver, step = ShopMenu.HubStep;
            // cột công trình ở App.prefab (giao diện sảnh chung LobbyDock, 2026-11-27)
            var contents = PrefabUtility.LoadPrefabContents(LobbyDockMenu.AppPath);
            try
            {
                var hub = contents.GetComponentInChildren<LobbyDock>(true);
                if (!hub)
                {
                    Debug.LogError("[Nút sảnh ô vuông] App.prefab chưa có LobbyDock (menu \"Sảnh chung: dời ...\")");
                    return;
                }
                var arr = new SerializedObject(hub).FindProperty("buildings");
                var items = HubScene.Buildings;
                RectTransform col = null;
                for (int i = 0; i < arr.arraySize && i < items.Length; i++)
                {
                    var b = arr.GetArrayElementAtIndex(i).objectReferenceValue as HubBuilding;
                    if (!b) continue;
                    var slot = (RectTransform)b.transform;
                    col = (RectTransform)slot.parent;
                    slot.anchorMin = slot.anchorMax = slot.pivot = new Vector2(0.5f, 1);
                    slot.sizeDelta = new Vector2(T, T);
                    slot.anchoredPosition = new Vector2(0, -over - i * step);
                    slot.localEulerAngles = Vector3.zero;
                    var card = Cards.FirstOrDefault(c => c.icon == items[i].icon);
                    if (card.sprite == null) continue; // Nhà, Cây bi: ẩn hẳn ở cột
                    var pic = AssetDatabase.LoadAssetAtPath<Sprite>(Dir + card.sprite + ".png");
                    if (!pic)
                    {
                        Debug.LogError("[Nút sảnh ô vuông] Thiếu " + Dir + card.sprite + ".png (ArtGen/Hud/o_san/cat_hinh.py)");
                        continue;
                    }
                    Tile(b, slot, pic, card.hue, nenS, vienS, dayS, tpl, i * 0.31f);
                    EditorUtility.SetDirty(b);
                    Debug.Log("[Nút sảnh ô vuông] " + items[i].name + " -> " + card.sprite);
                }
                if (col)
                {
                    col.sizeDelta = new Vector2(T + 8, over + step * arr.arraySize);
                    col.anchoredPosition = new Vector2(-8, col.anchoredPosition.y);
                }
                PrefabUtility.SaveAsPrefabAsset(contents, LobbyDockMenu.AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        static void Afk()
        {
            var contents = PrefabUtility.LoadPrefabContents(AppPath);
            try
            {
                var bars = contents.GetComponentInChildren<TopBars>(true);
                var btn = bars ? new SerializedObject(bars).FindProperty("afkBtn").objectReferenceValue as SketchButton : null;
                if (!btn)
                {
                    Debug.LogError("[Nút sảnh ô vuông] App.prefab không có TopBars.afkBtn");
                    return;
                }
                var rt = btn.Rect;
                var old = rt.sizeDelta;
                rt.sizeDelta = new Vector2(AfkW, AfkH);
                var le = btn.GetComponent<LayoutElement>();
                if (le)
                {
                    le.preferredWidth = AfkW;
                    le.preferredHeight = AfkH;
                }
                // đồng hồ nhô mép trái như cũ, to theo nút
                var clock = rt.Find("dong_ho") as RectTransform;
                if (clock)
                {
                    clock.sizeDelta = new Vector2(AfkClock, AfkClock);
                    clock.anchoredPosition = new Vector2(-18, 4);
                }
                // chữ (số bi / giờ AFK): chừa chỗ đồng hồ, to hơn
                var label = btn.Label;
                if (label)
                {
                    var lrt = label.rectTransform;
                    lrt.anchoredPosition = new Vector2(AfkClock * 0.25f + 2, lrt.anchoredPosition.y);
                    lrt.sizeDelta = new Vector2(-(AfkClock * 0.92f), lrt.sizeDelta.y);
                    label.enableAutoSizing = true;
                    label.fontSizeMin = 18;
                    label.fontSizeMax = 46;
                    label.fontSize = 46;
                }
                EditorUtility.SetDirty(btn);
                Debug.Log($"[Nút sảnh ô vuông] Nút AFK: {old} -> {rt.sizeDelta}");
                PrefabUtility.SaveAsPrefabAsset(contents, AppPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        static void Tile(HubBuilding b, RectTransform slot, Sprite pic, Color hue, Sprite nenS, Sprite vienS, Sprite dayS, TextMeshProUGUI tpl, float phase)
        {
            float T = ShopMenu.HubTileSize;
            // lòng ô = khung nhận chạm cũ (ClickCatcher), tô màu lúc Bind
            var bg = b.Bg;
            Theme.SetSprite(bg, nenS);
            bg.type = Image.Type.Simple;
            bg.preserveAspect = false;
            bg.color = hue;
            bg.raycastTarget = true;
            var brt = bg.rectTransform;
            brt.anchorMin = Vector2.zero;
            brt.anchorMax = Vector2.one;
            brt.offsetMin = brt.offsetMax = Vector2.zero;
            brt.localEulerAngles = Vector3.zero;
            // viền trắng giấy: con đầu của lòng ô (dưới hình, chữ)
            var vien = bg.transform.Find("vien_o") as RectTransform;
            if (!vien) vien = ShopMenu.Img("vien_o", bg.transform, vienS, Color.white).rectTransform;
            var vi = vien.GetComponent<Image>();
            Theme.SetSprite(vi, vienS);
            vi.color = Color.white;
            vi.raycastTarget = false;
            vien.anchorMin = Vector2.zero;
            vien.anchorMax = Vector2.one;
            vien.offsetMin = vien.offsetMax = Vector2.zero;
            vien.SetSiblingIndex(0);
            // hình to, tràn mép trên, thở lệch pha
            var icon = b.Icon;
            Theme.SetSprite(icon, pic);
            icon.type = Image.Type.Simple;
            icon.preserveAspect = true;
            icon.color = Color.white;
            icon.raycastTarget = false;
            var irt = icon.rectTransform;
            irt.SetParent(bg.transform, false);
            irt.anchorMin = irt.anchorMax = new Vector2(0.5f, 1);
            irt.pivot = new Vector2(0.5f, 0.5f);
            irt.anchoredPosition = new Vector2(0, -T * 0.42f + 4);
            irt.sizeDelta = new Vector2(T * 1.02f, T * 0.92f);
            irt.localEulerAngles = Vector3.zero;
            irt.SetSiblingIndex(1);
            var br = icon.GetComponent<Breathe>();
            if (!br) br = icon.gameObject.AddComponent<Breathe>();
            br.amount = 0.06f;
            br.period = 1.8f;
            br.phase = phase;
            // lớp đen mờ đáy ô dưới chữ (trên hình, dưới chữ)
            var day = bg.transform.Find("day_o") as RectTransform;
            if (!day) day = ShopMenu.Img("day_o", bg.transform, dayS, Color.white).rectTransform;
            var di = day.GetComponent<Image>();
            Theme.SetSprite(di, dayS);
            di.color = Color.white;
            di.raycastTarget = false;
            day.anchorMin = Vector2.zero;
            day.anchorMax = Vector2.one;
            day.offsetMin = day.offsetMax = Vector2.zero;
            day.SetSiblingIndex(2);
            // tên: chữ trắng viền mực ở đáy ô (gỡ băng tối của kiểu huy hiệu)
            var label = b.Label;
            var band = label.transform.parent && label.transform.parent.name == "bang_ten" ? label.transform.parent : bg.transform.Find("bang_ten");
            var lrt = label.rectTransform;
            lrt.SetParent(bg.transform, false);
            if (band) Object.DestroyImmediate(band.gameObject);
            lrt.anchorMin = new Vector2(0, 0);
            lrt.anchorMax = new Vector2(1, 0);
            lrt.pivot = new Vector2(0.5f, 0);
            lrt.offsetMin = new Vector2(8, 10);
            lrt.offsetMax = new Vector2(-8, 10 + ShopMenu.HubLabelH);
            lrt.localEulerAngles = Vector3.zero;
            lrt.SetAsLastSibling();
            if (tpl)
            {
                label.font = tpl.font;
                label.fontSharedMaterial = tpl.fontSharedMaterial;
                label.fontStyle = tpl.fontStyle;
            }
            label.enableAutoSizing = true;
            label.fontSizeMin = 14;
            label.fontSizeMax = ShopMenu.HubLabelSize;
            label.fontSize = ShopMenu.HubLabelSize;
            label.lineSpacing = -18;
            label.alignment = TextAlignmentOptions.Bottom;
            label.textWrappingMode = TextWrappingModes.Normal;
            label.color = Color.white;
            label.raycastTarget = false;
            ShopPageMenu.Ink(label, 0.28f);
            // băng keo thẻ giấy: tắt; chấm báo: góc trên phải, đè viền trắng
            var tape = slot.Find("bang_keo");
            if (tape) tape.gameObject.SetActive(false);
            var drt = b.Dot.rectTransform;
            drt.anchorMin = drt.anchorMax = new Vector2(1, 1);
            drt.pivot = new Vector2(0.5f, 0.5f);
            drt.anchoredPosition = new Vector2(-12, -10);
            drt.SetAsLastSibling();
            b.SetTile(true, hue);
        }
    }
}
