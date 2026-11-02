// Sân đấu (chép Web/src/view/battle/stage.ts): nền theo hệ đảo, hai tướng dạng sticker, chữ tượng thanh, số sát thương, rung màn.
// Địch đứng trên trái, phe mình dưới phải (lật ngang). Toạ độ theo khung web 540 × 464, nhân 2 sang UI (1080 × 928).
// Tướng: prefab Items/TranTuong, hình là AolaSticker (Editor lúc Play, bản dev); không có aola thì ô trống (hình giữ chỗ vẽ tay
// đã bỏ 2026-11-02), Body vẫn chạy clip giả (lao tới 35% quãng đường) làm chỗ neo.
// Nằm trong prefab màn hình Screens/Battle; hiệu ứng (chữ nổi, tượng thanh, vòng, tia) là prefab mục, dùng xong thì tắt để dùng lại.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using Random = UnityEngine.Random;

namespace PokiClash
{
    public sealed class ClipHandle
    {
        public bool hit, done;
    }

    public sealed class StageView : MonoBehaviour
    {
        public const float SW = 540, SH = 464, K = 2;
        public static readonly Vector2[] Pos = { new Vector2(392, 418), new Vector2(158, 236) }; // phe mình, địch
        static readonly float[] Height = { 176, 150 };
        public const string Idle = "idle", Hit = "hit", Attack = "attack", Skill = "skill";

        static readonly string[] WordsHit = { "BỐP!", "CHÁT!", "BỤP!", "HỰ!", "BINH!" };
        static readonly string[] WordsBig = { "ẦM!!", "RẦM!!", "OÀNH!!" };

        public float speed = 1;
        [SerializeField] Image sky, bg, flashImg;
        [SerializeField] RectTransform root, actorLayer, fxLayer, plateLayer;
        [SerializeField] StageActor actorPrefab;
        [SerializeField] StageFx textFx, burstFx, ringFx, sparkFx;
        public RectTransform PlateLayer => plateLayer;
        float flashT = -1, flashLife = 0.35f;
        Color flashColor;
        float shake;
        readonly Actor[] actors = new Actor[2];
        readonly List<Fx> fx = new List<Fx>();
        readonly Dictionary<StageFx, List<StageFx>> idle = new Dictionary<StageFx, List<StageFx>>(); // prefab → bản sao đang tắt

        sealed class Actor
        {
            public int side;
            public HeroDef hero;
            public bool boss;
            public StageActor view;
            public RectTransform rt, body, shadow, statusRt;
            public Image bodyImg, flashImg, emblem;
            public AolaSticker aola; // bản dev
            public string clip = Idle;
            public float t, flash, dead, enter = 9, exit, hop;
            public bool loop = true;
            public ClipHandle handle;
            public Action onHit;
            public bool hitFired = true;
            public List<(StatusId, int)> statuses = new List<(StatusId, int)>();
            public readonly List<RectTransform> statusIcons = new List<RectTransform>();
            public double size = 1; // cỡ của dạng đang hiện (theo sao)
            public float H => Height[side] * (float)size * (boss ? 1.18f : 1);
        }

        sealed class Fx
        {
            public StageFx item, prefab;
            public RectTransform rt;
            public CanvasGroup cg;
            public float t, life;
            public Action<Fx, float> update; // (fx, k = t/life)
            public int side = -1;
            public float lift, size;
            public Vector2 basePos;
        }

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image skyImg, RectTransform shakeRoot, Image bgImg, RectTransform actorsRt, RectTransform fxRt, RectTransform platesRt,
            Image flash, StageActor actor, StageFx text, StageFx burst, StageFx ring, StageFx spark)
        {
            sky = skyImg;
            root = shakeRoot;
            bg = bgImg;
            actorLayer = actorsRt;
            fxLayer = fxRt;
            plateLayer = platesRt;
            flashImg = flash;
            actorPrefab = actor;
            textFx = text;
            burstFx = burst;
            ringFx = ring;
            sparkFx = spark;
        }

        // nền theo đảo: màu trời trên cùng phủ cả phần dôi (máy dài), rồi ảnh nền trận
        public void Init(ZoneDef zone)
        {
            sky.color = Theme.Hex(zone.skyTop);
            var art = App.Art ? App.Art.Get("battle_" + Keys.Of(zone.id)) : null;
            Theme.SetSprite(bg, art);
            bg.color = art ? Color.white : Theme.Hex(zone.skyBottom);
            flashImg.gameObject.SetActive(false);
        }

