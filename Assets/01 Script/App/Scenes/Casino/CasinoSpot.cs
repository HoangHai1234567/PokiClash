// Một điểm chạm trên bản đồ đảo Casino (GD_Claude/29_DaoCasino.md mục 3): vùng chạm trong suốt phủ lên công trình vẽ trên nền, bảng
// tên nổi phía trên (tên, dòng trạng thái: "Mở ở cấp 15", "còn 2 ngày", số mồi…), biểu tượng khoá, chấm đỏ. Prefab Items/DiemCasino
// (menu "PokiClash/Prefab/Đảo Casino/Đảo: dựng màn"); số điểm cố định trong prefab màn Screens/Casino, không sinh lúc chạy.
using System;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class CasinoSpot : MonoBehaviour
    {
        [SerializeField] ClickCatcher hit;
        [SerializeField] Image plate, lockIcon, dot;
        [SerializeField] TextMeshProUGUI title, sub;
        [SerializeField] string id;

        public string Id => id;
        public RectTransform Rt => (RectTransform)transform;

        // Dùng khi dựng prefab (Editor).
        public void Setup(ClickCatcher hitArea, Image plateImg, Image lockImg, Image dotImg, TextMeshProUGUI titleText, TextMeshProUGUI subText)
        {
            hit = hitArea;
            plate = plateImg;
            lockIcon = lockImg;
            dot = dotImg;
            title = titleText;
            sub = subText;
        }

        public void SetId(string spotId) => id = spotId;

        // locked: mờ bảng, hiện khoá; subText rỗng thì ẩn dòng phụ; alert: chấm đỏ
        public void Bind(string name, string subText, bool locked, bool alert, Action onClick)
        {
            if (title) title.text = name;
            if (sub)
            {
                sub.gameObject.SetActive(!string.IsNullOrEmpty(subText));
                sub.text = subText ?? "";
                sub.color = locked ? Theme.Ink3 : Theme.Ink2;
            }
            if (lockIcon) lockIcon.gameObject.SetActive(locked);
            if (dot) dot.gameObject.SetActive(alert && !locked);
            if (plate) plate.color = locked ? new Color(0.93f, 0.9f, 0.84f, 0.92f) : new Color(1f, 0.98f, 0.92f, 0.97f);
            if (hit)
                hit.OnClick = () =>
                {
                    App.Audio.Play("click");
                    onClick?.Invoke();
                };
        }

        public void Show(bool on) => gameObject.SetActive(on);
    }
}
