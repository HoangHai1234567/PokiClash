// Mặt máy bi trên uGUI (toạ độ máy như bản web: x sang phải, y xuống, khung 460 × 680, hiện ở cỡ K lần). Prefab: phần "May" của Screens/Machine.
// Phần tĩnh là ảnh nướng Baked/Machine/may_tinh.png + nhãn ô, rương, máng mây, sáng ô dựng sẵn theo bàn mặc định. Lớp động (canvas con "Dong"):
// bi, vệt, loé đinh, chữ nổi, loé rương sinh từ prefab mục (Items/BiLan, VetBi, LoeDinh, ChuNoi, LoeRuong); bản hết hạn tắt đi để dùng lại.
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
            public Image ball, trail, pegFlash, burst;
            public TextMeshProUGUI floatText;
        }

        [SerializeField] Parts p;

        public Board Board { get; private set; }
        public RectTransform Root => (RectTransform)transform;
        public HoldArea Hold => p.hold;

        float[] glowT;
        Image[] flash;
        float[] flashT;
        readonly List<(Image ball, Image trail)> balls = new List<(Image, Image)>();
        readonly List<(TextMeshProUGUI t, float age, Vector2 at)> floats = new List<(TextMeshProUGUI, float, Vector2)>();
        readonly List<(Image img, float age)> bursts = new List<(Image, float)>();
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

        // Gắn bàn vật lý lúc vào màn. Ảnh tĩnh, nhãn ô và sáng ô của prefab dựng theo bàn mặc định (vị trí đinh, ô không đổi theo hạt giống).
        public void Bind(Board board)
        {
            Board = board;
            glowT = new float[p.glow.Length];
            flash = new Image[board.pegs.Count];
            flashT = new float[flash.Length];
        }

        public static Vector2 Local(double x, double y) => new Vector2((float)x * K, -(float)y * K);
        public Vector3 World(double x, double y) => Root.TransformPoint(Local(x, y));

        // ---------- lớp động ----------

        public void Flash(int peg)
        {
            if (peg < 0 || peg >= flash.Length) return;
            if (!flash[peg])
            {
                var pg = Board.pegs[peg];
                var img = Ui.Spawn(p.pegFlash, p.dyn);
                img.name = "loe" + peg;
                img.rectTransform.Place(new Vector2(0, 1), Local(pg.x, pg.y), Vector2.one * (float)(pg.r + 5) * 2 * K, new Vector2(0.5f, 0.5f));
                img.rectTransform.SetSiblingIndex(p.trailLayer.GetSiblingIndex());
                flash[peg] = img;
            }
            flashT[peg] = 0.25f;
            flash[peg].gameObject.SetActive(true);
        }

        // rare: ô rương sáng lâu và rõ hơn
        public void Glow(int slot, bool rare)
        {
            if (slot < 0 || slot >= p.glow.Length) return;
            glowT[slot] = rare ? 1.1f : 0.5f;
            p.glow[slot].gameObject.SetActive(true);
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

        // vòng loé răng cưa ở chỗ rương rơi vào (ô hiếm nổi bật hẳn)
        public void Burst(double x, double y, Color color)
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
            bursts.Add((img, 0));
        }

        // mỗi khung: đặt bi theo vật lý, máng mây, giảm dần loé / sáng / chữ nổi. mult = mức cược của bi chờ trên mây, 0 = không có bi
        public void Sync(float dt, double launcherX, int mult)
        {
            p.cloud.anchoredPosition = Local(launcherX, Board.DropY - 20);
            p.cloudBall.gameObject.SetActive(mult > 0);
            if (mult > 0) p.cloudBall.color = BallColor(mult);

            var list = Board.balls;
            while (balls.Count < list.Count) balls.Add(NewBall());
            float size = (float)Board.BallR * 2 * K;
            for (int i = 0; i < balls.Count; i++)
            {
                var (bi, tr) = balls[i];
                bool on = i < list.Count;
                if (bi.gameObject.activeSelf != on)
                {
                    bi.gameObject.SetActive(on);
                    tr.gameObject.SetActive(on);
                }
                if (!on) continue;
                var b = list[i];
                var c = BallColor(b.mult);
                bi.color = c;
                bi.rectTransform.anchoredPosition = Local(b.x, b.y);
                tr.color = new Color(c.r, c.g, c.b, 0.25f);
                tr.rectTransform.anchoredPosition = Local(b.x - b.vx * 0.02, b.y - b.vy * 0.02);
                tr.rectTransform.sizeDelta = Vector2.one * size * 0.85f;
            }

            var glow = p.glow;
            for (int i = 0; i < glow.Length; i++)
            {
                if (glowT[i] <= 0) continue;
                glowT[i] -= dt;
                if (glowT[i] <= 0) glow[i].gameObject.SetActive(false);
                else glow[i].color = new Color(1, 0.9f, 0.47f, Mathf.Min(0.75f, glowT[i]));
            }
            for (int i = 0; i < flash.Length; i++)
            {
                if (flashT[i] <= 0) continue;
                flashT[i] -= dt;
                if (flashT[i] <= 0) flash[i].gameObject.SetActive(false);
                else flash[i].color = new Color(1, 0.82f, 0.29f, Mathf.Min(1, flashT[i] * 2));
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
                floats[i] = (t, age, at);
            }
            for (int i = bursts.Count - 1; i >= 0; i--)
            {
                var (img, age) = bursts[i];
                age += dt;
                if (age > 0.6f)
                {
                    img.gameObject.SetActive(false);
                    freeBursts.Push(img);
                    bursts.RemoveAt(i);
                    continue;
                }
                float k = age / 0.6f;
                img.rectTransform.localScale = Vector3.one * (0.5f + k * 1.1f);
                img.rectTransform.localEulerAngles = new Vector3(0, 0, k * 40);
                var c = img.color;
                c.a = 1 - k * k;
                img.color = c;
                bursts[i] = (img, age);
            }
        }

        // bi và vệt mới khi số bi đang lăn vượt số đã có (bi thừa tắt đi, dùng lại ở đợt sau)
        (Image, Image) NewBall()
        {
            var tr = Ui.Spawn(p.trail, p.trailLayer);
            tr.name = "vet";
            var bi = Ui.Spawn(p.ball, p.ballLayer);
            bi.name = "bi";
            return (bi, tr);
        }
    }
}
