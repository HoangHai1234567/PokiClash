// Hộp mở rương dùng chung (máy bi, rương AFK, rương sau trận): tên rương, rương lắc rồi bật, thưởng, một nút.
// Hộp là prefab Dialogs/MoRuong (ChestDialog); thưởng đã được cộng vào bản lưu trước khi gọi.
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using UnityEngine;

namespace PokiClash
{
    public static class ChestBox
    {
        // chờ tới khi hộp đóng (bấm nút hoặc chạm ra ngoài). fill: màu thân rương (mặc định theo loại).
        public static IEnumerator Show(string title, SlotKind kind, Color? fill, List<Reward> rewards, string button)
        {
            bool closed = false;
            var dlg = App.Modals.Open<ChestDialog>(() => closed = true);
            yield return dlg.Play(title, kind, fill, rewards, button, () => closed);
        }

        public static IEnumerator Pop(RectTransform rt, float peak)
        {
            for (float t = 0; t < 0.35f; t += Time.unscaledDeltaTime)
            {
                if (!rt) yield break;
                float k = t / 0.35f;
                rt.localScale = Vector3.one * (k < 0.4f ? Mathf.Lerp(1, peak, k / 0.4f) : Mathf.Lerp(peak, 1, (k - 0.4f) / 0.6f));
                yield return null;
            }
            if (rt) rt.localScale = Vector3.one;
        }
    }
}