        // toạ độ web (gốc trên trái, y xuống) -> anchoredPosition trong khung sân (gốc trên trái)
        public static Vector2 P(float x, float y) => new Vector2(x * K, -y * K);
        public static Vector2 P(Vector2 p) => P(p.x, p.y);

        // ---------- tướng ----------

        // star: sao của tướng trên sân, chọn dạng trong dòng tiến hóa (hình và cỡ)
        public void SetActor(int side, HeroDef hero, bool boss, bool entering, int star = 1)
        {
            if (actors[side] != null)
            {
                actors[side].aola?.Destroy();
                Destroy(actors[side].rt.gameObject);
            }
            var form = App.Data.Cfg.FormOf(hero, star);
            var a = new Actor { side = side, hero = hero, size = form.size, boss = boss, enter = entering ? 0 : 9, t = Random.value * 2 };
            var v = Ui.Spawn(actorPrefab, actorLayer);
            v.name = "tuong_" + side;
            a.view = v;
            a.rt = v.Rect;
            // bóng dưới chân
            a.shadow = v.Shadow.rectTransform;
            a.shadow.sizeDelta = new Vector2(92 * (float)a.size * (side == 0 ? 1.15f : 1) * K, 22 * (float)a.size * K);
            a.shadow.anchoredPosition = new Vector2(0, 2 * K);

            float h = a.H * K;
            a.aola = AolaSticker.TryCreate(a.rt, hero, form.aola, h, side == 0);
            v.Body.gameObject.SetActive(a.aola == null);
            if (a.aola == null)
            {
                // không có hình aola (bản build, tướng chưa xuất): ô trống. Hình giữ chỗ vẽ tay đã bỏ (2026-11-02); Body vẫn
                // là chỗ neo cho chuyển động, chỉ tắt ảnh.
                var body = v.Body;
                body.sizeDelta = new Vector2(h * HeroArt.W / HeroArt.H, h);
                body.localScale = new Vector3(side == 0 ? -1 : 1, 1, 1);
                a.body = body;
                a.bodyImg = v.BodyImg;
                a.emblem = v.Emblem;
                a.flashImg = v.Flash;
                a.bodyImg.enabled = a.emblem.enabled = a.flashImg.enabled = false;
            }
            else
            {
                a.body = a.aola.Rect;
                // ảnh aola nằm ngay trên bóng, dưới dấu trạng thái (như thứ tự dựng cũ)
                a.aola.Rect.SetSiblingIndex(v.Shadow.transform.GetSiblingIndex() + 1);
            }
            a.statusRt = v.Status;
            a.statusRt.anchoredPosition = new Vector2(0, h + 8 * K);
            v.HideStatuses();
            actors[side] = a;
            Place(a);
        }

        public float Retreat(int side)
        {
            var a = actors[side];
            if (a == null) return 0;
            a.exit = 0.0001f;
            return 0.28f;
        }

        public void SetStatuses(int side, List<(StatusId, int)> st)
        {
            var a = actors[side];
            if (a == null) return;
            bool same = a.statuses.Count == st.Count;
            for (int i = 0; same && i < st.Count; i++) same = a.statuses[i].Item1 == st[i].Item1;
            a.statuses = new List<(StatusId, int)>(st);
            if (!same) BuildStatusIcons(a);
        }

        // chạy clip; onHit gọi lúc trúng đòn; handle.done khi clip xong
        public ClipHandle Play(int side, string clip, Action onHit = null)
        {
            var a = actors[side];
            var h = new ClipHandle();
            if (a == null || a.dead > 0)
            {
                onHit?.Invoke();
                h.hit = true;
                StartCoroutine(DoneAfter(h, 0.3f));
                return h;
            }
            if (a.handle != null)
            {
                a.handle.hit = a.handle.done = true;
            }
            a.clip = clip;
            a.t = 0;
            a.loop = false;
            a.onHit = onHit;
            a.hitFired = onHit == null;
            a.handle = h;
            if (onHit == null) h.hit = true;
            return h;
        }

