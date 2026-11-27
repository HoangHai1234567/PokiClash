// Màn nở trứng capsule (người dùng 2026-11-23, GD_Claude/26 mục 13): prefab Assets/04 Prefabs/Items/NoTrung (UiKit.eggHatch, menu
// "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng hết"), mở chồng trên mọi hộp (canvas riêng). Một quả: trứng rơi vào giữa, tia sáng màu bậc xoay sau
// lưng, lắc ba nhịp mạnh dần (nở lên bậc trên thì nhịp hai chớp trắng, đổi sang trứng bậc mới, chữ "NÂNG BẬC!"), vòm bật lên theo đường
// nối capsule, thân rơi xuống, chớp trắng + vòng toả + sao bắn, ô mảnh tướng nảy ra giữa, tên tướng và bậc; chạm để sang quả kế.
// Nhiều quả (tới 10): mỗi quả chạy nhanh không chờ chạm, xong hiện bảng tổng (gộp theo tướng) và nút Nhận; "Bỏ qua" nhảy tới bảng tổng.
// Hình trứng: ShopUi.Egg (bản 2 Assets/03 Art/Shop/v2/trung2_<bậc>.png từ 2026-11-27; bản đầu đã bỏ), đường nối đo từ ảnh (ShopUi.EggSeam).
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using Random = UnityEngine.Random;

