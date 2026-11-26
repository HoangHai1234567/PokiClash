// Hộp AFK "Đội tự đi ải" (nút đồng hồ ở sảnh). Bố cục mới (người dùng 2026-11-27: hộp cũ "nhìn không rõ ràng, khó hiểu và xấu", chọn
// hướng "cảnh + thanh mốc"): ít chữ, nhiều hình, một nút chính.
//   - Thẻ cảnh: ảnh sàn đấu của ải đang AFK (StageView.ArenaOf), các tướng rơi mảnh đứng trên sàn, chip trạng thái ở góc (Đang đi /
//     ×2 còn … / Đầy giờ); dải dưới thẻ: tên đảo · ải, mặt các tướng rơi mảnh và tỉ lệ mỗi giờ, nút Đổi ải ("afk_doi_ai"; sang đảo của
//     ải đang AFK để chọn ải khác bằng "AFK ải này"; ẩn khi hộp mở từ màn đảo).
//   - Giờ: "3,4 / 12 giờ" to, số lượt rơi mảnh đã dồn (mỗi giờ tròn một lượt); thanh dày chia vạch từng giờ, hình rương nằm trên thanh ở
//     đúng giờ sẽ ra rương kế tiếp (rương ra theo giờ dồn riêng chestAcc, không trùng mốc 3/6/9 của thanh), hết chỗ khay thì thôi vẽ.
//   - Khay "Rương đường đi": rương gỗ thật có rig (AfkSlot), nút TV "Mở ngay" nằm ngay dưới rương đầu khay đang đếm; chạm rương mở được
//     thì mở (hộp mở rương dùng rig: nhắc, gồng, bật nắp).
//   - Nút: Nhận mảnh (chính, xanh) và TV Tăng tốc ×2 (phụ, cam; đang tăng tốc thì ẩn, Nhận ra giữa). Luật chơi gom vào nút (i).
// Nút có hình TV đi qua lớp Ads (giới hạn mỗi ngày; bản dev: quảng cáo giả lập 3 giây; chưa có SDK thì ẩn). Bi thụ động ở Cây bi.
// Thẻ Phiêu Lưu: khay 5 ô, rương mở trong 1 giờ. Số liệu tự làm mới mỗi nửa giây khi hộp đang mở.
// Prefab Assets/04 Prefabs/Dialogs/Afk (menu "PokiClash/Prefab/Hộp thoại và màn/AFK: hộp Đội tự đi ải", EditorTools.AfkDialogMenu),
// mở bằng AfkPanel.Open; ô khay là Items/RuongAfk (dựng sẵn đủ ô trong prefab).
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class AfkPanel : Dialog
    {
        public static readonly Color ChestColor = Theme.Hex("#8fd3c8"); // nhãn AFK trên bản đồ đảo (AfkStageMenu)
        public static readonly Color GoColor = Theme.Hex("#5fae4e"), BoostColor = Theme.Hex("#f08a3c"), FullColor = Theme.Hex("#d9534f");

        [Serializable]
        public struct Parts
        {
            public GameObject[] locked; // chưa qua ải nào: câu "Qua ải 1 để mở", nút OK
            public GameObject[] unlocked; // phần còn lại dưới tiêu đề
            public SketchButton ok;
            public SketchButton info; // nút (i): bật / tắt tờ luật
            public Button rules; // tờ luật phủ trên nội dung, chạm để tắt
            public TextMeshProUGUI rulesText;
            // thẻ cảnh
            public RectTransform sceneMask; // khung cắt ảnh sàn đấu
            public Image scene;
            public RectTransform heroes; // chỗ các tướng rơi mảnh đứng (gốc chân ở mép dưới)
            public Image statusChip;
            public TextMeshProUGUI status;
            public TextMeshProUGUI stage, shard;
            public Image[] faces; // mặt tướng rơi mảnh trong dải dưới thẻ
            public SketchButton change; // Đổi ải
            // giờ
            public TextMeshProUGUI hours, rolls;
            public UiBar bar;
            public RectTransform[] ticks; // vạch từng giờ trên thanh (dựng dư, ẩn bớt theo số giờ tối đa)
            public RectTransform[] marks; // hình rương trên thanh ở giờ ra rương kế tiếp
            // khay
            public TextMeshProUGUI trayNote;
            public AfkSlot[] slots;
            public SketchButton openNow;
            // nút
            public SketchButton boost, claim;
        }

        [SerializeField] Parts p;

        const float SlotW4 = 168, SlotW5 = 148, SlotGap4 = 28, SlotGap5 = 18;
        static readonly float[] HeroH = { 250, 205, 205 }; // khung cảnh cao ~290 trên dải dưới
        static readonly float[] HeroDx = { 0, 150, -130 }; // tướng đầu giữa bệ, hai tướng sau hai bên (px thẻ)
        // bệ sau của ảnh sàn đấu (mọi ảnh BattleBG cùng bố cục: bệ đối thủ ~28% bề ngang, ~70% bề cao tính từ trên): cắt ảnh cho bệ nằm
        // ngay trên dải dưới, tướng đứng giữa bệ
        static readonly Vector2 ArenaSpot = new Vector2(0.28f, 0.705f);
        StageDef sceneStage;
        bool sceneSet;

        int slotCount;
        readonly Rng rng = new Rng(Rng.RandomSeed());
        float timer;
        bool live; // đã mở khoá, đang làm mới số liệu
        bool busy; // đang xem quảng cáo / mở rương
        Vector2 claimHome;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        public static void Open() => App.Modals.Open<AfkPanel>().Show();

        void Show()
        {
            bool locked = Progress.TotalCleared(S) == 0;
            foreach (var g in p.locked) g.SetActive(locked);
            foreach (var g in p.unlocked) g.SetActive(!locked);
            if (p.rules) p.rules.gameObject.SetActive(false);
            if (p.info) p.info.gameObject.SetActive(!locked);
            if (locked)
            {
                p.ok.SetOnClick(Close);
                return;
            }
            Build();
            live = true;
            Refresh();
        }

        // ---------- gán ----------

        void Build()
        {
            var cfg = D.Cfg;
            var st = Afk.Stage(S, D);
            var pool = Afk.Pool(st);
            var heroes = pool.Select(x => D.Hero(x.hero)).Where(h => h != null).ToList();

            // thẻ cảnh: sàn đấu của ải, tướng rơi mảnh đứng trên bệ
            sceneStage = st;
            sceneSet = false;
            SetScene();
            for (int i = p.heroes.childCount - 1; i >= 0; i--) Destroy(p.heroes.GetChild(i).gameObject);
            float cx = p.heroes.rect.width * ArenaSpot.x;
            for (int i = Mathf.Min(heroes.Count, HeroH.Length) - 1; i >= 0; i--) // tướng đầu vẽ sau cùng (đứng trước)
            {
                var pr = HeroArt.Portrait(p.heroes, heroes[i], HeroH[i]);
                pr.anchorMin = pr.anchorMax = new Vector2(0, 0);
                pr.pivot = new Vector2(0.5f, 0);
                pr.anchoredPosition = new Vector2(cx + HeroDx[i], 0);
                foreach (var g in pr.GetComponentsInChildren<Graphic>(true)) g.raycastTarget = false;
            }

            p.stage.text = st == null ? "" : Loc.F("{0} · Ải {1}", D.Zone(st.zone).name, st.idx);
            p.shard.text = heroes.Count > 0
                ? Loc.F("Mảnh {0} · {1:0}% mỗi giờ", string.Join(", ", heroes.Select(h => h.name)), cfg.afk.shardChance * 100)
                : Loc.T("Ải này không rơi mảnh, chỉ ra rương");
            for (int i = 0; i < p.faces.Length; i++)
            {
                var face = i < heroes.Count ? HeroArt.Face(heroes[i]) : null; // tướng .atomik chưa có ảnh mặt: bỏ ô
                p.faces[i].gameObject.SetActive(face);
                if (face) Theme.SetSprite(p.faces[i], face);
            }
            if (p.change)
            {
                p.change.gameObject.SetActive(App.Router.Current != SceneIds.Zone);
                p.change.SetOnClick(ChangeStage);
            }

            // vạch từng giờ trên thanh
            int cap = Mathf.Max(1, Mathf.RoundToInt((float)cfg.afkCapH));
            for (int i = 0; i < p.ticks.Length; i++)
            {
                bool on = i < cap - 1;
                p.ticks[i].gameObject.SetActive(on);
                if (on) p.ticks[i].anchorMin = p.ticks[i].anchorMax = new Vector2((i + 1f) / cap, 0.5f);
            }

            // khay: đủ ô theo khay (4, Thẻ Phiêu Lưu 5), xếp giữa
            slotCount = Mathf.Min(Afk.Slots(S, cfg, Now), p.slots.Length);
            float w = slotCount > 4 ? SlotW5 : SlotW4, step = w + (slotCount > 4 ? SlotGap5 : SlotGap4);
            for (int i = 0; i < p.slots.Length; i++)
            {
                var slot = p.slots[i];
                bool on = i < slotCount;
                slot.gameObject.SetActive(on);
                if (!on) continue;
                int idx = i;
                slot.name = "afk_ruong_" + i;
                slot.Arrange((i - (slotCount - 1) / 2f) * step, w);
                slot.Button.SetOnClick(() => SlotClick(idx));
            }
            // Mở ngay đứng ngay dưới rương đầu khay
            var on0 = p.openNow.Rect;
            on0.anchoredPosition = new Vector2(p.slots[0].Rect.anchoredPosition.x, on0.anchoredPosition.y);
            on0.sizeDelta = new Vector2(Mathf.Max(w + 100, 268), on0.sizeDelta.y); // đủ chỗ hình TV và "MỞ NGAY (4)" cỡ chữ thường

            p.openNow.SetOnClick(OpenNow);
            p.boost.SetOnClick(Boost);
            p.claim.SetOnClick(Claim);
            claimHome = p.claim.Rect.anchoredPosition;
            if (p.info) p.info.SetOnClick(() => p.rules.gameObject.SetActive(!p.rules.gameObject.activeSelf));
            if (p.rules)
            {
                p.rules.onClick.RemoveAllListeners();
                p.rules.onClick.AddListener(() => p.rules.gameObject.SetActive(false));
            }
            if (p.rulesText) p.rulesText.text = RulesText(cfg);
        }

        // ảnh sàn đấu của ải AFK phủ kín bề ngang khung, cắt cho bệ sau nằm ngay dưới chân tướng; ảnh nằm trong gói tải sau có thể chưa
        // có lúc mở hộp: Refresh gọi lại tới khi có
        void SetScene()
        {
            if (sceneSet) return;
            var art = StageView.ArenaOf(sceneStage, out var tint);
            p.scene.gameObject.SetActive(art);
            if (!art) return;
            sceneSet = true;
            Theme.SetSprite(p.scene, art);
            p.scene.color = tint;
            var m = p.sceneMask.rect.size;
            float h = Mathf.Max(m.y, m.x * art.rect.height / art.rect.width);
            float feetTop = m.y - p.heroes.offsetMin.y; // chân tướng tính từ mép trên khung
            var sr = p.scene.rectTransform;
            sr.anchorMin = sr.anchorMax = new Vector2(0.5f, 1);
            sr.pivot = new Vector2(0.5f, 1);
            sr.sizeDelta = new Vector2(m.x, h);
            sr.anchoredPosition = new Vector2(0, Mathf.Clamp(ArenaSpot.y * h - feetTop, 0, h - m.y));
        }

        string RulesText(BalanceConfig cfg)
        {
            var c = cfg.afk;
            var lines = new List<string>
            {
                Loc.F("Đội tự đánh một ải đã thắng, tối đa {0:0} giờ. Đầy giờ thì đội dừng: nhớ quay lại nhận.", cfg.afkCapH),
                Loc.F("Mỗi giờ tròn là một lượt: {0:0}% ra 1 mảnh tướng của ải.", c.shardChance * 100),
                Loc.F("Cứ {0:0} giờ ra 1 rương. Rương đầu khay đếm {1:0} giờ rồi mở được, rương sau chờ lượt.", c.chestEveryH, Afk.OpenH(S, cfg, Now)),
            };
            if (Ads.Ready) lines.Add(Loc.F("Nút có hình TV: xem quảng cáo ngắn để mở rương ngay, hoặc tăng tốc ×2 trong {0:0} giờ.", c.boostH));
            lines.Add(Loc.T("Đổi ải: chạm ải đã thắng trên đảo, bấm \"AFK ải này\"."));
            return "• " + string.Join("\n• ", lines);
        }

        // ---------- làm mới ----------

        static string Clock(double ms)
        {
            long sec = (long)Math.Ceiling(Math.Max(0, ms) / 1000);
            long h = sec / 3600, mm = sec / 60 % 60, ss = sec % 60;
            return h > 0 ? $"{h}:{mm:00}:{ss:00}" : $"{mm}:{ss:00}";
        }

        static string Dec(double v) => v.ToString("0.0", System.Globalization.CultureInfo.InvariantCulture).Replace('.', ',');

        void Refresh()
        {
            if (!live || Modal == null || !Modal.IsOpen) return;
            var s = S;
            var cfg = D.Cfg;
            double now = Now;
            var pd = Afk.Pending(s, cfg, now);
            bool boosting = Afk.Boosting(s, now);
            float cap = (float)cfg.afkCapH;
            SetScene();

            // trạng thái ở góc thẻ cảnh
            p.statusChip.color = pd.full ? FullColor : boosting ? BoostColor : GoColor;
            p.status.text = pd.full ? Loc.T("ĐẦY GIỜ") : boosting ? Loc.F("×2 · {0}", Clock(s.afk.boostUntil - now)) : Loc.T("ĐANG ĐI");

            // giờ, lượt mảnh, thanh, rương trên thanh
            p.hours.text = Loc.F("{0} / {1:0} giờ", Dec(pd.hours), cap);
            p.hours.color = pd.full ? FullColor : Theme.Ink;
            int rolls = (int)Math.Floor(pd.hours);
            p.rolls.text = Afk.Pool(Afk.Stage(s, D)).Count == 0 ? "" : rolls > 0 ? Loc.F("{0} lượt rơi mảnh", rolls) : Loc.T("Lượt mảnh đầu sau 1 giờ");
            p.bar.Set((float)pd.hours, cap, 0, "");
            int slots = Afk.Slots(s, cfg, now);
            int room = pd.full ? 0 : slots - s.afk.chests.Count;
            double next = pd.hours + (cfg.afk.chestEveryH - s.afk.chestAcc);
            for (int i = 0; i < p.marks.Length; i++)
            {
                double at = next + i * cfg.afk.chestEveryH;
                bool on = i < room && at <= cap + 1e-6;
                p.marks[i].gameObject.SetActive(on);
                if (on) p.marks[i].anchorMin = p.marks[i].anchorMax = new Vector2((float)(at / cap), p.marks[i].anchorMin.y);
            }

            // khay
            var times = Afk.ChestTimes(s, cfg, now);
            for (int i = 0; i < slotCount; i++)
            {
                if (i >= times.Count)
                {
                    p.slots[i].Set(AfkSlot.State.Empty, "");
                    continue;
                }
                var (start, ready) = times[i];
                if (ready <= now) p.slots[i].Set(AfkSlot.State.Ready, Loc.T("MỞ!"), 1, i * 0.3f);
                else if (start <= now) p.slots[i].Set(AfkSlot.State.Counting, Clock(ready - now), (float)((now - start) / Math.Max(1, ready - start)), i * 0.3f);
                else p.slots[i].Set(AfkSlot.State.Waiting, Loc.T("Chờ"));
            }
            double rate = boosting ? cfg.afk.boostMult : 1;
            p.trayNote.text = s.afk.chests.Count >= slots ? Loc.T("Khay đầy: mở rương để rương mới vào")
                : pd.full ? Loc.T("Đầy giờ: nhận để đội đi tiếp")
                : Loc.F("Rương kế sau {0}", Clock((cfg.afk.chestEveryH - s.afk.chestAcc) / rate * 3600000));
            p.trayNote.color = s.afk.chests.Count >= slots || pd.full ? FullColor : Theme.Ink2;

            bool counting = times.Count > 0 && times[0].ready > now && times[0].start <= now;
            p.openNow.gameObject.SetActive(counting && Ads.Ready);
            Ads.Bind(p.openNow, Loc.T("Mở ngay"), Ads.AfkChestOpen);

            // nút: tăng tốc ẩn khi đang tăng tốc (chip góc thẻ đếm giờ), Nhận ra giữa
            bool showBoost = !boosting && Ads.Ready;
            p.boost.gameObject.SetActive(showBoost);
            Ads.Bind(p.boost, Loc.T("Tăng tốc ×2"), Ads.AfkBoost, !pd.full); // đầy giờ thì AFK dừng, tăng tốc vô ích: nhận trước
            p.claim.Rect.anchoredPosition = showBoost ? claimHome : new Vector2(0, claimHome.y);
            p.claim.Interactable = pd.hours >= 1;
        }

        void Update()
        {
            if (!live || busy) return;
            if ((timer += Time.unscaledDeltaTime) < 0.5f) return;
            timer = 0;
            Refresh();
        }

        // ---------- việc ----------

        void Claim()
        {
            var r = Afk.Claim(S, D, Now, 1, rng);
            App.Save.Save();
            int shards = 0;
            foreach (var x in r.shards) shards += x.n;
            App.Audio.Play(shards > 0 ? "coin" : "click");
            Haptics.Play(shards > 0 ? Haptic.Reward : Haptic.UiTap);
            App.Toasts.Show(shards > 0 ? Loc.F("Nhặt {0} mảnh tướng", shards) : Loc.T("Lần này chưa nhặt được mảnh tướng"), App.Art.Icon("shard"));
            foreach (var x in r.shards)
                if (x.unlocked) App.Toasts.Show(Loc.F("Mở khóa {0}!", D.Hero(x.hero).name), App.Art.Icon("star"));
            Close();
        }

        // sang đảo của ải đang AFK: chạm ải đã thắng, bấm "AFK ải này"
        void ChangeStage()
        {
            var st = Afk.Stage(S, D);
            Close();
            App.Toasts.Show(Loc.T("Chạm ải đã thắng, bấm \"AFK ải này\""), App.Art.Icon("clock"));
            App.Router.Go(SceneIds.Zone, st != null ? st.zone : ZoneScene.LastZone);
        }

        void SlotClick(int i)
        {
            if (busy) return;
            double now = Now;
            var times = Afk.ChestTimes(S, D.Cfg, now);
            if (i >= times.Count) return;
            if (i == 0 && times[0].ready <= now)
            {
                OpenChest(false);
                return;
            }
            App.Audio.Play("error");
            App.Toasts.Show(i == 0 ? Loc.F("Còn {0} nữa mới mở được", Clock(times[0].ready - now)) : Loc.T("Rương mở lần lượt, mở rương đầu khay trước"), App.Art.Icon("clock"));
        }

        void OpenNow()
        {
            busy = true;
            Ads.Show(Ads.AfkChestOpen, ok =>
            {
                busy = false;
                if (ok) OpenChest(true);
                Refresh();
            });
        }

        void OpenChest(bool early)
        {
            int lv = S.level;
            var rs = Afk.OpenChest(S, D, Now, rng, early);
            if (rs == null) return;
            App.Save.Save();
            App.I.StartCoroutine(ShowChest(rs, lv));
        }

        IEnumerator ShowChest(List<Reward> rs, int lv)
        {
            busy = true;
            // rương gỗ thật (ảnh + rig như máy bi), không tô màu riêng
            yield return ChestBox.Show(Loc.T("Rương AFK"), SlotKind.ChestWood, null, rs, Loc.T("Nhận"));
            busy = false;
            if (S.level > lv) Dialogs.LevelUp(lv, S.level);
            if (this) Refresh();
        }

        void Boost()
        {
            if (Afk.Pending(S, D.Cfg, Now).full)
            {
                App.Toasts.Show(Loc.T("Đã đầy giờ AFK: nhận trước rồi hãy tăng tốc"), App.Art.Icon("clock"));
                return;
            }
            busy = true;
            Ads.Show(Ads.AfkBoost, ok =>
            {
                busy = false;
                if (ok && Afk.Boost(S, D.Cfg, Now))
                {
                    App.Save.Save();
                    App.Toasts.Show(Loc.F("Tăng tốc ×2 trong {0:0} giờ", D.Cfg.afk.boostH), App.Art.Icon("clock"));
                }
                Refresh();
            });
        }
    }
}