        System.Collections.IEnumerator DoneAfter(ClipHandle h, float s)
        {
            yield return new WaitForSecondsRealtime(s / Mathf.Max(0.1f, speed));
            h.done = true;
        }

        public void Hurt(int side, bool big = false)
        {
            var a = actors[side];
            if (a == null || a.dead > 0) return;
            a.flash = 0.16f;
            shake = Mathf.Max(shake, big ? 12 : 6);
            if (a.clip == Idle || a.clip == Hit)
            {
                a.clip = Hit;
                a.t = 0;
                a.loop = false;
            }
        }

        public void Dodge(int side)
        {
            if (actors[side] != null) actors[side].hop = 0.0001f;
        }

        public void Die(int side)
        {
            if (actors[side] != null) actors[side].dead = 0.0001f;
        }

        public Vector2 Head(int side)
        {
            var p = Pos[side];
            float hh = actors[side] != null ? Height[side] * (float)actors[side].size : Height[side];
            return new Vector2(p.x, p.y - hh * 0.85f);
        }

        public Vector2 Body(int side)
        {
            var p = Pos[side];
            float hh = actors[side] != null ? Height[side] * (float)actors[side].size : Height[side];
            return new Vector2(p.x, p.y - hh * 0.45f);
        }

        // ---------- clip của hình giữ chỗ ----------

        static float ClipLen(string clip) => clip == Attack ? 0.8f : clip == Skill ? 0.9f : clip == Hit ? 0.36f : 1.2f;
        static float HitAt(string clip) => clip == Skill ? 0.55f : 0.6f;

        // ---------- hiệu ứng ----------

        // lấy một bản sao đang tắt của prefab (thiếu thì sinh), đặt lên trên cùng lớp hiệu ứng
        StageFx Take(StageFx prefab)
        {
            if (!idle.TryGetValue(prefab, out var list)) idle[prefab] = list = new List<StageFx>();
            StageFx f = null;
            while (list.Count > 0 && !f)
            {
                f = list[list.Count - 1];
                list.RemoveAt(list.Count - 1);
            }
            if (f) f.gameObject.SetActive(true);
            else f = Ui.Spawn(prefab, fxLayer);
            f.transform.SetAsLastSibling();
            return f;
        }

        void Release(Fx f)
        {
            if (!f.item) return;
            f.item.gameObject.SetActive(false);
            idle[f.prefab].Add(f.item);
        }

        Fx AddFx(StageFx item, StageFx prefab, float life, Action<Fx, float> update)
        {
            var f = new Fx { item = item, prefab = prefab, rt = item.Rect, life = life, update = update, cg = item.Group };
            f.cg.alpha = 1;
            f.cg.blocksRaycasts = false;
            f.basePos = f.rt.anchoredPosition;
            fx.Add(f);
            update(f, 0);
            return f;
        }

        StageFx FxText(string text, Color color, float size)
        {
            var f = Take(textFx);
            var t = f.Label;
            t.text = text;
            t.color = color;
            t.fontSize = size * K;
            t.rectTransform.sizeDelta = new Vector2(900, size * K * 1.4f);
            return f;
        }

        // dòng tin: chữ mới hiện ở chỗ cũ, chữ trước bị đẩy lên một dòng
        public void Text(int side, string text, Color color, float size = 26, float dy = 0)
        {
            var h = Head(side);
            foreach (var f in fx)
                if (f.side == side)
                    f.lift += size + 6;
            float sx = side == 1 ? Mathf.Min(h.x, 200) : Mathf.Max(h.x, 330);
            var item = FxText(text, color, size);
            var rt = item.Rect;
            rt.anchoredPosition = P(sx, h.y + dy + 20);
            float rot = (Random.value - 0.5f) * 0.08f * Mathf.Rad2Deg;
            rt.localEulerAngles = new Vector3(0, 0, -rot);
            var fxi = AddFx(item, textFx, 1.25f, (f, k) =>
            {
                float pop = k < 0.15f ? 0.5f + k / 0.15f * 0.7f : k < 0.25f ? 1.2f - (k - 0.15f) / 0.1f * 0.2f : 1;
                f.cg.alpha = k > 0.7f ? 1 - (k - 0.7f) / 0.3f : 1;
                f.rt.localScale = new Vector3(pop, pop, 1);
                f.rt.anchoredPosition = f.basePos + new Vector2(0, (18 * f.t + f.lift) * K);
            });
            fxi.side = side;
            fxi.size = size;
        }

