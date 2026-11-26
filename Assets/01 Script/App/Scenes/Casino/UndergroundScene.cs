// Scene Hầm đấu (Đấu trường ngầm) của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.5; mỗi trò một scene). Prefab Screens/CasinoUnderground
// (menu "PokiClash/Prefab/Đảo Casino/Hầm đấu: dựng scene"). Lõi: Core/Casino/Underground.cs.
// Người dùng 2026-11-26 (lượt 2, chê bản chia hàng "quá cũ"): "tận dụng nhân vật dealer của đảo (nhân vật đen đen); đúng chất 1 đấu trường
// ngầm ở 1 hòn đảo cờ bạc; đội địch hiện thành 3 con lấy thẳng từ animation ra đứng idle, người chơi click / swipe trái phải để chọn; ở
// trên có nhân vật kia đứng, chọn con dễ thì mỉa mai, chọn đội khó thì hỏi có chắc thắng không; gen background đúng kiểu đấu trường
// ngầm, học hỏi cuphead".
// - Sân khấu (dưới Canvas/Nen, rộng 1080, neo mép trên): ảnh nền hầm đấu (ArtGen/Casino/ham_dau), Lão Mực (DealerRig) đứng trong quầy
//   nhà cái trên cao, hai tay tì mép quầy (lớp quầy cắt từ nền che thân dưới), bong bóng thoại cạnh quầy.
// - Biển gỗ treo dưới quầy ghi tên bậc (đã thắng thì đóng dấu). Giữa sàn cát: đội ngầm của bậc đang chọn, mỗi tướng là rig thật
//   (AolaSticker) đứng dáng đứng, tướng chủ lực ở giữa; rig chưa sẵn thì hiện chân dung tĩnh trước. Dưới chân đội: thẻ số tướng + lực
//   chiến (đỏ khi hơn đội mình, xanh khi kém), thẻ luật ngày (chỉ khi có), hàng chip chọn bậc.
// - Chọn bậc: vuốt ngang trên sàn, bấm hai mũi tên hoặc chạm chip; đội cũ lướt ra ngang, đội mới chạy từ cổng sắt dưới quầy ra chỗ đứng
//   (từng con một, nhỏ rồi to dần, nhún một cái). Mỗi lần chọn Lão Mực bình phẩm theo
//   lực chiến đội ngầm so với đội mình (dễ: cười mỉa; cân: gật gù; khó: xoa tay hỏi có chắc thắng; quá khó: giật mình), bậc đã thắng,
//   bậc Nhà Vô Địch; vừa vào và vừa đánh xong cũng có câu riêng. Chỉ diễn và nói, không gạ chơi thêm (GD_Claude/31 mục 1.2).
// - Chạm sàn hoặc biển: hộp chi tiết (cấp, sao từng tướng, luật ngày, thưởng). Bậc không khoá theo cấp người chơi.
// - Cổng sắt dưới quầy (song là lớp rời, trượt lên sau vòm đá) mở khi đội mới ra sân rồi sập lại; khán giả (PitCrowd) nhún nhẹ suốt,
//   reo hò khi đội mới ra và khi Lão Mực phản ứng mạnh (người dùng 2026-11-26 lượt 3).
// - Mỗi ngày chỉ đánh Underground daily trận (thẻ "Còn x/y lượt đánh hôm nay" dưới đồng hồ); hết lượt thì nút Đánh khoá.
// - Dải đáy (khung an toàn): đội của mình (hình tướng, số tướng, lực chiến), Đổi đội, Đánh (lệ phí).
// Đánh: trả lệ phí, sang trận (BattleArgs.ug); kết trận "Về Hầm đấu" quay lại scene này kèm UgReturn (bậc, thắng / thua).
// Mọi vật dựng sẵn trong prefab; lúc chạy chỉ dựng sticker tướng (mỗi khung một cái, như đội hình màn Tướng).
using System;
using System.Collections;
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
    // về lại Hầm đấu sau một trận: chọn sẵn bậc vừa đánh, Lão Mực phản ứng theo kết quả
    public sealed class UgReturn
    {
        public int tier;
        public bool won;
    }

    public sealed class UndergroundScene : SceneRoot
    {
        // ô hình một tướng đội mình: khung tô màu hệ, chân dung cả con phóng vừa ô (FitWhole)
        [Serializable]
        public struct Face
        {
            public GameObject root;
            public Image frame;
            public RectTransform art;
            public HeroPortrait portrait;
        }

        // chỗ đứng một tướng đội ngầm trên sàn: gốc ở chân; body chứa sticker, portrait là chân dung tĩnh hiện trước khi rig sẵn
        [Serializable]
        public struct Spot
        {
            public RectTransform root, body;
            public HeroPortrait portrait;
        }

        [Serializable]
        public struct Chip
        {
            public RectTransform root;
            public Image dot, ring;
            public GameObject won;
            public ClickCatcher click;
        }

        [SerializeField] RectTransform squad;
        [SerializeField] CanvasGroup squadGroup;
        [SerializeField] Spot[] spots;
        [SerializeField] SwipeArea swipe;
        [SerializeField] SketchButton prev, next;
        [SerializeField] Chip[] chips;
        [SerializeField] RectTransform sign;
        [SerializeField] TextMeshProUGUI tierName, wonStamp;
        [SerializeField] ClickCatcher signTap;
        [SerializeField] RectTransform infoTag;
        [SerializeField] TextMeshProUGUI count, power;
        [SerializeField] GameObject ruleTag;
        [SerializeField] TextMeshProUGUI rule;
        [SerializeField] DealerRig dealer;
        [SerializeField] RectTransform bubble;
        [SerializeField] TextMeshProUGUI bubbleText;
        [SerializeField] TextMeshProUGUI clock;
        [SerializeField] Face[] myFaces;
        [SerializeField] TextMeshProUGUI myCount, myPower;
        [SerializeField] SketchButton team, fight;
        [SerializeField] TeamPickerDialog pickerPrefab;
        [Tooltip("Song sắt của cổng (con của khung mặt nạ lòng vòm): trượt lên để mở")]
        [SerializeField] RectTransform gateBars;
        [SerializeField] PitCrowd crowd;
        [SerializeField] TextMeshProUGUI fights;

        public override string Title => Loc.T("Hầm đấu");
        public override string BackTo => SceneIds.Casino;
        // nhạc trận (người dùng 2026-11-26: "lấy luôn nhạc khi combat cho phần này"): vào trận từ đây nhạc chạy liền, không đổi bài
        public override string Music => "tran";

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // chỗ đứng trên sàn (toạ độ sân khấu, gốc mép trên giữa: x, y chân, cao dáng đứng) theo số tướng của đội; tướng chủ lực trước
        static readonly Vector3[][] Stand =
        {
            new[] { new Vector3(0, -1440, 300) },
            new[] { new Vector3(-190, -1440, 280), new Vector3(220, -1330, 240) },
            new[] { new Vector3(0, -1450, 290), new Vector3(-335, -1290, 225), new Vector3(335, -1290, 225) },
        };
        // cổng sắt dưới quầy: đội mới chạy từ đây ra chỗ đứng
        static readonly Vector2 Gate = new Vector2(0, -1030);
        // màu chip theo bậc: Đá, Đồng, Bạc, Vàng, Bạch Kim, Lục Bảo, Kim Cương, Cao Thủ, Đại Cao Thủ, Huyền Thoại; Nhà Vô Địch đỏ
        static readonly string[] TierHex =
            { "#9aa0a6", "#c8824a", "#cfd8e2", "#f2c230", "#e3f1ef", "#3fbf7f", "#7fd4ff", "#e0559a", "#f08a2c", "#9a5bd0" };
        const string ChampHex = "#e8553f";
        // tiếng khán giả (ArtGen/Sfx/ham_dau): ồn ào nền lặp suốt lúc ở trong hầm, reo bùng lên khi đội mới ra / Lão Mực phản ứng mạnh
        const float CrowdHum = 0.3f, CheerVolume = 0.75f, CheerGap = 1.1f;
        const float SlideOut = 0.13f, SlideX = 560, ChipGap = 76, ChipRow = 860;
        // cổng sắt: mở GateOpen giây (song trượt lên hết chiều cao), sập GateShut giây
        const float GateOpen = 0.16f, GateShut = 0.12f;
        // chạy ra từ cổng: mỗi con RunLen giây, con sau trễ RunLag; chờ rig tối đa RigWait rồi mới hiện chân dung tĩnh thay
        const float RunLen = 0.3f, RunLag = 0.07f, RigWait = 0.6f;

        readonly List<int> tiers = new List<int>();
        int cur;
        int day = -1;
        float nextTick, t, dragX;
        bool sliding;
        Coroutine slideCo, bubbleCo;
        readonly AolaSticker[] anim = new AolaSticker[3];
        readonly string[] waitForm = new string[3];
        readonly HeroDef[] heroes = new HeroDef[3];
        readonly float[] heights = new float[3];
        readonly Vector2[] standPos = new Vector2[3];
        int bindFrame;
        float fillTime, gateY;
        bool gateKnown;
        Coroutine gateCo;

        // Dùng khi dựng prefab (Editor).
        public void SetupStage(RectTransform squadRt, CanvasGroup squadCg, Spot[] spotList, SwipeArea swipeArea, SketchButton prevBtn,
            SketchButton nextBtn, Chip[] chipList, RectTransform signRt, TextMeshProUGUI tierText, TextMeshProUGUI wonText, ClickCatcher signClick,
            RectTransform info, TextMeshProUGUI countText, TextMeshProUGUI powerText, GameObject ruleRoot, TextMeshProUGUI ruleText)
        {
            squad = squadRt; squadGroup = squadCg; spots = spotList; swipe = swipeArea; prev = prevBtn; next = nextBtn; chips = chipList;
            sign = signRt; tierName = tierText; wonStamp = wonText; signTap = signClick; infoTag = info; count = countText; power = powerText;
            ruleTag = ruleRoot; rule = ruleText;
        }

        // Dùng khi dựng prefab (Editor).
        public void SetupDealer(DealerRig rig, RectTransform bubbleRt, TextMeshProUGUI bubbleLabel, TextMeshProUGUI clockText)
        {
            dealer = rig; bubble = bubbleRt; bubbleText = bubbleLabel; clock = clockText;
        }

        // Dùng khi dựng prefab (Editor).
        public void SetupMine(Face[] mine, TextMeshProUGUI mineCount, TextMeshProUGUI minePower, SketchButton teamBtn, SketchButton fightBtn,
            TeamPickerDialog picker)
        {
            myFaces = mine; myCount = mineCount; myPower = minePower; team = teamBtn; fight = fightBtn; pickerPrefab = picker;
        }

        // Dùng khi dựng prefab (Editor).
        public void SetupLife(RectTransform bars, PitCrowd pitCrowd, TextMeshProUGUI fightsText)
        {
            gateBars = bars; crowd = pitCrowd; fights = fightsText;
        }

        public override void Enter(object args)
        {
            if (gateBars)
            {
                if (!gateKnown) gateY = gateBars.anchoredPosition.y;
                gateKnown = true;
                gateBars.anchoredPosition = new Vector2(gateBars.anchoredPosition.x, gateY);
            }
            prev.SetOnClick(() => Step(-1));
            next.SetOnClick(() => Step(1));
            team.SetOnClick(PickTeam);
            swipe.Began = () => dragX = 0;
            swipe.Dragged = d => dragX += d.x;
            swipe.Ended = () =>
            {
                if (Mathf.Abs(dragX) > Screen.width * 0.06f) Step(dragX < 0 ? 1 : -1);
            };
            swipe.Tapped = _ => Detail();
            signTap.OnClick = Detail;
            for (int i = 0; i < chips.Length; i++)
            {
                int k = i;
                chips[i].click.OnClick = () => Jump(k);
            }
            bubble.gameObject.SetActive(false);
            squad.anchoredPosition = Vector2.zero;
            squadGroup.alpha = 1;
            sliding = false;
            LoadTiers();
            var back = args as UgReturn;
            cur = back != null && tiers.Contains(back.tier) ? tiers.IndexOf(back.tier) : FirstPick();
            Render();
            FillSquad();
            slideCo = StartCoroutine(RunOut(null));
            StartCoroutine(Welcome(back));
        }

        public override void Exit()
        {
            App.Audio.Loop("pitCrowd", 0);
            ClearSquad();
        }

        // khán giả reo: hình nhảy cao (PitCrowd) + tiếng reo (hai biến thể xen kẽ, không dồn nhau)
        void Cheer(float secs)
        {
            if (crowd) crowd.Cheer(secs);
            if (Time.unscaledTime - lastCheer < CheerGap) return;
            lastCheer = Time.unscaledTime;
            cheerFlip = !cheerFlip;
            App.Audio.Play(cheerFlip ? "pitCheer1" : "pitCheer2", CheerVolume, UnityEngine.Random.Range(0.96f, 1.05f));
        }

        float lastCheer = -10;
        bool cheerFlip;

        void OnDestroy() => ClearSquad();

        public override void Refresh() => Render();

        void LoadTiers()
        {
            double now = Now;
            day = Casino.Today(now);
            tiers.Clear();
            foreach (int i in Underground.TiersToday(D, now))
                if (Underground.Entry(D, i, now) != null) tiers.Add(i);
            cur = Mathf.Clamp(cur, 0, Mathf.Max(0, tiers.Count - 1));
        }

        // bậc mở đầu: bậc cao nhất chưa thắng mà đội ngầm không mạnh hơn đội mình quá 15%; không có thì bậc chưa thắng đầu tiên
        int FirstPick()
        {
            var s = S;
            var d = D;
            double now = Now;
            int mine = MyPower();
            int best = -1, first = -1;
            for (int k = 0; k < tiers.Count; k++)
            {
                if (Underground.WonToday(s, d, tiers[k], now)) continue;
                if (first < 0) first = k;
                if (Underground.Power(d, Underground.Entry(d, tiers[k], now)) <= mine * 1.15f) best = k;
            }
            return best >= 0 ? best : Mathf.Max(0, first);
        }

        void Update()
        {
            t += Mathf.Min(0.05f, Time.unscaledDeltaTime);
            App.Audio.Loop("pitCrowd", CrowdHum);
            for (int i = 0; i < anim.Length; i++) anim[i]?.Show(HeroViewer.Idle, t + i * 0.37f, true, squadGroup.alpha, false, 0);
            if (Time.unscaledTime < nextTick) return;
            nextTick = Time.unscaledTime + 0.5f;
            // qua 0 giờ: đội ngầm đổi, bày lại; không thì chỉ chạy đồng hồ
            double now = Now;
            if (Casino.Today(now) != day)
            {
                LoadTiers();
                Render();
                FillSquad();
                if (slideCo != null) StopCoroutine(slideCo);
                slideCo = StartCoroutine(RunOut(null));
            }
            else Clock(now);
        }

        // dựng sticker đang chờ: không trong khung vừa bày đội (khung chạm), mỗi khung một cái, tướng chủ lực trước
        void LateUpdate()
        {
            if (Time.frameCount <= bindFrame || !AolaSticker.CanBuildNow) return;
            // rig chậm (đang đọc file, gói tải sau chưa về): quá RigWait thì hiện chân dung tĩnh thay cho tới khi rig xong
            bool late = Time.unscaledTime - fillTime > RigWait;
            for (int i = 0; i < waitForm.Length; i++)
                if (waitForm[i] != null && heroes[i] != null && late) spots[i].portrait.gameObject.SetActive(true);
            for (int i = 0; i < waitForm.Length; i++)
            {
                if (waitForm[i] == null) continue;
                if (heroes[i] == null)
                {
                    waitForm[i] = null;
                    continue;
                }
                if (!AolaActor.Ready(waitForm[i])) continue;
                anim[i] = AolaSticker.TryCreate(spots[i].body, heroes[i], waitForm[i], heights[i], true);
                if (anim[i] != null)
                {
                    anim[i].HideShadow();
                    spots[i].portrait.gameObject.SetActive(false);
                }
                waitForm[i] = null;
                return;
            }
        }

        // ---------- vẽ ----------

        UgEntry Entry => tiers.Count == 0 ? null : Underground.Entry(D, tiers[cur], Now);

        void Render()
        {
            var s = S;
            var d = D;
            double now = Now;
            var cfg = d.Cfg.casino.underground;
            Clock(now);
            var e = Entry;
            bool any = e != null;
            sign.gameObject.SetActive(any);
            infoTag.gameObject.SetActive(any);
            prev.gameObject.SetActive(tiers.Count > 1);
            next.gameObject.SetActive(tiers.Count > 1);
            int mine = MyPower();
            int left = Underground.FightsLeft(s, d, now);
            if (fights)
            {
                fights.text = Loc.F("Còn {0}/{1} lượt đánh hôm nay", left, cfg.daily);
                fights.color = left > 0 ? Theme.Ink : Theme.RedD;
            }
            if (any)
            {
                int tier = tiers[cur];
                var tr = cfg.tiers[tier];
                bool won = Underground.WonToday(s, d, tier, now);
                int fee = Underground.Fee(s, d, tier);
                tierName.text = tr.Name;
                wonStamp.gameObject.SetActive(won);
                wonStamp.text = Loc.T("Đã thắng");
                int pw = Underground.Power(d, e);
                count.text = Loc.F("{0} tướng", Underground.Count(e));
                power.text = NumFmt.Short(pw);
                power.color = pw > mine * 1.15f ? Theme.RedD : pw < mine * 0.85f ? Theme.GreenD : Theme.Ink;
                bool ruled = !string.IsNullOrEmpty(e.rule?.kind);
                ruleTag.SetActive(ruled);
                if (ruled) rule.text = Underground.RuleText(e.rule);
                if (won && tr.weekly)
                {
                    fight.SetText(Loc.T("Đã thắng"));
                    fight.SetRole(BtnColor.Paper);
                    fight.Locked = true;
                    fight.SetOnClick(null);
                }
                else if (left <= 0)
                {
                    fight.SetText(Loc.T("Hết lượt hôm nay"));
                    fight.SetRole(BtnColor.Paper);
                    fight.Locked = true;
                    fight.SetOnClick(null);
                }
                else
                {
                    fight.Locked = false;
                    fight.SetText(won ? Loc.F("Đánh lại · {0}", fee) : Loc.F("Đánh · {0} bi", fee));
                    fight.SetRole(won ? BtnColor.Paper : BtnColor.Green);
                    fight.SetOnClick(Fight);
                }
            }
            else
            {
                ruleTag.SetActive(false);
                fight.SetText(Loc.T("Đánh"));
                fight.Locked = true;
                fight.SetOnClick(null);
            }
            // hàng chip: mỗi bậc hôm nay một chip, bậc đang chọn to hơn, bậc đã thắng có sao
            for (int k = 0; k < chips.Length; k++)
            {
                bool on = k < tiers.Count;
                chips[k].root.gameObject.SetActive(on);
                if (!on) continue;
                int tier = tiers[k];
                chips[k].dot.color = Theme.Hex(cfg.tiers[tier].weekly ? ChampHex : TierHex[Mathf.Min(tier, TierHex.Length - 1)]);
                chips[k].ring.color = k == cur ? Theme.Yellow : Theme.Ink;
                chips[k].won.SetActive(Underground.WonToday(s, d, tier, now));
                float sc = k == cur ? 1.45f : 1f;
                chips[k].root.localScale = new Vector3(sc, sc, 1);
                float gap = Mathf.Min(ChipGap, ChipRow / Mathf.Max(1, tiers.Count - 1));
                chips[k].root.anchoredPosition = new Vector2((k - (tiers.Count - 1) / 2f) * gap, chips[k].root.anchoredPosition.y);
            }
            // đội của mình
            var team0 = MyTeam();
            for (int k = 0; k < myFaces.Length; k++) BindFace(myFaces[k], k < team0.Count ? d.Hero(team0[k]) : null, 0);
            myCount.text = Loc.F("{0} tướng", team0.Count);
            myPower.text = NumFmt.Short(mine);
            team.SetText(Loc.T("Đổi đội"));
        }

        void Clock(double now) => clock.text = Loc.F("Đổi đội ngầm sau {0}", ShopUi.Clock(Underground.NextChange(now)));

        static List<string> MyTeam()
        {
            var s = S;
            return s.team.Where(h => s.Hero(h)?.owned == true && D.Hero(h) != null).Take(Progress.TeamSlots(s)).ToList();
        }

        static int MyPower()
        {
            var s = S;
            var d = D;
            return MyTeam().Sum(id => HeroStats.Power(d.Cfg, d.Hero(id), Teams.MemberOf(s, id, d)));
        }

        // star: sao để chọn dạng (0: sao của người chơi); h null thì ẩn ô
        static void BindFace(Face f, HeroDef h, int star)
        {
            f.root.SetActive(h != null);
            if (h == null) return;
            f.frame.color = Color.Lerp(Theme.Of(h.elem), Color.white, 0.45f);
            FitWhole(f.portrait, h, star, f.art.rect.size);
        }

        // cả con vừa ô, tâm phần có hình vào giữa ô (đo theo PortraitBoxes như ô đối thủ của hộp Chuẩn bị trận)
        static void FitWhole(HeroPortrait p, HeroDef h, int star, Vector2 box)
        {
            var c = PortraitBoxes.Of(HeroArt.FormOf(h, star).aola);
            const float aspect = HeroArt.W / (float)HeroArt.H;
            float height = Mathf.Min(box.y / Mathf.Max(0.05f, c.height), box.x / Mathf.Max(0.05f, c.width * aspect)) * 0.96f;
            p.Bind(h, Mathf.Min(height, box.y * 2), false, star);
            var rt = p.Rect;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.pivot = c.center;
            rt.anchoredPosition = Vector2.zero;
        }

        // ---------- đội ngầm trên sàn ----------

        void ClearSquad()
        {
            for (int i = 0; i < anim.Length; i++)
            {
                anim[i]?.Destroy();
                anim[i] = null;
                waitForm[i] = null;
                heroes[i] = null;
            }
        }

        // bày đội của bậc đang chọn: sticker dựng dần ở LateUpdate; tướng chưa nhập rig thì hiện chân dung tĩnh ngay
        void FillSquad()
        {
            ClearSquad();
            var d = D;
            var e = Entry;
            int n = Underground.Count(e);
            var order = new List<UgMember>();
            if (e != null)
            {
                string lead = Underground.Lead(e);
                var list = e.team.Take(n).ToList();
                order.AddRange(list.Where(m => m.hero == lead));
                order.AddRange(list.Where(m => m.hero != lead));
            }
            var stand = Stand[Mathf.Clamp(order.Count, 1, 3) - 1];
            for (int i = 0; i < spots.Length; i++)
            {
                var sp = spots[i];
                var h = i < order.Count ? d.Hero(order[i].hero) : null;
                sp.root.gameObject.SetActive(h != null);
                if (h == null) continue;
                int star = Math.Max(1, order[i].star);
                heroes[i] = h;
                heights[i] = stand[i].z;
                standPos[i] = new Vector2(stand[i].x, stand[i].y);
                sp.root.anchoredPosition = standPos[i];
                sp.root.localScale = Vector3.one;
                string form = HeroArt.FormOf(h, star).aola;
                bool rig = AolaActor.Find(form, out _, out _);
                // chân dung tĩnh (thay rig khi chưa nhập hoặc rig chậm): phần có hình cao ~1,2 dáng đứng, đáy hình ở chân, lật như
                // sticker (đội ngầm nhìn sang trái)
                var c = PortraitBoxes.Of(form);
                sp.portrait.Bind(h, stand[i].z * 1.2f / Mathf.Max(0.2f, c.height), false, star);
                var pr = sp.portrait.Rect;
                pr.anchorMin = pr.anchorMax = new Vector2(0.5f, 0);
                pr.pivot = new Vector2(c.center.x, c.yMin);
                pr.anchoredPosition = Vector2.zero;
                pr.localScale = new Vector3(-1, 1, 1);
                sp.portrait.gameObject.SetActive(!rig);
                if (rig)
                {
                    waitForm[i] = form;
                    AolaActor.Ready(form);
                }
            }
            bindFrame = Time.frameCount;
            fillTime = Time.unscaledTime;
        }

        // đội vừa bày chạy từ cổng sắt ra chỗ đứng: chờ rig dựng xong (tối đa RigWait), rồi từng con nhỏ → to, nhún một cái
        IEnumerator RunOut(Action done)
        {
            sliding = true;
            squad.anchoredPosition = Vector2.zero;
            squadGroup.alpha = 0;
            float t0 = Time.unscaledTime;
            // vừa vào scene: chờ mây chuyển cảnh tan để người chơi thấy đội chạy ra
            while (App.Router.Busy && Time.unscaledTime - t0 < 10) yield return null;
            t0 = Time.unscaledTime;
            fillTime = Mathf.Max(fillTime, t0);
            while (waitForm.Any(w => w != null) && Time.unscaledTime - t0 < RigWait) yield return null;
            int n = heroes.Count(h => h != null);
            // cổng sắt kéo lên, khán giả reo, rồi đội mới lao ra
            if (n > 0)
            {
                yield return MoveGate(true);
                Cheer(1.4f);
            }
            float len = RunLen + RunLag * Mathf.Max(0, n - 1);
            for (float u = 0; u < len; u += Time.unscaledDeltaTime)
            {
                squadGroup.alpha = Mathf.Clamp01(u / 0.08f);
                for (int i = 0; i < spots.Length; i++)
                {
                    if (heroes[i] == null) continue;
                    float a = Mathf.Clamp01((u - i * RunLag) / RunLen);
                    float e = 1 - Mathf.Pow(1 - a, 3);
                    var p = Vector2.LerpUnclamped(Gate, standPos[i], e);
                    p.y += Mathf.Sin(a * Mathf.PI) * 46; // nhún lên giữa đường
                    spots[i].root.anchoredPosition = p;
                    float sc = Mathf.Lerp(0.3f, 1f, e);
                    spots[i].root.localScale = new Vector3(sc, sc, 1);
                }
                yield return null;
            }
            squadGroup.alpha = 1;
            for (int i = 0; i < spots.Length; i++)
            {
                if (heroes[i] == null) continue;
                spots[i].root.anchoredPosition = standPos[i];
                spots[i].root.localScale = Vector3.one;
            }
            sliding = false;
            slideCo = null;
            if (n > 0)
            {
                if (gateCo != null) StopCoroutine(gateCo);
                gateCo = StartCoroutine(MoveGate(false));
            }
            done?.Invoke();
        }

        // song sắt trượt lên sau vòm đá (mở) hoặc sập xuống rồi nảy nhẹ (đóng)
        IEnumerator MoveGate(bool open)
        {
            if (!gateBars) yield break;
            float rise = gateBars.rect.height;
            float from = gateBars.anchoredPosition.y, to = gateY + (open ? rise : 0);
            float len = open ? GateOpen : GateShut;
            App.Audio.Play(open ? "whoosh" : "stamp", open ? 0.5f : 0.6f, open ? 1.25f : 0.8f);
            for (float u = 0; u < len; u += Time.unscaledDeltaTime)
            {
                float a = u / len;
                a = open ? 1 - (1 - a) * (1 - a) : a * a; // mở: chậm dần; sập: nhanh dần
                gateBars.anchoredPosition = new Vector2(gateBars.anchoredPosition.x, Mathf.Lerp(from, to, a));
                yield return null;
            }
            gateBars.anchoredPosition = new Vector2(gateBars.anchoredPosition.x, to);
            if (!open)
            {
                Haptics.Play(Haptic.UiTap);
                // nảy lên một chút rồi nằm yên
                for (float u = 0; u < 0.14f; u += Time.unscaledDeltaTime)
                {
                    float a = u / 0.14f;
                    gateBars.anchoredPosition = new Vector2(gateBars.anchoredPosition.x, to + Mathf.Sin(a * Mathf.PI) * rise * 0.07f);
                    yield return null;
                }
                gateBars.anchoredPosition = new Vector2(gateBars.anchoredPosition.x, to);
                gateCo = null;
            }
        }

        // ---------- chọn bậc ----------

        void Step(int dir)
        {
            if (sliding || tiers.Count < 2) return;
            Go((cur + dir + tiers.Count) % tiers.Count, dir);
        }

        void Jump(int k)
        {
            if (sliding || k == cur || k < 0 || k >= tiers.Count) return;
            Go(k, k > cur ? 1 : -1);
        }

        void Go(int k, int dir)
        {
            SketchButton.Sound?.Invoke("pick");
            Haptics.Play(Haptic.UiTap);
            if (slideCo != null) StopCoroutine(slideCo);
            slideCo = StartCoroutine(Slide(k, dir));
        }

        // đội cũ lướt ra phía ngược hướng vuốt, đội mới chạy từ cổng ra; chữ trên biển gỗ nảy; xong thì Lão Mực bình phẩm
        IEnumerator Slide(int k, int dir)
        {
            sliding = true;
            for (float u = 0; u < SlideOut; u += Time.unscaledDeltaTime)
            {
                float a = u / SlideOut;
                squad.anchoredPosition = new Vector2(-dir * SlideX * a * a, 0);
                squadGroup.alpha = 1 - a;
                yield return null;
            }
            cur = k;
            Render();
            FillSquad();
            StartCoroutine(ChestBox.Pop(sign, 1.12f));
            yield return RunOut(null);
            StartCoroutine(ChestBox.Pop(infoTag, 1.08f));
            Comment();
        }

        // ---------- Lão Mực ----------

        static string Pick(params string[] lines) => lines[UnityEngine.Random.Range(0, lines.Length)];

        IEnumerator Welcome(UgReturn back)
        {
            float t0 = Time.unscaledTime;
            while (App.Router.Busy && Time.unscaledTime - t0 < 10) yield return null;
            yield return new WaitForSecondsRealtime(0.25f);
            if (back == null && Underground.FightsLeft(S, D, Now) <= 0)
                Say(Loc.T("Hôm nay khách đánh đủ rồi. Mai ghé, hầm có lứa đội mới."), "sulk", 3.2f);
            else if (back != null && back.won)
                Say(Pick(Loc.T("Hừ... hên thôi! Lần sau đừng mong."), Loc.T("Thắng thật à?! Cả hầm ồ lên rồi kìa.")), "grumpy", 3f);
            else if (back != null)
                Say(Pick(Loc.T("Khè khè, lệ phí ta giữ nhé!"), Loc.T("Thua rồi à? Về luyện thêm đi, khách.")), "react_lose", 3f);
            else
                Say(Pick(Loc.T("Xuống tới Hầm đấu rồi đấy! Chọn đối thủ đi, khách."), Loc.T("Hôm nay hầm đông vui lắm. Vuốt xem các đội đi.")), "greet", 3.2f);
        }

        // bình phẩm bậc đang chọn theo lực chiến đội ngầm so với đội mình
        void Comment()
        {
            var e = Entry;
            if (e == null) return;
            var s = S;
            var d = D;
            if (Underground.FightsLeft(s, d, Now) <= 0)
            {
                Say(Loc.T("Hôm nay khách đánh đủ rồi. Mai ghé, hầm có lứa đội mới."), "sulk", 2.8f);
                return;
            }
            int tier = tiers[cur];
            var tr = d.Cfg.casino.underground.tiers[tier];
            if (Underground.WonToday(s, d, tier, Now))
            {
                Say(Pick(Loc.T("Đội này khách thắng rồi còn gì. Đánh lại chỉ có quà nhỏ thôi."), Loc.T("Hừ... lại tới trêu đội thua à?")), "react_win_small", 2.8f);
                return;
            }
            if (tr.weekly)
            {
                Say(Loc.T("Nhà Vô Địch của tuần đấy. Thắng nổi thì ta phục!"), "greet", 3f);
                return;
            }
            int mine = MyPower();
            if (mine <= 0) return;
            float r = Underground.Power(d, e) / (float)mine;
            if (r < 0.6f)
                Say(Pick(Loc.T("Chọn đội dễ thế này à? Khè khè!"), Loc.T("Bắt nạt tân binh vui lắm hả, khách?"),
                    Loc.T("Đội này thì ta nhắm mắt cũng đoán được ai thắng.")), "react_lose", 2.8f);
            else if (r < 1.15f)
                Say(Pick(Loc.T("Kèo này cân đấy. Ta thích!"), Loc.T("Ngang tài ngang sức, cả hầm đang ngó kìa.")), "talk", 2.6f);
            else if (r < 2f)
                Say(Pick(Loc.T("Có chắc thắng được không vậy?"), Loc.T("Lệ phí ta không trả lại đâu nhé."), Loc.T("Đội này cứng đấy. Run chưa?")),
                    "bet_watch", 2.8f);
            else
                Say(Pick(Loc.T("Liều thế?! Đội này mạnh gấp mấy lần đội của khách!"), Loc.T("Ô hô, gan to thật... hay là liều?")), "react_win_big", 3f);
        }

        // bong bóng thoại + clip của Lão Mực ("talk" lặp tới khi bong bóng tắt, clip khác chạy một lần rồi tự về dáng đứng)
        void Say(string text, string clip, float secs)
        {
            if (bubbleCo != null) StopCoroutine(bubbleCo);
            bubbleCo = StartCoroutine(SayCo(text, clip, secs));
        }

        IEnumerator SayCo(string text, string clip, float secs)
        {
            bool loop = clip == "talk";
            if (dealer)
            {
                if (loop) dealer.Loop(clip);
                else dealer.Play(clip);
            }
            // Lão Mực cười to, giật mình hay đập quầy thì cả hầm ồ theo
            if (clip == "react_lose" || clip == "react_win_big" || clip == "grumpy") Cheer(1.2f);
            bubbleText.text = text;
            bubble.gameObject.SetActive(true);
            yield return ChestBox.Pop(bubble, 1.08f);
            yield return new WaitForSecondsRealtime(secs);
            bubble.gameObject.SetActive(false);
            if (loop && dealer) dealer.Stop();
            bubbleCo = null;
        }

        // ---------- thao tác ----------

        static string ItemText(CasinoItem it)
        {
            switch (it.k)
            {
                case "evo": return Loc.F("{0} đá tiến hóa", it.n);
                case "stones": return Loc.F("{0} đá tiềm năng", it.n);
                case "crystal": return Loc.F("{0} đá tinh", it.n);
                case "balls": return Loc.F("{0} bi", it.n);
                default: return it.n + " " + it.k;
            }
        }

        // chạm sàn / biển: phần không bày trên sân (cấp, sao từng tướng, luật ngày, thưởng)
        void Detail()
        {
            if (sliding) return;
            var e = Entry;
            if (e == null) return;
            var s = S;
            var d = D;
            var cfg = d.Cfg.casino.underground;
            int tier = tiers[cur];
            var tr = cfg.tiers[tier];
            var sb = new System.Text.StringBuilder();
            foreach (var m in e.team.Take(Underground.Count(e)))
                sb.AppendLine(Loc.F("{0} cấp {1}, {2} sao", d.Hero(m.hero)?.name ?? m.hero, m.level, m.star));
            sb.AppendLine().AppendLine(Loc.F("Luật hôm nay: {0}", Underground.RuleText(e.rule)));
            var lead = d.Hero(Underground.Lead(e));
            string reward = Loc.F("Thắng lần đầu: {0} bi + {1} mảnh {2}", Mathf.RoundToInt((float)(Underground.Fee(s, d, tier) * cfg.winMult)), tr.shards, lead?.name ?? "");
            if (tr.items.Count > 0) reward += " + " + string.Join(" + ", tr.items.Select(ItemText));
            sb.AppendLine().AppendLine(reward);
            sb.Append(Loc.T("Thắng lại trong ngày: hoàn lệ phí và quà nhỏ. Thua: mất lệ phí."));
            App.Modals.Alert($"{tr.Name} · {e.Name}", sb.ToString(), Loc.T("Đóng"));
        }

        void Fight()
        {
            if (sliding) return;
            var s = S;
            var d = D;
            var e = Entry;
            if (e == null)
            {
                Render();
                return;
            }
            int tier = tiers[cur];
            var mine = MyTeam();
            if (mine.Count == 0)
            {
                PickTeam();
                return;
            }
            if (!Underground.Pay(s, d, tier, Now, out var why))
            {
                App.Audio.Play("error");
                App.Toasts.Show(why, Icon("lock"));
                return;
            }
            App.Save.Save();
            var list = mine.Take(Underground.TeamLimit(e)).ToList();
            App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = 90000 + tier, team = list, ug = new UgRef { tier = tier, day = Casino.Today(Now) } });
        }

        void PickTeam()
        {
            if (!pickerPrefab) return;
            var s = S;
            var d = D;
            var e = Entry;
            var dlg = App.Modals.Open(pickerPrefab);
            dlg.Show(MyTeam(), Progress.TeamSlots(s), e != null ? d.Hero(Underground.Lead(e)) : null, list =>
            {
                if (list != null && list.Count > 0)
                {
                    s.team = list;
                    App.Save.Save();
                }
                Render();
            });
        }

        // ---------- cho lượt chụp ----------

        public void StepForTest(int dir) => Step(dir);
        public void JumpForTest(int k) => Jump(k);
        public bool SquadReady => !sliding && waitForm.All(w => w == null);
        public bool Sliding => sliding;
        public void FightForTest() => Fight();
    }
}
