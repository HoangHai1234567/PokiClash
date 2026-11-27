// Biển chung của sảnh, Nhà, đảo Casino và chuyến tàu qua mây (người dùng 2026-11-27: "nước của 3 đảo phải liền mạch nhau ... tưởng tượng
// 3 đảo trong 1 map to"). Mọi lớp biển vẽ cùng một ảnh lát (Islands/sanh_bien, ô 1024 đơn vị ở cỡ thật) ghim theo toạ độ thế giới chứ
// không theo khung ảnh của từng lớp:
// - shader PokiClash/UISeaWorld (lớp biển mở: Hub bien_lat, Casino bien, Nhà bien_ngoai, chuyến tàu) và UIHomeSea khi _TileWorld = 1
//   (biển trong ảnh nền Nhà, sóng bờ sảnh / Casino) lấy ô lát theo vị trí thế giới của điểm ảnh: (xy − gốc) / cỡ ô, với gốc và cỡ ô là
//   biến toàn cục _PokiSeaO (xy gốc thế giới, zw = 1 / cỡ ô thế giới);
// - mỗi màn có một SeaAnchor trên lớp kéo (Hub: dao, Nhà: the_gioi, Casino: anh_nen_casino): gốc biển là điểm của lớp kéo nên biển trôi
//   và phóng theo bản đồ; mỗi khung SeaAnchor đang bật ghi _PokiSeaO;
// - chuyến tàu (ShipVoyage) giữ quyền ghi (Held) khi chạy: biển của nó ghim theo ảnh chụp màn cũ, và trước khi chụp màn mới nó dời gốc
//   biển của màn mới (Shift) cho trùng đúng chỗ biển của chuyến tàu khi camera tới nơi, nên ảnh chụp, dải biển, màn thật là một mặt nước.
using UnityEngine;

namespace PokiClash
{
    public static class SeaWorld
    {
        public const float Tile = 1024; // cỡ ô lát ở cỡ thật (đơn vị UI của lớp kéo)
        static readonly int Id = Shader.PropertyToID("_PokiSeaO");

        // chuyến tàu đang ghi gốc biển: SeaAnchor của màn không ghi
        public static bool Held;

        public static Vector3 Origin { get; private set; }
        public static float TileWorld { get; private set; } = 1;

        public static void Set(Vector3 origin, float tileWorld)
        {
            tileWorld = Mathf.Max(1e-6f, tileWorld);
            Origin = origin;
            TileWorld = tileWorld;
            Shader.SetGlobalVector(Id, new Vector4(origin.x, origin.y, 1f / tileWorld, 1f / tileWorld));
        }
    }

    // gốc biển của một màn: đặt trên lớp kéo của bản đồ (dựng bằng menu "PokiClash/Prefab/Sảnh và đảo/Biển chung: sảnh, Nhà, Casino")
    [DisallowMultipleComponent]
    public sealed class SeaAnchor : MonoBehaviour
    {
        public static SeaAnchor Active { get; private set; }

        [Tooltip("Lớp kéo của cả bản đồ (sảnh, Casino: keo của HubPan; Nhà: the_gioi): chuyến tàu dời lớp này để chụp phần đảo ngoài khung")]
        [SerializeField] RectTransform map;

        Vector2 shift; // dời gốc (toạ độ local của lớp), chuyến tàu đặt lúc tới cho biển màn mới nối liền biển chuyến tàu
        float mul = 1; // nhân cỡ ô (chuyến tàu đặt khi cỡ thật của màn cũ, màn mới lệch nhau)

        public RectTransform Rt => (RectTransform)transform;
        public RectTransform Map => map ? map : Rt;

        // Dùng khi dựng prefab (Editor).
        public void SetMap(RectTransform layer) => map = layer;
        public Vector3 OriginWorld => transform.TransformPoint(shift);
        public float TileWorld => SeaWorld.Tile * mul * Mathf.Abs(transform.lossyScale.x);

        void OnEnable()
        {
            Active = this;
            if (!SeaWorld.Held) Apply();
        }

        void OnDisable()
        {
            if (Active == this) Active = null;
        }

        void LateUpdate()
        {
            if (!SeaWorld.Held && Active == this) Apply();
        }

        public void Apply() => SeaWorld.Set(OriginWorld, TileWorld);

        // đặt gốc biển ở điểm thế giới w với cỡ ô thế giới t (dời theo bội số ô cho gọn: biển lặp nên trông y hệt)
        public void Match(Vector3 w, float t)
        {
            float sc = Mathf.Max(1e-6f, Mathf.Abs(transform.lossyScale.x));
            mul = Mathf.Max(0.05f, t / (SeaWorld.Tile * sc));
            Vector2 local = transform.InverseTransformPoint(w);
            float tl = SeaWorld.Tile * mul;
            shift = new Vector2(local.x - Mathf.Round(local.x / tl) * tl, local.y - Mathf.Round(local.y / tl) * tl);
        }
    }
}
