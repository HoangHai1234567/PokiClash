// Hộp chi tiết tướng (prefab Assets/04 Prefabs/Dialogs/ChiTietTuong, mở bằng HeroDetail.Open), từ trên xuống:
// - sân khấu: tướng to (Items/OXemTuong) đứng giữa, 4 nút clip dưới chân, góc trên trái là tên, hệ, sao, huy hiệu, độ hiếm, danh hiệu;
// - thanh mốc tiến hóa (EvolutionStrip), hàng 4 chỉ số, khung mảnh và nơi rơi (tướng chưa có);
// - 3 thẻ riêng cỡ nhỏ (chạm mở ChiTietThe), dưới mỗi thẻ là nút "Lên cấp n", thanh bản sao hoặc "Cấp tối đa";
// - dòng điều kiện tiến hóa và hàng nút Tiềm năng, Tiến hóa, đội;
// - nút hack tiến hóa ở góc trái sân khấu, trên hàng nút clip, để thử đổi dạng; hiện cả ở bản build (thử trên máy, người dùng
//   dặn 2026-11-06), nhớ tắt trước khi phát hành.
// Mọi phần có sẵn trong prefab, Render bật tắt và gán dữ liệu.
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
            public EvolutionStrip evolution; // thanh mốc tiến hóa dưới hàng ô xem (menu Thêm thanh tiến hóa vào ChiTietTuong)
            // tướng chưa có
            public GameObject shardBox;
            public TextMeshProUGUI shardTitle, drops;
            public UiBar shardBar;
            // thẻ riêng
            public LayoutElement cardRow;
            public CardColumn[] cards;
            // dòng điều kiện tiến hóa, hàng nút Tiềm năng, Tiến hóa, đội
            public GameObject teamRow;
            public TextMeshProUGUI evolveNeed;
            public SketchButton potentialButton, evolveButton, team;
            public Pulse potentialPulse, evolvePulse;
            // nút hack tiến hóa để thử (hiện cả ở bản build; menu Thêm nút hack tiến hóa vào ChiTietTuong)
            public SketchButton hackStar;
        }

        // nút thứ 5 "Mana" (menu "PokiClash/Prefab/Hộp chi tiết tướng: hạt lửa + nút Mana"): clip bắn + chiêu mana bằng hạt
        static readonly string[] ClipIds = { HeroViewer.Idle, HeroViewer.Attack, HeroViewer.Skill, HeroViewer.Hit, HeroViewer.Cast };
        const float CardH = 292, SlotH = 84; // thẻ mini và chỗ nút/thanh dưới thẻ

        [SerializeField] Parts p;
        [SerializeField] float viewSize = 520; // cạnh ô xem tướng trên sân khấu
        [SerializeField] CardDetailDialog cardDetail; // prefab Dialogs/ChiTietThe

        string id;
        Action onChange;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        public void Show(string heroId, Action changed)
        {
            id = heroId;
            onChange = changed;
            BindViewer();
            for (int i = 0; i < p.clips.Length && i < ClipIds.Length; i++)
            {
                var clip = ClipIds[i];
                p.clips[i].SetOnClick(() => p.viewer.Play(clip));
            }
            Render(null);
        }

        // dựng lại ô xem theo sao hiện tại (lên sao qua mốc tiến hóa thì đổi dạng)
        void BindViewer() => p.viewer.Bind(App.Data.Hero(id), viewSize, !App.Save.Data.Hero(id).owned);

        // hack thử: chưa có thì nhận tướng 1 sao; có rồi thì lên 1 sao, bỏ qua điều kiện; tối đa thì về 1 sao
        void HackStar()
        {
            var s = App.Save.Data;
            var hp = s.Hero(id);
            if (!hp.owned)
            {
                Progress.UnlockHero(s, id);
                hp.star = 1;
            }
            else hp.star = hp.star < App.Data.Cfg.maxStar ? hp.star + 1 : 1;
            App.Save.Save();
            App.Toasts.Show($"Hack: {App.Data.Hero(id).name} {hp.star} sao ({HeroArt.FormOf(App.Data.Hero(id)).name})", Icon("star"));
            onChange?.Invoke();
            BindViewer();
            Render(HeroViewer.Skill);
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
            p.stars.gameObject.SetActive(hp.owned);
            if (hp.owned) p.stars.Set(hp.star, cfg.maxStar);
            p.line.text = hero.line;
            double[] values = { stats.hp, stats.atk, stats.def, stats.spd };
            for (int i = 0; i < p.stats.Length && i < values.Length; i++) p.stats[i].text = ((long)values[i]).ToString();
            p.statNote.text = $"Ở cấp {s.level}, sao {hp.star}" + (badge > 0 ? $", huy hiệu {Badges.TierName(cfg, badge)} +{Badges.Bonus(cfg, badge) * 100:0}%" : "");
            if (p.evolution) p.evolution.Bind(hero, hp.star, hp.owned, cfg);
            if (p.hackStar)
            {
                p.hackStar.gameObject.SetActive(true); // hiện cả ở bản build để thử trên máy (người dùng dặn 2026-11-06)
                p.hackStar.SetText(!hp.owned ? "Hack: nhận" : hp.star < cfg.maxStar ? $"Hack: {hp.star + 1} sao" : "Hack: 1 sao");
                p.hackStar.FitWidth();
                p.hackStar.SetOnClick(HackStar);
            }

            // ---------- tướng chưa có: mảnh, nơi rơi ----------
            p.shardBox.SetActive(!hp.owned);
            if (!hp.owned)
            {
                p.shardTitle.text = $"Chưa có: cần {hero.shards} mảnh";
                p.shardBar.Set(hp.shards, hero.shards, 0, $"{hp.shards}/{hero.shards}", true);
                p.drops.text = HeroDetail.DropSources(d, hero);
            }

            // ---------- 3 thẻ riêng: dưới thẻ là nút lên cấp (đủ bản sao), thanh bản sao hoặc "Cấp tối đa" ----------
            float rowH = hp.owned ? CardH + SlotH : CardH;
            p.cardRow.preferredHeight = rowH;
            for (int i = 0; i < p.cards.Length; i++)
            {
                var c = p.cards[i];
                var slot = Progress.Slots[i];
                var card = d.Card(Progress.CardOf(hero, slot));
                var cp = hp.Card(slot);
                c.col.sizeDelta = new Vector2(c.col.sizeDelta.x, rowH);
                int lv = cp.lv;
                c.card.Bind(card, lv, Icon(card.icon), null, () => App.Modals.Open(cardDetail).Show(card, lv));
                bool maxLv = cp.lv >= cfg.cardMax;
                bool canUp = hp.owned && Progress.CanUpCard(s, cfg, id, slot);
                c.max.gameObject.SetActive(hp.owned && maxLv);
                c.bar.gameObject.SetActive(hp.owned && !maxLv && !canUp);
                if (hp.owned && !maxLv)
                {
                    int req = Progress.CardReq(cfg, cp.lv);
                    c.bar.Set(Mathf.Min(cp.copies, req), req, 0, $"{cp.copies}/{req} bản sao", true);
                }
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

            // ---------- hàng nút (tướng đã có) ----------
            p.teamRow.SetActive(hp.owned);
            p.evolveNeed.gameObject.SetActive(hp.owned);
            if (!hp.owned) return;

            // tiềm năng: mở hộp khoá ô, khai phá; nhịp phồng khi còn kết quả khai phá chưa chọn
            p.potentialButton.SetOnClick(() => PotentialPanel.Open(id, () =>
            {
                onChange?.Invoke();
                Render(null);
            }));
            bool fresh = hp.potentialNew != null;
            p.potentialPulse.enabled = fresh;
            if (!fresh) p.potentialButton.transform.localScale = Vector3.one;

            // tiến hóa
            bool canStar = hp.star < cfg.maxStar;
            // dạng của sao kế tiếp (đổi dạng thì phải đọc animation mới): đọc trước ở luồng phụ để bấm Tiến hóa không khựng
            if (canStar) Game.AolaActor.Prewarm(HeroArt.FormOf(hero, hp.star + 1).aola);
            p.evolveButton.gameObject.SetActive(canStar);
            p.evolveNeed.text = "Đã tiến hóa tối đa";
            if (canStar)
            {
                var need = Progress.StarNeed(cfg, hp.star + 1);
                bool ok = Progress.CanEvolve(s, cfg, id);
                p.evolveNeed.text = $"Lên {hp.star + 1} sao (+8% mọi chỉ số): tổng cấp 3 thẻ {Progress.CardSum(s, id)}/{need.cards} · cấp người chơi {s.level}/{need.level}";
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
                    BindViewer();
                    Render(HeroViewer.Skill);
                });
                p.evolveButton.Interactable = ok;
                p.evolvePulse.enabled = ok;
                if (!ok) p.evolveButton.transform.localScale = Vector3.one;
            }

            // đội
            bool inTeam = s.team.Contains(id);
            string teamLabel = inTeam ? "Bỏ khỏi đội" : "Cho vào đội";
            p.team.name = "nut_" + teamLabel;
            p.team.SetText(teamLabel);
            p.team.SetRole(inTeam ? BtnColor.Paper : BtnColor.Blue);
            p.team.SetOnClick(() =>
            {
                if (inTeam) s.team.Remove(id);
                else if (s.team.Count >= Progress.TeamSlots(s))
                {
                    App.Toasts.Show($"Đội đã đủ {Progress.TeamSlots(s)} tướng: bỏ bớt một tướng trước", Icon("team"));
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
