// Hộp Quán trọ của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.8, mốc C6): bảng nhiệm vụ đảo trong ngày. Bà chủ quán dẫn chuyện.
// - Mỗi việc một dòng: tên việc, thanh tiến độ "2/5", quà; nút Nhận (xong, chưa nhận) / Đã nhận / Đi làm (đưa tới trò của việc đó).
// - Dòng cuối: quà xong cả ngày (nhận khi đã nhận đủ từng việc).
// - Việc mới lúc 0 giờ (đồng hồ đếm ngược).
// Prefab Dialogs/QuanTro (menu "PokiClash/Prefab/Đảo Casino/Quán trọ: dựng hộp"), các dòng dựng sẵn. Lõi: Casino.InnToday / ClaimQuest /
// ClaimInnAll; tiến độ ghi bằng Casino.Track ở từng trò (thả bi ghi ở MachineScene).
using System;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class InnDialog : Dialog
    {
        [Serializable]
        public struct Row
        {
            public GameObject root;
            public Image card;
            public TextMeshProUGUI text, reward;
            public UiBar bar;
            public SketchButton act;
        }

        [SerializeField] TextMeshProUGUI title, sub, clock;
        [SerializeField] Row[] rows;
        [SerializeField] Image allCard;
        [SerializeField] TextMeshProUGUI allText, allReward;
        [SerializeField] SketchButton allClaim;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;
        static readonly Color DoneTint = Theme.Hex("#e6f7d9");

        Action<string> goTo;
        float nextTick;

        // Dùng khi dựng prefab (Editor).
        public void Setup(TextMeshProUGUI titleText, TextMeshProUGUI subText, TextMeshProUGUI clockText, Row[] rowList, Image all,
            TextMeshProUGUI allT, TextMeshProUGUI allR, SketchButton allBtn)
        {
            title = titleText; sub = subText; clock = clockText; rows = rowList; allCard = all; allText = allT; allReward = allR; allClaim = allBtn;
        }

        // go: mở trò của việc (mã trò Casino.*, hoặc SceneIds.Machine cho việc thả bi)
        public void Show(Action<string> go)
        {
            goTo = go;
            Render();
        }

        void Update()
        {
            if (Time.unscaledTime < nextTick || !clock) return;
            nextTick = Time.unscaledTime + 0.5f;
            Clock();
        }

        void Clock()
        {
            double now = Now;
            double left = Casino.Day - Casino.Hour(now) * 3600000.0;
            clock.text = Loc.F("Việc mới sau {0}", ShopUi.Clock(left));
        }

        void Render()
        {
            var s = S;
            var d = D;
            double now = Now;
            var st = Casino.Roll(s, d, now);
            var qs = Casino.InnToday(s, d, now);
            title.text = Loc.T("Quán trọ");
            int claimed = qs.Count(q => st.innClaimed.Contains(q.id));
            sub.text = claimed >= qs.Count && qs.Count > 0
                ? Loc.T("Bà chủ quán: Xong hết việc rồi à? Giỏi lắm! Ngồi nghỉ, mai lại có việc mới.")
                : Loc.T("Bà chủ quán: Ghé nghỉ chân đi! Hôm nay quán có mấy việc vặt, làm xong thì ghé nhận quà.");
            Clock();
            for (int i = 0; i < rows.Length; i++)
            {
                var row = rows[i];
                bool has = i < qs.Count;
                row.root.SetActive(has);
                if (!has) continue;
                var q = qs[i];
                int prog = Casino.InnProg(s, q.id);
                bool done = Casino.QuestDone(s, q), got = st.innClaimed.Contains(q.id);
                row.text.text = q.Text;
                row.reward.text = CasinoUi.Items(q.items);
                row.bar.Set(Mathf.Min(prog, q.n), q.n, 0, $"{Mathf.Min(prog, q.n)}/{q.n}", true);
                row.card.color = got ? DoneTint : Theme.Paper;
                var b = row.act;
                string id = q.id;
                if (got)
                {
                    b.SetText(Loc.T("Đã nhận"));
                    b.SetRole(BtnColor.Paper);
                    b.Locked = true;
                    b.SetOnClick(null);
                }
                else if (done)
                {
                    b.Locked = false;
                    b.SetText(Loc.T("Nhận"));
                    b.SetRole(BtnColor.Yellow);
                    b.SetOnClick(() => Claim(id));
                }
                else
                {
                    string game = GameOf(q.kind);
                    b.Locked = false;
                    b.SetText(Loc.T("Đi làm"));
                    b.SetRole(BtnColor.Green);
                    b.SetOnClick(() => Go(game));
                }
            }
            // quà xong cả ngày
            bool allGot = st.innAll, allReady = Casino.InnAllReady(s, d, now);
            allText.text = Loc.F("Xong cả {0} việc hôm nay ({1}/{0})", qs.Count, claimed);
            allReward.text = CasinoUi.Items(d.Cfg.casino.inn.all);
            allCard.color = allGot ? DoneTint : allReady ? Theme.Hex("#fff1c2") : Theme.Paper2;
            allClaim.SetText(allGot ? Loc.T("Đã nhận") : Loc.T("Nhận"));
            allClaim.SetRole(allReady ? BtnColor.Yellow : BtnColor.Paper);
            allClaim.Locked = !allReady;
            allClaim.SetOnClick(allReady ? ClaimAll : (Action)null);
        }

        // trò để làm việc kind
        public static string GameOf(string kind)
        {
            switch (kind)
            {
                case "fish":
                case "fish_rare": return Casino.Fishing;
                case "race":
                case "race_top3": return Casino.Race;
                case "market_buy": return Casino.Market;
                case "ug_win": return Casino.Underground;
                case "drop": return SceneIds.Machine;
                case "table":
                {
                    var d = D;
                    var sp = Casino.Active(d, Now).FirstOrDefault(x => d.Cfg.casino.Table(x.ev.booth) != null);
                    return sp?.ev.booth;
                }
                default: return null;
            }
        }

        void Go(string game)
        {
            if (game == null)
            {
                App.Toasts.Show(Loc.T("Hôm nay chưa có lều lữ khách nào ở bến"), Icon("flag"));
                return;
            }
            var go = goTo;
            Close();
            go?.Invoke(game);
        }

        void Claim(string id)
        {
            var r = Casino.ClaimQuest(S, D, id, Now, new Rng(Rng.RandomSeed()));
            if (r.Count == 0) return;
            App.Save.Save();
            App.Audio.Play("coin");
            Haptics.Play(Haptic.UiTap);
            App.Toasts.Show(CasinoUi.Rewards(r), Icon("star"));
            Render();
            int i = Casino.InnToday(S, D, Now).FindIndex(q => q.id == id);
            if (i >= 0 && i < rows.Length) StartCoroutine(ChestBox.Pop((RectTransform)rows[i].root.transform, 1.05f));
        }

        void ClaimAll()
        {
            var r = Casino.ClaimInnAll(S, D, Now, new Rng(Rng.RandomSeed()));
            if (r.Count == 0) return;
            App.Save.Save();
            App.Audio.Play("chest");
            Haptics.Play(Haptic.Win);
            App.Toasts.Show(Loc.T("Quà xong cả ngày: ") + CasinoUi.Rewards(r), Icon("star"));
            Render();
            StartCoroutine(ChestBox.Pop((RectTransform)allCard.transform, 1.06f));
        }
    }
}
