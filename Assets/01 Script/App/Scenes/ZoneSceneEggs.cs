// Easter egg vùng boss chưa mở của đảo vùng đất (người dùng 2026-11-18: "làm 1 vài easter egg cho các zone khi bị khóa (khi bị khóa
// thôi) để kích thích tò mò người chơi, thúc đẩy người chơi cày game để unlock", "làm cả 6"). Chỉ có khi vùng còn khoá, mở vùng là thôi
// (rương thì ở lại cho tới khi nhận):
// 1–2. Boss tung tuyệt kỹ (thay mắt boss, boss ló đầu; người dùng 2026-11-18: "làm tướng dùng ultimate skill, thi thoảng thôi để người
//    chơi nhìn thấy, nhấn mạnh là vài lần thôi"): mây quanh bệ dạt ra, boss hiện màu thật tung tuyệt kỹ tại chỗ (có hiệu ứng), xong mây
//    khép lại, boss về xám. Mỗi lần vào đảo nhiều nhất 3 lần: lần đầu sau 10–16 giây, sau đó cách 70–120 giây, boss đang trong khung.
//    Boss cuối đảo còn giấu (ZoneHeader.BossHidden, 2026-11-27) tung chiêu vẫn là bóng đen.
// 3. Cảnh vùng rò qua mây (land.secs[k].tease): đom đóm, đèn biển quét, bong bóng, hải âu, sét và mưa, cá voi phun nước, nấm phát
//    sáng, tuyết rơi, xoáy nước; đảo Mộc thêm bướm, gió hang nanh, lá rơi, pha lê lấp lánh (màu nhuộm theo tease.c).
// 4. Chọc mây: chạm mây thì đám quanh đó dạt ra rồi nảy về (lò xo từng đám, chạm liên tục cộng dồn mượt, mây giữ đục; người dùng
//    2026-11-18: "mây tỏa ra vẫn mờ và chưa mượt khi tap liên tục"); chọc 7 lần một vùng thì boss hắt xì thổi tung mây, quà một lần
//    (+3 bi, landPoke).
// 5. Rương bí ẩn (secs[k].cx, cy, gift) ló trong khe mây: chạm báo mở vùng để nhận; vùng mở rồi thì rương nảy, chạm nhận bi (landGift).
// 6. Ghi chú bút chì (secs[k].note) ở mép vùng, vẽ trên lớp mây cho đọc được, tan khi mây tan lúc mở vùng.
// Hình: Assets/03 Art/Islands/Co/trung_* (ArtGen/Islands/land_thuy/m0/ve_trung.py), rương pk_ruong_go; chỗ đặt do vung.py (trung) tính.
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;
using Random = UnityEngine.Random;

namespace PokiClash
{
    public sealed partial class ZoneScene
    {
        [Tooltip("Món chạm được của đảo vùng đất (Items/TrungPhuc: Image + ClickCatcher): mây phủ, rương bí ẩn")]
        [SerializeField] Image eggPrefab;
        [Tooltip("Hình easter egg vùng khoá: Islands/Co/trung_*, rương pk_ruong_go (menu Dựng cờ ải, vùng boss)")]
        [SerializeField] Sprite[] eggArt;

        const string GiftKey = "landGift", PokeKey = "landPoke", ChestArt = "pk_ruong_go";
        const int PokeSneeze = 7, PokeGift = 3;
        const float ChestW = 150;
        const int UltMax = 3; // số lần boss tung tuyệt kỹ mỗi lần vào đảo

        sealed class SecCloud
        {
            public Image img;
            public Vector2 pos;   // chỗ gốc (anchoredPosition)
            public Vector3 scale; // cỡ gốc (có lật)
            public int sec;
            // lò xo: lệch, vận tốc, chỗ nghỉ (hắt xì, tuyệt kỹ đẩy chỗ nghỉ ra xa rồi trả về 0); phồng cỡ tương tự
            public Vector2 off, vel, rest;
            public float so, sv, srest;
            public bool moving;
        }

        sealed class Tease
        {
            public string k;
            public int sec;
            public Vector2 at; // anchoredPosition tâm
            public float s, t, next, fx = -1;
            public readonly List<Image> imgs = new List<Image>();
            public float[] seed;
        }

        sealed class EggChest
        {
            public Image img, spark;
            public int sec, gift;
            public Vector2 pos;
        }

