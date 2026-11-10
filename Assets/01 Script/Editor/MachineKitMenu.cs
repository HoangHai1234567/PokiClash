// Bộ prefab cho ánh sáng, bảng số và màn mở rương nhóm của máy bi (2026-11-10): mã chạy không dựng GameObject (PrefabOnlyTests),
// các lớp sáng, khung chứa, khung cắt, nút sinh bằng Ui.Spawn từ các prefab nhỏ này. Menu dựng (hoặc dựng lại) prefab trong
// Assets/04 Prefabs/Items, gắn vào trường kit của MachineBoard trong Screens/Machine, và ghi viền 9 mảnh của khung bảng số
// pk_bang_so theo MachineScoreBoard.ScreenUv (phần ngoài màn tối).
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class MachineKitMenu
    {
        const string Dir = "Assets/04 Prefabs/Items/";
        const string MachinePath = "Assets/04 Prefabs/Screens/Machine.prefab";
        const string BoardArt = "Assets/03 Art/Pachinko/pk_bang_so.png";

        [MenuItem("PokiClash/Prefab/Máy bi: prefab ánh sáng, bảng số, mở rương", priority = 67)]
        public static void Build()
        {
            var image = Save("AnhMayBi", go =>
            {
                go.AddComponent<CanvasRenderer>();
                var img = go.AddComponent<Image>();
                img.raycastTarget = false;
            }).GetComponent<Image>();
            var mask = Save("MatNaMayBi", go => go.AddComponent<RectMask2D>()).GetComponent<RectMask2D>();
            var button = Save("NutAnhMayBi", go =>
            {
                go.AddComponent<CanvasRenderer>();
                var img = go.AddComponent<Image>();
                img.color = new Color(1, 1, 1, 0);
                img.raycastTarget = true;
                var b = go.AddComponent<Button>();
                b.transition = Selectable.Transition.None;
                b.targetGraphic = img;
                var nav = b.navigation;
                nav.mode = Navigation.Mode.None;
                b.navigation = nav;
            }).GetComponent<Button>();
            var board = Save("BangSoMayBi", go => go.AddComponent<MachineScoreBoard>()).GetComponent<MachineScoreBoard>();
            var open = Save("MoRuongNhom", go =>
            {
                var cv = go.AddComponent<Canvas>();
                cv.overrideSorting = true;
                cv.sortingOrder = 400;
                go.AddComponent<GraphicRaycaster>();
                go.AddComponent<MachineChestOpen>();
            }).GetComponent<MachineChestOpen>();

            var contents = PrefabUtility.LoadPrefabContents(MachinePath);
            try
            {
                var mb = contents.GetComponentInChildren<MachineBoard>(true);
                if (!mb)
                {
                    Debug.LogError($"[Máy bi] Không thấy MachineBoard trong {MachinePath}");
                    return;
                }
                var so = new SerializedObject(mb);
                so.FindProperty("kit.image").objectReferenceValue = image;
                so.FindProperty("kit.mask").objectReferenceValue = mask;
                so.FindProperty("kit.button").objectReferenceValue = button;
                so.FindProperty("kit.scoreBoard").objectReferenceValue = board;
                so.FindProperty("kit.chestOpen").objectReferenceValue = open;
                so.ApplyModifiedPropertiesWithoutUndo();
                PrefabUtility.SaveAsPrefabAsset(contents, MachinePath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(contents);
            }

            // viền 9 mảnh khung bảng số: trái, dưới, phải, trên (px ảnh gốc)
            if (AssetImporter.GetAtPath(BoardArt) is TextureImporter ti)
            {
                ti.GetSourceTextureWidthAndHeight(out int w, out int h);
                var uv = MachineScoreBoard.ScreenUv;
                var border = new Vector4(Mathf.Round(w * uv.x), Mathf.Round(h * (1 - uv.w)), Mathf.Round(w * (1 - uv.z)), Mathf.Round(h * uv.y));
                if (ti.spriteBorder != border)
                {
                    ti.spriteBorder = border;
                    ti.SaveAndReimport();
                }
            }
            else Debug.LogWarning($"[Máy bi] Chưa có {BoardArt}: bảng số dùng nền màu");
            Debug.Log($"[Máy bi] Bộ prefab ánh sáng, bảng số, mở rương vào {Dir} và {MachinePath}");
        }

        static GameObject Save(string name, System.Action<GameObject> fill)
        {
            var go = new GameObject(name, typeof(RectTransform));
            try
            {
                var rt = (RectTransform)go.transform;
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0.5f);
                rt.sizeDelta = new Vector2(100, 100);
                fill(go);
                return PrefabUtility.SaveAsPrefabAsset(go, Dir + name + ".prefab");
            }
            finally
            {
                Object.DestroyImmediate(go);
            }
        }
    }
}
