# Vá mã cho mốc D4 (lều Vòng Xoay có Lão Mực, GD_Claude/31): sửa từng đoạn trong các file dùng chung (không chép đè cả file, vì
# nhiều phiên cùng sửa), chép file mới. Chạy lại được (đoạn đã vá thì bỏ qua).
#   py -3 -I va_ma.py overlay   -> ghi bản đã vá vào ArtGen/Casino/so_lieu/overlay (để biên dịch thử ngoài Unity)
#   py -3 -I va_ma.py apply     -> vá thẳng vào Assets/01 Script (lúc giữ lượt Unity)
#   py -3 -I va_ma.py clean     -> xoá các file của D4 trong overlay
import os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
SCRIPT = os.path.join(PROJ, "Assets", "01 Script")
OVER = os.path.join(PROJ, "ArtGen", "Casino", "so_lieu", "overlay")
mode = sys.argv[1] if len(sys.argv) > 1 else "overlay"

# file mới: (nguồn, đích tương đối trong 01 Script)
NEW = [
    (os.path.join(HERE, "RouletteBall.cs"), "Core/Casino/RouletteBall.cs"),
    (os.path.join(HERE, "RouletteScene.cs"), "App/Scenes/Casino/RouletteScene.cs"),
    (os.path.join(HERE, "CasinoRouletteTour.cs"), "Editor/CasinoRouletteTour.cs"),
]

PATCH = {}


def patch(rel):
    def deco(fn):
        PATCH[rel] = fn
        return fn
    return deco


def once(s, old, new, mark=None):
    """thay old bằng new đúng một lần; đã có mark (mặc định: new) thì bỏ qua"""
    if (mark or new) in s:
        return s
    if s.count(old) != 1:
        raise SystemExit("Không thấy (hoặc thấy nhiều) đoạn cần vá: " + old[:80])
    return s.replace(old, new)


@patch("Core/CasinoConfig.cs")
def _(s):
    s = once(s, "        public int starShards = 2;\n    }",
             "        public int starShards = 2;\n"
             "        // trọng số ra của 26 ô (ô i = hệ i / 5, số i % 5 + 1; ô 25 Sao Vàng). Rỗng = 26 ô đều nhau (1/26). Đây là chỗ CHỈNH TỈ LỆ RA:\n"
             "        // viên bi trên màn chỉ diễn theo ô lõi đã chọn (Core/Casino/RouletteBall.cs). Hoàn trả hiện trong Cách chơi tính theo đây.\n"
             "        public int[] weights = new int[0];\n    }", mark="public int[] weights = new int[0];")
    s = once(s, "                r.starShards = J.Int(ro, \"starShards\", r.starShards);\n",
             "                r.starShards = J.Int(ro, \"starShards\", r.starShards);\n"
             "                if (ro.ContainsKey(\"weights\")) r.weights = Ints(ro[\"weights\"]);\n", mark="r.weights = Ints(")
    s = once(s, "            if (slots.reels.Count != 3 ||",
             "            if (roulette.weights.Length != 0 && (roulette.weights.Length != 26 || roulette.weights.Any(w => w < 0) || roulette.weights.Sum() <= 0))\n"
             "                err.Add(\"casino.roulette.weights: cần đúng 26 số không âm, tổng > 0 (hoặc bỏ trống)\");\n"
             "            if (slots.reels.Count != 3 ||", mark="casino.roulette.weights")
    return s


