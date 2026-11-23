// Thanh mốc tiến hóa dưới ô xem tướng trong hộp chi tiết (prefab Dialogs/ChiTietTuong, dựng bằng menu
// "PokiClash/Prefab/Hộp thoại và màn/Thêm thanh tiến hóa vào ChiTietTuong"). Bậc theo dạng (người dùng dặn 2026-11-19, StarTier.Stops): tướng có bao
// nhiêu hình thì bấy nhiêu mốc (dòng 2 dạng: Đồng, Bạc; dòng 1 dạng: một mốc, không tiến hóa). Mốc dàn đều trên thanh, dạng đầu ở đầu,
// dạng cuối ở cuối (2026-11-23); đoạn giữa hai mốc đầy dần theo sao trong bậc, tiến hóa thì tới mốc kế. Mỗi mốc có chân dung dạng của
// bậc đó, 5 sao tô màu bậc (bậc đã qua đủ 5, bậc đang ở theo sao trong bậc, bậc chưa tới trống) và tên bậc; bậc chưa tới (hoặc tướng
// chưa có) là bóng sẫm.
// Nút Tiến hóa (xanh lá) nằm trên thanh giữa mốc đang ở và mốc kế, dòng giá ngay dưới; hộp chi tiết gọi ShowEvolve. Lên sao (mảnh) ở
// hàng nút dưới của hộp, tách hẳn khỏi tiến hóa (đá, đổi hình).
// Mọi phần có sẵn trong prefab, Bind chỉ bật tắt và gán.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class EvolutionStrip : MonoBehaviour
    {
        [Serializable]
        public struct Node
        {
            public RectTransform root; // con của rail: neo ngang theo thứ tự mốc trên thanh
            public HeroPortrait portrait;
            public UiStars stars;
            public TextMeshProUGUI name;
        }

        [SerializeField] UiBar bar;
        [SerializeField] RectTransform rail; // cùng bề ngang với thanh, chứa các mốc
        [SerializeField] Node[] nodes = new Node[0];
        [SerializeField] TextMeshProUGUI note; // dòng 1 dạng
        [SerializeField] float portraitHeight = 140;
        [Tooltip("Nút Tiến hóa trên thanh, giữa mốc đang ở và mốc kế (con của rail); prefab cũ chưa có thì null")]
        [SerializeField] SketchButton evolve;
        [SerializeField] TextMeshProUGUI evolveCost; // dòng giá dưới nút
        [SerializeField] Pulse evolvePulse;

        int[] stops = { 1 };
        int shown; // số mốc đang hiện
        float captionSize; // cỡ chữ gốc của dòng giá

        // Dùng khi dựng prefab (Editor).
        public void Setup(UiBar barView, RectTransform railRt, Node[] nodeViews, TextMeshProUGUI noteText, SketchButton evolveButton = null,
            TextMeshProUGUI evolveCostText = null, Pulse pulse = null)
        {
            bar = barView;
            rail = railRt;
            nodes = nodeViews;
            note = noteText;
            evolve = evolveButton;
            evolveCost = evolveCostText;
            evolvePulse = pulse;
        }

        // mốc dạng thứ i trên thanh (0..1): dàn đều, dạng đầu ở đầu thanh, dạng cuối ở cuối thanh (người dùng 2026-11-23: "sao dạng
        // cuối lại chưa phải đứng cuối"; bản cũ đặt mốc ở sao 1 của bậc trên thanh bậc × 5 sao nên dạng cuối chỉ tới ~70% thanh)
        float NodePos(int i) => shown <= 1 ? 0 : Mathf.Clamp01(i / (float)(shown - 1));

        // phần thanh đã tô ở điểm dừng idx: đoạn giữa mốc bậc và mốc kế đầy dần theo sao trong bậc (sao 1 ở mốc, sao 5 được 4/5 đoạn),
        // tiến hóa thì tới mốc kế; đã ở dạng cuối thì đầy thanh (5 sao của bậc cuối xem ở hàng sao dưới mốc)
        float Fill(int idx)
        {
            if (shown <= 1 || idx < 0) return 0;
            int tier = idx / StarTier.PerTier, inTier = idx % StarTier.PerTier;
            if (tier >= shown - 1) return 1;
            return (tier + inTier / (float)StarTier.PerTier) / (shown - 1);
        }

        public void Bind(HeroDef hero, int star, bool owned, BalanceConfig cfg)
        {
            stops = StarTier.Stops(cfg, hero);
            int tiers = StarTier.Tiers(hero);
            shown = Mathf.Min(tiers, nodes.Length);
            int idx = owned ? StarTier.StopIndex(cfg, hero, star) : -1;
            int cur = owned ? idx / StarTier.PerTier : -1;
            bar.Set(owned ? Fill(idx) * 100 : 0, 100, 0, "", true);
            bar.gameObject.SetActive(shown > 1); // dòng 1 dạng: không có chặng nào để chạy, chỉ mốc + dòng chú thích (soát UI 2026-11-23)
            for (int i = 0; i < nodes.Length; i++)
            {
                var n = nodes[i];
                n.root.gameObject.SetActive(i < shown);
                if (i >= shown) continue;
                int first = i * StarTier.PerTier;
                float x = NodePos(i);
                n.root.anchorMin = new Vector2(x, n.root.anchorMin.y);
                n.root.anchorMax = new Vector2(x, n.root.anchorMax.y);
                bool reached = owned && i <= cur;
                n.portrait.Bind(hero, portraitHeight, !reached, stops[first]);
                int lit = !owned || i > cur ? 0 : i < cur ? StarTier.PerTier : idx % StarTier.PerTier + 1;
                n.stars.SetTier(i, lit);
                n.name.text = StarTier.Name(i);
                n.name.fontStyle = i == cur ? FontStyles.Bold : FontStyles.Normal;
                n.name.color = i == cur ? Color.Lerp(UiStars.TierColor(i), Theme.Ink, 0.45f) : Theme.Ink3;
            }
            if (note)
            {
                note.gameObject.SetActive(tiers == 1);
                note.text = Loc.T("Dòng 1 dạng: không tiến hóa, lên sao bằng mảnh");
            }
            ShowEvolve(-1, "", false, false, null);
        }

        // Nút Tiến hóa sang bậc toTier (1..số mốc − 1): đặt giữa mốc toTier − 1 và mốc toTier; toTier ngoài khoảng đó thì ẩn.
        // caption: dòng giá dưới nút ("20/20 đá · cấp 30"); ready: bấm được; pulse: nhịp phồng.
        public void ShowEvolve(int toTier, string caption, bool ready, bool pulse, Action onClick)
        {
            if (!evolve) return;
            bool on = toTier >= 1 && toTier < shown;
            evolve.gameObject.SetActive(on);
            if (evolveCost) evolveCost.gameObject.SetActive(on);
            if (evolvePulse) evolvePulse.enabled = on && pulse;
            if (!on)
            {
                evoTier = -1;
                return;
            }
            float x = (NodePos(toTier - 1) + NodePos(toTier)) / 2;
            var rt = evolve.Rect;
            rt.anchorMin = new Vector2(x, rt.anchorMin.y);
            rt.anchorMax = new Vector2(x, rt.anchorMax.y);
            if (!pulse) rt.localScale = Vector3.one;
            evolve.SetText(Loc.T("Tiến hóa"));
            evolve.Interactable = ready;
            evolve.SetOnClick(onClick);
            evoTier = toTier;
            if (evolveCost)
            {
                var ct = evolveCost.rectTransform;
                ct.anchorMin = new Vector2(x, ct.anchorMin.y);
                ct.anchorMax = new Vector2(x, ct.anchorMax.y);
                if (captionSize <= 0) captionSize = evolveCost.fontSize;
                evolveCost.enableAutoSizing = true;
                evolveCost.fontSizeMax = captionSize;
                evolveCost.fontSizeMin = captionSize * 0.6f;
                evolveCost.text = caption;
            }
            railWidth = -1; // đặt cỡ ở LateUpdate, khi hàng đã dàn xong (lúc Bind bề ngang thanh có thể chưa đúng)
            LateUpdate();
        }

        int evoTier = -1;
        float railWidth = -1;

        // nút và dòng giá vừa khoảng trống giữa hai mốc (dòng 3 dạng mốc gần nhau): nút không rộng hơn chữ, không lấn chân dung; dòng
        // giá không lấn tên bậc
        void LateUpdate()
        {
            if (!evolve || evoTier < 1 || !evolve.gameObject.activeSelf || !rail) return;
            float w = rail.rect.width;
            if (w <= 1 || Mathf.Approximately(w, railWidth)) return;
            railWidth = w;
            float span = (NodePos(evoTier) - NodePos(evoTier - 1)) * w;
            evolve.FitWidth();
            var rt = evolve.Rect;
            rt.sizeDelta = new Vector2(Mathf.Clamp(span - 120, 150, rt.sizeDelta.x), rt.sizeDelta.y);
            if (evolveCost) evolveCost.rectTransform.sizeDelta = new Vector2(Mathf.Max(90, span - 100), evolveCost.rectTransform.sizeDelta.y);
        }
    }
}
