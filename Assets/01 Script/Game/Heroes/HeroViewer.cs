// Ô xem tướng trong hộp chi tiết: chạy 4 clip Đứng, Đánh, Chiêu, Trúng (chép openHero của Web/src/view/screens/heroes.ts).
// Dáng đứng cỡ 70% ô, chân sát đáy; đánh và chiêu giữ cỡ 60%, neo ở 32% chiều ngang (vệt đòn bay xa thì bị cắt ở mép ô).
// Ô (khung cắt) rộng bằng khung nền sân khấu, các tỉ lệ trên tính theo cạnh ô vuông size, tâm ở giữa đáy.
// Prefab Assets/04 Prefabs/Items/OXemTuong: khung cắt, chân dung (kit ChanDung), lớp nháy (không dùng nữa, luôn tắt). Có aola
// (bản dev, ngoại lệ đã chốt: AolaSticker tự sinh lúc chạy) thì ẩn chân dung; tướng chưa có (bóng sẫm) thì chân dung aola tĩnh
// với hoạt cảnh giả (nhún, lao, phồng, giật lùi). Không có ảnh aola nào thì ô trống.
// Không dựng sticker trong khung chạm (người dùng dặn phản hồi phải ngay, 2026-11-07): Bind chỉ ghi tướng cần hiện, Update dựng ở
// khung sau khi animation đã đọc xong ở luồng phụ (AolaActor.Ready) và khung đó chưa ai dựng (AolaSticker.CanBuildNow). Trong lúc chờ:
// đổi dạng (tiến hóa) thì giữ sticker cũ, mở hộp thì hiện chân dung tĩnh.
// Dạng cũ có clip tiến hóa (dạng .atomik, 2026-11-08): đổi dạng thì phát clip đó trên sticker cũ, giữ khung cuối tới khi sticker
// dạng mới dựng xong (khung cuối trùng dáng đứng dạng mới nên không giật), rồi về Đứng; clip gọi trong lúc đó bỏ qua.
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HeroViewer : MonoBehaviour
    {
        public const string Idle = StageView.Idle, Attack = StageView.Attack, Skill = StageView.Skill, Hit = StageView.Hit;
        public const string Cast = StageView.Cast; // nút Mana: clip bắn + chiêu mana bằng hạt (tướng Hỏa)
        public const string Evolve = Game.AolaActor.Evolve;

        [SerializeField] RectTransform box;
        [SerializeField] HeroPortrait portrait;
        [SerializeField] Image flash;
        // hạt chồng lớp (HatLua, bộ Hỏa 2026-11-10): lớp chứa trong khung cắt, neo giữa đáy ô; gán bằng menu
        // "PokiClash/Prefab/Hộp chi tiết tướng: hạt lửa + nút Mana". Tướng Hỏa: Chiêu nổ tuyệt kỹ hạt, Mana bắn chiêu mana hạt,
        // vào một điểm đích ảo trước mặt (bảng chiêu ở StageView.FireFx)
        [SerializeField] Image hatPrefab;
        [SerializeField] RectTransform hatFloor, hatBack, hatFront;
        [SerializeField] Sprite[] hatSprites;
        HatLua hat;
        HeroDef shown;
        bool fxFired;
        const float FxH = 150; // chiều cao tướng chuẩn của công thức (đơn vị sân)

        HatLua Hat
        {
            get
            {
                if (hat == null && hatPrefab && hatFloor && hatBack && hatFront)
                    hat = new HatLua(hatPrefab, hatFloor, hatBack, hatFront, hatSprites);
                return hat != null && hat.Ready ? hat : null;
            }
        }

        // tỉ lệ lớp hạt: tướng chuẩn FxH đơn vị sân cao bằng tướng đang hiện lúc ra đòn (60% cạnh ô)
        float FxScale => size * 0.6f / (StageView.K * FxH);

        // lúc trúng của clip Chiêu / Mana: phát hạt tại chỗ (toạ độ sân, gốc ở giữa đáy ô, y xuống)
        // dạng đang hiện của tướng (0 là dạng đầu)
        int FormIdx
        {
            get
            {
                if (shown == null || shown.forms == null) return 0;
                string id = HeroArt.FormOf(shown).aola;
                for (int i = 0; i < shown.forms.Length; i++)
                    if (shown.forms[i].aola == id) return i;
                return 0;
            }
        }

        // chỗ đứng, miệng, đích ảo trong ô xem (toạ độ sân, gốc giữa đáy ô, y xuống)
        void FxGeo(out Vector2 feet, out Vector2 mouth, out Vector2 foe, out Vector2 foeBody)
        {
            float u = StageView.K * FxScale; // px ô cho 1 đơn vị sân
            foreach (var g in new[] { hatFloor, hatBack, hatFront }) g.localScale = new Vector3(FxScale, FxScale, 1);
            feet = new Vector2(-0.18f * size, -0.2f * size) / u;
            float half = box.rect.width * 0.5f / u;
            foe = new Vector2(Mathf.Min(feet.x + 210, half - 90), feet.y - 12); // đủ chỗ cho lốc, thiên thạch trong khung cắt
            foeBody = foe + new Vector2(0, -0.45f * FxH);
            mouth = feet + new Vector2(0.3f * FxH, -0.62f * FxH);
        }

        // chiêu nước (bộ Thủy): phát ngay lúc clip bắt đầu, nước nhả đúng khung trúng (như StageView.PreFx)
        void PreFx(string c)
        {
            if (c != Skill && c != Cast) return;
            var h = Hat;
            if (h == null || shown == null) return;
            bool ult = c == Skill;
            string kind = ult ? StageView.FireUlt(shown, FormIdx) : StageView.FireMana(shown);
            if (!HatLua.IsNuoc(kind) || HatLua.NuocAtHit(kind) || !h.HasWater) return;
            FxGeo(out var feet, out var mouth, out var foe, out var foeBody);
            float lead = aola != null ? aola.HitTime(c) : Len(c) * 0.55f;
            h.UseTheme(shown.id);
            h.PlayNuoc(kind, ult, feet, FxH, mouth, foe, foeBody, FxH, lead);
            fxFired = true; // khung trúng không phát lại
            holdAt = lead;
            holdLeft = lead + HatLua.HoldNuoc(kind, ult);
        }

        void FireFx(string c)
        {
            var h = Hat;
            if (h == null || shown == null) return;
            string kind = c == Skill ? StageView.FireUlt(shown, FormIdx) : StageView.FireMana(shown);
            if (kind == null) return;
            FxGeo(out var feet, out var mouth, out var foe, out var foeBody);
            h.UseTheme(shown.id);
            if (HatLua.IsNuoc(kind))
            {
                if (HatLua.NuocAtHit(kind) && h.HasWater) h.PlayNuoc(kind, c == Skill, feet, FxH, feet, foe, foeBody, FxH, 0);
                return;
            }
            if (c == Skill) h.PlayUlt(kind, foe, foeBody, FxH, -1);
            else
            {
                h.PlayMana(kind, feet, FxH, mouth, foe, foeBody, FxH);
                holdAt = t; // giữ dáng ra chiêu: phun tới khi luồng tắt, kim tới khi phóng hết, cầu tới khi rời miệng
                holdLeft = HatLua.HoldOf(kind);
            }
        }

        float holdAt, holdLeft;

        RectTransform body;
        AolaSticker aola;
        HeroDef waitHero; // sticker cần dựng ở khung sau (đang chờ animation đọc xong ở luồng phụ)
        string waitForm;
        int bindFrame; // khung gọi Bind (khung chạm): không dựng trong khung này
        string aolaKey; // "<tướng>|<dạng>" của sticker đang hiện: lên sao không đổi dạng thì giữ nguyên
        string clip = Idle;
        float t, size;
        bool silhouette;
        bool evolving; // đang phát clip tiến hóa của dạng cũ
        string afterEvolve; // clip được gọi trong lúc tiến hóa, chạy khi dạng mới hiện

        // Dùng khi nướng prefab (Editor).
        public void Setup(RectTransform boxRt, HeroPortrait portraitView, Image flashImg)
        {
            box = boxRt;
            portrait = portraitView;
            flash = flashImg;
        }

        // size: cạnh ô vuông; silhouette: bóng sẫm (tướng chưa có), không dùng aola
        public void Bind(HeroDef hero, float boxSize, bool isSilhouette)
        {
            waitHero = null;
            bindFrame = Time.frameCount;
            size = boxSize;
            shown = hero;
            hat?.Clear();
            silhouette = isSilhouette;
            // ô kéo ngang bằng khung nền sân khấu, cao bằng cạnh ô: mặt nạ không cắt hai bên (người dùng dặn 2026-11-08).
            // Thân neo giữa đáy ô nên chỗ đứng không đổi.
            box.anchorMin = new Vector2(0, box.anchorMin.y);
            box.anchorMax = new Vector2(1, box.anchorMax.y);
            box.anchoredPosition = new Vector2(0, box.anchoredPosition.y);
            box.sizeDelta = new Vector2(0, size);
            var form = HeroArt.FormOf(hero).aola;
            if (!silhouette && aola != null && aolaKey == hero.id + "|" + form)
            {
                Play(Idle); // cùng tướng cùng dạng (lên sao chưa tới mốc đổi dạng): giữ sticker đang chạy
                return;
            }
            if (!silhouette && Game.AolaActor.Find(form, out _, out _))
            {
                waitHero = hero;
                waitForm = form;
                Game.AolaActor.Ready(waitForm); // bắt đầu đọc trước nếu chưa
                // cùng tướng lên dạng mới, dạng cũ có clip tiến hóa: phát trên sticker cũ trước khi đổi
                if (aola != null && aolaKey != null && aolaKey.StartsWith(hero.id + "|") && aola.HasClip(Evolve))
                {
                    evolving = true;
                    afterEvolve = null;
                    clip = Evolve;
                    t = 0;
                    return;
                }
            }
            // có sticker cũ (đổi dạng) thì giữ tới khi cái mới dựng xong; không thì chân dung
            if (waitHero == null || aola == null)
            {
                aola?.Destroy();
                aola = null;
                Attach(hero);
            }
            Play(Idle);
        }

        // thân đang hiện: sticker aola, hoặc chân dung (tĩnh, bóng sẫm, đang chờ animation)
        void Attach(HeroDef hero)
        {
            portrait.gameObject.SetActive(aola == null);
            if (aola != null) body = aola.Rect;
            else
            {
                portrait.Bind(hero, size * 0.7f, silhouette);
                body = portrait.Rect;
            }
            // ảnh chớp từng là mặt nạ hình giữ chỗ (đã bỏ); tướng aola chớp bằng shader sticker
            flash.enabled = false;
            body.anchorMin = body.anchorMax = new Vector2(0.5f, 0);
            body.localEulerAngles = Vector3.zero;
            if (hatFront) hatFront.SetAsLastSibling(); // sticker mới sinh nằm cuối: lớp hạt trước tướng phải trên nó
        }

        public void Play(string c)
        {
            if (evolving)
            {
                afterEvolve = c;
                return;
            }
            clip = c;
            t = 0;
            fxFired = false;
            holdLeft = 0;
            hat?.Clear();
            PreFx(c);
        }

        static float Len(string c) => c == Attack ? 0.8f : c == Skill ? 0.9f : c == Hit ? 0.36f : c == Cast ? AolaSticker.CastLen : 1.2f;

        void OnDestroy() => aola?.Destroy();

        void Update()
        {
            // dựng sticker ở khung sau khung chạm, khi animation đã đọc xong; thay chân dung hoặc sticker cũ (giữ clip đang chạy).
            // Đang tiến hóa: chờ clip tiến hóa của dạng cũ chạy hết.
            bool evolveDone = !evolving || aola == null || t >= aola.Duration(Evolve);
            if (waitHero != null && evolveDone && Time.frameCount > bindFrame && AolaSticker.CanBuildNow && Game.AolaActor.Ready(waitForm))
            {
                var h = waitHero;
                waitHero = null;
                var made = AolaSticker.TryCreate(box, h, waitForm, size * 0.7f, false);
                aola?.Destroy();
                aola = made;
                aolaKey = made != null ? h.id + "|" + waitForm : null;
                Attach(h);
                if (evolving)
                {
                    // khung cuối clip tiến hóa là dáng đứng của dạng mới: về Đứng để liền mạch (clip Chiêu được gọi lúc bấm Tiến hóa
                    // neo nhỏ, lệch trái nên hình nhảy chỗ; chính clip tiến hóa đã khoe dạng mới)
                    evolving = false;
                    clip = Idle;
                    afterEvolve = null;
                    t = 0;
                }
            }
            if (!body) return;
            float dt = Mathf.Min(0.05f, Time.unscaledDeltaTime);
            t += dt;
            if (holdLeft > 0)
            {
                holdLeft -= dt;
                if ((clip == Cast || clip == Skill) && t > holdAt) t = holdAt;
            }
            hat?.Update(dt);
            if (!fxFired && (clip == Skill || clip == Cast) && t >= (aola != null ? aola.HitTime(clip) : Len(clip) * 0.55f))
            {
                fxFired = true;
                FireFx(clip);
            }
            // clip tiến hóa giữ khung cuối tới khi dạng mới dựng xong
            if (clip != Idle && !evolving && t >= (aola != null ? aola.Duration(clip) : Len(clip)))
            {
                clip = Idle;
                t = 0;
            }
            bool idle = clip == Idle;
            // vị trí neo như bản web: đứng giữa, chân ở 94%; đánh và chiêu neo 32% chiều ngang, chân ở 80%; tiến hóa đứng giữa
            bool centre = idle || clip == Hit || clip == Evolve;
            float ax = centre ? 0.5f : 0.32f, ay = centre ? 0.06f : 0.2f;
            float sc = centre ? 1f : 0.6f / 0.7f;
            Vector2 pos = new Vector2((ax - 0.5f) * size, ay * size);
            if (aola != null)
            {
                body.anchoredPosition = pos;
                body.localScale = new Vector3(sc, sc, 1);
                // hiệu ứng ở xa của đòn bắn (đạn, vụ nổ ở chỗ đối thủ của trận gốc): hiện trước mặt trong khung
                if (clip == Attack || clip == Skill || clip == Cast) aola.FarAhead(clip, 1.3f);
                else aola.Far(clip, null, false);
                aola.Show(clip, t, idle, 1, silhouette, 0);
                return;
            }
            // hình giữ chỗ: hoạt cảnh giả cho từng clip
            float k = t / Len(clip);
            float sx = sc, sy = sc, rot = 0, fl = 0;
            switch (clip)
            {
                case Idle:
                    sy *= 1 + Mathf.Sin(t * 4.2f) * 0.025f;
                    break;
                case Attack:
                {
                    float hit = 0.6f;
                    float u = Mathf.Min(1, k / hit), back = k > hit ? (k - hit) / (1 - hit) : 0;
                    pos.x += Mathf.Sin(u * Mathf.PI * 0.5f) * (1 - back) * size * 0.38f;
                    rot = -12 * Mathf.Sin(u * Mathf.PI) * (1 - back);
                    break;
                }
                case Skill:
                {
                    float s = 1 + 0.18f * Mathf.Sin(Mathf.Min(1, k / 0.55f) * Mathf.PI);
                    sx *= s;
                    sy *= s;
                    rot = Mathf.Sin(k * Mathf.PI * 4) * 6 * (1 - k);
                    fl = k < 0.55f ? Mathf.Sin(k / 0.55f * Mathf.PI) * 0.6f : 0;
                    break;
                }
                case Hit:
                    pos.x -= Mathf.Sin(k * Mathf.PI) * size * 0.05f;
                    sx *= 1 - Mathf.Sin(k * Mathf.PI) * 0.08f;
                    fl = (1 - k) * 0.65f;
                    break;
            }
            body.anchoredPosition = pos;
            body.localScale = new Vector3(sx, sy, 1);
            body.localEulerAngles = new Vector3(0, 0, rot);
            if (flash) flash.color = new Color(1, 1, 1, fl);
        }
    }
}