        readonly List<SecCloud> eggClouds = new List<SecCloud>();
        readonly List<SecCloud> movingClouds = new List<SecCloud>();
        // lò xo mây: độ cứng, cản (hơi nảy), lệch tối đa
        const float CloudK = 55, CloudC = 10, CloudSK = 70, CloudSC = 11, CloudMaxOff = 340;
        readonly List<Tease> eggTeases = new List<Tease>();
        readonly List<EggChest> eggChests = new List<EggChest>();
        readonly List<(Image img, int sec)> eggNotes = new List<(Image, int)>();
        readonly Dictionary<int, int> pokes = new Dictionary<int, int>();
        readonly HashSet<int> pokeTold = new HashSet<int>();
        Dictionary<string, Sprite> eggSprites;
        List<StageDef> landStages;
        float eggClock, nextUlt;
        int ultLeft;
        Coroutine ultCo;

        Sprite Egg(string n)
        {
            if (eggSprites == null)
            {
                eggSprites = new Dictionary<string, Sprite>();
                if (eggArt != null)
                    foreach (var sp in eggArt)
                        if (sp) eggSprites[sp.name] = sp;
            }
            return n != null && eggSprites.TryGetValue(n, out var s) ? s : null;
        }

        // một hình rời trên lớp nút: tâm ở chỗ bản đồ (y xuống), bề ngang w, cao theo tỉ lệ hình; nằm trên cùng
        Image EggItem(Image prefab, Sprite sp, string name, Vector2 map, float w, bool hit, Transform parent = null)
        {
            var img = Ui.Spawn(prefab, parent ? parent : p.nodeLayer);
            img.name = name;
            Theme.SetSprite(img, sp);
            img.raycastTarget = hit;
            img.color = Color.white;
            var rt = img.rectTransform;
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.sizeDelta = sp ? new Vector2(w, w * sp.rect.height / sp.rect.width) : new Vector2(w, w);
            rt.anchoredPosition = new Vector2(map.x, -map.y);
            rt.localScale = Vector3.one;
            rt.localEulerAngles = Vector3.zero;
            rt.SetAsLastSibling();
            return img;
        }

        static void SetAlpha(Graphic g, float a)
        {
            if (!g) return;
            var c = g.color;
            c.a = Mathf.Clamp01(a);
            g.color = c;
        }

        void ClearEggs()
        {
            if (ultCo != null) StopCoroutine(ultCo);
            ultCo = null;
            eggClouds.Clear();
            movingClouds.Clear();
            eggTeases.Clear();
            eggChests.Clear();
            eggNotes.Clear();
        }

        // câu báo vùng k còn khoá: hạ boss của vùng trước
        string SectionLockMsg(int k)
        {
            if (land == null || k <= 0 || k > land.habs.Count || landStages == null) return "";
            int bi = land.habs[k - 1].stage;
            var st = landStages[Mathf.Clamp(bi - 1, 0, landStages.Count - 1)];
            var boss = App.Data != null ? App.Data.Hero(Teams.StageLead(st, App.Data).hero) : null;
            return Loc.F("Hạ {0} ở ải {1} để mở vùng này", (boss != null ? boss.name : "boss"), bi);
        }

        // ---------- dựng: dưới mây (ghi chú, rương), trên mây (hiệu ứng rò qua mây, mắt boss) ----------

        void SpawnEggsUnder(SaveData s)
        {
            if (land.secs.Count == 0 || !secPrefab) return;
            for (int k = 0; k < land.secs.Count; k++)
            {
                var c = land.secs[k];
                bool locked = k >= landOpened;
                // ghi chú bút chì là ảnh có chữ: bản dịch là ảnh <tên>_<ngôn ngữ> (ArtGen/Islands/ve_trung_en.py), thiếu thì dùng bản Việt
                var noteArt = (Loc.Lang != Loc.Vi && c.note != null ? Egg(c.note + "_" + Loc.Lang) : null) ?? Egg(c.note);
                if (locked && noteArt)
                    eggNotes.Add((EggItem(secPrefab, noteArt, "ghi_chu_" + k, new Vector2((float)c.nx * mapW, (float)c.ny * mapH), (float)c.nw * mapW, false, OverParent), k));
                var chestArt = Egg(ChestArt);
                if (c.cx >= 0 && c.gift > 0 && chestArt && !LandBits.Has(s, GiftKey, zone, k))
                {
                    var map = new Vector2((float)c.cx * mapW, (float)c.cy * mapH);
                    var ch = new EggChest { sec = k, gift = c.gift };
                    ch.img = EggItem(eggPrefab ? eggPrefab : secPrefab, chestArt, "ruong_bi_an_" + k, map, ChestW, eggPrefab);
                    ch.pos = ch.img.rectTransform.anchoredPosition;
                    ch.spark = EggItem(secPrefab, App.Art ? App.Art.Get("anim_sparkle") : null, "lap_lanh", map + new Vector2(ChestW * 0.35f, -ChestW * 0.3f), 46, false);
                    var cc = ch.img.GetComponent<ClickCatcher>();
                    if (cc) cc.OnClick = () => TapChest(ch);
                    eggChests.Add(ch);
                }
            }
        }

