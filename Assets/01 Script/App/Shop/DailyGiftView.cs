// Màn nhận quà hôm nay (người dùng 2026-11-27: "khi nhận quà hằng ngày không để thành cái pop up nữa ... nền đen thôi, phần quà hiện ra phải
// glowing đẹp hơn, nút x2 reward phải hiện trước to hơn, breath to nhỏ, rồi nút nhận thường hiện sau"). Prefab Assets/04 Prefabs/Items/QuaNgay
// (UiKit.dailyGift, menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng hết" hoặc "Cửa hàng: chỉ màn quà ngày"), canvas riêng mở chồng mọi màn.
// Nhịp: nền tối dần sang đen · chữ "Quà hôm nay" rơi xuống · loé trắng, vệt loé ngang, vòng toả, quầng vàng mềm bung rồi thở, hai lớp tia quay
// ngược nhau (ánh sáng mềm cộng sáng pk_g_* của màn mở rương máy bi; người dùng chọn glow ở màn nhận quà) · hình quà bật ra, dập dềnh, sao vẽ
// tay lấp lánh quanh · số "+N" · 1,0 s nút "Nhận ×2" (quảng cáo) bật ra to rồi thở 1,0 ↔ 1,1, viền sáng mỏng bám mép nút (shader
// PokiClash/UIEdgeGlow, thay quầng mềm to sau nút: người dùng 2026-11-27 "lố quá") · 2,6 s nút "Nhận thường" mờ hiện
// dưới. Chưa có quảng cáo (hay hết lượt) thì không có ×2, nút Nhận hiện ngay. Bấm ×2 xem xong: dấu ×2 đập xuống, số đếm lên gấp đôi; rồi quà bay
// lên góc phải trên (chỗ chip bi) và màn tắt.
// Quà thẻ tuần / tháng, gói nhận theo ngày đang chờ nhận cùng lúc (hàng nhỏ "Kèm quà thẻ"); ×2 chỉ nhân quà hôm nay (Shop.ClaimGift).
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
using Random = UnityEngine.Random;

