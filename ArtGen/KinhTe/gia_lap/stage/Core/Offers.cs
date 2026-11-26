// Bộ máy ưu đãi (GD_Claude/26_CuaHang_IAP_QuangCao.md mục 7): nhận sự kiện (vào game, thua, thắng, hết bi, bi ít, jackpot, rương Huyền
// thoại), quét mốc (tướng mới, đảo mới, tướng sắp lên sao, cấp), dựng ưu đãi động theo nhu cầu, rồi trả danh sách popup đã qua trần:
// tối đa perOpen mỗi lần vào game, perDay mỗi ngày, ngày đầu firstDay, cách nhau gapMin phút, không bật trong 10 phút sau khi mua, mỗi
// gói bị đóng thì 24 giờ (3 lần: 72 giờ) mới tự bật lại, tích "Hôm nay không hiện nữa" thì thôi tới hôm sau. Không bán gì trước khi xong
// chuỗi hướng dẫn bắt buộc. Quà miễn phí (nhận quà ngày) không tính vào trần. Lớp app (OfferHost) hiện popup khi màn rảnh.
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    public enum OfferEvent { BattleLost, BattleWon, OutOfBalls, LowBalls, Jackpot, LegendChest }

    public sealed class OfferCtx
    {
        public OfferEvent e;
        public int stage;
        public bool boss; // thắng boss đảo
        public bool freeFix; // thua mà còn cách mạnh lên miễn phí làm ngay được
    }

    // một popup cần hiện. kind: claims (quà hôm nay), piggy (Lọ Bi đầy), offer (ưu đãi id = uid), chain (đợt Chuỗi Quà mới), intro (giới
    // thiệu gói id), refill (Hết bi), comeback (Quà Trở Lại, id = uid gói đi kèm)
    public sealed class Popup
    {
        public string kind, id, key;
        public bool free, first, warn;
        public override string ToString() => $"{kind}:{id}{(free ? " (free)" : "")}{(warn ? " (sắp hết)" : "")}";
    }

    public static class Offers
    {
        const double H = Shop.Hour, D = Shop.Day, M = 60000;
        // EXP trung bình mỗi bi thả ở máy bi, tính cả rương và mốc quà (đo bằng giả lập 300 người, GD_Claude/34 mục 1.1)
        public const double ExpPerBall = 9;

        static ShopConfig C(GameData d) => d.Cfg.shop;

        // ---------- trần ----------

        static void RollDay(OfferBook b, int day)
        {
            if (b.autoDay == day) return;
            b.autoDay = day;
            b.autoCount = 0;
        }

        // còn bao nhiêu popup bán tự bật được ngay lúc này (chưa tính perOpen)
        public static int Room(SaveData s, GameData d, double now)
        {
            var c = C(d).caps;
            var st = Shop.Of(s);
            var b = st.offers;
            int day = Shop.Today(now);
            RollDay(b, day);
            if (!Tutorial.CoreDone(s) || b.muteDay == day) return 0;
            if (now - b.lastBuy < c.afterBuyMin * M || now - b.lastAd < c.afterAdSec * 1000) return 0;
            if (b.autoCount > 0 && now - b.lastAuto < c.gapMin * M) return 0;
            int cap = day == Shop.Today(st.installAt) ? c.firstDay : c.perDay;
            return Math.Max(0, cap - b.autoCount);
        }

        // gói key bị đóng gần đây thì chưa tự bật lại
        public static bool Cooled(SaveData s, GameData d, string key, double now)
        {
            var b = Shop.Of(s).offers;
            if (!b.dismissAt.TryGetValue(key, out var at)) return true;
            int n = b.dismiss.TryGetValue(key, out var k) ? k : 0;
            var c = C(d).caps;
            return now - at >= (n >= 3 ? c.dismiss3H : c.dismissH) * H;
        }

        public static void Shown(SaveData s, GameData d, Popup p, double now)
        {
            var st = Shop.Of(s);
            var b = st.offers;
            if (!p.free)
            {
                RollDay(b, Shop.Today(now));
                b.autoCount++;
                b.lastAuto = now;
            }
            switch (p.kind)
            {
                case "offer":
                case "comeback":
                    var o = Shop.FindOffer(s, p.id);
                    if (o == null) break;
                    if (o.until <= 0)
                    {
                        var pack = o.pack != null ? C(d).Pack(o.pack) : null;
                        o.until = now + (pack?.hours ?? C(d).Offer(o.tpl)?.hours ?? 2) * H;
                    }
                    o.popped = true;
                    if (p.warn) o.warned = true;
                    break;
                case "piggy":
                    st.piggyFullShown = true;
                    break;
                case "refill":
                    b.lastRefill = now;
                    b.refillSeen = true;
                    break;
            }
        }

        // đóng popup: chưa mua thì ghi lần bị đóng của gói; mute = tích "Hôm nay không hiện nữa"
        public static void Closed(SaveData s, Popup p, bool bought, bool mute, double now)
        {
            var b = Shop.Of(s).offers;
            if (!bought && !p.free && p.key != null)
            {
                b.dismiss[p.key] = (b.dismiss.TryGetValue(p.key, out var n) ? n : 0) + 1;
                b.dismissAt[p.key] = now;
            }
            if (bought && p.key != null) b.dismiss.Remove(p.key);
            if (mute) b.muteDay = Shop.Today(now);
        }

        // ---------- lúc vào game ----------

        // có quà miễn phí chờ nhận hôm nay (quà ngày, thẻ tuần / tháng, gói nhận theo ngày)
        public static bool AnyClaim(SaveData s, GameData d, double now)
        {
            if (!Tutorial.CoreDone(s)) return false;
            if (Shop.GiftReady(s, now) || Shop.CardClaimable(s, "week", now) || Shop.CardClaimable(s, "month", now)) return true;
            return s.shop != null && s.shop.days.Keys.Any(id => Shop.DayClaimable(s, d, id, now));
        }

        // mỗi lần vào sảnh từ màn tải (mở game, quay lại sau reopenMin phút). Trả popup theo thứ tự, đã qua trần.
        public static List<Popup> Open(SaveData s, GameData d, double now, Rng rng)
        {
            var c = C(d);
            var st = Shop.Of(s);
            var b = st.offers;
            if (st.installAt <= 0) st.installAt = now;
            bool comeback = st.lastSeen > 0 && now - st.lastSeen >= c.caps.comebackDays * D;
            st.sessions++;
            st.lastSeen = now;
            Shop.Decay(s, c, now);
            Shop.Prune(s, now);
            var outL = new List<Popup>();
            if (!Tutorial.CoreDone(s)) return outL;

            int room = Math.Min(c.caps.perOpen, Room(s, d, now));
            int paid = 0;
            bool Take(Popup p)
            {
                if (p.free)
                {
                    outL.Add(p);
                    return true;
                }
                if (paid >= room || p.key != null && !Cooled(s, d, p.key, now)) return false;
                paid++;
                outL.Add(p);
                return true;
            }

            // 1. quà miễn phí hôm nay
            if (AnyClaim(s, d, now)) Take(new Popup { kind = "claims", free = true });
            // 2. Lọ Bi vừa đầy
            if (Shop.PiggyFull(s, c) && !st.piggyFullShown && Shop.PiggyCanBreak(s, c, now)) Take(new Popup { kind = "piggy", key = "piggy" });
            // 3. gói sắp hết giờ (đã từng popup, còn dưới 1 giờ)
            foreach (var o in Shop.Live(s, now).Where(o => o.until > 0 && o.until - now < H && o.popped && !o.warned).ToList())
                Take(new Popup { kind = "offer", id = o.uid, key = o.tpl + "_warn", warn = true });
            // 4. Quà Trở Lại
            if (comeback)
            {
                var o = Build(s, d, "comeback", null, now, rng);
                if (o != null) Take(new Popup { kind = "comeback", id = o.uid, key = "comeback", free = true });
            }
            // 5. gói người mới: Quà Nhập Môn hiện từ khi xong hướng dẫn, popup từ phiên 2 (đồng hồ chạy từ lần popup đầu); Gói Khởi Hành ngày 2
            EnsureStarter(s, d, now);
            var starter = b.active.Find(o => o.pack == "starter3" && !o.bought);
            if (starter != null && !starter.popped && st.sessions >= 2 && (starter.until <= 0 || starter.until > now))
                Take(new Popup { kind = "offer", id = starter.uid, key = "starter3" });
            if (!b.done.Contains("launch") && (Shop.Today(now) >= Shop.Today(st.installAt) + 1 || Shop.Bought(s, "starter3") > 0))
            {
                var o = Fixed(s, d, "launch", now);
                if (o != null && Take(new Popup { kind = "offer", id = o.uid, key = "launch" }))
                {
                    b.done.Add("launch");
                    // nạp đầu 3 bậc: các gói cùng nhóm mở cùng lúc, cùng đồng hồ (popup và bong bóng chỉ của gói đứng đầu)
                    foreach (var sib in c.packs.Where(q => q.group == "launch" && q.id != "launch").ToList()) Fixed(s, d, sib.id, now);
                }
            }
            // 6. Ưu Đãi Bất Ngờ (xác suất)
            if (paid < room && FlashOk(s, d, now))
            {
                var seg = Shop.SegmentOf(s, now);
                double p = seg >= Shop.Segment.Mid ? c.caps.flashChancePayer : c.caps.flashChance;
                if (rng.Chance(p))
                {
                    var o = Build(s, d, "flash", null, now, rng);
                    if (o != null)
                    {
                        Flashed(b, now);
                        Take(new Popup { kind = "offer", id = o.uid, key = "flash" });
                    }
                }
            }
            // 7. đợt Chuỗi Quà mới (từ ngày thứ 3, cách chainEveryDays ngày)
            if (c.chains.Count > 0 && !Shop.ChainLive(s, now) && now >= st.chainNext && Shop.Today(now) >= Shop.Today(st.installAt) + 2)
            {
                Shop.ChainStart(s, c, now);
                Take(new Popup { kind = "chain", key = "chain" });
            }
            // 8. giới thiệu thẻ tuần (cấp 10), Quỹ (cấp 15 hoặc ngày 3), mỗi thứ một lần
            if (s.level >= 10 && !b.done.Contains("intro_week") && !Shop.CardActive(s, "week", now) && Take(new Popup { kind = "intro", id = "week_card", key = "intro_week" }))
                b.done.Add("intro_week");
            if ((s.level >= 15 || Shop.Today(now) >= Shop.Today(st.installAt) + 3) && !b.done.Contains("intro_fund") && !st.fund &&
                Take(new Popup { kind = "intro", id = "fund", key = "intro_fund" }))
                b.done.Add("intro_fund");
            // 9. mốc: tướng vừa mở, đảo mới, tướng sắp lên sao
            foreach (var p in Scan(s, d, now, rng)) Take(p);
            return outL;
        }

        // Quà Nhập Môn vào danh sách ưu đãi (chưa chạy đồng hồ) ngay khi xong hướng dẫn
        public static void EnsureStarter(SaveData s, GameData d, double now)
        {
            var b = Shop.Of(s).offers;
            if (!Tutorial.CoreDone(s) || b.done.Contains("starter3") || C(d).Pack("starter3") == null) return;
            b.done.Add("starter3");
            b.active.Add(new ActiveOffer { uid = "starter3_" + (++b.seq), tpl = "starter3", pack = "starter3", price = C(d).Pack("starter3").price, created = now });
        }

        // gói cố định có hẹn giờ thành ưu đãi đang mở
        static ActiveOffer Fixed(SaveData s, GameData d, string packId, double now)
        {
            var p = C(d).Pack(packId);
            if (p == null) return null;
            var b = Shop.Of(s).offers;
            var o = new ActiveOffer { uid = packId + "_" + (++b.seq), tpl = packId, pack = packId, price = p.price, created = now, until = p.hours > 0 ? now + p.hours * H : 0 };
            b.active.Add(o);
            return o;
        }

        static List<Popup> Scan(SaveData s, GameData d, double now, Rng rng)
        {
            var c = C(d);
            var b = Shop.Of(s).offers;
            var outL = new List<Popup>();
            // tướng vừa mở khoá (so với lần quét trước; lần đầu chỉ ghi lại)
            var owned = s.heroes.Where(kv => kv.Value.owned).Select(kv => kv.Key).ToList();
            if (b.seenOwned != null)
            {
                var fresh = owned.Where(h => !b.seenOwned.Contains(h) && h != s.starter).ToList();
                if (fresh.Count > 0)
                {
                    var o = Build(s, d, "companion", fresh.Last(), now, rng);
                    if (o != null) outL.Add(new Popup { kind = "offer", id = o.uid, key = "companion" });
                }
            }
            b.seenOwned = owned;
            // đảo mới (đảo có tiến trình lần đầu)
            int zonesOn = s.zones.Count(z => z > 0);
            if (b.seenZones >= 0 && zonesOn > b.seenZones)
            {
                int zi = Array.FindLastIndex(s.zones, z => z > 0);
                var zoneElem = (Elem)Math.Max(0, zi);
                var counter = Elements.All.FirstOrDefault(x => Elements.Beats(x) == zoneElem);
                var o = Build(s, d, "newisle", "e:" + Keys.Of(counter), now, rng);
                if (o != null) outL.Add(new Popup { kind = "offer", id = o.uid, key = "newisle" });
            }
            b.seenZones = zonesOn;
            // tướng trong đội sắp lên sao: mỗi ngày tối đa một lần
            int day = Shop.Today(now);
            if (b.nearDay != day && Shop.Near(s, d, c.caps.nearStarPct) is string near)
            {
                b.nearDay = day;
                var o = Build(s, d, "nearstar", near, now, rng);
                if (o != null) outL.Add(new Popup { kind = "offer", id = o.uid, key = "nearstar" });
            }
            return outL;
        }

        // ---------- sự kiện ----------

        static bool FlashOk(SaveData s, GameData d, double now)
        {
            var c = C(d).caps;
            var b = Shop.Of(s).offers;
            int day = Shop.Today(now);
            if (b.flashDay == day && b.flashCount >= c.flashPerDay) return false;
            if (b.lastFlash > 0 && now - b.lastFlash < c.flashGapH * H) return false;
            return !Shop.Live(s, now).Any(o => o.tpl == "flash" || o.tpl == "hot");
        }

        static void Flashed(OfferBook b, double now)
        {
            int day = Shop.Today(now);
            if (b.flashDay != day)
            {
                b.flashDay = day;
                b.flashCount = 0;
            }
            b.flashCount++;
            b.lastFlash = now;
        }

        public static List<Popup> On(SaveData s, GameData d, OfferCtx x, double now, Rng rng)
        {
            var c = C(d);
            var st = Shop.Of(s);
            var b = st.offers;
            var outL = new List<Popup>();
            switch (x.e)
            {
                case OfferEvent.BattleLost:
                {
                    if (x.stage == b.lossStage) b.lossStreak++;
                    else
                    {
                        b.lossStage = x.stage;
                        b.lossStreak = 1;
                    }
                    if (b.lossStreak >= c.caps.reliefLosses && !x.freeFix && Shop.SegmentOf(s, now) != Shop.Segment.New &&
                        now - b.lastRelief >= c.caps.reliefGapH * H && Room(s, d, now) > 0 && Cooled(s, d, "relief", now))
                    {
                        var o = Build(s, d, "relief", null, now, rng);
                        if (o != null)
                        {
                            b.lastRelief = now;
                            outL.Add(new Popup { kind = "offer", id = o.uid, key = "relief" });
                        }
                    }
                    break;
                }
                case OfferEvent.BattleWon:
                    if (x.stage == b.lossStage) b.lossStreak = 0;
                    if (x.boss) Hot(s, d, now, rng, outL);
                    Jump(s, d, x.stage, now, rng, outL);
                    break;
                case OfferEvent.Jackpot:
                case OfferEvent.LegendChest:
                    Hot(s, d, now, rng, outL);
                    break;
                case OfferEvent.OutOfBalls:
                    if (now - b.lastRefill >= c.caps.refillGapMin * M) outL.Add(new Popup { kind = "refill", free = true, first = !b.refillSeen, key = "refill" });
                    break;
                case OfferEvent.LowBalls:
                    if (Tutorial.CoreDone(s) && FlashOk(s, d, now) && Room(s, d, now) > 0 && Cooled(s, d, "flash", now) && rng.Chance(c.caps.lowChance))
                    {
                        var o = Build(s, d, "flash", null, now, rng);
                        if (o != null)
                        {
                            o.until = now + 3 * H; // vào máy bi lúc bi còn ít: 3 giờ
                            Flashed(b, now);
                            outL.Add(new Popup { kind = "offer", id = o.uid, key = "flash" });
                        }
                    }
                    break;
            }
            return outL;
        }

        static void Hot(SaveData s, GameData d, double now, Rng rng, List<Popup> outL)
        {
            var c = C(d);
            if (!Tutorial.CoreDone(s) || !FlashOk(s, d, now) || Room(s, d, now) <= 0 || !Cooled(s, d, "hot", now) || !rng.Chance(c.caps.hotChance)) return;
            var o = Build(s, d, "hot", null, now, rng);
            if (o == null) return;
            Flashed(Shop.Of(s).offers, now);
            outL.Add(new Popup { kind = "offer", id = o.uid, key = "hot" });
        }

        // còn cách mạnh lên miễn phí làm ngay được không (lên sao, nâng thẻ, thả bi lên cấp): chuỗi gợi ý trước khi bán (mục 7.3)
        // team: đội vừa đánh (null = đội trong bản lưu)
        public static string FreeFix(SaveData s, GameData d, IEnumerable<string> team = null)
        {
            foreach (var h in team ?? s.team)
            {
                if (s.Hero(h) == null || !s.Hero(h).owned) continue;
                if (Progress.CanStarUp(s, d, h) || Progress.CanEvolve(s, d, h)) return Loc.F("Lên sao {0}", d.Hero(h).name);
                foreach (var slot in Progress.Slots)
                    if (Progress.CanUpCard(s, d.Cfg, h, slot)) return Loc.F("Nâng thẻ của {0}", d.Hero(h).name);
            }
            // "thả bi" chỉ là cách miễn phí khi số bi đang có đủ lên ít nhất một cấp. Trước 2026-11-26 cứ có 20 bi là tính, mà sau trận
            // nào cũng có hơn 20 bi, nên Gói Tiếp Sức không bao giờ bật (giả lập: 0 lần trên 300 người, GD_Claude/33 mục 2.6)
            if (s.level < d.Cfg.maxLevel && s.balls * ExpPerBall >= Progress.ExpToNext(s.level, d.Cfg) - s.exp)
                return Loc.T("Thả bi ở Máy bi để lên cấp");
            return null;
        }

        // ---------- Gói Vượt Mốc (GD_Claude/34 mục 2) ----------

        // các ải "mốc" của một đảo theo thứ tự: ải tướng, mini boss, boss (10 mốc mỗi đảo); tướng mốc k là tướng chủ lực của ải thứ k
        public static List<StageDef> MilestoneStages(GameData d, Elem zone) =>
            d.ZoneStages(zone).Where(st => st.tag == StageTag.Hero || st.kind != StageKind.Normal).OrderBy(st => st.idx).ToList();

        // vừa qua ải st: tướng để chào trong Gói Vượt Mốc (đi trước jumpAhead mốc, chưa có thì mới chào; hết mốc thì lấy mốc cuối).
        // null: ải không phải mốc, mốc còn thấp hơn jumpFrom, hoặc các tướng mốc trên đều đã có
        public static string JumpHero(SaveData s, GameData d, StageDef st)
        {
            if (st == null) return null;
            var k = C(d).caps;
            var ms = MilestoneStages(d, st.zone);
            int at = ms.FindIndex(m => m.id == st.id) + 1;
            if (at < Math.Max(1, k.jumpFrom) || at >= ms.Count) return null;
            for (int t = Math.Min(ms.Count, at + Math.Max(1, k.jumpAhead)); t <= ms.Count; t++)
            {
                string h = Teams.StageLead(ms[t - 1], d)?.hero;
                if (h == null || d.Hero(h) == null || d.Hero(h).minion) continue;
                var hp = s.Hero(h);
                if (hp == null || !hp.owned) return h;
            }
            return null;
        }

        // lần ĐẦU qua một ải mốc: dựng Gói Vượt Mốc cho tướng đi trước (mỗi lúc một gói đang mở)
        static void Jump(SaveData s, GameData d, int stageId, double now, Rng rng, List<Popup> outL)
        {
            var c = C(d);
            if (c.Offer("jump") == null || !Tutorial.CoreDone(s)) return;
            if (!s.clears.TryGetValue(stageId, out var n) || n != 1) return;
            string hero = JumpHero(s, d, d.Stage(stageId));
            if (hero == null) return;
            if (Shop.Of(s).offers.active.Any(o => o.tpl == "jump" && !o.bought && (o.until <= 0 || o.until > now))) return;
            var of = Build(s, d, "jump", hero, now, rng);
            if (of != null) outL.Add(new Popup { kind = "offer", id = of.uid, key = "jump" });
        }

        // ---------- thiếu cấp so với ải (GD_Claude/34 mục 1.5) ----------

        public struct LevelGap
        {
            public int foe, gap; // cấp địch mạnh nhất của ải; số cấp người chơi còn thiếu so với nó (0: không thiếu)
            public int balls; // số bi cần thả để lên đủ số cấp đó (ước lượng ExpPerBall EXP mỗi bi, làm tròn lên hai chữ số đầu)
        }

        // màn thua ghi "địch cấp X, bạn cấp Y: thả khoảng N bi để lên Z cấp"; Gói Tiếp Sức dựa vào đây để nghiêng về bi
        public static LevelGap GapTo(SaveData s, GameData d, StageDef st)
        {
            var g = new LevelGap();
            if (st == null) return g;
            foreach (var e in st.enemies) g.foe = Math.Max(g.foe, e.level);
            int to = Math.Min(g.foe, d.Cfg.maxLevel);
            g.gap = Math.Max(0, to - s.level);
            if (g.gap <= 0) return g;
            double exp = -s.exp;
            for (int lv = s.level; lv < to; lv++) exp += Progress.ExpToNext(lv, d.Cfg);
            double n = Math.Max(1, exp / ExpPerBall);
            double unit = Math.Pow(10, Math.Max(0, Math.Floor(Math.Log10(n)) - 1));
            g.balls = (int)(Math.Ceiling(n / unit) * unit);
            return g;
        }

        // ---------- dựng nội dung ưu đãi ----------

        // ưu đãi động theo mẫu tplId; ctx: id tướng (companion, nearstar) hoặc "e:<hệ>" (newisle). null nếu không dựng được.
        public static ActiveOffer Build(SaveData s, GameData d, string tplId, string ctx, double now, Rng rng)
        {
            var c = C(d);
            var t = c.Offer(tplId);
            if (t == null) return null;
            var st = Shop.Of(s);
            bool ladder = t.price <= 0;
            double price = ladder ? Shop.LadderPrice(s, c, now) : t.price;
            double v = t.value * price * c.valuePerUsd;
            var items = new List<ShopItem>();
            string hero = null;

            void Add(ShopItem it)
            {
                items.Add(it);
                v -= Shop.Value(c, d, it);
            }

            void Shards(string h, double share)
            {
                if (h == null || d.Hero(h) == null) return;
                var g = Progress.ShardGoal(s, d, h);
                double sv = Shop.ShardValue(c, d.Hero(h).rarity);
                int n = (int)Math.Floor(v * share / Math.Max(1, sv));
                if (g.need > 0) n = Math.Min(n, Math.Max(1, g.need - g.have));
                if (n > 0) Add(new ShopItem { k = "shards", h = h, n = n });
            }

            switch (tplId)
            {
                case "flash":
                    hero = Shop.Near(s, d, 0.5);
                    Shards(hero, 0.6);
                    if (v > c.Value(Eggs.Key(3)) * 1.2) Add(new ShopItem { k = Shop.Egg, r = 3, n = 1 });
                    break;
                case "hot":
                    // Ưu Đãi Nóng: trứng bậc cao nhất vừa túi giá trị (Sử thi → Huyền thoại khi giá trị dư dả)
                    Add(new ShopItem { k = Shop.Egg, r = v >= c.Value(Eggs.Key(4)) * 1.5 ? 4 : v >= c.Value(Eggs.Key(3)) * 1.5 ? 3 : 2, n = 1 });
                    break;
                case "relief":
                    hero = Shop.Carry(s, d);
                    // đang thiếu cấp so với ải vừa thua: gói chủ yếu là bi (bi → cấp → vượt ải, GD_Claude/34 mục 1.5);
                    // không thiếu cấp: mảnh và bản sao thẻ của tướng chủ lực như trước
                    bool lowLv = GapTo(s, d, d.Stage(st.offers.lossStage)).gap > 0;
                    Shards(hero, lowLv ? 0.2 : 0.5);
                    if (!lowLv && s.Hero(hero)?.owned == true) Add(new ShopItem { k = "copies", h = hero, n = 2 });
                    break;
                case "companion":
                    hero = ctx;
                    Shards(hero, 0.6);
                    Add(new ShopItem { k = Shop.Egg, r = 2, n = 1 });
                    break;
                case "nearstar":
                    hero = ctx ?? Shop.Near(s, d, c.caps.nearStarPct);
                    if (hero == null) return null;
                    Shards(hero, 1);
                    Add(new ShopItem { k = "evo", n = 1 });
                    break;
                case "jump":
                {
                    // tướng trọn bộ: mảnh mở khoá + mảnh lên sao tới mức cấp người chơi cho phép (không quá jumpMaxStar), bản sao thẻ,
                    // đá tiến hóa của các bậc trên đường. Giá: bậc thấp nhất của caps.jumpPrices mà gói đạt × t.value
                    hero = ctx;
                    var hd = hero != null ? d.Hero(hero) : null;
                    if (hd == null) return null;
                    var hp = s.Hero(hero);
                    bool own = hp != null && hp.owned;
                    var path = Progress.PathCost(d.Cfg, hd, own ? hp.star : 1, s.level, c.caps.jumpMaxStar);
                    int sh = Math.Max(0, path.shards + (own ? 0 : hd.shards) - (hp?.shards ?? 0));
                    var core = new List<ShopItem>();
                    if (sh > 0) core.Add(new ShopItem { k = "shards", h = hero, n = sh });
                    core.Add(new ShopItem { k = "copies", h = hero, n = Math.Max(1, c.caps.jumpCopies) * (1 + StarTier.Tier(path.to)) });
                    if (path.stones > 0) core.Add(new ShopItem { k = "evo", n = path.stones });
                    double cv = Shop.Value(c, d, core);
                    price = 0;
                    foreach (double step in c.caps.jumpPrices)
                        if (price <= 0 && step * c.valuePerUsd * t.value >= cv * 0.9) price = step; // sát bậc dưới (lệch dưới 10%) thì lấy bậc dưới
                    if (price <= 0) price = c.caps.jumpPrices[c.caps.jumpPrices.Length - 1];
                    ladder = false;
                    v = Math.Max(cv, t.value * price * c.valuePerUsd);
                    foreach (var it in core) Add(it);
                    break;
                }
                case "newisle":
                    Add(new ShopItem { k = Shop.Ticket, n = 1, r = (int)Rarity.Epic, h = ctx });
                    break;
                case "comeback":
                    foreach (var it in Shop.Resolve(s, d, t.items, true, null)) Add(it);
                    break;
                default:
                    foreach (var it in Shop.Resolve(s, d, t.items, true, ctx)) Add(it);
                    break;
            }
            // phần còn lại là bi (nhân bậc cấp: luôn bằng chừng ấy giờ bi thụ động)
            if (tplId != "comeback" && v > 5)
            {
                int balls = Shop.RoundBalls(v / Math.Max(0.0001, c.Value("balls")) * c.Band(s.level));
                if (balls > 0) items.Add(new ShopItem { k = "balls", n = balls });
            }
            if (items.Count == 0) return null;
            var o = new ActiveOffer
            {
                uid = tplId + "_" + (++st.offers.seq), tpl = tplId, price = price, items = items, created = now, until = now + t.hours * H, ladder = ladder, hero = hero,
            };
            st.offers.active.Add(o);
            return o;
        }
    }
}
