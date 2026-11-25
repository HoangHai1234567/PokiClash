// Scene Trường đua của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.3; mỗi trò một scene). Prefab Screens/CasinoRace (menu
// "PokiClash/Prefab/Đảo Casino/Trường đua: dựng scene"). Lõi: Core/Casino/Race.cs.
// Người dùng 2026-11-25: "random 3-5 tướng mỗi lane chạy đua nhau, trên đường chạy tướng có thể đánh nhau cho vui vui, có tướng bị
// choáng stun, nó cũng kiểu random ai về nhất cho vui thôi".
// - Trên: 5 hạng cúp, dòng điểm cúp tuần + lượt có thưởng, đường hôm nay (3 chặng theo hệ), Nhận quà tuần.
// - Sân: số làn = số tướng (3–5), chia đều; 3 dải chặng tô màu hệ; vạch đích. Mỗi tướng: chân dung tướng chạy kiểu nhảy cóc (nhún, bóp
//   giãn), tên dưới chân; lao vào đánh (dịch về phía đối thủ), vụt nổ chỗ trúng, choáng (lắc lư, sao xoay trên đầu, tối màu), chữ nổi
//   Choáng! / Vấp! / Né! / Gió thuận!, về đích hiện số hạng. Dòng tường thuật theo sự kiện.
// - Dưới: tướng đang chọn, Chọn tướng, Đua (lệ phí; hết lượt có thưởng là đua tập), Cổ vũ (vòng sáng co về khớp nút: Tuyệt / Tốt / Hụt;
//   Tuyệt có khiên né đòn ngắn).
// - Kết quả: hạng, bi, điểm cúp; bảng xếp hạng cả đoàn (trúng / bị choáng); Đua lại / Xong.
// Mọi vật dựng sẵn trong prefab (5 làn), không sinh lúc chạy.
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
    public sealed class RaceScene : SceneRoot
    {
        [System.Serializable]
        public struct Lane
        {
            public RectTransform token, body, stars, spin; // token: chân tướng trên làn; stars: chỗ sao choáng, spin: vòng sao xoay
            public HeroPortrait portrait;
            public Image face, burst, badge; // face: ảnh chân dung (tối đi khi choáng)
            public TextMeshProUGUI name, pop, badgeText;
            public RectTransform line; // vạch kẻ trên làn (làn đầu không có)
        }

        [SerializeField] SketchButton[] cups;
        [SerializeField] TextMeshProUGUI info, track, talk;
        [SerializeField] SketchButton claim;
        [SerializeField] RectTransform field;
        [SerializeField] Image[] segs;
        [SerializeField] Lane[] lanes;
        [SerializeField] TextMeshProUGUI hero;
        [SerializeField] SketchButton pick, go, cheer;
        [SerializeField] RectTransform cheerRing;
        [SerializeField] TextMeshProUGUI cheerText;
        [SerializeField] GameObject result;
        [SerializeField] TextMeshProUGUI resTitle, resInfo;
        [SerializeField] TextMeshProUGUI[] resRows;
        [SerializeField] SketchButton resAgain, resDone;
        [SerializeField] TeamPickerDialog pickerPrefab;

        public override string Title => Loc.T("Trường đua");
        public override string BackTo => SceneIds.Casino;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static RaceConfig C => D.Cfg.casino.race;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        int cup;
        string mine;
        RaceGame game;
        float acc;
        int evSeen;
        Rng rng;
        const float RingIn = 1.0f, RingWindow = 1.35f, PopSec = 1.1f;
        // diễn theo làn: lao (đích, còn bao lâu), vụt nổ, chữ nổi
        readonly float[] lungeT = new float[5], burstT = new float[5], popT = new float[5];
        readonly Vector2[] lungeDir = new Vector2[5];

        public RaceGame Game => game;

        // Dùng khi dựng prefab (Editor).
        public void Setup(SketchButton[] cupBtns, TextMeshProUGUI infoText, TextMeshProUGUI trackText, TextMeshProUGUI talkText, SketchButton claimBtn,
            RectTransform fieldRt, Image[] segImgs, Lane[] laneList, TextMeshProUGUI heroText, SketchButton pickBtn, SketchButton goBtn, SketchButton cheerBtn,
            RectTransform ring, TextMeshProUGUI ringText, GameObject res, TextMeshProUGUI rTitle, TextMeshProUGUI rInfo, TextMeshProUGUI[] rRows,
            SketchButton rAgain, SketchButton rDone, TeamPickerDialog picker)
        {
            cups = cupBtns; info = infoText; track = trackText; talk = talkText; claim = claimBtn; field = fieldRt; segs = segImgs; lanes = laneList;
            hero = heroText; pick = pickBtn; go = goBtn; cheer = cheerBtn; cheerRing = ring; cheerText = ringText; result = res; resTitle = rTitle;
            resInfo = rInfo; resRows = rRows; resAgain = rAgain; resDone = rDone; pickerPrefab = picker;
        }

        public override void Enter(object args)
        {
            rng = new Rng(Rng.RandomSeed());
            var s = S;
            mine = BestHero();
            cup = Enumerable.Range(0, C.cups.Count).LastOrDefault(i => Race.CupOpen(s, D, i));
            for (int i = 0; i < cups.Length; i++)
            {
                int k = i;
                cups[i].SetOnClick(() => { if (game == null || game.done) { cup = k; Render(); } });
            }
            pick.SetOnClick(PickHero);
            go.SetOnClick(StartRace);
            cheer.SetOnClick(Cheer);
            claim.SetOnClick(ClaimWeek);
            resAgain.SetOnClick(() => { result.SetActive(false); StartRace(); });
            resDone.SetOnClick(() => { result.SetActive(false); game = null; Render(); });
            result.SetActive(false);
            game = null;
            cheerText.text = "";
            talk.text = Loc.T("Chọn tướng rồi bấm Đua. Trên đường các tướng sẽ húc nhau, ai về nhất thì hên!");
            Render();
        }

        public override void Exit()
        {
            if (game == null || game.done || game.fee <= 0) { game = null; return; }
            Race.Run(C, game, null);
            var res = Race.Finish(S, D, game, Now);
            App.Save.Save();
            App.Toasts.Show(Loc.F("Trường đua: về thứ {0}/{1}, +{2} bi", res.place + 1, res.runners, res.balls), Icon("ball"));
            game = null;
        }

        string BestHero()
        {
            var s = S;
            var d = D;
            var tr = Race.TrackOf(C, Casino.Today(Now));
            return d.Heroes.Where(h => !h.minion && s.Hero(h.id)?.owned == true)
                .OrderByDescending(h => tr.Count(t => t == h.elem) * 1000 - tr.Count(t => Elements.Beats(t) == h.elem) * 500 + h.stats[5])
                .Select(h => h.id).FirstOrDefault() ?? s.starter;
        }

        void Render()
        {
            var s = S;
            var d = D;
            double now = Now;
            for (int i = 0; i < cups.Length; i++)
            {
                bool has = i < C.cups.Count;
                cups[i].gameObject.SetActive(has);
                if (!has) continue;
                cups[i].SetText(C.cups[i].Name);
                cups[i].SetRole(i == cup ? BtnColor.Yellow : BtnColor.Paper);
                cups[i].Locked = !Race.CupOpen(s, d, i);
            }
            var tr = Race.TrackOf(C, Casino.Today(now));
            track.text = Loc.F("Đường hôm nay: {0}", string.Join(" · ", tr.Select(Elements.Name)));
            for (int i = 0; i < segs.Length && i < tr.Length; i++) segs[i].color = Color.Lerp(Theme.Of(tr[i]), Theme.Paper, 0.55f);
            int pts = Race.Points(s, d, cup, now);
            int left = Casino.PlaysLeft(s, d, Casino.Race, now);
            double mult = Casino.RaceMult(d, now);
            info.text = Loc.F("Điểm cúp tuần: {0}/{1} · còn {2} lượt có thưởng", pts, C.weekPts, left) +
                        (mult > 1 ? " · " + Loc.F("Lễ Hội Đua ×{0}", mult.ToString("0.#")) : "");
            claim.gameObject.SetActive(Race.WeekReady(s, d, cup, now));
            claim.SetText(Loc.T("Nhận quà tuần"));
            var h = d.Hero(mine);
            hero.text = h != null ? Loc.F("{0} · hệ {1} · tốc {2}", h.name, Elements.Name(h.elem), h.stats[5]) : Loc.T("Chọn một tướng");
            bool racing = game != null && !game.done;
            go.gameObject.SetActive(!racing);
            pick.gameObject.SetActive(!racing);
            cheer.gameObject.SetActive(racing);
            bool open = Race.CupOpen(s, d, cup);
            int fee = Race.Fee(s, d, cup);
            go.SetText(!open ? Loc.F("Mở ở cấp {0}", C.cups[cup].level) : left > 0 ? Loc.F("Đua · {0} bi", fee) : Loc.T("Đua tập"));
            go.Locked = !open || h == null;
            if (game == null) Preview();
        }

        // chưa đua: 4 làn mẫu, tướng của mình ở làn đầu
        void Preview()
        {
            Layout(4);
            var h = D.Hero(mine);
            for (int i = 0; i < lanes.Length; i++)
            {
                var ln = lanes[i];
                ln.token.gameObject.SetActive(i < 4);
                if (i >= 4) continue;
                ln.token.anchoredPosition = new Vector2(60, ln.token.anchoredPosition.y);
                ln.stars.gameObject.SetActive(false);
                ln.burst.gameObject.SetActive(false);
                ln.pop.gameObject.SetActive(false);
                ln.badge.gameObject.SetActive(false);
                var show = i == 0 ? h : Mystery(i);
                ln.portrait.gameObject.SetActive(show != null);
                if (show != null) BindPortrait(ln, show, 4, i > 0);
                ln.name.text = i == 0 && h != null ? h.name : "?";
                ln.name.color = Theme.Ink;
            }
        }

        float LaneH(int n) => field.rect.height / Mathf.Max(1, n);
        float PortraitH(int n) => Mathf.Min(170, LaneH(n) * 0.7f);

        // tướng bí ẩn cho làn mẫu (bóng sẫm), đổi theo ngày
        HeroDef Mystery(int i)
        {
            var list = D.Heroes.Where(x => !x.minion && x.id != mine).ToList();
            return list.Count == 0 ? null : list[(Casino.Today(Now) * 7 + i * 13) % list.Count];
        }

        // chân dung cao theo số làn, chân trùng gốc token; sao choáng trên đầu, vụt nổ giữa thân
        void BindPortrait(Lane ln, HeroDef h, int n, bool silhouette = false)
        {
            float ph = PortraitH(n);
            ln.portrait.Bind(h, ph, silhouette);
            ln.portrait.Rect.anchoredPosition = new Vector2(0, -ph * HeroArt.FootY);
            ln.stars.anchoredPosition = new Vector2(0, ph * 0.95f);
            ln.burst.rectTransform.anchoredPosition = new Vector2(ph * 0.25f, ph * 0.5f);
            ln.badge.rectTransform.anchoredPosition = new Vector2(-ph * 0.5f, ph * 0.55f);
        }

        // chia đều n làn trên sân
        void Layout(int n)
        {
            float fh = field.rect.height, lh = fh / Mathf.Max(1, n);
            for (int i = 0; i < lanes.Length; i++)
            {
                var ln = lanes[i];
                float y = fh / 2 - lh * (i + 0.5f) - lh * 0.28f; // chân tướng hơi dưới giữa làn
                ln.token.anchoredPosition = new Vector2(ln.token.anchoredPosition.x, y);
                if (ln.line)
                {
                    ln.line.gameObject.SetActive(i > 0 && i < n);
                    ln.line.anchoredPosition = new Vector2(0, fh / 2 - lh * i);
                }
            }
        }

        void PickHero()
        {
            if (!pickerPrefab) return;
            var dlg = App.Modals.Open(pickerPrefab);
            dlg.Show(new List<string> { mine }, 1, null, list =>
            {
                if (list != null && list.Count > 0) mine = list[0];
                Render();
            });
        }

        void ClaimWeek()
        {
            var r = Race.ClaimWeek(S, D, cup, Now, rng);
            if (r.Count == 0) return;
            App.Save.Save();
            App.Audio.Play("chest");
            App.Toasts.Show(Loc.T("Quà tuần: ") + CasinoUi.Rewards(r), Icon("star"));
            Render();
        }

        void StartRace()
        {
            var g = Race.Start(S, D, cup, mine, Now, rng, out var why);
            if (g == null)
            {
                App.Toasts.Show(why, Icon("lock"));
                return;
            }
            App.Save.Save();
            game = g;
            acc = 0;
            evSeen = 0;
            for (int i = 0; i < 5; i++) lungeT[i] = burstT[i] = popT[i] = 0;
            int n = g.runners.Count;
            Layout(n);
            var d = D;
            for (int i = 0; i < lanes.Length; i++)
            {
                var ln = lanes[i];
                bool has = i < n;
                ln.token.gameObject.SetActive(has);
                if (!has) continue;
                var r = g.runners[i];
                var h = d.Hero(r.hero);
                ln.portrait.gameObject.SetActive(h != null);
                if (h != null) BindPortrait(ln, h, n);
                ln.name.text = (r.player ? "★ " : "") + (h?.name ?? r.hero);
                ln.name.color = r.player ? Theme.RedD : Theme.Ink;
                ln.stars.gameObject.SetActive(false);
                ln.burst.gameObject.SetActive(false);
                ln.pop.gameObject.SetActive(false);
                ln.badge.gameObject.SetActive(false);
            }
            talk.text = Loc.F("{0} tướng vào vạch xuất phát. Chạy!", n);
            cheerText.text = "";
            App.Audio.Play("whoosh");
            Render();
        }

        void Cheer()
        {
            if (game == null || game.done) return;
            int k = Race.CheerSeg(game);
            if (k < 0) return;
            float t = (float)Race.SinceSegStart(game);
            float err = Mathf.Abs(t - RingIn);
            int q = err < 0.13f ? 2 : err < 0.32f ? 1 : 0;
            Race.Cheer(C, game, q);
            cheerText.text = q == 2 ? Loc.T("Tuyệt! Tăng tốc, né được một cú húc") : q == 1 ? Loc.T("Tốt! Tăng tốc") : Loc.T("Hụt");
            Haptics.Play(q > 0 ? Haptic.UiTap : Haptic.UiError);
            if (q == 2) App.Audio.Play("buff");
        }

        void Update()
        {
            if (game == null || !field) return;
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.1f);
            if (!game.done)
            {
                acc += dt;
                while (acc >= Race.Dt && !game.done)
                {
                    acc -= (float)Race.Dt;
                    if (Race.CheerSeg(game) >= 0 && Race.SinceSegStart(game) > RingWindow) Race.Cheer(C, game, 0);
                    Race.Step(C, game);
                }
                int k = Race.CheerSeg(game);
                cheerRing.gameObject.SetActive(k >= 0);
                if (k >= 0)
                {
                    float t = (float)Race.SinceSegStart(game);
                    float sc = t <= RingIn ? Mathf.Lerp(2.0f, 1.0f, t / RingIn) : 1 - (t - RingIn) * 0.4f;
                    cheerRing.localScale = new Vector3(sc, sc, 1);
                    if (t < 0.05f) cheerText.text = Loc.F("Chặng {0}: chạm khi vòng khớp nút!", k + 1);
                }
            }
            ConsumeEvents();
            Draw(dt);
            if (game.done && !result.activeSelf && evSeen >= game.events.Count) Finish();
        }

        string NameOf(int i) => i >= 0 && i < game.runners.Count ? D.Hero(game.runners[i].hero)?.name ?? game.runners[i].hero : "";

        // sự kiện mới của lõi → diễn trên sân, tường thuật
        void ConsumeEvents()
        {
            for (; evSeen < game.events.Count; evSeen++)
            {
                var e = game.events[evSeen];
                int me = game.PlayerIndex;
                switch (e.kind)
                {
                    case RaceEv.Hit:
                        Lunge(e.a, e.b);
                        if (e.b >= 0 && e.b < 5) burstT[e.b] = 0.38f;
                        Pop(e.b, Loc.T("Choáng!"), Theme.RedD);
                        talk.text = Loc.F("{0} húc {1} choáng váng!", NameOf(e.a), NameOf(e.b));
                        App.Audio.Play("stamp", 0.7f, 1.2f);
                        if (e.b == me) Haptics.Play(Haptic.UiError);
                        else if (e.a == me) Haptics.Play(Haptic.UiTap);
                        break;
                    case RaceEv.Trip:
                        Lunge(e.a, e.b);
                        Pop(e.a, Loc.T("Vấp!"), Theme.Orange);
                        talk.text = Loc.F("{0} lao vào {1} nhưng hụt, vấp ngã!", NameOf(e.a), NameOf(e.b));
                        break;
                    case RaceEv.Dodge:
                        Lunge(e.a, e.b);
                        Pop(e.b, Loc.T("Né!"), Theme.BlueD);
                        Pop(e.a, Loc.T("Vấp!"), Theme.Orange, false);
                        talk.text = Loc.F("{0} né gọn cú húc của {1}!", NameOf(e.b), NameOf(e.a));
                        break;
                    case RaceEv.Gust:
                        Pop(e.a, Loc.T("Gió thuận!"), Theme.GreenD);
                        talk.text = Loc.F("{0} gặp gió thuận, phóng vụt lên!", NameOf(e.a));
                        break;
                    case RaceEv.Finish:
                        int place = Race.Order(game).IndexOf(e.a);
                        if (e.a >= 0 && e.a < 5)
                        {
                            lanes[e.a].badge.gameObject.SetActive(true);
                            lanes[e.a].badge.color = place == 0 ? Theme.Yellow : Theme.Paper2;
                            lanes[e.a].badgeText.text = (place + 1).ToString();
                        }
                        if (place == 0) talk.text = Loc.F("{0} về nhất!", NameOf(e.a));
                        break;
                }
            }
        }

        void Lunge(int a, int b)
        {
            if (a < 0 || a >= 5 || b < 0 || b >= game.runners.Count) return;
            float dx = (float)(game.runners[b].pos - game.runners[a].pos);
            float dy = lanes[b].token.anchoredPosition.y - lanes[a].token.anchoredPosition.y;
            lungeDir[a] = new Vector2(Mathf.Clamp(dx * 3, -60, 60) + Mathf.Sign(dx) * 20, Mathf.Clamp(dy * 0.45f, -70, 70));
            lungeT[a] = 0.28f;
        }

        void Pop(int i, string text, Color c, bool replace = true)
        {
            if (i < 0 || i >= 5) return;
            if (!replace && popT[i] > 0) return;
            var ln = lanes[i];
            ln.pop.text = text;
            ln.pop.color = c;
            bool left = ln.token.anchoredPosition.x > field.rect.width * 0.68f;
            ln.pop.rectTransform.pivot = new Vector2(left ? 1 : 0, 0.5f);
            ln.pop.alignment = left ? TextAlignmentOptions.MidlineRight : TextAlignmentOptions.MidlineLeft;
            popT[i] = PopSec;
        }

        void Draw(float dt)
        {
            float w = field.rect.width;
            float hh = PortraitH(game.runners.Count);
            double len = game.Length(C);
            float tNow = Time.unscaledTime;
            for (int i = 0; i < game.runners.Count && i < lanes.Length; i++)
            {
                var ln = lanes[i];
                var r = game.runners[i];
                bool stunned = r.Stunned(game.t) && r.finishT < 0;
                bool moving = !stunned && r.finishT < 0;
                float x = Mathf.Lerp(70, w - 70, (float)(r.pos / len));
                // lao vào đánh: ra rồi về
                Vector2 lunge = Vector2.zero;
                if (lungeT[i] > 0)
                {
                    lungeT[i] -= dt;
                    float k = Mathf.Sin(Mathf.Clamp01(1 - lungeT[i] / 0.28f) * Mathf.PI);
                    lunge = lungeDir[i] * k;
                }
                ln.token.anchoredPosition = new Vector2(x + lunge.x, ln.token.anchoredPosition.y);
                // nhảy cóc: nhún theo nhịp chạy, bóp giãn lúc chạm đất
                float ph = tNow * 9f + i * 1.7f;
                float hop = moving ? Mathf.Abs(Mathf.Sin(ph)) * 18f : 0;
                float squash = moving ? 1 + (Mathf.Abs(Mathf.Sin(ph)) < 0.25f ? -0.08f : 0.03f) : 1;
                ln.body.anchoredPosition = new Vector2(0, hop + lunge.y);
                ln.body.localScale = new Vector3(2 - squash, squash, 1);
                ln.body.localEulerAngles = new Vector3(0, 0, stunned ? Mathf.Sin(tNow * 18 + i) * 10 : moving ? Mathf.Sin(ph) * 3 : 0);
                if (ln.face) ln.face.color = stunned ? new Color(0.68f, 0.68f, 0.76f) : Color.white;
                // sao choáng xoay trên đầu
                ln.stars.gameObject.SetActive(stunned);
                if (stunned)
                    for (int k = 0; k < ln.spin.childCount; k++)
                    {
                        float a = tNow * 5.5f + k * Mathf.PI * 2 / ln.spin.childCount;
                        var st = (RectTransform)ln.spin.GetChild(k);
                        st.anchoredPosition = new Vector2(Mathf.Cos(a) * hh * 0.32f, Mathf.Sin(a) * hh * 0.11f);
                        float s = 0.75f + 0.3f * Mathf.Sin(a);
                        st.localScale = new Vector3(s, s, 1);
                        st.localEulerAngles = new Vector3(0, 0, tNow * 200f);
                    }
                // vụt nổ chỗ trúng
                if (burstT[i] > 0)
                {
                    burstT[i] -= dt;
                    float k = 1 - burstT[i] / 0.38f;
                    ln.burst.gameObject.SetActive(true);
                    float s = k < 0.4f ? Mathf.Lerp(0.3f, 1.4f, k / 0.4f) : Mathf.Lerp(1.4f, 0.6f, (k - 0.4f) / 0.6f);
                    ln.burst.rectTransform.localScale = new Vector3(s, s, 1);
                    ln.burst.color = new Color(1f, 0.85f, 0.25f, 1 - Mathf.Clamp01((k - 0.5f) * 2));
                }
                else ln.burst.gameObject.SetActive(false);
                // chữ nổi bay lên, mờ dần
                if (popT[i] > 0)
                {
                    popT[i] -= dt;
                    float k = 1 - popT[i] / PopSec;
                    ln.pop.gameObject.SetActive(true);
                    float side = ln.pop.rectTransform.pivot.x > 0.5f ? -1 : 1;
                    ln.pop.rectTransform.anchoredPosition = new Vector2(side * (hh * 0.42f + 6 + k * 10), hh * 0.5f + k * 26);
                    var c = ln.pop.color;
                    ln.pop.color = new Color(c.r, c.g, c.b, 1 - Mathf.Clamp01((k - 0.6f) / 0.4f));
                }
                else ln.pop.gameObject.SetActive(false);
            }
        }

        void Finish()
        {
            var res = Race.Finish(S, D, game, Now);
            App.Save.Save();
            cheerRing.gameObject.SetActive(false);
            cheerText.text = "";
            App.Audio.Play(res.place == 0 ? "win" : "stamp");
            Haptics.Play(res.place == 0 ? Haptic.Win : Haptic.UiTap);
            result.SetActive(true);
            resTitle.text = res.place == 0 ? Loc.T("Về nhất!") : Loc.F("Về thứ {0}/{1}", res.place + 1, res.runners);
            resInfo.text = game.fee <= 0 ? Loc.T("Đua tập: không lệ phí, không thưởng.")
                : Loc.F("+{0} bi · +{1} điểm cúp tuần", res.balls, res.points) + (res.weekReady ? "\n" + Loc.T("Đủ điểm: nhận quà tuần!") : "");
            var order = Race.Order(game);
            for (int i = 0; i < resRows.Length; i++)
            {
                bool has = i < order.Count;
                resRows[i].gameObject.SetActive(has);
                if (!has) continue;
                var r = game.runners[order[i]];
                resRows[i].text = Loc.F("{0}. {1} · húc trúng {2} · bị choáng {3}", i + 1, NameOf(order[i]), r.hits, r.stuns);
                resRows[i].color = r.player ? Theme.RedD : Theme.Ink;
            }
            Render();
        }
    }
}