        void SpawnEggsOver()
        {
            if (land.secs.Count == 0 || !secPrefab) return;
            for (int k = landOpened; k < land.secs.Count; k++)
                foreach (var t in land.secs[k].tease) SpawnTease(t, k);
        }

        void SpawnTease(LandTease t, int k)
        {
            var tz = new Tease { k = t.k, sec = k, at = new Vector2((float)t.x * mapW, -(float)t.y * mapH), s = (float)t.s * mapW };
            var map = new Vector2(tz.at.x, -tz.at.y);
            Sprite A(string n) => App.Art ? App.Art.Get(n) : null;
            void Add(Sprite sp, float w, int n, Color c)
            {
                for (int i = 0; i < n; i++)
                {
                    var img = EggItem(secPrefab, sp, "trung_" + t.k, map, w, false, OverParent);
                    img.color = c;
                    tz.imgs.Add(img);
                }
            }
            // màu nhuộm của dữ liệu (tease.c), không có thì màu mặc định của loại
            Color Tint(Color def, float a)
            {
                var c = !string.IsNullOrEmpty(t.c) && ColorUtility.TryParseHtmlString(t.c, out var pc) ? pc : def;
                c.a = a;
                return c;
            }
            switch (t.k)
            {
                case "dom_dom": Add(A("anim_glow"), 46, 9, Tint(new Color(1, 0.95f, 0.45f), 0)); break;
                case "den_bien":
                    Add(A("anim_beam"), tz.s, 1, new Color(1, 0.95f, 0.7f, 0.5f));
                    tz.imgs[0].rectTransform.pivot = new Vector2(0, 0.5f);
                    break;
                case "bong_bong": Add(Egg("trung_bong"), 40, 8, new Color(1, 1, 1, 0)); break;
                case "chim":
                    {
                        // hải âu cắt từ chính ảnh nền của đảo (land_<đảo>_chim_*), thiếu thì mượn của đảo Thủy
                        Sprite Bird(int i)
                        {
                            var b = A(land.art + "_chim_" + i);
                            return b ? b : A("land_thuy_chim_" + i);
                        }
                        Add(Bird(1), 92, 1, Color.white);
                        Add(Bird(2), 84, 1, Color.white);
                        break;
                    }
                case "buom":
                    {
                        // bướm cánh trắng nhuộm mỗi con một màu, bay lượn trên mây
                        // màu đậm: nằm trên nền mây trắng, màu phấn thì chìm mất (tour 2026-11-19)
                        var pal = new[] { new Color(1f, 0.36f, 0.6f), new Color(1f, 0.78f, 0.1f), new Color(0.3f, 0.6f, 1f), new Color(1f, 0.5f, 0.15f), new Color(0.66f, 0.4f, 1f) };
                        foreach (var c in pal) Add(Egg("trung_buom"), 110, 1, c);
                        break;
                    }
                case "gio": Add(A("anim_wind"), 170, 3, new Color(1, 1, 1, 0)); break;
                case "la_roi": Add(Egg("trung_la"), 78, 10, Tint(new Color(0.94f, 0.54f, 0.24f), 0)); break;
                case "pha_le": Add(A("anim_sparkle"), 96, 6, Tint(new Color(0.78f, 1f, 0.72f), 0)); break;
                case "set":
                    Add(A("anim_glow"), tz.s * 1.6f, 1, new Color(1, 1, 0.85f, 0));
                    Add(Egg("trung_set"), 74, 1, new Color(1, 1, 1, 0));
                    Add(A("anim_rain"), 12, 10, new Color(0.75f, 0.85f, 1, 0));
                    break;
                case "phun_nuoc":
                    Add(Egg("trung_nuoc"), 112, 1, Color.white);
                    tz.imgs[0].rectTransform.pivot = new Vector2(0.5f, 0);
                    tz.imgs[0].rectTransform.localScale = new Vector3(1, 0, 1);
                    break;
                case "phat_sang": Add(A("anim_glow"), tz.s, 1, new Color(0.78f, 0.45f, 1, 0.4f)); break;
                case "tuyet": Add(Egg("trung_tuyet"), 64, 16, Tint(Color.white, 0)); break; // tuyết (Thủy), tro xám (Hỏa)
                case "xoay": Add(A("anim_whirlpool"), tz.s, 1, new Color(1, 1, 1, 0.9f)); break;
            }
            tz.seed = tz.imgs.Select((_, i) => Mathf.Repeat(Mathf.Sin((k * 13 + i) * 12.9898f) * 43758.547f, 1f)).ToArray();
            tz.next = eggClock + Random.Range(1f, 4f);
            eggTeases.Add(tz);
        }

