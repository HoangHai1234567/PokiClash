// Popup ưu đãi kiểu mới (OfferPopup), tông cửa hàng bản 3 (người dùng 2026-11-27 duyệt tông cửa hàng bản 3: "làm popup và trang con cùng tông
// màu này luôn"; GD_Claude/26 mục 15). Menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: popup ưu đãi (PopUuDai)" (chạy lại được, không cần Play)
// dựng:
// - Items/PopCot (OfferPopColumn): ô đứng o_nen tô màu + o_tia sao nổ, tên trắng viền mực trên đầu, hình gói, ruy băng giá trị, lưới ô món
//   (Items/OMonCuaHang của màn cửa hàng), nhãn góc trái, nút giá xanh lá (nut_gia) trong dải tối đáy, chữ "Đã mua";
// - Dialogs/PopUuDai (OfferPopup): biến thể tờ giấy gốc HopThoai, ẩn tờ giấy và băng keo; khung chàm (the_nen tô chàm + caro nen_trang lát),
//   thẻ đầu ba lớp the_nen / the_phai / the_tia như thẻ cửa hàng, hình gói tràn mép trên, ruy băng nhan_gia_tri, tên vàng viền mực trong dải
//   tối đáy thẻ, dòng phụ trắng, chỗ nội dung (lưới / hàng ô), hàng nút miễn phí (Hết bi), nhãn giới hạn + đồng hồ, nút giá to, nút "Hôm nay
//   không hiện nữa" dưới khung, nút đóng góc phải thẻ; thêm vào UiKit.dialogs.
// Sprite bản 3 do ArtGen/Shop/v3/ve_ui.py vẽ (viền 9 mảnh đặt như ShopPageMenu). Prefab Items/PopMon cũ (ô món giấy) không dùng nữa.
// Nhóm chọn một gói (bản 4, 2026-11-27, OfferPopup.ShowGroup): thêm vào PopCot huy hiệu sao nổ (huy_hieu.png, ArtGen/Shop/v3/ve_huy_hieu.py);
// vào PopUuDai nền tối phủ màn (nen_toi), khung bản 3 gom vào khung_ban3 để tắt cả cụm, băng tên (muc_bang), viên đỏ đồng hồ to có icon
// đồng hồ. Dựng + chụp bằng cờ: Editor/OfferGroupTour.cs (Temp/pop_group_build.flag, Temp/pop_group_tour.flag). Ô cột có thêm lớp hoa văn
// lát (hoa_van.png, ArtGen/Shop/v3/ve_hoa_van.py) bật thay sao nổ ở popup nhiều bậc.
// Chụp thử (đang Play): "PokiClash/Thử/Cửa hàng/popup ưu đãi kiểu mới: chụp" → Temp/PokiShots/pop_uu_dai/; sao lưu và trả bản lưu.
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;
using static PokiClash.EditorTools.ShopMenu;

namespace PokiClash.EditorTools
{
    public static class OfferPopupMenu
    {
        const string SheetBase = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string ItemCellPath = "Assets/04 Prefabs/Items/OMonCuaHang.prefab";
        const string ColumnPath = "Assets/04 Prefabs/Items/PopCot.prefab";
        const string PopPath = "Assets/04 Prefabs/Dialogs/PopUuDai.prefab";
        const string V3 = "Assets/03 Art/Shop/v3/";
        static readonly Color Navy = Theme.Hex("#16142a"), Gold = Theme.Hex("#ffd84a"), Page = Theme.Hex("#3b3558"), DoneGreen = Theme.Hex("#a6ff6e");
        // viền 9 mảnh (trái, dưới, phải, trên), trùng ShopPageMenu
        static readonly Vector4 CardBorder = new Vector4(40, 110, 40, 40), TileBorder = new Vector4(34, 104, 34, 34), BtnBorder = new Vector4(36, 36, 36, 36),
            ValueBorder = new Vector4(34, 10, 14, 10);

        [MenuItem("PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: popup ưu đãi (PopUuDai)", priority = 72)]
        public static void Build()
        {
            if (!BakedArt.Current)
            {
                var guid = AssetDatabase.FindAssets("t:BakedArt").FirstOrDefault();
                if (guid != null) BakedArt.Current = AssetDatabase.LoadAssetAtPath<BakedArt>(AssetDatabase.GUIDToAssetPath(guid));
            }
            if (!Theme.Kit)
            {
                var ua = AssetDatabase.FindAssets("t:UiAssets").FirstOrDefault();
                if (ua != null) Theme.Init(AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(ua)));
            }
            var cell = AssetDatabase.LoadAssetAtPath<GameObject>(ItemCellPath)?.GetComponent<ShopItemCell>();
            if (!cell)
            {
                Debug.LogError("[Cửa hàng] Thiếu " + ItemCellPath + " (chạy menu Cửa hàng: chỉ màn cửa hàng trước).");
                return;
            }
            var col = BuildColumn();
            BuildPopup(cell, col);
            AssetDatabase.SaveAssets();
            Debug.Log($"[Cửa hàng] Đã dựng {ColumnPath}, {PopPath} (UiKit), tông bản 3.");
        }

