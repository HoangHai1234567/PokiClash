// Màn đảo kiểu vùng đất (ZoneDef.land, GD_Claude/18_DaoVungDat_Habitat.md, M1 2026-11-18): một đảo rộng kéo hai chiều
// (ScrollRect của Screens/Zone bật cả ngang lẫn dọc lúc chạy, không đổi cây prefab), ảnh nền vẽ sẵn đường và các bệ tròn.
// - Habitat: mỗi ải tướng một bệ ZoneNode (Items/BeAi) đặt ở tâm bệ của ảnh nền, không vẽ bệ đất (ảnh nền đã có), phóng theo cỡ
//   habitat; tướng chạy rig .atomik qua AolaSticker: idle liên tục, cứ 8–15 giây đánh một lần (hai con trong khung không đánh
//   cùng lúc), chạm thì đánh ngay rồi camera lướt tới và mở hộp chuẩn bị. Ải chưa mở vẫn đủ màu (người dùng chốt 2026-11-13).
//   Ải đã qua: idle chậm lại, thôi đánh. Ải vừa mở (thắng xong quay về): camera lướt từ ải trước tới, tướng diễn ra sân.
// - Ải xen giữa: cờ LandFlag (Items/CoAi; góp ý 2026-11-18: chia đều, không số, nổi bật, đổi sang cờ), cỡ ở land.pip, rải đều
//   trên phần đường ngoài vòng đá và thân tướng; điểm mốc mỗi habitat trượt trong đoạn đường ôm vòng đá cho các chặng thưa đều
//   nhau; chân cờ nằm đúng trên đường (người dùng 2026-11-18: "phải đặt các mốc đúng nằm trên path", bỏ xếp so le hai bên đường
//   của chấm cũ). Cờ và habitat xếp lớp theo chân (thấp hơn đè lên). Cách rải khớp
//   ArtGen/Islands/land_thuy/m0/build_land.py (layout). Chưa gán cờ thì dùng chấm ZonePip cũ (không số).
// - Vùng boss (land.secs; người dùng 2026-11-18: "phân section cho đảo, đánh xong 1 boss thì unlock section sau, chưa unlock thì
//   tướng không play animation", rồi "kết hợp cả A và B, mây tan ra, có bút chì vào tô màu section mới"; phủ đen bị chê):
//   vùng chưa mở vẽ phác chì chưa tô (landSketch: con đầu của ảnh bản đồ, shader PokiClash/UILandSketch đọc biến toàn cục
//   _PokiLandOpened), hiệu ứng và đèn trong vùng tắt, cờ nét chưa tô, tướng xám đứng yên, mây vẽ tay (land.secs[k].clouds) phủ trên
//   cùng; chạm vào báo phải hạ boss nào. Vừa mở vùng (thắng boss quay về): mây tản ra rồi tan, bút chì bay vào ngoáy dọc đường, màu loang
//   theo nét bút (_PokiLandReveal), tô nốt, tướng boss diễn ra sân, cờ mọc lên lần lượt. Vùng đã mở mà chưa diễn (LandShown, lưu
//   trong bản lưu) thì vào đảo là diễn, kể cả vùng 0 lần đầu vào đảo; trong lúc diễn khoá mọi thao tác (CloudCover.Block), người chơi
//   phải xem hết (người dùng 2026-11-18). Chốt này thay "ải chưa mở vẫn đủ màu" (2026-11-13) ở đảo vùng đất.
// - Sóng đập bờ: material landWater (shader PokiClash/UIInkWater, ảnh khoảng cách tới bờ) đặt lên ảnh nền.
// - Máy yếu: chỉ dựng và chạy hình tướng nằm trong khung nhìn cộng lề; hình đã dựng giữ tới khi rời màn.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;
using Random = UnityEngine.Random;

namespace PokiClash
{
    public sealed partial class ZoneScene
    {
        [Tooltip("Sóng đập bờ cho ảnh nền vùng đất (shader PokiClash/UIInkWater; menu PokiClash/Đảo vùng đất/Dựng nước, ảnh)")]
        [SerializeField] Material landWater;
        [Tooltip("Sóng đập bờ từng đảo vùng đất: material tên land_water_<đảo> (land.art = land_<đảo>); không có thì dùng landWater")]
        [SerializeField] Material[] landWaters;
        [Tooltip("Phác chì vùng boss từng đảo: material tên land_sketch_<đảo> (ảnh trường vùng riêng); menu Dựng cờ ải, vùng boss")]
        [SerializeField] Material[] landSketches;
        [Tooltip("Camera kéo, chụm hai ngón để zoom của đảo vùng đất (trên khung cuộn, cùng chỗ ScrollRect; menu Dựng nước, ảnh)")]
        [SerializeField] LandView landView;
        [Tooltip("Lớp sáng tối theo giờ máy trên ảnh bản đồ (menu PokiClash/Sáng tối/Dựng lớp sáng tối)")]
        [SerializeField] DayNight dayNight;
        [Tooltip("Cờ ải xen giữa của đảo vùng đất (Items/CoAi; menu PokiClash/Đảo vùng đất/Dựng cờ ải)")]
        [SerializeField] LandFlag flagPrefab;
        [Tooltip("Hình rời của vùng boss (mây phủ, bút chì): Items/HinhDong; menu PokiClash/Đảo vùng đất/Dựng cờ ải, vùng boss")]
        [SerializeField] Image secPrefab;
        [Tooltip("Phác chì vùng boss chưa mở: con đầu của ảnh bản đồ (dưới hiệu ứng), material shader PokiClash/UILandSketch")]
        [SerializeField] Image landSketch;
        [Tooltip("Bút chì bay vào tô màu vùng boss vừa mở (Assets/03 Art/Islands/Co/but_chi.png)")]
        [SerializeField] Sprite pencilArt;
        // canvas con cùng khung toạ độ với lớp nút (anh em ngay sau nó): mây phủ tĩnh tách riêng cho canvas chính (cờ bay, hiệu ứng chạy
        // mỗi khung) khỏi gộp lại hàng trăm đám mây mỗi khung; lớp trên mây cho easter egg, bút chì, boss ló đầu (đo hiệu năng 2026-11-18)
        [Tooltip("Canvas con chứa mây phủ vùng boss (menu Dựng cờ ải, vùng boss)")]
        [SerializeField] RectTransform cloudLayer;
        [Tooltip("Canvas con trên lớp mây: easter egg, bút chì, boss ló đầu")]
        [SerializeField] RectTransform overLayer;
        Transform CloudParent => cloudLayer ? cloudLayer : p.nodeLayer;
        Transform OverParent => overLayer ? overLayer : p.nodeLayer;

