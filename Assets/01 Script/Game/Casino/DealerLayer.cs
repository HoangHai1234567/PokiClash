// Một lớp vẽ của Lão Mực (DealerRig): chỉ dựng lưới các slot có frontMask[s] == front, từ tư thế chung của rig, vào một Graphic
// uGUI (thứ tự vẽ theo vị trí trong cây canvas như mọi Image). Lớp sau và lớp trước kẹp mặt bàn + đồ trên bàn ở giữa.
// Gốc rig ở gốc RectTransform (pivot); RectTransform nên đặt pivot (0.5, 0) ở chỗ "giữa hai bàn chân" trong cảnh.
using AtomSpine;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    [RequireComponent(typeof(CanvasRenderer))]
    public sealed class DealerLayer : MaskableGraphic
    {
        DealerRig rig;
        bool[] mask;
        bool want;
        AtomikPose.SkinPass pass;
        Vector3[] verts;
        Vector2[] uvs;
        Color32[] cols;

        public override Texture mainTexture => rig != null && rig.Asset != null && rig.Asset.atlas != null ? rig.Asset.atlas : s_WhiteTexture;

        public void Bind(DealerRig r, bool[] slotMask, bool front)
        {
            rig = r;
            mask = slotMask;
            want = front;
            pass = r.State.pose.NewPass();
            int n = Mathf.Max(1, r.State.pose.maxVerts);
            verts = new Vector3[n];
            uvs = new Vector2[n];
            cols = new Color32[n];
            raycastTarget = false;
            SetMaterialDirty();
            SetVerticesDirty();
        }

        protected override void OnPopulateMesh(VertexHelper vh)
        {
            vh.Clear();
            if (rig == null || rig.State == null || pass == null) return;
            var pose = rig.State.pose;
            pose.tint = color;
            int nv = pose.Skin(pass, mask, want, verts, uvs, cols, 1f, false, -1, out _);
            if (nv == 0) return;
            float s = rig.Scale;
            for (int i = 0; i < nv; i++) vh.AddVert(new Vector3(verts[i].x * s, verts[i].y * s, 0), cols[i], uvs[i]);
            var tris = pass.Tris;
            int count = pass.Count;
            for (int k = 0; k + 2 < count; k += 3)
            {
                int a = tris[k], b = tris[k + 1], c = tris[k + 2];
                if (a == b && b == c) continue;
                vh.AddTriangle(a, b, c);
            }
        }
    }
}
