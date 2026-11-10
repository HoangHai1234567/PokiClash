// Một hạt của cảnh Trang trại (prefab Items/HatTrangTrai): bụi cuốc, tia rèn, khói lò, hạt thóc, quả rơi, tim, bi thu hoạch.
// Bay theo vận tốc và trọng lực, xoay, phóng to dần hoặc nảy lúc hiện, mờ dần cuối đời; hết đời thì tắt để FarmScene dùng lại.
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

        void Update()
        {
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
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
