// Một hạt của cảnh Trang trại (prefab Items/HatTrangTrai): bụi cuốc, tia rèn, khói lò, hạt thóc, quả rơi, tim, bi thu hoạch.
// Bay theo vận tốc và trọng lực, xoay, phóng to dần hoặc nảy lúc hiện, mờ dần cuối đời; hết đời thì tắt để FarmScene dùng lại.
// Fly: bay theo đường cong tới một đích rồi báo tới nơi (Nhà: bi Cây bi bay về chip bi).
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class FarmFx : MonoBehaviour
    {
        [SerializeField] Image img;

        Vector2 vel;
        float gravity, life, age, spin, size0, size1, drag, alpha0 = 1;
        bool pop;

        public bool Busy => gameObject.activeSelf;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image image) => img = image;

        // pos: toạ độ cục bộ trong lớp hạt; size0 → size1: cỡ lúc đầu và lúc cuối; pop: nảy to lên lúc hiện (tim, quả)
        public void Play(Sprite s, Color c, Vector2 pos, Vector2 velocity, float g, float lifeTime, float sizeStart, float sizeEnd, float spinDeg = 0,
            bool popIn = false, float airDrag = 0)
        {
            flying = false;
            onArrive = null;
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            img.sprite = s;
            img.color = c;
            alpha0 = c.a;
            img.enabled = s;
            var rt = (RectTransform)transform;
            rt.localPosition = pos;
            rt.localRotation = Quaternion.Euler(0, 0, Random.Range(-20f, 20f));
            vel = velocity;
            gravity = g;
            life = Mathf.Max(0.05f, lifeTime);
            age = 0;
            spin = spinDeg;
            size0 = sizeStart;
            size1 = sizeEnd;
            pop = popIn;
            drag = airDrag;
            Apply();
        }

        // bay theo đường cong từ a tới b (toạ độ cục bộ trong lớp cha), trễ delay giây, tới nơi gọi arrive (Nhà: bi Cây bi bay về chip bi
        // của thanh trên). Đường bậc ba: vọt lên lệch sang một bên khỏi chỗ đi, lượn rồi lao vào đích từ phía dưới (như icon bay của máy bi).
        public void Fly(Sprite s, Vector2 a, Vector2 b, float delay, float dur, float size, System.Action arrive)
        {
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            img.sprite = s;
            img.color = Color.white;
            img.enabled = false;
            flying = true;
            fa = a;
            fb = b;
            float side = Random.Range(-1f, 1f);
            fc1 = a + new Vector2(side * 170, 220 + Random.Range(0, 110));
            fc2 = b + new Vector2(-side * 60, -170);
            fside = side;
            fwait = delay;
            fdur = Mathf.Max(0.1f, dur);
            size0 = size;
            age = 0;
            onArrive = arrive;
            var rt = (RectTransform)transform;
            rt.localPosition = a;
            rt.localRotation = Quaternion.identity;
            rt.localScale = Vector3.one;
            rt.sizeDelta = new Vector2(size, size);
        }

        bool flying;
        Vector2 fa, fb, fc1, fc2;
        float fside, fwait, fdur;
        System.Action onArrive;

        void UpdateFly(float dt)
        {
            var rt = (RectTransform)transform;
            if (fwait > 0)
            {
                fwait -= dt;
                return;
            }
            img.enabled = true;
            age += dt;
            float k = Mathf.Min(1, age / fdur), m = 1 - k;
            rt.localPosition = m * m * m * fa + 3 * m * m * k * fc1 + 3 * m * k * k * fc2 + k * k * k * fb;
            // nảy to lúc bật ra (0,3 → 1,35 → 1), nhỏ dần khi tới đích
            float s = age < 0.07f ? Mathf.Lerp(0.3f, 1.35f, age / 0.07f) : age < 0.17f ? Mathf.Lerp(1.35f, 1f, (age - 0.07f) / 0.1f)
                : Mathf.Lerp(1f, 0.72f, (age - 0.17f) / Mathf.Max(0.01f, fdur - 0.17f));
            rt.sizeDelta = new Vector2(size0 * s, size0 * s);
            rt.localRotation = Quaternion.Euler(0, 0, Mathf.Sin(k * Mathf.PI) * 25 * fside);
            if (k < 1) return;
            flying = false;
            gameObject.SetActive(false);
            var cb = onArrive;
            onArrive = null;
            cb?.Invoke();
        }

        void OnDisable()
        {
            // tắt giữa đường (rời màn): vẫn báo tới nơi để số bi không kẹt
            if (!flying) return;
            flying = false;
            var cb = onArrive;
            onArrive = null;
            cb?.Invoke();
        }

        void Update()
        {
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            if (flying)
            {
                UpdateFly(dt);
                return;
            }
            age += dt;
            if (age >= life)
            {
                gameObject.SetActive(false);
                return;
            }
            vel.y -= gravity * dt;
            if (drag > 0) vel *= Mathf.Exp(-drag * dt);
            var rt = (RectTransform)transform;
            rt.localPosition += (Vector3)(vel * dt);
            rt.localRotation *= Quaternion.Euler(0, 0, spin * dt);
            Apply();
        }

        void Apply()
        {
            float t = age / life;
            float size = Mathf.Lerp(size0, size1, t);
            if (pop) size *= t < 0.15f ? Mathf.Lerp(0.2f, 1.25f, t / 0.15f) : t < 0.3f ? Mathf.Lerp(1.25f, 1f, (t - 0.15f) / 0.15f) : 1f;
            ((RectTransform)transform).sizeDelta = new Vector2(size, size);
            var c = img.color;
            c.a = alpha0 * (t > 0.65f ? 1 - (t - 0.65f) / 0.35f : 1);
            img.color = c;
        }
    }
}
