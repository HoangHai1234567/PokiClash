// Chuyển scene: khép mây → Exit scene cũ → gỡ scene cũ → nạp cộng scene mới → Enter(args) → mở mây.
// Yêu cầu đến khi đang chuyển dở thì xếp hàng, chỉ giữ yêu cầu mới nhất.
using System;
using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace PokiClash
{
    public sealed class SceneRouter : MonoBehaviour
    {
        [SerializeField] CloudCover cover;
        [SerializeField] TopBars bars;
        bool busy;
        (string scene, object args)? pending;

        public string Current { get; private set; }
        public SceneRoot CurrentRoot { get; private set; }
        public bool Busy => busy;
        public event Action<SceneRoot> Entered;

        // Dùng khi nướng prefab (Editor).
        public void Setup(CloudCover cloud, TopBars topBars)
        {
            cover = cloud;
            bars = topBars;
        }

        public void Go(string scene, object args = null)
        {
            if (busy)
            {
                pending = (scene, args);
                return;
            }
            StartCoroutine(Run(scene, args));
        }

        public void Back()
        {
            if (CurrentRoot) CurrentRoot.OnBack();
            else Go(SceneIds.Hub);
        }

        IEnumerator Run(string scene, object args)
        {
            busy = true;
            if (!cover.Closed)
            {
                App.Audio?.Play("whoosh");
                yield return cover.Close();
            }
            else cover.Block(true);

            App.Modals?.CloseAll();
            if (CurrentRoot)
            {
                try
                {
                    CurrentRoot.Exit();
                }
                catch (Exception e)
                {
                    Debug.LogException(e);
                }
            }
            if (Current != null)
            {
                var old = SceneManager.GetSceneByName(Current);
                if (old.isLoaded) yield return SceneManager.UnloadSceneAsync(old);
            }
            CurrentRoot = null;
            Current = null;

            var op = Application.CanStreamedLevelBeLoaded(scene) ? SceneManager.LoadSceneAsync(scene, LoadSceneMode.Additive) : null;
            if (op == null)
            {
                Debug.LogError($"[Scene] Không nạp được scene '{scene}' (chưa có trong Build Settings?)");
                App.Toasts?.Show($"Chưa có scene {scene}");
                if (scene != SceneIds.Hub)
                {
                    busy = false;
                    Go(SceneIds.Hub);
                }
                else
                {
                    yield return cover.Open();
                    busy = false;
                }
                yield break;
            }
            yield return op;

            var loaded = SceneManager.GetSceneByName(scene);
            SceneManager.SetActiveScene(loaded);
            SceneRoot root = null;
            foreach (var go in loaded.GetRootGameObjects())
            {
                root = go.GetComponentInChildren<SceneRoot>(true);
                if (root) break;
            }
            Current = scene;
            CurrentRoot = root;
            if (root == null) Debug.LogError($"[Scene] Scene '{scene}' thiếu SceneRoot");

            bars.Show(root ? root.Bar : TopBar.None, root ? root.Title : scene);
            if (root)
            {
                try
                {
                    root.Enter(args);
                }
                catch (Exception e)
                {
                    Debug.LogException(e);
                }
            }
            Entered?.Invoke(root);

            // chờ một chút cho bố cục dựng xong như bản web (60 ms) rồi mới mở mây
            yield return new WaitForSecondsRealtime(0.06f);
            yield return cover.Open();
            busy = false;

            if (pending.HasValue)
            {
                var p = pending.Value;
                pending = null;
                Go(p.scene, p.args);
            }
        }
    }
}
