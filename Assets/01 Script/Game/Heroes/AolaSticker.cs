// Tướng aola trên sân đấu (CHỈ TRONG EDITOR HOẶC BẢN DEV, define POKICLASH_DEV): AolaActor đặt ở xa trong thế giới, một
// camera riêng render ra RenderTexture, RawImage trên sân hiện ảnh đó qua shader viền sticker. Không có aola (bản phát
// hành, hoặc tướng chưa xuất anim.json) thì TryCreate trả null và ô tướng trên sân để trống.
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
        static int count;

        public RectTransform Rect { get; private set; }
        RawImage img;
        Material mat;
        AolaActor actor;
        GameObject world;
        RenderTexture rt;
        bool flip;
        float stageHeight; // chiều cao dáng đứng trên sân (đơn vị web)

        static string ClipName(string c) =>
            c == StageView.Attack ? AolaActor.Attack : c == StageView.Skill ? AolaActor.Skill : c == StageView.Hit ? AolaActor.Hit : AolaActor.Idle;

        // aola: thư mục của dạng cần hiện (HeroDef.Form theo sao)
        public static AolaSticker TryCreate(RectTransform parent, HeroDef hero, string aola, float uiHeight, bool flip)
        {
            if (string.IsNullOrEmpty(AolaActor.ReskinDir) || string.IsNullOrEmpty(aola)) return null;
            var go = new GameObject("aola_" + hero.id);
            go.transform.position = new Vector3(10000 + 50 * (count++ % 40), 0, 0);
            var actor = go.AddComponent<AolaActor>();
            actor.Manual = true;
            if (!actor.LoadHero(aola, 1f, flip, 0))
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
            var cam = camGo.AddComponent<Camera>();
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

        public float Duration(string clip) => actor.Duration(ClipName(clip));

        public float HitTime(string clip) => actor.HitFrame(ClipName(clip)) / actor.Fps;

        // Độ lệch thêm (đơn vị sân) để đỉnh lao của clip đánh rơi vào 72% quãng tới đối thủ: A·m(t) − m(t) như bản web.
        public bool Lunge(string clip, float t, float tx, float ty, out Vector2 o)
        {
            o = Vector2.zero;
            var name = ClipName(clip);
            if (name != AolaActor.Attack || !actor.HasClip(name)) return false;
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

        public void Show(string clip, float t, bool loop, float alpha, bool gray, float flash)
        {
            var name = ClipName(clip);
            int n = Mathf.Max(1, actor.FrameCount(name));
            int i = Mathf.FloorToInt(t * actor.Fps);
            int fi = loop ? ((i % n) + n) % n : Mathf.Clamp(i, 0, n - 1);
            actor.ShowFrame(name, fi);
            img.color = new Color(1, 1, 1, alpha);
            if (mat)
            {
                mat.SetFloat("_Gray", gray ? 1 : 0);
                mat.SetFloat("_Flash", Mathf.Min(1, flash * 5) * 0.65f);
            }
        }

        public void Destroy()
        {
            if (world) Object.Destroy(world);
            if (rt) rt.Release();
        }
    }
}
