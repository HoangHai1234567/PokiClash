// Gắn ảnh bộ phận máy bi vẽ tay (ArtGen/Pachinko, "build.py --duyet bo_phan") vào prefab:
// - Screens/Machine: máng mây "dam_may" dùng pk_may_tha, bi chờ dưới mây "bi_cho" dùng pk_bi;
// - Items/BiLan (bi đang lăn): pk_bi, tắt chấm sáng vẽ tạm "sang".
// Ảnh vẽ tay là ảnh màu thường nên bỏ vật liệu UIKit (vật liệu đó giải mã hình vẽ tạm mã hoá kênh). Bi trắng xám, game tô màu
// theo mức cược (MachineBoard.BallColor). Mặt máy tĩnh (Baked/Machine/may_tinh.png) và nấm (pk_bumper) script đã ghi sẵn,
// nấm thay hình tạm cùng tên qua menu "PokiClash/Dựng lại danh mục ảnh".
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class MachinePartsMenu
    {
        const string MachinePath = "Assets/04 Prefabs/Screens/Machine.prefab";
        const string BallPath = "Assets/04 Prefabs/Items/BiLan.prefab";
        const string Dir = "Assets/03 Art/Pachinko/";

        [MenuItem("PokiClash/Prefab/Máy bi: ảnh bộ phận", priority = 65)]
        public static void Build()
        {
            var cloud = Load("pk_may_tha");
            var ball = Load("pk_bi");
            if (!cloud || !ball) return;

            var contents = PrefabUtility.LoadPrefabContents(MachinePath);
            try
            {
                int n = 0;
                foreach (var img in contents.GetComponentsInChildren<Image>(true))
                {
                    if (img.name == "dam_may") n += Set(img, cloud, Color.white);
                    else if (img.name == "bi_cho") n += Set(img, ball);
                }
                PrefabUtility.SaveAsPrefabAsset(contents, MachinePath);
                Debug.Log($"[Máy bi] Gắn ảnh máng mây, bi chờ vào {MachinePath} ({n} ảnh)");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }

            var bi = PrefabUtility.LoadPrefabContents(BallPath);
            try
            {
                Set(bi.GetComponent<Image>(), ball);
                var shine = bi.transform.Find("sang");
                if (shine) shine.gameObject.SetActive(false);
                PrefabUtility.SaveAsPrefabAsset(bi, BallPath);
                Debug.Log($"[Máy bi] Gắn ảnh bi vào {BallPath}");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(bi);
            }
        }

        // ---------- nút tròn, viên cược, đèn vòm (2026-11-06) ----------
        // Học nút vòm của máy tham khảo (gói ArtGen/Pachinko/gui_gpt/bo_moi lượt 1, ảnh pk_nut_*, pk_cuoc*): nút thả là nút vòm to giữa
        // dưới máy (giữa hai chân tủ), nút thả liền vòm nhỏ bên phải, dòng đếm bi bên trái; thanh mốc và ô quà dời xuống một hàng.
        // Nút giữ SketchButton (bấm, giữ, chữ) nhưng nền để trong suốt, hình là ảnh con "vom"/"hinh"; MachineScene đổi ảnh theo trạng
        // thái. Đèn vòm: bóng rời "den_*" đặt khít bóng vẽ trên tủ theo ArtGen/Pachinko/refs/den_vom.json (build_bo_moi.py --den).
        // Toạ độ trong khoi_may (gốc trên trái, y xuống): tủ hết ở y 1307, khối cao 1530, khung nội dung dài tới 1650 ở màn 9:16.
        const string BulbsJson = "ArtGen/Pachinko/refs/den_vom.json";
        static readonly Vector2 DropAt = new Vector2(540, 1415), DropSize = new Vector2(280, 221);
        static readonly Vector2 AutoAt = new Vector2(842, 1418), AutoSize = new Vector2(186, 150);
        const float TokenSize = 124, TokenStep = 124, LowerRow = 90; // ảnh viên chừa lề cho vạch nhún: hình tròn khoảng 75 % khung

        [System.Serializable]
        class BulbData
        {
            public float[] image;
            public float[][] bulbs;
            public float outer_d, sprite_fill;
        }

        [MenuItem("PokiClash/Prefab/Máy bi: nút tròn, viên cược, đèn vòm", priority = 66)]
        public static void BuildControls()
        {
            var dome = Load("pk_nut_tha");
            var auto = Load("pk_nut_lien");
            var token = Load("pk_cuoc");
            var bulb = Load("pk_den_tat");
            var ring = Load("pk_fx_vong_dut");
            foreach (var n in new[] { "pk_nut_tha_nhan", "pk_nut_tha_het", "pk_nut_tha_lon", "pk_nut_lien_bat", "pk_cuoc_chon", "pk_cuoc_khoa",
                         "pk_cuoc_max", "pk_den_sang", "pk_den_sang_hong" })
                Load(n);
            if (!dome || !auto || !token || !bulb || !ring) return;
            var json = System.IO.Path.Combine(Application.dataPath, "..", BulbsJson);
            if (!System.IO.File.Exists(json))
            {
                Debug.LogError($"[Máy bi] Chưa có {BulbsJson}: chạy py -3 -I ArtGen/Pachinko/build_bo_moi.py --den");
                return;
            }
            var bulbs = ParseBulbs(System.IO.File.ReadAllText(json));

            var contents = PrefabUtility.LoadPrefabContents(MachinePath);
            try
            {
                var scene = contents.GetComponent<MachineScene>();
                var block = Find(contents.transform, "khoi_may");
                var so = new SerializedObject(scene);

                // nút thả: vòm to, chữ trên nắp, vòng nhịp sau vòm, ẩn hình bi nhỏ của nút cũ
                var drop = (RectTransform)Find(block, "nut_tha_bi");
                var dropBtn = drop.GetComponent<PokiClash.UI.SketchButton>();
                Place(drop, DropAt, DropSize);
                var holdRing = Child(drop, "vong_giu", ring);
                holdRing.rectTransform.anchorMin = holdRing.rectTransform.anchorMax = new Vector2(0.5f, 0.5f);
                holdRing.rectTransform.sizeDelta = Vector2.one * DropSize.x * 1.15f;
                holdRing.gameObject.SetActive(false);
                var dropDome = Child(drop, "vom", dome);
                dropDome.rectTransform.SetSiblingIndex(1);
                var icon = drop.Find("bi");
                if (icon) icon.gameObject.SetActive(false);
                // chữ giữa nắp (nắp chiếm khoảng 5–55 % chiều cao từ trên), không chạm mép vòm
                LabelOn(dropBtn, new Vector2(0.14f, 0.52f), new Vector2(0.86f, 0.82f), 24, 46);
                Flat(dropBtn);

                var autoRt = (RectTransform)Find(block, "nut_tha_lien");
                var autoBtn = autoRt.GetComponent<PokiClash.UI.SketchButton>();
                Place(autoRt, AutoAt, AutoSize);
                var autoDome = Child(autoRt, "vom", auto);
                // "THẢ LIỀN 20" xuống hai dòng cho vừa nắp nhỏ
                LabelOn(autoBtn, new Vector2(0.17f, 0.5f), new Vector2(0.83f, 0.9f), 12, 26);
                if (autoBtn.Label) autoBtn.Label.textWrappingMode = TMPro.TextWrappingModes.Normal;
                Flat(autoBtn);

                // dòng đếm bi bên trái nút thả; thanh mốc và ô quà xuống một hàng
                var counter = (RectTransform)Find(block, "dem");
                counter.anchorMin = counter.anchorMax = new Vector2(0, 1);
                counter.pivot = new Vector2(0, 0.5f);
                counter.anchoredPosition = new Vector2(40, -DropAt.y + 20);
                counter.sizeDelta = new Vector2(350, 60);
                var ct = counter.GetComponent<TMPro.TextMeshProUGUI>();
                if (ct && !ct.enableAutoSizing)
                {
                    ct.fontSizeMax = ct.fontSize;
                    ct.fontSizeMin = 22;
                    ct.enableAutoSizing = true;
                }
                foreach (var n in new[] { "thanh_Rage", "o_qua", "huyen_thoai" })
                {
                    var rt = (RectTransform)Find(block, n);
                    // dời một lần: đã ở hàng dưới (dưới đáy khối) thì thôi
                    if (rt && -rt.anchoredPosition.y < 1530) rt.anchoredPosition += new Vector2(0, -LowerRow);
                }

                // viên cược: theo thứ tự nút cược của MachineScene, xếp dọc dưới chữ "Cược"
                var betsProp = so.FindProperty("p.bets");
                var tokens = new System.Collections.Generic.List<Image>();
                for (int i = 0; i < betsProp.arraySize; i++)
                {
                    var b = (PokiClash.UI.SketchButton)betsProp.GetArrayElementAtIndex(i).objectReferenceValue;
                    if (!b) continue;
                    var rt = b.Rect;
                    rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 1);
                    rt.pivot = new Vector2(0.5f, 0.5f);
                    rt.anchoredPosition = new Vector2(0, -(TokenStep + i * TokenStep));
                    rt.sizeDelta = Vector2.one * TokenSize;
                    var le = b.GetComponent<LayoutElement>();
                    if (le) le.preferredWidth = le.preferredHeight = TokenSize;
                    tokens.Add(Child(rt, "hinh", token));
                    var cap = rt.Find("cap");
                    if (cap && cap.TryGetComponent<TMPro.TextMeshProUGUI>(out var capText))
                    {
                        var cr = capText.rectTransform;
                        // "n bi" dưới số cược, chừa ổ khoá vẽ ở góc dưới phải
                        cr.anchorMin = new Vector2(0.18f, 0.28f);
                        cr.anchorMax = new Vector2(0.72f, 0.47f);
                        cr.offsetMin = cr.offsetMax = Vector2.zero;
                        cr.anchoredPosition = Vector2.zero;
                        capText.enableAutoSizing = true;
                        capText.fontSizeMin = 14;
                        capText.fontSizeMax = 22;
                        capText.margin = Vector4.zero;
                        capText.alignment = TMPro.TextAlignmentOptions.Center;
                    }
                    Flat(b, false);
                }

                // đèn vòm: bóng rời khít bóng vẽ trên tủ (tắt sẵn, MachineScene bật và cho chạy)
                var cab = (RectTransform)Find(block, "than_may_ve");
                for (int i = cab.childCount - 1; i >= 0; i--)
                    if (cab.GetChild(i).name.StartsWith("den_")) Object.DestroyImmediate(cab.GetChild(i).gameObject);
                float sx = cab.sizeDelta.x / bulbs.image[0], sy = cab.sizeDelta.y / bulbs.image[1];
                float w = bulbs.outer_d / bulbs.sprite_fill * sx, h = w * bulb.rect.height / bulb.rect.width;
                var lamps = new System.Collections.Generic.List<Image>();
                for (int i = 0; i < bulbs.bulbs.Length; i++)
                {
                    var img = Child(cab, $"den_{i:00}", bulb);
                    var r = img.rectTransform;
                    r.anchorMin = r.anchorMax = new Vector2(0, 1);
                    r.pivot = new Vector2(0.5f, 0.5f);
                    r.anchoredPosition = new Vector2(bulbs.bulbs[i][0] * sx, -bulbs.bulbs[i][1] * sy);
                    r.sizeDelta = new Vector2(w, h);
                    img.gameObject.SetActive(false);
                    lamps.Add(img);
                }

                so.FindProperty("p.dropDome").objectReferenceValue = dropDome;
                so.FindProperty("p.autoDome").objectReferenceValue = autoDome;
                so.FindProperty("p.holdRing").objectReferenceValue = holdRing;
                SetArray(so.FindProperty("p.betTokens"), tokens);
                SetArray(so.FindProperty("p.bulbs"), lamps);
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, MachinePath);
                Debug.Log($"[Máy bi] Nút vòm, {tokens.Count} viên cược, {lamps.Count} đèn vòm vào {MachinePath}");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }

        // JsonUtility không đọc mảng lồng: tự tách "bulbs": [[x, y], ...]
        static BulbData ParseBulbs(string text)
        {
            float Num(string key)
            {
                var m = System.Text.RegularExpressions.Regex.Match(text, "\"" + key + "\"\\s*:\\s*([-0-9.]+)");
                return float.Parse(m.Groups[1].Value, System.Globalization.CultureInfo.InvariantCulture);
            }
            var d = new BulbData { outer_d = Num("outer_d"), sprite_fill = Num("sprite_fill") };
            var img = System.Text.RegularExpressions.Regex.Match(text, "\"image\"\\s*:\\s*\\[\\s*([0-9.]+)\\s*,\\s*([0-9.]+)\\s*\\]");
            d.image = new[] { P(img.Groups[1].Value), P(img.Groups[2].Value) };
            var list = new System.Collections.Generic.List<float[]>();
            var body = text.Substring(text.IndexOf("\"bulbs\""));
            body = body.Substring(body.IndexOf('[') + 1);
            foreach (System.Text.RegularExpressions.Match m in System.Text.RegularExpressions.Regex.Matches(body, "\\[\\s*([-0-9.]+)\\s*,\\s*([-0-9.]+)\\s*\\]"))
                list.Add(new[] { P(m.Groups[1].Value), P(m.Groups[2].Value) });
            d.bulbs = list.ToArray();
            return d;
        }

        static float P(string s) => float.Parse(s, System.Globalization.CultureInfo.InvariantCulture);

        static Transform Find(Transform t, string name)
        {
            foreach (var c in t.GetComponentsInChildren<Transform>(true))
                if (c.name == name) return c;
            return null;
        }

        // đặt theo tâm (toạ độ khoi_may: gốc trên trái, y xuống)
        static void Place(RectTransform rt, Vector2 at, Vector2 size)
        {
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = new Vector2(at.x, -at.y);
            rt.sizeDelta = size;
            rt.localScale = Vector3.one;
            var le = rt.GetComponent<LayoutElement>();
            if (le)
            {
                le.preferredWidth = size.x;
                le.preferredHeight = size.y;
            }
        }

        // ảnh con phủ kín cha, sau chữ (dựng lại thì dùng lại ảnh cũ cùng tên)
        static Image Child(Transform parent, string name, Sprite sprite)
        {
            var t = parent.Find(name);
            var img = t ? t.GetComponent<Image>() : new GameObject(name, typeof(RectTransform), typeof(Image)).GetComponent<Image>();
            img.transform.SetParent(parent, false);
            img.transform.SetSiblingIndex(0);
            var r = img.rectTransform;
            r.anchorMin = Vector2.zero;
            r.anchorMax = Vector2.one;
            r.pivot = new Vector2(0.5f, 0.5f);
            r.offsetMin = r.offsetMax = Vector2.zero;
            img.sprite = sprite;
            img.material = null;
            img.color = Color.white;
            img.type = Image.Type.Simple;
            img.preserveAspect = true;
            img.raycastTarget = false;
            return img;
        }

        // chữ nút nằm trên nắp vòm, tự co
        static void LabelOn(PokiClash.UI.SketchButton b, Vector2 min, Vector2 max, float minSize, float maxSize)
        {
            var l = b.Label;
            if (!l) return;
            var r = l.rectTransform;
            r.anchorMin = min;
            r.anchorMax = max;
            r.offsetMin = r.offsetMax = Vector2.zero;
            r.anchoredPosition = Vector2.zero;
            l.enableAutoSizing = true;
            l.fontSizeMax = maxSize;
            l.fontSizeMin = minSize;
            l.alignment = TMPro.TextAlignmentOptions.Center;
        }

        // nền SketchButton trong suốt (hình là ảnh con); nút có hình nhấn riêng thì tắt hoạt cảnh nhấn chung (trường noMotion nếu có)
        static void Flat(PokiClash.UI.SketchButton b, bool noMotion = true)
        {
            b.SetColor(new Color(1, 1, 1, 0));
            var so = new SerializedObject(b);
            var nm = so.FindProperty("noMotion");
            if (nm != null && noMotion)
            {
                nm.boolValue = true;
                so.ApplyModifiedPropertiesWithoutUndo();
            }
            EditorUtility.SetDirty(b);
        }

        static void SetArray(SerializedProperty prop, System.Collections.Generic.List<Image> items)
        {
            prop.arraySize = items.Count;
            for (int i = 0; i < items.Count; i++) prop.GetArrayElementAtIndex(i).objectReferenceValue = items[i];
        }

        static Sprite Load(string name)
        {
            var path = Dir + name + ".png";
            AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
            var s = AssetDatabase.LoadAssetAtPath<Sprite>(path);
            if (!s) Debug.LogError($"[Máy bi] Chưa có {path}: chạy py -3 -I ArtGen/Pachinko/build.py --duyet bo_phan");
            return s;
        }

        static int Set(Image img, Sprite sprite, Color? color = null)
        {
            if (!img) return 0;
            img.sprite = sprite;
            if (color.HasValue) img.color = color.Value;
            img.material = null;
            img.preserveAspect = true;
            img.type = Image.Type.Simple;
            EditorUtility.SetDirty(img);
            return 1;
        }
    }
}
