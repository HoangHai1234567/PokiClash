// Icon thưởng bay về ô chứa (người dùng 2026-11-27: "từ giờ khi thu thập được cái gì thì biểu tượng của cái đấy sẽ move vào phần chứa nó.
// Ví dụ ở đây nhận được kinh nghiệm thì kinh nghiệm tỏa ra move đến icon kinh nghiệm ở trên, thu thập được mảnh tướng hay shard thì chui
// vào ô heroes").
// - Nhịp: từ chỗ nhận, vài icon (3–10 theo số lượng) toả ra (bung nhanh rồi hãm, xoay nhẹ, bật to), khựng một nhịp so le, rồi bay cong về
//   ô chứa (tăng tốc dần, nhỏ lại khi tới). Mỗi icon tới thì ô chứa nảy, tiếng "pick" cao dần; icon cuối tới thì rung nhẹ.
// - Ô chứa (Target): kinh nghiệm → vòng cấp của thanh trên (thanh sảnh hoặc ô cấp của thanh màn con; máy bi: thanh kinh nghiệm của máy);
//   bi → chip bi (máy bi, đảo Casino) hoặc nút giữa của kệ sảnh chung; mảnh tướng, đá tiến hóa, đá tinh → ô Tướng; bản sao thẻ → Sổ thẻ;
//   trứng, vé chọn tướng, quyền lợi → Cửa hàng; đá tiềm năng → thẻ Hang Tiềm Năng. Ô chứa đang không hiện (màn bên trong, màn trận) thì
//   icon bay về hướng chỗ ô chứa thường nằm (kinh nghiệm góc trái trên, bi góc phải trên, Cửa hàng / Tướng / Sổ thẻ chỗ các ô ở đáy) rồi
//   mờ dần.
// - Vẽ trên mọi thứ (cả hộp thoại): lớp riêng là con của thanh trên (khung app, sống qua mọi màn) có Canvas đè thứ tự vẽ (Order).
// Nơi gọi: hộp nhận quà ChestDialog (mọi ô thưởng khi bấm Nhận / chạm ra ngoài), nút Nhận mảnh của bảng AFK, hộp rương mốc đảo, hộp
// kết quả trận (cả Hầm đấu; đoán ô chứa theo nội dung ô: RewardTile.Dest), màn quà hôm nay, các trò đảo Casino (bi thắng ván ở lều Đêm Bài
// / Vòng Xoay / Máy Quả và quà kèm, bán cá ở Bến câu và Chợ đen, món mua và đổi thẻ ở Chợ đen, bi về đích và quà tuần ở Trường đua, quà
// việc ở Quán trọ; trang trí mua ở Chợ đen bay về ô Nhà). Thưởng đã cộng vào bản lưu trước khi bay (số
// trên ô chứa đổi ngay, icon bay chỉ là cảm giác).
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class RewardFly : MonoBehaviour
    {
        public enum To { None, Level, Balls, Heroes, Cards, Shop, Cave, Home }

        const int Order = 150; // trên hộp thoại và các màn mở thưởng riêng (quà hôm nay, nở trứng...), dưới lớp hướng dẫn (500)
        const float Size = 72;

        static RewardFly layer;

        sealed class Bit
        {
            public Image img;
            public RectTransform rt;
            public Vector2 from, burst, ctrl, to;
            public float t, burstT, wait, flyT, spin, rot0;
            public RectTransform target;
            public bool last, live;
            public int no;
        }

        readonly List<Bit> bits = new List<Bit>();
        RectTransform rect;
        int landedInRun;

        // ---------- gọi từ ngoài ----------

        // ô chứa của một loại thưởng (RewardKind)
        public static To Of(RewardKind k) =>
            k == RewardKind.Exp ? To.Level : k == RewardKind.Balls ? To.Balls :
            k == RewardKind.Card || k == RewardKind.LegendCopies ? To.Cards :
            k == RewardKind.Stones ? To.Cave :
            k == RewardKind.Egg || k == RewardKind.Ticket || k == RewardKind.Perk || k == RewardKind.HeroChest || k == RewardKind.GoldChest ? To.Shop :
            k == RewardKind.Shards || k == RewardKind.Hero || k == RewardKind.EvoStones || k == RewardKind.Crystal ? To.Heroes :
            k == RewardKind.Deco ? To.Home :
            To.None; // mồi câu: không có ô chứa

        // icon của một món thưởng (Reward)
        static Sprite IconOf(Reward r)
        {
            var a = App.Art;
            if (!a) return null;
            switch (r.k)
            {
                case RewardKind.Exp: return a.Icon("exp");
                case RewardKind.Balls: return a.Icon("ball");
                case RewardKind.Shards: case RewardKind.Hero: case RewardKind.Crystal: return a.Icon("shard");
                case RewardKind.Stones: case RewardKind.EvoStones: return a.Icon("rock");
                case RewardKind.Deco: return a.Icon("house");
                case RewardKind.Card: case RewardKind.LegendCopies:
                {
                    var cd = r.drop != null && App.Data != null ? App.Data.Card(r.drop.card) : null;
                    return cd != null ? a.Icon(cd.icon) : a.Icon("cards");
                }
                default: return a.Icon("chest");
            }
        }

        // bi (thắng ván, bán cá, về đích...) từ điểm thế giới from về chip bi
        public static void Balls(int n, Vector3 fromWorld, float delay = 0)
        {
            if (n > 0) Send(To.Balls, App.Art ? App.Art.Icon("ball") : null, fromWorld, n, delay);
        }

        // một danh sách thưởng (quà việc, quà tuần, món mua...): gộp theo ô chứa, mỗi ô chứa một loạt so le
        public static void Rewards(IList<Reward> list, Vector3 fromWorld, float delay = 0)
        {
            if (list == null || list.Count == 0) return;
            var order = new List<To>();
            var sum = new Dictionary<To, (Sprite icon, int n)>();
            foreach (var r in list)
            {
                var to = Of(r.k);
                if (to == To.None) continue;
                int n = r.k == RewardKind.Shards && r.res != null ? r.res.n : Mathf.Max(1, r.n);
                if (sum.TryGetValue(to, out var had)) sum[to] = (had.icon, had.n + n);
                else
                {
                    sum[to] = (IconOf(r), n);
                    order.Add(to);
                }
            }
            for (int i = 0; i < order.Count; i++) Send(order[i], sum[order[i]].icon, fromWorld, sum[order[i]].n, delay + 0.1f * i);
        }

        // ô chứa của một món cửa hàng (ShopItem.k)
        public static To OfShop(string k) =>
            k == "balls" ? To.Balls : k == "shards" || k == "evo" || k == "crystal" ? To.Heroes : k == "copies" ? To.Cards :
            k == "stones" ? To.Cave : string.IsNullOrEmpty(k) ? To.None : To.Shop;

        // icon chuẩn của loại món (bi, mảnh, đá); null thì nơi gọi dùng hình của món
        public static Sprite IconFor(string k)
        {
            if (!App.Art) return null;
            return k == "balls" ? App.Art.Icon("ball") : k == "shards" ? App.Art.Icon("shard") : k == "stones" || k == "evo" ? App.Art.Icon("rock") : null;
        }

        // bay amount (định số icon) từ điểm thế giới from về ô chứa của to; delay: chờ trước khi toả
        public static void Send(To to, Sprite icon, Vector3 fromWorld, int amount, float delay = 0)
        {
            if (to == To.None || !icon) return;
            var l = Layer();
            if (!l) return;
            l.Launch(to, icon, fromWorld, amount, delay);
        }

        // ô thưởng của hộp nhận quà: mỗi ô một loạt, so le nhau
        public static void FromTiles(IList<RewardTile> tiles, IList<To> dest, IList<int> amounts)
        {
            if (tiles == null || dest == null) return;
            for (int i = 0; i < tiles.Count && i < dest.Count; i++)
            {
                var t = tiles[i];
                if (!t || dest[i] == To.None) continue;
                var icon = t.FlyIcon;
                if (!icon) continue;
                int n = amounts != null && i < amounts.Count ? amounts[i] : 1;
                Send(dest[i], icon, t.FlyFrom, n, i * 0.08f);
            }
        }

        // ô chứa đang hiện cho loại thưởng; null nếu không có chỗ (màn bên trong)
        public static RectTransform Target(To to)
        {
            var dock = LobbyDock.I;
            bool lobby = dock && dock.Visible;
            RectTransform Btn(int i)
            {
                if (!lobby || dock.Bottom == null || i >= dock.Bottom.Length) return null;
                var b = dock.Bottom[i].button;
                return b && b.gameObject.activeInHierarchy ? b.Rect : null;
            }
            switch (to)
            {
                case To.Level:
                {
                    var r = App.Bars ? App.Bars.LevelRing : null;
                    if (r) return r;
                    var bar = FindAnyObjectByType<MachineExpBar>();
                    return bar && bar.isActiveAndEnabled ? (RectTransform)bar.transform : null;
                }
                case To.Balls:
                {
                    var chip = App.Bars ? App.Bars.BallChip : null;
                    return chip && chip.gameObject.activeInHierarchy ? chip : Btn(2);
                }
                case To.Heroes: return Btn(1);
                case To.Cards: return Btn(3);
                case To.Shop: return Btn(0);
                case To.Home: return Btn(4);
                case To.Cave:
                    if (lobby && dock.Buildings != null)
                        foreach (var b in dock.Buildings)
                            if (b && b.gameObject.activeInHierarchy && b.name.Contains("Hang"))
                                return (RectTransform)b.transform;
                    return Btn(1);
            }
            return null;
        }

        // ---------- lớp bay ----------

        static RewardFly Layer()
        {
            if (layer) return layer;
            var host = App.Bars ? App.Bars.FlyLayer : null;
            if (!host) return null;
            var go = new GameObject("bay_ve_o_chua", typeof(RectTransform), typeof(Canvas));
            go.layer = host.gameObject.layer;
            var rt = (RectTransform)go.transform;
            rt.SetParent(host, false);
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            var cv = go.GetComponent<Canvas>();
            cv.overrideSorting = true;
            cv.sortingOrder = Order;
            layer = go.AddComponent<RewardFly>();
            layer.rect = rt;
            return layer;
        }

        Vector2 Local(Vector3 world)
        {
            var cam = PokiCanvas.UiCamera;
            var scr = RectTransformUtility.WorldToScreenPoint(cam, world);
            RectTransformUtility.ScreenPointToLocalPointInRectangle(rect, scr, cam, out var l);
            return l;
        }

        Bit Take()
        {
            foreach (var b in bits)
                if (!b.live)
                    return b;
            var img = new GameObject("icon", typeof(RectTransform), typeof(Image)).GetComponent<Image>();
            img.transform.SetParent(transform, false);
            img.raycastTarget = false;
            img.preserveAspect = true;
            var bit = new Bit { img = img, rt = img.rectTransform };
            bits.Add(bit);
            return bit;
        }

        void Launch(To to, Sprite icon, Vector3 fromWorld, int amount, float delay)
        {
            var target = Target(to);
            var from = Local(fromWorld);
            var r = rect.rect;
            // không có ô chứa: bay về hướng chỗ ô chứa thường nằm rồi mờ
            Vector2 to0 = target ? Local(target.TransformPoint(target.rect.center)) : Fallback(to, r, from);
            int n = Mathf.Clamp(Mathf.CeilToInt(Mathf.Sqrt(Mathf.Max(1, amount)) * 1.6f), 3, 10);
            for (int i = 0; i < n; i++)
            {
                var b = Take();
                b.live = true;
                b.no = i;
                b.last = i == n - 1;
                b.target = target;
                b.from = from;
                float a = (i / (float)n) * Mathf.PI * 2 + UnityEngine.Random.Range(-0.4f, 0.4f);
                b.burst = from + new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * UnityEngine.Random.Range(90f, 190f);
                b.to = to0;
                // điểm uốn: lệch sang một bên đường bay cho đường cong
                var mid = (b.burst + to0) * 0.5f;
                var dir = (to0 - b.burst).normalized;
                b.ctrl = mid + new Vector2(-dir.y, dir.x) * UnityEngine.Random.Range(-160f, 160f);
                b.t = -delay;
                b.burstT = 0.26f;
                b.wait = 0.06f + i * 0.045f;
                b.flyT = UnityEngine.Random.Range(0.5f, 0.62f);
                b.spin = UnityEngine.Random.Range(-260f, 260f);
                b.rot0 = UnityEngine.Random.Range(-18f, 18f);
                Theme.SetSprite(b.img, icon);
                b.img.color = Color.white;
                b.rt.sizeDelta = new Vector2(Size, Size);
                b.rt.anchoredPosition = from;
                b.rt.localScale = Vector3.zero;
                b.img.gameObject.SetActive(true);
                b.rt.SetAsLastSibling();
            }
            landedInRun = 0;
        }

        // chỗ ô chứa thường nằm (thanh trên, kệ sảnh chung), trong lớp bay
        static Vector2 Fallback(To to, Rect r, Vector2 from)
        {
            switch (to)
            {
                case To.Level: return new Vector2(r.xMin + 110, r.yMax - 90);
                case To.Balls: return new Vector2(r.xMax - 170, r.yMax - 90);
                case To.Shop: return new Vector2(-412, r.yMin + 110);
                case To.Heroes: return new Vector2(-214, r.yMin + 110);
                case To.Cards: return new Vector2(214, r.yMin + 110);
                case To.Home: return new Vector2(412, r.yMin + 110);
                case To.Cave: return new Vector2(r.xMax - 90, r.yMax - 330);
            }
            return new Vector2(from.x * 0.6f, r.yMax + 60);
        }

        void Update()
        {
            float dt = Time.unscaledDeltaTime;
            foreach (var b in bits)
            {
                if (!b.live) continue;
                b.t += dt;
                if (b.t < 0) continue;
                float t = b.t;
                if (t < b.burstT)
                {
                    // toả: bung nhanh rồi hãm, bật to
                    float u = t / b.burstT;
                    float e = 1 - (1 - u) * (1 - u) * (1 - u);
                    b.rt.anchoredPosition = Vector2.Lerp(b.from, b.burst, e);
                    float s = u < 0.6f ? Mathf.Lerp(0, 1.15f, u / 0.6f) : Mathf.Lerp(1.15f, 1, (u - 0.6f) / 0.4f);
                    b.rt.localScale = Vector3.one * s;
                    b.rt.localEulerAngles = new Vector3(0, 0, b.rot0 + b.spin * t * 0.4f);
                    continue;
                }
                t -= b.burstT;
                if (t < b.wait)
                {
                    // khựng: lơ lửng nhẹ
                    b.rt.anchoredPosition = b.burst + new Vector2(0, 6 * Mathf.Sin(t * 14));
                    continue;
                }
                t -= b.wait;
                float k = Mathf.Clamp01(t / b.flyT);
                float q = k * k * (1.6f - 0.6f * k); // tăng tốc dần
                // ô chứa có thể dời (cuộn, thanh trượt): bám chỗ hiện tại
                if (b.target) b.to = Local(b.target.TransformPoint(b.target.rect.center));
                var p0 = Vector2.Lerp(b.burst, b.ctrl, q);
                var p1 = Vector2.Lerp(b.ctrl, b.to, q);
                b.rt.anchoredPosition = Vector2.Lerp(p0, p1, q);
                b.rt.localScale = Vector3.one * Mathf.Lerp(1, 0.55f, q);
                b.rt.localEulerAngles = new Vector3(0, 0, b.rot0 + b.spin * (b.burstT * 0.4f + t));
                if (!b.target) b.img.color = new Color(1, 1, 1, Mathf.Clamp01((1 - q) * 2.5f));
                if (k >= 1) Land(b);
            }
        }

        void Land(Bit b)
        {
            b.live = false;
            b.img.gameObject.SetActive(false);
            if (!b.target) return;
            UiMotion.Of(b.target).Punch(0.3f);
            landedInRun++;
            App.Audio?.Play("pick", 0.4f, 1.05f + Mathf.Min(landedInRun, 12) * 0.035f);
            if (b.last) Haptics.Play(Haptic.UiTap);
        }
    }
}