        // ---------- chạy theo thời gian ----------

        void TickEggs(float dt)
        {
            if (land == null || land.secs.Count == 0) return;
            eggClock += dt;
            float night = DayCycle.Night(DayCycle.Hour), t = eggClock;
            foreach (var tz in eggTeases) TickTease(tz, t, dt, night);
            TickClouds(dt);
            foreach (var ch in eggChests)
            {
                if (!ch.img) continue;
                bool open = ch.sec < landOpened;
                float hop = open ? Mathf.Max(0, Mathf.Sin(Mathf.Repeat(t, 2f) / 0.45f * Mathf.PI)) * (Mathf.Repeat(t, 2f) < 0.45f ? 1 : 0) : 0;
                ch.img.rectTransform.anchoredPosition = ch.pos + new Vector2(0, hop * 22);
                if (ch.spark)
                {
                    float tw = 0.5f + 0.5f * Mathf.Sin(t * (open ? 5f : 2.6f) + ch.sec);
                    SetAlpha(ch.spark, open ? tw : tw * 0.7f);
                    ch.spark.rectTransform.localScale = Vector3.one * (0.7f + 0.4f * tw);
                }
            }
            // boss tung tuyệt kỹ: vài lần mỗi lần vào đảo, một con đang trong khung nhìn
            if (ultCo == null && ultLeft > 0 && t >= nextUlt)
            {
                var cand = landHeroes.Where(h => h.locked && h.sticker != null && h.sticker.HasClip(StageView.Skill) && InView(h, -40)).ToList();
                if (cand.Count > 0)
                {
                    ultLeft--;
                    nextUlt = t + Random.Range(70f, 120f);
                    ultCo = StartCoroutine(Ult(cand[Random.Range(0, cand.Count)]));
                }
                else nextUlt = t + 3; // chưa có boss nào trong khung: thử lại sau
            }
        }

