// Điều khiển trận (chép vòng run() của Web/src/view/battle/battleScreen.ts):
// Picking → người chơi chọn hoặc máy chọn; Ready → Execute; Idle → Advance; ForceSwap → hộp chọn tướng thay.
// Tự chơi bật/tắt giữa chừng; tốc độ ×1/2/3 lưu vào cài đặt. Hết trận: thưởng ải, hộp kết quả.
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
        float speed = 1;
        bool auto, busy, alive = true, waitingPick;
        bool usedAuto; // có lượt người chơi nào để máy tự chơi (ghi trận)
        float startedAt;
        readonly HashSet<string> hinted = new HashSet<string>();
        public Battle Battle => b;

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
            team = args.team ?? save.team;
            speed = Mathf.Clamp(save.settings.speed, 1, 3);
            int unlock = save.level;
            // thử thách huy hiệu: hạt giống cố định theo (hệ, bậc, trận), thua đánh lại vẫn gặp cùng trận
            uint seed = badge != null ? Badges.Seed(d, badge.zone, badge.tier, badge.i) : Rng.RandomSeed();
            b = Battle.Create(d, Teams.Player(save, team, d), Teams.Enemy(stage), seed, unlock, Math.Max(unlock, stage.enemies[0].level));
            view.Init(b, zone);
            view.Stage.speed = speed;
            view.SetSpeed((int)speed);
            view.SpeedBtn.SetOnClick(ToggleSpeed);
            view.AutoBtn.SetOnClick(ToggleAuto);
            view.PauseBtn.SetOnClick(Menu);
            view.OnPickCard = (i, rt) => { if (!busy) StartCoroutine(OnPick(i, rt)); };
            view.OnInnate = OnInnate;
            view.OnSwap = i => { if (!busy) StartCoroutine(OnSwap(i)); };
            player = new BattlePlayer(this, b, view, () => speed)
            {
                Alive = () => alive,
                OnRound = r => Banner($"Hiệp {r}", "Bạn đi trước", false),
                Banner = Banner,
                OnTurnFoe = _ => view.RenderFoeThinking(),
            };
            StartCoroutine(Run());
        }

        // cho công cụ thử (menu PokiClash/Thử): bấm thẻ thứ i, bật tự chơi, đặt tốc độ
        public void TestPick(int i)
        {
            if (busy || i >= view.OfferCards.Count) return;
            StartCoroutine(OnPick(i, (RectTransform)view.OfferCards[i].transform));
        }

        public bool WaitingPlayer => waitingPick && !busy;
        // thời gian phát phần ra đòn mỗi lượt người chơi, quy về tốc độ ×1 (để đo nhịp trận)
        public readonly List<float> PlayerTurnSeconds = new List<float>();
        public bool Auto => auto;

        public void SetAuto(bool on)
        {
            if (auto != on) ToggleAuto();
        }

        public void SetSpeed(int s)
        {
            while ((int)speed != Mathf.Clamp(s, 1, 3)) ToggleSpeed();
        }

        public void Stop()
        {
            alive = false;
            StopAllCoroutines();
        }

        object W(float ms) => new WaitForSecondsRealtime(ms / 1000f / speed);

        // ---------- vòng trận ----------

        IEnumerator Run()
        {
            view.Stage.SetActor(0, b.ActiveOf(0).hero, false, true, b.ActiveOf(0).star);
            view.Stage.SetActor(1, b.ActiveOf(1).hero, b.ActiveOf(1).boss, true, b.ActiveOf(1).star);
            view.FillPlate(0);
            view.FillPlate(1);
            yield return Intro();
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
                    if (side == 0) PlayerTurnSeconds.Add((Time.realtimeSinceStartup - t0) * speed);
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

        // màn VS: đội địch, chữ VS, đội bạn
        IEnumerator Intro()
        {
            var o = view.Intro;
            o.gameObject.SetActive(true);
            o.transform.SetAsLastSibling();
            var cg = o.Group;
            cg.alpha = 1;
            o.Title.text = $"{zone.name} · Ải {stage.idx} · {stage.name}";
            TeamRow(o.Row(1), 1);
            var vs = o.Vs;
            TeamRow(o.Row(0), 0);
            App.Audio.Play("whoosh");
            for (float t = 0; t < 0.5f; t += Time.unscaledDeltaTime)
            {
                float k = Mathf.Min(1, t / 0.5f);
                float s = k < 0.6f ? Mathf.Lerp(0.3f, 1.12f, k / 0.6f) : Mathf.Lerp(1.12f, 1, (k - 0.6f) / 0.4f);
                vs.rectTransform.localScale = new Vector3(s, s, 1);
                yield return null;
            }
            yield return new WaitForSecondsRealtime(1.0f);
            for (float t = 0; t < 0.3f; t += Time.unscaledDeltaTime)
            {
                cg.alpha = 1 - t / 0.3f;
                yield return null;
            }
            o.gameObject.SetActive(false);
        }

        // chân dung một đội trong màn VS (hàng dựng sẵn, chân dung là bản sao kit)
        void TeamRow(RectTransform row, int side)
        {
            for (int i = row.childCount - 1; i >= 0; i--) Destroy(row.GetChild(i).gameObject);
            var fs = b.sides[side].fighters;
            for (int i = 0; i < fs.Count; i++)
            {
                float h = side == 1 && fs[i].boss ? 240 : 192;
                var p = HeroArt.Portrait(row, fs[i].hero, h, false, fs[i].star);
                p.anchorMin = p.anchorMax = new Vector2(0.5f, 0);
                p.anchoredPosition = new Vector2((i - (fs.Count - 1) / 2f) * 220, 10);
                if (side == 1) p.localScale = new Vector3(1, 1, 1);
                else p.localScale = new Vector3(-1, 1, 1);
            }
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
            Hint("pick", null);
            while (alive && waitingPick)
            {
                if (auto)
                {
                    waitingPick = false;
                    yield return AiPicking();
                    yield break;
                }
                yield return null;
            }
        }

        IEnumerator OnPick(int i, RectTransform cardRt)
        {
            if (busy || b.phase != Phase.Picking || b.turn.side != 0 || auto) yield break;
            busy = true;
            App.Audio.Play("pick");
            var slot = view.EmptyTiles.Count > 0 ? view.EmptyTiles[0] : null;
            if (cardRt && slot) yield return FlyCard(cardRt, slot);
            b.Pick(i);
            view.RenderQueue(-1, b.phase == Phase.Picking);
            view.RenderOffer(auto);
            view.RenderBottom(auto);
            busy = false;
            if (b.phase == Phase.Ready)
            {
                yield return W(350);
                waitingPick = false;
            }
        }

        IEnumerator FlyCard(RectTransform from, RectTransform to)
        {
            // thẻ bay: thẻ kit dùng lại trong lớp phủ, gán cùng thẻ với thẻ vừa chọn
            var clone = view.TakeFlyCard(from.GetComponent<UiCard>());
            clone.anchorMin = clone.anchorMax = new Vector2(0.5f, 0.5f);
            clone.sizeDelta = from.rect.size;
            clone.position = from.position;
            from.gameObject.SetActive(false);
            var a = clone.position;
            var z = to.position;
            for (float t = 0; t < 0.27f; t += Time.unscaledDeltaTime)
            {
                float k = t / 0.27f;
                float e = k * k * (3 - 2 * k);
                clone.position = Vector3.Lerp(a, z, e);
                float s = Mathf.Lerp(1, 0.32f, e);
                clone.localScale = new Vector3(s, s, 1);
                clone.localEulerAngles = new Vector3(0, 0, 12 * e);
                yield return null;
            }
            view.ReleaseFlyCard();
        }

        void OnInnate(InnateKind which, RectTransform btn)
        {
            if (b.turn.side != 0 || auto || busy) return;
            string why = b.InnateBlock(which);
            if (why != "")
            {
                App.Audio.Play("error");
                StartCoroutine(view.Shake(btn));
                App.Toasts.Show(why, App.Art.Icon("info"));
                return;
            }
            var evs = b.UseInnate(which);
            if (evs.Count > 0)
            {
                player.LastSnap = evs[evs.Count - 1].snap;
                view.ApplySnap(player.LastSnap);
            }
            App.Audio.Play("buff");
            if (which == InnateKind.Ult)
            {
                App.Audio.Play("ult");
                view.Stage.Text(0, "Tuyệt kỹ sẵn sàng!", "#ff8fb3", 22);
            }
            view.RenderQueue(-1, true);
            view.RenderBottom(auto);
        }

        IEnumerator OnSwap(int idx)
        {
            if (b.turn.side != 0 || auto || busy) yield break;
            if (idx == b.sides[0].active) yield break;
            if (!b.CanSwap(idx))
            {
                App.Audio.Play("error");
                var f = b.sides[0].fighters[idx];
                App.Toasts.Show(f.dead ? $"{f.hero.name} đã gục" : "Chỉ đổi tướng đầu lượt, trước khi chọn thẻ", App.Art.Icon("info"));
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
                    var evs = b.UseInnate(inn.Value);
                    if (evs.Count > 0)
                    {
                        player.LastSnap = evs[evs.Count - 1].snap;
                        view.ApplySnap(player.LastSnap);
                    }
                    var c = b.InnateCard(b.ActiveOf(side), inn.Value).card;
                    view.Stage.Text(side, $"{(inn == InnateKind.Ult ? "Tuyệt kỹ" : "Chiêu")}: {c.name}", inn == InnateKind.Ult ? "#ff8fb3" : "#8ec5ff", 20);
                    App.Audio.Play("buff");
                    view.RenderQueue(-1, true);
                    yield return W(380);
                }
                // địch ở các ải đầu chọn kém hơn (nhiễu cao), về sau chọn kỹ
                int i = BattleAi.PickIndex(b, side == 1 ? BattleAi.EnemyNoise(stage.id) : 0.12);
                if (side == 0)
                {
                    var card = i < view.OfferCards.Count ? view.OfferCards[i] : null;
                    if (card)
                    {
                        var rt = (RectTransform)card.transform;
                        rt.anchoredPosition += new Vector2(0, 28);
                        rt.localScale = new Vector3(1.05f, 1.05f, 1);
                        yield return W(260);
                        App.Audio.Play("pick");
                        var slot = view.EmptyTiles.Count > 0 ? view.EmptyTiles[0] : null;
                        if (slot) yield return FlyCard(rt, slot);
                    }
                    b.Pick(i);
                    view.RenderQueue(-1, b.phase == Phase.Picking);
                    view.RenderOffer(true);
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

        // ---------- gợi ý 2 trận đầu ----------

        void Hint(string key, RectTransform anchor)
        {
            var s = App.Save.Data;
            if (!s.settings.hints || hinted.Contains(key) || s.stats.battles > 1) return;
            hinted.Add(key);
            string text = key == "pick" ? "Chọn 1 trong 3 thẻ, 5 lần. Thẻ chạy lần lượt rồi tướng đánh thường."
                : key == "skill" ? "Đủ mana: bấm Chiêu để xen chiêu vào hàng thẻ. Không tốn lần chọn!"
                : "Đủ nộ: bật Tuyệt kỹ, nó thay cú đánh thường cuối lượt.";
            var hint = Ui.Spawn(Theme.Prefabs.hint, view.Overlay);
            hint.name = "goi_y";
            hint.Set(text, 620);
            var bubble = hint.Rect;
            bubble.anchorMin = bubble.anchorMax = new Vector2(0.5f, 0);
            bubble.pivot = new Vector2(0.5f, 0);
            // gợi ý chọn thẻ nằm trên mép bảng dưới (không che thẻ), gợi ý Chiêu/Tuyệt kỹ nằm trên hàng nút
            bubble.anchoredPosition = anchor ? new Vector2(0, 190) : new Vector2(-210, BattleView.PanelH + 240);
            StartCoroutine(Remove(bubble.gameObject, 4.2f));
        }

        static IEnumerator Remove(GameObject go, float s)
        {
            yield return new WaitForSecondsRealtime(s);
            if (go) Destroy(go);
        }

        void LateUpdate()
        {
            // gợi ý Chiêu, Tuyệt kỹ khi lần đầu dùng được
            if (b == null || b.phase != Phase.Picking || b.turn.side != 0 || auto) return;
            if (b.InnateBlock(InnateKind.Skill) == "") Hint("skill", view.SkillBtn);
            if (b.InnateBlock(InnateKind.Ult) == "") Hint("ult", view.UltBtn);
        }

        // ---------- nút trên ----------

        void ToggleSpeed()
        {
            speed = speed >= 3 ? 1 : speed + 1;
            view.Stage.speed = speed;
            view.SetSpeed((int)speed);
            App.Save.Data.settings.speed = (int)speed;
            App.Save.Save();
        }

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
            dlg.Show($"{zone.name} · Ải {stage.idx}: {stage.name}", () =>
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
            yield return new WaitForSecondsRealtime(0.5f);
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
            StageReward rw = null;
            if (win) rw = Progress.WinStage(s, d, stage.id, new Rng(Rng.RandomSeed()));
            else s.stats.battles++;
            App.Save.Save();
            App.Audio.Play(win ? "win" : "lose");

            var next = d.ZoneStages(stage.zone).FirstOrDefault(x => x.idx == stage.idx + 1);
            var m = App.Modals.Open(resultPrefab, mandatory: true);
            m.Show(win, $"{zone.name} · Ải {stage.idx} · {stage.name}", 40, $"{b.round} hiệp · gây {b.dmgDealt[0]} sát thương");
            if (rw != null)
            {
                m.Reward(App.Art.Icon("ball"), null, $"+{rw.balls} bi", rw.first ? "Lần đầu qua ải" : null, Color.white);
                foreach (var sh in rw.shards)
                {
                    var hero = d.Hero(sh.hero);
                    var prog = s.Hero(sh.hero);
                    m.Reward(null, hero, sh.unlocked ? $"Mở khóa {hero.name}!" : $"{hero.name} +{sh.n} mảnh",
                        sh.unlocked ? "Tướng mới đã vào đội hình" : sh.converted > 0 ? $"Đã có tướng: đổi thành {sh.converted} bản sao thẻ" : $"{prog.shards}/{hero.shards} mảnh",
                        sh.unlocked ? Theme.Hex("#fff3c4") : Color.white);
                    if (sh.unlocked) App.Audio.Play("chest");
                }
            }
            else
            {
                var foeElem = d.Hero(stage.enemies[0].hero).elem;
                var strong = Elements.All.First(x => Elements.Beats(x) == foeElem);
                m.Tips("• Thả bi ở Máy bi để lên cấp: mọi tướng mạnh lên.\n• Nâng thẻ và tiến hóa ở mục Tướng.\n" +
                       $"• Chọn tướng khắc hệ địch ({Elements.Name(foeElem)} bị {Elements.Name(strong)} khắc).");
            }
            if (win && s.balls > 0)
                m.Button($"Máy bi ({s.balls})", BtnColor.Orange, 250, () => App.Router.Go(SceneIds.Machine));
            if (win && next != null && Progress.StageOpen(s, next))
                // về đảo và mở luôn hộp chuẩn bị của ải kế
                m.Button("Ải tiếp »", BtnColor.Green, 210, () => App.Router.Go(SceneIds.Zone, new ZoneArgs { zone = stage.zone, prep = next.id }));
            m.Button("Đánh lại", BtnColor.Paper, 200, () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = stage.id, team = team }));
            m.Button(zone.name, BtnColor.Paper, 200, () => App.Router.Go(SceneIds.Zone, stage.zone));
            yield return new WaitForSecondsRealtime(0.12f);
            App.Audio.Play("stamp");
            if (s.level > before) Dialogs.LevelUp(before, s.level);
        }

        // kết trận Hang: thắng thì đá và trừ một lượt; thua không mất lượt
        IEnumerator CaveFinish(bool win)
        {
            var s = App.Save.Data;
            var cfg = App.Data.Cfg;
            s.stats.battles++;
            int stones = 0;
            if (win)
            {
                s.stats.wins++;
                stones = Potential.WinCave(s, cfg, cave.day, cave.tier);
            }
            App.Save.Save();
            App.Audio.Play(win ? "win" : "lose");
            var m = App.Modals.Open(resultPrefab, mandatory: true);
            m.Show(win, $"Hang Tiềm Năng · Tầng {cfg.cave.tiers[cave.tier].name} · boss hệ {Elements.Name(cave.zone)}", 38,
                $"{b.round} hiệp · gây {b.dmgDealt[0]} sát thương");
            int left = Potential.CaveLeft(s, cfg, cave.day);
            if (win)
                m.Reward(App.Art.Icon("rock"), null, stones > 0 ? $"+{stones} đá tiềm năng" : "Hết lượt hôm nay: không có đá",
                    $"Còn {Mathf.Max(0, left)} lượt hôm nay · có {s.potentialStones} đá", Theme.Hex("#f4efff"));
            else
                m.Tips($"Thua không mất lượt (còn {left} lượt). Chọn tướng khắc hệ {Elements.Name(cave.zone)}, khai phá tiềm năng hoặc thử tầng dễ hơn.");
            if (left > 0)
                m.Button(win ? "Đánh tiếp" : "Đánh lại", BtnColor.Green, 230,
                    () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = stage.id, team = team, cave = cave }));
            m.Button("Về Hang", BtnColor.Paper, 220, () => App.Router.Go(SceneIds.Cave));
            yield return new WaitForSecondsRealtime(0.12f);
            App.Audio.Play("stamp");
        }

        // kết trận thử thách: thắng thì bi và tiến độ; trận cuối của bậc thì hộp huy hiệu rồi mở rương; thua thì giữ tiến độ
        IEnumerator BadgeFinish(bool win)
        {
            var s = App.Save.Data;
            var d = App.Data;
            var cfg = d.Cfg;
            int before = s.level;
            var rng = new Rng(Rng.RandomSeed());
            BadgeWin rw = null;
            s.stats.battles++;
            if (win)
            {
                s.stats.wins++;
                rw = Badges.Win(s, d, badge.zone, rng);
            }
            App.Save.Save();
            App.Audio.Play(win ? "win" : "lose");

            int n = Badges.Count(cfg, badge.tier);
            var m = App.Modals.Open(resultPrefab, mandatory: true);
            m.Show(win, $"Đền Huy Hiệu · {Elements.Name(badge.zone)} · {Badges.TierName(cfg, badge.tier)} · Trận {badge.i}/{n}", 38,
                $"{b.round} hiệp · gây {b.dmgDealt[0]} sát thương");
            if (rw != null)
                m.Reward(App.Art.Icon("ball"), null, $"+{rw.balls} bi", rw.tierDone > 0 ? "Xong bậc!" : $"Tiến độ {badge.i}/{n}", Color.white);
            else
                m.Tips("Thua thì đánh lại trận này, tiến độ vẫn giữ. Chọn tướng khắc hệ " + Elements.Name(badge.zone) + ", nâng thẻ và tiến hóa để mạnh hơn.");
            var cur = Badges.Current(s, cfg, badge.zone);
            var nextRef = win && cur != null && rw.tierDone == 0 ? new BadgeRef { zone = badge.zone, tier = cur.Value.tier, i = cur.Value.i } : null;
            if (nextRef != null)
                m.Button("Trận tiếp »", BtnColor.Green, 240,
                    () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = Badges.StageId(d, nextRef.zone, nextRef.tier, nextRef.i), team = team, badge = nextRef }));
            if (!win)
                m.Button("Đánh lại", BtnColor.Green, 220, () => App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = stage.id, team = team, badge = badge }));
            m.Button("Về Đền", BtnColor.Paper, 220, () => App.Router.Go(SceneIds.Badges, badge.zone));
            yield return new WaitForSecondsRealtime(0.12f);
            App.Audio.Play("stamp");

            if (rw != null && rw.tierDone > 0)
            {
                // hộp huy hiệu rồi mở rương (trên hộp kết quả), sau cùng mới báo lên cấp
                yield return new WaitForSecondsRealtime(0.5f);
                bool closed = false;
                App.Audio.Play("level");
                var bm = App.Modals.Open(badgePrefab, () => closed = true);
                bm.Show(badge.zone, rw.tierDone, $"Huy hiệu {Elements.Name(badge.zone)} · {Badges.TierName(cfg, rw.tierDone)}",
                    $"Tướng hệ {Elements.Name(badge.zone)} +{Badges.Bonus(cfg, rw.tierDone) * 100:0}% Máu, Công, Thủ (bậc cao nhất, không cộng dồn).",
                    $"Mở {Pachinko.ChestName(rw.chest)}");
                while (!closed) yield return null;
                yield return ChestBox.Show(Pachinko.ChestName(rw.chest), rw.chest, null, rw.rewards, "Nhận");
            }
            if (s.level > before) Dialogs.LevelUp(before, s.level);
        }
    }
}
