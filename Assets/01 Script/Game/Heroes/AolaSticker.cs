// Tướng aola trên sân đấu: prefab tướng (AolaActor, Assets/04 Prefabs/Heroes) đặt ở xa trong thế giới, một camera riêng render
// ra RenderTexture, RawImage trên sân hiện ảnh đó qua shader viền sticker. Dạng chưa nhập vào project (menu PokiClash/Tướng/
// Nhập hình tướng aola) thì TryCreate trả null và ô tướng trên sân để trống.
// Camera chỉ chụp khi hình đổi (AolaActor.Version: animation 25 khung/giây trên màn 60 khung, khung camera dời), các khung khác tắt và
// RawImage giữ ảnh cũ; cứ 30 khung chụp lại một lần phòng RenderTexture mất nội dung (Android đi nền rồi về).
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class AolaSticker
    {
        const float Span = 3.4f; // khung camera = 3,4 lần chiều cao dáng đứng (đủ chỗ cho clip lao)
        const float FootV = 0.2f; // chân nằm ở 20% chiều cao ảnh
        static int count, builtFrame = -1;

        // Dựng sticker tốn (prefab, hàng chục hình, RenderTexture có depth): giao diện (hộp chi tiết, đội hình) mỗi khung dựng tối đa
        // một cái và không dựng trong khung chạm, chờ khung sau thì giữ hình cũ hoặc chân dung (người dùng dặn phản hồi phải ngay,
        // 2026-11-07). Sân đấu dựng cả đội lúc vào trận thì không hỏi.
        public static bool CanBuildNow => builtFrame != Time.frameCount;

        public RectTransform Rect { get; private set; }
        RawImage img;
        Material mat;
        AolaActor actor;
        GameObject world;
        Camera cam;
        RenderTexture rt;
        bool flip;
        float stageHeight; // chiều cao dáng đứng trên sân (đơn vị web)
        int seenVersion = -1, lastShot = -1000; // AolaActor.Version lúc chụp gần nhất, khung (Time.frameCount) chụp gần nhất
        bool camDirty = true; // khung camera vừa dời: chụp lại

        static string ClipName(string c) =>
            c == StageView.Attack ? AolaActor.Attack : c == StageView.Skill ? AolaActor.Skill : c == StageView.Cast ? AolaActor.Cast :
            c == StageView.Hit ? AolaActor.Hit : c == AolaActor.Evolve ? AolaActor.Evolve : AolaActor.Idle;

        // dạng có clip này không (clip tiến hóa: chỉ dạng .atomik có, HeroViewer phát trước khi đổi dạng)
        public bool HasClip(string clip) => actor.HasClip(ClipName(clip));

        // aola: tên dạng cần hiện (HeroDef.Form theo sao)
        public static AolaSticker TryCreate(RectTransform parent, HeroDef hero, string aola, float uiHeight, bool flip)
        {
            if (!AolaActor.Find(aola, out var prefab, out int form)) return null;
            builtFrame = Time.frameCount;
            var actor = Object.Instantiate(prefab, new Vector3(10000 + 50 * (count++ % 40), 0, 0), Quaternion.identity);
            var go = actor.gameObject;
            go.name = "aola_" + hero.id;
            actor.Manual = true;
            if (!actor.LoadForm(form, 1f, flip, 0))
            {
                Object.Destroy(go);
                return null;
            }
            var s = new AolaSticker { actor = actor, world = go, flip = flip, stageHeight = uiHeight / StageView.K };
            int px = Mathf.Clamp(Mathf.NextPowerOfTwo((int)(uiHeight * Span)), 256, 1024);
            // URP render graph báo lỗi mỗi khung nếu RenderTexture đích của camera không có depth buffer
            s.rt = new RenderTexture(px, px, 16, RenderTextureFormat.ARGB32) { name = "aola_" + hero.id };
            var camGo = new GameObject("cam");
            camGo.transform.SetParent(go.transform, false);
            camGo.transform.localPosition = new Vector3(0, Span * (0.5f - FootV), -10);
            var cam = s.cam = camGo.AddComponent<Camera>();
            cam.orthographic = true;
            cam.orthographicSize = Span / 2;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0, 0, 0, 0);
            cam.targetTexture = s.rt;
            cam.nearClipPlane = 0.1f;
            cam.farClipPlane = 50;

            s.img = new GameObject("aola", typeof(RectTransform)).AddComponent<RawImage>();
            s.Rect = s.img.rectTransform;
            s.Rect.SetParent(parent, false);
            s.Rect.anchorMin = s.Rect.anchorMax = new Vector2(0.5f, 0);
            s.Rect.pivot = new Vector2(0.5f, FootV);
            s.Rect.sizeDelta = new Vector2(uiHeight * Span, uiHeight * Span);
            s.img.texture = s.rt;
            s.img.raycastTarget = false;
            var baseMat = Theme.Assets ? Theme.Assets.sticker : null;
            if (baseMat)
            {
                s.mat = new Material(baseMat);
                s.mat.SetFloat("_White", 3f * px / 512f);
                s.mat.SetFloat("_Ink", 2.5f * px / 512f);
                s.img.material = s.mat;
            }
            return s;
        }

        // chiêu bắn của tướng không có clip bắn (1_5): đứng dáng đứng, sân tự nhún tới (StageView.Place), tia phóng ở giữa
        public const float CastLen = 0.6f;
        public bool HasCast => actor.HasClip(AolaActor.Cast);
        public bool ManaUsesClip => actor.ManaUsesClip;

        public float Duration(string clip) => clip == StageView.Cast && !HasCast ? CastLen : actor.Duration(ClipName(clip));

        public float HitTime(string clip) =>
            clip == StageView.Cast && !HasCast ? CastLen * 0.5f : actor.HitFrame(ClipName(clip)) / actor.Fps;

        // Chiêu bắn tia (AolaActor.Beam): chỗ bắn so với chân (đơn vị sân, y xuống, đã lật theo phía) và cỡ tia; không khai: false
        public bool Beam(out Vector2 muzzle, out float scale)
        {
            muzzle = Vector2.zero;
            if (!actor.Beam(out var m, out scale)) return false;
            float k = stageHeight / Mathf.Max(1, actor.IdleHeightPx);
            muzzle = new Vector2((flip ? -m.x : m.x) * k, m.y * k);
            return true;
        }

        // kiểu tia riêng (AolaActor.BeamStyle: tia_bang, tia_xoay, tia_trieu của 3 boss cuối đảo Thủy); null = tia nước thường
        public string BeamStyle => actor ? actor.BeamStyle : null;

        // cảm giác trúng của clip sân (AolaActor.Impact)
        public bool Impact(string clip, out float stop, out float shake, out float push, out string flash)
        {
            stop = shake = push = 0;
            flash = null;
            return actor && actor.Impact(ClipName(clip), out stop, out shake, out push, out flash);
        }

        // Độ lệch thêm (đơn vị sân) để đỉnh lao của clip đánh rơi vào 72% quãng tới đối thủ: A·m(t) − m(t) như bản web.
        // Clip khác (chiêu cuối) chỉ lao khi anim.json khai "lunge" (AolaActor.Lunges).
        public bool Lunge(string clip, float t, float tx, float ty, out Vector2 o)
        {
            o = Vector2.zero;
            var name = ClipName(clip);
            if (!actor.Lunges(name) || !actor.HasClip(name)) return false;
            int n = actor.FrameCount(name);
            int fi = Mathf.Min(n - 1, Mathf.FloorToInt(t * actor.Fps));
            float scale = stageHeight / Mathf.Max(1, actor.IdleHeightPx);
            var d = actor.Disp(name, fi);
            var pk = actor.Disp(name, actor.PeakFrame(name));
            float mx = (flip ? -d.x : d.x) * scale, my = d.y * scale;
            float Mx = (flip ? -pk.x : pk.x) * scale, My = pk.y * scale;
            float M = Mathf.Sqrt(Mx * Mx + My * My);
            if (M <= 30) return false; // clip bắn từ xa: sân đấu tự nhún tới
            float k = Mathf.Sqrt(tx * tx + ty * ty) / M;
            float ang = Mathf.Atan2(ty, tx) - Mathf.Atan2(My, Mx);
            float cs = Mathf.Cos(ang) * k, sn = Mathf.Sin(ang) * k;
            o = new Vector2(mx * cs - my * sn - mx, mx * sn + my * cs - my);
            return true;
        }

        // Hiệu ứng ở xa của clip (đạn bay, vụ nổ ở chỗ đối thủ của trận gốc, AolaActor.FarTarget): to = đối thủ so với chân
        // (đơn vị sân, y xuống); null hoặc clip không có: như bản gốc. shift: khung camera dịch về phía đối thủ nửa quãng (thân
        // vẫn trong khung), ảnh dịch ngược lại để thân đứng yên trên sân (sân đấu; nơi tự đặt chỗ ảnh thì không dịch).
        public void Far(string clip, Vector2? to, bool shift = true)
        {
            var name = ClipName(clip);
            if (to == null || !actor.HasFar(name))
            {
                actor.SetFarTarget(null);
                if (shift) Shift(Vector2.zero);
                return;
            }
            float h = Mathf.Max(1, stageHeight);
            var d = to.Value;
            actor.SetFarTarget(new Vector2((flip ? -d.x : d.x) / h, -d.y / h));
            if (shift) Shift(new Vector2(Mathf.Clamp(d.x / h * 0.5f, -1.1f, 1.1f), Mathf.Clamp(-d.y / h * 0.5f, -0.8f, 0.8f)));
        }

        // khung xem tướng (không có đối thủ): hiệu ứng ở xa hiện trước mặt, cách chân heights lần chiều cao, trong khung camera
        public void FarAhead(string clip, float heights) =>
            Far(clip, new Vector2((flip ? -1 : 1) * heights * stageHeight, -0.4f * stageHeight), false);

        // dịch khung camera (đơn vị thế giới = chiều cao dáng đứng; +y lên) và ảnh trên sân theo
        void Shift(Vector2 w)
        {
            if (!cam) return;
            var lp = new Vector3(w.x, Span * (0.5f - FootV) + w.y, -10);
            if (cam.transform.localPosition != lp)
            {
                cam.transform.localPosition = lp;
                camDirty = true;
                cam.enabled = true;
            }
            Rect.anchoredPosition = w * stageHeight * StageView.K;
        }

        // bật camera đúng khung hình đổi; trong cùng một khung đã bật thì giữ (Show gọi hai lần không tắt mất lần chụp)
        void SyncCamera()
        {
            if (!cam) return;
            int now = Time.frameCount;
            if (lastShot == now) return;
            bool shoot = camDirty || actor.Version != seenVersion || now - lastShot > 30 || !rt.IsCreated();
            cam.enabled = shoot;
            if (!shoot) return;
            seenVersion = actor.Version;
            camDirty = false;
            lastShot = now;
        }

        public void Show(string clip, float t, bool loop, float alpha, bool gray, float flash)
        {
            // hình aola theo khung (floor t·fps), rig .atomik theo thời gian liên tục (AolaActor.ShowTime)
            actor.ShowTime(ClipName(clip), t, loop);
            SyncCamera();
            img.color = new Color(1, 1, 1, alpha);
            if (mat)
            {
                mat.SetFloat("_Gray", gray ? 1 : 0);
                mat.SetFloat("_Flash", Mathf.Min(1, flash * 5) * 0.65f);
            }
        }

        // bỏ bóng dưới chân (màn boot)
        public void HideShadow() => actor.HideShadow = true;

        // Xoá cả ảnh trên UI, RT và material. Nơi dựng lại trong cùng khung (ô xem tướng khi tiến hóa, đội hình màn Tướng) mà để
        // sót ảnh cũ thì nó trỏ vào RT đã giải phóng: trên Android hiện thành ô đen đặc che sau tướng mới.
        public void Destroy()
        {
            if (cam) cam.enabled = false;
            if (img) Object.Destroy(img.gameObject);
            if (world) Object.Destroy(world);
            if (rt)
            {
                rt.Release();
                Object.Destroy(rt);
            }
            if (mat) Object.Destroy(mat);
        }
    }
}
