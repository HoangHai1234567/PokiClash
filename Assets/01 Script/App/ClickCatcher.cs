// Nhận chạm trên một vùng (nền tối của hộp thoại, vùng đảo trên sảnh...): gọi OnClick.
using System;
using UnityEngine;
using UnityEngine.EventSystems;

namespace PokiClash
{
    public sealed class ClickCatcher : MonoBehaviour, IPointerClickHandler
    {
        public Action OnClick;
        public void OnPointerClick(PointerEventData e) => OnClick?.Invoke();
    }
}
