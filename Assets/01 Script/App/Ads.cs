// Lớp móc quảng cáo thưởng và cửa hàng (change add-monetization-hooks). Tính năng chỉ gọi Ads.Show(chỗ đặt, done) và Store.Buy(gói, done).
// Cổng AdGate giữ giới hạn mỗi ngày: xem xong mới trừ lượt rồi done(true); bỏ ngang thì done(false), không trừ lượt.
// Đã mua "Bỏ quảng cáo" thì trao thưởng ngay (vẫn trừ lượt). SDK thật gắn vào Ads.Current / Store.Current;
// bản dev dùng quảng cáo và cửa hàng giả lập (App/Dev/FakeMonetization.cs). Chưa có SDK thì Ready = false: các nút ẩn.
using System;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using UnityEngine;

namespace PokiClash
{
    public interface IRewardAds
    {
        // done(true) khi xem xong, done(false) khi bỏ giữa chừng hoặc không tải được
        void Show(string placement, Action<bool> done);
    }

    public interface IStore
    {
        // done(true) khi cửa hàng báo mua thành công
        void Buy(string product, Action<bool> done);
    }

    public static class Ads
    {
        // chỗ đặt quảng cáo
        public const string TreeDouble = AdGate.TreeDouble, AfkChestOpen = AdGate.AfkChestOpen, AfkBoost = AdGate.AfkBoost,
            CaveExtra = AdGate.CaveExtra, FarmBoost = AdGate.FarmBoost,
            FreeBalls = AdGate.FreeBalls, FreeEgg = AdGate.FreeEgg, BattleRetry = AdGate.BattleRetry, WinDouble = AdGate.WinDouble,
            ChestUpgrade = AdGate.ChestUpgrade, DailyGiftAd = AdGate.DailyGift; // cửa hàng (GD_Claude/26 mục 8.1)

        public static IRewardAds Current;

        static SaveData S => App.Save.Data;
        static int Today => Afk.Today(SaveService.Now());

        public static bool NoAds => AdGate.NoAds(S);
        public static bool Ready => Current != null || NoAds;
        public static int Left(string p) => AdGate.Left(S, App.Data.Cfg, Today, p);

        public static void Show(string placement, Action<bool> done)
        {
            if (Left(placement) <= 0)
            {
                App.Toasts.Show(Loc.T("Hết lượt hôm nay"), App.Art.Icon("tv"));
                done?.Invoke(false);
                return;
            }
            // Bỏ quảng cáo; Thẻ Phiêu Lưu: 1 lượt trao ngay mỗi ngày (GD_Claude/26 mục 6.8)
            if (NoAds || Shop.UseAdSkip(S, App.Data.Cfg.shop, SaveService.Now()))
            {
                Grant();
                return;
            }
            if (Current == null)
            {
                done?.Invoke(false);
                return;
            }
            Current.Show(placement, ok =>
            {
                if (ok) Grant();
                else done?.Invoke(false);
            });

            void Grant()
            {
                bool ok = AdGate.Use(S, App.Data.Cfg, Today, placement);
                if (ok) Shop.OnAd(S, SaveService.Now()); // bảng mốc quảng cáo hôm nay, chặn popup bán 5 giây
                ShopLog.Event(ok ? "ad_done" : "ad_fail", placement, 0);
                App.Save.Save();
                done?.Invoke(ok);
            }
        }

        // nút quảng cáo: ghi số lượt còn hôm nay (chỗ không giới hạn thì không ghi), hết lượt thì xám "Hết lượt hôm nay"
        public static void Bind(SketchButton b, string label, string placement, bool can = true)
        {
            int left = Left(placement);
            var t = b.Label;
            if (!t.enableAutoSizing)
            {
                t.fontSizeMax = t.fontSize;
                t.fontSizeMin = 16;
                t.textWrappingMode = TMPro.TextWrappingModes.NoWrap;
                t.enableAutoSizing = true;
            }
            b.SetText(left <= 0 ? Loc.T("Hết lượt hôm nay") : left >= AdGate.Unlimited ? label : $"{label} ({left})");
            b.Interactable = left > 0 && can;
            var tv = b.transform.Find("tv"); // hết lượt: không còn quảng cáo để xem, bỏ hình TV cho chữ đủ chỗ
            if (tv) tv.gameObject.SetActive(left > 0);
        }
    }

    public static class Store
    {
        public static IStore Current;
        public static Func<string, string> PriceText; // SDK cửa hàng trả giá đã bản địa hoá theo mã sản phẩm (chưa có: ShopService.Price tự ghi)

        public static bool Ready => Current != null;

        // trả tiền một mã sản phẩm, không trao gì (ShopService trao bằng lõi Shop sau khi done(true))
        public static void Pay(string product, Action<bool> done)
        {
            if (Current == null)
            {
                App.Toasts.Show(Loc.T("Cửa hàng chưa sẵn sàng"), App.Art.Icon("lock"));
                done?.Invoke(false);
                return;
            }
            Current.Buy(product, ok => done?.Invoke(ok));
        }

        // mua xong thì ghi quyền lợi ngay (AdGate.Buy) và lưu
        public static void Buy(string product, Action<bool> done)
        {
            if (Current == null)
            {
                done?.Invoke(false);
                return;
            }
            Current.Buy(product, ok =>
            {
                if (ok) ok = AdGate.Buy(App.Save.Data, App.Data.Cfg, product, SaveService.Now());
                if (ok) App.Save.Save();
                done?.Invoke(ok);
            });
        }
    }
}
