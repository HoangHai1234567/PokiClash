// Dịch vụ cửa hàng (GD_Claude/26_CuaHang_IAP_QuangCao.md): mua qua cửa hàng thật (Store.Pay, bản dev là cửa hàng giả lập), trao bằng lõi
// Shop / Offers, lưu, hiện quà (hộp mở rương ChestBox), nở trứng (EggHatchView), dùng vé chọn tướng, nhận quà miễn phí, quảng cáo thưởng của cửa
// hàng. Ghi sự kiện đo (ShopLog) cho việc chỉnh số sau này (mục 9.6). Màn nào cũng gọi qua đây, không gọi Shop.Buy* trực tiếp.
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using UnityEngine;

namespace PokiClash
{
    public static class ShopService
    {
        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static ShopConfig C => App.Data.Cfg.shop;
        static double Now => SaveService.Now();
        static Rng R => new Rng(Rng.RandomSeed());

        // giá hiện trên nút: cửa hàng thật trả chuỗi đã bản địa hoá (Store.PriceText); chưa có thì bảng tạm theo bậc giá
        public static string Price(double usd)
        {
            if (usd <= 0) return Loc.T("Miễn phí");
            var store = Store.PriceText?.Invoke(ShopConfig.Product(usd));
            if (!string.IsNullOrEmpty(store)) return store;
            if (Loc.IsEn) return "$" + usd.ToString("0.00", System.Globalization.CultureInfo.InvariantCulture);
            int[] vnd = { 25000, 49000, 75000, 125000, 249000, 499000, 749000, 999000, 1249000, 2499000 };
            double[] usdT = { 0.99, 1.99, 2.99, 4.99, 9.99, 19.99, 29.99, 39.99, 49.99, 99.99 };
            int i = Array.FindIndex(usdT, x => Math.Abs(x - usd) < 0.005);
            int v = i >= 0 ? vnd[i] : (int)Math.Round(usd * 25000 / 1000) * 1000;
            return v.ToString("#,0", System.Globalization.CultureInfo.InvariantCulture).Replace(",", ".") + "đ";
        }

        public static string Product(ShopPack p) => p.kind == "noads" ? ShopConfig.NoAdsProduct : ShopConfig.Product(p.price);

        // ---------- mua ----------

        static void Pay(string product, string what, double usd, Action<bool> done)
        {
            ShopLog.Event("iap_start", what, usd);
            Store.Pay(product, ok =>
            {
                ShopLog.Event(ok ? "iap_done" : "iap_fail", what, usd);
                done(ok);
            });
        }

        // gói cố định; done(true) khi đã trao (quà đã hiện)
        public static void BuyPack(string id, Action<bool> done = null)
        {
            var p = C.Pack(id);
            if (p == null || !Shop.CanBuy(S, D, p, Now))
            {
                App.Toasts.Show(Loc.T("Gói này không mua được nữa"), App.Art.Icon("lock"));
                done?.Invoke(false);
                return;
            }
            Pay(Product(p), "pack:" + id, p.price, ok =>
            {
                if (!ok)
                {
                    done?.Invoke(false);
                    return;
                }
                var got = Shop.BuyPack(S, D, id, Now, R);
                // gói trứng (mục Trứng): mua xong nở luôn, khỏi qua hộp nhận
                if (p.tab == "eggs" && got != null && got.Count > 0 && got.All(r => r.k == RewardKind.Egg))
                {
                    App.Save.Save();
                    ShopLog.Event("egg_buy", id, p.price);
                    HatchMany(got.GroupBy(r => Eggs.TierOf(r.id)).Select(g => (g.Key, g.Sum(r => r.n))).ToList(), () => done?.Invoke(true));
                    return;
                }
                Bought(p.Name, got, done);
            });
        }

