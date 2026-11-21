// Chuyển scene: khép mây → Exit scene cũ → gỡ scene cũ → nạp cộng scene mới → Enter(args) → mở mây.
// Yêu cầu đến khi đang chuyển dở thì xếp hàng, chỉ giữ yêu cầu mới nhất.
// Màn che: mây hai bên (CloudCover); sảnh ↔ Nhà và màn tải dùng chuyến tàu qua mây (ShipVoyage.Takes) nếu App đã gắn.
// Màn che chung một giao diện ISceneCover.
using System;
using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;
using PokiClash.Core;

namespace PokiClash
{
    // màn che lúc chuyển scene: Close che kín (rồi mới gỡ scene cũ), Open mở ra màn mới
    public interface ISceneCover
    {
        bool Closed { get; }
        IEnumerator Close();
        IEnumerator Open();
        void Block(bool on);
    }

    public sealed class SceneRouter : MonoBehaviour
    {
        [SerializeField] CloudCover cover;
        [SerializeField] TopBars bars;
        ShipVoyage voyage; // App gắn lúc chạy (prefab riêng)
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

        public void SetVoyage(ShipVoyage v) => voyage = v;

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
            ISceneCover tr = voyage && voyage.Takes(Current, scene) ? voyage : cover;
            if (!tr.Closed)
            {
                if (tr == (ISceneCover)cover)
                {
                    App.Audio?.Play("whoosh");
                    Haptics.Play(Haptic.Transition);
                }
                yield return tr.Close();
            }
            else tr.Block(true);

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
                App.Toasts?.Show(Loc.F("Chưa có scene {0}", scene));
                if (scene != SceneIds.Hub)
                {
                    busy = false;
                    Go(SceneIds.Hub);
                }
                else
                {
                    yield return tr.Open();
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
                PokiClash.Game.LocService.Tree(go); // chữ có sẵn trong scene, trước khi Enter gán chữ của code
                if (!root) root = go.GetComponentInChildren<SceneRoot>(true);
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
            yield return tr.Open();
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
