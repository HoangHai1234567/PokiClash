// Nội dung tải sau theo hệ (GD_Claude/27_TaiNoiDungSau.md, người dùng chốt 2026-11-23): 5 gói "noi_dung_<hệ>" gồm đảo, nền trận, nhạc
// đảo, tướng và lính cùng hệ (trừ dòng tướng khởi đầu). Mỗi gói là một nhóm Addressables, nhãn "pack_<hệ>".
//  - Android phát hành (AAB): mỗi nhóm là một asset pack fast-follow của Play Asset Delivery; Play tự tải sau khi cài. Nạp một gói chưa
//    tải thì bộ nạp của Addressables for Android tự xin Play tải (PlayAssetDeliveryAssetBundleProvider); ở đây chỉ hỏi trạng thái để
//    hiện tiến độ, và Prefetch xin tải trước mọi gói (tải ngầm phiên đầu) mà không nạp vào bộ nhớ.
//  - APK thử (bản đủ), Editor: gói nằm sẵn trong StreamingAssets / AssetDatabase, nạp ngay.
//  - Nạp: cả gói một lần (Request), giữ trong bộ nhớ đệm theo tên asset; Get<T>(tên) trả ngay, chưa nạp thì null (nơi gọi dùng ảnh thay
//    thế / chân dung tĩnh rồi hỏi lại, như AolaActor.Ready). Một gói nạp một lúc; Request(first) đẩy gói lên đầu hàng chờ.
//  - Chạy hàng chờ: App.Update gọi Tick mỗi khung.
//  - Gỡ lỗi (Editor): SimulateMissing giả lập gói chưa tải (chờ SimulateSeconds có tiến độ), SimulateOffline giả lập mất mạng.
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;
using UnityEngine.ResourceManagement.ResourceLocations;
using Object = UnityEngine.Object;

namespace PokiClash.Game
{
    public static class ContentPacks
    {
        public static readonly string[] Elems = { "thuy", "hoa", "kim", "moc", "tho" };
        public static string Label(string elem) => "pack_" + elem;
        public static string PackName(string elem) => "noi_dung_" + elem; // tên nhóm Addressables = tên asset pack của Play

        public enum State { Missing, Downloading, Loading, Ready, Failed }

        sealed class Pack
        {
            public string elem;
            public State state = State.Missing;
            public float progress;
            public string error;
            public float simEnd;
            public bool simDone;
            public readonly List<AsyncOperationHandle> handles = new List<AsyncOperationHandle>();
            public readonly List<string> keys = new List<string>();
        }

        static readonly Dictionary<string, Pack> Packs = new Dictionary<string, Pack>();
        static readonly Dictionary<string, Object> Cache = new Dictionary<string, Object>();
        static readonly List<string> Queue = new List<string>();
        static string active;

        public static bool SimulateMissing, SimulateOffline;
        public static float SimulateSeconds = 4;

        // kiểu asset trong gói: Sprite (ảnh đảo, nền trận), AolaAnim (dạng tướng, kéo theo AtomikAsset, atlas, animation), Material
        // (nước, phác vùng đảo), AudioClip (nhạc đảo), Texture2D (atlas dạng aola), SpriteAtlas không cần (Sprite tự kéo atlas)
        static readonly Type[] Types = { typeof(Sprite), typeof(AolaAnim), typeof(Material), typeof(AudioClip), typeof(Texture2D) };

        // (hệ, trạng thái mới): giao diện (sảnh, màn chờ đảo) nghe để vẽ lại
        public static event Action<string, State> Changed;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void Reset()
        {
            Packs.Clear();
            Cache.Clear();
            Queue.Clear();
            active = null;
            Changed = null;
        }

        static Pack P(string elem)
        {
            if (!Packs.TryGetValue(elem, out var p)) Packs[elem] = p = new Pack { elem = elem };
            return p;
        }

        public static bool IsPack(string elem) => !string.IsNullOrEmpty(elem) && Array.IndexOf(Elems, elem) >= 0;

        // gói không có tên (asset bản cài) luôn sẵn
        public static State StateOf(string elem) => IsPack(elem) ? P(elem).state : State.Ready;
        public static bool Ready(string elem) => StateOf(elem) == State.Ready;
        public static float Progress(string elem) => Ready(elem) ? 1 : IsPack(elem) ? P(elem).progress : 1;
        public static string Error(string elem) => IsPack(elem) ? P(elem).error : null;

