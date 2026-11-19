// Tàu đậu ở bến trong một màn (sảnh: bến cạnh đảo Thủy; Nhà: bến ở mép dưới đảo). Người dùng 2026-11-19.
// - Đậu: nhấp nhô, bọt vỗ mạn, mũi quay theo dockFace. Chạm tàu: OnTap (sảnh: về Nhà; Nhà: về đảo).
// - Đường ra khơi: north / south là các điểm từ chỗ đậu ra tới chỗ giao tàu cho lớp mây (ShipVoyage), toạ độ local của khung cha
//   (lớp kéo của màn, để tàu trôi theo khi kéo). Đi qua các điểm bằng đường cong Catmull-Rom, tăng tốc lúc rời bến, hãm lúc cập bến.
// - Bến thứ hai (sảnh: bến trên, giữa đảo Hỏa và Kim; người dùng: "thêm 1 bến đỗ nữa ở phần trên các đảo"): chỗ đậu mặc định, mọi
//   chuyến hướng bắc (về Nhà, từ Nhà về) đi / tới bến này. Tàu từ màn tải cập bến chính (dưới), người chơi tương tác ngay, tàu tự chạy
//   nhanh vòng ngoài đảo lên bến hai (transfer).
// - Màn gán Frame (đặt ngay camera: điểm p hiện ở vị trí thế giới w, kẹp trong giới hạn kéo) và Glide (camera lướt tới điểm, chờ xong)
//   để ShipVoyage dàn cảnh lúc đi, lúc tới.
// Dựng bằng ShipBuild.Pier (Editor). Mỗi lúc chỉ một bến đang bật (Active): bến của màn đang mở.
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace PokiClash
{
    public sealed class PierShip : MonoBehaviour
    {
        public static PierShip Active { get; private set; }

        [SerializeField] ShipLook look;
        [SerializeField] Vector2 dock;
        [SerializeField] Vector2 dockFace = Vector2.right;
        [SerializeField] Vector2[] north = new Vector2[0], south = new Vector2[0];
        [SerializeField] float speed = 300; // đơn vị/giây khung cha, lúc chạy đều
        [SerializeField] ClickCatcher tap;
        [Tooltip("Điểm camera nhìn khi tàu đi / tới (giữa chỗ đậu và điểm ra khơi), neo như tàu")]
        [SerializeField] RectTransform focus;
        [Header("Bến thứ hai (sảnh: bến trên)")]
        [SerializeField] bool hasDock2;
        [SerializeField] Vector2 dock2, dock2Face = Vector2.down;
        [SerializeField] Vector2[] north2 = new Vector2[0]; // từ bến hai ra khơi phía bắc
        [SerializeField] Vector2[] transfer = new Vector2[0]; // từ bến chính sang bến hai (vòng ngoài đảo), không gồm hai đầu
        [SerializeField] float transferSpeed = 2.4f; // nhân tốc độ khi chuyển bến

        public Action<RectTransform, Vector3> Frame; // camera: điểm p hiện ở vị trí thế giới w (đặt ngay)
        public Func<RectTransform, IEnumerator> Glide; // camera lướt tới điểm p, xong thì trả về
        public Action OnTap;

        bool busy;
        Coroutine moving; // chuyển bến

        public ShipLook Look => look;
        public RectTransform ShipRect => look.Ship;
        public bool Busy => busy;
        public float Speed => speed;

        // Dùng khi dựng prefab (Editor).
        public void Setup(ShipLook l, Vector2 dockAt, Vector2 face, Vector2[] northPath, Vector2[] southPath, float spd, ClickCatcher catcher)
        {
            look = l;
            dock = dockAt;
            dockFace = face;
            north = northPath ?? new Vector2[0];
            south = southPath ?? new Vector2[0];
            speed = spd;
            tap = catcher;
        }

        // Dùng khi dựng prefab (Editor): bến thứ hai
        public void SetupDock2(Vector2 at, Vector2 face, Vector2[] northPath, Vector2[] transferPath, float transferMul)
        {
            hasDock2 = true;
            dock2 = at;
            dock2Face = face;
            north2 = northPath ?? new Vector2[0];
            transfer = transferPath ?? new Vector2[0];
            transferSpeed = transferMul;
        }

        void OnEnable()
        {
            Active = this;
            if (tap) tap.OnClick = () =>
            {
                if (!busy) OnTap?.Invoke();
            };
            Park();
        }

        void OnDisable()
        {
            if (Active == this) Active = null;
            busy = false;
            moving = null;
        }

        // chuyến hướng bắc đi / tới bến hai (nếu có)
        bool Second(bool northward) => hasDock2 && northward;

        Vector2 DockOf(bool northward) => Second(northward) ? dock2 : dock;
        Vector2 FaceOf(bool northward) => Second(northward) ? dock2Face : dockFace;
        Vector2[] PathOf(bool northward) => Second(northward) ? north2 : northward ? north : south;

        public bool Has(bool northward) => PathOf(northward).Length > 0;

        // Dùng khi dựng prefab (Editor).
        public void SetFocus(RectTransform f) => focus = f;

        // điểm nhìn cho chuyến đi / tới hướng này: giữa chỗ đậu và điểm ra khơi (camera thấy cả hai); chưa có thì là tàu
        public RectTransform FocusFor(bool northward)
        {
            if (!focus) return look.Ship;
            var p = PathOf(northward);
            var d = DockOf(northward);
            focus.anchoredPosition = Vector2.Lerp(d, p.Length > 0 ? p[p.Length - 1] : d, 0.55f);
            return focus;
        }

        // về chỗ đậu ngay: bến hai nếu có (chỗ đậu mặc định), không thì bến chính
        public void Park() => ParkAt(hasDock2);

        void ParkAt(bool second)
        {
            if (moving != null) StopCoroutine(moving);
            moving = null;
            busy = false;
            look.Show(true);
            look.Pos = second ? dock2 : dock;
            look.Face(second ? dock2Face : dockFace, true);
            look.ClearFoam();
        }

        void Update()
        {
            look.Night(DayCycle.Night(DayCycle.Hour));
            if (!busy) look.Tick(Time.unscaledDeltaTime, 0);
        }

        // điểm cuối đường ra khơi (chỗ giao tàu cho lớp mây), toạ độ thế giới
        public Vector3 ExitWorld(bool northward)
        {
            var p = PathOf(northward);
            return ToWorld(p.Length > 0 ? p[p.Length - 1] : DockOf(northward));
        }

        // hướng tàu ở điểm cuối khi đi VÀO bến (ngược hướng ra khơi), hướng trong không gian thế giới
        public Vector2 EntryDir(bool fromNorth)
        {
            var pts = Line(fromNorth);
            int n = pts.Count;
            var d = DockOf(fromNorth);
            if (n < 2) return ((Vector2)(ToWorld(d) - ToWorld(d + FaceOf(fromNorth)))).normalized;
            return ((Vector2)(ToWorld(pts[n - 2]) - ToWorld(pts[n - 1]))).normalized;
        }

        public Vector3 ToWorld(Vector2 local) => look.transform.TransformPoint(local);

        List<Vector2> Line(bool northward)
        {
            var list = new List<Vector2> { DockOf(northward) };
            list.AddRange(PathOf(northward));
            return list;
        }

        // rời bến theo đường; trả về khi đã đi phần `until` của đường (lớp mây nhận tàu từ đó, tàu của màn đứng lại và bị ẩn)
        public IEnumerator Depart(bool northward, float until = 1)
        {
            if (moving != null) ParkAt(Second(northward)); // đang chuyển bến dở: về luôn chỗ đậu của chuyến này
            var path = Sample(Line(northward));
            float L = path.length, s = 0, v = 0, accel = speed / 0.7f;
            busy = true;
            look.Show(true);
            while (s < L)
            {
                float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
                v = Mathf.Min(speed, v + accel * dt);
                s = Mathf.Min(L, s + v * dt);
                Move(path, s, v, dt);
                if (s >= until * L) yield break;
                yield return null;
            }
        }

        // tốc độ hiện tại trên đường (lớp mây giữ đà khi nhận tàu)
        public float CurrentSpeed { get; private set; }

        // vào bến: từ điểm cuối đường về chỗ đậu, hãm dần, quay mũi theo hướng đậu; vào bến chính mà có bến hai thì tự chuyển bến
        public IEnumerator Arrive(bool fromNorth, float startSpeed)
        {
            var line = Line(fromNorth);
            line.Reverse();
            var path = Sample(line);
            float L = path.length, s = 0, v = Mathf.Max(startSpeed, speed * 0.5f), brake = Mathf.Min(L * 0.7f, 260);
            busy = true;
            look.Show(true);
            while (s < L - 0.5f)
            {
                float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
                float want = speed * Mathf.Clamp((L - s) / brake, 0.1f, 1);
                v = Mathf.MoveTowards(v, want, speed * 2.2f * dt);
                s = Mathf.Min(L, s + v * dt);
                Move(path, s, v, dt);
                yield return null;
            }
            look.Pos = DockOf(fromNorth);
            look.Face(FaceOf(fromNorth));
            for (float t = 0; t < 0.35f; t += Time.unscaledDeltaTime)
            {
                look.Tick(Time.unscaledDeltaTime, 0);
                yield return null;
            }
            busy = false;
            CurrentSpeed = 0;
            if (hasDock2 && !Second(fromNorth) && isActiveAndEnabled) moving = StartCoroutine(Transfer());
        }

        // chuyển bến: từ bến chính chạy nhanh vòng ngoài đảo lên bến hai (không chặn thao tác của người chơi)
        IEnumerator Transfer()
        {
            yield return new WaitForSecondsRealtime(0.5f);
            var line = new List<Vector2> { dock };
            line.AddRange(transfer);
            line.Add(dock2);
            var path = Sample(line);
            float top = speed * transferSpeed, L = path.length, s = 0, v = 0, accel = top / 0.8f, brake = Mathf.Min(L * 0.3f, 420);
            busy = true;
            while (s < L - 0.5f)
            {
                float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
                float want = top * Mathf.Clamp((L - s) / brake, 0.12f, 1);
                v = Mathf.Min(want, v + accel * dt);
                s = Mathf.Min(L, s + v * dt);
                Move(path, s, v, dt);
                yield return null;
            }
            look.Pos = dock2;
            look.Face(dock2Face);
            busy = false;
            CurrentSpeed = 0;
            moving = null;
        }

        // đặt tàu ở điểm cuối đường (chờ lớp mây giao), ẩn
        public void HoldAtExit(bool fromNorth)
        {
            if (moving != null) StopCoroutine(moving);
            moving = null;
            busy = true;
            var p = PathOf(fromNorth);
            look.Pos = p.Length > 0 ? p[p.Length - 1] : DockOf(fromNorth);
            look.Face(EntryLocal(fromNorth), true);
            look.Show(false);
        }

        Vector2 EntryLocal(bool fromNorth)
        {
            var line = Line(fromNorth);
            int n = line.Count;
            return n >= 2 ? line[n - 2] - line[n - 1] : -FaceOf(fromNorth);
        }

        void Move(Polyline path, float s, float v, float dt)
        {
            var p = path.At(s);
            var ahead = path.At(Mathf.Min(path.length, s + 14));
            var d = ahead - p;
            if (d.sqrMagnitude < 0.01f && s > 1) d = p - path.At(s - 14);
            look.Pos = p;
            look.Face(d);
            look.Tick(dt, v);
            CurrentSpeed = v;
        }

        // ---------- đường cong qua các điểm ----------

        sealed class Polyline
        {
            public readonly List<Vector2> pts = new List<Vector2>();
            public readonly List<float> acc = new List<float>();
            public float length;

            public Vector2 At(float s)
            {
                if (pts.Count == 1) return pts[0];
                s = Mathf.Clamp(s, 0, length);
                int lo = 0, hi = acc.Count - 1;
                while (hi - lo > 1)
                {
                    int m = (lo + hi) / 2;
                    if (acc[m] <= s) lo = m;
                    else hi = m;
                }
                float seg = acc[hi] - acc[lo];
                return Vector2.Lerp(pts[lo], pts[hi], seg > 0 ? (s - acc[lo]) / seg : 0);
            }
        }

        static Polyline Sample(List<Vector2> ctrl)
        {
            var pl = new Polyline();
            int n = ctrl.Count;
            if (n == 1)
            {
                pl.pts.Add(ctrl[0]);
                pl.acc.Add(0);
                return pl;
            }
            for (int i = 0; i < n - 1; i++)
            {
                var p0 = ctrl[Mathf.Max(0, i - 1)];
                var p1 = ctrl[i];
                var p2 = ctrl[i + 1];
                var p3 = ctrl[Mathf.Min(n - 1, i + 2)];
                for (int k = 0; k < 16; k++)
                {
                    float t = k / 16f;
                    float t2 = t * t, t3 = t2 * t;
                    var q = 0.5f * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3);
                    Add(pl, q);
                }
            }
            Add(pl, ctrl[n - 1]);
            return pl;
        }

        static void Add(Polyline pl, Vector2 q)
        {
            if (pl.pts.Count > 0) pl.length += Vector2.Distance(pl.pts[pl.pts.Count - 1], q);
            pl.pts.Add(q);
            pl.acc.Add(pl.length);
        }
    }
}
