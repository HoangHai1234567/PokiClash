// Mặt máy bi trên uGUI (toạ độ máy như bản web: x sang phải, y xuống, khung 460 × 680, hiện ở cỡ K lần). Prefab: phần "May" của Screens/Machine.
// Phần tĩnh là ảnh nướng Baked/Machine/may_tinh.png + nhãn ô, rương, máng mây, sáng ô dựng sẵn theo bàn mặc định. Lớp động (canvas con "Dong"):
// bi, loé đinh, chữ nổi, loé rương sinh từ prefab mục (Items/BiLan, LoeDinh, ChuNoi, LoeRuong); vệt bi là Items/VetBiDai
// (TrailGraphic); nấm và hạt hiệu ứng (MachineFx) là bản sao Items/HatMayBi. Bản hết hạn tắt đi để dùng lại.
// Hiệu ứng chép máy bi tham khảo (GD_Claude/07_MayBi.md): vệt bi 0,3 giây, đinh loé 0,067 giây, nấm phồng xẹp 0,23 giây,
// ô sáng kèm quầng và sao, rương có bảng loé theo cấp, rương vàng có bộ jackpot; hạt chạy theo giờ của máy (chậm khi máy chậm).
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
        Image[] flash;
        float[] flashT;
        Image[] bumpers; // nấm động theo chỉ số đinh (null nếu không phải nấm)
        float[] bumpT;
        readonly List<Image> balls = new List<Image>();
        readonly List<(TextMeshProUGUI t, float age, Vector2 at)> floats = new List<(TextMeshProUGUI, float, Vector2)>();
        readonly List<(Image img, float age, float size)> bursts = new List<(Image, float, float)>();
        Vector2 shakeBase;
        float shakeT, shakeDur, shakeAmp;
        float launchT = -1; // thời gian từ lúc thả (máng mây co giãn), âm = không chạy
        MachineFx fx;
        public MachineFx Fx => fx;

        // đinh sáng: phồng 1,15 → 1 trong 0,067 giây (như máy tham khảo, rồi tắt), ở đây mờ thêm 0,1 giây cho kịp thấy
        public const float FlashPop = 0.067f, FlashTime = FlashPop + 0.1f;
        // nấm bị chạm: cỡ theo các mốc (giây, hệ số) trong 0,233 giây
        static readonly float[] BumpCurve = { 0, 0.905f, 0.033f, 1.184f, 0.1f, 0.894f, 0.167f, 1.053f, 0.233f, 1 };
        // máng mây lúc thả: chiều cao co giãn như cần phóng của máy tham khảo (0,63 → 1,57 → 0,89 → 1,2 → 1), giảm nửa biên độ
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
            shakeBase = Root.anchoredPosition;
            fx = new MachineFx(p.particle, p.fxLayer);
            LayoutBumpers();
        }

        // nấm là ảnh động (ảnh tĩnh không vẽ nấm) nằm dưới lớp vệt, để phồng xẹp được khi bị chạm
        void LayoutBumpers()
        {
            var pegs = Board.pegs;
            bumpers = new Image[pegs.Count];
            bumpT = new float[pegs.Count];
            if (!p.particle) return;
            var sprite = fx.Sprite("pk_bumper");
            for (int i = 0; i < pegs.Count; i++)
            {
                if (pegs[i].kind != PegKind.Bumper) continue;
                var img = fx.Take(p.dyn);
                img.name = "nam" + i;
                img.sprite = sprite;
                img.color = Color.white;
                img.enabled = true;
                var rt = img.rectTransform;
                rt.anchoredPosition = Local(pegs[i].x, pegs[i].y);
                // ảnh nấm chừa 2 đơn vị quanh viền
                rt.sizeDelta = Vector2.one * (float)(pegs[i].r + 2) * 2 * K;
                rt.localScale = Vector3.one;
                rt.localEulerAngles = Vector3.zero;
                rt.SetSiblingIndex(p.trailLayer.GetSiblingIndex());
                bumpers[i] = img;
                bumpT[i] = -1;
            }
        }

        // sáng ô: một ảnh mỗi ô (thêm bản sao của ảnh đầu nếu thiếu, ảnh thừa tắt). Nhãn số ô (con của "nhan" ở hàng đáy):
        // ô EXP và ô +1 bi có số và chữ phụ ("XP", "bi"), ô rương không có chữ (rương vẽ sẵn trong ảnh tĩnh).
        void LayoutSlots()
        {
            var slots = Board.slots;
            float top = (float)Board.SlotTop * K, h = (float)(Board.BH - 8 - Board.SlotTop) * K;
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
                rt.anchoredPosition = new Vector2((float)slots[i].x0 * K, -top);
                rt.sizeDelta = new Vector2((float)(slots[i].x1 - slots[i].x0) * K, h);
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
                if (!t) continue;
                float y = -((RectTransform)c).anchoredPosition.y / K;
                if (Mathf.Abs(y - (float)Board.Floor) < 3) nums.Add(t);
                else if (Mathf.Abs(y - (float)(Board.Floor + 14)) < 3) subs.Add(t);
            }
            if (nums.Count == 0 || subs.Count == 0) return;
            int n = 0;
            foreach (var sl in slots)
            {
                int exp = Pachinko.Exp(sl.reward);
                if (exp == 0 && sl.reward != SlotKind.Ball) continue;
                while (nums.Count <= n) nums.Add(Instantiate(nums[0], labels));
                while (subs.Count <= n) subs.Add(Instantiate(subs[0], labels));
                float cx = (float)(sl.x0 + sl.x1) / 2 * K, w = (float)(sl.x1 - sl.x0);
                var num = nums[n];
                num.text = exp > 0 ? exp.ToString() : "+1";
                num.color = exp > 0 ? XpColor : BallPink;
                num.fontSize = (w < 30 ? 13 : 17) * K;
                num.rectTransform.anchoredPosition = new Vector2(cx, -(float)Board.Floor * K);
                num.rectTransform.sizeDelta = new Vector2(w * K, num.rectTransform.sizeDelta.y);
                var sub = subs[n];
                sub.text = exp > 0 ? "XP" : "bi";
                sub.rectTransform.anchoredPosition = new Vector2(cx, -(float)(Board.Floor + 14) * K);
                sub.rectTransform.sizeDelta = new Vector2(w * K, sub.rectTransform.sizeDelta.y);
                num.gameObject.SetActive(true);
                sub.gameObject.SetActive(true);
                n++;
            }
            for (int i = n; i < nums.Count; i++) nums[i].gameObject.SetActive(false);
            for (int i = n; i < subs.Count; i++) subs[i].gameObject.SetActive(false);
        }

        // rương nhỏ (prefab kit Ruong, con của "nhan"): một cái giữa mỗi ô rương ở đáy, một cái trong mỗi cốc và két.
        // Prefab có sẵn vài cái theo bàn cũ: dùng lại, thiếu thì nhân bản, thừa thì tắt. Ô đáy giữ cỡ và độ cao của rương ô sẵn có.
        void LayoutChestIcons(Transform labels)
        {
            var icons = new List<ChestIcon>(labels.GetComponentsInChildren<ChestIcon>(true));
            if (icons.Count == 0) return;
            float slotY = float.NaN, slotW = 0, cupW = 0;
            foreach (var ic in icons)
            {
                float y = -ic.Rect.anchoredPosition.y / K;
                if (y > Board.SlotTop)
                {
                    slotY = ic.Rect.anchoredPosition.y;
                    slotW = ic.Rect.sizeDelta.x;
                }
                else cupW = ic.Rect.sizeDelta.x;
            }
            if (float.IsNaN(slotY)) slotY = -(float)(Board.Floor + 4) * K;
            if (slotW <= 0) slotW = 0.38f * 48 * K;
            if (cupW <= 0) cupW = slotW;

            var want = new List<(SlotKind kind, Vector2 at, float w)>();
            foreach (var sl in Board.slots)
                if (Pachinko.IsChest(sl.reward)) want.Add((sl.reward, new Vector2((float)(sl.x0 + sl.x1) / 2 * K, slotY), slotW));
            foreach (var c in Board.cups)
            {
                // cốc tròn: rương ở thân cốc như bàn cũ; két: rương giữa vùng cảm biến, to hơn một chút
                var at = c.r > 0 ? new Vector2((float)c.x * K, -(float)(c.y + 2) * K) : new Vector2((float)c.x * K, -(float)c.y * K);
                want.Add((c.reward, at, c.r > 0 ? cupW : cupW * 1.4f));
            }
            for (int i = 0; i < want.Count; i++)
            {
                if (i >= icons.Count) icons.Add(Instantiate(icons[0], labels));
                var (kind, at, w) = want[i];
                icons[i].Bind(kind, w);
                icons[i].Rect.anchoredPosition = at;
                icons[i].gameObject.SetActive(true);
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
                fx.Emit(MachineFx.BumperHit, Local(pg.x, pg.y), (float)pg.r * 2 * K / 1.1f);
                return;
            }
            fx.Emit(MachineFx.PegHit, Local(pg.x, pg.y), (float)pg.r * 2 * K);
            fx.Emit(MachineFx.PegSpark, Local(pg.x, pg.y), MachineFx.UnitBall);
            if (!flash[peg])
            {
                var img = Ui.Spawn(p.pegFlash, p.dyn);
                img.name = "loe" + peg;
                img.rectTransform.Place(new Vector2(0, 1), Local(pg.x, pg.y), Vector2.one * (float)(pg.r + 2) * 2 * K, new Vector2(0.5f, 0.5f));
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
            fx.Emit(MachineFx.SlotHit, Local((sl.x0 + sl.x1) / 2, Board.Floor - 6), w / MachineFx.SlotU);
        }

        // rương rơi vào: bảng loé cấp 2 (gỗ, bạc) hoặc 3 (vàng)
        public void ChestFx(double x, double y, int tier) => fx.Emit(MachineFx.ChestHit(tier), Local(x, y), MachineFx.UnitBall * 0.35f);

        public void JackpotFx(double x, double y) => fx.Emit(MachineFx.Jackpot, Local(x, y), MachineFx.UnitBall);

        // bi lọt cốc bạc hoặc két
        public void CupFx(double x, double y) => fx.Emit(MachineFx.RingHit, Local(x, y), MachineFx.UnitBall);

        // thả bi: máng mây co giãn, khói và chớp dưới mây
        public void Launch(double x)
        {
            launchT = 0;
            fx.Emit(MachineFx.Launch, Local(x, Board.DropY - 4), MachineFx.UnitBall);
        }

        // mỗi khung: đặt bi theo vật lý, máng mây, vệt, giảm dần loé / sáng / chữ nổi. dt là giờ thật, simDt là giờ của máy (nhỏ hơn
        // khi máy chạy chậm): bi, vệt, đinh, nấm và hạt theo giờ máy. mult = mức cược của bi chờ trên mây, 0 = không có bi
        public void Sync(float dt, float simDt, double launcherX, int mult)
        {
            simTime += simDt;
            p.cloud.anchoredPosition = Local(launcherX, Board.DropY - 20);
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
                if (bumpT[i] >= end) bumpT[i] = -1;
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
                    glow[i].color = new Color(1, 0.86f, 0.3f, Mathf.Min(0.95f, glowT[i]) * blink);
                }
                else glow[i].color = new Color(1, 0.9f, 0.47f, Mathf.Min(0.75f, glowT[i]));
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
                flash[i].color = new Color(1, 0.86f, 0.35f, a);
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
