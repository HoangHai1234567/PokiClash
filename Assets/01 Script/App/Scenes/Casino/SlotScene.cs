// Scene lều Hội Máy Quả (máy quả 3×3, 5 đường) của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.7, mốc C7). Prefab Screens/CasinoSlot
// (menu "PokiClash/Prefab/Đảo Casino/Lều lữ khách: dựng 3 scene"). Lõi: Core/Casino/Slots.cs. Phần chung: CasinoTableScene.
// - Khung 3 cuộn × 3 hàng; quay: các cuộn chạy hình rồi dừng lần lượt trái sang phải, đúng ô dừng lõi đã chọn (hình trên cuộn là dải
//   thật của cuộn, không xếp suýt trúng). Ô thuộc đường thắng sáng vàng; dòng kể đường thắng ("Đường giữa: 3 ngọc Thủy ×8").
// - Biểu tượng: 5 ngọc hệ, bi, huy hiệu khách mời (ba cái trên một đường: thêm mảnh tướng khách mời), Sao (thay mọi biểu tượng trừ Rương),
//   Rương (2 cái ở đâu cũng được: ×2 cược; 3 cái: lượt miễn phí, quay tự động nối tiếp).
// - Nút Quay (giá), Quay nhanh (bỏ bớt diễn, không tự quay), Bảng trả (trả từng biểu tượng, hoàn trả tính chính xác).
// Mọi vật dựng sẵn trong prefab (9 ô), không sinh lúc chạy.
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
    public sealed class SlotScene : CasinoTableScene
    {
        [System.Serializable]
        public struct Cell
        {
            public Image frame, icon;
            public TextMeshProUGUI label;
        }

        [SerializeField] Cell[] cells; // [cuộn * 3 + hàng]
        [SerializeField] TextMeshProUGUI lines, banner;
        [SerializeField] SketchButton spin, quick, pays;

        public override string Title => Loc.T("Hội Máy Quả");
        protected override string Game => Casino.Slot;
        protected override CasinoTable Table => C;
        protected override bool Busy => spinning;

        static SlotsConfig C => D.Cfg.casino.slots;

        protected override string HelpText =>
            Loc.T("Quay 3 cuộn. Ba biểu tượng giống nhau trên một trong 5 đường (ba hàng ngang, hai đường chéo) thì thắng; Sao thay được mọi biểu tượng trừ Rương.") + "\n" +
            Loc.T("Hai Rương ở đâu cũng được: trả gấp đôi cược. Ba Rương: được lượt quay miễn phí cùng mức cược.") + "\n" +
            Loc.T("Ba huy hiệu khách mời trên một đường: thêm mảnh tướng khách mời. Không có tự quay; Quay nhanh chỉ bỏ bớt diễn.");

        bool spinning, fast;
        SlotRound last;
        static (double rtp, double hit, double freeP, double badge)? exact;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Cell[] cellList, TextMeshProUGUI linesText, TextMeshProUGUI bannerText, SketchButton spinBtn, SketchButton quickBtn, SketchButton paysBtn)
        {
            cells = cellList; lines = linesText; banner = bannerText; spin = spinBtn; quick = quickBtn; pays = paysBtn;
        }

        static readonly string[] LineName = { "Đường giữa", "Đường trên", "Đường dưới", "Chéo xuống", "Chéo lên" };

        public static string SymName(int sym)
        {
            if (sym >= 0 && sym < 5) return Loc.F("ngọc {0}", Elements.Name(Elements.All[sym]));
            switch (sym)
            {
                case Slots.BallSym: return Loc.T("bi");
                case Slots.Badge: return Loc.T("huy hiệu khách mời");
                case Slots.Wild: return Loc.T("Sao");
                case Slots.Chest: return Loc.T("Rương");
                default: return "?";
            }
        }

        protected override void EnterTable()
        {
            spinning = false;
            last = null;
            spin.SetOnClick(Spin);
            quick.SetOnClick(() =>
            {
                fast = !fast;
                Draw();
            });
            pays.SetText(Loc.T("Bảng trả"));
            pays.SetOnClick(PayTable);
            // khung lúc vào: một ô dừng ngẫu nhiên của dải thật
            var sp = Slots.Spin(C, 0, rng);
            ShowGrid(sp.grid, null);
            lines.text = "";
            banner.text = Loc.T("Bấm Quay để thử vận");
            Draw();
        }

        protected override void OnTierChanged() => Draw();

        void Draw()
        {
            var mode = Mode;
            spin.SetText(mode == TableMode.Free ? Loc.T("Quay miễn phí") : mode == TableMode.Practice ? Loc.T("Quay tập") : Loc.F("Quay · {0} bi", BetNow));
            spin.SetRole(mode == TableMode.Practice ? BtnColor.Blue : BtnColor.Green);
            spin.Locked = spinning;
            quick.SetText(fast ? Loc.T("Quay nhanh: bật") : Loc.T("Quay nhanh: tắt"));
            quick.SetRole(fast ? BtnColor.Yellow : BtnColor.Paper);
        }

        void Spin()
        {
            if (spinning) return;
            var mode = Mode;
            var round = Slots.PlayAs(S, D, tier, mode, Now, rng, out var jar, out var extra, out var why);
            if (round == null)
            {
                NoBalls(why);
                return;
            }
            App.Save.Save();
            StartCoroutine(Run(round, mode, jar, extra));
        }

        IEnumerator Run(SlotRound round, TableMode mode, JarResult jar, List<Reward> extra)
        {
            spinning = true;
            last = round;
            Draw();
            lines.text = "";
            int shown = 0;
            for (int k = 0; k < round.spins.Count; k++)
            {
                var sp = round.spins[k];
                banner.text = sp.free ? Loc.F("Lượt miễn phí {0}/{1}", k, round.spins.Count - 1)
                    : mode == TableMode.Free ? Loc.T("Lượt miễn phí đầu tiên!") : mode == TableMode.Practice ? Loc.T("Quay tập") : Loc.T("Đang quay...");
                yield return Reels(sp, sp.free || fast);
                shown += sp.payout;
                var winCells = new HashSet<int>();
                foreach (var (line, sym, p) in sp.lines)
                    for (int r = 0; r < 3; r++) winCells.Add(r * 3 + Slots.LineRows[line][r]);
                if (sp.chests >= 2)
                    for (int r = 0; r < 3; r++)
                        for (int row = 0; row < 3; row++)
                            if (sp.grid[r, row] == Slots.Chest) winCells.Add(r * 3 + row);
                ShowGrid(sp.grid, winCells);
                var parts = sp.lines.Select(l => Loc.F("{0}: 3 {1} ×{2}", Loc.T(LineName[l.line]), SymName(l.sym), l.pays)).ToList();
                if (sp.chests == 2) parts.Add(Loc.F("2 Rương ×{0} cược", C.scatter2));
                if (sp.freeWon > 0) parts.Add(Loc.F("3 Rương: +{0} lượt miễn phí!", sp.freeWon));
                lines.text = parts.Count > 0 ? string.Join("\n", parts) : Loc.T("Không trúng đường nào");
                if (sp.payout > 0 || sp.freeWon > 0) App.Audio.Play(sp.freeWon > 0 ? "prize" : "coin", 0.5f + Mathf.Min(0.5f, sp.payout / (float)Mathf.Max(1, round.bet) * 0.1f));
                yield return new WaitForSecondsRealtime(sp.payout > 0 || sp.freeWon > 0 ? (fast ? 0.5f : 1.0f) : (fast ? 0.15f : 0.4f));
            }
            int total = round.Payout;
            int net = mode == TableMode.Paid ? total - round.bet : mode == TableMode.Free ? Casino.FreeWin(total, round.bet) : 0;
            string free = round.spins.Count > 1 ? " " + Loc.F("({0} lượt miễn phí)", round.spins.Count - 1) : "";
            banner.text = mode == TableMode.Practice ? (total > 0 ? Loc.F("Trúng {0} bi (quay tập, không nhận)", total) : Loc.T("Trượt (quay tập)"))
                : total > 0 ? Loc.F("Trúng {0} bi", total) + free + " · " + (net >= 0 ? Loc.F("lời {0}", net) : Loc.F("lỗ {0}", -net))
                : mode == TableMode.Free ? Loc.T("Trượt, không mất gì") : Loc.F("Trượt · −{0} bi", round.bet);
            spinning = false;
            AfterRound(net, mode == TableMode.Paid ? jar : null, extra);
            Draw();
        }

        // cuộn chạy hình ngẫu nhiên của dải thật rồi dừng lần lượt ở ô đích
        IEnumerator Reels(SlotSpin sp, bool quickSpin)
        {
            float start = Time.unscaledTime;
            float[] stopAt = { quickSpin ? 0.15f : 0.55f, quickSpin ? 0.25f : 0.9f, quickSpin ? 0.35f : 1.25f };
            var offset = new int[3];
            for (int r = 0; r < 3; r++) offset[r] = rng.Int(0, C.reels[r].strip.Length - 1);
            var done = new bool[3];
            float nextStep = 0;
            App.Audio.Play("whoosh", 0.6f);
            while (!done[2])
            {
                float t = Time.unscaledTime - start;
                bool step = t >= nextStep;
                if (step) nextStep = t + 0.06f;
                for (int r = 0; r < 3; r++)
                {
                    if (done[r]) continue;
                    if (t >= stopAt[r])
                    {
                        done[r] = true;
                        for (int row = 0; row < 3; row++) BindCell(r, row, sp.grid[r, row], false);
                        App.Audio.Play("land", 0.5f);
                        continue;
                    }
                    if (!step) continue;
                    offset[r]++;
                    for (int row = 0; row < 3; row++) BindCell(r, row, Slots.Sym(C.reels[r], offset[r], row), false);
                }
                yield return null;
            }
        }

        void ShowGrid(int[,] grid, HashSet<int> win)
        {
            for (int r = 0; r < 3; r++)
                for (int row = 0; row < 3; row++)
                    BindCell(r, row, grid[r, row], win != null && win.Contains(r * 3 + row));
        }

        void BindCell(int reel, int row, int sym, bool win)
        {
            int i = reel * 3 + row;
            if (cells == null || i >= cells.Length) return;
            var c = cells[i];
            c.frame.color = win ? Theme.Yellow : Theme.Paper;
            string icon = sym >= 0 && sym < 5 ? ElemIcon(Elements.All[sym]) : sym == Slots.BallSym ? "ball" : sym == Slots.Badge ? "crown" : sym == Slots.Wild ? "star" : "chest";
            Theme.SetSprite(c.icon, App.Art.Icon(icon));
            c.icon.color = sym >= 0 && sym < 5 ? Color.white : sym == Slots.Badge ? Theme.Hex("#c07a2c") : Color.white;
            c.label.text = sym == Slots.Badge ? Loc.T("khách mời") : sym == Slots.Wild ? Loc.T("Sao") : "";
        }

        // bảng trả: từng biểu tượng × cược mỗi đường, Sao, Rương; hoàn trả tính chính xác trên mọi tổ hợp dừng
        void PayTable()
        {
            exact ??= Slots.Exact(C);
            var e = exact.Value;
            var sb = new System.Text.StringBuilder();
            sb.AppendLine(Loc.F("Cược {0} bi chia đều 5 đường ({1} bi mỗi đường).", BetNow, BetNow / (float)Slots.Lines));
            foreach (var p in C.pays.OrderByDescending(x => x.pays))
                sb.AppendLine(Loc.F("3 {0}: ×{1} cược đường", SymName(p.sym), p.pays));
            sb.AppendLine(Loc.F("3 Sao: ×{0} cược đường", C.wildPays));
            sb.AppendLine(Loc.F("2 Rương ở đâu cũng được: ×{0} tổng cược. 3 Rương: {1} lượt miễn phí", C.scatter2, C.freeSpins));
            var bs = C.badgeShards;
            if (bs.Length > 0) sb.AppendLine(Loc.F("3 huy hiệu trên một đường: +{0} mảnh khách mời (theo bậc cược)", string.Join(" / ", bs)));
            sb.AppendLine();
            sb.AppendLine(Loc.F("Hoàn trả {0}% · trúng {1}% số lượt · ra lượt miễn phí {2}%", (e.rtp * 100).ToString("0.0"), (e.hit * 100).ToString("0"),
                (e.freeP * 100).ToString("0.0")));
            App.Modals.Alert(Loc.T("Bảng trả"), sb.ToString().TrimEnd(), Loc.T("Đóng"));
        }

        // ---------- cho lượt chụp ----------

        public bool Spinning => spinning;
        public void SpinForTest() => Spin();
    }
}
