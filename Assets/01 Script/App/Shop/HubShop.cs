// Cửa hàng ở sảnh (GD_Claude/26_CuaHang_IAP_QuangCao.md mục 5.1): nút Cửa hàng nằm ở hàng nút đáy (HubScene, phiên khác làm); đây là nút Lọ
// Bi (thanh bi dâng dần) và cột bong bóng ưu đãi đang mở (tối đa 3, đồng hồ bút chì; chạm là mở popup của gói). Không hiện trước khi xong
// chuỗi hướng dẫn bắt buộc. Gắn vào Screens/Hub bằng menu "PokiClash/Prefab/Hộp thoại và màn/Cửa hàng: dựng hết"; tự cập nhật, HubScene không phải gọi.
using System;
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
        }

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
            // bong bóng: ưu đãi đang mở có hẹn giờ (sớm hết trước), rồi chuỗi quà
            var live = Shop.Live(S, now).OrderBy(o => o.until <= 0 ? double.MaxValue : o.until).ToList();
            int i = 0;
            foreach (var o in live)
            {
                if (i >= bubbles.Length) break;
                // nhóm chọn một: chỉ gói đứng đầu nhóm có bong bóng (mở ra thấy cả nhóm)
                var grp = o.pack != null ? App.Data.Cfg.shop.Pack(o.pack)?.group : null;
                if (!string.IsNullOrEmpty(grp) && grp != o.pack) continue;
                Bind(i++, o.uid, o.tpl == "relief" ? "fist" : o.tpl == "hot" ? "flame" : o.tpl == "jump" ? "crown" : o.pack == "starter3" || o.pack == "launch" ? "star" : "coin",
                    o.until, () => ShopSheet.OpenPopup(new Popup { kind = "offer", id = o.uid, free = true }, null));
            }
            if (i < bubbles.Length && Shop.ChainLive(S, now))
                Bind(i++, "chain", "seed", st.chainUntil, () => ShopSheet.OpenPopup(new Popup { kind = "chain", free = true }, null));
            for (; i < bubbles.Length; i++)
            {
                bound[i] = null;
                if (bubbles[i].button && bubbles[i].button.gameObject.activeSelf) bubbles[i].button.gameObject.SetActive(false);
            }
        }

        void Bind(int i, string key, string icon, double until, Action click)
        {
            var b = bubbles[i];
            if (!b.button) return;
            b.button.gameObject.SetActive(true);
            if (bound[i] != key)
            {
                bound[i] = key;
                b.icon.sprite = App.Art.Icon(icon);
                b.button.SetOnClick(click);
            }
            double left = until - SaveService.Now();
            b.timer.text = until <= 0 ? Loc.T("Mới!") : ShortClock(left);
            b.timer.color = until > 0 && left < 3600000 ? Theme.RedD : Theme.Ink;
        }

        static string ShortClock(double ms)
        {
            var t = TimeSpan.FromMilliseconds(Math.Max(0, ms));
            if (t.TotalDays >= 1) return Loc.F("{0}n", (int)t.TotalDays);
            if (t.TotalHours >= 1) return $"{(int)t.TotalHours}:{t.Minutes:00}";
            return $"{t.Minutes}:{t.Seconds:00}";
        }
    }
}
