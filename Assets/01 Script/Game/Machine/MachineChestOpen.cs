// Màn mở nhiều rương của máy bi (2026-11-10, chép màn mở capsule thú của máy tham khảo, số đo ở bản đục: prefab
// pbui_common_reward, clip *_in_new, bảng tổng kết pbui_a_view_pet_common_openall). Dựng bằng code lúc mở, phủ cả màn:
// - nền đen 0,8, tia sáng mềm xoay chậm, ruy băng tiêu đề đập vào trong 0,367 giây;
// - tối đa 5 rương một nhóm bay từ khay vào chỗ theo bố cục của máy đó (1: giữa; 2: hai bên; 3: tam giác; 4: 2 × 2; 5: ngũ giác),
//   đứng trên gối mây, lơ lửng, quầng sau rương thở 0,9 ↔ 1;
// - chạm một rương (hoặc "Mở tất cả": lần lượt cách 0,15 giây) thì mở theo clip 1,1 giây: lắc quanh đáy 0 / +7,1 / -2,5 … trong
//   0,25 giây (rương vàng 0,433 giây, cú cuối 10,2°) đồng thời nén 1 → 0,8; 0,3 giây phồng 1,2, nắp vọt lên (47, 274) nghiêng 45°,
//   thân rơi (26, -166) nghiêng -26°, hai mảnh mờ 0,367–0,433 giây rồi tắt; 0,317 giây chớp tròn (alpha 1 → 0 lúc 0,45, cỡ 0,98 →
//   1,79), vòng sóng (tắt 0,433), hạt; thưởng quý nhất của rương nảy ra (kéo 1 × 2,5, nảy 48, bẹt 1,3 × 0,9, 0,95 × 1,1, yên lúc 0,933);
// - mở hết thì bảng tổng kết: mọi thưởng của nhóm gộp thành ô, mỗi ô bật trong 0,667 giây (cỡ 0,76 → 1,18 → 1), quầng sau ô
//   0,217–0,267 giây, thẻ và mảnh lật từ thẻ úp tô màu độ hiếm; nút "Nhận" / "Mở tiếp (n)".
// Toạ độ của máy đó tính trên khung rộng 750, ở đây nhân theo bề rộng màn. Thưởng đã cộng vào bản lưu trước khi gọi.
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
    public sealed class MachineChestOpen : MonoBehaviour
    {
        public struct Item
        {
            public SlotKind kind;
            public int x;
            public List<Reward> rewards;
        }

        static readonly Vector2[][] Layout =
        {
            new[] { new Vector2(0, 28) },
            new[] { new Vector2(-170, 28), new Vector2(170, 28) },
            new[] { new Vector2(-170, 156), new Vector2(170, 156), new Vector2(0, -193) },
            new[] { new Vector2(-170, 156), new Vector2(170, 156), new Vector2(-180, -193), new Vector2(170, -193) },
            new[] { new Vector2(0, 438), new Vector2(-215, 155), new Vector2(-170, -192), new Vector2(170, -192), new Vector2(215, 155) },
        };
        static readonly float[] Shake = { 0, 7.1f, -2.5f, 7.1f, -2.5f, 7.1f, -2.5f };
        static readonly float[] ShakeGold = { 0, 7.1f, -2.5f, 7.1f, -2.5f, 7.1f, -4f, 10.2f, 0 };
        public const float RefW = 750, OpenAllGap = 0.15f;
        // nền đen 0,8 của máy tham khảo (hoà gamma); project hoà trong không gian linear nên cần 0,92 mới tối như vậy
        public const float Dim = 0.92f;

        sealed class Slot
        {
            public Item item;
            public RectTransform holder, chest;
            public Image closed, lid, body, glow, rays;
            public RewardTile tile;
            public bool opened, opening;
            public Vector2 home;
        }

        RectTransform root, layer;
        Image backdrop, raysBg;
        TextMeshProUGUI font;
        RewardTile tilePrefab;
        MachineFx fx;
        float k; // px màn cho 1 đơn vị khung 750
        readonly List<Slot> slots = new List<Slot>();
        bool done, closing;
        SketchButton openAll, confirm;
        float time;

        static Sprite S(string n) => MachineGlow.Sprite(n);
        static string Key(SlotKind k) => k == SlotKind.ChestGold ? "vang" : k == SlotKind.ChestSilver ? "bac" : "go";
        static int Tier(SlotKind k) => k == SlotKind.ChestGold ? 2 : k == SlotKind.ChestSilver ? 1 : 0;
        static Color TierColor(int t) => t >= 2 ? Theme.Hex("#ffd24a") : t == 1 ? Theme.Hex("#b98cff") : Theme.Hex("#7cc8ff");

        // mở một nhóm (tối đa 5) và chờ tới khi người chơi bấm nút cuối
        // đủ prefab (Items/MoRuongNhom, AnhMayBi, NutAnhMayBi) mới mở kiểu nhóm; thiếu thì máy mở từng hộp thoại rương như cũ
        public static bool Ready => MachineGlow.Prefabs.chestOpen && MachineGlow.Prefabs.image && MachineGlow.Prefabs.button;

        public static IEnumerator Play(RectTransform frame, List<Item> items, int left, Vector3 from, TextMeshProUGUI font, Image particle)
        {
            if (!Ready) yield break;
            var v = Ui.Spawn(MachineGlow.Prefabs.chestOpen, frame);
            v.name = "mo_ruong_nhom";
            v.Build(frame, items, font, particle);
            yield return v.Run(left, from);
            if (v) Destroy(v.gameObject);
        }

        void Build(RectTransform frame, List<Item> items, TextMeshProUGUI tmp, Image particle)
        {
            font = tmp;
            var dlg = Theme.Prefabs ? Theme.Prefabs.GetDialog<ChestDialog>() : null;
            tilePrefab = dlg ? dlg.TilePrefab : null;
            root = (RectTransform)transform;
            root.Stretch();
            root.localScale = Vector3.one;
            root.SetAsLastSibling();
            // canvas riêng (có sẵn trong prefab, kèm GraphicRaycaster) vẽ trên mọi canvas con của màn máy (lớp động của mặt máy có
            // canvas riêng)
            if (TryGetComponent<Canvas>(out var cv))
            {
                cv.overrideSorting = true;
                cv.sortingOrder = 400;
            }
            k = Mathf.Max(1, frame.rect.width / RefW);

            var btn = MachineGlow.NewButton("nen", root);
            backdrop = btn.image;
            backdrop.rectTransform.Stretch();
            backdrop.color = new Color(0, 0, 0, 0);
            backdrop.material = Theme.Plain;
            backdrop.raycastTarget = true; // chặn chạm xuống màn máy
            btn.onClick.AddListener(TapEmpty);

            raysBg = MachineGlow.Make("tia_nen", root, MachineGlow.Rays, MachineGlow.Hex("#ffe08a", 0));
            if (raysBg) raysBg.rectTransform.sizeDelta = Vector2.one * frame.rect.width * 1.5f;
            layer = New("lop", root);
            layer.Stretch();
            fx = new MachineFx(particle, layer);

            var n = Mathf.Clamp(items.Count, 1, 5);
            for (int i = 0; i < n; i++) slots.Add(MakeSlot(items[i], Vector2.Scale(Layout[n - 1][i], new Vector2(1, 0.8f)) * k + new Vector2(0, -60 * k))); // dọc nén 0,8 cho chừa chỗ ruy băng
        }

        RectTransform New(string name, Transform parent) => MachineGlow.NewRect(name, parent);

        Image Img(string name, Transform parent, Sprite s)
        {
            var img = MachineGlow.NewImage(name, parent);
            img.sprite = s;
            img.preserveAspect = s;
            img.raycastTarget = false;
            img.material = Theme.Plain;
            return img;
        }

        Slot MakeSlot(Item it, Vector2 home)
        {
            var s = new Slot { item = it, home = home };
            float w = 188 * k * 1.1f; // rương rộng như capsule (188 đơn vị khung 750) thêm chút
            s.holder = New("ruong", layer);
            s.holder.anchoredPosition = home;
            s.rays = MachineGlow.Make("tia", s.holder, MachineGlow.Rays, MachineGlow.A(TierColor(Tier(it.kind)), 0));
            if (s.rays) s.rays.rectTransform.sizeDelta = Vector2.one * w * 2.6f;
            s.glow = MachineGlow.Make("quang", s.holder, MachineGlow.Glow, MachineGlow.A(TierColor(Tier(it.kind)), 0.3f));
            if (s.glow) s.glow.rectTransform.sizeDelta = Vector2.one * w * 1.5f;
            var cloud = Img("may", s.holder, S("pk_may_do"));
            cloud.enabled = cloud.sprite;
            cloud.rectTransform.sizeDelta = new Vector2(w * 1.25f, w * 0.45f);
            cloud.rectTransform.anchoredPosition = new Vector2(0, -w * 0.42f);
            // rương: gốc ở đáy để lắc quanh đáy; nút trong suốt phủ rương, bấm thì mở
            var b = MachineGlow.NewButton("than_ruong", s.holder);
            b.onClick.AddListener(() => StartCoroutine(Open(s)));
            s.chest = (RectTransform)b.transform;
            s.chest.pivot = new Vector2(0.5f, 0);
            s.chest.anchoredPosition = new Vector2(0, -w * 0.4f);
            s.chest.sizeDelta = new Vector2(w, w * 0.8f);
            string key = Key(it.kind);
            var closedSprite = S("pk_ruong_" + key);
            if (closedSprite)
            {
                s.closed = Img("dong", s.chest, closedSprite);
                s.closed.rectTransform.Stretch();
            }
            else
            {
                var ic = MachineBoard.ChestIcon(s.chest, it.kind, w);
                ic.anchorMin = ic.anchorMax = new Vector2(0.5f, 0.5f);
                ic.anchoredPosition = Vector2.zero;
                s.closed = ic.GetComponentInChildren<Image>();
            }
            if (it.x > 1)
            {
                var tag = Ui.Spawn(font, s.holder);
                tag.text = "×" + it.x;
                tag.fontSize = 34 * k * 0.6f;
                tag.fontStyle = FontStyles.Bold;
                tag.color = Theme.Hex("#fff3c4");
                tag.outlineWidth = 0.2f;
                tag.outlineColor = Theme.Hex("#2B2118");
                tag.raycastTarget = false;
                tag.rectTransform.anchoredPosition = new Vector2(w * 0.45f, w * 0.35f);
            }
            s.holder.gameObject.SetActive(false);
            return s;
        }

        IEnumerator Run(int left, Vector3 from)
        {
            App.Audio.Play("whoosh");
            // nền và tia
            for (float t = 0; t < 0.2f; t += Time.unscaledDeltaTime)
            {
                backdrop.color = new Color(0, 0, 0, Dim * t / 0.2f);
                yield return null;
            }
            backdrop.color = new Color(0, 0, 0, Dim);
            StartCoroutine(Title(slots.Count > 1 ? $"Mở {slots.Count} rương" : "Mở rương"));
            // rương bay vào từ khay
            var start = (Vector2)root.InverseTransformPoint(from);
            for (int i = 0; i < slots.Count; i++) StartCoroutine(FlyIn(slots[i], start, i * 0.08f));
            yield return new WaitForSecondsRealtime(0.4f + slots.Count * 0.08f);
            if (slots.Count > 1) openAll = MakeButton("Mở tất cả", new Vector2(0, -560 * k * 0.95f), Theme.Yellow, OpenAll);
            // chờ mở hết
            while (slots.Any(q => !q.opened)) yield return null;
            if (openAll) openAll.gameObject.SetActive(false);
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Summary(left);
            while (!done) yield return null;
            closing = true;
            for (float t = 0; t < 0.2f; t += Time.unscaledDeltaTime)
            {
                float a = 1 - t / 0.2f;
                foreach (var g in root.GetComponentsInChildren<Graphic>()) g.canvasRenderer.SetAlpha(a);
                yield return null;
            }
        }

        IEnumerator Title(string text)
        {
            var holder = New("tieu_de", root);
            holder.anchoredPosition = new Vector2(0, 470 * k);
            var rib = Img("ruy_bang", holder, S("pk_ruy_bang"));
            rib.enabled = rib.sprite;
            rib.rectTransform.sizeDelta = new Vector2(520 * k, 158 * k);
            var t = Ui.Spawn(font, holder);
            t.text = text;
            t.alignment = TextAlignmentOptions.Center;
            t.fontSize = 44 * k * 0.95f;
            t.fontStyle = FontStyles.Bold;
            t.color = Color.white;
            t.outlineWidth = 0.2f;
            t.outlineColor = Theme.Hex("#2B2118");
            t.raycastTarget = false;
            t.rectTransform.sizeDelta = new Vector2(480 * k, 80 * k);
            t.rectTransform.anchoredPosition = new Vector2(0, 8 * k);
            // đập vào trong 0,367 giây: 1,6 → 0,92 → 1
            for (float x = 0; x < 0.367f; x += Time.unscaledDeltaTime)
            {
                float u = x / 0.367f;
                holder.localScale = Vector3.one * (u < 0.55f ? Mathf.Lerp(1.6f, 0.92f, u / 0.55f) : Mathf.Lerp(0.92f, 1, (u - 0.55f) / 0.45f));
                yield return null;
            }
            holder.localScale = Vector3.one;
        }

        IEnumerator FlyIn(Slot s, Vector2 start, float delay)
        {
            yield return new WaitForSecondsRealtime(delay);
            s.holder.gameObject.SetActive(true);
            App.Audio.Play("pick", 0.5f, 1.1f);
            var mid = (start + s.home) / 2 + new Vector2(0, 160 * k);
            for (float t = 0; t < 0.4f; t += Time.unscaledDeltaTime)
            {
                float u = t / 0.4f, e = 1 - (1 - u) * (1 - u);
                s.holder.anchoredPosition = (1 - e) * (1 - e) * start + 2 * (1 - e) * e * mid + e * e * s.home;
                s.holder.localScale = Vector3.one * (u < 0.75f ? Mathf.Lerp(0.35f, 1.12f, u / 0.75f) : Mathf.Lerp(1.12f, 1, (u - 0.75f) / 0.25f));
                yield return null;
            }
            s.holder.localScale = Vector3.one;
            s.holder.anchoredPosition = s.home;
            fx.Emit(MachineFx.RingHit, s.home + new Vector2(0, -60 * k * 0.6f), MachineFx.UnitBall * 0.9f);
        }

        void OpenAll()
        {
            if (openAll) openAll.gameObject.SetActive(false);
            StartCoroutine(OpenAllRun());
        }

        IEnumerator OpenAllRun()
        {
            foreach (var s in slots)
            {
                if (s.opened || s.opening) continue;
                StartCoroutine(Open(s));
                yield return new WaitForSecondsRealtime(OpenAllGap);
            }
        }

        void TapEmpty()
        {
            // chạm chỗ trống: chưa mở hết thì mở rương kế (như máy tham khảo chạm để đi tiếp)
            var next = slots.FirstOrDefault(q => !q.opened && !q.opening);
            if (next != null && !closing) StartCoroutine(Open(next));
        }

        IEnumerator Open(Slot s)
        {
            if (s.opened || s.opening) yield break;
            s.opening = true;
            int tier = Tier(s.item.kind);
            bool gold = tier >= 2;
            var col = TierColor(tier);
            App.Audio.Play("whoosh", 0.6f, 1.1f);
            // lắc quanh đáy và nén 1 → 0,8
            var keys = gold ? ShakeGold : Shake;
            float shake = gold ? 0.433f : 0.25f;
            for (float t = 0; t < shake; t += Time.unscaledDeltaTime)
            {
                float u = t / shake * (keys.Length - 1);
                int a = Mathf.Min(keys.Length - 2, (int)u);
                s.chest.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(keys[a], keys[a + 1], u - a));
                s.chest.localScale = Vector3.one * Mathf.Lerp(1, 0.8f, t / shake);
                yield return null;
            }
            s.chest.localEulerAngles = Vector3.zero;
            // phồng 1,2 trong 0,05 giây
            for (float t = 0; t < 0.05f; t += Time.unscaledDeltaTime)
            {
                s.chest.localScale = Vector3.one * Mathf.Lerp(0.8f, 1.2f, t / 0.05f);
                yield return null;
            }
            App.Audio.Play("chest");
            Haptics.Play(gold ? Haptic.OpenGold : tier == 1 ? Haptic.OpenSilver : Haptic.OpenWood);
            StartCoroutine(Pieces(s));
            StartCoroutine(Burst(s, col, tier));
            yield return Reveal(s, col);
            s.opened = true;
            s.opening = false;
        }

        // nắp vọt lên nghiêng 45°, thân rơi nghiêng -26°, mờ 0,367–0,433 giây (tính từ lúc mở 0,3), co về 0,3 rồi tắt
        IEnumerator Pieces(Slot s)
        {
            string key = Key(s.item.kind);
            var lidS = S($"pk_ruong_{key}_nap");
            var bodyS = S($"pk_ruong_{key}_than");
            var w = s.chest.sizeDelta.x;
            RectTransform lid = null, body = null;
            if (lidS && bodyS)
            {
                var closedSprite = s.closed ? s.closed.sprite : null;
                float sw = closedSprite ? closedSprite.rect.width : 320, sh = closedSprite ? closedSprite.rect.height : 260;
                float scale = w / sw;
                var bi = Img("than", s.holder, bodyS);
                bi.rectTransform.pivot = new Vector2(0.5f, 0);
                bi.rectTransform.sizeDelta = new Vector2(w, bodyS.rect.height * scale);
                bi.rectTransform.anchoredPosition = s.chest.anchoredPosition;
                var li = Img("nap", s.holder, lidS);
                li.rectTransform.pivot = new Vector2(0.5f, 0);
                li.rectTransform.sizeDelta = new Vector2(w, lidS.rect.height * scale);
                li.rectTransform.anchoredPosition = s.chest.anchoredPosition + new Vector2(0, Mathf.Max(0, sh - lidS.rect.height) * scale); // mép dưới nắp ở đường ghép của rương đóng
                lid = li.rectTransform;
                body = bi.rectTransform;
                s.lid = li;
                s.body = bi;
            }
            s.chest.gameObject.SetActive(false);
            if (!lid) yield break;
            Vector2 l0 = lid.anchoredPosition, b0 = body.anchoredPosition;
            var lTo = l0 + new Vector2(47, 274) * k;
            var bTo = b0 + new Vector2(26, -166) * k;
            for (float t = 0; t < 0.167f; t += Time.unscaledDeltaTime)
            {
                float u = Mathf.Min(1, t / 0.06f), e = 1 - (1 - u) * (1 - u);
                lid.anchoredPosition = Vector2.Lerp(l0, lTo, e);
                lid.localEulerAngles = new Vector3(0, 0, -45 * e);
                body.anchoredPosition = Vector2.Lerp(b0, bTo, e);
                body.localEulerAngles = new Vector3(0, 0, 26 * e);
                float f = Mathf.Clamp01((t - 0.067f) / 0.066f); // mờ 0,367–0,433
                float sc = Mathf.Lerp(1.2f, 0.3f, Mathf.Clamp01((t - 0.067f) / 0.1f));
                lid.localScale = body.localScale = Vector3.one * sc;
                s.lid.color = s.body.color = new Color(1, 1, 1, 1 - f);
                yield return null;
            }
            lid.gameObject.SetActive(false);
            body.gameObject.SetActive(false);
        }

        // chớp tròn, vòng sóng, hạt; rương quý thêm tia và lớp quầng
        IEnumerator Burst(Slot s, Color col, int tier)
        {
            var at = s.holder.anchoredPosition;
            float w = s.chest.sizeDelta.x;
            var flash = MachineGlow.Make("chop", s.holder, MachineGlow.Glow, Color.white);
            var wave = MachineGlow.Make("song", s.holder, MachineGlow.Ring, MachineGlow.A(col, 0.9f));
            fx.Emit(MachineFx.ChestHit(tier >= 2 ? 3 : 2), at, MachineFx.UnitBall * 0.35f * k);
            if (s.rays) StartCoroutine(Fade(s.rays, MachineGlow.A(col, tier >= 2 ? 0.4f : tier == 1 ? 0.25f : 0.15f), 0.3f));
            for (float t = 0; t < 0.15f; t += Time.unscaledDeltaTime)
            {
                float u = t / 0.133f;
                if (flash)
                {
                    flash.rectTransform.sizeDelta = Vector2.one * w * 1.8f * Mathf.Lerp(0.98f, 1.79f, Mathf.Min(1, u));
                    flash.color = new Color(1, 1, 1, Mathf.Max(0, 1 - u));
                }
                if (wave)
                {
                    float v = Mathf.Min(1, t / 0.116f);
                    wave.rectTransform.sizeDelta = Vector2.one * 1000 * k * Mathf.Lerp(0.15f, 1, 1 - (1 - v) * (1 - v));
                    wave.color = MachineGlow.A(col, 0.9f * (1 - v));
                }
                yield return null;
            }
            if (flash) Destroy(flash.gameObject);
            if (wave) Destroy(wave.gameObject);
        }

        IEnumerator Fade(Image img, Color to, float dur)
        {
            var from = img.color;
            for (float t = 0; t < dur && img; t += Time.unscaledDeltaTime)
            {
                img.color = Color.Lerp(from, to, t / dur);
                yield return null;
            }
            if (img) img.color = to;
        }

        // thưởng quý nhất nảy ra khỏi rương: kéo 1 × 2,5, nảy 48, bẹt 1,3 × 0,9, rồi 0,95 × 1,1, yên lúc 0,616 giây sau khi mở
        IEnumerator Reveal(Slot s, Color col)
        {
            if (!tilePrefab) yield break;
            var best = Best(s.item.rewards);
            if (best == null) yield break;
            var tiles = ChestDialog.BuildTiles(new List<Reward> { best }, tilePrefab, s.holder);
            if (tiles.Count == 0) yield break;
            var tile = s.tile = tiles[0];
            for (int i = 1; i < tiles.Count; i++) Destroy(tiles[i].gameObject);
            var rt = tile.Rect;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0);
            rt.sizeDelta = new Vector2(RewardTile.W, RewardTile.H);
            var y0 = s.chest.anchoredPosition.y;
            float baseS = k * 0.9f;
            // mốc (giây từ lúc bật, sx, sy, cao)
            float[] T = { 0, 0.15f, 0.36f, 0.48f, 0.616f };
            Vector3[] V = { new Vector3(0.4f, 1f, 0), new Vector3(1f, 1.15f, 48), new Vector3(1.3f, 0.9f, 0), new Vector3(0.95f, 1.1f, 0), new Vector3(1, 1, 0) };
            for (float t = 0; t < T[T.Length - 1]; t += Time.unscaledDeltaTime)
            {
                int a = 0;
                while (a < T.Length - 2 && t > T[a + 1]) a++;
                float u = (t - T[a]) / (T[a + 1] - T[a]);
                var v = Vector3.Lerp(V[a], V[a + 1], u);
                if (a == 0) v.y = Mathf.Lerp(2.5f * 0.4f, 1.15f, u); // kéo dài lúc bật
                rt.localScale = new Vector3(v.x, v.y, 1) * baseS;
                rt.anchoredPosition = new Vector2(0, y0 + v.z * k * Mathf.Sin(Mathf.Clamp01(t / 0.36f) * Mathf.PI));
                yield return null;
            }
            rt.localScale = Vector3.one * baseS;
            rt.anchoredPosition = new Vector2(0, y0);
        }

        static int Rank(Reward r)
        {
            switch (r.k)
            {
                case RewardKind.Shards: return 100 + (int)App.Data.Hero(r.res.hero).rarity * 10 + (r.res.unlocked ? 5 : 0);
                case RewardKind.Card: return 50 + (int)r.drop.rarity * 10;
                case RewardKind.Stones: return 40;
                case RewardKind.Balls: return 20;
                default: return 10;
            }
        }

        static Reward Best(List<Reward> rewards) => rewards == null || rewards.Count == 0 ? null : rewards.OrderByDescending(Rank).First();

        static Rarity? RarityOf(Reward r) =>
            r.k == RewardKind.Shards ? App.Data.Hero(r.res.hero).rarity : r.k == RewardKind.Card ? r.drop.rarity : r.k == RewardKind.Stones ? Rarity.Epic : (Rarity?)null;

        // bảng tổng kết: rương mờ đi, mọi thưởng của nhóm gộp thành lưới ô bật lần lượt
        IEnumerator Summary(int left)
        {
            foreach (var s in slots) StartCoroutine(Shrink(s.holder));
            yield return new WaitForSecondsRealtime(0.25f);
            var all = slots.SelectMany(q => q.item.rewards ?? new List<Reward>()).ToList();
            var grid = New("tong_ket", layer);
            var tiles = tilePrefab ? ChestDialog.BuildTiles(all, tilePrefab, grid) : new List<RewardTile>();
            int cols = Mathf.Min(4, Mathf.Max(1, tiles.Count)), rows = (tiles.Count + cols - 1) / cols;
            float cw = RewardTile.W + 40, ch = RewardTile.H + 40;
            float fit = Mathf.Min(1.25f, (root.rect.height * 0.62f) / Mathf.Max(1, rows * ch));
            grid.localScale = Vector3.one * fit;
            // ô theo thứ tự thưởng (thẻ, mảnh lật từ thẻ úp); thứ tự BuildTiles: XP, bi, đá, thẻ, mảnh
            var order = new List<Rarity?>();
            int exp = all.Count(q => q.k == RewardKind.Exp) > 0 ? 1 : 0, balls = all.Any(q => q.k == RewardKind.Balls) ? 1 : 0;
            int stones = all.Any(q => q.k == RewardKind.Stones) ? 1 : 0;
            for (int i = 0; i < exp + balls; i++) order.Add(null);
            if (stones > 0) order.Add(Rarity.Epic);
            foreach (var g in all.Where(q => q.k == RewardKind.Card).GroupBy(q => (q.drop.hero, q.drop.slot))) order.Add(g.First().drop.rarity);
            foreach (var r in all.Where(q => q.k == RewardKind.Shards)) order.Add(App.Data.Hero(r.res.hero).rarity);
            for (int i = 0; i < tiles.Count; i++)
            {
                int r = i / cols, c = i % cols;
                int inRow = Mathf.Min(cols, tiles.Count - r * cols);
                var rt = tiles[i].Rect;
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(RewardTile.W, RewardTile.H);
                rt.anchoredPosition = new Vector2((c - (inRow - 1) / 2f) * cw, ((rows - 1) / 2f - r) * ch);
                rt.localScale = Vector3.zero;
                var rar = i < order.Count ? order[i] : null;
                StartCoroutine(PopTile(grid, rt, rar, i * 0.09f));
            }
            yield return new WaitForSecondsRealtime(0.667f + tiles.Count * 0.09f);
            confirm = MakeButton(left > 0 ? $"Mở tiếp ({left})" : "Nhận", new Vector2(0, -560 * k * 0.95f), Theme.Yellow, () => done = true);
        }

        IEnumerator Shrink(RectTransform rt)
        {
            for (float t = 0; t < 0.25f && rt; t += Time.unscaledDeltaTime)
            {
                rt.localScale = Vector3.one * Mathf.Lerp(1, 0.5f, t / 0.233f);
                foreach (var g in rt.GetComponentsInChildren<Graphic>()) g.canvasRenderer.SetAlpha(1 - t / 0.25f);
                yield return null;
            }
            if (rt) rt.gameObject.SetActive(false);
        }

        // một ô tổng kết: quầng sau ô, cỡ 0,76 → 1,18 → 1 trong 0,667 giây; ô có độ hiếm lật từ thẻ úp tô màu độ hiếm
        IEnumerator PopTile(RectTransform grid, RectTransform rt, Rarity? rar, float delay)
        {
            yield return new WaitForSecondsRealtime(delay);
            var col = rar.HasValue ? Theme.Of(rar.Value) : Theme.Hex("#ffe08a");
            var halo = MachineGlow.Make("quang_o", grid, MachineGlow.Glow, MachineGlow.A(col, 0));
            if (halo)
            {
                halo.rectTransform.anchoredPosition = rt.anchoredPosition;
                halo.rectTransform.sizeDelta = Vector2.one * RewardTile.H * 1.9f;
                halo.rectTransform.SetSiblingIndex(rt.GetSiblingIndex());
            }
            Image back = null;
            var backS = S("pk_the_up");
            if (rar.HasValue && backS)
            {
                back = Img("the_up", rt, backS);
                back.preserveAspect = false;
                back.rectTransform.anchorMin = back.rectTransform.anchorMax = new Vector2(0.5f, 1);
                back.rectTransform.pivot = new Vector2(0.5f, 1);
                back.rectTransform.sizeDelta = new Vector2(RewardTile.Frame, RewardTile.Frame);
                back.rectTransform.anchoredPosition = Vector2.zero;
                back.color = Color.Lerp(Color.white, col, 0.65f);
            }
            App.Audio.Play("pick", 0.45f, 1 + delay * 0.4f);
            for (float t = 0; t < 0.667f; t += Time.unscaledDeltaTime)
            {
                float s = t < 0.2f ? Mathf.Lerp(0.76f, 1.18f, t / 0.2f) : t < 0.4f ? Mathf.Lerp(1.18f, 1f, (t - 0.2f) / 0.2f) : 1;
                float sx = s;
                if (back)
                {
                    // lật: 0,25–0,4 giây thẻ úp hẹp lại, đổi sang mặt ô, mở ra lại
                    float f = Mathf.Clamp01((t - 0.25f) / 0.15f);
                    sx *= Mathf.Abs(Mathf.Cos(f * Mathf.PI));
                    if (f >= 0.5f && back.gameObject.activeSelf)
                    {
                        back.gameObject.SetActive(false);
                        fx.Emit(MachineFx.RingHit, (Vector2)layer.InverseTransformPoint(rt.position), MachineFx.UnitBall * 0.8f, col);
                    }
                }
                rt.localScale = new Vector3(sx, s, 1);
                if (halo) halo.color = MachineGlow.A(col, t < 0.217f ? 0 : Mathf.Min(0.6f, (t - 0.217f) / 0.05f * 0.6f));
                yield return null;
            }
            if (back) back.gameObject.SetActive(false);
            rt.localScale = Vector3.one;
        }

        SketchButton MakeButton(string text, Vector2 at, Color color, Action click)
        {
            var prefab = Theme.Prefabs ? Theme.Prefabs.buttonBig : null;
            if (!prefab) return null;
            var b = Ui.Spawn(prefab, root);
            b.name = "nut_" + text;
            var rt = b.Rect;
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = at;
            b.SetText(text);
            b.SetColor(color);
            b.SetOnClick(click);
            StartCoroutine(ChestBox.Pop(rt, 1.15f));
            return b;
        }

        void Update()
        {
            float dt = Time.unscaledDeltaTime;
            time += dt;
            fx?.Update(dt);
            if (raysBg)
            {
                raysBg.rectTransform.localEulerAngles = new Vector3(0, 0, -time * 10);
                if (!closing) raysBg.color = MachineGlow.Hex("#ffe08a", Mathf.Min(0.07f, time * 0.2f));
            }
            for (int i = 0; i < slots.Count; i++)
            {
                var s = slots[i];
                if (!s.holder || !s.holder.gameObject.activeSelf) continue;
                // lơ lửng (chưa mở, không đang bay vào) và quầng thở 0,9 ↔ 1 (chu kỳ của máy đó: 1,75 giây lên, 4,25 giây về)
                if (!s.opening && !s.opened && s.holder.localScale.x >= 0.999f)
                    s.chest.anchoredPosition = new Vector2(0, -s.chest.sizeDelta.x * 0.4f + Mathf.Sin(time * 3.9f + i * 1.3f) * 7 * k);
                if (s.glow)
                {
                    float ph = time % 6f;
                    float g = ph < 1.75f ? Mathf.Lerp(0.9f, 1, ph / 1.75f) : Mathf.Lerp(1, 0.9f, (ph - 1.75f) / 4.25f);
                    s.glow.rectTransform.localScale = Vector3.one * g;
                }
                if (s.rays) s.rays.rectTransform.localEulerAngles = new Vector3(0, 0, time * 25);
            }
        }
    }
}
