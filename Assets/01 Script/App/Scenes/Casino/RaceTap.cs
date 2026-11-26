// Vùng chạm của màn Trường đua: con ở vạch xuất phát (chọn để cược), đồng chip mức cược. Dựng sẵn trong prefab (CasinoRaceMenu), RaceScene
// gán index và onTap lúc vào màn.
using System;
using UnityEngine;
using UnityEngine.EventSystems;

namespace PokiClash
{
    public sealed class RaceTap : MonoBehaviour, IPointerClickHandler
    {
        public int index;
        public Action<int> onTap;
        public Action<Vector2> onTapAt; // chỗ chạm trên màn hình (vùng chạm rộng: nơi nhận tự tìm vật gần nhất)

        public void OnPointerClick(PointerEventData e)
        {
            onTap?.Invoke(index);
            onTapAt?.Invoke(e.position);
        }

        // lượt chụp của Editor bấm thay ngón tay
        public void SimulateClick() => onTap?.Invoke(index);
    }
}