        public static bool Offline => SimulateOffline || Application.internetReachability == NetworkReachability.NotReachable;

        // Gói đã có trên máy (không cần mạng để nạp). APK đủ, Editor: luôn có.
        public static bool Downloaded(string elem)
        {
            if (!IsPack(elem)) return true;
            if (Application.isEditor) return !SimulateMissing || P(elem).simDone;
#if UNITY_ANDROID && !UNITY_EDITOR
            if (PadMode) return !string.IsNullOrEmpty(UnityEngine.Android.AndroidAssetPacks.GetAssetPackPath(PackName(elem)));
#endif
            return true;
        }

        // Nạp gói vào bộ nhớ: chưa có trong hàng thì thêm cuối; first = đẩy lên đầu (đảo vừa chọn, tướng vừa mở). Failed thì thử lại.
        public static void Request(string elem, bool first = false)
        {
            if (!IsPack(elem)) return;
            var p = P(elem);
            if (p.state == State.Ready || active == elem) return;
            // chưa có trên máy mà mất mạng: lỗi ngay (nơi gọi báo "cần mạng", không báo "đang tải" trước)
            if (!Downloaded(elem) && Offline)
            {
                Queue.Remove(elem);
                Set(p, State.Failed, "offline");
                return;
            }
            if (p.state == State.Failed) Set(p, State.Missing);
            Queue.Remove(elem);
            if (first) Queue.Insert(0, elem);
            else Queue.Add(elem);
        }

        // Tải ngầm (không nạp) mọi gói chưa có trên máy, theo thứ tự cho trước. Chỉ có tác dụng ở bản Play Asset Delivery; fast-follow
        // thường đã tự tải từ lúc cài, gọi lại không hại.
        public static void Prefetch(IEnumerable<string> order)
        {
            if (Application.isEditor)
            {
                if (!SimulateMissing || Offline) return;
                foreach (var e in order)
                {
                    var p = P(e);
                    if (!p.simDone && p.simEnd <= 0) StartSim(p);
                }
                    return;
            }
#if UNITY_ANDROID && !UNITY_EDITOR
            if (!PadMode || Offline) return;
            var names = new List<string>();
            foreach (var e in order)
                if (IsPack(e) && !Downloaded(e)) names.Add(PackName(e));
            if (names.Count == 0) return;
            try
            {
                UnityEngine.Android.AndroidAssetPacks.DownloadAssetPackAsync(names.ToArray(), OnPadInfo);
            }
            catch (InvalidOperationException e)
            {
                Debug.LogWarning("[Gói] Không xin tải trước được: " + e.Message);
            }
#endif
        }

        public static T Get<T>(string key) where T : Object
        {
            if (string.IsNullOrEmpty(key)) return null;
            return Cache.TryGetValue(Key(typeof(T), key), out var o) ? o as T : null;
        }

        static string Key(Type t, string name) => t.Name + ":" + name;

        // Gỡ gói khỏi bộ nhớ (vẫn còn trên máy); lần sau Request thì nạp lại
        public static void Release(string elem)
        {
            if (!IsPack(elem) || active == elem) return;
            var p = P(elem);
            foreach (var k in p.keys) Cache.Remove(k);
            p.keys.Clear();
            foreach (var h in p.handles)
                if (h.IsValid()) Addressables.Release(h);
            p.handles.Clear();
            if (p.state == State.Ready) Set(p, State.Missing);
        }

        static void Set(Pack p, State s, string error = null)
        {
            p.state = s;
            p.error = error;
            if (s == State.Ready) p.progress = 1;
            Changed?.Invoke(p.elem, s);
        }

        // ---- hàng chờ ----

        // App.Update gọi mỗi khung (không tự sinh GameObject: luật PrefabOnlyTests)
        public static void Tick() => Step();

        static void Step()
        {
            if (Application.isEditor && SimulateMissing) TickSim();
            if (active == null)
            {
                if (Queue.Count == 0) return;
                active = Queue[0];
                Queue.RemoveAt(0);
                Begin(P(active));
                return;
            }
            var p = P(active);
            if (p.state == State.Downloading && Application.isEditor && p.simDone) Load(p);
            if (p.state == State.Ready || p.state == State.Failed || p.state == State.Missing) active = null;
        }

