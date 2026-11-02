// Hạt hiệu ứng của máy bi trên uGUI. Mỗi hạt là một bản sao prefab mục Items/HatMayBi (Image trắng, tô màu lúc chạy); hết đời
// thì tắt, lần sau dùng lại. Hình hạt là ảnh fx_* tìm qua ArtLibrary: ảnh gen (03 Art/Pachinko, gói P4) nếu có, không thì ảnh
// thay thế trong 03 Art/Fallback (Web/scripts/draw_machine_fx.py).
// Các bộ hiệu ứng chép cấu trúc của máy bi tham khảo: số hạt, đời, tốc, trọng lực, kẹp tốc, cỡ và màu theo đời (bảng ở
// GD_Claude/07_MayBi.md, mục "Hiệu ứng chép"). Cỡ và tốc tính theo đơn vị u của máy đó, đổi ra px bằng unit lúc phát:
// hiệu ứng theo bi dùng UnitBall (bi máy đó 0,162 u), hiệu ứng ô dùng độ rộng ô (ô máy đó 0,9 u).
using System.Collections.Generic;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class MachineFx
    {
        // px canvas cho 1 u của máy tham khảo, theo cỡ bi: bi ở đây 18 × K px, ở đó 0,162 u
        public static float UnitBall => (float)Core.Board.BallR * 2 * MachineBoard.K / 0.162f;
        public const float SlotU = 0.9f; // bề rộng ô của máy tham khảo (u)
        const float G = 9.81f; // trọng lực của hệ hạt (u/giây²), nhân với grav của từng loạt

        // một loạt hạt giống nhau, như một hệ hạt phát một lần
        public sealed class Burst
        {
            public string sprite = "fx_glow"; // tên ảnh; rỗng = hình chữ nhật trắng
            public int count = 1;
            public float delay;
            public float life = 0.2f, lifeMax; // lifeMax > 0: ngẫu nhiên life..lifeMax
            public float size = 1, sizeMax; // u
            public float speed, speedMax; // u/giây
            public float dir = 90, arc; // hướng giữa và độ rộng cung phát (độ, 90 = lên)
            public float radius; // điểm phát lệch theo hướng bay, ngẫu nhiên 0..radius (u)
            public float grav; // hệ số trọng lực (dương = rơi)
            public float limit, dampen; // tốc vượt limit (u/giây) mất phần dampen mỗi khung 1/30 giây
            public float[] curve = { 0, 1, 1, 1 }; // cỡ theo đời: cặp (t, hệ số)
            public Color from = Color.white, to = Color.white;
            public float fadeIn; // alpha 0 → 1 trong phần đời đầu này
            public float fadeAt = 1; // alpha giữ tới phần đời này rồi giảm về 0
            public float stretch; // > 0: kéo dài theo hướng bay, dài = cỡ × stretch, rộng = cỡ × thin
            public float thin = 0.35f;
            public bool flip; // vệt kéo dài quay đầu sáng vào tâm
            public bool spin; // xoay ngẫu nhiên lúc phát
        }

        struct Hat
        {
            public Image img;
            public Burst b;
            public float age, life, size, unit, rot;
            public Vector2 pos, vel;
            public Color tint;
        }

        readonly Image prefab;
        readonly RectTransform layer;
        readonly List<Hat> live = new List<Hat>();
        readonly Stack<Image> free = new Stack<Image>();
        readonly Dictionary<string, Sprite> sprites = new Dictionary<string, Sprite>();

        public MachineFx(Image prefab, RectTransform layer)
        {
            this.prefab = prefab;
            this.layer = layer;
        }

        public int Live => live.Count;

        public Sprite Sprite(string name)
        {
            if (string.IsNullOrEmpty(name)) return null;
            if (!sprites.TryGetValue(name, out var s))
                sprites[name] = s = ArtLibrary.Current ? ArtLibrary.Current.Get(name) : null;
            return s;
        }

        public Image Take(Transform parent)
        {
            Image img;
            if (free.Count > 0)
            {
                img = free.Pop();
                if (img.transform.parent != parent) img.transform.SetParent(parent, false);
                img.gameObject.SetActive(true);
            }
            else
            {
                img = Ui.Spawn(prefab, parent);
                img.name = "hat";
            }
            img.rectTransform.SetAsLastSibling();
            return img;
        }

        public void Give(Image img)
        {
            img.gameObject.SetActive(false);
            free.Push(img);
        }

        // phát một loạt tại at (px canvas của mặt máy), unit = px cho 1 u, tint nhân thêm vào màu
        public void Emit(Burst b, Vector2 at, float unit, Color? tint = null)
        {
            if (!prefab) return;
            for (int i = 0; i < b.count; i++)
            {
                float a = (b.dir + (b.arc > 0 ? Random.Range(-b.arc / 2, b.arc / 2) : 0)) * Mathf.Deg2Rad;
                var d = new Vector2(Mathf.Cos(a), Mathf.Sin(a));
                float sp = b.speedMax > 0 ? Random.Range(b.speed, b.speedMax) : b.speed;
                var img = Take(layer);
                img.sprite = Sprite(b.sprite);
                img.enabled = false;
                live.Add(new Hat
                {
                    img = img,
                    b = b,
                    age = 0,
                    life = b.lifeMax > 0 ? Random.Range(b.life, b.lifeMax) : b.life,
                    size = b.sizeMax > 0 ? Random.Range(b.size, b.sizeMax) : b.size,
                    unit = unit,
                    rot = b.spin ? Random.Range(0f, 360f) : 0,
                    pos = at + d * (b.radius > 0 ? Random.Range(0, b.radius) * unit : 0),
                    // tốc bằng 0 vẫn giữ hướng (vệt kéo dài cần hướng)
                    vel = d * Mathf.Max(sp, 1e-4f) * unit,
                    tint = tint ?? Color.white,
                });
            }
        }

        public void Emit(Burst[] set, Vector2 at, float unit, Color? tint = null)
        {
            foreach (var b in set) Emit(b, at, unit, tint);
        }

        public static float Curve(float[] k, float t)
        {
            if (t <= k[0]) return k[1];
            for (int i = 2; i < k.Length; i += 2)
                if (t <= k[i]) return Mathf.Lerp(k[i - 1], k[i + 1], (t - k[i - 2]) / Mathf.Max(1e-5f, k[i] - k[i - 2]));
            return k[k.Length - 1];
        }

        public void Update(float dt)
        {
            for (int i = live.Count - 1; i >= 0; i--)
            {
                var h = live[i];
                var b = h.b;
                h.age += dt;
                float t = (h.age - b.delay) / h.life;
                if (t >= 1)
                {
                    Give(h.img);
                    live.RemoveAt(i);
                    continue;
                }
                if (t < 0)
                {
                    live[i] = h;
                    continue;
                }
                h.img.enabled = true;
                h.vel.y -= b.grav * G * h.unit * dt;
                if (b.dampen > 0)
                {
                    float sp = h.vel.magnitude, lim = b.limit * h.unit;
                    if (sp > lim && sp > 1e-3f)
                    {
                        float keep = lim + (sp - lim) * Mathf.Pow(1 - b.dampen, dt * 30);
                        h.vel *= Mathf.Max(keep, 1e-4f * h.unit) / sp;
                    }
                }
                h.pos += h.vel * dt;
                float s = h.size * h.unit * Curve(b.curve, t);
                var c = Color.Lerp(b.from, b.to, t) * h.tint;
                float alpha = b.fadeIn > 0 && t < b.fadeIn ? t / b.fadeIn : 1;
                if (t > b.fadeAt) alpha *= 1 - (t - b.fadeAt) / Mathf.Max(1e-5f, 1 - b.fadeAt);
                c.a *= alpha;
                h.img.color = c;
                var rt = h.img.rectTransform;
                rt.anchoredPosition = h.pos;
                if (b.stretch > 0)
                {
                    rt.sizeDelta = new Vector2(s * b.stretch, s * b.thin);
                    float ang = Mathf.Atan2(h.vel.y, h.vel.x) * Mathf.Rad2Deg + (b.flip ? 180 : 0);
                    rt.localEulerAngles = new Vector3(0, 0, ang);
                }
                else
                {
                    rt.sizeDelta = new Vector2(s, s);
                    rt.localEulerAngles = new Vector3(0, 0, h.rot);
                }
                live[i] = h;
            }
        }

        public void Clear()
        {
            foreach (var h in live) Give(h.img);
            live.Clear();
        }

        // ---------- các bộ hiệu ứng ----------

        static Color C(string hex, float a = 1)
        {
            ColorUtility.TryParseHtmlString(hex, out var c);
            c.a = a;
            return c;
        }

        // đinh bị chạm: quầng sau đinh co 1,10 → 0,68 trong 0,067 giây (đinh sáng phồng 1,15 → 1 do MachineBoard.Flash),
        // kèm hai lấp lánh nhỏ văng ra. Cỡ theo đường kính đinh (unit = px của đường kính đinh)
        public static readonly Burst[] PegHit =
        {
            new Burst { life = 0.067f, size = 2.6f, curve = new[] { 0, 1.10f, 1, 0.68f }, from = C("#ffd968", 0.95f), to = C("#ffb347", 0.9f), fadeAt = 0.7f },
        };
        public static readonly Burst[] PegSpark =
        {
            new Burst { sprite = "fx_sparkle", count = 2, life = 0.18f, lifeMax = 0.3f, size = 0.09f, sizeMax = 0.14f, speed = 0.6f, speedMax = 1.6f, arc = 360,
                curve = new[] { 0, 0.4f, 0.25f, 1, 1, 0.2f }, from = C("#fff2a8"), to = C("#ffc94a"), fadeAt = 0.5f, spin = true },
        };

        // nấm bị chạm: quầng 3 (co 1 → 0,16 trong 0,15 giây), vòng 1,62 lan 0,16 → 1 trong 0,19 giây, quầng 1,75 lan 0,32 → 1.
        // Máy tham khảo dùng tím; ở đây theo màu nấm. unit = px của đường kính nấm / 1,1 (nấm máy đó đường kính 1,1 u)
        public static readonly Burst[] BumperHit =
        {
            new Burst { life = 0.15f, size = 3f, curve = new[] { 0, 1f, 1, 0.16f }, from = C("#ff8a6a", 0.79f), to = C("#ff6a50", 0.79f), fadeAt = 0.5f },
            new Burst { sprite = "fx_ring", life = 0.19f, size = 1.62f, curve = new[] { 0, 0.16f, 1, 1 }, from = C("#ffb08a"), to = C("#ff5a3c"), fadeIn = 0.2f, fadeAt = 0.55f },
            new Burst { life = 0.15f, size = 1.75f, curve = new[] { 0, 0.32f, 1, 1 }, from = C("#ffd0a0", 0.63f), to = C("#ff8a5a", 0.63f), fadeAt = 0.5f },
        };

        // bi rơi vào ô: ba quầng (0,15 / 0,15 / 0,1 giây), 6 sao bắn rất nhanh rồi bị hãm lại lơ lửng, 6 vệt sáng hướng tâm
        // chớp 0,07–0,1 giây. unit = px của bề rộng ô / 0,9
        public static readonly Burst[] SlotHit =
        {
            new Burst { life = 0.15f, size = 3.51f, curve = new[] { 0, 0, 0.17f, 0.79f, 0.38f, 0.9f, 1, 1 }, from = C("#ffc854", 0.85f), to = C("#ff9135", 0.85f), fadeAt = 0 },
            new Burst { life = 0.15f, size = 2.6f, curve = new[] { 0, 0.54f, 0.24f, 0.84f, 1, 1 }, from = C("#fff0c8"), to = C("#ff8507"), fadeAt = 0.5f },
            new Burst { life = 0.1f, size = 0.78f, curve = new[] { 0, 0.35f, 0.16f, 0.78f, 1, 1 }, from = C("#ffb04f"), to = C("#ffe08f"), fadeIn = 1 },
            new Burst { sprite = "fx_sparkle", count = 6, life = 0.2f, lifeMax = 0.35f, size = 0.2f, sizeMax = 0.9f, speed = 15, speedMax = 60, arc = 200,
                limit = 0.25f, dampen = 0.7f, curve = new[] { 0, 0, 0.61f, 0.99f, 1, 0 }, from = C("#ffd666"), to = C("#fff4b8") },
            new Burst { sprite = "fx_streak", count = 6, life = 0.07f, lifeMax = 0.1f, size = 0.65f, sizeMax = 1.3f, speed = 0.01f, arc = 144, radius = 0.35f,
                stretch = 2, thin = 0.3f, curve = new[] { 0, 1f, 1, 0.57f }, from = C("#ffb347"), to = C("#ffe08f"), fadeIn = 0.3f, fadeAt = 0.7f },
        };

        // rương rơi vào (bảng điểm cấp 2; cấp 3 thêm 6 tia bắn 10–20 u/giây, vòng to 1,5 lần, quầng 6). unit tính theo rương
        public static Burst[] ChestHit(int tier)
        {
            float ring = tier >= 3 ? 1.5f : 1;
            var list = new List<Burst>
            {
                new Burst { life = 0.2f, size = 4.2f, from = C("#fff0a0"), to = C("#ffa435"), fadeAt = 0.5f },
                new Burst { life = tier >= 2 ? 0.4f : 0.2f, size = tier >= 3 ? 6 : 4.5f, curve = new[] { 0, 0.18f, 0.88f, 0.53f, 1, 0.53f }, from = C("#ffe052"), to = C("#ffe052"), fadeIn = 0.3f, fadeAt = 0.7f },
                new Burst { sprite = "fx_ring", life = 0.2f, size = 4.5f * ring, curve = new[] { 0, 0.18f, 0.96f, 1, 1, 1 }, from = C("#ffe052"), to = C("#ffe052"), fadeIn = 0.15f, fadeAt = 0.6f },
                new Burst { sprite = "fx_ring", life = 0.2f, size = 4.2f * ring, curve = new[] { 0, 0.18f, 0.96f, 1, 1, 1 }, from = C("#ffa900"), to = C("#ffa900"), fadeIn = 0.15f, fadeAt = 0.6f },
                new Burst { sprite = "fx_sparkle", count = tier >= 3 ? 3 : 2, life = 0.2f, lifeMax = 0.6f, size = 0.1f, sizeMax = 0.5f, speed = 0.1f, arc = 360, radius = tier >= 3 ? 1.5f : 1,
                    curve = new[] { 0, 1f, 1, 0.3f }, from = Color.white, to = C("#fff2a8") },
                new Burst { sprite = "fx_star", count = 2, life = 0.2f, lifeMax = 0.6f, size = tier >= 3 ? 0.5f : 0.3f, sizeMax = 1, speed = 0.1f, arc = 360, radius = 1,
                    curve = new[] { 0, 1f, 1, tier >= 3 ? 0.14f : 0.3f }, from = C("#ffdf06"), to = C("#ff9a30"), spin = true },
            };
            if (tier >= 3)
                list.Add(new Burst { sprite = "fx_streak", count = 6, life = 0.2f, lifeMax = 0.5f, size = 0.5f, sizeMax = 1, speed = 10, speedMax = 20, arc = 360,
                    stretch = 2.5f, thin = 0.3f, curve = new[] { 0, 0.01f, 0.24f, 1, 1, 0.17f }, from = Color.white, to = C("#ffe08f") });
            return list.ToArray();
        }

        // rương vàng (jackpot): vòng 0,24 giây, hai quầng 0,35 giây, 4 tia rơi nhẹ, 3 sao bắn (trễ 0,05 giây), 1 sao nảy (trễ 0,1 giây),
        // sao lõi. Toàn bộ khoảng 0,5 giây. unit = UnitBall
        public static readonly Burst[] Jackpot =
        {
            new Burst { sprite = "fx_ring", life = 0.24f, size = 3.6f, curve = new[] { 0, 0.18f, 1, 1 }, from = C("#ffd068"), to = C("#ffd068"), fadeAt = 0.5f },
            new Burst { life = 0.35f, size = 5.18f, curve = new[] { 0, 0.18f, 0.41f, 1, 1, 1 }, from = C("#ff8d00", 0.8f), to = C("#ff8d00", 0.8f), fadeAt = 0.5f },
            new Burst { life = 0.35f, size = 5.18f, curve = new[] { 0, 1f, 1, 0.34f }, from = C("#ffd300", 0.9f), to = C("#ffd300", 0.9f), fadeAt = 0.5f },
            new Burst { sprite = "fx_streak", count = 4, life = 0.15f, lifeMax = 0.4f, size = 0.17f, speed = 1.6f, speedMax = 10, arc = 360, radius = 0.78f, grav = 0.2f,
                dampen = 0.1f, stretch = 4, thin = 0.5f, curve = new[] { 0, 1f, 0.54f, 1, 1, 0.56f }, from = Color.white, to = C("#fff2a8") },
            new Burst { sprite = "fx_star", count = 3, delay = 0.05f, life = 0.3f, lifeMax = 0.5f, size = 0.42f, sizeMax = 0.82f, speed = 4.8f, speedMax = 8.2f, arc = 270, radius = 0.78f,
                dampen = 0.2f, spin = true, curve = new[] { 0, 0.64f, 0.35f, 0.99f, 0.4f, 0.98f, 0.8f, 0.85f, 0.99f, 0 }, from = C("#ffd24a"), to = C("#ffb000") },
            new Burst { sprite = "fx_star", delay = 0.1f, life = 0.3f, lifeMax = 0.5f, size = 0.35f, sizeMax = 1.22f, speed = 0.7f, speedMax = 2.2f, arc = 120, radius = 0.78f,
                dampen = 0.2f, spin = true, curve = new[] { 0, 0.64f, 0.35f, 0.99f, 0.4f, 0.98f, 0.8f, 0.85f, 0.99f, 0 }, from = C("#ffd24a"), to = C("#ffb000") },
            new Burst { sprite = "fx_star", life = 0.25f, size = 1.57f, speed = 1.4f, dampen = 0.2f, curve = new[] { 0, 0.36f, 1, 0.67f }, from = C("#ffe27a"), to = C("#ffd24a"), fadeAt = 0.5f },
        };

        // bi lọt cốc bạc hoặc két: chớp 0,2 giây, vòng 0,1 giây, 10 chấm và 10 sao văng (sao rơi nhẹ). unit = UnitBall
        public static readonly Burst[] RingHit =
        {
            new Burst { life = 0.2f, size = 0.7f, spin = true, curve = new[] { 0, 0.71f, 1, 1 }, from = C("#ffe7ae"), to = C("#ff7c00"), fadeAt = 0.5f },
            new Burst { sprite = "fx_ring", life = 0.1f, size = 1, curve = new[] { 0, 0.38f, 1, 1 }, from = Color.white, to = Color.white, fadeAt = 0 },
            new Burst { count = 10, life = 0.2f, lifeMax = 0.4f, size = 0.05f, sizeMax = 0.1f, speed = 0, speedMax = 2, arc = 360, radius = 0.3f,
                curve = new[] { 0, 0.36f, 0.12f, 1, 0.8f, 0.85f, 1, 0.3f }, from = C("#fff2c0"), to = C("#ffb347") },
            new Burst { sprite = "fx_sparkle", count = 10, life = 0.4f, lifeMax = 0.6f, size = 0.2f, sizeMax = 0.3f, speed = 0, speedMax = 2, arc = 360, radius = 0.5f, grav = 0.3f, spin = true,
                curve = new[] { 0, 0.36f, 0.12f, 1, 0.8f, 0.85f, 1, 0.3f }, from = Color.white, to = C("#ffe08f") },
        };

        // thả bi: khói lao xuống 0,15 giây (thu 1 → 0,26), quầng mờ, một chấm lửa nhỏ. unit = UnitBall
        public static readonly Burst[] Launch =
        {
            new Burst { sprite = "fx_puff", life = 0.15f, size = 0.4f, sizeMax = 0.7f, speed = 5, dir = -90, curve = new[] { 0, 1f, 1, 0.26f }, from = Color.white, to = C("#fff7d0") },
            new Burst { life = 0.15f, size = 0.7f, sizeMax = 1.2f, speed = 5, dir = -90, curve = new[] { 0, 1f, 1, 0.26f }, from = C("#fff78c", 0.38f), to = C("#ffe736", 0.38f) },
            new Burst { count = 2, life = 0.1f, lifeMax = 0.3f, size = 0.05f, sizeMax = 0.15f, speed = 1, speedMax = 5, dir = -90, arc = 19, radius = 0.13f,
                curve = new[] { 0, 1f, 1, 0 }, from = C("#ffed8f"), to = C("#ff8600") },
        };
    }
}
