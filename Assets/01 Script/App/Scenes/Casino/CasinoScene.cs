// Màn đảo Casino "Bến Lữ Khách" (GD_Claude/29_DaoCasino.md, mốc C2): bản đồ đảo kéo được (nền tạm là concept đã gen), các điểm chạm
// cố định (CasinoSpot) phủ lên công trình: Tháp Máy Bi ở giữa, Bến câu, Trường đua, Chợ đen, Hầm đấu, Quán trọ, 3 bãi lều sự kiện
// (Đêm Bài, Vòng Xoay, Máy Quả), bảng lịch lữ khách ở bến. Hàng nút đáy: Bói sao, Lịch lữ khách, Về sảnh.
// - Tháp Máy Bi: vào màn máy bi, quay lại thì về đảo (MachineScene nhận args SceneIds.Casino).
// - Trò chưa mở: báo điều kiện (Casino.Need). Lần đầu ra đảo: truyện mở đảo; trò mới mở: thông báo một lần (CasinoState.seen).
// - Lều may rủi chỉ hiện khi sự kiện đang mở (Casino.Booth); bãi trống báo đoàn kế tiếp ghé sau mấy ngày.
// Từng trò mở màn riêng qua CasinoGames.Open (mốc C3–C7).
using System;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class CasinoScene : SceneRoot
    {
        public override string Title => Loc.T("Bến Lữ Khách");
        public override string BackTo => SceneIds.Hub;
        // thanh sảnh chung + hàng nút / cột của sảnh (LobbyDock, người dùng 2026-11-27): không tên, không nút quay lại; về sảnh bằng ô
        // "Đảo chính" (nút giữa của kệ chung), con tàu ở bến hoặc phím Back
        public override TopBar Bar => TopBar.Hud;

        // thứ tự điểm trong prefab (CasinoSpot.Id)
        public static readonly string[] Ids =
            { "tower", "fishing", "race", "market", "underground", "inn", "booth_blackjack", "booth_roulette", "booth_slot", "board" };

        [SerializeField] CasinoSpot[] spots;
        [SerializeField] SketchButton lucky, board, home;
        [SerializeField] TextMeshProUGUI info;
        [Tooltip("Cọc bãi trống và lều sự kiện vẽ trên đảo, theo thứ tự Booths (C8: ảnh công trình rời)")]
        [SerializeField] Image[] pads, tents;
        [Tooltip("Tàu đậu ở bến nam (chuyến tàu qua mây sảnh ↔ đảo cập / rời ở đây; chạm tàu là về sảnh)")]
        [SerializeField] PierShip pier;
        [SerializeField] HubPan pan;
        [Tooltip("Giao diện cố định (dòng tin, hàng nút): chuyến tàu ẩn đi trước khi chụp màn làm nền trôi")]
        [SerializeField] CanvasGroup chrome;
        [Tooltip("Nhún công trình định kỳ và khi chạm (người dùng 2026-11-25: cho biết công trình bấm được)")]
        [SerializeField] CasinoBob bob;
        Coroutine chromeFade;

        public static readonly string[] Booths = { Casino.Blackjack, Casino.Roulette, Casino.Slot };

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Dùng khi dựng prefab (Editor).
        public void Setup(CasinoSpot[] spotList, SketchButton luckyBtn, SketchButton boardBtn, SketchButton homeBtn, TextMeshProUGUI infoText)
        {
            spots = spotList;
            lucky = luckyBtn;
            board = boardBtn;
            home = homeBtn;
            info = infoText;
        }

        // Dùng khi dựng prefab (Editor).
        public void SetupBooths(Image[] padImgs, Image[] tentImgs)
        {
            pads = padImgs;
            tents = tentImgs;
        }

        // Dùng khi dựng prefab (Editor).
        public void SetupPier(PierShip ship, HubPan mapPan, CanvasGroup ui)
        {
            pier = ship;
            pan = mapPan;
            chrome = ui;
        }

        // Dùng khi dựng prefab (Editor).
        public void SetupBob(CasinoBob b) => bob = b;

        // ảnh công trình dưới mỗi điểm chạm (bãi lều: lều nếu đang dựng, không thì cọc)
        string ArtOf(string spotId)
        {
            switch (spotId)
            {
                case "tower": return "thap";
                case "fishing": return "ben_cau";
                case "race": return "dua";
                case "market": return "cho";
                case "underground": return "hang";
                case "inn": return "quan_tro";
                case "board": return "ben_tau";
            }
            string booth = BoothOf(spotId);
            int i = booth == null ? -1 : System.Array.IndexOf(Booths, booth);
            if (i < 0) return null;
            bool tent = tents != null && i < tents.Length && tents[i] && tents[i].gameObject.activeSelf;
            var img = tent ? tents[i] : pads != null && i < pads.Length ? pads[i] : null;
            return img ? img.GetComponent<CasinoBuilding>()?.Id : null;
        }

        void HookBob()
        {
            if (!bob) return;
            bob.Allowed = () => (!chrome || chrome.alpha > 0.99f) && App.Modals.Count == 0 && !App.Router.Busy;
            foreach (var sp in spots)
            {
                if (!sp) continue;
                var id = sp.Id;
                sp.OnTapFx = () => bob.Bounce(ArtOf(id), 1.6f);
            }
        }

        // bến tàu: camera cho chuyến tàu qua mây (đặt ngay / lướt tới tàu), chạm tàu là về sảnh
        void HookPier()
        {
            if (!pier) return;
            pier.Frame = (p, w) =>
            {
                if (pan) pan.FrameAt(p, w);
            };
            pier.Glide = GlideTo;
            pier.OnTap = () => App.Router.Go(SceneIds.Hub);
        }

        System.Collections.IEnumerator GlideTo(RectTransform p)
        {
            if (!pan) yield break;
            pan.GlideTo(p);
            float t0 = Time.unscaledTime;
            while (pan.Gliding && Time.unscaledTime - t0 < 1f) yield return null;
        }

        // chuyến tàu qua mây ẩn giao diện cố định trước khi chụp màn (thế giới liền, giao diện không trôi theo), hiện lại khi tàu cập bến
        public override void Chrome(bool on, bool fade)
        {
            if (!chrome) return;
            if (chromeFade != null) StopCoroutine(chromeFade);
            chromeFade = null;
            chrome.blocksRaycasts = on;
            if (fade && isActiveAndEnabled) chromeFade = StartCoroutine(FadeChrome(on ? 1 : 0));
            else chrome.alpha = on ? 1 : 0;
        }

        System.Collections.IEnumerator FadeChrome(float to)
        {
            float from = chrome.alpha;
            for (float t = 0; t < 0.25f; t += Time.unscaledDeltaTime)
            {
                chrome.alpha = Mathf.Lerp(from, to, t / 0.25f);
                yield return null;
            }
            chrome.alpha = to;
            chromeFade = null;
        }

        // lều dựng khi sự kiện của lều đang mở (và mục lều đã mở theo cấp), không thì cọc bãi trống
        void ShowBooth(string booth, bool tent)
        {
            int i = System.Array.IndexOf(Booths, booth);
            if (i < 0) return;
            if (tents != null && i < tents.Length && tents[i]) tents[i].gameObject.SetActive(tent);
            if (pads != null && i < pads.Length && pads[i]) pads[i].gameObject.SetActive(!tent);
        }

        public override void Enter(object args)
        {
            HookPier();
            HookBob();
            Chrome(true, false);
            RaiseBar();
            // hộp các trò mở trên đảo (trò có scene riêng đi qua CasinoGames.SceneOf)
            CasinoGames.Register(Casino.Inn, close =>
            {
                App.Modals.Open<InnDialog>(close).Show(GoTask);
                return true;
            });
            Render();
            StartCoroutine(AfterArrive());
        }

        // dòng tin + hàng nút của đảo nằm trên kệ nút sảnh chung (LobbyDock sát đáy, nút Máy Bi giữa nhô cao): đẩy lên trên đỉnh nút giữa
        void RaiseBar()
        {
            if (!LobbyDock.I || !lucky) return;
            var row = lucky.transform.parent as RectTransform;
            var bar = row ? row.parent as RectTransform : null;
            if (bar) bar.anchoredPosition = new Vector2(bar.anchoredPosition.x, LobbyDock.CenterTop + 8);
        }

        // truyện mở đảo, thông báo trò mới: chờ chuyển cảnh xong (tàu cập bến, giao diện hiện lại) rồi mới hiện
        System.Collections.IEnumerator AfterArrive()
        {
            float t0 = Time.unscaledTime;
            while ((App.Router.Busy || (chrome && chrome.alpha < 0.99f)) && Time.unscaledTime - t0 < 20) yield return null;
            if (!Casino.Of(S).intro) Intro();
            else Announce();
        }

        public override void Refresh() => Render();

        // ---------- tên trò ----------

        public static string NameOf(string id)
        {
            switch (id)
            {
                case Casino.Fishing: return Loc.T("Bến câu");
                case Casino.Race: return Loc.T("Trường đua");
                case Casino.Market: return Loc.T("Chợ đen");
                case Casino.Underground: return Loc.T("Hầm đấu");
                case Casino.Inn: return Loc.T("Quán trọ");
                case Casino.Booths: return Loc.T("Lều lữ khách");
                default: return id;
            }
        }

        static string BoothOf(string spotId) => spotId.StartsWith("booth_") ? spotId.Substring(6) : null;

        // ---------- lần đầu, trò mới ----------

        void Intro()
        {
            // Lão Mực đón ở bến (D6); Gợi ý tắt thì hộp chữ như trước
            var st = Casino.Of(S);
            if (CasinoGuide.Port(Announce))
            {
                st.intro = true;
                App.Save.Save();
                return;
            }
            App.Modals.Alert(Loc.T("Bến Lữ Khách"),
                Loc.T("Giữa năm đảo hệ có một bến nghỉ chân. Thám hiểm gia nào đi qua cũng ghé lại: sửa thuyền, đổi đồ, kể chuyện và thử vận ở Tháp Máy Bi giữa đảo.") + "\n\n" +
                Loc.T("Quanh tháp có bến câu, trường đua, chợ đen, hầm đấu và quán trọ, mở dần theo cấp. Thỉnh thoảng có đoàn lữ khách ghé bến dựng lều chơi vài ngày rồi đi."),
                Loc.T("Vào bến"), () =>
                {
                    Casino.Of(S).intro = true;
                    App.Save.Save();
                    Announce();
                });
        }

        void Announce()
        {
            var fresh = Casino.NewlyOpen(S, D);
            foreach (var id in fresh)
            {
                App.Toasts.Show(Loc.F("Mới mở: {0}", NameOf(id)), Icon("star"));
                Casino.MarkSeen(S, "open:" + id);
            }
            if (fresh.Count > 0)
            {
                App.Save.Save();
                Render();
            }
        }

        // ---------- vẽ ----------

        void Render()
        {
            if (spots == null) return;
            var s = S;
            var d = D;
            double now = Now;
            var st = Casino.Roll(s, d, now);
            foreach (var sp in spots)
            {
                if (!sp) continue;
                string id = sp.Id;
                Guide.Mark(CasinoGuide.SpotKey(id), sp); // chỗ Lão Mực khoanh khi đón ở bến
                switch (id)
                {
                    case "tower":
                        sp.Bind(Loc.T("Tháp Máy Bi"), Loc.F("{0} bi", NumFmt.Short(s.balls)), false, false,
                            () => App.Router.Go(SceneIds.Machine, SceneIds.Casino));
                        break;
                    case "fishing":
                    {
                        bool open = Casino.Unlocked(s, d, Casino.Fishing);
                        sp.Bind(NameOf(id), open ? Loc.F("{0} mồi", Fishing.BaitLeft(s, d, now)) : Casino.Need(s, d, Casino.Fishing), !open,
                            open && Fishing.FreeLeft(s, d, now) > 0, () => Open(Casino.Fishing));
                        break;
                    }
                    case "race":
                    {
                        bool open = Casino.Unlocked(s, d, Casino.Race);
                        double mult = Casino.RaceMult(d, now);
                        string sub = !open ? Casino.Need(s, d, Casino.Race)
                            : mult > 1 ? Loc.F("Lễ Hội Đua ×{0}", mult.ToString("0.#"))
                            : Loc.F("{0} lượt có thưởng", Casino.PlaysLeft(s, d, Casino.Race, now));
                        sp.Bind(NameOf(id), sub, !open, open && mult > 1, () => Open(Casino.Race));
                        break;
                    }
                    case "market":
                    {
                        bool open = Casino.Unlocked(s, d, Casino.Market);
                        sp.Bind(NameOf(id), open ? Loc.F("Đổi hàng sau {0}", ShopUi.Clock(BlackMarket.NextRefresh(d, now))) : Casino.Need(s, d, Casino.Market),
                            !open, false, () => Open(Casino.Market));
                        break;
                    }
                    case "underground":
                    {
                        bool open = Casino.Unlocked(s, d, Casino.Underground);
                        var tiers = Underground.TiersToday(d, now);
                        int won = tiers.Count(t => Underground.TierOpen(s, d, t) && Underground.WonToday(s, d, t, now));
                        int can = tiers.Count(t => Underground.TierOpen(s, d, t));
                        int left = open ? Underground.FightsLeft(s, d, now) : 0;
                        sp.Bind(NameOf(id), open ? Loc.F("Còn {0} lượt đánh hôm nay", left) : Casino.Need(s, d, Casino.Underground),
                            !open, open && won < can && left > 0, () => Open(Casino.Underground));
                        break;
                    }
                    case "inn":
                    {
                        bool open = Casino.Unlocked(s, d, Casino.Inn);
                        var qs = open ? Casino.InnToday(s, d, now) : null;
                        int done = qs?.Count(q => st.innClaimed.Contains(q.id)) ?? 0;
                        bool ready = open && (qs.Any(q => Casino.QuestDone(s, q) && !st.innClaimed.Contains(q.id)) || Casino.InnAllReady(s, d, now));
                        sp.Bind(NameOf(id), open ? Loc.F("Nhiệm vụ {0}/{1}", done, qs.Count) : Casino.Need(s, d, Casino.Inn), !open, ready,
                            () => Open(Casino.Inn));
                        break;
                    }
                    case "board":
                    {
                        var act = Casino.Active(d, now);
                        sp.Bind(Loc.T("Lịch lữ khách"), act.Count > 0 ? act[0].ev.Name : Loc.T("Chưa có đoàn nào"), false,
                            Casino.Unlocked(s, d, Casino.Booths) && act.Any(a => !st.seen.Contains("ev:" + a.Key)), Board);
                        break;
                    }
                    default:
                    {
                        string booth = BoothOf(id);
                        if (booth == null) break;
                        bool open = Casino.Unlocked(s, d, Casino.Booths);
                        bool allowed = Casino.TablesAllowed(d); // vùng tắt lều may rủi: bãi luôn trống, không báo đoàn ghé
                        var span = allowed ? Casino.Booth(d, booth, now) : null;
                        ShowBooth(booth, open && span != null);
                        if (!open)
                            sp.Bind(Loc.T("Bãi lều"), Casino.Need(s, d, Casino.Booths), true, false, () => Open(Casino.Booths));
                        else if (span != null)
                            sp.Bind(span.ev.Name, Loc.F("Còn {0}", ShopUi.Clock(Casino.Left(span, now))), false, !st.seen.Contains("ev:" + span.Key),
                                () => OpenBooth(booth, span));
                        else
                        {
                            var next = !allowed ? null : d.Cfg.casino.events.Where(e => e.booth == booth).Select(e => Casino.NextSpan(d, e, Casino.Today(now)))
                                .Where(x => x != null).OrderBy(x => x.startDay).FirstOrDefault();
                            string sub = next != null ? Loc.F("{0} ghé sau {1} ngày", next.ev.Name, next.startDay - Casino.Today(now)) : "";
                            sp.Bind(Loc.T("Bãi lều trống"), sub, false, false, () => App.Toasts.Show(sub, Icon("flag")));
                        }
                        break;
                    }
                }
            }
            if (bob) bob.SetCandidates(BobCandidates(s, d, now, st));
            var lk = Casino.LuckyActive(s, now);
            if (info)
                info.text = lk is Elem e
                    ? Loc.F("Hệ may mắn hôm nay: {0}. Cá hệ này cắn câu nhiều gấp đôi, tướng hệ này chạy nhanh hơn.", Elements.Name(e))
                    : Loc.T("Lật Bói sao để biết hệ may mắn hôm nay.");
            if (lucky)
            {
                lucky.SetText(lk is Elem le ? Elements.Name(le) : Loc.T("Bói sao"));
                lucky.SetRole(lk == null ? BtnColor.Yellow : BtnColor.Paper);
                lucky.SetOnClick(Lucky);
            }
            if (board)
            {
                board.SetText(Loc.T("Lịch lữ khách"));
                board.SetOnClick(Board);
            }
            if (home)
            {
                // có kệ chung thì nút Về sảnh thừa (nút giữa "Đảo chính")
                home.gameObject.SetActive(!LobbyDock.I);
                home.SetText(Loc.T("Về sảnh"));
                home.SetOnClick(() => App.Router.Go(SceneIds.Hub));
            }
        }

        // công trình nhún định kỳ: chỗ đang mở; chỗ có việc (chấm đỏ) trọng số cao; chỗ khoá, bãi lều trống không nhún
        System.Collections.Generic.IEnumerable<(string, float)> BobCandidates(SaveData s, GameData d, double now, CasinoState st)
        {
            yield return ("thap", 1f);
            yield return ("ben_tau", 0.5f);
            if (Casino.Unlocked(s, d, Casino.Fishing)) yield return ("ben_cau", Fishing.FreeLeft(s, d, now) > 0 ? 3f : 1f);
            if (Casino.Unlocked(s, d, Casino.Race)) yield return ("dua", Casino.RaceMult(d, now) > 1 ? 2.5f : 1f);
            if (Casino.Unlocked(s, d, Casino.Market)) yield return ("cho", 1f);
            if (Casino.Unlocked(s, d, Casino.Underground))
            {
                var tiers = Underground.TiersToday(d, now);
                bool todo = Underground.FightsLeft(s, d, now) > 0 && tiers.Any(t => Underground.TierOpen(s, d, t) && !Underground.WonToday(s, d, t, now));
                yield return ("hang", todo ? 2f : 1f);
            }
            if (Casino.Unlocked(s, d, Casino.Inn))
            {
                var qs = Casino.InnToday(s, d, now);
                bool ready = qs.Any(q => Casino.QuestDone(s, q) && !st.innClaimed.Contains(q.id)) || Casino.InnAllReady(s, d, now);
                yield return ("quan_tro", ready ? 3f : 1f);
            }
            if (Casino.Unlocked(s, d, Casino.Booths) && Casino.TablesAllowed(d))
                foreach (var booth in Booths)
                {
                    var span = Casino.Booth(d, booth, now);
                    if (span != null) yield return ("leu_" + booth, st.seen.Contains("ev:" + span.Key) ? 1.5f : 3f);
                }
        }

        // ---------- thao tác ----------

        void Open(string game)
        {
            if (!Casino.Unlocked(S, D, game))
            {
                App.Toasts.Show(Casino.Need(S, D, game), Icon("lock"));
                return;
            }
            if (!CasinoGames.Open(game, Render)) App.Toasts.Show(Loc.T("Trò này đang được dựng"), Icon("pencil"));
        }

        void OpenBooth(string booth, CasinoSpan span)
        {
            Casino.MarkSeen(S, "ev:" + span.Key);
            App.Save.Save();
            if (!CasinoGames.Open(booth, Render)) App.Toasts.Show(Loc.T("Trò này đang được dựng"), Icon("pencil"));
            Render();
        }

        void Lucky()
        {
            var s = S;
            double now = Now;
            if (!Casino.LuckyFlipped(s, now))
            {
                var e = Casino.FlipLucky(s, now);
                App.Save.Save();
                App.Toasts.Show(Loc.F("Hệ may mắn hôm nay: {0}", Elements.Name(e)), Icon(Keys.Of(e)));
                Haptics.Play(Haptic.UiTap);
            }
            Render();
        }

        // lịch lữ khách: sự kiện đang mở (còn bao lâu, khách mời), hai sự kiện kế
        void Board()
        {
            var s = S;
            var d = D;
            double now = Now;
            var act = Casino.Active(d, now);
            var sb = new System.Text.StringBuilder();
            if (act.Count == 0) sb.AppendLine(Loc.T("Hôm nay chưa có đoàn lữ khách nào ở bến."));
            foreach (var a in act)
            {
                string guest = Casino.Guest(d, a);
                var h = guest != null ? d.Hero(guest) : null;
                sb.AppendLine(Loc.F("{0}: còn {1}", a.ev.Name, ShopUi.Clock(Casino.Left(a, now))) +
                              (h != null && a.ev.booth != "race_fest" ? " · " + Loc.F("khách mời {0}", h.name) : ""));
                Casino.MarkSeen(s, "ev:" + a.Key);
            }
            var up = Casino.Upcoming(d, now, 2);
            if (up.Count > 0)
            {
                sb.AppendLine();
                sb.AppendLine(Loc.T("Sắp ghé:"));
                foreach (var u in up) sb.AppendLine(Loc.F("{0}: sau {1} ngày", u.ev.Name, u.startDay - Casino.Today(now)));
            }
            if (!Casino.Unlocked(s, d, Casino.Booths)) sb.AppendLine().Append(Casino.Need(s, d, Casino.Booths));
            else if (!Casino.TablesAllowed(d)) sb.AppendLine().Append(Loc.T("Lều lữ khách không mở ở khu vực của bạn."));
            var st = Casino.Of(s);
            if (st.betAll > 0)
                sb.AppendLine().AppendLine().Append(Loc.F("Ở lều lữ khách từ trước tới nay: đã cược {0} bi · đã thắng {1} bi",
                    NumFmt.Short((long)st.betAll), NumFmt.Short((long)st.wonAll)));
            App.Save.Save();
            App.Modals.Alert(Loc.T("Lịch lữ khách"), sb.ToString().TrimEnd(), Loc.T("Đóng"));
            Render();
        }

        // nút "Đi làm" của Quán trọ: mở trò của việc (việc thả bi thì vào máy bi, quay lại về đảo)
        void GoTask(string game)
        {
            if (game == SceneIds.Machine) App.Router.Go(SceneIds.Machine, SceneIds.Casino);
            else Open(game);
        }
    }

    // mở màn từng trò của đảo; trả false nếu trò chưa có màn (mốc sau). Màn trò đăng ký vào đây khi được dựng.
    public static class CasinoGames
    {
        static readonly System.Collections.Generic.Dictionary<string, Func<Action, bool>> openers =
            new System.Collections.Generic.Dictionary<string, Func<Action, bool>>();

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void Reset() => openers.Clear();

        public static void Register(string game, Func<Action, bool> open) => openers[game] = open;

        // scene của trò (null: trò chưa có scene, hoặc mở bằng hộp trên đảo)
        public static string SceneOf(string game)
        {
            switch (game)
            {
                case Casino.Fishing: return SceneIds.CasinoFishing;
                case Casino.Race: return SceneIds.CasinoRace;
                case Casino.Market: return SceneIds.CasinoMarket;
                case Casino.Underground: return SceneIds.CasinoUnderground;
                case Casino.Blackjack: return SceneIds.CasinoBlackjack;
                case Casino.Roulette: return SceneIds.CasinoRoulette;
                case Casino.Slot: return SceneIds.CasinoSlot;
                default: return null;
            }
        }

        // scene bàn may rủi: không bật popup bán bi / ưu đãi (mục 8, chơi có trách nhiệm)
        public static bool IsTable(string scene) =>
            scene == SceneIds.CasinoBlackjack || scene == SceneIds.CasinoRoulette || scene == SceneIds.CasinoSlot;

        public static bool Open(string game, Action onClose)
        {
            if (openers.TryGetValue(game, out var f)) return f(onClose);
            // mỗi trò tương tác một scene riêng (người dùng 2026-11-25 "mỗi gameplay 1 scene"); quay lại thì về đảo
            string scene = SceneOf(game);
            if (scene == null) return false;
            App.Router.Go(scene, game);
            return true;
        }
    }
}
