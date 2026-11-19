// Mây vành rời quanh một bản đồ (người dùng 2026-11-19: "mây xung quanh đảo chính cứ tách riêng ra để khi đi thì nó tách luôn chứ
// không để liền mảng trắng"). Mỗi đám mây là một ảnh trong lớp kéo của màn:
// - trôi nhẹ lệch pha;
// - toả ra quanh tàu của màn (PierShip.Active) rồi khép lại khi tàu đi qua (nhanh lúc toả, chậm lúc khép), kể cả lúc tàu đậu;
// - chuyến tàu qua mây (ShipVoyage) đọc vị trí gốc + độ toả từng đám để mang sang dải mây khi chụp màn (Hide trước khi chụp), lúc tới
//   thì trả độ toả về (SetOffset) rồi Show: mây nối liền, không nhảy.
// Sảnh: lớp "may_vien_roi" dựng bằng menu "PokiClash/Prefab/Sảnh bản đồ thế giới" (khoá "ring" của hub_map.json). Màn khác gắn
// bằng Setup(ảnh mây) trong menu dựng màn: mọi ảnh mây là con trực tiếp của gốc CloudRing, neo giữa (0,5; 0,5).
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class CloudRing : MonoBehaviour
    {
        public static CloudRing Active { get; private set; }

        [SerializeField] Image[] clouds = new Image[0];
        [SerializeField] float holeRadius = 290; // bán kính toả quanh tàu cỡ 1 (đơn vị của lớp mây)
        [SerializeField] float drift = 7; // biên độ trôi nhẹ

        Vector2[] home, off;
        float[] phase;
        CanvasGroup group;

        public int Count => clouds.Length;
        public Image Cloud(int i) => clouds[i];
        public RectTransform Layer => (RectTransform)transform;
        public float Hole => holeRadius;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Image[] cloudImgs, float hole)
        {
            clouds = cloudImgs;
            holeRadius = hole;
        }

        void Awake()
        {
            int n = clouds.Length;
            home = new Vector2[n];
            off = new Vector2[n];
            phase = new float[n];
            for (int i = 0; i < n; i++)
            {
                home[i] = clouds[i].rectTransform.anchoredPosition;
                phase[i] = (i * 0.618f % 1) * 6.28f;
            }
            group = GetComponent<CanvasGroup>();
        }

        void OnEnable() => Active = this;

        void OnDisable()
        {
            if (Active == this) Active = null;
        }

        // vị trí gốc (có trôi nhẹ, chưa toả) và độ toả hiện tại, toạ độ của lớp mây
        public Vector2 Home(int i) => home[i] + Drift(i);
        public Vector2 Offset(int i) => off[i];

        public void SetOffset(int i, Vector2 o)
        {
            off[i] = o;
            clouds[i].rectTransform.anchoredPosition = Home(i) + o;
        }

        public void Show(bool on)
        {
            if (group) group.alpha = on ? 1 : 0;
            else
                foreach (var c in clouds)
                    c.enabled = on;
        }

        Vector2 Drift(int i)
        {
            float t = Time.unscaledTime * 0.22f + phase[i];
            return new Vector2(Mathf.Sin(t) * drift, Mathf.Sin(t * 0.7f + 1.3f) * drift * 0.4f);
        }

        void Update()
        {
            if (home == null) return;
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            var ship = PierShip.Active;
            bool push = ship && ship.isActiveAndEnabled && ship.Look.Shown && ship.gameObject.scene == gameObject.scene;
            Vector2 center = Vector2.zero, head = Vector2.up;
            bool moving = false;
            float R = holeRadius, R2 = 0;
            if (push)
            {
                float size = ship.ShipRect.lossyScale.x / Mathf.Max(1e-5f, transform.lossyScale.x);
                center = (Vector2)Layer.InverseTransformPoint(ship.ShipRect.position) + new Vector2(0, 110 * size);
                moving = ship.Busy;
                head = ship.Look.Heading;
                R = holeRadius * Mathf.Max(0.7f, size) * (ship.Busy ? 1 : 0.62f); // tàu đậu: chừa quanh thân, không trống cả vùng
                R2 = R * 2.6f;
            }
            for (int i = 0; i < clouds.Length; i++)
            {
                var p = Home(i);
                var target = Vector2.zero;
                if (push && moving) target = ShipVoyage.Side(p, center, head, R, R2, i);
                else if (push)
                {
                    var d = p - center;
                    d.y *= 0.78f;
                    float r = d.magnitude;
                    if (r < R2)
                    {
                        var nd = r > 1 ? d / r : new Vector2(i % 2 == 0 ? 1 : -1, 0);
                        float k = (1 - r / R2) * (1 - r / R2);
                        target = new Vector2(nd.x * R * k, nd.y * R * k / 0.78f);
                    }
                }
                float rate = target.sqrMagnitude > off[i].sqrMagnitude ? 24f : 3.2f;
                off[i] = Vector2.Lerp(off[i], target, 1 - Mathf.Exp(-rate * dt));
                clouds[i].rectTransform.anchoredPosition = p + off[i];
            }
        }
    }
}
