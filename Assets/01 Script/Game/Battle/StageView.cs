// Sân đấu (chép Web/src/view/battle/stage.ts): nền theo hệ đảo (đảo có bộ sàn đấu thì theo ải, kèm phần động ArenaAnim), hai tướng dạng sticker, chữ tượng thanh, số sát thương, rung màn.
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
        // cast: clip ngắn của chiêu bắn tia (tướng aola có khai, AolaSticker.Beam)
        public const string Idle = "idle", Hit = "hit", Attack = "attack", Skill = "skill", Cast = "cast";

        static readonly string[] WordsHit = { "BỐP!", "CHÁT!", "BỤP!", "HỰ!", "BINH!" };
        static readonly string[] WordsBig = { "ẦM!!", "RẦM!!", "OÀNH!!" };

        public float speed = 1; // nhịp sân ngoài lúc ra đòn: giây sân mỗi giây thật (BattleController đặt)
        public float fast = 1;  // công cụ thử chạy nhanh gấp fast, cả lúc ra đòn (BattleController.FastForward)
        [SerializeField] Image sky, bg, flashImg;
        [SerializeField] RectTransform root, actorLayer, fxLayer, plateLayer;
        [SerializeField] StageActor actorPrefab;
        [SerializeField] StageFx textFx, burstFx, ringFx, sparkFx;
        [SerializeField] StageFx beamFx; // tia nước của chiêu bắn (Items/TiaNuoc, menu "PokiClash/Prefab/Sàn đấu: tia nước của chiêu bắn")
        [SerializeField] StageFx imageFx; // ảnh hiệu ứng rời, đổi ảnh lúc dùng (Items/AnhHieuUng, cùng menu)
        [SerializeField] Sprite beamSplash, beamDrops, beamRipple, beamSparkle; // nổ nước, giọt, vòng sóng, lấp lánh (Assets/03 Art/Fx)
        // tia riêng của 3 boss cuối đảo Thủy (người dùng dặn 2026-11-07): ảnh thân tia theo tên (anim.json "cast.tia": tia_bang,
        // tia_xoay, tia_trieu) và hiệu ứng phụ của từng kiểu (mảnh băng, vòng xoáy, vòng sóng âm); cùng menu gán
        [SerializeField] Sprite[] beamStyles;
        [SerializeField] Sprite beamShard, beamVortex, beamSoundRing;
        public RectTransform PlateLayer => plateLayer;
        float flashT = -1, flashLife = 0.35f;
        Color flashColor;
        float shake;
        // cảm giác trúng (skill pokiclash-hero-fx): clip .atomik khai impact* thì lúc trúng sân khựng, màn rung kiểu trauma, con bị
        // đánh bật lùi kèm nghiêng. Tướng không khai thì như cũ.
        float freeze, trauma;
        const float FreezeSlow = 0.06f, RecoilLen = 0.38f, TraumaDecay = 1.3f, TraumaX = 12, TraumaY = 8;
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
            public float recoil = -1, push; // bật lùi do cú trúng có impact: giây sân đã qua (-1 = không), quãng theo chiều cao
            public bool loop = true;
            public ClipHandle handle;
            public Action onHit;
            public bool hitFired = true;
            public List<(StatusId, int)> statuses = new List<(StatusId, int)>();
            public readonly List<RectTransform> statusIcons = new List<RectTransform>();
            public double size = 1; // cỡ của dạng đang hiện (theo sao)
            public int form, forms = 1; // dạng đang hiện trong dòng tiến hóa và số dạng (cỡ tia của chiêu bắn)
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

        // nền theo đảo: màu trời trên cùng phủ cả phần dôi (máy dài), rồi ảnh nền trận (FitBg: ảnh vẽ dư trời thì chìa lên phần dôi).
        // Đảo có bộ sàn đấu (ArtGen/BattleBG/build_thuy.py) thì theo ải: ải mini boss, boss "battle_<đảo>_s<ải>", rồi chặng
        // "battle_<đảo>_c<chặng>"; không có thì nền hệ. Sàn đấu có phần động (ArenaAnim) và màu trời riêng. stage null (thử thách huy
        // hiệu, hang): nền hệ.
        public void Init(ZoneDef zone, StageDef stage = null)
        {
            this.zone = zone;
            this.stage = stage;
            arenaArt = null;
            ApplyArena(1);
            flashImg.gameObject.SetActive(false);
        }

        // boss tiến hóa: nền dạng sau ("…_s70_2", "…_s70_3") nếu có
        public void SetPhase(int phase) => ApplyArena(phase);

        [SerializeField] ArenaAnim arena; // lớp "PhanDong" ngay trên ảnh nền (menu "PokiClash/Prefab/Sàn đấu: lớp phần động")
        ZoneDef zone;
        StageDef stage;
        string arenaArt;

        static string ArenaArt(ZoneDef zone, StageDef st, int phase)
        {
            string z = "battle_" + Keys.Of(zone.id);
            if (st == null || !App.Art) return z;
            string s = $"{z}_s{st.idx}";
            if (phase > 1 && HasArena($"{s}_{phase}")) return $"{s}_{phase}";
            if (HasArena(s)) return s;
            string c = $"{z}_c{st.chapter + 1:00}";
            return HasArena(c) ? c : z;
        }

        // nền có ảnh riêng, hoặc mượn ảnh nền khác: đảo Mộc dùng chung nền (ArtGen/BattleBG/build_moc.py), khoá trong arena_fx.json có
        // "use" (khoá nền có ảnh) và "tint" (màu phủ ảnh: ải mini boss, boss dạng 2, 3)
        static bool HasArena(string name) => App.Art.HasArt(name) || ArenaAnim.Use(name.Substring("battle_".Length)) != null;

        void ApplyArena(int phase)
        {
            string name = ArenaArt(zone, stage, phase);
            if (name == arenaArt) return;
            arenaArt = name;
            string key = name.Substring("battle_".Length);
            string use = ArenaAnim.Use(key);
            var art = App.Art ? App.Art.Get(use != null ? "battle_" + use : name) : null;
            Theme.SetSprite(bg, art);
            string tint = ArenaAnim.Tint(key);
            bg.color = art ? (tint != null ? Theme.Hex(tint) : Color.white) : Theme.Hex(zone.skyBottom);
            sky.color = Theme.Hex(ArenaAnim.Sky(key) ?? zone.skyTop);
            if (arena) arena.Bind(key);
            fitRoom = -1;
            FitBg();
        }

        // Máy dài hơn 9:16 thì vùng sân cao thêm phía trên khung 1080 × 928 (9:20 thêm 480, 21:9 thêm 600). Ảnh nền rộng 1080, cao theo
        // ảnh, đáy ảnh trùng đáy khung: ảnh cũ cao đúng 928 thì như trước (phần dôi là màu trời); ảnh vẽ dư trời (ArtGen/BattleBG/
        // build_troi.py, 1080 × 1528) thì phần trên chìa lên phủ phần dôi, máy thấp hơn cắt bớt từ trên (Image Filled, không méo).
        // Toạ độ tướng, phần động, bảng vẫn theo khung. Chớp sáng phủ cả vùng sân. Chừa thêm ShakePad cho mép trên khỏi hở lúc rung
        // (phần chừa nằm dưới thanh trên, thanh trên vẽ sau vùng sân).
        const float ShakePad = 16;
        float fitRoom = -1;

        void FitBg()
        {
            var area = transform.parent as RectTransform; // Vung san
            float room = (area ? area.rect.height : SH * K) + ShakePad;
            if (Mathf.Approximately(room, fitRoom)) return;
            fitRoom = room;
            float w = SW * K;
            var s = bg.sprite;
            float h = s ? w * s.rect.height / s.rect.width : SH * K;
            var rt = bg.rectTransform;
            rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0);
            rt.anchoredPosition = Vector2.zero;
            rt.sizeDelta = new Vector2(w, h);
            bg.type = Image.Type.Filled;
            bg.fillMethod = Image.FillMethod.Vertical;
            bg.fillOrigin = (int)Image.OriginVertical.Bottom;
            bg.fillAmount = Mathf.Min(1, room / h);
            var fr = flashImg.rectTransform;
            fr.anchorMin = Vector2.zero;
            fr.anchorMax = new Vector2(1, 0);
            fr.pivot = new Vector2(0.5f, 0);
            fr.anchoredPosition = Vector2.zero;
            fr.sizeDelta = new Vector2(0, Mathf.Max(room, SH * K));
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
            a.form = hero.FormIndex(App.Data.Cfg.formStars, star);
            a.forms = Mathf.Max(1, hero.forms.Length);
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
            if (clip == Skill && arena) arena.Flare(); // sàn đấu bừng sáng theo chiêu, Tuyệt kỹ
            if (clip != Idle && clip != Hit) a.rt.SetAsLastSibling(); // con đang ra đòn nằm trên con kia
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
            yield return Wait(s);
            h.done = true;
        }

        // chờ s giây sân (theo nhịp lúc đó: đang ra đòn thì chậm cùng sân); sân tắt thì thôi chờ
        public System.Collections.IEnumerator Wait(float s)
        {
            float end = Clock + s;
            while (this && isActiveAndEnabled && Clock < end) yield return null;
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

        static float ClipLen(string clip) => clip == Attack ? 0.8f : clip == Skill ? 0.9f : clip == Hit ? 0.36f :
            clip == Cast ? AolaSticker.CastLen : 1.2f;
        static float HitAt(string clip) => clip == Skill ? 0.55f : clip == Cast ? 0.5f : 0.6f;

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

        // clip đang chạy của tướng side (menu thử chụp lúc ra đòn)
        public string ClipOf(int side) => actors[side] == null || actors[side].loop ? Idle : actors[side].clip;

        // Lúc ra đòn cả sân chậm lại cho rõ animation (người dùng 2026-11-04, thay cách chỉ kéo chậm clip chiêu của 2026-11-03): tướng đang
        // chạy clip đánh thì sân chạy ×1,3 tốc độ gốc aola; chiêu bắn (động tác bắn, tia bay, tan) và clip CHIÊU (tuyệt kỹ, chiêu mana của
        // boss làm riêng) ×1. Cả hai tướng, chữ nổi, hiệu ứng, rung và chờ của BattlePlayer (Wait) cùng chậm. Vào nhịp chậm ngay lúc clip
        // bắt đầu, ra lại nhịp sân mượt trong SlowEase giây thật.
        const float AttackPace = 1.3f, SkillPace = 1f, SlowEase = 0.1f;
        float slow = 1;  // hệ số đang nhân vào nhịp sân (1: nhịp thường)
        float skillHold; // giây sân còn giữ nhịp chiêu sau clip bắn (tia còn bay, tan)
        public float Clock { get; private set; } // giây sân đã chạy

        // Chiêu mana bắn tia (người dùng 2026-11-03): mặc định của mọi tướng, quái thường, phần lớn mini boss; số ít boss làm riêng
        // khai "mana": "clip" trong anim.json (AolaSticker.ManaUsesClip) thì phát clip CHIÊU như cũ.

        public bool CanBeam(int side) => beamFx && actors[side] != null && !(actors[side].aola?.ManaUsesClip ?? false);

        // Tia từ chỗ bắn của side tới thân đối thủ (người dùng 2026-11-03: to, có hoạt cảnh, tan cho đẹp):
        // - phóng: nổ nước nhỏ và lấp lánh ở chỗ bắn;
        // - bay: thân tia vươn ra (đầu bọt dẫn trước), gợn sóng liên tục, lõi sáng mảnh hơn bên trong, giọt nước văng dọc đường;
        // - trúng (lúc đầu tia tới nơi): nổ nước lớn, giọt văng, vòng sóng loang dưới chân đối thủ, lấp lánh, rung sân nhẹ;
        // - tan: đuôi tia rút dần về phía đối thủ (nước chảy hết vào chỗ trúng), mảnh dần rồi mờ.
        // Chỗ bắn và cỡ tia: dạng có clip bắn thì theo anim.json (AolaSticker.Beam); không thì từ trước ngực, cỡ to dần theo dạng trong
        // dòng (một dạng: vừa), boss to hơn. Ảnh nước dùng chung; tướng hệ khác tạm nhuộm màu hệ tới khi có ảnh riêng.
        // Trả về thời gian tới nơi (giây sân).
        public float Beam(int side)
        {
            var a = actors[side];
            if (!beamFx || a == null) return 0;
            int other = side == 0 ? 1 : 0;
            Vector2 m;
            float scale;
            if (a.aola == null || !a.aola.Beam(out m, out scale))
            {
                var dir = Pos[other].x < Pos[side].x ? -1f : 1f;
                m = new Vector2(dir * a.H * 0.3f, -a.H * 0.5f);
                scale = a.forms <= 1 ? 1f : 0.7f + 0.7f * a.form / (a.forms - 1f);
                if (a.boss) scale *= 1.2f;
            }
            var from = Pos[side] + m;
            var to = Body(other);
            var d = to - from;
            float len = d.magnitude, ang = Mathf.Atan2(d.y, d.x);
            var nrm = len > 0 ? new Vector2(-d.y, d.x) / len : Vector2.up; // pháp tuyến (web)
            var tint = a.hero.elem == Elem.Thuy ? Color.white : Color.Lerp(Color.white, Theme.Of(a.hero.elem), 0.75f);
            float flipY = d.x < 0 ? -1 : 1; // bắn sang trái thì lật dọc để vệt sáng vẫn ở trên
            // bề dày tia (đơn vị web): dạng đầu (cỡ 0.7) 84, to dần chậm hơn cỡ (dạng cuối cỡ 1.4 khoảng 127, quái một dạng 104)
            float h = 84 * Mathf.Pow(scale / 0.7f, 0.6f);
            // cỡ hiệu ứng phụ (nổ, giọt, lấp lánh): to dần còn chậm hơn, để không che thân tướng bắn
            float g = Mathf.Pow(scale / 0.7f, 0.4f);
            // tia riêng (3 boss cuối đảo Thủy): ảnh thân tia khác, giữ lâu hơn, thêm hiệu ứng phụ theo kiểu
            string style = a.aola != null ? a.aola.BeamStyle : null;
            Sprite styleArt = null;
            if (!string.IsNullOrEmpty(style) && beamStyles != null)
                foreach (var s in beamStyles)
                    if (s && s.name == style)
                    {
                        styleArt = s;
                        break;
                    }
            var bodyArt = styleArt ? styleArt : (beamFx.Image ? beamFx.Image.sprite : null);
            if (styleArt) tint = Color.white;
            const float grow = 0.2f, shrink = 0.22f;
            float hold = styleArt ? 0.45f : 0.3f, life = grow + hold + shrink;
            // tia xoắn vẽ vòng xoắn kín cả bề dày ảnh, tia triều đã có vòng sóng âm đi kèm: không làm dày thêm, để dạng cuối
            // không che thân tướng bắn (soi tour 2026-11-07)
            if (styleArt) h *= style == "tia_xoay" ? 0.85f : style == "tia_trieu" ? 1f : 1.15f;
            skillHold = Mathf.Max(skillHold, life);

            // thân tia và lõi sáng: vẽ đoạn [đuôi, đầu] của đường bắn, đầu vươn ra nhanh, đuôi rút về đối thủ lúc tan
            for (int layer = 0; layer < 2; layer++)
            {
                bool core = layer == 1;
                var item = Take(beamFx);
                if (item.Image)
                {
                    // bản sao lấy từ hàng chờ có thể còn ảnh tia riêng của lần trước: luôn gán lại
                    if (bodyArt && item.Image.sprite != bodyArt) Theme.SetSprite(item.Image, bodyArt);
                    item.Image.color = core ? Color.Lerp(tint, Color.white, 0.7f) : tint;
                }
                item.Rect.pivot = new Vector2(0, 0.5f);
                float thick = core ? 0.42f : 1f, phase = core ? 1.7f : 0f;
                AddFx(item, beamFx, life, (f, k) =>
                {
                    float t = k * life;
                    float head = Mathf.Min(1, t / grow);
                    head = 1 - (1 - head) * (1 - head) * (1 - head);
                    float tail = Mathf.Clamp01((t - grow - hold) / shrink);
                    tail *= tail;
                    var p0 = from + d * tail;
                    float wob = 1 + 0.12f * Mathf.Sin(t * 38 + phase) + 0.06f * Mathf.Sin(t * 71 + phase);
                    f.rt.anchoredPosition = P(p0);
                    f.rt.sizeDelta = new Vector2(Mathf.Max(1, len * (head - tail)) * K, h * thick * wob * (1 - 0.6f * tail) * K);
                    f.rt.localEulerAngles = new Vector3(0, 0, -ang * Mathf.Rad2Deg + Mathf.Sin(t * 23 + phase) * 1.5f);
                    f.rt.localScale = new Vector3(1, flipY, 1);
                    f.cg.alpha = (core ? 0.6f : 1f) * (tail > 0.6f ? (1 - tail) / 0.4f : 1);
                });
            }

            // phóng: nổ nước nhỏ, lấp lánh ở chỗ bắn (nhỏ hơn đầu tướng)
            Pop(beamSplash, from, 64 * g, tint, 0, 0.3f, 0.4f, 1.1f, Random.value * 360);
            Pop(beamSparkle, from - nrm * 30 * g, 34 * g, Color.white, 0.03f, 0.3f, 0.3f, 1.2f, 0);
            // bay: giọt nước văng ra hai bên khi đầu tia đi qua (từ quá nửa đường, xa thân tướng bắn)
            for (int i = 0; i < 4; i++)
            {
                float u = 0.4f + 0.13f * i;
                float side2 = i % 2 == 0 ? 1 : -1;
                var at = from + d * u + nrm * side2 * h * 0.35f;
                var fly = nrm * side2 * 50 * g * (0.7f + Random.value * 0.5f) + d.normalized * 20 * g;
                float delay = grow * (1 - Mathf.Pow(1 - u, 1f / 3f));
                Drift(beamDrops, at, fly, 30 * g, tint, delay, 0.45f, Random.value * 360);
            }
            if (styleArt) StyleBeamFx(style, from, d, nrm, h, g, grow, hold);
            var victim = actors[other];
            StartCoroutine(BeamHit(other, to, victim != null ? victim.H : Height[other], g, tint, grow));
            if (styleArt) StartCoroutine(StyleBeamHit(style, other, to, victim != null ? victim.H : Height[other], g, grow));
            return grow;
        }

        // hiệu ứng phụ dọc đường tia của kiểu tia riêng: tia băng văng mảnh băng, tia xoắn có vòng xoáy quay dọc thân,
        // tia triều có vòng sóng âm chuông đồng nở lần lượt
        void StyleBeamFx(string style, Vector2 from, Vector2 d, Vector2 nrm, float h, float g, float grow, float hold)
        {
            switch (style)
            {
                case "tia_bang":
                    for (int i = 0; i < 8; i++)
                    {
                        float u = 0.25f + 0.09f * i;
                        float s2 = i % 2 == 0 ? 1 : -1;
                        var at = from + d * u + nrm * s2 * h * 0.4f;
                        var fly = nrm * s2 * 70 * g * (0.6f + Random.value * 0.6f) + d.normalized * 30 * g;
                        Drift(beamShard, at, fly, 40 * g, Color.white, grow * u, 0.55f, Random.value * 360);
                    }
                    break;
                case "tia_xoay":
                    // vòng đầu cách chỗ bắn một khúc, cỡ bằng bề dày tia: không trùm đầu tướng bắn ở dạng cuối
                    for (int i = 0; i < 5; i++)
                    {
                        float u = 0.35f + 0.14f * i;
                        Spin(beamVortex, from + d * u, h, Color.white, grow * u, hold + 0.1f, i % 2 == 0 ? 540 : -540);
                    }
                    break;
                case "tia_trieu":
                    // vòng theo g (to chậm hơn bề dày tia), bắt đầu từ quá nửa đường để không trùm tướng bắn
                    for (int i = 0; i < 3; i++)
                    {
                        float u = 0.42f + 0.18f * i;
                        Pop(beamSoundRing, from + d * u, 110 * g, Color.white, grow * u + 0.06f * i, 0.42f, 0.3f, 1.3f, 0);
                    }
                    shake = Mathf.Max(shake, 5);
                    break;
            }
        }

        // lúc trúng của kiểu tia riêng: thêm một nhịp riêng cho đặc biệt (chùm mảnh băng, vòng xoáy lớn, vòng sóng âm kép)
        System.Collections.IEnumerator StyleBeamHit(string style, int target, Vector2 at, float tH, float g, float after)
        {
            yield return Wait(after);
            float e = tH * Mathf.Lerp(1, g, 0.5f);
            switch (style)
            {
                case "tia_bang":
                    for (int i = 0; i < 6; i++)
                    {
                        float ang = i / 6f * Mathf.PI * 2 + Random.value * 0.5f;
                        Drift(beamShard, at, new Vector2(Mathf.Cos(ang), Mathf.Sin(ang) - 0.3f) * e * 0.9f, e * 0.28f, Color.white,
                            0.02f * i, 0.5f, Random.value * 360);
                    }
                    break;
                case "tia_xoay": // nhỏ hơn thân con bị trúng (Spin nở tới 1,1 lần cỡ)
                    Spin(beamVortex, at, e * 0.8f, Color.white, 0, 0.55f, 720);
                    break;
                case "tia_trieu": // vòng kép, vòng lớn nở tới khoảng 1,1 lần thân rồi mờ, vòng trong nhỏ hơn thân
                    Pop(beamSoundRing, at, e * 0.85f, Color.white, 0, 0.45f, 0.3f, 1.3f, 0);
                    Pop(beamSoundRing, at, e * 0.55f, Color.white, 0.12f, 0.4f, 0.3f, 1.3f, 0);
                    shake = Mathf.Max(shake, 10);
                    break;
            }
        }

        // ảnh hiệu ứng nở rồi quay đều (spin độ mỗi lần sống), mờ ở cuối, sau delay giây sân
        void Spin(Sprite s, Vector2 at, float size, Color tint, float delay, float life, float spin)
        {
            if (!imageFx || !s) return;
            var item = Take(imageFx);
            Theme.SetSprite(item.Image, s);
            item.Image.color = tint;
            var rt = item.Rect;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = P(at);
            float aspect = s.rect.height / Mathf.Max(1, s.rect.width);
            float rot0 = Random.value * 360;
            AddFx(item, imageFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life, e = 1 - (1 - u) * (1 - u);
                float sc = 0.4f + 0.7f * e;
                f.rt.sizeDelta = new Vector2(size * sc, size * sc * aspect) * K;
                f.rt.localEulerAngles = new Vector3(0, 0, -(rot0 + spin * u));
                f.cg.alpha = u < 0.6f ? 1 : (1 - u) / 0.4f;
            });
        }

        // trúng: nổ nước, giọt văng, vòng sóng dưới chân, lấp lánh, rung sân nhẹ; cỡ theo thân con bị trúng (tH),
        // nhỏ hơn thân để vẫn thấy nó bị trúng, nhỉnh dần theo dạng của con bắn (g)
        System.Collections.IEnumerator BeamHit(int target, Vector2 at, float tH, float g, Color tint, float after)
        {
            yield return Wait(after);
            float e = tH * Mathf.Lerp(1, g, 0.5f);
            Pop(beamSplash, at, e * 0.75f, tint, 0, 0.4f, 0.35f, 1.25f, Random.value * 360);
            Pop(beamSplash, at, e * 0.45f, Color.Lerp(tint, Color.white, 0.6f), 0.05f, 0.32f, 0.3f, 1.15f, Random.value * 360);
            for (int i = 0; i < 3; i++)
            {
                float a = Random.value * Mathf.PI * 2;
                Drift(beamDrops, at, new Vector2(Mathf.Cos(a), Mathf.Sin(a) - 0.4f) * e * 0.7f, e * 0.2f, tint, 0.02f * i, 0.45f, Random.value * 360);
            }
            Ripple(Pos[target], e * 1.1f, tint, 0.03f, 0.5f);
            Pop(beamSparkle, at + new Vector2(e * 0.4f, -e * 0.35f), e * 0.22f, Color.white, 0.08f, 0.3f, 0.3f, 1.2f, 0);
            Pop(beamSparkle, at + new Vector2(-e * 0.4f, -e * 0.15f), e * 0.16f, Color.white, 0.14f, 0.3f, 0.3f, 1.2f, 0);
            Spark(target, Theme.Hex("#cfe9ff"));
            shake = Mathf.Max(shake, 6);
        }

        // ảnh hiệu ứng của chiêu bắn nở ra từ s0 tới s1 rồi mờ (cỡ theo bề rộng ảnh, giữ tỉ lệ), sau delay giây sân
        void Pop(Sprite s, Vector2 at, float size, Color tint, float delay, float life, float s0, float s1, float rot)
        {
            if (!imageFx || !s) return;
            var item = Take(imageFx);
            Theme.SetSprite(item.Image, s);
            item.Image.color = tint;
            var rt = item.Rect;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = P(at);
            float aspect = s.rect.height / Mathf.Max(1, s.rect.width);
            AddFx(item, imageFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life, e = 1 - (1 - u) * (1 - u);
                float sc = s0 + (s1 - s0) * e;
                f.rt.sizeDelta = new Vector2(size * sc, size * sc * aspect) * K;
                f.rt.localEulerAngles = new Vector3(0, 0, -(rot + 25 * u));
                f.cg.alpha = u < 0.55f ? 1 : (1 - u) / 0.45f;
            });
        }

        // ảnh hiệu ứng bay theo vận tốc (đơn vị web mỗi lần sống), rơi xuống, xoay, mờ dần, sau delay giây
        void Drift(Sprite s, Vector2 at, Vector2 fly, float size, Color tint, float delay, float life, float rot)
        {
            if (!imageFx || !s) return;
            float fall = 160 * life; // quãng rơi theo thời gian sống
            var item = Take(imageFx);
            Theme.SetSprite(item.Image, s);
            item.Image.color = tint;
            var rt = item.Rect;
            rt.pivot = new Vector2(0.5f, 0.5f);
            float aspect = s.rect.height / Mathf.Max(1, s.rect.width);
            AddFx(item, imageFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life;
                var p = at + fly * u + new Vector2(0, fall * u * u); // rơi
                f.rt.anchoredPosition = P(p);
                float sc = 0.6f + 0.5f * u;
                f.rt.sizeDelta = new Vector2(size * sc, size * sc * aspect) * K;
                f.rt.localEulerAngles = new Vector3(0, 0, -(rot + 120 * u));
                f.cg.alpha = u < 0.6f ? 1 : (1 - u) / 0.4f;
            });
        }

        // vòng sóng loang dưới chân: dẹt, nở rộng, mờ dần
        void Ripple(Vector2 feet, float width, Color tint, float delay, float life)
        {
            if (!imageFx || !beamRipple) return;
            var item = Take(imageFx);
            Theme.SetSprite(item.Image, beamRipple);
            item.Image.color = tint;
            var rt = item.Rect;
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = P(feet);
            rt.localEulerAngles = Vector3.zero;
            float aspect = beamRipple.rect.height / Mathf.Max(1, beamRipple.rect.width);
            AddFx(item, imageFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life, e = 1 - (1 - u) * (1 - u);
                float sc = 0.4f + 0.9f * e;
                f.rt.sizeDelta = new Vector2(width * sc, width * sc * aspect) * K;
                f.cg.alpha = u < 0.4f ? 1 : (1 - u) / 0.6f;
            });
        }

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
            FitBg(); // xoay màn, đổi khung Game view
            float raw = Mathf.Min(0.05f, Time.unscaledDeltaTime);
            // đang ra đòn: sân về nhịp của clip chậm nhất đang chạy (không nhanh hơn nhịp thường)
            float pace = skillHold > 0 ? SkillPace : float.MaxValue;
            foreach (var a in actors)
            {
                if (a == null || a.loop) continue;
                if (a.clip == Attack) pace = Mathf.Min(pace, AttackPace);
                else if (a.clip == Cast || a.clip == Skill) pace = Mathf.Min(pace, SkillPace);
            }
            float goal = Mathf.Min(1, pace / Mathf.Max(0.1f, speed));
            slow = goal < slow ? goal : Mathf.MoveTowards(slow, goal, raw / SlowEase);
            float dt = raw * speed * slow * fast;
            if (freeze > 0) // khựng lúc trúng: sân gần như đứng trong giây thật đã khai
            {
                freeze -= raw;
                dt *= FreezeSlow;
            }
            Clock += dt;
            skillHold = Mathf.Max(0, skillHold - dt);
            foreach (var a in actors)
            {
                if (a == null) continue;
                a.t += dt;
                a.flash = Mathf.Max(0, a.flash - dt);
                if (a.enter < 9) a.enter += dt;
                if (a.exit > 0) a.exit += dt;
                if (a.hop > 0) a.hop = a.hop > 0.5f ? 0 : a.hop + dt;
                if (a.dead > 0) a.dead += dt;
                if (a.recoil >= 0) a.recoil = a.recoil + dt > RecoilLen ? -1 : a.recoil + dt;
                if (!a.loop)
                {
                    float len = a.aola != null ? a.aola.Duration(a.clip) : ClipLen(a.clip);
                    float hitT = a.aola != null ? a.aola.HitTime(a.clip) : len * HitAt(a.clip);
                    if (!a.hitFired && a.t >= hitT)
                    {
                        a.hitFired = true;
                        Impact(a);
                        a.onHit?.Invoke();
                        if (a.handle != null) a.handle.hit = true;
                    }
                    if (a.t >= len)
                    {
                        if (!a.hitFired)
                        {
                            a.hitFired = true;
                            Impact(a);
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
            var jolt = new Vector2((Random.value - 0.5f) * shake, (Random.value - 0.5f) * shake);
            if (trauma > 0) // rung trauma (Eiserloh): lệch = tối đa × trauma², sóng sin lệch tần số (mượt), giảm theo giờ thật
            {
                trauma = Mathf.Max(0, trauma - raw * TraumaDecay);
                float q = trauma * trauma, n = Time.unscaledTime * 30;
                jolt += new Vector2((Mathf.Sin(n * 1.7f) + Mathf.Sin(n * 2.3f + 1.3f)) * 0.5f * TraumaX * q,
                    (Mathf.Sin(n * 1.1f + 0.7f) + Mathf.Sin(n * 2.9f)) * 0.5f * TraumaY * q);
            }
            root.anchoredPosition = jolt * K;

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
                else flashImg.color = new Color(flashColor.r, flashColor.g, flashColor.b, (1 - k) * 0.7f * flashColor.a); // hex 8 số: chớp nhạt
            }
        }

        // cú trúng của clip có khai impact (AolaSticker.Impact): khựng sân (tối đa 0,2 giây thật), cộng trauma rung, đẩy lùi đối thủ
        void Impact(Actor a)
        {
            if (a.aola == null || !a.aola.Impact(a.clip, out var stop, out var tr, out var push, out var flash)) return;
            freeze = Mathf.Max(freeze, Mathf.Min(0.2f, stop));
            trauma = Mathf.Min(1, trauma + tr);
            if (!string.IsNullOrEmpty(flash)) Flash(flash);
            var d = actors[a.side == 0 ? 1 : 0];
            if (d != null && d.dead <= 0 && push > 0)
            {
                d.recoil = 0;
                d.push = push;
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
            bool lunged = false;
            // chiêu cuối của tướng aola chỉ lao khi clip có khai (AolaSticker.Lunge); không khai thì đứng tại chỗ như trước
            if (!a.loop && (a.clip == Attack || a.clip == Skill))
            {
                if (a.aola != null && a.aola.Lunge(a.clip, a.t, tx, ty, out var o))
                {
                    ox = o.x;
                    oy = o.y;
                    lunged = true;
                }
                else if (a.clip == Attack || a.aola == null)
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
            // chiêu bắn của tướng không có clip bắn: nhún nhẹ về phía đối thủ lúc phóng tia
            if (!a.loop && a.clip == Cast && (a.aola == null || !a.aola.HasCast))
            {
                float k = Mathf.Clamp01(a.t / AolaSticker.CastLen);
                float nudge = Mathf.Sin(k * Mathf.PI) * 0.06f;
                ox = tx * nudge;
                oy = ty * nudge;
            }
            if (a.recoil >= 0) // bật lùi (Impact): ra xa đối thủ trong 15% đầu, về chỗ êm; nghiêng ra sau; lúc khựng rung ngang tại chỗ
            {
                float u = a.recoil / RecoilLen, v = Mathf.Clamp01((u - 0.15f) / 0.85f);
                float f = u < 0.15f ? Mathf.Sin(u / 0.15f * Mathf.PI * 0.5f) : 1 - v * v * (3 - 2 * v);
                var away = new Vector2(p.x - other.x, p.y - other.y).normalized * (f * a.push * a.H);
                ox += away.x;
                oy += away.y;
                rot += (a.side == 0 ? 1 : -1) * 0.09f * f;
                if (freeze > 0) ox += Mathf.Sin(Time.unscaledTime * 95) * 0.015f * a.H;
            }
            a.rt.anchoredPosition = P(x + ox, y + oy);
            a.rt.localEulerAngles = new Vector3(0, 0, -rot * Mathf.Rad2Deg);

            if (a.aola != null)
            {
                // đòn bắn từ xa (không lao) của aola: đạn bay và vụ nổ vẽ về thân đối thủ (AolaSticker.Far)
                bool far = !a.loop && !lunged && (a.clip == Attack || a.clip == Skill);
                a.aola.Far(a.loop ? Idle : a.clip, far ? Body(a.side == 0 ? 1 : 0) - new Vector2(x + ox, y + oy) : (Vector2?)null);
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