        static GameObject NewRoot(string name, params System.Type[] comps) => Rt(name, null, comps).gameObject;

        static T Save<T>(GameObject root, string path) where T : Component
        {
            try
            {
                return PrefabUtility.SaveAsPrefabAsset(root, path).GetComponent<T>();
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }

        static RectTransform Anchors(RectTransform r, Vector2 min, Vector2 max)
        {
            r.anchorMin = min;
            r.anchorMax = max;
            r.offsetMin = r.offsetMax = Vector2.zero;
            r.pivot = new Vector2(0.5f, 0.5f);
            return r;
        }

        static void Ink(TextMeshProUGUI t, float width)
        {
            t.outlineWidth = width;
            t.outlineColor = Navy;
        }

        static void Auto(TextMeshProUGUI t, float min, float max, bool wrap = false)
        {
            t.enableAutoSizing = true;
            t.fontSizeMin = min;
            t.fontSizeMax = max;
            t.textWrappingMode = wrap ? TextWrappingModes.Normal : TextWrappingModes.NoWrap;
        }

        // sprite bản 3, đặt viền 9 mảnh nếu khác
        static Sprite V3Sprite(string name, Vector4 border)
        {
            string path = V3 + name + ".png";
            var ti = AssetImporter.GetAtPath(path) as TextureImporter;
            if (!ti)
            {
                Debug.LogError($"[Cửa hàng] Thiếu {path}: chạy ArtGen/Shop/v3/ve_ui.py --assets");
                return null;
            }
            if (ti.spriteBorder != border)
            {
                ti.spriteBorder = border;
                ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Sprite>(path);
        }

        static Image Sliced(string name, Transform parent, Sprite s, Color c)
        {
            var img = Img(name, parent, s, c);
            img.type = Image.Type.Sliced;
            img.rectTransform.Stretch();
            return img;
        }

        // nút giá bản 3: tấm xám hai tông viền mực (nut_gia) tô xanh lá; đè đổi tấm tối (nut_gia_an); chữ chép từ nút kit
        static SketchButton PriceButton(Transform parent, string name, float w, float h, float font)
        {
            var kso = new SerializedObject(Kit.buttonNormal);
            var outlined = (Material)kso.FindProperty("labelOutlined").objectReferenceValue;
            var plain = (Material)kso.FindProperty("labelPlain").objectReferenceValue;
            var img = Img(name, parent, V3Sprite("nut_gia", BtnBorder), ShopHue.Lime);
            img.type = Image.Type.Sliced;
            img.raycastTarget = true;
            img.rectTransform.sizeDelta = new Vector2(w, h);
            var src = Kit.buttonNormal.Label;
            var label = Object.Instantiate(src.gameObject, img.transform, false).GetComponent<TextMeshProUGUI>();
            label.name = "chu";
            foreach (var c in label.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(c);
            foreach (var c in label.GetComponents<LayoutElement>()) Object.DestroyImmediate(c);
            for (int i = label.transform.childCount - 1; i >= 0; i--) Object.DestroyImmediate(label.transform.GetChild(i).gameObject);
            Auto(label, 16, font);
            label.fontSize = font;
            label.alignment = TextAlignmentOptions.Center;
            label.raycastTarget = false;
            label.rectTransform.Stretch(22, 8, 22, 18); // chừa môi tối dưới
            var b = img.gameObject.AddComponent<SketchButton>();
            b.Setup(img, label, false, img.sprite, V3Sprite("nut_gia_an", BtnBorder), outlined, plain);
            b.SetRole(BtnColor.Green);
            b.SetColor(ShopHue.Lime);
            b.SetText("Mua");
            return b;
        }

        // ruy băng đỏ "Giá trị ×N" (nhan_gia_tri), neo góc phải trên, chìa ra mép
        static (Image bg, TextMeshProUGUI text) ValueRibbon(Transform parent, TextMeshProUGUI tpl, Vector2 pos, Vector2 size, float font)
        {
            var value = Img("gia_tri", parent, V3Sprite("nhan_gia_tri", ValueBorder), Color.white);
            value.type = Image.Type.Sliced;
            value.rectTransform.Place(new Vector2(1, 1), pos, size, new Vector2(1, 1));
            var t = Text(tpl, value.transform, "chu", font, TextAlignmentOptions.Center, Color.white);
            t.rectTransform.Stretch(size.y * 0.5f, 3, 12, 5);
            Auto(t, 16, font);
            Ink(t, 0.25f);
            return (value, t);
        }

        // cụm hiệu ứng tắt sẵn: quầng sáng phập phồng (Pulse) + vầng tia xoay (Spin) + vùng lấp lánh (Twinkle, các sao dựng sẵn làm con)
        static RectTransform FxGroup(string name, Transform parent, Color glowC, float glowSize, float pulse, Color raysC, float raysSize, float spin,
            Vector2 sparkArea, int sparks)
        {
            var center = new Vector2(0.5f, 0.5f);
            var g = Rt(name, parent);
            g.Place(new Vector2(0.5f, 1), Vector2.zero, new Vector2(10, 10), center);
            var glow = Img("quang", g, V3Sprite("quang", Vector4.zero), glowC);
            glow.rectTransform.Place(center, Vector2.zero, new Vector2(glowSize, glowSize), center);
            var pu = glow.gameObject.AddComponent<Pulse>();
            pu.amount = pulse;
            pu.period = 1.8f;
            var rays = Img("tia", g, V3Sprite("tia_xoay", Vector4.zero), raysC);
            rays.rectTransform.Place(center, Vector2.zero, new Vector2(raysSize, raysSize), center);
            rays.gameObject.AddComponent<Spin>().speed = spin;
            var area = Rt("lap_lanh", g);
            area.Place(center, Vector2.zero, sparkArea, center);
            var stars = new Image[sparks];
            for (int i = 0; i < sparks; i++)
            {
                stars[i] = Img("sao_" + i, area, V3Sprite("lap_lanh", Vector4.zero), Color.white);
                stars[i].rectTransform.Place(center, Vector2.zero, new Vector2(40, 40), center);
                stars[i].rectTransform.localScale = Vector3.zero;
            }
            var tw = area.gameObject.AddComponent<Twinkle>();
            tw.stars = stars;
            tw.color = new Color(1, 0.97f, 0.8f, 1);
            foreach (var gr in g.GetComponentsInChildren<Graphic>(true)) gr.raycastTarget = false;
            g.gameObject.SetActive(false);
            return g;
        }

        // ---------- ô cột ----------

        static OfferPopColumn BuildColumn()
        {
            var (titleTpl, hintTpl) = Templates();
            var root = NewRoot("PopCot", typeof(CanvasRenderer), typeof(Image), typeof(LayoutElement));
            ((RectTransform)root.transform).sizeDelta = new Vector2(280, 500);
            var le = root.GetComponent<LayoutElement>();
            le.preferredWidth = 280;
            le.preferredHeight = 500;
            var bg = root.GetComponent<Image>();
            Theme.SetSprite(bg, V3Sprite("o_nen", TileBorder));
            bg.type = Image.Type.Sliced;
            bg.color = ShopHue.Berry.fill;
            bg.raycastTarget = false;
            var rays = Sliced("tia", root.transform, V3Sprite("o_tia", TileBorder), ShopHue.Berry.rays);
            // hoa văn lát mờ (nhóm chọn một gói / Hết bi bản 4, thay sao nổ): mảnh hình cột trái cửa hàng, nét trắng, trong viền, trên dải đáy
            var pattern = Img("hoa_van", root.transform, V3Sprite("hoa_van", Vector4.zero), new Color(1, 1, 1, 0.2f));
            pattern.type = Image.Type.Tiled;
            pattern.rectTransform.Stretch(14, 14, 14, OfferPopColumn.FootH + 2);
            pattern.gameObject.SetActive(false);

            var head = Text(titleTpl, root.transform, "ten", 40, TextAlignmentOptions.Center, Color.white);
            head.rectTransform.anchorMin = new Vector2(0, 1);
            head.rectTransform.anchorMax = new Vector2(1, 1);
            head.rectTransform.pivot = new Vector2(0.5f, 1);
            head.rectTransform.offsetMin = new Vector2(14, -OfferPopColumn.HeadH);
            head.rectTransform.offsetMax = new Vector2(-14, -8);
            Auto(head, 20, 40);
            Ink(head, 0.3f);

            var art = Img("hinh", root.transform, null, Color.white);
            art.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -OfferPopColumn.HeadH), new Vector2(240, 170), new Vector2(0.5f, 1));
            art.preserveAspect = true;

            var items = Rt("mon", root.transform, typeof(GridLayoutGroup));
            items.anchorMin = Vector2.zero;
            items.anchorMax = Vector2.one;
            items.offsetMin = new Vector2(22, OfferPopColumn.FootH);
            items.offsetMax = new Vector2(-22, -OfferPopColumn.HeadH);
            var grid = items.GetComponent<GridLayoutGroup>();
            grid.spacing = new Vector2(10, 14);
            grid.childAlignment = TextAnchor.MiddleCenter;
            grid.constraint = GridLayoutGroup.Constraint.FixedColumnCount;
            grid.constraintCount = 1;
            grid.cellSize = new Vector2(ShopItemCell.Size, ShopItemCell.Size);

            var (valueBg, valueText) = ValueRibbon(root.transform, titleTpl, new Vector2(10, -OfferPopColumn.HeadH - 4), new Vector2(118, 48), 30);

            // nhãn góc trái ("Nhận ngay"): chìa ra mép trên
            var tag = Img("nhan", root.transform, Sketch.Pill, Theme.GreenD);
            tag.type = Image.Type.Sliced;
            tag.rectTransform.Place(new Vector2(0, 1), new Vector2(-10, 20), new Vector2(172, 48), new Vector2(0, 1));
            tag.rectTransform.localEulerAngles = new Vector3(0, 0, 7);
            var tagText = Text(hintTpl, tag.transform, "chu", 24, TextAlignmentOptions.Center, Color.white);
            tagText.rectTransform.Stretch(8, 2, 8, 2);
            Auto(tagText, 14, 24);
            tagText.fontStyle = FontStyles.Bold;

            var buy = PriceButton(root.transform, "nut_mua", 0, 82, 34);
            var br = buy.Rect;
            br.anchorMin = new Vector2(0.07f, 0);
            br.anchorMax = new Vector2(0.93f, 0);
            br.pivot = new Vector2(0.5f, 0);
            br.anchoredPosition = new Vector2(0, 12);
            br.sizeDelta = new Vector2(0, 82);

            var done = Text(titleTpl, root.transform, "da_mua", 30, TextAlignmentOptions.Center, DoneGreen);
            Anchors(done.rectTransform, new Vector2(0.04f, 0.01f), new Vector2(0.96f, 0.0f));
            done.rectTransform.offsetMax = new Vector2(0, OfferPopColumn.FootH - 10);
            Auto(done, 16, 30, true);
            Ink(done, 0.25f);

            // huy hiệu giá trị (popup chọn một gói, bản 4): sao nổ hồng đè giữa mép trên, "×N" to + "GIÁ TRỊ"; lớp trong thở, lớp ngoài để đập vào
            var badge = Rt("huy_hieu", root.transform);
            badge.Place(new Vector2(0.5f, 1), new Vector2(0, 8), new Vector2(252, 216), new Vector2(0.5f, 0.5f));
            var star = Img("sao", badge, V3Sprite("huy_hieu", Vector4.zero), Color.white);
            star.rectTransform.Stretch();
            star.preserveAspect = true;
            var breathe = star.gameObject.AddComponent<Breathe>();
            breathe.amount = 0.06f;
            breathe.period = 1.5f;
            breathe.lift = 0;
            var badgeText = Text(titleTpl, star.transform, "so", 78, TextAlignmentOptions.Center, Color.white);
            badgeText.rectTransform.Stretch(24, 28, 24, 78);
            Auto(badgeText, 36, 78);
            Ink(badgeText, 0.32f);
            var badgeSub = Text(titleTpl, star.transform, "chu", 30, TextAlignmentOptions.Center, Color.white);
            badgeSub.rectTransform.Stretch(40, 136, 40, 38);
            Auto(badgeSub, 16, 30);
            Ink(badgeSub, 0.3f);
            badge.gameObject.SetActive(false);

            foreach (var gr in root.GetComponentsInChildren<Graphic>(true))
                if (!gr.transform.IsChildOf(buy.transform)) gr.raycastTarget = false;
            buy.GetComponent<Image>().raycastTarget = true;
            root.AddComponent<OfferPopColumn>().Setup(new OfferPopColumn.Parts
            {
                bg = bg, rays = rays, art = art, tag = tag, valueBg = valueBg, head = head, tagText = tagText, valueText = valueText, done = done,
                items = items, grid = grid, buy = buy, badge = badge, badgeText = badgeText, badgeSub = badgeSub, pattern = pattern,
                plainFoot = V3Sprite("o_tron_nut", TileBorder), plainBare = V3Sprite("o_tron", new Vector4(34, 34, 34, 34)),
            });
            return Save<OfferPopColumn>(root, ColumnPath);
        }

        // ---------- popup ----------

        static void BuildPopup(ShopItemCell cell, OfferPopColumn column)
        {
            var kit = Kit;
            var (titleTpl, hintTpl) = Templates();
            const float W = OfferPopup.W, In = OfferPopup.Inset, HH = OfferPopup.HeaderH;
            var center = new Vector2(0.5f, 0.5f);
            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetBase));
            try
            {
                root.name = "PopUuDai";
                var view = root.GetComponent<ModalSheet>();
                view.Configure(W, false, false);
                view.SetFlat(true); // khung thẳng, không nghiêng như tờ giấy
                var dc = view.Dim.color;
                view.Dim.color = new Color(dc.r, dc.g, dc.b, 0.8f);
                var sheet = view.Sheet;
                foreach (var f in sheet.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(f);
                foreach (var l in sheet.GetComponents<LayoutGroup>()) Object.DestroyImmediate(l);
                // ẩn tờ giấy gốc (nền, khâu chỉ, lưới, băng keo), giữ nút đóng
                var paper = sheet.GetComponent<Image>();
                if (paper) paper.enabled = false;
                var close = (RectTransform)view.Close.transform;
                foreach (Transform c in sheet)
                    if (c != close) c.gameObject.SetActive(false);
                sheet.anchorMin = sheet.anchorMax = center;
                sheet.pivot = center;
                sheet.anchoredPosition = new Vector2(0, -30);
                sheet.sizeDelta = new Vector2(W, 1470);

                // nền tối phủ cả màn của nhóm chọn một (bản 4; tắt sẵn, OfferPopup.ShowGroup bật): tấm chàm rất tối to hơn màn + caro mờ; chặn
                // chạm (chỉ nút X đóng, khỏi lỡ tay chạm khe giữa hai ô)
                var backdrop = Img("nen_toi", sheet, null, new Color(0.055f, 0.047f, 0.12f, 0.9f));
                backdrop.rectTransform.Place(center, Vector2.zero, new Vector2(3200, 5600), center);
                backdrop.raycastTarget = true;
                var backCaro = Img("caro", backdrop.transform, V3Sprite("nen_trang", Vector4.zero), new Color(1, 1, 1, 0.06f));
                backCaro.type = Image.Type.Tiled;
                backCaro.rectTransform.Stretch();
                backdrop.gameObject.SetActive(false);

                // khung chàm viền mực + caro lát (như trang cửa hàng bản 3)
                var frameRoot = Rt("khung_ban3", sheet);
                frameRoot.Stretch();
                var frame = Sliced("khung", frameRoot, V3Sprite("the_nen", CardBorder), Page);
                frame.raycastTarget = true; // chạm vào khung không đóng popup
                var caro = Img("caro", frameRoot, V3Sprite("nen_trang", Vector4.zero), new Color(1, 1, 1, 0.55f));
                caro.type = Image.Type.Tiled;
                caro.rectTransform.Stretch(18, 18, 18, 18);

                // thẻ đầu ba lớp như thẻ cửa hàng
                var header = Rt("dau", sheet);
                header.Place(new Vector2(0.5f, 1), new Vector2(0, -In), new Vector2(W - 2 * In, HH), new Vector2(0.5f, 1));
                var headBg = Sliced("nen", header, V3Sprite("the_nen", CardBorder), ShopHue.Berry.fill);
                var headPanel = Sliced("mang_phai", header, V3Sprite("the_phai", CardBorder), ShopHue.Berry.panel);
                var headRays = Sliced("sao_no", header, V3Sprite("the_tia", CardBorder), ShopHue.Berry.rays);
                // tên vàng viền mực trong dải tối đáy thẻ
                var title = Text(titleTpl, header, "ten", 60, TextAlignmentOptions.Center, Gold);
                title.rectTransform.anchorMin = new Vector2(0, 0);
                title.rectTransform.anchorMax = new Vector2(1, 0);
                title.rectTransform.pivot = new Vector2(0.5f, 0);
                title.rectTransform.offsetMin = new Vector2(40, 10);
                title.rectTransform.offsetMax = new Vector2(-40, 96);
                Auto(title, 30, 60);
                Ink(title, 0.3f);

                // cụm hiệu ứng (bản 4, tắt sẵn; OfferPopup.HeadFx đặt chỗ và bật): sau băng tên / hình gói / huy hiệu
                var fxPack = FxGroup("fx_goi", sheet, new Color(1, 0.9f, 0.55f, 0.6f), 560, 0.07f, new Color(1, 0.84f, 0.3f, 0.5f), 500, 10,
                    new Vector2(420, 380), 5);
                var fxBadge = FxGroup("fx_gia_tri", sheet, new Color(1, 0.5f, 0.72f, 0.55f), 380, 0.1f, new Color(1, 0.62f, 0.8f, 0.55f), 340, -22,
                    new Vector2(300, 260), 3);

                // nhóm chọn một (bản 4): băng tím tên vàng bên phải hình gói, ngay dưới là viên đỏ đồng hồ to (tắt sẵn)
                var banner = Img("bang_ten", sheet, V3Sprite("muc_bang", new Vector4(30, 30, 30, 30)), Color.white);
                banner.type = Image.Type.Sliced;
                banner.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(130, -112), new Vector2(640, 116), center);
                banner.rectTransform.localEulerAngles = new Vector3(0, 0, 2);
                var bannerTitle = Text(titleTpl, banner.transform, "ten", 60, TextAlignmentOptions.Center, Gold);
                bannerTitle.rectTransform.Stretch(40, 8, 40, 16);
                Auto(bannerTitle, 30, 60);
                Ink(bannerTitle, 0.3f);
                banner.gameObject.SetActive(false);
                var bigTimerBg = Img("dong_ho_to", sheet, V3Sprite("vien", new Vector4(24, 24, 24, 24)), Theme.Hex("#d8224e"));
                bigTimerBg.type = Image.Type.Sliced;
                bigTimerBg.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(150, -240), new Vector2(540, 84), center);
                var clock = Img("icon", bigTimerBg.transform, AssetDatabase.LoadAssetAtPath<Sprite>("Assets/03 Art/Fallback/Icons/clock.png"), Color.white);
                clock.preserveAspect = true;
                clock.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(-18, 4), new Vector2(104, 104), center);
                var bigTimerText = Text(titleTpl, bigTimerBg.transform, "chu", 46, TextAlignmentOptions.Center, Color.white);
                bigTimerText.rectTransform.Stretch(70, 6, 22, 12);
                Auto(bigTimerText, 24, 46);
                Ink(bigTimerText, 0.28f);
                bigTimerBg.gameObject.SetActive(false);

                // hình gói tràn quá mép trên (tâm; OfferPopup.Layout đặt chỗ)
                var pack = Img("hinh_goi", sheet, null, Color.white);
                pack.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -155), new Vector2(430, 430), center);
                pack.preserveAspect = true;

                // huy hiệu giá trị ở đầu (gói theo ngày, bản 4; tắt sẵn): sao nổ hồng cạnh viên đồng hồ, dưới băng tên
                var headBadge = Rt("huy_hieu_dau", sheet);
                headBadge.Place(new Vector2(0.5f, 1), new Vector2(392, -236), new Vector2(236, 204), center);
                headBadge.localEulerAngles = new Vector3(0, 0, -6);
                var hbStar = Img("sao", headBadge, V3Sprite("huy_hieu", Vector4.zero), Color.white);
                hbStar.rectTransform.Stretch();
                hbStar.preserveAspect = true;
                var hbBreathe = hbStar.gameObject.AddComponent<Breathe>();
                hbBreathe.amount = 0.06f;
                hbBreathe.period = 1.5f;
                hbBreathe.lift = 0;
                var headBadgeText = Text(titleTpl, hbStar.transform, "so", 74, TextAlignmentOptions.Center, Color.white);
                headBadgeText.rectTransform.Stretch(22, 26, 22, 74);
                Auto(headBadgeText, 34, 74);
                Ink(headBadgeText, 0.32f);
                var headBadgeSub = Text(titleTpl, hbStar.transform, "chu", 28, TextAlignmentOptions.Center, Color.white);
                headBadgeSub.rectTransform.Stretch(36, 128, 36, 36);
                Auto(headBadgeSub, 14, 28);
                Ink(headBadgeSub, 0.3f);
                headBadge.gameObject.SetActive(false);

                // ruy băng giá trị: chìa ra mép phải thẻ đầu
                var (valueBg, valueText) = ValueRibbon(sheet, titleTpl, new Vector2(-In + 12, -In - 60), new Vector2(300, 72), 38);

                var sub = Text(hintTpl, sheet, "dong_phu", 30, TextAlignmentOptions.Center, Color.white);
                sub.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -HH - 60), new Vector2(880, 64), center);
                Auto(sub, 18, 30, true);
                Ink(sub, 0.2f);

                // nội dung: lưới ô món hoặc hàng ô cột
                var content = Rt("noi_dung", sheet);
                content.Place(new Vector2(0.5f, 1), new Vector2(0, -HH - 104), new Vector2(OfferPopup.ContentW, 500), new Vector2(0.5f, 1));
                // ngày 3 của gói theo ngày (tắt sẵn): quầng + tia + lấp lánh sau các ô (trước lưới / hàng)
                var fxDay = FxGroup("fx_ngay3", content, new Color(1, 0.86f, 0.45f, 0.55f), 560, 0.08f, new Color(1, 0.82f, 0.25f, 0.45f), 510, 14,
                    new Vector2(400, 380), 4);
                var gridRt = Rt("luoi", content, typeof(GridLayoutGroup));
                gridRt.Stretch();
                var grid = gridRt.GetComponent<GridLayoutGroup>();
                grid.childAlignment = TextAnchor.UpperCenter;
                grid.spacing = new Vector2(20, 20);
                var rowRt = Rt("hang", content, typeof(HorizontalLayoutGroup));
                rowRt.Stretch();
                var row = rowRt.GetComponent<HorizontalLayoutGroup>();
                row.childAlignment = TextAnchor.UpperCenter;
                row.spacing = 18;
                row.childControlWidth = row.childControlHeight = false;
                row.childForceExpandWidth = row.childForceExpandHeight = false;
                // mũi tên cong ngày 1 → 2 → 3 (tắt sẵn), trên các ô
                var arrows = new Image[2];
                for (int i = 0; i < arrows.Length; i++)
                {
                    arrows[i] = Img("mui_ten_" + (i + 1), content, V3Sprite("mui_ten", Vector4.zero), Color.white);
                    arrows[i].rectTransform.Place(new Vector2(0.5f, 1), Vector2.zero, new Vector2(190, 173), center);
                    arrows[i].preserveAspect = true;
                    arrows[i].gameObject.SetActive(false);
                }

                // hàng nút miễn phí của popup Hết bi (xem quảng cáo nhận bi, Tới Nhà)
                var freeRow = Rt("mien_phi", sheet, typeof(HorizontalLayoutGroup));
                freeRow.Place(new Vector2(0.5f, 1), new Vector2(0, -1150), new Vector2(880, 104), new Vector2(0.5f, 1));
                var fl = freeRow.GetComponent<HorizontalLayoutGroup>();
                fl.spacing = 20;
                fl.childAlignment = TextAnchor.MiddleCenter;
                fl.childControlWidth = fl.childControlHeight = false;
                fl.childForceExpandWidth = fl.childForceExpandHeight = false;
                var freeAd = PriceButton(freeRow, "nut_qc", 420, 100, 34);
                freeAd.SetColor(Theme.Blue);
                freeAd.SetText("Xem");
                var freeHome = PriceButton(freeRow, "nut_nha", 420, 100, 34);
                freeHome.SetText("Tới Nhà");
                freeRow.gameObject.SetActive(false);

                // nhãn giới hạn + đồng hồ: viên chàm chữ trắng
                var pills = Rt("nhan", sheet, typeof(HorizontalLayoutGroup));
                pills.Place(new Vector2(0.5f, 1), new Vector2(0, -1140), new Vector2(880, 54), new Vector2(0.5f, 1));
                var hl = pills.GetComponent<HorizontalLayoutGroup>();
                hl.spacing = 16;
                hl.childAlignment = TextAnchor.MiddleCenter;
                hl.childControlWidth = hl.childControlHeight = false;
                hl.childForceExpandWidth = hl.childForceExpandHeight = false;
                TextMeshProUGUI Pill(string n, float w, out GameObject go)
                {
                    var img = Img(n, pills, Sketch.Pill, new Color(Navy.r, Navy.g, Navy.b, 0.9f));
                    img.type = Image.Type.Sliced;
                    img.rectTransform.sizeDelta = new Vector2(w, 54);
                    var t = Text(hintTpl, img.transform, "chu", 26, TextAlignmentOptions.Center, Color.white);
                    t.rectTransform.Stretch(12, 2, 12, 2);
                    Auto(t, 16, 26);
                    t.fontStyle = FontStyles.Bold;
                    go = img.gameObject;
                    return t;
                }
                var limit = Pill("gioi_han", 270, out var limitPill);
                var timer = Pill("dong_ho", 330, out var timerPill);

                // nút giá to xanh lá (khung tâm để thở)
                var wrap = Rt("nut_mua_khung", sheet);
                wrap.Place(new Vector2(0.5f, 1), new Vector2(0, -1290), new Vector2(600, 136), center);
                var buy = PriceButton(wrap, "nut_mua", 560, 128, 56);
                buy.Rect.Place(center, Vector2.zero, new Vector2(560, 128), center);

                // "Hôm nay không hiện nữa" dưới khung
                var mute = Ui.Spawn(kit.buttonSmall, sheet);
                mute.name = "nut_tat";
                mute.Rect.Place(new Vector2(0.5f, 1), new Vector2(0, -1500), new Vector2(480, mute.Rect.sizeDelta.y), new Vector2(0.5f, 1));
                mute.SetRole(BtnColor.Paper);
                mute.SetText("Hôm nay không hiện nữa");

                // nút đóng của tờ gốc: góc phải trên thẻ đầu
                close.anchorMin = close.anchorMax = new Vector2(1, 1);
                close.pivot = center;
                close.anchoredPosition = new Vector2(-30, -30);
                close.SetAsLastSibling();

                foreach (var gr in sheet.GetComponentsInChildren<Graphic>(true))
                    if (gr != frame && gr != backdrop && !gr.transform.IsChildOf(buy.transform) && !gr.transform.IsChildOf(mute.transform) &&
                        !gr.transform.IsChildOf(close) && !gr.transform.IsChildOf(freeRow))
                        gr.raycastTarget = false;
                buy.GetComponent<Image>().raycastTarget = freeAd.GetComponent<Image>().raycastTarget = freeHome.GetComponent<Image>().raycastTarget = true;

                var dlg = root.AddComponent<OfferPopup>();
                dlg.Setup(new OfferPopup.Parts
                {
                    sheet = sheet, header = header, value = valueBg.rectTransform, content = content, pills = pills, buyWrap = wrap, closeBtn = close,
                    headBg = headBg, headPanel = headPanel, headRays = headRays, packArt = pack, title = title, sub = sub, valueText = valueText,
                    limit = limit, timer = timer, grid = grid, row = row, limitPill = limitPill, timerPill = timerPill, buy = buy, mute = mute,
                    freeRow = freeRow, freeAd = freeAd, freeHome = freeHome,
                    frame = frameRoot.gameObject, backdrop = backdrop.gameObject, banner = banner.rectTransform, bigTimer = bigTimerBg.rectTransform,
                    bannerTitle = bannerTitle, bigTimerText = bigTimerText, bigTimerBg = bigTimerBg,
                    headBadge = headBadge, headBadgeText = headBadgeText, headBadgeSub = headBadgeSub,
                    fxPack = fxPack, fxBadge = fxBadge, fxDay = fxDay, arrows = arrows,
                }, cell, column);
                var saved = PrefabUtility.SaveAsPrefabAsset(root, PopPath).GetComponent<OfferPopup>();
                if (!kit.dialogs.Any(x => x is OfferPopup))
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

        // ---------- chụp thử ----------

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();

        [MenuItem("PokiClash/Thử/Cửa hàng/popup ưu đãi kiểu mới: chụp (đang Play)", priority = 158)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Cửa hàng] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(RunTour());
        }

        static IEnumerator RunTour()
        {
            var dir = Path.Combine(PlayTour.ShotDir, "pop_uu_dai");
            if (Directory.Exists(dir)) Directory.Delete(dir, true);
            Directory.CreateDirectory(dir);
            int n = 0;
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            IEnumerator Shot(string name, float wait)
            {
                yield return new WaitForSecondsRealtime(wait);
                yield return new WaitForEndOfFrame();
                var tex = ScreenCapture.CaptureScreenshotAsTexture();
                File.WriteAllBytes(Path.Combine(dir, $"{n++:00}_{name}.jpg"), tex.EncodeToJPG(88));
                Object.Destroy(tex);
            }
            IEnumerator Show(Popup p, string name)
            {
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.25f);
                ShopSheet.OpenPopup(p, null);
                yield return Shot(name + "_vao", 0.3f);
                yield return Shot(name, 1.2f);
                App.Modals.CloseAll();
            }
            // sảnh lúc chưa đụng bản lưu (thanh trên: nút bánh răng neo góc phải, 2026-11-27)
            App.Modals.CloseAll();
            yield return Shot("sanh", 0.4f);
            try
            {
                var c = D.Cfg.shop;
                Tutorial.Skip(S);
                S.shop = null;
                var st = Shop.Of(S);
                st.installAt = Now - 5 * 86400000.0;
                st.sessions = 5;
                S.level = Mathf.Max(S.level, 12);
                var b = st.offers;

                // 1. Quà Nhập Môn (3 cột ngày), có nút "Hôm nay không hiện nữa"
                Offers.EnsureStarter(S, D, Now);
                var starter = b.active.Find(o => o.pack == "starter3");
                if (starter != null)
                {
                    starter.until = Now + 71 * 3600000.0;
                    yield return Show(new Popup { kind = "offer", id = starter.uid, key = "starter3" }, "qua_nhap_mon");
                    starter.until = Now;
                }

                // 2. Khởi Hành 3 bậc (cột bậc)
                double until = Now + 48 * 3600000.0;
                foreach (var pk in c.packs.Where(q => q.group == "launch").OrderBy(q => q.price))
                    b.active.Add(new ActiveOffer { uid = pk.id + "_" + (++b.seq), tpl = pk.id, pack = pk.id, price = pk.price, created = Now, until = until });
                var lead = b.active.Find(o => o.pack == "launch" && !o.bought && o.until > Now);
                if (lead != null) yield return Show(new Popup { kind = "offer", id = lead.uid, key = "launch", free = true }, "khoi_hanh");
                foreach (var o in b.active.Where(o => o.pack != null && c.Pack(o.pack)?.group == "launch")) o.until = Now;

                // 3. Vượt Mốc (tướng), 4. Ưu Đãi Nóng, 5. Tiếp Sức (lưới ô món)
                var ms = Offers.MilestoneStages(D, Elem.Thuy);
                string hero = ms.Count >= 6 ? Teams.StageLead(ms[5], D).hero : null;
                if (hero != null)
                {
                    S.Hero(hero).owned = false;
                    var jump = Offers.Build(S, D, "jump", hero, Now, new Rng(1));
                    yield return Show(new Popup { kind = "offer", id = jump.uid, key = "jump" }, "vuot_moc");
                    jump.until = Now;
                }
                foreach (var tpl in new[] { "hot", "relief" })
                {
                    var o = Offers.Build(S, D, tpl, null, Now, new Rng(2));
                    if (o == null) continue;
                    yield return Show(new Popup { kind = "offer", id = o.uid, key = tpl }, tpl == "hot" ? "uu_dai_nong" : "tiep_suc");
                    o.until = Now;
                }

                // 6. Hết bi lần đầu (chỉ cách miễn phí), Hết bi (3 gói), Sắp hết bi (có nút Hôm nay không hiện nữa)
                yield return Show(new Popup { kind = "refill", first = true, free = true }, "het_bi_lan_dau");
                yield return Show(new Popup { kind = "refill", free = true }, "het_bi");
                yield return Show(new Popup { kind = "refill", warn = true }, "sap_het_bi");

                // 7. chip bi chỉ hiện ở máy bi / đảo Casino; túi bi đầy thì số đỏ (2026-11-27)
                App.Modals.CloseAll();
                S.balls = BallBag.Cap(S, D.Cfg, Now) + 5;
                foreach (var (scene, name) in new[] { (SceneIds.Machine, "may_bi_tui_day"), (SceneIds.Hub, "sanh_sau") })
                {
                    App.Router.Go(scene);
                    yield return new WaitForSecondsRealtime(0.3f);
                    for (float t = 0; (App.Router.Busy || App.Router.Current != scene) && t < 20; t += Time.unscaledDeltaTime) yield return null;
                    App.Modals.CloseAll();
                    App.Bars.Refresh();
                    yield return Shot(name, 1.2f);
                }
                Debug.Log("[Cửa hàng] Xong chụp popup ưu đãi kiểu mới: " + dir);
            }
            finally
            {
                App.Modals.CloseAll();
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
        }
    }
}