@patch("Core/Casino/Roulette.cs")
def _(s):
    s = once(s, "        public static double Rtp(RouletteConfig c, RlKind k) => Cover(k) * (Pays(c, k) + 1) / (double)Pockets;\n",
             "        public static double Rtp(RouletteConfig c, RlKind k) => Cover(k) * (Pays(c, k) + 1) / (double)Pockets;\n"
             "\n"
             "        // ---------- tỉ lệ ra từng ô (RouletteConfig.weights; rỗng = đều nhau) ----------\n"
             "\n"
             "        static bool Weighted(RouletteConfig c) => c.weights != null && c.weights.Length == Pockets;\n"
             "\n"
             "        public static double Chance(RouletteConfig c, int pocket)\n"
             "        {\n"
             "            if (!Weighted(c)) return 1.0 / Pockets;\n"
             "            double total = 0;\n"
             "            foreach (int w in c.weights) total += Math.Max(0, w);\n"
             "            return total > 0 ? Math.Max(0, c.weights[pocket]) / total : 1.0 / Pockets;\n"
             "        }\n"
             "\n"
             "        // xác suất thắng và hoàn trả của MỘT cửa cụ thể theo tỉ lệ ra đang đặt\n"
             "        public static double Chance(RouletteConfig c, RlBet b)\n"
             "        {\n"
             "            double p = 0;\n"
             "            for (int i = 0; i < Pockets; i++)\n"
             "                if (Hits(b, i)) p += Chance(c, i);\n"
             "            return p;\n"
             "        }\n"
             "\n"
             "        public static double RtpOf(RouletteConfig c, RlBet b) => Chance(c, b) * (Pays(c, b.kind) + 1);\n"
             "\n"
             "        // hoàn trả thấp nhất / cao nhất trong mọi cửa (để ghi trong Cách chơi)\n"
             "        public static void RtpRange(RouletteConfig c, out double lo, out double hi)\n"
             "        {\n"
             "            double a = double.MaxValue, z = 0;\n"
             "            void See(RlKind k, int v)\n"
             "            {\n"
             "                double r = RtpOf(c, new RlBet { kind = k, v = v });\n"
             "                a = Math.Min(a, r);\n"
             "                z = Math.Max(z, r);\n"
             "            }\n"
             "            for (int e = 0; e < 5; e++) See(RlKind.Elem, e);\n"
             "            for (int n = 1; n <= 5; n++) See(RlKind.Num, n);\n"
             "            for (int p = 0; p < StarPocket; p++) See(RlKind.Single, p);\n"
             "            See(RlKind.Star, 0);\n"
             "            lo = a;\n"
             "            hi = z;\n"
             "        }\n"
             "\n"
             "        // chọn ô ra: đều nhau thì giữ đúng lối gọi rng cũ; có trọng số thì bốc theo trọng số\n"
             "        public static int Pick(RouletteConfig c, Rng rng)\n"
             "        {\n"
             "            if (!Weighted(c)) return rng.Int(0, Pockets - 1);\n"
             "            double total = 0;\n"
             "            foreach (int w in c.weights) total += Math.Max(0, w);\n"
             "            if (total <= 0) return rng.Int(0, Pockets - 1);\n"
             "            double x = rng.Next() * total;\n"
             "            for (int i = 0; i < Pockets; i++)\n"
             "            {\n"
             "                x -= Math.Max(0, c.weights[i]);\n"
             "                if (x < 0) return i;\n"
             "            }\n"
             "            return Pockets - 1;\n"
             "        }\n", mark="public static int Pick(RouletteConfig c, Rng rng)")
    s = once(s, "var r = new RlSpin { pocket = rng.Int(0, Pockets - 1), staked = bets.Sum(b => b.amount) };",
             "var r = new RlSpin { pocket = Pick(c, rng), staked = bets.Sum(b => b.amount) };")
    s = once(s, "// mảnh khách mời). Mọi cửa hoàn trả 25/26 ≈ 96,2%. Tối đa `chips` chip mỗi vòng, mỗi chip một mức cược của bậc đang chọn.\n",
             "// mảnh khách mời). Mọi cửa hoàn trả 25/26 ≈ 96,2%. Tối đa `chips` chip mỗi vòng, mỗi chip một mức cược của bậc đang chọn.\n"
             "// Ô ra do LÕI chọn (Pick: đều nhau, hoặc theo RouletteConfig.weights nếu đặt); viên bi trên màn chỉ diễn theo ô đã chọn\n"
             "// (RouletteBall.cs: tìm một cú thả bi mà mô phỏng vật lý cho bi nằm đúng ô đó), không quyết định kết quả.\n",
             mark="Ô ra do LÕI chọn")
    return s


