// Màn mở khoá tướng mới (người dùng 2026-11-23: "khi unlock được 1 tướng làm phần hoạt ảnh như trong brawl star khi unlock tướng"; học
// nhịp từ bản mổ D:/Ripper/BrawlStar/Analysis/unlock/BAO_CAO.md, chỉ lấy nhịp và cấu trúc, hình vẽ tay phẳng của PokiClash, không quầng
// sáng). Prefab Assets/04 Prefabs/Items/MoKhoaTuong (UiKit.heroUnlock, menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng hết"), canvas riêng trên mọi hộp.
// Vũ đạo một kiểu cho mọi bậc (60 khung/giây, khoá tuyến tính, nảy nhờ khoá vượt rồi về):
//   1. Tụ lực 0 → 1,0 s: nền mực xanh thẫm, vệt tốc độ dọc lặp 0,18 s, tướng là bóng đặc phóng 0,1 → 1,0 và trôi xuống 90, sao tụ vào;
//   2. Lấy đà 2 khung: co 1,0 → 0,83;
//   3. Bùng 1 khung: cắt cứng sang nền màu bậc + hoa văn sao trôi, chớp trắng 5 khung che chỗ cắt;
//   4. Lộ diện 0,3 s: tướng bật màu, kéo dọc 0,30 × 1,63 (7 khung) → 1 (6) → ép 1,10 × 0,94 (2) → 1 (3), đĩa giấy sau lưng nở theo;
//   5. Bố cục: tướng lên 230 (15 khung); bảng tin trượt từ phải vào sau 3 khung (10 khung, vượt 20, lùi 2); huy hiệu hệ hiện dần,
//      kéo dọc bay lên → rơi ép ngang → về; nút Tiếp nảy nhắc mỗi 3 giây.
// Bậc cao chồng thêm lớp (không đổi vũ đạo): Khá đĩa giấy sau lưng; Hiếm tia xoay; Sử thi thêm sao lấp lánh và lớp tia thứ hai;
// Huyền thoại thêm sao băng toả ra. Nền trơn màu bậc (người dùng 2026-11-23: "background bỏ mấy cái icon đi để nền trơn thôi").
// Tướng (người dùng 2026-11-23: "làm tướng xoay xoay liên tục rồi hiện ra play animation gì đó (ulti hoặc appear rồi idle), nhìn hình
// hơi vỡ"): rig .atomik / aola qua AolaSticker (ảnh chụp 2048 cho nét): pha tụ lực tướng là bóng tối quay quanh trục dọc 3 vòng nhanh
// dần, dừng ở mặt trước đúng lúc bùng; lộ diện diễn clip ra sân (không có thì chiêu cuối nếu không nhảy đè, không nữa thì đánh) rồi
// đứng. Rig nằm trong gói tải sau (GD_Claude/27) thì xin nạp ngay lúc mở màn (AolaActor.Ready), pha tụ lực tạm dùng bóng chân dung, tới
// lúc bùng mà gói đã về thì đổi sang rig; chưa về (máy chưa tải) thì chân dung (prefab kit ChanDung, luôn có trong bản cài).
using System;
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using Random = UnityEngine.Random;

