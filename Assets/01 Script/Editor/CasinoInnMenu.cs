// Hộp Quán trọ (InnDialog, GD_Claude/29_DaoCasino.md mục 6.8, mốc C6). Menu "PokiClash/Prefab/Đảo Casino/Quán trọ: dựng hộp":
// Dialogs/QuanTro = bản sao tờ giấy gốc Dialogs/HopThoai (rộng 1000, cỡ cố định), hình quán trọ cắt từ đảo, tiêu đề, lời bà chủ quán,
// đồng hồ việc mới, 3 dòng việc dựng sẵn (tên việc, thanh tiến độ Kit/bar, quà, nút Nhận / Đã nhận / Đi làm), dòng quà xong cả ngày;
// đăng ký vào UiKit.dialogs để App.Modals.Open<T>() mở. Số dòng = casino.inn.count (3); đổi số việc mỗi ngày thì sửa Rows rồi dựng lại.
// Lượt chụp chung với Chợ đen (CasinoMarketMenu, cờ Temp/casino_market_tour.flag); cờ dựng Temp/casino_market_build.flag dựng cả hai.
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class CasinoInnMenu
    {
        const string SheetBase = "Assets/04 Prefabs/Dialogs/HopThoai.prefab";
        const string DialogPath = "Assets/04 Prefabs/Dialogs/QuanTro.prefab";
        const string InnArt = "Assets/03 Art/Casino/casino_ct_quan_tro.png";
        const int Rows = 3;
        const float SheetW = 1000, RowW = 940, RowH = 196, RowGap = 12, Top = -262;

        static T Load<T>() where T : Object =>
            AssetDatabase.FindAssets("t:" + typeof(T).Name).Select(g => AssetDatabase.LoadAssetAtPath<T>(AssetDatabase.GUIDToAssetPath(g))).FirstOrDefault(a => a);

        static TextMeshProUGUI T(Transform p, string n, float size, Color c, Vector2 anchor, Vector2 pos, Vector2 box, Vector2 pivot,
            TextAlignmentOptions align = TextAlignmentOptions.TopLeft)
        {
            var t = HomeSceneMenu.Text(p, n, size, c, align);
            HomeSceneMenu.At(t.rectTransform, anchor, pos, box, pivot);
            t.enableAutoSizing = true;
            t.fontSizeMin = size * 0.65f;
            t.fontSizeMax = size;
            return t;
        }

        [MenuItem("PokiClash/Prefab/Đảo Casino/Quán trọ: dựng hộp", priority = 76)]
        public static void Build()
        {
            var assets = Load<UiAssets>();
            if (!assets) return;
            Theme.Init(assets);
            var kit = assets.prefabs;
            if (!kit.bar) { Debug.LogError("[Đảo Casino] UiKit thiếu bar (thanh tiến độ)."); return; }
            var root = (GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(SheetBase));
            try
            {
                root.name = "QuanTro";
                var view = root.GetComponent<ModalSheet>();
                view.Configure(SheetW, false, false);
                var sheet = view.Sheet;
                foreach (var f in sheet.GetComponents<ContentSizeFitter>()) Object.DestroyImmediate(f);
                foreach (var l in sheet.GetComponents<LayoutGroup>()) Object.DestroyImmediate(l);
                sheet.anchorMin = sheet.anchorMax = new Vector2(0.5f, 0.5f);
                sheet.pivot = new Vector2(0.5f, 0.5f);
                sheet.anchoredPosition = new Vector2(0, -20);
                float allY = Top - Rows * (RowH + RowGap) - 6;
                sheet.sizeDelta = new Vector2(SheetW, -allY + 190 + 40);
                var page = HomeSceneMenu.Fill(HomeSceneMenu.Node(sheet, "noi_dung"));
                page.SetAsLastSibling();
                var close = view.Close ? (RectTransform)view.Close.transform : null;
                if (close) close.SetAsLastSibling();

                // đầu: hình quán trọ (cắt từ đảo), tiêu đề, lời bà chủ quán, đồng hồ việc mới
                var pic = HomeSceneMenu.Img(page, "hinh_quan", AssetDatabase.LoadAssetAtPath<Sprite>(InnArt), Color.white);
                pic.preserveAspect = true;
                HomeSceneMenu.At(pic.rectTransform, new Vector2(0, 1), new Vector2(34, -22), new Vector2(190, 146), new Vector2(0, 1));
                var title = T(page, "tieu_de", 54, Theme.Ink, new Vector2(0, 1), new Vector2(240, -26), new Vector2(620, 70), new Vector2(0, 1),
                    TextAlignmentOptions.MidlineLeft);
                var sub = T(page, "ba_chu", 24, Theme.Ink2, new Vector2(0, 1), new Vector2(240, -98), new Vector2(700, 80), new Vector2(0, 1));
                var clock = T(page, "dong_ho", 24, Theme.BlueD, new Vector2(0.5f, 1), new Vector2(0, -196), new Vector2(900, 40), new Vector2(0.5f, 1),
                    TextAlignmentOptions.Center);

                var rows = new InnDialog.Row[Rows];
                for (int i = 0; i < Rows; i++)
                {
                    var card = HomeSceneMenu.Img(page, "viec_" + i, Sketch.PanelThin, Theme.Paper, false, true);
                    HomeSceneMenu.At(card.rectTransform, new Vector2(0.5f, 1), new Vector2(0, Top - i * (RowH + RowGap)), new Vector2(RowW, RowH), new Vector2(0.5f, 1));
                    var text = T(card.transform, "ten", 30, Theme.Ink, new Vector2(0, 1), new Vector2(24, -14), new Vector2(620, 44), new Vector2(0, 1));
                    var bar = ((GameObject)PrefabUtility.InstantiatePrefab(kit.bar.gameObject, card.transform)).GetComponent<UiBar>();
                    bar.name = "tien_do";
                    bar.SetKind(UiBar.Kind.Exp);
                    HomeSceneMenu.At((RectTransform)bar.transform, new Vector2(0, 1), new Vector2(24, -70), new Vector2(600, 42), new Vector2(0, 1));
                    var reward = T(card.transform, "qua", 23, Theme.GreenD, new Vector2(0, 1), new Vector2(24, -126), new Vector2(620, 50), new Vector2(0, 1));
                    var act = HomeSceneMenu.Button(assets, card.transform, "hanh_dong", Loc.T("Đi làm"), BtnColor.Green, new Vector2(250, 100));
                    HomeSceneMenu.At((RectTransform)act.transform, new Vector2(1, 0.5f), new Vector2(-20, 0), new Vector2(250, 100), new Vector2(1, 0.5f));
                    rows[i] = new InnDialog.Row { root = card.gameObject, card = card, text = text, reward = reward, bar = bar, act = act };
                }

                // quà xong cả ngày
                var all = HomeSceneMenu.Img(page, "xong_ca_ngay", Sketch.PanelThin, Theme.Paper2, false, true);
                HomeSceneMenu.At(all.rectTransform, new Vector2(0.5f, 1), new Vector2(0, allY), new Vector2(RowW, 170), new Vector2(0.5f, 1));
                var allText = T(all.transform, "ten", 30, Theme.Ink, new Vector2(0, 1), new Vector2(24, -18), new Vector2(620, 44), new Vector2(0, 1));
                var allReward = T(all.transform, "qua", 24, Theme.GreenD, new Vector2(0, 1), new Vector2(24, -76), new Vector2(620, 60), new Vector2(0, 1));
                var allClaim = HomeSceneMenu.Button(assets, all.transform, "nhan_het", Loc.T("Nhận"), BtnColor.Yellow, new Vector2(250, 100));
                HomeSceneMenu.At((RectTransform)allClaim.transform, new Vector2(1, 0.5f), new Vector2(-20, 0), new Vector2(250, 100), new Vector2(1, 0.5f));

                var dlgComp = root.AddComponent<InnDialog>();
                dlgComp.Setup(title, sub, clock, rows, all, allText, allReward, allClaim);
                var dlg = PrefabUtility.SaveAsPrefabAsset(root, DialogPath).GetComponent<InnDialog>();
                kit.dialogs.RemoveAll(x => !x || (x is InnDialog && x != dlg));
                if (!kit.dialogs.Contains(dlg)) kit.dialogs.Add(dlg);
                EditorUtility.SetDirty(kit);
                AssetDatabase.SaveAssets();
                Debug.Log("[Đảo Casino] Đã dựng " + DialogPath);
            }
            finally
            {
                Object.DestroyImmediate(root);
            }
        }
    }
}