        void TickTease(Tease tz, float t, float dt, float night)
        {
            var im = tz.imgs;
            switch (tz.k)
            {
                case "dom_dom":
                    for (int i = 0; i < im.Count; i++)
                    {
                        float sd = tz.seed[i];
                        im[i].rectTransform.anchoredPosition = tz.at + new Vector2(Mathf.Sin(t * 0.5f + sd * 31) * tz.s * 0.45f, Mathf.Cos(t * 0.37f + sd * 17) * tz.s * 0.22f);
                        float tw = 0.5f + 0.5f * Mathf.Sin(t * 2.7f + sd * 40);
                        SetAlpha(im[i], (0.35f + 0.65f * night) * tw * tw);
                    }
                    break;
                case "den_bien":
                    im[0].rectTransform.localEulerAngles = new Vector3(0, 0, t * 35);
                    SetAlpha(im[0], 0.3f + 0.4f * night);
                    break;
                case "bong_bong":
                    for (int i = 0; i < im.Count; i++)
                    {
                        float sd = tz.seed[i], u = Mathf.Repeat(t / 3.6f + sd, 1);
                        im[i].rectTransform.anchoredPosition = tz.at + new Vector2((sd - 0.5f) * tz.s * 0.6f + Mathf.Sin(u * 7 + sd * 9) * 18, u * tz.s * 0.8f);
                        im[i].rectTransform.localScale = Vector3.one * (0.6f + 0.6f * sd);
                        SetAlpha(im[i], Mathf.Sin(u * Mathf.PI));
                    }
                    break;
                case "chim":
                    for (int i = 0; i < im.Count; i++)
                    {
                        float a = t * 0.45f + i * Mathf.PI;
                        im[i].rectTransform.anchoredPosition = tz.at + new Vector2(Mathf.Cos(a) * tz.s * 0.45f, Mathf.Sin(a) * tz.s * 0.16f + Mathf.Sin(t * 3 + i) * 8 + 80);
                        im[i].rectTransform.localScale = new Vector3(Mathf.Sin(a) > 0 ? -1 : 1, 1, 1);
                    }
                    break;
                case "set":
                    {
                        // chớp: hai nhá trong 0,5 giây, sét hiện lúc nhá; mưa rơi liên tục dưới mây
                        if (tz.fx < 0 && t >= tz.next)
                        {
                            tz.fx = 0;
                            tz.next = t + Random.Range(3f, 6f);
                            var b = im[1].rectTransform;
                            b.anchoredPosition = tz.at + new Vector2(Random.Range(-tz.s * 0.3f, tz.s * 0.3f), -tz.s * 0.05f);
                            b.localScale = new Vector3(Random.value < 0.5f ? -1 : 1, 1, 1);
                        }
                        float fl = 0;
                        if (tz.fx >= 0)
                        {
                            tz.fx += dt;
                            fl = Mathf.Max(Spike(tz.fx - 0.06f), Spike(tz.fx - 0.3f) * 0.7f);
                            if (tz.fx > 0.6f) tz.fx = -1;
                        }
                        SetAlpha(im[0], fl * 0.85f);
                        SetAlpha(im[1], fl > 0.35f ? 1 : 0);
                        for (int i = 2; i < im.Count; i++)
                        {
                            float sd = tz.seed[i], u = Mathf.Repeat(t * 0.9f + sd, 1);
                            im[i].rectTransform.anchoredPosition = tz.at + new Vector2((sd - 0.5f) * tz.s * 0.7f, -tz.s * 0.1f - u * tz.s * 0.55f);
                            SetAlpha(im[i], 0.65f * Mathf.Sin(u * Mathf.PI));
                        }
                        break;
                    }
                case "phun_nuoc":
                    {
                        if (tz.fx < 0 && t >= tz.next)
                        {
                            tz.fx = 0;
                            tz.next = t + Random.Range(4f, 7f);
                        }
                        float k = 0;
                        if (tz.fx >= 0)
                        {
                            tz.fx += dt;
                            float u = tz.fx;
                            k = u < 0.35f ? Mathf.SmoothStep(0, 1.1f, u / 0.35f) : u < 0.5f ? Mathf.Lerp(1.1f, 1, (u - 0.35f) / 0.15f) : u < 1.1f ? 1 : Mathf.Max(0, 1 - (u - 1.1f) / 0.4f);
                            if (u > 1.5f) tz.fx = -1;
                        }
                        im[0].rectTransform.localScale = new Vector3(1 + 0.08f * Mathf.Sin(t * 20) * (k > 0 ? 1 : 0), k, 1);
                        break;
                    }
                case "phat_sang":
                    SetAlpha(im[0], 0.3f + 0.3f * Mathf.Sin(t * 2.4f + tz.sec) + 0.3f * night);
                    im[0].rectTransform.localScale = Vector3.one * (0.92f + 0.1f * Mathf.Sin(t * 2.4f + tz.sec));
                    break;
                case "tuyet":
                    for (int i = 0; i < im.Count; i++)
                    {
                        float sd = tz.seed[i], u = Mathf.Repeat(t * 0.11f + sd, 1);
                        im[i].rectTransform.anchoredPosition = tz.at + new Vector2((sd - 0.5f) * tz.s + Mathf.Sin(t * 0.9f + sd * 20) * 30, tz.s * 0.25f - u * tz.s * 0.6f);
                        im[i].rectTransform.localEulerAngles = new Vector3(0, 0, t * (20 + 40 * sd));
                        im[i].rectTransform.localScale = Vector3.one * (0.7f + 0.5f * sd);
                        SetAlpha(im[i], Mathf.Sin(u * Mathf.PI));
                    }
                    break;
                case "xoay":
                    im[0].rectTransform.localEulerAngles = new Vector3(0, 0, -t * 30);
                    break;
                case "buom":
                    for (int i = 0; i < im.Count; i++)
                    {
                        float sd = tz.seed[i], a = t * (0.5f + 0.25f * sd) + sd * 31;
                        im[i].rectTransform.anchoredPosition = tz.at + new Vector2(Mathf.Sin(a) * tz.s * 0.42f,
                            Mathf.Cos(a * 0.77f + sd * 9) * tz.s * 0.2f + Mathf.Sin(t * 5 + sd * 13) * 7);
                        // vỗ cánh: bề ngang co giãn, nghiêng theo hướng bay
                        float flap = 0.3f + 0.7f * Mathf.Abs(Mathf.Sin(t * 9 + sd * 10));
                        im[i].rectTransform.localScale = new Vector3(flap, 1, 1) * (0.8f + 0.4f * sd);
                        im[i].rectTransform.localEulerAngles = new Vector3(0, 0, Mathf.Cos(a) * 18);
                    }
                    break;
                case "gio":
                    for (int i = 0; i < im.Count; i++)
                    {
                        float sd = tz.seed[i], u = Mathf.Repeat(t / 3.4f + i / (float)im.Count, 1);
                        im[i].rectTransform.anchoredPosition = tz.at + new Vector2((u - 0.5f) * tz.s * 2.2f, (sd - 0.5f) * tz.s * 0.8f + Mathf.Sin(u * 6 + sd * 7) * 12);
                        im[i].rectTransform.localScale = Vector3.one * (0.75f + 0.5f * sd);
                        SetAlpha(im[i], 0.9f * Mathf.Sin(u * Mathf.PI));
                    }
                    break;
                case "la_roi":
                    for (int i = 0; i < im.Count; i++)
                    {
                        float sd = tz.seed[i], u = Mathf.Repeat(t * 0.15f + sd, 1);
                        im[i].rectTransform.anchoredPosition = tz.at + new Vector2((sd - 0.5f) * tz.s + Mathf.Sin(t * 1.3f + sd * 20) * 40, tz.s * 0.3f - u * tz.s * 0.7f);
                        im[i].rectTransform.localEulerAngles = new Vector3(0, 0, Mathf.Sin(t * 2 + sd * 9) * 55);
                        im[i].rectTransform.localScale = Vector3.one * (0.7f + 0.5f * sd);
                        SetAlpha(im[i], Mathf.Sin(u * Mathf.PI));
                    }
                    break;
                case "pha_le":
                    for (int i = 0; i < im.Count; i++)
                    {
                        // lấp lánh: mỗi tia nhá lên rồi tắt, mỗi lượt một chỗ mới quanh cụm pha lê
                        float sd = tz.seed[i], cyc = t / (1.6f + sd) + sd * 7, u = Mathf.Repeat(cyc, 1);
                        float h = Mathf.Floor(cyc) * 12.9898f + i * 78.233f;
                        float hx = Mathf.Repeat(Mathf.Sin(h) * 43758.547f, 1), hy = Mathf.Repeat(Mathf.Sin(h * 1.7f) * 24634.63f, 1);
                        var rt = im[i].rectTransform;
                        rt.anchoredPosition = tz.at + new Vector2((hx - 0.5f) * tz.s, (hy - 0.3f) * tz.s * 0.7f);
                        float pop = u < 0.5f ? Mathf.Sin(u / 0.5f * Mathf.PI) : 0;
                        rt.localScale = Vector3.one * (pop * (0.6f + 0.6f * sd));
                        rt.localEulerAngles = new Vector3(0, 0, t * 40 + sd * 90);
                        SetAlpha(im[i], pop > 0.01f ? 1 : 0);
                    }
                    break;
            }
        }

