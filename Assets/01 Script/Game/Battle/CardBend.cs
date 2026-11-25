// Uốn lá bài trên lưới UI (bộ bài tráo kiểu riffle uốn lá, người dùng 2026-11-25): cắt các tam giác của Graphic thành dải dọc theo trục x
// của gốc lá (mỗi Step px; lưới theo toạ độ gốc lá, chung cho mọi Graphic con nên các mảnh 9-slice và icon không hở mép), rồi đẩy đỉnh theo
// trục z của gốc lá về phía người xem: z = −Amount · f(x). Side +1: mép +x vểnh lên (mép −x nằm yên), −1: mép −x vểnh, 0: giữa võng lên.
// Lá đang nằm nghiêng 3D (DraftDeck) nên độ dời z hiện ra thành đường cong. Amount = 0 thì giữ lưới gốc, không tốn gì.
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    [DisallowMultipleComponent]
    public sealed class CardBend : BaseMeshEffect
    {
        const float Step = 12;
        RectTransform root;
        float amount;
        int side;

        static readonly List<UIVertex> src = new List<UIVertex>(), dst = new List<UIVertex>();
        static readonly List<UIVertex> polyA = new List<UIVertex>(8), polyB = new List<UIVertex>(8);
        static readonly List<float> xA = new List<float>(8), xB = new List<float>(8);

        // gắn vào mọi Graphic của lá (khung, icon), gốc uốn là lá
        public static CardBend[] Attach(RectTransform card)
        {
            var gs = card.GetComponentsInChildren<Graphic>(true);
            var r = new CardBend[gs.Length];
            for (int i = 0; i < gs.Length; i++)
            {
                if (!gs[i].TryGetComponent<CardBend>(out var b)) b = gs[i].gameObject.AddComponent<CardBend>();
                b.root = card;
                r[i] = b;
            }
            return r;
        }

        public static void Set(CardBend[] bends, float a, int s)
        {
            if (bends == null) return;
            foreach (var b in bends)
                if (b)
                    b.Set(a, s);
        }

        public void Set(float a, int s)
        {
            bool was = Mathf.Abs(amount) >= 0.05f, now = Mathf.Abs(a) >= 0.05f;
            if (Mathf.Abs(a - amount) < 0.05f && s == side) return;
            amount = now ? a : 0;
            side = s;
            if ((was || now) && graphic) graphic.SetVerticesDirty();
        }

        public override void ModifyMesh(VertexHelper vh)
        {
            if (!IsActive() || !root || Mathf.Abs(amount) < 0.05f) return;
            src.Clear();
            dst.Clear();
            vh.GetUIVertexStream(src);
            var toRoot = root.worldToLocalMatrix * transform.localToWorldMatrix;
            var fromRoot = toRoot.inverse;
            float half = Mathf.Max(1, root.rect.width * 0.5f);
            for (int t = 0; t + 2 < src.Count; t += 3)
            {
                float x0 = toRoot.MultiplyPoint3x4(src[t].position).x;
                float x1 = toRoot.MultiplyPoint3x4(src[t + 1].position).x;
                float x2 = toRoot.MultiplyPoint3x4(src[t + 2].position).x;
                float lo = Mathf.Min(x0, Mathf.Min(x1, x2)), hi = Mathf.Max(x0, Mathf.Max(x1, x2));
                float a = lo, g = (Mathf.Floor(lo / Step) + 1) * Step;
                while (true)
                {
                    float b = Mathf.Min(g, hi);
                    if (b - a > 0.01f || hi - lo < 0.01f)
                    {
                        polyA.Clear();
                        xA.Clear();
                        polyA.Add(src[t]);
                        polyA.Add(src[t + 1]);
                        polyA.Add(src[t + 2]);
                        xA.Add(x0);
                        xA.Add(x1);
                        xA.Add(x2);
                        Clip(polyA, xA, polyB, xB, a, true);
                        Clip(polyB, xB, polyA, xA, b, false);
                        for (int k = 1; k + 1 < polyA.Count; k++)
                        {
                            dst.Add(polyA[0]);
                            dst.Add(polyA[k]);
                            dst.Add(polyA[k + 1]);
                        }
                    }
                    if (b >= hi) break;
                    a = b;
                    g += Step;
                }
            }
            for (int i = 0; i < dst.Count; i++)
            {
                var v = dst[i];
                var p = toRoot.MultiplyPoint3x4(v.position);
                p.z -= amount * F(p.x / half);
                v.position = fromRoot.MultiplyPoint3x4(p);
                dst[i] = v;
            }
            vh.Clear();
            vh.AddUIVertexTriangleStream(dst);
        }

        float F(float u)
        {
            if (side > 0)
            {
                float w = Mathf.Clamp01((u + 1) * 0.5f);
                return w * w;
            }
            if (side < 0)
            {
                float w = Mathf.Clamp01((1 - u) * 0.5f);
                return w * w;
            }
            return Mathf.Clamp01(1 - u * u);
        }

        // cắt đa giác theo x ≥ edge (keepGreater) hoặc x ≤ edge (Sutherland–Hodgman), nội suy mọi thuộc tính đỉnh
        static void Clip(List<UIVertex> inV, List<float> inX, List<UIVertex> outV, List<float> outX, float edge, bool keepGreater)
        {
            outV.Clear();
            outX.Clear();
            int n = inV.Count;
            for (int i = 0; i < n; i++)
            {
                int j = (i + 1) % n;
                float xi = inX[i], xj = inX[j];
                bool ii = keepGreater ? xi >= edge : xi <= edge;
                bool jj = keepGreater ? xj >= edge : xj <= edge;
                if (ii)
                {
                    outV.Add(inV[i]);
                    outX.Add(xi);
                }
                if (ii != jj && Mathf.Abs(xj - xi) > 1e-5f)
                {
                    float t = (edge - xi) / (xj - xi);
                    outV.Add(Lerp(inV[i], inV[j], t));
                    outX.Add(edge);
                }
            }
        }

        static UIVertex Lerp(UIVertex a, UIVertex b, float t)
        {
            var v = a;
            v.position = Vector3.LerpUnclamped(a.position, b.position, t);
            v.normal = Vector3.LerpUnclamped(a.normal, b.normal, t);
            v.tangent = Vector4.LerpUnclamped(a.tangent, b.tangent, t);
            v.color = Color32.Lerp(a.color, b.color, t);
            v.uv0 = Vector4.LerpUnclamped(a.uv0, b.uv0, t);
            v.uv1 = Vector4.LerpUnclamped(a.uv1, b.uv1, t);
            v.uv2 = Vector4.LerpUnclamped(a.uv2, b.uv2, t);
            v.uv3 = Vector4.LerpUnclamped(a.uv3, b.uv3, t);
            return v;
        }
    }
}