@patch("Game/Casino/DealerRig.cs")
def _(s):
    s = once(s, "        Action onDone;\n        string doneClip;\n",
             "        Action onDone;\n        string doneClip;\n        bool scrubbing;      // đang kéo thời gian bằng tay (Scrub): Update không tự chạy clip\n        float scrubMix;\n",
             mark="bool scrubbing;")
    s = once(s, "            FinishPending();\n            onDone = done;\n            doneClip = clip;\n            State.Play(clip, false, mix);",
             "            FinishPending();\n            scrubbing = false;\n            onDone = done;\n            doneClip = clip;\n            State.Play(clip, false, mix);",
             mark="scrubbing = false;\n            onDone = done;")
    s = once(s, "            if (!Has(clip)) return;\n            FinishPending();\n            State.Play(clip, true, mix);",
             "            if (!Has(clip)) return;\n            FinishPending();\n            scrubbing = false;\n            State.Play(clip, true, mix);",
             mark="scrubbing = false;\n            State.Play(clip, true, mix);")
    s = once(s, "            if (!Ready()) return;\n            FinishPending();\n            if (State.CurrentName != Idle) State.Play(Idle, true, mix);\n        }\n",
             "            if (!Ready()) return;\n            FinishPending();\n            scrubbing = false;\n            if (State.CurrentName != Idle) State.Play(Idle, true, mix);\n        }\n"
             "\n"
             "        /// <summary>Kéo thời gian một clip LẶP theo tham số ngoài (Vòng Xoay: rl_watch theo góc viên bi): mỗi khung gọi một lần với\n"
             "        /// thời điểm trong clip (giây) và dt thật. Lần đầu hoà từ dáng đang có sang trong ~0,2 giây thật; sau đó dáng bám đúng\n"
             "        /// thời điểm đưa vào. Dừng bằng EndScrub hoặc Play / Loop / Stop.</summary>\n"
             "        public void Scrub(string clip, float time, float dt)\n"
             "        {\n"
             "            if (!Has(clip)) return;\n"
             "            int i = Asset.FindClip(clip);\n"
             "            float dur = Asset.anims[i].dur;\n"
             "            if (dur <= 0) return;\n"
             "            time = Mathf.Repeat(time, dur);\n"
             "            if (!scrubbing || State.CurrentName != clip)\n"
             "            {\n"
             "                FinishPending();\n"
             "                State.ClearQueue();\n"
             "                scrubbing = true;\n"
             "                scrubMix = 0.2f;\n"
             "            }\n"
             "            if (scrubMix > 0)\n"
             "            {\n"
             "                // chụp lại dáng đang hoà rồi hoà tiếp về dáng của thời điểm mới: phần hoà chạy theo giờ thật, không theo tốc độ kéo\n"
             "                scrubMix = Mathf.Max(0, scrubMix - Mathf.Max(0, dt));\n"
             "                State.Start(i, true, scrubMix + Mathf.Max(1e-4f, dt), time, false);\n"
             "                State.Advance(Mathf.Max(1e-4f, dt));\n"
             "                State.ClearQueue();\n"
             "            }\n"
             "            else State.Seek(time);\n"
             "        }\n"
             "\n"
             "        /// <summary>Thôi kéo thời gian: clip đang kéo chạy tiếp như clip lặp (thường gọi Play clip khác ngay sau).</summary>\n"
             "        public void EndScrub() => scrubbing = false;\n",
             mark="public void Scrub(string clip, float time, float dt)")
    s = once(s, "            if (Application.isPlaying) State.Advance(Time.deltaTime);",
             "            if (Application.isPlaying && !scrubbing) State.Advance(Time.deltaTime);")
    return s


@patch("Editor/ArtImporter.cs")
def _(s):
    return once(s, "                || assetPath.Contains(\"/Casino/HamDau/hd_\")",
                "                || assetPath.Contains(\"/Casino/Leu/rl_nen\") || assetPath.Contains(\"/Casino/Leu/rl_ban\") // lều Vòng Xoay có dealer (GD_Claude/31 D4): 1144 x 2048\n"
                "                || assetPath.Contains(\"/Casino/HamDau/hd_\")", mark="/Casino/Leu/rl_nen")


@patch("Editor/CasinoTablesMenu.cs")
def _(s):
    # Chỉ thay khối Roulette (BuildRouletteOnly, RlCell, BuildRoulette) bằng bản mới nhất. Phần chung (Common, CommonCompact, Make, Build)
    # đã vá xong từ 2026-11-26 và từ đó do phiên Đêm Bài / Máy Quả chỉnh tiếp: KHÔNG vá ở đây nữa để khỏi đè.
    a = s.index("        // ---------- Roulette")
    b = s.index("        // ---------- Máy quả ----------")
    return s[:a] + open(os.path.join(HERE, "BuildRoulette.cs.txt"), encoding="utf-8").read() + s[b:]


