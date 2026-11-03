// Dải tuyệt kỹ (người dùng chốt 2026-11-03): khung truyện tranh của màn VS cắt thành một hình bình hành nằm ngang màn, giữa sân: viền
// giấy, viền mực, lòng khung theo phe (nền vẽ tay dùng chung hoặc tia, BattleIntro.PaintPanel); mặt tướng ra chiêu to, sát dải, đặt về
// phía phe nó (phe mình bên trái quay phải, địch bên phải quay trái; mặt vẽ tay HeroArt.Face, chưa có thì chân dung phóng cho đầu lấp dải); phía
// kia là khung lời dẫn "Tuyệt kỹ · <tên tướng>" và tên tuyệt kỹ chữ to viền mực.
// Dải trượt vào từ phía phe ra chiêu, mặt trượt chậm hơn dải (có chiều sâu), chữ bật ra, giữ một lúc rồi trượt tiếp sang phía kia.
// Dựng bằng menu "PokiClash/Prefab/Trận: màn VS truyện tranh" (trong lớp phủ của prefab Screens/Battle, tắt sẵn). BattlePlayer chờ dải
// chạy xong mới phát clip tuyệt kỹ.
using System.Collections;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class UltCutIn : MonoBehaviour
    {
        public const float Height = 360, Lean = 90; // cao dải; cạnh bên xiên: đầu trên lệch phải Lean so với đầu dưới
        const float Margin = 26, Paper = 12, FaceSize = 470, FaceInset = 250, TextInset = 190;

        [SerializeField] RectTransform band, faceBox, textBox;
        [SerializeField] PolyGraphic paper, ink, panel;
        [SerializeField] Image art, face;
        [SerializeField] RayGraphic rays;
        [SerializeField] HeroPortrait portrait;
        [SerializeField] RectTransform captionBox;
        [SerializeField] TextMeshProUGUI caption, skill;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi dựng prefab (Editor).
        public void Setup(RectTransform bandRt, PolyGraphic paperPoly, PolyGraphic inkPoly, PolyGraphic panelPoly, Image artImg, RayGraphic rayGfx,
            RectTransform faceRt, Image faceImg, HeroPortrait por, RectTransform textRt, RectTransform captionRt, TextMeshProUGUI captionText,
            TextMeshProUGUI skillText)
        {
            band = bandRt;
            paper = paperPoly;
            ink = inkPoly;
            panel = panelPoly;
            art = artImg;
            rays = rayGfx;
            faceBox = faceRt;
            face = faceImg;
            portrait = por;
            textBox = textRt;
            captionBox = captionRt;
            caption = captionText;
            skill = skillText;
        }

        // stage: khung sân (dải nằm ngang giữa sân); speed: nấc tốc độ trận 1..3 (nhanh hơn thì dải ngắn hơn)
        public IEnumerator Play(HeroDef h, string heroName, int star, string skillName, bool mineSide, RectTransform stage, float speed)
        {
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            float w = Rect.rect.width, hh = Height / 2;
            var mid = Rect.InverseTransformPoint(stage.TransformPoint(stage.rect.center));
            band.anchoredPosition = new Vector2(0, mid.y);

            var pts = new[]
            {
                new Vector2(-w / 2 + Margin, -hh), new Vector2(w / 2 - Margin - Lean, -hh),
                new Vector2(w / 2 - Margin, hh), new Vector2(-w / 2 + Margin + Lean, hh),
            };
            paper.Points = PolyGraphic.Inset(pts, -Paper);
            ink.Points = pts;
            panel.Points = PolyGraphic.Inset(pts, BattleIntro.Border);
            BattleIntro.PaintPanel(panel, art, rays, mineSide);

            // mặt về phía phe ra chiêu, chữ phía kia; nền ảnh và tia tụ ở mặt
            float s = mineSide ? -1 : 1;
            float faceX = s * (w / 2 - FaceInset);
            faceBox.anchoredPosition = new Vector2(faceX, 0);
            faceBox.localScale = new Vector3(mineSide ? -1 : 1, 1, 1);
            float artSide = 2 * (Mathf.Abs(faceX) + w / 2);
            art.rectTransform.sizeDelta = new Vector2(artSide, artSide);
            art.rectTransform.anchoredPosition = new Vector2(faceX, 0);
            ((RectTransform)rays.transform).anchoredPosition = new Vector2(faceX, 0);
            rays.Set(hh * 0.9f, w * 1.6f);
            var sprite = HeroArt.Face(h, star);
            face.gameObject.SetActive(sprite);
            portrait.gameObject.SetActive(!sprite);
            if (sprite)
            {
                Theme.SetSprite(face, sprite);
                face.rectTransform.sizeDelta = new Vector2(FaceSize, FaceSize);
            }
            else HeroArt.FitHead(portrait, h, star, new Vector2(FaceSize, Height - 2 * BattleIntro.Border));
            textBox.anchoredPosition = new Vector2(-s * TextInset, 0);
            caption.text = $"Tuyệt kỹ · {heroName}";
            skill.text = skillName;

            // trượt vào từ phía phe ra chiêu, giữ, trượt tiếp sang phía kia
            float k = 1 / (1 + 0.35f * (Mathf.Clamp(speed, 1, 3) - 1));
            float inT = 0.2f * k, hold = 0.62f * k, outT = 0.2f * k;
            float from = -s * (w + 200), to = s * (w + 200), drift = -s * 70;
            textBox.localScale = Vector3.zero;
            for (float t = 0; ; t += Time.unscaledDeltaTime)
            {
                float a = Mathf.Clamp01(t / inT), o = Mathf.Clamp01((t - inT - hold) / outT);
                float e = 1 - (1 - a) * (1 - a) * (1 - a);
                band.anchoredPosition = new Vector2(from * (1 - e) + to * o * o, mid.y);
                // mặt chậm hơn dải: tới sau, trôi nhẹ suốt lúc giữ
                float lag = 1 - Mathf.Clamp01(t / (inT * 1.6f));
                faceBox.anchoredPosition = new Vector2(faceX + from * 0.25f * lag * lag + drift * Mathf.Clamp01(t / (inT + hold)), 0);
                float p = Mathf.Clamp01((t - inT * 0.6f) / 0.2f);
                textBox.localScale = Vector3.one * (p < 0.6f ? Mathf.Lerp(0, 1.15f, p / 0.6f) : Mathf.Lerp(1.15f, 1, (p - 0.6f) / 0.4f));
                if (o >= 1) break;
                yield return null;
            }
            gameObject.SetActive(false);
        }
    }
}