        public void Text(int side, string text, string hex, float size = 26) => Text(side, text, Theme.Hex(hex), size);

        public void Number(int side, double n, Color color, bool big = false)
        {
            var b = Body(side);
            var item = FxText(((long)n).ToString(), color, big ? 46 : 34);
            var rt = item.Rect;
            rt.anchoredPosition = P(b.x + (Random.value - 0.5f) * 60, b.y - 10);
            rt.localEulerAngles = new Vector3(0, 0, (Random.value - 0.5f) * 0.3f * Mathf.Rad2Deg);
            AddFx(item, textFx, 1f, (f, k) =>
            {
                float pop = k < 0.15f ? 0.5f + k / 0.15f * 0.7f : k < 0.25f ? 1.2f - (k - 0.15f) / 0.1f * 0.2f : 1;
                f.cg.alpha = k > 0.7f ? 1 - (k - 0.7f) / 0.3f : 1;
                f.rt.localScale = new Vector3(pop, pop, 1);
                f.rt.anchoredPosition = f.basePos + new Vector2(0, 70 * f.t * K);
            });
        }

        public void Burst(int side, bool big, string word = null)
        {
            var b = Body(side);
            var words = big ? WordsBig : WordsHit;
            word ??= words[Random.Range(0, words.Length)];
            var item = Take(burstFx);
            item.Image.color = big ? Theme.Hex("#ffd24a") : Theme.Hex("#fff6c8");
            var rt = item.Rect;
            rt.sizeDelta = new Vector2(160 * K, 112 * K);
            rt.anchoredPosition = P(b.x + (Random.value - 0.5f) * 30, b.y - 20);
            rt.localEulerAngles = new Vector3(0, 0, (Random.value - 0.5f) * 0.5f * Mathf.Rad2Deg);
            item.Label.text = word;
            float sz = big ? 1.35f : 1;
            AddFx(item, burstFx, 0.6f, (f, k) =>
            {
                float pop = k < 0.2f ? 0.3f + k / 0.2f * 0.9f : 1.2f - Mathf.Min(0.2f, (k - 0.2f) * 0.5f);
                f.cg.alpha = k > 0.75f ? 1 - (k - 0.75f) / 0.25f : 1;
                f.rt.localScale = new Vector3(pop * sz, pop * sz, 1);
            });
            Spark(side, big ? Theme.Hex("#ffd24a") : Color.white);
        }

        public void Ring(int side, Color color)
        {
            var b = Body(side);
            var item = Take(ringFx);
            item.Image.color = color;
            var rt = item.Rect;
            rt.anchoredPosition = P(b);
            AddFx(item, ringFx, 0.6f, (f, k) =>
            {
                f.cg.alpha = 1 - k;
                f.rt.sizeDelta = new Vector2(140 * (0.3f + k) * K, 84 * (0.3f + k) * K);
            });
        }

        public void Ring(int side, string hex) => Ring(side, Theme.Hex(hex));

        public void Spark(int side, Color color)
        {
            var b = Body(side);
            for (int i = 0; i < 9; i++)
            {
                float a = Random.value * Mathf.PI * 2, v = 120 + Random.value * 160, s = 6 + Random.value * 8;
                var item = Take(sparkFx);
                item.Image.color = color;
                var rt = item.Rect;
                rt.sizeDelta = new Vector2((s + 6) * K, 6 * K);
                rt.localEulerAngles = new Vector3(0, 0, -a * Mathf.Rad2Deg);
                rt.anchoredPosition = P(b);
                AddFx(item, sparkFx, 0.45f, (f, k) =>
                {
                    f.cg.alpha = 1 - k;
                    float d = v * f.t;
                    f.rt.anchoredPosition = f.basePos + new Vector2(Mathf.Cos(a) * d, -Mathf.Sin(a) * d) * K;
                });
            }
        }

        public void Flash(Color color)
        {
            flashColor = color;
            flashT = 0;
            flashImg.gameObject.SetActive(true);
        }

        public void Flash(string hex = "#ffffff") => Flash(Theme.Hex(hex));

        // ---------- trạng thái trên đầu ----------

