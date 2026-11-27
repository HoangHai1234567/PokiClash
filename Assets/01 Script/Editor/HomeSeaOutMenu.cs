// Biển ngoài ảnh nền màn Nhà như sảnh (người dùng 2026-11-27: "sao viền xung quanh có màu xanh gì đây", sau khi biển trong ảnh nền đổi
// sang ảnh biển lát của sảnh, UIHomeSea _TileMix): ngoài ảnh nền trước là màu biển cũ phẳng (nen_hai_ben) nên lộ viền xanh đậm.
// - Lớp "bien_ngoai" (Image lát Islands/sanh_bien) trong the_gioi, ngay sau ảnh nền "nen", tràn ra mỗi bên Reach (2 ô lát 1024): gốc lát
//   trùng góc dưới trái ảnh nền nên ô lát khớp với shader (_TileST = cỡ ảnh nền / 1024); trôi theo bản đồ; tối về đêm như biển trong
//   (DayNight.seaDark).
// - nen_hai_ben (lớp màu phẳng sau cùng, đứng yên theo màn) đổi sang màu trung bình của ảnh biển lát.
// - Lớp nhuộm theo giờ (sang_toi/nhuom) tràn ra Reach như bien_ngoai ("khi drag rìa bị hở": trước chỉ phủ vừa ảnh nền, ra rìa lộ dải
//   mây, biển chưa nhuộm).
// Menu "PokiClash/Prefab/Nhà/Biển ngoài như sảnh" hoặc cờ Temp/home_sea_out.flag (chạy khi Unity không Play, không biên dịch);
// HomeSceneMenu gọi lại sau khi dựng màn Nhà. Chạy lại được.
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class HomeSeaOutMenu
    {
        const string HomePath = "Assets/04 Prefabs/Screens/Home.prefab";
        const string TilePath = "Assets/03 Art/Islands/sanh_bien.png";
        const float Reach = 2048; // tràn ra mỗi bên: số chẵn ô lát 1024 để giữ gốc lát
        static readonly Color Outer = new Color32(16, 221, 251, 255); // màu trung bình sanh_bien

        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/home_sea_out.flag"));
        static double nextPoll;

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating || EditorApplication.isPlayingOrWillChangePlaymode) return;
            if (!File.Exists(Flag)) return;
            File.Delete(Flag);
            Patch();
        }

        [MenuItem("PokiClash/Prefab/Nhà/Biển ngoài như sảnh")]
        public static void Patch()
        {
            var tile = AssetDatabase.LoadAssetAtPath<Sprite>(TilePath);
            if (!tile)
            {
                Debug.LogError("[Nhà] Thiếu " + TilePath);
                return;
            }
            var root = PrefabUtility.LoadPrefabContents(HomePath);
            try
            {
                var world = root.GetComponentsInChildren<RectTransform>(true).FirstOrDefault(t => t.name == "the_gioi");
                var baseRt = world ? world.Find("nen") as RectTransform : null;
                if (!world || !baseRt)
                {
                    Debug.LogError("[Nhà] Screens/Home thiếu the_gioi/nen");
                    return;
                }
                var rt = world.Find("bien_ngoai") as RectTransform;
                if (!rt)
                {
                    var go = new GameObject("bien_ngoai", typeof(RectTransform), typeof(CanvasRenderer), typeof(Image));
                    go.layer = baseRt.gameObject.layer;
                    rt = (RectTransform)go.transform;
                    rt.SetParent(world, false);
                }
                // vẽ ngay trước ảnh nền: đưa về cuối rồi chèn vào chỗ ảnh nền (đặt thẳng chỉ số khi đã đứng trước ảnh nền sẽ đẩy nó ra
                // sau ảnh nền: lần chạy lại 17:32 ngày 2026-11-27 làm biển lát che kín đồng cỏ Nhà)
                rt.SetAsLastSibling();
                rt.SetSiblingIndex(baseRt.GetSiblingIndex());
                // cùng khung ảnh nền, tràn ra mỗi bên Reach: ô lát bắt đầu từ góc dưới trái, cách góc ảnh nền đúng 2 ô
                rt.anchorMin = baseRt.anchorMin;
                rt.anchorMax = baseRt.anchorMax;
                rt.pivot = baseRt.pivot;
                rt.anchoredPosition = baseRt.anchoredPosition;
                rt.sizeDelta = baseRt.sizeDelta;
                rt.offsetMin = baseRt.offsetMin - new Vector2(Reach, Reach);
                rt.offsetMax = baseRt.offsetMax + new Vector2(Reach, Reach);
                rt.localScale = baseRt.localScale;
                var img = rt.GetComponent<Image>();
                img.sprite = tile;
                img.type = Image.Type.Tiled;
                img.pixelsPerUnitMultiplier = 1;
                img.color = Color.white;
                img.raycastTarget = false;

                var sides = root.GetComponentsInChildren<Image>(true).FirstOrDefault(i => i.name == "nen_hai_ben");
                if (sides) sides.color = Outer;

                // lớp nhuộm theo giờ (sang_toi/nhuom, shader nhân màu) tràn ra như bien_ngoai: kéo ra rìa không lộ dải sáng chưa nhuộm
                // (người dùng 2026-11-27 "khi drag rìa bị hở"); tia nắng (Image, không quy uv) và đèn giữ khung ảnh
                var tint = world.Find("sang_toi/nhuom") as RectTransform;
                if (tint)
                {
                    tint.offsetMin = -Vector2.one * Reach;
                    tint.offsetMax = Vector2.one * Reach;
                }

                var dn = root.GetComponentInChildren<DayNight>(true);
                if (dn)
                {
                    var so = new SerializedObject(dn);
                    var arr = so.FindProperty("seaDark");
                    bool has = false;
                    for (int i = 0; i < arr.arraySize; i++) has |= arr.GetArrayElementAtIndex(i).objectReferenceValue == img;
                    if (!has)
                    {
                        arr.arraySize++;
                        arr.GetArrayElementAtIndex(arr.arraySize - 1).objectReferenceValue = img;
                        so.ApplyModifiedPropertiesWithoutUndo();
                    }
                }
                PrefabUtility.SaveAsPrefabAsset(root, HomePath);
                Debug.Log($"[Nhà] Biển ngoài: bien_ngoai {rt.rect.size} (ảnh nền {baseRt.rect.size}), nhuộm {(tint ? tint.rect.size.ToString() : "không có")}, " +
                          $"nen_hai_ben {(sides ? "đổi màu" : "không có")}, " +
                          $"DayNight {(dn ? "seaDark có bien_ngoai" : "không có")}");
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
            SeaWorldMenu.Apply("home"); // biển chung: gốc biển, vật liệu ghim theo thế giới, mép cứng (2026-11-27)
        }
    }
}
