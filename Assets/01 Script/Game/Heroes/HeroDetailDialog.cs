// Hộp chi tiết tướng (prefab Assets/04 Prefabs/Dialogs/ChiTietTuong, mở bằng HeroDetail.Open): ô xem 4 clip (Items/OXemTuong),
// thông tin, chỉ số, khung mảnh và nơi rơi (tướng chưa có), 3 thẻ riêng (thanh bản sao hoặc "Cấp tối đa", nút "Lên cấp n"),
// dải tiềm năng, mục tiến hóa hoặc "Đã tiến hóa tối đa", nút đội. Mọi phần có sẵn trong prefab, Render bật tắt và gán dữ liệu.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HeroDetailDialog : Dialog
    {
        // một cột thẻ riêng
        [Serializable]
        public struct CardColumn
        {
            public RectTransform col;
            public UiCard card;
            public TextMeshProUGUI max; // "Cấp tối đa"
            public UiBar bar; // bản sao / cần
            public SketchButton up; // "Lên cấp n" (có Pulse)
        }

        [Serializable]
        public struct Parts
        {
            // ô xem và thông tin
            public Image viewBg;
            public HeroViewer viewer;
            public SketchButton[] clips; // Đứng, Đánh, Chiêu, Trúng
            public TextMeshProUGUI name, title, rarity, line, statNote;
            public UiElemTag elemTag;
            public BadgeIcon badge;
            public UiStars stars;
            public TextMeshProUGUI[] stats; // Máu, Công, Thủ, Tốc
            // tướng chưa có
            public GameObject shardBox;
            public TextMeshProUGUI shardTitle, drops;
            public UiBar shardBar;
            // thẻ riêng
            public LayoutElement cardRow;
            public CardColumn[] cards;
            // tiềm năng, tiến hóa, đội
            public PotentialStrip potential;
            public GameObject evolve, maxed, teamRow;
            public TextMeshProUGUI evolveTitle, evolveNeed;
            public SketchButton evolveButton, team;
            public Pulse evolvePulse;
        }

        static readonly string[] ClipIds = { HeroViewer.Idle, HeroViewer.Attack, HeroViewer.Skill, HeroViewer.Hit };

        [SerializeField] Parts p;

        string id;
        Action onChange;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        public void Show(string heroId, Action changed)
        {
            id = heroId;
            onChange = changed;
            p.viewer.Bind(App.Data.Hero(id), 400, !App.Save.Data.Hero(id).owned);
            for (int i = 0; i < p.clips.Length && i < ClipIds.Length; i++)
            {
                var clip = ClipIds[i];
                p.clips[i].SetOnClick(() => p.viewer.Play(clip));
            }
            Render(null);
        }

        // vẽ lại theo bản lưu; playClip: clip cho ô xem chạy (bản cũ dựng lại ô xem nên clip về Đứng)
        void Render(string playClip)
        {
            var d = App.Data;
            var s = App.Save.Data;
            var cfg = d.Cfg;
            var hero = d.Hero(id);
            var hp = s.Hero(id);
            int badge = Badges.Tier(s, hero.elem);
            var stats = HeroStats.Compute(cfg, hero, s.level, hp.star, false, Potential.Mods(s, d, hero)); // đã gồm huy hiệu và tiềm năng

            // ---------- ô xem và thông tin ----------
            var ec = Theme.Of(hero.elem);
            p.viewBg.color = new Color(ec.r, ec.g, ec.b, 0.22f);
            p.viewer.Play(playClip ?? HeroViewer.Idle);
            p.name.text = hero.name;
            p.title.text = hero.title;
            p.elemTag.Set(hero.elem);
            p.badge.gameObject.SetActive(badge > 0);
            if (badge > 0) p.badge.Bind(hero.elem, badge, 56); // huy hiệu cạnh nhãn hệ
            p.rarity.text = Elements.RarityName(hero.rarity);
            p.rarity.color = Theme.Of(hero.rarity);
            p.rarity.rectTransform.anchoredPosition = new Vector2(badge > 0 ? 160 : 112, -110);
            p.stars.gameObject.SetActive(hp.owned);
            if (hp.owned) p.stars.Set(hp.star, cfg.maxStar);
            p.line.text = hero.line;
            double[] values = { stats.hp, stats.atk, stats.def, stats.spd };
            for (int i = 0; i < p.stats.Length && i < values.Length; i++) p.stats[i].text = ((long)values[i]).ToString();
            p.statNote.text = $"Ở cấp {s.level}, sao {hp.star}" + (badge > 0 ? $", huy hiệu {Badges.TierName(cfg, badge)} +{Badges.Bonus(cfg, badge) * 100:0}%" : "");

            // ---------- tướng chưa có: mảnh, nơi rơi ----------
            p.shardBox.SetActive(!hp.owned);
            if (!hp.owned)
            {
                p.shardTitle.text = $"Chưa có: cần {hero.shards} mảnh";
                p.shardBar.Set(hp.shards, hero.shards, 0, $"{hp.shards}/{hero.shards}", true);
                p.drops.text = HeroDetail.DropSources(d, hero);
            }

            // ---------- 3 thẻ riêng ----------
            float rowH = hp.owned ? 560 : 440;
            p.cardRow.preferredHeight = rowH;
            for (int i = 0; i < p.cards.Length; i++)
            {
                var c = p.cards[i];
                var slot = Progress.Slots[i];
                var card = d.Card(Progress.CardOf(hero, slot));
                var cp = hp.Card(slot);
                c.col.sizeDelta = new Vector2(c.col.sizeDelta.x, rowH);
                c.card.Bind(card, cp.lv, Icon(card.icon));
                bool maxLv = cp.lv >= cfg.cardMax;
                c.max.gameObject.SetActive(hp.owned && maxLv);
                c.bar.gameObject.SetActive(hp.owned && !maxLv);
                if (hp.owned && !maxLv)
                {
                    int req = Progress.CardReq(cfg, cp.lv);
                    c.bar.Set(Mathf.Min(cp.copies, req), req, 0, $"{cp.copies}/{req} bản sao", true);
                }
                bool canUp = hp.owned && Progress.CanUpCard(s, cfg, id, slot);
                c.up.gameObject.SetActive(canUp);
                if (!canUp) continue;
                string label = $"Lên cấp {cp.lv + 1}";
                c.up.name = "nut_" + label;
                c.up.SetText(label);
                c.up.SetOnClick(() =>
                {
                    if (!Progress.UpCard(s, cfg, id, slot)) return;
                    App.Audio.Play("level");
                    App.Toasts.Show($"{card.name} lên cấp!", Icon("up"));
                    App.Save.Save();
                    onChange?.Invoke();
                    Render(HeroViewer.Skill);
                });
            }

            // ---------- tiềm năng ----------
            p.potential.gameObject.SetActive(hp.owned);
            if (hp.owned)
                p.potential.Bind(id, () =>
                {
                    onChange?.Invoke();
                    Render(null);
                });

            // ---------- tiến hóa ----------
            bool canStar = hp.owned && hp.star < cfg.maxStar;
            p.evolve.SetActive(canStar);
            p.maxed.SetActive(hp.owned && !canStar);
            if (canStar)
            {
                var need = Progress.StarNeed(cfg, hp.star + 1);
                bool ok = Progress.CanEvolve(s, cfg, id);
                p.evolveTitle.text = $"Tiến hóa lên {hp.star + 1} sao: +8% mọi chỉ số";
                p.evolveNeed.text = $"Tổng cấp 3 thẻ {Progress.CardSum(s, id)}/{need.cards} · Cấp người chơi {s.level}/{need.level}";
                p.evolveButton.SetOnClick(() =>
                {
                    if (!Progress.Evolve(s, cfg, id))
                    {
                        App.Toasts.Show("Chưa đủ điều kiện tiến hóa", Icon("info"));
                        return;
                    }
                    App.Audio.Play("level");
                    App.Toasts.Show($"{hero.name} tiến hóa {s.Hero(id).star} sao!", Icon("star"));
                    App.Save.Save();
                    onChange?.Invoke();
                    Render(HeroViewer.Skill);
                });
                p.evolveButton.Interactable = ok;
                p.evolvePulse.enabled = ok;
                if (!ok) p.evolveButton.transform.localScale = Vector3.one;
            }

            // ---------- đội ----------
            p.teamRow.SetActive(hp.owned);
            if (hp.owned)
            {
                bool inTeam = s.team.Contains(id);
                string label = inTeam ? "Bỏ khỏi đội" : "Cho vào đội";
                p.team.name = "nut_" + label;
                p.team.SetText(label);
                p.team.SetRole(inTeam ? BtnColor.Paper : BtnColor.Blue);
                p.team.SetOnClick(() =>
                {
                    if (inTeam) s.team.Remove(id);
                    else if (s.team.Count >= 3)
                    {
                        App.Toasts.Show("Đội tối đa 3 tướng: bỏ bớt một tướng trước", Icon("team"));
                        return;
                    }
                    else s.team.Add(id);
                    App.Save.Save();
                    onChange?.Invoke();
                    Render(null);
                });
            }
        }
    }
}
