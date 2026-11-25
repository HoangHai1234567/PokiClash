// Công trình đảo Casino nhún nhún để người chơi biết bấm được (người dùng 2026-11-25: "thêm kiểu hoạt ảnh gì đó (ánh sáng hoặc anim) hoặc
// thi thoảng nhún nhún các building để người chơi biết là ấn được"). Không dùng quầng sáng (luật VFX của dự án: không glow).
// - Cứ 2,5–3,5 giây chọn một công trình đang mở để nhún (nén giãn quanh chân, tắt dần); chỗ có việc (chấm đỏ) được chọn nhiều hơn,
//   chỗ khoá không nhún. Danh sách và trọng số do CasinoScene đặt mỗi lần vẽ (SetCandidates).
// - Chạm công trình: nhún ngay, mạnh hơn (Bounce từ CasinoSpot.OnTapFx).
// - Không nhún khi giao diện đảo đang ẩn (chuyến tàu qua mây) hoặc đang có hộp thoại.
// Công trình neo giãn theo khung nên đổi pivot không dời ảnh; pivot đặt sát chân lúc dựng (CasinoSceneMenu) để nén giãn quanh chân.
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed class CasinoBob : MonoBehaviour
    {
        [SerializeField] CasinoBuilding[] buildings = new CasinoBuilding[0];
        [SerializeField] float every = 3f, jitter = 0.5f, dur = 0.55f, amp = 0.065f;

        readonly Dictionary<string, CasinoBuilding> byId = new Dictionary<string, CasinoBuilding>();
        readonly List<(string id, float w)> cands = new List<(string, float)>();
        readonly Dictionary<RectTransform, (float t0, float k)> live = new Dictionary<RectTransform, (float, float)>();
        readonly List<RectTransform> done = new List<RectTransform>();
        float next;
        string last;

        public System.Func<bool> Allowed; // CasinoScene: giao diện đang hiện, không có hộp thoại

        // Dùng khi dựng prefab (Editor).
        public void Setup(CasinoBuilding[] list) => buildings = list;

        void Awake()
        {
            foreach (var b in buildings)
                if (b) byId[b.Id] = b;
            next = Time.unscaledTime + 1.2f;
        }

        public void SetCandidates(IEnumerable<(string id, float w)> list)
        {
            cands.Clear();
            cands.AddRange(list);
        }

        // nhún một công trình (k: độ mạnh, chạm là 1,6)
        public void Bounce(string id, float k = 1f)
        {
            if (string.IsNullOrEmpty(id) || !byId.TryGetValue(id, out var b) || !b || !b.isActiveAndEnabled) return;
            live[(RectTransform)b.transform] = (Time.unscaledTime, k);
        }

        void Update()
        {
            float now = Time.unscaledTime;
            if (now >= next)
            {
                next = now + every + Random.Range(-jitter, jitter);
                if (Allowed == null || Allowed()) Bounce(Pick());
            }
            done.Clear();
            foreach (var kv in live)
            {
                float t = (now - kv.Value.t0) / dur;
                var rt = kv.Key;
                if (!rt || t >= 1)
                {
                    if (rt) rt.localScale = Vector3.one;
                    done.Add(rt);
                    continue;
                }
                // nén giãn quanh chân: vươn lên, nén xuống, nảy nhẹ rồi yên (tắt dần)
                float s = Mathf.Sin(t * Mathf.PI * 3f) * (1 - t) * (1 - t) * amp * kv.Value.k;
                rt.localScale = new Vector3(1 - s * 0.6f, 1 + s, 1);
            }
            foreach (var rt in done) live.Remove(rt);
        }

        // chọn theo trọng số, tránh lặp lại công trình vừa nhún
        string Pick()
        {
            float sum = 0;
            foreach (var c in cands)
                if (c.w > 0 && (c.id != last || cands.Count == 1) && byId.TryGetValue(c.id, out var b) && b && b.isActiveAndEnabled) sum += c.w;
            if (sum <= 0) return null;
            float r = Random.value * sum;
            foreach (var c in cands)
            {
                if (c.w <= 0 || (c.id == last && cands.Count > 1) || !byId.TryGetValue(c.id, out var b) || !b || !b.isActiveAndEnabled) continue;
                r -= c.w;
                if (r <= 0)
                {
                    last = c.id;
                    return c.id;
                }
            }
            return null;
        }
    }
}
