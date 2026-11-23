// Chim, bướm, ong trên màn Nhà (người dùng 2026-11-23: "thêm chim chóc, bướm ong ... vào cho sinh động"). Ảnh vẽ bằng
// ArtGen/Home/life/make_life.py (tô phẳng, viền mực như lá gió) ở Resources/HomeLife; mỗi con là một Image sinh từ treePrefab (prefab ảnh
// thường) trong lớp hạt, dùng lại suốt phiên. Chỉ quanh khung nhìn: con nào ra quá xa khung thì đặt lại chỗ khác trong khung.
// - Bướm (5): bay lượn chậm quanh một điểm trên đất đã mở, vỗ cánh bằng co giãn ngang, đầu quay theo hướng bay, thỉnh thoảng đậu
//   xuống khép mở cánh chậm.
// - Ong (4): bay số 8 nhanh quanh ruộng, vườn, bồn hoa, Cây bi (không có thì đất trống), vài giây đổi chỗ; cánh đập bằng hai ảnh.
// - Chim: đàn 2–5 con bay ngang khung nhìn mỗi 10–22 giây, vỗ cánh 3 khung rồi lượn; cây lắc mạnh đôi khi có chim vụt ra (BirdFrom).
// - Đêm (DayCycle) thì tan hết, sáng lại hiện.
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed partial class HomeScene
    {
        sealed class Critter
        {
            public Image img;
            public RectTransform rt;
            public int kind;          // 0 bướm, 1 ong, 2 chim
            public Sprite[] frames;
            public Vector2 pos, vel, home, target; // px bản đồ (y xuống)
            public float t, ph, speed, rest, alt, wait, fade, size, dir, flapLeft;
            public bool on, gliding;
            public int frame = -1;
        }

        const int ButterflyN = 5, BeeN = 4;
        readonly List<Critter> critters = new List<Critter>();
        Sprite[][] butterflySp;
        Sprite[] beeSp, birdA, birdB;
        float flockWait = 5f, lifeAlpha = 1;

        static float Rnd(float lo, float hi) => UnityEngine.Random.Range(lo, hi);

        Sprite[] LoadLife(string prefix, int n)
        {
            var list = new List<Sprite>();
            for (int i = 1; i <= n; i++)
            {
                var s = Resources.Load<Sprite>("HomeLife/" + prefix + i);
                if (s) list.Add(s);
            }
            return list.ToArray();
        }

        void LifeEnter()
        {
            if (beeSp == null)
            {
                var b = LoadLife("butterfly_", 4);
                butterflySp = new Sprite[b.Length][];
                for (int i = 0; i < b.Length; i++) butterflySp[i] = new[] { b[i] };
                beeSp = LoadLife("bee_", 2);
                birdA = LoadLife("bird_a_", 3);
                birdB = LoadLife("bird_b_", 3);
            }
            swayClock = Rnd(0f, 50f);
            flockWait = Rnd(3f, 7f);
            lifeAlpha = 1 - Mathf.Clamp01((DayCycle.Night(DayCycle.Hour) - 0.35f) / 0.4f); // vào màn lúc đêm: không hiện rồi mới tan
            lifeReady = false; // đặt chỗ khi khung nhìn đã có (LandView đặt máy xong)
        }

        bool lifeReady;

        void LifeExit()
        {
            foreach (var f in flyTrees)
                if (f.rt) Destroy(f.rt.gameObject);
            flyTrees.Clear();
            shakeImg = null;
            foreach (var c in critters) Hide(c);
        }

        void LifeTick(float dt)
        {
            SwayTrees(dt);
            TickFlying(dt);
            TickCritters(dt);
        }

        // ---------- dựng, đặt chỗ ----------

        Critter Make(int kind, Sprite[] frames, float size)
        {
            if (!treePrefab || !fxLayer || frames == null || frames.Length == 0) return null;
            var c = critters.Find(x => !x.on && x.kind == kind && x.img);
            if (c == null)
            {
                var img = Ui.Spawn(treePrefab, fxLayer);
                img.raycastTarget = false;
                img.preserveAspect = false;
                c = new Critter { img = img, rt = img.rectTransform, kind = kind };
                c.rt.anchorMin = c.rt.anchorMax = new Vector2(0, 1);
                c.rt.pivot = new Vector2(0.5f, 0.5f);
                critters.Add(c);
            }
            c.frames = frames;
            c.frame = -1;
            c.size = size;
            c.on = true;
            c.t = 0;
            c.ph = Rnd(0f, 6.2832f);
            c.fade = 0;
            c.rest = 0;
            c.gliding = false;
            c.img.gameObject.SetActive(true);
            c.rt.SetAsLastSibling();
            SetFrame(c, 0);
            return c;
        }

        void SetFrame(Critter c, int i)
        {
            i = Mathf.Clamp(i, 0, c.frames.Length - 1);
            if (c.frame == i) return;
            c.frame = i;
            var s = c.frames[i];
            Theme.SetSprite(c.img, s);
            var r = s.rect.size;
            c.rt.sizeDelta = r * (c.size / Mathf.Max(r.x, r.y));
        }

        void Hide(Critter c)
        {
            c.on = false;
            if (c.img) c.img.gameObject.SetActive(false);
        }

        // điểm bản đồ ngẫu nhiên trong phần khung không bị thanh trên / dưới che, ưu tiên đất đã mở đi được
        Vector2 OpenPointInView()
        {
            var size = landView.ViewSize;
            Vector2 m = Vector2.zero;
            for (int k = 0; k < 14; k++)
            {
                var v = new Vector2(Rnd(0.08f, 0.92f) * size.x, Rnd(TopInset + 60, Mathf.Max(TopInset + 80, size.y - BottomInset - 40)));
                m = landView.ViewToMap(v);
                if (WalkableAt(CellF(m))) return m;
            }
            return m;
        }

        // chỗ ong tìm tới: ruộng, vườn, bồn hoa, Cây bi đang trong khung; không có thì đất trống
        Vector2 FlowerPointInView()
        {
            var h = S.home;
            Vector2 best = Vector2.zero;
            int seen = 0;
            foreach (var b in h.buildings)
            {
                var df = Home.Def(D.Cfg, b.def);
                if (df == null || !(b.def == "field" || b.def == "orchard" || b.def == "flowerbed" || df.kind == "tree")) continue;
                var m = CellTop(b.gx + df.size / 2f, b.gy + df.size / 2f) - new Vector2(0, df.size * CH * 0.35f);
                if (!InView(m, 0, -40)) continue;
                if (UnityEngine.Random.Range(0, ++seen) == 0) best = m;
            }
            return seen > 0 ? best : OpenPointInView();
        }

        void PlaceButterfly(Critter c)
        {
            c.home = OpenPointInView();
            c.pos = c.home + UnityEngine.Random.insideUnitCircle * 90;
            c.target = c.home + UnityEngine.Random.insideUnitCircle * 220;
            c.vel = Vector2.zero;
            c.speed = Rnd(55f, 80f);
            c.alt = Rnd(30f, 60f);
            c.fade = 0;
        }

        void PlaceBee(Critter c)
        {
            c.home = FlowerPointInView();
            c.pos = c.home + UnityEngine.Random.insideUnitCircle * 60;
            c.wait = Rnd(5f, 9f);
            c.alt = 30;
            c.fade = 0;
        }

        // đàn chim bay ngang khung nhìn
        void SpawnFlock()
        {
            var size = landView.ViewSize;
            int n = UnityEngine.Random.Range(2, 6);
            float dir = UnityEngine.Random.value < 0.5f ? 1 : -1;
            var skin = UnityEngine.Random.value < 0.5f ? birdA : birdB;
            if (skin == null || skin.Length == 0) return;
            float vy = Rnd(TopInset + 80, size.y * 0.62f);
            var lead = landView.ViewToMap(new Vector2(dir > 0 ? -90 : size.x + 90, vy));
            float speed = Rnd(230f, 290f);
            for (int k = 0; k < n; k++)
            {
                var c = Make(2, skin, Rnd(60f, 70f));
                if (c == null) return;
                c.dir = dir;
                c.pos = lead + new Vector2(-dir * k * Rnd(42f, 70f), (k % 2 == 0 ? 1 : -1) * k * Rnd(16f, 30f));
                c.vel = new Vector2(dir * speed * Rnd(0.96f, 1.04f), Rnd(-18f, 18f));
                c.flapLeft = Rnd(0.9f, 1.6f);
                c.fade = 1;
            }
        }

        // chim vụt ra từ tán cây (cây lắc mạnh): bay chếch lên rồi đi ngang
        void BirdFrom(Vector2 canopy)
        {
            if (lifeAlpha < 0.5f) return;
            var skin = UnityEngine.Random.value < 0.5f ? birdA : birdB;
            var c = Make(2, skin, Rnd(58f, 66f));
            if (c == null) return;
            c.dir = UnityEngine.Random.value < 0.5f ? 1 : -1;
            c.pos = canopy;
            c.vel = new Vector2(c.dir * Rnd(150f, 210f), -Rnd(150f, 210f));
            c.flapLeft = 1.4f;
            c.fade = 0.2f;
        }

        // ---------- mỗi khung ----------

        void TickCritters(float dt)
        {
            if (!landView || !landView.On || !fxLayer || beeSp == null) return;
            var size = landView.ViewSize;
            if (size.x <= 0) return;
            // đêm: tan hết (chạng vạng mờ dần), sáng lại hiện
            float night = DayCycle.Night(DayCycle.Hour);
            float want = 1 - Mathf.Clamp01((night - 0.35f) / 0.4f);
            lifeAlpha = Mathf.MoveTowards(lifeAlpha, want, dt * 0.5f);
            if (!lifeReady && lifeAlpha > 0.01f)
            {
                lifeReady = true;
                if (butterflySp != null)
                    for (int i = 0; i < ButterflyN && butterflySp.Length > 0; i++)
                    {
                        var c = Make(0, butterflySp[i % butterflySp.Length], Rnd(42f, 50f));
                        if (c != null) PlaceButterfly(c);
                    }
                for (int i = 0; i < BeeN; i++)
                {
                    var c = Make(1, beeSp, Rnd(28f, 32f));
                    if (c != null) PlaceBee(c);
                }
            }
            if ((flockWait -= dt) <= 0)
            {
                flockWait = Rnd(10f, 22f);
                if (lifeAlpha > 0.5f && mode == Mode.Normal) SpawnFlock();
            }
            foreach (var c in critters)
            {
                if (!c.on || !c.img) continue;
                c.t += dt;
                c.fade = Mathf.MoveTowards(c.fade, 1, dt * 1.6f);
                var v = landView.ToView(c.pos);
                bool far = v.x < -260 || v.x > size.x + 260 || v.y < -260 || v.y > size.y + 260;
                if (c.kind == 2)
                {
                    if (far && c.t > 0.5f)
                    {
                        Hide(c);
                        continue;
                    }
                    TickBird(c, dt);
                }
                else if (far && c.t > 1.5f)
                {
                    // bướm, ong ra quá xa khung (người chơi kéo bản đồ đi): đặt lại trong khung, hiện dần
                    c.t = 0;
                    if (c.kind == 0) PlaceButterfly(c);
                    else PlaceBee(c);
                }
                else if (c.kind == 0) TickButterfly(c, dt);
                else TickBee(c, dt);
                c.img.color = new Color(1, 1, 1, c.fade * lifeAlpha);
                bool vis = lifeAlpha > 0.01f;
                if (c.img.enabled != vis) c.img.enabled = vis;
            }
        }

        // hướng bay (px bản đồ, y xuống) → góc cho ảnh đầu hướng lên
        static float Heading(Vector2 vel) => Mathf.Atan2(-vel.y, vel.x) * Mathf.Rad2Deg - 90;

        void TickButterfly(Critter c, float dt)
        {
            float flap;
            if (c.rest > 0)
            {
                // đậu: hạ xuống sát đất, khép mở cánh chậm
                c.rest -= dt;
                c.alt = Mathf.MoveTowards(c.alt, 4, 70 * dt);
                flap = 0.55f + 0.45f * Mathf.Cos(c.t * 2.4f);
                if (c.rest <= 0) c.target = c.home + UnityEngine.Random.insideUnitCircle * 220;
            }
            else
            {
                var to = c.target - c.pos;
                if (to.magnitude < 16)
                {
                    if (UnityEngine.Random.value < 0.3f) c.rest = Rnd(1.2f, 3.2f);
                    c.target = c.home + UnityEngine.Random.insideUnitCircle * 220;
                }
                var wantV = to.normalized * c.speed;
                wantV += new Vector2(-wantV.y, wantV.x).normalized * (Mathf.Sin(c.t * 2.7f + c.ph) * c.speed * 0.6f); // lượn lắc ngang đường bay
                c.vel = Vector2.Lerp(c.vel, wantV, 1 - Mathf.Exp(-2.2f * dt));
                c.pos += c.vel * dt;
                c.alt = Mathf.Lerp(c.alt, 44 + 16 * Mathf.Sin(c.t * 1.9f + c.ph), 1 - Mathf.Exp(-3f * dt));
                flap = Mathf.Abs(Mathf.Cos(c.t * Mathf.PI * 5.2f + c.ph));
            }
            float bob = c.rest > 0 ? 0 : 5 * Mathf.Sin(c.t * Mathf.PI * 10.4f + c.ph); // nhấp lên theo nhịp đập cánh
            c.rt.anchoredPosition = new Vector2(c.pos.x, -c.pos.y + c.alt + bob);
            c.rt.localScale = new Vector3(0.18f + 0.82f * flap, 1, 1);
            if (c.vel.sqrMagnitude > 25 && c.rest <= 0)
                c.rt.localRotation = Quaternion.Slerp(c.rt.localRotation, Quaternion.Euler(0, 0, Heading(c.vel)), 1 - Mathf.Exp(-5f * dt));
        }

        void TickBee(Critter c, float dt)
        {
            if ((c.wait -= dt) <= 0)
            {
                c.wait = Rnd(5f, 9f);
                c.home = FlowerPointInView();
            }
            // số 8 quanh chỗ đang tìm, rung lắc nhỏ; dời chỗ thì bay thẳng tới (giới hạn tốc độ)
            var target = c.home + new Vector2(Mathf.Sin(c.t * 2.6f + c.ph) * 58, Mathf.Sin(c.t * 5.2f + c.ph) * 22)
                         + new Vector2(Mathf.Sin(c.t * 17f + c.ph * 3) * 4, Mathf.Sin(c.t * 13f + c.ph) * 4);
            var step = Vector2.Lerp(c.pos, target, 1 - Mathf.Exp(-3.5f * dt)) - c.pos;
            float maxStep = 230 * dt;
            if (step.magnitude > maxStep) step = step.normalized * maxStep;
            c.pos += step;
            if (dt > 0) c.vel = Vector2.Lerp(c.vel, step / dt, 1 - Mathf.Exp(-10f * dt));
            c.alt = 30 + 6 * Mathf.Sin(c.t * 7f + c.ph);
            SetFrame(c, (int)(c.t * 36) % 2);
            c.rt.anchoredPosition = new Vector2(c.pos.x, -c.pos.y + c.alt);
            c.rt.localScale = Vector3.one;
            if (c.vel.sqrMagnitude > 25) c.rt.localRotation = Quaternion.Slerp(c.rt.localRotation, Quaternion.Euler(0, 0, Heading(c.vel)), 1 - Mathf.Exp(-9f * dt));
        }

        void TickBird(Critter c, float dt)
        {
            // vỗ cánh (khung 1 → 2 → 3 → 2) rồi lượn (khung 1), xen kẽ; mới vụt ra thì vỗ nhanh và ngóc lên
            c.flapLeft -= dt;
            if (c.flapLeft <= 0)
            {
                c.gliding = !c.gliding;
                c.flapLeft = c.gliding ? Rnd(0.6f, 1.2f) : Rnd(0.9f, 1.7f);
            }
            if (c.gliding) SetFrame(c, 0);
            else
            {
                int f = (int)((c.t + c.ph) * 11f) % 4;
                SetFrame(c, f == 3 ? 1 : f);
            }
            // chim vụt ra: sức ngóc lên giảm dần về bay ngang
            c.vel.y = Mathf.MoveTowards(c.vel.y, 0, 120 * dt);
            c.pos += c.vel * dt;
            float wave = 12 * Mathf.Sin(c.t * 1.4f + c.ph);
            c.rt.anchoredPosition = new Vector2(c.pos.x, -c.pos.y + wave);
            c.rt.localScale = new Vector3(c.dir, 1, 1);
            c.rt.localRotation = Quaternion.Euler(0, 0, Mathf.Clamp(-c.vel.y * 0.12f, -25, 25) * c.dir);
        }
    }
}
