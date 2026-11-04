// Đặt thân máy vẽ tay (ArtGen/Pachinko, ảnh đã duyệt bằng "build.py --duyet") vào Screens/Machine:
// - "than_may_ve": ảnh Assets/03 Art/Pachinko/pk_than_may.png sau mặt máy, đúng khung đo trong ảnh (px khối máy);
// - tắt khung giấy tạm "May/than_may" (thân máy vẽ tay thay nó);
// - dời thanh kinh nghiệm vào rãnh của đầu máy (thanh vừa trong rãnh, vòng cấp đè lên hốc tròn bên trái);
// - nút tỉ lệ thành nút tròn trong suốt chỉ có chữ "i", nằm trong hốc tròn bên phải (chữ "Tỉ lệ" ẩn, vẫn giữ để công cụ thử tìm nút);
// - cột cược và khay rương sát mép màn, thu nhỏ cho khỏi đè viền tủ.
// Số đo đọc từ ArtGen/Pachinko/refs/than_may_da_duyet.json. Chạy lại được (đặt lại vị trí theo số đo mới).
using System.IO;
using PokiClash.UI;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class MachineCabinetMenu
    {
        const string MachinePath = "Assets/04 Prefabs/Screens/Machine.prefab";
        const string SpritePath = "Assets/03 Art/Pachinko/pk_than_may.png";
        const string BlockPath = "Canvas/An toan/Khung/Noi dung/khoi_may";
        const float Margin = 6, Gap = 4; // cột cược, khay rương: cách mép màn, cách viền tủ
        static string JsonPath => Path.GetFullPath(Path.Combine(Application.dataPath, "../ArtGen/Pachinko/refs/than_may_da_duyet.json"));

        [System.Serializable]
        sealed class Measure
        {
            public float[] cabinet, window, groove, badge, info; // khung x0, y0, x1, y1; hốc tròn cx, cy, d (px khối máy, y xuống)
        }

        // mép phải (right) hoặc trái nhất của các nút trong cột, theo px khối máy (gốc trái)
        static float Edge(RectTransform block, RectTransform col, bool right)
        {
            float best = right ? float.MinValue : float.MaxValue;
            var corners = new Vector3[4];
            foreach (var b in col.GetComponentsInChildren<SketchButton>(true))
            {
                b.Rect.GetWorldCorners(corners);
                foreach (var c in corners)
                {
                    float x = block.InverseTransformPoint(c).x - block.rect.xMin;
                    best = right ? Mathf.Max(best, x) : Mathf.Min(best, x);
                }
            }
            return best;
        }

        [MenuItem("PokiClash/Prefab/Máy bi: thân máy vẽ tay", priority = 64)]
        public static void Build()
        {
            if (!File.Exists(JsonPath))
            {
                Debug.LogError("[Máy bi] Chưa duyệt thân máy: chạy py -3 -I ArtGen/Pachinko/build.py --duyet (thiếu " + JsonPath + ")");
                return;
            }
            var m = JsonUtility.FromJson<Measure>(File.ReadAllText(JsonPath));
            AssetDatabase.ImportAsset(SpritePath, ImportAssetOptions.ForceUpdate);
            var sprite = AssetDatabase.LoadAssetAtPath<Sprite>(SpritePath);
            if (!sprite)
            {
                Debug.LogError("[Máy bi] Không nạp được " + SpritePath);
                return;
            }
            var contents = PrefabUtility.LoadPrefabContents(MachinePath);
            try
            {
                var block = contents.transform.Find(BlockPath);
                var machine = block ? block.Find("May") : null;
                if (!machine)
                {
                    Debug.LogError("[Máy bi] Không thấy " + BlockPath + "/May trong " + MachinePath);
                    return;
                }

                // ảnh thân máy, sau mặt máy
                var cab = block.Find("than_may_ve") as RectTransform;
                if (!cab)
                {
                    var go = new GameObject("than_may_ve", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                    cab = (RectTransform)go.transform;
                    cab.SetParent(block, false);
                }
                var img = cab.GetComponent<Image>();
                img.sprite = sprite;
                img.raycastTarget = false;
                img.color = Color.white;
                cab.Place(new Vector2(0, 1), new Vector2(m.cabinet[0], -m.cabinet[1]),
                    new Vector2(m.cabinet[2] - m.cabinet[0], m.cabinet[3] - m.cabinet[1]), new Vector2(0, 1));
                // sau mặt máy (chạy lại menu thì thân máy đã ở trước "May": giữ nguyên, đặt lại sẽ đẩy nó lên trên mặt máy)
                if (cab.GetSiblingIndex() > machine.GetSiblingIndex()) cab.SetSiblingIndex(machine.GetSiblingIndex());

                var paper = machine.Find("than_may");
                if (paper) paper.gameObject.SetActive(false);

                // thanh kinh nghiệm theo rãnh và hốc vòng cấp
                var bar = block.Find("thanh_kinh_nghiem") as RectTransform;
                if (bar)
                {
                    float gx0 = m.groove[0], gy0 = m.groove[1], gx1 = m.groove[2], gy1 = m.groove[3];
                    float gcy = (gy0 + gy1) / 2, gh = gy1 - gy0;
                    float x0 = m.badge[0] - m.badge[2] / 2 - 4, h = Mathf.Max(gh, m.badge[2]) + 8;
                    bar.Place(new Vector2(0, 1), new Vector2(x0, -(gcy - h / 2)), new Vector2(gx1 + 2 - x0, h), new Vector2(0, 1));
                    var thanh = bar.Find("thanh_exp") as RectTransform;
                    if (thanh) thanh.Place(new Vector2(0, 0.5f), new Vector2(gx0 + 3 - x0, 0), new Vector2(gx1 - gx0 - 6, gh - 6), new Vector2(0, 0.5f));
                    var badge = bar.Find("vong_cap") as RectTransform;
                    if (badge)
                    {
                        badge.Place(new Vector2(0, 0.5f), new Vector2(m.badge[0] - x0, -(m.badge[1] - gcy)), new Vector2(124, 124), new Vector2(0.5f, 0.5f));
                        badge.localScale = Vector3.one * (m.badge[2] / 124f);
                    }
                }

                // nút tỉ lệ: tròn, trong suốt, chữ "i" trong hốc bên phải
                var rates = block.Find("nut_ti_le") as RectTransform;
                if (rates)
                {
                    float d = m.info[2] * 0.82f;
                    rates.Place(new Vector2(0, 1), new Vector2(m.info[0], -m.info[1]), new Vector2(d, d), new Vector2(0.5f, 0.5f));
                    var le = rates.GetComponent<LayoutElement>();
                    if (le) le.ignoreLayout = true;
                    var btn = rates.GetComponent<SketchButton>();
                    var so = new SerializedObject(btn);
                    so.FindProperty("color").enumValueIndex = (int)BtnColor.Custom;
                    so.FindProperty("baseColor").colorValue = new Color(1, 1, 1, 0);
                    so.ApplyModifiedPropertiesWithoutUndo();
                    var bg = rates.GetComponent<Image>();
                    if (bg) bg.color = new Color(1, 1, 1, 0);
                    if (btn.Label) btn.Label.gameObject.SetActive(false);
                    var icon = rates.Find("i") as RectTransform;
                    if (icon) icon.Place(new Vector2(0.5f, 0.5f), Vector2.zero, Vector2.one * m.info[2] * 0.6f, new Vector2(0.5f, 0.5f));
                }

                // cột cược, khay rương: sát mép màn (cách Margin) và thu nhỏ cho nút không đè viền tủ (đo theo mép các nút, px khối máy)
                var blockRt = (RectTransform)block;
                var bets = block.Find("cot_cuoc") as RectTransform;
                if (bets)
                {
                    bets.localScale = Vector3.one;
                    bets.anchoredPosition = new Vector2(Margin, bets.anchoredPosition.y); // neo trái, gốc trái
                    float right = Edge(blockRt, bets, true), room = m.cabinet[0] - Gap - Margin;
                    if (right - Margin > room) bets.localScale = Vector3.one * (room / (right - Margin));
                }
                var tray = block.Find("khay_ruong") as RectTransform;
                if (tray)
                {
                    tray.localScale = Vector3.one;
                    tray.anchoredPosition = new Vector2(-Margin, tray.anchoredPosition.y); // neo phải, gốc phải
                    float w = blockRt.rect.width, left = Edge(blockRt, tray, false), room = w - Margin - (m.cabinet[2] + Gap);
                    if (w - Margin - left > room) tray.localScale = Vector3.one * (room / (w - Margin - left));
                }

                PrefabUtility.SaveAsPrefabAsset(contents, MachinePath);
                Debug.Log($"[Máy bi] Đặt thân máy vẽ tay vào {MachinePath} ({sprite.rect.width} x {sprite.rect.height})");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }
        }
    }
}
