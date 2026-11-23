// Điều khiển trận (chép vòng run() của Web/src/view/battle/battleScreen.ts):
// Picking → người chơi chọn hoặc máy chọn; Ready → Execute; Idle → Advance; ForceSwap → hộp chọn tướng thay.
// Tự chơi bật/tắt giữa chừng; một nhịp trận, không có nấc tốc độ (lúc ra đòn sân tự chậm, StageView). Hết trận: thưởng ải, hộp kết quả.
// Nằm sẵn trên gốc prefab Screens/Battle; hộp Kết quả, Tạm dừng, Đổi tướng, Huy hiệu là prefab Dialogs/Tran*.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BattleArgs
    {
        public int stageId;
        public List<string> team; // null = đội trong bản lưu
        public BadgeRef badge; // trận thử thách của Đền Huy Hiệu (null = ải thường)
        public CaveRef cave; // trận Hang Tiềm Năng
        public double boost; // Tiếp sức (quảng cáo battle_retry, GD_Claude/26 mục 7.3): + phần trăm công và máu cả đội ta trong trận này
    }

    // tầng tier của Hang Tiềm Năng, boss hệ zone, ngày day (theo giờ máy)
    public sealed class CaveRef
    {
        public Elem zone;
        public int tier, day;
    }

    // trận i của bậc tier, dãy huy hiệu hệ zone
    public sealed class BadgeRef
    {
        public Elem zone;
        public int tier, i;
    }

    public sealed class BattleController : MonoBehaviour
    {
        [SerializeField] BattleView view;
        [SerializeField] BattleResultDialog resultPrefab;
        [SerializeField] BattlePauseDialog pausePrefab;
        [SerializeField] BattleSwapDialog swapPrefab;
        [SerializeField] BadgeWinDialog badgePrefab;
        Battle b;
        BattlePlayer player;
        StageDef stage;
        ZoneDef zone;
        List<string> team;
        BadgeRef badge;
        CaveRef cave;
        // nhịp trận (người dùng 2026-11-03: đánh và animation nhanh như lúc chạy thử, ×3 cũ). 2026-11-04 bỏ nấc tốc độ ×2, ×3: lúc ra
        // đòn sân tự chậm lại cho rõ animation (StageView), ngoài lúc đó chạy nhịp này. 2026-11-09: animation tướng về tốc độ gốc, nhịp này
        // chỉ còn tăng nhịp trận (chờ giữa các bước, chữ nổi, hiệu ứng, ra sân, rút lui, gục)
        const float Pace = 3f;
        float fast = 1; // công cụ thử chạy nhanh (FastForward)
        bool auto, busy, alive = true, waitingPick;
        bool usedAuto; // có lượt người chơi nào để máy tự chơi (ghi trận)
        float startedAt;
        public Battle Battle => b;
        public bool IsBoss => stage != null && stage.enemies.Any(e => e.boss); // nhạc boss (BattleScene.Music)

        // Dùng khi nướng prefab (Editor).
        public void Setup(BattleView battleView, BattleResultDialog result, BattlePauseDialog pause, BattleSwapDialog swap, BadgeWinDialog badgeWin)
        {
            view = battleView;
            resultPrefab = result;
            pausePrefab = pause;
            swapPrefab = swap;
            badgePrefab = badgeWin;
        }

        public void Begin(BattleArgs args)
        {
            var d = App.Data;
            var save = App.Save.Data;
            badge = args.badge;
            cave = args.cave;
            stage = cave != null ? Potential.CaveStage(d, cave.zone, cave.tier)
                : badge != null ? Badges.Stage(d, badge.zone, badge.tier, badge.i) : d.Stage(args.stageId) ?? d.Stage(1);
            zone = d.Zone(stage.zone);
            team = (args.team ?? save.team).Take(Progress.TeamSlots(save)).ToList(); // chỉ mang đủ số ô đội đã mở
            int unlock = save.level;
            // thử thách huy hiệu: hạt giống cố định theo (hệ, bậc, trận), thua đánh lại vẫn gặp cùng trận
            uint seed = badge != null ? Badges.Seed(d, badge.zone, badge.tier, badge.i) : Rng.RandomSeed();
            var mine = Teams.Player(save, team, d);
            if (args.boost > 0)
                foreach (var mb in mine.members)
                {
                    var o = mb.mods;
                    mb.mods = new StatMods { hpPct = (o?.hpPct ?? 0) + args.boost, atkPct = (o?.atkPct ?? 0) + args.boost, defPct = o?.defPct ?? 0, spd = o?.spd ?? 0 };
                }
            b = Battle.Create(d, mine, Teams.Enemy(stage, d), seed, unlock, Math.Max(unlock, stage.enemies[0].level));
            if (args.boost > 0) App.Toasts.Show(Loc.F("Tiếp sức: +{0}% công và máu", Math.Round(args.boost * 100)), App.Art.Icon("fist"));
            // trận hướng dẫn người mới (trận gương, trận 2 ở đảo mình khắc): thẻ rút sẵn, khoá thua ngầm (GD_Claude/25_FTUE.md)
            if (badge == null && cave == null) b.script = Tutorial.BattleFor(save, d, stage);
            view.Init(b, zone, badge == null && cave == null ? stage : null);
            view.Stage.speed = Pace;
            view.Stage.Epic = EpicOf();
            FastForward(1);
            view.AutoBtn.SetOnClick(ToggleAuto);
            view.AutoBtn.gameObject.SetActive(Tutorial.CoreDone(save)); // người mới: Tự chơi hiện sau chuỗi hướng dẫn
            Guide.Mark("battle.offer", view.Offer);
            Guide.Mark("battle.queue", view.QRow);
            Guide.Mark("battle.auto", view.AutoBtn);
            Guide.Mark("battle.stage", view.Stage);
            view.PauseBtn.SetOnClick(Menu);
            view.OnPickCard = (i, rt) => { if (!busy) StartCoroutine(OnPick(i, rt)); };
            view.OnInnate = (w, rt) => { if (!busy) StartCoroutine(OnInnate(w, rt)); };
            view.OnSwap = i => { if (!busy) StartCoroutine(OnSwap(i)); };
            player = new BattlePlayer(this, b, view)
            {
                Alive = () => alive,
                OnRound = r => Banner(Loc.F("Hiệp {0}", r), Loc.T("Bạn đi trước"), false),
                Banner = Banner,
                UltCut = UltCut,
                OnTurnFoe = _ =>
                {
                    view.RenderFoeThinking();
                    Guide.Note(Tutorial.FoeTurn, "battle.stage", Loc.T("Lượt địch"), 1.6f);
                },
            };
            StartCoroutine(Run());
        }

        // cho công cụ thử (menu PokiClash/Thử): bấm thẻ thứ i, bật tự chơi, chạy nhanh
        public void TestPick(int i)
        {
            if (busy || i >= view.OfferCards.Count || !view.OfferCards[i]) return;
            StartCoroutine(OnPick(i, (RectTransform)view.OfferCards[i].transform));
        }

        // Độ "epic" của cảm giác đánh 0..1 (người dùng 2026-11-16: tướng sau, độ khó cao hơn thì combat càng epic; StageView.Power):
        // ải thường = 50% tiến độ cả game (đảo theo order, ải trong đảo) + 35% tiến độ trong đảo (mỗi đảo dồn lên boss cuối) + 15% nếu
        // có boss. Thủy ải 1 ≈ 0, Thủy ải 70 ≈ 0,6, Hỏa ải 70 ≈ 0,7, Thổ ải 70 = 1. Thử thách huy hiệu theo bậc, hang theo tầng.
        float EpicOf()
        {
            var d = App.Data;
            if (cave != null)
                return Mathf.Clamp01(0.25f + 0.75f * cave.tier / Mathf.Max(1f, d.Cfg.cave.tiers.Count - 1));
            if (badge != null)
                return Mathf.Clamp01(0.2f + 0.8f * (badge.tier - 1) / Mathf.Max(1f, d.Cfg.badges.tiers.Count - 1));
            int n = Mathf.Max(1, d.ZoneStages(stage.zone).Count());
            int islands = Mathf.Max(1, d.Zones.Count);
            float inIsland = n > 1 ? (stage.idx - 1f) / (n - 1) : 0;
            float game = Mathf.Clamp01((zone.order * n + stage.idx - 1f) / Mathf.Max(1f, islands * n - 1f));
            float e = 0.5f * game + 0.35f * inIsland;
            if (stage.enemies.Any(x => x.boss)) e += 0.15f;
            return Mathf.Clamp01(e);
        }

        public bool WaitingPlayer => waitingPick && !busy && view.Flying == 0;
        // thời gian phát phần ra đòn mỗi lượt người chơi, quy về nhịp thường khi công cụ thử chạy nhanh (để đo nhịp trận)
        public readonly List<float> PlayerTurnSeconds = new List<float>();
        public bool Auto => auto;

        public void SetAuto(bool on)
        {
            if (auto != on) ToggleAuto();
        }

        // công cụ thử: cả trận (kể cả lúc ra đòn) chạy nhanh gấp k; người chơi không có nấc tốc độ
        public void FastForward(float k)
        {
            fast = Mathf.Max(1, k);
            view.Stage.fast = fast;
        }

        public void Stop()
        {
            alive = false;
            StopAllCoroutines();
        }

        object W(float ms) => new WaitForSecondsRealtime(ms / 1000f / (Pace * fast));

        // ---------- vòng trận ----------

        IEnumerator Run()
        {
            // Hai tướng ra sân lúc hai khung màn VS tách ra (trước 2026-11-17: dựng trước màn VS nên clip ra sân chạy hết sau màn che, người
            // chơi không thấy): địch trước, phe mình sau 0,2 giây; chờ clip ra sân (tối đa 2,4 giây) rồi mới băng rôn hiệp 1.
            view.FillPlate(0);
            view.FillPlate(1);
            bool entered = false;
            void Enter()
            {
                if (entered || !alive) return;
                entered = true;
                StartCoroutine(EnterBoth());
            }
            if (view.Intro && view.Intro.Ready) view.Intro.OnSplit = Enter;
            yield return Intro();
            if (!alive) yield break;
            Enter();
            yield return null;
            yield return new WaitForSecondsRealtime(0.25f / fast);
            float te = Time.realtimeSinceStartup;
            while (alive && (view.Stage.IsEntering(0) || view.Stage.IsEntering(1)) && Time.realtimeSinceStartup - te < 2.4f / fast) yield return null;
            if (!alive) yield break;
            startedAt = Time.realtimeSinceStartup;
            yield return player.PlayAll(b.StartBattle());
            while (alive && b.phase != Phase.Over)
            {
                if (b.phase == Phase.ForceSwap)
                {
                    if (b.turn.side == 0)
                    {
                        int idx = -1;
                        if (auto) idx = b.sides[0].fighters.FindIndex(f => !f.dead);
                        else yield return ChooseForced(i => idx = i);
                        if (!alive) yield break;
                        yield return player.PlayAll(b.ForceSwap(idx));
                    }
                    else yield return player.PlayAll(b.Advance());
                    continue;
                }
                if (b.phase == Phase.Picking)
                {
                    if (b.turn.side == 0 && auto) usedAuto = true;
                    if (b.turn.side == 0 && !auto) yield return PlayerPicking();
                    else yield return AiPicking();
                    if (!alive) yield break;
                    view.RenderOffer(auto);
                    float t0 = Time.realtimeSinceStartup;
                    int side = b.turn.side;
                    yield return player.PlayAll(b.Execute());
                    if (side == 0) PlayerTurnSeconds.Add((Time.realtimeSinceStartup - t0) * fast);
                    continue;
                }
                if (b.phase == Phase.Ready)
                {
                    yield return player.PlayAll(b.Execute());
                    continue;
                }
                yield return player.PlayAll(b.Advance());
            }
            if (alive) yield return Finish();
        }

        IEnumerator EnterBoth()
        {
            view.Stage.SetActor(1, b.ActiveOf(1).hero, b.ActiveOf(1).boss, true, Teams.LookStar(b.Data.Cfg, b.ActiveOf(1)));
            yield return new WaitForSecondsRealtime(0.2f / fast);
            if (!alive) yield break;
            view.Stage.SetActor(0, b.ActiveOf(0).hero, false, true, Teams.LookStar(b.Data.Cfg, b.ActiveOf(0)));
        }

        // màn VS kiểu trang truyện tranh (BattleIntro): đội địch khung trên, đội bạn khung dưới, lực chiến cả đội như hộp Chuẩn bị trận
        IEnumerator Intro()
        {
            if (!view.Intro || !view.Intro.Ready) yield break;
            var d = b.Data;
            int foePower = TeamPower.Of(d.Cfg, d, Teams.Enemy(stage, d));
            int minePower = TeamPower.Of(d.Cfg, d, Teams.Player(App.Save.Data, team, d));
            yield return view.Intro.Play(Loc.F("{0} · Ải {1}", zone.name, stage.idx), stage.name, Members(0), Members(1), minePower, foePower);
        }

        // tướng một phe cho màn VS (dạng theo sao như trên sân)
        List<BattleIntro.Member> Members(int side) =>
            b.sides[side].fighters.Select(f => new BattleIntro.Member
                { hero = f.hero, name = f.Name, star = Teams.LookStar(b.Data.Cfg, f), level = f.level, boss = f.boss }).ToList();

        // tuyệt kỹ: khung truyện tranh cắt thành dải hình bình hành ngang sân (UltCutIn) với mặt tướng ra chiêu và tên chiêu;
        // prefab chưa có dải thì băng rôn như cũ
        IEnumerator UltCut(int side, CardDef c)
        {
            var f = b.ActiveOf(side);
            if (view.UltCut)
                yield return view.UltCut.Play(f.hero, f.Name, Teams.LookStar(b.Data.Cfg, f), c.name, side == 0, (RectTransform)view.Stage.transform);
            else StartCoroutine(Banner(c.name, Loc.F("Tuyệt kỹ của {0}", f.Name), true));
        }

        // băng rôn giữa sân (hiệp mới, tuyệt kỹ)
        IEnumerator Banner(string title, string sub, bool ult)
        {
            var bn = view.TakeBanner();
            bn.Bind(title, sub, ult);
            var rt = bn.Rect;
            var cg = bn.Group;
            float w = 1200;
            for (float t = 0; t < 0.35f; t += Time.unscaledDeltaTime)
            {
                float k = t / 0.35f;
                float e = 1 - Mathf.Pow(1 - k, 3) + Mathf.Sin(k * Mathf.PI) * 0.06f;
                rt.anchoredPosition = new Vector2(-w * (1 - e), rt.anchoredPosition.y);
                rt.localEulerAngles = new Vector3(0, 0, 4 * (1 - e));
                yield return null;
            }
            rt.anchoredPosition = new Vector2(0, rt.anchoredPosition.y);
            rt.localEulerAngles = Vector3.zero;
            yield return W(ult ? 900 : 750);
            for (float t = 0; t < 0.25f; t += Time.unscaledDeltaTime)
            {
                float k = t / 0.25f;
                rt.anchoredPosition = new Vector2(w * k, rt.anchoredPosition.y);
                rt.localEulerAngles = new Vector3(0, 0, -3 * k);
                cg.alpha = 1 - k;
                yield return null;
            }
            view.ReleaseBanner(bn);
        }

        // ---------- người chơi chọn ----------

        IEnumerator PlayerPicking()
        {
            waitingPick = true;
            view.RenderQueue(-1, true);
            view.RenderOffer(auto);
            view.RenderBottom(auto);
            TutorTurn();
            while (alive && waitingPick)
            {
                // bật tự chơi giữa lúc chiêu đang chiếu (hoặc thẻ còn đang bay vào hàng) thì chờ xong
                if (auto && !busy && view.Flying == 0)
                {
                    waitingPick = false;
                    yield return AiPicking();
                    yield break;
                }
                yield return null;
            }
        }

        // Chọn thẻ (GameFeel 1.14, 2.4, 6.5; 2026-11-16): logic chạy ngay lúc chạm (Battle.Pick, chia lượt thẻ mới liền), hình đuổi theo
        // (BattleView.FlyToSlot). Không khoá chọn trong lúc thẻ bay, nên chạm nhanh liên tiếp không bị nuốt; chọn đủ thì chờ mọi thẻ chạm
        // hàng rồi mới ra đòn. Tiếng chọn leo cao độ theo lần chọn (ngũ cung), tiếng "land" khi thẻ cắm vào ô.
        IEnumerator OnPick(int i, RectTransform cardRt)
        {
            if (busy || b.phase != Phase.Picking || b.turn.side != 0 || auto) yield break;
            var t = b.turn;
            if (i < 0 || i >= t.offer.Count) yield break;
            int pickNo = t.picksTotal - t.picksLeft, qIdx = t.queue.Count;
            App.Audio.Play("pick", 1, BattlePlayer.Semitone(BattlePlayer.Pent(pickNo)));
            var slot = view.EmptyTiles.Count > 0 ? view.EmptyTiles[0] : null;
            var fallback = slot ? slot.position : cardRt ? cardRt.position : Vector3.zero;
            var clone = view.PickOffer(cardRt ? cardRt.GetComponent<UiCard>() : null);
            b.Pick(i);
            if (clone) view.HoldTile(qIdx);
            view.RenderQueue(-1, b.phase == Phase.Picking);
            view.RenderOffer(auto);
            view.RenderBottom(auto);
            // hướng dẫn: thẻ đầu xếp vào hàng (B2), đủ 5 lần chọn thì hàng chạy cuối lượt (B3)
            if (b.phase == Phase.Ready) Guide.Note(Tutorial.RunQueue, "battle.queue", Loc.F("Hàng thẻ chạy lần lượt, rồi {0} đánh thường.", b.ActiveOf(0).Name), 3.2f);
            else Guide.Note(Tutorial.Queue, "battle.queue", Loc.T("Thẻ xếp vào hàng. Mỗi lượt chọn 5 lần."), 3.2f);
            if (clone) yield return view.FlyToSlot(clone, qIdx, fallback, pickNo);
            if (b.phase == Phase.Ready && waitingPick)
            {
                while (alive && view.Flying > 0) yield return null;
                yield return W(200);
                waitingPick = false;
            }
        }

        // Chiêu: ra đòn ngay (chiếu xong mới chọn thẻ tiếp); Tuyệt kỹ: chỉ bật, thay cú đánh thường cuối lượt
        IEnumerator OnInnate(InnateKind which, RectTransform btn)
        {
            if (b.phase != Phase.Picking || b.turn.side != 0 || auto || busy) yield break;
            string why = b.InnateBlock(which);
            if (why != "")
            {
                App.Audio.Play("error");
                StartCoroutine(view.Shake(btn));
                App.Toasts.Show(why, App.Art.Icon("info"));
                yield break;
            }
            busy = true;
            var evs = b.UseInnate(which);
            App.Audio.Play("buff");
            view.RenderBottom(auto); // nút tắt ngay lúc bấm
            if (which == InnateKind.Ult)
            {
                App.Audio.Play("ult");
                view.Stage.Text(0, Loc.T("Tuyệt kỹ sẵn sàng!"), "#ff8fb3", 22);
            }
            yield return player.PlayAll(evs);
            busy = false;
            view.RenderQueue(-1, b.phase == Phase.Picking);
            view.RenderBottom(auto);
            // chiêu hạ đối thủ (hoặc xong trận): hết lúc chọn, cất thẻ mời, vòng trận chạy tiếp
            // (còn chọn thì thẻ mời giữ nguyên, không chia lại)
            if (b.phase != Phase.Picking)
            {
                view.RenderOffer(auto);
                waitingPick = false;
            }
            else if (which == InnateKind.Skill) Guide.Note(Tutorial.PickMore, "battle.offer", Loc.T("Chọn tiếp nhé."), 2.4f);
        }

        IEnumerator OnSwap(int idx)
        {
            if (b.turn.side != 0 || auto || busy) yield break;
            if (idx == b.sides[0].active) yield break;
            if (!b.CanSwap(idx))
            {
                App.Audio.Play("error");
                var f = b.sides[0].fighters[idx];
                App.Toasts.Show(f.dead ? Loc.F("{0} đã gục", f.hero.name) : Loc.T("Chỉ đổi tướng đầu lượt, trước khi chọn thẻ"), App.Art.Icon("info"));
                yield break;
            }
            busy = true;
            yield return player.PlayAll(b.Swap(idx));
            busy = false;
            view.RenderQueue(-1, true);
            view.RenderOffer(auto);
            view.RenderBottom(auto);
        }

        // hộp chọn tướng thay (bắt buộc), gợi ý khắc hệ
        IEnumerator ChooseForced(Action<int> done)
        {
            int chosen = -1;
            var dlg = App.Modals.Open(swapPrefab);
            dlg.Show(b, i => chosen = i);
            while (chosen < 0 && alive) yield return null;
            done(chosen);
        }

        // ---------- máy chọn (địch, hoặc tự chơi) ----------

        IEnumerator AiPicking()
        {
            int side = b.turn.side;
            view.RenderQueue(-1, true);
            view.RenderBottom(auto);
            if (side == 1) view.RenderFoeThinking();
            else view.RenderOffer(true);
            yield return W(420);
            int sw = BattleAi.SwapChoice(b);
            if (sw >= 0) yield return player.PlayAll(b.Swap(sw));
            while (alive && b.phase == Phase.Picking)
            {
                var inn = BattleAi.Innate(b);
                if (inn.HasValue)
                {
                    var c = b.InnateCard(b.ActiveOf(side), inn.Value).card;
                    var evs = b.UseInnate(inn.Value);
                    App.Audio.Play("buff");
                    view.RenderBottom(auto);
                    if (inn == InnateKind.Ult) view.Stage.Text(side, Loc.F("Tuyệt kỹ: {0}", c.name), "#ff8fb3", 20);
                    // chiêu: tên chiêu và đòn ra ngay trong lúc chiếu sự kiện
                    yield return player.PlayAll(evs);
                    view.RenderQueue(-1, b.phase == Phase.Picking);
                    yield return W(380);
                    continue; // chiêu hạ đối thủ thì hết lúc chọn
                }
                // địch ở các ải đầu chọn kém hơn (nhiễu cao), về sau chọn kỹ
                int i = BattleAi.PickIndex(b, side == 1 ? BattleAi.EnemyNoise(stage.id) : 0.12);
                if (side == 0)
                {
                    int pickNo = b.turn.picksTotal - b.turn.picksLeft, qIdx = b.turn.queue.Count;
                    var card = i < view.OfferCards.Count ? view.OfferCards[i] : null;
                    RectTransform clone = null;
                    var fallback = Vector3.zero;
                    if (card)
                    {
                        var rt = (RectTransform)card.transform;
                        rt.anchoredPosition += new Vector2(0, 28);
                        rt.localScale = new Vector3(1.05f, 1.05f, 1);
                        yield return W(260);
                        App.Audio.Play("pick", 1, BattlePlayer.Semitone(BattlePlayer.Pent(pickNo)));
                        if (card) // tắt tự chơi lúc chờ thì thẻ đã bị chia lại
                        {
                            var slot = view.EmptyTiles.Count > 0 ? view.EmptyTiles[0] : null;
                            fallback = slot ? slot.position : rt.position;
                            clone = view.PickOffer(card);
                        }
                    }
                    if (!alive || b.phase != Phase.Picking) break;
                    b.Pick(i);
                    if (clone) view.HoldTile(qIdx);
                    view.RenderQueue(-1, b.phase == Phase.Picking);
                    view.RenderOffer(true);
                    if (clone) yield return view.FlyToSlot(clone, qIdx, fallback, pickNo);
                }
                else
                {
                    var back = i < view.BackCards.Count ? view.BackCards[i] : null;
                    if (back)
                    {
                        back.anchoredPosition += new Vector2(0, 32);
                        back.localEulerAngles = new Vector3(0, 0, 4);
                        yield return W(200);
                    }
                    App.Audio.Play("deal");
                    b.Pick(i);
                    view.RenderQueue(-1, b.phase == Phase.Picking);
                    view.RenderFoeThinking();
                    yield return W(260);
                }
            }
        }

        // ---------- hướng dẫn người mới (GD_Claude/25_FTUE.md chặng B, C, D) ----------

        // đầu mỗi lượt chọn của người chơi
        void TutorTurn()
        {
            var s = App.Save.Data;
            var d = App.Data;
            // B1: trận gương, lượt đầu: ép chọn một thẻ
            if (b.script != null) Guide.Force(Tutorial.PickCard, "battle.offer", Loc.T("Lượt của bạn! Chọn 1 trong 3 thẻ."));
            // C14: trận 2 ở đảo mình khắc
            if (b.script != null && Tutorial.Done(s, Tutorial.Isles) && Battle.ElemMult(b.ActiveOf(0), b.ActiveOf(1)) > 1)
                Guide.Note(Tutorial.Counter, "battle.stage", Loc.F("{0} khắc {1}: đòn của bạn ×1,5!", Elements.Name(b.ActiveOf(0).hero.elem), Elements.Name(b.ActiveOf(1).hero.elem)), 3.6f);
            if (!Tutorial.CoreDone(s)) return;
            // D6: Tự chơi; D7: thẻ hiếm lần đầu
            if (s.stats.battles >= 2 && Guide.Hint(Tutorial.Auto, "battle.auto", Loc.T("Tự chơi: máy đánh thay bạn, tắt lúc nào cũng được.")))
                return;
            if (b.turn.offer.Any(id => d.Card(id)?.rarity >= Rarity.Rare))
                Guide.Note(Tutorial.RareCard, "battle.offer", Loc.T("Thẻ hiếm (viền màu đậm) mạnh hơn thẻ thường."), 3.2f);
        }

        int seenForm = -1;

        void LateUpdate()
        {
            if (b == null || App.Save?.Data == null) return;
            var s = App.Save.Data;
            if (view.SkillBtn) Guide.Mark("battle.skill", view.SkillBtn);
            if (view.UltBtn) Guide.Mark("battle.ult", view.UltBtn);
            // lượt chọn của người chơi đã vẽ xong (hàng thẻ, thẻ mời của lượt mới), không lúc chiêu đang chiếu hay thẻ đang bay
            bool myPick = WaitingPlayer && b.phase == Phase.Picking && b.turn.side == 0 && !auto;
            // B5, C15: Chiêu, Tuyệt kỹ lần đầu dùng được: ép bấm
            if (myPick && b.InnateBlock(InnateKind.Skill) == "")
                Guide.Force(Tutorial.Skill, "battle.skill", Loc.T("Đủ mana! Chiêu ra đòn ngay, không tốn lần chọn."));
            if (myPick && b.InnateBlock(InnateKind.Ult) == "")
                Guide.Force(Tutorial.Ult, "battle.ult", Loc.T("Nộ đầy! Tuyệt kỹ thay cú đánh thường cuối lượt."));
            if (!Tutorial.CoreDone(s) || b.phase == Phase.Over) return;
            // D2: hiệu ứng mới lần đầu (trên tướng hai bên); D3: bị choáng
            for (int side = 0; side < 2; side++)
            {
                var f = b.ActiveOf(side);
                foreach (var st in f.statuses)
                    if (!Tutorial.Done(s, Tutorial.StatusTip(st.id)))
                        Guide.Note(Tutorial.StatusTip(st.id), "battle.stage", StatusText(st.id), 3.6f);
            }
            if (b.turn.side == 0 && b.turn.stunned) Guide.Note(Tutorial.Stun, "battle.stage", Loc.T("Bị choáng: mất trọn lượt này."), 3f);
            // D5: địch tiến hóa giữa trận
            var foe = b.ActiveOf(1);
            if (foe.evo)
            {
                if (seenForm >= 0 && foe.form > seenForm)
                    Guide.Note(Tutorial.EvoNow, "battle.stage", Loc.T("Tiến hóa! Hạ tiếp tới dạng cuối."), 3f);
                seenForm = foe.form;
            }
        }

        static string StatusText(StatusId id)
        {
            switch (id)
            {
                case StatusId.Burn: return Loc.T("Bỏng: mất máu đầu mỗi lượt.");
                case StatusId.Poison: return Loc.T("Độc: mất máu đầu mỗi lượt, cộng dồn.");
                case StatusId.Stun: return Loc.T("Choáng: mất trọn lượt sau.");
                case StatusId.Regen: return Loc.T("Hồi phục: hồi máu đầu mỗi lượt.");
                case StatusId.Evade: return Loc.T("Né: tránh cú đánh thường kế tiếp.");
                default: return "";
            }
        }

        // ---------- nút trên ----------

        void ToggleAuto()
        {
            auto = !auto;
            view.SetAuto(auto);
            view.RenderOffer(auto);
            view.RenderBottom(auto);
        }

        public void Menu()
        {
            var dlg = App.Modals.Open(pausePrefab);
            dlg.Show(Loc.F("{0} · Ải {1}: {2}", zone.name, stage.idx, stage.name), () =>
            {
                Stop();
                LogBattle("bo");
                App.Save.Data.stats.battles++;
                App.Save.Save();
                if (badge != null) App.Router.Go(SceneIds.Badges, badge.zone);
                else if (cave != null) App.Router.Go(SceneIds.Cave);
                else App.Router.Go(SceneIds.Zone, stage.zone);
            });
        }

        // ---------- kết thúc ----------

        // ghi một dòng vào Logs/tran.csv (chỉ Editor và bản Development)
        void LogBattle(string result)
        {
#if UNITY_EDITOR || DEVELOPMENT_BUILD
            var d = App.Data;
            BattleLog.Write(zone, stage, team.Select(h => d.Hero(h).name), App.Save.Data.level, result, b.round,
                startedAt > 0 ? Time.realtimeSinceStartup - startedAt : 0, BattleLog.HpPct(b), usedAuto);
#endif
        }

        IEnumerator Finish()
        {
            bool win = b.winner == 0;
            LogBattle(win ? "thang" : "thua");
            // con cuối nằm hẳn (clip chết chạy trọn), bên thắng nhún mừng một cái, rồi mới hiện bảng kết quả
            yield return view.Stage.WaitSettled(4.5f);
            if (b.winner >= 0 && b.winner < 2 && !view.Stage.IsDown(b.winner)) view.Stage.Dodge(b.winner);
            yield return new WaitForSecondsRealtime(0.55f);
            if (badge != null)
            {
                yield return BadgeFinish(win);
                yield break;
            }
            if (cave != null)
            {
                yield return CaveFinish(win);
                yield break;
            }
            var s = App.Save.Data;
            var d = App.Data;
            int before = s.level;
            // trận hướng dẫn: trận gương (B8: hộp kết quả chỉ chừa nút Máy bi), trận 2 ở đảo mình khắc (C16: khoanh ô mảnh)
            bool tutFirst = win && b.script != null && !Tutorial.Done(s, Tutorial.Balls);
            bool tutCounter = win && b.script != null && !tutFirst && stage.zone == Tutorial.CounterIsland(s, d) && !Tutorial.Done(s, Tutorial.Shards);
            bool firstLoss = !win && !Tutorial.Done(s, Tutorial.FirstLoss);
            StageReward rw = null;
            if (win) rw = Progress.WinStage(s, d, stage.id, new Rng(Rng.RandomSeed()));
            else s.stats.battles++;
            if (win) Tutorial.SeedTree(s, d.Cfg, PokiClash.Game.SaveService.Now()); // cây bi đầu tiên có sẵn 10 bi
            if (tutCounter) Tutorial.MarkAll(s, Tutorial.CounterIsle, Tutorial.CounterGo, Tutorial.Counter);
            if (firstLoss) Tutorial.Mark(s, Tutorial.FirstLoss);
            App.Save.Save();
            App.Audio.Play(win ? "win" : "lose");
            Haptics.Play(win ? Haptic.Win : Haptic.Lose);

            // cửa hàng (GD_Claude/26 mục 7.3): báo thua / thắng cho bộ máy ưu đãi; trận có kịch bản hướng dẫn thì không
            bool scripted = b.script != null;
            string freeFix = !win ? Offers.FreeFix(s, d, team) : null;
            if (!scripted)
                OfferHost.Raise(win ? new OfferCtx { e = OfferEvent.BattleWon, stage = stage.id, boss = stage.enemies.Any(e => e.boss) }
                    : new OfferCtx { e = OfferEvent.BattleLost, stage = stage.id, freeFix = freeFix != null });
            int lossStreak = !win && s.shop != null && s.shop.offers.lossStage == stage.id ? s.shop.offers.lossStreak : 0;

            var next = d.ZoneStages(stage.zone).FirstOrDefault(x => x.idx == stage.idx + 1);
            var m = App.Modals.Open(resultPrefab, mandatory: true);
            m.Show(win, Loc.F("{0} · Ải {1} · {2}", zone.name, stage.idx, stage.name), 40, Loc.F("{0} hiệp · gây {1} sát thương", b.round, b.dmgDealt[0]));
            if (rw != null)
            {
                m.Reward().Item(App.Art.Icon("ball"), $"×{rw.balls}", Loc.T("Bi")).Tag(rw.first ? Loc.T("Lần đầu") : "", Theme.Yellow);
                foreach (var sh in rw.shards)
                {
                    var hero = d.Hero(sh.hero);
                    // nhãn: mở khoá, mảnh đổi thành bản sao thẻ (tướng 20 sao), hoặc tiến độ mảnh (chưa có: tới mở khoá; đã có: tới sao kế)
                    var goal = Progress.ShardGoal(s, d, sh.hero);
                    var tile = m.Reward().Hero(hero, $"×{sh.n}").Tag(sh.unlocked ? Loc.T("MỞ KHÓA!") : sh.converted > 0 ? Loc.F("→ {0} thẻ", sh.converted)
                        : goal.need > 0 ? $"{goal.have}/{goal.need}" : $"{goal.have}", sh.unlocked ? Theme.Red : Theme.Paper2);
                    if (sh.unlocked) App.Audio.Play("chest");
                    if (tutCounter && sh.hero != s.starter && goal.need > 0)
                    {
                        Guide.Mark("result.shard", tile);
                        Guide.Note(Tutorial.Shards, "result.shard", Loc.F("Gom đủ {0} mảnh để thu phục {1}.", goal.need, hero.name), 4.5f);
                    }
                }
                if (rw.evoStones > 0) m.Reward().EvoStones(rw.evoStones);
                // Nhận ×2 bằng quảng cáo (win_double): trao thêm đúng chừng ấy bi, mảnh, đá tiến hóa
                if (!scripted)
                {
                    var won = rw;
                    m.AdButton(Loc.T("Nhận ×2"), Ads.WinDouble, true, () =>
                    {
                        var rng2 = new Rng(Rng.RandomSeed());
                        var extra = new List<Reward>();
                        if (won.balls > 0)
                        {
                            s.balls += won.balls;
                            extra.Add(new Reward { k = RewardKind.Balls, n = won.balls });
                        }
                        foreach (var sh in won.shards)
                            extra.Add(new Reward { k = RewardKind.Shards, n = sh.n, hero = sh.hero, res = Progress.AddShards(s, d, sh.hero, sh.n, rng2) });
                        if (won.evoStones > 0)
                        {
                            s.evoStones += won.evoStones;
                            extra.Add(new Reward { k = RewardKind.EvoStones, n = won.evoStones });
                        }
                        App.Save.Save();
                        ShopService.Show(Loc.T("Thưởng ×2"), extra);
                    });
                }
            }
            else
            {
                var foeElem = d.Hero(stage.enemies[0].hero).elem;
                var strong = Elements.All.First(x => Elements.Beats(x) == foeElem);
                // lần thua đầu (E2): nói rõ thua không mất gì, rồi cách mạnh hơn (hàng nút bên dưới đi thẳng tới đó)
                // thua từ lần 2 liền ở ải này: nói rõ cách miễn phí đang làm được ngay, rồi mới tới nút Tiếp sức (quảng cáo)
                string streakLine = lossStreak >= 2
                    ? Loc.F("Thua {0} lần liền ở ải này. ", lossStreak) + (freeFix != null ? Loc.F("Làm ngay được: {0}.\n", freeFix) : Loc.T("Thử đánh ải dễ hơn, hoặc nhận AFK rồi quay lại.\n"))
                    : "";
                m.Tips((firstLoss ? Loc.T("Thua không mất gì! Mạnh hơn bằng:\n") : "") + streakLine +
                       Loc.T("• Thả bi ở Máy bi để lên cấp: mọi tướng mạnh lên.\n• Nâng thẻ và tiến hóa ở mục Tướng.\n") +
                       Loc.F("• Chọn tướng khắc hệ địch ({0} bị {1} khắc), hoặc đánh ải dễ hơn ở đảo khác.", Elements.Name(foeElem), Elements.Name(strong)));
                if (lossStreak >= 2 && !scripted)
                    m.AdButton(Loc.F("Tiếp sức +{0}%", Math.Round(d.Cfg.shop.retryBoost * 100)), Ads.BattleRetry, false,
                        () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = stage.id, team = team, boost = d.Cfg.shop.retryBoost }));
            }
            if (tutFirst)
            {
                // B8: chỉ một đường đi tiếp, tới Máy Bi
                var mb = m.Button(Loc.F("Máy bi ({0})", s.balls), BtnColor.Orange, 250, () => App.Router.Go(SceneIds.Machine));
                Guide.Mark("result.machine", mb);
                Guide.Force(Tutorial.Balls, "result.machine", Loc.T("Bi! Thả bi vào Máy Bi để lên cấp."));
            }
            else
            {
                if (s.balls > 0)
                    m.Button(Loc.F("Máy bi ({0})", s.balls), BtnColor.Orange, 250, () => App.Router.Go(SceneIds.Machine));
                if (!win && Tutorial.Shows(s, d, Tutorial.HubPart.Heroes, PokiClash.Game.SaveService.Now()))
                    m.Button(Loc.T("Tướng"), BtnColor.Green, 200, () => App.Router.Go(SceneIds.Heroes));
                if (win && next != null && Progress.StageOpen(s, next))
                    // về đảo và mở luôn hộp chuẩn bị của ải kế
                    m.Button(Loc.T("Ải tiếp »"), BtnColor.Green, 210, () => App.Router.Go(SceneIds.Zone, new ZoneArgs { zone = stage.zone, prep = next.id }));
                m.Button(Loc.T("Đánh lại"), BtnColor.Paper, 200, () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = stage.id, team = team }));
                m.Button(zone.name, BtnColor.Paper, 200, () => App.Router.Go(SceneIds.Zone, stage.zone));
            }
            yield return new WaitForSecondsRealtime(0.12f);
            App.Audio.Play("stamp");
            Haptics.Play(Haptic.Stamp);
            // tướng mới mở khoá nhờ mảnh của trận: màn mở khoá (App/Shop/HeroUnlockView) đè lên hộp kết quả; trận hướng dẫn thì thôi
            // (mũi tên chỉ dẫn đang khoá chạm vào hộp kết quả)
            var fresh = rw != null && !scripted ? rw.shards.Where(x => x.unlocked).Select(x => x.hero).ToList() : new List<string>();
            if (fresh.Count > 0)
            {
                yield return new WaitForSecondsRealtime(0.5f);
                bool fin = false;
                HeroUnlockView.Play(fresh, () => fin = true);
                while (!fin) yield return null;
            }
            if (s.level > before) Dialogs.LevelUp(before, s.level);
        }

        // kết trận Hang, kết trận thử thách Đền Huy Hiệu: side meta tự lo (agent B, 2026-11-17: Game/Potential/CaveResult.cs,
        // Game/Badges/BadgeResult.cs; sao từng trận, thưởng lần đầu, đá tinh, mốc sao)
        IEnumerator CaveFinish(bool win) => CaveResult.Run(b, cave, stage, team, resultPrefab);

        IEnumerator BadgeFinish(bool win) => BadgeResult.Run(b, badge, stage, team, resultPrefab, badgePrefab);
    }
}
