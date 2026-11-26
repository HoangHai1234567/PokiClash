// Viên bi của Vòng Xoay Ngũ Hành (GD_Claude/31 mốc D4): mô phỏng vật lý viên bi trên bánh xe, tất định theo hạt giống, không phụ thuộc
// Unity. Ô ra do LÕI chọn trước (Roulette.Spin, theo tỉ lệ trong cấu hình); ở đây chỉ tìm một cú thả bi THẬT (chỉ đổi lực thả trong
// khoảng tự nhiên) mà mô phỏng cho bi nằm đúng ô đó (RouletteBall.Plan), rồi ghi lại cả đường đi để màn phát lại nguyên văn. Vì vậy
// hình thấy là vật lý thật, còn tỉ lệ ra hoàn toàn do lõi kiểm soát.
//
// Hình học (đơn vị: bán kính vành ngoài của lòng chảo = 1; nhìn từ trên xuống, góc ngược chiều kim đồng hồ, 0 rad ở bên phải):
//   vành gỗ 0,90..1 | đường bi chạy (nghiêng) 0,80..0,90, bi tì vách ở RTrack | sườn dốc có 8 mấu chắn (hình thoi) 0,70..0,80
//   | MÂM xoay: vòng số 0,61..0,70, vòng ô (có vách ngăn 26 ô) 0,50..0,61, nón giữa < 0,50.
// Mâm xoay ngược chiều kim đồng hồ (Ω > 0) chậm dần về tốc độ nghỉ; bi được thả theo chiều kim đồng hồ (ω < 0).
// Vị trí trên mâm đánh số 0..25 theo góc trong hệ mâm (vị trí j chiếm [j, j + 1) × 2π/26); ô (hệ, số) nào nằm ở vị trí nào: RouletteWheel.
using System;
using System.Collections.Generic;

namespace PokiClash.Core
{
    // Cách xếp 26 ô của lõi (Roulette: ô i = hệ i / 5, số i % 5 + 1, ô 25 Sao Vàng) quanh mâm: các hệ xen kẽ nhau như bánh xe thật,
    // cùng một số cách đều nhau; Sao Vàng ở vị trí 25.
    public static class RouletteWheel
    {
        public const int Slots = 26;
        public const double Step = Math.PI * 2 / Slots;

        // vị trí trên mâm -> ô của lõi
        public static int PocketAt(int slot)
        {
            if (slot == Slots - 1) return Roulette.StarPocket;
            int e = slot % 5, q = slot / 5;
            return e * 5 + (q + 2 * e) % 5;
        }

        // ô của lõi -> vị trí trên mâm
        public static int SlotOf(int pocket)
        {
            if (pocket == Roulette.StarPocket) return Slots - 1;
            int e = pocket / 5, n = pocket % 5;
            int q = ((n - 2 * e) % 5 + 5) % 5;
            return q * 5 + e;
        }

        // ---- hình học dùng chung cho mô phỏng, hình vẽ (ArtGen/Casino/dealer/d4/ve_banh_xe.py) và màn (RouletteScene) ----
        public const float RTrack = 0.868f;     // tâm bi khi tì vách đường chạy (vách ở 0,90, bi lún nhẹ vào vách cho gọn mắt)
        public const float RSlope = 0.80f;      // mép trong đường chạy, bắt đầu sườn dốc
        public const float RRotor = 0.70f;      // mép mâm xoay
        public const float RRing = 0.61f;       // ranh vòng số / vòng ô
        public const float RPocket = 0.555f;    // bi nằm trong ô ở bán kính này
        public const float RCone = 0.50f;       // chân nón giữa
        public const float BallR = 0.040f;      // bán kính bi (to hơn bi thật để đọc được trên điện thoại)
        public const int Diamonds = 8;
        public const float RDiamond = 0.765f, DiamondR = 0.020f;
        public const float FretH = 0.035f;      // vách ngăn ô cao chừng này

        public static double DiamondAngle(int i) => (i + 0.5) * Math.PI * 2 / Diamonds;

        // độ cao mặt lòng chảo tại bán kính r (lòng chảo nông để bi ở phía gần không khuất sau vành). Chiếu nghiêng:
        // x màn = R·x, y màn = R·(TiltK·y + TiltKz·(Height(r) + z + BallR)) (bi nằm TRÊN mặt nên tâm cao hơn mặt một bán kính).
        public const float TiltK = 0.6f, TiltKz = 0.8f;
        public const float RRimIn = 0.905f, HRim = 0.085f, HTrackOut = 0.07f, HTrackIn = 0.035f;

