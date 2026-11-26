// Lão Mực ở góc màn trong lớp phủ hướng dẫn (đảo Casino, GD_Claude/31_LaoMuc_Dealer.md mục 4.5; D7 2026-11-27):
// "PokiClash/Prefab/Đảo Casino/Lão Mực: góc màn trong lớp hướng dẫn" vá Kit/HuongDan (không đụng App.prefab: App giữ bản lồng của prefab
// này). Khung "lao_muc_goc" (RectMask2D, gốc giữa mép dưới, cỡ GuideOverlay.MucW x MucH) cắt ngang ngực ông; lớp "truot" để trồi lên;
// rig DealerRig (lao_muc.bytes) hai lớp vẽ sau / trước như ở các lều. Đặt ngay trước ghi chú để ghi chú vẽ đè lên. Chạy lại được.
// GuideMenu.BuildOverlay (dựng lại cả lớp phủ) cũng gọi Add, nên dựng lại không mất Lão Mực.
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class GuideLaoMucMenu
    {
        const string OverlayPath = "Assets/04 Prefabs/Kit/HuongDan.prefab";
        const string RigPath = "Assets/03 Art/Casino/Dealer/lao_muc.bytes";
        const float RigScale = 0.5f; // từ ngực lên (~780 px rig) vừa khung cao MucH
        const float ChestY = 720f;   // điểm rig (px, gốc giữa hai chân, y lên) nằm ở mép dưới khung

        [MenuItem("PokiClash/Prefab/Đảo Casino/Lão Mực: góc màn trong lớp hướng dẫn", priority = 90)]
        public static void Patch()
        {
            var root = PrefabUtility.LoadPrefabContents(OverlayPath);
            try
            {
                var ov = root.GetComponent<GuideOverlay>();
                if (!ov)
                {
                    Debug.LogError("[Lão Mực] Không thấy GuideOverlay trong " + OverlayPath);
                    return;
                }
                var so = new SerializedObject(ov);
                var area = so.FindProperty("area").objectReferenceValue as RectTransform;
                var note = so.FindProperty("note").objectReferenceValue as Component;
                if (!area)
                {
                    Debug.LogError("[Lão Mực] GuideOverlay thiếu area trong " + OverlayPath);
                    return;
                }
                if (!Add(area, ov, note ? note.transform : null)) return;
                PrefabUtility.SaveAsPrefabAsset(root, OverlayPath);
                Debug.Log("[Lão Mực] Đã thêm Lão Mực góc màn vào " + OverlayPath);
            }
            finally
            {
                PrefabUtility.UnloadPrefabContents(root);
            }
        }

        public static bool Add(RectTransform area, GuideOverlay ov, Transform note)
        {
            var rigFile = AssetDatabase.LoadAssetAtPath<TextAsset>(RigPath);
            if (!rigFile)
            {
                Debug.LogWarning("[Lão Mực] Thiếu rig " + RigPath + ": lớp hướng dẫn không có Lão Mực góc màn");
                return false;
            }
            var old = area.Find("lao_muc_goc");
            if (old) Object.DestroyImmediate(old.gameObject);

            var frame = New("lao_muc_goc", area, typeof(RectMask2D));
            frame.anchorMin = frame.anchorMax = new Vector2(0.5f, 0.5f);
            frame.pivot = new Vector2(0.5f, 0);
            frame.sizeDelta = new Vector2(GuideOverlay.MucW, GuideOverlay.MucH);
            if (note && note.parent == area) frame.SetSiblingIndex(note.GetSiblingIndex());

            var slide = New("truot", frame);
            slide.anchorMin = slide.anchorMax = slide.pivot = new Vector2(0.5f, 0);
            slide.sizeDelta = frame.sizeDelta;
            slide.anchoredPosition = Vector2.zero;

            var holder = New("lao_muc", slide);
            holder.anchorMin = holder.anchorMax = holder.pivot = new Vector2(0.5f, 0);

            DealerLayer Layer(string n)
            {
                var rt = New(n, slide, typeof(CanvasRenderer), typeof(DealerLayer));
                rt.anchorMin = rt.anchorMax = rt.pivot = new Vector2(0.5f, 0);
                rt.sizeDelta = new Vector2(1000, 1400);
                rt.anchoredPosition = new Vector2(0, -ChestY * RigScale);
                var l = rt.GetComponent<DealerLayer>();
                l.raycastTarget = false;
                return l;
            }
            var back = Layer("lao_muc_sau");
            var front = Layer("lao_muc_truoc");
            var rig = holder.gameObject.AddComponent<DealerRig>();
            rig.Setup(rigFile, back, front, RigScale);
            ov.SetupMuc(frame, slide, rig);
            frame.gameObject.SetActive(false);
            return true;
        }

        static RectTransform New(string name, Transform parent, params System.Type[] comps)
        {
            var types = new System.Type[comps.Length + 1];
            types[0] = typeof(RectTransform);
            comps.CopyTo(types, 1);
            var go = new GameObject(name, types) { layer = LayerMask.NameToLayer("UI") };
            var rt = (RectTransform)go.transform;
            rt.SetParent(parent, false);
            return rt;
        }
    }
}
