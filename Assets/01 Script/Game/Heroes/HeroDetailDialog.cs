// Hộp chi tiết tướng (prefab Assets/04 Prefabs/Dialogs/ChiTietTuong, mở bằng HeroDetail.Open), từ trên xuống:
// - sân khấu: tướng to (Items/OXemTuong) đứng giữa, 4 nút clip dưới chân, góc trên trái là tên, hệ, sao (5 sao tô màu bậc) và nhãn
//   bậc ("Bạc 3 sao"), huy hiệu, độ hiếm, danh hiệu;
// - thanh mốc tiến hóa theo bậc (EvolutionStrip), hàng 4 chỉ số (số gọn NumFmt.Short), khung mảnh và nơi rơi (tướng chưa có);
// - 3 thẻ riêng cỡ nhỏ (chạm mở ChiTietThe), dưới mỗi thẻ là nút "Lên cấp n", thanh bản sao hoặc "Cấp tối đa";
// - thanh mảnh của lần lên sao kế, dòng điều kiện và hàng nút Tiềm năng, "Lên sao" (chỉ tốn mảnh; bước đi qua mốc bậc cũ cần cấp
//   người chơi), đội. Tiến hóa (đá + cấp, đổi hình) là nút riêng màu xanh lá trên thanh tiến hóa, giữa mốc đang ở và mốc kế
//   (người dùng dặn 2026-11-19: tách rõ lên sao với tiến hóa; tướng có bao nhiêu hình thì bấy nhiêu bậc, StarTier.Stops);
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
            // nhãn bậc cạnh hàng sao, thanh mảnh / đá của bước kế và icon của nó (menu "PokiClash/Prefab/Hộp chi tiết tướng: nhãn bậc sao +
            // thanh mảnh, đá"); prefab chưa dựng thì null: nhãn bậc chỉ ở dòng chỉ số, số mảnh / đá chỉ ở dòng điều kiện
            public TextMeshProUGUI tierLabel;
            public UiBar evolveBar;
            public Image evolveIcon;
        }

        // nút thứ 5 "Mana" (menu "PokiClash/Prefab/Hộp chi tiết tướng: hạt lửa + nút Mana"): clip bắn + chiêu mana bằng hạt;
        // nút 6, 7 "Ra sân", "Chết" (menu "PokiClash/Prefab/Hộp chi tiết tướng: nút Ra sân + Chết"): chỉ hiện khi dạng có clip đó
        static readonly string[] ClipIds =
        {
            HeroViewer.Idle, HeroViewer.Attack, HeroViewer.Skill, HeroViewer.Hit, HeroViewer.Cast, HeroViewer.Appear, HeroViewer.Die,
        };
        const int FirstOptional = 5; // từ nút này trở đi: ẩn nếu dạng không có clip

        void Update()
        {
            if (p.clips == null || !p.viewer) return;
            for (int i = FirstOptional; i < p.clips.Length && i < ClipIds.Length; i++)
            {
                var b = p.clips[i];
                bool has = p.viewer.Has(ClipIds[i]);
                if (b && b.gameObject.activeSelf != has) b.gameObject.SetActive(has);
            }
        }
        const float CardH = 292, SlotH = 84; // thẻ mini và chỗ nút/thanh dưới thẻ

        [SerializeField] Parts p;
        [SerializeField] float viewSize = 520; // cạnh ô xem tướng trên sân khấu
        [SerializeField] CardDetailDialog cardDetail; // prefab Dialogs/ChiTietThe

        string id;
        Action onChange;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // Bỏ ô Tốc (người dùng duyệt 2026-11-17: trận không dùng tốc). Hàng "chi_so" của prefab: mỗi chỉ số là 3 con liền nhau
        // (icon, nhãn, số) đặt cố định; ẩn nhóm thứ 4 và dời nhóm 2, 3 cho 3 nhóm giãn đều trên đúng khoảng cũ. Nhóm 1 và số thứ 4
        // không dời nên gọi lại nhiều lần vẫn ra như nhau. Prefab khác cấu trúc (mỗi số một ô riêng) thì dùng Ui.DropLastCell.
        static void DropSpeedGroup(TextMeshProUGUI[] nums)
        {
            var row = nums[0].transform.parent;
            bool shared = true;
            foreach (var n in nums) shared &= n.transform.parent == row && n.transform.GetSiblingIndex() >= 2;
            if (!shared)
            {
                Ui.DropLastCell(System.Array.ConvertAll(nums, x => (RectTransform)x.transform.parent));
                return;
            }
            Transform[] Group(int i)
            {
                int s = nums[i].transform.GetSiblingIndex();
                return new[] { row.GetChild(s - 2), row.GetChild(s - 1), nums[i].transform };
            }
            // đo bằng localPosition (mỗi ô có thể neo theo mốc riêng nên anchoredPosition không so được với nhau)
            float x0 = nums[0].transform.localPosition.x, x3 = nums[3].transform.localPosition.x;
            foreach (var t in Group(3)) t.gameObject.SetActive(false);
            for (int i = 1; i < 3; i++)
            {
                float dx = Mathf.Lerp(x0, x3, i / 2f) - nums[i].transform.localPosition.x;
                if (Mathf.Abs(dx) < 0.01f) continue;
                foreach (var t in Group(i)) t.localPosition += new Vector3(dx, 0, 0);
            }
        }

        // chữ đầu hộp (sao, bậc, độ hiếm) vẽ trên hình tướng: hình to hay tràn lên chữ (người dùng dặn 2026-11-19: sao, bậc phải rõ).
        // Đưa nhánh chứa chữ lên sau nhánh chứa ô xem ở cha chung; cha chung có LayoutGroup thì thôi (đổi thứ tự sẽ dời chỗ)
        static void DrawAbove(Transform top, Transform below)
        {
            for (var h = top; h && h.parent; h = h.parent)
            {
                var parent = h.parent;
                Transform b = null;
                for (var v = below; v && v.parent; v = v.parent)
                    if (v.parent == parent)
                    {
                        b = v;
                        break;
                    }
                if (!b) continue;
                if (b == h || parent.GetComponent<LayoutGroup>()) return;
                if (h.GetSiblingIndex() < b.GetSiblingIndex()) h.SetSiblingIndex(b.GetSiblingIndex());
                return;
            }
        }

        public void Show(string heroId, Action changed)
        {
            id = heroId;
            onChange = changed;
            if (p.stars && p.viewer) DrawAbove(p.stars.transform, p.viewer.transform);
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

        // hack thử: chưa có thì nhận tướng 1 sao; có rồi thì lên 1 sao hiện (qua cả mốc tiến hóa), bỏ qua điều kiện; tối đa thì về 1 sao
        void HackStar()
        {
            var s = App.Save.Data;
            var hp = s.Hero(id);
            var hero = App.Data.Hero(id);
            if (!hp.owned)
            {
                Progress.UnlockHero(s, id);
                hp.star = 1;
            }
            else hp.star = hp.star < StarTier.MaxStar ? StarTier.NextStop(App.Data.Cfg, hero, hp.star) : 1;
            App.Save.Save();
            App.Toasts.Show($"Hack: {hero.name} {StarTier.Label(App.Data.Cfg, hero, hp.star)} ({HeroArt.FormOf(hero).name})", Icon("star"));
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
            p.rarity.color = Theme.RarityInk(hero.rarity); // cùng màu chữ độ hiếm với thẻ tướng
            p.stars.gameObject.SetActive(hp.owned);
            if (hp.owned)
            {
                p.stars.SetSize(StarSize); // sao to cho rõ (người dùng dặn 2026-11-19)
                p.stars.SetTiered(cfg, hero, hp.star);
            }
            string tierText = StarTier.Label(cfg, hero, hp.star);
            if (p.tierLabel)
            {
                // chữ viền như tên tướng (ruột màu bậc, viền mực): đọc được cả khi hình tướng tràn lên đầu hộp
                p.tierLabel.gameObject.SetActive(hp.owned);
                p.tierLabel.text = tierText;
                p.tierLabel.fontSharedMaterial = p.name.fontSharedMaterial;
                p.tierLabel.color = UiStars.TierColor(StarTier.TierOf(cfg, hero, hp.star));
                p.rarity.fontSharedMaterial = p.name.fontSharedMaterial;
                p.rarity.color = Theme.Of(hero.rarity);
            }
            p.line.text = hero.line;
            double[] values = { stats.hp, stats.atk, stats.def };
            if (p.stats.Length == 4) DropSpeedGroup(p.stats); // bỏ ô Tốc
            for (int i = 0; i < p.stats.Length && i < values.Length; i++) p.stats[i].text = NumFmt.Short(values[i]);
            p.statNote.text = $"Ở cấp {s.level}" + (hp.owned ? $", {tierText}" : "") +
                              (badge > 0 ? $", huy hiệu {Badges.TierName(cfg, badge)} +{Badges.Bonus(cfg, badge) * 100:0}%" : "");
            if (p.evolution) p.evolution.Bind(hero, hp.star, hp.owned, cfg);
            if (p.hackStar)
            {
                p.hackStar.gameObject.SetActive(true); // hiện cả ở bản build để thử trên máy (người dùng dặn 2026-11-06)
                p.hackStar.SetText(!hp.owned ? "Hack: nhận" : hp.star < StarTier.MaxStar ? $"Hack: {StarTier.Label(cfg, hero, StarTier.NextStop(cfg, hero, hp.star))}" : "Hack: 1 sao");
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
            if (p.evolveBar) p.evolveBar.transform.parent.gameObject.SetActive(hp.owned);
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

            // lên sao (hàng nút dưới, chỉ mảnh) và tiến hóa (nút xanh lá trên thanh tiến hóa, đá + cấp, đổi hình): hai nút riêng
            var step = Progress.NextStep(s, d, id);
            int next = StarTier.NextStop(cfg, hero, hp.star);
            int tier = StarTier.TierOf(cfg, hero, hp.star), tiers = StarTier.Tiers(hero);
            // dạng của sao kế tiếp (tiến hóa đổi dạng thì phải đọc animation mới): đọc trước ở luồng phụ để bấm không khựng
            if (step != Progress.StarStep.Max) Game.AolaActor.Prewarm(HeroArt.FormOf(hero, next).aola);
            int Gain(int from, int to) => Mathf.RoundToInt((float)((HeroStats.StarMult(cfg, to) / HeroStats.StarMult(cfg, from) - 1) * 100));
            string LvNeed(int lv) => lv <= 0 || s.level >= lv ? "" : $" · cần cấp {lv} (đang {s.level})";

            // nút Tiến hóa trên thanh: sang bậc kế (hiện cả khi chưa tới sao cuối bậc, mờ, để thấy chỗ tiến hóa)
            if (p.evolution)
            {
                if (tier + 1 < tiers)
                {
                    int toStar = StarTier.TierStartStar(cfg, hero, tier + 1);
                    var evoCost = Progress.EvolveCost(cfg, hero, StarTier.Tier(toStar));
                    bool atGate = step == Progress.StarStep.Evolve;
                    bool can = atGate && Progress.CanEvolve(s, d, id);
                    string caption = atGate
                        ? $"{s.evoStones}/{evoCost.stones} đá" + (s.level < evoCost.level ? $" · cấp {evoCost.level}" : "")
                        : $"cần {StarTier.Name(tier)} 5 sao";
                    p.evolution.ShowEvolve(tier + 1, caption, can, can, () => DoEvolve(hero));
                }
                else p.evolution.ShowEvolve(-1, "", false, false, null);
            }

            bool ok = false;
            if (step == Progress.StarStep.Max)
            {
                p.evolveNeed.text = $"Đã đạt {tierText}, tối đa: mảnh nhận thêm đổi thành bản sao thẻ";
                EvolveBar(Icon("star"), UiStars.TierColor(tiers - 1), 1, 1, "Tối đa");
            }
            else if (step == Progress.StarStep.StarUp)
            {
                var c = Progress.StarUpCost(cfg, hero, hp.star);
                ok = Progress.CanStarUp(s, d, id);
                p.evolveNeed.text = $"Lên {StarTier.Label(cfg, hero, next)} (+{Gain(hp.star, next)}% chỉ số): {hp.shards}/{c.shards} mảnh {hero.name}{LvNeed(c.level)}";
                EvolveBar(Icon("shard"), Color.white, hp.shards, c.shards, $"{hp.shards}/{c.shards} mảnh");
            }
            else
            {
                // sao cuối bậc: lên sao dừng, chờ tiến hóa ở nút trên thanh; thanh mảnh tính cho lần lên sao đầu của bậc sau
                var gate = Progress.EvolveCost(s, d, id);
                var after = Progress.StarUpCost(cfg, hero, next);
                string form = HeroArt.FormOf(hero, next).name;
                p.evolveNeed.text = $"Đủ {tierText}: bấm Tiến hóa trên thanh để thành {form} (+{Gain(hp.star, next)}% chỉ số; " +
                                    $"{gate.stones} đá{(gate.level > 0 ? $", cấp {gate.level}" : "")})";
                EvolveBar(Icon("shard"), Color.white, hp.shards, after.shards, $"{hp.shards}/{after.shards} mảnh");
            }
            p.evolveButton.gameObject.SetActive(true);
            p.evolveButton.name = "nut_len_sao";
            p.evolveButton.SetText(step == Progress.StarStep.Max ? "Tối đa" : "Lên sao");
            p.evolveButton.SetOnClick(() =>
            {
                var st = Progress.NextStep(s, d, id);
                if (!Progress.StarUp(s, d, id))
                {
                    App.Toasts.Show(st == Progress.StarStep.Max ? "Đã tối đa sao"
                        : st == Progress.StarStep.Evolve ? $"Đủ 5 sao {StarTier.Name(StarTier.TierOf(cfg, hero, s.Hero(id).star))}: bấm Tiến hóa trên thanh"
                        : "Chưa đủ mảnh hoặc cấp", Icon("info"));
                    return;
                }
                App.Audio.Play("level");
                App.Toasts.Show($"{hero.name} lên {StarTier.Label(cfg, hero, s.Hero(id).star)}!", Icon("star"));
                App.Save.Save();
                onChange?.Invoke();
                Render(HeroViewer.Skill);
            });
            p.evolveButton.Interactable = ok;
            p.evolvePulse.enabled = ok;
            if (!ok) p.evolveButton.transform.localScale = Vector3.one;

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

        const float StarSize = 44; // cỡ sao cạnh tên tướng

        // tiến hóa (nút trên thanh tiến hóa): đá + cấp, sang bậc sau, đổi hình
        void DoEvolve(HeroDef hero)
        {
            var s = App.Save.Data;
            var d = App.Data;
            if (!Progress.Evolve(s, d, id))
            {
                App.Toasts.Show("Chưa đủ đá tiến hóa hoặc cấp", Icon("info"));
                return;
            }
            App.Audio.Play("level");
            int now = s.Hero(id).star;
            App.Toasts.Show($"{HeroArt.FormOf(hero, now).name} tiến hóa: {StarTier.Label(d.Cfg, hero, now)}!", Icon("star"));
            App.Save.Save();
            onChange?.Invoke();
            BindViewer(); // qua bậc là đổi dạng
            Render(HeroViewer.Skill);
        }

        // thanh mảnh của lần lên sao kế (prefab chưa dựng thanh thì bỏ qua)
        void EvolveBar(Sprite icon, Color tint, int have, int need, string text)
        {
            if (p.evolveIcon)
            {
                Theme.SetSprite(p.evolveIcon, icon);
                p.evolveIcon.color = tint;
            }
            if (p.evolveBar) p.evolveBar.Set(Mathf.Min(have, need), need, 0, text, true);
        }
    }
}
