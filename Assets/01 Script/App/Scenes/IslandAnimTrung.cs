// Easter egg bản đồ sảnh (người dùng 2026-11-23: "bố cục scene các đảo này vẫn hơi tĩnh ... thêm các easter egg vào để người chơi khám
// phá"; ArtGen/Islands/sanh_moi/trung_sanh/trung_sanh.py ghi các món "e_*" vào khoá world_map của island_anim.json; hình sinh vật vẽ
// tay cùng nét bản đồ: trung_sanh/to_sinh_vat_1.png cắt ra Islands/Anim/anim_ca, ca_vang, cua, ca_voi, duoi_ca_voi, voi_phun, chai,
// da_lua, rua). Phần của IslandAnim. Cảnh sống tự chạy và 8 bí mật chạm vào mới lộ:
//  0 núi lửa (e_nui): tự phun đá dung nham mỗi 40–70 s; chạm miệng núi thì phun ngay;
//  1 hải đăng (e_den): chạm thì đèn bật, chùm sáng quét 2,5 vòng;
//  2 xác tàu (e_tau): lão cua thỉnh thoảng ló ra; chạm thì cua bò ra bãi cát vẫy càng rồi bò về;
//  3 xoáy nước (e_xoay): chạm thì xoáy nhả một chai thư dập dềnh gần đó; chạm chai đọc thư (thư gợi ý các bí mật khác);
//  4 san hô (e_sanho): chạm thì đàn cá nhỏ túa ra;
//  5 cá voi (e_voi): nổi lên phun nước, lặn, vẫy đuôi theo chu kỳ 30–45 s; chạm lúc đang nổi;
//  6 cá vàng (e_ca): cá nhảy khỏi mặt biển rải rác; thỉnh thoảng là cá vàng, chạm kịp lúc đang nhảy;
//  7 rùa biển (e_rua): bơi vòng chậm; chạm thì lặn, lát sau nổi lại.
// Lần đầu thấy mỗi bí mật: +5 bi (cá vàng +10), báo "Bí mật bản đồ n/8" (SaveData.extra["hubEgg"], bit = số thứ tự trên).
// Điểm chạm là Image trong suốt trên lớp phần động (trên ảnh đảo, dưới mây che): chạm trúng thì không vào đảo.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace PokiClash
{
    // nhận cú chạm nổi lên từ điểm chạm (Image trong suốt, con của lớp này) rồi tra bảng taps: không gắn thêm component lúc chạy
    // (PrefabOnlyTests); chạm không trúng điểm nào thì chuyển tiếp lên lớp cha như khi chưa có lớp này
    public sealed partial class IslandAnim : IPointerClickHandler
    {
        readonly Dictionary<GameObject, Action> taps = new Dictionary<GameObject, Action>();

        public void OnPointerClick(PointerEventData e)
        {
            var go = e.rawPointerPress ? e.rawPointerPress : e.pointerCurrentRaycast.gameObject;
            if (go && taps.TryGetValue(go, out var a))
            {
                a?.Invoke();
                return;
            }
            if (transform.parent) ExecuteEvents.ExecuteHierarchy(transform.parent.gameObject, e, ExecuteEvents.pointerClickHandler);
        }

        // tour thử: chạm điểm chạm tên n
        public bool TestTap(string n)
        {
            foreach (var kv in taps)
                if (kv.Key && kv.Key.name == n)
                {
                    kv.Value?.Invoke();
                    return true;
                }
            return false;
        }

        const string EggKey = "hubEgg";
        public const int EggCount = 8;
        enum Egg { Volcano, Light, Wreck, Bottle, Coral, Whale, Gold, Turtle }

        static string EggName(Egg e) => e switch
        {
            Egg.Volcano => Loc.T("Núi lửa thức giấc"),
            Egg.Light => Loc.T("Hải đăng thắp sáng"),
            Egg.Wreck => Loc.T("Lão cua giữ xác tàu"),
            Egg.Bottle => Loc.T("Thư trong chai"),
            Egg.Coral => Loc.T("Đàn cá san hô"),
            Egg.Whale => Loc.T("Cá voi phun nước"),
            Egg.Gold => Loc.T("Cá vàng hiếm"),
            _ => Loc.T("Rùa biển lặn"),
        };

        // thư trong chai: gợi ý các bí mật khác
        static string Letter(int i) => (i % 7) switch
        {
            0 => Loc.T("Gửi người nhặt được: đáy xoáy nước có cả một kho chai thư. Ai ném nhiều thế nhỉ?"),
            1 => Loc.T("Cá vàng chỉ nhảy lên khi không ai để ý. Nhìn kỹ mặt biển nhé!"),
            2 => Loc.T("Lão cua ở xác tàu giữ một bí mật. Gõ cửa thử xem."),
            3 => Loc.T("Đêm qua núi lửa ợ một cái, cả đảo Hỏa rung rinh."),
            4 => Loc.T("Ngọn hải đăng đã tắt từ lâu. Ai đó hãy thắp nó lên."),
            5 => Loc.T("Bé rùa biển rất nhát. Chạm nhẹ thôi kẻo nó lặn mất."),
            _ => Loc.T("Thấy cá voi phun nước thì vẫy tay chào nó nhé!"),
        };

        static int EggBits(SaveData s)
        {
            if (s?.extra == null || !s.extra.TryGetValue(EggKey, out var o) || o == null) return 0;
            try
            {
                return Convert.ToInt32(o);
            }
            catch (Exception)
            {
                return 0;
            }
        }

        // lần đầu thấy: +bi, báo số bí mật đã tìm
        void Found(Egg e)
        {
            var s = App.Save?.Data;
            if (s?.extra == null) return;
            int bits = EggBits(s), b = 1 << (int)e;
            if ((bits & b) != 0) return;
            bits |= b;
            s.extra[EggKey] = (double)bits;
            int gift = e == Egg.Gold ? 10 : 5;
            s.balls += gift;
            int n = 0;
            for (int i = 0; i < EggCount; i++)
                if ((bits & (1 << i)) != 0) n++;
            App.Audio?.Play("coin");
            App.Toasts.Show(Loc.F("Bí mật bản đồ {0}/{1}: {2} +{3} bi", n, EggCount, EggName(e), gift), App.Art ? App.Art.Icon("chest") : null);
            App.Save.Save();
        }

        // điểm chạm trong suốt
        Image Hot(string name, Action tap)
        {
            var img = Ui.Spawn(itemPrefab, transform);
            img.name = name;
            img.sprite = null;
            img.color = new Color(1, 1, 1, 0);
            img.raycastTarget = true;
            taps[img.gameObject] = tap;
            collect?.Add(img);
            return img;
        }

        static void Hide(Image img)
        {
            if (!img) return;
            var c = img.color;
            if (c.a == 0) return;
            c.a = 0;
            img.color = c;
        }

        // tour thử (HubWaterTour): cho cá voi nổi / cá vàng nhảy ngay
        public void TestEgg(string kind)
        {
            foreach (var f in fx)
            {
                if (kind == "voi" && f is Whale w) w.Now(clock);
                if (kind == "ca_vang" && f is Fish fi) fi.GoldNow(clock);
            }
        }

        static Vector2 Pt(List<object> a) => new Vector2(Convert.ToSingle(a[0]), Convert.ToSingle(a[1]));

        bool AddEgg(string k, Vector2 p, float s, int seed, Dictionary<string, object> it)
        {
            float r = (float)J.Num(it, "r", s);
            var to = new Vector2((float)J.Num(it, "tx", p.x), (float)J.Num(it, "ty", p.y));
            switch (k)
            {
                case "e_nui":
                    {
                        var v = new Volcano { host = this, at = p, size = s, seed = seed, bombs = NewImages("da_lua", 6), smoke = NewImages("smoke_big", 3), embers = NewImages("embers", 2) };
                        v.hot = Hot("cham_nui_lua", () => v.Tap());
                        v.r = r;
                        fx.Add(v);
                        return true;
                    }
                case "e_den":
                    {
                        var l = new Light { host = this, at = p, lamp = new Vector2((float)J.Num(it, "lx", p.x), (float)J.Num(it, "ly", p.y)), size = s, r = r, beam = NewImage("beam"), star = NewImage("sparkle") };
                        l.hot = Hot("cham_hai_dang", () => l.Tap());
                        fx.Add(l);
                        return true;
                    }
                case "e_tau":
                    {
                        var c = new Crab { host = this, at = p, to = to, size = s, r = r, seed = seed, img = NewImage("cua"), rings = NewImages("vong", 1) };
                        c.hot = Hot("cham_xac_tau", () => c.Tap());
                        fx.Add(c);
                        return true;
                    }
                case "e_xoay":
                    {
                        var w = new Whirl { host = this, at = p, to = to, size = s, r = r, seed = seed, bottle = NewImage("chai"), rings = NewImages("vong", 2) };
                        w.hot = Hot("cham_xoay_nuoc", () => w.Tap());
                        w.hotBottle = Hot("cham_chai_thu", () => w.TapBottle());
                        fx.Add(w);
                        return true;
                    }
                case "e_sanho":
                    {
                        var c = new Coral { host = this, size = s, r = r, seed = seed, fish = NewImages("ca", 5), rings = NewImages("vong", 1) };
                        foreach (var q in J.Arr(it, "pts"))
                        {
                            var at = Pt(J.Arr(q));
                            int idx = c.pts.Count;
                            c.pts.Add(at);
                            c.hots.Add(Hot("cham_san_ho", () => c.Tap(idx)));
                        }
                        fx.Add(c);
                        return true;
                    }
                case "e_voi":
                    {
                        var w = new Whale { host = this, at = p, size = s, seed = seed, body = NewImage("ca_voi"), tail = NewImage("duoi_ca_voi"), spout = NewImage("voi_phun"), rings = NewImages("vong", 2) };
                        foreach (var img in new[] { w.body, w.tail })
                        {
                            img.type = Image.Type.Filled;
                            img.fillMethod = Image.FillMethod.Vertical;
                            img.fillOrigin = (int)Image.OriginVertical.Top; // phần trên mặt nước lộ dần khi nổi
                        }
                        w.hot = Hot("cham_ca_voi", () => w.Tap());
                        fx.Add(w);
                        return true;
                    }
                case "e_ca":
                    {
                        var f = new Fish { host = this, size = s, seed = seed, img = NewImage("ca"), rings = NewImages("vong", 2), sparkle = NewImage("sparkle"), blue = SpriteOf("ca"), gold = SpriteOf("ca_vang") };
                        foreach (var q in J.Arr(it, "pts")) f.pts.Add(Pt(J.Arr(q)));
                        if (f.pts.Count == 0) f.pts.Add(p);
                        f.hot = Hot("cham_ca_vang", () => f.Tap());
                        fx.Add(f);
                        return true;
                    }
                case "e_rua":
                    {
                        var u = new Turtle { host = this, at = p, size = s, seed = seed, rx = (float)J.Num(it, "rx", 0.1), ry = (float)J.Num(it, "ry", 0.02), img = NewImage("rua"), rings = NewImages("vong", 1) };
                        u.hot = Hot("cham_rua", () => u.Tap());
                        fx.Add(u);
                        return true;
                    }
            }
            return false;
        }

        // vòng gợn chạy một lần từ lúc t0 (cỡ w)
        static void RingOnce(Image img, Vector2 pos, float w, float t, float t0, float life = 0.9f, float amax = 0.7f)
        {
            float k = (t - t0) / life;
            if (k < 0 || k > 1)
            {
                Hide(img);
                return;
            }
            float sc = 0.4f + 0.9f * (1 - (1 - k) * (1 - k));
            Place(img, pos, w, (1 - k) * amax, 0, new Vector3(sc, sc, 1));
        }

        // ---------- núi lửa: đá dung nham bắn vòng cung, khói đen bùng, tàn lửa ----------
        sealed class Volcano : Fx
        {
            public Vector2 at;
            public float size, r;
            public int seed;
            public Image hot;
            public Image[] bombs, smoke, embers;
            float start = -99, next = -1;
            int gen;

            public void Tap()
            {
                App.Audio?.Play("pick");
                Erupt(host.clock);
                host.Found(Egg.Volcano);
            }

            void Erupt(float t)
            {
                if (t - start < 2.4f) return;
                start = t;
                gen++;
                App.Audio?.Play("whoosh");
            }

            public override void Tick(float t)
            {
                float w = host.S(size);
                var p0 = host.P(at);
                Place(hot, p0, host.S(r) * 2, 0);
                if (next < 0) next = t + 9 + Hash(seed, 1) * 10;
                if (t >= next)
                {
                    Erupt(t);
                    next = t + 40 + Hash(seed, gen + 5) * 30;
                }
                float e = t - start;
                for (int i = 0; i < bombs.Length; i++)
                {
                    float d = e - i * 0.11f;
                    float h = Hash(seed, gen * 31 + i), h2 = Hash(seed, gen * 31 + i + 13);
                    float life = 1.0f + 0.3f * h2;
                    if (d < 0 || d > life)
                    {
                        Hide(bombs[i]);
                        continue;
                    }
                    // vòng cung thấp (đỉnh 0,35–0,5 bề ngang miệng núi), rơi xuống sườn: miệng núi sát mép trên bản đồ, bay cao lọt vào mây vành
                    float vx = (h - 0.5f) * 2 * w * 1.3f, vy = w * (1.7f + 0.4f * h2), g = w * 4.2f;
                    var pos = p0 + new Vector2(vx * d, vy * d - 0.5f * g * d * d);
                    float a = d > life - 0.2f ? (life - d) / 0.2f : Mathf.Min(1, d / 0.05f);
                    Place(bombs[i], pos, w * (0.2f + 0.1f * h), a, d * 300 * (h < 0.5f ? 1 : -1));
                }
                for (int i = 0; i < smoke.Length; i++)
                {
                    float d = e - i * 0.18f;
                    const float life = 2.2f;
                    if (d < 0 || d > life)
                    {
                        Hide(smoke[i]);
                        continue;
                    }
                    float k = d / life, ease = 1 - (1 - k) * (1 - k);
                    float h = Hash(seed, gen * 7 + i);
                    var c = Color.Lerp(new Color(0.33f, 0.29f, 0.29f), new Color(0.62f, 0.58f, 0.56f), k);
                    c.a = k < 0.1f ? k / 0.1f : 1 - Mathf.SmoothStep(0, 1, (k - 0.4f) / 0.6f);
                    float sc = 0.5f + 1.1f * ease;
                    var pos = p0 + new Vector2((h - 0.5f) * w * 0.6f + k * w * 0.4f, ease * w * 0.8f + w * 0.05f);
                    Place(smoke[i], pos, w * 0.7f, 1, (h - 0.5f) * 40, new Vector3(sc, sc, 1));
                    smoke[i].color = c;
                }
                for (int i = 0; i < embers.Length; i++)
                {
                    float d = e - 0.1f - i * 0.25f;
                    const float life = 1.4f;
                    if (d < 0 || d > life)
                    {
                        Hide(embers[i]);
                        continue;
                    }
                    float k = d / life;
                    float h = Hash(seed, gen * 3 + i);
                    Place(embers[i], p0 + new Vector2((h - 0.5f) * w * 0.8f, k * w * 0.9f), w * 0.4f, Mathf.Sin(k * Mathf.PI), k * 60);
                }
            }
        }

        // ---------- hải đăng: đèn bật, chùm sáng quét 2,5 vòng rồi tắt ----------
        sealed class Light : Fx
        {
            public Vector2 at, lamp;
            public float size, r;
            public Image hot, beam, star;
            float start = -99;

            public void Tap()
            {
                App.Audio?.Play("pick");
                if (host.clock - start > 4.5f) start = host.clock;
                host.Found(Egg.Light);
            }

            public override void Tick(float t)
            {
                Place(hot, host.P(at), host.S(r) * 2, 0);
                float e = t - start;
                const float dur = 4.5f;
                if (e < 0 || e > dur)
                {
                    Hide(beam);
                    Hide(star);
                    return;
                }
                float a = Mathf.Min(1, Mathf.Min(e / 0.3f, (dur - e) / 0.6f));
                var lp = host.P(lamp);
                beam.rectTransform.pivot = new Vector2(0, 0.5f); // gốc chùm sáng ở đèn
                Place(beam, lp, host.S(size), a * 0.75f, 200 + e / dur * 900);
                float k = 1 + Mathf.Sin(e * 9) * 0.15f;
                Place(star, lp, host.S(size) * 0.22f, a, e * 90, new Vector3(k, k, 1));
            }
        }

        // ---------- xác tàu: lão cua ló ra, bò ra bãi, vẫy càng, bò về ----------
        sealed class Crab : Fx
        {
            public Vector2 at, to;
            public float size, r;
            public int seed;
            public Image hot, img;
            public Image[] rings;
            float start = -99, peek = -99, next = -1;

            public void Tap()
            {
                App.Audio?.Play("pick");
                if (host.clock - start > 4f) start = host.clock;
                host.Found(Egg.Wreck);
            }

            public override void Tick(float t)
            {
                float w = host.S(size);
                Vector2 a = host.P(at), b = host.P(to);
                Place(hot, a, host.S(r) * 2, 0);
                if (next < 0) next = t + 14 + Hash(seed, 2) * 20;
                if (t >= next)
                {
                    if (t - start > 4f) peek = t; // ló ra nhìn rồi thụt vào: gợi ý có gì ở xác tàu
                    next = t + 45 + Hash(seed, Mathf.FloorToInt(t)) * 30;
                }
                RingOnce(rings[0], a, w * 1.6f, t, Mathf.Max(start, peek));
                float e = t - start;
                if (e >= 0 && e < 3.9f)
                {
                    Vector2 pos;
                    float sc = 1, rot = 0;
                    if (e < 0.3f)
                    {
                        pos = a;
                        float k = e / 0.3f;
                        sc = k < 0.7f ? k / 0.7f * 1.15f : 1.15f - (k - 0.7f) / 0.3f * 0.15f;
                    }
                    else if (e < 1.3f)
                    {
                        float k = Mathf.SmoothStep(0, 1, (e - 0.3f) / 1.0f);
                        pos = Vector2.Lerp(a, b, k) + new Vector2(0, Mathf.Abs(Mathf.Sin(e * 22)) * w * 0.06f);
                        rot = Mathf.Sin(e * 26) * 8;
                    }
                    else if (e < 2.6f)
                    {
                        pos = b + new Vector2(0, Mathf.Abs(Mathf.Sin(e * 7)) * w * 0.12f);
                        rot = Mathf.Sin(e * 9) * 12;
                    }
                    else if (e < 3.6f)
                    {
                        float k = Mathf.SmoothStep(0, 1, (e - 2.6f) / 1.0f);
                        pos = Vector2.Lerp(b, a, k) + new Vector2(0, Mathf.Abs(Mathf.Sin(e * 22)) * w * 0.06f);
                        rot = Mathf.Sin(e * 26) * 8;
                    }
                    else
                    {
                        pos = a;
                        sc = 1 - (e - 3.6f) / 0.3f;
                    }
                    Place(img, pos, w, 1, rot, new Vector3(sc, sc, 1));
                    return;
                }
                float pe = t - peek;
                if (pe >= 0 && pe < 1.6f)
                {
                    float k = pe < 0.3f ? pe / 0.3f : pe > 1.2f ? 1 - (pe - 1.2f) / 0.4f : 1;
                    Place(img, a + new Vector2(0, w * 0.1f * k), w, 1, Mathf.Sin(pe * 8) * 10 * k, new Vector3(k, k, 1));
                    return;
                }
                Hide(img);
            }
        }

        // ---------- xoáy nước: nhả chai thư; chai dập dềnh, chạm thì đọc thư rồi chai chìm ----------
        sealed class Whirl : Fx
        {
            public Vector2 at, to;
            public float size, r;
            public int seed;
            public Image hot, hotBottle, bottle;
            public Image[] rings;
            float start = -99, sink = -99;
            bool out_;
            int letter;

            public void Tap()
            {
                App.Audio?.Play("pick");
                float t = host.clock;
                if (out_ || t - start < 1.5f) return;
                start = t;
                sink = -99;
                out_ = true;
                letter = Mathf.FloorToInt(Hash(seed, Mathf.FloorToInt(t * 3)) * 7);
            }

            public void TapBottle()
            {
                if (!out_ || host.clock - start < 0.9f) return;
                App.Audio?.Play("pick");
                out_ = false;
                sink = host.clock;
                App.Modals.Alert(Loc.T("Thư trong chai"), Letter(letter), Loc.T("Cất thư"), null, false);
                host.Found(Egg.Bottle);
            }

            public override void Tick(float t)
            {
                float w = host.S(size);
                Vector2 a = host.P(at), b = host.P(to);
                Place(hot, a, host.S(r) * 2, 0);
                RingOnce(rings[0], a, host.S(r) * 1.6f, t, start, 1.1f, 0.8f);
                RingOnce(rings[1], b, w * 2.2f, t, start + 0.8f, 1.0f, 0.7f);
                float e = t - start;
                if (out_)
                {
                    Vector2 pos;
                    float rot;
                    if (e < 0.8f)
                    {
                        float k = e / 0.8f;
                        pos = Vector2.Lerp(a, b, k) + new Vector2(0, 4 * k * (1 - k) * w * 2.2f);
                        rot = k * 540;
                    }
                    else
                    {
                        pos = b + new Vector2(Mathf.Sin(t * 0.7f) * w * 0.15f, Mathf.Sin(t * 1.9f) * w * 0.08f);
                        rot = 20 + Mathf.Sin(t * 1.3f) * 12;
                    }
                    Place(bottle, pos, w, 1, rot);
                    Place(hotBottle, pos, w * 1.8f, 0);
                    return;
                }
                Hide(hotBottle);
                hotBottle.rectTransform.sizeDelta = Vector2.zero;
                float se = t - sink;
                if (se >= 0 && se < 0.6f)
                {
                    float k = 1 - se / 0.6f;
                    Place(bottle, b + new Vector2(0, -(1 - k) * w * 0.3f), w, k, 20, new Vector3(k, k, 1));
                    return;
                }
                Hide(bottle);
            }
        }

        // ---------- san hô: đàn cá nhỏ túa ra ----------
        sealed class Coral : Fx
        {
            public readonly List<Vector2> pts = new List<Vector2>();
            public readonly List<Image> hots = new List<Image>();
            public float size, r;
            public int seed;
            public Image[] fish, rings;
            float start = -99;
            int at;

            public void Tap(int i)
            {
                App.Audio?.Play("pick");
                if (host.clock - start < 1.2f) return;
                start = host.clock;
                at = i;
                host.Found(Egg.Coral);
            }

            public override void Tick(float t)
            {
                for (int i = 0; i < pts.Count; i++) Place(hots[i], host.P(pts[i]), host.S(r) * 2, 0);
                float w = host.S(size);
                var p0 = host.P(pts.Count > 0 ? pts[Mathf.Clamp(at, 0, pts.Count - 1)] : Vector2.zero);
                RingOnce(rings[0], p0, w * 3, t, start);
                float e = t - start;
                for (int i = 0; i < fish.Length; i++)
                {
                    const float life = 1.1f;
                    float d = e - i * 0.05f;
                    if (d < 0 || d > life)
                    {
                        Hide(fish[i]);
                        continue;
                    }
                    float k = d / life, ease = 1 - (1 - k) * (1 - k);
                    float ang = (Hash(seed, i + Mathf.FloorToInt(start * 10)) * 360f) * Mathf.Deg2Rad;
                    var dir = new Vector2(Mathf.Cos(ang), Mathf.Sin(ang) * 0.5f);
                    var pos = p0 + dir * ease * w * 4.5f;
                    bool right = dir.x > 0;
                    float a = k < 0.1f ? k / 0.1f : 1 - Mathf.SmoothStep(0, 1, (k - 0.55f) / 0.45f);
                    Place(fish[i], pos, w, a, Mathf.Sin(d * 30) * 10, new Vector3(right ? -1 : 1, 1, 1));
                }
            }
        }

        // ---------- cá voi: nổi lên (phần trên mặt nước lộ dần), phun nước, lặn, vẫy đuôi ----------
        sealed class Whale : Fx
        {
            public Vector2 at;
            public float size;
            public int seed;
            public Image hot, body, tail, spout;
            public Image[] rings;
            float cycle = -1, period, spoutAt = -99;
            int gen;

            public void Now(float t)
            {
                cycle = t;
                if (period < 6) period = 30;
            }

            public void Tap()
            {
                float e = host.clock - cycle;
                if (e < 0 || e > 3.1f) return;
                App.Audio?.Play("pick");
                spoutAt = host.clock; // phun thêm một lần
                host.Found(Egg.Whale);
            }

            static void Rise(Image img, Vector2 water, float w, float k, float dx)
            {
                if (k <= 0.001f)
                {
                    Hide(img);
                    return;
                }
                var sp = img.sprite;
                float h = sp ? w * sp.rect.height / sp.rect.width : w;
                img.fillAmount = Mathf.Clamp01(k);
                Place(img, water + new Vector2(dx, k * h - h * 0.5f), w, 1);
            }

            public override void Tick(float t)
            {
                float w = host.S(size);
                var p0 = host.P(at);
                if (cycle < 0)
                {
                    cycle = t + 6 + Hash(seed, 1) * 8;
                    period = 30 + Hash(seed, 2) * 15;
                }
                if (t > cycle + period)
                {
                    gen++;
                    cycle += period;
                    period = 30 + Hash(seed, gen + 3) * 15;
                }
                float e = t - cycle;
                // thân: nổi 0–0,7 s, giữ tới 2,4 s, lặn tới 3,1 s
                float kb = e < 0 ? 0 : e < 0.7f ? 1 - (1 - e / 0.7f) * (1 - e / 0.7f) : e < 2.4f ? 1 : e < 3.1f ? 1 - (e - 2.4f) / 0.7f : 0;
                Rise(body, p0, w, kb, e > 2.4f ? (e - 2.4f) * w * 0.25f : 0);
                bool up = kb > 0.3f;
                Place(hot, p0 + new Vector2(0, w * 0.2f), up ? w * 1.1f : 0, 0);
                // vòi phun: lúc 0,9 s (hoặc khi chạm), vươn 0,35 s, giữ, tan
                float se = t - Mathf.Max(cycle + 0.9f, spoutAt);
                if (up && se >= 0 && se < 1.5f)
                {
                    spout.rectTransform.pivot = new Vector2(0.5f, 0.05f);
                    float sy = se < 0.35f ? se / 0.35f : 1 + Mathf.Sin(se * 14) * 0.04f;
                    float a = se > 1.1f ? 1 - (se - 1.1f) / 0.4f : 1;
                    var sp = body.sprite;
                    float h = sp ? w * sp.rect.height / sp.rect.width : w;
                    Place(spout, p0 + new Vector2(-w * 0.05f, kb * h * 0.92f), w * 0.55f, a, 0, new Vector3(1, sy, 1));
                }
                else Hide(spout);
                // đuôi: 3,5–5 s
                float te = e - 3.5f;
                float kt = te < 0 ? 0 : te < 0.5f ? te / 0.5f : te < 1.0f ? 1 : te < 1.5f ? 1 - (te - 1.0f) / 0.5f : 0;
                Rise(tail, p0 + new Vector2(w * 0.45f, 0), w * 0.7f, kt, 0);
                RingOnce(rings[0], p0, w * 1.6f, t, cycle, 1.2f, 0.75f);
                RingOnce(rings[1], p0 + new Vector2(w * 0.45f, 0), w * 1.1f, t, cycle + 4.5f, 1.0f, 0.75f);
            }
        }

        // ---------- cá nhảy: vòng cung khỏi mặt biển ở các chỗ rải rác; thỉnh thoảng là cá vàng (chạm kịp lúc đang nhảy) ----------
        sealed class Fish : Fx
        {
            public readonly List<Vector2> pts = new List<Vector2>();
            public float size;
            public int seed;
            public Image hot, img, sparkle;
            public Image[] rings;
            public Sprite blue, gold;
            float next = -1, start = -99, dur = 0.9f, lastGold = -99;
            int gen, spot;
            float dir = 1;
            bool golden, caught, forceGold;

            public void GoldNow(float t)
            {
                next = t;
                forceGold = true;
            }

            public void Tap()
            {
                if (!golden || caught || host.clock - start > dur) return;
                caught = true;
                App.Audio?.Play("pick");
                host.Found(Egg.Gold);
            }

            public override void Tick(float t)
            {
                float w = host.S(size);
                if (next < 0) next = t + 2 + Hash(seed, 1) * 4;
                if (t >= next)
                {
                    gen++;
                    start = t;
                    spot = Mathf.FloorToInt(Hash(seed, gen * 3) * pts.Count) % pts.Count;
                    dir = Hash(seed, gen * 5) < 0.5f ? -1 : 1;
                    // cá vàng: 12 % mỗi lượt, cách lần trước ít nhất 40 s; nhảy chậm, cao hơn cho kịp chạm
                    golden = forceGold || (Hash(seed, gen * 7) < 0.12f && t - lastGold > 40);
                    forceGold = false;
                    if (golden) lastGold = t;
                    caught = false;
                    dur = golden ? 1.5f : 0.9f;
                    img.sprite = golden ? gold : blue;
                    next = t + dur + 3 + Hash(seed, gen * 11) * 5;
                }
                var p0 = host.P(pts.Count > 0 ? pts[spot] : Vector2.zero);
                float e = t - start, k = e / dur;
                float span = w * 1.5f, height = w * (golden ? 1.3f : 1.0f);
                RingOnce(rings[0], p0 - new Vector2(span * 0.5f * dir, 0), w * 1.4f, t, start, 0.8f, 0.7f);
                RingOnce(rings[1], p0 + new Vector2(span * 0.5f * dir, 0), w * 1.4f, t, start + dur, 0.8f, 0.7f);
                if (k < 0 || k > 1)
                {
                    Hide(img);
                    Hide(sparkle);
                    hot.rectTransform.sizeDelta = Vector2.zero;
                    return;
                }
                var pos = p0 + new Vector2((k - 0.5f) * span * dir, 4 * k * (1 - k) * height);
                float vx = span, vy = 4 * (1 - 2 * k) * height;
                float ang = Mathf.Atan2(vy, vx) * Mathf.Rad2Deg;
                float a = k < 0.08f ? k / 0.08f : k > 0.92f ? (1 - k) / 0.08f : 1;
                // hình gốc nhìn sang trái: bay sang phải thì lật
                float fw = golden ? w * 1.3f : w;
                Place(img, pos, fw, caught ? a * 0.5f : a, dir > 0 ? ang : -ang, new Vector3(dir > 0 ? -1 : 1, 1, 1));
                if (golden)
                {
                    float s = 0.8f + Mathf.Sin(e * 12) * 0.25f;
                    Place(sparkle, pos + new Vector2(0, w * 0.45f), w * 0.5f, a, e * 120, new Vector3(s, s, 1));
                    Place(hot, pos, caught ? 0 : w * 2.4f, 0);
                }
                else
                {
                    Hide(sparkle);
                    hot.rectTransform.sizeDelta = Vector2.zero;
                }
            }
        }

        // ---------- rùa biển: bơi vòng elip chậm, quẫy vây; chạm thì lặn, 5 s sau nổi lại ----------
        sealed class Turtle : Fx
        {
            public Vector2 at;
            public float size, rx, ry;
            public int seed;
            public Image hot, img;
            public Image[] rings;
            float dive = -99;

            public void Tap()
            {
                if (host.clock - dive < 6f) return;
                App.Audio?.Play("pick");
                dive = host.clock;
                host.Found(Egg.Turtle);
            }

            public override void Tick(float t)
            {
                float w = host.S(size), RX = host.S(rx), RY = host.S(ry);
                float ang = t * Mathf.PI * 2 / 52f + seed;
                var pos = host.P(at) + new Vector2(Mathf.Cos(ang) * RX, Mathf.Sin(ang) * RY);
                var v = new Vector2(-Mathf.Sin(ang) * RX, Mathf.Cos(ang) * RY);
                float rot = Mathf.Atan2(v.y, v.x) * Mathf.Rad2Deg - 90; // hình gốc đầu hướng lên
                float de = t - dive;
                float k = de < 0 || de > 5.6f ? 1 : de < 0.8f ? 1 - de / 0.8f : de < 5f ? 0 : (de - 5f) / 0.6f;
                RingOnce(rings[0], pos, w * 1.8f, t, dive, 1.0f, 0.7f);
                float paddle = 1 + Mathf.Sin(t * 3.2f + seed) * 0.05f;
                float sc = 0.55f + 0.45f * k;
                Place(img, pos, w, k, rot, new Vector3(sc * paddle, sc, 1));
                var c = img.color; // dưới mặt nước một chút: ngả lam
                img.color = new Color(0.86f, 0.95f, 1f, c.a);
                Place(hot, pos, k > 0.5f ? w * 1.6f : 0, 0);
            }
        }
    }
}