        // nhóm dấu dựng sẵn trong prefab tướng: bật nhóm có trong danh sách, xếp theo thứ tự trạng thái
        void BuildStatusIcons(Actor a)
        {
            a.view.HideStatuses();
            a.statusIcons.Clear();
            foreach (var (id, _) in a.statuses)
            {
                var g = a.view.Group(id);
                g.gameObject.SetActive(true);
                g.SetAsLastSibling();
                a.statusIcons.Add(g);
            }
        }

        void UpdateStatusIcons(Actor a)
        {
            float t = Time.unscaledTime;
            a.statusRt.gameObject.SetActive(a.dead <= 0 && a.statuses.Count > 0);
            for (int k = 0; k < a.statusIcons.Count && k < a.statuses.Count; k++)
            {
                var g = a.statusIcons[k];
                var id = a.statuses[k].Item1;
                if (id == StatusId.Stun)
                    for (int i = 0; i < g.childCount; i++)
                    {
                        float ang = t * 3 + i * Mathf.PI * 2 / 3;
                        ((RectTransform)g.GetChild(i)).anchoredPosition = new Vector2(Mathf.Cos(ang) * 30, Mathf.Sin(ang) * 8) * K;
                    }
                else if (id == StatusId.Burn)
                    for (int i = 0; i < g.childCount; i++)
                        ((RectTransform)g.GetChild(i)).anchoredPosition = new Vector2(-26 + i * 26, -30 - Mathf.Sin(t * 8 + i) * 3) * K;
                else if (id == StatusId.Regen)
                    ((RectTransform)g.GetChild(0)).anchoredPosition = new Vector2(34, -20 + (t * 30) % 30) * K;
                else if (id == StatusId.Evade)
                {
                    var img = g.GetChild(0).GetComponent<Image>();
                    var c = img.color;
                    c.a = 0.5f + Mathf.Sin(t * 6) * 0.2f;
                    img.color = c;
                    ((RectTransform)g.GetChild(0)).anchoredPosition = new Vector2(0, -80 * K);
                }
            }
        }

        void OnDestroy()
        {
            foreach (var a in actors) a?.aola?.Destroy();
        }

        // ---------- cập nhật ----------

        void Update()
        {
            float dt = Mathf.Min(0.05f, Time.unscaledDeltaTime) * speed;
            foreach (var a in actors)
            {
                if (a == null) continue;
                a.t += dt;
                a.flash = Mathf.Max(0, a.flash - dt);
                if (a.enter < 9) a.enter += dt;
                if (a.exit > 0) a.exit += dt;
                if (a.hop > 0) a.hop = a.hop > 0.5f ? 0 : a.hop + dt;
                if (a.dead > 0) a.dead += dt;
                if (!a.loop)
                {
                    float len = a.aola != null ? a.aola.Duration(a.clip) : ClipLen(a.clip);
                    float hitT = a.aola != null ? a.aola.HitTime(a.clip) : len * HitAt(a.clip);
                    if (!a.hitFired && a.t >= hitT)
                    {
                        a.hitFired = true;
                        a.onHit?.Invoke();
                        if (a.handle != null) a.handle.hit = true;
                    }
                    if (a.t >= len)
                    {
                        if (!a.hitFired)
                        {
                            a.hitFired = true;
                            a.onHit?.Invoke();
                        }
                        a.clip = Idle;
                        a.t = 0;
                        a.loop = true;
                        if (a.handle != null)
                        {
                            a.handle.hit = a.handle.done = true;
                            a.handle = null;
                        }
                    }
                }
                Place(a);
                UpdateStatusIcons(a);
            }
            shake = Mathf.Max(0, shake - dt * 40);
            root.anchoredPosition = new Vector2((Random.value - 0.5f) * shake, (Random.value - 0.5f) * shake) * K;

            for (int i = fx.Count - 1; i >= 0; i--)
            {
                var f = fx[i];
                f.t += dt;
                if (f.t >= f.life || f.rt == null)
                {
                    Release(f);
                    fx.RemoveAt(i);
                    continue;
                }
                f.update(f, f.t / f.life);
            }

            if (flashT >= 0)
            {
                flashT += dt;
                float k = flashT / flashLife;
                if (k >= 1)
                {
                    flashT = -1;
                    flashImg.gameObject.SetActive(false);
                }
                else flashImg.color = new Color(flashColor.r, flashColor.g, flashColor.b, (1 - k) * 0.7f);
            }
        }