namespace PokiClash
{
    public sealed class EggHatchView : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image dim, rays, rays2, ring, flash, eggTop, eggBottom;
            public RectTransform egg, tileHolder, grid;
            public Image[] sparks;
            public TextMeshProUGUI title, hint, up, heroName;
            public Button catcher;
            public SketchButton ok, skip;
        }

        [SerializeField] Parts p;
        [SerializeField] RewardTile tilePrefab;

        // bề ngang trứng: bản 2 có viền sticker dày + cánh / lấp lánh nên khung 390 (bản đầu đã bỏ dùng 320) cho thân trứng to như cũ
        const float EggW = 390;

        public static bool Playing { get; private set; }

        bool tapped, skipAll;
        Vector2 eggHome;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, RewardTile tile)
        {
            p = parts;
            tilePrefab = tile;
        }

        public static void Play(List<Hatch> got, Action closed)
        {
            var prefab = Theme.Prefabs ? Theme.Prefabs.eggHatch : null;
            if (!prefab || got == null || got.Count == 0)
            {
                // chưa dựng prefab: hộp nhận thưởng thường
                ShopService.Show(Loc.T("Trứng nở"), got?.Select(h => h.reward).ToList() ?? new List<Reward>(), closed);
                return;
            }
            var v = Ui.Spawn(prefab, App.Modals.transform);
            v.name = "no_trung";
            var rt = (RectTransform)v.transform;
            rt.Stretch();
            rt.SetAsLastSibling();
            Playing = true;
            App.I.StartCoroutine(v.Run(got, closed));
        }

        void OnDestroy() => Playing = false;

        IEnumerator Run(List<Hatch> got, Action closed)
        {
            p.catcher.onClick.AddListener(() => tapped = true);
            p.skip.SetOnClick(() => skipAll = true);
            p.skip.gameObject.SetActive(got.Count > 1);
            p.ok.gameObject.SetActive(false);
            p.grid.gameObject.SetActive(false);
            p.flash.color = new Color(1, 1, 1, 0);
            p.up.gameObject.SetActive(false);
            p.heroName.gameObject.SetActive(false);
            eggHome = p.egg.anchoredPosition;
            yield return Fade(p.dim, 0, p.dim.color.a, 0.2f);
            bool fast = got.Count > 2;
            for (int i = 0; i < got.Count && !skipAll; i++)
            {
                p.title.text = got.Count > 1 ? $"{ShopUi.EggName(got[i].from)} ({i + 1}/{got.Count})" : ShopUi.EggName(got[i].from);
                yield return One(got[i], fast);
            }
            if (got.Count > 1) yield return Summary(got);
            // tướng mới mở khoá lúc nở nhanh (nhiều quả): màn mở khoá sau bảng tổng
            if (fast)
            {
                bool fin = false;
                HeroUnlockView.Play(HeroUnlockView.Unlocked(got.Select(h => h.reward)), () => fin = true);
                while (!fin) yield return null;
            }
            Playing = false;
            Destroy(gameObject);
            closed?.Invoke();
        }

        void Paint(int tier)
        {
            var s = ShopUi.Egg(tier);
            foreach (var img in new[] { p.eggTop, p.eggBottom }) Theme.SetSprite(img, s);
            float h = s ? EggW * s.rect.height / s.rect.width : EggW * 1.35f;
            p.egg.sizeDelta = new Vector2(EggW, h);
            float seam = ShopUi.EggSeam(tier);
            p.eggTop.fillAmount = seam;
            p.eggBottom.fillAmount = 1 - seam;
            // vòm xoay quanh đường nối
            foreach (var img in new[] { p.eggTop, p.eggBottom })
            {
                var r = img.rectTransform;
                r.anchorMin = r.anchorMax = new Vector2(0.5f, 1 - seam);
                r.pivot = new Vector2(0.5f, (1 - seam));
                r.sizeDelta = new Vector2(EggW, h);
                r.anchoredPosition = Vector2.zero;
                r.localEulerAngles = Vector3.zero;
                r.localScale = Vector3.one;
                img.color = Color.white;
            }
            var c = ShopUi.TierColor(tier);
            p.rays.color = new Color(c.r, c.g, c.b, p.rays.color.a);
            p.rays2.color = new Color(c.r, c.g, c.b, p.rays2.color.a);
            p.ring.color = new Color(c.r, c.g, c.b, 0);
        }

        IEnumerator One(Hatch h, bool fast)
        {
            float k = fast ? 0.55f : 1; // nhịp nhanh khi nở nhiều quả
            for (int i = p.tileHolder.childCount - 1; i >= 0; i--) Destroy(p.tileHolder.GetChild(i).gameObject);
            p.heroName.gameObject.SetActive(false);
            p.up.gameObject.SetActive(false);
            p.hint.gameObject.SetActive(false);
            p.egg.gameObject.SetActive(true);
            Paint(h.from);

            // 1. rơi vào giữa, tia sáng hiện
            App.Audio.Play("whoosh", 0.6f, 1.1f);
            StartCoroutine(Fade(p.rays, 0, 0.75f, 0.3f * k));
            StartCoroutine(Fade(p.rays2, 0, 0.45f, 0.3f * k));
            for (float t = 0, d = 0.35f * k; t < d; t += Time.unscaledDeltaTime)
            {
                float e = EaseOutBack(t / d);
                p.egg.anchoredPosition = eggHome + new Vector2(0, 520 * (1 - e));
                p.egg.localScale = Vector3.one * Mathf.Lerp(0.4f, 1, Mathf.Clamp01(t / d * 1.6f));
                yield return null;
            }
            p.egg.anchoredPosition = eggHome;
            p.egg.localScale = Vector3.one;
            Haptics.Play(Haptic.LandSilver);

            // 2. lắc ba nhịp mạnh dần; nhịp hai đổi bậc nếu nở lên
            for (int w = 0; w < 3; w++)
            {
                float amp = 7 + 6 * w;
                for (float t = 0, d = 0.2f * k; t < d; t += Time.unscaledDeltaTime)
                {
                    float x = t / d;
                    p.egg.localEulerAngles = new Vector3(0, 0, Mathf.Sin(x * Mathf.PI * 3) * amp * (1 - x * 0.4f));
                    float sq = 1 + Mathf.Sin(x * Mathf.PI) * 0.06f * (w + 1);
                    p.egg.localScale = new Vector3(sq, 2 - sq, 1);
                    yield return null;
                }
                p.egg.localEulerAngles = Vector3.zero;
                p.egg.localScale = Vector3.one;
                App.Audio.Play("peg", 0.5f, 1 + w * 0.15f);
                Haptics.Play(Haptic.UiTap);
                Sparks(6 + w * 3, 160 + 60 * w, h.from);
                if (w == 1 && h.Up)
                {
                    StartCoroutine(Flash(0.75f, 0.25f));
                    Paint(h.tier);
                    p.up.gameObject.SetActive(true);
                    p.up.text = Loc.T("NÂNG BẬC!");
                    p.up.color = ShopUi.TierColor(h.tier);
                    StartCoroutine(ChestBox.Pop(p.up.rectTransform, 1.4f));
                    App.Audio.Play("stamp");
                    Haptics.Play(Haptic.OpenGold);
                    yield return Wait(0.35f * k);
                }
                yield return Wait(0.1f * k);
            }

            // 3. bật vòm, thân rơi, chớp, vòng toả
            App.Audio.Play("chest");
            Haptics.Play(h.tier >= (int)Rarity.Epic ? Haptic.OpenGold : Haptic.OpenSilver);
            StartCoroutine(Flash(0.9f, 0.35f));
            StartCoroutine(Ring(h.tier));
            Sparks(p.sparks.Length, 420, h.tier);
            var top = p.eggTop.rectTransform;
            var bot = p.eggBottom.rectTransform;
            float dir = Random.value < 0.5f ? -1 : 1;
            for (float t = 0, d = 0.4f * k; t < d; t += Time.unscaledDeltaTime)
            {
                float x = t / d;
                float e = 1 - (1 - x) * (1 - x);
                top.anchoredPosition = new Vector2(dir * 140 * e, 320 * e - 160 * x * x);
                top.localEulerAngles = new Vector3(0, 0, -dir * 50 * e);
                bot.anchoredPosition = new Vector2(0, -150 * x * x);
                var a = new Color(1, 1, 1, 1 - x);
                p.eggTop.color = a;
                p.eggBottom.color = new Color(1, 1, 1, 1 - Mathf.Clamp01(x * 1.4f));
                yield return null;
            }
            p.egg.gameObject.SetActive(false);
            p.up.gameObject.SetActive(false);

            // 4. ô mảnh tướng
            var r = h.reward;
            var hero = App.Data.Hero(r.hero);
            if (hero != null && tilePrefab)
            {
                var tile = Ui.Spawn(tilePrefab, p.tileHolder).Hero(hero, "×" + r.n).Caption(Theme.Paper, false); // tên to ở dưới
                var res = r.res;
                if (res != null && res.unlocked) tile.Tag(Loc.T("MỞ KHÓA!"), Theme.Red);
                else if (res != null && res.converted > 0) tile.Tag(Loc.F("→ {0} thẻ", res.converted), Theme.Paper2);
                else
                {
                    var g = Progress.ShardGoal(App.Save.Data, App.Data, r.hero);
                    tile.Tag(g.need > 0 ? $"{g.have}/{g.need}" : $"{g.have}", Theme.Paper2);
                }
                var tr = (RectTransform)tile.transform;
                tr.anchorMin = tr.anchorMax = tr.pivot = new Vector2(0.5f, 0.5f);
                tr.anchoredPosition = Vector2.zero;
                yield return Reveal(tr, k);
                p.heroName.gameObject.SetActive(true);
                p.heroName.text = $"{hero.name}\n<size=70%><color=#{ColorUtility.ToHtmlStringRGB(Theme.Of(hero.rarity))}>{Elements.RarityName(hero.rarity).ToUpperInvariant()}</color></size>";
                if (res != null && res.unlocked)
                {
                    p.up.gameObject.SetActive(true);
                    p.up.text = Loc.T("TƯỚNG MỚI!");
                    p.up.color = Theme.Red;
                    StartCoroutine(ChestBox.Pop(p.up.rectTransform, 1.5f));
                    App.Audio.Play("stamp");
                    // màn mở khoá tướng (kiểu Brawl Stars) ngay sau khi ô mảnh hiện
                    if (!fast)
                    {
                        yield return new WaitForSecondsRealtime(0.5f);
                        bool fin = false;
                        HeroUnlockView.Play(new[] { hero.id }, () => fin = true);
                        while (!fin) yield return null;
                    }
                }
            }
            if (fast)
            {
                yield return Wait(0.45f);
                yield break;
            }
            p.hint.gameObject.SetActive(true);
            tapped = false;
            while (!tapped && !skipAll)
            {
                p.hint.alpha = 0.55f + 0.45f * Mathf.Sin(Time.unscaledTime * 4);
                yield return null;
            }
            p.hint.gameObject.SetActive(false);
        }

        IEnumerator Summary(List<Hatch> got)
        {
            p.egg.gameObject.SetActive(false);
            p.up.gameObject.SetActive(false);
            p.heroName.gameObject.SetActive(false);
            p.skip.gameObject.SetActive(false);
            for (int i = p.tileHolder.childCount - 1; i >= 0; i--) Destroy(p.tileHolder.GetChild(i).gameObject);
            p.title.text = Loc.F("Nở {0} trứng", got.Count);
            p.grid.gameObject.SetActive(true);
            // quả đã chạy nhanh vẫn còn chạy dở khi bỏ qua: bảng tổng là nguồn đúng (mảnh đã cộng lúc Eggs.Open)
            ChestDialog.BuildTiles(got.Select(h => h.reward).ToList(), tilePrefab, p.grid);
            foreach (RectTransform c in p.grid)
            {
                if (c.TryGetComponent<RewardTile>(out var rt)) rt.Caption(Theme.Paper);
                StartCoroutine(ChestBox.Pop(c, 1.15f));
            }
            App.Audio.Play("stamp");
            bool done = false;
            p.ok.gameObject.SetActive(true);
            p.ok.SetText(Loc.T("Nhận"));
            p.ok.SetOnClick(() => done = true);
            while (!done) yield return null;
        }

        // ---------- hiệu ứng ----------

        void Update()
        {
            float dt = Time.unscaledDeltaTime;
            p.rays.rectTransform.Rotate(0, 0, -18 * dt);
            p.rays2.rectTransform.Rotate(0, 0, 11 * dt);
        }

        IEnumerator Flash(float peak, float d)
        {
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                p.flash.color = new Color(1, 1, 1, peak * (1 - t / d));
                yield return null;
            }
            p.flash.color = new Color(1, 1, 1, 0);
        }

        IEnumerator Ring(int tier)
        {
            var c = ShopUi.TierColor(tier);
            var r = p.ring.rectTransform;
            for (float t = 0, d = 0.45f; t < d; t += Time.unscaledDeltaTime)
            {
                float x = t / d;
                r.localScale = Vector3.one * Mathf.Lerp(0.3f, 2.6f, 1 - (1 - x) * (1 - x));
                p.ring.color = new Color(c.r, c.g, c.b, 1 - x);
                yield return null;
            }
            p.ring.color = new Color(c.r, c.g, c.b, 0);
        }

        // sao bắn ra từ trứng
        void Sparks(int n, float dist, int tier)
        {
            var c = Color.Lerp(ShopUi.TierColor(tier), Color.white, 0.35f);
            for (int i = 0; i < n && i < p.sparks.Length; i++)
            {
                var s = p.sparks[i];
                if (s.gameObject.activeSelf) continue;
                StartCoroutine(Spark(s, Random.Range(0, 360f), dist * Random.Range(0.6f, 1.1f), c));
            }
        }

        IEnumerator Spark(Image s, float ang, float dist, Color c)
        {
            s.gameObject.SetActive(true);
            var r = s.rectTransform;
            var dir = new Vector2(Mathf.Cos(ang * Mathf.Deg2Rad), Mathf.Sin(ang * Mathf.Deg2Rad));
            float d = Random.Range(0.35f, 0.55f), size = Random.Range(0.6f, 1.2f);
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                float x = t / d;
                r.anchoredPosition = eggHome + dir * dist * (1 - (1 - x) * (1 - x)) + new Vector2(0, -60 * x * x);
                r.localScale = Vector3.one * size * (1 - x * 0.6f);
                r.localEulerAngles = new Vector3(0, 0, ang + 200 * x);
                s.color = new Color(c.r, c.g, c.b, 1 - x * x);
                yield return null;
            }
            s.gameObject.SetActive(false);
        }

        static IEnumerator Fade(Graphic g, float from, float to, float d)
        {
            var c = g.color;
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                if (!g) yield break;
                g.color = new Color(c.r, c.g, c.b, Mathf.Lerp(from, to, t / d));
                yield return null;
            }
            if (g) g.color = new Color(c.r, c.g, c.b, to);
        }

        // ô hiện ra: kéo dọc 0,3 × 1,63 → 1 → ép 1,1 × 0,94 → đứng yên (nhịp lộ diện của màn mở khoá Brawl Stars: khoá tuyến tính, nảy nhờ
        // khoá vượt rồi về; báo cáo mổ ở D:/Ripper/BrawlStar/Analysis/unlock/BAO_CAO.md)
        static IEnumerator Reveal(RectTransform rt, float k)
        {
            Vector2[] keys = { new Vector2(0.3f, 1.63f), new Vector2(1, 1), new Vector2(1.1f, 0.94f), new Vector2(1, 1) };
            float[] at = { 0, 0.12f, 0.2f, 0.3f };
            float total = at[at.Length - 1], d = total * Mathf.Max(0.7f, k);
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                float x = t / d * total;
                int i = 0;
                while (i < at.Length - 2 && x > at[i + 1]) i++;
                var s = Vector2.Lerp(keys[i], keys[i + 1], Mathf.InverseLerp(at[i], at[i + 1], x));
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

        IEnumerator Wait(float s)
        {
            for (float t = 0; t < s && !skipAll; t += Time.unscaledDeltaTime) yield return null;
        }

        static float EaseOutBack(float x)
        {
            const float c1 = 1.70158f, c3 = c1 + 1;
            x = Mathf.Clamp01(x);
            return 1 + c3 * Mathf.Pow(x - 1, 3) + c1 * Mathf.Pow(x - 1, 2);
        }
    }
}
