// Hộp "Quảng cáo giả lập" (prefab Assets/04 Prefabs/Dialogs/QuangCaoGia, bắt buộc, rộng 620): hình TV, số giây đếm lùi, nút "Bỏ qua".
// Chỉ FakeRewardAds (App/Dev/FakeMonetization.cs, bản dev) mở hộp này; lớp không bọc #if để prefab trong UiKit không mất script
// ở bản phát hành.
using System;
using PokiClash.UI;
using TMPro;
using UnityEngine;

namespace PokiClash
{
    public sealed class FakeAdDialog : Dialog
    {
        [SerializeField] TextMeshProUGUI count;
        [SerializeField] SketchButton skip;

        // Dùng khi nướng prefab (Editor).
        public void Setup(TextMeshProUGUI countText, SketchButton skipButton)
        {
            count = countText;
            skip = skipButton;
        }

        public void Show(int seconds, Action onSkip)
        {
            SetCount(seconds);
            skip.SetOnClick(onSkip);
        }

        public void SetCount(int seconds) => count.text = seconds.ToString();
    }
}
