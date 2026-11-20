// Bố cục màn máy bi bản 2 (GD_Claude/23; concept 2 + cờ đuôi nheo của concept 1, người dùng chốt 2026-11-20; bố cục, số đèn đo
// theo bản đục máy bi Clash of Critters, hình là của mình: ArtGen/Pachinko/v2). Đọc ArtGen/Pachinko/v2/refs/bo_cuc_v2.json (khối,
// px khối máy: gốc trên trái, y xuống) và v2_do.json (bóng đèn vẽ sẵn trên thân máy), sửa Screens/Machine:
// - nền phòng pk_nen_phong phủ màn, giữ tỉ lệ;
// - than_may_ve: thân máy vòm đỏ pk_than_may_v2 theo vùng vẽ của nó; 90 lớp sáng fx2_den_vang phủ đúng bóng vẽ sẵn (vòm, hai cột,
//   gờ đế; một vòng liền) thành p.bulbs (MachineScene.UpdateBulbs bật/tắt);
// - bàn "May" thu BOARD_SCALE, mặt tĩnh may_tinh_v2 (cam ngoài vòm trong suốt: thân máy hiện ra quanh vòm trời);
// - thanh kinh nghiệm lên trên cùng, nút tỉ lệ ở đầu phải thanh; chỗ bảng số "cho_bang_so" trên đỉnh vòm (p.scoreSlot);
// - nút PUSH vòm sao pk_push_* (không chữ), nút thả liền nhỏ pk_v2_lien có chú thích dưới; viên cược "nut_cuoc" pk_v2_cuoc thay
//   cột cược (p.betCycle, bấm đổi mức); khung khay pk_v2_khay (p.trayFrame) chứa khay rương; thanh đếm bi pk_v2_dem sau chữ đếm;
//   thanh mốc quà + ô quà ở góc dưới phải.
// Chạy lại được (đặt lại theo số đo). Ảnh cắt bằng py -3 -I ArtGen/Pachinko/v2/cat_v2.py.
using System.Collections.Generic;
using System.IO;
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class MachineV2Menu
    {
        const string MachinePath = "Assets/04 Prefabs/Screens/Machine.prefab";
        const string BlockPath = "Canvas/An toan/Khung/Noi dung/khoi_may";
        const string ArtDir = "Assets/03 Art/Pachinko/";
        const string FacePath = "Assets/03 Art/Baked/Machine/may_tinh_v2.png";
        static string RefDir => Path.GetFullPath(Path.Combine(Application.dataPath, "../ArtGen/Pachinko/v2/refs"));

        // thanh kinh nghiệm: phóng 1,12, mép trên 122 px trên đỉnh khối (sát dưới thanh trên của app ở màn 9:16); nút tỉ lệ ở đầu phải
        const float BarScale = 1.12f, BarX = 100, BarTop = 122, RatesX = 948, RatesY = 60, RatesD = 84;

        static readonly string[] Need =
        {
            "pk_nen_phong", "pk_than_may_v2", "pk_bang_so_v2", "pk_push_thuong", "pk_push_lun", "pk_push_het", "pk_push_lon", "pk_v2_cuoc",
            "pk_v2_cuoc_khoa", "pk_v2_khay", "pk_v2_dem", "pk_v2_lien", "pk_v2_lien_bat", "fx2_den_vang", "fx2_den_hong", "fx2_quang",
            "pk_so_0", "pk_so_9", "pk_sao_bang", "fx2_mui_ten",
        };

        [System.Serializable]
        sealed class Layout
        {
            public float board_scale;
            public float[] board, score, push, bet, auto, tray, counter, gift;
        }

        [System.Serializable]
        sealed class UnityDo
        {
            public float[] rect, bulbs; // vùng vẽ thân máy x, y, w, h; bóng x, y, r liền nhau (px khối máy)
            public float core; // lõi bóng trong ảnh sáng (phần còn lại là quầng)
        }

        [System.Serializable]
        sealed class Sao
        {
            public float[] size, anchor; // tâm ngôi sao trong ảnh (tỉ lệ, gốc trên trái)
            public float star_w; // bề ngang ngôi sao / bề ngang ảnh
        }

        [System.Serializable]
        sealed class Do
        {
            public UnityDo unity;
            public Sao sao;
        }

        [System.Serializable]
        sealed class MatV2
        {
            public float ext, bw;
            public float[] entry; // chỗ ống phóng chui vào mặt chơi (đơn vị máy)
        }

        // sao băng: ngôi sao rộng 64 đơn vị máy, nghiêng 15° cho đuôi rủ dọc ống phóng
        const float StarUnits = 64, StarTilt = -15;

        static Sprite S(string name) => AssetDatabase.LoadAssetAtPath<Sprite>(ArtDir + name + ".png");

        static void Box(RectTransform rt, float[] r) =>
            rt.Place(new Vector2(0, 1), new Vector2(r[0], -r[1]), new Vector2(r[2] - r[0], r[3] - r[1]), new Vector2(0, 1));

        static Image Img(Transform parent, string name, Sprite s, bool preserve = true)
        {
            var t = parent.Find(name);
            GameObject go;
            if (t) go = t.gameObject;
            else
            {
                go = new GameObject(name, typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                go.transform.SetParent(parent, false);
            }
            var img = go.GetComponent<Image>();
            img.sprite = s;
            img.preserveAspect = preserve;
            img.raycastTarget = false;
            img.color = Color.white;
            img.type = Image.Type.Simple;
            return img;
        }

        static RectTransform Rect(Transform parent, string name)
        {
            var t = parent.Find(name) as RectTransform;
            if (t) return t;
            var go = new GameObject(name, typeof(RectTransform));
            go.transform.SetParent(parent, false);
            return (RectTransform)go.transform;
        }

        // đặt rt ngay trước target trong thứ tự vẽ (chạy lại menu không đảo thứ tự)
        static void PutBefore(Transform rt, Transform target)
        {
            int i = target.GetSiblingIndex();
            rt.SetSiblingIndex(rt.GetSiblingIndex() < i ? i - 1 : i);
        }

        static void SetRef(SerializedObject so, string path, Object value)
        {
            var sp = so.FindProperty(path);
            if (sp == null) Debug.LogError("[Máy bi v2] Không thấy trường " + path);
            else sp.objectReferenceValue = value;
        }

        // mặt bàn tĩnh mới nằm trong Baked/Machine (bộ nhập chỉ ép nén ở đó): tự đặt kiểu Sprite, giữ nét 2048
        static void SetupFace()
        {
            AssetDatabase.ImportAsset(FacePath, ImportAssetOptions.ForceUpdate);
            var ti = AssetImporter.GetAtPath(FacePath) as TextureImporter;
            if (!ti) return;
            if (ti.textureType == TextureImporterType.Sprite && ti.maxTextureSize == 2048) return;
            ti.textureType = TextureImporterType.Sprite;
            ti.spriteImportMode = SpriteImportMode.Single;
            ti.mipmapEnabled = false;
            ti.alphaIsTransparency = true;
            ti.wrapMode = TextureWrapMode.Clamp;
            ti.npotScale = TextureImporterNPOTScale.None;
            ti.maxTextureSize = 2048;
            ti.SaveAndReimport();
        }

        [MenuItem("PokiClash/Prefab/Máy bi: bố cục bản 2 (concept 2)", priority = 66)]
        public static void Build()
        {
            string layPath = Path.Combine(RefDir, "bo_cuc_v2.json"), doPath = Path.Combine(RefDir, "v2_do.json");
            if (!File.Exists(layPath) || !File.Exists(doPath))
            {
                Debug.LogError("[Máy bi v2] Thiếu số đo: chạy py -3 -I ArtGen/Pachinko/v2/make_parts_refs.py rồi cat_v2.py");
                return;
            }
            var lay = JsonUtility.FromJson<Layout>(File.ReadAllText(layPath));
            var doAll = JsonUtility.FromJson<Do>(File.ReadAllText(doPath));
            var dov = doAll.unity;
            AssetDatabase.Refresh();
            SetupFace();
            EditorApplication.ExecuteMenuItem("PokiClash/Dựng lại danh mục ảnh");
            var missing = new List<string>();
            foreach (var n in Need)
                if (!S(n)) missing.Add(n);
            var face = AssetDatabase.LoadAssetAtPath<Sprite>(FacePath);
            if (!face) missing.Add("may_tinh_v2");
            if (missing.Count > 0)
            {
                Debug.LogError("[Máy bi v2] Chưa có ảnh: " + string.Join(", ", missing) + " (chạy cat_v2.py)");
                return;
            }

            var contents = PrefabUtility.LoadPrefabContents(MachinePath);
            try
            {
                var root = contents.transform;
                var block = root.Find(BlockPath) as RectTransform;
                var scene = contents.GetComponent<MachineScene>();
                if (!block || !scene)
                {
                    Debug.LogError("[Máy bi v2] Không thấy " + BlockPath + " hoặc MachineScene");
                    return;
                }
                var so = new SerializedObject(scene);

                // 1. nền phòng phủ màn, giữ tỉ lệ
                var bg = root.Find("Canvas/Nen/ban_go") as RectTransform;
                if (bg)
                {
                    var bi = bg.GetComponent<Image>();
                    var room = S("pk_nen_phong");
                    bi.sprite = room;
                    bi.color = Color.white;
                    bi.type = Image.Type.Simple;
                    bi.preserveAspect = false;
                    bg.anchorMin = bg.anchorMax = bg.pivot = new Vector2(0.5f, 0.5f);
                    bg.anchoredPosition = Vector2.zero;
                    var fit = bg.GetComponent<AspectRatioFitter>() ?? bg.gameObject.AddComponent<AspectRatioFitter>();
                    fit.aspectMode = AspectRatioFitter.AspectMode.EnvelopeParent;
                    fit.aspectRatio = room.rect.width / room.rect.height;
                }

                // 2. thân máy + lớp sáng trên bóng vẽ sẵn
                var cab = block.Find("than_may_ve") as RectTransform;
                var ci = cab.GetComponent<Image>();
                ci.sprite = S("pk_than_may_v2");
                ci.color = Color.white;
                ci.preserveAspect = false;
                var r = dov.rect;
                cab.Place(new Vector2(0, 1), new Vector2(r[0], -r[1]), new Vector2(r[2], r[3]), new Vector2(0, 1));
                foreach (Transform c in cab)
                    if (c.name.StartsWith("den_") && c.name != "den_v2") c.gameObject.SetActive(false); // bóng rời bản cũ
                var lights = Rect(cab, "den_v2");
                lights.gameObject.SetActive(true);
                lights.Stretch();
                for (int i = lights.childCount - 1; i >= 0; i--) Object.DestroyImmediate(lights.GetChild(i).gameObject);
                var lit = S("fx2_den_vang");
                var bulbs = new List<Image>();
                for (int i = 0; i + 2 < dov.bulbs.Length; i += 3)
                {
                    var img = Img(lights, $"d{i / 3:000}", lit);
                    img.color = new Color(1, 1, 1, 0);
                    float d = 2 * dov.bulbs[i + 2] / dov.core;
                    img.rectTransform.Place(new Vector2(0, 1), new Vector2(dov.bulbs[i] - r[0], -(dov.bulbs[i + 1] - r[1])), Vector2.one * d, new Vector2(0.5f, 0.5f));
                    bulbs.Add(img);
                }
                var bp = so.FindProperty("p.bulbs");
                bp.arraySize = bulbs.Count;
                for (int i = 0; i < bulbs.Count; i++) bp.GetArrayElementAtIndex(i).objectReferenceValue = bulbs[i];

                // 3. bàn thu nhỏ, mặt tĩnh có góc trong suốt
                var may = block.Find("May") as RectTransform;
                may.localScale = Vector3.one * lay.board_scale;
                may.anchoredPosition = new Vector2(lay.board[0], -lay.board[1]);
                var tinh = may.Find("anh_tinh")?.GetComponent<Image>();
                if (tinh) tinh.sprite = face;
                // tấm giấy kem sau mặt bàn (KhungMong): bản cũ bị góc cam che, bản 2 góc trong suốt nên nó lộ ra quanh vòm
                var paper = may.Find("mat_may");
                if (paper) paper.gameObject.SetActive(false);
                // mặt bàn bản 3 (ghep_ban_v2.py): ảnh rộng hơn khung bàn EXT đơn vị bên phải (ống vàng ngoài của làn phóng); sao băng che
                // chỗ ống chui vào mặt chơi (như máy tham khảo), sao nhỏ lật gương ở góc trái; nằm trên cùng trong bàn (bi đi dưới sao)
                var mv = File.Exists(Path.Combine(RefDir, "mat_v2.json")) ? JsonUtility.FromJson<MatV2>(File.ReadAllText(Path.Combine(RefDir, "mat_v2.json"))) : null;
                if (tinh && mv != null)
                {
                    var tr = tinh.rectTransform;
                    tr.Stretch();
                    tr.offsetMax = new Vector2(mv.ext * MachineBoard.K, 0);
                }
                var star = S("pk_sao_bang");
                if (mv != null && star && doAll.sao != null && doAll.sao.anchor != null && doAll.sao.anchor.Length == 2)
                {
                    float w = StarUnits / doAll.sao.star_w * MachineBoard.K;
                    var size = new Vector2(w, w * star.rect.height / star.rect.width);
                    var pivot = new Vector2(doAll.sao.anchor[0], 1 - doAll.sao.anchor[1]);
                    var right = Img(may, "sao_bang", star);
                    right.rectTransform.Place(new Vector2(0, 1), new Vector2(mv.entry[0], -mv.entry[1]) * MachineBoard.K, size, pivot);
                    right.rectTransform.localEulerAngles = new Vector3(0, 0, StarTilt);
                    right.rectTransform.localScale = Vector3.one;
                    right.rectTransform.SetAsLastSibling();
                    var left = Img(may, "sao_bang_trai", star);
                    left.rectTransform.Place(new Vector2(0, 1), new Vector2(mv.bw - mv.entry[0] - 22, -(mv.entry[1] - 6)) * MachineBoard.K, size * 0.62f, pivot);
                    left.rectTransform.localEulerAngles = new Vector3(0, 0, -StarTilt);
                    left.rectTransform.localScale = new Vector3(-1, 1, 1);
                    left.rectTransform.SetAsLastSibling();
                }

                // 4. thanh kinh nghiệm trên cùng, nút tỉ lệ ở đầu phải
                var bar = block.Find("thanh_kinh_nghiem") as RectTransform;
                if (bar)
                {
                    bar.localScale = Vector3.one * BarScale;
                    bar.anchorMin = bar.anchorMax = bar.pivot = new Vector2(0, 1);
                    bar.anchoredPosition = new Vector2(BarX, BarTop);
                }
                var rates = block.Find("nut_ti_le") as RectTransform;
                if (rates) rates.Place(new Vector2(0, 1), new Vector2(RatesX, RatesY), Vector2.one * RatesD, new Vector2(0.5f, 0.5f));

                // 5. chỗ bảng số trên đỉnh vòm (bảng dựng lúc vào màn), đứng sau bàn trong thứ tự vẽ (đè lên huy hiệu vòm)
                var slot = Rect(block, "cho_bang_so");
                Box(slot, lay.score);
                PutBefore(slot, may);
                PutBefore(may, slot); // ngay sau bàn
                SetRef(so, "p.scoreSlot", slot);

                // 6. nút PUSH: vòm sao, không chữ; gốc co giãn ở chân vòm (nhảy, lún từ đế)
                var drop = block.Find("nut_tha_bi") as RectTransform;
                Box(drop, lay.push);
                var vom = drop.Find("vom") as RectTransform;
                if (vom)
                {
                    vom.Stretch();
                    vom.pivot = new Vector2(0.5f, 0.06f);
                    vom.offsetMin = vom.offsetMax = Vector2.zero;
                    var vi = vom.GetComponent<Image>();
                    vi.sprite = S("pk_push_thuong");
                    vi.preserveAspect = true;
                    vi.color = Color.white;
                }
                var dl = drop.Find("nhan");
                if (dl) dl.gameObject.SetActive(false);

                // 7. nút thả liền: vòm nhỏ có mũi tên vòng, chú thích "LIỀN ×N" dưới nút
                var auto = block.Find("nut_tha_lien") as RectTransform;
                Box(auto, lay.auto);
                var av = auto.Find("vom") as RectTransform;
                if (av)
                {
                    av.Stretch();
                    var ai = av.GetComponent<Image>();
                    ai.sprite = S("pk_v2_lien");
                    ai.preserveAspect = true;
                    ai.color = Color.white;
                }
                var al = auto.Find("nhan")?.GetComponent<TextMeshProUGUI>();
                if (al)
                {
                    al.rectTransform.Place(new Vector2(0.5f, 0), new Vector2(0, 2), new Vector2(200, 40), new Vector2(0.5f, 1));
                    al.enableAutoSizing = false;
                    al.fontSize = 28;
                    al.alignment = TextAlignmentOptions.Center;
                    al.color = Theme.Hex("#fff3c4");
                }

                // 8. viên cược thay cột cược
                var col = block.Find("cot_cuoc");
                RectTransform nut = block.Find("nut_cuoc") as RectTransform;
                if (!nut && col && col.Find("cuoc_x1"))
                {
                    nut = (RectTransform)Object.Instantiate(col.Find("cuoc_x1").gameObject, block).transform;
                    nut.name = "nut_cuoc";
                }
                if (col) col.gameObject.SetActive(false);
                if (nut)
                {
                    nut.gameObject.SetActive(true);
                    nut.SetSiblingIndex(col ? col.GetSiblingIndex() + 1 : nut.GetSiblingIndex());
                    Box(nut, lay.bet);
                    nut.localScale = Vector3.one;
                    var hinh = nut.Find("hinh") as RectTransform;
                    if (hinh)
                    {
                        hinh.Stretch();
                        var hi = hinh.GetComponent<Image>();
                        hi.sprite = S("pk_v2_cuoc");
                        hi.preserveAspect = true;
                        hi.color = Color.white;
                        SetRef(so, "p.betCycleArt", hi);
                    }
                    var nl = nut.Find("nhan")?.GetComponent<TextMeshProUGUI>();
                    if (nl)
                    {
                        nl.rectTransform.Stretch(30, 12, 30, 18);
                        nl.enableAutoSizing = false;
                        nl.fontSize = 54;
                        nl.alignment = TextAlignmentOptions.Center;
                        nl.color = Theme.Hex("#fff3c4"); // bản casino: viên cược tím, chữ kem
                    }
                    var cap = nut.Find("cap");
                    if (cap) cap.gameObject.SetActive(false);
                    SetRef(so, "p.betCycle", nut.GetComponent<SketchButton>());
                }

                // 9. khung khay + khay rương trong khung (chỉ một rương hiện, giữa khung)
                var khay = block.Find("khay_ruong") as RectTransform;
                var frame = Img(block, "khung_khay", S("pk_v2_khay"), false);
                Box(frame.rectTransform, lay.tray);
                if (khay)
                {
                    PutBefore(frame.rectTransform, khay);
                    Box(khay, lay.tray);
                    var empty = so.FindProperty("p.trayEmpty").objectReferenceValue as GameObject;
                    foreach (Transform c in khay)
                    {
                        var t = c.GetComponent<TextMeshProUGUI>();
                        if (t && (!empty || c.gameObject != empty)) c.gameObject.SetActive(false); // chữ "Rương chờ"
                        if (c.GetComponent<SketchButton>())
                        {
                            var cr = (RectTransform)c;
                            cr.anchorMin = cr.anchorMax = cr.pivot = new Vector2(0.5f, 0.5f);
                            cr.anchoredPosition = new Vector2(0, 6);
                            cr.localScale = Vector3.one * 1.05f;
                        }
                    }
                    if (empty)
                    {
                        var er = (RectTransform)empty.transform;
                        er.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(170, 50), new Vector2(0.5f, 0.5f));
                        var et = empty.GetComponent<TextMeshProUGUI>();
                        if (et) et.color = Theme.Hex("#fff3c4");
                    }
                }
                SetRef(so, "p.trayFrame", frame.rectTransform);

                // 10. thanh đếm bi: ảnh thanh có icon bi ở đầu, chữ đếm phần còn lại
                var dem = block.Find("dem")?.GetComponent<TextMeshProUGUI>();
                var pill = Img(block, "khung_dem", S("pk_v2_dem"), false);
                Box(pill.rectTransform, lay.counter);
                if (dem)
                {
                    PutBefore(pill.rectTransform, dem.rectTransform);
                    var c = lay.counter;
                    float h = c[3] - c[1];
                    dem.rectTransform.Place(new Vector2(0, 1), new Vector2(c[0] + h * 1.25f, -c[1]), new Vector2(c[2] - c[0] - h * 1.6f, h), new Vector2(0, 1));
                    dem.enableAutoSizing = false;
                    dem.fontSize = 40;
                    dem.alignment = TextAlignmentOptions.Center;
                    dem.color = Theme.Hex("#fff3c4"); // bản casino: thanh đếm tím sẫm, chữ kem
                }
                // chữ gợi ý "chạm hoặc giữ để thả bi" nằm trên nền tím của mặt chơi casino: chữ kem
                foreach (var t in root.GetComponentsInChildren<TextMeshProUGUI>(true))
                    if (t.text.Contains("để thả bi")) t.color = Theme.Hex("#fff3c4");

                // 11. thanh mốc quà + ô quà góc dưới phải
                var g = lay.gift;
                float gy = (g[1] + g[3]) / 2;
                var rage = block.Find("thanh_Rage") as RectTransform;
                if (rage) rage.Place(new Vector2(0, 1), new Vector2(g[0], -gy), new Vector2(g[2] - g[0] - 84, 40), new Vector2(0, 0.5f));
                var gift = block.Find("o_qua") as RectTransform;
                if (gift)
                {
                    gift.Place(new Vector2(0, 1), new Vector2(g[2] - 42, -gy), new Vector2(124, 124), new Vector2(0.5f, 0.5f));
                    gift.localScale = Vector3.one * 0.72f;
                }

                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, MachinePath);
                Debug.Log($"[Máy bi v2] Đã dựng bố cục bản 2: {bulbs.Count} bóng thân máy, bàn ×{lay.board_scale}");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
