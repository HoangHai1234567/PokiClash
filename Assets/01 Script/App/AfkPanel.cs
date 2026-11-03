// Hộp AFK (nút đồng hồ ở sảnh): ải đội đang AFK và tướng rơi mảnh, thanh giờ, khay rương AFK kèm giờ mở, các nút Nhận mảnh /
// Đổi ải / Mở ngay / Tăng tốc ×2. Đổi ải sang đảo của ải đang AFK để chọn ải khác ("AFK ải này" ở hộp chuẩn bị trận); nút ẩn khi
// hộp mở từ màn đảo. Bi thụ động không còn ở đây mà ở Cây bi (TreePanel).
// Nút có hình TV đi qua lớp Ads (giới hạn mỗi ngày; bản dev: quảng cáo giả lập 3 giây; chưa có SDK thì ẩn).
// Thẻ Phiêu Lưu: khay 5 ô, rương mở trong 1 giờ. Số liệu tự làm mới mỗi nửa giây khi hộp đang mở.
// Prefab Assets/04 Prefabs/Dialogs/Afk (hộp dùng chung, mở bằng AfkPanel.Open); ô khay là Items/RuongAfk.
using System;
using System.Collections;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class AfkPanel : Dialog
    {
        public static readonly Color ChestColor = Theme.Hex("#8fd3c8");

        [Serializable]
        public struct Parts
        {
            public GameObject[] locked; // chưa qua ải nào: câu "Qua ải 1 để mở", hàng nút OK
            public GameObject[] unlocked; // phần còn lại dưới tiêu đề
            public SketchButton ok;
            public TextMeshProUGUI rate, shardNote, trayNote, boostText, adsNote;
            public UiBar bar;
            public RectTransform tray;
            public AfkSlot slotPrefab;
            public SketchButton claim, openNow, boost;
            public SketchButton change; // Đổi ải (menu PokiClash/Prefab/AFK theo ải)
        }

        [SerializeField] Parts p;

        AfkSlot[] slots;
        readonly Rng rng = new Rng(Rng.RandomSeed());
        float timer;
        bool live; // đã mở khoá, đang làm mới số liệu
        bool busy; // đang xem quảng cáo / mở rương

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
            var st = Afk.Stage(S, D);
            var pool = Afk.Pool(st);
            p.rate.text = st == null ? "" : $"Đang AFK: {D.Zone(st.zone).name} · Ải {st.idx}";
            p.shardNote.text = pool.Count > 0
                ? $"Mỗi giờ {D.Cfg.afk.shardChance * 100:0}% ra 1 mảnh: {string.Join(", ", pool.Select(x => D.Hero(x.hero).name))}"
                : "Ải này không rơi mảnh tướng, chỉ ra rương";
            if (p.change)
            {
                p.change.gameObject.SetActive(App.Router.Current != SceneIds.Zone);
                p.change.SetOnClick(ChangeStage);
            }

            for (int i = p.tray.childCount - 1; i >= 0; i--) Destroy(p.tray.GetChild(i).gameObject);
            int n = Afk.Slots(S, D.Cfg, Now); // Thẻ Phiêu Lưu: 5 ô
            float w = n > 4 ? 144 : 176, step = w + 16;
            slots = new AfkSlot[n];
            for (int i = 0; i < n; i++)
            {
                int idx = i;
                var slot = Ui.Spawn(p.slotPrefab, p.tray);
                slot.name = "afk_ruong_" + i;
                slot.Arrange((i - (n - 1) / 2f) * step, w);
                slot.Button.SetOnClick(() => SlotClick(idx));
                slots[i] = slot;
            }

            p.openNow.SetOnClick(OpenNow);
            p.boost.SetOnClick(Boost);
            p.claim.SetOnClick(Claim);
            p.adsNote.gameObject.SetActive(Ads.Ready);
            if (Ads.Ready)
                p.adsNote.text = Ads.NoAds ? "Đã mua Bỏ quảng cáo: nút có hình TV nhận thưởng ngay." : "Nút có hình TV: xem một quảng cáo ngắn để nhận thưởng.";
        }

        // ---------- làm mới ----------

        static string Clock(double ms)
        {
            long sec = (long)System.Math.Ceiling(System.Math.Max(0, ms) / 1000);
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
            p.bar.Set((float)pd.hours, (float)cfg.afkCapH, 0, $"{Dec(pd.hours)} / {cfg.afkCapH:0} giờ");

            var times = Afk.ChestTimes(s, cfg, now);
            for (int i = 0; i < slots.Length; i++)
            {
                bool has = i < times.Count;
                bool ready = has && times[i].ready <= now;
                slots[i].Set(has, ready, !has ? "" : ready ? "Mở được" : times[i].start <= now ? Clock(times[i].ready - now) : "Chờ");
            }
            p.trayNote.text = s.afk.chests.Count >= Afk.Slots(s, cfg, now) ? "Khay đầy, mở bớt rương"
                : $"Cứ {cfg.afk.chestEveryH:0} giờ AFK ra 1 rương; rương tiếp: {Dec(s.afk.chestAcc)} / {cfg.afk.chestEveryH:0} giờ. Rương đếm {Afk.OpenH(s, cfg, now):0} giờ rồi mở được.";

            bool counting = times.Count > 0 && times[0].ready > now;
            p.openNow.gameObject.SetActive(counting && Ads.Ready);
            Ads.Bind(p.openNow, "Mở ngay", Ads.AfkChestOpen);
            bool boosting = Afk.Boosting(s, now);
            p.boost.gameObject.SetActive(!boosting && Ads.Ready);
            p.boostText.gameObject.SetActive(boosting);
            Ads.Bind(p.boost, "Tăng tốc ×2", Ads.AfkBoost, !pd.full); // đầy giờ thì AFK dừng, tăng tốc vô ích: nhận trước
            if (boosting) p.boostText.text = $"Tăng tốc ×2: còn {Clock(s.afk.boostUntil - now)}";

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
            App.Toasts.Show(shards > 0 ? $"Nhặt {shards} mảnh tướng" : "Lần này chưa nhặt được mảnh tướng", App.Art.Icon("shard"));
            foreach (var x in r.shards)
                if (x.unlocked) App.Toasts.Show($"Mở khóa {D.Hero(x.hero).name}!", App.Art.Icon("star"));
            Close();
        }

        // sang đảo của ải đang AFK: chạm ải đã thắng, bấm "AFK ải này"
        void ChangeStage()
        {
            var st = Afk.Stage(S, D);
            Close();
            App.Toasts.Show("Chạm ải đã thắng, bấm \"AFK ải này\"", App.Art.Icon("clock"));
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
            App.Toasts.Show(i == 0 ? $"Còn {Clock(times[0].ready - now)} nữa mới mở được" : "Rương mở lần lượt, mở rương đầu khay trước", App.Art.Icon("clock"));
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

        IEnumerator ShowChest(System.Collections.Generic.List<Reward> rs, int lv)
        {
            busy = true;
            yield return ChestBox.Show("Rương AFK", SlotKind.ChestWood, ChestColor, rs, "Nhận");
            busy = false;
            if (S.level > lv) Dialogs.LevelUp(lv, S.level);
            if (this) Refresh();
        }

        void Boost()
        {
            if (Afk.Pending(S, D.Cfg, Now).full)
            {
                App.Toasts.Show("Đã đầy giờ AFK: nhận bi trước rồi hãy tăng tốc", App.Art.Icon("clock"));
                return;
            }
            busy = true;
            Ads.Show(Ads.AfkBoost, ok =>
            {
                busy = false;
                if (ok && Afk.Boost(S, D.Cfg, Now))
                {
                    App.Save.Save();
                    App.Toasts.Show($"Tăng tốc ×2 trong {D.Cfg.afk.boostH:0} giờ", App.Art.Icon("clock"));
                }
                Refresh();
            });
        }
    }
}
