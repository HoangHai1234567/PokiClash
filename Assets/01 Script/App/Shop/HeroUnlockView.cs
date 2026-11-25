// Màn mở khoá tướng mới: bút chì vẽ tướng lên trang sổ rồi tướng bật ra (người dùng 2026-11-24: "khi ăn unlock tướng là có bút chì
// vẽ lên trang giấy hình tướng rồi tướng bật ra play 1 animation thì đấy, có fx sao trắng khi nó bật ra rồi hiện chỉ số ở dưới";
// chọn: bút chì đi theo viền thật, cả màn là trang sổ, thay hẳn màn cột sáng kiểu Brawl Stars trước đó). Prefab Assets/04 Prefabs/
// Items/MoKhoaTuong (UiKit.heroUnlock, menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: chỉ màn mở khoá tướng (MoKhoaTuong)"),
// canvas riêng trên mọi hộp. Mọi bậc một vũ đạo; bậc chỉ đổi màu nền lộ quanh mép trang và viên bậc.
//   1. Trang sổ (sổ phép của nhân vật chính) trượt lên. Trong lúc đó dựng hình tướng ẩn (rig .atomik / aola qua AolaSticker, đứng yên
//      ở khung đầu dáng đứng; rig chưa tải về thì chân dung), đọc độ phủ của hình (AsyncGPUReadback, hai lượt: cả ảnh tìm hộp, rồi cắt
//      hộp 256) và lấy các vòng viền ngoài (Core/Contour).
//   2. Bút chì bay vào, lần theo từng vòng viền (nét chì InkStroke hiện ngay sau ngòi; sang vòng khác thì nhấc bút).
//   3. Bút chì gạch zích zắc từng hàng từ trên xuống: tranh chì hiện dần (shader UIPencilDraw, cùng công thức hàng với bút).
//   4. Sáp màu tô tràn chéo từ trên trái xuống, bút chì quẹt theo mép tô rồi bay ra.
//   5. Tướng bật ra: tranh và nét chì tắt, hình thật (sticker viền giấy) nảy lên, diễn chiêu cuối tại chỗ (chiêu nhảy đè
//      thì đòn đánh) rồi đứng lặp; sao trắng viền mực bắn ra, lấp lánh quanh tướng.
//   6. Ruy băng TƯỚNG MỚI! đóng xuống, khối chữ dưới tướng nảy ra: tên, bậc, hệ, danh hiệu, 3 dòng chỉ số (StatPips), nút Xem tướng /
//      Tiếp. Chạm màn trong lúc vẽ thì vẽ xong ngay và bật ra.
// Máy không đọc được ảnh từ GPU (không hỗ trợ AsyncGPUReadback): bỏ bước lần viền, gạch và tô trong hộp ước theo khung rig.
using System;
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HeroUnlockView : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image rarityBg, page, pencil; // nền màu bậc (lộ quanh mép trang), trang sổ, bút chì (gốc ở ngòi)
            public RectTransform hero, art, info, fx; // hero: chỗ tướng trên trang (gốc ở chân); art: khung hình (con của hero); info: khối chữ
            public RawImage drawing; // tranh chì (material UIPencilDraw)
            public InkStroke ink; // nét viền
            public Image[] stars; // sao trắng (bay ra) rồi lấp lánh (nháy tại chỗ), con của fx
            public int bigStars; // số sao bay ra đầu mảng, còn lại là lấp lánh
            public Image badgeIcon, ribbon;
            public TextMeshProUGUI ribbonText, heroName, rarity, title, elem;
            public Image rarityPill;
            public SketchButton next, view;
            public Button catcher;
            public StatPips[] stats; // Máu, Công, Thủ: số kèm 5 nấc bình hành (như màn chọn tướng khởi đầu)
        }

        [SerializeField] Parts p;

        public const int Rows = 7; // số hàng gạch zích zắc (material UIPencilDraw đặt _Rows bằng số này)
        const float F = 1 / 60f; // một khung
        const float RigH = 680; // chiều cao dáng đứng của rig trên trang
        const float HeroH = 860; // chiều cao khung chân dung (tướng chiếm ~80%)
        const float PenIn = 0.22f, Travel = 0.1f, OutlineSpeed = 1900, OutlineMin = 0.75f, OutlineMax = 1.3f;
        const float HatchT = 0.7f, ColorT = 0.5f;
        static readonly Queue<(string hero, Action done)> queue = new Queue<(string, Action)>();
        public static bool Playing { get; private set; }

        bool tapped, closing;
        Vector2 heroHome, pageHome, ribbonHome;
        int tier;
        AolaSticker rig;
        string rigClip = Game.AolaActor.Idle;
        float rigT, rigAlpha = 1;
        bool rigLoop = true, rigFrozen;
        RectTransform portrait;
        Graphic[] portraitG;
        float scribble = -1; // độ to tiếng bút chì lặp (khoá "pencil", ArtGen/Sfx/but_chi), gửi mỗi khung; 0 thì nhỏ dần rồi thôi gửi
        Rect box = new Rect(0, 0, 1, 1); // hộp quanh hình, theo uv 0–1 của khung nguồn
        List<Vector2[]> loopsUv; // các vòng viền, uv 0–1 của khung nguồn

        public void Setup(Parts parts) => p = parts;

        // xếp hàng: nhiều tướng mới cùng lúc thì lần lượt; done gọi khi tướng cuối đóng
        public static void Play(IEnumerable<string> heroes, Action done = null)
        {
            var list = new List<string>();
            foreach (var h in heroes)
                if (!string.IsNullOrEmpty(h) && App.Data.Hero(h) != null && !list.Contains(h)) list.Add(h);
            if (list.Count == 0)
            {
                done?.Invoke();
                return;
            }
            for (int i = 0; i < list.Count; i++) queue.Enqueue((list[i], i == list.Count - 1 ? done : null));
            if (!Playing) Next();
        }

        // tướng vừa mở khoá trong một lô thưởng (mảnh đủ mở khoá)
        public static List<string> Unlocked(IEnumerable<Reward> rewards)
        {
            var l = new List<string>();
            if (rewards == null) return l;
            foreach (var r in rewards)
                if (r != null && r.k == RewardKind.Shards && r.res != null && r.res.unlocked) l.Add(r.res.hero ?? r.hero);
            return l;
        }

        static void Next()
        {
            if (queue.Count == 0)
            {
                Playing = false;
                return;
            }
            var (hero, done) = queue.Dequeue();
            var prefab = Theme.Prefabs ? Theme.Prefabs.heroUnlock : null;
            if (!prefab)
            {
                done?.Invoke();
                Next();
                return;
            }
            Playing = true;
            var v = Ui.Spawn(prefab, App.Modals.transform);
            v.name = "mo_khoa_tuong";
            var rt = (RectTransform)v.transform;
            rt.Stretch();
            rt.SetAsLastSibling();
            App.I.StartCoroutine(v.Run(App.Data.Hero(hero), () =>
            {
                done?.Invoke();
                Next();
            }));
        }

        IEnumerator Run(HeroDef h, Action done)
        {
            tier = (int)h.rarity;
            var tc = Theme.Of(h.rarity);
            heroHome = p.hero.anchoredPosition;
            pageHome = p.page.rectTransform.anchoredPosition;
            ribbonHome = p.ribbon.rectTransform.anchoredPosition;
            p.catcher.onClick.AddListener(() => tapped = true);

            p.ribbonText.text = Loc.T("TƯỚNG MỚI!");
            p.heroName.text = h.name;
            p.rarity.text = Elements.RarityName(h.rarity).ToUpperInvariant();
            p.rarityPill.color = tc;
            p.rarity.color = tc.grayscale > 0.62f ? Theme.Ink : Color.white;
            p.title.text = h.title ?? "";
            p.elem.text = Loc.F("Hệ {0}", Elements.Name(h.elem));
            Theme.SetSprite(p.badgeIcon, App.Art.Icon(ElemIcon(h.elem)));
            p.rarityBg.color = tc;
            // chỉ số lúc này (cấp người chơi, sao của tướng, như hộp chi tiết); nấc theo thứ hạng trong các tướng cùng độ hiếm
            var save = App.Save?.Data;
            var owned = save?.Hero(h.id);
            var st = HeroStats.Compute(App.Data.Cfg, h, save != null ? save.level : 1, owned != null ? owned.star : 1, false,
                save != null ? Potential.Mods(save, App.Data, h) : null);
            int[] statVal = { (int)st.hp, (int)st.atk, (int)st.def };
            var statPips = StatPips.RarityPips(App.Data, h);

            p.info.gameObject.SetActive(false);
            p.ribbon.gameObject.SetActive(false);
            p.pencil.gameObject.SetActive(false);
            p.drawing.gameObject.SetActive(false);
            p.ink.gameObject.SetActive(false);
            foreach (var s in p.stars) s.gameObject.SetActive(false);

            // 1. trang sổ trượt lên; trong lúc đó dựng hình ẩn và đọc viền
            App.Audio.Play("whoosh", 0.7f, 0.9f);
            Haptics.Play(Haptic.UiOpen);
            StartCoroutine(Slide(p.page.rectTransform, pageHome + new Vector2(0, -1900), pageHome, 20, 36));
            var form = HeroArt.FormOf(h).aola;
            bool hasForm = !string.IsNullOrEmpty(form);
            // rig nằm trong gói tải sau (GD_Claude/27): xin nạp, chờ tối đa 0,8 s rồi dùng chân dung
            for (float w = 0; hasForm && !Game.AolaActor.Ready(form) && w < 0.8f; w += Time.unscaledDeltaTime) yield return null;
            Texture tex = null;
            var uv = new Rect(0, 0, 1, 1);
            RectTransform over = null;
            float premul = 0;
            if (hasForm && Game.AolaActor.Ready(form)) rig = AolaSticker.TryCreate(p.art, h, form, RigH, false, 2048);
            if (rig != null)
            {
                rig.HideShadow();
                rigAlpha = 0;
                rigFrozen = true;
                var img = rig.Rect.GetComponentInChildren<RawImage>(true);
                tex = img.texture;
                over = img.rectTransform;
                premul = 1;
                // hộp ước theo khung rig (khung = chiều cao dáng đứng x span, chân ở 20%): dùng khi không đọc được ảnh
                float span = Mathf.Max(1, over.rect.height / RigH);
                box = Rect.MinMaxRect(0.5f - 0.6f / span, 0.2f - 0.03f / span, 0.5f + 0.6f / span, 0.2f + 1.1f / span);
                for (int i = 0; i < 3; i++) yield return null; // camera chụp khung đầu
            }
            else
            {
                portrait = HeroArt.Portrait(p.art, h, HeroH, false);
                portrait.anchorMin = portrait.anchorMax = new Vector2(0.5f, 0);
                portrait.pivot = new Vector2(0.5f, 0);
                portrait.anchoredPosition = Vector2.zero;
                portraitG = portrait.GetComponentsInChildren<Graphic>(true);
                Image body = null;
                foreach (var g in portraitG)
                    if (g is Image im && im.sprite && (!body || im.rectTransform.rect.height > body.rectTransform.rect.height))
                        body = im;
                SetAlpha(portraitG, 0);
                if (body)
                {
                    tex = body.sprite.texture;
                    var r = body.sprite.textureRect;
                    uv = new Rect(r.x / tex.width, r.y / tex.height, r.width / tex.width, r.height / tex.height);
                    over = body.rectTransform;
                }
                box = new Rect(0.08f, 0.04f, 0.84f, 0.92f);
                yield return null;
            }
            if (tex) yield return Analyse(tex, uv);

            // tranh chì và nét viền phủ đúng khung nguồn
            var penR = p.pencil.rectTransform;
            if (over)
            {
                var dr = p.drawing.rectTransform;
                dr.SetParent(over, false);
                dr.anchorMin = box.min;
                dr.anchorMax = box.max;
                dr.offsetMin = dr.offsetMax = Vector2.zero;
                dr.localScale = Vector3.one;
                p.drawing.texture = tex;
                p.drawing.uvRect = new Rect(uv.x + box.x * uv.width, uv.y + box.y * uv.height, box.width * uv.width, box.height * uv.height);
                p.drawing.color = new Color(0, 0, premul, 1);
                p.drawing.gameObject.SetActive(true);
                var ir = p.ink.rectTransform;
                ir.SetParent(over, false);
                ir.anchorMin = Vector2.zero;
                ir.anchorMax = Vector2.one;
                ir.pivot = Vector2.zero;
                ir.offsetMin = ir.offsetMax = Vector2.zero;
                ir.localScale = Vector3.one;
                var size = over.rect.size;
                var loops = new List<Vector2[]>();
                if (loopsUv != null)
                    foreach (var l in loopsUv)
                    {
                        var q = new Vector2[l.Length];
                        for (int k = 0; k < l.Length; k++) q[k] = Vector2.Scale(l[k], size);
                        loops.Add(q);
                    }
                p.ink.SetLoops(loops);
                // Sổ Phép "Bìa Sổ" (trang trí): nét viền mang màu hệ của tướng
                if (save != null && SoPhep.HasCover(save, App.Data.Cfg)) p.ink.color = Color.Lerp(Theme.Of(h.elem), Theme.Ink, 0.3f);
                p.ink.gameObject.SetActive(true);
            }

            // điểm trên khung nguồn (toạ độ cục bộ của nét viền) → toạ độ của bút chì
            var root = (RectTransform)transform;
            Vector2 Pen(Vector2 inkLocal) => root.InverseTransformPoint(p.ink.rectTransform.TransformPoint(inkLocal));
            Vector2 BoxPt(float x, float y)
            {
                var s = p.ink.rectTransform.rect.size;
                return Vector2.Scale(new Vector2(box.x + x * box.width, box.y + y * box.height), s);
            }
            void Wobble(float t)
            {
                penR.localEulerAngles = new Vector3(0, 0, Mathf.Sin(t * 37) * 3);
                penR.localScale = Vector3.one * (1 + 0.025f * Mathf.Sin(t * 53));
            }

            if (over)
            {
                // 2. bút chì bay vào chỗ bắt đầu, lần theo các vòng viền
                penR.gameObject.SetActive(true);
                penR.SetAsLastSibling();
                scribble = 0.8f;
                Vector2 first = p.ink.Count > 0 ? Pen(p.ink.LoopStart(0)) : Pen(BoxPt(0, 1));
                Vector2 enter = first + new Vector2(520, -760);
                for (float t = 0; t < PenIn && !tapped; t += Time.unscaledDeltaTime)
                {
                    float k = 1 - (1 - t / PenIn) * (1 - t / PenIn);
                    penR.anchoredPosition = Vector2.Lerp(enter, first, k);
                    Wobble(t);
                    yield return null;
                }
                float total = p.ink.Total;
                float speed = total / Mathf.Clamp(total / OutlineSpeed, OutlineMin, OutlineMax);
                float drawn = 0, clock = 0;
                for (int li = 0; li < p.ink.Count && !tapped; li++)
                {
                    if (li > 0) // nhấc bút sang vòng kế: cung lên, to hơn chút
                    {
                        Vector2 a = penR.anchoredPosition, b = Pen(p.ink.LoopStart(li));
                        for (float t = 0; t < Travel && !tapped; t += Time.unscaledDeltaTime)
                        {
                            float k = t / Travel;
                            penR.anchoredPosition = Vector2.Lerp(a, b, k * k * (3 - 2 * k)) + new Vector2(0, Mathf.Sin(k * Mathf.PI) * 40);
                            penR.localScale = Vector3.one * (1 + 0.08f * Mathf.Sin(k * Mathf.PI));
                            yield return null;
                        }
                    }
                    float len = p.ink.LoopLength(li);
                    for (float d = 0; d < len && !tapped; d += speed * Time.unscaledDeltaTime)
                    {
                        clock += Time.unscaledDeltaTime;
                        p.ink.Drawn = drawn + d;
                        penR.anchoredPosition = Pen(p.ink.PointOn(li, d));
                        Wobble(clock);
                        yield return null;
                    }
                    drawn += len;
                    p.ink.Drawn = drawn;
                }

                // 3. gạch zích zắc từng hàng từ trên xuống (đúng công thức hàng của shader)
                for (float t = 0; t < HatchT && !tapped; t += Time.unscaledDeltaTime)
                {
                    float k = t / HatchT;
                    p.drawing.color = new Color(k, 0, premul, 1);
                    float rf = k * Rows;
                    int row = Mathf.Min(Rows - 1, (int)rf);
                    float xr = rf - row;
                    float x = row % 2 == 0 ? xr : 1 - xr;
                    float y = 1 - (row + 0.5f + 0.3f * Mathf.Sin(t * 70)) / Rows;
                    penR.anchoredPosition = Pen(BoxPt(x, y));
                    Wobble(t);
                    yield return null;
                }

                // 4. sáp màu tô tràn chéo, bút quẹt qua lại theo mép tô
                for (float t = 0; t < ColorT && !tapped; t += Time.unscaledDeltaTime)
                {
                    float k = t / ColorT;
                    p.drawing.color = new Color(1, k, premul, 1);
                    float front = k * 1.3f - 0.1f, s = Mathf.PingPong(t * 7, 1);
                    float y = Mathf.Clamp01(1 - (front - 0.35f * s) / 0.65f);
                    penR.anchoredPosition = Pen(BoxPt(s, y));
                    Wobble(t);
                    yield return null;
                }
                p.ink.Drawn = p.ink.Total;
                p.drawing.color = new Color(1, 1, premul, 1);
                StartCoroutine(PenOut(penR));
            }

            // 5. tướng bật ra
            if (scribble > 0) scribble = 0;
            p.drawing.gameObject.SetActive(false);
            p.ink.gameObject.SetActive(false);
            // gói rig về trong lúc vẽ: đổi chân dung sang rig
            if (rig == null && hasForm && Game.AolaActor.Ready(form))
            {
                rig = AolaSticker.TryCreate(p.art, h, form, RigH, false, 2048);
                if (rig != null)
                {
                    rig.HideShadow();
                    if (portrait) portrait.gameObject.SetActive(false);
                }
            }
            if (rig != null)
            {
                rigAlpha = 1;
                rigFrozen = false;
                rigClip = !rig.Jumps ? StageView.Skill : StageView.Attack; // tại chỗ (clip ra sân có con bay từ ngoài vào, lệch khỏi trang)
                rigT = 0;
                rigLoop = false;
            }
            else if (portraitG != null) SetAlpha(portraitG, 1);
            StartCoroutine(KeysPos(p.hero, new[] { V(0.8f, 0.8f), V(1.14f, 1.14f), V(0.95f, 0.95f), V(1, 1) },
                new[] { heroHome, heroHome + new Vector2(0, 70), heroHome + new Vector2(0, -8), heroHome }, new[] { 0, 7, 14, 20 }));
            StartCoroutine(Burst());
            App.Audio.Play("chest");
            App.Audio.Play("stamp", 0.9f, 0.85f);
            Haptics.Play(tier >= (int)Rarity.Epic ? Haptic.OpenGold : Haptic.OpenSilver);

            // 6. ruy băng đóng xuống, khối chữ nảy ra, chỉ số đầy dần
            yield return Frames(10);
            p.ribbon.gameObject.SetActive(true);
            StartCoroutine(KeysPos(p.ribbon.rectTransform, new[] { V(1.4f, 1.4f), V(0.92f, 0.92f), V(1, 1) },
                new[] { ribbonHome + new Vector2(0, 60), ribbonHome, ribbonHome }, new[] { 0, 6, 10 }));
            App.Audio.Play("stamp");
            Haptics.Play(Haptic.Stamp);
            yield return Frames(6);
            p.info.gameObject.SetActive(true);
            StartCoroutine(Pop(p.info));
            if (p.stats != null)
                for (int k = 0; k < p.stats.Length && k < 3; k++)
                    if (p.stats[k]) p.stats[k].Set(TeamPower.Text(statVal[k]), statPips[k], 0.2f + 0.1f * k);

            // nút
            p.next.SetText(Loc.T("Tiếp"));
            bool done2 = false, toHero = false;
            p.next.SetOnClick(() => done2 = true);
            p.view.gameObject.SetActive(App.Router != null);
            p.view.SetText(Loc.T("Xem tướng"));
            p.view.SetOnClick(() =>
            {
                toHero = true;
                done2 = true;
            });
            yield return Frames(14);
            StartCoroutine(Pop(p.next.Rect));
            float nextNudge = Time.unscaledTime + 3;
            tapped = false;
            while (!done2)
            {
                if (Time.unscaledTime > nextNudge)
                {
                    nextNudge = Time.unscaledTime + 3;
                    StartCoroutine(Pop(p.next.Rect));
                }
                yield return null;
            }
            closing = true;
            for (float t = 0; t < 0.18f; t += Time.unscaledDeltaTime)
            {
                if (TryGetComponent<CanvasGroup>(out var cg)) cg.alpha = 1 - t / 0.18f;
                yield return null;
            }
            Playing = queue.Count > 0;
            rig?.Destroy();
            rig = null;
            Destroy(gameObject);
            if (toHero)
            {
                queue.Clear();
                App.Modals.CloseAll();
                App.Router.Go(SceneIds.Heroes);
            }
            done?.Invoke();
        }

        // đọc độ phủ: lượt 1 cả khung nguồn 128 x 128 tìm hộp quanh hình; lượt 2 cắt đúng hộp, cạnh dài 256, lấy vòng viền
        IEnumerator Analyse(Texture tex, Rect uv)
        {
            if (!SystemInfo.supportsAsyncGPUReadback) yield break;
            byte[] a1 = null;
            yield return ReadAlpha(tex, uv, 128, 128, r => a1 = r);
            var b = a1 != null ? Contour.Bounds(a1, 128, 128) : null;
            if (b == null) yield break;
            box = Rect.MinMaxRect(Mathf.Max(0, b[0] - 2) / 128f, Mathf.Max(0, b[1] - 2) / 128f, Mathf.Min(128, b[2] + 3) / 128f,
                Mathf.Min(128, b[3] + 3) / 128f);
            float bw = box.width * uv.width * tex.width, bh = box.height * uv.height * tex.height;
            int w2 = bw >= bh ? 256 : Mathf.Max(16, Mathf.RoundToInt(256 * bw / bh));
            int h2 = bh >= bw ? 256 : Mathf.Max(16, Mathf.RoundToInt(256 * bh / bw));
            var sub = new Rect(uv.x + box.x * uv.width, uv.y + box.y * uv.height, box.width * uv.width, box.height * uv.height);
            byte[] a2 = null;
            yield return ReadAlpha(tex, sub, w2, h2, r => a2 = r);
            if (a2 == null) yield break;
            loopsUv = new List<Vector2[]>();
            foreach (var l in Contour.Loops(a2, w2, h2))
            {
                var q = new Vector2[l.Length / 2];
                for (int k = 0; k < q.Length; k++)
                    q[k] = new Vector2(box.x + l[2 * k] / w2 * box.width, box.y + l[2 * k + 1] / h2 * box.height);
                loopsUv.Add(q);
            }
        }

        // chép vùng uv của ảnh vào RenderTexture tạm w x h rồi đọc kênh alpha (hàng dưới trước); lỗi hoặc quá 1 s thì null
        static IEnumerator ReadAlpha(Texture tex, Rect uv, int w, int h, Action<byte[]> got)
        {
            var rt = RenderTexture.GetTemporary(w, h, 0, RenderTextureFormat.ARGB32);
            Graphics.Blit(tex, rt, uv.size, uv.position);
            byte[] res = null;
            bool finished = false;
            AsyncGPUReadback.Request(rt, 0, TextureFormat.RGBA32, r =>
            {
                if (!r.hasError)
                {
                    var d = r.GetData<byte>();
                    res = new byte[w * h];
                    for (int i = 0; i < res.Length; i++) res[i] = d[i * 4 + 3];
                }
                finished = true;
            });
            for (float t = 0; !finished && t < 1; t += Time.unscaledDeltaTime) yield return null;
            if (!finished) AsyncGPUReadback.WaitAllRequests();
            RenderTexture.ReleaseTemporary(rt);
            got(res);
        }

        // bút chì bay ra góc trên phải rồi tắt
        IEnumerator PenOut(RectTransform pen)
        {
            Vector2 a = pen.anchoredPosition, b = a + new Vector2(700, 900);
            for (float t = 0; t < 0.25f; t += Time.unscaledDeltaTime)
            {
                float k = t / 0.25f;
                pen.anchoredPosition = Vector2.Lerp(a, b, k * k);
                pen.localEulerAngles = new Vector3(0, 0, -25 * k);
                yield return null;
            }
            pen.gameObject.SetActive(false);
        }

        // sao trắng bắn ra từ thân tướng (chậm dần, xoay, thu nhỏ rồi tắt), lấp lánh nháy tại chỗ quanh tướng, lệch nhịp
        IEnumerator Burst()
        {
            var fx = p.fx;
            Vector2 c = (Vector2)fx.InverseTransformPoint(p.hero.TransformPoint(new Vector3(0, RigH * 0.45f, 0)));
            int n = p.stars.Length, big = Mathf.Min(p.bigStars, n);
            var pos = new Vector2[n];
            var vel = new Vector2[n];
            var life = new float[n];
            var delay = new float[n];
            var size = new float[n];
            var spin = new float[n];
            for (int i = 0; i < n; i++)
            {
                var rnd = new System.Random(i * 7919 + tier);
                float R(float a, float b) => a + (b - a) * (float)rnd.NextDouble();
                if (i < big)
                {
                    float ang = (i + R(-0.3f, 0.3f)) / big * Mathf.PI * 2;
                    var dir = new Vector2(Mathf.Cos(ang), Mathf.Sin(ang));
                    pos[i] = c + dir * R(60, 140);
                    vel[i] = dir * R(900, 1500);
                    life[i] = R(0.55f, 0.85f);
                    size[i] = R(0.75f, 1.15f);
                    spin[i] = R(-400, 400);
                }
                else
                {
                    float ang = R(0, Mathf.PI * 2);
                    pos[i] = c + new Vector2(Mathf.Cos(ang) * R(220, 380), Mathf.Sin(ang) * R(200, 420));
                    delay[i] = R(0.12f, 0.7f);
                    life[i] = R(0.3f, 0.45f);
                    size[i] = R(0.6f, 1);
                    spin[i] = R(-90, 90);
                }
                p.stars[i].rectTransform.anchoredPosition = pos[i];
                p.stars[i].rectTransform.localScale = Vector3.zero;
                p.stars[i].gameObject.SetActive(true);
            }
            float end = 0;
            for (int i = 0; i < n; i++) end = Mathf.Max(end, delay[i] + life[i]);
            for (float t = 0; t < end; t += Time.unscaledDeltaTime)
            {
                float dt = Time.unscaledDeltaTime;
                for (int i = 0; i < n; i++)
                {
                    var r = p.stars[i].rectTransform;
                    float u = (t - delay[i]) / life[i];
                    if (u < 0 || u > 1)
                    {
                        r.localScale = Vector3.zero;
                        continue;
                    }
                    float s;
                    if (i < big)
                    {
                        pos[i] += vel[i] * dt;
                        vel[i] *= Mathf.Max(0, 1 - 4.5f * dt);
                        r.anchoredPosition = pos[i];
                        s = u < 0.12f ? u / 0.12f : u > 0.6f ? 1 - (u - 0.6f) / 0.4f : 1;
                    }
                    else s = Mathf.Sin(u * Mathf.PI); // nháy: to lên rồi nhỏ lại
                    r.localScale = Vector3.one * (size[i] * s);
                    r.localEulerAngles = new Vector3(0, 0, spin[i] * t);
                }
                yield return null;
            }
            foreach (var s in p.stars) s.gameObject.SetActive(false);
        }

        static void SetAlpha(Graphic[] gs, float a)
        {
            foreach (var g in gs)
                if (g)
                {
                    var c = g.color;
                    g.color = new Color(c.r, c.g, c.b, a);
                }
        }

        void OnDestroy()
        {
            if (scribble > 0 && App.Audio != null) App.Audio.Loop("pencil", 0);
            rig?.Destroy();
            rig = null;
        }

        static string ElemIcon(Elem e) => e == Elem.Hoa ? "e_hoa" : e == Elem.Thuy ? "e_thuy" : e == Elem.Moc ? "e_moc" : e == Elem.Kim ? "e_kim" : "e_tho";

        static Vector2 V(float x, float y) => new Vector2(x, y);

        static IEnumerator Frames(int n)
        {
            for (float t = 0; t < n * F; t += Time.unscaledDeltaTime) yield return null;
        }

        static IEnumerator KeysPos(RectTransform rt, Vector2[] scale, Vector2[] pos, int[] at)
        {
            float total = at[at.Length - 1] * F;
            for (float t = 0; t < total; t += Time.unscaledDeltaTime)
            {
                float fr = t / F;
                int i = 0;
                while (i < at.Length - 2 && fr > at[i + 1]) i++;
                float k = Mathf.InverseLerp(at[i], at[i + 1], fr);
                var s = Vector2.Lerp(scale[i], scale[i + 1], k);
                rt.localScale = new Vector3(s.x, s.y, 1);
                rt.anchoredPosition = Vector2.Lerp(pos[i], pos[i + 1], k);
                yield return null;
            }
            var e = scale[scale.Length - 1];
            rt.localScale = new Vector3(e.x, e.y, 1);
            rt.anchoredPosition = pos[pos.Length - 1];
        }

        // trượt vào: tới chỗ trong 70% thời gian, vượt over px, rồi về (dễ dần)
        static IEnumerator Slide(RectTransform rt, Vector2 from, Vector2 to, int frames, float over)
        {
            float d = frames * F, a = 0.7f;
            var dir = (to - from).normalized;
            for (float t = 0; t < d; t += Time.unscaledDeltaTime)
            {
                float k = t / d;
                Vector2 pos;
                if (k < a)
                {
                    float u = k / a;
                    pos = Vector2.LerpUnclamped(from, to + dir * over, 1 - (1 - u) * (1 - u) * (1 - u));
                }
                else
                {
                    float u = (k - a) / (1 - a);
                    pos = Vector2.Lerp(to + dir * over, to, u * u * (3 - 2 * u));
                }
                rt.anchoredPosition = pos;
                yield return null;
            }
            rt.anchoredPosition = to;
        }

        static IEnumerator Pop(RectTransform rt)
        {
            // nảy nhắc 1 → 1,17 → 0,92 → 1 trong 0,25 s
            float[] at = { 0, 0.08f, 0.17f, 0.25f };
            float[] s = { 1, 1.17f, 0.92f, 1 };
            for (float t = 0; t < 0.25f; t += Time.unscaledDeltaTime)
            {
                int i = 0;
                while (i < at.Length - 2 && t > at[i + 1]) i++;
                rt.localScale = Vector3.one * Mathf.Lerp(s[i], s[i + 1], Mathf.InverseLerp(at[i], at[i + 1], t));
                yield return null;
            }
            rt.localScale = Vector3.one;
        }

        void Update()
        {
            if (scribble >= 0)
            {
                App.Audio.Loop("pencil", scribble);
                if (scribble == 0) scribble = -1;
            }
            if (rig == null) return;
            // trước lúc bật ra: đứng yên khung đầu dáng đứng, ẩn (tranh chì lấy ảnh này); sau: clip một lần rồi đứng lặp
            if (!rigFrozen)
            {
                rigT += Time.unscaledDeltaTime;
                if (!rigLoop && rigT >= rig.Duration(rigClip))
                {
                    rigClip = Game.AolaActor.Idle;
                    rigT = 0;
                    rigLoop = true;
                }
            }
            rig.Show(rigFrozen ? Game.AolaActor.Idle : rigClip, rigFrozen ? 0 : rigT, rigFrozen || rigLoop, rigAlpha, false, 0);
        }
    }
}
