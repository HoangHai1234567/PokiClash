// Mặt máy bi trên uGUI (toạ độ máy: x sang phải, y xuống, khung 460 × 680, hiện ở cỡ K lần). Prefab: phần "May" của Screens/Machine.
// Bàn chép bàn table_01 của máy bi tham khảo (Core/Pachinko.cs): khung vòm, làn phóng mép phải, 22 đinh, nấm đỉnh, hai nấm lớn có
// vòng tiến độ, mái hai cánh, cốc dưới mái, đáy V, 5 ô. Phần tĩnh là ảnh Baked/Machine/may_tinh.png (ghép bằng
// ArtGen/Pachinko/ghep_ban.py theo hình học xuất từ Board, refs/mat_may.json) + nhãn ô, rương dựng lại lúc Bind theo board.slots,
// board.cups. Lớp động (canvas con "Dong"): bi, loé đinh, chữ nổi, loé rương sinh từ prefab mục (Items/BiLan, LoeDinh, ChuNoi,
// LoeRuong); vệt bi là Items/VetBiDai (TrailGraphic); hạt hiệu ứng (MachineFx) là bản sao Items/HatMayBi, bản hết hạn tắt đi để
// dùng lại. Nấm đỉnh, hai nấm lớn cùng vòng tiến độ và hình quà giữa nấm là bản sao Items/HatMayBi tạo lúc Bind (gắn lại thì dọn).
// Bi chờ ở chân làn là "bi_cho" (con của "may_tha"; ảnh máng mây cũ "dam_may" tắt).
// Hiệu ứng chép máy bi tham khảo (GD_Claude/07_MayBi.md): vệt bi 0,3 giây, đinh loé 0,067 giây, nấm phồng xẹp 0,23 giây,
// ô sáng kèm quầng và sao, rương có bảng loé theo cấp, rương vàng có bộ jackpot; hạt chạy theo giờ của máy (chậm khi máy chậm).
// Trạng thái sáng vẽ tay (gói ArtGen/Pachinko/gui_gpt/bo_moi lượt 2): đinh, núm đáy V chạm thì hiện pk_dinh_sang đè đúng chỗ; nấm
// lớn đổi sang pk_bumper_sang, nấm đỉnh sang pk_u_loi_sang lúc phồng; cốc dưới mái sáng (pk_coc_sang) khi bi lọt; ô đáy sáng bằng
// lớp tia (pk_o_sang, ô rương pk_o_sang_ruong) tô màu theo ô.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class MachineBoard : MonoBehaviour
    {
        public const float K = 1.72f; // cỡ máy trên khung 1080 (web 0,86 ở khung 540)

        public static readonly Color XpColor = Theme.Hex("#c18cf0");
        public static readonly Color BallPink = Theme.Hex("#ff8fb3");
        public static readonly Color ChestTagColor = Theme.Hex("#9a6a1e");

        [Serializable]
        public struct Parts
        {
            public HoldArea hold; // vùng chạm cả máy
            public RectTransform dyn, trailLayer, ballLayer, fxLayer, cloud;
            public Image cloudBall;
            public Image[] glow; // sáng ô, theo thứ tự ô đáy của bàn mặc định
            [Header("Prefab mục")]
            public Image ball, pegFlash, burst;
            public Image particle; // Items/HatMayBi: hạt hiệu ứng, nấm (menu "PokiClash/Prefab/Máy bi: hạt hiệu ứng")
            public TrailGraphic trail; // Items/VetBiDai: vệt đuôi một bi (cùng menu)
            public TextMeshProUGUI floatText;
        }

        [SerializeField] Parts p;

        public Board Board { get; private set; }
        public RectTransform Root => (RectTransform)transform;
        public HoldArea Hold => p.hold;

        Image[] glow; // sáng ô theo thứ tự ô đáy của bàn đang gắn (dựng lại từ prefab lúc Bind)
        float[] glowT, glowMax;
        Color[] glowTint; // màu lớp tia sáng theo loại ô (có ảnh pk_o_sang); trắng = cách tô cũ
        bool rayGlow;
        Sprite bumperNormal, bumperLit, topNormal, topLit;
        // vòng tiến độ của hai nấm lớn (rãnh, phần đầy tô vàng quay theo chiều kim đồng hồ từ đỉnh), hình quà giữa nấm
        readonly Image[] ringTrack = new Image[2], ringFill = new Image[2];
        readonly float[] ringShown = new float[2], ringWant = new float[2], ringHold = new float[2];
        readonly List<GameObject> made = new List<GameObject>(); // đồ động tạo lúc Bind (nấm, vòng, hình quà), gắn lại thì dọn
        public static readonly Color RingColor = Theme.Hex("#f7c948");
        // hình sáng đè lên phần tĩnh (cốc, két): ảnh, tuổi, đời
        readonly List<(Image img, float age, float life)> lits = new List<(Image, float, float)>();
        Image[] flash;
        float[] flashT;
        bool[] flashLit; // loé đinh là hình sáng vẽ tay (giữ màu) thay vì loé tròn tô vàng
        Image[] bumpers; // nấm động theo chỉ số đinh (null nếu không phải nấm)
        float[] bumpT;
        readonly List<Image> balls = new List<Image>();
        readonly List<(TextMeshProUGUI t, float age, Vector2 at)> floats = new List<(TextMeshProUGUI, float, Vector2)>();
        readonly List<(Image img, float age, float size)> bursts = new List<(Image, float, float)>();
        Vector2 shakeBase;
        float shakeT, shakeDur, shakeAmp;
        float launchT = -1; // thời gian từ lúc phóng (bi chờ co giãn), âm = không chạy
        MachineFx fx;
        public MachineFx Fx => fx;

        // nhãn số ô đáy theo mức cược (như số trên ô của máy tham khảo đổi theo cược): EXP × cược, "+cược" bi;
        // rương ở ô, cốc, két có nhãn "×cược" khi cược trên 1. Đổi cược thì các số nhún 1,4 → 1 trong 0,25 giây
        readonly List<(TextMeshProUGUI t, int exp, float w)> slotNums = new List<(TextMeshProUGUI, int, float)>();
        readonly List<TextMeshProUGUI> chestTags = new List<TextMeshProUGUI>();
        int mult = 1;
        float multT = -1;
        public const float MultPop = 0.25f;

        // đinh sáng: phồng 1,15 → 1 trong 0,067 giây (như máy tham khảo, rồi tắt), ở đây mờ thêm 0,1 giây cho kịp thấy
        public const float FlashPop = 0.067f, FlashTime = FlashPop + 0.1f;
        // nấm bị chạm: cỡ theo các mốc (giây, hệ số) trong 0,233 giây
        static readonly float[] BumpCurve = { 0, 0.905f, 0.033f, 1.184f, 0.1f, 0.894f, 0.167f, 1.053f, 0.233f, 1 };
        // bi chờ lúc phóng: chiều cao co giãn như cần phóng của máy tham khảo (0,63 → 1,57 → 0,89 → 1,2 → 1), giảm nửa biên độ
        static readonly float[] LaunchCurve = { 0, 0.63f, 0.067f, 1.57f, 0.133f, 0.89f, 0.2f, 1.2f, 0.233f, 1 };

        // vệt bi như vệt của máy tham khảo: dài 0,3 giây, rộng 0,18 u (hơn bi một chút), đậm dần về 0 theo tuổi; lấy mẫu mỗi 0,03
        // giây. Máy đó alpha đầu 0,52 trên nền bàn sẫm; nền giấy sáng ở đây cần 0,6 mới rõ
        public const float TrailTime = 0.3f, TrailStep = 0.03f, TrailWidth = 0.18f, TrailAlpha = 0.6f;

        sealed class Trail
        {
            public readonly List<(Vector2 at, float t)> pts = new List<(Vector2, float)>(); // cũ trước, mới sau
            public TrailGraphic g;
            public Vector2 head;
            public Color color;
            public bool alive, seen;
        }

        readonly Dictionary<int, Trail> trails = new Dictionary<int, Trail>();
        readonly List<int> trailGone = new List<int>();
        readonly List<Vector2> trailPts = new List<Vector2>();
        readonly List<float> trailAlpha = new List<float>();
        readonly Stack<TrailGraphic> freeTrails = new Stack<TrailGraphic>();
        float simTime;
        readonly Stack<TextMeshProUGUI> freeFloats = new Stack<TextMeshProUGUI>();
        readonly Stack<Image> freeBursts = new Stack<Image>();

        public static Color ChestColor(SlotKind k) =>
            k == SlotKind.ChestGold ? Theme.Hex("#f7c948") : k == SlotKind.ChestSilver ? Theme.Hex("#c9d3dc") : Theme.Hex("#c98a4a");

        public static Color BallColor(int mult) => mult >= 5 ? Theme.Hex("#ffd24a") : mult > 1 ? Theme.Hex("#8ec5ff") : BallPink;

        // hình rương (thân tô màu + khoá tròn), rộng w
        public static RectTransform ChestIcon(Transform parent, SlotKind kind, float w, Color? fill = null) =>
            Ui.Spawn(Theme.Prefabs.chest, parent).Bind(kind, w, fill).Rect;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        // Gắn bàn vật lý lúc vào màn. Ảnh tĩnh dựng theo bàn mặc định (vị trí đinh, ô không đổi theo hạt giống); sáng ô và
        // nhãn số ô dựng lại theo board.slots, nên prefab nướng cho số ô cũ vẫn dùng được khi mặt máy đổi.
        public void Bind(Board board)
        {
            Board = board;
            LayoutSlots();
            flash = new Image[board.pegs.Count];
            flashT = new float[flash.Length];
            flashLit = new bool[flash.Length];
            shakeBase = Root.anchoredPosition;
            foreach (var (img, _, _) in lits)
                if (img) img.gameObject.SetActive(false);
            lits.Clear();
            fx = new MachineFx(p.particle, p.fxLayer);
            foreach (var go in made)
                if (go) Destroy(go);
            made.Clear();
            LayoutBumpers();
            LayoutGlowRays();
            // chữ gợi ý "chạm hoặc giữ để thả bi" (nướng ở mép trên khung cũ): dời xuống trong vòm, ngay dưới nấm đỉnh
            foreach (var t in GetComponentsInChildren<TextMeshProUGUI>(true))
                if (t.text.Contains("để thả bi"))
                {
                    var rt = t.rectTransform;
                    rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
                    rt.pivot = new Vector2(0.5f, 0.5f);
                    rt.anchoredPosition = Local(Board.X(0), Board.Y(4.27));
                }
            // máng mây của bàn cũ thôi dùng: chỉ giữ bi chờ, đặt ở chân làn phóng
            if (p.cloud)
            {
                foreach (var img in p.cloud.GetComponentsInChildren<Image>(true))
                    if (img.name == "dam_may") img.gameObject.SetActive(false);
                var (lx, ly) = board.lane[0];
                p.cloud.anchoredPosition = Local(lx, ly);
                p.cloud.localScale = Vector3.one;
                if (p.cloudBall)
                {
                    var rt = p.cloudBall.rectTransform;
                    // tâm bi chờ đúng gốc (pivot) của "may_tha", tức chân làn
                    rt.anchorMin = rt.anchorMax = p.cloud.pivot;
                    rt.pivot = new Vector2(0.5f, 0.5f);
                    rt.anchoredPosition = Vector2.zero;
                    rt.sizeDelta = Vector2.one * (float)Board.BallR * 2 * K;
                }
            }
        }

        // ảnh động riêng của bàn (không lấy từ kho hạt hiệu ứng: kho đó tắt và dùng lại ảnh)
        Image Make(string name, Transform parent)
        {
            var img = Ui.Spawn(p.particle, parent);
            img.name = name;
            img.color = Color.white;
            img.enabled = true;
            img.raycastTarget = false;
            var rt = img.rectTransform;
            rt.localScale = Vector3.one;
            rt.localEulerAngles = Vector3.zero;
            made.Add(img.gameObject);
            return img;
        }

        // lớp tia sáng ô (ảnh vẽ tay): ô rương có sao; tô theo loại ô (EXP tím, bi hồng, rương theo màu rương)
        void LayoutGlowRays()
        {
            var ray = fx.Sprite("pk_o_sang");
            var rayChest = fx.Sprite("pk_o_sang_ruong");
            rayGlow = ray;
            glowTint = new Color[glow.Length];
            for (int i = 0; i < glow.Length; i++)
            {
                glowTint[i] = Color.white;
                if (!rayGlow || i >= Board.slots.Count) continue;
                var kind = Board.slots[i].reward;
                bool chest = Pachinko.IsChest(kind);
                Theme.SetSprite(glow[i], chest && rayChest ? rayChest : ray);
                glow[i].type = Image.Type.Simple;
                glow[i].preserveAspect = false;
                glowTint[i] = chest ? ChestColor(kind) : kind == SlotKind.Ball ? BallPink : XpColor;
            }
        }

        // hình sáng đè đúng chỗ phần tĩnh (dưới lớp vệt, bi): nhún 1,12 → 1 rồi giữ, mờ dần ở 40 % đời cuối
        void Lit(string sprite, Vector2 at, Vector2 size, float life)
        {
            var s = fx.Sprite(sprite);
            if (!s || !p.particle) return;
            var img = fx.Take(p.dyn);
            img.name = "sang";
            Theme.SetSprite(img, s);
            img.color = Color.white;
            img.enabled = true;
            img.preserveAspect = true;
            var rt = img.rectTransform;
            rt.anchoredPosition = at;
            rt.sizeDelta = size;
            rt.localEulerAngles = Vector3.zero;
            rt.localScale = Vector3.one * 1.12f;
            rt.SetSiblingIndex(p.trailLayer.GetSiblingIndex());
            lits.Add((img, 0, life));
        }

        // nấm lớn, nấm đỉnh là ảnh động (ảnh tĩnh không vẽ) nằm dưới lớp vệt, để phồng xẹp được khi bị chạm. Mỗi nấm lớn có vòng
        // tiến độ đè lên vành nấm (rãnh kem, phần đầy vàng) và hình quà giữa nấm (đặt bằng RingReward); vòng, hình quà là con của
        // nấm nên phồng theo nấm.
        void LayoutBumpers()
        {
            var pegs = Board.pegs;
            bumpers = new Image[pegs.Count];
            bumpT = new float[pegs.Count];
            if (!p.particle) return;
            bumperNormal = fx.Sprite("pk_bumper");
            bumperLit = fx.Sprite("pk_bumper_sang");
            topNormal = fx.Sprite("pk_nam_dinh") ?? bumperNormal;
            topLit = fx.Sprite("pk_u_loi_sang") ?? bumperLit;
            var ring = fx.Sprite("pk_vong_nam") ?? fx.Sprite("pk_fx_vong_day");
            for (int i = 0; i < pegs.Count; i++)
            {
                var pg = pegs[i];
                if (pg.kind != PegKind.Bumper && pg.kind != PegKind.Top) continue;
                bool top = pg.kind == PegKind.Top;
                var img = Make((top ? "nam_dinh" : "nam") + i, p.dyn);
                img.sprite = top ? topNormal : bumperNormal;
                var rt = img.rectTransform;
                rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
                rt.pivot = new Vector2(0.5f, 0.5f);
                rt.anchoredPosition = Local(pg.x, pg.y);
                // ảnh nấm chừa 2 đơn vị quanh viền (nấm đỉnh: ảnh núm, chừa 1)
                rt.sizeDelta = Vector2.one * (float)(pg.r + (top ? 1 : 2)) * 2 * K;
                rt.SetSiblingIndex(p.trailLayer.GetSiblingIndex());
                bumpers[i] = img;
                bumpT[i] = -1;
                int r = System.Array.IndexOf(Board.ringPeg, i);
                if (r < 0 || !ring) continue;
                ringTrack[r] = RingImage("vong_ranh", img.rectTransform, ring, new Color(1, 0.97f, 0.88f, 0.92f));
                ringFill[r] = RingImage("vong_day", img.rectTransform, ring, RingColor);
                ringFill[r].type = Image.Type.Filled;
                ringFill[r].fillMethod = Image.FillMethod.Radial360;
                ringFill[r].fillOrigin = (int)Image.Origin360.Top;
                ringFill[r].fillClockwise = true;
                ringFill[r].fillAmount = ringShown[r] = ringWant[r];
            }
        }

        Image RingImage(string name, RectTransform parent, Sprite s, Color c)
        {
            var img = Make(name, parent);
            img.sprite = s;
            img.color = c;
            var rt = img.rectTransform;
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            return img;
        }

        // hình quà giữa nấm lớn thứ i theo cfg.rings[i]: rương nhỏ, hoặc icon bi/XP kèm "+v"
        public void RingReward(int i, GiftStep g)
        {
            if (i < 0 || i >= Board.ringPeg.Length || g == null) return;
            int peg = Board.ringPeg[i];
            var host = peg >= 0 && peg < bumpers.Length && bumpers[peg] ? bumpers[peg].rectTransform : null;
            if (!host) return;
            for (int c = host.childCount - 1; c >= 0; c--)
                if (host.GetChild(c).name == "qua") Destroy(host.GetChild(c).gameObject);
            float d = (float)Board.pegs[peg].r * 2 * K;
            // đĩa kem lót sau hình quà cho dễ đọc trên nền nấm
            var plate = Make("qua", host);
            plate.sprite = fx.Sprite("pk_dia_nam");
            plate.enabled = plate.sprite;
            plate.rectTransform.anchorMin = plate.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            plate.rectTransform.anchoredPosition = Vector2.zero;
            plate.rectTransform.sizeDelta = Vector2.one * d * 0.66f;
            if (g.k.StartsWith("chest"))
            {
                var ic = ChestIcon(host, Pachinko.FromKey(g.k), d * 0.44f);
                ic.name = "qua";
                ic.anchorMin = ic.anchorMax = new Vector2(0.5f, 0.5f);
                ic.anchoredPosition = new Vector2(0, d * 0.02f);
                made.Add(ic.gameObject);
                return;
            }
            // khung chứa icon và số: bản sao hạt (prefab) để trong suốt
            var box = Make("qua", host);
            box.sprite = null;
            box.color = new Color(1, 1, 1, 0);
            var holder = box.rectTransform;
            holder.anchorMin = holder.anchorMax = new Vector2(0.5f, 0.5f);
            holder.anchoredPosition = Vector2.zero;
            holder.sizeDelta = Vector2.one * d * 0.6f;
            var icon = Make("icon", holder);
            icon.sprite = App.Art ? App.Art.Icon(g.k == "balls" ? "ball" : "exp") : null;
            icon.preserveAspect = true;
            icon.rectTransform.anchorMin = icon.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
            icon.rectTransform.anchoredPosition = new Vector2(0, d * 0.07f);
            icon.rectTransform.sizeDelta = Vector2.one * d * 0.3f;
            if (!p.floatText) return;
            var t = Ui.Spawn(p.floatText, holder);
            t.name = "so";
            t.text = "+" + g.v;
            t.fontSize = 15 * K;
            t.fontStyle = FontStyles.Bold;
            t.color = Theme.Ink;
            t.raycastTarget = false;
            var tr = t.rectTransform;
            tr.anchorMin = tr.anchorMax = new Vector2(0.5f, 0.5f);
            tr.anchoredPosition = new Vector2(0, -d * 0.15f);
            tr.sizeDelta = new Vector2(d * 0.6f, 16 * K);
        }

        // phần đầy của vòng nấm i (0..1); pop: vừa đầy thì vòng chạy tới đầy rồi về số dư
        public void SetRing(int i, float fill, bool instant = false)
        {
            if (i < 0 || i >= ringWant.Length) return;
            ringWant[i] = Mathf.Clamp01(fill);
            if (instant) ringShown[i] = ringWant[i];
            if (ringFill[i]) ringFill[i].fillAmount = ringShown[i];
        }

        // vòng nấm i vừa đầy: nấm phồng to, loé vòng, vòng chạy hết rồi về số dư
        public void RingFull(int i)
        {
            if (i < 0 || i >= Board.ringPeg.Length) return;
            int peg = Board.ringPeg[i];
            var pg = Board.pegs[peg];
            ringShown[i] = 1;
            ringHold[i] = 0.4f;
            if (ringFill[i]) ringFill[i].fillAmount = 1;
            bumpT[peg] = 0;
            fx.Emit(MachineFx.RingHit, Local(pg.x, pg.y), MachineFx.UnitBall * 2.2f);
            Burst(pg.x, pg.y, RingColor, 1.3f);
        }

        // hàng số và hàng chữ phụ trong ô đáy (toạ độ máy)
        static double NumY(Slot s) => s.y0 + (Board.BH - s.y0) * 0.36;
        static double SubY(Slot s) => s.y0 + (Board.BH - s.y0) * 0.6;
        // rương nhỏ trong cốc dưới mái: trên miệng cốc vẽ trong ảnh tĩnh (ghep_ban.py đặt cốc ở 60 % chiều cao cảm biến)
        static Vector2 CupChestAt(Cup c) => Local(c.x, c.y - c.h / 2 + c.h * 0.42);
        // nhãn trong prefab nướng cho bàn cũ: số ô ở y 650, chữ phụ ở y 664 (đơn vị máy); lần gắn đầu đổi tên để lần sau tìm theo tên
        const float OldNumY = 650, OldSubY = 664;

        // sáng ô: một ảnh mỗi ô (thêm bản sao của ảnh đầu nếu thiếu, ảnh thừa tắt), phủ cảm biến ô. Nhãn số ô (con của "nhan"): ô EXP
        // và ô bi có số và chữ phụ ("XP", "bi"), ô rương không có chữ (rương nhỏ đặt giữa ô).
        void LayoutSlots()
        {
            var slots = Board.slots;
            var list = new List<Image>(p.glow);
            while (list.Count < slots.Count)
            {
                var g = Instantiate(p.glow[0], p.glow[0].transform.parent);
                g.name = "sang_o" + list.Count;
                list.Add(g);
            }
            for (int i = 0; i < list.Count; i++)
            {
                list[i].gameObject.SetActive(false);
                if (i >= slots.Count) continue;
                var rt = list[i].rectTransform;
                var sl = slots[i];
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0, 1);
                rt.anchoredPosition = new Vector2((float)sl.x0 * K, -(float)sl.y0 * K);
                rt.sizeDelta = new Vector2((float)(sl.x1 - sl.x0) * K, (float)(Math.Min(sl.y1, Board.BH - 2) - sl.y0) * K);
            }
            glow = list.ToArray();
            glowT = new float[glow.Length];
            glowMax = new float[glow.Length];

            var labels = transform.Find("nhan");
            if (!labels) return;
            LayoutChestIcons(labels);
            var nums = new List<TextMeshProUGUI>();
            var subs = new List<TextMeshProUGUI>();
            foreach (Transform c in labels)
            {
                var t = c.GetComponent<TextMeshProUGUI>();
                if (!t || c.name == "cuoc_ruong") continue;
                float y = -((RectTransform)c).anchoredPosition.y / K;
                if (c.name == "so_o" || c.name != "phu_o" && Mathf.Abs(y - OldNumY) < 3) nums.Add(t);
                else if (c.name == "phu_o" || Mathf.Abs(y - OldSubY) < 3) subs.Add(t);
            }
            if (nums.Count == 0 || subs.Count == 0) return;
            int n = 0;
            slotNums.Clear();
            foreach (var sl in slots)
            {
                int exp = Pachinko.Exp(sl.reward);
                if (exp == 0 && sl.reward != SlotKind.Ball) continue;
                while (nums.Count <= n) nums.Add(Instantiate(nums[0], labels));
                while (subs.Count <= n) subs.Add(Instantiate(subs[0], labels));
                float cx = (float)(sl.x0 + sl.x1) / 2 * K, w = (float)(sl.x1 - sl.x0);
                var num = nums[n];
                num.name = "so_o";
                num.color = exp > 0 ? XpColor : BallPink;
                slotNums.Add((num, exp, w));
                num.rectTransform.anchoredPosition = new Vector2(cx, -(float)NumY(sl) * K);
                num.rectTransform.sizeDelta = new Vector2(w * K, num.rectTransform.sizeDelta.y);
                var sub = subs[n];
                sub.name = "phu_o";
                sub.text = exp > 0 ? "XP" : "bi";
                sub.rectTransform.anchoredPosition = new Vector2(cx, -(float)SubY(sl) * K);
                sub.rectTransform.sizeDelta = new Vector2(w * K, sub.rectTransform.sizeDelta.y);
                num.gameObject.SetActive(true);
                sub.gameObject.SetActive(true);
                n++;
            }
            for (int i = n; i < nums.Count; i++) nums[i].gameObject.SetActive(false);
            for (int i = n; i < subs.Count; i++) subs[i].gameObject.SetActive(false);
            subFont = subs[0].fontSize;

            // nhãn "×cược" dưới mỗi rương: bản sao chữ phụ, đặt theo rương nhỏ đã dựng (LayoutChestIcons), cùng thứ tự
            // (nhãn đã sinh ở lần Bind trước thì dùng lại)
            var oldTags = new List<TextMeshProUGUI>();
            foreach (Transform c in labels)
                if (c.name == "cuoc_ruong" && c.TryGetComponent<TextMeshProUGUI>(out var t)) oldTags.Add(t);
            chestTags.Clear();
            for (int i = 0; i < chestSpots.Count; i++)
            {
                var (ic, inSlot, sl) = chestSpots[i];
                var tag = chestTags.Count < oldTags.Count ? oldTags[chestTags.Count] : Instantiate(subs[0], labels);
                tag.name = "cuoc_ruong";
                // rương ở ô đáy: nhãn ở hàng chữ phụ của ô; rương trong cốc: nhãn bên phải rương
                var at = ic.Rect.anchoredPosition;
                var size = ic.Rect.sizeDelta;
                float tw = 30 * K;
                tag.rectTransform.anchoredPosition = inSlot ? new Vector2(at.x, -(float)SubY(sl) * K - 6 * K)
                    : new Vector2(at.x + size.x / 2 + tw / 2 + 1 * K, at.y);
                tag.rectTransform.sizeDelta = new Vector2(tw, tag.rectTransform.sizeDelta.y);
                tag.fontSize = subFont * 1.35f;
                tag.color = ChestTagColor;
                tag.fontStyle = FontStyles.Bold;
                tag.gameObject.SetActive(true);
                chestTags.Add(tag);
            }
            for (int i = chestTags.Count; i < oldTags.Count; i++) oldTags[i].gameObject.SetActive(false);
            ApplyMult();
        }

        float subFont = 14 * K;
        readonly List<(ChestIcon ic, bool inSlot, Slot sl)> chestSpots = new List<(ChestIcon, bool, Slot)>();

        // số trên máy theo mức cược x (gọi khi vào màn và khi đổi cược); pop: các số nhún lên một cái khi đổi
        public void SetMult(int x, bool pop = true)
        {
            x = Mathf.Max(1, x);
            if (x == mult) return;
            mult = x;
            ApplyMult();
            if (pop) multT = 0;
        }

        void ApplyMult()
        {
            foreach (var (t, exp, w) in slotNums)
            {
                if (!t) continue;
                string s = exp > 0 ? (exp * mult).ToString() : "+" + mult;
                t.text = s;
                // ô ở bàn này rộng (khoảng 80 đơn vị máy): số to; 3 chữ số trở lên co lại cho vừa ô
                float size = 22 * K;
                if (s.Length >= 3) size *= s.Length >= 4 ? 0.7f : 0.85f;
                t.fontSize = size;
            }
            foreach (var tag in chestTags)
            {
                if (!tag) continue;
                tag.text = "×" + mult;
                tag.gameObject.SetActive(mult > 1);
            }
        }

        // rương nhỏ (prefab kit Ruong, con của "nhan"): một cái giữa mỗi ô rương ở đáy, một cái trên mỗi cốc. Prefab có sẵn vài
        // cái theo bàn cũ: dùng lại, thiếu thì nhân bản, thừa thì tắt.
        void LayoutChestIcons(Transform labels)
        {
            chestSpots.Clear();
            var icons = new List<ChestIcon>(labels.GetComponentsInChildren<ChestIcon>(true));
            if (icons.Count == 0) return;
            var want = new List<(SlotKind kind, Vector2 at, float w, bool inSlot, Slot sl)>();
            foreach (var sl in Board.slots)
                if (Pachinko.IsChest(sl.reward))
                    want.Add((sl.reward, Local((sl.x0 + sl.x1) / 2, NumY(sl) + 2), (float)(sl.x1 - sl.x0) * 0.5f * K, true, sl));
            foreach (var c in Board.cups)
                want.Add((c.reward, CupChestAt(c), (float)c.w * 0.5f * K, false, default));
            for (int i = 0; i < want.Count; i++)
            {
                if (i >= icons.Count) icons.Add(Instantiate(icons[0], labels));
                var (kind, at, w, inSlot, sl) = want[i];
                icons[i].Bind(kind, w);
                icons[i].Rect.anchoredPosition = at;
                icons[i].gameObject.SetActive(true);
                chestSpots.Add((icons[i], inSlot, sl));
            }
            for (int i = want.Count; i < icons.Count; i++) icons[i].gameObject.SetActive(false);
        }

        public static Vector2 Local(double x, double y) => new Vector2((float)x * K, -(float)y * K);
        public Vector3 World(double x, double y) => Root.TransformPoint(Local(x, y));

        // ---------- lớp động ----------

        // bi chạm đinh: đinh sáng phồng, quầng sau đinh co lại, hai lấp lánh; chạm nấm: nấm phồng xẹp và bộ quầng, vòng của nấm
        public void Flash(int peg)
        {
            if (peg < 0 || peg >= flash.Length) return;
            var pg = Board.pegs[peg];
            if (bumpers[peg])
            {
                bumpT[peg] = 0;
                var lit = pg.kind == PegKind.Top ? topLit : bumperLit;
                if (lit) bumpers[peg].sprite = lit;
                fx.Emit(MachineFx.BumperHit, Local(pg.x, pg.y), (float)pg.r * 2 * K / 1.1f);
                return;
            }
            fx.Emit(MachineFx.PegHit, Local(pg.x, pg.y), (float)pg.r * 2 * K);
            fx.Emit(MachineFx.PegSpark, Local(pg.x, pg.y), MachineFx.UnitBall);
            if (!flash[peg])
            {
                var img = Ui.Spawn(p.pegFlash, p.dyn);
                img.name = "loe" + peg;
                // hình sáng vẽ tay đè khít đinh vẽ trong ảnh tĩnh (đinh 2r + 2; núm đáy V vẽ bằng núm cam 2r + 1,5, sáng bằng
                // pk_u_loi_sang); chưa có ảnh thì loé tròn tô vàng như cũ
                bool knob = pg.kind == PegKind.Post;
                var lit = fx.Sprite(knob ? "pk_u_loi_sang" : "pk_dinh_sang");
                float d = (float)(pg.r + 2) * 2;
                if (lit)
                {
                    Theme.SetSprite(img, lit);
                    img.preserveAspect = true;
                    flashLit[peg] = true;
                    d = (float)(pg.r * 2 + (knob ? 1.5 : 2));
                }
                img.rectTransform.Place(new Vector2(0, 1), Local(pg.x, pg.y), Vector2.one * d * K, new Vector2(0.5f, 0.5f));
                img.rectTransform.SetSiblingIndex(p.trailLayer.GetSiblingIndex());
                flash[peg] = img;
            }
            flashT[peg] = FlashTime;
            flash[peg].gameObject.SetActive(true);
        }

        // tier 0: ô thường (0,5 giây), 1: rương gỗ, bạc (1,1 giây), 2: rương vàng (1,6 giây, sáng đậm hơn)
        public void Glow(int slot, int tier)
        {
            if (slot < 0 || slot >= Board.slots.Count || slot >= glow.Length) return;
            glowT[slot] = glowMax[slot] = tier >= 2 ? 1.6f : tier == 1 ? 1.1f : 0.5f;
            glow[slot].gameObject.SetActive(true);
        }

        // rung cả mặt máy (rương vàng): lệch ngẫu nhiên amp px, nhỏ dần trong dur giây
        public void Shake(float amp, float dur)
        {
            if (shakeT <= 0) shakeBase = Root.anchoredPosition;
            shakeAmp = amp;
            shakeT = shakeDur = dur;
        }

        public void Float(double x, double y, string text, Color color, float size = 22)
        {
            TextMeshProUGUI t;
            if (freeFloats.Count > 0)
            {
                t = freeFloats.Pop();
                t.gameObject.SetActive(true);
                t.rectTransform.SetAsLastSibling();
            }
            else
            {
                t = Ui.Spawn(p.floatText, p.fxLayer);
                t.name = "chu";
            }
            t.text = text;
            t.fontSize = size * K;
            t.color = color;
            var at = Local(x, y);
            t.rectTransform.anchoredPosition = at;
            floats.Add((t, 0, at));
        }

        // vòng loé răng cưa ở chỗ rương rơi vào (ô hiếm nổi bật hẳn); size: cỡ so với vòng thường (rương vàng to hơn)
        public void Burst(double x, double y, Color color, float size = 1)
        {
            Image img;
            if (freeBursts.Count > 0)
            {
                img = freeBursts.Pop();
                img.gameObject.SetActive(true);
            }
            else
            {
                img = Ui.Spawn(p.burst, p.fxLayer);
                img.name = "loe_ruong";
            }
            img.color = color;
            var rt = img.rectTransform;
            rt.anchoredPosition = Local(x, y);
            rt.localScale = Vector3.one;
            rt.localEulerAngles = Vector3.zero;
            rt.SetAsFirstSibling();
            bursts.Add((img, 0, size));
        }

        // bi rơi vào ô đáy: bộ quầng, sao, vệt ở miệng ô, cỡ theo bề rộng ô
        public void SlotFx(int slot)
        {
            if (slot < 0 || slot >= Board.slots.Count) return;
            var sl = Board.slots[slot];
            float w = (float)(sl.x1 - sl.x0) * K;
            fx.Emit(MachineFx.SlotHit, Local((sl.x0 + sl.x1) / 2, sl.y0 + 6), w / MachineFx.SlotU);
        }

        // rương rơi vào: bảng loé cấp 2 (gỗ, bạc) hoặc 3 (vàng)
        public void ChestFx(double x, double y, int tier) => fx.Emit(MachineFx.ChestHit(tier), Local(x, y), MachineFx.UnitBall * 0.35f);

        public void JackpotFx(double x, double y) => fx.Emit(MachineFx.Jackpot, Local(x, y), MachineFx.UnitBall);

        // bi lọt cốc dưới mái: bộ vòng, chấm, sao; cốc (cái gần chỗ bi nhất) sáng lên
        public void CupFx(double x, double y)
        {
            fx.Emit(MachineFx.RingHit, Local(x, y), MachineFx.UnitBall);
            int best = -1;
            double bd = double.MaxValue;
            for (int i = 0; i < Board.cups.Count; i++)
            {
                double dx = Board.cups[i].x - x, dy = Board.cups[i].y - y, d2 = dx * dx + dy * dy;
                if (d2 < bd)
                {
                    bd = d2;
                    best = i;
                }
            }
            if (best < 0) return;
            var c = Board.cups[best];
            // cỡ như lúc ghép mặt máy tĩnh (ArtGen/Pachinko/ghep_ban.py): cốc rộng 86 % cảm biến, tâm ở 60 % chiều cao cảm biến
            float cw = (float)c.w * 0.86f;
            Lit("pk_coc_sang", Local(c.x, c.y - c.h / 2 + c.h * 0.6), new Vector2(cw, cw * 56f / 96f) * K, 0.8f);
        }

        // phóng bi: bi chờ ở chân làn co giãn như cần phóng của máy tham khảo, khói và chớp ở chân làn
        public void Launch()
        {
            launchT = 0;
            var (x, y) = Board.lane[0];
            fx.Emit(MachineFx.Launch, Local(x, y + 4), MachineFx.UnitBall);
        }

        // mỗi khung: đặt bi theo vật lý, bi chờ, vệt, vòng nấm, giảm dần loé / sáng / chữ nổi. dt là giờ thật, simDt là giờ của máy
        // (nhỏ hơn khi máy chạy chậm): bi, vệt, đinh, nấm và hạt theo giờ máy. mult = mức cược của bi chờ ở chân làn, 0 = không có bi
        public void Sync(float dt, float simDt, int mult)
        {
            simTime += simDt;
            p.cloudBall.gameObject.SetActive(mult > 0);
            if (mult > 0) p.cloudBall.color = BallColor(mult);
            if (launchT >= 0)
            {
                launchT += dt;
                float k = 1 + (MachineFx.Curve(LaunchCurve, launchT) - 1) * 0.5f;
                p.cloud.localScale = new Vector3(1 / Mathf.Sqrt(k), k, 1);
                if (launchT > LaunchCurve[LaunchCurve.Length - 2])
                {
                    launchT = -1;
                    p.cloud.localScale = Vector3.one;
                }
            }

            var list = Board.balls;
            while (balls.Count < list.Count) balls.Add(NewBall());
            for (int i = 0; i < balls.Count; i++)
            {
                var bi = balls[i];
                bool on = i < list.Count;
                if (bi.gameObject.activeSelf != on) bi.gameObject.SetActive(on);
                if (!on) continue;
                var b = list[i];
                bi.color = BallColor(b.mult);
                bi.rectTransform.anchoredPosition = Local(b.x, b.y);
            }
            SyncTrails();
            fx.Update(simDt);

            for (int i = 0; i < bumpers.Length; i++)
            {
                if (!bumpers[i] || bumpT[i] < 0) continue;
                bumpT[i] += simDt;
                float end = BumpCurve[BumpCurve.Length - 2];
                bumpers[i].rectTransform.localScale = Vector3.one * (bumpT[i] >= end ? 1 : MachineFx.Curve(BumpCurve, bumpT[i]));
                if (bumpT[i] >= end)
                {
                    bumpT[i] = -1;
                    var normal = Board.pegs[i].kind == PegKind.Top ? topNormal : bumperNormal;
                    if (normal) bumpers[i].sprite = normal;
                }
            }
            // vòng nấm chạy dần tới số mới (đầy rồi thì chạy về số dư từ 0)
            for (int i = 0; i < ringFill.Length; i++)
            {
                if (ringHold[i] > 0)
                {
                    ringHold[i] -= dt;
                    continue;
                }
                if (!ringFill[i] || Mathf.Approximately(ringShown[i], ringWant[i])) continue;
                if (ringShown[i] >= 1 && ringWant[i] < 1) ringShown[i] = 0;
                ringShown[i] = Mathf.MoveTowards(ringShown[i], ringWant[i], dt * 1.5f);
                ringFill[i].fillAmount = ringShown[i];
            }
            for (int i = lits.Count - 1; i >= 0; i--)
            {
                var (img, age, life) = lits[i];
                age += simDt;
                if (age >= life)
                {
                    fx.Give(img);
                    lits.RemoveAt(i);
                    continue;
                }
                float k = age / life;
                img.rectTransform.localScale = Vector3.one * (age < 0.08f ? Mathf.Lerp(1.12f, 1, age / 0.08f) : 1);
                img.color = new Color(1, 1, 1, k > 0.6f ? 1 - (k - 0.6f) / 0.4f : 1);
                lits[i] = (img, age, life);
            }
            if (multT >= 0)
            {
                multT += dt;
                float k = Mathf.Min(1, multT / MultPop);
                var sc = Vector3.one * (1 + 0.4f * (1 - k) * (1 - k));
                foreach (var (t, _, _) in slotNums)
                    if (t) t.rectTransform.localScale = sc;
                foreach (var tag in chestTags)
                    if (tag) tag.rectTransform.localScale = sc;
                if (k >= 1) multT = -1;
            }
            for (int i = 0; i < glow.Length; i++)
            {
                if (glowT[i] <= 0) continue;
                glowT[i] -= dt;
                if (glowT[i] <= 0) glow[i].gameObject.SetActive(false);
                // rương vàng: sáng đậm và nhấp nháy 3 lần trong nửa giây đầu
                else if (glowMax[i] > 1.5f)
                {
                    float age = glowMax[i] - glowT[i];
                    float blink = age < 0.5f ? 0.55f + 0.45f * Mathf.Abs(Mathf.Cos(age * Mathf.PI * 6)) : 1;
                    var c = rayGlow ? glowTint[i] : new Color(1, 0.86f, 0.3f);
                    c.a = Mathf.Min(0.95f, glowT[i]) * blink;
                    glow[i].color = c;
                }
                else
                {
                    // lớp tia vẽ tay: đậm hơn lớp tô phẳng cũ (tia có khe trong suốt), tắt dần trong 0,3 giây cuối
                    var c = rayGlow ? glowTint[i] : new Color(1, 0.9f, 0.47f);
                    c.a = rayGlow ? Mathf.Min(0.95f, glowT[i] / 0.3f) : Mathf.Min(0.75f, glowT[i]);
                    glow[i].color = c;
                }
            }
            for (int i = 0; i < flash.Length; i++)
            {
                if (flashT[i] <= 0) continue;
                flashT[i] -= simDt;
                if (flashT[i] <= 0)
                {
                    flash[i].gameObject.SetActive(false);
                    continue;
                }
                float age = FlashTime - flashT[i];
                flash[i].rectTransform.localScale = Vector3.one * (age < FlashPop ? Mathf.Lerp(1.15f, 1, age / FlashPop) : 1);
                float a = age < FlashPop ? 1 : 1 - (age - FlashPop) / (FlashTime - FlashPop);
                // hình sáng vẽ tay giữ màu thật; loé tròn cũ tô vàng
                flash[i].color = flashLit[i] ? new Color(1, 1, 1, a) : new Color(1, 0.86f, 0.35f, a);
            }
            if (shakeT > 0)
            {
                shakeT -= dt;
                float k = Mathf.Max(0, shakeT / shakeDur);
                Root.anchoredPosition = shakeT > 0 ? shakeBase + UnityEngine.Random.insideUnitCircle * shakeAmp * k * k : shakeBase;
            }
            for (int i = floats.Count - 1; i >= 0; i--)
            {
                var (t, age, at) = floats[i];
                age += dt;
                if (age > 1.1f)
                {
                    t.gameObject.SetActive(false);
                    freeFloats.Push(t);
                    floats.RemoveAt(i);
                    continue;
                }
                float k = age / 1.1f;
                t.alpha = k > 0.6f ? 1 - (k - 0.6f) / 0.4f : 1;
                t.rectTransform.anchoredPosition = at + new Vector2(0, age * 50 * K);
                // số nhảy ra: 0,3 → 1,3 trong 0,08 giây rồi về 1
                t.rectTransform.localScale = Vector3.one * (age < 0.08f ? Mathf.Lerp(0.3f, 1.3f, age / 0.08f) : age < 0.16f ? Mathf.Lerp(1.3f, 1, (age - 0.08f) / 0.08f) : 1);
                floats[i] = (t, age, at);
            }
            for (int i = bursts.Count - 1; i >= 0; i--)
            {
                var (img, age, scale) = bursts[i];
                age += dt;
                float life = 0.6f * Mathf.Max(1, scale * 0.8f);
                if (age > life)
                {
                    img.gameObject.SetActive(false);
                    freeBursts.Push(img);
                    bursts.RemoveAt(i);
                    continue;
                }
                float k = age / life;
                img.rectTransform.localScale = Vector3.one * (0.5f + k * 1.1f) * scale;
                img.rectTransform.localEulerAngles = new Vector3(0, 0, k * 40 * (scale > 1 ? -1 : 1));
                var c = img.color;
                c.a = 1 - k * k;
                img.color = c;
                bursts[i] = (img, age, scale);
            }
        }

        // vệt dải sau mỗi bi (theo id bi): mẫu vị trí mỗi TrailStep giây giờ máy, các đoạn nối mẫu liền nhau, mờ dần theo tuổi.
        // Bi rơi rồi thì vệt còn lại mờ hết trong TrailTime giây.
        void SyncTrails()
        {
            foreach (var tr in trails.Values) tr.seen = false;
            foreach (var b in Board.balls)
            {
                if (!trails.TryGetValue(b.id, out var tr))
                {
                    tr = new Trail();
                    trails[b.id] = tr;
                }
                tr.seen = tr.alive = true;
                tr.head = Local(b.x, b.y);
                tr.color = BallColor(b.mult);
                if (tr.pts.Count == 0 || simTime - tr.pts[tr.pts.Count - 1].t >= TrailStep) tr.pts.Add((tr.head, simTime));
            }
            float w = TrailWidth * MachineFx.UnitBall;
            trailGone.Clear();
            foreach (var kv in trails)
            {
                var tr = kv.Value;
                if (!tr.seen) tr.alive = false;
                while (tr.pts.Count > 0 && simTime - tr.pts[0].t > TrailTime) tr.pts.RemoveAt(0);
                if (!tr.alive && tr.pts.Count == 0)
                {
                    if (tr.g)
                    {
                        tr.g.gameObject.SetActive(false);
                        freeTrails.Push(tr.g);
                    }
                    trailGone.Add(kv.Key);
                    continue;
                }
                if (!p.trail) continue;
                trailPts.Clear();
                trailAlpha.Clear();
                if (tr.alive)
                {
                    trailPts.Add(tr.head);
                    trailAlpha.Add(1);
                }
                for (int k = tr.pts.Count - 1; k >= 0; k--)
                {
                    trailPts.Add(tr.pts[k].at);
                    trailAlpha.Add(Mathf.Clamp01(1 - (simTime - tr.pts[k].t) / TrailTime));
                }
                if (!tr.g) tr.g = TakeTrail();
                var col = tr.color;
                col.a = TrailAlpha;
                tr.g.Set(trailPts, trailAlpha, w, col);
            }
            foreach (var id in trailGone) trails.Remove(id);
        }

        TrailGraphic TakeTrail()
        {
            if (freeTrails.Count > 0)
            {
                var g = freeTrails.Pop();
                g.gameObject.SetActive(true);
                return g;
            }
            var t = Ui.Spawn(p.trail, p.trailLayer);
            t.name = "vet";
            return t;
        }

        // bi mới khi số bi đang lăn vượt số đã có (bi thừa tắt đi, dùng lại ở đợt sau)
        Image NewBall()
        {
            var bi = Ui.Spawn(p.ball, p.ballLayer);
            bi.name = "bi";
            return bi;
        }
    }
}
