// Sân vận động của Trường đua (người dùng 2026-11-26: "thiết kế track đua như kiểu sân vận động 2 bên có khán giả"). Gắn trên khung
// nhìn `san` của Screens/CasinoRace, mọi vật dựng sẵn bằng menu "PokiClash/Prefab/Đảo Casino/Trường đua: dựng scene"; hình ở
// Assets/03 Art/Baked/Casino/race_*.png (ArtGen/Casino/truong_dua/dong_goi.py).
// Khung nhìn phủ kín màn hình (người dùng 2026-11-26: "cho trường đua fullscreen"): khán đài neo mép trên, hàng rào và cổ động viên
// neo mép dưới, mặt đường giãn ở giữa theo chiều cao màn.
// Thế giới cuộn ngang theo máy quay (px = đơn vị đường đua × K), khung nhìn đứng yên. Các lớp từ xa tới gần:
// - khán đài mái sọc hai tầng (dải lát lật gương, trôi chậm hơn mặt đường) + cờ mái phất + 6 hàng khán giả ngồi;
// - tường trước khán đài, mặt đường (lát theo chặng, nhuộm màu hệ), cổng chặng (cột cờ màu hệ, biển tên hệ, vạch phấn; cổng cuối là
//   vạch đích ca rô), trang trí theo hệ hai mép đường;
// - [tướng do RaceScene vẽ chen vào giữa];
// - hàng rào dây, hai hàng cổ động viên quay lưng ở sát máy quay (trôi nhanh hơn mặt đường).
// Khán giả, cờ, trang trí là một nhóm hình dựng sẵn xoay vòng theo chỗ đứng trong thế giới (không sinh lúc chạy): mỗi chỗ băm ra
// hình, cỡ, nhịp nhún riêng nên cuộn qua vẫn là "người đó". Khán giả nhún theo độ náo nhiệt (Mood), bật theo chỗ có va chạm (Pulse),
// làm sóng người (Wave), hàng gần nhảy khi người chơi cổ vũ trúng (CheerJump); hoa giấy (Burst / Rain), chớp trắng (Flash).
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class RaceStadium : MonoBehaviour
    {
        public const float K = 27f; // px màn cho mỗi đơn vị đường đua
        const float WaveSec = 1.5f, Gravity = 1500f;

        [Serializable]
        public struct Tiles
        {
            public RectTransform[] items; // neo trên trái, pivot (0,5; 1)
            public float width, parallax;
            public bool mirror; // ô lẻ lật gương (mép nối luôn khớp)
        }

        [Serializable]
        public struct Gate
        {
            public RectTransform far, near; // cụm phía xa (sau tướng), cụm phía gần (trước tướng)
            public RectTransform flagFar, flagNear; // lá cờ, phất quanh cán
            public Image clothFar, clothNear; // vải cờ trắng để nhuộm màu hệ (cổng đích: cờ ca rô, để trống)
            public Image signFill; // mặt biển tròn
            public TextMeshProUGUI sign; // tên hệ của chặng bắt đầu ở cổng này
        }

        [Serializable]
        public struct Parts
        {
            public RectTransform view;
            public Tiles stands, standsLow, walls, fences; // standsLow: tầng ghế dưới (cùng hình, vẽ trước, mái bị tầng trên che)
            public RectTransform[] grounds; // pivot (0; 1)
            public Image[] groundFill; // dải mặt đường của từng ô (nhuộm màu chặng)
            public RectTransform[] roofFlags;
            public float roofFlagStep, roofFlagY;
            public Image[] fans; // hàng × cột, hàng xa trước
            public int fanCols;
            public float fanStep, fanScale;
            public float[] fanRowY; // đáy hình của từng hàng, tính từ mép trên khung
            public Sprite[] fanSprites;
            public Image[] nearFans; // hàng × cột, hàng xa trước; neo mép dưới khung
            public int nearCols;
            public float[] nearRowY, nearRowScale, nearRowStep, nearRowParallax; // nearRowY: đáy hình tính từ mép dưới khung (âm: thụt dưới màn)
            public Sprite[] nearSprites;
            public Gate[] gates;
            public Image[] decalsFar, decalsNear;
            public Sprite[] decalSprites; // 5 hệ theo thứ tự Elements.All, mỗi hệ 3 hình
            public float decalStep, decalScale, decalFarY, decalNearY; // decalFarY từ mép trên, decalNearY từ mép dưới
            public float feetTop, feetBottomInset; // dải đặt chân tướng: làn đầu từ mép trên, làn cuối cách mép dưới
            public Image[] confetti;
            public Image flash;
        }

        struct PulseHit
        {
            public float x, radius, amp, t0;
        }

        [SerializeField] Parts p;

        Elem[] terrain = new Elem[0];
        float segPx = 60 * K, groundW = 1020, cam, lastCam, mood = 0.15f, moodTo = 0.15f, clock;
        float waveT = -1, cheerT = -1, cheerAmp, flashA, rainLeft, rainAcc;
        Color rainA = Color.white, rainB = Color.white;
        int[] fanSlot = new int[0], nearSlot = new int[0];
        readonly PulseHit[] pulses = new PulseHit[4];
        Vector2[] cPos = new Vector2[0], cVel = new Vector2[0];
        float[] cLife = new float[0], cSpin = new float[0];
        uint rngState = 0x1234567u;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        public float Cam => cam;
        public float Width => p.view ? p.view.rect.width : 1080;
        public float Height => p.view ? p.view.rect.height : 1920;
        float FeetBottom => Height - p.feetBottomInset;

        // bề cao một làn khi có n tướng
        public float LaneGap(int n) => (FeetBottom - p.feetTop) / Mathf.Max(1, n);
        public float LengthPx => segPx * Mathf.Max(1, terrain.Length);
        public float Mood { set => moodTo = Mathf.Clamp01(value); }

        // x trong khung nhìn của một vị trí trên đường đua
        public float ViewX(double pos) => (float)pos * K - cam;

        // y chân tướng của làn i trong n làn (tính từ mép trên khung, dương xuống dưới)
        public float LaneY(int i, int n) => Mathf.Lerp(p.feetTop, FeetBottom, (i + 0.5f) / Mathf.Max(1, n));

        // y vạch kẻ giữa làn i − 1 và làn i
        public float LaneLineY(int i, int n) => Mathf.Lerp(p.feetTop, FeetBottom, (float)i / Mathf.Max(1, n)) + 4;

        public Color SegColor(int seg) => seg >= 0 && seg < terrain.Length ? Color.Lerp(Theme.Of(terrain[seg]), Theme.Paper, 0.5f) : Theme.Hex("#e3cfa4");

        public int SegAt(float worldPx) => Mathf.FloorToInt(worldPx / segPx);

        // đường hôm nay: màu từng chặng, cờ và biển tên hệ ở cổng
        public void SetTrack(Elem[] elems, double segUnits)
        {
            terrain = elems ?? new Elem[0];
            segPx = Mathf.Max(200, (float)segUnits * K);
            groundW = segPx / Mathf.Ceil(segPx / Mathf.Max(200, Width));
            foreach (var g in p.grounds) g.sizeDelta = new Vector2(groundW + 1, g.sizeDelta.y);
            for (int i = 0; i < p.gates.Length; i++)
            {
                var g = p.gates[i];
                bool finish = i == p.gates.Length - 1;
                bool has = finish || i < terrain.Length;
                g.far.gameObject.SetActive(has);
                g.near.gameObject.SetActive(has);
                if (!has || finish) continue;
                var c = Theme.Of(terrain[i]);
                if (g.clothFar) g.clothFar.color = c;
                if (g.clothNear) g.clothNear.color = c;
                if (g.signFill) g.signFill.color = Color.Lerp(c, Color.white, 0.72f);
                if (g.sign)
                {
                    g.sign.text = Elements.Name(terrain[i]);
                    g.sign.color = Color.Lerp(c, Theme.Ink, 0.45f);
                }
            }
            for (int i = 0; i < fanSlot.Length; i++) fanSlot[i] = int.MinValue;
            Place();
        }

        public void SetCamera(float camPx)
        {
            cam = camPx;
        }

        // khán giả quanh chỗ viewX bật lên (va chạm, gió thuận, đổi ngôi đầu)
        public void Pulse(float viewX, float radius, float amp)
        {
            int k = 0;
            for (int i = 1; i < pulses.Length; i++)
                if (pulses[i].t0 < pulses[k].t0) k = i;
            pulses[k] = new PulseHit { x = viewX, radius = Mathf.Max(60, radius), amp = amp, t0 = clock };
        }

        // sóng người chạy ngang khán đài
        public void Wave()
        {
            if (waveT < 0) waveT = 0;
        }

        // hàng cổ động viên sát máy quay nhảy (người chơi cổ vũ trúng nhịp)
        public void CheerJump(float amp)
        {
            cheerT = 0;
            cheerAmp = amp;
        }

        public void Flash(float a) => flashA = Mathf.Max(flashA, a);

        // hoa giấy bung từ một điểm trong khung (x từ trái, y từ mép trên xuống)
        public void Burst(Vector2 at, int n, Color a, Color b)
        {
            EnsureConfetti();
            for (int i = 0; i < cLife.Length && n > 0; i++)
            {
                if (cLife[i] > 0) continue;
                float ang = Mathf.Lerp(0.15f, 0.85f, Rand()) * Mathf.PI;
                float sp = Mathf.Lerp(420, 980, Rand());
                Spawn(i, at, new Vector2(Mathf.Cos(ang) * sp * 0.9f, Mathf.Sin(ang) * sp), Rand() < 0.5f ? a : b);
                n--;
            }
        }

        // hoa giấy rơi từ mái xuống trong sec giây
        public void Rain(float sec, Color a, Color b)
        {
            rainLeft = Mathf.Max(rainLeft, sec);
            rainA = a;
            rainB = b;
        }

        public void Calm()
        {
            rainLeft = 0;
            waveT = cheerT = -1;
            flashA = 0;
            for (int i = 0; i < pulses.Length; i++) pulses[i].amp = 0;
            EnsureConfetti();
            for (int i = 0; i < cLife.Length; i++)
            {
                cLife[i] = 0;
                p.confetti[i].enabled = false;
            }
            if (p.flash) p.flash.enabled = false;
        }

        float Rand()
        {
            rngState ^= rngState << 13;
            rngState ^= rngState >> 17;
            rngState ^= rngState << 5;
            return (rngState & 0xFFFFFF) / (float)0x1000000;
        }

        static uint Hash(int a, int b)
        {
            unchecked
            {
                uint x = (uint)a * 0x9E3779B1u ^ (uint)(b + 7) * 0x85EBCA6Bu;
                x ^= x >> 15;
                x *= 0x2C1B3C6Du;
                x ^= x >> 12;
                x *= 0x297A2D39u;
                x ^= x >> 15;
                return x;
            }
        }

        void EnsureConfetti()
        {
            int n = p.confetti != null ? p.confetti.Length : 0;
            if (cLife.Length == n) return;
            cPos = new Vector2[n];
            cVel = new Vector2[n];
            cLife = new float[n];
            cSpin = new float[n];
        }

        void Spawn(int i, Vector2 at, Vector2 vel, Color c)
        {
            cPos[i] = at;
            cVel[i] = vel;
            cLife[i] = Mathf.Lerp(1.3f, 2.1f, Rand());
            cSpin[i] = Mathf.Lerp(-540, 540, Rand());
            var img = p.confetti[i];
            img.enabled = true;
            img.color = c;
            img.rectTransform.localEulerAngles = new Vector3(0, 0, Rand() * 360);
        }

        // mỗi khung hình: RaceScene đặt máy quay rồi gọi
        public void Tick(float dt)
        {
            clock += dt;
            mood = Mathf.MoveTowards(mood, moodTo, dt * 1.6f);
            float dCam = cam - lastCam;
            lastCam = cam;
            for (int i = 0; i < pulses.Length; i++) pulses[i].x -= dCam;
            if (waveT >= 0)
            {
                waveT += dt;
                if (waveT > WaveSec) waveT = -1;
            }
            if (cheerT >= 0)
            {
                cheerT += dt;
                if (cheerT > 1.1f) cheerT = -1;
            }
            Place();
            DrawFans();
            DrawNearFans();
            DrawFlags();
            DrawConfetti(dt);
            if (p.flash)
            {
                flashA = Mathf.MoveTowards(flashA, 0, dt * 2.6f);
                p.flash.enabled = flashA > 0.01f;
                if (p.flash.enabled) p.flash.color = new Color(1, 1, 1, flashA);
            }
        }

        // ---------- lớp nền ----------

        static void PlaceTiles(Tiles t, float camPx)
        {
            if (t.items == null || t.width <= 0) return;
            float off = camPx * t.parallax;
            int k0 = Mathf.FloorToInt(off / t.width);
            for (int i = 0; i < t.items.Length; i++)
            {
                int k = k0 + i;
                var rt = t.items[i];
                rt.anchoredPosition = new Vector2(k * t.width - off + t.width * 0.5f, rt.anchoredPosition.y);
                if (t.mirror) rt.localScale = new Vector3((k & 1) == 0 ? 1 : -1, 1, 1);
            }
        }

        void Place()
        {
            PlaceTiles(p.standsLow, cam);
            PlaceTiles(p.stands, cam);
            PlaceTiles(p.walls, cam);
            PlaceTiles(p.fences, cam);
            int k0 = Mathf.FloorToInt(cam / groundW);
            for (int i = 0; i < p.grounds.Length; i++)
            {
                int k = k0 + i;
                p.grounds[i].anchoredPosition = new Vector2(k * groundW - cam, p.grounds[i].anchoredPosition.y);
                if (i < p.groundFill.Length && p.groundFill[i]) p.groundFill[i].color = SegColor(SegAt((k + 0.5f) * groundW));
            }
            float w = Width;
            for (int i = 0; i < p.gates.Length; i++)
            {
                var g = p.gates[i];
                bool finish = i == p.gates.Length - 1;
                if (!finish && i >= terrain.Length) continue;
                float x = (finish ? terrain.Length : i) * segPx + K - cam; // vạch nằm trước mũi tướng một đơn vị
                bool on = x > -260 && x < w + 260;
                if (g.far.gameObject.activeSelf != on) g.far.gameObject.SetActive(on);
                if (g.near.gameObject.activeSelf != on) g.near.gameObject.SetActive(on);
                if (!on) continue;
                g.far.anchoredPosition = new Vector2(x, g.far.anchoredPosition.y);
                g.near.anchoredPosition = new Vector2(x, g.near.anchoredPosition.y);
            }
            Decals(p.decalsFar, p.decalFarY, 31, false);
            Decals(p.decalsNear, p.decalNearY, 59, true);
        }

        void Decals(Image[] pool, float y, int salt, bool fromBottom)
        {
            if (pool == null || p.decalSprites == null || p.decalSprites.Length < 15) return;
            float len = LengthPx;
            int j0 = Mathf.FloorToInt((cam - 140) / p.decalStep);
            for (int i = 0; i < pool.Length; i++)
            {
                int j = j0 + i;
                uint h = Hash(j, salt);
                float wx = j * p.decalStep + (h & 127) - 64f;
                int seg = SegAt(wx);
                float gate = Mathf.Abs(wx - Mathf.Round(wx / segPx) * segPx);
                bool show = seg >= 0 && seg < terrain.Length && wx > 120 && wx < len - 120 && gate > 150 && (h >> 8) % 10 < 7;
                var img = pool[i];
                if (img.enabled != show) img.enabled = show;
                if (!show) continue;
                int e = Mathf.Max(0, Array.IndexOf(Elements.All, terrain[seg]));
                var sp = p.decalSprites[e * 3 + (int)((h >> 12) % 3)];
                if (img.sprite != sp)
                {
                    img.sprite = sp;
                    img.rectTransform.sizeDelta = sp.rect.size * p.decalScale;
                }
                float jit = (h >> 16) & 15;
                img.rectTransform.anchoredPosition = new Vector2(wx - cam, fromBottom ? y - jit : -(y + jit));
            }
        }

        // ---------- khán giả ----------

        void Dress(Image img, Sprite[] sprites, uint h, float scale, int emptyOneIn)
        {
            bool on = sprites != null && sprites.Length > 0 && (emptyOneIn <= 0 || (h >> 5) % (uint)emptyOneIn != 0);
            img.enabled = on;
            if (!on) return;
            var sp = sprites[h % (uint)sprites.Length];
            img.sprite = sp;
            float k = scale * (0.92f + ((h >> 9) & 15) / 15f * 0.16f);
            img.rectTransform.sizeDelta = sp.rect.size * k;
        }

        // độ nhấc của một khán giả ở viewX: nhún nền theo độ náo nhiệt + nhảy cuồng lúc nước rút + bật theo va chạm + sóng người
        float Lift(float x, uint h, float w)
        {
            float ph = (h & 1023) * 0.00614f;
            float y = Mathf.Sin(clock * Mathf.Lerp(2.4f, 6.5f, mood) + ph) * Mathf.Lerp(1.5f, 5f, mood);
            if (mood > 0.7f) y += Mathf.Abs(Mathf.Sin(clock * 8.5f + ph)) * 16f * (mood - 0.7f) / 0.3f;
            for (int i = 0; i < pulses.Length; i++)
            {
                var q = pulses[i];
                if (q.amp <= 0) continue;
                float d = Mathf.Abs(x - q.x) / q.radius;
                if (d >= 1) continue;
                float tau = clock - q.t0 - d * 0.18f;
                if (tau < 0 || tau > 0.84f) continue;
                y += q.amp * (1 - d * 0.6f) * Mathf.Abs(Mathf.Sin(tau / 0.42f * Mathf.PI)) * (tau < 0.42f ? 1 : 0.5f);
            }
            if (waveT >= 0)
            {
                float xw = waveT / WaveSec * (w + 400) - 200;
                float d = Mathf.Abs(x - xw) / 150f;
                if (d < 1) y += 30f * (1 - d) * (1 - d);
            }
            return y;
        }

        void DrawFans()
        {
            if (p.fans == null || p.fanCols <= 0 || p.fanRowY == null) return;
            if (fanSlot.Length != p.fans.Length)
            {
                fanSlot = new int[p.fans.Length];
                for (int i = 0; i < fanSlot.Length; i++) fanSlot[i] = int.MinValue;
            }
            float off = cam * p.stands.parallax, w = Width;
            int rows = Mathf.Min(p.fanRowY.Length, p.fans.Length / p.fanCols);
            for (int r = 0; r < rows; r++)
            {
                float rowOff = (r & 1) * p.fanStep * 0.5f;
                int j0 = Mathf.FloorToInt((off - rowOff) / p.fanStep) - 1;
                for (int c = 0; c < p.fanCols; c++)
                {
                    int idx = r * p.fanCols + c, j = j0 + c;
                    var img = p.fans[idx];
                    uint h = Hash(j, r);
                    if (fanSlot[idx] != j)
                    {
                        fanSlot[idx] = j;
                        Dress(img, p.fanSprites, h, p.fanScale, 12);
                    }
                    if (!img.enabled) continue;
                    float x = j * p.fanStep + rowOff - off + ((h >> 20) & 15) - 8;
                    var rt = img.rectTransform;
                    rt.anchoredPosition = new Vector2(x, -p.fanRowY[r] + Lift(x, h, w));
                    rt.localEulerAngles = new Vector3(0, 0, Mathf.Sin(clock * 3.1f + (h & 255) * 0.07f) * (1.5f + 4 * mood));
                }
            }
        }

        void DrawNearFans()
        {
            if (p.nearFans == null || p.nearCols <= 0 || p.nearRowY == null) return;
            if (nearSlot.Length != p.nearFans.Length)
            {
                nearSlot = new int[p.nearFans.Length];
                for (int i = 0; i < nearSlot.Length; i++) nearSlot[i] = int.MinValue;
            }
            float w = Width;
            int rows = Mathf.Min(p.nearRowY.Length, p.nearFans.Length / p.nearCols);
            for (int r = 0; r < rows; r++)
            {
                float step = p.nearRowStep[r], off = cam * p.nearRowParallax[r];
                int j0 = Mathf.FloorToInt(off / step) - 1;
                for (int c = 0; c < p.nearCols; c++)
                {
                    int idx = r * p.nearCols + c, j = j0 + c;
                    var img = p.nearFans[idx];
                    uint h = Hash(j, 97 + r * 13);
                    if (nearSlot[idx] != j)
                    {
                        nearSlot[idx] = j;
                        Dress(img, p.nearSprites, h, p.nearRowScale[r], 0);
                    }
                    float x = j * step - off + ((h >> 20) & 31) - 16;
                    float lift = Lift(x, h, w) * (1.2f + 0.4f * r);
                    if (cheerT >= 0)
                    {
                        float tau = cheerT - (h & 7) * 0.02f;
                        if (tau > 0 && tau < 0.9f) lift += cheerAmp * Mathf.Abs(Mathf.Sin(tau / 0.45f * Mathf.PI)) * (tau < 0.45f ? 1 : 0.55f);
                    }
                    var rt = img.rectTransform;
                    rt.anchoredPosition = new Vector2(x, p.nearRowY[r] + lift);
                    rt.localEulerAngles = new Vector3(0, 0, Mathf.Sin(clock * 2.6f + (h & 255) * 0.09f) * (1.5f + 3 * mood));
                }
            }
        }

        void DrawFlags()
        {
            if (p.roofFlags != null && p.roofFlagStep > 0)
            {
                float off = cam * p.stands.parallax;
                int j0 = Mathf.FloorToInt(off / p.roofFlagStep) - 1;
                for (int c = 0; c < p.roofFlags.Length; c++)
                {
                    int j = j0 + c;
                    var rt = p.roofFlags[c];
                    rt.anchoredPosition = new Vector2(j * p.roofFlagStep + p.roofFlagStep * 0.5f - off, -p.roofFlagY);
                    rt.localEulerAngles = new Vector3(0, 0, Mathf.Sin(clock * 2.6f + j * 1.3f) * 5f);
                }
            }
            for (int i = 0; i < p.gates.Length; i++)
            {
                var g = p.gates[i];
                if (!g.far.gameObject.activeSelf) continue;
                float a = Mathf.Sin(clock * 3.4f + i * 1.7f) * 6f;
                if (g.flagFar) g.flagFar.localEulerAngles = new Vector3(0, 0, a);
                if (g.flagNear) g.flagNear.localEulerAngles = new Vector3(0, 0, -a * 0.8f);
            }
        }

        // ---------- hoa giấy ----------

        void DrawConfetti(float dt)
        {
            EnsureConfetti();
            if (rainLeft > 0)
            {
                rainLeft -= dt;
                rainAcc += dt * 16;
                float w = Width;
                for (int i = 0; i < cLife.Length && rainAcc >= 1; i++)
                {
                    if (cLife[i] > 0) continue;
                    rainAcc -= 1;
                    Spawn(i, new Vector2(Rand() * w, -20), new Vector2(Mathf.Lerp(-90, 90, Rand()), -Mathf.Lerp(120, 320, Rand())), Rand() < 0.5f ? rainA : rainB);
                }
                if (rainAcc > 3) rainAcc = 3;
            }
            for (int i = 0; i < cLife.Length; i++)
            {
                if (cLife[i] <= 0) continue;
                cLife[i] -= dt;
                var img = p.confetti[i];
                if (cLife[i] <= 0)
                {
                    img.enabled = false;
                    continue;
                }
                var v = cVel[i];
                v.y -= Gravity * dt;
                v.x *= Mathf.Exp(-1.6f * dt);
                if (v.y < -330) v.y = -330; // giấy rơi lững lờ
                cVel[i] = v;
                cPos[i] += new Vector2(v.x + Mathf.Sin(clock * 6 + i) * 40, -v.y) * dt;
                var rt = img.rectTransform;
                rt.anchoredPosition = new Vector2(cPos[i].x, -cPos[i].y);
                rt.localEulerAngles = new Vector3(0, 0, rt.localEulerAngles.z + cSpin[i] * dt);
                var c = img.color;
                img.color = new Color(c.r, c.g, c.b, Mathf.Clamp01(cLife[i] / 0.35f));
            }
        }
    }
}
