// Một bệ của Đền Huy Hiệu (prefab Assets/04 Prefabs/Items/BenHuyHieu): dải màu hệ, huy hiệu bậc cao nhất (lắc nhẹ khi đã có, bóng mờ khi chưa),
// tên hệ và bậc; dãy chưa mở: ổ khoá và điều kiện mở; đã mở: phần cộng, rồi "Đã đạt bậc cao nhất!" hoặc bậc đang đánh n/5, thanh tiến độ,
// nút "Thử thách" (thu_thach_<hệ>). Mọi phần có sẵn trong prefab, Bind bật tắt theo dữ liệu.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BadgePedestal : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image bg, band;
            public BadgeIcon badge;
            public Wobble wobble; // trên huy hiệu, bật khi đã có bậc
            public TextMeshProUGUI title, need, bonus, done, progress;
            public GameObject lockIcon;
            public UiBar bar;
            public SketchButton go;
        }

        [SerializeField] Parts p;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        public void Bind(ZoneDef zone, SaveData s, GameData d, Action onChallenge)
        {
            var cfg = d.Cfg;
            var z = zone.id;
            bool open = Badges.LineOpen(s, z);
            int tier = Badges.Tier(s, z);
            name = "ben_" + Keys.Of(z);
            p.bg.color = open ? Theme.CardFill : new Color(0.9f, 0.87f, 0.8f, 0.9f);
            p.band.color = Theme.Of(z);

            p.badge.Bind(z, tier, 200);
            p.wobble.enabled = tier > 0;
            if (tier <= 0) p.badge.Rect.localEulerAngles = Vector3.zero;

            p.title.text = $"Hệ {Elements.Name(z)}" + (tier > 0 ? $" · {Badges.TierName(cfg, tier)}" : "");
            p.title.color = Theme.Of(z);

            p.lockIcon.SetActive(!open);
            p.need.gameObject.SetActive(!open);
            p.bonus.gameObject.SetActive(open);
            p.done.gameObject.SetActive(false);
            p.progress.gameObject.SetActive(false);
            p.bar.gameObject.SetActive(false);
            p.go.gameObject.SetActive(false);
            if (!open)
            {
                p.need.text = Badges.TempleOpen(s) ? $"Thắng mini boss {zone.name} (ải {Islands.MiniAt(z)}) để mở" : "Thắng boss Đảo Thủy để mở Đền Huy Hiệu";
                return;
            }

            var bonus = Badges.Bonus(cfg, tier);
            p.bonus.text = bonus > 0 ? $"Tướng hệ {Elements.Name(z)}: +{bonus * 100:0}% Máu, Công, Thủ" : $"Chưa có huy hiệu. Bậc Đồng: +{Badges.Bonus(cfg, 1) * 100:0}% cho tướng hệ {Elements.Name(z)}";

            var cur = Badges.Current(s, cfg, z);
            if (cur == null)
            {
                p.done.gameObject.SetActive(true);
                return;
            }
            var (ct, ci) = cur.Value;
            int n = Badges.Count(cfg, ct);
            p.progress.gameObject.SetActive(true);
            p.progress.text = $"Đang đánh: {Badges.TierName(cfg, ct)} · {ci - 1}/{n}";
            p.bar.gameObject.SetActive(true);
            p.bar.Set(ci - 1, n, 0, null, true);
            p.go.gameObject.SetActive(true);
            p.go.name = "thu_thach_" + Keys.Of(z);
            p.go.SetOnClick(onChallenge);
        }
    }
}
