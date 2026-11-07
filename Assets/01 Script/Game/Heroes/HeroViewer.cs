// Ô xem tướng trong hộp chi tiết: chạy 4 clip Đứng, Đánh, Chiêu, Trúng (chép openHero của Web/src/view/screens/heroes.ts).
// Dáng đứng cỡ 70% ô, chân sát đáy; đánh và chiêu giữ cỡ 60%, neo ở 32% chiều ngang (vệt đòn bay xa thì bị cắt ở mép ô).
// Prefab Assets/04 Prefabs/Items/OXemTuong: khung cắt, chân dung (kit ChanDung), lớp nháy (không dùng nữa, luôn tắt). Có aola
// (bản dev, ngoại lệ đã chốt: AolaSticker tự sinh lúc chạy) thì ẩn chân dung; tướng chưa có (bóng sẫm) thì chân dung aola tĩnh
// với hoạt cảnh giả (nhún, lao, phồng, giật lùi). Không có ảnh aola nào thì ô trống.
// Không dựng sticker trong khung chạm (người dùng dặn phản hồi phải ngay, 2026-11-07): Bind chỉ ghi tướng cần hiện, Update dựng ở
// khung sau khi animation đã đọc xong ở luồng phụ (AolaActor.Ready) và khung đó chưa ai dựng (AolaSticker.CanBuildNow). Trong lúc chờ:
// đổi dạng (tiến hóa) thì giữ sticker cũ, mở hộp thì hiện chân dung tĩnh.
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HeroViewer : MonoBehaviour
    {
        public const string Idle = StageView.Idle, Attack = StageView.Attack, Skill = StageView.Skill, Hit = StageView.Hit;

        [SerializeField] RectTransform box;
        [SerializeField] HeroPortrait portrait;
        [SerializeField] Image flash;

        RectTransform body;
        AolaSticker aola;
        HeroDef waitHero; // sticker cần dựng ở khung sau (đang chờ animation đọc xong ở luồng phụ)
        string waitForm;
        int bindFrame; // khung gọi Bind (khung chạm): không dựng trong khung này
        string aolaKey; // "<tướng>|<dạng>" của sticker đang hiện: lên sao không đổi dạng thì giữ nguyên
        string clip = Idle;
        float t, size;
        bool silhouette;

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
            silhouette = isSilhouette;
            box.sizeDelta = new Vector2(size, size);
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
        }

        public void Play(string c)
        {
            clip = c;
            t = 0;
        }

        static float Len(string c) => c == Attack ? 0.8f : c == Skill ? 0.9f : c == Hit ? 0.36f : 1.2f;

        void OnDestroy() => aola?.Destroy();

        void Update()
        {
            // dựng sticker ở khung sau khung chạm, khi animation đã đọc xong; thay chân dung hoặc sticker cũ (giữ clip đang chạy)
            if (waitHero != null && Time.frameCount > bindFrame && AolaSticker.CanBuildNow && Game.AolaActor.Ready(waitForm))
            {
                var h = waitHero;
                waitHero = null;
                var made = AolaSticker.TryCreate(box, h, waitForm, size * 0.7f, false);
                aola?.Destroy();
                aola = made;
                aolaKey = made != null ? h.id + "|" + waitForm : null;
                Attach(h);
            }
            if (!body) return;
            t += Mathf.Min(0.05f, Time.unscaledDeltaTime);
            if (clip != Idle && t >= (aola != null ? aola.Duration(clip) : Len(clip)))
            {
                clip = Idle;
                t = 0;
            }
            bool idle = clip == Idle;
            // vị trí neo như bản web: đứng giữa, chân ở 94%; đánh và chiêu neo 32% chiều ngang, chân ở 80%
            float ax = idle || clip == Hit ? 0.5f : 0.32f, ay = idle || clip == Hit ? 0.06f : 0.2f;
            float sc = idle || clip == Hit ? 1f : 0.6f / 0.7f;
            Vector2 pos = new Vector2((ax - 0.5f) * size, ay * size);
            if (aola != null)
            {
                body.anchoredPosition = pos;
                body.localScale = new Vector3(sc, sc, 1);
                // hiệu ứng ở xa của đòn bắn (đạn, vụ nổ ở chỗ đối thủ của trận gốc): hiện trước mặt trong khung
                if (clip == Attack || clip == Skill) aola.FarAhead(clip, 1.3f);
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
