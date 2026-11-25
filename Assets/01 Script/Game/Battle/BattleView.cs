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
        readonly List<RectTransform> backs = new List<RectTransform>();
        readonly List<TeamSlot> slots = new List<TeamSlot>();
        readonly List<FoeFace> foes = new List<FoeFace>();
        int[] foeStar; // sao để vẽ mặt từng địch (boss tiến hóa đổi theo dạng đang hiện)
        readonly List<UiCard> dealt = new List<UiCard>(); // thẻ chọn đang hiện (bản sao kit, xoá khi vẽ lại)
        readonly List<QueueTile> flyIdle = new List<QueueTile>();
        readonly List<BattleBanner> bannerIdle = new List<BattleBanner>();
        readonly Dictionary<RectTransform, Coroutine> dealing = new Dictionary<RectTransform, Coroutine>();

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
                tile.Bind(Icon(c.icon), c.name, Theme.Of(c.rarity), Theme.CardFill, false);
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
        // Logic chạy ngay lúc chạm (BattleController gọi Battle.Pick và chia lượt thẻ mới liền), hình đuổi theo: thẻ chọn nhấc lên lấy đà,
        // bay theo cung vào ô của nó, ô bật lên lúc chạm; hai thẻ còn lại chìm xuống. Nhiều thẻ bay cùng lúc được, nên chạm nhanh liên
        // tiếp không bị nuốt. Ô đang chờ thẻ bay tới ẩn tới lúc chạm (landing).

        readonly List<UiCard> flyCardIdle = new List<UiCard>();
        readonly HashSet<int> landing = new HashSet<int>();
        public int Flying { get; private set; } // số thẻ đang bay vào hàng

        // ô qIdx của hàng thẻ sẽ nhận thẻ bay: ẩn tới khi thẻ chạm
        public void HoldTile(int qIdx) => landing.Add(qIdx);

        // chọn thẻ chosen trong lượt thẻ đang hiện: trả về bản sao để bay (nằm trên cùng lớp phủ, gốc ở tâm, đúng chỗ và cỡ thẻ cũ);
        // thẻ cũ tắt, hai thẻ kia chìm xuống rồi xoá
        public RectTransform PickOffer(UiCard chosen)
        {
            RectTransform clone = null;
            if (chosen)
            {
                var from = (RectTransform)chosen.transform;
                var c = chosen.Card;
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
                clone = (RectTransform)fc.transform;
                clone.SetAsLastSibling();
                clone.anchorMin = clone.anchorMax = clone.pivot = new Vector2(0.5f, 0.5f);
                clone.sizeDelta = from.rect.size;
                clone.position = from.TransformPoint(from.rect.center);
                clone.localScale = from.localScale;
                clone.localEulerAngles = from.localEulerAngles;
                StopDeal(from);
                dealt.Remove(chosen);
                OfferCards.Remove(chosen);
                Destroy(chosen.gameObject);
            }
            // hai thẻ không được chọn: thôi bấm được ngay, chìm xuống (nhích lên một chút rồi rơi, co về 0)
            for (int k = dealt.Count - 1; k >= 0; k--)
            {
                var other = dealt[k];
                dealt.RemoveAt(k);
                if (!other) continue;
                OfferCards.Remove(other);
                other.SetInteractable(false);
                var rt = (RectTransform)other.transform;
                StopDeal(rt);
                if (other.TryGetComponent<UiMotion>(out var m)) m.enabled = false;
                StartCoroutine(Discard(rt, k));
            }
            return clone;
        }

        void StopDeal(RectTransform rt)
        {
            if (dealing.TryGetValue(rt, out var co) && co != null) StopCoroutine(co);
            dealing.Remove(rt);
        }

        IEnumerator Discard(RectTransform rt, int i)
        {
            if (!rt) yield break;
            var p0 = rt.anchoredPosition;
            float s0 = rt.localScale.x, r0 = rt.localEulerAngles.z, dir = i % 2 == 0 ? -1 : 1;
            const float len = 0.18f;
            for (float t = 0; t < len; t += Time.unscaledDeltaTime)
            {
                if (!rt) yield break;
                float k = t / len;
                // 0 → 30%: nhích lên, phồng 4%; 30% → hết: rơi xuống, co về 0 (ease-in), nghiêng ra ngoài
                float up = k < 0.3f ? Mathf.Sin(k / 0.3f * Mathf.PI * 0.5f) : 1 - (k - 0.3f) / 0.7f;
                float fall = k < 0.3f ? 0 : Mathf.Pow((k - 0.3f) / 0.7f, 2);
                rt.anchoredPosition = p0 + new Vector2(0, 14 * up - 90 * fall);
                float s = s0 * (k < 0.3f ? 1 + 0.04f * up : Mathf.Lerp(1.04f, 0, fall));
                rt.localScale = new Vector3(s, s, 1);
                rt.localEulerAngles = new Vector3(0, 0, r0 + dir * 8 * fall);
                yield return null;
            }
            if (rt) Destroy(rt.gameObject);
        }

        // bay bản sao clone (từ PickOffer) vào ô qIdx của hàng thẻ: nhấc lên lấy đà 0,07 giây, bay theo cung 0,26 giây (vụt đi rồi chậm
        // lại cắm vào ô), xoay nhẹ; chạm thì ô bật lên (0,8 → 1,22 → 1), tiếng "land" leo cao độ theo lần chọn, rung tay một tích.
        // fallback: chỗ bay tới khi hàng chưa có ô qIdx (thẻ tự chơi)
        public IEnumerator FlyToSlot(RectTransform clone, int qIdx, Vector3 fallback, int pickNo)
        {
            if (!clone) yield break;
            Flying++;
            var parent = (RectTransform)clone.parent;
            Vector2 a = parent.InverseTransformPoint(clone.position);
            float s0 = clone.localScale.x, r0 = clone.localEulerAngles.z;
            if (r0 > 180) r0 -= 360;
            // ô đích dời theo layout trong lúc bay: lấy chỗ của nó mỗi khung
            Vector2 Target()
            {
                var w = qIdx >= 0 && qIdx < tiles.Count && tiles[qIdx] && tiles[qIdx].gameObject.activeInHierarchy ? tiles[qIdx].Card.position : fallback;
                return parent.InverseTransformPoint(w);
            }
            float endScale = 112f / Mathf.Max(1, clone.rect.width);
            const float lift = 0.07f, fly = 0.26f;
            var lifted = a + new Vector2(0, 34);
            for (float t = 0; t < lift; t += Time.unscaledDeltaTime)
            {
                if (!clone) break;
                float k = 1 - Mathf.Pow(1 - t / lift, 3);
                clone.localPosition = Vector2.Lerp(a, lifted, k);
                float s = Mathf.Lerp(s0, 1.1f, k);
                clone.localScale = new Vector3(s, s, 1);
                clone.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(r0, -5, k));
                yield return null;
            }
            for (float t = 0; t < fly && clone; t += Time.unscaledDeltaTime)
            {
                float k = t / fly;
                float e = 1 - Mathf.Pow(1 - k, 2.5f); // ease-out: pha nhấc đã là lấy đà, bay vụt đi rồi chậm lại cắm vào ô
                var z = Target();
                // cung: điểm điều khiển cao hơn đường thẳng (thẻ vồng lên rồi cắm xuống ô)
                var ctrl = (lifted + z) * 0.5f + new Vector2(0, 150);
                float u = 1 - e;
                clone.localPosition = u * u * lifted + 2 * u * e * ctrl + e * e * z;
                float s = Mathf.Lerp(1.1f, endScale, e);
                clone.localScale = new Vector3(s, s, 1);
                clone.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(-5, 0, e) + Mathf.Sin(e * Mathf.PI) * 12);
                yield return null;
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
            Haptics.Play(Haptic.CardLand);
            if (p.qCount) StartCoroutine(Pop(p.qCount.rectTransform, 1, 1.25f, 1, 0.2f, 0));
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
            if (p.reroll) p.reroll.gameObject.SetActive(false);
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
                OfferLabel(t.side == 0 ? Loc.F("{0} ra đòn!", who) : Loc.F("{0} (địch) ra đòn!", who), -120, 70);
                return;
            }
            // số thẻ đổi theo Sổ Phép (2–6): quá bề ngang thì thu nhỏ cả hàng (3 thẻ giữ nguyên chỗ cũ)
            int n = t.offer.Count;
            float w = UiCard.NormalSize.x, gap = 24;
            float sc = Mathf.Min(1, 1010f / Mathf.Max(1, n * w + (n - 1) * gap));
            float step = (w + gap) * sc, x0 = -(n - 1) * step / 2;
            if (p.reroll)
            {
                bool can = !auto && b.CanReroll();
                p.reroll.gameObject.SetActive(can);
                if (can) p.reroll.SetText(Loc.F("Lật trang ×{0}", b.RerollsLeft(0)));
            }
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
                // tiếng chọn do BattleController phát (leo cao độ theo lần chọn); đè ngón thì lún và rung một tích
                card.ClickSound = null;
                card.PressHaptic = !auto;
                var rt = (RectTransform)card.transform;
                rt.Place(new Vector2(0.5f, 1), new Vector2(x0 + i * step, -12), UiCard.NormalSize, new Vector2(0.5f, 1));
                OfferCards.Add(card);
                dealt.Add(card);
                StartDeal(rt, i * 0.05f, sc);
            }
            App.Audio.Play("deal");
        }

        void StartDeal(RectTransform rt, float delay, float fin = 1)
        {
            if (dealing.TryGetValue(rt, out var co) && co != null) StopCoroutine(co);
            dealing[rt] = StartCoroutine(Deal(rt, delay, fin));
        }

        // chia bài (bộ UI Sa Bàn, như deal của Web/src/uikit/fx.ts): bay từ chồng bài dưới giữa lên chỗ, xoay, quá đà rồi đứng;
        // xong thì thẻ nhún tại chỗ, mỗi lá một nhịp (UiMotion.idle)
        IEnumerator Deal(RectTransform rt, float delay, float fin = 1)
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
                float sc = Mathf.Lerp(Mathf.Lerp(0.55f, 1.06f, a), 1, b) * fin;
                rt.localScale = new Vector3(sc, sc, 1);
                rt.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(Mathf.Lerp(-24, 3, a), 0, b));
                yield return null;
            }
            if (!rt) yield break;
            rt.localScale = new Vector3(fin, fin, 1);
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
            OfferLabel(b.phase == Phase.Picking ? Loc.F("{0} đang chọn thẻ...", b.ActiveOf(1).Name) : Loc.T("Địch ra đòn!"), -16, 64);
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
