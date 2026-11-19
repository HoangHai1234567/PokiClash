// Con tàu của người chơi (người dùng 2026-11-19: bến tàu cạnh đảo Thủy ở sảnh, bến ở mép dưới đảo Nhà, chuyến tàu qua mây, màn tải).
// - Ảnh theo hướng đi: đi lên nhìn đuôi (tau_len), đi xuống nhìn mũi (tau_xuong), đi ngang nhìn hông (tau_ngang, lật khi sang trái).
//   Đổi hướng thì bóp ngang về 0 rồi bung bằng ảnh mới (đọc như quay đầu); có vùng đệm 8 độ để khỏi lật qua lật lại.
// - Nghiêng theo hướng (tối đa 16 độ), nhấp nhô, lắc nhẹ.
// - Nước rẽ sóng (người dùng 2026-11-19): sóng mũi (tau_mui, 6 khung động) ở mũi tàu, xoay theo hướng đi, đậm theo tốc độ (đi xuống
//   mũi gần mắt: vẽ trên thân, còn lại dưới thân); bọt rẽ từ mũi trôi dọc hai bên mạn ra sau rồi tan; vệt chữ V (tau_vet) sau đuôi.
//   Khi đứng, bọt vỗ nhẹ hai bên mạn. Bọt nằm trong thế giới: trôi theo Flow (lớp chuyến tàu: ngược chiều camera).
// - Theo giờ (DayCycle, người dùng 2026-11-19 "mây và thời tiết ở loading cũng phải đổi theo giờ"): SetTint nhuộm thân, vệt, bọt
//   khi tàu nằm ngoài lớp nhuộm của màn (lớp chuyến tàu); Night(k) thắp quầng đèn lồng ở đuôi (đi lên, đi ngang; đi xuống đèn khuất).
// - Tàu 3D (người dùng 2026-11-19: "làm thẳng tàu thành model 3d ... để nó xoay cho mượt"): mô hình Tripo render 32 hướng trong
//   Blender (ArtGen/Islands/sanh_moi/ben_tau/tau3d: render_32.py, hau_ky.py → Assets/03 Art/Ship/3d/tau_hd_*.png, tau_hd.json).
//   Có bộ khung này thì chọn khung theo hướng (khoảng 11,25 độ, đổi ngay, không bóp), đuôi / mũi / đèn lồng theo từng khung.
// Ảnh vẽ tay cũ Assets/03 Art/Ship (ArtGen/Islands/sanh_moi/ben_tau/cat_tau.py), gốc (0,5; 0,25) ở mớn nước. Dựng bằng ShipBuild (Editor):
// gốc ShipLook phủ khung cha, cùng gốc toạ độ với khung cha (con neo ở pivot cha), nên Pos là toạ độ local của khung cha.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ShipLook : MonoBehaviour
    {
        enum View { Up, Down, Side }

        [SerializeField] RectTransform ship; // gốc tàu: vị trí, cỡ
        [SerializeField] RectTransform body; // nhấp nhô, nghiêng, bóp lúc quay
        [SerializeField] Image hull;
        [SerializeField] Image wake; // vệt chữ V, con của ship (trước thân: vẽ dưới tàu), gốc ở đỉnh chữ V
        [SerializeField] Sprite[] wakeFrames = new Sprite[0]; // vệt chữ V động (tau_vet_1..10): đoạn bọt trôi ra sau
        [Header("Tàu 3D: khung theo hướng")]
        [SerializeField] Sprite[] dirSprites = new Sprite[0];
        [SerializeField] float[] dirAngles = new float[0]; // góc hướng trên màn của từng khung (độ, 0 = phải, 90 = lên)
        [SerializeField] Vector2[] dirBow = new Vector2[0], dirLantern = new Vector2[0]; // so với gốc, đơn vị ảnh, y lên
        [SerializeField] Image bow; // sóng mũi, con của ship (cùng cấp thân)
        [SerializeField] Sprite[] bowFrames = new Sprite[0];
        [SerializeField] Image lantern; // quầng đèn lồng (anim_glow), con của body, trên thân
        [Tooltip("Quầng đèn vẽ trên lớp nhuộm của màn (sảnh: lớp đèn đêm den), bám theo chỗ đèn lồng; trống thì vẽ ngay trên thân")]
        [SerializeField] Image lanternTop;
        [SerializeField] Sprite up, down, side;
        [SerializeField] Image[] foam = new Image[0]; // bọt (dưới tàu)
        [SerializeField] Sprite[] foamSprites = new Sprite[0];
        [SerializeField] float size = 1;

        View view = View.Side, want = View.Side;
        bool flip, wantFlip;
        Vector2 heading = Vector2.right;
        float tilt, bobT, turnT = 1, emitT, lapT, wakeA, bowA, night, wakeT;
        // mũi tàu ở mớn nước (đơn vị ảnh, so với gốc): đi lên mũi ở xa (trên), đi ngang mũi bên phải, đi xuống mũi gần (dưới)
        static readonly Vector2 BowUp = new Vector2(0, 118), BowSide = new Vector2(116, 8), BowDown = new Vector2(0, -16);
        Color tintC = Color.white;
        // chỗ đèn lồng trên ảnh (đơn vị ảnh, so với gốc ở mớn nước): đi lên đèn giữa lan can đuôi, đi ngang đèn trên cột đuôi
        static readonly Vector2 LanternUp = new Vector2(0, 56), LanternSide = new Vector2(-94, 108);
        float[] age, life, spin;
        Vector2[] vel;
        int next;

        public RectTransform Ship => ship;
        public Vector2 Heading => heading;
        public Vector2 Flow { get; set; } // vận tốc dòng nước (đơn vị/giây)

        public Vector2 Pos
        {
            get => ship.anchoredPosition;
            set => ship.anchoredPosition = value;
        }

        public float Size
        {
            get => size;
            set
            {
                size = value;
                ship.localScale = new Vector3(size, size, 1);
            }
        }

        // Dùng khi dựng prefab (Editor).
        public void Setup(RectTransform shipRt, RectTransform bodyRt, Image hullImg, Image wakeImg, Image lanternImg, Sprite upS, Sprite downS,
            Sprite sideS, Image[] foamImgs, Sprite[] foamS, float scale)
        {
            lantern = lanternImg;
            ship = shipRt;
            body = bodyRt;
            hull = hullImg;
            wake = wakeImg;
            up = upS;
            down = downS;
            side = sideS;
            foam = foamImgs;
            foamSprites = foamS;
            size = scale;
            Apply(View.Side, false);
        }

        void Awake()
        {
            int n = foam.Length;
            age = new float[n];
            life = new float[n];
            spin = new float[n];
            vel = new Vector2[n];
            for (int i = 0; i < n; i++)
            {
                life[i] = 0;
                foam[i].gameObject.SetActive(false);
            }
            bobT = Random.value * 10;
            Size = size;
        }

        public void Show(bool on)
        {
            ship.gameObject.SetActive(on);
            if (!on) ClearFoam();
        }

        public bool Shown => ship.gameObject.activeSelf;

        bool Dir3D => dirSprites.Length > 0 && dirAngles.Length == dirSprites.Length;
        int dirIdx = -1;

        // Dùng khi dựng prefab (Editor): bộ khung 32 hướng của tàu 3D
        public void SetDirFrames(Sprite[] sprites, float[] angles, Vector2[] bows, Vector2[] lanterns)
        {
            dirSprites = sprites;
            dirAngles = angles;
            dirBow = bows;
            dirLantern = lanterns;
        }

        int NearestDir(float a)
        {
            int best = 0;
            float bd = 999;
            for (int i = 0; i < dirAngles.Length; i++)
            {
                float d = Mathf.Abs(Mathf.DeltaAngle(dirAngles[i], a));
                if (d < bd)
                {
                    bd = d;
                    best = i;
                }
            }
            return best;
        }

        void ApplyDir(float a, bool force)
        {
            int i = NearestDir(a);
            // vùng đệm 1,5 độ quanh ranh hai khung: khỏi đổi qua đổi lại
            if (!force && dirIdx >= 0 && i != dirIdx && Mathf.Abs(Mathf.DeltaAngle(dirAngles[dirIdx], a)) < Mathf.Abs(Mathf.DeltaAngle(dirAngles[i], a)) + 1.5f)
                i = dirIdx;
            if (i == dirIdx && !force) return;
            dirIdx = i;
            hull.sprite = dirSprites[i];
        }

        // màu nhân theo giờ (lớp chuyến tàu; trong màn thì lớp nhuộm của màn đã nhuộm)
        public void SetTint(Color c)
        {
            tintC = c;
            if (hull) hull.color = c;
        }

        // độ đêm 0..1: đèn lồng
        public void Night(float k) => night = k;

        // Dùng khi dựng prefab (Editor): khung vệt chữ V động
        public void SetWakeFrames(Sprite[] frames) => wakeFrames = frames;

        // Dùng khi dựng prefab (Editor): sóng mũi
        public void SetBow(Image img, Sprite[] frames)
        {
            bow = img;
            bowFrames = frames;
        }

        Vector2 BowLocal => Dir3D && dirIdx >= 0 && dirIdx < dirBow.Length ? dirBow[dirIdx]
            : view == View.Up ? BowUp : view == View.Down ? BowDown : new Vector2(flip ? -BowSide.x : BowSide.x, BowSide.y);

        // mũi gần mắt (đi về phía người xem): sóng mũi vẽ trên thân
        bool BowNear => Dir3D ? BowLocal.y < -8 : view == View.Down;

        // Dùng khi dựng prefab (Editor): quầng đèn đặt trên lớp nhuộm của màn (không bị nhân tối)
        public void SetLanternTop(Image img) => lanternTop = img;

        public void ClearFoam()
        {
            if (life == null) return;
            for (int i = 0; i < foam.Length; i++)
            {
                life[i] = 0;
                foam[i].gameObject.SetActive(false);
            }
        }

        // quay mũi theo hướng d (instant: đổi ảnh ngay, không bóp)
        public void Face(Vector2 d, bool instant = false)
        {
            if (d.sqrMagnitude < 1e-6f) return;
            heading = d.normalized;
            float a = Mathf.Atan2(heading.y, heading.x) * Mathf.Rad2Deg;
            if (Dir3D)
            {
                ApplyDir(a, instant);
                return;
            }
            var (v, f) = Pick(a);
            if (instant)
            {
                want = v;
                wantFlip = f;
                turnT = 1;
                Apply(v, f);
                tilt = TiltOf(a, v, f);
                return;
            }
            if (v != want || f != wantFlip)
            {
                want = v;
                wantFlip = f;
                if (turnT >= 1) turnT = 0; // bắt đầu bóp; giữa chừng thì đổi đích, đổi ảnh lúc bóp hết
            }
        }

        (View, bool) Pick(float a)
        {
            const float pad = 8;
            // giữ ảnh hiện tại tới khi góc vào hẳn vùng khác 8 độ
            if (Inside(a, want, wantFlip) > -pad) return (want, wantFlip);
            if (a > 55 && a < 125) return (View.Up, false);
            if (a < -55 && a > -125) return (View.Down, false);
            return (View.Side, Mathf.Abs(a) > 90);
        }

        static float Inside(float a, View v, bool f)
        {
            switch (v)
            {
                case View.Up: return Mathf.Min(a - 55, 125 - a);
                case View.Down: return Mathf.Min(-55 - a, a + 125);
                default: return f ? Mathf.Abs(a) - 125 : 55 - Mathf.Abs(a);
            }
        }

        static float TiltOf(float a, View v, bool f)
        {
            float t = v == View.Up ? a - 90 : v == View.Down ? a + 90 : f ? a - 180 : a;
            return Mathf.Clamp(Mathf.DeltaAngle(0, t), -16, 16);
        }

        void Apply(View v, bool f)
        {
            view = v;
            flip = f;
            if (!hull) return;
            hull.sprite = v == View.Up ? up : v == View.Down ? down : side;
            hull.SetNativeSize();
        }

        // khoảng từ gốc tàu tới đuôi (đơn vị ảnh, trước khi nhân cỡ) theo ảnh đang hiện
        float Stern => Dir3D && dirIdx >= 0 && dirIdx < dirBow.Length ? dirBow[dirIdx].magnitude * 0.9f
            : view == View.Side ? 92 : view == View.Up ? 6 : 26;

        // mỗi khung: speed là tốc độ tàu so với mặt nước (đơn vị/giây của khung cha)
        public void Tick(float dt, float speed)
        {
            if (!ship.gameObject.activeSelf) return; // tàu ẩn (lớp mây chưa nhận / đã giao tàu): không nhả bọt
            dt = Mathf.Min(dt, 0.05f);
            bobT += dt;
            // quay đầu: bóp ngang, đổi ảnh ở giữa, bung lại
            if (turnT < 1)
            {
                float before = turnT;
                turnT = Mathf.Min(1, turnT + dt / 0.24f);
                if (before < 0.5f && turnT >= 0.5f) Apply(want, wantFlip);
            }
            float sx = turnT < 1 ? Mathf.Max(0.06f, Mathf.Abs(Mathf.Cos(Mathf.PI * turnT))) : 1;
            float a = Mathf.Atan2(heading.y, heading.x) * Mathf.Rad2Deg;
            if (Dir3D)
            {
                if (dirIdx < 0) ApplyDir(a, true);
                // phần lệch giữa hướng thật và khung gần nhất: xoay nhẹ thân cho mượt giữa hai khung
                tilt = Mathf.LerpAngle(tilt, Mathf.Clamp(Mathf.DeltaAngle(dirAngles[dirIdx], a) * 0.5f, -5, 5), 1 - Mathf.Exp(-8 * dt));
                sx = 1;
                flip = false;
            }
            else tilt = Mathf.LerpAngle(tilt, TiltOf(a, view, flip), 1 - Mathf.Exp(-8 * dt));
            body.localPosition = new Vector3(0, Mathf.Sin(bobT * 2.1f) * 2.4f, 0);
            body.localEulerAngles = new Vector3(0, 0, tilt + Mathf.Sin(bobT * 1.37f) * 1.6f);
            body.localScale = new Vector3(sx * (flip ? -1 : 1), 1, 1);
            Wake(dt, speed, a);
            Bow(dt, speed, a);
            Foam(dt, speed);
            Lantern();
        }

        void Bow(float dt, float speed, float a)
        {
            if (!bow || bowFrames.Length == 0) return;
            bowA = Mathf.Lerp(bowA, Mathf.Clamp01((speed - 50) / 260f) * 0.95f, 1 - Mathf.Exp(-6 * dt));
            bool on = bowA > 0.02f;
            if (bow.enabled != on) bow.enabled = on;
            if (!on) return;
            bow.sprite = bowFrames[(int)(bobT * 14) % bowFrames.Length];
            var rt = bow.rectTransform;
            rt.anchoredPosition = BowLocal + (Vector2)body.localPosition;
            rt.localEulerAngles = new Vector3(0, 0, a - 90);
            float st = Mathf.Lerp(0.7f, 1.2f, Mathf.InverseLerp(80, 1200, speed));
            rt.localScale = new Vector3(st, st, 1);
            bow.color = new Color(tintC.r, tintC.g, tintC.b, bowA);
            // đi xuống: mũi gần mắt, sóng vẽ trên thân; còn lại sóng ở phía xa / bên hông: dưới thân
            int bi = rt.GetSiblingIndex(), ti = body.GetSiblingIndex();
            if (BowNear != (bi > ti)) rt.SetSiblingIndex(ti);
        }

        void Lantern()
        {
            if (!lantern) return;
            bool hidden = Dir3D ? false : view == View.Down;
            float k = hidden || !Shown ? 0 : night;
            bool on = k > 0.01f;
            var g = lanternTop ? lanternTop : lantern;
            if (lanternTop && lantern.enabled) lantern.enabled = false;
            if (g.enabled != on) g.enabled = on;
            if (!on) return;
            var rt = lantern.rectTransform;
            rt.anchoredPosition = Dir3D && dirIdx >= 0 && dirIdx < dirLantern.Length ? dirLantern[dirIdx] : view == View.Up ? LanternUp : LanternSide;
            float f = 1 + Mathf.Sin(bobT * 7.3f) * 0.06f + Mathf.Sin(bobT * 13.1f) * 0.04f;
            rt.localScale = new Vector3(f, f, 1);
            if (lanternTop)
            {
                var tr = lanternTop.rectTransform;
                tr.position = rt.position;
                float s = ship.lossyScale.x / Mathf.Max(1e-5f, tr.parent ? tr.parent.lossyScale.x : 1) * f;
                tr.sizeDelta = rt.sizeDelta;
                tr.localScale = new Vector3(s, s, 1);
            }
            g.color = new Color(1, 0.86f, 0.55f, k * (0.8f + 0.2f * Mathf.Sin(bobT * 5.1f)));
        }

        void Wake(float dt, float speed, float a)
        {
            if (!wake) return;
            wakeA = Mathf.Lerp(wakeA, Mathf.Clamp01((speed - 40) / 320f) * 0.95f, 1 - Mathf.Exp(-6 * dt));
            if (wakeFrames.Length > 0)
            {
                // khung đổi theo tốc độ (4–16 khung/giây): bọt trên hai tia trôi ra sau như nước rẽ thật
                wakeT += dt * Mathf.Clamp(speed / 90f, 4, 16);
                wake.sprite = wakeFrames[(int)wakeT % wakeFrames.Length];
            }
            var rt = wake.rectTransform;
            rt.anchoredPosition = -heading * Stern;
            rt.localEulerAngles = new Vector3(0, 0, a - 90);
            float st = Mathf.Lerp(0.55f, 1.3f, Mathf.InverseLerp(80, 1400, speed));
            rt.localScale = new Vector3(0.85f + 0.15f * st, st, 1);
            wake.color = new Color(tintC.r, tintC.g, tintC.b, wakeA);
        }

        void Foam(float dt, float speed)
        {
            if (foam.Length == 0 || age == null) return;
            var perp = new Vector2(-heading.y, heading.x);
            if (speed > 30)
            {
                emitT -= dt;
                if (emitT <= 0)
                {
                    emitT = Mathf.Lerp(0.11f, 0.05f, Mathf.InverseLerp(30, 600, speed));
                    // nước rẽ: bọt sinh ở hai bên mũi, trôi dọc mạn ra sau và toả ra
                    var bowP = Pos + BowLocal * size;
                    for (int s = -1; s <= 1; s += 2)
                    {
                        float out_ = Random.Range(8f, 18f) * size;
                        Emit(bowP + perp * s * out_, -heading * (speed * 0.22f + Random.Range(12f, 26f)) + perp * s * Random.Range(30f, 56f),
                            Random.Range(0.75f, 1.1f), Random.Range(0.45f, 0.72f));
                    }
                }
            }
            else
            {
                // đứng yên: bọt vỗ hai bên mạn
                lapT -= dt;
                if (lapT <= 0)
                {
                    lapT = Random.Range(0.55f, 0.9f);
                    float s = Random.value < 0.5f ? -1 : 1;
                    var at = Pos + new Vector2(s * Random.Range(46f, 74f) * (view == View.Side ? 1.35f : 0.75f), Random.Range(-8f, 4f)) * size;
                    Emit(at, new Vector2(s * Random.Range(5f, 10f), 0), Random.Range(1.4f, 1.9f), Random.Range(0.32f, 0.46f));
                }
            }
            for (int i = 0; i < foam.Length; i++)
            {
                if (life[i] <= 0) continue;
                age[i] += dt;
                float k = age[i] / life[i];
                if (k >= 1)
                {
                    life[i] = 0;
                    foam[i].gameObject.SetActive(false);
                    continue;
                }
                var rt = foam[i].rectTransform;
                vel[i] *= Mathf.Exp(-1.4f * dt);
                rt.anchoredPosition += (vel[i] + Flow) * dt;
                float sc = (spin[i] > 0 ? 1 : -1) * Mathf.Lerp(0.45f, 1.15f, Mathf.Sqrt(k)) * size * Mathf.Abs(spin[i]);
                rt.localScale = new Vector3(sc, Mathf.Abs(sc), 1);
                foam[i].color = new Color(tintC.r, tintC.g, tintC.b, 0.9f * (1 - k * k) * Mathf.Min(1, age[i] / 0.08f));
            }
        }

        void Emit(Vector2 at, Vector2 v, float lifeS, float scale)
        {
            int i = next;
            next = (next + 1) % foam.Length;
            age[i] = 0;
            life[i] = lifeS;
            vel[i] = v;
            spin[i] = (Random.value < 0.5f ? -1 : 1) * scale;
            var img = foam[i];
            if (foamSprites.Length > 0) img.sprite = foamSprites[Random.Range(0, foamSprites.Length)];
            img.SetNativeSize();
            var rt = img.rectTransform;
            rt.anchoredPosition = at;
            rt.localEulerAngles = new Vector3(0, 0, Random.Range(-25f, 25f));
            img.color = new Color(1, 1, 1, 0);
            img.gameObject.SetActive(true);
        }
    }
}
