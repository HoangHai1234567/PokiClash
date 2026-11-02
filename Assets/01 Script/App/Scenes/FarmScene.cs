// Trang trại: 8 chỗ làm (icon loại chỗ, hệ hợp, sticker tướng nhún khi làm / ngồi khi hết sức, vòng sức còn, bong bóng bi tích),
// "Thu hoạch", "Tự xếp", "Năng suất ×2" (quảng cáo). Chạm một chỗ mở danh sách chọn tướng (năng suất, thời lượng, hợp hệ, nghỉ còn bao lâu)
// và nút "Rút ra". Chưa có ảnh đảo trang trại: các chỗ xếp lưới 2 cột trên nền trời.
// Prefab màn hình Assets/04 Prefabs/Screens/Farm (nền, khung cuộn, hàng nút, lưới chỗ); mỗi chỗ là bản sao prefab Items/ChoTrangTrai
// (FarmSpotTile), sinh một lần rồi gán lại khi làm mới; danh sách chọn tướng là hộp Dialogs/ChonTuongTrangTrai (FarmPickerDialog).
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class FarmScene : SceneRoot
    {
        public override string Title => "Trang trại";

        [SerializeField] TextMeshProUGUI info, boostLeft;
        [SerializeField] SketchButton harvest, auto, boost;
        [SerializeField] RectTransform grid;
        [SerializeField] LayoutElement gridLayout;
        [SerializeField] FarmSpotTile spotPrefab;
        [SerializeField] FarmPickerDialog pickerPrefab;

        readonly List<FarmSpotTile> spots = new List<FarmSpotTile>();
        float timer;
        bool busy;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        public static string KindIcon(string kind) =>
            kind == "duck" ? "wave" : kind == "veg" ? "seed" : kind == "orchard" ? "leaf" : kind == "bakery" ? "flame" : "hammer";

        public static string Num(double v) => v.ToString("0.##", System.Globalization.CultureInfo.InvariantCulture).Replace('.', ',');

        public static string Dec(double v) => v.ToString("0.0", System.Globalization.CultureInfo.InvariantCulture).Replace('.', ',');

        public static string Clock(double hours)
        {
            int m = (int)Math.Ceiling(Math.Max(0, hours) * 60);
            return m >= 60 ? $"{m / 60}:{m % 60:00}" : $"{m}p";
        }

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI infoText, TextMeshProUGUI boostText, SketchButton harvestButton, SketchButton autoButton, SketchButton boostButton,
            RectTransform gridRt, FarmSpotTile spot, FarmPickerDialog picker)
        {
            info = infoText;
            boostLeft = boostText;
            harvest = harvestButton;
            auto = autoButton;
            boost = boostButton;
            grid = gridRt;
            gridLayout = grid.GetComponent<LayoutElement>();
            spotPrefab = spot;
            pickerPrefab = picker;
        }

        public override void Enter(object args)
        {
            if (!grid) return;
            harvest.SetOnClick(Harvest);
            auto.SetOnClick(AutoAssign);
            boost.SetOnClick(Boost);
            Build();
        }

        public override void Refresh() => Build();

        void Update()
        {
            if (busy || (timer += Time.unscaledDeltaTime) < 10) return;
            Build(); // sức và bi đổi theo giờ
        }

        void Build()
        {
            timer = 0;
            if (!grid) return;
            var s = S;
            var d = D;
            var cfg = d.Cfg;
            double now = Now;
            Farm.Tick(s, d, now);
            var f = Farm.Of(s, cfg, now);

            // hàng nút
            int stock = f.spots.Sum(sp => (int)Math.Floor(sp.stock));
            info.text = $"Tướng làm ra bi theo sức (độ hiếm, cấp, sao), đúng hệ hợp ×{Num(cfg.farm.match)}. Hết sức thì đổi ca; tướng rút ra nghỉ 15–60 phút. Làm ở trang trại không ảnh hưởng ra trận.";
            harvest.SetText($"Thu hoạch ({stock})");
            harvest.Interactable = stock > 0;
            bool boosting = Farm.Boosting(f, now);
            boostLeft.gameObject.SetActive(boosting);
            if (boosting) boostLeft.text = $"Năng suất ×2: còn {Clock((f.boostUntil - now) / 3600000)}";
            boost.gameObject.SetActive(!boosting && Ads.Ready);
            if (!boosting && Ads.Ready) Ads.Bind(boost, "×2 năng suất", Ads.FarmBoost);

            // 8 chỗ, lưới 2 cột
            int rows = (f.spots.Count + 1) / 2;
            gridLayout.preferredHeight = rows * 320 + (rows - 1) * 14;
            int open = Farm.SpotsOpen(cfg, s.level);
            while (spots.Count < f.spots.Count) spots.Add(Ui.Spawn(spotPrefab, grid));
            for (int i = spots.Count - 1; i >= f.spots.Count; i--)
            {
                Destroy(spots[i].gameObject);
                spots.RemoveAt(i);
            }
            for (int i = 0; i < f.spots.Count; i++)
            {
                int k = i;
                spots[i].Bind(d, s, i, i < open, f.spots[i], () => Picker(k));
            }
        }

        // ---------- danh sách chọn tướng ----------

        void Picker(int i)
        {
            App.Modals.Open(pickerPrefab).Show(i, reopen =>
            {
                Build();
                if (reopen) Picker(i);
            });
        }

        // ---------- việc ----------

        void Harvest()
        {
            int n = Farm.Harvest(S, D, Now);
            if (n <= 0) return;
            App.Save.Save();
            App.Audio.Play("coin");
            App.Toasts.Show($"Thu hoạch {n} bi", Icon("ball"));
            Build();
        }

        void AutoAssign()
        {
            var placed = Farm.Auto(S, D, Now);
            App.Save.Save();
            App.Toasts.Show(placed.Count > 0 ? $"Đã xếp {placed.Count} tướng" : "Không còn tướng rảnh hoặc chỗ trống", Icon("team"));
            Build();
        }

        void Boost()
        {
            busy = true;
            Ads.Show(Ads.FarmBoost, ok =>
            {
                busy = false;
                if (ok && Farm.Boost(S, D, Now))
                {
                    App.Save.Save();
                    App.Toasts.Show("Năng suất ×2 trong 1 giờ", Icon("seed"));
                }
                Build();
            });
        }
    }
}
