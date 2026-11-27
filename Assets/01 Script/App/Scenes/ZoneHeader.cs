// Thanh hải trình đầu màn đảo (người dùng 2026-11-27: "thanh này trong các đảo nhìn ổn nhưng chưa có sự ấn tượng và độc đáo, thử thiết
// kế sáng tạo hơn"). Thay khung thông tin mỏng cũ (nhãn hệ, dòng cấp, nhãn độ khó, số ải, thanh rương, dòng gợi ý hệ khắc) bằng một tấm
// bản đồ hải trình, ít chữ (chi tiết khi chạm).
// Bản 2 (người dùng 2026-11-27: "2 ô đầu cuối nhìn viền đậm và không rõ ràng, phải giấu finalboss đi cho bí ẩn"): hai đầu là ô vuông bo
// tròn viền trắng giấy như hai cột ô ở sảnh (lòng ô tô màu, lớp đen mờ đáy ô dưới chữ), bỏ đĩa + vòng mực đậm:
// - trái: ô hệ, lòng màu hệ nhạt, icon hệ to, "1/70" chữ trắng viền mực ở đáy ô; chạm thì hiện gợi ý hệ khắc;
// - giữa: đường mòn chấm vẽ tay uốn lượn giữa hai ô; quãng đã đi tô màu hệ, chấm to, có làn sáng chạy dọc; quãng chưa đi là chấm mực
//   nhạt. Rương mốc nằm trên đường theo tỉ lệ số ải (lắc khi mở được, mờ khi đã nhận). Ghim "ải kế" (màu hệ, ghi cấp ải kế) nhấp nhô
//   trên đường đúng chỗ đang đánh;
// - phải: ô boss đỏ: boss đảo (tướng chính ải cuối) GIẤU thành bóng đen có dấu "?" nhấp nhô cho tới khi mở tới ải cuối (như bệ ải chưa mở
//   trên bản đồ); lộ diện thì đủ màu, chinh phục xong đội vương miện. "BOSS" ở đáy ô; chạm thì báo cấp boss;
// - dấu độ khó đóng nghiêng ở góc trên ô boss (màu theo độ khó, như con dấu cao su).
// Dựng bằng menu "PokiClash/Prefab/Sảnh và đảo/Đảo: thanh hải trình" (Editor/ZoneHeaderMenu.cs); ZoneScene.ShowInfo gọi Bind. Chấm
// đường mòn sinh lúc chạy (một lần) từ chấm mẫu trong prefab.
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ZoneHeader : MonoBehaviour
    {
        [Serializable]
        public struct Chest
        {
            public Image image;
            public ClickCatcher click;
            public Wobble wobble;
        }

        [Serializable]
        public struct Parts
        {
            [Header("Ô hệ")]
            public RectTransform crest;
            public Image crestFill, icon; // crestFill: lòng ô (tô màu hệ nhạt)
            public ClickCatcher crestClick;
            public TextMeshProUGUI count;

            [Header("Đường mòn")]
            public RectTransform trail;
            public Image dash; // chấm mẫu (tắt), chấm đường mòn chép từ đây lúc chạy
            public RectTransform pin;
            public Image pinBg;
            public TextMeshProUGUI pinText;
            public Chest[] chests;

            [Header("Boss")]
            public RectTransform boss;
            public ClickCatcher bossClick;
            public HeroPortrait portrait;
            public RectTransform mystery; // dấu "?" trên bóng đen
            public TextMeshProUGUI bossLabel; // "BOSS" (chữ cố định trong prefab)
            public GameObject crown;

            [Header("Độ khó")]
            public Image stamp;
            public TextMeshProUGUI stampText;
        }

        const int Dashes = 46;
        const float Wave = 15, Periods = 1.5f; // đường mòn: biên độ uốn, số nhịp uốn trên cả đường
        const float CrestPale = 0.5f; // lòng ô hệ: màu hệ pha trắng (icon hệ cùng màu vẫn nổi)
        static readonly Color InkFaint = new Color(0.17f, 0.13f, 0.1f, 0.32f);
        static readonly Color Shadow = Theme.Hex("#22161b"); // bóng đen boss chưa lộ diện

        [SerializeField] Parts p;

        readonly List<Image> dashes = new List<Image>();
        float progress, pinY, mysteryY;
        Color hue;
        bool pinOn, mysteryBase;

        public RectTransform Rect => (RectTransform)transform;

        // Boss cuối đảo còn giấu: st là ải cuối của đảo mà chưa mở. Thanh này, bệ ải và habitat trên bản đồ đảo (ZoneScene, ZoneSceneLand)
        // hiện bóng đen, tên "???", chạm thì chỉ báo cấp boss (BossTip), không mở hộp chuẩn bị (hộp đó lộ mặt boss). Người dùng
        // 2026-11-27: "phải giấu finalboss đi cho bí ẩn", "giấu boss trên bản đồ đảo luôn".
        public static bool BossHidden(SaveData s, GameData d, StageDef st) =>
            st != null && !d.ZoneStages(st.zone).Any(x => x.idx > st.idx) && !Progress.StageOpen(s, st);

        public static void BossTip(GameData d, StageDef st)
        {
            var z = d.Zone(st.zone);
            App.Toasts.Show(Loc.F("Boss đảo cấp {0}. Tới ải cuối mới lộ diện.", z != null ? z.levelMax : 0), App.Art ? App.Art.Icon("lock") : null);
        }

        // Dùng khi dựng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        // claim(n): chạm rương mốc thứ n; ZoneScene lo nhận / báo
        public void Bind(ZoneDef z, SaveData s, GameData d, int prog, Action<int> claim)
        {
            int size = Mathf.Max(1, Islands.Size(z.id));
            var at = Islands.Chests(z.id);
            hue = Theme.Of(z.id);
            progress = Mathf.Clamp01(prog / (float)size);

            // ô hệ: lòng màu hệ nhạt, icon, số ải; chạm hiện gợi ý hệ khắc
            p.crestFill.color = Color.Lerp(hue, Color.white, CrestPale);
            Theme.SetSprite(p.icon, App.Art ? App.Art.Icon("e_" + Keys.Of(z.id)) : null);
            p.count.text = $"{prog}/{size}";
            string tip = Loc.F("{0}. Địch hệ {1}: dùng tướng hệ {2} để khắc.", z.sub, Elements.Name(z.id), Elements.Name(Progress.CounterOf(z.id)));
            p.crestClick.OnClick = () =>
            {
                App.Audio.Play("click");
                UiMotion.Of(p.crest).Punch(0.12f);
                App.Toasts.Show(tip, App.Art ? App.Art.Icon("e_" + Keys.Of(Progress.CounterOf(z.id))) : null);
            };

            // đường mòn: chấm đã đi màu hệ, chưa đi mực nhạt
            BuildDashes();
            for (int i = 0; i < dashes.Count; i++)
            {
                float f = (i + 0.5f) / dashes.Count;
                bool passed = f <= progress;
                var img = dashes[i];
                img.color = passed ? hue : InkFaint;
                img.rectTransform.sizeDelta = passed ? new Vector2(20, 9) : new Vector2(13, 6);
            }

            // rương mốc theo tỉ lệ số ải; rương cuối to, vàng; rương thừa ẩn
            int canClaim = Progress.ZoneChestReady(s, z.id);
            for (int i = 0; i < p.chests.Length; i++)
            {
                var c = p.chests[i];
                bool shown = i < at.Length;
                c.image.gameObject.SetActive(shown);
                if (!shown) continue;
                int k = i;
                bool got = s.zoneChests[(int)z.id] > i, can = canClaim == i, big = i == at.Length - 1;
                float f = at[i] / (float)size, sz = big ? 78 : at.Length > 2 ? 58 : 70;
                var rt = c.image.rectTransform;
                rt.sizeDelta = new Vector2(sz, sz);
                rt.anchoredPosition = Point(f) + new Vector2(0, sz * 0.32f);
                c.image.color = got ? new Color(0.6f, 0.6f, 0.6f, 0.5f) : big ? Color.white : Theme.Hex("#e3e9f0");
                c.click.OnClick = () => claim?.Invoke(k);
                c.wobble.enabled = can;
                if (!can) rt.localEulerAngles = Vector3.zero;
            }

            // ghim ải kế: cấp ải kế, đúng chỗ đang đánh; xong đảo thì ẩn
            int next = Progress.NextLevel(s, d, z.id);
            pinOn = next > 0 && prog < size;
            p.pin.gameObject.SetActive(pinOn);
            if (pinOn)
            {
                foreach (var g in p.pinBg.GetComponentsInChildren<Image>(true)) g.color = hue; // viên và mũi nhọn
                p.pinText.text = Loc.F("Lv{0}", next);
                var pt = Point(Mathf.Clamp(progress, 0.03f, 0.97f));
                p.pin.anchoredPosition = pt;
                pinY = pt.y;
                p.pin.SetAsLastSibling();
            }

            // boss: tướng chính ải cuối; chưa mở tới ải cuối thì là bóng đen có dấu "?"; chinh phục xong thì đội vương miện
            var stages = d.ZoneStages(z.id).ToList();
            var last = stages.Count > 0 ? stages[stages.Count - 1] : null;
            var lead = last != null ? Teams.StageLead(last, d) : null;
            var hero = lead != null ? d.Hero(lead.hero) : null;
            bool known = last != null && !BossHidden(s, d, last);
            p.portrait.gameObject.SetActive(hero != null);
            if (hero != null)
            {
                var box = ((RectTransform)p.portrait.transform.parent).rect.size;
                HeroArt.FitBody(p.portrait, hero, Teams.EnemyFormStar(lead), box, 0.98f, 2.2f);
                foreach (var g in p.portrait.GetComponentsInChildren<Image>(true)) g.color = known ? Color.white : Shadow;
            }
            if (!mysteryBase)
            {
                mysteryY = p.mystery.anchoredPosition.y; // chỗ gốc trong prefab (Update làm nhấp nhô quanh đây)
                mysteryBase = true;
            }
            p.mystery.gameObject.SetActive(!known);
            p.crown.SetActive(prog >= size);
            string bossTip = known && hero != null
                ? Loc.F("Boss đảo: {0}, cấp {1}.", hero.name, z.levelMax)
                : Loc.F("Boss đảo cấp {0}. Tới ải cuối mới lộ diện.", z.levelMax);
            p.bossClick.OnClick = () =>
            {
                App.Audio.Play("click");
                UiMotion.Of(p.boss).Punch(0.12f);
                App.Toasts.Show(bossTip);
            };

            // dấu độ khó
            var df = Progress.DifficultyOf(s, d, z);
            p.stamp.color = DifficultyTag.ColorOf(df);
            p.stampText.text = Progress.DifficultyText(df);
        }

        // điểm trên đường mòn ở tỉ lệ f (0 đầu, 1 cuối), toạ độ trong lớp đường mòn
        Vector2 Point(float f)
        {
            var r = p.trail.rect;
            return new Vector2(Mathf.Lerp(r.xMin, r.xMax, f), Wave * Mathf.Sin(f * Periods * Mathf.PI * 2));
        }

        float Slope(float f)
        {
            var r = p.trail.rect;
            float dy = Wave * Periods * Mathf.PI * 2 * Mathf.Cos(f * Periods * Mathf.PI * 2);
            return Mathf.Atan2(dy, r.width) * Mathf.Rad2Deg;
        }

        void BuildDashes()
        {
            if (dashes.Count == 0)
            {
                p.dash.gameObject.SetActive(false);
                for (int i = 0; i < Dashes; i++)
                {
                    var img = Instantiate(p.dash, p.trail, false);
                    img.name = "cham_" + i;
                    img.gameObject.SetActive(true);
                    dashes.Add(img);
                }
                // rương, ghim vẽ trên chấm
                foreach (var c in p.chests)
                    if (c.image)
                        c.image.transform.SetAsLastSibling();
            }
            for (int i = 0; i < dashes.Count; i++)
            {
                float f = (i + 0.5f) / dashes.Count;
                var rt = dashes[i].rectTransform;
                rt.anchoredPosition = Point(f);
                rt.localEulerAngles = new Vector3(0, 0, Slope(f));
            }
        }

        void Update()
        {
            float t = Time.unscaledTime;
            // làn sáng chạy dọc quãng đã đi: chấm phồng lên lần lượt về phía ghim
            for (int i = 0; i < dashes.Count; i++)
            {
                float f = (i + 0.5f) / dashes.Count;
                if (f > progress) break;
                float wave = Mathf.Repeat(t * 0.55f - f * 1.4f, 1f);
                float k = 1 + 0.45f * Mathf.Max(0, 1 - Mathf.Abs(wave - 0.5f) * 8);
                dashes[i].rectTransform.localScale = new Vector3(k, k, 1);
            }
            // ghim nhấp nhô
            if (pinOn) p.pin.anchoredPosition = new Vector2(p.pin.anchoredPosition.x, pinY + 7 * Mathf.Abs(Mathf.Sin(t * 2.6f)));
            // dấu "?" nhấp nhô, nghiêng qua lại
            if (p.mystery && p.mystery.gameObject.activeSelf)
            {
                p.mystery.anchoredPosition = new Vector2(p.mystery.anchoredPosition.x, mysteryY + 5 * Mathf.Sin(t * 2.3f));
                p.mystery.localEulerAngles = new Vector3(0, 0, 7 * Mathf.Sin(t * 1.6f));
            }
        }
    }
}