        // nhá sáng: vọt lên rồi tắt trong ~0,2 giây quanh mốc 0
        static float Spike(float d) => d < 0 ? 0 : Mathf.Exp(-d * 14) * Mathf.Clamp01(d * 40);

        // ---------- chạm ----------

        void TapChest(EggChest ch)
        {
            if (!ch.img) return;
            if (ch.sec >= landOpened)
            {
                App.Audio?.Play("pick");
                App.Toasts.Show(Loc.T("Rương bí ẩn: mở vùng này để nhận"), Icon("chest"));
                StartCoroutine(Wobble(ch.img.rectTransform));
                return;
            }
            var s = App.Save?.Data;
            if (s == null || LandBits.Has(s, GiftKey, zone, ch.sec)) return;
            App.Audio?.Play("chest");
            s.balls += ch.gift;
            LandBits.Add(s, GiftKey, zone, ch.sec);
            App.Toasts.Show(Loc.F("Rương bí ẩn: +{0} bi", ch.gift), Icon("chest"));
            App.Save.Save(); // màn dựng lại, rương biến mất
        }

        void PokeCloud(SecCloud sc)
        {
            if (!sc.img || sc.sec < landOpened) return;
            int k = sc.sec;
            App.Audio?.Play("pick");
            if (pokeTold.Add(k)) App.Toasts.Show(SectionLockMsg(k), Icon("lock"));
            pokes.TryGetValue(k, out int n);
            pokes[k] = ++n;
            if (n >= PokeSneeze)
            {
                pokes[k] = 0;
                StartCoroutine(Sneeze(k, sc.pos));
            }
            else Kick(sc.pos, 300, 900, 1.1f, k);
        }

        void Wake(SecCloud c)
        {
            if (c.moving) return;
            c.moving = true;
            movingClouds.Add(c);
        }