        // ưu đãi đang mở (popup hẹn giờ)
        public static void BuyOffer(string uid, Action<bool> done = null)
        {
            var o = Shop.FindOffer(S, uid);
            if (o == null || o.bought || o.until > 0 && o.until <= Now)
            {
                App.Toasts.Show(Loc.T("Ưu đãi đã hết giờ"), App.Art.Icon("clock"));
                done?.Invoke(false);
                return;
            }
            var pack = o.pack != null ? C.Pack(o.pack) : null;
            double price = pack?.price ?? o.price;
            string product = pack != null ? Product(pack) : ShopConfig.Product(price);
            Pay(product, "offer:" + o.tpl, price, ok =>
            {
                if (!ok)
                {
                    done?.Invoke(false);
                    return;
                }
                var got = Shop.BuyOffer(S, D, uid, Now, R);
                if (pack != null && pack.id == "starter3") Offers.EnsureStarter(S, D, Now);
                Bought(OfferName(o), got, done);
            });
        }

        // ô kế của Chuỗi Quà (miễn phí hoặc trả tiền)
        public static void ChainTake(int step, Action<bool> done = null)
        {
            var def = Shop.ChainNow(S, C);
            if (def == null || step >= def.steps.Count) return;
            var cs = def.steps[step];
            if (cs.price <= 0)
            {
                Free(Shop.ChainTake(S, D, step, false, Now, R), def.Name, done);
                return;
            }
            Pay(ShopConfig.Product(cs.price), "chain:" + def.id + ":" + step, cs.price, ok =>
            {
                if (!ok)
                {
                    done?.Invoke(false);
                    return;
                }
                Bought(def.Name, Shop.ChainTake(S, D, step, true, Now, R), done);
            });
        }

        public static string OfferName(ActiveOffer o)
        {
            if (o.pack != null && C.Pack(o.pack) is ShopPack p) return p.Name;
            return C.Offer(o.tpl)?.Name ?? Loc.T("Ưu đãi");
        }

        static void Bought(string title, List<Reward> got, Action<bool> done)
        {
            App.Save.Save();
            App.Audio.Play("chest");
            if (got == null)
            {
                done?.Invoke(false);
                return;
            }
            Show(Loc.F("Đã mua: {0}", title), got, () => done?.Invoke(true));
        }

        // quà miễn phí (ô chuỗi, quà ngày, thẻ, quỹ, mốc quảng cáo)
        public static void Free(List<Reward> got, string title, Action<bool> done = null)
        {
            if (got == null)
            {
                done?.Invoke(false);
                return;
            }
            App.Save.Save();
            ShopLog.Event("claim", title, 0);
            Show(title, got, () => done?.Invoke(true));
        }

        // hộp nhận quà: hộp mở rương có sẵn (rương vàng), lưới ô thưởng
        public static void Show(string title, List<Reward> got, Action closed = null)
        {
            if (got.Count == 0)
            {
                closed?.Invoke();
                return;
            }
            App.I.StartCoroutine(Run());

            IEnumerator Run()
            {
                yield return ChestBox.Show(title, SlotKind.ChestGold, null, got, Loc.T("Nhận"));
                // mảnh đủ mở khoá tướng (vé chọn tướng, gói mảnh): màn mở khoá sau hộp nhận
                HeroUnlockView.Play(HeroUnlockView.Unlocked(got), closed);
            }
        }

        // ---------- trứng, vé ----------

        // nở n quả bậc tier trong túi (màn nở trứng EggHatchView)
        public static void HatchEggs(int tier, int n, Action closed = null) => HatchMany(new List<(int, int)> { (tier, n) }, closed);

        static void HatchMany(List<(int tier, int n)> groups, Action closed)
        {
            var got = new List<Hatch>();
            foreach (var (tier, n) in groups.OrderBy(g => g.tier)) got.AddRange(Eggs.Open(S, D, tier, n, true, Now, R));
            Play(got, closed);
        }

        // Trứng Thường miễn phí hôm nay (quảng cáo free_egg), nở luôn không qua túi
        public static void FreeEgg(Action closed = null)
        {
            Ads.Show(Ads.FreeEgg, ok =>
            {
                if (!ok) return;
                Play(Eggs.Open(S, D, 0, 1, false, Now, R), closed);
            });
        }

