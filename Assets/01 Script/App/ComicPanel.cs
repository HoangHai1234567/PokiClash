// Ô tranh truyện tranh (App/StoryIntro): tứ giác lồi bất kỳ, góc tính bằng đơn vị UI từ góc dưới trái của rect. Tranh phủ kín khung bao của
// tứ giác (giữ tỉ lệ ảnh, chừa lề Spare để trôi), Zoom / Pan dời tranh bên trong mà mép ô đứng yên. Một texture (sprite), không Mask.
using UnityEngine;
using UnityEngine.Sprites;
using UnityEngine.UI;

namespace PokiClash
{
    [RequireComponent(typeof(CanvasRenderer))]
    public sealed class ComicPanel : MaskableGraphic
    {
        public const float Spare = 1.05f; // lề để trôi (phóng 3%, lia 10); dời quá lề thì kẹp lại, không lộ mép tranh

        [SerializeField] Sprite sprite;

        readonly Vector2[] quad = new Vector2[4];
        bool hasQuad;
        float zoom = 1;
        Vector2 pan;
        Vector2 focus = new Vector2(0.5f, 0.5f);

        // điểm cần giữ khi tranh bị cắt (tỉ lệ ảnh, gốc dưới trái): tranh dời cho điểm này gần tâm ô nhất mà không lộ mép
        public Vector2 Focus
        {
            get => focus;
            set
            {
                focus = value;
                SetVerticesDirty();
            }
        }

        public Sprite Sprite
        {
            get => sprite;
            set
            {
                sprite = value;
                SetAllDirty();
            }
        }

        public override Texture mainTexture => sprite ? sprite.texture : s_WhiteTexture;

        public void SetQuad(Vector2[] corners)
        {
            for (int i = 0; i < 4; i++) quad[i] = corners[i];
            hasQuad = true;
            SetVerticesDirty();
        }

        public void SetDrift(float z, Vector2 p)
        {
            if (Mathf.Approximately(z, zoom) && p == pan) return;
            zoom = z;
            pan = p;
            SetVerticesDirty();
        }

        protected override void OnPopulateMesh(VertexHelper vh)
        {
            vh.Clear();
            if (!hasQuad) return;
            var r = rectTransform.rect;
            Vector2 min = quad[0], max = quad[0];
            for (int i = 1; i < 4; i++)
            {
                min = Vector2.Min(min, quad[i]);
                max = Vector2.Max(max, quad[i]);
            }
            var size = max - min;
            var center = (min + max) * 0.5f;
            float aspect = sprite ? sprite.rect.width / Mathf.Max(1, sprite.rect.height) : size.x / Mathf.Max(1, size.y);
            float w = Mathf.Max(size.x, size.y * aspect), h = w / aspect;
            w *= Spare * zoom;
            h *= Spare * zoom;
            // tâm tranh lệch khỏi tâm ô: kéo điểm lấy nét về tâm, cộng phần trôi, kẹp để mép tranh không lọt vào ô
            float mx = Mathf.Max(0, (w - size.x) * 0.5f), my = Mathf.Max(0, (h - size.y) * 0.5f);
            var off = new Vector2(Mathf.Clamp((0.5f - focus.x) * w + pan.x, -mx, mx), Mathf.Clamp((0.5f - focus.y) * h + pan.y, -my, my));
            var uv = sprite ? DataUtility.GetOuterUV(sprite) : new Vector4(0, 0, 1, 1);
            for (int i = 0; i < 4; i++)
            {
                var q = quad[i];
                float u = 0.5f + (q.x - center.x - off.x) / w;
                float v = 0.5f + (q.y - center.y - off.y) / h;
                vh.AddVert(new Vector3(r.xMin + q.x, r.yMin + q.y), color, new Vector2(Mathf.Lerp(uv.x, uv.z, u), Mathf.Lerp(uv.y, uv.w, v)));
            }
            vh.AddTriangle(0, 1, 2);
            vh.AddTriangle(0, 2, 3);
        }
    }
}