        public static float Height(float r)
        {
            if (r >= RRimIn) return HRim;
            if (r >= RSlope) return Lerp(HTrackIn, HTrackOut, (r - RSlope) / (RRimIn - RSlope));
            if (r >= RRotor) return Lerp(0f, HTrackIn, (r - RRotor) / (RSlope - RRotor));
            return 0f;
        }

        static float Lerp(float a, float b, float t) => a + (b - a) * (t < 0 ? 0 : t > 1 ? 1 : t);
    }

    public enum RlHitKind { Roll, Diamond, Fret, Land, Settle }

    public struct RlHit
    {
        public float t;          // giây từ lúc bi vào đường chạy
        public RlHitKind kind;
        public float power;      // 0..1 (để chỉnh âm lượng, rung)
    }

    // Đường đi đã ghi của một cú thả bi: mẫu đều Dt giây. Sau Duration bi nằm yên trong ô (đi theo mâm).
    public sealed class RlTrack
    {
        public const float Dt = 1f / 120f;
        public float[] x, y, z;      // bi trong hệ lòng chảo (đứng yên), z = độ nảy trên mặt
        public int count;
        public int slot;             // vị trí trên mâm bi nằm lại
        public float restAngle, restR;   // góc trong hệ mâm và bán kính lúc nằm yên
        public float duration;       // giây tới khi nằm yên hẳn
        public float capture;        // giây bi vào hẳn ô cuối (sau đó chỉ còn lắc trong ô): lúc biết kết quả
        public float dropTime;       // giây bi rời vách đường chạy
        public int laps10;           // số vòng bi chạy quanh lòng chảo × 10
        public int fretHits, diamondHits, hops;   // va vách ngăn, va mấu chắn, số lần nảy qua vách
        public double rotor0, omega0, omegaIdle, decay;   // mâm: góc lúc bi vào, Ω lúc đó, Ω nghỉ, hệ số tắt dần
        public float ballSpeed0;     // tốc độ góc bi lúc vào (rad/s, âm = theo chiều kim đồng hồ)
        public int tries;            // số cú thử để ra đúng ô
        public int shift;            // mâm lệch pha mấy ô so với góc dự tính (Plan, slack)
        public readonly List<RlHit> hits = new List<RlHit>();

        // góc mâm sau t giây kể từ lúc bi vào (Ω(t) = Ω nghỉ + (Ω0 − Ω nghỉ)·e^(−decay·t))
        public double Rotor(double t) => RouletteBall.RotorAngle(rotor0, omega0, omegaIdle, decay, t);

        public double RotorSpeed(double t) => RouletteBall.RotorSpeed(omega0, omegaIdle, decay, t);

        // vị trí bi tại t (nội suy giữa hai mẫu); quá Duration: bi nằm trong ô, quay theo mâm
        public void Sample(float t, out float bx, out float by, out float bz)
        {
            if (t >= duration || count == 0)
            {
                double a = restAngle + Rotor(t);
                bx = (float)(Math.Cos(a) * restR);
                by = (float)(Math.Sin(a) * restR);
                bz = 0;
                return;
            }
            if (t < 0) t = 0;
            float f = t / Dt;
            int i = (int)f;
            if (i >= count - 1) { bx = x[count - 1]; by = y[count - 1]; bz = z[count - 1]; return; }
            float u = f - i;
            bx = x[i] + (x[i + 1] - x[i]) * u;
            by = y[i] + (y[i + 1] - y[i]) * u;
            bz = z[i] + (z[i + 1] - z[i]) * u;
        }
    }

    public static class RouletteBall
    {
        // ---- số của mô phỏng (đo bằng ArtGen/Casino/dealer/d4/sim/chay.py: thời lượng, số vòng, số lần nảy) ----
        public const double EntryAngle = 40 * Math.PI / 180;   // bi vào đường chạy ở góc này (phải, phía xa)
        public const double OmegaSpin = 2.5, OmegaIdle = 0.32, RotorDecay = 0.20;   // mâm: rad/s lúc vừa quất, lúc nghỉ; tắt dần 1/s
        public const double BallMin = 10.4, BallMax = 12.6;    // tốc độ góc bi lúc thả (rad/s), chọn trong khoảng này
        const double RimA0 = 0.72, RimA2 = 0.0125;             // ma sát lăn + cản khí trên đường chạy: ω' = −(A0 + A2·ω²)
        const double SlopeG = 24.0, SlopeG2 = 34.0;            // lực kéo vào tâm trên đường chạy / trên sườn dốc
        const double Gz = 20.0;                                // trọng lực cho cú nảy (bán kính / s²)
        const double HopSpeed = 0.95;                          // nhanh hơn mức này (so với mâm) thì nảy qua vách, chậm hơn thì dội lại
        const double Sub = 1.0 / 480.0;
        const double MaxTime = 14.0;
        public static string LastFail;   // để dò: trạng thái cuối của cú mô phỏng không nằm yên