        static void Begin(Pack p)
        {
            if (!Downloaded(p.elem))
            {
                if (Offline)
                {
                    Set(p, State.Failed, "offline");
                    return;
                }
                if (Application.isEditor && p.simEnd <= 0) StartSim(p);
#if UNITY_ANDROID && !UNITY_EDITOR
                // bộ nạp PAD tự xin tải khi nạp; xin thêm ở đây để nhận tiến độ (Play gộp hai lời xin cùng gói)
                try { UnityEngine.Android.AndroidAssetPacks.DownloadAssetPackAsync(new[] { PackName(p.elem) }, OnPadInfo); }
                catch (InvalidOperationException) { }
                Load(p);
#endif
                if (p.state != State.Ready && p.state != State.Failed) Set(p, State.Downloading);
                return;
            }
            Load(p);
        }

        // nạp mọi asset của gói (theo từng kiểu; Addressables tự kéo phụ thuộc, bộ nạp PAD tự tải gói nếu chưa có)
        static void Load(Pack p)
        {
            if (p.handles.Count > 0) return; // đang nạp
            Set(p, State.Loading);
            p.progress = Mathf.Max(p.progress, 0.9f);
            string label = Label(p.elem);
            int left = Types.Length;
            bool failed = false;
            string err = null;
            foreach (var t in Types)
            {
                var type = t;
                var locs = Addressables.LoadResourceLocationsAsync(label, type);
                locs.Completed += h =>
                {
                    if (h.Status != AsyncOperationStatus.Succeeded || h.Result == null || h.Result.Count == 0)
                    {
                        Addressables.Release(h);
                        Done();
                        return;
                    }
                    var list = new List<IResourceLocation>(h.Result);
                    Addressables.Release(h);
                    var load = Addressables.LoadAssetsAsync<Object>(list, o =>
                    {
                        if (!o) return;
                        string k = Key(type, o.name);
                        Cache[k] = o;
                        p.keys.Add(k);
                    }, false);
                    p.handles.Add(load);
                    load.Completed += lh =>
                    {
                        if (lh.Status != AsyncOperationStatus.Succeeded)
                        {
                            failed = true;
                            err = lh.OperationException != null ? lh.OperationException.Message : "load";
                        }
                        Done();
                    };
                };
            }

            void Done()
            {
                if (--left > 0) return;
                if (failed)
                {
                    Debug.LogWarning($"[Gói] Nạp gói {p.elem} lỗi: {err}");
                    Release(p.elem);
                    Set(p, State.Failed, Offline ? "offline" : err);
                }
                else Set(p, State.Ready);
            }
        }

        // ---- giả lập (Editor) ----

        static void StartSim(Pack p)
        {
            p.simEnd = Time.realtimeSinceStartup + SimulateSeconds;
            p.progress = 0;
        }

        static void TickSim()
        {
            foreach (var p in Packs.Values)
            {
                if (p.simDone || p.simEnd <= 0) continue;
                if (Offline)
                {
                    p.simEnd = 0;
                    if (p.state == State.Downloading) Set(p, State.Failed, "offline");
                    continue;
                }
                float left = p.simEnd - Time.realtimeSinceStartup;
                p.progress = Mathf.Clamp01(1 - left / Mathf.Max(0.1f, SimulateSeconds)) * 0.9f;
                if (left <= 0) p.simDone = true;
            }
        }

#if UNITY_ANDROID && !UNITY_EDITOR
        static int padMode = -1;

        // bản AAB có asset pack của Unity (bật Split Application Binary); APK đủ thì không
        static bool PadMode
        {
            get
            {
                if (padMode < 0)
                {
                    try { padMode = UnityEngine.Android.AndroidAssetPacks.GetCoreUnityAssetPackNames().Length > 0 ? 1 : 0; }
                    catch (Exception) { padMode = 0; }
                }
                return padMode == 1;
            }
        }

        // tiến độ tải gói (Play gọi lại nhiều lần trong lúc tải)
        static void OnPadInfo(UnityEngine.Android.AndroidAssetPackInfo info)
        {
            foreach (var e in Elems)
            {
                if (PackName(e) != info.name) continue;
                var p = P(e);
                if (info.size > 0 && p.state != State.Ready) p.progress = 0.9f * info.bytesDownloaded / info.size;
                if (info.status == UnityEngine.Android.AndroidAssetPackStatus.Completed && p.state == State.Downloading) p.progress = 0.9f;
            }
        }
#endif
    }
}
