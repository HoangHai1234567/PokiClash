// Mây che từng đảo trên bản đồ sảnh (người dùng 2026-11-19: "ban đầu mây che hết, chọn xong mây đảo đó tan ra", xong trận hướng dẫn
// thì tan nốt). Mỗi đảo một nhóm mây (con "may_<hệ>" của lớp "suong_mu", dựng sẵn trong Screens/Hub bằng menu "PokiClash/Prefab/Sảnh
// bản đồ thế giới (mây, điểm bấm)" từ Assets/03 Art/Islands/hub_map.json). Mây nhận chạm: chạm vào đảo còn mây thì báo cách mở.
// Tan mây: từng đám dạt ra xa tâm đảo, phồng lên, mờ dần, đám gần tâm tan trước; xong thì tắt cả nhóm.
using System;
using System.Collections;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HubFog : MonoBehaviour
    {
        [Serializable]
        public struct Group
        {
            public Elem zone;
            public RectTransform root; // tâm đảo (điểm bấm), các đám mây đặt quanh
            public Image[] clouds;
            public ClickCatcher[] hits;
        }

        [SerializeField] Group[] groups;
        [SerializeField] float revealTime = 1.6f;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Group[] g) => groups = g;

        public bool Has(Elem e) => Find(e) >= 0;

        int Find(Elem e)
        {
            if (groups == null) return -1;
            for (int i = 0; i < groups.Length; i++)
                if (groups[i].zone == e && groups[i].root)
                    return i;
            return -1;
        }

        public RectTransform Center(Elem e)
        {
            int i = Find(e);
            return i >= 0 ? groups[i].root : null;
        }

        // covered: bit = Elem còn mây (chưa mở, hoặc mở rồi mà chưa diễn tan); onLockedTap: chạm vào mây của đảo đó
        public void Apply(int covered, Action<Elem> onLockedTap)
        {
            if (groups == null) return;
            foreach (var g in groups)
            {
                if (!g.root) continue;
                bool on = (covered & HubIslands.Bit(g.zone)) != 0;
                g.root.gameObject.SetActive(on);
                if (!on) continue;
                ResetGroup(g);
                var z = g.zone;
                if (g.hits != null)
                    foreach (var h in g.hits)
                        if (h)
                            h.OnClick = () => onLockedTap?.Invoke(z);
            }
        }

        static void ResetGroup(Group g)
        {
            if (g.clouds == null) return;
            foreach (var c in g.clouds)
            {
                if (!c) continue;
                c.transform.localScale = new Vector3(Mathf.Sign(c.transform.localScale.x == 0 ? 1 : c.transform.localScale.x), 1, 1);
                var col = c.color;
                col.a = 1;
                c.color = col;
                c.raycastTarget = true;
            }
        }

        // diễn tan mây một đảo (gọi khi nhóm đang hiện); xong thì tắt nhóm
        public IEnumerator Reveal(Elem e)
        {
            int i = Find(e);
            if (i < 0) yield break;
            var g = groups[i];
            if (g.clouds == null || g.clouds.Length == 0)
            {
                g.root.gameObject.SetActive(false);
                yield break;
            }
            int n = g.clouds.Length;
            var start = new Vector2[n];
            var dir = new Vector2[n];
            var delay = new float[n];
            var flip = new float[n];
            float far = 1;
            for (int k = 0; k < n; k++)
            {
                if (!g.clouds[k]) continue;
                start[k] = g.clouds[k].rectTransform.anchoredPosition;
                far = Mathf.Max(far, start[k].magnitude);
                g.clouds[k].raycastTarget = false;
                flip[k] = Mathf.Sign(g.clouds[k].transform.localScale.x == 0 ? 1 : g.clouds[k].transform.localScale.x);
            }
            for (int k = 0; k < n; k++)
            {
                float m = start[k].magnitude;
                dir[k] = m > 1 ? start[k] / m : UnityEngine.Random.insideUnitCircle.normalized;
                // đám gần tâm tan trước, lệch nhẹ ngẫu nhiên
                delay[k] = 0.35f * (m / far) + UnityEngine.Random.Range(0f, 0.12f);
            }
            App.Audio?.Play("whoosh");
            float t = 0, life = revealTime;
            while (t < life + 0.5f)
            {
                t += Time.unscaledDeltaTime;
                for (int k = 0; k < n; k++)
                {
                    var c = g.clouds[k];
                    if (!c) continue;
                    float u = Mathf.Clamp01((t - delay[k]) / (life - 0.4f));
                    float ease = 1 - (1 - u) * (1 - u) * (1 - u);
                    c.rectTransform.anchoredPosition = start[k] + dir[k] * (260 + 180 * (k % 3)) * ease;
                    float sc = 1 + 0.35f * ease;
                    c.transform.localScale = new Vector3(flip[k] * sc, sc, 1);
                    var col = c.color;
                    col.a = 1 - Mathf.SmoothStep(0, 1, Mathf.Clamp01((u - 0.15f) / 0.85f));
                    c.color = col;
                }
                yield return null;
            }
            for (int k = 0; k < n; k++)
                if (g.clouds[k])
                {
                    g.clouds[k].rectTransform.anchoredPosition = start[k];
                    g.clouds[k].transform.localScale = new Vector3(flip[k], 1, 1);
                }
            g.root.gameObject.SetActive(false);
        }
    }
}
