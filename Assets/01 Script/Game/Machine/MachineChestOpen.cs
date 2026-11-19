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
// Làm đẹp lại 2026-11-19 (chủ dự án dặn "fx mở rương phải đẹp"), tô phẳng theo luật hiệu ứng không quầng, hình vẽ tay gen Magnific
// (ArtGen/Pachinko/cat_magnific.py: pk_fx_hao_quang, pk_fx_quat_sang, pk_fx_bung, pk_fx_vong_giot, giấy màu, xu, ngọc, rương mở sạch):
// - rương đóng đứng trước vầng tia phẳng màu bậc rương xoay chậm (thay quầng mềm), đáp xuống thì phụt bụi;
// - chạm: gồng (lắc mạnh dần, nén 0,86 × 1,06, nhún nhảy nhỏ; rương vàng gồng lâu hơn), lấp lánh hút vào rương, vầng tia đậm dần;
// - bật nắp: đổi sang rương mở (nắp ngửa, lòng sáng kem), bóp giãn 1,25 × 0,8 → 0,9 × 1,15 → 1; loé gai, vòng dày, vòng giọt lan ra,
//   quạt sáng vọt lên từ lòng rương, giấy màu nhiều màu bắn lên rồi rơi, giọt sáng toả, sao; rương bạc thêm xu, rương vàng thêm xu,
//   ngọc, đợt pháo thứ hai và cả màn giật nhẹ;
// - thưởng quý nhất vọt ra từ lòng rương lên trên rương (kéo dài, nảy, bẹt rồi đứng), vầng tia chuyển lên sau thưởng.
// Hạt (Items/HatMayBi) neo góc trên trái nên mọi điểm phát đổi qua Fx() trước khi phát.
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
        public const float Dim = 0.95f; // 2026-11-19: tối hơn chút cho rương, giấy màu nổi (0,92 vẫn thấy rõ mặt máy phía sau)

        sealed class Slot
        {
            public Item item;
            public RectTransform holder, chest;
            public Image closed, lid, body, glow, rays, fan;
            public RewardTile tile;
            public bool opened, opening, landed;
            public Vector2 home;
            public float raysA; // alpha vầng tia đang muốn (Update chạy tới)
            public Vector2 raysAt; // chỗ vầng tia muốn tới (giữa rương, rồi sau thưởng)
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

            // vầng tia phẳng lớn sau cả màn (thay tia sáng mềm), xoay chậm, rất nhạt
            raysBg = Flat("tia_nen", root, Sun, MachineGlow.Hex("#ffe08a", 0));
            if (raysBg) raysBg.rectTransform.sizeDelta = Vector2.one * frame.rect.width * 1.6f;
            layer = New("lop", root);
            layer.Stretch();
            fx = new MachineFx(particle, layer);

            var n = Mathf.Clamp(items.Count, 1, 5);
            for (int i = 0; i < n; i++) slots.Add(MakeSlot(items[i], Vector2.Scale(Layout[n - 1][i], new Vector2(1, 0.8f)) * k + new Vector2(0, -60 * k))); // dọc nén 0,8 cho chừa chỗ ruy băng
        }

        RectTransform New(string name, Transform parent) => MachineGlow.NewRect(name, parent);

        // hình hiệu ứng phẳng gen Magnific (cat_magnific.py); thiếu thì dùng hình cũ cùng vai
        const string Sun = "pk_fx_hao_quang", SunOld = "pk_fx_tia_toa", Fan = "pk_fx_quat_sang", FanOld = "pk_o_sang_ruong", Pop = "pk_fx_bung",
            PopOld = "pk_fx_loe", Drops = "pk_fx_vong_giot";

        // ảnh phẳng tô màu (không cộng sáng), lấy tên dự phòng nếu chưa có ảnh mới; null nếu thiếu cả hai
        Image Flat(string name, Transform parent, string sprite, Color color)
        {
            string use = S(sprite) ? sprite : sprite == Sun ? SunOld : sprite == Fan ? FanOld : sprite == Pop ? PopOld : sprite == Drops ? "pk_fx_vong_dut" : sprite;
            var img = MachineGlow.Make(name, parent, use, color, false);
            if (img)
            {
                img.raycastTarget = false;
                img.preserveAspect = true;
                img.material = Theme.Plain;
            }
            return img;
        }

        // điểm trong lớp (gốc giữa) → toạ độ neo của hạt (Items/HatMayBi neo góc trên trái)
        Vector2 Fx(Vector2 local)
        {
            var r = layer.rect;
            return new Vector2(local.x - r.xMin, local.y - r.yMax);
        }

        Vector2 Local(RectTransform rt, Vector2 offset) => (Vector2)layer.InverseTransformPoint(rt.TransformPoint(offset));

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
            // vầng tia phẳng màu bậc rương sau rương: nhạt lúc chờ, đậm lên khi gồng, chuyển lên sau thưởng khi mở
            int tier = Tier(it.kind);
            // màu hoà trong không gian linear: alpha thấp trông đậm hơn số ghi, nên để nhạt
            s.raysA = tier >= 2 ? 0.16f : tier == 1 ? 0.12f : 0.09f;
            s.raysAt = new Vector2(0, -w * 0.05f);
            s.rays = Flat("tia", s.holder, Sun, MachineGlow.A(TierColor(tier), 0));
            if (s.rays)
            {
                s.rays.rectTransform.sizeDelta = Vector2.one * w * 1.5f;
                s.rays.rectTransform.anchoredPosition = s.raysAt;
            }
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
            // đáp: bụi phụt hai bên chân rương, rương bẹt nhẹ rồi đứng
            float w = s.chest.sizeDelta.x;
            fx.Emit(Dust, Fx(Local(s.chest, new Vector2(0, w * 0.05f))), w);
            for (float t = 0; t < 0.22f; t += Time.unscaledDeltaTime)
            {
                float u = t / 0.22f, q = Mathf.Sin(u * Mathf.PI) * (1 - u);
                s.chest.localScale = new Vector3(1 + 0.18f * q, 1 - 0.16f * q, 1);
                yield return null;
            }
            s.chest.localScale = Vector3.one;
            s.landed = true;
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
            // bấm lúc rương còn bay vào: chờ đáp xong mới gồng
            for (float t = 0; !s.landed && t < 1.5f; t += Time.unscaledDeltaTime) yield return null;
            int tier = Tier(s.item.kind);
            bool gold = tier >= 2;
            var col = TierColor(tier);
            float w = s.chest.sizeDelta.x;
            App.Audio.Play("whoosh", 0.6f, 1.1f);
            // 1. gồng: lắc quanh đáy mạnh dần (theo nhịp lắc của máy tham khảo, biên độ tăng), nén 1 → 0,86 × 1,06 và nhún nhảy
            // nhỏ; lấp lánh hút vào lòng rương; vầng tia đậm dần
            var keys = gold ? ShakeGold : Shake;
            float shake = gold ? 0.6f : tier == 1 ? 0.45f : 0.36f;
            s.raysA = gold ? 0.3f : 0.24f;
            float suck = 0;
            for (float t = 0; t < shake; t += Time.unscaledDeltaTime)
            {
                float u = t / shake, grow = 0.55f + 0.75f * u;
                float ku = u * (keys.Length - 1);
                int a = Mathf.Min(keys.Length - 2, (int)ku);
                s.chest.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(keys[a], keys[a + 1], ku - a) * grow);
                float hop = Mathf.Abs(Mathf.Sin(u * Mathf.PI * (gold ? 4 : 3))) * w * 0.035f * u;
                s.chest.anchoredPosition = new Vector2(0, -w * 0.4f + hop);
                s.chest.localScale = new Vector3(Mathf.Lerp(1, 1.06f, u), Mathf.Lerp(1, 0.86f, u), 1);
                if ((suck += Time.unscaledDeltaTime) > (gold ? 0.05f : 0.07f))
                {
                    suck = 0;
                    SuckIn(s, col, w);
                }
                yield return null;
            }
            s.chest.localEulerAngles = Vector3.zero;
            s.chest.anchoredPosition = new Vector2(0, -w * 0.4f);
            App.Audio.Play("chest");
            Haptics.Play(gold ? Haptic.OpenGold : tier == 1 ? Haptic.OpenSilver : Haptic.OpenWood);
            // 2. bật nắp: có ảnh rương mở sạch thì đổi ảnh và bóp giãn; thiếu thì nắp, thân bay ra như capsule (bản cũ)
            var openS = S($"pk_ruong_{Key(s.item.kind)}_mo_sach");
            if (openS && s.closed)
            {
                s.closed.sprite = openS;
                StartCoroutine(Squash(s.chest));
            }
            else StartCoroutine(Pieces(s));
            StartCoroutine(Burst(s, col, tier));
            if (gold) StartCoroutine(Jolt(14 * k * 0.6f));
            else if (tier == 1) StartCoroutine(Jolt(6 * k * 0.6f));
            yield return Reveal(s, col);
            s.opened = true;
            s.opening = false;
        }

        // một lấp lánh xuất hiện quanh rương rồi lao vào lòng rương (gồng trước khi bật)
        void SuckIn(Slot s, Color col, float w)
        {
            var c = Local(s.chest, new Vector2(0, w * 0.45f));
            float ang = UnityEngine.Random.Range(0f, 360f), r = w * UnityEngine.Random.Range(0.75f, 1.1f), life = 0.22f;
            var from = c + new Vector2(Mathf.Cos(ang * Mathf.Deg2Rad), Mathf.Sin(ang * Mathf.Deg2Rad)) * r;
            fx.Emit(new MachineFx.Burst
            {
                sprite = "pk_fx_tinh_tu", life = life, size = 0.16f, sizeMax = 0.24f, speed = r / w / life, dir = ang + 180, rotRange = 20,
                curve = new[] { 0, 0.3f, 0.3f, 1f, 1, 0.4f }, from = Color.white, to = Color.Lerp(Color.white, col, 0.6f), fadeAt = 0.75f,
            }, Fx(from), w);
        }

        // rương mở bóp giãn quanh đáy: 1,25 × 0,8 → 0,9 × 1,15 → 1,04 × 0,97 → 1 trong 0,36 giây
        IEnumerator Squash(RectTransform rt)
        {
            float[] T = { 0, 0.06f, 0.16f, 0.26f, 0.36f };
            Vector2[] V = { new Vector2(1.25f, 0.8f), new Vector2(1.25f, 0.8f), new Vector2(0.9f, 1.15f), new Vector2(1.04f, 0.97f), Vector2.one };
            for (float t = 0; t < T[T.Length - 1] && rt; t += Time.unscaledDeltaTime)
            {
                int a = 0;
                while (a < T.Length - 2 && t > T[a + 1]) a++;
                float u = (t - T[a]) / (T[a + 1] - T[a]);
                u = u * u * (3 - 2 * u);
                var v = Vector2.Lerp(V[a], V[a + 1], u);
                rt.localScale = new Vector3(v.x, v.y, 1);
                yield return null;
            }
            if (rt) rt.localScale = Vector3.one;
        }

        // cả lớp giật nhẹ (rương bạc, vàng): lệch ngẫu nhiên giảm dần trong 0,3 giây
        IEnumerator Jolt(float amp)
        {
            for (float t = 0; t < 0.3f && layer; t += Time.unscaledDeltaTime)
            {
                float d = amp * (1 - t / 0.3f);
                layer.anchoredPosition = new Vector2(UnityEngine.Random.Range(-d, d), UnityEngine.Random.Range(-d, d));
                yield return null;
            }
            if (layer) layer.anchoredPosition = Vector2.zero;
        }

        // nắp vọt lên nghiêng 45°, thân rơi nghiêng -26°, mờ 0,367–0,433 giây (tính từ lúc mở 0,3), co về 0,3 rồi tắt
        // (chỉ dùng khi chưa có ảnh rương mở sạch)
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

        // bật nắp: loé gai, vòng dày, vòng giọt, quạt sáng từ lòng rương, giấy màu, giọt sáng, sao; bạc thêm xu; vàng thêm xu, ngọc,
        // đợt pháo thứ hai. Mọi hình đều phẳng (không cộng sáng)
        IEnumerator Burst(Slot s, Color col, int tier)
        {
            float w = s.chest.sizeDelta.x;
            var mouth = Local(s.chest, new Vector2(0, w * 0.5f)); // lòng rương (rương cao 0,8 w, gốc ở đáy)
            var at = Fx(mouth);
            var pale = Color.Lerp(Color.white, col, 0.35f);
            fx.Emit(OpenFlash, at, w, pale);
            fx.Emit(OpenRing, at, w, col);
            fx.Emit(OpenSparks, at, w, Color.Lerp(Color.white, col, 0.5f));
            foreach (var c in Confetti) fx.Emit(ConfettiBurst(tier), at, w, c);
            if (tier >= 1) fx.Emit(Coins(tier), at, w);
            if (tier >= 2) fx.Emit(Gems, at, w);
            // quạt sáng vọt lên từ lòng rương, đứng lại sau thưởng, thở nhẹ
            s.fan = Flat("quat", s.holder, Fan, MachineGlow.A(pale, 0.9f));
            if (s.fan)
            {
                var frt = s.fan.rectTransform;
                frt.pivot = new Vector2(0.5f, 0.04f);
                frt.anchoredPosition = (Vector2)s.holder.InverseTransformPoint(s.chest.TransformPoint(new Vector2(0, w * 0.48f)));
                frt.sizeDelta = new Vector2(w * 1.15f, w * 1.0f);
                frt.SetSiblingIndex(s.chest.GetSiblingIndex()); // sau rương: quạt mọc từ lòng rương lên
                StartCoroutine(FanRise(frt));
            }
            if (tier >= 2)
            {
                yield return new WaitForSecondsRealtime(0.16f);
                var hi = Fx(mouth + new Vector2(0, w * 0.6f));
                fx.Emit(OpenFlash, hi, w * 0.7f, MachineGlow.Hex("#fff3b0"));
                foreach (var c in Confetti) fx.Emit(ConfettiBurst(1), hi, w * 0.9f, c);
                fx.Emit(OpenSparks, hi, w * 0.8f, MachineGlow.Hex("#ffe27a"));
                App.Audio.Play("coin", 0.7f, 1.2f);
            }
        }

        // quạt sáng: dài ra 0 → 1,12 → 1 trong 0,3 giây rồi thở 0,96 ↔ 1,04
        IEnumerator FanRise(RectTransform rt)
        {
            for (float t = 0; rt; t += Time.unscaledDeltaTime)
            {
                float y = t < 0.18f ? Mathf.Lerp(0, 1.12f, t / 0.18f) : t < 0.3f ? Mathf.Lerp(1.12f, 1, (t - 0.18f) / 0.12f) : 1 + 0.04f * Mathf.Sin((t - 0.3f) * 5);
                float x = t < 0.18f ? Mathf.Lerp(0.6f, 1, t / 0.18f) : 1;
                rt.localScale = new Vector3(x, y, 1);
                yield return null;
            }
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

        // thưởng quý nhất vọt ra từ lòng rương lên trên rương: kéo 0,4 × 1,0 → 1 × 1,15 (vọt lên), bẹt 1,3 × 0,9 khi dừng, 0,95 × 1,1,
        // đứng lúc 0,62 giây; vầng tia chuyển lên sau thưởng; tới đỉnh thì loé nhỏ
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
            float w = s.chest.sizeDelta.x;
            float y0 = s.chest.anchoredPosition.y + w * 0.42f; // lòng rương
            float y1 = s.chest.anchoredPosition.y + w * 0.62f; // đứng trên rương
            float baseS = k * 0.9f;
            s.raysAt = new Vector2(0, y1 + RewardTile.H * baseS * 0.5f);
            float[] T = { 0, 0.18f, 0.36f, 0.48f, 0.62f };
            Vector3[] V = { new Vector3(0.4f, 1f, 0), new Vector3(1f, 1.15f, 1.18f), new Vector3(1.3f, 0.9f, 1), new Vector3(0.95f, 1.1f, 1), new Vector3(1, 1, 1) };
            bool popped = false;
            for (float t = 0; t < T[T.Length - 1]; t += Time.unscaledDeltaTime)
            {
                int a = 0;
                while (a < T.Length - 2 && t > T[a + 1]) a++;
                float u = (t - T[a]) / (T[a + 1] - T[a]);
                if (a == 0) u = 1 - (1 - u) * (1 - u); // vọt nhanh rồi chậm
                var v = Vector3.Lerp(V[a], V[a + 1], u);
                rt.localScale = new Vector3(v.x, v.y, 1) * baseS;
                rt.anchoredPosition = new Vector2(0, Mathf.LerpUnclamped(y0, y1, v.z));
                if (!popped && t >= T[1])
                {
                    popped = true;
                    fx.Emit(TilePop, Fx(Local(rt, new Vector2(0, RewardTile.H * 0.5f))), w, Color.Lerp(Color.white, col, 0.4f));
                }
                yield return null;
            }
            rt.localScale = Vector3.one * baseS;
            rt.anchoredPosition = new Vector2(0, y1);
        }

        // ---------- bộ hạt mở rương (unit = bề rộng rương) ----------

        static Color Hc(string hex) => MachineGlow.Hex(hex, 1);

        // giấy màu: mỗi màu một loạt (tint nhân vào hình trắng)
        static readonly Color[] Confetti = { Hc("#ff8fb3"), Hc("#ffd24a"), Hc("#7cc8ff"), Hc("#8fe0b0"), Hc("#c49bff") };

        static readonly MachineFx.Burst[] Dust =
        {
            new MachineFx.Burst { sprite = "pk_fx_bui", count = 3, life = 0.35f, lifeMax = 0.5f, size = 0.16f, sizeMax = 0.24f, speed = 0.5f, speedMax = 0.9f, dir = 180, arc = 30,
                dampen = 0.25f, curve = new[] { 0, 0.5f, 0.3f, 1f, 1, 1.15f }, from = Color.white, to = Hc("#f3e6d0"), fadeAt = 0.4f, spin = true },
            new MachineFx.Burst { sprite = "pk_fx_bui", count = 3, life = 0.35f, lifeMax = 0.5f, size = 0.16f, sizeMax = 0.24f, speed = 0.5f, speedMax = 0.9f, dir = 0, arc = 30,
                dampen = 0.25f, curve = new[] { 0, 0.5f, 0.3f, 1f, 1, 1.15f }, from = Color.white, to = Hc("#f3e6d0"), fadeAt = 0.4f, spin = true },
        };

        // loé gai to co nhanh, loé nhỏ trắng ở giữa
        static readonly MachineFx.Burst[] OpenFlash =
        {
            new MachineFx.Burst { sprite = Pop, life = 0.22f, size = 1.5f, curve = new[] { 0, 0.5f, 0.25f, 1.15f, 1, 1.3f }, from = Color.white, to = Color.white, fadeAt = 0.35f, spin = true },
            new MachineFx.Burst { sprite = "pk_fx_lap_lanh_beo", life = 0.18f, size = 0.7f, curve = new[] { 0, 0.3f, 0.3f, 1.1f, 1, 0.6f }, from = Color.white, to = Color.white, fadeAt = 0.5f, rotRange = 10 },
        };

        // vòng dày và vòng giọt lan ra
        static readonly MachineFx.Burst[] OpenRing =
        {
            new MachineFx.Burst { sprite = "pk_fx_vong_day", life = 0.3f, size = 2.4f, curve = new[] { 0, 0.2f, 1, 1f }, from = Color.white, to = Color.white, fadeAt = 0.45f },
            new MachineFx.Burst { sprite = Drops, life = 0.32f, size = 2.0f, curve = new[] { 0, 0.3f, 1, 1.2f }, from = Color.white, to = Color.white, fadeAt = 0.5f, spin = true },
        };

        // giọt sáng bắn toả (kéo dài theo hướng bay), lấp lánh, sao
        static readonly MachineFx.Burst[] OpenSparks =
        {
            new MachineFx.Burst { sprite = "pk_fx_giot", count = 10, life = 0.22f, lifeMax = 0.34f, size = 0.32f, sizeMax = 0.5f, speed = 5, speedMax = 8, arc = 360, dampen = 0.35f,
                stretch = 1.6f, thin = 0.4f, curve = new[] { 0, 1f, 1, 0.3f }, from = Color.white, to = Color.white, fadeAt = 0.6f },
            new MachineFx.Burst { sprite = "pk_fx_tinh_tu", count = 6, life = 0.35f, lifeMax = 0.6f, size = 0.12f, sizeMax = 0.24f, speed = 1, speedMax = 2.8f, arc = 360, radius = 0.3f,
                dampen = 0.3f, curve = new[] { 0, 0.2f, 0.25f, 1.1f, 1, 0.3f }, from = Color.white, to = Color.white, fadeAt = 0.6f, rotSpeed = 120 },
            new MachineFx.Burst { sprite = "fx_star", count = 4, life = 0.45f, lifeMax = 0.7f, size = 0.14f, sizeMax = 0.22f, speed = 2.5f, speedMax = 4.5f, dir = 90, arc = 150,
                grav = 0.5f, spin = true, rotSpeed = 300, curve = new[] { 0, 0.4f, 0.2f, 1, 1, 0.6f }, from = Hc("#ffe27a"), to = Hc("#ffb000"), fadeAt = 0.7f },
        };

        // giấy màu bắn lên theo quạt rồi rơi, xoay; mỗi màu gọi một lần (ít hơn ở rương gỗ)
        static MachineFx.Burst[] ConfettiBurst(int tier)
        {
            int n = tier >= 2 ? 3 : tier == 1 ? 2 : 1;
            MachineFx.Burst B(string sp, int c, float s0, float s1) => new MachineFx.Burst
            {
                sprite = sp, count = c, life = 0.8f, lifeMax = 1.25f, size = s0, sizeMax = s1, speed = 3.5f, speedMax = 7f, dir = 90, arc = 120, radius = 0.15f,
                grav = 0.9f, limit = 1.2f, dampen = 0.12f, spin = true, rotSpeed = 420, curve = new[] { 0, 0.5f, 0.12f, 1f, 1, 0.85f }, fadeAt = 0.75f,
            };
            return new[]
            {
                B("pk_fx_giay_dai", n, 0.1f, 0.15f),
                B("pk_fx_giay_vuong", n, 0.06f, 0.09f),
                B("pk_fx_giay_tron", Mathf.Max(1, n - 1), 0.05f, 0.08f),
                B("pk_fx_day_xoan", tier >= 1 ? 1 : 0, 0.14f, 0.2f),
            };
        }

        // xu vàng bắn lên, lật (xen hình xu nghiêng), rơi
        static MachineFx.Burst[] Coins(int tier)
        {
            int n = tier >= 2 ? 5 : 3;
            MachineFx.Burst B(string sp, int c) => new MachineFx.Burst
            {
                sprite = sp, count = c, life = 0.75f, lifeMax = 1.0f, size = 0.16f, sizeMax = 0.22f, speed = 4f, speedMax = 7.5f, dir = 90, arc = 90, radius = 0.1f,
                grav = 1.4f, spin = false, rotRange = 25, rotSpeed = 200, curve = new[] { 0, 0.5f, 0.15f, 1f, 1, 0.9f }, fadeAt = 0.8f,
            };
            return new[] { B("pk_xu", n), B("pk_xu_nghieng", n - 1) };
        }

        static readonly MachineFx.Burst[] Gems =
        {
            new MachineFx.Burst { sprite = "pk_ngoc_tim", count = 3, life = 0.8f, lifeMax = 1.1f, size = 0.16f, sizeMax = 0.22f, speed = 4.5f, speedMax = 7f, dir = 90, arc = 70,
                grav = 1.2f, rotRange = 30, rotSpeed = 160, curve = new[] { 0, 0.5f, 0.15f, 1f, 1, 0.9f }, fadeAt = 0.8f },
        };

        // thưởng vọt tới đỉnh: loé gai nhỏ, 4 lấp lánh
        static readonly MachineFx.Burst[] TilePop =
        {
            new MachineFx.Burst { sprite = Pop, life = 0.16f, size = 0.9f, curve = new[] { 0, 0.5f, 0.4f, 1.1f, 1, 1.2f }, from = Color.white, to = Color.white, fadeAt = 0.3f, spin = true },
            new MachineFx.Burst { sprite = "pk_fx_lap_lanh_beo", count = 4, life = 0.3f, lifeMax = 0.45f, size = 0.1f, sizeMax = 0.16f, speed = 1.5f, speedMax = 3, arc = 360, radius = 0.3f,
                dampen = 0.3f, curve = new[] { 0, 0.3f, 0.3f, 1.1f, 1, 0.4f }, from = Color.white, to = Color.white, fadeAt = 0.6f, rotRange = 15 },
        };

        static int Rank(Reward r)
        {
            switch (r.k)
            {
                case RewardKind.Shards: return 100 + (int)App.Data.Hero(r.res.hero).rarity * 10 + (r.res.unlocked ? 5 : 0);
                case RewardKind.Card: return 50 + (int)r.drop.rarity * 10;
                case RewardKind.EvoStones: return 45;
                case RewardKind.Stones: return 40;
                case RewardKind.Balls: return 20;
                default: return 10;
            }
        }

        static Reward Best(List<Reward> rewards) => rewards == null || rewards.Count == 0 ? null : rewards.OrderByDescending(Rank).First();

        static Rarity? RarityOf(Reward r) =>
            r.k == RewardKind.Shards ? App.Data.Hero(r.res.hero).rarity : r.k == RewardKind.Card ? r.drop.rarity : r.k == RewardKind.Stones ? Rarity.Epic : r.k == RewardKind.EvoStones ? Rarity.Legend : (Rarity?)null;

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
            // ô theo thứ tự thưởng (thẻ, mảnh lật từ thẻ úp); thứ tự BuildTiles: XP, bi, đá tiềm năng, đá tiến hóa, thẻ, mảnh
            var order = new List<Rarity?>();
            int exp = all.Count(q => q.k == RewardKind.Exp) > 0 ? 1 : 0, balls = all.Any(q => q.k == RewardKind.Balls) ? 1 : 0;
            int stones = all.Any(q => q.k == RewardKind.Stones) ? 1 : 0;
            for (int i = 0; i < exp + balls; i++) order.Add(null);
            if (stones > 0) order.Add(Rarity.Epic);
            if (all.Any(q => q.k == RewardKind.EvoStones)) order.Add(Rarity.Legend);
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

        // một ô tổng kết: vầng tia phẳng màu độ hiếm sau ô (xoay chậm, thay quầng mềm), cỡ 0,76 → 1,18 → 1 trong 0,667 giây; ô có độ
        // hiếm lật từ thẻ úp tô màu độ hiếm
        IEnumerator PopTile(RectTransform grid, RectTransform rt, Rarity? rar, float delay)
        {
            yield return new WaitForSecondsRealtime(delay);
            var col = rar.HasValue ? Theme.Of(rar.Value) : Theme.Hex("#ffe08a");
            var halo = rar.HasValue ? Flat("tia_o", grid, Sun, MachineGlow.A(col, 0)) : null;
            if (halo)
            {
                halo.rectTransform.anchoredPosition = rt.anchoredPosition;
                halo.rectTransform.sizeDelta = Vector2.one * RewardTile.H * 1.4f;
                halo.rectTransform.SetSiblingIndex(rt.GetSiblingIndex());
                StartCoroutine(Spin(halo.rectTransform, 30));
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
                        fx.Emit(TilePop, Fx((Vector2)layer.InverseTransformPoint(rt.position)), RewardTile.H * grid.localScale.x, Color.Lerp(Color.white, col, 0.5f));
                    }
                }
                rt.localScale = new Vector3(sx, s, 1);
                if (halo) halo.color = MachineGlow.A(col, t < 0.217f ? 0 : Mathf.Min(0.32f, (t - 0.217f) / 0.1f * 0.32f));
                yield return null;
            }
            if (back) back.gameObject.SetActive(false);
            rt.localScale = Vector3.one;
        }

        IEnumerator Spin(RectTransform rt, float degPerSec)
        {
            for (float a = UnityEngine.Random.Range(0f, 360f); rt; a += degPerSec * Time.unscaledDeltaTime)
            {
                rt.localEulerAngles = new Vector3(0, 0, a);
                yield return null;
            }
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
                if (!closing) raysBg.color = MachineGlow.Hex("#ffe08a", Mathf.Min(0.035f, time * 0.12f));
            }
            for (int i = 0; i < slots.Count; i++)
            {
                var s = slots[i];
                if (!s.holder || !s.holder.gameObject.activeSelf) continue;
                // lơ lửng (chưa mở, không đang bay vào); vầng tia thở 0,9 ↔ 1 (chu kỳ quầng của máy đó: 1,75 giây lên, 4,25 giây về), đậm
                // dần tới raysA, dời tới raysAt (lên sau thưởng khi mở), mở rồi thì to hơn
                if (!s.opening && !s.opened && s.holder.localScale.x >= 0.999f)
                    s.chest.anchoredPosition = new Vector2(0, -s.chest.sizeDelta.x * 0.4f + Mathf.Sin(time * 3.9f + i * 1.3f) * 7 * k);
                if (s.rays)
                {
                    var rrt = s.rays.rectTransform;
                    float ph = time % 6f;
                    float g = ph < 1.75f ? Mathf.Lerp(0.9f, 1, ph / 1.75f) : Mathf.Lerp(1, 0.9f, (ph - 1.75f) / 4.25f);
                    float big = s.opening || s.opened ? 1.15f : 1;
                    float kk = 1 - Mathf.Exp(-dt * 10);
                    rrt.localScale = Vector3.Lerp(rrt.localScale, Vector3.one * g * big, kk);
                    rrt.anchoredPosition = Vector2.Lerp(rrt.anchoredPosition, s.raysAt, kk);
                    rrt.localEulerAngles = new Vector3(0, 0, time * (s.opened ? 18 : 25));
                    var c = s.rays.color;
                    c.a = Mathf.MoveTowards(c.a, s.raysA, dt * 1.5f);
                    s.rays.color = c;
                }
            }
        }
    }
}
