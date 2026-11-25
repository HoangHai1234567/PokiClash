// Dựng 5 nấc chỉ số hình bình hành (StatPips) lên một dòng có sẵn chữ và số, cho các menu dựng prefab: màn chọn tướng khởi đầu
// (StarterDialogMenu), màn mở khoá tướng (ShopPageMenu). Người dùng 2026-11-24: nền trắng, hình bình hành, Máu xanh lá, Công đỏ, Thủ
// xanh dương. Ảnh nấc 120 x 60 (2x) ở 03 Art/Kit, sinh bằng ArtGen/UI/nac_chi_so/nac_binh_hanh.py.
using PokiClash.UI;
using TMPro;
using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash.EditorTools
{
    public static class StatPipsBuild
    {
        public static readonly string[] Labels = { "Máu", "Công", "Thủ" };
        const string Base = "Assets/03 Art/Kit/nac_binh_hanh.png", Fill = "Assets/03 Art/Kit/nac_binh_hanh_mau.png";
        public const float Ratio = 120f / 60f; // rộng / cao của ảnh nấc

        public static Color FillColor(int k) => k == 0 ? Theme.Hp : k == 1 ? Theme.Red : Theme.Blue;

        // 5 nấc cao h, nấc đầu ở x (mép trái, tính từ mép trái dòng), cách nhau step; k: 0 Máu, 1 Công, 2 Thủ
        public static StatPips Add(RectTransform row, int k, float x, float h, float step, TextMeshProUGUI label, TextMeshProUGUI value)
        {
            var baseSp = AssetDatabase.LoadAssetAtPath<Sprite>(Base);
            var fillSp = AssetDatabase.LoadAssetAtPath<Sprite>(Fill);
            if (!baseSp || !fillSp) Debug.LogError("[Chỉ số] Thiếu ảnh nấc " + Base + " / " + Fill);
            var fills = new Image[5];
            for (int j = 0; j < fills.Length; j++)
            {
                var pip = Img("nac_" + j, row, baseSp, Color.white);
                pip.rectTransform.Place(new Vector2(0, 0.5f), new Vector2(x + step * j, 0), new Vector2(h * Ratio, h), new Vector2(0, 0.5f));
                var fill = Img("mau", pip.transform, fillSp, FillColor(k));
                fill.rectTransform.anchorMin = Vector2.zero;
                fill.rectTransform.anchorMax = Vector2.one;
                fill.rectTransform.pivot = new Vector2(0, 0.5f); // mọc ngang từ mép trái
                fill.rectTransform.offsetMin = fill.rectTransform.offsetMax = Vector2.zero;
                fill.enabled = false;
                fills[j] = fill;
            }
            var sp = row.gameObject.AddComponent<StatPips>();
            sp.label = label;
            sp.value = value;
            sp.fills = fills;
            return sp;
        }

        static Image Img(string name, Transform parent, Sprite s, Color c)
        {
            var go = new GameObject(name, typeof(RectTransform), typeof(Image));
            go.transform.SetParent(parent, false);
            var img = go.GetComponent<Image>();
            img.sprite = s;
            img.color = c;
            img.raycastTarget = false;
            return img;
        }
    }
}
