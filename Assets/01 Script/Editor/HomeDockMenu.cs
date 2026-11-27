// Hàng nút đáy màn Nhà làm lại (người dùng 2026-11-27: "thiết kế lại phần này phải có 1 nền đằng sau, có thể làm giống phần đảo chính,
// icon quá nhỏ"). Trước: 4 nút tròn 112 px (icon 64 px) trôi trên bản đồ, chữ trong viên giấy nhỏ. Nay như hàng nút đáy sảnh (HubDockMenu):
// - kệ gỗ: mép bàn gỗ (boot_ban_go xoay ngang) chạy suốt đáy màn, viền mực trên, tràn xuống quá mép an toàn, nhận chạm (chạm hụt nút không
//   kéo bản đồ);
// - 4 thẻ giấy ghi chú (boot_giay_ghi, 9 mảnh) 176 px nghiêng nhẹ so le, băng keo màu theo việc (Xây lục, Lát ô vàng, Thu hết hồng,
//   Ra đảo lam) dán mép trên, icon 112 px, chữ dưới icon; xếp giữa bằng HorizontalLayoutGroup nên chế độ Xây / Lát ô (chỉ còn thẻ "Xong")
//   thẻ nằm giữa kệ;
// - chấm đỏ góc trên phải thẻ Thu hết khi có đồ chờ thu.
// Mỗi thẻ vẫn là HomeRingButton (HomeScene đổi chữ / icon Xây ↔ Xong, bật tắt thẻ theo chế độ, chấm đỏ) bọc SketchButton của thẻ, nên
// không phải sửa HomeScene. Chữ trên thẻ: Pangolin màu mực, không dùng chữ đen đậm (người dùng 2026-11-27).
// Menu "PokiClash/Prefab/Nhà và side meta/Nhà: hàng nút đáy (kệ gỗ, thẻ giấy)" hoặc cờ Temp/home_dock.flag: dựng lại riêng hang_nut_nha
// trong Screens/Home và nối lại HomeScene (hud*, btn*). HomeCrittersMenu.BuildUi gọi BuildBar nên dựng lại cả lớp nha_ui cũng ra kiểu này.
using System.Linq;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using M = PokiClash.EditorTools.HomeSceneMenu;

namespace PokiClash.EditorTools
{
    public static class HomeDockMenu
    {
        const string ScreenPath = "Assets/04 Prefabs/Screens/Home.prefab";
        const string WoodPath = "Assets/03 Art/Boot/boot_ban_go.png";
        const string CardPath = "Assets/03 Art/Boot/boot_giay_ghi.png";
        const string BarName = "hang_nut_nha";
        const float WoodH = 196, Bleed = 160, Card = 176, IconSz = 112, Gap = 66;
        static readonly string[] Names = { "xay", "lat", "thu", "ra_dao" };
        static readonly string[] Labels = { "Xây", "Lát ô", "Thu hết", "Ra đảo" };
        static readonly string[] Icons = { "hammer", "pencil", "seed", "map" };
        static readonly float[] Tilt = { 3f, -2f, 2f, -3f };

        // Temp/home_dock.flag: biên dịch xong và không Play thì dựng một lần rồi xoá cờ (Unity dùng chung nhiều phiên)
        static double nextPoll;

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            var f = System.IO.Path.GetFullPath(System.IO.Path.Combine(Application.dataPath, "../Temp/home_dock.flag"));
            if (!System.IO.File.Exists(f)) return;
            System.IO.File.Delete(f);
            Patch();
        }