        void Place(Actor a)
        {
            var p = Pos[a.side];
            float x = p.x, y = p.y;
            // ra sân: rơi từ trên xuống, nảy nhẹ
            if (a.enter < 0.45f)
            {
                float k = a.enter / 0.45f;
                y -= (1 - k) * (1 - k) * 260;
            }
            float alpha = 1;
            if (a.exit > 0)
            {
                alpha = Mathf.Max(0, 1 - a.exit / 0.28f);
                x += (a.side == 0 ? 1 : -1) * a.exit * 500;
            }
            if (a.hop > 0) y -= Mathf.Sin(a.hop / 0.5f * Mathf.PI) * 40;
            float rot = 0;
            if (a.dead > 0)
            {
                float k = Mathf.Min(1, a.dead / 0.7f);
                alpha = 1 - k * 0.85f;
                rot = (a.side == 0 ? 1 : -1) * k * 1.25f;
                y += k * 12;
            }
            a.rt.gameObject.SetActive(a.dead <= 1.4f);

            // quãng lao: nắn chuyển động của clip đánh tới đối thủ (aola), hình giữ chỗ thì tự nhún tới 35%
            float ox = 0, oy = 0;
            var other = Pos[a.side == 0 ? 1 : 0];
            float tx = (other.x - p.x) * 0.72f, ty = (other.y - p.y) * 0.72f;
            if (!a.loop && (a.clip == Attack || a.clip == Skill && a.aola == null))
            {
                if (a.aola != null && a.aola.Lunge(a.clip, a.t, tx, ty, out var o))
                {
                    ox = o.x;
                    oy = o.y;
                }
                else
                {
                    float len = a.aola != null ? a.aola.Duration(a.clip) : ClipLen(a.clip);
                    float hitT = a.aola != null ? a.aola.HitTime(a.clip) : len * HitAt(a.clip);
                    float u = Mathf.Min(1, a.t / Mathf.Max(0.01f, hitT));
                    float back = a.t > hitT ? Mathf.Min(1, (a.t - hitT) / Mathf.Max(0.01f, len - hitT)) : 0;
                    float lunge = Mathf.Sin(u * Mathf.PI * 0.5f) * (1 - back) * (a.clip == Skill ? 0.12f : 0.35f);
                    ox = tx * lunge;
                    oy = ty * lunge;
                }
            }
            a.rt.anchoredPosition = P(x + ox, y + oy);
            a.rt.localEulerAngles = new Vector3(0, 0, -rot * Mathf.Rad2Deg);

            if (a.aola != null)
            {
                a.aola.Show(a.loop ? Idle : a.clip, a.t, a.loop, alpha, a.dead > 0, a.flash);
            }
            else
            {
                // nhịp thở lúc đứng, giật lùi lúc trúng đòn
                float sy = 1, sx = 1;
                if (a.clip == Idle) sy = 1 + Mathf.Sin(a.t * 4.2f) * 0.025f;
                if (a.clip == Hit) sx = 1 - Mathf.Sin(a.t / 0.36f * Mathf.PI) * 0.08f;
                a.body.localScale = new Vector3((a.side == 0 ? -1 : 1) * sx, sy, 1);
                if (a.clip == Hit) a.body.anchoredPosition = new Vector2((a.side == 0 ? 1 : -1) * Mathf.Sin(a.t / 0.36f * Mathf.PI) * 10 * K, 0);
                else a.body.anchoredPosition = Vector2.zero;
                var gray = a.dead > 0 ? new Color(0.62f, 0.6f, 0.58f, alpha) : new Color(1, 1, 1, alpha);
                a.bodyImg.color = gray;
                a.emblem.color = gray;
                a.flashImg.color = new Color(1, 1, 1, Mathf.Min(1, a.flash * 5) * 0.65f * alpha);
            }
            var sc = a.view.Shadow;
            sc.color = new Color(Theme.Ink.r, Theme.Ink.g, Theme.Ink.b, 0.35f * alpha);
            // bóng đứng yên ở chân khi lao
            a.shadow.anchoredPosition = new Vector2(-ox * K, (y + oy - p.y - 2) * K);
        }
    }
}