        static void Play(List<Hatch> got, Action closed)
        {
            if (got.Count == 0)
            {
                closed?.Invoke();
                return;
            }
            App.Save.Save();
            ShopLog.Event("egg_hatch", string.Join(",", got.Select(h => h.from + ">" + h.tier)), 0);
            EggHatchView.Play(got, () =>
            {
                if (got.Any(h => h.tier >= (int)Rarity.Legend)) OfferHost.Raise(new OfferCtx { e = OfferEvent.LegendChest });
                closed?.Invoke();
            });
        }

        public static void UseTicket(bool week, int index, string hero, Action closed = null)
        {
            var r = Shop.UseTicket(S, D, week, index, hero, Now, R);
            if (r == null) return;
            Free(new List<Reward> { r }, Loc.T("Vé chọn tướng"), _ => closed?.Invoke());
        }

        // ---------- quảng cáo thưởng của cửa hàng ----------

        // bi miễn phí (tab Bi, popup Hết bi)
        public static void FreeBalls(Action closed = null)
        {
            Ads.Show(Ads.FreeBalls, ok =>
            {
                if (!ok) return;
                int n = Shop.RoundBalls(C.adBalls * C.Band(S.level));
                Free(Shop.Grant(S, D, new List<ShopItem> { new ShopItem { k = "balls", n = n } }, Now, R), Loc.T("Bi miễn phí"), _ => closed?.Invoke());
            });
        }

        public static int FreeBallsN => Shop.RoundBalls(C.adBalls * C.Band(S.level));

        // quà ngày; twice: xem quảng cáo để nhận ×2
        public static void Gift(bool twice, Action closed = null)
        {
            if (!twice)
            {
                Free(Shop.ClaimGift(S, D, false, Now, R), Loc.T("Quà hôm nay"), _ => closed?.Invoke());
                return;
            }
            Ads.Show(Ads.DailyGiftAd, ok =>
            {
                if (ok) Free(Shop.ClaimGift(S, D, true, Now, R), Loc.T("Quà hôm nay ×2"), _ => closed?.Invoke());
            });
        }

        // nhận hết quà miễn phí hôm nay (quà ngày, thẻ tuần / tháng, gói nhận theo ngày) trong một hộp
        public static void ClaimAll(Action closed = null)
        {
            var got = new List<Reward>();
            var now = Now;
            var rng = R;
            got.AddRange(Shop.ClaimGift(S, D, false, now, rng) ?? new List<Reward>());
            foreach (var id in new[] { "week", "month" }) got.AddRange(Shop.ClaimCard(S, D, id, now, rng) ?? new List<Reward>());
            if (S.shop != null)
                foreach (var id in S.shop.days.Keys.ToList())
                    got.AddRange(Shop.ClaimDay(S, D, id, now, rng) ?? new List<Reward>());
            Free(got, Loc.T("Quà hôm nay"), _ => closed?.Invoke());
        }
    }

    // nhật ký sự kiện cửa hàng (Logs/shop.csv, bản dev ghi file; bản phát hành chỉ giữ chỗ cho Firebase Analytics)
    public static class ShopLog
    {
        public static Action<string, string, double> Sink; // SDK đo gắn vào đây (S5)

        public static void Event(string evt, string what, double usd)
        {
            Sink?.Invoke(evt, what, usd);
#if UNITY_EDITOR || DEVELOPMENT_BUILD
            try
            {
                var dir = Path.Combine(Application.persistentDataPath, "Logs");
                Directory.CreateDirectory(dir);
                File.AppendAllText(Path.Combine(dir, "shop.csv"),
                    $"{DateTime.Now:yyyy-MM-dd HH:mm:ss},{evt},{what?.Replace(',', ';')},{usd:0.00}\n");
            }
            catch (Exception)
            {
                // nhật ký thử, lỗi ghi thì bỏ qua
            }
#endif
        }
    }
}
