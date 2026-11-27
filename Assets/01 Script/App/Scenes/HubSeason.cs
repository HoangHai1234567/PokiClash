// Trang trí theo mùa ở sảnh và màn tải (Season; người dùng 2026-11-27: mùa đông Giáng sinh "làm thêm tuyết rơi và tuyết phủ lên một số
// phần trên đảo, thi thoảng ông già Noel bay qua bay lại", "làm thêm tuyết cho đảo Casino", "làm cho cả loading"). Tự gắn lúc chạy
// (HubSeasonHook: nghe SceneRouter.Entered, nhìn ShipVoyage.I), không sửa prefab Hub, ShipVoyage.
// Mùa Noel ở sảnh (HubSeason):
// - tuyết phủ: mỗi ảnh đảo "hinh" có ảnh sanh_dao_<tên> (5 đảo hệ + đảo Casino) mà Resources/Seasons/noel/tuyet_<tên> có thì đặt lớp tuyết
//   (tách từ bản GPT vẽ lại đảo có tuyết, khớp đúng toạ độ ảnh đảo, ArtGen/Seasons/noel/tach_tuyet.py) làm con đầu của "hinh", phủ kín
//   khung: dưới lớp nhuộm sáng tối (đêm tối theo), dưới mây che đảo chưa mở; đảo Kim vốn đã có tuyết nên không có lớp;
// - tuyết rơi (SnowFall) và ông già Noel bay ngang (SantaFlyby) ở lớp trời ngay trên khung bản đồ kéo được (HubPan), dưới hàng nút và
//   thanh trên: không che nút, không nhận chạm. Gắn với thế giới (người dùng 2026-11-27: "đừng để kiểu UI, khi drag cam thì vị trí cũng
//   phải thay đổi"): cả hai dời theo độ dời lớp bản đồ HubPan kéo (bông tuyết thêm thị sai theo lớp gần / xa), kéo bản đồ thì ông già Noel
//   trôi cùng đảo. Lớp trời ẩn trong lúc chuyến tàu qua mây chạy (ShipVoyage chụp màn sảnh làm nền: ảnh chụp không dính bông tuyết, ông
//   già Noel đứng hình; chuyến tàu có tuyết rơi riêng);
// - nhạc: AudioService.MusicFor lấy Season.HubMusic ("sanh_noel").
// Mùa Noel ở chuyến tàu qua mây (VoyageSeason, cả màn tải lúc mở game): tuyết rơi trên biển và mây (trôi theo camera của chuyến tàu như
// biển), dưới logo / thanh tải; nhạc màn tải là bài mùa (Season.LoadMusic) nên sang sảnh nhạc nối liền. Ông già Noel chỉ bay ở sảnh
// (người dùng 2026-11-27, bỏ chuyến bay ở màn tải).
// Mùa Noel ở màn Nhà và đảo Casino (MapSeason; người dùng 2026-11-27: "các màn home / đảo casino chưa thấy tuyết, làm giống ở phần đảo
// chính"): tuyết rơi ở lớp trời ngay trên khung bản đồ kéo được (Nhà: LandView, Casino: HubPan), dưới giao diện cố định; dời theo bản đồ
// khi kéo như ở sảnh; ẩn lúc chuyến tàu qua mây chạy. Tuyết phủ (người dùng 2026-11-27: "làm tuyết phủ lên đảo / cây cối / các
// building"): SeasonSkin đổi ảnh nền đảo, công trình, cây, vách, đồ ven biển sang bản có tuyết (Resources/Seasons/noel/map). Không có ông
// già Noel (chỉ ở sảnh).
// Đổi mùa giữa chừng (menu thử) thì lần bật lại dựng lại.
using System.Collections.Generic;
using System.Reflection;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HubSeason : MonoBehaviour
    {
        public static HubSeason Current { get; private set; }

        public SeasonId Built { get; private set; } = SeasonId.None;
        public SantaFlyby Santa { get; private set; }
        public SnowFall Snow { get; private set; }
        public int Covers { get; private set; }
        public string CoverList { get; private set; } = ""; // các đảo đã phủ tuyết (tour ghi log)

        readonly List<GameObject> made = new List<GameObject>();
        GameObject sky;
        RectTransform world; // lớp bản đồ HubPan kéo (độ dời của nó là độ dời thế giới)
        Vector2 world0;

        Vector2 WorldShift => world ? world.anchoredPosition - world0 : Vector2.zero;

        void OnEnable()
        {
            Current = this;
            Apply();
        }

        void OnDisable()
        {
            if (Current == this) Current = null;
        }

        void OnDestroy() => Clear();

        void LateUpdate()
        {
            if (!sky) return;
            bool show = !(ShipVoyage.I && ShipVoyage.I.isActiveAndEnabled);
            if (sky.activeSelf != show) sky.SetActive(show);
            if (Snow) Snow.scroll = WorldShift; // tuyết trôi theo bản đồ khi kéo
        }

        public void Apply()
        {
            var s = Season.Current;
            if (s == Built) return;
            Clear();
            Built = s;
            if (s == SeasonId.Noel) BuildNoel();
        }

        void Clear()
        {
            foreach (var g in made)
                if (g) Destroy(g);
            made.Clear();
            sky = null;
            Santa = null;
            Snow = null;
            Covers = 0;
            CoverList = "";
            Built = SeasonId.None;
        }

        void BuildNoel()
        {
            // tuyết phủ từng đảo, theo tên ảnh đảo (đảo Casino có HubIslandArt hệ ghi tạm Thủy nên không dựa vào Zone)
            foreach (var art in GetComponentsInChildren<HubIslandArt>(true))
            {
                var own = art.GetComponent<Image>();
                if (!own || !own.sprite || !own.sprite.name.StartsWith("sanh_dao_")) continue;
                string key = own.sprite.name.Substring("sanh_dao_".Length).Replace("(Clone)", "").Trim();
                var spr = Resources.Load<Sprite>("Seasons/noel/tuyet_" + key);
                if (!spr) continue;
                var rt = (RectTransform)new GameObject("tuyet_mua", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image)).transform;
                rt.SetParent(art.transform, false);
                rt.SetAsFirstSibling();
                rt.anchorMin = Vector2.zero;
                rt.anchorMax = Vector2.one;
                rt.offsetMin = rt.offsetMax = Vector2.zero;
                var img = rt.GetComponent<Image>();
                img.sprite = spr;
                img.raycastTarget = false;
                made.Add(rt.gameObject);
                Covers++;
                CoverList += (CoverList.Length > 0 ? ", " : "") + key;
            }
            // lớp trời: ngay trên khung bản đồ kéo được; tuyết, ông già Noel không đứng yên theo màn mà dời theo lớp bản đồ HubPan kéo
            var pan = GetComponentInChildren<HubPan>(true);
            var parent = pan ? (RectTransform)pan.transform.parent : (RectTransform)transform;
            world = pan ? typeof(HubPan).GetField("target", BindingFlags.NonPublic | BindingFlags.Instance)?.GetValue(pan) as RectTransform : null;
            world0 = world ? world.anchoredPosition : Vector2.zero;
            var skyRt = SeasonFx.Layer("mua_troi", parent, pan ? pan.transform.GetSiblingIndex() + 1 : -1);
            sky = skyRt.gameObject;
            made.Add(sky);
            Snow = SeasonFx.Snow(skyRt);
            // đoàn xe bay trên lớp tuyết cho rõ hình
            Santa = SantaFlyby.Create(skyRt, f => f.worldShift = () => WorldShift);
        }
    }

    // tuyết rơi + ông già Noel trên chuyến tàu qua mây và màn tải (gắn vào ShipVoyage)
    public sealed class VoyageSeason : MonoBehaviour
    {
        public static VoyageSeason Current { get; private set; }

        public SeasonId Built { get; private set; } = SeasonId.None;
        public SnowFall Snow { get; private set; }

        GameObject sky;
        ShipVoyage sv;
        FieldInfo fQc, fDir;

        void OnEnable()
        {
            Current = this;
            Apply();
        }

        void OnDisable()
        {
            if (Current == this) Current = null;
        }

        // tuyết rơi trôi theo camera chuyến tàu (toạ độ màn y = dir × (q − qc)): tàu tiến lên thì tuyết trôi xuống như biển, không đứng
        // yên theo màn. Ông già Noel ở màn tải bay kèm tàu (đi theo camera) nên không dời.
        void LateUpdate()
        {
            if (!Snow || !sv || fQc == null || fDir == null) return;
            float qc = (float)fQc.GetValue(sv);
            int dir = (int)fDir.GetValue(sv);
            Snow.scroll = new Vector2(0, -dir * qc);
        }

        public void Apply()
        {
            var s = Season.Current;
            if (s == Built) return;
            if (sky) Destroy(sky);
            sky = null;
            Snow = null;
            Built = s;
            if (s != SeasonId.Noel) return;
            sv = GetComponent<ShipVoyage>();
            const BindingFlags F = BindingFlags.NonPublic | BindingFlags.Instance;
            fQc = typeof(ShipVoyage).GetField("qc", F);
            fDir = typeof(ShipVoyage).GetField("dir", F);
            var area = typeof(ShipVoyage).GetField("area", F)?.GetValue(sv) as RectTransform;
            var boot = typeof(ShipVoyage).GetField("bootUi", F)?.GetValue(sv) as CanvasGroup;
            if (!area) return;
            // dưới logo, thanh tải, mẹo nếu chúng cùng cha; không thì trên cùng của khung biển
            int at = boot && boot.transform.parent == area ? boot.transform.GetSiblingIndex() : -1;
            var rt = SeasonFx.Layer("mua_troi", area, at);
            sky = rt.gameObject;
            Snow = SeasonFx.Snow(rt);
            // ông già Noel chỉ bay ở sảnh (người dùng 2026-11-27: "ông già noel chỉ hiện ở màn đảo chính thôi")
        }
    }

    // tuyết rơi ở màn có bản đồ kéo được ngoài sảnh (Nhà, đảo Casino); gắn vào SceneRoot của màn
    public sealed class MapSeason : MonoBehaviour
    {
        public static MapSeason Current { get; private set; }

        public SeasonId Built { get; private set; } = SeasonId.None;
        public SnowFall Snow { get; private set; }
        public SeasonSkin Skin { get; private set; }

        GameObject sky;
        RectTransform view, world; // khung kéo, lớp bản đồ (LandView dời + phóng; HubPan chỉ dời)
        Vector3 mark; // điểm bản đồ (local lớp bản đồ) nằm giữa khung ở khung trước
        Vector2 shift; // độ dời cộng dồn của bản đồ trên màn
        float nextTry;

        void OnEnable()
        {
            Current = this;
            Apply();
        }

        void OnDisable()
        {
            if (Current == this) Current = null;
        }

        void OnDestroy()
        {
            if (sky) Destroy(sky);
        }

        public void Apply()
        {
            var s = Season.Current;
            if (s == Built) return;
            if (sky) Destroy(sky);
            sky = null;
            Snow = null;
            Built = s;
            // tuyết phủ: đổi ảnh màn sang bản mùa ngay (trước khi chuyến tàu chụp màn làm nền)
            if (!Skin) Skin = GetComponent<SeasonSkin>() ?? gameObject.AddComponent<SeasonSkin>();
            Skin.Apply(s);
        }

        void LateUpdate()
        {
            if (Built != SeasonId.Noel) return;
            if (!sky)
            {
                // LandView của Nhà nhận lớp bản đồ trong Enter: chưa có thì dò lại sau 0,25 giây
                if (Time.unscaledTime < nextTry) return;
                nextTry = Time.unscaledTime + 0.25f;
                if (!Build()) return;
            }
            bool show = !(ShipVoyage.I && ShipVoyage.I.isActiveAndEnabled);
            if (sky.activeSelf != show) sky.SetActive(show);
            if (!Snow || !view || !world) return;
            // điểm bản đồ giữa khung ở khung trước giờ nằm đâu: phần lệch là độ dời bản đồ khung này (kéo, trôi, phóng quanh chỗ chụm);
            // phóng quanh giữa khung thì không dời tuyết
            Vector2 c = view.rect.center;
            shift += (Vector2)view.InverseTransformPoint(world.TransformPoint(mark)) - c;
            mark = world.InverseTransformPoint(view.TransformPoint(c));
            Snow.scroll = shift;
        }

        bool Build()
        {
            const BindingFlags F = BindingFlags.NonPublic | BindingFlags.Instance;
            view = world = null;
            var lv = GetComponentInChildren<LandView>(true);
            if (lv)
            {
                world = typeof(LandView).GetField("content", F)?.GetValue(lv) as RectTransform;
                view = lv.transform as RectTransform;
            }
            else
            {
                var pan = GetComponentInChildren<HubPan>(true);
                if (pan)
                {
                    world = typeof(HubPan).GetField("target", F)?.GetValue(pan) as RectTransform;
                    view = pan.transform as RectTransform;
                }
            }
            if (!view || !world || !view.parent) return false;
            // lớp trời ngay trên khung bản đồ: dưới giao diện cố định (thanh trên, hàng nút, vòng nút), không nhận chạm
            var rt = SeasonFx.Layer("mua_troi", view.parent, view.GetSiblingIndex() + 1);
            sky = rt.gameObject;
            Snow = SeasonFx.Snow(rt);
            mark = world.InverseTransformPoint(view.TransformPoint(view.rect.center));
            shift = Vector2.zero;
            return true;
        }
    }

    static class SeasonFx
    {
        public static RectTransform Layer(string name, Transform parent, int sibling)
        {
            var rt = (RectTransform)new GameObject(name, typeof(RectTransform)).transform;
            rt.SetParent(parent, false);
            if (sibling >= 0) rt.SetSiblingIndex(sibling);
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            return rt;
        }

        // tuyết rơi trên Canvas riêng: lưới dựng lại mỗi khung không làm bẩn canvas của màn
        public static SnowFall Snow(Transform parent)
        {
            var rt = (RectTransform)new GameObject("tuyet_roi", typeof(RectTransform), typeof(Canvas), typeof(CanvasRenderer)).transform;
            rt.SetParent(parent, false);
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            return rt.gameObject.AddComponent<SnowFall>();
        }
    }

    // gắn HubSeason vào màn sảnh mỗi lần vào sảnh, VoyageSeason vào chuyến tàu (không sửa HubScene, ShipVoyage, prefab)
    sealed class HubSeasonHook : MonoBehaviour
    {
        static HubSeasonHook I;
        bool hooked;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        static void Boot()
        {
            if (I) return;
            var go = new GameObject("HubSeasonHook");
            DontDestroyOnLoad(go);
            I = go.AddComponent<HubSeasonHook>();
        }

        void Update()
        {
            var sv = ShipVoyage.I;
            if (sv && !sv.GetComponent<VoyageSeason>()) sv.gameObject.AddComponent<VoyageSeason>();
            if (hooked || App.Router == null) return;
            App.Router.Entered += OnEntered;
            hooked = true;
            if (App.Router.CurrentRoot) OnEntered(App.Router.CurrentRoot);
        }

        void OnDestroy()
        {
            if (hooked && App.Router != null) App.Router.Entered -= OnEntered;
        }

        static void OnEntered(SceneRoot root)
        {
            if (root is HubScene h) Attach(h);
            else if (root is HomeScene || root is CasinoScene)
            {
                var m = root.GetComponent<MapSeason>();
                if (!m) root.gameObject.AddComponent<MapSeason>();
                else m.Apply();
            }
        }

        static void Attach(HubScene h)
        {
            var s = h.GetComponent<HubSeason>();
            if (!s) h.gameObject.AddComponent<HubSeason>();
            else s.Apply();
        }
    }
}