        public static double RotorAngle(double a0, double w0, double wIdle, double decay, double t) =>
            a0 + wIdle * t + (w0 - wIdle) * (1 - Math.Exp(-decay * t)) / decay;

        public static double RotorSpeed(double w0, double wIdle, double decay, double t) => wIdle + (w0 - wIdle) * Math.Exp(-decay * t);

        /// <summary>Tìm cú thả bi nằm đúng vị trí slot trên mâm. rotor0: góc mâm dự tính lúc bi vào đường chạy; omega0: tốc độ mâm lúc đó.
        /// Chỉ đổi lực thả (và hạt giống các cú nảy) trong khoảng tự nhiên. slack: cho phép mâm lệch pha tối đa chừng ấy Ô so với
        /// rotor0 (bánh xe đối xứng theo từng ô nên lùi mâm m ô thì bi nằm lệch đúng m ô; màn nắn pha mâm trong lúc mâm tăng tốc);
        /// đọc lại rotor0 trong kết quả. Luôn trả về một đường đi (xem tries).</summary>
        public static RlTrack Plan(int slot, double rotor0, double omega0, Rng rng, int slack = 2, int maxTries = 3000)
        {
            RlTrack spare = null;
            int n = RouletteWheel.Slots;
            for (int i = 1; i <= maxTries; i++)
            {
                double w = -rng.Range(BallMin, BallMax);
                uint seed = (uint)(rng.Next() * 4294967295.0) | 1u;
                var tr = Simulate(rotor0, omega0, w, seed, null);
                if (tr == null) continue;
                tr.tries = i;
                int m = ((tr.slot - slot) % n + n) % n;      // mâm phải lùi m ô (m > n / 2: tiến n − m ô)
                if (m > n / 2) m -= n;
                if (Math.Abs(m) > slack) continue;
                if (!Nice(tr) && i < 400)
                {
                    if (spare == null) spare = Shift(tr, m, slot);
                    continue;
                }
                return Shift(tr, m, slot);
            }
            if (spare != null) return spare;
            // không tới đây với bánh xe hiện tại (kiểm trong test); nếu có thì lấy một cú bất kỳ rồi lùi mâm cho khớp
            RlTrack any = null;
            for (uint s = 1; any == null && s < 50; s++) any = Simulate(rotor0, omega0, -(BallMin + BallMax) * 0.5, s, null);
            if (any == null) return null;
            int mm = ((any.slot - slot) % n + n) % n;
            any.tries = maxTries + 1;
            return Shift(any, mm > n / 2 ? mm - n : mm, slot);
        }

        // mâm lùi m ô (vách ngăn vẫn ở chỗ cũ nên đường đi y nguyên), bi nằm ở vị trí slot
        static RlTrack Shift(RlTrack tr, int m, int slot)
        {
            double shift = m * RouletteWheel.Step;
            tr.rotor0 += shift;
            tr.restAngle -= (float)shift;
            tr.slot = slot;
            tr.shift = m;
            return tr;
        }

        // nhịp đẹp: không quá ngắn / dài, có lách cách qua vách ngăn
        public static bool Nice(RlTrack t) => t.duration >= 4.6f && t.duration <= 9.5f && t.hops >= 2 && t.hops <= 9;

