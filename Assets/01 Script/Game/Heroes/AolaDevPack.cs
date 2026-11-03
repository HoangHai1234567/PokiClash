// Hình tướng aola trên máy thật (prototype). Bước build Editor/AolaDevBuild chép export của mọi tướng
// (anim.json, portrait.png) và hình bộ phận chúng dùng vào StreamingAssets/PokiDev/reskin, giữ nguyên cấu trúc thư mục reskin
// (anim.json trỏ hình bằng đường dẫn tương đối), rồi xoá ngay sau build. Lúc chạy:
// - Android: StreamingAssets nằm trong APK (assets/PokiDev/...), File không đọc được. File nào AolaActor cần thì đọc thẳng
//   từ APK (APK là file zip, Application.dataPath trỏ tới nó) rồi chép ra persistentDataPath/PokiDev/reskin lúc cần.
//   Build mới (stamp khác) thì xoá bản chép cũ. Hình trong APK là PNG 256 màu; anim.json nằm dạng anim.json.gz (APK để
//   StreamingAssets không nén), giải nén lúc chép ra;
// - nền khác: đọc thẳng thư mục StreamingAssets (json không gzip).
// Bản build không mang thư mục này (AolaDevBuild.AllBuilds tắt và không phải Development Build) thì Root trả null.
using System.IO;
using UnityEngine;
#if !UNITY_EDITOR
using System.IO.Compression;
#endif

namespace PokiClash.Game
{
    public static class AolaDevPack
    {
        public const string Folder = "PokiDev", Stamp = "stamp.txt", Gz = ".gz";

#if !UNITY_EDITOR
        static bool checkedRoot;
        static string root; // thư mục reskin đọc được bằng File (null nếu bản build không mang hình)
        static ZipArchive apk; // Android

        static bool InApk => Application.platform == RuntimePlatform.Android;

        public static string Root
        {
            get
            {
                if (checkedRoot) return root;
                checkedRoot = true;
                var pack = Application.streamingAssetsPath + "/" + Folder;
                if (!InApk)
                {
                    root = File.Exists(Path.Combine(pack, Stamp)) ? pack + "/reskin" : null;
                    return root;
                }
                var stampBytes = Read(Stamp);
                if (stampBytes == null)
                {
                    Debug.LogWarning("[Tướng aola] Bản build không mang hình tướng (thiếu StreamingAssets/" + Folder + ").");
                    return null;
                }
                var stamp = System.Text.Encoding.UTF8.GetString(stampBytes).Trim();
                var local = Path.Combine(Application.persistentDataPath, Folder);
                var localStamp = Path.Combine(local, Stamp);
                if (!File.Exists(localStamp) || File.ReadAllText(localStamp).Trim() != stamp)
                {
                    if (Directory.Exists(local)) Directory.Delete(local, true);
                    Directory.CreateDirectory(local);
                    File.WriteAllText(localStamp, stamp);
                }
                root = Path.Combine(local, "reskin").Replace('\\', '/');
                return root;
            }
        }

        // Android: file dưới Root chưa có thì chép từ APK ra (đường dẫn đầy đủ, như AolaActor tính)
        public static void Ensure(string fullPath)
        {
            if (!InApk || Root == null || File.Exists(fullPath)) return;
            var p = fullPath.Replace('\\', '/');
            if (!p.StartsWith(root + "/")) return;
            var rel = "reskin" + p.Substring(root.Length);
            var data = Read(rel) ?? Gunzip(Read(rel + Gz));
            if (data == null) return;
            Directory.CreateDirectory(Path.GetDirectoryName(p));
            File.WriteAllBytes(p, data);
        }

        static byte[] Gunzip(byte[] gz)
        {
            if (gz == null) return null;
            using (var z = new GZipStream(new MemoryStream(gz), CompressionMode.Decompress))
            using (var ms = new MemoryStream())
            {
                z.CopyTo(ms);
                return ms.ToArray();
            }
        }

        // đọc một file của gói trong APK; rel tính từ assets/PokiDev
        static byte[] Read(string rel)
        {
            try
            {
                if (apk == null) apk = new ZipArchive(File.OpenRead(Application.dataPath), ZipArchiveMode.Read);
                var e = apk.GetEntry("assets/" + Folder + "/" + rel);
                if (e == null) return null;
                using (var s = e.Open())
                using (var ms = new MemoryStream())
                {
                    s.CopyTo(ms);
                    return ms.ToArray();
                }
            }
            catch (System.Exception ex)
            {
                Debug.LogWarning("[Tướng aola] Không đọc được " + rel + " trong APK: " + ex.Message);
                return null;
            }
        }
#else
        public static string Root => null;

        public static void Ensure(string fullPath) { }
#endif
    }
}
