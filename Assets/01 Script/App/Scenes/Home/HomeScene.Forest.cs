// Rừng màn Nhà (người dùng 2026-11-23: "việc dọn rừng sẽ tặng cho người chơi 1 ít bi ... hiện số bi ở trên đầu rừng ... khi mở làm kiểu
// các cây bay lên trời (squash and stretch) ... làm thêm gió thổi cho cây đung đưa nhẹ nhàng, thi thoảng cây lắc lắc"). Học Clash of
// Critters: ô đất khoá có bong bóng trên đầu (pbsc_homestead_expand_bubble: icon 3 viên bi + số bi thưởng, ô xẻng giá mở); mở xong thì
// bung bụi + lá (pbfx_camp_expand_3x3: 9 cụm khói sprite bay lên, đời 0,4–0,6 s; 3 lá to bắn 5–7 đv/s rơi theo trọng lực, 5 lá nhỏ lượn).
// - Bong bóng bi (ForestBubbles, gọi mỗi giây từ Labels): ô rừng dọn được hoặc chỉ thiếu gỗ / quặng / thợ (LotTappable) hiện "icon bi
//   +N" (N = home.rings[].balls của vòng) trên tán cây giữa ô; chạm bong bóng = chạm ô rừng. Đang dọn: chỉ nhãn giờ còn.
// - Dọn xong (RenderForests → LaunchForest): cây trong khung nhìn bay lên trời lần lượt từ giữa ô ra, mỗi cây nén xuống (0,13 s) → bật
//   giãn dài (0,09 s) → vọt lên nhanh dần, nghiêng nhẹ, mờ dần; gốc mỗi cây bung một cụm khói kem + bụi, cây to văng lá. Bi bay từ trên
//   đầu ô lên chip bi (ReportCleared → FlyBalls). Không quầng, không cộng sáng.
// - Gió (SwayTrees): cây trong khung nhìn nghiêng quanh gốc 0–2,4 độ, ngả theo chiều gió của lá bay (HomeWind: sang trái), cơn gió là
//   sóng chạy ngang bản đồ; thỉnh thoảng một cây to lắc mạnh rồi êm dần (0,9 s), rụng vài lá, đôi khi có chim vụt ra.
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed partial class HomeScene
    {
        // ---------- bong bóng bi trên ô rừng ----------

        // mốc ô rừng cao tới ngọn cây cao nhất quanh giữa ô (bong bóng neo ở đỉnh mốc)
        void FitMarker(int lot)
        {
            if (!forests.TryGetValue(lot, out var mk) || !mk || !forestTrees.TryGetValue(lot, out var list)) return;
            var c = C;
            var (i, j) = Home.LotIJ(c, lot);
            var mid = CellTop(i * c.lot + c.lot / 2f, j * c.lot + c.lot / 2f);
            float h = 150;
            foreach (var (img, _) in list)
            {
                if (!img) continue;
                var rt = img.rectTransform;
                var ap = rt.anchoredPosition;
                if (Mathf.Abs(ap.x - mid.x) > 160 || Mathf.Abs(-ap.y - mid.y) > 110) continue;
                float top = -ap.y - (1 - rt.pivot.y) * rt.sizeDelta.y; // y bản đồ của ngọn (y xuống)
                h = Mathf.Max(h, mid.y - top);
            }
            mk.Place(null, new Vector2(1, h + 6), new Vector2(0.5f, 0), mid);
            mk.Img.enabled = false;
        }

        void ForestBubbles(double now)
        {
            var h = S.home;
            foreach (var kv in forests)
            {
                var mk = kv.Value;
                if (!mk) continue;
                if (h.clearing.TryGetValue(kv.Key, out var until))
                {
                    mk.Label(Loc.T("Dọn ") + Clock((until - now) / 60000));
                    mk.Bubble(null);
                    continue;
                }
                mk.Label(null);
                int balls = Home.RingOf(C, kv.Key)?.balls ?? 0;
                if (balls > 0 && LotTappable(kv.Key))
                {
                    mk.Bubble(Icon("ball"), "+" + TopBars.Fmt(balls));
                    mk.Fill(-1);
                }
                else mk.Bubble(null);
            }
        }

        // chạm bong bóng bi: như chạm ô rừng (OnTap)
        void TapLot(int lot)
        {
            if (mode != Mode.Normal || S.home.lots.Contains(lot) || !LotTappable(lot)) return;
            selLot = lot;
            selBuilding = -1;
            App.Audio.Play("click");
            selPop = true;
            PickLot(lot);
            RefreshPanel();
        }

        // chỗ bi thưởng bay ra (trên đầu ô rừng vừa dọn, chỉ ô đang thấy trên màn) và bong bóng nảy tắt
        List<(HomeObject o, Vector3 at, int n)> ClearedRewardFrom(List<int> lots)
        {
            var from = new List<(HomeObject o, Vector3 at, int n)>();
            var cam = PokiCanvas.UiCamera;
            foreach (int lot in lots)
            {
                int balls = Home.RingOf(C, lot)?.balls ?? 0;
                if (balls <= 0 || !forests.TryGetValue(lot, out var mk) || !mk) continue;
                var at = mk.BubbleWorld();
                var scr = RectTransformUtility.WorldToScreenPoint(cam, at);
                if (scr.x < 0 || scr.y < 0 || scr.x > Screen.width || scr.y > Screen.height) continue;
                mk.PopBubble();
                from.Add((mk, at, balls));
            }
            return from;
        }

        // ---------- cây bay lên trời khi dọn xong ----------

        sealed class FlyTree
        {
            public Image img;
            public RectTransform rt;
            public Vector2 start;  // anchoredPosition lúc rời đất (lớp hạt, neo trên trái: = (x, −y bản đồ))
            public float t, delay, sx, vx, spin, h;
            public bool launched;
        }

        readonly List<FlyTree> flyTrees = new List<FlyTree>();
        HomeWind wind;

        // điểm bản đồ (gốc cây) có trong khung nhìn không; up: phần hình nhô lên trên gốc (px bản đồ)
        bool InView(Vector2 m, float up, float margin = 120)
        {
            if (!landView || !landView.On) return false;
            var v = landView.ToView(m);
            var size = landView.ViewSize;
            return v.x > -margin && v.x < size.x + margin && v.y > -margin && v.y < size.y + up * landView.Zoom + margin;
        }

        void LaunchForest(int lot, List<(Image img, float depth)> trees)
        {
            var c = C;
            var (i, j) = Home.LotIJ(c, lot);
            var mid = CellTop(i * c.lot + c.lot / 2f, j * c.lot + c.lot / 2f);
            float far = c.lot * CW * 0.5f;
            int n = 0;
            foreach (var (img, _) in trees)
            {
                if (!img) continue;
                var rt = img.rectTransform;
                var ap = rt.anchoredPosition;
                var foot = new Vector2(ap.x, -ap.y);
                if (!fxLayer || !InView(foot, rt.sizeDelta.y))
                {
                    Destroy(img.gameObject);
                    continue;
                }
                rt.SetParent(fxLayer, true); // trên công trình, quái; vẫn dưới mây và lớp nhuộm ngày đêm
                rt.SetAsLastSibling();
                rt.localRotation = Quaternion.identity;
                float d = (foot - mid).magnitude / Mathf.Max(1, far);
                flyTrees.Add(new FlyTree
                {
                    img = img, rt = rt, start = rt.anchoredPosition, sx = Mathf.Sign(rt.localScale.x), h = rt.sizeDelta.y,
                    delay = Mathf.Clamp01(d) * 0.42f + UnityEngine.Random.Range(0f, 0.12f),
                    vx = UnityEngine.Random.Range(-55f, 55f), spin = UnityEngine.Random.Range(-26f, 26f),
                });
                n++;
            }
            if (n == 0) return;
            App.Audio.Play("whoosh");
            Haptics.Play(Haptic.CardTap);
        }

        static float EaseOut(float x) => 1 - (1 - x) * (1 - x);

        void TickFlying(float dt)
        {
            const float Squash = 0.13f, Snap = 0.09f, Life = 0.85f;
            for (int k = flyTrees.Count - 1; k >= 0; k--)
            {
                var f = flyTrees[k];
                if (!f.rt)
                {
                    flyTrees.RemoveAt(k);
                    continue;
                }
                f.t += dt;
                float t = f.t - f.delay;
                if (t < 0) continue;
                float sx, sy, x = 0, y = 0, rot = 0, a = 1;
                if (t < Squash)
                {
                    // lấy đà: nén xuống quanh gốc, bè ra
                    float e = EaseOut(t / Squash);
                    sy = 1 - 0.3f * e;
                    sx = 1 + 0.22f * e;
                }
                else
                {
                    float u = t - Squash;
                    if (!f.launched)
                    {
                        f.launched = true;
                        TreePuff(f);
                    }
                    if (u > Life)
                    {
                        Destroy(f.rt.gameObject);
                        flyTrees.RemoveAt(k);
                        continue;
                    }
                    // bật: từ nén sang giãn dài trong Snap giây, rồi dịu về hơi dài trong lúc bay (tốc độ kéo dài hình)
                    float e = EaseOut(Mathf.Clamp01(u / Snap));
                    float relax = Mathf.Clamp01((u - Snap) / 0.35f);
                    sy = Mathf.Lerp(Mathf.Lerp(0.7f, 1.34f, e), 1.12f, relax);
                    sx = Mathf.Lerp(Mathf.Lerp(1.22f, 0.78f, e), 0.9f, relax);
                    y = 700 * u + 1300 * u * u; // vọt lên nhanh dần (px bản đồ)
                    x = f.vx * u;
                    rot = f.spin * u * 1.4f;
                    a = 1 - Mathf.Clamp01((u - 0.42f) / 0.36f);
                }
                f.rt.localScale = new Vector3(f.sx * sx, sy, 1);
                f.rt.anchoredPosition = f.start + new Vector2(x, y);
                f.rt.localRotation = Quaternion.Euler(0, 0, rot);
                var col = Color.Lerp(LockedTint, Color.white, Mathf.Clamp01(t / 0.2f)); // rời đất: hết tô tối của ô khoá
                col.a = a;
                f.img.color = col;
            }
        }

        // gốc cây vừa rời đất: cụm khói kem + bụi đất bay lên rồi tan; cây to văng 1–2 lá
        void TreePuff(FlyTree f)
        {
            var foot = ToLocal(new Vector2(f.start.x, -f.start.y));
            bool big = f.h > 120;
            float R(float lo, float hi) => UnityEngine.Random.Range(lo, hi);
            // cụm to, vừa, nhỏ lệch nhau (khói đều cỡ đọc thành hạt rải); đồ nhỏ (gốc cây, khúc gỗ, bụi) chỉ 40% có khói
            float k = Mathf.Clamp(f.h / 220f, 0.55f, 1.2f) * R(0.75f, 1.35f);
            if (big || UnityEngine.Random.value < 0.4f)
                Fx(Prop(FarmProp.Smoke), new Color(1f, 0.98f, 0.94f, 0.95f), foot + new Vector2(R(-18, 18), 8), new Vector2(R(-45, 45), R(30, 75)), -40,
                    R(0.7f, 1f), 64 * k, 150 * k, R(-40, 40), true, 1.6f);
            if (!big) return;
            if (UnityEngine.Random.value < 0.5f)
                Fx(Prop(FarmProp.Dust), new Color(1f, 1f, 1f, 0.9f), foot + new Vector2(R(-34, 34), 2), new Vector2(R(-100, 100), R(10, 45)), -20,
                    R(0.5f, 0.7f), 40 * k, 92 * k, R(-60, 60), true, 2.2f);
            if (UnityEngine.Random.value < 0.6f) Leaf(foot + new Vector2(R(-20, 20), f.h * 0.55f), 1);
        }

        // lá văng / rụng (ảnh lá của gió)
        void Leaf(Vector2 at, int n, bool gentle = false)
        {
            if (!wind && fxLayer) wind = fxLayer.GetComponentInChildren<HomeWind>(true);
            for (int i = 0; i < n; i++)
            {
                var sp = wind ? wind.Leaf(UnityEngine.Random.Range(0, 3)) : null; // 3 ảnh lá đầu (cánh hoa là ảnh thứ 4)
                if (!sp) return;
                if (gentle) // rụng: lả xuống, trôi theo gió sang trái
                    Fx(sp, Color.white, at + UnityEngine.Random.insideUnitCircle * 30, new Vector2(UnityEngine.Random.Range(-70f, -20f), UnityEngine.Random.Range(-10f, 30f)),
                        90, UnityEngine.Random.Range(1.4f, 1.9f), 24, 22, UnityEngine.Random.Range(-160f, 160f), false, 1.4f);
                else
                    Fx(sp, Color.white, at, new Vector2(UnityEngine.Random.Range(-240f, 240f), UnityEngine.Random.Range(140f, 320f)), 650,
                        UnityEngine.Random.Range(0.8f, 1.1f), 26, 22, UnityEngine.Random.Range(-420f, 420f), false, 1f);
            }
        }

        // ---------- gió lay cây ----------

        float swayClock;
        Image shakeImg;
        float shakeT = 9, shakeWait = 2.5f;

        static float Hash01(Vector2 m) => Mathf.Repeat(Mathf.Sin(m.x * 0.1291f + m.y * 0.7823f) * 437.585f, 1f);

        void SwayTrees(float dt)
        {
            if (!landView || !landView.On) return;
            swayClock += dt;
            shakeT += dt;
            float t = swayClock;
            bool pickNow = (shakeWait -= dt) <= 0;
            Image pick = null;
            int seen = 0;
            var size = landView.ViewSize;
            float z = landView.Zoom;
            foreach (var kv in forestTrees)
            {
                var list = kv.Value;
                if (list.Count == 0) continue;
                // cả ô xa khung nhìn thì bỏ qua (ô rừng rộng ~1.150 px bản đồ)
                if (kv.Key != RimKey && list[0].img)
                {
                    var v0 = landView.ToView(new Vector2(list[0].img.rectTransform.anchoredPosition.x, -list[0].img.rectTransform.anchoredPosition.y));
                    float pad = 1500 * z;
                    if (v0.x < -pad || v0.x > size.x + pad || v0.y < -pad || v0.y > size.y + pad) continue;
                }
                foreach (var (img, _) in list)
                {
                    if (!img) continue;
                    var rt = img.rectTransform;
                    var ap = rt.anchoredPosition;
                    var m = new Vector2(ap.x, -ap.y);
                    var v = landView.ToView(m);
                    if (v.x < -220 || v.x > size.x + 220 || v.y < -80 || v.y > size.y + rt.sizeDelta.y * z + 80) continue;
                    float ph = Hash01(m) * 6.2832f;
                    // cơn gió là sóng chạy ngang bản đồ theo chiều gió (sang trái); cây ngả theo gió, lắc qua lại quanh chỗ ngả
                    float gust = 0.55f + 0.45f * Mathf.Sin(t * 0.55f + m.x * 0.0016f + m.y * 0.0007f);
                    float ang = gust * (0.8f + 1.2f * Mathf.Sin(t * 1.6f * (0.85f + 0.3f * Hash01(m * 1.7f)) + ph)) + 0.35f * Mathf.Sin(t * 2.9f + ph * 1.7f);
                    if (img == shakeImg && shakeT < 1f) ang += 6f * Mathf.Sin(shakeT * 24f) * Mathf.Exp(-shakeT * 4.2f);
                    rt.localRotation = Quaternion.Euler(0, 0, ang);
                    if (pickNow && rt.sizeDelta.y > 140 && UnityEngine.Random.Range(0, ++seen) == 0) pick = img;
                }
            }
            if (!pickNow) return;
            shakeWait = UnityEngine.Random.Range(1.6f, 4.2f);
            if (!pick) return;
            shakeImg = pick;
            shakeT = 0;
            // rụng vài lá từ tán, đôi khi một con chim vụt ra
            var prt = pick.rectTransform;
            var foot = new Vector2(prt.anchoredPosition.x, -prt.anchoredPosition.y);
            var canopy = foot - new Vector2(0, prt.sizeDelta.y * 0.62f);
            Leaf(ToLocal(canopy), UnityEngine.Random.Range(1, 4), true);
            if (UnityEngine.Random.value < 0.3f) BirdFrom(canopy);
        }
    }
}
