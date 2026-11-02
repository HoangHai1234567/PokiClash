// Gốc của mỗi scene chức năng: khai báo kiểu thanh trên (Hud/Back/None), tên, đích quay lại; giữ canvas nội dung.
// SceneRouter tìm SceneRoot trong scene vừa nạp rồi gọi Enter(args).
// Mỗi scene là một bản sao prefab màn hình (Assets/04 Prefabs/Screens) mang sẵn canvas và vùng nội dung.
using UnityEngine;

namespace PokiClash
{
    public enum TopBar { Hud, Back, None }

    public abstract class SceneRoot : MonoBehaviour
    {
        public const float BarHeight = 150; // chiều cao thanh trên (đã gồm lề), nội dung bắt đầu dưới đó

        public virtual TopBar Bar => TopBar.Back;
        public virtual string Title => name;
        public virtual string BackTo => SceneIds.Hub;

        [SerializeField] PokiCanvas view;
        [SerializeField] RectTransform content;

        public PokiCanvas View => view;
        public RectTransform Bg => view.Bg;
        public RectTransform Frame => view.Frame;

        // vùng nội dung dưới thanh trên
        public RectTransform Content => content;

        // Dùng khi nướng prefab (Editor).
        public void SetupView(PokiCanvas canvas, RectTransform contentRt)
        {
            view = canvas;
            content = contentRt;
        }

        protected virtual void Awake()
        {
            if (App.I == null)
            {
                // chưa có Boot (bấm Play thẳng ở scene này trong Editor): nạp Boot, Boot sẽ mở lại scene này
                App.PendingFirst = gameObject.scene.name;
                UnityEngine.SceneManagement.SceneManager.LoadScene(SceneIds.Boot);
                enabled = false;
                return;
            }
            if (!view) Debug.LogError($"[{name}] Scene chưa có prefab màn hình: chạy PokiClash/Prefab/4. Nướng màn hình.");
        }

        // Gọi sau khi scene nạp xong, khi mây còn che. args do nơi gọi SceneRouter.Go truyền vào.
        public abstract void Enter(object args);

        // Gọi trước khi gỡ scene (mây đã che).
        public virtual void Exit() { }

        // Nút quay lại của thanh trên (hoặc phím Back của Android).
        public virtual void OnBack() => App.Router.Go(BackTo);

        // Dữ liệu lưu đổi (thả bi, nhận AFK...): làm mới phần hiển thị.
        public virtual void Refresh() { }
    }
}
