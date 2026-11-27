// Giao diện trận (chép bố cục Web/src/view/battle/battleScreen.ts + battle.css, khung 540 × 960 nhân 2):
// thanh trên (tạm dừng, hiệp, nhãn lượt, Tự chơi), sân đấu, bảng thông tin hai bên, hàng mặt địch góc trên trái sân,
// bảng dưới (hàng thẻ 5 ô + ô đòn kết, bộ bài tráo và 3 thẻ để chọn, chân dung đội, nút Chiêu và Tuyệt kỹ), lớp phủ (băng rôn, VS, gợi ý).
// Bộ bài (DraftDeck, 2026-11-25): tráo chờ lượt, tới lượt rút thì chia 3 lá bay ra lật mặt, chọn xong hai lá còn lại về bộ tráo lại.
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
            // thẻ chọn: dòng chữ (dựng sẵn), lá úp của bộ bài tráo (prefab mục)
            public TextMeshProUGUI offerLabel;
            public RectTransform backPrefab;
            // Sổ Phép "Lật Trang": nút đổi cả bộ thẻ ở đầu hàng thẻ, cạnh chip "Chọn" (menu Editor SoPhepMenu vá vào Screens/Battle)
            public SketchButton reroll;
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
        public Action OnReroll;

        readonly List<QueueTile> tiles = new List<QueueTile>();
        readonly List<RectTransform> empties = new List<RectTransform>();
        readonly List<TeamSlot> slots = new List<TeamSlot>();
        readonly List<FoeFace> foes = new List<FoeFace>();
        int[] foeStar; // sao để vẽ mặt từng địch (boss tiến hóa đổi theo dạng đang hiện)
        readonly List<UiCard> dealt = new List<UiCard>(); // thẻ chọn đang hiện (bản sao kit, xoá khi vẽ lại)
        readonly List<QueueTile> flyIdle = new List<QueueTile>();
        readonly List<BattleBanner> bannerIdle = new List<BattleBanner>();

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        // ---------- bắt đầu trận ----------

        // stage: ải trên đảo (chọn sàn đấu theo ải); null với thử thách huy hiệu, hang
        public void Init(Battle battle, ZoneDef zone, StageDef stage = null)
        {
            b = battle;
            d = battle.Data;
            p.stage.Init(zone, stage);
            // thanh máu dâng (FillHp): trận mới thì quên tướng ra sân, việc dâng dở của trận trước
            for (int i = 0; i < 2; i++)
            {
                lastActive[i] = -1;
                fillCo[i] = nudgeCo[i] = null;
            }
            if (plateScale == null) plateScale = new[] { p.plates[0].Rect.localScale, p.plates[1].Rect.localScale };
            else
                for (int i = 0; i < 2; i++) p.plates[i].Rect.localScale = plateScale[i];
            // mặt địch ở góc trên trái thay chấm đội dự bị của bảng địch
            p.plates[1].ShowBench = !p.foeRow || !p.foePrefab;
            var en = b.sides[1].fighters;
            foeStar = new int[en.Count];
            for (int i = 0; i < en.Count; i++) foeStar[i] = Teams.LookStar(d.Cfg, en[i]);
            RenderFoes(null);
            if (p.reroll)
            {
                p.reroll.SetOnClick(() => OnReroll?.Invoke());
                p.reroll.gameObject.SetActive(false);
            }
            // bộ bài: dựng lần đầu (lớp bộ, lớp viền độ hiếm, lớp lá bay trong ô thẻ chọn), trận mới thì về nguyên
            deck = DraftDeck.Ensure(p.offer, p.backPrefab, DeckAt, p.qRow);
            deck.ResetAll();
            foreach (var c in dealt)
                if (c)
                    Destroy(c.gameObject);
            dealt.Clear();
            OfferCards.Clear();
            revealed.Clear();
            offerClick.Clear();
            offerTurn = null;
            offerSig = null;
            p.offerLabel.gameObject.SetActive(false);
            // trận trước bị thoát giữa lúc thẻ đang bay (coroutine bị dừng): không để đếm thẻ bay kẹt
            Flying = 0;
            landing.Clear();
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
                bool changed = lastActive[side] != s.active[side]; // đầu trận, đổi tướng: thanh máu dâng từ 0 thay vì tụt (vệt vàng như mất máu)
                lastActive[side] = s.active[side];
                if (fillCo[side] != null)
                {
                    // đang dâng: ảnh chụp mới thành đích, thanh máu giữ nhịp dâng (ghi đè ngay trong khung này, chữ không nháy)
                    fillTo[side] = s;
                    p.plates[side].Apply(s, side, d.Cfg);
                    HoldFill(side);
                }
                else if (changed && !f.dead && f.hp > 0) FillHp(side, s, 0.5f);
                else p.plates[side].Apply(s, side, d.Cfg);
                Stage.SetStatuses(side, f.st);
            }
            RenderFoes(s);
        }

        // ---------- thanh máu dâng có nhịp (2026-11-17) ----------
        // Boss tiến hóa, hồi sinh, đầu trận, tướng mới vào sân: thanh máu dâng từ `from` (phần máu tối đa) tới máu trong ảnh chụp trong
        // dur giây, nhanh rồi chậm, số chạy theo; xong thì bảng nảy nhẹ. Giá trị đầu đặt tức thì để vệt vàng lùi chậm của UiBar không hiện
        // như mất máu. Bảng (BattlePlate) vẫn vẽ mana, nộ, chip như thường; chỉ thanh máu do đây lái.

        readonly UiBar[] hpBars = new UiBar[2];
        readonly Coroutine[] fillCo = new Coroutine[2];
        readonly Snap[] fillTo = new Snap[2];
        readonly float[] fillShown = new float[2];
        readonly int[] lastActive = { -1, -1 };

        UiBar HpBar(int side)
        {
            if (!hpBars[side] && p.plates != null && side < p.plates.Length && p.plates[side])
                foreach (var bar in p.plates[side].GetComponentsInChildren<UiBar>(true))
                    if (bar.Type == UiBar.Kind.Hp)
                    {
                        hpBars[side] = bar;
                        break;
                    }
            return hpBars[side];
        }

        static string HpText(double v, FSnap f) => $"{NumFmt.Short(v)}/{NumFmt.Short(f.maxHp)}{(f.shield > 0 ? Loc.F(" +{0} khiên", NumFmt.Short(f.shield)) : "")}";

        public void FillHp(int side, Snap to, float dur, float from = 0)
        {
            if (to == null || !isActiveAndEnabled) return;
            if (fillCo[side] != null) StopCoroutine(fillCo[side]);
            fillTo[side] = to;
            fillCo[side] = StartCoroutine(Fill(side, dur, from));
        }

        // giữ thanh máu ở giá trị đang dâng (sau khi bảng vẽ ảnh chụp mới)
        void HoldFill(int side)
        {
            var bar = HpBar(side);
            var s = fillTo[side];
            if (!bar || s == null) return;
            var f = s.f[side][s.active[side]];
            bar.Set(fillShown[side], (float)f.maxHp, (float)f.shield, HpText(fillShown[side], f));
        }

        IEnumerator Fill(int side, float dur, float from)
        {
            var s0 = fillTo[side];
            var f0 = s0.f[side][s0.active[side]];
            p.plates[side].Apply(s0, side, d.Cfg);
            var bar = HpBar(side);
            if (!bar)
            {
                fillCo[side] = null;
                yield break;
            }
            fillShown[side] = from * (float)f0.maxHp;
            bar.Set(fillShown[side], (float)f0.maxHp, (float)f0.shield, HpText(fillShown[side], f0), true);
            for (float t = 0; t < dur; t += Time.unscaledDeltaTime)
            {
                var s = fillTo[side];
                var f = s.f[side][s.active[side]];
                float k = t / dur, e = 1 - (1 - k) * (1 - k) * (1 - k);
                fillShown[side] = Mathf.Lerp(from * (float)f.maxHp, (float)f.hp, e);
                HoldFill(side);
                yield return null;
            }
            fillCo[side] = null;
            p.plates[side].Apply(fillTo[side], side, d.Cfg);
            if (nudgeCo[side] != null) StopCoroutine(nudgeCo[side]);
            nudgeCo[side] = StartCoroutine(Nudge(p.plates[side].Rect, plateScale[side], 1.05f, 0.22f));
        }

        readonly Coroutine[] nudgeCo = new Coroutine[2];
        Vector3[] plateScale; // cỡ gốc của hai bảng (lấy lúc vào trận)

        // nảy cỡ quanh cỡ gốc s0 (không đụng góc xoay của bảng)
        static IEnumerator Nudge(RectTransform rt, Vector3 s0, float peak, float len)
        {
            if (!rt) yield break;
            for (float t = 0; t < len; t += Time.unscaledDeltaTime)
            {
                if (!rt) yield break;
                float k = t / len, s = k < 0.4f ? Mathf.Lerp(1, peak, k / 0.4f) : Mathf.Lerp(peak, 1, Mathf.SmoothStep(0, 1, (k - 0.4f) / 0.6f));
                rt.localScale = s0 * s;
                yield return null;
            }
            if (rt) rt.localScale = s0;
        }

        // ---------- thanh trên ----------

        public void SetRound(int r)
        {
            p.roundLbl.text = Loc.F("Hiệp {0}", r);
            Bump(p.roundLbl.rectTransform, 2);
        }

        public void SetTurn(int side)
        {
            p.turnLbl.text = side == 0 ? Loc.T("Lượt bạn") : Loc.T("Lượt địch");
            p.turnChip.color = side == 0 ? Theme.Green : Theme.Red;
            Bump(p.turnChip.rectTransform, 3); // đổi lượt: nhãn nảy một cái (trước chỉ đổi chữ, dễ lỡ)
        }

        // nảy cỡ một mục của thanh trên (lấy cỡ gốc lần đầu, không cộng dồn khi nảy liền nhau)
        readonly Coroutine[] bumpCo = new Coroutine[4];
        readonly Vector3[] bumpBase = new Vector3[4];

        void Bump(RectTransform rt, int slot)
        {
            if (!rt || !isActiveAndEnabled) return;
            if (bumpCo[slot] != null) StopCoroutine(bumpCo[slot]);
            else bumpBase[slot] = rt.localScale;
            bumpCo[slot] = StartCoroutine(BumpRun(rt, slot));
        }

        IEnumerator BumpRun(RectTransform rt, int slot)
        {
            yield return Nudge(rt, bumpBase[slot], 1.14f, 0.24f);
            bumpCo[slot] = null;
        }

        public void SetAuto(bool on)
        {
            AutoBtn.SetText(on ? Loc.T("Đang tự chơi") : Loc.T("Tự chơi"));
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
            p.qTitle.text = mine ? Loc.T("Hàng thẻ của bạn") : Loc.F("Hàng thẻ của {0}", b.ActiveOf(1).Name);
            p.qCount.text = picking ? Loc.F("Chọn {0}/{1}", t.picksTotal - t.picksLeft + 1, t.picksTotal) : Loc.T("Ra đòn!");

            if (execIdx >= 0) landing.Clear(); // đã ra đòn: không còn ô nào chờ thẻ bay
            NowTile = null;
            nowTile = null;
            if (popNow != null)
            {
                StopCoroutine(popNow);
                popNow = null;
            }
            int i = 0;
            foreach (var q in t.queue)
            {
                var c = d.Card(q.card);
                var tile = Tile(i);
                var tranh = App.Art ? App.Art.CardArt(c.id) : null; // thẻ chung có tranh (GD_Claude/36): ô hàng thẻ dùng đúng tranh như thẻ chọn
                tile.Bind(tranh ? tranh : Icon(c.icon), c.name, Theme.Of(c.rarity), Theme.CardFill, false);
                tile.transform.SetAsLastSibling();
                if (i < execIdx) tile.Done();
                if (i == execIdx) Now(tile);
                if (landing.Contains(i)) tile.Card.localScale = Vector3.zero; // thẻ đang bay tới ô này: ô hiện khi thẻ chạm
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
            fin.Bind(Icon(ult != null ? ult.icon : t.stunned ? "bolt" : "fist"), ult != null ? ult.name : t.stunned ? CardText.StatusLabel(StatusId.Stun) : Loc.T("Đánh thường"),
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
            nowTile = tile;
        }

        QueueTile nowTile;
        Coroutine popNow;

        // ô đang chạy bật lên (1 → 1,32 → 1,15) lúc thẻ của nó ra đòn
        public void PopNow()
        {
            if (!nowTile) return;
            if (popNow != null) StopCoroutine(popNow);
            popNow = StartCoroutine(Pop(nowTile.Card, 1, 1.32f, 1.15f, 0.2f, 3));
        }

        // nảy scale from → peak → to trong len giây thật (GameFeel 4.7: pha lên 65% ease-out, pha về 35%), xoay nhẹ rot độ rồi về rot cuối
        static IEnumerator Pop(RectTransform rt, float from, float peak, float to, float len, float rotEnd, float rot0 = 0)
        {
            for (float t = 0; t < len; t += Time.unscaledDeltaTime)
            {
                if (!rt) yield break;
                float k = t / len;
                float s = k < 0.65f ? Mathf.Lerp(from, peak, 1 - Mathf.Pow(1 - k / 0.65f, 3)) : Mathf.Lerp(peak, to, Mathf.SmoothStep(0, 1, (k - 0.65f) / 0.35f));
                rt.localScale = new Vector3(s, s, 1);
                rt.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(rot0, rotEnd, k));
                yield return null;
            }
            if (!rt) yield break;
            rt.localScale = new Vector3(to, to, 1);
            rt.localEulerAngles = new Vector3(0, 0, rotEnd);
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

        // ---------- thẻ được chọn bay vào hàng (GameFeel 2.4, 6.2, 6.5; 2026-11-16) ----------
        // Logic chạy ngay lúc chạm (BattleController gọi Battle.Pick liền), hình đuổi theo: thẻ chọn nhấc lên lấy đà, bay theo cung vào ô
        // của nó, ô bật lên lúc chạm; hai thẻ còn lại lật úp bay về bộ bài (2026-11-25, trước đó chìm xuống), bộ tráo lại rồi chia lượt
        // thẻ mới. Ô đang chờ thẻ bay tới ẩn tới lúc chạm (landing).

        readonly List<UiCard> flyCardIdle = new List<UiCard>();
        readonly HashSet<int> landing = new HashSet<int>();
        public int Flying { get; private set; } // số thẻ đang bay vào hàng

        // ô qIdx của hàng thẻ sẽ nhận thẻ bay: ẩn tới khi thẻ chạm
        public void HoldTile(int qIdx) => landing.Add(qIdx);

        // chọn thẻ chosen trong lượt thẻ đang hiện: trả về bản sao để bay (nằm trên cùng lớp phủ, gốc ở tâm, đúng chỗ và cỡ thẻ cũ);
        // thẻ cũ tắt (viền độ hiếm bung ra tại chỗ), hai thẻ kia lật úp bay về bộ bài
        public RectTransform PickOffer(UiCard chosen)
        {
            RectTransform clone = null;
            if (chosen)
            {
                var from = (RectTransform)chosen.transform;
                clone = (RectTransform)TakeFlyCard(chosen.Card).transform;
                clone.sizeDelta = from.rect.size;
                clone.position = from.TransformPoint(from.rect.center);
                clone.localScale = from.localScale;
                clone.localEulerAngles = from.localEulerAngles;
                if (deck) deck.Picked(chosen);
                dealt.Remove(chosen);
                OfferCards.Remove(chosen);
                revealed.Remove(chosen);
                offerClick.Remove(chosen);
                Destroy(chosen.gameObject);
            }
            // hai thẻ không được chọn: thôi bấm được ngay, lật úp bay về bộ bài
            ReturnOffer();
            return clone;
        }

        // bản sao thẻ để bay (kho dùng lại), trên cùng lớp phủ, gốc ở tâm
        UiCard TakeFlyCard(CardDef c)
        {
            UiCard fc = null;
            while (flyCardIdle.Count > 0 && !fc)
            {
                fc = flyCardIdle[flyCardIdle.Count - 1];
                flyCardIdle.RemoveAt(flyCardIdle.Count - 1);
            }
            if (fc)
            {
                fc.gameObject.SetActive(true);
                fc.Bind(c, 1, Icon(c.icon));
            }
            else fc = UiCard.Create(p.overlay, c, 1, false, Icon(c.icon));
            var rt = (RectTransform)fc.transform;
            rt.SetAsLastSibling();
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = UiCard.NormalSize;
            rt.localEulerAngles = Vector3.zero;
            return fc;
        }

        // địch chọn (2026-11-25): lá trên đỉnh bộ bài nhấc lên dựng đứng, bay vào ô qIdx của hàng thẻ địch, lật ra mặt giữa đường
        // (FlyToSlot có lá úp). Đếm vào Flying ngay từ lúc nhấc để lượt địch chờ lá cuối chạm hàng rồi mới ra đòn.
        public IEnumerator FoeDraw(string cardId, int qIdx, int pickNo)
        {
            var c = d.Card(cardId);
            if (c == null) yield break;
            var clone = (RectTransform)TakeFlyCard(c).transform;
            RectTransform back = null;
            if (deck)
            {
                var top = deck.TopPose(true);
                float s = top.scale / Mathf.Max(1e-4f, p.overlay.lossyScale.x);
                clone.position = top.pos;
                clone.localScale = new Vector3(0, s, 1);
                back = deck.TakeBack(p.overlay);
                back.position = top.pos;
                back.rotation = top.q;
                back.localScale = new Vector3(s, s, 1);
                Flying++;
                yield return deck.Lift(back, 0.12f);
                Flying--;
                if (!clone) yield break;
                if (back)
                {
                    clone.position = back.position;
                    clone.localScale = new Vector3(0, back.localScale.y, 1);
                }
            }
            else
            {
                clone.position = p.offer.TransformPoint(p.offer.rect.center);
                clone.localScale = new Vector3(0.6f, 0.6f, 1);
            }
            var fallback = EmptyTiles.Count > 0 && EmptyTiles[0] ? EmptyTiles[0].position : clone.position;
            yield return FlyToSlot(clone, qIdx, fallback, pickNo, back, true);
        }

        // bay bản sao clone (từ PickOffer, FoeDraw) vào ô qIdx của hàng thẻ: nhấc lên lấy đà 0,07 giây, bay theo cung 0,26 giây (vụt đi
        // rồi chậm lại cắm vào ô), xoay nhẹ; chạm thì ô bật lên (0,8 → 1,22 → 1), tiếng "land" leo cao độ theo lần chọn, rung tay một tích
        // (trừ lá của địch). back: lá úp bay cùng, lật ra mặt thẻ trong 0,02 → 0,22 giây đầu (lá địch rút từ bộ bài).
        // fallback: chỗ bay tới khi hàng chưa có ô qIdx (thẻ tự chơi)
        public IEnumerator FlyToSlot(RectTransform clone, int qIdx, Vector3 fallback, int pickNo, RectTransform back = null, bool foe = false)
        {
            if (!clone) yield break;
            Flying++;
            var parent = (RectTransform)clone.parent;
            Vector2 a = parent.InverseTransformPoint(clone.position);
            float s0 = clone.localScale.y, r0 = clone.localEulerAngles.z;
            if (r0 > 180) r0 -= 360;
            float tt = 0; // thời gian từ lúc nhấc (cho lật)
            // lật: nửa đầu lá úp co ngang về 0 (mặt thẻ ẩn), nửa sau mặt thẻ nở ra
            float FlipX(float s)
            {
                if (!back && tt > 0.25f) return 1;
                float f = Mathf.Clamp01((tt - 0.02f) / 0.2f);
                if (f < 0.5f && back)
                {
                    back.localPosition = clone.localPosition;
                    back.localEulerAngles = clone.localEulerAngles;
                    back.localScale = new Vector3(s * Mathf.Cos(f * Mathf.PI), s, 1);
                    return 0;
                }
                if (back)
                {
                    if (deck) deck.ReleaseBack(back);
                    else back.gameObject.SetActive(false);
                    back = null;
                }
                return f >= 1 ? 1 : -Mathf.Cos(f * Mathf.PI);
            }
            bool flips = back;
            // ô đích dời theo layout trong lúc bay: lấy chỗ của nó mỗi khung
            Vector2 Target()
            {
                var w = qIdx >= 0 && qIdx < tiles.Count && tiles[qIdx] && tiles[qIdx].gameObject.activeInHierarchy ? tiles[qIdx].Card.position : fallback;
                return parent.InverseTransformPoint(w);
            }
            float endScale = 112f / Mathf.Max(1, clone.rect.width);
            float liftTo = flips ? 0.9f : 1.1f; // lá rút từ bộ (nhỏ) nhấc tới cỡ vừa rồi lao vào ô
            const float lift = 0.07f, fly = 0.26f;
            var lifted = a + new Vector2(0, 34);
            for (float t = 0; t < lift; t += Time.unscaledDeltaTime, tt += Time.unscaledDeltaTime)
            {
                if (!clone) break;
                float k = 1 - Mathf.Pow(1 - t / lift, 3);
                clone.localPosition = Vector2.Lerp(a, lifted, k);
                clone.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(r0, -5, k));
                float s = Mathf.Lerp(s0, liftTo, k);
                clone.localScale = new Vector3(s * (flips ? FlipX(s) : 1), s, 1);
                yield return null;
            }
            for (float t = 0; t < fly && clone; t += Time.unscaledDeltaTime, tt += Time.unscaledDeltaTime)
            {
                float k = t / fly;
                float e = 1 - Mathf.Pow(1 - k, 2.5f); // ease-out: pha nhấc đã là lấy đà, bay vụt đi rồi chậm lại cắm vào ô
                var z = Target();
                // cung: điểm điều khiển cao hơn đường thẳng (thẻ vồng lên rồi cắm xuống ô)
                var ctrl = (lifted + z) * 0.5f + new Vector2(0, 150);
                float u = 1 - e;
                clone.localPosition = u * u * lifted + 2 * u * e * ctrl + e * e * z;
                clone.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(-5, 0, e) + Mathf.Sin(e * Mathf.PI) * 12);
                float s = Mathf.Lerp(liftTo, endScale, e);
                clone.localScale = new Vector3(s * (flips ? FlipX(s) : 1), s, 1);
                yield return null;
            }
            if (back)
            {
                if (deck) deck.ReleaseBack(back);
                else back.gameObject.SetActive(false);
            }
            if (clone)
            {
                clone.gameObject.SetActive(false);
                if (clone.TryGetComponent<UiCard>(out var fc)) flyCardIdle.Add(fc);
            }
            Flying--;
            landing.Remove(qIdx);
            if (qIdx >= 0 && qIdx < tiles.Count && tiles[qIdx] && tiles[qIdx].gameObject.activeInHierarchy)
                StartCoroutine(Pop(tiles[qIdx].Card, 0.8f, 1.22f, 1, 0.22f, 0, -8)); // từ cỡ bản sao lúc chạm (không chớp mất), nảy rồi đứng
            App.Audio.Play("land", 0.9f, BattlePlayer.Semitone(BattlePlayer.Pent(pickNo)));
            if (!foe) Haptics.Play(Haptic.CardLand);
            if (p.qCount) StartCoroutine(Pop(p.qCount.rectTransform, 1, 1.25f, 1, 0.2f, 0));
        }

        // ---------- bộ bài và thẻ chọn (DraftDeck, người dùng 2026-11-25) ----------
        // Lượt thẻ mới (tên lượt, số lần chọn còn, số Lật trang còn, các thẻ) thì chia lại: thẻ cũ về bộ, bộ tráo, 3 lá bay ra lật mặt.
        // Vẽ lại cùng lượt thẻ (đổi tướng đầu lượt, bật / tắt tự chơi) thì giữ thẻ, chỉ đổi bấm được. Thẻ bấm được khi đã lật xong.

        public readonly List<UiCard> OfferCards = new List<UiCard>();
        readonly HashSet<UiCard> revealed = new HashSet<UiCard>();
        readonly Dictionary<UiCard, Action> offerClick = new Dictionary<UiCard, Action>();
        DraftDeck deck;
        Turn offerTurn;
        string offerSig;
        bool offerAuto;
        static readonly Vector2 DeckAt = new Vector2(0, -12 - 232); // giữa ô thẻ chọn (thẻ đặt ở y −12, cao 464): lá giữa che bộ bài

        // bộ bài đang tráo / chia, thẻ chưa lật đủ (chưa chọn được)
        public bool Dealing => deck && deck.Busy;

        // nhịp bộ bài: địch, tự chơi nhanh hơn; công cụ thử chạy nhanh thì nhanh theo
        float DeckSpeed(bool quick) => (quick ? 1.35f : 1f) * Mathf.Max(1, p.stage ? p.stage.fast : 1);

        // thẻ đang hiện về bộ bài (lá đã lật thì lật úp giữa đường bay về, lá đang chia thì lá úp quay về)
        void ReturnOffer()
        {
            foreach (var c in dealt)
                if (c)
                {
                    if (deck) deck.Return(c);
                    else Destroy(c.gameObject);
                }
            dealt.Clear();
            OfferCards.Clear();
            revealed.Clear();
            offerClick.Clear();
        }

        // dòng chữ ở đầu ô (bộ bài nằm giữa ô, dưới dòng chữ)
        void OfferLabel(string text)
        {
            var lbl = p.offerLabel;
            lbl.gameObject.SetActive(true);
            lbl.text = text;
            lbl.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, -16), new Vector2(1000, 64), new Vector2(0.5f, 1));
        }

        public void RenderOffer(bool auto)
        {
            var t = b.turn;
            offerAuto = auto;
            if (t.side != 0 || b.phase != Phase.Picking)
            {
                ReturnOffer();
                offerTurn = null;
                offerSig = null;
                if (p.reroll) p.reroll.gameObject.SetActive(false);
                if (b.phase == Phase.Over)
                {
                    p.offerLabel.gameObject.SetActive(false);
                    if (deck)
                    {
                        deck.Loop(false);
                        deck.Show(false);
                    }
                    return;
                }
                string who = b.ActiveOf(t.side).Name;
                OfferLabel(t.side == 0 ? Loc.F("{0} ra đòn!", who) : Loc.F("{0} (địch) ra đòn!", who));
                // hai bên ra đòn: bộ bài tráo chậm, không tiếng, chờ lượt rút sau
                if (deck)
                {
                    deck.Speed = DeckSpeed(false);
                    deck.Show(true);
                    deck.Loop(true);
                }
                return;
            }
            string sig = t.picksLeft + "|" + b.RerollsLeft(0) + "|" + string.Join(",", t.offer);
            if (ReferenceEquals(t, offerTurn) && sig == offerSig && dealt.Count > 0)
            {
                foreach (var c in dealt)
                    if (c && revealed.Contains(c) && offerClick.TryGetValue(c, out var click))
                        c.SetClick(auto ? null : click);
                ShowReroll();
                return;
            }
            offerTurn = t;
            offerSig = sig;
            ReturnOffer();
            p.offerLabel.gameObject.SetActive(false);
            if (p.reroll) p.reroll.gameObject.SetActive(false);
            // số thẻ đổi theo Sổ Phép (2–6): quá bề ngang thì thu nhỏ cả hàng (3 thẻ giữ nguyên chỗ cũ)
            int n = t.offer.Count;
            float w = UiCard.NormalSize.x, gap = 24;
            float sc = Mathf.Min(1, 1010f / Mathf.Max(1, n * w + (n - 1) * gap));
            float step = (w + gap) * sc, x0 = -(n - 1) * step / 2;
            for (int i = 0; i < n; i++)
            {
                int idx = i;
                var cd = d.Card(t.offer[i]);
                var card = UiCard.Create(p.offer, cd, 1, false, Icon(cd.icon));
                // tiếng chọn do BattleController phát (leo cao độ theo lần chọn); đè ngón thì lún và rung một tích
                card.ClickSound = null;
                card.PressHaptic = true;
                offerClick[card] = () =>
                {
                    if (card.TryGetComponent<UiMotion>(out var mm)) mm.idle = false; // thôi nhún khi thẻ được chọn (thẻ bay vào hàng)
                    OnPickCard?.Invoke(idx, (RectTransform)card.transform);
                };
                var rt = (RectTransform)card.transform;
                rt.Place(new Vector2(0.5f, 1), new Vector2(x0 + i * step, -12), UiCard.NormalSize, new Vector2(0.5f, 1));
                rt.localScale = new Vector3(sc, sc, 1);
                OfferCards.Add(card);
                dealt.Add(card);
            }
            if (deck)
            {
                deck.Speed = DeckSpeed(auto);
                deck.Deal(dealt, Revealed, ShowReroll);
            }
            else
                foreach (var c in dealt)
                    Revealed(c);
        }

        // một thẻ lật xong: bấm được (trừ lúc tự chơi), nhún tại chỗ, mỗi lá một nhịp (UiMotion.idle)
        void Revealed(UiCard card)
        {
            if (!card) return;
            revealed.Add(card);
            if (!offerAuto && offerClick.TryGetValue(card, out var click)) card.SetClick(click);
            var m = UiMotion.Of(card);
            m.enabled = true;
            m.idleLift = 8;
            m.idleTilt = 1;
            m.idlePeriod = 3.4f;
            m.idle = true;
        }

        // nút Lật trang (Sổ Phép) hiện khi thẻ đã lật đủ
        void ShowReroll()
        {
            if (!p.reroll) return;
            bool can = !offerAuto && !Dealing && b.phase == Phase.Picking && b.turn.side == 0 && b.CanReroll();
            p.reroll.gameObject.SetActive(can);
            if (can) p.reroll.SetText(Loc.F("Lật trang ×{0}", b.RerollsLeft(0)));
        }

        // lượt địch: bộ bài tráo nhanh; mỗi lần địch chọn, lá trên đỉnh bay vào hàng thẻ của địch (FoeDraw)
        public void RenderFoeThinking()
        {
            ReturnOffer();
            offerTurn = null;
            offerSig = null;
            if (p.reroll) p.reroll.gameObject.SetActive(false);
            bool picking = b.phase == Phase.Picking;
            OfferLabel(picking ? Loc.F("{0} đang chọn thẻ...", b.ActiveOf(1).Name) : Loc.T("Địch ra đòn!"));
            if (!deck) return;
            deck.Speed = DeckSpeed(true);
            deck.Show(true);
            if (picking) deck.Loop(true, 0.75f, 0.08f);
            else deck.Loop(true);
        }

        // chờ bộ bài tráo xong vòng đang dở (địch rút lá trên đỉnh lúc bộ đã vuông)
        public IEnumerator DeckReady()
        {
            if (deck) yield return deck.WaitSquare(0.6f);
        }

        // ---------- hàng dưới: chân dung đội, Chiêu, Tuyệt kỹ ----------

        readonly List<RectTransform> wobbling = new List<RectTransform>();
        readonly List<RectTransform> pulsing = new List<RectTransform>();
        readonly bool[] wasReady = new bool[2]; // Chiêu, Tuyệt kỹ đã dùng được ở lần vẽ trước
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
                string why = t.side == 0 ? b.InnateBlock(which) : Loc.T("Lượt địch");
                bool used = which == InnateKind.Skill ? t.side == 0 && t.skillUsed : t.side == 0 && t.ult != null;
                bool ready = why == "" && myTurn;
                var btn = which == InnateKind.Ult ? p.ult : p.skill;
                btn.gameObject.SetActive(true);
                btn.transform.SetAsLastSibling();
                var w = which;
                var rt = btn.Rect;
                btn.Bind(card, Icon(card.icon), used, why, ready, me.rage, () => OnInnate?.Invoke(w, rt));
                if (ready) pulsing.Add(rt);
                // vừa chuyển sang dùng được: icon bật lên, tiếng "keng", rung một tích
                int wi = which == InnateKind.Skill ? 0 : 1;
                if (ready && !wasReady[wi])
                {
                    btn.PopReady();
                    App.Audio.Play("coin", 0.55f, wi == 0 ? 1f : 1.12f);
                    Haptics.Play(Haptic.CardLand);
                }
                wasReady[wi] = ready;
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