@patch("Tests/CasinoTests.cs")
def _(s):
    return once(s, "        [Test]\n        public void Roulette_SaoVang_ThemManhKhachMoi()",
                open(os.path.join(HERE, "Tests_Roulette.cs.txt"), encoding="utf-8").read() +
                "        [Test]\n        public void Roulette_SaoVang_ThemManhKhachMoi()", mark="Roulette_TiLeRa_TheoTrongSo")


@patch("App/Scenes/Casino/CasinoTableScene.cs")
def _(s):
    # bảng thông tin gập (người dùng 2026-11-26: "mấy cái này để trong 1 cái toggle bên trái dưới thôi, không dàn ra như này")
    s = once(s, "        [SerializeField] protected SketchButton help;\n",
             "        [SerializeField] protected SketchButton help;\n"
             "        // bản gọn (Vòng Xoay): bậc cược, tờ tin, Hũ bàn, Cách chơi nằm trong MỘT bảng gập; nút gập ở góc trái dưới ghi mức cược đang chọn\n"
             "        [SerializeField] protected SketchButton infoToggle;\n"
             "        [SerializeField] protected RectTransform infoPanel;\n", mark="protected SketchButton infoToggle;")
    s = once(s, "        public override void Enter(object args)\n",
             "        // Dùng khi dựng prefab (Editor): nút gập + bảng chứa phần chung.\n"
             "        public void SetupInfo(SketchButton toggle, RectTransform panel)\n"
             "        {\n"
             "            infoToggle = toggle; infoPanel = panel;\n"
             "        }\n"
             "\n"
             "        protected bool InfoOpen => infoPanel && infoPanel.gameObject.activeSelf;\n"
             "\n"
             "        protected void SetInfo(bool open)\n"
             "        {\n"
             "            if (!infoPanel) return;\n"
             "            infoPanel.gameObject.SetActive(open);\n"
             "            if (infoToggle) infoToggle.SetRole(open ? BtnColor.Yellow : BtnColor.Paper);\n"
             "        }\n"
             "\n"
             "        public override void Enter(object args)\n", mark="public void SetupInfo(SketchButton toggle, RectTransform panel)")
    s = once(s, "            help.SetOnClick(ShowHelp);\n",
             "            help.SetOnClick(ShowHelp);\n"
             "            if (infoToggle)\n"
             "            {\n"
             "                infoToggle.SetOnClick(() =>\n"
             "                {\n"
             "                    if (Busy) return;\n"
             "                    SetInfo(!InfoOpen);\n"
             "                });\n"
             "                SetInfo(false);\n"
             "            }\n", mark="SetInfo(!InfoOpen);")
    s = once(s, "            RenderTable();\n            OnTierChanged();\n",
             "            RenderTable();\n            OnTierChanged();\n            SetInfo(false);   // chọn xong mức cược thì gập bảng\n",
             mark="chọn xong mức cược thì gập bảng")
    s = once(s, "            var st = Casino.Roll(s, d, now);\n",
             "            var st = Casino.Roll(s, d, now);\n"
             "            if (infoToggle) infoToggle.SetText(Loc.F(\"Cược {0} bi\", NumFmt.Short(BetNow)));\n",
             mark="infoToggle.SetText(Loc.F(")
    return s


def main():
    if mode == "clean":
        for _, rel in NEW:
            p = os.path.join(OVER, rel)
            if os.path.isfile(p):
                os.remove(p)
        for rel in PATCH:
            p = os.path.join(OVER, rel)
            if os.path.isfile(p):
                os.remove(p)
        print("đã xoá file D4 trong overlay")
        return
    dst_root = SCRIPT if mode == "apply" else OVER
    for src, rel in NEW:
        dst = os.path.join(dst_root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        print("chép", rel)
    for rel, fn in PATCH.items():
        src = os.path.join(SCRIPT, rel)
        s = open(src, encoding="utf-8").read()
        bom = s.startswith("﻿")
        nl = "\r\n" if "\r\n" in s else "\n"
        t = fn(s.replace("\r\n", "\n"))
        if nl == "\r\n":
            t = t.replace("\n", "\r\n")
        dst = os.path.join(dst_root, rel)
        if mode == "apply" and t == s:
            print("đã vá sẵn", rel)
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w", encoding="utf-8", newline="").write(t)
        print("vá", rel)


main()
