// Lớp sáng tối trên ảnh đảo (sảnh: trên ảnh đảo lớn; màn đảo: trên ảnh bản đồ, dưới đường, chấm ải, tướng), menu
// "PokiClash/Sáng tối/Dựng lớp sáng tối (Zone, Hub)". Theo giờ máy (DayCycle):
// - nhuom: nhân màu cả cảnh (shader PokiClash/UIMultiply): chạng vạng ấm cam, đêm ngả xanh nhẹ (đảo còn sáng); biển tối thêm: sảnh
//   qua seaDark, đảo vùng đất qua shader sóng (_PokiNight, càng xa bờ càng tối) và tấm biển lặp quanh đảo;
//   nhuom tràn rộng ra ngoài ảnh (bleed của menu) để kéo, zoom tới rìa vẫn kín màu: chỉ phủ khung cắt nên nền ngoài khung (sảnh:
//   nen_hai_ben, lộ hai bên trên màn rộng) nhân màu qua seaOutside (người dùng báo 2026-11-18: kéo sảnh ra rìa lộ mép chữ nhật);
// - nang: tia nắng dịu chéo từ góc trên trái, trôi chậm (shader PokiClash/UISunRays, cộng sáng), mạnh nhất giữa ngày, tắt về đêm;
//   đảo, sảnh: RawImage tràn như nhuom, uvRect tính theo khung ảnh nên ra rìa dải nắng chạy tiếp (không lộ chữ nhật sáng);
// - den: đèn ban đêm đọc khoá "lights" của island_anim.json theo đảo: glow (quầng đèn ấm phập phồng), beam (đèn hải đăng quét vòng);
//   hiện dần khi trời tối.
// - clouds: mây của màn (sảnh: vành mây may_vien và mây trôi, cùng hình mây vẽ tay của đảo vùng đất) nhân DayCycle.CloudTint: chiều
//   xỉn, đêm ngả xanh xám như mây đảo vùng đất (IslandAnim), đồng bộ giữa các màn (người dùng dặn 2026-11-18).
// Ảnh nhuom, nang tắt hẳn khi không có tác dụng (giữa trưa không nhuộm, đêm không nắng) để đỡ vẽ cả màn.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class DayNight : MonoBehaviour
    {
        [SerializeField] Image tint;
        [Tooltip("Tia nắng. RawImage (đảo, sảnh): tràn như nhuom, uvRect quy về khung lights (= khung ảnh) nên dải nắng chạy liền ra ngoài ảnh")]
        [SerializeField] Graphic rays;
        [SerializeField] RectTransform lights;
        [SerializeField] Image itemPrefab; // Items/HinhDong
        [SerializeField] TextAsset data;   // Assets/03 Art/Islands/island_anim.json
        [Tooltip("Gắn sẵn khi vào màn (sảnh: world); rỗng thì chờ Bind")]
        [SerializeField] string autoKey;
        [Tooltip("Biển nền tối thêm về đêm (sảnh: bien); biển trong ảnh đảo vùng đất tối theo shader sóng (_PokiNight)")]
        [SerializeField] Graphic[] seaDark;
        [Tooltip("Biển nền nằm ngoài khung cắt của lớp nhuộm (sảnh: nen_hai_ben): tối như seaDark, nhân thêm màu nhuộm")]
        [SerializeField] Graphic[] seaOutside;
        [Tooltip("Mây của màn (sảnh: may_vien, mây trôi): nhân DayCycle.CloudTint như mây đảo vùng đất; menu PokiClash/Sáng tối/Mây sảnh")]
        [SerializeField] Graphic[] clouds;
        Color[] seaBase, outsideBase;

        struct Lamp
        {
            public Image img;
            public Vector2 at;
            public float size;
            public bool beam;
            public int seed;
        }

        readonly List<Lamp> lamps = new List<Lamp>();
        Func<Vector2, bool> lampHidden; // đảo vùng đất: đèn trong vùng boss chưa mở tắt (vùng vẽ phác chì)

        // tắt đèn ở chỗ hidden(at) trả true (at: tỉ lệ ảnh, y từ trên); null: bật hết
        public void HideLampsWhere(Func<Vector2, bool> hidden)
        {
            lampHidden = hidden;
            Tick();
        }
        Dictionary<string, object> root;
        float clock;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Image tintImg, Graphic raysImg, RectTransform lightLayer, Image item, TextAsset json, string key, Graphic[] seas = null,
            Graphic[] outside = null)
        {
            seaDark = seas ?? new Graphic[0];
            seaOutside = outside ?? new Graphic[0];
            tint = tintImg;
            rays = raysImg;
            lights = lightLayer;
            itemPrefab = item;
            data = json;
            autoKey = key;
        }

        void Start()
        {
            if (!string.IsNullOrEmpty(autoKey)) Bind(autoKey);
            Tick();
        }

        public void Bind(string key)
        {
            if (lights)
                for (int i = lights.childCount - 1; i >= 0; i--) Destroy(lights.GetChild(i).gameObject);
            lamps.Clear();
            if (!data || !itemPrefab || !lights || !App.Art) return;
            root ??= J.Obj(MiniJson.Parse(data.text));
            var entry = J.Obj(root, key);
            if (entry == null) return;
            int seed = 0;
            foreach (var o in J.Arr(entry, "lights"))
            {
                var it = J.Obj(o);
                bool beam = J.Str(it, "k") == "beam";
                var img = Ui.Spawn(itemPrefab, lights);
                img.name = beam ? "den_quet" : "den";
                Theme.SetSprite(img, App.Art.Get(beam ? "anim_beam" : "anim_glow"));
                img.raycastTarget = false;
                lamps.Add(new Lamp { img = img, at = new Vector2((float)J.Num(it, "x"), (float)J.Num(it, "y")), size = (float)J.Num(it, "s"), beam = beam, seed = seed++ });
            }
            Tick();
        }

        // nhân màu k lên màu gốc (lấy lần đầu) của các ảnh biển nền
        static void Darken(Graphic[] gs, ref Color[] bases, Color k)
        {
            if (gs == null || gs.Length == 0) return;
            if (bases == null || bases.Length != gs.Length)
            {
                bases = new Color[gs.Length];
                for (int i = 0; i < gs.Length; i++) bases[i] = gs[i] ? gs[i].color : Color.white;
            }
            for (int i = 0; i < gs.Length; i++)
                if (gs[i]) gs[i].color = bases[i] * k;
        }

        void Update()
        {
            clock += Mathf.Min(Time.unscaledDeltaTime, 0.1f);
            Tick();
        }

        void Tick()
        {
            float h = DayCycle.Hour, night = DayCycle.Night(h), sun = DayCycle.Sun(h);
            Shader.SetGlobalFloat("_PokiNight", night); // shader sóng tối biển xa bờ về đêm
            var seaK = Color.Lerp(Color.white, DayCycle.SeaNight, night);
            var tintC = DayCycle.Tint(h);
            Darken(seaDark, ref seaBase, seaK);
            Darken(seaOutside, ref outsideBase, seaK * tintC);
            if (clouds != null && clouds.Length > 0)
            {
                var ct = DayCycle.CloudTint(h);
                foreach (var g in clouds)
                    if (g) g.color = new Color(ct.r, ct.g, ct.b, g.color.a);
            }
            if (tint)
            {
                bool on = tintC.r < 0.995f || tintC.g < 0.995f || tintC.b < 0.995f;
                tint.enabled = on;
                if (on) tint.color = tintC;
            }
            if (rays)
            {
                // ban ngày nắng vàng nhạt; chạng vạng chỉ còn chút nắng cam xiên (người dùng 2026-11-18: chiều tối giảm ánh nắng)
                float dusk = DayCycle.Dusk(h) * (1 - night);
                float k = Mathf.Max(sun, dusk * 0.3f);
                bool on = k > 0.01f;
                rays.enabled = on;
                if (on) rays.color = new Color(1, Mathf.Lerp(1, 0.66f, dusk), Mathf.Lerp(1, 0.42f, dusk), k);
                // uv 0..1 trùng khung ảnh (lights), phần tràn ra ngoài có uv ngoài 0..1: shader tính dải theo uv nên không lộ mép
                if (on && rays is RawImage ri && lights)
                {
                    Rect rr = ri.rectTransform.rect, lr = lights.rect;
                    if (lr.width > 1 && lr.height > 1)
                        ri.uvRect = new Rect((rr.xMin - lr.xMin) / lr.width, (rr.yMin - lr.yMin) / lr.height, rr.width / lr.width, rr.height / lr.height);
                }
            }
            if (!lights) return;
            var r = lights.rect;
            foreach (var l in lamps)
            {
                if (lampHidden != null && lampHidden(l.at))
                {
                    l.img.enabled = false;
                    continue;
                }
                float w = l.size * r.width;
                var rt = l.img.rectTransform;
                rt.anchorMin = rt.anchorMax = Vector2.zero;
                var sp = l.img.sprite;
                float hh = sp ? w * sp.rect.height / sp.rect.width : w;
                rt.sizeDelta = new Vector2(w, hh);
                rt.anchoredPosition = new Vector2(l.at.x * r.width, (1 - l.at.y) * r.height);
                float a;
                if (l.beam)
                {
                    rt.pivot = new Vector2(0, 0.5f); // gốc chùm sáng ở đèn
                    rt.localEulerAngles = new Vector3(0, 0, clock * 40f);
                    a = night * 0.55f;
                }
                else
                {
                    rt.pivot = new Vector2(0.5f, 0.5f);
                    float k = 1 + Mathf.Sin(clock * 2.1f + l.seed * 1.3f) * 0.08f;
                    rt.localScale = new Vector3(k, k, 1);
                    a = night * (0.75f + 0.25f * Mathf.Sin(clock * 3.3f + l.seed));
                }
                l.img.enabled = a > 0.01f;
                l.img.color = new Color(1, 1, 1, a);
            }
        }
    }
}
