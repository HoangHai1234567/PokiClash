// Bộ bài tráo ở ô chọn thẻ của trận (người dùng 2026-11-25): bộ 10 lá úp nằm trên mặt bàn giữa ô chọn thẻ, nhìn chéo từ trên xuống.
// - Góc nhìn 3D: mỗi lá xoay thật (ngả ra sau Tilt độ, xoay chéo Yaw độ trên mặt bàn); camera trực giao nên lá thành hình bình hành;
//   lá trên cao hơn lá dưới Thick px, thấy độ dày xấp bài.
// - Tráo (người dùng 2026-11-25): mỗi lần tráo chọn ngẫu nhiên một trong 6 kiểu, không lặp kiểu vừa dùng:
//   Cắt (rút xấp dưới đặt lên đỉnh, 2 lần), Riffle uốn lá (tách hai xấp, mép trong từng lá uốn vểnh lên rồi thả xen kẽ về giữa — uốn
//   thật trên lưới, CardBend), Chặt ba xấp (dàn trái / phải rồi gom theo thứ tự ngẫu nhiên), Thả từng xấp (nhấc bộ, bóc 1–3 lá từ đỉnh
//   thả sang chồng mới), Xoa bài (rải lộn xộn trên bàn, xoay vòng, gom), Trải dải (trải thành dải ngang, gợn sóng, vuốt gom).
//   Chưa tới lượt người chơi rút (địch đang chọn, hai bên ra đòn) bộ tráo lặp, chậm hơn; giữa hai lần chọn tráo một lần nhanh.
// - Tới lượt rút: tráo nốt lần đang dở rồi thôi; 3 lá trên đỉnh nhấc khỏi bộ, dựng dần lên trong lúc bay theo cung tới chỗ (thứ tự
//   ngẫu nhiên) rồi lật ra mặt. Sử thi, Huyền thoại khựng lại rung trước khi lật (viền độ hiếm hé ra sau lưng lá úp), lật thì viền bung.
// - Chọn xong: lá chọn bay vào hàng thẻ (BattleView.FlyToSlot); các lá còn lại lật úp giữa đường, nằm dần xuống về đỉnh bộ, bộ cắt lại
//   rồi chia. Địch rút: lá trên đỉnh nhấc lên dựng đứng (Lift) rồi bay vào hàng thẻ của địch, lật giữa đường (BattleView.FoeDraw).
// Viền độ hiếm (shader PokiClash/UICardAura, material the_aura_<độ hiếm>) nằm ở lớp riêng sau mọi thẻ (ngay trước hàng thẻ) và bám
// theo thẻ mỗi khung, nên viền thẻ này không đè mặt thẻ bên cạnh hay ô hàng thẻ. Chỉ vẽ; BattleView quyết định khi nào chia, trả, rút.
// Dựng sẵn (luật prefab, 2026-11-27): component này, ba lớp (bộ, viền, lá bay), khung viền (Items/VienHiemThe) và material viền theo độ
// hiếm nằm trong Screens/Battle, do menu "PokiClash/Prefab/Trận/Bộ bài tráo: lớp + viền độ hiếm" (Editor/DraftDeckMenu.cs) vá vào.
using System;
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    [DefaultExecutionOrder(100)] // sau UiMotion (nhún, lún khi đè): viền bám đúng chỗ thẻ trong cùng khung
    public sealed class DraftDeck : MonoBehaviour
    {
        public const int Count = 10; // số lá thấy trong bộ
        public const float Scale = 0.62f; // cỡ lá trong bộ so với thẻ thật
        const float Tilt = 55, Yaw = 30; // lá nằm trên bàn: ngả ra sau, xoay chéo trên mặt bàn
        const float Thick = 3.2f; // mỗi lá cao hơn lá dưới (px)
        const float AuraPad = 96; // viền tràn ra mỗi bên thẻ (px), đủ chỗ cho lưỡi lửa cao nhất của Huyền thoại
        static readonly Vector2 CardSize = new Vector2(320, 464); // UiCard.NormalSize
        public static Vector2 AuraSize => CardSize + new Vector2(AuraPad, AuraPad) * 2; // khung viền (menu dựng material, prefab mục)

        // dựng sẵn trong Screens/Battle: lớp bộ bài và lớp lá bay (con của ô thẻ chọn), lớp viền (ngay trước hàng thẻ), khung viền,
        // material viền Hiếm / Sử thi / Huyền thoại
        [SerializeField] RectTransform deckLayer, auraHost, flyHost;
        [SerializeField] Image auraPrefab;
        [SerializeField] Material[] auraMats = new Material[3];
        public bool Baked => deckLayer && auraHost && flyHost && auraPrefab && auraMats != null && auraMats.Length == 3 &&
                             auraMats[0] && auraMats[1] && auraMats[2];

        // nhịp (giây, ở Speed = 1)
        public const float CutQuick = 0.21f; // mỗi lần cắt giữa hai lần chọn (cắt 2 lần)
        static readonly float CosT = Mathf.Cos(Tilt * Mathf.Deg2Rad); // độ sâu trên mặt bàn hiện ra trên màn
        const float DealStagger = 0.06f, DealFly = 0.26f, FlipLen = 0.16f, ReturnLen = 0.22f;

        public float Speed = 1; // >1 nhanh hơn (địch, tự chơi, công cụ thử chạy nhanh)
        public bool Busy => dealCo != null; // đang cắt / chia, thẻ chưa lật đủ

        RectTransform offer, deck, auraLayer, flyLayer, backPrefab;
        readonly List<RectTransform> stack = new List<RectTransform>(); // từ đáy lên đỉnh
        readonly float[] jitYaw = new float[Count + 1], jitX = new float[Count + 1];
        int hidden; // số lá trên đỉnh đang ở ngoài (đã chia / rút, chưa về)
        int returning; // số lá đang bay về
        bool shuffling, loop, loopQuiet = true, shown;
        float loopPace = 1, loopPause = 0.5f;
        readonly Dictionary<RectTransform, CardBend[]> bends = new Dictionary<RectTransform, CardBend[]>();
        Coroutine loopCo, dealCo, showCo;
        float showS, bumpT = -1, bumpK;
        readonly List<RectTransform> backIdle = new List<RectTransform>();

        sealed class Entry
        {
            public UiCard card;
            public RectTransform back; // lá úp đang bay thay thẻ (trước khi lật)
            public Aura aura;
            public Coroutine co;
            public bool revealed;
        }

        readonly Dictionary<UiCard, Entry> entries = new Dictionary<UiCard, Entry>();

        float Dt => Time.unscaledDeltaTime * Mathf.Max(0.1f, Speed);

        // ---------- dựng ----------

        // auraBehind: lớp viền độ hiếm nằm ngay trước mục này trong cha của nó (hàng thẻ: lửa của Huyền thoại ló sau các ô, không đè lên)
        public static DraftDeck Ensure(RectTransform offer, RectTransform backPrefab, Vector2 center, RectTransform auraBehind = null)
        {
            var d = offer.GetComponent<DraftDeck>();
            if (!d || !d.Baked || !backPrefab)
            {
                Debug.LogError("[Bộ bài] Screens/Battle chưa dựng sẵn bộ bài (DraftDeck, lớp, khung viền, material, lá úp): chạy menu " +
                               "\"PokiClash/Prefab/Trận/Bộ bài tráo: lớp + viền độ hiếm\".");
                return d;
            }
            d.Build(offer, backPrefab, center, auraBehind);
            return d;
        }

        void Build(RectTransform o, RectTransform back, Vector2 center, RectTransform auraBehind)
        {
            if (deck) return;
            offer = o;
            backPrefab = back;
            deck = deckLayer;
            deck.anchorMin = deck.anchorMax = new Vector2(0.5f, 1);
            deck.pivot = new Vector2(0.5f, 0.5f);
            deck.sizeDelta = CardSize;
            deck.anchoredPosition = center;
            deck.SetSiblingIndex(0);
            auraLayer = auraHost;
            auraLayer.anchorMin = Vector2.zero;
            auraLayer.anchorMax = Vector2.one;
            if (auraLayer.parent is RectTransform host) auraLayer.pivot = host.pivot;
            auraLayer.offsetMin = auraLayer.offsetMax = Vector2.zero;
            if (auraBehind && auraBehind.parent == auraLayer.parent)
            {
                // ngay trước hàng thẻ (dời từ sau ra trước thì chỗ đích lùi một)
                int i = auraBehind.GetSiblingIndex();
                auraLayer.SetSiblingIndex(auraLayer.GetSiblingIndex() < i ? i - 1 : i);
            }
            flyLayer = Stretch(flyHost);
            flyLayer.SetAsLastSibling();
            var rnd = new System.Random(7);
            for (int k = 0; k <= Count; k++)
            {
                jitYaw[k] = (float)(rnd.NextDouble() * 5 - 2.5); // lá xếp tay, lệch nhau chút ít
                jitX[k] = (float)(rnd.NextDouble() * 3 - 1.5);
            }
            for (int k = 0; k < Count; k++)
            {
                var c = NewBack(deck);
                Place(c, k);
                c.localScale = new Vector3(Scale, Scale, 1);
                bends[c] = CardBend.Attach(c);
                stack.Add(c);
            }
            deck.localScale = Vector3.zero;
        }

        RectTransform Stretch(RectTransform rt)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.pivot = offer.pivot;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            return rt;
        }

        RectTransform NewBack(Transform parent)
        {
            var b = Ui.Spawn(backPrefab, parent); // Ensure đã chặn khi thiếu lá úp
            b.name = "la_up";
            b.anchorMin = b.anchorMax = b.pivot = new Vector2(0.5f, 0.5f);
            b.sizeDelta = CardSize;
            foreach (var g in b.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
            return b;
        }

        // tầng k trong bộ (toạ độ lớp bộ, tâm bộ ở giữa): lá trên cao hơn lá dưới Thick px
        Vector2 Slot(int k) => new Vector2(jitX[Mathf.Clamp(k, 0, Count)], Thick * k - Thick * (Count - 1) / 2f);

        // tư thế nằm của tầng k (so với lớp bộ): xoay chéo trên mặt bàn rồi ngả ra sau
        Quaternion Lie(int k) => Quaternion.Euler(Tilt, 0, Yaw + jitYaw[Mathf.Clamp(k, 0, Count)]);

        void Place(RectTransform c, int k)
        {
            c.anchoredPosition = Slot(k);
            c.localRotation = Lie(k);
        }

        // hướng rút xấp dưới ra (trên màn, toạ độ lớp bộ): theo cạnh ngắn của lá trên mặt bàn, sang trái chếch xuống
        static Vector2 PullDir()
        {
            var v = Quaternion.Euler(Tilt, 0, Yaw) * Vector3.left;
            return new Vector2(v.x, v.y);
        }

        // trận mới: bộ về nguyên, tắt
        public void ResetAll()
        {
            StopAllCoroutines();
            loopCo = dealCo = showCo = null;
            shuffling = loop = false;
            returning = hidden = 0;
            foreach (var e in entries.Values)
                if (e.back) ReleaseBack(e.back);
            entries.Clear();
            foreach (var a in auras) Hide(a);
            auras.Clear();
            for (int i = flyLayer.childCount - 1; i >= 0; i--)
            {
                var c = (RectTransform)flyLayer.GetChild(i);
                if (c.gameObject.activeSelf && c.name == "la_up") ReleaseBack(c);
            }
            for (int k = 0; k < stack.Count; k++)
            {
                stack[k].gameObject.SetActive(true);
                stack[k].SetSiblingIndex(k);
                Place(stack[k], k);
                Bend(stack[k], 0, 0);
            }
            shown = false;
            showS = 0;
            bumpT = -1;
            deck.localScale = Vector3.zero;
        }

        // ---------- hiện / ẩn, cắt lặp ----------

        public void Show(bool on)
        {
            if (shown == on) return;
            shown = on;
            if (showCo != null) StopCoroutine(showCo);
            showCo = StartCoroutine(ShowRun(on));
        }

        IEnumerator ShowRun(bool on)
        {
            float from = showS, len = on ? 0.32f : 0.2f;
            for (float t = 0; t < len; t += Time.unscaledDeltaTime)
            {
                float k = t / len;
                showS = on ? Mathf.LerpUnclamped(from, 1, BackOut(k)) : Mathf.Lerp(from, 0, k * k);
                yield return null;
            }
            showS = on ? 1 : 0;
            showCo = null;
        }

        // tráo lặp khi chưa tới lượt rút (pace: nhân độ dài mỗi lần tráo, nghỉ pause giây giữa hai lần); quiet: không tiếng (lúc ra đòn)
        public void Loop(bool on, float pace = 1, float pause = 0.5f, bool quiet = true)
        {
            loop = on;
            loopPace = pace;
            loopPause = pause;
            loopQuiet = quiet;
            if (on && loopCo == null && dealCo == null) loopCo = StartCoroutine(LoopRun());
        }

        IEnumerator LoopRun()
        {
            while (loop)
            {
                while (returning > 0) yield return null;
                if (!loop || !shown || dealCo != null) break;
                yield return Shuffle(false, loopPace, loopQuiet);
                for (float w = 0; loop && w < loopPause; w += Dt) yield return null;
            }
            loopCo = null;
        }

        // chờ bộ vuông (không đang cắt dở) — để rút lá trên đỉnh
        public IEnumerator WaitSquare(float max)
        {
            for (float w = 0; shuffling && w < max; w += Time.unscaledDeltaTime) yield return null;
        }

        // ---------- tráo: chọn kiểu ----------

        public enum Style { Cut, Riffle, Chop, Overhand, Wash, Fan }
        public static int ForceStyle = -1; // công cụ thử: ép kiểu tráo kế tiếp (−1: ngẫu nhiên)
        Style lastStyle = Style.Cut;

        // một lần tráo: quick (giữa hai lần chọn, ~0,5 giây) hay lặp lúc chờ (dài hơn 25%, nhân pace)
        IEnumerator Shuffle(bool quick, float pace, bool quiet)
        {
            Style st;
            if (ForceStyle >= 0 && ForceStyle <= (int)Style.Fan)
            {
                st = (Style)ForceStyle;
                ForceStyle = -1;
            }
            else
            {
                st = (Style)UnityEngine.Random.Range(0, 5);
                if (st >= lastStyle) st++; // không lặp kiểu vừa dùng
            }
            lastStyle = st;
            float m = quick ? 1 : 1.25f * Mathf.Max(0.3f, pace);
            switch (st)
            {
                case Style.Riffle:
                    yield return Riffle(0.5f * m, quiet);
                    break;
                case Style.Chop:
                    yield return Chop(0.52f * m, quiet);
                    break;
                case Style.Overhand:
                    yield return Overhand(0.52f * m, quiet);
                    break;
                case Style.Wash:
                    yield return Wash(0.56f * m, quiet);
                    break;
                case Style.Fan:
                    yield return Fan(0.52f * m, quiet);
                    break;
                default:
                    yield return Cut(CutQuick * (quick ? 1 : 1.6f * pace), quiet);
                    if (quick) yield return Cut(CutQuick, quiet);
                    break;
            }
        }

        void Bend(RectTransform c, float amount, int side)
        {
            if (bends.TryGetValue(c, out var b)) CardBend.Set(b, amount, side);
        }

        // đầu một lần tráo: lá ở ngoài coi như đã về (hiện lại trong lúc cả bộ chuyển động), ghi tư thế đầu
        int BeginShuffle(out Vector2[] p0, out Quaternion[] q0)
        {
            shuffling = true;
            hidden = 0;
            int n = stack.Count;
            p0 = new Vector2[n];
            q0 = new Quaternion[n];
            for (int i = 0; i < n; i++)
            {
                stack[i].gameObject.SetActive(true);
                p0[i] = stack[i].anchoredPosition;
                q0[i] = stack[i].localRotation;
            }
            return n;
        }

        // cuối một lần tráo: thứ tự mới (đáy lên đỉnh), mọi lá về đúng tầng, phẳng, gõ vuông
        void EndShuffle(List<RectTransform> order, bool quiet)
        {
            stack.Clear();
            stack.AddRange(order);
            for (int k = 0; k < stack.Count; k++)
            {
                stack[k].SetSiblingIndex(k);
                Place(stack[k], k);
                Bend(stack[k], 0, 0);
            }
            Bump(0.045f);
            if (!quiet) App.Audio?.PlayGap("deal", 0.04f, 0.35f, UnityEngine.Random.Range(0.95f, 1.1f));
            shuffling = false;
        }

        static float Smooth(float u)
        {
            u = Mathf.Clamp01(u);
            return u * u * (3 - 2 * u);
        }

        // chỗ trên mặt bàn lệch off (px trên màn) ở tầng k
        Vector2 At(Vector2 off, int k) => Slot(k) + off;

        // ---------- kiểu Riffle uốn lá ----------
        // tách hai xấp cạnh nhau theo cạnh ngắn của lá; mép trong từng lá uốn vểnh lên; thả xen kẽ từ đáy hai xấp, lá vừa thả duỗi phẳng
        // và trượt về giữa chồng lên nhau
        IEnumerator Riffle(float len, bool quiet)
        {
            int n = BeginShuffle(out var p0, out var q0);
            int h = n / 2;
            var dir = PullDir();
            float d = CardSize.x * Scale * 0.6f;
            Vector2 offL = dir * d, offR = -dir * d;
            const float bendMax = 70;
            var slotOf = new int[n];
            int o = 0;
            for (int j = 0; j < Mathf.Max(h, n - h); j++)
            {
                if (j < h) slotOf[j] = o++;
                if (h + j < n) slotOf[h + j] = o++;
            }
            var started = new bool[n];
            const float split = 0.24f, bendEnd = 0.36f, rel = 0.38f, move = 0.16f, end = 0.9f;
            float step = (end - rel - move) / Mathf.Max(1, n - 1);
            if (!quiet) App.Audio?.Play("card", 0.3f, 1.2f);
            for (float T = 0; ; T += Dt)
            {
                float k = Mathf.Clamp01(T / Mathf.Max(0.05f, len));
                for (int i = 0; i < n; i++)
                {
                    var c = stack[i];
                    bool left = i < h;
                    int lv = left ? i : i - h;
                    Vector2 pk = At(left ? offL : offR, lv);
                    var qk = Lie(lv) * Quaternion.Euler(0, 0, left ? 5 : -5);
                    int side = left ? 1 : -1; // mép trong: xấp trái là mép +x, xấp phải là mép −x
                    float st = rel + slotOf[i] * step;
                    if (k < split)
                    {
                        float e = Out3(k / split);
                        c.anchoredPosition = Vector2.Lerp(p0[i], pk, e) + new Vector2(0, left ? 0 : Mathf.Sin(e * Mathf.PI) * 18);
                        c.localRotation = Quaternion.Slerp(q0[i], qk, e);
                        Bend(c, 0, side);
                    }
                    else if (k < st)
                    {
                        c.anchoredPosition = pk;
                        c.localRotation = qk;
                        Bend(c, bendMax * Out3((k - split) / (bendEnd - split)), side);
                    }
                    else
                    {
                        float u = Mathf.Clamp01((k - st) / move);
                        if (!started[i])
                        {
                            started[i] = true;
                            c.SetAsLastSibling(); // lá thả sau nằm trên lá thả trước
                            if (!quiet) App.Audio?.PlayGap("deal", 0.03f, 0.2f, UnityEngine.Random.Range(1.5f, 1.9f));
                        }
                        float e = Smooth(u);
                        int s = slotOf[i];
                        c.anchoredPosition = Vector2.Lerp(pk, Slot(s), e) + new Vector2(0, Mathf.Sin(u * Mathf.PI) * 10);
                        c.localRotation = Quaternion.Slerp(qk, Lie(s), e);
                        Bend(c, bendMax * (1 - Out3(u / 0.6f)), side);
                    }
                }
                if (k >= 1) break;
                yield return null;
            }
            var ns = new RectTransform[n];
            for (int i = 0; i < n; i++) ns[slotOf[i]] = stack[i];
            EndShuffle(new List<RectTransform>(ns), quiet);
        }

        // ---------- kiểu Chặt ba xấp ----------
        // xấp trên dàn ra sau phải, xấp giữa dàn ra trước trái (theo cạnh ngắn của lá, không chồng lên nhau); gom hai xấp về lên xấp đáy
        // theo thứ tự ngẫu nhiên
        IEnumerator Chop(float len, bool quiet)
        {
            int n = BeginShuffle(out var p0, out var q0);
            int a = UnityEngine.Random.Range(2, 4), c3 = UnityEngine.Random.Range(2, 4);
            int b = n - a - c3;
            var dir = PullDir();
            float d = CardSize.x * Scale * 1.1f;
            Vector2 spotL = dir * d, spotR = -dir * d;
            bool leftFirst = UnityEngine.Random.value < 0.5f;
            // pile: 0 đáy, 1 giữa (sang trái), 2 trên (sang phải)
            int Pile(int i) => i < a ? 0 : i < a + b ? 1 : 2;
            int InPile(int i) => i < a ? i : i < a + b ? i - a : i - a - b;
            int first = leftFirst ? 1 : 2;
            int firstCount = first == 1 ? b : c3;
            var raised = new bool[3];
            for (float T = 0; ; T += Dt)
            {
                float k = Mathf.Clamp01(T / Mathf.Max(0.05f, len));
                for (int pile = 1; pile <= 2; pile++)
                {
                    bool isFirst = pile == first;
                    float g0 = isFirst ? 0.48f : 0.68f;
                    if (!raised[pile] && k >= g0)
                    {
                        raised[pile] = true;
                        for (int i = 0; i < n; i++)
                            if (Pile(i) == pile)
                                stack[i].SetAsLastSibling();
                        if (!quiet) App.Audio?.PlayGap("deal", 0.04f, 0.3f, 1.15f);
                    }
                }
                for (int i = 0; i < n; i++)
                {
                    var c = stack[i];
                    int pile = Pile(i), ip = InPile(i);
                    if (pile == 0)
                    {
                        c.anchoredPosition = Vector2.Lerp(p0[i], Slot(ip), Smooth(k / 0.3f));
                        c.localRotation = Quaternion.Slerp(q0[i], Lie(ip), Smooth(k / 0.3f));
                        continue;
                    }
                    Vector2 spot = pile == 1 ? spotL : spotR;
                    float o0 = pile == 2 ? 0f : 0.1f; // xấp trên đi trước
                    float u1 = Mathf.Clamp01((k - o0) / 0.28f);
                    bool isFirst = pile == first;
                    float g0 = isFirst ? 0.48f : 0.68f;
                    float u2 = Mathf.Clamp01((k - g0) / 0.22f);
                    int fin = a + (isFirst ? 0 : firstCount) + ip;
                    Vector2 out1 = At(spot, ip);
                    float e1 = Out3(u1), e2 = Smooth(u2);
                    var pos = Vector2.Lerp(p0[i], out1, e1) + new Vector2(0, Mathf.Sin(u1 * Mathf.PI) * 22);
                    pos = Vector2.Lerp(pos, Slot(fin), e2) + new Vector2(0, Mathf.Sin(u2 * Mathf.PI) * 26);
                    c.anchoredPosition = pos;
                    var q = Quaternion.Slerp(q0[i], Lie(ip) * Quaternion.Euler(0, 0, pile == 1 ? 7 : -7), e1);
                    c.localRotation = Quaternion.Slerp(q, Lie(fin), e2);
                }
                if (k >= 1) break;
                yield return null;
            }
            var order = new List<RectTransform>(n);
            for (int i = 0; i < a; i++) order.Add(stack[i]);
            foreach (int pile in new[] { first, 3 - first })
                for (int i = 0; i < n; i++)
                    if (Pile(i) == pile)
                        order.Add(stack[i]);
            EndShuffle(order, quiet);
        }

        // ---------- kiểu Thả từng xấp ----------
        // cả bộ nhấc lên lùi ra sau phải; bóc từng xấp 1–3 lá trên đỉnh thả sang chồng mới phía trước trái (xấp sau nằm trên xấp trước, nên
        // thứ tự các xấp đảo lại); cuối cùng chồng mới trượt về giữa
        IEnumerator Overhand(float len, bool quiet)
        {
            int n = BeginShuffle(out var p0, out var q0);
            var chunks = new List<Vector2Int>(); // (lá đầu, số lá), từ đỉnh xuống
            for (int top = n; top > 0;)
            {
                int cnt = Mathf.Min(top, UnityEngine.Random.Range(1, 4));
                chunks.Add(new Vector2Int(top - cnt, cnt));
                top -= cnt;
            }
            var dir = PullDir();
            Vector2 held = -dir * 55 + new Vector2(0, 46), pile = dir * 150;
            var chunkOf = new int[n];
            var level = new int[n];
            int lvl = 0;
            for (int j = 0; j < chunks.Count; j++)
                for (int q = 0; q < chunks[j].y; q++)
                {
                    int i = chunks[j].x + q;
                    chunkOf[i] = j;
                    level[i] = lvl++;
                }
            const float lift = 0.14f, mv = 0.17f, last = 0.84f, slide = 0.86f;
            float step = (last - lift - mv) / Mathf.Max(1, chunks.Count - 1);
            var began = new bool[chunks.Count];
            for (float T = 0; ; T += Dt)
            {
                float k = Mathf.Clamp01(T / Mathf.Max(0.05f, len));
                for (int j = 0; j < chunks.Count; j++)
                    if (!began[j] && k >= lift + j * step)
                    {
                        began[j] = true;
                        for (int q = 0; q < chunks[j].y; q++) stack[chunks[j].x + q].SetAsLastSibling();
                        if (!quiet) App.Audio?.PlayGap("deal", 0.03f, 0.25f, UnityEngine.Random.Range(1.2f, 1.5f));
                    }
                float back = Smooth((k - slide) / (1 - slide));
                for (int i = 0; i < n; i++)
                {
                    var c = stack[i];
                    float e0 = Out3(k / lift);
                    Vector2 hp = At(held, i);
                    float st = lift + chunkOf[i] * step;
                    if (k < st)
                    {
                        c.anchoredPosition = Vector2.Lerp(p0[i], hp, e0);
                        c.localRotation = Quaternion.Slerp(q0[i], Lie(i) * Quaternion.Euler(0, 0, -4), e0);
                        continue;
                    }
                    float u = Mathf.Clamp01((k - st) / mv), e = Smooth(u);
                    var lp = At(pile, level[i]);
                    c.anchoredPosition = Vector2.Lerp(hp, lp, e) + new Vector2(0, Mathf.Sin(u * Mathf.PI) * 18) - pile * back;
                    c.localRotation = Quaternion.Slerp(Lie(i) * Quaternion.Euler(0, 0, -4), Lie(level[i]), e) * Quaternion.Euler(0, 0, Mathf.Sin(u * Mathf.PI) * 8);
                }
                if (k >= 1) break;
                yield return null;
            }
            var ns = new RectTransform[n];
            for (int i = 0; i < n; i++) ns[level[i]] = stack[i];
            EndShuffle(new List<RectTransform>(ns), quiet);
        }

        // ---------- kiểu Xoa bài ----------
        // rải các lá lộn xộn ra mặt bàn (mỗi lá một hướng), xoay vòng như hai tay xoa, gom về thành bộ theo thứ tự mới
        IEnumerator Wash(float len, bool quiet)
        {
            int n = BeginShuffle(out var p0, out var q0);
            var ang = new float[n];
            var rad = new float[n];
            var yaw = new float[n];
            var fin = new int[n];
            for (int i = 0; i < n; i++)
            {
                ang[i] = UnityEngine.Random.Range(0f, Mathf.PI * 2);
                rad[i] = UnityEngine.Random.Range(60f, 165f);
                yaw[i] = UnityEngine.Random.Range(-65f, 65f);
                fin[i] = i;
            }
            for (int i = n - 1; i > 0; i--)
            {
                int j = UnityEngine.Random.Range(0, i + 1);
                (fin[i], fin[j]) = (fin[j], fin[i]);
            }
            // rải: thứ tự vẽ lộn xộn
            var mess = new List<int>();
            for (int i = 0; i < n; i++) mess.Insert(UnityEngine.Random.Range(0, mess.Count + 1), i);
            foreach (int i in mess) stack[i].SetAsLastSibling();
            Vector2 Off(int i, float extra) => new Vector2(Mathf.Cos(ang[i] + extra) * rad[i], Mathf.Sin(ang[i] + extra) * rad[i] * CosT);
            const float spread = 0.3f, swirl = 0.62f;
            bool gathered = false;
            if (!quiet) App.Audio?.Play("card", 0.3f, 0.9f);
            for (float T = 0; ; T += Dt)
            {
                float k = Mathf.Clamp01(T / Mathf.Max(0.05f, len));
                if (!gathered && k >= swirl)
                {
                    gathered = true; // gom: lá về tầng thấp vẽ trước
                    var byFin = new RectTransform[n];
                    for (int i = 0; i < n; i++) byFin[fin[i]] = stack[i];
                    foreach (var c in byFin) c.SetAsLastSibling();
                    if (!quiet) App.Audio?.Play("card", 0.3f, 1.1f);
                }
                float sw = Smooth((k - spread) / (swirl - spread));
                for (int i = 0; i < n; i++)
                {
                    var c = stack[i];
                    float extra = 1.7f * sw;
                    var spreadPos = At(Off(i, extra), 0) + new Vector2(0, mess.IndexOf(i) * 0.8f);
                    var spreadRot = Lie(0) * Quaternion.Euler(0, 0, yaw[i] + 50 * sw);
                    if (k < spread)
                    {
                        float e = Out3(k / spread);
                        c.anchoredPosition = Vector2.Lerp(p0[i], spreadPos, e) + new Vector2(0, Mathf.Sin(e * Mathf.PI) * 14);
                        c.localRotation = Quaternion.Slerp(q0[i], spreadRot, e);
                    }
                    else if (k < swirl)
                    {
                        c.anchoredPosition = spreadPos;
                        c.localRotation = spreadRot;
                    }
                    else
                    {
                        float u = (k - swirl) / (1 - swirl), e = Smooth(u);
                        c.anchoredPosition = Vector2.Lerp(spreadPos, Slot(fin[i]), e) + new Vector2(0, Mathf.Sin(u * Mathf.PI) * 10);
                        c.localRotation = Quaternion.Slerp(spreadRot, Lie(fin[i]), e);
                    }
                }
                if (k >= 1) break;
                yield return null;
            }
            var ns = new RectTransform[n];
            for (int i = 0; i < n; i++) ns[fin[i]] = stack[i];
            EndShuffle(new List<RectTransform>(ns), quiet);
        }

        // ---------- kiểu Trải dải ----------
        // trải bộ thành dải ngang trên mặt bàn (lá dưới bên trái), một làn sóng chạy qua dải, rồi vuốt gom về giữa
        IEnumerator Fan(float len, bool quiet)
        {
            int n = BeginShuffle(out var p0, out var q0);
            const float S = 205, go = 0.34f, gather = 0.6f, dur = 0.28f;
            float stg = 0.06f / Mathf.Max(1, n - 1);
            if (!quiet) App.Audio?.Play("card", 0.3f, 1f);
            bool swept = false;
            for (float T = 0; ; T += Dt)
            {
                float k = Mathf.Clamp01(T / Mathf.Max(0.05f, len));
                if (!swept && k >= gather)
                {
                    swept = true;
                    if (!quiet) App.Audio?.Play("card", 0.3f, 1.25f);
                }
                for (int i = 0; i < n; i++)
                {
                    var c = stack[i];
                    float x = -S + 2 * S * i / Mathf.Max(1, n - 1);
                    var fanPos = Slot(0) + new Vector2(x, i * 0.8f);
                    var fanRot = Lie(i) * Quaternion.Euler(0, 0, -6 + 12f * i / Mathf.Max(1, n - 1));
                    float u1 = Mathf.Clamp01((k - i * stg) / go);
                    float wave = Mathf.Sin(Mathf.Clamp01((k - 0.36f - i * 0.018f) / 0.12f) * Mathf.PI) * 20; // làn sóng chạy từ trái sang
                    float u2 = Mathf.Clamp01((k - gather - i * stg) / dur);
                    float e1 = Out3(u1), e2 = Smooth(u2);
                    var pos = Vector2.Lerp(p0[i], fanPos, e1) + new Vector2(0, wave);
                    c.anchoredPosition = Vector2.Lerp(pos, Slot(i), e2) + new Vector2(0, Mathf.Sin(u2 * Mathf.PI) * 8);
                    c.localRotation = Quaternion.Slerp(Quaternion.Slerp(q0[i], fanRot, e1), Lie(i), e2);
                }
                if (k >= 1) break;
                yield return null;
            }
            EndShuffle(new List<RectTransform>(stack), quiet);
        }

        // ---------- kiểu Cắt ----------

        // một lần cắt: rút xấp dưới (35–65% số lá) ra bên cạnh, xấp trên rơi xuống, xấp rút nhấc lên đặt lên đỉnh, gõ vuông bộ
        IEnumerator Cut(float len, bool quiet)
        {
            shuffling = true;
            // lá đang ở ngoài (địch rút, lá còn bay về) coi như đã về: hiện lại trong lúc cả bộ đang chuyển động
            hidden = 0;
            int n = stack.Count;
            int m = Mathf.Clamp(UnityEngine.Random.Range(Mathf.RoundToInt(n * 0.35f), Mathf.RoundToInt(n * 0.65f) + 1), 1, n - 1);
            var p0 = new Vector2[n];
            var q0 = new Quaternion[n];
            for (int i = 0; i < n; i++)
            {
                stack[i].gameObject.SetActive(true);
                p0[i] = stack[i].anchoredPosition;
                q0[i] = stack[i].localRotation;
            }
            float dist = CardSize.x * Scale * 1.02f; // rút ra gần hết bề ngang lá (trên mặt bàn)
            var pull = PullDir() * dist;
            const float outEnd = 0.36f, dropA = 0.22f, dropB = 0.44f;
            bool raised = false, landed = false;
            if (!quiet) App.Audio?.Play("card", 0.3f, 1.3f);
            for (float T = 0; ; T += Dt)
            {
                float k = Mathf.Clamp01(T / Mathf.Max(0.05f, len));
                if (!raised && k >= outEnd)
                {
                    raised = true; // xấp rút nhấc lên trên xấp còn lại: vẽ sau
                    for (int i = 0; i < m; i++) stack[i].SetAsLastSibling();
                }
                for (int i = 0; i < n; i++)
                {
                    var c = stack[i];
                    if (i < m)
                    {
                        // xấp dưới: rút ra → vòng lên trên → đặt xuống tầng mới (trên đỉnh), xoay nhẹ trên mặt bàn lúc đang cầm
                        int fs = n - m + i;
                        float spin;
                        if (k < outEnd)
                        {
                            float e = Out3(k / outEnd);
                            c.anchoredPosition = p0[i] + pull * e;
                            spin = -6 * e;
                        }
                        else
                        {
                            float u = (k - outEnd) / (1 - outEnd), e = u * u * (3 - 2 * u);
                            c.anchoredPosition = Vector2.Lerp(p0[i] + pull, Slot(fs), e) + new Vector2(0, Mathf.Sin(u * Mathf.PI) * 26);
                            spin = -6 * (1 - e);
                        }
                        c.localRotation = Quaternion.Slerp(q0[i], Lie(fs), k) * Quaternion.Euler(0, 0, spin);
                    }
                    else
                    {
                        // xấp trên: rơi xuống chỗ xấp dưới vừa rút (rơi nhanh dần)
                        float u = Mathf.Clamp01((k - dropA) / (dropB - dropA));
                        c.anchoredPosition = Vector2.Lerp(p0[i], Slot(i - m), u * u);
                        c.localRotation = Quaternion.Slerp(q0[i], Lie(i - m), u);
                    }
                }
                if (!landed && k >= 0.94f)
                {
                    landed = true;
                    Bump(0.045f);
                    if (!quiet) App.Audio?.PlayGap("deal", 0.04f, 0.35f, UnityEngine.Random.Range(0.95f, 1.1f));
                }
                if (k >= 1) break;
                yield return null;
            }
            var ns = new List<RectTransform>(n);
            for (int i = m; i < n; i++) ns.Add(stack[i]);
            for (int i = 0; i < m; i++) ns.Add(stack[i]);
            stack.Clear();
            stack.AddRange(ns);
            for (int k = 0; k < n; k++) Place(stack[k], k);
            shuffling = false;
        }

        void Bump(float k)
        {
            bumpT = 0;
            bumpK = k;
        }

        // ---------- chia, lật ----------

        // chia các thẻ (đã đặt sẵn ở chỗ, cỡ cuối; sẽ tắt tới lúc lật). revealed: mỗi thẻ lật xong; done: thẻ cuối lật xong
        public void Deal(IList<UiCard> cards, Action<UiCard> revealed, Action done)
        {
            bool fromLoop = loopCo != null;
            loop = false;
            if (dealCo != null) StopCoroutine(dealCo);
            var list = new List<UiCard>();
            foreach (var c in cards)
                if (c)
                {
                    c.gameObject.SetActive(false);
                    entries[c] = new Entry { card = c };
                    list.Add(c);
                }
            Show(true);
            dealCo = StartCoroutine(DealRun(list, fromLoop, revealed, done));
        }

        IEnumerator DealRun(List<UiCard> cards, bool fromLoop, Action<UiCard> revealed, Action done)
        {
            // lá đang bay về: chờ chạm bộ
            for (float w = 0; returning > 0 && w < 0.5f; w += Time.unscaledDeltaTime) yield return null;
            while (shuffling) yield return null; // đang tráo chờ lượt: tráo nốt lần dở
            if (!fromLoop) yield return Shuffle(true, 1, false); // vừa có lá về (hay bộ mới hiện): tráo lại một lần, kiểu ngẫu nhiên
            // thứ tự bay ngẫu nhiên
            var order = new List<int>();
            for (int i = 0; i < cards.Count; i++) order.Insert(UnityEngine.Random.Range(0, order.Count + 1), i);
            int left = 0;
            for (int o = 0; o < order.Count; o++)
            {
                var c = cards[order[o]];
                if (!c || !entries.TryGetValue(c, out var e)) continue;
                left++;
                e.co = StartCoroutine(DealOne(e, o, () =>
                {
                    left--;
                    revealed?.Invoke(e.card);
                }));
                for (float w = 0; w < DealStagger; w += Dt) yield return null;
            }
            while (left > 0) yield return null;
            dealCo = null;
            done?.Invoke();
        }

        IEnumerator DealOne(Entry e, int o, Action onRevealed)
        {
            var card = e.card;
            var crt = (RectTransform)card.transform;
            var rar = card.Card != null ? card.Card.rarity : Rarity.Common;
            Vector2 target = crt.anchoredPosition;
            float fin = crt.localScale.x;
            Vector3 targetW = crt.TransformPoint(crt.rect.center);

            // lá trên đỉnh bộ nhấc ra (đang nằm)
            var top = TopPose(true);
            var back = TakeBack(flyLayer);
            e.back = back;
            back.position = top.pos;
            back.rotation = top.q;
            float s0 = top.scale / Mathf.Max(1e-4f, flyLayer.lossyScale.x);
            back.localScale = new Vector3(s0, s0, 1);
            var q0 = back.localRotation;
            if (rar >= Rarity.Rare)
            {
                e.aura = TakeAura(rar);
                if (e.aura != null)
                {
                    e.aura.target = back;
                    e.aura.alphaTo = rar >= Rarity.Epic ? 0.35f : 0; // Sử thi trở lên hé viền sau lưng lá úp
                }
            }
            App.Audio?.Play("card", 0.5f, 1.05f + o * 0.08f);

            // bay theo cung, vụt đi rồi chậm lại; dựng dần từ tư thế nằm lên mặt về phía người xem; lá rơi gần như thẳng (lá giữa) vồng cao hơn
            Vector2 a = flyLayer.InverseTransformPoint(top.pos);
            Vector2 z = flyLayer.InverseTransformPoint(targetW);
            float dx = Mathf.Abs(z.x - a.x);
            var ctrl = (a + z) * 0.5f + new Vector2(0, 80 + dx * 0.12f + (dx < 60 ? 110 : 0));
            float spin = (z.x >= a.x ? -1 : 1) * (dx < 60 ? 5 : 11);
            float sTop = fin * 1.04f;
            for (float t = 0; t < DealFly; t += Dt)
            {
                if (!back) yield break;
                float k = t / DealFly, ee = Out3(k), u = 1 - ee;
                back.localPosition = u * u * a + 2 * u * ee * ctrl + ee * ee * z;
                float s = Mathf.Lerp(s0, sTop, ee);
                back.localScale = new Vector3(s, s, 1);
                float stand = Out3(Mathf.Clamp01(k / 0.75f)); // dựng lên nhanh hơn bay (đứng hẳn trước khi tới chỗ)
                back.localRotation = Quaternion.Slerp(q0, Quaternion.identity, stand) * Quaternion.Euler(0, 0, Mathf.Sin(ee * Mathf.PI) * spin);
                yield return null;
            }
            back.localPosition = z;
            back.localRotation = Quaternion.identity;
            back.localScale = new Vector3(sTop, sTop, 1);

            // Sử thi, Huyền thoại: khựng lại rung, viền hé dần (tụ lực trước khi lật)
            if (rar >= Rarity.Epic)
            {
                float hold = rar == Rarity.Legend ? 0.26f : 0.12f, amp = rar == Rarity.Legend ? 3f : 2f;
                if (e.aura != null) e.aura.alphaTo = 0.7f;
                App.Audio?.Play("buff", 0.3f, rar == Rarity.Legend ? 1.5f : 1.3f);
                for (float t = 0; t < hold; t += Dt)
                {
                    if (!back) yield break;
                    float k = t / hold;
                    back.localEulerAngles = new Vector3(0, 0, Mathf.Sin(t * 70) * amp * (0.4f + 0.6f * k));
                    float s = sTop * (1 + 0.035f * k);
                    back.localScale = new Vector3(s, s, 1);
                    yield return null;
                }
                back.localEulerAngles = Vector3.zero;
            }

            // lật: lá úp co ngang về 0, thẻ nở ra quá đà rồi đứng; nhấc lên một chút trong lúc lật
            float flip = rar == Rarity.Legend ? 0.2f : FlipLen;
            float sB = back.localScale.y;
            bool faced = false;
            for (float t = 0; t < flip; t += Dt)
            {
                float k = t / flip;
                float lift = Mathf.Sin(k * Mathf.PI) * 18;
                if (k < 0.5f)
                {
                    if (!back) yield break;
                    float u = k / 0.5f;
                    back.localScale = new Vector3(sB * (1 - u * u), sB * (1 + 0.05f * u), 1);
                    back.localPosition = z + new Vector2(0, lift);
                }
                else
                {
                    if (!faced)
                    {
                        faced = true;
                        Reveal(e, rar);
                    }
                    if (!crt) yield break;
                    float u = (k - 0.5f) / 0.5f;
                    float sx = BackOut(u), sy = Mathf.Lerp(1.05f, 1, u), toFin = Mathf.Lerp(1, fin / sTop, u);
                    crt.localScale = new Vector3(Mathf.LerpUnclamped(0, sTop, sx) * toFin, sTop * sy * toFin, 1);
                    crt.anchoredPosition = target + new Vector2(0, lift);
                }
                yield return null;
            }
            if (!faced) Reveal(e, rar);
            if (!crt) yield break;
            crt.localScale = new Vector3(fin, fin, 1);
            crt.anchoredPosition = target;
            crt.localEulerAngles = Vector3.zero;
            e.revealed = true;
            e.co = null;
            onRevealed?.Invoke();
        }

        // nửa sau của lật: thẻ thay lá úp, viền bung, tiếng và rung theo độ hiếm
        void Reveal(Entry e, Rarity rar)
        {
            var crt = (RectTransform)e.card.transform;
            if (e.back)
            {
                ReleaseBack(e.back);
                e.back = null;
            }
            e.card.gameObject.SetActive(true);
            crt.localEulerAngles = Vector3.zero;
            crt.localScale = new Vector3(0, crt.localScale.y, 1);
            if (e.aura != null)
            {
                e.aura.target = crt;
                e.aura.alphaTo = 1;
                if (rar >= Rarity.Epic)
                {
                    e.aura.burst = 0.001f;
                    e.aura.punch = rar == Rarity.Legend ? 0.16f : 0.1f;
                }
                else e.aura.punch = 0.06f;
            }
            switch (rar)
            {
                case Rarity.Legend:
                    App.Audio?.Play("level", 0.55f, 1.1f);
                    Haptics.Play(Haptic.LandGold);
                    break;
                case Rarity.Epic:
                    App.Audio?.Play("coin", 0.55f, 1.15f);
                    Haptics.Play(Haptic.LandSilver);
                    break;
                case Rarity.Rare:
                    App.Audio?.Play("coin", 0.35f, 1.5f);
                    break;
                default:
                    App.Audio?.Play("deal", 0.5f, 1.25f);
                    break;
            }
        }

        // ---------- trả về bộ ----------

        // thẻ không được chọn (hoặc cả lượt thẻ bị thay): lật úp giữa đường bay về đỉnh bộ; thẻ chưa lật thì lá úp của nó bay về
        public void Return(UiCard card)
        {
            if (!card) return;
            entries.TryGetValue(card, out var e);
            entries.Remove(card);
            if (e != null)
            {
                if (!e.revealed && dealCo != null)
                {
                    StopCoroutine(dealCo); // một lá chưa lật bị thu thì cả lượt chia dở bỏ
                    dealCo = null;
                }
                if (e.co != null) StopCoroutine(e.co);
                if (e.aura != null) e.aura.alphaTo = 0;
                if (!e.revealed)
                {
                    if (e.aura != null) e.aura.target = null;
                    if (e.back) StartCoroutine(BackHome(e.back));
                    if (!card.gameObject.activeSelf)
                    {
                        Destroy(card.gameObject);
                        return;
                    }
                }
            }
            StartCoroutine(ReturnRun(card));
        }

        // lá chọn rời ô (bản sao bay vào hàng): viền bung ra rồi tắt tại chỗ
        public void Picked(UiCard card)
        {
            if (!card || !entries.TryGetValue(card, out var e)) return;
            entries.Remove(card);
            if (e.co != null) StopCoroutine(e.co);
            if (e.back) ReleaseBack(e.back);
            if (e.aura != null)
            {
                e.aura.target = null;
                e.aura.alphaTo = 0;
                e.aura.punch = 0.2f;
                e.aura.fade = 7;
            }
        }

        IEnumerator ReturnRun(UiCard card)
        {
            returning++;
            card.SetInteractable(false);
            if (card.TryGetComponent<UiMotion>(out var m)) m.enabled = false;
            var crt = (RectTransform)card.transform;
            var wc = crt.TransformPoint(crt.rect.center);
            crt.pivot = new Vector2(0.5f, 0.5f);
            crt.position = wc;
            var parent = (RectTransform)crt.parent;
            Vector2 a = parent.InverseTransformPoint(wc);
            float s0 = crt.localScale.x;
            var q0 = crt.rotation; // so với thế giới (thẻ trong ô, lá úp trong lớp lá bay: hai cha khác nhau)
            RectTransform back = null;
            for (float t = 0; t < ReturnLen; t += Dt)
            {
                float k = t / ReturnLen, ee = k * k * (3 - 2 * k), u = 1 - ee;
                var land = LandPose();
                Vector2 z = parent.InverseTransformPoint(land.pos);
                var ctrl = (a + z) * 0.5f + new Vector2(0, 70);
                Vector2 pos = u * u * a + 2 * u * ee * ctrl + ee * ee * z;
                float s = Mathf.Lerp(s0, land.scale / Mathf.Max(1e-4f, parent.lossyScale.x), ee);
                var q = Quaternion.Slerp(q0, land.q, ee) * Quaternion.Euler(0, 0, Mathf.Sin(ee * Mathf.PI) * 8);
                if (k < 0.4f)
                {
                    if (!crt) break;
                    crt.localPosition = pos;
                    crt.localScale = new Vector3(s * (1 - Mathf.Pow(k / 0.4f, 2)), s, 1);
                    crt.rotation = q;
                }
                else
                {
                    if (!back)
                    {
                        if (crt) Destroy(crt.gameObject);
                        crt = null;
                        back = TakeBack(flyLayer);
                    }
                    back.localPosition = flyLayer.InverseTransformPoint(parent.TransformPoint(pos));
                    float sx = Out3(Mathf.Clamp01((k - 0.4f) / 0.35f));
                    float bs = s * parent.lossyScale.x / Mathf.Max(1e-4f, flyLayer.lossyScale.x);
                    back.localScale = new Vector3(bs * sx, bs, 1);
                    back.rotation = q;
                }
                yield return null;
            }
            if (crt) Destroy(crt.gameObject);
            if (back) ReleaseBack(back);
            Land();
            returning--;
        }

        // lá úp đang bay ra (lượt chia dở bị bỏ) quay về bộ
        IEnumerator BackHome(RectTransform back)
        {
            returning++;
            Vector2 a = back.localPosition;
            float s0 = back.localScale.y;
            var q0 = back.rotation;
            for (float t = 0; t < ReturnLen && back; t += Dt)
            {
                float k = t / ReturnLen, ee = k * k * (3 - 2 * k);
                var land = LandPose();
                Vector2 z = flyLayer.InverseTransformPoint(land.pos);
                back.localPosition = Vector2.Lerp(a, z, ee) + new Vector2(0, Mathf.Sin(ee * Mathf.PI) * 40);
                float s = Mathf.Lerp(s0, land.scale / Mathf.Max(1e-4f, flyLayer.lossyScale.x), ee);
                back.localScale = new Vector3(s, s, 1);
                back.rotation = Quaternion.Slerp(q0, land.q, ee);
                yield return null;
            }
            if (back) ReleaseBack(back);
            Land();
            returning--;
        }

        // một lá chạm đỉnh bộ: hiện lại tầng trên cùng còn trống, bộ nảy nhẹ
        void Land()
        {
            if (hidden > 0)
            {
                hidden--;
                int k = Count - 1 - hidden;
                var c = stack[k];
                c.gameObject.SetActive(true);
                Place(c, k);
            }
            Bump(0.035f);
            App.Audio?.PlayGap("deal", 0.04f, 0.35f, 0.95f);
        }

        // ---------- rút (địch) ----------

        public struct Pose
        {
            public Vector3 pos;
            public Quaternion q; // so với thế giới
            public float scale; // cỡ thế giới (lossy)
        }

        // lá trên đỉnh bộ (take: rút khỏi bộ, tầng đó tắt)
        public Pose TopPose(bool take)
        {
            int k = Count - 1 - hidden;
            float sc = Scale * deck.parent.lossyScale.x; // cỡ đúng cả khi bộ đang ẩn / đang nảy
            if (k < 0)
                return new Pose { pos = deck.position, q = deck.rotation * Lie(Count - 1), scale = sc };
            var c = stack[k];
            var pose = new Pose { pos = c.position, q = c.rotation, scale = sc };
            if (take)
            {
                c.gameObject.SetActive(false);
                hidden++;
            }
            return pose;
        }

        // chỗ lá về đáp: tầng ngay trên đỉnh hiện tại
        Pose LandPose()
        {
            int k = Mathf.Clamp(Count - hidden, 0, Count);
            return new Pose { pos = deck.TransformPoint(Slot(k)), q = deck.rotation * Lie(k), scale = Scale * deck.parent.lossyScale.x };
        }

        // lá vừa rút (đang nằm như trong bộ): nhấc lên, dựng đứng mặt về phía người xem, to dần
        public IEnumerator Lift(RectTransform back, float len)
        {
            if (!back) yield break;
            var q0 = back.localRotation;
            Vector3 p0 = back.localPosition;
            float s0 = back.localScale.y;
            for (float t = 0; t < len && back; t += Dt)
            {
                float k = Out3(t / len);
                back.localRotation = Quaternion.Slerp(q0, Quaternion.identity, k);
                back.localPosition = p0 + new Vector3(0, 46 * k, 0);
                float s = s0 * Mathf.Lerp(1, 1.15f, k);
                back.localScale = new Vector3(s, s, 1);
                yield return null;
            }
            if (!back) yield break;
            back.localRotation = Quaternion.identity;
        }

        // lá úp lấy từ kho (dùng cho lá bay, cả lá địch rút bay trong lớp phủ), đặt trên cùng parent
        public RectTransform TakeBack(Transform parent)
        {
            RectTransform b = null;
            while (backIdle.Count > 0 && !b)
            {
                b = backIdle[backIdle.Count - 1];
                backIdle.RemoveAt(backIdle.Count - 1);
            }
            if (!b) b = NewBack(parent);
            else b.SetParent(parent, false);
            b.gameObject.SetActive(true);
            b.SetAsLastSibling();
            b.localRotation = Quaternion.identity;
            return b;
        }

        public void ReleaseBack(RectTransform b)
        {
            if (!b) return;
            b.gameObject.SetActive(false);
            if (flyLayer && b.parent != flyLayer) b.SetParent(flyLayer, false);
            if (!backIdle.Contains(b)) backIdle.Add(b);
        }

        // ---------- viền độ hiếm ----------

        sealed class Aura
        {
            public RectTransform rt;
            public Image img;
            public RectTransform target;
            public float alpha, alphaTo, burst = -1, punch, fade = 6;
        }

        readonly List<Aura> auras = new List<Aura>();
        readonly List<Aura> auraIdle = new List<Aura>();

        Aura TakeAura(Rarity r)
        {
            var mat = Mat(r);
            if (!mat) return null;
            Aura a = null;
            while (auraIdle.Count > 0 && (a == null || !a.rt))
            {
                a = auraIdle[auraIdle.Count - 1];
                auraIdle.RemoveAt(auraIdle.Count - 1);
            }
            if (a == null || !a.rt)
            {
                var img = Ui.Spawn(auraPrefab, auraLayer);
                img.name = "vien";
                img.raycastTarget = false;
                var rt = img.rectTransform;
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
                a = new Aura { rt = rt, img = img };
            }
            a.rt.gameObject.SetActive(true);
            a.rt.sizeDelta = CardSize + new Vector2(AuraPad, AuraPad) * 2;
            a.img.material = mat;
            a.alpha = 0;
            a.alphaTo = 0;
            a.burst = -1;
            a.punch = 0;
            a.fade = 6;
            a.target = null;
            a.img.color = new Color(0, 0, 0, 0);
            auras.Add(a);
            return a;
        }

        void Hide(Aura a)
        {
            if (a.rt) a.rt.gameObject.SetActive(false);
            a.target = null;
            if (!auraIdle.Contains(a)) auraIdle.Add(a);
        }

        void LateUpdate()
        {
            float dt = Mathf.Min(0.05f, Time.unscaledDeltaTime);
            // bộ: hiện / ẩn × nảy khi gõ vuông
            float bump = 1;
            if (bumpT >= 0)
            {
                bumpT += dt / 0.16f;
                if (bumpT >= 1) bumpT = -1;
                else bump = 1 + bumpK * Mathf.Sin(bumpT * Mathf.PI);
            }
            if (deck) deck.localScale = new Vector3(showS * bump, showS * bump, 1);

            for (int i = auras.Count - 1; i >= 0; i--)
            {
                var a = auras[i];
                if (!a.rt)
                {
                    auras.RemoveAt(i);
                    continue;
                }
                var tg = a.target;
                bool live = tg && tg.gameObject.activeInHierarchy;
                if (live)
                {
                    a.rt.position = tg.TransformPoint(tg.rect.center);
                    a.rt.rotation = tg.rotation;
                    var ls = tg.lossyScale;
                    var ps = auraLayer.lossyScale;
                    a.rt.localScale = new Vector3(ls.x / Mathf.Max(1e-5f, ps.x), ls.y / Mathf.Max(1e-5f, ps.y), 1) * (1 + a.punch);
                }
                else
                {
                    a.alphaTo = 0;
                    if (a.punch > 0) a.rt.localScale *= 1 + a.punch * dt * 6; // lá đã rời: viền nở ra lúc tắt
                }
                a.alpha = Mathf.MoveTowards(a.alpha, a.alphaTo, dt * a.fade);
                if (a.burst >= 0)
                {
                    a.burst += dt / 0.5f;
                    if (a.burst >= 1) a.burst = -1;
                }
                if (live) a.punch = Mathf.MoveTowards(a.punch, 0, dt * 0.6f);
                a.img.color = new Color(a.burst >= 0 ? Mathf.Clamp(a.burst, 0.004f, 0.996f) : 0, 0, 0, a.alpha);
                if (a.alpha <= 0 && a.alphaTo <= 0 && !live)
                {
                    auras.RemoveAt(i);
                    Hide(a);
                }
            }
        }

        // ---------- material theo độ hiếm (asset dựng sẵn, một bản mỗi bậc, dùng chung) ----------

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void ClearStatics() => ForceStyle = -1;

        Material Mat(Rarity r)
        {
            int i = (int)r - (int)Rarity.Rare;
            return i >= 0 && auraMats != null && i < auraMats.Length ? auraMats[i] : null;
        }

#if UNITY_EDITOR
        // thông số viền từng bậc: menu DraftDeckMenu chép material gốc the_aura rồi gọi hàm này, lưu thành the_aura_<độ hiếm>.mat
        public static void StyleAura(Material m, Rarity r)
        {
            var c1 = Theme.Of(r);
            m.SetColor("_C1", c1);
            m.SetColor("_CInk", Color.Lerp(c1, Theme.Ink, 0.45f));
            m.SetVector("_Card", new Vector4(151, 224, -3, 2)); // phần giấy của khung thẻ (lề trong suốt 6 trái, 12 phải, 6 trên, 10 dưới)
            m.SetVector("_Size", CardSize + new Vector2(AuraPad, AuraPad) * 2);
            m.SetFloat("_Radius", 18);
            switch (r)
            {
                case Rarity.Rare: // viền mỏng gợn nhẹ, hai sao
                    m.SetColor("_C2", Theme.Hex("#9cc8f2"));
                    m.SetColor("_C3", Theme.Hex("#e6f3ff"));
                    m.SetFloat("_Width", 11);
                    m.SetFloat("_Amp", 0.45f);
                    m.SetFloat("_Top", 0.15f);
                    m.SetFloat("_Rise", 0.7f);
                    m.SetVector("_Freq", new Vector4(0.05f, 0.03f, 0, 0));
                    m.SetFloat("_Spark", 2);
                    m.SetFloat("_Rays", 0);
                    m.SetFloat("_InkW", 2);
                    break;
                case Rarity.Epic: // dày hơn, lửa vừa, ba sao
                    m.SetColor("_C2", Theme.Hex("#c7a4f2"));
                    m.SetColor("_C3", Theme.Hex("#f5ecff"));
                    m.SetFloat("_Width", 19);
                    m.SetFloat("_Amp", 0.75f);
                    m.SetFloat("_Top", 0.45f);
                    m.SetFloat("_Rise", 1.1f);
                    m.SetVector("_Freq", new Vector4(0.05f, 0.024f, 0, 0));
                    m.SetFloat("_Spark", 3);
                    m.SetFloat("_Rays", 0);
                    m.SetFloat("_InkW", 2.5f);
                    break;
                default: // Huyền thoại: dày nhất, lửa cao, năm sao, tia nắng sau thẻ
                    m.SetColor("_C2", Theme.Hex("#ffcc4d"));
                    m.SetColor("_C3", Theme.Hex("#fff4c8"));
                    m.SetFloat("_Width", 27);
                    m.SetFloat("_Amp", 0.95f);
                    m.SetFloat("_Top", 0.7f);
                    m.SetFloat("_Rise", 1.5f);
                    m.SetVector("_Freq", new Vector4(0.055f, 0.024f, 0, 0));
                    m.SetFloat("_Spark", 5);
                    m.SetFloat("_Rays", 1);
                    m.SetFloat("_InkW", 3);
                    break;
            }
        }
#endif

        static float Out3(float k) => 1 - Mathf.Pow(1 - Mathf.Clamp01(k), 3);

        static float BackOut(float k)
        {
            const float c1 = 1.3f, c3 = c1 + 1;
            float x = Mathf.Clamp01(k) - 1;
            return 1 + c3 * x * x * x + c1 * x * x;
        }
    }
}