        // cú đẩy: mây trong bán kính bị đẩy ra ngoài (mạnh ở gần), phồng nhẹ; lò xo kéo về (TickClouds)
        void Kick(Vector2 at, float radius, float speed, float puff, int sec = -1)
        {
            foreach (var c in eggClouds)
            {
                if (!c.img || !c.img.gameObject.activeSelf || (sec >= 0 && c.sec != sec)) continue;
                var d = c.pos + c.off - at;
                float dist = d.magnitude;
                if (dist >= radius) continue;
                float fall = 1 - dist / radius;
                var dir = dist > 1 ? d / dist : Random.insideUnitCircle.normalized;
                c.vel += dir * (speed * fall);
                c.sv += puff * fall;
                Wake(c);
            }
        }

        // đặt chỗ nghỉ của lò xo cho mây quanh at (dạt ra xa push, phồng sr) rồi trả về 0 khi gọi lại với push = 0
        List<SecCloud> PushClouds(Vector2 at, float radius, float push, float sr, int sec, List<SecCloud> only = null)
        {
            var list = only ?? eggClouds.Where(c => c.img && c.sec == sec && (c.pos - at).sqrMagnitude < radius * radius).ToList();
            foreach (var c in list)
            {
                if (!c.img) continue;
                var d = c.pos - at;
                float fall = 1 - Mathf.Clamp01(d.magnitude / radius);
                var dir = d.sqrMagnitude > 1 ? d.normalized : Vector2.up;
                c.rest = push > 0 ? dir * (push * (0.45f + fall)) + Vector2.up * (push * 0.08f) : Vector2.zero;
                c.srest = push > 0 ? sr * (0.5f + fall) : 0;
                Wake(c);
            }
            return list;
        }

        // lò xo từng đám mây đang động: kéo về chỗ nghỉ, hơi nảy; yên hẳn thì về đúng chỗ gốc và thôi tính
        void TickClouds(float dt)
        {
            for (int i = movingClouds.Count - 1; i >= 0; i--)
            {
                var c = movingClouds[i];
                if (!c.img)
                {
                    movingClouds.RemoveAt(i);
                    continue;
                }
                var acc = -CloudK * (c.off - c.rest) - CloudC * c.vel;
                c.vel += acc * dt;
                c.off += c.vel * dt;
                if (c.off.sqrMagnitude > CloudMaxOff * CloudMaxOff) c.off = c.off.normalized * CloudMaxOff;
                c.sv += (-CloudSK * (c.so - c.srest) - CloudSC * c.sv) * dt;
                c.so = Mathf.Clamp(c.so + c.sv * dt, -0.2f, 0.6f);
                var rt = c.img.rectTransform;
                rt.anchoredPosition = c.pos + c.off;
                rt.localScale = c.scale * (1 + c.so);
                if (c.rest == Vector2.zero && c.srest == 0 && c.off.sqrMagnitude < 0.25f && c.vel.sqrMagnitude < 1 && Mathf.Abs(c.so) < 0.002f && Mathf.Abs(c.sv) < 0.01f)
                {
                    c.off = c.vel = Vector2.zero;
                    c.so = c.sv = 0;
                    rt.anchoredPosition = c.pos;
                    rt.localScale = c.scale;
                    c.moving = false;
                    movingClouds.RemoveAt(i);
                }
            }
        }

        // boss hắt xì: mây quanh chỗ chọc bị thổi tung ra xa (giữ đục), một lúc sau lò xo kéo về; lần đầu mỗi vùng có quà
        IEnumerator Sneeze(int k, Vector2 at)
        {
            App.Audio?.Play("whoosh");
            App.Toasts.Show(Loc.T("Hắt xì!"), Icon("lock"));
            var list = PushClouds(at, 720, 300, 0.3f, k);
            Kick(at, 720, 1400, 0.8f, k);
            yield return new WaitForSecondsRealtime(1.0f);
            PushClouds(at, 0, 0, 0, k, list);
            yield return new WaitForSecondsRealtime(0.8f);
            var s = App.Save?.Data;
            if (s != null && !LandBits.Has(s, PokeKey, zone, k))
            {
                s.balls += PokeGift;
                LandBits.Add(s, PokeKey, zone, k);
                App.Audio?.Play("coin");
                App.Toasts.Show(Loc.F("Boss hắt xì rơi ra +{0} bi", PokeGift), Icon("chest"));
                App.Save.Save();
            }
        }

        static IEnumerator Wobble(RectTransform rt)
        {
            for (float t = 0; t < 0.45f && rt; t += Time.unscaledDeltaTime)
            {
                rt.localEulerAngles = new Vector3(0, 0, Mathf.Sin(t * 45) * 10 * (1 - t / 0.45f));
                yield return null;
            }
            if (rt) rt.localEulerAngles = Vector3.zero;
        }