        // khớp build_land.py: PAD, HERO_H
        const float LandPad = 0;
        public static float LandHeroH(int size) => size >= 4 ? 480 : 360;
        const float AtkMin = 8, AtkMax = 15, AtkGap = 2, TapOpen = 0.45f, SeaBleed = 20000;
        const string Idle = StageView.Idle, Attack = StageView.Attack, Appear = Game.AolaActor.Appear;

        sealed class LandHero
        {
            public StageDef st;
            public ZoneNode node;
            public HeroDef hero;
            public string form;
            public AolaSticker sticker;
            public bool failed, cleared, appear, locked; // locked: ở vùng boss chưa mở (đứng yên, tô tối)
            public string lockMsg;
            public float stand, scale, t, next;
            public string clip = Idle;
            public Vector2 pos;   // tâm bệ trên khung ảnh (gốc trên trái, y âm xuống)
            public float bodyH;   // cao thân tướng trên màn (để biết còn trong khung nhìn)
        }

        LandDef land;
        readonly List<LandHero> landHeroes = new List<LandHero>();
        readonly List<ZonePip> landPips = new List<ZonePip>();
        readonly List<LandFlag> landFlags = new List<LandFlag>();
        // vùng boss: biến toàn cục của shader phác chì; bút chì (pivot ở mũi, khớp ve_co.py; cỡ = cỡ ảnh × PencilScale đơn vị bản đồ)
        static readonly int OpenedId = Shader.PropertyToID("_PokiLandOpened"), RevSecId = Shader.PropertyToID("_PokiLandRevealSec"),
            RevNId = Shader.PropertyToID("_PokiLandRevealN"), RevFadeId = Shader.PropertyToID("_PokiLandRevealFade"),
            RevId = Shader.PropertyToID("_PokiLandReveal");
        static readonly Vector4[] revealBuf = new Vector4[24];
        static readonly Vector2 PencilPivot = new Vector2(0.1139f, 0.1477f);
        // mở vùng: chờ camera lướt, mây tan, bút ngoáy, tô nốt (giây); bán kính vệt tô, biên độ ngoáy ngang đường (đơn vị bản đồ)
        const float FlagGap = 0.14f; // cờ mọc cách nhau (giây)
        static CloudCover inputCover;
        const float RevWait = 0.8f, CloudGone = 1.1f, PenTime = 2.6f, PenFill = 0.6f, PenRadius = 330, PenZig = 210, PencilScale = 1.4f;
        List<Image>[] secClouds;
        int landOpened = 99;
        float cloudHour = -1;
        Coroutine reveal;
        float appliedZoom = -1;
        static Vector2 MapPt(Vector2 flipped) => new Vector2(flipped.x, -flipped.y); // chỗ trên khung ảnh (y âm) → toạ độ bản đồ (y dương xuống)
        float landClock, lastAtk = -99;
        Coroutine glide;
        // tiến độ đã thấy của từng đảo vùng đất: ải mới mở thì lướt camera và cho tướng ra sân
        static readonly Dictionary<Elem, int> landSeen = new Dictionary<Elem, int>();

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)] // Play không reload domain
        static void ResetLand() => landSeen.Clear();

        // cách dựng gốc của khung cuộn (đảo kiểu cũ dùng lại khi rời đảo vùng đất)
        bool scrollSaved, scrollH, scrollV;
        Vector2 contentMin, contentMax, contentPivot;
        Material mapMaterial;

        // ---------- vào đảo ----------

        // đảo có vùng đất: dựng khung cuộn hai chiều, ảnh nền, sóng; không có thì trả khung cuộn về như cũ
        bool EnterLand(ZoneDef z)
        {
            var c = p.content;
            if (!scrollSaved)
            {
                scrollSaved = true;
                scrollH = p.scroll.horizontal;
                scrollV = p.scroll.vertical;
                contentMin = c.anchorMin;
                contentMax = c.anchorMax;
                contentPivot = c.pivot;
                mapMaterial = p.map.material == p.map.defaultMaterial ? null : p.map.material;
            }
            land = z.land != null && z.land.Has ? z.land : null;
            if (land == null)
            {
                p.scroll.horizontal = scrollH;
                p.scroll.vertical = scrollV;
                c.anchorMin = contentMin;
                c.anchorMax = contentMax;
                c.pivot = contentPivot;
                c.anchoredPosition = Vector2.zero;
                c.localScale = Vector3.one;
                p.map.material = mapMaterial;
                p.map.rectTransform.anchoredPosition = new Vector2(0, -PadT);
                p.scroll.enabled = true;
                if (seaScroll)
                {
                    seaScroll.rectTransform.offsetMin = seaScroll.rectTransform.offsetMax = Vector2.zero;
                    seaScroll.pixelsPerUnitMultiplier = 1;
                }
                if (landView) landView.End();
                if (landSketch) landSketch.gameObject.SetActive(false);
                return false;
            }
            mapW = (float)land.w;
            mapH = (float)land.h;
            c.anchorMin = c.anchorMax = new Vector2(0, 1);
            c.pivot = new Vector2(0, 1);
            p.scroll.horizontal = true;
            p.scroll.vertical = true;
            if (landView)
            {
                // camera riêng: bản đồ nằm sát mép lớp nội dung, khung trên / dưới tính bằng lề che (không đệm PadT, PadB)
                c.sizeDelta = new Vector2(mapW, mapH);
                p.map.rectTransform.anchoredPosition = Vector2.zero;
                p.scroll.StopMovement();
                p.scroll.enabled = false;
                landView.Changed -= OnLandView;
                landView.Changed += OnLandView;
                // vùng được kéo, zoom ra ngoài ảnh: vành mây (land.pan, tỉ lệ bề ngang ảnh)
                var around = land.pan.Count >= 4
                    ? new Vector4((float)land.pan[0], (float)land.pan[1], (float)land.pan[2], (float)land.pan[3]) * mapW
                    : Vector4.zero;
                landView.Begin(c, new Vector2(mapW, mapH), PadT, PadB, around);
            }
            else c.sizeDelta = new Vector2(mapW, PadT + mapH + PadB);
            var sprite = App.Art ? App.Art.Get(land.art) : null;
            p.map.name = "anh_" + land.art;
            Theme.SetSprite(p.map, sprite);
            p.map.rectTransform.sizeDelta = new Vector2(mapW, mapH);
            var water = IslandMat(landWaters, "land_water_", landWater);
            p.map.material = water ? water : mapMaterial;
            // biển quanh đảo: tấm biển lặp cắt từ chính nét biển của ảnh nền, cùng mật độ điểm ảnh, tràn ra ngoài bản đồ (thay biển lặp
            // cũ có vẽ sóng, hai lớp nước không khớp; góp ý 2026-11-18)
            var seaArt = App.Art && !string.IsNullOrEmpty(land.sea) ? App.Art.Get(land.sea) : null;
            if (seaScroll && seaArt && sprite)
            {
                seaScroll.sprite = seaArt;
                seaScroll.type = Image.Type.Tiled;
                seaScroll.color = Color.white;
                seaScroll.pixelsPerUnitMultiplier = sprite.rect.width / mapW;
                var sr = seaScroll.rectTransform;
                sr.offsetMin = -Vector2.one * SeaBleed;
                sr.offsetMax = Vector2.one * SeaBleed;
            }
            if (mapAnim) mapAnim.Bind(land.art);
            if (dayNight) dayNight.Bind(land.art);
            // boss vùng khoá tung tuyệt kỹ: tính lại mỗi lần vào đảo (dựng lại màn sau khi lưu không tính lại)
            ultLeft = UltMax;
            nextUlt = eggClock + Random.Range(10f, 16f);
            if (landSketch)
            {
                // ảnh trường vùng riêng từng đảo; đảo chưa có material phác chì thì tắt phác (mây vẫn phủ)
                var sketch = IslandMat(landSketches, "land_sketch_", landSketch.material);
                bool on = land.secs.Count > 0 && sprite && sketch;
                landSketch.gameObject.SetActive(on);
                if (on)
                {
                    landSketch.material = sketch;
                    landSketch.sprite = sprite; // không qua Theme.SetSprite: giữ material phác chì
                    var r = landSketch.rectTransform;
                    r.anchorMin = Vector2.zero;
                    r.anchorMax = Vector2.one;
                    r.offsetMin = r.offsetMax = Vector2.zero;
                    r.SetAsFirstSibling(); // ngay trên ảnh bản đồ, dưới hiệu ứng, sáng tối
                }
            }
            return true;
        }

        // material riêng của đảo đang mở: tên <đầu>_<đảo>, đảo lấy từ land.art (land_thuy → thuy)
        Material IslandMat(Material[] mats, string head, Material fallback)
        {
            string key = land != null && land.art != null && land.art.StartsWith("land_") ? head + land.art.Substring(5) : null;
            if (mats != null && key != null)
                foreach (var m in mats)
                    if (m && m.name == key) return m;
            return fallback && (key == null || fallback.name == key) ? fallback : null;
        }

        public override void Exit() => ClearLandHeroes();

        void ClearLandHeroes()
        {
            if (reveal != null)
            {
                StopCoroutine(reveal);
                LockInput(false);
            }
            reveal = null;
            secClouds = null;
            ClearEggs();
            foreach (var layer in new[] { cloudLayer, overLayer })
                if (layer)
                    for (int i = layer.childCount - 1; i >= 0; i--) Destroy(layer.GetChild(i).gameObject);
            Shader.SetGlobalFloat(RevSecId, -1);
            foreach (var h in landHeroes) h.sticker?.Destroy();
            landHeroes.Clear();
            landPips.Clear();
            landFlags.Clear();
            appliedZoom = -1;
        }

        // ---------- rải ải trên đường ----------

        struct LandLay
        {
            public Vector2[] pos; // chỗ từng ải (theo idx - 1) trên khung ảnh, gốc trên trái, y dương xuống
            public float[] at;    // quãng đường của từng ải tính từ bến
            public List<TrailPt> poly;
        }

        static bool InRing(LandDef l, LandHab h, Vector2 q, float grow)
        {
            float rx = (float)h.ring.x * (float)l.w + LandPad + grow, ry = (float)h.ring.y * (float)l.h + LandPad + grow;
            float dx = (q.x - (float)h.at.x * (float)l.w) / rx, dy = (q.y - (float)h.at.y * (float)l.h) / ry;
            return dx * dx + dy * dy <= 1;
        }

        // habitat ở tâm bệ; chấm ải xen giữa rải đều trên phần đường giữa hai habitat nằm ngoài vòng đá và khung thân tướng;
        // ải xen giữa đặt đúng trên đường (không so le ra hai bên)
        static LandLay LandLayout(LandDef l, List<StageDef> stages)
        {
            float W = (float)l.w, H = (float)l.h;
            var poly = new List<TrailPt>();
            foreach (var q in l.path)
            {
                var x = new Vector2((float)q.x * W, (float)q.y * H);
                float d = poly.Count == 0 ? 0 : poly[poly.Count - 1].d + Vector2.Distance(x, poly[poly.Count - 1].p);
                poly.Add(new TrailPt { p = x, d = d });
            }
            float len = poly[poly.Count - 1].d;
            int n = Mathf.Max(2, Mathf.FloorToInt(len / 2f));
            var Q = new Vector2[n];
            for (int i = 0; i < n; i++) Q[i] = PointAt(poly, i * 2f);
            var free = Enumerable.Repeat(true, n).ToArray();
            var along = new float[l.habs.Count];
            var span = new List<int>[l.habs.Count]; // đoạn đường ôm vòng đá của từng habitat (chỉ số mẫu)
            for (int k = 0; k < l.habs.Count; k++)
            {
                var h = l.habs[k];
                float cx = (float)h.at.x * W, cy = (float)h.at.y * H;
                float rx = (float)h.ring.x * W + LandPad, ry = (float)h.ring.y * H + LandPad, body = LandHeroH(h.size) * 0.62f;
                float near = Mathf.Max(rx, ry) * 1.6f, best = float.MaxValue;
                // mốc chia cờ: điểm đường gần bệ (road) nếu dữ liệu có, không thì tâm bệ; khớp build_land.py
                float ax = h.HasRoad ? (float)h.road.x * W : cx, ay = h.HasRoad ? (float)h.road.y * H : cy;
                span[k] = new List<int>();
                for (int i = 0; i < n; i++)
                {
                    float dx = Q[i].x - cx, dy = Q[i].y - cy;
                    if (InRing(l, h, Q[i], 0) || Mathf.Abs(dx) < 0.4f * rx && dy < 0 && dy > -body - LandPad) free[i] = false;
                    float ex = Q[i].x - ax, ey = Q[i].y - ay, dd = ex * ex + ey * ey;
                    if (dd <= near * near) span[k].Add(i);
                    if (dd < best)
                    {
                        best = dd;
                        along[k] = i * 2f;
                    }
                }
                // đường xuyên qua tâm bệ (đảo Mộc): điểm mốc giữ ở tâm, không trượt (trượt ra trước bệ thì cờ chặng sau rơi xuống
                // trước bệ, 2026-11-19); khớp build_land.py (near.min() > 0.35·ry)
                if (Mathf.Sqrt(best) <= 0.35f * ry)
                {
                    span[k].Clear();
                    span[k].Add((int)(along[k] / 2f));
                }
            }
            // chia đều (góp ý 2026-11-18): điểm mốc của habitat (trừ ải đầu, cuối) trượt trong đoạn ôm vòng đá, chọn chỗ cho khoảng
            // cách chấm của hai chặng kề nhau lớn nhất có thể (tối đa phần nhỏ hơn), lặp vài lượt
            var pre = new int[n + 1];
            for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + (free[i] ? 1 : 0);
            float FreeLen(float a, float b)
            {
                int i0 = Mathf.Clamp(Mathf.CeilToInt(a / 2f), 0, n), i1 = Mathf.Clamp(Mathf.FloorToInt(b / 2f), -1, n - 1);
                return i1 < i0 ? 0 : (pre[i1 + 1] - pre[i0]) * 2f;
            }
            for (int pass = 0; pass < 4; pass++)
                for (int k = 1; k < l.habs.Count - 1; k++)
                {
                    int n0 = Mathf.Max(1, l.habs[k].stage - l.habs[k - 1].stage - 1), n1 = Mathf.Max(1, l.habs[k + 1].stage - l.habs[k].stage - 1);
                    float pick = along[k], bv = -1;
                    var cand = span[k].Count > 0 ? span[k] : new List<int> { (int)(along[k] / 2f) };
                    for (int ci = 0; ci < cand.Count; ci += 4)
                    {
                        float c = cand[ci] * 2f;
                        if (c <= along[k - 1] || c >= along[k + 1]) continue;
                        float v = Mathf.Min(FreeLen(along[k - 1], c) / n0, FreeLen(c, along[k + 1]) / n1);
                        if (v > bv)
                        {
                            bv = v;
                            pick = c;
                        }
                    }
                    along[k] = pick;
                }
            var lay = new LandLay { pos = new Vector2[stages.Count], at = new float[stages.Count], poly = poly };
            for (int k = 0; k < l.habs.Count; k++)
            {
                var h = l.habs[k];
                int hi = h.stage - 1;
                if (hi < 0 || hi >= stages.Count) continue;
                lay.pos[hi] = new Vector2((float)h.at.x * W, (float)h.at.y * H);
                lay.at[hi] = along[k];
                if (k + 1 >= l.habs.Count) continue;
                int a = h.stage, m = l.habs[k + 1].stage - a - 1;
                if (m <= 0) continue;
                var idx = new List<int>();
                for (int i = 0; i < n; i++)
                    if (free[i] && i * 2f >= along[k] && i * 2f <= along[k + 1]) idx.Add(i);
                if (idx.Count == 0) // không còn chỗ trống: rải thẳng trên đường giữa hai habitat
                    for (int i = 0; i < n; i++)
                        if (i * 2f >= along[k] && i * 2f <= along[k + 1]) idx.Add(i);
                float gap = idx.Count * 2f / m;
                for (int j = 1; j <= m; j++)
                {
                    int qi = idx[Mathf.Clamp((int)((j - 0.5f) * gap / 2f), 0, idx.Count - 1)];
                    int si = a + j - 1;
                    if (si >= stages.Count) continue;
                    lay.pos[si] = Q[qi];
                    lay.at[si] = qi * 2f;
                }
            }
            return lay;
        }

        // ---------- dựng bản đồ ----------

        // vệt đường đã đi, chấm ải xen giữa, habitat; trả chỗ cần đưa vào giữa khung (ải đang đánh)
        Vector2 RenderLand(ZoneDef z, GameData d, SaveData s, List<StageDef> stages, int prog)
        {
            var lay = LandLayout(land, stages);
            landStages = stages;
            int cur = Mathf.Min(prog, stages.Count - 1);
            // đường đi xuyên tâm bệ (đảo Mộc): không vẽ nét đã đi trong lòng vòng đá
            if (prog > 0) DashesAlong(lay.poly, lay.at[0], lay.at[cur], q => land.habs.Any(h => InRing(land, h, q, 12)));
            float pip = (float)land.pip, pipNow = (float)land.pipNow;
            // vùng boss: số vùng đã mở; vùng vừa mở so với lần vào trước (thắng boss quay về) dựng như còn khoá rồi diễn mở (mây tan, bút
            // chì tô); câu báo khi chạm vào vùng khoá (hạ boss của vùng trước)
            bool secs = land.secs.Count > 0;
            int opened = secs ? land.OpenSections(prog) : 99;
            int shown = secs ? Mathf.Min(LandShown.Get(s, zone), opened) : opened;
            int revealK = secs && shown < opened ? opened - 1 : -1;
            if (reveal != null)
            {
                StopCoroutine(reveal);
                LockInput(false);
            }
            reveal = null;
            SetLandOpened(revealK >= 0 ? revealK : opened);
            bool Locked(int idx) => secs && land.SectionOf(idx) >= landOpened;
            string LockMsg(int idx)
            {
                int k = land.SectionOf(idx);
                if (k <= 0 || k > land.habs.Count) return "";
                int bi = land.habs[k - 1].stage;
                var bst = stages[Mathf.Clamp(bi - 1, 0, stages.Count - 1)];
                var boss = d.Hero(Teams.StageLead(bst, d).hero);
                return Loc.F("Hạ {0} ở ải {1} để mở vùng này", (boss != null ? boss.name : "boss"), bi);
            }
            for (int i = 0; i < stages.Count; i++)
            {
                var st = stages[i];
                if (st.tag == StageTag.Hero) continue;
                bool cleared = Progress.StageCleared(s, st), open = Progress.StageOpen(s, st);
                int id = st.id;
                var at = Flip(lay.pos[i]);
                if (flagPrefab)
                {
                    var flag = Ui.Spawn(flagPrefab, p.nodeLayer);
                    int idx = st.idx;
                    string msg = secs ? LockMsg(idx) : null;
                    // xét lúc chạm: vùng có thể vừa mở xong (bút chì tô)
                    Action tap = () =>
                    {
                        if (secs && land.SectionOf(idx) >= landOpened) App.Toasts.Show(msg, Icon("lock"));
                        else StagePrep.Open(id);
                    };
                    flag.Bind(st, open, cleared, open && !cleared, at, tap, pip, pipNow, Locked(idx));
                    landFlags.Add(flag);
                    afkAt[id] = at + new Vector2(0, -pipNow * 0.25f - 30); // dưới ô đá chân cờ
                    continue;
                }
                var pipObj = Ui.Spawn(pipPrefab, p.nodeLayer);
                pipObj.Bind(st, open, cleared, open && !cleared, at, () => StagePrep.Open(id), pip, pipNow, false);
                landPips.Add(pipObj);
                afkAt[id] = at + new Vector2(0, -pipNow * 0.5f - 30);
            }
            // habitat trên cao dựng trước, dưới thấp dựng sau (đè lên)
            bool newOpen = landSeen.TryGetValue(zone, out int seen) && prog > seen;
            foreach (var h in land.habs.OrderBy(x => x.at.y))
            {
                if (h.stage < 1 || h.stage > stages.Count) continue;
                var st = stages[h.stage - 1];
                var en = Teams.StageLead(st, d);
                var hero = d.Hero(en.hero);
                int fs = Teams.EnemyFormStar(en);
                bool cleared = Progress.StageCleared(s, st), open = Progress.StageOpen(s, st), current = open && !cleared;
                var at = Flip(lay.pos[h.stage - 1]);
                float scale = LandHeroH(h.size) / ZoneNode.HeroHeight(st.kind);
                var lh = new LandHero
                {
                    st = st, hero = hero, cleared = cleared, pos = at, scale = scale, bodyH = LandHeroH(h.size) * 0.62f,
                    stand = ZoneNode.HeroHeight(st.kind) * 0.62f, form = hero.Form(d.Cfg.formStars, fs).aola,
                    appear = newOpen && current, locked = Locked(h.stage),
                };
                if (lh.locked) lh.lockMsg = LockMsg(h.stage);
                var node = Ui.Spawn(nodePrefab, p.nodeLayer);
                node.Bind(st, hero, fs, en.level, open, cleared, current, at, h.plate, null, () => TapHabitat(lh), false);
                node.Rect.localScale = Vector3.one * scale;
                if (lh.locked)
                {
                    node.ShowPortraitBody(false); // vùng khoá: tướng nằm dưới mây, không vẽ chân dung tạm, ẩn bảng tên
                    node.ShowPlate(false);
                }
                lh.node = node;
                afkAt[st.id] = NodeTag(st, at, scale);
                if (!string.IsNullOrEmpty(lh.form) && Game.AolaActor.Find(lh.form, out _, out _)) Game.AolaActor.Ready(lh.form);
                else lh.failed = true;
                landHeroes.Add(lh);
            }
            SortByFoot();
            // easter egg dưới mây (ghi chú bút chì, rương bí ẩn), rồi mây phủ các vùng chưa mở (trên cờ, tướng, bảng tên; một hình mây cho
            // mọi đám, gộp lệnh vẽ; chạm được: chọc mây), rồi easter egg trên mây (cảnh rò qua mây, mắt boss)
            if (secs) SpawnEggsUnder(s);
            secClouds = secs ? new List<Image>[land.secs.Count] : null;
            var cloudArt = secs && App.Art ? App.Art.Get(string.IsNullOrEmpty(land.cloud) ? "land_thuy_may_2" : land.cloud) : null;
            if (secs && secPrefab && cloudArt)
                for (int k = landOpened; k < land.secs.Count; k++)
                {
                    var list = secClouds[k] = new List<Image>();
                    var c = land.secs[k].clouds;
                    for (int q = 0; q + 3 < c.Count; q += 4)
                    {
                        var img = Ui.Spawn(eggPrefab ? eggPrefab : secPrefab, CloudParent);
                        img.name = "may_vung_" + k;
                        Theme.SetSprite(img, cloudArt);
                        img.raycastTarget = eggPrefab; // chọc mây (easter egg); kéo bản đồ vẫn được (sự kiện kéo lên LandView)
                        var rt = img.rectTransform;
                        rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
                        rt.pivot = new Vector2(0.5f, 0.5f);
                        float w = (float)c[q + 2] * mapW;
                        rt.sizeDelta = new Vector2(w, w * cloudArt.rect.height / cloudArt.rect.width);
                        rt.anchoredPosition = new Vector2((float)c[q] * mapW, -(float)c[q + 1] * mapH);
                        rt.localScale = new Vector3(c[q + 3] > 0.5 ? -1 : 1, 1, 1);
                        rt.localEulerAngles = Vector3.zero;
                        rt.SetAsLastSibling();
                        list.Add(img);
                        var sc = new SecCloud { img = img, pos = rt.anchoredPosition, scale = rt.localScale, sec = k };
                        eggClouds.Add(sc);
                        var cc = img.GetComponent<ClickCatcher>();
                        if (cc) cc.OnClick = () => PokeCloud(sc);
                    }
                }
            if (secs) SpawnEggsOver();
            cloudHour = -1;
            TintSectionClouds();
            if (revealK >= 0)
            {
                LockInput(true); // bắt xem hết cảnh mở vùng
                reveal = StartCoroutine(RevealSection(revealK, lay));
            }
            OnLandView();
            var focus = Flip(lay.pos[cur]);
            var ch = land.habs.FirstOrDefault(x => x.stage == cur + 1);
            if (ch != null) focus += new Vector2(0, LandHeroH(ch.size) * 0.3f); // ải tướng: đưa cả thân tướng vào giữa
            return focus;
        }

        // cờ và habitat xếp lớp theo chân (y âm xuống): chân thấp hơn (gần người xem) vẽ sau, cờ dưới habitat đè lên tướng,
        // cờ trên habitat nằm sau tướng
        void SortByFoot()
        {
            var items = new List<(Transform t, float y)>();
            foreach (var f in landFlags) items.Add((f.transform, f.Foot.y));
            foreach (var h in landHeroes)
                if (h.node) items.Add((h.node.transform, h.pos.y));
            if (items.Count == 0) return;
            int at = items.Min(x => x.t.GetSiblingIndex());
            foreach (var it in items.OrderByDescending(x => x.y)) it.t.SetSiblingIndex(at++);
        }

        // ---------- camera ----------

        Vector2 ViewSize => ((RectTransform)p.scroll.transform).rect.size;

        // vị trí lớp nội dung để điểm f (khung ảnh, y âm xuống) nằm giữa khung nhìn, kẹp trong vùng đất
        Vector2 LandTarget(Vector2 f)
        {
            var v = ViewSize;
            float x = Mathf.Clamp(-(f.x - v.x * 0.5f), -Mathf.Max(0, mapW - v.x), 0);
            float y = Mathf.Clamp(PadT - f.y - v.y * 0.5f, 0, Mathf.Max(0, p.content.sizeDelta.y - v.y));
            return new Vector2(x, y);
        }

        // vào đảo: ải mới mở thì lướt từ ải trước tới; không thì đặt ở ải đang đánh rồi lướt nhẹ cho thấy là kéo được
        IEnumerator LandToCurrent(Vector2 focus)
        {
            yield return null;
            int prog = App.Save.Data.zones[(int)zone];
            bool fresh = landSeen.TryGetValue(zone, out int seen) && prog > seen;
            landSeen[zone] = prog;
            if (landView && landView.On)
            {
                // vào đảo: zoom vừa phủ kín khung (máy dọc: vừa khít chiều cao đảo), canh ải đang đánh; ải vừa mở thì lướt từ ải trước tới
                if (fresh)
                {
                    var stg = App.Data.ZoneStages(zone).ToList();
                    var lay0 = LandLayout(land, stg);
                    landView.Show(MapPt(Flip(lay0.pos[Mathf.Clamp(seen, 0, stg.Count - 1)])), landView.CoverZoom, 0);
                    landView.Show(MapPt(focus), landView.CoverZoom, 0.9f);
                }
                else landView.Show(MapPt(focus), landView.CoverZoom, 0);
                yield break;
            }
            var to = LandTarget(focus);
            var from = to + new Vector2(-160, 0);
            if (fresh)
            {
                var stages = App.Data.ZoneStages(zone).ToList();
                var lay = LandLayout(land, stages);
                from = LandTarget(Flip(lay.pos[Mathf.Clamp(seen, 0, stages.Count - 1)]));
            }
            p.content.anchoredPosition = from;
            GlideTo(to, fresh ? 0.9f : 0.6f);
        }

        void GlideTo(Vector2 to, float dur)
        {
            if (glide != null) StopCoroutine(glide);
            glide = StartCoroutine(Glide(to, dur));
        }

        IEnumerator Glide(Vector2 to, float dur)
        {
            p.scroll.StopMovement();
            var from = p.content.anchoredPosition;
            for (float t = 0; t < dur; t += Time.unscaledDeltaTime)
            {
                float k = t / dur;
                k = 1 - (1 - k) * (1 - k) * (1 - k); // chậm dần
                p.content.anchoredPosition = Vector2.LerpUnclamped(from, to, k);
                yield return null;
            }
            p.content.anchoredPosition = to;
            glide = null;
        }

        // tour thử (Editor/LandMenu): đưa ải idx (1..) vào giữa khung ngay; false nếu đảo đang mở không phải vùng đất
        public bool LandFocus(int idx, float zoom = 1f)
        {
            if (land == null) return false;
            var stages = App.Data.ZoneStages(zone).ToList();
            var lay = LandLayout(land, stages);
            int i = Mathf.Clamp(idx - 1, 0, stages.Count - 1);
            var f = Flip(lay.pos[i]);
            var hb = land.habs.FirstOrDefault(x => x.stage == idx);
            if (hb != null) f += new Vector2(0, LandHeroH(hb.size) * 0.3f);
            if (landView && landView.On)
            {
                landView.Show(MapPt(f), zoom, 0);
                return true;
            }
            if (glide != null) StopCoroutine(glide);
            glide = null;
            p.scroll.StopMovement();
            p.content.anchoredPosition = LandTarget(f);
            return true;
        }

        // tour thử: trạng thái camera vùng đất
        public string LandDebug() => landView ? landView.Describe() : Loc.T("không có LandView");

        // tour thử: nhìn toàn đảo (zoom nhỏ nhất)
        public bool LandOverview()
        {
            if (!landView || !landView.On) return false;
            landView.ShowAll(0);
            return true;
        }

        // tour thử: tướng của ải idx đánh ngay (không mở hộp chuẩn bị); false nếu hình tướng chưa dựng
        public bool LandAttack(int idx)
        {
            var h = landHeroes.FirstOrDefault(x => x.st.idx == idx);
            if (h?.sticker == null || !h.sticker.HasClip(Attack)) return false;
            h.clip = Attack;
            h.t = 0;
            lastAtk = landClock;
            return true;
        }

        // số vùng boss đã mở (cho shader phác chì, ẩn hiệu ứng, đèn trong vùng khoá); tắt tô màu dở dang
        void SetLandOpened(int n)
        {
            landOpened = n;
            Shader.SetGlobalFloat(OpenedId, n);
            Shader.SetGlobalFloat(RevSecId, -1);
            Shader.SetGlobalFloat(RevNId, 0);
            Shader.SetGlobalFloat(RevFadeId, 0);
            Func<Vector2, bool> hid = null;
            if (land != null && land.secs.Count > 0)
            {
                var l = land;
                hid = q => l.SectionAt(q.x, q.y) >= landOpened;
            }
            if (mapAnim) mapAnim.HideWhere(hid);
            if (dayNight) dayNight.HideLampsWhere(hid);
        }

        // mây phủ xỉn theo giờ như mây đảo (DayCycle.CloudTint); chỉ đổi màu khi giờ đổi
        void TintSectionClouds()
        {
            if (secClouds == null) return;
            float hr = DayCycle.Hour;
            if (Mathf.Abs(hr - cloudHour) < 0.02f) return;
            cloudHour = hr;
            var ct = DayCycle.CloudTint(hr);
            foreach (var list in secClouds)
                if (list != null)
                    foreach (var img in list)
                        if (img) img.color = new Color(ct.r, ct.g, ct.b, img.color.a);
        }

        // mở vùng k: mây tản ra rồi tan, bút chì bay vào ngoáy dọc đường của vùng, màu loang theo nét bút, tô nốt, rồi cờ có màu, tướng
        // cử động
        IEnumerator RevealSection(int k, LandLay lay)
        {
            // màn mây chuyển cảnh mở xong thì nhả lớp chắn (CloudCover.Open): chờ chuyển cảnh xong rồi mới khoá lại
            while (App.Router != null && App.Router.Busy) yield return null;
            LockInput(true);
            yield return new WaitForSecondsRealtime(RevWait);
            var sec = land.secs[k];
            var center = new Vector2((float)(sec.x0 + sec.x1) * 0.5f * mapW, -(float)(sec.y0 + sec.y1) * 0.5f * mapH);
            // đưa cả vùng vào giữa màn (vừa khung, không gần quá 0,8)
            if (landView && landView.On)
            {
                var vs = landView.ViewSize;
                float bw = (float)(sec.x1 - sec.x0) * mapW, bh = (float)(sec.y1 - sec.y0) * mapH;
                float zf = Mathf.Clamp(Mathf.Min(vs.x / bw, vs.y / bh) * 0.92f, landView.MinZoom, 0.8f);
                landView.Show(MapPt(center), zf, 0.6f);
            }
            var clouds = secClouds != null && k < secClouds.Length ? secClouds[k] : null;
            if (clouds != null && clouds.Count > 0)
            {
                var from = clouds.Select(c => c ? c.rectTransform.anchoredPosition : Vector2.zero).ToArray();
                var sc = clouds.Select(c => c ? c.rectTransform.localScale : Vector3.one).ToArray();
                var col = clouds.Select(c => c ? c.color : Color.white).ToArray();
                for (float t = 0; t < CloudGone; t += Time.unscaledDeltaTime)
                {
                    float e = Mathf.SmoothStep(0, 1, t / CloudGone);
                    for (int i = 0; i < clouds.Count; i++)
                    {
                        if (!clouds[i]) continue;
                        var dir = from[i] - center;
                        dir = dir.sqrMagnitude > 1 ? dir.normalized : Vector2.up;
                        var rt = clouds[i].rectTransform;
                        rt.anchoredPosition = from[i] + dir * (300 * e) + Vector2.up * (50 * e);
                        rt.localScale = sc[i] * (1 + 0.3f * e);
                        clouds[i].color = new Color(col[i].r, col[i].g, col[i].b, 1 - e);
                    }
                    FadeSectionEggs(k, e);
                    yield return null;
                }
                foreach (var c in clouds)
                    if (c) c.gameObject.SetActive(false);
                secClouds[k] = null;
            }
            // mây tan: tướng của vùng hiện ra (xám như bản phác) chờ bút chì tô
            foreach (var h in landHeroes)
                if (h.locked && land.SectionOf(h.st.idx) == k)
                {
                    if (h.sticker != null) h.sticker.Rect.gameObject.SetActive(true);
                    if (h.node) h.node.ShowPlate(true);
                }
            // đường ngoáy của bút: dọc đường từ boss trước tới boss vùng này, lệch trái phải xen kẽ, kết thúc ở bệ boss
            int a = k > 0 ? land.habs[k - 1].stage : 1, b = land.habs[k].stage;
            float d0 = lay.at[Mathf.Clamp(a - 1, 0, lay.at.Length - 1)], d1 = lay.at[Mathf.Clamp(b - 1, 0, lay.at.Length - 1)];
            var pts = new List<Vector2>();
            const int N = 16;
            for (int j = 0; j < N; j++)
            {
                float d = Mathf.Lerp(d0, d1, j / (N - 1f));
                var q = PointAt(lay.poly, d);
                var tan = PointAt(lay.poly, d + 24) - PointAt(lay.poly, d - 24);
                var nor = tan.sqrMagnitude > 0 ? new Vector2(-tan.y, tan.x).normalized : Vector2.up;
                float side = (j % 2 == 0 ? 1 : -1) * (j == 0 ? 0.3f : 1);
                pts.Add(q + nor * PenZig * side);
            }
            pts.Add(new Vector2(lay.pos[b - 1].x, lay.pos[b - 1].y));
            int n = Mathf.Min(pts.Count, revealBuf.Length);
            var rad = new float[n];
            Image pen = null;
            if (secPrefab && pencilArt)
            {
                pen = Ui.Spawn(secPrefab, OverParent);
                pen.name = "but_chi";
                Theme.SetSprite(pen, pencilArt);
                pen.raycastTarget = false;
                var prt = pen.rectTransform;
                prt.anchorMin = prt.anchorMax = new Vector2(0, 1);
                prt.pivot = PencilPivot;
                prt.sizeDelta = pencilArt.rect.size * PencilScale;
                prt.localScale = Vector3.one;
                prt.SetAsLastSibling();
            }
            void Push(float fade)
            {
                for (int j = 0; j < revealBuf.Length; j++)
                    revealBuf[j] = j < n ? new Vector4(pts[j].x / mapW, 1 - pts[j].y / mapH, rad[j] / mapW, 0) : Vector4.zero;
                Shader.SetGlobalVectorArray(RevId, revealBuf);
                Shader.SetGlobalFloat(RevNId, n);
                Shader.SetGlobalFloat(RevFadeId, fade);
                Shader.SetGlobalFloat(RevSecId, k);
            }
            for (float t = 0; t < PenTime + 0.35f; t += Time.unscaledDeltaTime)
            {
                float u = Mathf.Clamp01(t / PenTime) * (n - 1);
                int i0 = Mathf.Min((int)u, n - 1);
                var q = Vector2.Lerp(pts[i0], pts[Mathf.Min(i0 + 1, n - 1)], Mathf.SmoothStep(0, 1, u - i0));
                q += new Vector2(Mathf.Sin(t * 31) * 14, Mathf.Cos(t * 27) * 10); // tay ngoáy
                for (int j = 0; j <= i0; j++) rad[j] = Mathf.Min(PenRadius, rad[j] + PenRadius * Time.unscaledDeltaTime / 0.35f);
                if (pen)
                {
                    pen.rectTransform.anchoredPosition = Flip(q);
                    pen.rectTransform.localEulerAngles = new Vector3(0, 0, Mathf.Sin(t * 12) * 6);
                }
                Push(0);
                yield return null;
            }
            // tô nốt phần còn lại của vùng, bút bay đi
            var p0 = pen ? pen.rectTransform.anchoredPosition : Vector2.zero;
            for (float t = 0; t < PenFill; t += Time.unscaledDeltaTime)
            {
                float e = Mathf.SmoothStep(0, 1, t / PenFill);
                Push(e);
                if (pen)
                {
                    pen.rectTransform.anchoredPosition = p0 + new Vector2(260, 220) * e;
                    pen.color = new Color(1, 1, 1, 1 - e);
                }
                yield return null;
            }
            if (pen) Destroy(pen.gameObject);
            SetLandOpened(k + 1);
            // tướng boss của vùng diễn ra sân, cờ mọc lên lần lượt theo đường
            foreach (var h in landHeroes)
                if (h.locked && land.SectionOf(h.st.idx) == k)
                {
                    h.locked = false;
                    h.next = landClock + Random.Range(3f, AtkMax);
                    if (h.sticker != null && h.sticker.HasClip(Appear))
                    {
                        h.clip = Appear;
                        h.t = 0;
                    }
                }
            var flags = landFlags.Where(f => f && land.SectionOf(f.Idx) == k).OrderBy(f => f.Idx).ToList();
            for (int i = 0; i < flags.Count; i++) flags[i].PopIn(0.25f + i * FlagGap);
            yield return new WaitForSecondsRealtime(0.25f + flags.Count * FlagGap + LandFlag.PopTime);
            if (App.Save?.Data != null) LandShown.Set(App.Save.Data, zone, k + 1);
            LockInput(false);
            reveal = null;
        }

        // khoá / mở mọi thao tác chạm (lớp chắn của màn mây chuyển cảnh, phủ trên mọi canvas)
        static void LockInput(bool on)
        {
            if (!inputCover) inputCover = FindAnyObjectByType<CloudCover>(FindObjectsInactive.Include);
            if (inputCover) inputCover.Block(on);
        }

        // chạm habitat: tướng đánh ngay, camera lướt cho habitat vào giữa, rồi mở hộp chuẩn bị; vùng chưa mở thì chỉ báo hạ boss nào
        void TapHabitat(LandHero h)
        {
            if (h.locked)
            {
                App.Toasts.Show(h.lockMsg, Icon("lock"));
                return;
            }
            if (h.sticker != null && h.sticker.HasClip(Attack))
            {
                h.clip = Attack;
                h.t = 0;
                lastAtk = landClock;
            }
            var f = h.pos + new Vector2(0, h.bodyH * 0.5f);
            if (landView && landView.On) landView.Show(MapPt(f), Mathf.Max(landView.Zoom, 0.7f), TapOpen);
            else GlideTo(LandTarget(f), TapOpen);
            StartCoroutine(OpenLater(h.st.id, TapOpen));
        }

        IEnumerator OpenLater(int id, float delay)
        {
            yield return new WaitForSecondsRealtime(delay);
            StagePrep.Open(id);
        }

        // zoom đổi: zoom xa thì cờ ải và bảng tên phóng bù cho còn đọc được, chạm được (tướng giữ cỡ theo bệ)
        void OnLandView()
        {
            if (!landView || !landView.On) return;
            float z = landView.Zoom;
            if (Mathf.Abs(z - appliedZoom) < 0.005f) return;
            appliedZoom = z;
            float kp = Mathf.Clamp(0.5f / z, 1, 1.8f), kn = Mathf.Clamp(0.45f / z, 1, 2f);
            foreach (var pip in landPips)
                if (pip) pip.transform.localScale = Vector3.one * kp;
            foreach (var f in landFlags)
                if (f) f.transform.localScale = Vector3.one * kp; // phóng quanh chân cờ
            foreach (var h in landHeroes)
                if (h.node) h.node.SetPlateZoom(kn);
        }

        // ---------- tướng trên habitat ----------

        // còn trong khung nhìn (cộng lề) không: theo tâm bệ và thân tướng phía trên
        bool InView(LandHero h, float margin)
        {
            if (landView && landView.On)
            {
                var vs = landView.ViewSize;
                var sp = landView.ToView(MapPt(h.pos));
                return sp.x > -margin && sp.x < vs.x + margin && sp.y > -margin && sp.y - h.bodyH * landView.Zoom < vs.y + margin;
            }
            var v = ViewSize;
            var c = p.content.anchoredPosition;
            float left = -c.x, top = c.y;
            float x = h.pos.x, down = PadT - h.pos.y; // khoảng cách từ mép trên lớp nội dung tới tâm bệ
            return x > left - margin && x < left + v.x + margin && down > top - margin && down - h.bodyH < top + v.y + margin;
        }

        void Update()
        {
            // biển lặp quanh đảo tối thêm về đêm (cùng mức biển xa bờ trong ảnh, shader sóng)
            if (land != null && seaScroll) seaScroll.color = Color.Lerp(Color.white, DayCycle.SeaNight, DayCycle.Night(DayCycle.Hour));
            if (land != null)
            {
                TintSectionClouds();
                TickEggs(Mathf.Min(0.05f, Time.unscaledDeltaTime));
            }
            if (land == null || landHeroes.Count == 0) return;
            float dt = Mathf.Min(0.05f, Time.unscaledDeltaTime);
            landClock += dt;
            // zoom xa thì tướng bé trên màn: vẽ thưa khung (2 hay 3 khung một lần, so le giữa các tướng) cho đỡ tốn camera hình tướng
            float zm = landView && landView.On ? landView.Zoom : 1;
            int step = zm >= 0.7f ? 1 : zm >= 0.5f ? 2 : 3, hi = 0;
            foreach (var h in landHeroes)
            {
                hi++;
                if (h.sticker == null) continue;
                if (h.locked || !InView(h, 240))
                {
                    h.sticker.Hold(); // không vẽ lại: ngoài khung nhìn hay đứng yên ở vùng khoá
                    continue;
                }
                h.t += dt * (h.cleared ? 0.75f : 1f);
                if (h.clip != Idle)
                {
                    if (h.t >= h.sticker.Duration(h.clip))
                    {
                        h.clip = Idle;
                        h.t = 0;
                        h.next = landClock + Random.Range(AtkMin, AtkMax);
                    }
                }
                else if (!h.cleared && landClock >= h.next && landClock - lastAtk >= AtkGap && h.sticker.HasClip(Attack))
                {
                    h.clip = Attack;
                    h.t = 0;
                    lastAtk = landClock;
                }
                if (step > 1 && h.clip == Idle && (Time.frameCount + hi) % step != 0)
                {
                    h.sticker.Hold();
                    continue;
                }
                h.sticker.Show(h.clip, h.t, h.clip == Idle, 1, false, 0);
            }
        }

        // dựng hình tướng: mỗi khung tối đa một cái (AolaSticker.CanBuildNow), con trong khung nhìn trước, khi animation đã đọc xong
        void LateUpdate()
        {
            if (land == null || landHeroes.Count == 0 || !AolaSticker.CanBuildNow) return;
            foreach (var h in landHeroes)
            {
                if (h.sticker != null || h.failed || !InView(h, 700)) continue;
                if (!Game.AolaActor.Ready(h.form)) continue;
                h.sticker = AolaSticker.TryCreate(h.node.HeroRect, h.hero, h.form, h.stand * h.scale, false);
                if (h.sticker == null)
                {
                    h.failed = true;
                    continue;
                }
                h.sticker.Rect.localScale = Vector3.one / h.scale;
                h.node.ShowPortraitBody(false);
                if (h.locked)
                {
                    // vùng chưa mở: một khung idle, xám như bản phác, không chạy tiếp (Update bỏ qua tới khi vùng mở)
                    h.clip = Idle;
                    h.t = 0;
                    h.sticker.Show(Idle, 0, true, 1, true, 0);
                    // vùng còn mây phủ: ẩn ảnh tướng (và ảnh hiệu ứng con) cho đỡ lệnh vẽ; hiện khi tung tuyệt kỹ hay khi mây tan
                    int sk = land.SectionOf(h.st.idx);
                    if (secClouds != null && sk < secClouds.Length && secClouds[sk] != null) h.sticker.Rect.gameObject.SetActive(false);
                    return;
                }
                h.t = Random.value * 2;
                h.next = landClock + Random.Range(2f, AtkMax);
                if (h.appear && h.sticker.HasClip(Appear))
                {
                    h.clip = Appear;
                    h.t = 0;
                    h.appear = false;
                }
                h.sticker.Show(h.clip, h.t, h.clip == Idle, 1, false, 0);
                return;
            }
        }
    }
}
