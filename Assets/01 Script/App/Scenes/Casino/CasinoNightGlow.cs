// Đèn đêm của công trình đảo Casino (GD_Claude/29 mục C8, 2026-11-27; cách của màn Nhà, không quầng sáng): mỗi ảnh tự sáng casino_e_<mã>
// (đèn lồng chợ và lều, đuốc hang, kính tháp máy bi; ArtGen/Casino/night/casino_emit.py) nằm ở lớp "tu_sang" ngay trên lớp nhuộm đêm,
// vật liệu shader PokiClash/UIIslandEmit tự sáng theo giờ (_PokiNight, DayNight đặt). Lớp này nằm khác cha với công trình nên mỗi khung
// chép theo công trình: bật / tắt (lều sự kiện), vị trí, co giãn khi nhún (CasinoBob), độ trong.
// Dựng sẵn trong prefab (menu "PokiClash/Prefab/Đảo Casino/Đảo: dựng màn"); ở đây không sinh gì.
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class CasinoNightGlow : MonoBehaviour
    {
        [SerializeField] Image[] src = new Image[0]; // ảnh công trình
        [SerializeField] Image[] glow = new Image[0]; // ảnh tự sáng cùng khung

        // Dùng khi dựng prefab (Editor).
        public void Setup(Image[] buildings, Image[] glows)
        {
            src = buildings;
            glow = glows;
        }

        void LateUpdate()
        {
            for (int i = 0; i < glow.Length; i++)
            {
                var g = glow[i];
                if (!g) continue;
                var s = i < src.Length ? src[i] : null;
                bool on = s && s.isActiveAndEnabled;
                if (g.gameObject.activeSelf != on) g.gameObject.SetActive(on);
                if (!on) continue;
                RectTransform a = s.rectTransform, b = g.rectTransform;
                b.anchoredPosition = a.anchoredPosition;
                b.localScale = a.localScale;
                b.localRotation = a.localRotation;
                var c = g.color;
                if (!Mathf.Approximately(c.a, s.color.a))
                {
                    c.a = s.color.a;
                    g.color = c;
                }
            }
        }
    }
}