        // boss vùng khoá tung tuyệt kỹ: mây quanh bệ dạt ra, boss hiện màu thật tung chiêu tại chỗ (hiệu ứng ở phía trước), xong mây khép
        // lại, boss về xám đứng yên
        IEnumerator Ult(LandHero h)
        {
            int k = land.SectionOf(h.st.idx);
            var at = h.pos + new Vector2(0, h.bodyH * 0.4f); // tâm thân tướng (cùng toạ độ với mây)
            App.Audio?.Play("whoosh");
            var near = PushClouds(at, 560, 300, 0.12f, k); // mây dạt ra (giữ đục), lò xo đưa tới chỗ nghỉ
            yield return new WaitForSecondsRealtime(0.55f);
            if (h.sticker != null)
            {
                h.sticker.Rect.gameObject.SetActive(true); // ảnh tướng vùng khoá vốn ẩn dưới mây
                App.Audio?.Play("ult");
                h.sticker.FarAhead(StageView.Skill, 1.3f); // hiệu ứng ở xa hiện trước mặt (không có đối thủ)
                float dur = h.sticker.Duration(StageView.Skill) + 0.25f;
                for (float t = 0; t < dur && h.sticker != null && h.locked; t += Time.unscaledDeltaTime)
                {
                    h.sticker.Show(StageView.Skill, t, false, 1, h.hidden, 0); // boss cuối còn giấu: tung chiêu vẫn là bóng đen
                    yield return null;
                }
                if (h.sticker != null)
                {
                    h.sticker.Far(StageView.Skill, null);
                    if (h.locked) h.sticker.Show(Idle, 0, true, 1, true, 0);
                }
            }
            yield return new WaitForSecondsRealtime(0.35f);
            PushClouds(at, 0, 0, 0, k, near); // mây khép lại theo lò xo
            yield return new WaitForSecondsRealtime(0.7f);
            if (h.sticker != null && h.locked && secClouds != null && k < secClouds.Length && secClouds[k] != null)
                h.sticker.Rect.gameObject.SetActive(false);
            ultCo = null;
        }

        // ---------- mở vùng: thôi easter egg của vùng (rương ở lại, thành rương nhận được) ----------

        // e: 0..1 theo lúc mây tan
        void FadeSectionEggs(int k, float e)
        {
            for (int i = movingClouds.Count - 1; i >= 0; i--)
                if (movingClouds[i].sec == k)
                {
                    movingClouds[i].moving = false;
                    movingClouds.RemoveAt(i);
                }
            foreach (var tz in eggTeases)
                if (tz.sec == k)
                    foreach (var im in tz.imgs)
                        if (im) im.gameObject.SetActive(e < 0.5f);
            foreach (var (img, sec) in eggNotes)
                if (sec == k && img) SetAlpha(img, 1 - e);
        }

        // tour thử: ép easter egg của vùng k (ult: boss tung tuyệt kỹ, poke: chọc 7 lần, chest: chạm rương)
        public string LandEgg(string cmd, int k)
        {
            switch (cmd)
            {
                case "ult":
                    var h = landHeroes.FirstOrDefault(x => x.locked && land.SectionOf(x.st.idx) == k && x.sticker != null);
                    if (h == null) return Loc.T("không có tướng khoá đã dựng ở vùng ") + k;
                    if (!h.sticker.HasClip(StageView.Skill)) return Loc.T("tướng ải ") + h.st.idx + Loc.T(" không có clip tuyệt kỹ");
                    if (ultCo != null) StopCoroutine(ultCo);
                    ultCo = StartCoroutine(Ult(h));
                    return Loc.T("tuyệt kỹ ải ") + h.st.idx;
                case "poke":
                    var sc = eggClouds.FirstOrDefault(c => c.sec == k && c.img);
                    if (sc == null) return Loc.T("không có mây vùng ") + k;
                    for (int i = 0; i < PokeSneeze; i++) PokeCloud(sc);
                    return Loc.T("chọc vùng ") + k;
                case "poke1": // một lần chạm (thử chạm liên tục)
                    var s1 = eggClouds.Where(c => c.sec == k && c.img).OrderBy(c => c.pos.y).Skip(eggClouds.Count(c => c.sec == k) / 2).FirstOrDefault();
                    if (s1 == null) return Loc.T("không có mây vùng ") + k;
                    PokeCloud(s1);
                    return Loc.T("chạm vùng ") + k;
                case "chest":
                    var ch = eggChests.FirstOrDefault(c => c.sec == k);
                    if (ch == null) return Loc.T("không có rương vùng ") + k;
                    TapChest(ch);
                    return Loc.T("chạm rương vùng ") + k;
            }
            return "?";
        }
    }
}
