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
