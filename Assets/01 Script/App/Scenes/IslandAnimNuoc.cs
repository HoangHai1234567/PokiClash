// Nước động bản đồ sảnh (người dùng 2026-11-23: "các phần nước suối này vẫn hơi tĩnh, học hỏi Kingdom Rush 5 ... làm nước động hơn";
// ArtGen/Islands/sanh_moi/nuoc_dong.py ghi khoá world_map của island_anim.json). Phần của IslandAnim:
// - "flows": ảnh phủ nước từng đảo (sanh_nuoc_<đảo>, material Resources/sanh_nuoc_<đảo> shader PokiClash/UIFlowWater): con của gốc đảo
//   "dao_<đảo>" (anh em của lớp phần động) nên nhún cùng đảo khi bấm; không thấy gốc đảo thì nằm trong lớp này. Vệt bọt sông trôi xuôi,
//   vệt thác trôi xuống do shader vẽ;
// - "splash": bọt cuộn chân thác (KR5 stage_2_props_waterfall_splash): múi bọt nở ra, bốc lên, tan, nối nhau;
// - "rings": vòng gợn toả ra quanh chân thác (KR5 Stage_1_decos_waterfall_ripples), nở dần rồi mờ;
// - "glint": đốm lấp lánh mặt biển (KR5 WaterSparks): đổi hình theo nhịp, hiện một lúc rồi tắt, mỗi lần lệch chỗ.
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed partial class IslandAnim
    {
        readonly List<GameObject> flowObjs = new List<GameObject>();

        void ClearFlows()
        {
            foreach (var o in flowObjs)
                if (o) Destroy(o);
            flowObjs.Clear();
        }

        void BindFlows(Dictionary<string, object> entry)
        {
            ClearFlows();
            foreach (var o in J.Arr(entry, "flows"))
            {
                var f = J.Obj(o);
                string zone = J.Str(f, "zone");
                var sprite = App.Art.Get(J.Str(f, "sprite"));
                var mat = Resources.Load<Material>("sanh_nuoc_" + zone);
                if (!sprite || !mat) continue;
                var r = Rect4(J.Arr(f, "rect"));
                var box = Rect4(J.Arr(f, "box"));
                // gốc đảo dao_<đảo> (anh em của lớp này, HubMapMenu dựng): toạ độ neo tính theo khung ảnh đảo
                Transform parent = transform;
                var island = transform.parent ? transform.parent.Find("dao_" + zone) : null;
                Vector4 frame = new Vector4(0, 0, 1, 1);
                if (island && box.z > box.x)
                {
                    parent = island;
                    frame = box;
                }
                var img = Ui.Spawn(itemPrefab, parent); // Items/HinhDong (luật dự án: mã chạy không tự dựng GameObject)
                img.name = "nuoc_" + zone;
                var go = img.gameObject;
                var rt = img.rectTransform;
                rt.pivot = new Vector2(0.5f, 0.5f);
                rt.localEulerAngles = Vector3.zero;
                float fw = frame.z - frame.x, fh = frame.w - frame.y;
                rt.anchorMin = new Vector2((r.x - frame.x) / fw, 1 - (r.w - frame.y) / fh);
                rt.anchorMax = new Vector2((r.z - frame.x) / fw, 1 - (r.y - frame.y) / fh);
                rt.offsetMin = rt.offsetMax = Vector2.zero;
                rt.localScale = Vector3.one;
                var hinh = island ? island.Find("hinh") : null;
                if (hinh) rt.SetSiblingIndex(hinh.GetSiblingIndex() + 1);
                img.type = Image.Type.Simple;
                img.color = Color.white;
                img.sprite = sprite; // không qua Theme.SetSprite: giữ material nước
                img.material = mat;
                img.raycastTarget = false;
                flowObjs.Add(go);
            }
        }

        static Vector4 Rect4(List<object> a) => a != null && a.Count >= 4
            ? new Vector4(System.Convert.ToSingle(a[0]), System.Convert.ToSingle(a[1]), System.Convert.ToSingle(a[2]), System.Convert.ToSingle(a[3]))
            : Vector4.zero;

        void OnDestroy() => ClearFlows();

        // kiểu động thêm (không có trong switch chính): nước sảnh ở đây, easter egg sảnh (e_*) ở IslandAnimTrung.cs
        void AddMore(string k, Vector2 p, float s, int seed, Dictionary<string, object> it)
        {
            if (AddEgg(k, p, s, seed, it)) return;
            switch (k)
            {
                case "splash":
                    {
                        var puffs = new Sprite[] { SpriteOf("bot_1"), SpriteOf("bot_2"), SpriteOf("bot_3") };
                        fx.Add(new Splash { host = this, at = p, size = s, seed = seed, items = NewImages("bot_1", 5), puffs = puffs });
                        break;
                    }
                case "rings": fx.Add(new Rings { host = this, at = p, size = s, seed = seed, items = NewImages("vong", 2) }); break;
                case "glint":
                    fx.Add(new Glint
                    {
                        host = this, at = p, size = s, seed = seed, img = NewImage("lap_1"),
                        frames = new Sprite[] { SpriteOf("lap_1"), SpriteOf("lap_2"), SpriteOf("lap_3") },
                    });
                    break;
            }
        }

        // bọt cuộn chân thác: các múi nối nhau, mỗi múi 1,1 s: bật ra ở chân thác (lệch trái phải trong bề ngang thác), nở nhanh rồi chậm,
        // bốc lên một chút; giữ đục suốt đời rồi tan bằng co lại (KR5: bọt, khói tách cụm rồi mới mất; mờ dần cả đời thì trông như bong
        // bóng trong suốt); đổi hình múi mỗi lượt
        sealed class Splash : Fx
        {
            public Vector2 at;
            public float size;
            public int seed;
            public Image[] items;
            public Sprite[] puffs;
            public override void Tick(float t)
            {
                float w = host.S(size);
                var p0 = host.P(at);
                const float life = 1.1f;
                int n = items.Length;
                for (int i = 0; i < n; i++)
                {
                    float o = (float)i / n * life;
                    float age = Mathf.Repeat(t + o, life);
                    int gen = Mathf.FloorToInt((t + o) / life);
                    float k = age / life;
                    float r = Hash(seed, gen * 17 + i);
                    var img = items[i];
                    var sp = puffs[(gen + i) % puffs.Length];
                    if (sp && img.sprite != sp) img.sprite = sp;
                    float e = 1 - (1 - k) * (1 - k);
                    float shrink = k > 0.7f ? 1 - (k - 0.7f) / 0.3f * 0.75f : 1;
                    float sc = (0.5f + 0.55f * e) * (0.8f + 0.4f * r) * shrink;
                    float a = k < 0.08f ? k / 0.08f : k > 0.88f ? (1 - k) / 0.12f : 1;
                    var pos = p0 + new Vector2((r - 0.5f) * w * 1.1f + (r - 0.5f) * w * 0.3f * e, e * w * 0.45f - w * 0.1f);
                    Place(img, pos, w, a, (r - 0.5f) * 40 + k * 25 * (r < 0.5f ? -1 : 1), new Vector3(r < 0.5f ? -sc : sc, sc, 1));
                }
            }
        }

        // vòng gợn: hai vòng so le, nở 0,5 → 1,2 trong 1,8 s, mờ dần (nhạt: nằm dưới bọt, chỉ gợi mặt nước động)
        sealed class Rings : Fx
        {
            public Vector2 at;
            public float size;
            public int seed;
            public Image[] items;
            public override void Tick(float t)
            {
                float w = host.S(size);
                var p0 = host.P(at);
                const float life = 1.8f;
                for (int i = 0; i < items.Length; i++)
                {
                    float age = Mathf.Repeat(t + (float)i / items.Length * life + Hash(seed, 0) * life, life);
                    float k = age / life;
                    float sc = 0.5f + 0.7f * (1 - (1 - k) * (1 - k));
                    float a = (k < 0.15f ? k / 0.15f : 1 - (k - 0.15f) / 0.85f) * 0.6f;
                    Place(items[i], p0, w, a, 0, new Vector3(sc, sc, 1));
                }
            }
        }

        // đốm lấp lánh: bật 1,1–1,6 s (đổi hình mỗi 0,16 s), tắt 1,4–3 s, mỗi lượt lệch chỗ
        sealed class Glint : Fx
        {
            public Vector2 at;
            public float size;
            public int seed;
            public Image img;
            public Sprite[] frames;
            public override void Tick(float t)
            {
                float on = 1.1f + Hash(seed, 1) * 0.5f, period = on + 1.4f + Hash(seed, 2) * 1.6f;
                float tt = t + Hash(seed, 3) * period;
                int n = Mathf.FloorToInt(tt / period);
                float ph = tt - n * period;
                float w = host.S(size);
                if (ph > on)
                {
                    var c = img.color;
                    if (c.a != 0)
                    {
                        c.a = 0;
                        img.color = c;
                    }
                    return;
                }
                var sp = frames[Mathf.FloorToInt(ph / 0.16f + seed) % frames.Length];
                if (sp && img.sprite != sp) img.sprite = sp;
                float a = Mathf.Min(1, Mathf.Min(ph / 0.15f, (on - ph) / 0.3f));
                var off = new Vector2(Hash(seed, n * 7) - 0.5f, Hash(seed, n * 7 + 3) - 0.5f) * new Vector2(w * 1.6f, w * 0.6f);
                Place(img, host.P(at) + off, w, a);
            }
        }
    }
}
