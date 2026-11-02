// Một thẻ trong mục "Gói hỗ trợ" của Sổ tay (prefab Assets/04 Prefabs/Items/GoiHoTro): hình, tên, mô tả, trạng thái (hạn còn lại),
// nút "Mua" / "Gia hạn" (ẩn khi chưa có cửa hàng hoặc đã mua gói mua một lần).
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class PackCard : MonoBehaviour
    {
        [SerializeField] Image card, icon;
        [SerializeField] TextMeshProUGUI title, desc, status;
        [SerializeField] SketchButton buy;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image cardImg, Image iconImg, TextMeshProUGUI titleText, TextMeshProUGUI descText, TextMeshProUGUI statusText, SketchButton buyBtn)
        {
            card = cardImg;
            icon = iconImg;
            title = titleText;
            desc = descText;
            status = statusText;
            buy = buyBtn;
        }

        // storeReady: đã có cửa hàng (bản dev: cửa hàng giả lập). onBuy: bấm nút mua.
        public void Bind(ProductDef pr, SaveData s, double now, bool storeReady, Action onBuy)
        {
            bool pass = pr.id == "adventure_pass";
            bool owned = pass ? AdGate.PassActive(s, now) : AdGate.NoAds(s);
            name = "goi_" + pr.id;
            card.color = owned ? Theme.Hex("#e6f7d9") : Theme.Paper;
            icon.sprite = App.Art.Icon(pass ? "clock" : "tv"); // giữ material mặc định như code cũ (material = null)
            title.text = pr.name;
            desc.text = pr.desc;
            status.text = pass
                ? owned ? $"Còn {Math.Ceiling((s.ent.passUntil - now) / 86400000)} ngày" : "Chưa có"
                : owned ? "Đã mua" : "Chưa có";
            status.color = owned ? Theme.GreenD : Theme.Ink3;
            bool show = storeReady && (pass || !owned);
            buy.name = "mua_" + pr.id;
            buy.gameObject.SetActive(show);
            if (!show) return;
            buy.SetText(pass && owned ? "Gia hạn" : "Mua");
            buy.SetOnClick(onBuy);
        }
    }
}
