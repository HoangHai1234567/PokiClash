// Giao diện trận (chép bố cục Web/src/view/battle/battleScreen.ts + battle.css, khung 540 × 960 nhân 2):
// thanh trên (tạm dừng, hiệp, nhãn lượt, Tự chơi), sân đấu, bảng thông tin hai bên, hàng mặt địch góc trên trái sân,
// bảng dưới (hàng thẻ 5 ô + ô đòn kết, 3 thẻ để chọn, chân dung đội, nút Chiêu và Tuyệt kỹ), lớp phủ (băng rôn, VS, gợi ý).
// Chỉ vẽ; BattleController quyết định khi nào vẽ lại và nối nút bấm.
// Dựng sẵn trong prefab màn hình Screens/Battle; ô hàng thẻ, ô trống, lá úp, ô đồng đội, mặt địch, băng rôn là prefab mục (dùng lại, thừa thì tắt).
using System;
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BattleView : MonoBehaviour
    {
        public const float TopH = 112, PanelH = 880;

        [Serializable]
        public struct Parts
        {
            public StageView stage;
            public RectTransform overlay, offer, qRow, qHead, bottom;
            // thanh trên
            public TextMeshProUGUI roundLbl, turnLbl;
            public Image turnChip;
            public SketchButton autoBtn, pauseBtn;
            // bảng thông tin: 0 phe mình, 1 địch
            public BattlePlate[] plates;
            // hàng mặt địch ở góc trên trái sân (dựng sẵn, trong lớp bảng của sân) và ô mặt (prefab mục Items/TranMatDich)
            public RectTransform foeRow;
            public FoeFace foePrefab;
            // đầu hàng thẻ
            public Image qIcon;
            public TextMeshProUGUI qTitle, qCount;
            // hàng thẻ: ô thẻ, ô trống (prefab mục), mũi tên và ô đòn kết (dựng sẵn, cuối hàng)
            public QueueTile tilePrefab, finTile;
            public RectTransform emptyPrefab, arrow;
            // thẻ chọn: dòng chữ (dựng sẵn), lá úp của địch (prefab mục)
            public TextMeshProUGUI offerLabel;
            public RectTransform backPrefab;
            // hàng dưới: ô đồng đội (prefab mục), Chiêu, Tuyệt kỹ (dựng sẵn)
            public TeamSlot slotPrefab;
            public InnateButton skill, ult;
            // lớp phủ: màn VS, dải tuyệt kỹ (dựng sẵn), băng rôn (prefab mục)
            public BattleIntro intro;
            public UltCutIn ultCut;
            public BattleBanner bannerPrefab;
        }

        [SerializeField] Parts p;

        public StageView Stage => p.stage;
        public RectTransform Overlay => p.overlay;
        public RectTransform Offer => p.offer;
        public RectTransform QRow => p.qRow;
        public SketchButton AutoBtn => p.autoBtn;
        public SketchButton PauseBtn => p.pauseBtn;
        public BattleIntro Intro => p.intro;
        public UltCutIn UltCut => p.ultCut;
        Battle b;
        GameData d;

        public Action<int, RectTransform> OnPickCard; // chỉ số thẻ, hình thẻ
        public Action<InnateKind, RectTransform> OnInnate;
        public Action<int> OnSwap;

        readonly List<QueueTile> tiles = new List<QueueTile>();
        readonly List<RectTransform> empties = new List<RectTransform>();
        readonly List<RectTransform> backs = new List<RectTransform>();
        readonly List<TeamSlot> slots = new List<TeamSlot>();
        readonly List<FoeFace> foes = new List<FoeFace>();
        int[] foeStar; // sao để vẽ mặt từng địch (boss tiến hóa đổi theo dạng đang hiện)
        readonly List<UiCard> dealt = new List<UiCard>(); // thẻ chọn đang hiện (bản sao kit, xoá khi vẽ lại)
        readonly List<QueueTile> flyIdle = new List<QueueTile>();
        readonly List<BattleBanner> bannerIdle = new List<BattleBanner>();
        readonly Dictionary<RectTransform, Coroutine> dealing = new Dictionary<RectTransform, Coroutine>();
        UiCard flyCard;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        // ---------- bắt đầu trận ----------

        // stage: ải trên đảo (chọn sàn đấu theo ải); null với thử thách huy hiệu, hang
        public void Init(Battle battle, ZoneDef zone, StageDef stage = null)
        {
            b = battle;
            d = battle.Data;
            p.stage.Init(zone, stage);
            // mặt địch ở góc trên trái thay chấm đội dự bị của bảng địch
            p.plates[1].ShowBench = !p.foeRow || !p.foePrefab;
            var en = b.sides[1].fighters;
            foeStar = new int[en.Count];
            for (int i = 0; i < en.Count; i++) foeStar[i] = Teams.LookStar(d.Cfg, en[i]);
            RenderFoes(null);
        }

        // hàng mặt địch theo ảnh chụp của sự kiện (gục thì có dấu X đúng lúc màn diễn); null: đầu trận
        void RenderFoes(Snap s)
        {
            if (!p.foeRow || !p.foePrefab || foeStar == null) return;
            var en = b.sides[1].fighters;
            int act = s != null ? s.active[1] : b.sides[1].active;
            for (int i = 0; i < en.Count; i++)
            {
                if (i >= foes.Count) foes.Add(Ui.Spawn(p.foePrefab, p.foeRow));
                foes[i].gameObject.SetActive(true);
                bool dead = s != null && i < s.f[1].Count ? s.f[1][i].dead : en[i].dead;
                foes[i].Bind(en[i].hero, foeStar[i], i, i == act, dead);
            }
            for (int k = en.Count; k < foes.Count; k++) foes[k].gameObject.SetActive(false);
        }

        // boss lên dạng sau: mặt đổi theo (ảnh chụp kế tiếp vẽ lại)
        public void SetFoeForm(int i, int form)
        {
            if (foeStar != null && i >= 0 && i < foeStar.Length) foeStar[i] = Teams.FormStar(d.Cfg, form);
        }

        public void FillPlate(int side) => p.plates[side].Fill(b.ActiveOf(side));
        public void SetPlateName(int side, string n) => p.plates[side].SetName(n);

        public void ApplySnap(Snap s)
        {
            for (int side = 0; side < 2; side++)
            {
                var f = s.f[side][s.active[side]];
                p.plates[side].Apply(s, side, d.Cfg);
                Stage.SetStatuses(side, f.st);
            }
            RenderFoes(s);
        }

        // ---------- thanh trên ----------

        public void SetRound(int r) => p.roundLbl.text = $"Hiệp {r}";

        public void SetTurn(int side)
        {
            p.turnLbl.text = side == 0 ? "Lượt bạn" : "Lượt địch";
            p.turnChip.color = side == 0 ? Theme.Green : Theme.Red;
        }

        public void SetAuto(bool on)
        {
            AutoBtn.SetText(on ? "Đang tự chơi" : "Tự chơi");
            AutoBtn.SetColor(on ? Theme.Green : Theme.Paper);
            AutoBtn.Label.color = on ? Color.white : Theme.Ink;
        }

        // ---------- hàng thẻ ----------

        Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // execIdx: ô đang chạy (-1 = chưa chạy; = số ô = đòn kết)
        public void RenderQueue(int execIdx, bool picking)
        {
            var t = b.turn;
            bool mine = t.side == 0;
            p.qHead.gameObject.SetActive(true);
            p.qIcon.sprite = Icon(mine ? "cards" : "skull");
            p.qTitle.text = mine ? "Hàng thẻ của bạn" : $"Hàng thẻ của {b.ActiveOf(1).Name}";
            p.qCount.text = picking ? $"Chọn {t.picksTotal - t.picksLeft + 1}/{t.picksTotal}" : "Ra đòn!";

            NowTile = null;
            int i = 0;
            foreach (var q in t.queue)
            {
                var c = d.Card(q.card);
                var tile = Tile(i);
                tile.Bind(Icon(c.icon), c.name, Theme.Of(c.rarity), Theme.CardFill, false);
                tile.transform.SetAsLastSibling();
                if (i < execIdx) tile.Done();
                if (i == execIdx) Now(tile);
                i++;
            }
            for (int k = i; k < tiles.Count; k++) tiles[k].gameObject.SetActive(false);
            EmptyTiles.Clear();
            int e = 0;
            // hàng chỉ có thẻ chung (chiêu ra ngay), ô trống = số lần chọn còn lại
            for (int k = t.queue.Count; k < t.picksTotal; k++)
            {
                var slot = Empty(e++);
                slot.SetAsLastSibling();
                EmptyTiles.Add(slot);
            }
            for (int k = e; k < empties.Count; k++) empties[k].gameObject.SetActive(false);
            p.arrow.gameObject.SetActive(true);
            p.arrow.SetAsLastSibling();
            var ult = t.ult != null ? d.Card(t.ult.card) : null;
            var fin = p.finTile;
            fin.gameObject.SetActive(true);
            fin.Bind(Icon(ult != null ? ult.icon : t.stunned ? "bolt" : "fist"), ult != null ? ult.name : t.stunned ? "Choáng" : "Đánh thường",
                Theme.Paper3, ult != null ? Theme.Hex("#ffd3e6") : Theme.Hex("#ffe3d8"), false, 128);
            fin.transform.SetAsLastSibling();
            if (execIdx >= t.queue.Count) Now(fin);
        }

        public readonly List<RectTransform> EmptyTiles = new List<RectTransform>();
        public RectTransform NowTile { get; private set; }

        QueueTile Tile(int i)
        {
            if (i >= tiles.Count) tiles.Add(Ui.Spawn(p.tilePrefab, p.qRow));
            tiles[i].gameObject.SetActive(true);
            return tiles[i];
        }

        RectTransform Empty(int i)
        {
            if (i >= empties.Count)
            {
                var e = Ui.Spawn(p.emptyPrefab, p.qRow);
                e.name = "o_trong";
                empties.Add(e);
            }
            empties[i].gameObject.SetActive(true);
            return empties[i];
        }

        void Now(QueueTile tile)
        {
            tile.Now();
            NowTile = tile.Rect;
        }

        // ô bay từ hàng thẻ lên đầu tướng: bản sao hình của ô from, nằm trên cùng lớp phủ
        public QueueTile TakeFlyTile(QueueTile from)
        {
            QueueTile f = null;
            while (flyIdle.Count > 0 && !f)
            {
                f = flyIdle[flyIdle.Count - 1];
                flyIdle.RemoveAt(flyIdle.Count - 1);
            }
            if (f) f.gameObject.SetActive(true);
            else f = Ui.Spawn(p.tilePrefab, p.overlay);
            f.transform.SetAsLastSibling();
            f.CopyFrom(from);
            return f;
        }

        public void ReleaseFlyTile(QueueTile f)
        {
            if (!f) return;
            f.gameObject.SetActive(false);
            flyIdle.Add(f);
        }

        // thẻ bay từ ô chọn xuống hàng thẻ: thẻ kit dùng lại, gán theo thẻ from
        public RectTransform TakeFlyCard(UiCard from)
        {
            var c = from.Card;
            if (!flyCard) flyCard = UiCard.Create(p.overlay, c, 1, false, Icon(c.icon));
            else
            {
                flyCard.gameObject.SetActive(true);
                flyCard.Bind(c, 1, Icon(c.icon));
            }
            flyCard.transform.SetAsLastSibling();
            var rt = (RectTransform)flyCard.transform;
            rt.pivot = ((RectTransform)from.transform).pivot; // như bản chép thẻ cũ: giữ gốc của thẻ chọn (giữa mép trên)
            rt.localEulerAngles = Vector3.zero;
            return rt;
        }

        public void ReleaseFlyCard()
        {
            if (flyCard) flyCard.gameObject.SetActive(false);
        }

        // ---------- 3 thẻ chọn ----------

        public readonly List<UiCard> OfferCards = new List<UiCard>();

        // xoá mọi thứ trong ô thẻ chọn (như xoá hết con của Offer)
        void ClearOffer()
        {
            foreach (var c in dealt)
                if (c)
                    Destroy(c.gameObject);
            dealt.Clear();
            foreach (var bk in backs) bk.gameObject.SetActive(false);
            p.offerLabel.gameObject.SetActive(false);
        }

        void OfferLabel(string text, float y, float h)
        {
            var lbl = p.offerLabel;
            lbl.gameObject.SetActive(true);
            lbl.text = text;
            lbl.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, y), new Vector2(1000, h), new Vector2(0.5f, 1));
        }

        public void RenderOffer(bool auto)
        {
            var t = b.turn;
            ClearOffer();
            OfferCards.Clear();
            BackCards.Clear();
            if (t.side != 0 || b.phase != Phase.Picking)
            {
                if (b.phase == Phase.Over) return;
                string who = b.ActiveOf(t.side).Name;
                OfferLabel(t.side == 0 ? $"{who} ra đòn!" : $"{who} (địch) ra đòn!", -120, 70);
                return;
            }
            float x0 = -(3 * UiCard.NormalSize.x + 2 * 24) / 2 + UiCard.NormalSize.x / 2;
            for (int i = 0; i < t.offer.Count; i++)
            {
                int idx = i;
                UiCard card = null;
                card = UiCard.Create(p.offer, d.Card(t.offer[i]), 1, false, Icon(d.Card(t.offer[i]).icon), null,
                    auto ? (Action)null : () =>
                    {
                        // thôi nhún khi thẻ được chọn (thẻ bay vào hàng)
                        if (card.TryGetComponent<UiMotion>(out var mm)) mm.idle = false;
                        OnPickCard?.Invoke(idx, (RectTransform)card.transform);
                    });
                var rt = (RectTransform)card.transform;
                rt.Place(new Vector2(0.5f, 1), new Vector2(x0 + i * (UiCard.NormalSize.x + 24), -12), UiCard.NormalSize, new Vector2(0.5f, 1));
                OfferCards.Add(card);
                dealt.Add(card);
                StartDeal(rt, i * 0.05f);
            }
            App.Audio.Play("deal");
        }

        void StartDeal(RectTransform rt, float delay)
        {
            if (dealing.TryGetValue(rt, out var co) && co != null) StopCoroutine(co);
            dealing[rt] = StartCoroutine(Deal(rt, delay));
        }

        // chia bài (bộ UI Sa Bàn, như deal của Web/src/uikit/fx.ts): bay từ chồng bài dưới giữa lên chỗ, xoay, quá đà rồi đứng;
        // xong thì thẻ nhún tại chỗ, mỗi lá một nhịp (UiMotion.idle)
        IEnumerator Deal(RectTransform rt, float delay)
        {
            var target = rt.anchoredPosition;
            var from = new Vector2(-target.x * 0.6f, -520);
            rt.localScale = Vector3.zero;
            yield return new WaitForSecondsRealtime(delay);
            const float len = 0.5f;
            for (float t = 0; t < len; t += Time.unscaledDeltaTime)
            {
                if (!rt) yield break;
                float k = t / len;
                // 0 → 70%: tới quá đà (cao hơn 28, xoay 3 độ, phóng 1,06); 70% → hết: về chỗ
                float a = k < 0.7f ? 1 - Mathf.Pow(1 - k / 0.7f, 3) : 1;
                float b = k < 0.7f ? 0 : 1 - Mathf.Pow(1 - (k - 0.7f) / 0.3f, 3);
                var over = target + new Vector2(0, 28);
                rt.anchoredPosition = Vector2.Lerp(Vector2.LerpUnclamped(target + from, over, a), target, b);
                float sc = Mathf.Lerp(Mathf.Lerp(0.55f, 1.06f, a), 1, b);
                rt.localScale = new Vector3(sc, sc, 1);
                rt.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(Mathf.Lerp(-24, 3, a), 0, b));
                yield return null;
            }
            if (!rt) yield break;
            rt.localScale = Vector3.one;
            rt.anchoredPosition = target;
            rt.localEulerAngles = Vector3.zero;
            dealing.Remove(rt);
            var m = PokiClash.UI.UiMotion.Of(rt);
            m.idleLift = 8;
            m.idleTilt = 1;
            m.idlePeriod = 3.4f;
            m.idle = true;
        }

        // lượt địch: lá úp chia một lần mỗi lượt; các lần sau chỉ trả lá vừa chọn về chỗ
        public readonly List<RectTransform> BackCards = new List<RectTransform>();

        public void RenderFoeThinking()
        {
            var t = b.turn;
            if (b.phase == Phase.Picking && BackCards.Count > 0 && BackCards[0])
            {
                foreach (var c in BackCards)
                {
                    c.anchoredPosition = new Vector2(c.anchoredPosition.x, -90);
                    c.localEulerAngles = Vector3.zero;
                }
                return;
            }
            ClearOffer();
            BackCards.Clear();
            OfferLabel(b.phase == Phase.Picking ? $"{b.ActiveOf(1).Name} đang chọn thẻ..." : "Địch ra đòn!", -16, 64);
            if (b.phase != Phase.Picking) return;
            for (int i = 0; i < t.offer.Count; i++)
            {
                var rt = Back(i);
                rt.SetAsLastSibling();
                rt.localEulerAngles = Vector3.zero;
                rt.Place(new Vector2(0.5f, 1), new Vector2((i - (t.offer.Count - 1) / 2f) * 248, -90), new Vector2(224, 312), new Vector2(0.5f, 1));
                BackCards.Add(rt);
                StartDeal(rt, i * 0.06f);
            }
        }

        RectTransform Back(int i)
        {
            if (i >= backs.Count)
            {
                var bk = Ui.Spawn(p.backPrefab, p.offer);
                bk.name = "la_up";
                backs.Add(bk);
            }
            backs[i].gameObject.SetActive(true);
            return backs[i];
        }

        // ---------- hàng dưới: chân dung đội, Chiêu, Tuyệt kỹ ----------

        readonly List<RectTransform> wobbling = new List<RectTransform>();
        readonly List<RectTransform> pulsing = new List<RectTransform>();
        public RectTransform SkillBtn { get; private set; }
        public RectTransform UltBtn { get; private set; }

        public void RenderBottom(bool auto)
        {
            wobbling.Clear();
            pulsing.Clear();
            var side = b.sides[0];
            var t = b.turn;
            bool myTurn = t.side == 0 && b.phase == Phase.Picking && !auto;
            int i = 0;
            for (; i < side.fighters.Count; i++)
            {
                var f = side.fighters[i];
                int idx = i;
                bool can = myTurn && b.CanSwap(i);
                bool act = i == side.active;
                var slot = Slot(i);
                slot.transform.SetAsLastSibling();
                slot.Bind(f, i, act, () => OnSwap?.Invoke(idx));
                if (can) wobbling.Add(slot.Rect);
            }
            for (int k = i; k < slots.Count; k++) slots[k].gameObject.SetActive(false);
            var me = b.ActiveOf(0);
            foreach (var which in new[] { InnateKind.Skill, InnateKind.Ult })
            {
                var (card, lv) = b.InnateCard(me, which);
                string why = t.side == 0 ? b.InnateBlock(which) : "Lượt địch";
                bool used = which == InnateKind.Skill ? t.side == 0 && t.skillUsed : t.side == 0 && t.ult != null;
                bool ready = why == "" && myTurn;
                var btn = which == InnateKind.Ult ? p.ult : p.skill;
                btn.gameObject.SetActive(true);
                btn.transform.SetAsLastSibling();
                var w = which;
                var rt = btn.Rect;
                btn.Bind(card, Icon(card.icon), used, why, ready, me.rage, () => OnInnate?.Invoke(w, rt));
                if (ready) pulsing.Add(rt);
                if (which == InnateKind.Skill) SkillBtn = rt;
                else UltBtn = rt;
            }
        }

        TeamSlot Slot(int i)
        {
            if (i >= slots.Count) slots.Add(Ui.Spawn(p.slotPrefab, p.bottom));
            slots[i].gameObject.SetActive(true);
            return slots[i];
        }

        void Update()
        {
            float t = Time.unscaledTime;
            foreach (var w in wobbling)
                if (w) w.localEulerAngles = new Vector3(0, 0, Mathf.Sin(t * Mathf.PI * 2 / 1.2f) * 2.5f);
            foreach (var pr in pulsing)
                if (pr)
                {
                    float s = 1 + 0.04f * (0.5f - 0.5f * Mathf.Cos(t * Mathf.PI * 2));
                    pr.localScale = new Vector3(s, s, 1);
                }
        }

        // rung khi bấm nút không dùng được
        public IEnumerator Shake(RectTransform rt)
        {
            var basePos = rt.anchoredPosition;
            for (float t = 0; t < 0.45f; t += Time.unscaledDeltaTime)
            {
                if (!rt) yield break;
                float k = t / 0.45f;
                rt.anchoredPosition = basePos + new Vector2(Mathf.Sin(k * Mathf.PI * 8) * 10 * (1 - k), 0);
                yield return null;
            }
            if (rt) rt.anchoredPosition = basePos;
        }

        // ---------- lớp phủ: băng rôn ----------

        // băng rôn đang tắt (thiếu thì sinh), đặt trên cùng lớp phủ
        public BattleBanner TakeBanner()
        {
            BattleBanner bn = null;
            while (bannerIdle.Count > 0 && !bn)
            {
                bn = bannerIdle[bannerIdle.Count - 1];
                bannerIdle.RemoveAt(bannerIdle.Count - 1);
            }
            if (bn) bn.gameObject.SetActive(true);
            else bn = Ui.Spawn(p.bannerPrefab, p.overlay);
            bn.transform.SetAsLastSibling();
            return bn;
        }

        public void ReleaseBanner(BattleBanner bn)
        {
            if (!bn) return;
            bn.gameObject.SetActive(false);
            bannerIdle.Add(bn);
        }
    }
}