namespace PokiClash
{
    public sealed class HeroUnlockView : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image dark, rarityBg, pattern, disc, rays, rays2, flash;
            public RectTransform speed, hero, spin, panel, badge; // spin: con của hero, quay quanh trục dọc
            public Image[] streaks, sparks, shooting;
            public Image badgeIcon, ribbon;
            public TextMeshProUGUI ribbonText, heroName, rarity, title, elem;
            public Image rarityPill;
            public SketchButton next, view;
            public Button catcher;
        }

        [SerializeField] Parts p;

        const float F = 1 / 60f; // một khung
        const float HeroH = 820;
        const float RigH = 560; // chiều cao dáng đứng của rig trên màn
        const float Charge = 1.2f; // pha tụ lực (giây)
        const float Turns = 3; // số vòng quay trong pha tụ lực
        static readonly Queue<(string hero, Action done)> queue = new Queue<(string, Action)>();
        public static bool Playing { get; private set; }

        bool tapped, closing;
        Vector2 heroHome, panelHome, badgeHome;
        int tier;
        float t0;
        AolaSticker rig;
        string rigClip = Game.AolaActor.Idle;
        float rigT, rigTint = 1;
        bool rigLoop = true;
        RectTransform spin; // khung quay quanh trục dọc (scale x = cos góc): p.spin, con của p.hero

        public void Setup(Parts parts) => p = parts;

        // xếp hàng: nhiều tướng mới cùng lúc thì lần lượt; done gọi khi tướng cuối đóng
        public static void Play(IEnumerable<string> heroes, Action done = null)
        {
            var list = new List<string>();
            foreach (var h in heroes)
                if (!string.IsNullOrEmpty(h) && App.Data.Hero(h) != null && !list.Contains(h)) list.Add(h);
            if (list.Count == 0)
            {
                done?.Invoke();
                return;
            }
            for (int i = 0; i < list.Count; i++) queue.Enqueue((list[i], i == list.Count - 1 ? done : null));
            if (!Playing) Next();
        }

        // tướng vừa mở khoá trong một lô thưởng (mảnh đủ mở khoá)
        public static List<string> Unlocked(IEnumerable<Reward> rewards)
        {
            var l = new List<string>();
            if (rewards == null) return l;
            foreach (var r in rewards)
                if (r != null && r.k == RewardKind.Shards && r.res != null && r.res.unlocked) l.Add(r.res.hero ?? r.hero);
            return l;
        }

        static void Next()
        {
            if (queue.Count == 0)
            {
                Playing = false;
                return;
            }
            var (hero, done) = queue.Dequeue();
            var prefab = Theme.Prefabs ? Theme.Prefabs.heroUnlock : null;
            if (!prefab)
            {
                done?.Invoke();
                Next();
                return;
            }
            Playing = true;
            var v = Ui.Spawn(prefab, App.Modals.transform);
            v.name = "mo_khoa_tuong";
            var rt = (RectTransform)v.transform;
            rt.Stretch();
            rt.SetAsLastSibling();
            App.I.StartCoroutine(v.Run(App.Data.Hero(hero), () =>
            {
                done?.Invoke();
                Next();
            }));
        }

        IEnumerator Run(HeroDef h, Action done)
        {
            tier = (int)h.rarity;
            var tc = Theme.Of(h.rarity);
            heroHome = p.hero.anchoredPosition;
            panelHome = p.panel.anchoredPosition;
            badgeHome = p.badge.anchoredPosition;
            p.catcher.onClick.AddListener(() => tapped = true);

            // dựng: rig (bóng = nhân màu tối) hoặc, chưa có rig, chân dung bóng đặc + chân dung màu thật cùng chỗ
            var form = HeroArt.FormOf(h).aola;
            spin = p.spin;
            bool hasForm = !string.IsNullOrEmpty(form);
            // Ready: dạng sẵn (đã đọc, atlas nạp, gói đã về) thì dựng rig ngay; chưa thì bắt đầu nạp, hỏi lại mỗi khung trong pha tụ lực
            rig = hasForm && Game.AolaActor.Ready(form) ? AolaSticker.TryCreate(spin, h, form, RigH, false, 2048) : null;
            RectTransform shadow = null, color = null;
            if (rig != null)
            {
                rigTint = 0.12f;
                rigClip = Game.AolaActor.Idle;
                rigLoop = true;
            }
            else
            {
                shadow = HeroArt.Portrait(spin, h, HeroH, true);
                color = HeroArt.Portrait(spin, h, HeroH, false);
                foreach (var r in new[] { shadow, color })
                {
                    r.anchorMin = r.anchorMax = new Vector2(0.5f, 0);
                    r.pivot = new Vector2(0.5f, 0);
                    r.anchoredPosition = Vector2.zero;
                }
                foreach (var g in shadow.GetComponentsInChildren<Graphic>()) g.color = new Color(0.13f, 0.2f, 0.42f, 1);
                color.gameObject.SetActive(false);
            }

            p.ribbonText.text = Loc.T("TƯỚNG MỚI!");
            p.heroName.text = h.name;
            p.rarity.text = Elements.RarityName(h.rarity).ToUpperInvariant();
            p.rarityPill.color = tc;
            p.rarity.color = tc.grayscale > 0.62f ? Theme.Ink : Color.white;
            p.title.text = h.title ?? "";
            p.elem.text = Elements.Name(h.elem);
            Theme.SetSprite(p.badgeIcon, App.Art.Icon(ElemIcon(h.elem)));
            p.rarityBg.color = Color.Lerp(tc, Theme.Ink, 0.25f);
            p.disc.color = Color.Lerp(tc, Color.white, 0.55f);
            p.rays.color = Color.Lerp(tc, Color.white, 0.35f);
            p.rays2.color = Color.Lerp(tc, Color.white, 0.6f);
            foreach (var s in p.sparks) s.color = Color.Lerp(tc, Color.white, 0.5f);

            // trạng thái đầu: pha tụ lực
            Show(p.dark, true);
            p.speed.gameObject.SetActive(true);
            foreach (var g in new Graphic[] { p.rarityBg, p.pattern, p.disc, p.rays, p.rays2 }) Show(g, false); // hoa văn: nền trơn, không bật
            foreach (var s in p.sparks) s.gameObject.SetActive(false);
            foreach (var s in p.shooting) s.gameObject.SetActive(false);
            p.panel.gameObject.SetActive(false);
            p.badge.gameObject.SetActive(false);
            p.next.gameObject.SetActive(false);
            p.view.gameObject.SetActive(false);
            p.flash.color = new Color(1, 1, 1, 0);

            // 1. tụ lực: bóng phóng 0,1 → 1,0, trôi xuống 90, quay quanh trục dọc nhanh dần (dừng ở mặt trước); sao tụ vào tâm
            App.Audio.Play("launch", 0.8f, 0.8f);
            Haptics.Play(Haptic.UiOpen);
            t0 = Time.unscaledTime;
            StartCoroutine(Gather(Charge));
            for (float t = 0; t < Charge; t += Time.unscaledDeltaTime)
            {
                float x = t / Charge;
                p.hero.localScale = Vector3.one * Mathf.Lerp(0.1f, 1, x);
                p.hero.anchoredPosition = heroHome + new Vector2(0, 90 * (1 - x));
                float ang = 360 * Turns * Mathf.Pow(x, 1.7f);
                spin.localScale = new Vector3(Mathf.Cos(ang * Mathf.Deg2Rad), 1, 1);
                if (rig == null && hasForm) Game.AolaActor.Ready(form); // đẩy việc nạp gói / đọc rig
                yield return null;
            }
            spin.localScale = Vector3.one;
            // 2. lấy đà 2 khung: co 1,0 → 0,83, tối thêm
            p.hero.anchoredPosition = heroHome;
            if (rig != null) rigTint = 0.06f;
            else foreach (var g in shadow.GetComponentsInChildren<Graphic>()) g.color = new Color(0.08f, 0.12f, 0.28f, 1);
            p.hero.localScale = Vector3.one * 0.91f;
            yield return Frames(1);
            p.hero.localScale = Vector3.one * 0.83f;
            yield return Frames(1);

            // 3. bùng: cắt cứng sang nền bậc, chớp trắng che chỗ cắt
            Show(p.dark, false);
            p.speed.gameObject.SetActive(false);
            Show(p.rarityBg, true);
            if (tier >= (int)Rarity.Uncommon) Show(p.disc, true);
            if (tier >= (int)Rarity.Rare) Show(p.rays, true);
            if (tier >= (int)Rarity.Epic) Show(p.rays2, true);
            StartCoroutine(Flash(0.95f, 5 * F));
            App.Audio.Play("chest");
            App.Audio.Play("stamp", 0.9f, 0.85f);
            Haptics.Play(tier >= (int)Rarity.Epic ? Haptic.OpenGold : Haptic.OpenSilver);
            // gói về trong pha tụ lực: đổi chân dung sang rig ngay lúc bùng (chớp trắng che chỗ đổi)
            if (rig == null && hasForm && Game.AolaActor.Ready(form))
            {
                rig = AolaSticker.TryCreate(spin, h, form, RigH, false, 2048);
                if (rig != null)
                {
                    if (shadow) shadow.gameObject.SetActive(false);
                    if (color) color.gameObject.SetActive(false);
                }
            }
            if (rig != null)
            {
                // bật màu, diễn clip ra sân (hoặc chiêu cuối / đánh) rồi đứng (Update)
                rigTint = 1;
                rigClip = rig.HasClip(Game.AolaActor.Appear) ? Game.AolaActor.Appear : !rig.Jumps ? StageView.Skill : StageView.Attack;
                rigT = 0;
                rigLoop = false;
            }
            else if (shadow && color)
            {
                shadow.gameObject.SetActive(false);
                color.gameObject.SetActive(true);
            }
            if (tier >= (int)Rarity.Epic) StartCoroutine(Twinkle());
            if (tier >= (int)Rarity.Legend) StartCoroutine(Shooting());

            // 4. lộ diện: kéo dọc → về → ép → về; đĩa sau lưng nở 1,22 → 1,75 rồi theo nhịp tướng
            yield return Keys(p.hero, new[] { V(1, 1), V(0.3f, 1.63f), V(1, 1), V(1.1f, 0.94f), V(1, 1) }, new[] { 0, 7, 13, 15, 18 }, p.disc.rectTransform,
                new[] { V(1.22f, 1.22f), V(0.55f, 0.55f), V(0.95f, 0.95f), V(1.05f, 1.05f), V(1, 1) });

            // 5. bố cục: tướng lên 230 trong 15 khung; bảng vào sau 3 khung: 10 khung, vượt 20, lùi 2
            StartCoroutine(Move(p.hero, heroHome, heroHome + new Vector2(0, 230), 15));
            StartCoroutine(Move(p.disc.rectTransform, p.disc.rectTransform.anchoredPosition, p.disc.rectTransform.anchoredPosition + new Vector2(0, 230), 15));
            StartCoroutine(Move(p.rays.rectTransform, p.rays.rectTransform.anchoredPosition, p.rays.rectTransform.anchoredPosition + new Vector2(0, 230), 15));
            StartCoroutine(Move(p.rays2.rectTransform, p.rays2.rectTransform.anchoredPosition, p.rays2.rectTransform.anchoredPosition + new Vector2(0, 230), 15));
            yield return Frames(3);
            p.panel.gameObject.SetActive(true);
            yield return Move(p.panel, panelHome + new Vector2(1170, 0), panelHome + new Vector2(-20, 0), 10);
            App.Audio.Play("whoosh", 0.6f, 1.2f);
            yield return Move(p.panel, panelHome + new Vector2(-20, 0), panelHome, 2);

            // huy hiệu hệ: hiện dần, kéo dọc bay lên → rơi ép ngang → về
            p.badge.gameObject.SetActive(true);
            p.badgeIcon.color = Color.white;
            StartCoroutine(Fade(p.badgeIcon, 0, 1, 7 * F));
            yield return KeysPos(p.badge, new[] { V(1, 1), V(1, 1.4f) }, new[] { badgeHome, badgeHome + new Vector2(0, 90) }, new[] { 0, 11 });
            App.Audio.Play("stamp");
            Haptics.Play(Haptic.Stamp);
            yield return KeysPos(p.badge, new[] { V(1, 1.4f), V(1.3f, 1), V(1, 1) }, new[] { badgeHome + new Vector2(0, 90), badgeHome + new Vector2(0, 50), badgeHome }, new[] { 0, 3, 7 });

            // nút
            p.next.gameObject.SetActive(true);
            p.next.SetText(Loc.T("Tiếp"));
            bool done2 = false, toHero = false;
            p.next.SetOnClick(() => done2 = true);
            p.view.gameObject.SetActive(App.Router != null);
            p.view.SetText(Loc.T("Xem tướng"));
            p.view.SetOnClick(() =>
            {
                toHero = true;
                done2 = true;
            });
            StartCoroutine(Pop(p.next.Rect));
            float nextNudge = Time.unscaledTime + 3;
            tapped = false;
            while (!done2)
            {
                if (Time.unscaledTime > nextNudge)
                {
                    nextNudge = Time.unscaledTime + 3;
                    StartCoroutine(Pop(p.next.Rect));
                }
                yield return null;
            }
            closing = true;
            for (float t = 0; t < 0.18f; t += Time.unscaledDeltaTime)
            {
                if (TryGetComponent<CanvasGroup>(out var cg)) cg.alpha = 1 - t / 0.18f;
                yield return null;
            }
            Playing = queue.Count > 0;
            rig?.Destroy();
            rig = null;
            Destroy(gameObject);
            if (toHero)
            {
                queue.Clear();
                App.Modals.CloseAll();
                App.Router.Go(SceneIds.Heroes);
            }
            done?.Invoke();
        }

        void OnDestroy()
        {
            rig?.Destroy();
            rig = null;
        }

        static string ElemIcon(Elem e) => e == Elem.Hoa ? "e_hoa" : e == Elem.Thuy ? "e_thuy" : e == Elem.Moc ? "e_moc" : e == Elem.Kim ? "e_kim" : "e_tho";

        static Vector2 V(float x, float y) => new Vector2(x, y);

        static void Show(Graphic g, bool on) => g.gameObject.SetActive(on);

        static IEnumerator Frames(int n)
        {
            for (float t = 0; t < n * F; t += Time.unscaledDeltaTime) yield return null;
        }

        // khoá tỉ lệ tuyến tính theo khung (60/giây); follow (nếu có) chạy khoá riêng cùng mốc
        static IEnumerator Keys(RectTransform rt, Vector2[] keys, int[] at, RectTransform follow = null, Vector2[] fkeys = null)
        {
            float total = at[at.Length - 1] * F;
            for (float t = 0; t < total; t += Time.unscaledDeltaTime)
            {
                float fr = t / F;
                int i = 0;
                while (i < at.Length - 2 && fr > at[i + 1]) i++;
                float k = Mathf.InverseLerp(at[i], at[i + 1], fr);
                var s = Vector2.Lerp(keys[i], keys[i + 1], k);
                rt.localScale = new Vector3(s.x, s.y, 1);
                if (follow && fkeys != null)
                {
                    var f = Vector2.Lerp(fkeys[i], fkeys[i + 1], k);
                    follow.localScale = new Vector3(f.x, f.y, 1);
                }
                yield return null;
            }
            rt.localScale = new Vector3(keys[keys.Length - 1].x, keys[keys.Length - 1].y, 1);
            if (follow && fkeys != null) follow.localScale = new Vector3(fkeys[fkeys.Length - 1].x, fkeys[fkeys.Length - 1].y, 1);
        }

        static IEnumerator KeysPos(RectTransform rt, Vector2[] scale, Vector2[] pos, int[] at)
        {
            float total = at[at.Length - 1] * F;
            for (float t = 0; t < total; t += Time.unscaledDeltaTime)
            {
                float fr = t / F;
                int i = 0;
                while (i < at.Length - 2 && fr > at[i + 1]) i++;
                float k = Mathf.InverseLerp(at[i], at[i + 1], fr);
                var s = Vector2.Lerp(scale[i], scale[i + 1], k);
                rt.localScale = new Vector3(s.x, s.y, 1);
                rt.anchoredPosition = Vector2.Lerp(pos[i], pos[i + 1], k);
                yield return null;
            }
            var e = scale[scale.Length - 1];
            rt.localScale = new Vector3(e.x, e.y, 1);
            rt.anchoredPosition = pos[pos.Length - 1];
        }

        static IEnumerator Move(RectTransform rt, Vector2 from, Vector2 to, int frames)
        {
            float d = frames * F;
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                rt.anchoredPosition = Vector2.Lerp(from, to, t / d);
                yield return null;
            }
            rt.anchoredPosition = to;
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

        static IEnumerator Fade(Graphic g, float from, float to, float d)
        {
            var c = g.color;
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                g.color = new Color(c.r, c.g, c.b, Mathf.Lerp(from, to, t / d));
                yield return null;
            }
            g.color = new Color(c.r, c.g, c.b, to);
        }

        static IEnumerator Pop(RectTransform rt)
        {
            // nảy nhắc 1 → 1,17 → 0,92 → 1 trong 0,25 s
            float[] at = { 0, 0.08f, 0.17f, 0.25f };
            float[] s = { 1, 1.17f, 0.92f, 1 };
            for (float t = 0; t < 0.25f; t += Time.unscaledDeltaTime)
            {
                int i = 0;
                while (i < at.Length - 2 && t > at[i + 1]) i++;
                rt.localScale = Vector3.one * Mathf.Lerp(s[i], s[i + 1], Mathf.InverseLerp(at[i], at[i + 1], t));
                yield return null;
            }
            rt.localScale = Vector3.one;
        }

        // sao tụ về tâm trong pha tụ lực (vẽ trên bóng tướng)
        IEnumerator Gather(float d)
        {
            var center = heroHome + new Vector2(0, HeroH * 0.45f);
            for (int i = 0; i < p.sparks.Length; i++)
            {
                var s = p.sparks[i];
                float ang = i * 360f / p.sparks.Length + Random.Range(-15f, 15f);
                StartCoroutine(GatherOne(s, center, ang, Random.Range(0, d * 0.5f), d * 0.5f));
            }
            yield break;
        }

        IEnumerator GatherOne(Image s, Vector2 center, float ang, float delay, float d)
        {
            for (float t = 0; t < delay; t += Time.unscaledDeltaTime) yield return null;
            var dir = new Vector2(Mathf.Cos(ang * Mathf.Deg2Rad), Mathf.Sin(ang * Mathf.Deg2Rad));
            s.gameObject.SetActive(true);
            var c = new Color(0.75f, 0.85f, 1, 1);
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                float x = t / d;
                s.rectTransform.anchoredPosition = center + dir * Mathf.Lerp(520, 20, x);
                s.rectTransform.localScale = Vector3.one * Mathf.Lerp(0.4f, 1.1f, x);
                s.rectTransform.localEulerAngles = new Vector3(0, 0, 180 * x);
                s.color = new Color(c.r, c.g, c.b, Mathf.Min(1, x * 3));
                yield return null;
            }
            s.gameObject.SetActive(false);
        }

        // Sử thi trở lên: sao lấp lánh so le quanh tướng (nở 0,25 s, co 0,4 s, chu kỳ 1,53 s)
        IEnumerator Twinkle()
        {
            var tc = Color.Lerp(Theme.Of((Rarity)tier), Color.white, 0.5f);
            int i = 0;
            while (!closing)
            {
                var s = p.sparks[i++ % p.sparks.Length];
                if (!s.gameObject.activeSelf) StartCoroutine(TwinkleOne(s, tc));
                for (float t = 0; t < 1.53f / p.sparks.Length * 2; t += Time.unscaledDeltaTime) yield return null;
            }
        }

        IEnumerator TwinkleOne(Image s, Color c)
        {
            s.gameObject.SetActive(true);
            s.color = c;
            s.rectTransform.anchoredPosition = p.hero.anchoredPosition + new Vector2(Random.Range(-380f, 380f), Random.Range(40f, HeroH + 80));
            for (float t = 0; t < 0.65f; t += Time.unscaledDeltaTime)
            {
                float k = t < 0.25f ? Mathf.Lerp(0.08f, 0.63f, t / 0.25f) : Mathf.Lerp(0.63f, 0, (t - 0.25f) / 0.4f);
                s.rectTransform.localScale = Vector3.one * k * 1.6f;
                yield return null;
            }
            s.gameObject.SetActive(false);
        }

        // Huyền thoại: sao băng bắn toả ra ngoài (0,67 → 1,64, bay xa 640–960 trong 2,7 s, so le 0,4 s)
        IEnumerator Shooting()
        {
            int i = 0;
            while (!closing)
            {
                var s = p.shooting[i++ % p.shooting.Length];
                if (!s.gameObject.activeSelf) StartCoroutine(ShootOne(s));
                for (float t = 0; t < 0.4f; t += Time.unscaledDeltaTime) yield return null;
            }
        }

        IEnumerator ShootOne(Image s)
        {
            s.gameObject.SetActive(true);
            float ang = Random.Range(0, 360f);
            var dir = new Vector2(Mathf.Cos(ang * Mathf.Deg2Rad), Mathf.Sin(ang * Mathf.Deg2Rad));
            float dist = Random.Range(640f, 960f);
            var from = p.hero.anchoredPosition + new Vector2(0, HeroH * 0.45f);
            s.rectTransform.localEulerAngles = new Vector3(0, 0, ang - 135); // đầu sao (góc trên trái của hình) đi trước
            s.color = Color.white;
            for (float t = 0; t < 2.7f && !closing; t += Time.unscaledDeltaTime)
            {
                float x = t / 2.7f;
                s.rectTransform.anchoredPosition = from + dir * dist * x;
                s.rectTransform.localScale = Vector3.one * Mathf.Lerp(0.67f, 1.64f, x);
                s.color = new Color(s.color.r, s.color.g, s.color.b, 1 - x * x);
                yield return null;
            }
            s.gameObject.SetActive(false);
        }

        void Update()
        {
            float dt = Time.unscaledDeltaTime;
            // rig: clip một lần (ra sân / chiêu cuối) xong thì đứng lặp
            if (rig != null)
            {
                rigT += dt;
                if (!rigLoop && rigT >= rig.Duration(rigClip))
                {
                    rigClip = Game.AolaActor.Idle;
                    rigT = 0;
                    rigLoop = true;
                }
                rig.Tint = rigTint;
                rig.Show(rigClip, rigT, rigLoop, 1, false, 0);
            }
            // vệt tốc độ dọc chạy xuống, lặp 0,18 s
            if (p.speed.gameObject.activeSelf)
            {
                float ph = ((Time.unscaledTime - t0) % 0.18f) / 0.18f;
                for (int i = 0; i < p.streaks.Length; i++)
                {
                    var r = p.streaks[i].rectTransform;
                    float off = (ph + i * 0.37f) % 1f;
                    r.anchoredPosition = new Vector2(r.anchoredPosition.x, Mathf.Lerp(1200, -1200, off));
                }
            }
            p.rays.rectTransform.Rotate(0, 0, -36 * dt);
            p.rays2.rectTransform.Rotate(0, 0, 22 * dt);
        }
    }
}
