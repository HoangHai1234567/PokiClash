// Ông già Noel cưỡi xe trượt, ba tuần lộc kéo, thi thoảng bay ngang trời sảnh (mùa Noel, người dùng 2026-11-27). Ảnh GPT 2.6 vẽ theo nét
// game (ArtGen/Seasons/noel/xuat_noel.py → Assets/03 Art/Seasons/Resources/Seasons/noel): xe trượt có ông già Noel và túi quà; tuần lộc
// hai dáng phi (duỗi chân / co chân) đổi nhau lệch pha giữa ba con cho ra bước phi; dây cương là nét mực nâu nối đầu dây của xe với đai
// bụng tuần lộc sau, ngực con sau với đai bụng con trước, bám theo dáng đang hiện. Ông già Noel kiểu dân gian chung (không theo hình của
// hãng nào), tuần lộc mũi nâu (không phải nhân vật có bản quyền).
// Bay qua trong ~10 giây theo đường lượn sóng nhẹ ở nửa trên màn, chiều ngẫu nhiên (lật ngang khi bay sang trái), cả đoàn nhấp nhô lệch
// pha, đoàn nghiêng theo đường bay; sau xe rắc bụi tuyết lấp lánh rơi chậm rồi mờ. Sảnh: lần đầu 6–10 giây sau khi vào sảnh, sau đó cách
// 35–75 giây; không bay khi đang có hộp thoại, bước hướng dẫn hay chuyển cảnh. Màn tải (VoyageSeason) đặt nhịp riêng qua Create(configure):
// bay một lần ngay khi màn tải hiện (gate). Tiếng chuông xe ("noelBells") lúc đoàn vào màn.
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class SantaFlyby : MonoBehaviour
    {
        // điểm neo trên ảnh (tỉ lệ ảnh, gốc dưới trái): đầu dây của xe; tuần lộc theo dáng: sau (đai bụng, cũng là gốc đặt ảnh), trước (ngực)
        static readonly Vector2 SledRope = new Vector2(0.987f, 0.365f);
        static readonly Vector2[] DeerBack = { new Vector2(0.490f, 0.334f), new Vector2(0.405f, 0.354f) };
        static readonly Vector2[] DeerFront = { new Vector2(0.782f, 0.359f), new Vector2(0.748f, 0.378f) };
        // gốc đặt từng tuần lộc tính từ đầu dây của xe (điểm ảnh của ảnh xuất), đoàn hơi ngẩng lên
        static readonly Vector2[] DeerHome = { new Vector2(140, 12), new Vector2(350, 26), new Vector2(560, 40) };
        static readonly Color Ink = new Color32(74, 42, 26, 255);
        static readonly Color Gold = new Color32(255, 233, 168, 255);

        public float scale = 0.55f; // ảnh xuất bằng 50 % tờ GPT; 0,55 cho cả đoàn rộng ~ nửa màn 1080
        public float firstMin = 6, firstMax = 10, gapMin = 35, gapMax = 75, duration = 10;
        public float retry = 3; // tới giờ mà chưa bay được thì thử lại sau chừng này giây
        public float yMin = 0.6f, yMax = 0.8f; // độ cao đường bay (phần chiều cao màn, tính từ đáy)
        public System.Func<bool> gate; // điều kiện bay riêng (màn tải: đang tải); null: sảnh rảnh (CanStart)
        // độ dời của thế giới trên màn (sảnh: lớp bản đồ HubPan): đoàn xe và bụi tuyết dời theo, kéo bản đồ thì ông già Noel trôi cùng
        // đảo (người dùng 2026-11-27: "đừng để kiểu UI"); null: đi theo màn (màn tải: bay kèm tàu, camera đi cùng tàu)
        public System.Func<Vector2> worldShift;
        Vector2 shift0, shiftLast;

        RectTransform area, team, sled;
        readonly RectTransform[] deer = new RectTransform[3];
        readonly Image[] deerImg = new Image[3];
        readonly RectTransform[] ropes = new RectTransform[3];
        readonly Sprite[] deerSpr = new Sprite[2];
        Sprite dustSpr;
        float wait, fly = -1, dir = 1, y0, back, front, emit;

        struct Dust
        {
            public RectTransform rt;
            public Image img;
            public Vector2 v;
            public float life, max, size;
        }

        readonly List<Dust> dust = new List<Dust>();

        public bool Flying => fly >= 0;
        public RectTransform Team => team; // cả đoàn (tour đo vị trí)

        // configure: đặt nhịp / điều kiện riêng trước lúc hẹn chuyến đầu (màn tải bay sớm, một lần)
        public static SantaFlyby Create(RectTransform parent, System.Action<SantaFlyby> configure = null)
        {
            var go = new GameObject("ong_gia_noel", typeof(RectTransform));
            var rt = (RectTransform)go.transform;
            rt.SetParent(parent, false);
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            var s = go.AddComponent<SantaFlyby>();
            configure?.Invoke(s);
            return s.Build() ? s : null;
        }

        static Sprite Load(string n) => Resources.Load<Sprite>("Seasons/noel/" + n);

        bool Build()
        {
            area = (RectTransform)transform;
            var sledSpr = Load("noel_xe");
            deerSpr[0] = Load("noel_tuan_loc_1");
            deerSpr[1] = Load("noel_tuan_loc_2");
            if (!sledSpr || !deerSpr[0] || !deerSpr[1])
            {
                Debug.LogWarning("[Mùa] Thiếu ảnh ông già Noel trong Resources/Seasons/noel");
                Destroy(gameObject);
                return false;
            }
            var ft = SnowFall.FlakeTexture;
            dustSpr = Sprite.Create(ft, new Rect(0, 0, ft.width, ft.height), new Vector2(0.5f, 0.5f), 100);

            team = Rect("doan", area);
            team.anchorMin = team.anchorMax = Vector2.zero;
            team.sizeDelta = Vector2.zero;
            for (int i = 0; i < 3; i++) // dây sau cùng, tuần lộc giữa (con trước vẽ trước), xe trên cùng đè đầu dây
            {
                ropes[i] = Rect("day_" + i, team);
                ropes[i].pivot = new Vector2(0, 0.5f);
                var img = ropes[i].gameObject.AddComponent<Image>();
                img.color = Ink;
                img.raycastTarget = false;
            }
            for (int i = 2; i >= 0; i--)
            {
                deer[i] = Rect("tuan_loc_" + i, team);
                deerImg[i] = deer[i].gameObject.AddComponent<Image>();
                deerImg[i].raycastTarget = false;
            }
            sled = Rect("xe", team);
            var si = sled.gameObject.AddComponent<Image>();
            si.sprite = sledSpr;
            si.raycastTarget = false;
            sled.pivot = SledRope;
            sled.sizeDelta = sledSpr.rect.size * scale;
            back = sled.sizeDelta.x * SledRope.x + 30;
            front = (DeerHome[2].x + deerSpr[0].rect.width * (1 - DeerBack[0].x)) * scale + 30;
            team.gameObject.SetActive(false);
            wait = Random.Range(firstMin, firstMax);
            return true;
        }

        static RectTransform Rect(string name, Transform parent)
        {
            var rt = (RectTransform)new GameObject(name, typeof(RectTransform)).transform;
            rt.SetParent(parent, false);
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            return rt;
        }

        bool CanStart() => gate != null ? gate() :
            App.I && App.Modals.Count == 0 && Guide.Idle && App.Router != null && !App.Router.Busy && App.Router.Current == SceneIds.Hub && !ShipVoyage.Booting;

        // bay ngay (tour thử)
        public void FlyNow() => Begin();

        void Begin()
        {
            var r = area.rect;
            dir = Random.value < 0.5f ? 1 : -1;
            y0 = r.height * Random.Range(yMin, yMax);
            fly = 0;
            shift0 = Shift;
            team.gameObject.SetActive(true);
            team.localScale = new Vector3(dir, 1, 1);
            App.Audio.Play("noelBells", 0.6f);
        }

        Vector2 Shift => worldShift != null ? worldShift() : Vector2.zero;

        // đoàn xe còn chạm khung nhìn không (tính cả phần đầu tuần lộc, đuôi xe)
        bool Visible()
        {
            var r = area.rect;
            var p = team.anchoredPosition;
            float left = dir > 0 ? back : front, right = dir > 0 ? front : back, half = 220 * scale;
            return p.x + right > 0 && p.x - left < r.width && p.y + half > 0 && p.y - half < r.height;
        }

        void Update()
        {
            if (!team) return;
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            var sh = Shift;
            var moved = sh - shiftLast;
            shiftLast = sh;
            UpdateDust(dt, moved);
            if (fly < 0)
            {
                wait -= dt;
                if (wait > 0) return;
                if (!CanStart())
                {
                    wait = retry;
                    return;
                }
                Begin();
            }
            fly += dt;
            float p = fly / duration;
            var r = area.rect;
            float x0 = dir > 0 ? -front : r.width + front, x1 = dir > 0 ? r.width + back : -back;
            Vector2 Pos(float q) => new Vector2(Mathf.LerpUnclamped(x0, x1, q), y0 + Mathf.Sin(q * Mathf.PI * 1.4f) * r.height * 0.03f + (q - 0.5f) * r.height * 0.05f);
            var pos = Pos(p);
            var vel = Pos(p + 0.01f) - pos;
            team.anchoredPosition = pos + (sh - shift0);
            // hết đường bay mà người chơi kéo bản đồ làm đoàn xe còn trong khung thì bay tiếp tới khi ra khỏi khung (tối đa gấp đôi đường)
            if (p >= 1 && (!Visible() || p >= 2))
            {
                fly = -1;
                team.gameObject.SetActive(false);
                wait = Random.Range(gapMin, gapMax);
                return;
            }
            float tilt = Mathf.Clamp(Mathf.Atan2(vel.y, Mathf.Abs(vel.x)) * Mathf.Rad2Deg * 0.6f, -8, 8);
            team.localEulerAngles = new Vector3(0, 0, tilt * dir);
            Animate(Time.unscaledTime);
            emit -= dt;
            if (emit <= 0)
            {
                emit = 0.05f;
                Emit();
            }
        }

        void Animate(float tt)
        {
            sled.anchoredPosition = new Vector2(0, Mathf.Sin(tt * 4.2f) * 4);
            sled.localEulerAngles = new Vector3(0, 0, Mathf.Sin(tt * 4.2f + 0.8f) * 1.5f);
            var prev = sled.anchoredPosition; // đầu dây của xe (gốc ảnh xe)
            for (int i = 0; i < 3; i++)
            {
                int pose = (int)((tt + i * 0.09f) / 0.12f) % 2;
                var spr = deerSpr[pose];
                if (deerImg[i].sprite != spr) deerImg[i].sprite = spr;
                var size = spr.rect.size * scale;
                deer[i].pivot = DeerBack[pose];
                deer[i].sizeDelta = size;
                deer[i].anchoredPosition = DeerHome[i] * scale + new Vector2(0, Mathf.Sin(tt * 8.4f + i * 1.3f) * 3);
                Rope(ropes[i], prev, deer[i].anchoredPosition);
                prev = deer[i].anchoredPosition + Vector2.Scale(DeerFront[pose] - DeerBack[pose], size);
            }
        }

        void Rope(RectTransform rt, Vector2 a, Vector2 b)
        {
            var d = b - a;
            rt.anchoredPosition = a;
            rt.sizeDelta = new Vector2(d.magnitude, Mathf.Max(2, 5 * scale));
            rt.localEulerAngles = new Vector3(0, 0, Mathf.Atan2(d.y, d.x) * Mathf.Rad2Deg);
        }

        // bụi tuyết lấp lánh rắc từ đuôi xe (trắng xen vàng nhạt), rơi chậm, nhỏ dần, mờ dần
        void Emit()
        {
            Dust d = default;
            int idx = dust.FindIndex(q => q.life <= 0);
            if (idx < 0)
            {
                if (dust.Count >= 40) return;
                var rt = Rect("bui", area);
                rt.anchorMin = rt.anchorMax = Vector2.zero;
                var img = rt.gameObject.AddComponent<Image>();
                img.sprite = dustSpr;
                img.raycastTarget = false;
                d.rt = rt;
                d.img = img;
                dust.Add(d);
                idx = dust.Count - 1;
            }
            d = dust[idx];
            var sz = sled.sizeDelta;
            // đuôi xe, ngang chân ván trượt (toạ độ trong ảnh xe → toạ độ màn)
            var local = new Vector3(-sz.x * SledRope.x * 0.85f, -sz.y * SledRope.y * 0.75f, 0);
            var world = sled.TransformPoint(local);
            var lp = (Vector2)area.InverseTransformPoint(world) - area.rect.min;
            d.rt.anchoredPosition = lp + Random.insideUnitCircle * 10;
            d.v = new Vector2(-dir * Random.Range(10f, 40f), -Random.Range(20f, 50f));
            d.max = d.life = Random.Range(0.8f, 1.3f);
            d.size = Random.Range(7f, 15f);
            d.img.color = Random.value < 0.35f ? Gold : Color.white;
            d.rt.gameObject.SetActive(true);
            dust[idx] = d;
        }

        // moved: thế giới vừa dời bao nhiêu trên màn (bụi tuyết nằm trong thế giới, dời theo)
        void UpdateDust(float dt, Vector2 moved)
        {
            for (int i = 0; i < dust.Count; i++)
            {
                var d = dust[i];
                if (d.life <= 0) continue;
                d.life -= dt;
                if (d.life <= 0)
                {
                    d.rt.gameObject.SetActive(false);
                    dust[i] = d;
                    continue;
                }
                float k = d.life / d.max;
                d.rt.anchoredPosition += d.v * dt + moved;
                d.rt.sizeDelta = Vector2.one * d.size * (0.4f + 0.6f * k);
                var c = d.img.color;
                c.a = Mathf.Clamp01(k * 1.5f);
                d.img.color = c;
                dust[i] = d;
            }
        }
    }
}
