// Inspector của prefab tướng (AolaActor): ô xem trước hiện chân dung các dạng theo thứ tự tiến hóa; ảnh nhỏ trong cửa sổ
// Project là chân dung dạng cuối. Prefab không trỏ thẳng tới ảnh (AolaAnim nạp qua Resources), nên phải vẽ ở đây.
using PokiClash.Game;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    [CustomEditor(typeof(AolaActor))]
    public sealed class AolaActorEditor : Editor
    {
        public override bool HasPreviewGUI() => true;

        public override GUIContent GetPreviewTitle() => new GUIContent("Các dạng");

        public override void OnPreviewGUI(Rect r, GUIStyle background)
        {
            var forms = ((AolaActor)target).Forms;
            if (forms == null || forms.Length == 0) return;
            float w = r.width / forms.Length;
            for (int i = 0; i < forms.Length; i++)
            {
                var s = forms[i] ? forms[i].LoadPortrait() : null;
                var cell = new Rect(r.x + i * w, r.y, w, r.height - 16);
                if (s) GUI.DrawTexture(cell, s.texture, ScaleMode.ScaleToFit, true, HeroArt.W / (float)HeroArt.H); // ảnh vuông, hiện 4:5
                GUI.Label(new Rect(cell.x, cell.yMax, w, 16), forms[i] ? forms[i].name : "(thiếu)", EditorStyles.centeredGreyMiniLabel);
            }
        }

        public override Texture2D RenderStaticPreview(string assetPath, Object[] subAssets, int width, int height)
        {
            var forms = ((AolaActor)target).Forms;
            var last = forms != null && forms.Length > 0 ? forms[forms.Length - 1] : null;
            var s = last ? last.LoadPortrait() : null;
            if (!s) return null;
            // khung 4:5 đặt giữa ô vuông: dst u 0,1..0,9 lấy src 0..1
            var rt = RenderTexture.GetTemporary(width, height, 0, RenderTextureFormat.ARGB32);
            var prev = RenderTexture.active;
            RenderTexture.active = rt;
            GL.Clear(true, true, Color.clear);
            float k = (float)height / width * 4f / 5f;
            Graphics.Blit(s.texture, rt, new Vector2(1 / k, 1), new Vector2(-(1 - k) / 2 / k, 0));
            var tex = new Texture2D(width, height, TextureFormat.RGBA32, false);
            tex.ReadPixels(new Rect(0, 0, width, height), 0, 0);
            tex.Apply();
            RenderTexture.active = prev;
            RenderTexture.ReleaseTemporary(rt);
            return tex;
        }
    }
}
