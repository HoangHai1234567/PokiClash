// Thanh mốc tiến hóa dưới ô xem tướng trong hộp chi tiết (prefab Dialogs/ChiTietTuong, dựng bằng menu
// "PokiClash/Prefab/Thêm thanh tiến hóa vào ChiTietTuong"). Bậc sao 2026-11-17 (StarTier): thanh là sao tổng 1..20, mỗi bậc (Đồng,
// Bạc, Vàng, Kim Cương) là một mốc đặt ở sao 1 của bậc (sao 1, 6, 11, 16), thanh đầy ở Kim Cương 5★. Mốc có chân dung dạng ở bậc đó
// (dạng 2 ở Bạc, dạng 3 ở Vàng theo BalanceConfig.formStars; Kim Cương giữ dạng cuối), 5 sao tô màu bậc (bậc đã qua đủ 5, bậc đang ở
// theo sao trong bậc, bậc chưa tới trống) và tên bậc; bậc chưa tới (hoặc tướng chưa có) là bóng sẫm.
// Prefab cũ 3 mốc vẫn chạy (3 bậc đầu); chạy lại menu để có 4 mốc.
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

        // Dùng khi dựng prefab (Editor).
        public void Setup(UiBar barView, RectTransform railRt, Node[] nodeViews, TextMeshProUGUI noteText)
        {
            bar = barView;
            rail = railRt;
            nodes = nodeViews;
            note = noteText;
        }

        // sao bắt đầu của bậc tier (0 là Đồng)
        public static int StartStar(int tier) => StarTier.Star(tier, 1);

        // vị trí sao trên thanh (0..1): sao 1 ở đầu, Kim Cương 5★ ở cuối
        public static float Pos(int star) => Mathf.Clamp01((star - 1) / (float)(StarTier.MaxStar - 1));

        // phần thanh đã đầy ở sao này
        public static float Fill(int star) => Pos(star);

        public void Bind(HeroDef hero, int star, bool owned, BalanceConfig cfg)
        {
            int count = Mathf.Min(StarTier.Count, nodes.Length);
            int cur = owned ? StarTier.Tier(star) : -1;
            bar.Set(owned ? Fill(star) * 100 : 0, 100, 0, "", true);
            for (int i = 0; i < nodes.Length; i++)
            {
                var n = nodes[i];
                n.root.gameObject.SetActive(i < count);
                if (i >= count) continue;
                int from = StartStar(i);
                float x = Pos(from);
                n.root.anchorMin = new Vector2(x, n.root.anchorMin.y);
                n.root.anchorMax = new Vector2(x, n.root.anchorMax.y);
                bool reached = owned && star >= from;
                n.portrait.Bind(hero, portraitHeight, !reached, from);
                int lit = !owned || i > cur ? 0 : i < cur ? StarTier.PerTier : StarTier.InTier(star);
                n.stars.SetTier(i, lit);
                n.name.text = StarTier.Name(i);
                n.name.fontStyle = i == cur ? FontStyles.Bold : FontStyles.Normal;
                n.name.color = i == cur ? Color.Lerp(UiStars.TierColor(i), Theme.Ink, 0.45f) : Theme.Ink3;
            }
            note.gameObject.SetActive(false); // dòng "1 dạng" cũ: 4 mốc bậc luôn hiện, hình đổi theo dạng của dòng
        }
    }
}