        /// <summary>Mô phỏng một cú thả (tất định theo tham số). null nếu bi không nằm yên trong thời hạn.</summary>
        public static RlTrack Simulate(double rotor0, double omega0, double ballW, uint seed, RlTrack reuse)
        {
            var rng = new Rng(seed);
            var tr = reuse ?? new RlTrack();
            int cap = (int)(MaxTime / RlTrack.Dt) + 8;
            if (tr.x == null || tr.x.Length < cap) { tr.x = new float[cap]; tr.y = new float[cap]; tr.z = new float[cap]; }
            tr.hits.Clear();
            tr.count = 0; tr.fretHits = 0; tr.diamondHits = 0; tr.hops = 0; tr.dropTime = -1; tr.laps10 = 0; tr.capture = 0; tr.shift = 0;
            tr.rotor0 = rotor0; tr.omega0 = omega0; tr.omegaIdle = OmegaIdle; tr.decay = RotorDecay; tr.ballSpeed0 = (float)ballW;

            const double Rt = RouletteWheel.RTrack, Rs = RouletteWheel.RSlope, Rr = RouletteWheel.RRotor, Rg = RouletteWheel.RRing,
                Rp = RouletteWheel.RPocket, Rc = RouletteWheel.RCone, Hf = RouletteWheel.FretH, step = RouletteWheel.Step;
            const int NS = RouletteWheel.Slots;
            // bi: vị trí, vận tốc (hệ đứng yên), độ nảy
            double px = Math.Cos(EntryAngle) * Rt, py = Math.Sin(EntryAngle) * Rt;
            double vx = -Math.Sin(EntryAngle) * ballW * Rt, vy = Math.Cos(EntryAngle) * ballW * Rt;
            double z = 0.05, vz = 0;
            double t = 0, swept = 0, lastTheta = EntryAngle;
            double quiet = 0;
            int sub = 0, rollTick = 0;
            bool onRim = true;
            int lastCell = -1;
            int nd = RouletteWheel.Diamonds;
            double dR = RouletteWheel.RDiamond, dHit = RouletteWheel.DiamondR + RouletteWheel.BallR * 0.75;

            while (t < MaxTime)
            {
                if (sub % 4 == 0)
                {
                    int k = tr.count++;
                    tr.x[k] = (float)px; tr.y[k] = (float)py; tr.z[k] = (float)z;
                }
                sub++;
                double r = Math.Sqrt(px * px + py * py);
                double ux = px / r, uy = py / r;          // hướng tâm ra
                double tx = -uy, ty = ux;                 // tiếp tuyến ngược chiều kim đồng hồ
                double phi = RotorAngle(rotor0, omega0, OmegaIdle, RotorDecay, t);
                double Om = RotorSpeed(omega0, OmegaIdle, RotorDecay, t);
                bool ground = z <= 1e-6;
                double ax = 0, ay = 0;

                if (ground)
                {
                    if (r > Rr)
                    {
                        // lòng chảo đứng yên: lực kéo vào tâm (dốc) + ma sát lăn, cản khí
                        double g = r >= Rs ? SlopeG : SlopeG2;
                        ax -= ux * g; ay -= uy * g;
                        double sp = Math.Sqrt(vx * vx + vy * vy);
                        if (sp > 1e-6)
                        {
                            double w = sp / r;
                            double dec = (RimA0 + RimA2 * w * w) * r;
                            ax -= vx / sp * dec; ay -= vy / sp * dec;
                        }
                    }
                    else
                    {
                        // mâm xoay: mặt mâm kéo bi theo, dốc đưa bi về vòng ô, nón giữa đẩy ra
                        double svx = tx * Om * r, svy = ty * Om * r;
                        double relS = Math.Abs((vx - svx) * tx + (vy - svy) * ty);
                        double mu = r >= Rg ? 1.4 : relS > HopSpeed ? 1.1 : 4.2;   // bi còn lăn nhanh qua vách thì mặt mâm chưa "bắt" được nó
                        ax -= (vx - svx) * mu; ay -= (vy - svy) * mu;
                        double rad;
                        if (r >= Rg) rad = -26.0;
                        else if (r >= Rc) rad = -260.0 * (r - Rp);
                        else rad = 40.0;
                        double vr = vx * ux + vy * uy;
                        if (r < Rg) rad -= 9.0 * vr;      // lòng ô hãm dao động hướng tâm
                        ax += ux * rad; ay += uy * rad;
                        // lòng ô hơi trũng: khi đã chậm, kéo nhẹ bi về giữa ô
                        if (r < Rg && r >= Rc - 0.02)
                        {
                            double beta = Wrap(Math.Atan2(py, px) - phi);
                            double c = (Math.Floor(beta / step) + 0.5) * step;
                            double rel = (vx - svx) * tx + (vy - svy) * ty;
                            if (Math.Abs(rel) < 0.9)
                            {
                                double pull = -120.0 * (beta - c) * r;
                                ax += tx * pull; ay += ty * pull;
                            }
                        }
                    }
                }
                vx += ax * Sub; vy += ay * Sub;
                px += vx * Sub; py += vy * Sub;
                if (!ground || vz != 0)
                {
                    vz -= Gz * Sub;
                    z += vz * Sub;
                    if (z <= 0)
                    {
                        z = 0;
                        double hit = -vz;
                        if (hit > 0.45)
                        {
                            vz = hit * 0.38;
                            tr.hits.Add(new RlHit { t = (float)t, kind = RlHitKind.Land, power = (float)Math.Min(1, hit / 2.2) });
                        }
                        else vz = 0;
                        // chạm mặt: mất bớt vận tốc so với mặt đang chạm
                        double rr = Math.Sqrt(px * px + py * py);
                        if (rr <= Rr)
                        {
                            double sx = -py / rr * Om * rr, sy = px / rr * Om * rr;
                            vx -= (vx - sx) * 0.16; vy -= (vy - sy) * 0.16;
                        }
                        else { vx *= 0.97; vy *= 0.97; }
                    }
                }
                t += Sub;

                r = Math.Sqrt(px * px + py * py);
                ux = px / r; uy = py / r; tx = -uy; ty = ux;
                // vách đường chạy: không ra ngoài được
                if (r > Rt)
                {
                    px = ux * Rt; py = uy * Rt;
                    double vr = vx * ux + vy * uy;
                    if (vr > 0) { vx -= ux * vr * 1.25; vy -= uy * vr * 1.25; }
                    r = Rt;
                }
                bool rimNow = r > Rt - 0.004;
                if (onRim && !rimNow && tr.dropTime < 0) tr.dropTime = (float)t;
                if (!rimNow) onRim = false;
                // đếm vòng + tiếng lăn (mỗi 1/8 vòng một nhịp khi còn trên đường chạy)
                double theta = Math.Atan2(py, px);
                double dth = theta - lastTheta;
                if (dth > Math.PI) dth -= Math.PI * 2; else if (dth < -Math.PI) dth += Math.PI * 2;
                lastTheta = theta;
                if (r > Rr) swept += Math.Abs(dth);
                int tick = (int)(swept / (Math.PI / 4));
                if (tick != rollTick)
                {
                    rollTick = tick;
                    if (r > Rs && z <= 1e-6)
                        tr.hits.Add(new RlHit { t = (float)t, kind = RlHitKind.Roll, power = (float)Math.Min(1, Math.Sqrt(vx * vx + vy * vy) / 11.0) });
                }

                // mấu chắn trên sườn dốc
                if (z < 0.05 && r > Rr - 0.01 && r < Rs + 0.03)
                {
                    for (int i = 0; i < nd; i++)
                    {
                        double a = RouletteWheel.DiamondAngle(i);
                        double dx = px - Math.Cos(a) * dR, dy = py - Math.Sin(a) * dR;
                        double d2 = dx * dx + dy * dy;
                        if (d2 >= dHit * dHit || d2 < 1e-12) continue;
                        double d = Math.Sqrt(d2), nx = dx / d, ny = dy / d;
                        double vn = vx * nx + vy * ny;
                        px += nx * (dHit - d); py += ny * (dHit - d);
                        if (vn < 0)
                        {
                            double e = 0.5 + 0.2 * rng.Next();
                            vx -= nx * vn * (1 + e); vy -= ny * vn * (1 + e);
                            // lệch ngẫu nhiên nhỏ theo tiếp tuyến của chỗ chạm + nảy lên
                            double j = (rng.Next() - 0.5) * 0.5 * -vn;
                            vx += -ny * j; vy += nx * j;
                            vz = Math.Max(vz, Math.Min(2.0, 0.5 * -vn + 0.25));
                            if (z < 1e-4) z = 1e-4;
                            tr.diamondHits++;
                            tr.hits.Add(new RlHit { t = (float)t, kind = RlHitKind.Diamond, power = (float)Math.Min(1, -vn / 4.0) });
                        }
                        break;
                    }
                }

                // vách ngăn ô trên mâm (góc mâm lấy ở thời điểm mới)
                r = Math.Sqrt(px * px + py * py);
                if (r < Rg + 0.02 && r > Rc - 0.03)
                {
                    double phiN = RotorAngle(rotor0, omega0, OmegaIdle, RotorDecay, t);
                    double beta = Wrap(Math.Atan2(py, px) - phiN);
                    int cell = (int)Math.Floor(beta / step) % NS;
                    if (lastCell >= 0 && cell != lastCell)
                    {
                        // hướng vượt: +1 = sang ô kế theo chiều ngược kim đồng hồ của mâm
                        int dir = (cell - lastCell + NS) % NS == 1 ? 1 : -1;
                        if (z < Hf)
                        {
                            ux = px / r; uy = py / r; tx = -uy; ty = ux;
                            double svx = tx * Om * r, svy = ty * Om * r;
                            double rel = (vx - svx) * tx + (vy - svy) * ty;      // vận tốc tiếp tuyến so với mâm
                            double sp = Math.Abs(rel);
                            if (sp > HopSpeed && rel * dir > 0)
                            {
                                // đập mép vách rồi nảy qua: mất bớt tốc, bật lên, lệch hướng tâm chút ít
                                double keep = 0.70 + 0.12 * rng.Next();
                                double nrel = rel * keep;
                                vx += tx * (nrel - rel); vy += ty * (nrel - rel);
                                vz = Math.Max(vz, Math.Min(1.1, 0.15 * sp + 0.2));
                                if (z < 1e-4) z = 1e-4;
                                double kick = (rng.Next() - 0.45) * 0.22 * sp;
                                vx += ux * kick; vy += uy * kick;
                                tr.hops++;
                                lastCell = cell;
                                tr.capture = (float)t;
                            }
                            else
                            {
                                // chậm: dội lại, ở yên trong ô cũ (đặt bi sát vách phía trong ô)
                                if (rel * dir > 0)
                                {
                                    double nrel = -rel * 0.32;
                                    vx += tx * (nrel - rel); vy += ty * (nrel - rel);
                                }
                                double edge = (dir > 0 ? lastCell + 1 : lastCell) * step;
                                double ang = edge - dir * 1.5e-3 + phiN;
                                px = Math.Cos(ang) * r; py = Math.Sin(ang) * r;
                            }
                            if (sp > 0.12)
                            {
                                tr.fretHits++;
                                tr.hits.Add(new RlHit { t = (float)t, kind = RlHitKind.Fret, power = (float)Math.Min(1, sp / 4.5) });
                            }
                        }
                        else
                        {
                            lastCell = cell;      // bay qua trên vách
                            tr.capture = (float)t;
                        }
                    }
                    else lastCell = cell;
                }
                else lastCell = -1;

                // nằm yên: trên mặt mâm, trong vòng ô, gần như đứng so với mâm
                if (z <= 1e-6 && vz == 0 && r < Rg && r > Rc)
                {
                    ux = px / r; uy = py / r; tx = -uy; ty = ux;
                    double rvx = vx - tx * Om * r, rvy = vy - ty * Om * r;
                    if (rvx * rvx + rvy * rvy < 0.03 * 0.03 && Math.Abs(r - Rp) < 0.012) quiet += Sub;
                    else quiet = 0;
                    if (quiet > 0.2)
                    {
                        // đường đi kết thúc đúng chỗ nằm yên để lúc chuyển sang "đi theo mâm" không giật
                        int k = tr.count < cap ? tr.count++ : cap - 1;
                        tr.x[k] = (float)px; tr.y[k] = (float)py; tr.z[k] = 0;
                        tr.duration = k * RlTrack.Dt;
                        double rest = Math.Atan2(py, px) - RotorAngle(rotor0, omega0, OmegaIdle, RotorDecay, tr.duration);
                        tr.slot = (int)Math.Floor(Wrap(Math.Atan2(py, px) - RotorAngle(rotor0, omega0, OmegaIdle, RotorDecay, t)) / step) % NS;
                        tr.restAngle = (float)rest;
                        tr.restR = (float)r;
                        tr.laps10 = (int)(swept / (Math.PI * 2) * 10);
                        if (tr.dropTime < 0) tr.dropTime = tr.duration;
                        if (tr.capture <= 0 || tr.capture > tr.duration) tr.capture = Math.Max(tr.dropTime, tr.duration - 0.5f);
                        tr.hits.Add(new RlHit { t = tr.duration, kind = RlHitKind.Settle, power = 1 });
                        return tr;
                    }
                }
                else quiet = 0;
            }
            LastFail = "r=" + Math.Sqrt(px * px + py * py).ToString("0.000") + " z=" + z.ToString("0.000") + " vz=" + vz.ToString("0.00") +
                       " v=" + Math.Sqrt(vx * vx + vy * vy).ToString("0.00") + " fret=" + tr.fretHits;
            return null;
        }

        static double Wrap(double a)
        {
            a %= Math.PI * 2;
            return a < 0 ? a + Math.PI * 2 : a;
        }
    }
}
