// Sổ tay: cài đặt (nét vẽ rung, âm thanh, gợi ý trong trận, tốc độ trận mặc định) có hiệu lực ngay, mục "Gói hỗ trợ"
// (Thẻ Phiêu Lưu, Bỏ quảng cáo: trạng thái, hạn còn lại) và xoá dữ liệu có xác nhận.
// Bản dev (Editor, Development Build) có thêm Bảng thử, Chỉnh số, Máy tự chơi (App/Dev/NotebookDev.cs). Tờ giấy cuộn dọc.
// Prefab màn hình Assets/04 Prefabs/Screens/Notebook; thẻ gói là prefab Items/GoiHoTro (PackCard), sinh theo cấu hình.
using System;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class NotebookScene : SceneRoot
    {
        public override string Title => "Sổ tay";

        [Serializable]
        public struct Parts
        {
            public ScrollRect scroll;
            public SketchButton boil, sound, hints;
            public SketchButton[] speed; // ×1, ×2, ×3
            public GameObject packs; // mục "Gói hỗ trợ" (ẩn khi chưa có cửa hàng và chưa có gói)
            public Transform packNote; // dòng "Không bán bi..." trong mục gói: thẻ gói chèn ngay trước
            public GameObject packDevNote; // "Bản thử: cửa hàng giả lập..." (chỉ bản dev)
            public SketchButton reset;
            public TextMeshProUGUI version;
            public NotebookDevPanel dev; // phần dev (chỉ bản dev)
        }

        [SerializeField] Parts p;
        [SerializeField] PackCard packPrefab;

        readonly List<PackCard> packCards = new List<PackCard>();
        bool shown;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts, PackCard pack)
        {
            p = parts;
            packPrefab = pack;
        }

        public override void Enter(object args)
        {
            p.reset.SetOnClick(() =>
                App.Modals.Confirm("Xoá dữ liệu?", $"Mọi tiến trình mất hết: về cấp 1, 10 bi, chỉ có {App.Data.Hero(App.Data.Starters[0]).name}.", "Xoá", () =>
                {
                    App.Save.Reset();
                    App.Router.Go(SceneIds.Hub);
                }));
            Render();
        }

        void Render()
        {
            float keep = shown ? p.scroll.verticalNormalizedPosition : 1;
            shown = true;

            var st = App.Save.Data.settings;
            Toggle(p.boil, st.boil, x => st.boil = x);
            Toggle(p.sound, st.sound, x => st.sound = x);
            Toggle(p.hints, st.hints, x => st.hints = x);
            for (int i = 0; i < p.speed.Length; i++)
            {
                int sp = i + 1;
                p.speed[i].SetRole(st.speed == sp ? BtnColor.Green : BtnColor.Paper);
                p.speed[i].SetOnClick(() =>
                {
                    App.Save.Data.settings.speed = sp;
                    App.Save.Save();
                    Render();
                });
            }

            Packs();
            p.version.text = $"PokiClash · bản lưu v{App.Data.Cfg.saveVersion} · {Application.version}";

#if UNITY_EDITOR || DEVELOPMENT_BUILD
            p.dev.gameObject.SetActive(true);
            NotebookDev.Bind(p.dev, Render);
#else
            p.dev.gameObject.SetActive(false);
#endif
            Canvas.ForceUpdateCanvases();
            p.scroll.verticalNormalizedPosition = keep;
        }

        // Gói hỗ trợ: chỉ bán quyền lợi, không bán bi, đá tiềm năng hay lượt quay máy bi. Chưa có cửa hàng (bản phát hành chưa gắn SDK)
        // thì ẩn, trừ khi đã có gói.
        void Packs()
        {
            var s = App.Save.Data;
            var products = App.Data.Cfg.ads.products;
            bool show = Store.Ready || s.ent != null;
            p.packs.SetActive(show);
            if (!show) return;
#if UNITY_EDITOR || DEVELOPMENT_BUILD
            p.packDevNote.SetActive(true);
#else
            p.packDevNote.SetActive(false);
#endif
            // thẻ sinh một lần (danh sách gói không đổi lúc chạy), các lần sau chỉ gán lại
            while (packCards.Count < products.Count)
            {
                var c = Ui.Spawn(packPrefab, p.packNote.parent);
                c.transform.SetSiblingIndex(p.packNote.GetSiblingIndex());
                packCards.Add(c);
            }
            double now = SaveService.Now();
            for (int i = 0; i < products.Count; i++)
            {
                var pr = products[i];
                packCards[i].Bind(pr, s, now, Store.Ready, () =>
                    Store.Buy(pr.id, ok =>
                    {
                        if (ok) App.Toasts.Show("Đã mua " + pr.name, App.Art.Icon("star"));
                        Render();
                    }));
            }
        }

        void Toggle(SketchButton b, bool value, Action<bool> set)
        {
            string label = value ? "Bật" : "Tắt";
            b.name = "nut_" + label;
            b.SetText(label);
            b.SetRole(value ? BtnColor.Green : BtnColor.Paper);
            b.SetOnClick(() =>
            {
                set(!value);
                App.Save.Save(); // App áp cài đặt ngay khi bản lưu đổi
                Render();
            });
        }
    }
}