        [MenuItem("PokiClash/Prefab/Nhà và side meta/Nhà: hàng nút đáy (kệ gỗ, thẻ giấy)", priority = 66)]
        public static void Patch()
        {
            var assets = M.Load<UiAssets>();
            Theme.Init(assets);
            var root = PrefabUtility.LoadPrefabContents(ScreenPath);
            try
            {
                var scene = root.GetComponentInChildren<HomeScene>(true);
                var old = root.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == BarName);
                if (!scene || !old || !(old.parent is RectTransform ui))
                {
                    Debug.LogError($"[Nhà] Không thấy HomeScene hoặc {BarName} trong {ScreenPath}");
                    return;
                }
                int idx = old.GetSiblingIndex();
                Object.DestroyImmediate(old.gameObject);
                var hud = BuildBar(ui);
                hud[0].transform.parent.parent.SetSiblingIndex(idx);
                var so = new SerializedObject(scene);
                string[] hudF = { "hudBuild", "hudPaint", "hudHarvest", "hudSail" }, btnF = { "btnBuild", "btnPaint", "btnHarvest", "btnSail" };
                for (int i = 0; i < 4; i++)
                {
                    so.FindProperty(hudF[i]).objectReferenceValue = hud[i];
                    so.FindProperty(btnF[i]).objectReferenceValue = hud[i].Button;
                }
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(root, ScreenPath);
                Debug.Log("[Nhà] Đã dựng lại hàng nút đáy: kệ gỗ, 4 thẻ giấy (Xây, Lát ô, Thu hết, Ra đảo).");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        // dựng hang_nut_nha dưới ui (lớp nha_ui, trong vùng an toàn); trả 4 thẻ theo thứ tự Xây, Lát ô, Thu hết, Ra đảo
        public static HomeRingButton[] BuildBar(RectTransform ui)
        {
            var art = M.Load<ArtLibrary>();
            var wood = AssetDatabase.LoadAssetAtPath<Sprite>(WoodPath);
            var card = Sliced(CardPath, new Vector4(30, 30, 30, 30));
            var tape = AssetDatabase.LoadAssetAtPath<Sprite>(UiRefreshMenu.TapePath);
            var body = Theme.Body;

            var bar = M.Node(ui, BarName);
            bar.anchorMin = new Vector2(0, 0);
            bar.anchorMax = new Vector2(1, 0);
            bar.pivot = new Vector2(0.5f, 0);
            bar.anchoredPosition = Vector2.zero;
            bar.sizeDelta = new Vector2(0, WoodH + 40);
            bar.SetAsLastSibling();
            Shelf(bar, wood);

            var row = M.Node(bar, "the", typeof(HorizontalLayoutGroup));
            M.At(row, new Vector2(0.5f, 0), new Vector2(0, WoodH / 2 + 6), new Vector2(1040, Card), new Vector2(0.5f, 0.5f));
            var hl = row.GetComponent<HorizontalLayoutGroup>();
            hl.spacing = Gap;
            hl.childAlignment = TextAnchor.MiddleCenter;
            hl.childControlWidth = hl.childControlHeight = false;
            hl.childForceExpandWidth = hl.childForceExpandHeight = false;

            var tapes = new[] { Theme.TapeGreen, Theme.TapeYellow, Theme.TapePink, Theme.TapeBlue };
            var res = new HomeRingButton[4];
            for (int i = 0; i < 4; i++)
                res[i] = CardButton(row, Names[i], Labels[i], art ? art.Icon(Icons[i]) : null, card, tape, tapes[i], Tilt[i], body);
            return res;
        }

        // mép bàn gỗ: ảnh ván dọc xoay ngang trong khung cắt, viền mực trên (như HubDockMenu.Shelf)
        static void Shelf(RectTransform bar, Sprite wood)
        {
            var clip = M.Node(bar, "ke_go", typeof(RectMask2D));
            clip.anchorMin = new Vector2(0, 0);
            clip.anchorMax = new Vector2(1, 0);
            clip.pivot = new Vector2(0.5f, 0);
            clip.anchoredPosition = new Vector2(0, -Bleed);
            clip.sizeDelta = new Vector2(240, WoodH + Bleed); // rộng hơn khung 120 mỗi bên (máy rộng)
            if (wood)
            {
                var img = M.Img(clip, "go", wood, Color.white);
                img.preserveAspect = false;
                var rt = img.rectTransform;
                rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
                rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(WoodH + Bleed + 40, 1600); // xoay 90°: rộng thành cao
                rt.localEulerAngles = new Vector3(0, 0, 90);
            }
            var bg = M.Img(clip, "phu_toi", null, new Color(0.23f, 0.16f, 0.11f, wood ? 0.12f : 1f), true); // tối nhẹ cho thẻ nổi; nhận chạm
            M.Fill(bg.rectTransform);
            var ink = M.Img(clip, "vien_muc", null, Theme.Ink);
            var irt = ink.rectTransform;
            irt.anchorMin = new Vector2(0, 1);
            irt.anchorMax = new Vector2(1, 1);
            irt.pivot = new Vector2(0.5f, 1);
            irt.anchoredPosition = Vector2.zero;
            irt.sizeDelta = new Vector2(0, 7);
        }

        // thẻ giấy: khung (HomeRingButton, nghiêng) → nền giấy (SketchButton) → icon, chữ; băng keo mép trên; chấm đỏ góc trên phải
        static HomeRingButton CardButton(RectTransform row, string name, string label, Sprite icon, Sprite card, Sprite tape, Color tapeColor,
            float tilt, TMP_FontAsset font)
        {
            var slot = M.Node(row, name);
            slot.sizeDelta = new Vector2(Card, Card);
            slot.localEulerAngles = new Vector3(0, 0, tilt);

            var img = M.Img(slot, "nut", card, Theme.CardFill, true, true);
            M.Fill(img.rectTransform);
            var icn = M.Img(img.transform, "icon", icon, Color.white);
            icn.preserveAspect = true;
            M.At(icn.rectTransform, new Vector2(0.5f, 0.5f), new Vector2(0, 16), new Vector2(IconSz, IconSz), new Vector2(0.5f, 0.5f));
            var cap = M.Text(img.transform, "chu", 32, Theme.Ink);
            if (font)
            {
                cap.font = font;
                cap.fontSharedMaterial = font.material;
            }
            cap.fontStyle = FontStyles.Normal;
            cap.textWrappingMode = TextWrappingModes.NoWrap;
            cap.enableAutoSizing = true;
            cap.fontSizeMin = 22;
            cap.fontSizeMax = 32;
            M.At(cap.rectTransform, new Vector2(0.5f, 0), new Vector2(0, 28), new Vector2(Card - 16, 40), new Vector2(0.5f, 0.5f));
            cap.text = label;
            var btn = img.gameObject.AddComponent<SketchButton>();
            btn.Setup(img, cap, false, card, card, null, null);
            btn.SetColor(Theme.CardFill);

            if (tape)
            {
                var t = M.Img(slot, "bang_keo", tape, tapeColor);
                t.preserveAspect = false;
                M.At(t.rectTransform, new Vector2(0.5f, 1), new Vector2(0, 2), new Vector2(92, 30), new Vector2(0.5f, 0.5f));
                t.rectTransform.localEulerAngles = new Vector3(0, 0, -tilt * 2.5f - 4);
            }
            var dot = M.Img(slot, "cham", Sketch.Dot, Theme.Red);
            M.At(dot.rectTransform, new Vector2(1, 1), new Vector2(-8, -8), new Vector2(36, 36), new Vector2(0.5f, 0.5f));
            dot.gameObject.SetActive(false);

            var hb = slot.gameObject.AddComponent<HomeRingButton>();
            hb.Setup(btn, icn, cap, null, null, dot.gameObject);
            return hb;
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
    }
}
