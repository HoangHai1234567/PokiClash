// Bản đồ thế giới ở sảnh (người dùng 2026-11-19; ArtGen/Islands/sanh_moi/build_sanh.py ghi world_map.png, hub_map.json và khoá
// world_map của island_anim.json). Menu "PokiClash/Prefab/Sảnh bản đồ thế giới (mây, điểm bấm)" sửa Screens/Hub:
// - ảnh "dao" thành world_map, cỡ hub_map.view (rộng hơn khung 1080 x 1920 cả hai chiều), giữa khung; HubPan kéo được 4 hướng tới mép
//   ảnh; nền ngoài ảnh (biển, hai bên) thành màu giấy như vành mây vẽ sẵn của ảnh; tắt vành mây cũ "may_vien";
// - phần động "dong" (IslandAnim) và đèn đêm (DayNight) đọc khoá world_map;
// - năm bảng vùng (HubZone) đặt ở mốc lớn của từng đảo (realms[].at), con của ảnh bản đồ;
// - lớp "suong_mu" (HubFog) trên bảng vùng: mỗi đảo một nhóm mây (realms[].clouds), mỗi đám Image + ClickCatcher;
// - tắt làng máy bi; công trình side meta (Nhà, Đền Huy Hiệu, Hang Tiềm Năng, Cây bi) ra cột nút cố định bên phải, trên hàng nút đáy.
// Chạy lại được. Thêm đảo: sửa build_sanh.py (REALMS), chạy lại script rồi menu này.
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HubMapMenu
    {
        const string HubPath = "Assets/04 Prefabs/Screens/Hub.prefab";
        const string ArtDir = "Assets/03 Art/Islands/";
        const string MapJson = ArtDir + "hub_map.json";
        const string AnimJson = ArtDir + "island_anim.json";
        const string ItemPath = "Assets/04 Prefabs/Items/HinhDong.prefab";
        const float FW = 1080, FH = 1920;
        static readonly Color Paper = new Color(0.992f, 0.961f, 0.906f); // #fdf5e7, giấy quanh vành mây vẽ sẵn

        // cột thẻ giấy công trình: thẻ boot_giay_ghi (như hàng nút đáy), icon to, tên dưới, băng keo màu, chấm báo góc trên phải.
        // Dựng lại các HubBuilding mới (giữ icon, chấm báo của cái cũ), gán vào HubScene.buildings theo thứ tự cũ.
        static void SideColumn(RectTransform parent, SerializedProperty bs)
        {
            var assets = AssetDatabase.LoadAssetAtPath<UiAssets>(AssetDatabase.GUIDToAssetPath(AssetDatabase.FindAssets("t:UiAssets")[0]));
            Theme.Init(assets);
            var card = AssetDatabase.LoadAssetAtPath<Sprite>("Assets/03 Art/Boot/boot_giay_ghi.png");
            var tape = AssetDatabase.LoadAssetAtPath<Sprite>(UiRefreshMenu.TapePath);
            var old = parent.Find("cot_cong_trinh");
            var keep = new List<(Sprite icon, RectTransform dot)>();
            for (int i = 0; i < bs.arraySize; i++)
            {
                var b = bs.GetArrayElementAtIndex(i).objectReferenceValue as HubBuilding;
                if (!b)
                {
                    keep.Add((null, null));
                    continue;
                }
                var bso = new SerializedObject(b);
                var ic = bso.FindProperty("icon").objectReferenceValue as Image;
                var dot = bso.FindProperty("dot").objectReferenceValue as Image;
                keep.Add((ic ? ic.sprite : null, dot ? dot.rectTransform : null));
            }
            var col = new GameObject("cot_cong_trinh_moi", typeof(RectTransform)).GetComponent<RectTransform>();
            col.SetParent(parent, false);
            col.anchorMin = col.anchorMax = new Vector2(1, 1);
            col.pivot = new Vector2(1, 1);
            col.sizeDelta = new Vector2(150, 4 * 150);
            col.anchoredPosition = new Vector2(-12, -(SceneRoot.BarHeight + 24));
            const float C = 132, Gap = 14;
            var tapes = new[] { Theme.TapeGreen, Theme.TapeYellow, Theme.TapeBlue, Theme.TapePink };
            for (int i = 0; i < bs.arraySize; i++)
            {
                var slot = new GameObject("the_" + HubScene.Buildings[i].name, typeof(RectTransform)).GetComponent<RectTransform>();
                slot.SetParent(col, false);
                slot.anchorMin = slot.anchorMax = new Vector2(0.5f, 1);
                slot.pivot = new Vector2(0.5f, 1);
                slot.sizeDelta = new Vector2(C, C);
                slot.anchoredPosition = new Vector2(0, -i * (C + Gap));
                slot.localEulerAngles = new Vector3(0, 0, i % 2 == 0 ? 2f : -2f);
                var bg = NewImg(slot, "nen", card, Theme.CardFill, true);
                bg.type = Image.Type.Sliced;
                Stretch(bg.rectTransform);
                var click = bg.gameObject.AddComponent<ClickCatcher>();
                var icon = NewImg(bg.transform, "icon", keep[i].icon, Color.white, false);
                icon.preserveAspect = true;
                icon.rectTransform.anchorMin = icon.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
                icon.rectTransform.anchoredPosition = new Vector2(0, 14);
                icon.rectTransform.sizeDelta = new Vector2(70, 70);
                var label = new GameObject("chu", typeof(RectTransform), typeof(CanvasRenderer), typeof(TextMeshProUGUI)).GetComponent<TextMeshProUGUI>();
                label.transform.SetParent(bg.transform, false);
                label.font = Theme.Bold;
                label.fontSize = 22;
                label.enableAutoSizing = true;
                label.fontSizeMin = 14;
                label.fontSizeMax = 22;
                label.alignment = TextAlignmentOptions.Center;
                label.color = Theme.Ink;
                label.raycastTarget = false;
                label.rectTransform.anchorMin = label.rectTransform.anchorMax = new Vector2(0.5f, 0);
                label.rectTransform.anchoredPosition = new Vector2(0, 24);
                label.rectTransform.sizeDelta = new Vector2(C - 14, 32);
                label.text = HubScene.Buildings[i].name;
                var t = NewImg(slot, "bang_keo", tape, tapes[i % tapes.Length], false);
                t.rectTransform.anchorMin = t.rectTransform.anchorMax = new Vector2(0.5f, 1);
                t.rectTransform.anchoredPosition = new Vector2(0, 2);
                t.rectTransform.sizeDelta = new Vector2(70, 24);
                t.rectTransform.localEulerAngles = new Vector3(0, 0, -6);
                // chấm báo: dựng mới theo hình, màu, cỡ của chấm cũ (chấm cũ nằm trong prefab lồng, không dời ra được)
                var oldDot = keep[i].dot ? keep[i].dot.GetComponent<Image>() : null;
                var dotImg = NewImg(slot, "cham", oldDot ? oldDot.sprite : null, oldDot ? oldDot.color : new Color(0.9f, 0.25f, 0.2f), false);
                dotImg.rectTransform.anchorMin = dotImg.rectTransform.anchorMax = new Vector2(1, 1);
                dotImg.rectTransform.anchoredPosition = new Vector2(-12, -12);
                dotImg.rectTransform.sizeDelta = oldDot ? oldDot.rectTransform.sizeDelta : new Vector2(30, 30);
                var hb = slot.gameObject.AddComponent<HubBuilding>();
                hb.Setup(bg, icon, label, dotImg, click);
                bs.GetArrayElementAtIndex(i).objectReferenceValue = hb;
            }
            if (old) Object.DestroyImmediate(old.gameObject);
            col.name = "cot_cong_trinh";
            col.SetAsLastSibling();
            // các công trình cũ trên đảo (làng, cong_trinh, cay_bi): xoá nếu còn sót
            foreach (var t in parent.root.GetComponentsInChildren<HubBuilding>(true))
                if (!t.transform.IsChildOf(col))
                    Object.DestroyImmediate(t.gameObject);
        }

        static Image NewImg(Transform parent, string name, Sprite s, Color c, bool raycast)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
            go.layer = LayerMask.NameToLayer("UI");
            go.transform.SetParent(parent, false);
            var img = go.GetComponent<Image>();
            Theme.SetSprite(img, s);
            img.color = c;
            img.raycastTarget = raycast;
            return img;
        }

        static void Stretch(RectTransform rt)
        {
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
        }

        [MenuItem("PokiClash/Prefab/Sảnh bản đồ thế giới (mây, điểm bấm)", priority = 63)]
        static void Build()
        {
            foreach (var n in new[] { "sanh_bien", "sanh_dao_thuy", "sanh_dao_hoa", "sanh_dao_kim", "sanh_dao_moc", "sanh_dao_tho" })
                AssetDatabase.ImportAsset(ArtDir + n + ".png", ImportAssetOptions.ForceUpdate);
            AssetDatabase.ImportAsset(MapJson, ImportAssetOptions.ForceUpdate);
            AssetDatabase.ImportAsset(AnimJson, ImportAssetOptions.ForceUpdate);
            ArtImporter.BuildLibrary();
            var json = AssetDatabase.LoadAssetAtPath<TextAsset>(MapJson);
            var anim = AssetDatabase.LoadAssetAtPath<TextAsset>(AnimJson);
            var map = AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + "world_map.png");
            var item = AssetDatabase.LoadAssetAtPath<GameObject>(ItemPath)?.GetComponent<Image>();
            if (!json || !anim || !item)
            {
                Debug.LogError("[Sảnh] Thiếu world_map.png / hub_map.json / island_anim.json / Items/HinhDong: chạy ArtGen/Islands/sanh_moi/build_sanh.py");
                return;
            }
            var root = J.Obj(MiniJson.Parse(json.text));
            var view = J.Arr(root, "view");
            float vw = System.Convert.ToSingle(view[0]), vh = System.Convert.ToSingle(view[1]);
            var cloud = AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + J.Str(root, "cloud") + ".png");
            var contents = PrefabUtility.LoadPrefabContents(HubPath);
            try
            {
                RectTransform Find(string n) => contents.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == n);
                var scene = contents.GetComponentInChildren<HubScene>(true);
                var so = new SerializedObject(scene);
                var khung = Find("khung_anh");
                var dao = Find("dao");
                if (!dao || !khung)
                {
                    Debug.LogError("[Sảnh] Không thấy khung_anh / dao trong Hub: chạy menu Đảo sảnh: ghép ảnh, kéo, mây viền trước");
                    return;
                }
                // ảnh bản đồ: giữa khung, rộng hơn khung
                float mx = (vw - FW) / 2 / FW, my = (vh - FH) / 2 / FH;
                dao.anchorMin = new Vector2(-mx, -my);
                dao.anchorMax = new Vector2(1 + mx, 1 + my);
                dao.pivot = new Vector2(0.5f, 0.5f);
                dao.offsetMin = dao.offsetMax = Vector2.zero;
                var daoImg = dao.GetComponent<Image>();
                // tách từng đảo (người dùng 2026-11-19: "tách từng đảo 1 ra rồi xếp chúng lại", "drag ra rìa vẫn phải thấy mây và nước"):
                // ảnh dao chỉ còn nhận kéo (trong suốt); biển lát rộng ra ngoài mép, các đảo là ảnh riêng xếp đúng chỗ (khoá "islands")
                daoImg.sprite = null;
                daoImg.color = new Color(1, 1, 1, 0);
                daoImg.raycastTarget = true; // chỗ trống nhận kéo
                foreach (var n in new[] { "bien_lat" })
                {
                    var o = dao.Find(n);
                    if (o) Object.DestroyImmediate(o.gameObject);
                }
                for (int i = dao.childCount - 1; i >= 0; i--)
                    if (dao.GetChild(i).name.StartsWith("dao_"))
                        Object.DestroyImmediate(dao.GetChild(i).gameObject);
                var seaSpr = AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + J.Str(root, "sea", "sanh_bien") + ".png");
                var seaGo = new GameObject("bien_lat", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                var seaRt = (RectTransform)seaGo.transform;
                seaRt.SetParent(dao, false);
                seaRt.anchorMin = Vector2.zero;
                seaRt.anchorMax = Vector2.one;
                seaRt.offsetMin = -Vector2.one * 2400; // kéo quá rìa (dây chun) vẫn là biển
                seaRt.offsetMax = Vector2.one * 2400;
                seaRt.SetSiblingIndex(0);
                var seaImg = seaGo.GetComponent<Image>();
                seaImg.sprite = seaSpr;
                seaImg.type = Image.Type.Tiled;
                seaImg.raycastTarget = false;
                int isl = 0;
                var arts = new List<HubIslandArt>();
                foreach (var o in J.Arr(root, "islands"))
                {
                    var it = J.Obj(o);
                    var rc = J.Arr(it, "rect");
                    float u0 = System.Convert.ToSingle(rc[0]), v0 = System.Convert.ToSingle(rc[1]);
                    float u1 = System.Convert.ToSingle(rc[2]), v1 = System.Convert.ToSingle(rc[3]);
                    string sprName = J.Str(it, "sprite");
                    var spr = AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + sprName + ".png");
                    // gốc "dao_<hệ>": phủ khung ảnh đảo, gốc ở chân đảo (nhún quanh chân); con "hinh" (ảnh đảo). Quầng sáng thở cả ngày
                    // (2026-11-19) đã bỏ (người dùng 2026-11-20): đèn đêm (đuốc, chỗ phát sáng) dựng ở lớp den_dao (HubNightMenu)
                    var box = new GameObject("dao_" + J.Str(it, "zone"), typeof(RectTransform)).GetComponent<RectTransform>();
                    box.SetParent(dao, false);
                    box.anchorMin = new Vector2(u0, 1 - v1);
                    box.anchorMax = new Vector2(u1, 1 - v0);
                    box.offsetMin = box.offsetMax = Vector2.zero;
                    box.pivot = new Vector2(0.5f, 0.18f);
                    box.offsetMin = box.offsetMax = Vector2.zero;
                    box.SetSiblingIndex(1 + isl++);
                    var go = new GameObject("hinh", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                    var rt = (RectTransform)go.transform;
                    rt.SetParent(box, false);
                    rt.anchorMin = Vector2.zero;
                    rt.anchorMax = Vector2.one;
                    rt.offsetMin = rt.offsetMax = Vector2.zero;
                    var img = go.GetComponent<Image>();
                    img.sprite = spr;
                    img.raycastTarget = true; // bấm theo hình đảo (HubIslandArt lọc bằng mặt nạ)
                    if (!spr) Debug.LogError("[Sảnh] Thiếu ảnh đảo " + sprName + ": chạy ArtGen/Islands/sanh_moi/build_sanh.py");
                    // mặt nạ bấm thô từ ảnh đảo (đọc file, không cần bật đọc texture)
                    const int MW = 96;
                    int mw = MW, mh = MW;
                    byte[] bits = new byte[0];
                    var path = System.IO.Path.Combine(Application.dataPath, "..", ArtDir + sprName + ".png");
                    if (System.IO.File.Exists(path))
                    {
                        var tex = new Texture2D(2, 2);
                        tex.LoadImage(System.IO.File.ReadAllBytes(path));
                        mh = Mathf.Max(1, Mathf.RoundToInt(MW * (float)tex.height / tex.width));
                        bits = new byte[mw * mh];
                        for (int y = 0; y < mh; y++)
                            for (int x = 0; x < mw; x++)
                            {
                                var c = tex.GetPixelBilinear((x + 0.5f) / mw, 1 - (y + 0.5f) / mh);
                                bits[y * mw + x] = (byte)(c.a > 0.5f ? 1 : 0);
                            }
                        Object.DestroyImmediate(tex);
                    }
                    var art = go.AddComponent<HubIslandArt>();
                    art.Setup(Keys.ToElem(J.Str(it, "zone")), box, mw, mh, bits);
                    arts.Add(art);
                }
                scene.SetupIslands(arts.ToArray());
                var dong = dao.GetComponentInChildren<IslandAnim>(true);
                if (dong) dong.Setup(anim, "world_map", item);
                foreach (var n in new[] { "bien", "nen_hai_ben" })
                {
                    var r = Find(n);
                    if (!r) continue;
                    var img = r.GetComponent<Image>();
                    img.sprite = null;
                    img.type = Image.Type.Simple;
                    img.color = Paper;
                }
                var ring = Find("may_vien");
                if (ring) ring.gameObject.SetActive(false);
                var pan = khung.GetComponent<HubPan>();
                // kéo được ra quá mép đảo một đoạn: rìa luôn thấy biển và mây (người dùng 2026-11-19)
                const float EdgeX = 300, EdgeY = 220;
                pan.Setup(Find("keo"), new Vector2(mx + EdgeX / FW, my + EdgeY / FH));

                // đèn đêm đọc khoá world_map; lớp đèn phủ đúng ảnh bản đồ
                var dn = contents.GetComponentInChildren<DayNight>(true);
                if (dn)
                {
                    var dso = new SerializedObject(dn);
                    dso.FindProperty("autoKey").stringValue = "world_map";
                    var sd = dso.FindProperty("seaDark");
                    var seaG = dao.Find("bien_lat") ? dao.Find("bien_lat").GetComponent<Graphic>() : null;
                    if (seaG)
                    {
                        sd.arraySize = 1;
                        sd.GetArrayElementAtIndex(0).objectReferenceValue = seaG;
                    }
                    var lights = dso.FindProperty("lights").objectReferenceValue as RectTransform;
                    if (lights)
                    {
                        // lớp đèn thành con của ảnh bản đồ (toạ độ đèn tỉ lệ theo ảnh), ngay trên phần động
                        lights.SetParent(dao, false);
                        lights.anchorMin = Vector2.zero;
                        lights.anchorMax = Vector2.one;
                        lights.offsetMin = lights.offsetMax = Vector2.zero;
                        var dongRt = dao.Find("dong");
                        lights.SetSiblingIndex(dongRt ? dongRt.GetSiblingIndex() + 1 : 0);
                    }
                    dso.ApplyModifiedPropertiesWithoutUndo();
                }

                // bảng vùng ở mốc lớn từng đảo
                var at = new Dictionary<Elem, Vector2>();
                var realms = J.Arr(root, "realms");
                foreach (var o in realms)
                {
                    var r = J.Obj(o);
                    var a = J.Arr(r, "at");
                    at[Keys.ToElem(J.Str(r, "zone"))] = new Vector2(System.Convert.ToSingle(a[0]), System.Convert.ToSingle(a[1]));
                }
                var zones = so.FindProperty("zones");
                for (int i = 0; i < zones.arraySize; i++)
                {
                    var z = zones.GetArrayElementAtIndex(i).objectReferenceValue as HubZone;
                    if (!z || !at.TryGetValue(z.Zone, out var uv)) continue;
                    var rt = (RectTransform)z.transform;
                    rt.SetParent(dao, false);
                    rt.anchorMin = rt.anchorMax = new Vector2(uv.x, 1 - uv.y);
                    rt.anchoredPosition = Vector2.zero;
                    rt.localScale = Vector3.one;
                    // vùng chạm tròn (con đầu có ClickCatcher) đúng mốc
                    var hit = z.GetComponentsInChildren<ClickCatcher>(true).FirstOrDefault();
                    if (hit) rt.anchoredPosition -= (Vector2)rt.InverseTransformPoint(hit.transform.position);
                }

                // mây che từng đảo
                // (HubNightMenu chuyển mây che lên lớp bang_dao trên đèn đêm: xoá cả ở đó)
                foreach (var oldFog in new[] { dao.Find("suong_mu"), dao.parent ? dao.parent.Find("bang_dao/suong_mu") : null })
                    if (oldFog) Object.DestroyImmediate(oldFog.gameObject);
                var fogRt = new GameObject("suong_mu", typeof(RectTransform)).GetComponent<RectTransform>();
                fogRt.SetParent(dao, false);
                fogRt.anchorMin = Vector2.zero;
                fogRt.anchorMax = Vector2.one;
                fogRt.offsetMin = fogRt.offsetMax = Vector2.zero;
                fogRt.SetAsLastSibling();
                var groups = new List<HubFog.Group>();
                int total = 0;
                foreach (var o in realms)
                {
                    var r = J.Obj(o);
                    var e = Keys.ToElem(J.Str(r, "zone"));
                    var c0 = at[e];
                    var g = new GameObject("may_" + J.Str(r, "zone"), typeof(RectTransform)).GetComponent<RectTransform>();
                    g.SetParent(fogRt, false);
                    g.anchorMin = g.anchorMax = new Vector2(c0.x, 1 - c0.y);
                    g.sizeDelta = Vector2.zero;
                    var imgs = new List<Image>();
                    var hits = new List<ClickCatcher>();
                    foreach (var q in J.Arr(r, "clouds"))
                    {
                        var c = J.Arr(q);
                        float u = System.Convert.ToSingle(c[0]), v = System.Convert.ToSingle(c[1]), w = System.Convert.ToSingle(c[2]);
                        bool flip = System.Convert.ToInt32(c[3]) == 1;
                        var go = new GameObject("may", typeof(RectTransform), typeof(Image), typeof(ClickCatcher));
                        var crt = (RectTransform)go.transform;
                        crt.SetParent(g, false);
                        crt.anchorMin = crt.anchorMax = new Vector2(0.5f, 0.5f);
                        float cw = w * vw;
                        crt.sizeDelta = new Vector2(cw, cloud ? cw * cloud.rect.height / cloud.rect.width : cw * 0.53f);
                        crt.anchoredPosition = new Vector2((u - c0.x) * vw, -(v - c0.y) * vh);
                        crt.localScale = new Vector3(flip ? -1 : 1, 1, 1);
                        var img = go.GetComponent<Image>();
                        img.sprite = cloud;
                        img.raycastTarget = true;
                        imgs.Add(img);
                        hits.Add(go.GetComponent<ClickCatcher>());
                        total++;
                    }
                    groups.Add(new HubFog.Group { zone = e, root = g, clouds = imgs.ToArray(), hits = hits.ToArray() });
                }
                var fog = fogRt.gameObject.AddComponent<HubFog>();
                fog.Setup(groups.ToArray());

                // mây vành rời (khoá "ring", người dùng 2026-11-19: vành mây tách từng đám, tàu đi qua thì toả ra): dưới lớp mây che đảo
                var oldRing = dao.Find("may_vien_roi");
                if (oldRing) Object.DestroyImmediate(oldRing.gameObject);
                var ringRt = new GameObject("may_vien_roi", typeof(RectTransform), typeof(CanvasGroup)).GetComponent<RectTransform>();
                ringRt.SetParent(dao, false);
                ringRt.anchorMin = Vector2.zero;
                ringRt.anchorMax = Vector2.one;
                ringRt.offsetMin = ringRt.offsetMax = Vector2.zero;
                ringRt.SetSiblingIndex(fogRt.GetSiblingIndex());
                var ringCg = ringRt.GetComponent<CanvasGroup>();
                ringCg.blocksRaycasts = false;
                ringCg.interactable = false;
                var ringImgs = new List<Image>();
                foreach (var q in J.Arr(root, "ring"))
                {
                    var c = J.Arr(q);
                    float u = System.Convert.ToSingle(c[0]), v = System.Convert.ToSingle(c[1]), w = System.Convert.ToSingle(c[2]);
                    bool flip = System.Convert.ToInt32(c[3]) == 1;
                    var go = new GameObject("may", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                    var crt = (RectTransform)go.transform;
                    crt.SetParent(ringRt, false);
                    crt.anchorMin = crt.anchorMax = new Vector2(0.5f, 0.5f);
                    float cw = w * vw;
                    crt.sizeDelta = new Vector2(cw, cloud ? cw * cloud.rect.height / cloud.rect.width : cw * 0.53f);
                    crt.anchoredPosition = new Vector2((u - 0.5f) * vw, (0.5f - v) * vh);
                    crt.localScale = new Vector3(flip ? -1 : 1, 1, 1);
                    var img = go.GetComponent<Image>();
                    img.sprite = cloud;
                    img.raycastTarget = false;
                    ringImgs.Add(img);
                }
                ringRt.gameObject.AddComponent<CloudRing>().Setup(ringImgs.ToArray(), 290);
                // theo giờ: mây vành rời và mây che đảo nhân DayCycle.CloudTint (dưới lớp nhuộm của sảnh) như mây đảo vùng đất
                var dnc = contents.GetComponentInChildren<DayNight>(true);
                if (dnc)
                {
                    var dso2 = new SerializedObject(dnc);
                    var arr = dso2.FindProperty("clouds");
                    var all = new List<Graphic>(ringImgs);
                    foreach (var g in groups) all.AddRange(g.clouds);
                    arr.arraySize = all.Count;
                    for (int i = 0; i < all.Count; i++) arr.GetArrayElementAtIndex(i).objectReferenceValue = all[i];
                    dso2.ApplyModifiedPropertiesWithoutUndo();
                }

                // làng máy bi: bỏ khỏi đảo (Máy Bi ở hàng nút đáy)
                var village = so.FindProperty("village").objectReferenceValue as Component;
                if (village)
                {
                    var vroot = village.transform;
                    while (vroot.parent && vroot.parent != dao.parent && vroot.parent.name != "anh_nen_world") vroot = vroot.parent;
                    vroot.gameObject.SetActive(false);
                }

                // mây trôi ngang cũ của sảnh: tắt (ảnh bản đồ đã có vành mây vẽ sẵn; mây trôi đè lên mốc đảo)
                var clouds = so.FindProperty("clouds");
                for (int i = 0; i < clouds.arraySize; i++)
                    if (clouds.GetArrayElementAtIndex(i).objectReferenceValue is RectTransform crt0)
                        crt0.gameObject.SetActive(false);

                // công trình side meta: cột thẻ giấy cố định bên phải, dưới thanh trên (kiểu thẻ của hàng nút đáy)
                var bs = so.FindProperty("buildings");
                var bottom = Find("hang_nut");
                var parent = (RectTransform)(bottom ? bottom.parent : scene.transform);
                SideColumn(parent, bs);

                so.FindProperty("fog").objectReferenceValue = fog;
                so.FindProperty("pan").objectReferenceValue = pan;
                so.ApplyModifiedPropertiesWithoutUndo();
                // đèn đêm các đảo (đuốc, chỗ phát sáng) trên lớp nhuộm: gắn lại vào ảnh đảo vừa dựng
                HubNightMenu.Apply(contents);
                PrefabUtility.SaveAsPrefabAsset(contents, HubPath);
                Debug.Log($"[Sảnh] Đã dựng bản đồ thế giới {vw}x{vh}, {groups.Count} đảo, {total} đám mây che, {ringImgs.Count} mây vành rời, {bs.arraySize} công trình ra cột thẻ bên phải.");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
            AssetDatabase.SaveAssets();
        }
    }
}