namespace PokiClash
{
    public sealed class DailyGiftView : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image dim, rays, rays2, halo, haloCore, flare, ring, flash, art, btnGlow;
            public RectTransform item, x2Wrap, extras;
            public Image[] stars;
            public TextMeshProUGUI title, count, itemName, extrasTitle;
            public UiStamp stamp;
            public SketchButton x2, plain;
            public CanvasGroup plainGroup;
        }

        [SerializeField] Parts p;
        [SerializeField] RewardTile tilePrefab;

        // nền đen hẳn (người dùng: "nền đen thôi"; khoảng màu Linear: 0,93 rồi 0,98 vẫn thấy rõ sảnh, soi 2026-11-27)
        const float DimA = 1f, X2At = 1.0f, PlainAfter = 1.6f;
        const float GlowA = 0.6f; // độ sáng viền nút ×2 lúc thở nhỏ nhất (to nhất GlowA + 0,25)

        public static bool Playing { get; private set; }

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static ShopConfig C => App.Data.Cfg.shop;
        static double Now => SaveService.Now();

        bool giftReady, idle, chosen;
        Material glowMat;
        Vector2 itemHome;
        float[] starNext;
        int mainN;
        ShopItem mainItem;
        List<ShopItem> extraItems = new List<ShopItem>();

        // quà toả thành icon bay về ô chứa (RewardFly): quà chính từ hình quà, quà kèm từ từng ô
        void FlyRewards(int mainCount)
        {
            if (mainItem != null)
                RewardFly.Send(RewardFly.OfShop(mainItem.k), RewardFly.IconFor(mainItem.k) ?? p.art.sprite, p.item.TransformPoint(p.item.rect.center),
                    Math.Max(1, mainCount));
            int i = 0;
            foreach (RectTransform c in p.extras)
            {
                if (i >= extraItems.Count) break;
                var it = extraItems[i];
                if (c.gameObject.activeSelf && c.TryGetComponent<RewardTile>(out var rt))
                    RewardFly.Send(RewardFly.OfShop(it.k), RewardFly.IconFor(it.k) ?? rt.FlyIcon, rt.FlyFrom, Math.Max(1, Shop.Norm(it).n), 0.1f + 0.08f * i);
                i++;
            }
        }

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, RewardTile tile)
        {
            p = parts;
            tilePrefab = tile;
        }

        // mở màn nếu có quà chờ nhận; false: chưa dựng prefab hoặc không còn gì để nhận (nơi gọi tự xử lý)
        public static bool Open(Action closed)
        {
            var prefab = Theme.Prefabs ? Theme.Prefabs.dailyGift : null;
            // AnyClaim chờ xong hướng dẫn (hàng popup lúc vào game); bấm từ cửa hàng thì quà hôm nay còn nhận là đủ
            if (!prefab || S == null || !Shop.GiftReady(S, Now) && !Offers.AnyClaim(S, D, Now)) return false;
            var v = Ui.Spawn(prefab, App.Modals.transform);
            v.name = "qua_ngay";
            var rt = (RectTransform)v.transform;
            rt.Stretch();
            rt.SetAsLastSibling();
            Playing = true;
            App.I.StartCoroutine(v.Run(closed));
            return true;
        }

        void OnDestroy()
        {
            Playing = false;
            if (glowMat) Destroy(glowMat);
        }

        // viền sáng bám mép nút ×2: Image không ảnh phủ nút, tràn GlowReach px mỗi bên, shader PokiClash/UIEdgeGlow (material
        // Resources/UIEdgeGlow). Mép vẽ của ảnh nút sk_Button (128 px, cắt 9 ô viền 52 px, không phóng) lùi vào trong khung: trái 5,
        // phải 11, trên 5, dưới 13 px. Đặt theo cỡ nút thật nên prefab dựng trước đổi (quầng ảnh to) vẫn ra viền mới.
        const float GlowReach = 30;

        void FitGlow()
        {
            var g = p.btnGlow;
            var src = Resources.Load<Material>("UIEdgeGlow");
            if (!src)
            {
                g.gameObject.SetActive(false);
                return;
            }
            var size = p.x2.Rect.rect.size;
            var rt = g.rectTransform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = p.x2.Rect.anchoredPosition;
            rt.sizeDelta = size + 2 * GlowReach * Vector2.one;
            rt.localScale = Vector3.one;
            g.sprite = null;
            if (!glowMat) glowMat = new Material(src);
            g.material = glowMat;
            glowMat.SetVector("_Box", new Vector4(size.x * 0.5f - 8, size.y * 0.5f - 9, -3, 4));
            glowMat.SetVector("_Size", new Vector4(rt.sizeDelta.x, rt.sizeDelta.y, 0, 0));
            glowMat.SetFloat("_Width", GlowReach);
        }

        // ---------- dữ liệu ----------

        // quà chính (hình to) và các món kèm (hàng nhỏ): quà hôm nay trước, rồi quà thẻ, gói theo ngày
        (List<ShopItem> main, List<ShopItem> extra) Contents()
        {
            var groups = new List<List<ShopItem>>();
            giftReady = Shop.GiftReady(S, Now);
            if (giftReady) groups.Add(Shop.Resolve(S, D, C.dailyGift, true, null));
            foreach (var id in new[] { "week", "month" })
                if (Shop.CardClaimable(S, id, Now)) groups.Add(Shop.Resolve(S, D, C.Card(id).daily, true, null));
            if (S.shop != null)
                foreach (var kv in S.shop.days)
                {
                    var pk = C.Pack(kv.Key);
                    if (pk != null && Shop.DayClaimable(S, D, kv.Key, Now)) groups.Add(Shop.Resolve(S, D, pk.days[kv.Value.claimed].items, pk.scale, null));
                }
            var main = groups.Count > 0 ? groups[0] : new List<ShopItem>();
            var extra = groups.Skip(1).SelectMany(g => g).ToList();
            // quà chính nhiều món: món đầu là hình to, món còn lại vào hàng nhỏ
            if (main.Count > 1)
            {
                extra.InsertRange(0, main.Skip(1));
                main = main.Take(1).ToList();
            }
            return (main, extra);
        }

        List<Reward> Claim(bool twice)
        {
            var got = new List<Reward>();
            var now = Now;
            var rng = new Rng(Rng.RandomSeed());
            if (giftReady) got.AddRange(Shop.ClaimGift(S, D, twice, now, rng) ?? new List<Reward>());
            foreach (var id in new[] { "week", "month" }) got.AddRange(Shop.ClaimCard(S, D, id, now, rng) ?? new List<Reward>());
            if (S.shop != null)
                foreach (var id in S.shop.days.Keys.ToList())
                    got.AddRange(Shop.ClaimDay(S, D, id, now, rng) ?? new List<Reward>());
            App.Save.Save();
            ShopLog.Event("claim", twice ? "Quà hôm nay ×2" : "Quà hôm nay", 0);
            return got;
        }

        // ---------- nhịp ----------

        IEnumerator Run(Action closed)
        {
            var (main, extra) = Contents();
            var first = main.FirstOrDefault() ?? extra.FirstOrDefault();
            mainItem = first;
            extraItems = extra;
            mainN = first != null ? Shop.Norm(first).n : 0;
            Theme.SetSprite(p.art, first != null ? ShopPage.ArtFor(new List<ShopItem> { first }) : App.Art.Icon("star"));
            p.art.preserveAspect = true;
            p.title.text = Loc.T("Quà hôm nay");
            p.itemName.text = first != null ? ShopUi.ItemName(first) : "";
            SetCount(mainN);
            for (int i = p.extras.childCount - 1; i >= 0; i--) Destroy(p.extras.GetChild(i).gameObject);
            foreach (var it in extra) ShopUi.Tile(Ui.Spawn(tilePrefab, p.extras), it);
            foreach (RectTransform c in p.extras)
                if (c.TryGetComponent<RewardTile>(out var rt)) rt.Caption(Theme.Paper);
            bool hasExtra = extra.Count > 0;
            p.extras.gameObject.SetActive(hasExtra);
            p.extrasTitle.gameObject.SetActive(hasExtra);
            p.extrasTitle.text = Loc.T("Kèm quà thẻ");

            bool canX2 = giftReady && Ads.Ready && Ads.Left(Ads.DailyGiftAd) > 0;
            Ads.Bind(p.x2, Loc.T("Nhận ×2"), Ads.DailyGiftAd);
            p.x2.SetRole(BtnColor.Orange);
            p.x2.SetOnClick(() => Choose(true, closed));
            p.plain.SetText(canX2 ? Loc.T("Nhận thường") : Loc.T("Nhận"));
            p.plain.SetRole(canX2 ? BtnColor.Paper : BtnColor.Green);
            p.plain.SetOnClick(() => Choose(false, closed));
            if (!canX2) p.plain.Rect.localScale = Vector3.one * 1.3f;
            FitGlow();

            // trạng thái đầu
            itemHome = p.item.anchoredPosition;
            foreach (var g in new Graphic[] { p.rays, p.rays2, p.halo, p.haloCore, p.flare, p.ring, p.flash, p.btnGlow }) SetA(g, 0);
            p.item.localScale = Vector3.zero;
            p.count.transform.localScale = Vector3.zero;
            p.itemName.alpha = 0;
            p.stamp.gameObject.SetActive(false);
            p.x2Wrap.gameObject.SetActive(false);
            p.plainGroup.alpha = 0;
            p.plainGroup.interactable = p.plainGroup.blocksRaycasts = false;
            p.extras.localScale = p.extrasTitle.transform.localScale = Vector3.zero;
            foreach (var s in p.stars) s.gameObject.SetActive(false);
            starNext = p.stars.Select(_ => Random.Range(0.8f, 2.2f)).ToArray();
            var titleRt = p.title.rectTransform;
            var titleHome = titleRt.anchoredPosition;
            p.title.alpha = 0;

            // 1. nền đen, chữ rơi xuống
            StartCoroutine(Fade(p.dim, 0, DimA, 0.25f));
            App.Audio.Play("whoosh", 0.6f, 1.05f);
            yield return Wait(0.12f);
            for (float t = 0, d = 0.4f; t < d; t += Time.unscaledDeltaTime)
            {
                float e = EaseOutBack(t / d);
                titleRt.anchoredPosition = titleHome + new Vector2(0, 90 * (1 - e));
                p.title.alpha = Mathf.Clamp01(t / d * 2);
                yield return null;
            }
            titleRt.anchoredPosition = titleHome;
            p.title.alpha = 1;

            // 2. loé: chớp trắng, vệt loé ngang, vòng toả, quầng + tia bung, quà bật ra, sao bắn
            App.Audio.Play("chest");
            Haptics.Play(Haptic.OpenGold);
            StartCoroutine(Flash());
            StartCoroutine(Flare());
            StartCoroutine(Ring());
            StartCoroutine(Fade(p.rays, 0, 0.55f, 0.4f));
            StartCoroutine(Fade(p.rays2, 0, 0.35f, 0.4f));
            StartCoroutine(Fade(p.haloCore, 0, 0.9f, 0.25f));
            StartCoroutine(HaloIn());
            for (int i = 0; i < p.stars.Length; i++) StartCoroutine(Burst(p.stars[i], i * 360f / p.stars.Length + Random.Range(-12f, 12f)));
            yield return Reveal(p.item);
            idle = true;
            StartCoroutine(Pop((RectTransform)p.count.transform, 1.3f, 0.3f));
            StartCoroutine(Fade(p.itemName, 0, 1, 0.3f));
            if (hasExtra)
            {
                StartCoroutine(Pop(p.extrasTitle.rectTransform, 1.15f, 0.3f));
                StartCoroutine(Pop(p.extras, 1.1f, 0.35f));
            }

            // 3. nút ×2 bật ra to rồi thở; nút thường hiện sau
            yield return Wait(Mathf.Max(0, X2At - 0.75f));
            if (canX2 && !chosen)
            {
                p.x2Wrap.gameObject.SetActive(true);
                App.Audio.Play("peg", 0.6f, 1.2f);
                yield return Pop(p.x2Wrap, 1.18f, 0.32f);
                StartCoroutine(Fade(p.btnGlow, 0, GlowA, 0.3f));
                yield return Wait(PlainAfter);
            }
            if (!chosen)
            {
                for (float t = 0, d = 0.35f; t < d && !chosen; t += Time.unscaledDeltaTime)
                {
                    p.plainGroup.alpha = t / d;
                    yield return null;
                }
                p.plainGroup.alpha = 1;
                p.plainGroup.interactable = p.plainGroup.blocksRaycasts = true;
            }
        }

        void Choose(bool twice, Action closed)
        {
            if (chosen) return;
            chosen = true;
            p.x2.Interactable = false;
            p.plainGroup.interactable = false;
            if (!twice)
            {
                StartCoroutine(Finish(Claim(false), false, closed));
                return;
            }
            // hộp quảng cáo (bản dev: hộp thoại giả lập trong lớp hộp thoại) phải nằm trên màn này: tạm bỏ thứ tự vẽ riêng
            var cv = GetComponent<Canvas>();
            if (cv) cv.overrideSorting = false;
            Ads.Show(Ads.DailyGiftAd, ok =>
            {
                if (!this) return;
                if (cv) cv.overrideSorting = true;
                if (!ok)
                {
                    // quảng cáo hỏng / bỏ giữa chừng: giữ màn, bấm lại được
                    chosen = false;
                    Ads.Bind(p.x2, Loc.T("Nhận ×2"), Ads.DailyGiftAd);
                    p.plainGroup.alpha = 1;
                    p.plainGroup.interactable = p.plainGroup.blocksRaycasts = true;
                    return;
                }
                StartCoroutine(Finish(Claim(true), true, closed));
            });
        }

        IEnumerator Finish(List<Reward> got, bool twice, Action closed)
        {
            // nút lui đi
            StartCoroutine(Fade(p.btnGlow, p.btnGlow.color.a, 0, 0.2f));
            StartCoroutine(Shrink(p.x2Wrap, 0.2f));
            StartCoroutine(FadeGroup(p.plainGroup, 0.2f));
            if (twice)
            {
                // dấu ×2 đập xuống, số đếm lên gấp đôi
                p.stamp.gameObject.SetActive(true);
                p.stamp.Set("×2", Theme.Red);
                var srt = (RectTransform)p.stamp.transform;
                const float stampS = 1.7f; // dấu kit cỡ chữ nhỏ: phóng to cho đọc rõ trên hình quà
                for (float t = 0, d = 0.22f; t < d; t += Time.unscaledDeltaTime)
                {
                    float x = t / d;
                    srt.localScale = Vector3.one * stampS * Mathf.Lerp(3f, 1f, x * x);
                    yield return null;
                }
                srt.localScale = Vector3.one * stampS;
                App.Audio.Play("stamp");
                Haptics.Play(Haptic.OpenGold);
                StartCoroutine(Flash(0.3f));
                StartCoroutine(Ring());
                for (int i = 0; i < p.stars.Length; i++) StartCoroutine(Burst(p.stars[i], i * 360f / p.stars.Length + 18));
                for (float t = 0, d = 0.5f; t < d; t += Time.unscaledDeltaTime)
                {
                    SetCount(Mathf.RoundToInt(Mathf.Lerp(mainN, mainN * 2, t / d)));
                    p.count.transform.localScale = Vector3.one * (1 + 0.12f * Mathf.Sin(t / d * Mathf.PI * 4));
                    yield return null;
                }
                SetCount(mainN * 2);
                p.count.transform.localScale = Vector3.one;
                yield return Wait(0.45f);
            }
            else yield return Wait(0.1f);

            // quà toả thành icon bay về ô chứa (người dùng 2026-11-27: thu được gì thì icon cái đó bay vào chỗ chứa nó), hình quà thu nhỏ
            // tại chỗ, ánh sáng tắt, nền sáng lại
            idle = false;
            App.Audio.Play("whoosh", 0.7f, 1.3f);
            FlyRewards(twice ? mainN * 2 : mainN);
            var from = p.item.anchoredPosition;
            foreach (var g in new Graphic[] { p.rays, p.rays2, p.halo, p.haloCore, p.title, p.count, p.itemName, p.extrasTitle })
                StartCoroutine(Fade(g, g.color.a, 0, 0.3f));
            StartCoroutine(Shrink(p.extras, 0.25f));
            if (p.stamp.gameObject.activeSelf) StartCoroutine(Shrink((RectTransform)p.stamp.transform, 0.2f));
            for (float t = 0, d = 0.3f; t < d; t += Time.unscaledDeltaTime)
            {
                float x = t / d;
                p.item.anchoredPosition = from;
                p.item.localScale = Vector3.one * (x < 0.3f ? Mathf.Lerp(1, 1.12f, x / 0.3f) : Mathf.Lerp(1.12f, 0, (x - 0.3f) / 0.7f));
                yield return null;
            }
            p.item.gameObject.SetActive(false);
            Haptics.Play(Haptic.UiTap);
            yield return Fade(p.dim, p.dim.color.a, 0, 0.22f);
            Playing = false;
            Destroy(gameObject);
            // mảnh đủ mở khoá tướng: màn mở khoá sau quà (như ShopService.Show)
            HeroUnlockView.Play(HeroUnlockView.Unlocked(got), closed);
        }

        void SetCount(int n) => p.count.text = "+" + NumFmt.Short(Math.Max(0, n));

        // ---------- vòng lặp chờ ----------

        void Update()
        {
            float dt = Time.unscaledDeltaTime, tt = Time.unscaledTime;
            p.rays.rectTransform.Rotate(0, 0, -10 * dt);
            p.rays2.rectTransform.Rotate(0, 0, 7 * dt);
            if (!idle) return;
            // quầng thở, quà dập dềnh
            p.halo.rectTransform.localScale = Vector3.one * (1 + 0.07f * Mathf.Sin(tt * 2.6f));
            SetA(p.halo, 0.62f + 0.18f * Mathf.Sin(tt * 2.6f));
            p.item.anchoredPosition = itemHome + new Vector2(0, 10 * Mathf.Sin(tt * 2.2f));
            // nút ×2 thở to nhỏ 1,0 ↔ 1,1; viền sáng (con của khung thở nên to nhỏ theo nút) chỉ sáng tối nhẹ theo nhịp
            if (p.x2Wrap.gameObject.activeSelf && !chosen)
            {
                float b = 0.5f - 0.5f * Mathf.Cos(tt * Mathf.PI * 2 / 1.1f);
                p.x2Wrap.localScale = Vector3.one * (1 + 0.1f * b);
                SetA(p.btnGlow, GlowA + 0.25f * b);
            }
            // sao vẽ tay lấp lánh quanh quà
            for (int i = 0; i < p.stars.Length; i++)
            {
                starNext[i] -= dt;
                if (starNext[i] > 0 || p.stars[i].gameObject.activeSelf) continue;
                starNext[i] = Random.Range(0.9f, 2.4f);
                StartCoroutine(Twinkle(p.stars[i]));
            }
        }

        // ---------- hiệu ứng ----------

        IEnumerator Flash(float peak = 0.5f)
        {
            for (float t = 0, d = 0.3f; t < d; t += Time.unscaledDeltaTime)
            {
                SetA(p.flash, peak * (1 - t / d));
                yield return null;
            }
            SetA(p.flash, 0);
        }

        IEnumerator Flare()
        {
            var r = p.flare.rectTransform;
            for (float t = 0, d = 0.5f; t < d; t += Time.unscaledDeltaTime)
            {
                float x = t / d;
                r.localScale = new Vector3(Mathf.Lerp(0.2f, 1.3f, 1 - (1 - x) * (1 - x)), Mathf.Lerp(1.4f, 0.6f, x), 1);
                SetA(p.flare, x < 0.2f ? x / 0.2f : 1 - (x - 0.2f) / 0.8f);
                yield return null;
            }
            SetA(p.flare, 0);
        }

        IEnumerator Ring()
        {
            var r = p.ring.rectTransform;
            for (float t = 0, d = 0.5f; t < d; t += Time.unscaledDeltaTime)
            {
                float x = t / d;
                r.localScale = Vector3.one * Mathf.Lerp(0.3f, 2.4f, 1 - (1 - x) * (1 - x));
                SetA(p.ring, 0.9f * (1 - x));
                yield return null;
            }
            SetA(p.ring, 0);
        }

        IEnumerator HaloIn()
        {
            var r = p.halo.rectTransform;
            for (float t = 0, d = 0.4f; t < d; t += Time.unscaledDeltaTime)
            {
                float x = t / d;
                r.localScale = Vector3.one * (x < 0.6f ? Mathf.Lerp(0.2f, 1.3f, x / 0.6f) : Mathf.Lerp(1.3f, 1f, (x - 0.6f) / 0.4f));
                SetA(p.halo, Mathf.Min(1, x * 2) * 0.8f);
                yield return null;
            }
        }

        // sao bắn ra từ quà rồi tắt
        IEnumerator Burst(Image s, float ang)
        {
            if (s.gameObject.activeSelf) yield break;
            s.gameObject.SetActive(true);
            var r = s.rectTransform;
            var dir = new Vector2(Mathf.Cos(ang * Mathf.Deg2Rad), Mathf.Sin(ang * Mathf.Deg2Rad));
            float d = Random.Range(0.45f, 0.65f), dist = Random.Range(260f, 400f), size = Random.Range(0.7f, 1.2f);
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                float x = t / d;
                r.anchoredPosition = itemHome + dir * dist * (1 - (1 - x) * (1 - x));
                r.localScale = Vector3.one * size * (1 - x * 0.5f);
                r.localEulerAngles = new Vector3(0, 0, ang + 180 * x);
                SetA(s, 1 - x * x);
                yield return null;
            }
            s.gameObject.SetActive(false);
        }

        // lấp lánh tại chỗ quanh quà: to ra, xoay, nhỏ lại
        IEnumerator Twinkle(Image s)
        {
            s.gameObject.SetActive(true);
            var r = s.rectTransform;
            float ang = Random.Range(0, 360f), dist = Random.Range(190f, 330f);
            r.anchoredPosition = itemHome + new Vector2(Mathf.Cos(ang * Mathf.Deg2Rad), Mathf.Sin(ang * Mathf.Deg2Rad)) * dist;
            float d = Random.Range(0.5f, 0.8f), size = Random.Range(0.5f, 1f);
            SetA(s, 1);
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                float x = t / d;
                r.localScale = Vector3.one * size * Mathf.Sin(x * Mathf.PI);
                r.localEulerAngles = new Vector3(0, 0, 90 * x);
                yield return null;
            }
            s.gameObject.SetActive(false);
        }

        // quà hiện ra: kéo dọc rồi ép, nảy về (nhịp lộ diện như màn nở trứng)
        static IEnumerator Reveal(RectTransform rt)
        {
            Vector2[] keys = { new Vector2(0.2f, 1.6f), new Vector2(1.15f, 0.9f), new Vector2(0.96f, 1.05f), new Vector2(1, 1) };
            float[] at = { 0, 0.14f, 0.24f, 0.34f };
            float total = at[at.Length - 1];
            for (float t = 0; t < total; t += Time.unscaledDeltaTime)
            {
                int i = 0;
                while (i < at.Length - 2 && t > at[i + 1]) i++;
                var s = Vector2.Lerp(keys[i], keys[i + 1], Mathf.InverseLerp(at[i], at[i + 1], t));
                rt.localScale = new Vector3(s.x, s.y, 1);
                yield return null;
            }
            rt.localScale = Vector3.one;
        }

        static IEnumerator Pop(RectTransform rt, float peak, float d)
        {
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                float k = t / d;
                rt.localScale = Vector3.one * (k < 0.55f ? Mathf.Lerp(0, peak, k / 0.55f) : Mathf.Lerp(peak, 1, (k - 0.55f) / 0.45f));
                yield return null;
            }
            rt.localScale = Vector3.one;
        }

        static IEnumerator Shrink(RectTransform rt, float d)
        {
            var s0 = rt.localScale;
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                rt.localScale = s0 * (1 - t / d);
                yield return null;
            }
            rt.localScale = Vector3.zero;
        }

        static IEnumerator FadeGroup(CanvasGroup g, float d)
        {
            float a0 = g.alpha;
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                g.alpha = a0 * (1 - t / d);
                yield return null;
            }
            g.alpha = 0;
        }

        static IEnumerator Fade(Graphic g, float from, float to, float d)
        {
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                if (!g) yield break;
                SetA(g, Mathf.Lerp(from, to, t / d));
                yield return null;
            }
            if (g) SetA(g, to);
        }

        static void SetA(Graphic g, float a)
        {
            if (!g) return;
            var c = g.color;
            g.color = new Color(c.r, c.g, c.b, a);
        }

        static IEnumerator Wait(float s)
        {
            for (float t = 0; t < s; t += Time.unscaledDeltaTime) yield return null;
        }

        static float EaseOutBack(float x)
        {
            const float c1 = 1.70158f, c3 = c1 + 1;
            x = Mathf.Clamp01(x);
            return 1 + c3 * Mathf.Pow(x - 1, 3) + c1 * Mathf.Pow(x - 1, 2);
        }
    }
}
