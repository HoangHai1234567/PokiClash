// Một tướng trên sân đấu (prefab Assets/04 Prefabs/Items/TranTuong): bóng dưới chân, dấu trạng thái trên đầu (sao choáng, lửa
// bỏng, dấu hồi, vòng né). Hình là AolaSticker (Editor lúc Play, bản dev), chèn ngay sau bóng. Body (thân, biểu tượng, lớp nháy)
// là chỗ của hình giữ chỗ vẽ tay cũ, đã bỏ 2026-11-02: các ảnh trong đó luôn tắt, Body chỉ còn làm chỗ neo khi không có aola.
using PokiClash.Core;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class StageActor : MonoBehaviour
    {
        [SerializeField] Image shadow;
        [SerializeField] RectTransform body;
        [SerializeField] Image bodyImg, emblem, flash;
        [SerializeField] RectTransform status;
        [SerializeField] RectTransform stun, burn, regen, evade; // nhóm dấu của từng trạng thái, tắt khi không có
        // độc (2026-11-17): bọt độc xanh, dựng bằng menu "PokiClash/Prefab/Trận/Sàn đấu: dấu trạng thái độc" (StatusPoisonMenu); chưa dựng thì
        // null: sân bỏ qua dấu này (bảng vẫn có chip "Độc")
        [SerializeField] RectTransform poison;

        public RectTransform Rect => (RectTransform)transform;
        public Image Shadow => shadow;
        public RectTransform Body => body;
        public Image BodyImg => bodyImg;
        public Image Emblem => emblem;
        public Image Flash => flash;
        public RectTransform Status => status;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Image shadowImg, RectTransform bodyRt, Image bodyImage, Image emblemImg, Image flashImg, RectTransform statusRt,
            RectTransform stunRt, RectTransform burnRt, RectTransform regenRt, RectTransform evadeRt)
        {
            shadow = shadowImg;
            body = bodyRt;
            bodyImg = bodyImage;
            emblem = emblemImg;
            flash = flashImg;
            status = statusRt;
            stun = stunRt;
            burn = burnRt;
            regen = regenRt;
            evade = evadeRt;
        }

        // Dùng khi dựng dấu độc (Editor).
        public void SetPoison(RectTransform rt) => poison = rt;

        // nhóm dấu của trạng thái (null: prefab chưa có nhóm này)
        public RectTransform Group(StatusId id) =>
            id == StatusId.Stun ? stun : id == StatusId.Burn ? burn : id == StatusId.Regen ? regen : id == StatusId.Poison ? poison :
            id == StatusId.Evade ? evade : null;

        public void HideStatuses()
        {
            stun.gameObject.SetActive(false);
            burn.gameObject.SetActive(false);
            regen.gameObject.SetActive(false);
            evade.gameObject.SetActive(false);
            if (poison) poison.gameObject.SetActive(false);
        }
    }
}
