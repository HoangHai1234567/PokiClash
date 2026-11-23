// Sổ tay: cài đặt (âm thanh, rung máy, gợi ý trong trận) có hiệu lực ngay, mục "Gói hỗ trợ"
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
        public override string Title => Loc.T("Sổ tay");

        [Serializable]
        public struct Parts
        {
            public ScrollRect scroll;
            public SketchButton sound, hints;
            public SketchButton haptics; // dòng "Rung" (thêm bằng menu PokiClash/Prefab/Hộp thoại và màn/Sổ tay: thêm dòng Rung)
            public SketchButton lowFlash; // dòng "Giảm nhấp nháy" (menu PokiClash/Prefab/Hộp thoại và màn/Sổ tay: thêm dòng Giảm nhấp nháy)
            public SketchButton language; // dòng "Ngôn ngữ" (menu PokiClash/Prefab/Hộp thoại và màn/Sổ tay: thêm dòng Ngôn ngữ), 2026-11-21
            public SketchButton howTo; // dòng "Cách chơi" (menu PokiClash/Prefab/Hộp thoại và màn/Hướng dẫn: hộp Cách chơi, dòng Sổ tay), 2026-11-22
            public SketchButton story; // dòng "Cốt truyện mở đầu" (menu PokiClash/Prefab/Hộp thoại và màn/Sổ tay: thêm dòng Cốt truyện), 2026-11-23
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
                App.Modals.Confirm(Loc.T("Xoá dữ liệu?"), Loc.T("Mọi tiến trình mất hết: về cấp 1, 10 bi, chọn lại tướng khởi đầu."), Loc.T("Xoá"), () =>
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
            Toggle(p.sound, st.sound, x => st.sound = x);
            Toggle(p.hints, st.hints, x => st.hints = x);
            // bật rung thì rung thử một cú để người chơi biết máy có rung
            if (p.haptics) Toggle(p.haptics, st.haptics, x => st.haptics = x, x => { if (x) Haptics.Play(Haptic.OpenSilver); });
            if (p.lowFlash) Toggle(p.lowFlash, st.lowFlash, x => st.lowFlash = x);
            if (p.language) Language(p.language);
            if (p.howTo)
                p.howTo.SetOnClick(() =>
                {
                    App.Audio.Play("click");
                    HowToDialog.Open();
                });
            // xem lại cốt truyện mở đầu (App/StoryIntro, không ghi cờ); App chưa gắn prefab cốt truyện thì ẩn cả dòng
            if (p.story)
            {
                p.story.transform.parent.gameObject.SetActive(App.I && App.I.storyPrefab);
                p.story.SetOnClick(() => StoryIntro.Replay());
            }

            Packs();
            p.version.text = Loc.F("PokiClash · bản lưu v{0} · {1}", App.Data.Cfg.saveVersion, Application.version);

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
                // mua qua cửa hàng (GD_Claude/26): Thẻ Phiêu Lưu, Bỏ quảng cáo là gói của cửa hàng, trao bằng ShopService (kèm quà của gói)
                packCards[i].Bind(pr, s, now, Store.Ready, () => ShopService.BuyPack(pr.id, ok => Render()));
            }
        }

        // after: gọi sau khi đã lưu và áp cài đặt (giá trị mới)
        void Toggle(SketchButton b, bool value, Action<bool> set, Action<bool> after = null)
        {
            b.name = "nut_" + (value ? "Bật" : "Tắt"); // tên vật giữ tiếng Việt (tour thử tìm theo tên)
            b.SetText(value ? Loc.T("Bật") : Loc.T("Tắt"));
            b.SetRole(value ? BtnColor.Green : BtnColor.Paper);
            b.ClickSound = "toggle";
            b.SetOnClick(() =>
            {
                set(!value);
                App.Save.Save(); // App áp cài đặt ngay khi bản lưu đổi
                after?.Invoke(!value);
                Render();
            });
        }

        // Ngôn ngữ (2026-11-21): nút ghi tên ngôn ngữ đang dùng bằng chính ngôn ngữ đó, bấm thì đổi sang ngôn ngữ kế tiếp
        // (App.SetLanguage dựng lại dữ liệu và nạp lại màn này). Chữ "Ngôn ngữ" của dòng dịch theo bảng như mọi chữ prefab.
        void Language(SketchButton b)
        {
            int i = Array.IndexOf(LocService.Langs, Loc.Lang);
            string next = LocService.Langs[(i + 1) % LocService.Langs.Length];
            b.name = "nut_NgonNgu";
            b.SetText(LangName(Loc.Lang));
            b.SetRole(BtnColor.Blue);
            b.SetOnClick(() => App.SetLanguage(next));
        }

        static string LangName(string lang) => lang == Loc.En ? "English" : "Tiếng Việt";
    }
}
