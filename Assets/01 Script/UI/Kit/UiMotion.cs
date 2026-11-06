// Hiệu ứng nhỏ dùng chung của bộ UI Sa Bàn (GD_Claude/17_BoUI.md, chép Web/src/uikit/fx.ts và kit.css):
// thở (nút chính, chấm đỏ), nhún tại chỗ (thẻ, ô tướng, bảng tên), lún khi đè và nảy khi thả (nút), lắc (bấm khi chưa đủ điều
// kiện), hiện ra (danh sách hiện lần lượt). Một component giữ hết phần scale, xoay, dịch thêm của phần tử nên các hiệu ứng không
// giẫm lên nhau. Khi layout group hay code khác dời phần tử, gốc mới được nhận lại; đứng yên thì không ghi transform.
// Thời gian không theo timeScale (UI vẫn chạy khi trận tạm dừng).
using UnityEngine;

namespace PokiClash.UI
{
    [DisallowMultipleComponent]
    public sealed class UiMotion : MonoBehaviour
    {
        public enum SpawnFrom { Pop, Drop, Up }

        [Header("Thở: phồng xẹp nhẹ (nút chính, chấm đỏ)")]
        public bool breath;
        public float breathAmount = 0.045f, breathPeriod = 2.2f;

        [Header("Nhún tại chỗ: lên xuống, nghiêng nhẹ (thẻ, ô tướng)")]
        public bool idle;
        public float idleLift = 8, idleTilt = 0.8f, idlePeriod = 3.2f;

        [Header("Hiện ra khi bật")]
        public bool spawnOnEnable;
        public SpawnFrom spawnFrom = SpawnFrom.Pop;
        public float spawnDelay;
        public float staggerStep = 0.05f; // trễ thêm theo thứ tự trong cha (danh sách hiện lần lượt)

        const float PressLen = 0.08f, PunchLen = 0.36f, SpawnLen = 0.44f, ShakeLen = 0.3f;

        RectTransform rt;
        float t0, period, press, pressTo, punchT = -1, punchK = 1, shakeT = -1, spawnT, spawnWait;
        bool spawning, has, dirty;
        Vector2 basePos, lastPos;
        Vector3 baseScale, lastScale;
        float baseRot, lastRot;

        public static UiMotion Of(Component c) => c.TryGetComponent<UiMotion>(out var m) ? m : c.gameObject.AddComponent<UiMotion>();

        // đè (lún 0,9, nghiêng 1 độ) / thả
        public void Press(bool down) => pressTo = down ? 1 : 0;

        // nảy: 1 → 1,12 → 0,97 → 1 trong 0,36 giây (k: độ mạnh)
        public void Punch(float k = 1)
        {
            punchT = 0;
            punchK = k;
        }

        public void Shake() => shakeT = 0;

        // hiện ra sau delay giây (ẩn ngay từ giờ)
        public void Spawn(float delay = 0)
        {
            spawning = true;
            spawnWait = delay;
            spawnT = 0;
            LateUpdate();
        }

        public bool Spawning => spawning;

        void Awake() => rt = (RectTransform)transform;

        void OnEnable()
        {
            t0 = Random.value * 10f;
            period = Mathf.Max(0.2f, idlePeriod * Random.Range(0.85f, 1.15f));
            has = false;
            punchT = shakeT = -1;
            press = pressTo = 0;
            spawning = false;
            if (spawnOnEnable) Spawn(spawnDelay + transform.GetSiblingIndex() * staggerStep);
        }

        void OnDisable()
        {
            if (has && dirty) Apply(1, 0, Vector2.zero);
            dirty = false;
        }

        void Capture()
        {
            if (!rt) rt = (RectTransform)transform;
            if (!has)
            {
                basePos = rt.anchoredPosition;
                baseScale = rt.localScale;
                baseRot = rt.localEulerAngles.z;
                has = true;
                return;
            }
            // có ai khác dời (layout group, code chia bài...): nhận đó là gốc mới
            if ((rt.anchoredPosition - lastPos).sqrMagnitude > 0.01f) basePos = rt.anchoredPosition;
            if ((rt.localScale - lastScale).sqrMagnitude > 1e-6f) baseScale = rt.localScale;
            if (Mathf.Abs(Mathf.DeltaAngle(rt.localEulerAngles.z, lastRot)) > 0.01f) baseRot = rt.localEulerAngles.z;
        }

