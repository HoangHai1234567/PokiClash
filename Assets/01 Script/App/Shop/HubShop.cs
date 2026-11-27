// Cửa hàng ở sảnh (GD_Claude/26_CuaHang_IAP_QuangCao.md mục 5.1): nút Cửa hàng nằm ở hàng nút đáy (HubScene, phiên khác làm); đây là nút Lọ
// Bi (thanh bi dâng dần) và cột ưu đãi đang mở (tối đa 3; chạm là mở popup của gói). Không hiện trước khi xong chuỗi hướng dẫn bắt buộc.
// Nằm trong App.prefab, vùng an toàn của canvas thanh trên, cạnh giao diện sảnh chung LobbyDock (2026-11-27: sống qua sảnh, Nhà, đảo
// Casino; LobbyDock bật tắt cả cụm). Dựng bằng menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng hết" (hoặc "Cửa hàng: tờ popup + cụm sảnh"); tự cập
// nhật, HubScene không phải gọi.
// Bản 3 (người dùng 2026-11-27: "các icon này khó nhìn quá và xấu ... nổi bật hơn, đẹp hơn và phải có hiệu ứng breath"; mục 17): bỏ đĩa vàng +
// icon vector nhỏ; mỗi ưu đãi là hình gói bản 2 to (hộp quà Nhập Môn, ba lô Khởi Hành, lọ bi...) đứng trên vầng tia kem xoay chậm, thở
// (Breathe, lệch pha), đồng hồ trong viên tối chữ trắng (dưới 1 giờ thì viên đỏ). Lọ Bi: hình lọ, thanh viên tối đầy vàng.
// Ưu đãi động (Bất Ngờ, Nóng, Tiếp Sức, Vượt Mốc...) và Chuỗi Quà mỗi loại một icon riêng (ShopUi.TplArt, uu2_<mã mẫu>.png).
// Bản ô vuông (người dùng 2026-11-27: "to rõ ràng, hình vuông bo tròn và có viền trắng" như cột icon máy bi của Clash of Critters; dựng ở
// Editor/ShopMenu.cs BuildHub): mỗi nút là ô vuông viền trắng giấy (Shop/v3/o_san_vien), lòng ô (o_san_nen) tô màu của gói (ShopHue),
// hình gói to tràn mép trên và vẫn thở; đồng hồ chữ trắng viền mực ở đáy ô (dưới 1 giờ chữ vàng); Lọ Bi giữ thanh đầy trong đáy ô.
using System;
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HubShop : MonoBehaviour
    {
        [Serializable]
        public struct Bubble
        {
            public SketchButton button;
            public Image icon;
            public TextMeshProUGUI timer;
            public Image timerBg; // viên đồng hồ: tối, đỏ khi dưới 1 giờ (bản ô vuông: không có, chữ đổi màu)
            public Image tile; // lòng ô vuông: tô màu của gói
        }

        static readonly Color Navy = new Color32(0x16, 0x14, 0x2a, 0xeb), Urgent = new Color32(0xe8, 0x28, 0x5a, 0xff),
            UrgentText = new Color32(0xff, 0xe1, 0x4a, 0xff);

        [SerializeField] GameObject root;
        [SerializeField] SketchButton shop, piggy;
        [SerializeField] GameObject shopDot;
        [SerializeField] Image piggyFill;
        [SerializeField] TextMeshProUGUI piggyText;
        [SerializeField] Bubble[] bubbles = new Bubble[3];

        float next;
        readonly string[] bound = new string[3];

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;

        // Dùng khi nướng prefab (Editor).
        public void Setup(GameObject rootGo, SketchButton shopBtn, GameObject dot, SketchButton piggyBtn, Image fill, TextMeshProUGUI pText, Bubble[] bubs)
        {
            root = rootGo;
            shop = shopBtn;
            shopDot = dot;
            piggy = piggyBtn;
            piggyFill = fill;
            piggyText = pText;
            bubbles = bubs;
        }

        void Start()
        {
            if (shop) shop.SetOnClick(() => ShopSheet.OpenShop());
            piggy.SetOnClick(() => ShopSheet.OpenPopup(new Popup { kind = "piggy", free = true }, null));
            Refresh();
        }

        void Update()
        {
            if (Time.unscaledTime < next) return;
            next = Time.unscaledTime + 0.5f;
            Refresh();
        }

        void Refresh()
        {
            if (App.Save == null || App.Data == null) return;
            bool on = Tutorial.CoreDone(S);
            if (root.activeSelf != on) root.SetActive(on);
            if (!on) return;
            double now = SaveService.Now();
            var st = Shop.Of(S);
            var c = D.Cfg.shop;
            if (shopDot) shopDot.SetActive(Offers.AnyClaim(S, D, now) || Eggs.BagTotal(S) + st.tickets.Count > 0);
            // Lọ Bi
            double cap = Shop.PiggyCap(S, c);
            float k = cap > 0 ? (float)(st.piggy / cap) : 0;
            piggyFill.fillAmount = k;
            piggyFill.color = k >= 1 ? Theme.Orange : Theme.Yellow;
            piggyText.text = k >= 1 ? Loc.T("Đầy!") : NumFmt.Short((int)st.piggy);
            // ưu đãi đang mở có hẹn giờ (sớm hết trước), rồi chuỗi quà
            var live = Shop.Live(S, now).OrderBy(o => o.until <= 0 ? double.MaxValue : o.until).ToList();
            int i = 0;
            foreach (var o in live)
            {
                if (i >= bubbles.Length) break;
                // nhóm chọn một: chỉ gói đứng đầu nhóm có icon (mở ra thấy cả nhóm)
                var grp = o.pack != null ? App.Data.Cfg.shop.Pack(o.pack)?.group : null;
                if (!string.IsNullOrEmpty(grp) && grp != o.pack) continue;
                var offer = o;
                Bind(i++, o.uid, () => OfferArt(offer), o.until, () => ShopSheet.OpenPopup(new Popup { kind = "offer", id = offer.uid, free = true }, null),
                    ShopHue.Offer(o).fill);
            }
            if (i < bubbles.Length && Shop.ChainLive(S, now))
                Bind(i++, "chain", ChainArt, st.chainUntil, () => ShopSheet.OpenPopup(new Popup { kind = "chain", free = true }, null), ShopHue.Grape.fill);
            for (; i < bubbles.Length; i++)
            {
                bound[i] = null;
                if (bubbles[i].button && bubbles[i].button.gameObject.activeSelf) bubbles[i].button.gameObject.SetActive(false);
            }
        }

        // hình ưu đãi: hình riêng của gói (bản 2) hoặc icon loại ưu đãi (ShopUi.TplArt), không thì hình to theo món như thẻ cửa hàng
        static Sprite OfferArt(ActiveOffer o) => ShopUi.OfferArt(o) ?? ShopPage.ArtFor(Shop.OfferItems(S, D, o));

        // chuỗi quà: icon ba hộp quà xích nối, chưa có ảnh thì hình theo món của ô đang mở
        static Sprite ChainArt()
        {
            var own = ShopUi.TplArt("chain");
            if (own) return own;
            var def = Shop.ChainNow(S, D.Cfg.shop);
            var st = Shop.Of(S);
            var items = def != null && st.chainStep < def.steps.Count ? Shop.Resolve(S, D, def.steps[st.chainStep].items, true, null) : new List<ShopItem>();
            return items.Count > 0 ? ShopPage.ArtFor(items) : ShopUi.Balls(3);
        }

        void Bind(int i, string key, Func<Sprite> art, double until, Action click, Color hue)
        {
            var b = bubbles[i];
            if (!b.button) return;
            b.button.gameObject.SetActive(true);
            if (bound[i] != key)
            {
                bound[i] = key;
                Theme.SetSprite(b.icon, art());
                b.icon.preserveAspect = true;
                b.button.SetOnClick(click);
                if (b.tile) b.tile.color = hue;
            }
            double left = until - SaveService.Now();
            b.timer.text = until <= 0 ? Loc.T("Mới!") : ShopUi.Clock(left); // "1 ngày 22 giờ" / "19:34:05" (bản cũ "1n" khó hiểu)
            bool urgent = until > 0 && left < 3600000;
            b.timer.color = urgent && !b.timerBg ? UrgentText : Color.white;
            if (b.timerBg) b.timerBg.color = urgent ? Urgent : Navy;
        }
    }
}
