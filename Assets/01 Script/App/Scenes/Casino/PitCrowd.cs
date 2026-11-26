// Khán giả của Hầm đấu nhún (người dùng 2026-11-26: "làm tiếp cổng sắt mở đóng và khán giả nhún"). Mỗi mảnh là một nhóm khán giả cắt rời
// từ ảnh nền (ArtGen/Casino/ham_dau/tach_lop.py), đặt đè đúng chỗ cũ; nền bên dưới vẫn còn mảng tối của chính nhóm đó nên mảnh chỉ
// nhích LÊN rồi về (không bao giờ xuống dưới chỗ nghỉ): chỗ hở lộ ra đúng màu, không thấy mép.
// Bình thường nhún nhẹ, lệch nhịp nhau; Cheer() (đội mới ra sân, Lão Mực vừa nói) thì nhảy cao và nhanh hơn trong chốc lát.
// Nằm sẵn trong prefab Screens/CasinoUnderground (menu "PokiClash/Prefab/Đảo Casino/Hầm đấu: dựng scene").
using System;
using UnityEngine;

namespace PokiClash
{
    public sealed class PitCrowd : MonoBehaviour
    {
        [Serializable]
        public struct Piece
        {
            public RectTransform rt;
            [Tooltip("Độ nhích lên lớn nhất lúc reo hò (đơn vị canvas)")]
            public float amp;
        }

        [SerializeField] Piece[] pieces;
        [Tooltip("Phần biên độ lúc bình thường so với lúc reo hò")]
        [SerializeField] float idle = 0.42f;

        Vector2[] rest;
        float[] beat, speed;
        float cheer, cheerTill;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Piece[] list) => pieces = list;

        void OnEnable()
        {
            if (pieces == null) return;
            if (rest == null)
            {
                rest = new Vector2[pieces.Length];
                beat = new float[pieces.Length];
                speed = new float[pieces.Length];
                for (int i = 0; i < pieces.Length; i++)
                {
                    rest[i] = pieces[i].rt ? pieces[i].rt.anchoredPosition : Vector2.zero;
                    // lệch nhịp cố định theo thứ tự mảnh (không ngẫu nhiên: ảnh chụp thử lần nào cũng như nhau)
                    beat[i] = (i * 0.37f) % 1f;
                    speed[i] = 0.95f + (i * 0.23f) % 0.4f;
                }
            }
            cheer = 0;
            cheerTill = 0;
        }

        // reo hò trong secs giây: nhảy cao hơn, nhanh hơn
        public void Cheer(float secs = 1.3f) => cheerTill = Mathf.Max(cheerTill, Time.unscaledTime + secs);

        void Update()
        {
            if (rest == null) return;
            float dt = Mathf.Min(0.05f, Time.unscaledDeltaTime);
            cheer = Mathf.MoveTowards(cheer, Time.unscaledTime < cheerTill ? 1 : 0, dt * 4f);
            float k = Mathf.Lerp(idle, 1f, cheer);
            for (int i = 0; i < pieces.Length; i++)
            {
                if (!pieces[i].rt) continue;
                beat[i] += dt * speed[i] * (1f + 0.9f * cheer);
                // nảy: |sin| cho cú chạm đáy gọn, đỉnh tròn
                float hop = Mathf.Abs(Mathf.Sin(beat[i] * Mathf.PI));
                pieces[i].rt.anchoredPosition = rest[i] + new Vector2(0, pieces[i].amp * k * hop);
            }
        }
    }
}