        void LateUpdate()
        {
            float dt = Mathf.Min(0.05f, Time.unscaledDeltaTime);
            bool active = breath || idle || spawning || punchT >= 0 || shakeT >= 0 || press > 0 || pressTo > 0;
            if (!active)
            {
                if (dirty)
                {
                    Capture();
                    Apply(1, 0, Vector2.zero);
                    dirty = false;
                }
                return;
            }
            Capture();
            press = Mathf.MoveTowards(press, pressTo, dt / PressLen);
            float s = 1, rot = 0;
            var off = Vector2.zero;
            float tt = Time.unscaledTime + t0;
            if (breath) s *= 1 + breathAmount * 0.5f * (1 - Mathf.Cos(tt * Mathf.PI * 2 / Mathf.Max(0.2f, breathPeriod)));
            if (idle)
            {
                float w = tt * Mathf.PI * 2 / period;
                off.y += idleLift * 0.5f * (1 - Mathf.Cos(w));
                rot += idleTilt * Mathf.Sin(w);
            }
            s *= 1 - 0.1f * press;
            rot -= press;
            if (punchT >= 0)
            {
                punchT += dt;
                float k = punchT / PunchLen;
                if (k >= 1) punchT = -1;
                else
                {
                    float c = k < 0.6f ? Mathf.Lerp(1, 1.12f, Out(k / 0.6f)) : k < 0.82f ? Mathf.Lerp(1.12f, 0.97f, (k - 0.6f) / 0.22f) : Mathf.Lerp(0.97f, 1, (k - 0.82f) / 0.18f);
                    s *= 1 + (c - 1) * punchK;
                    rot += Mathf.Sin(k * Mathf.PI) * punchK;
                }
            }
            if (shakeT >= 0)
            {
                shakeT += dt;
                float k = shakeT / ShakeLen;
                if (k >= 1) shakeT = -1;
                else off.x += Mathf.Sin(k * Mathf.PI * 6) * 14 * (1 - k);
            }
            if (spawning)
            {
                if (spawnWait > 0)
                {
                    spawnWait -= dt;
                    s = 0;
                }
                else
                {
                    spawnT += dt;
                    float k = spawnT / SpawnLen;
                    if (k >= 1) spawning = false;
                    else
                    {
                        // 0 → 65%: tới quá đà (1,07, nghiêng 2 độ); 65% → hết: về đứng yên
                        float a = k < 0.65f ? Out(k / 0.65f) : 1;
                        float b = k < 0.65f ? 0 : Out((k - 0.65f) / 0.35f);
                        float from = spawnFrom == SpawnFrom.Pop ? 0 : 0.6f;
                        float sc = Mathf.Lerp(Mathf.Lerp(from, 1.07f, a), 1, b);
                        float r0 = spawnFrom == SpawnFrom.Up ? 4 : -8;
                        rot += Mathf.Lerp(Mathf.Lerp(r0, 2, a), 0, b);
                        float dy = spawnFrom == SpawnFrom.Drop ? 120 : spawnFrom == SpawnFrom.Up ? -140 : 0;
                        off.y += dy * (1 - a);
                        s *= sc;
                    }
                }
            }
            Apply(s, rot, off);
            dirty = true;
        }

        void Apply(float s, float rot, Vector2 off)
        {
            rt.localScale = new Vector3(baseScale.x * s, baseScale.y * s, baseScale.z);
            rt.anchoredPosition = basePos + off;
            var e = rt.localEulerAngles;
            rt.localEulerAngles = new Vector3(e.x, e.y, baseRot + rot);
            lastPos = rt.anchoredPosition;
            lastScale = rt.localScale;
            lastRot = rt.localEulerAngles.z;
        }

        static float Out(float k) => 1 - Mathf.Pow(1 - Mathf.Clamp01(k), 3);
    }
}
