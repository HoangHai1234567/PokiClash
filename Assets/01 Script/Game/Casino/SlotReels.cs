// Hình trên ba cuộn của máy quả "Háu Ăn" (lều Hội Máy Quả, GD_Claude/29 mục 6.7; rig ArtGen/Casino/may_qua). Máy là rig AtomSpine vẽ
// bằng DealerRig + DealerLayer (ô cuộn trên ảnh máy để trống); lớp này là các Image uGUI nằm trong ô cuộn, mỗi khung đặt lại theo
// xương của tấm khung cuộn nên máy nhún, nghiêng, bẹp thì hình cuộn méo theo đúng như khung.
// - root: con của lớp vẽ máy (gốc rig ở pivot của lớp), anchoredPosition = chỗ xương `cuon` (tâm ô cuộn), xoay + tỉ lệ theo xương
//   `tam_d` (trục x của xương hướng lên: dài trục x = giãn dọc, dài trục y = phình ngang).
// - Mỗi cuộn một Mask chữ nhật (lòng cuộn) chứa 5 ô hình: hàng −1..3, trượt dọc theo vị trí dừng dạng số thực p:
//   hàng r hiện strip[(⌊p⌋ − 1 + r) mod n] ở độ cao top − (r − (p − ⌊p⌋) + 0,5) × cellH; p giảm dần thì hình chạy XUỐNG; p nguyên =
//   đúng lưới Slots.Sym(cuộn, p, hàng).
// - Chạy nhanh (từ BlurFrom ô / giây): mỗi ô đổi sang hình NHOÈ DỌC của biểu tượng (Leu/sl_bt_<k>_nhoe.png, cao gấp BlurTall lần),
//   các vệt nối nhau thành dải chạy như cuộn máy quả thật; hãm lại gần lúc dừng thì trả hình nét.
// - wins: 9 khung sáng (cuộn × 3 + hàng) cho ô thuộc đường thắng, nhấp nháy.
// Mọi vật dựng sẵn trong prefab (Editor/CasinoSlotMenu.cs); ở đây không sinh GameObject.
using System.Collections.Generic;
using PokiClash.Core;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class SlotReels : MonoBehaviour
    {
        public const int Rows = 5;
        public const float BlurFrom = 9f, BlurTall = 1.9f;   // BlurTall = bề cao ảnh nhoè / ảnh nét (ArtGen/Casino/may_qua/leu/dua_vao_unity.py)

        [SerializeField] DealerRig machine;
        [SerializeField] RectTransform root;
        [SerializeField] Image[] cells;   // [cuộn * Rows + k], k = 0..4 ứng hàng −1..3
        [SerializeField] Image[] wins;    // [cuộn * 3 + hàng]
        [SerializeField] Sprite[] symbols; // theo mã biểu tượng của Slots (0..8)
        [SerializeField] Sprite[] blurred; // cùng thứ tự: hình nhoè dọc lúc cuộn chạy nhanh
        [SerializeField] float cellH = 99, top = 148.5f;
        [SerializeField] string frameBone = "tam_d", centerBone = "cuon";

        SlotsConfig cfg;
        int bFrame = -2, bCenter = -1;
        bool anyWin;

        // Dùng khi dựng prefab (Editor).
        public void Setup(DealerRig rig, RectTransform rootRt, Image[] cellList, Image[] winList, Sprite[] symbolList, Sprite[] blurList,
            float cellHeight, float topY)
        {
            machine = rig; root = rootRt; cells = cellList; wins = winList; symbols = symbolList; blurred = blurList; cellH = cellHeight; top = topY;
        }

        public void Bind(SlotsConfig c) => cfg = c;

        /// <summary>Đặt cuộn ở vị trí dừng p (số thực, đơn vị ô); speed (ô / giây): nhanh thì dùng hình nhoè dọc.</summary>
        public void Set(int reel, float p, float speed)
        {
            if (cfg == null || cells == null || reel < 0 || reel >= cfg.reels.Count) return;
            var strip = cfg.reels[reel].strip;
            int n = strip.Length;
            if (n == 0) return;
            int whole = Mathf.FloorToInt(p);
            float f = p - whole;
            float sp = Mathf.Abs(speed);
            bool blur = sp >= BlurFrom && blurred != null && blurred.Length > 0;
            // hình nét: kéo dãn nhẹ theo tốc độ; hình nhoè: cao gấp BlurTall, càng nhanh vệt càng dài
            float stretch = blur ? BlurTall * (1f + Mathf.Min(0.5f, (sp - BlurFrom) * 0.02f)) : 1f + Mathf.Min(0.35f, sp * 0.04f);
            float alpha = 1f;
            for (int k = 0; k < Rows; k++)
            {
                int i = reel * Rows + k;
                if (i >= cells.Length || !cells[i]) continue;
                var img = cells[i];
                int r = k - 1;
                int sym = strip[((whole - 1 + r) % n + n) % n];
                var set = blur ? blurred : symbols;
                var sprite = set != null && sym >= 0 && sym < set.Length ? set[sym] : null;
                if (img.sprite != sprite) img.sprite = sprite;
                var rt = img.rectTransform;
                var a = rt.anchoredPosition;
                a.y = top - (r - f + 0.5f) * cellH;
                rt.anchoredPosition = a;
                rt.localScale = new Vector3(1, stretch, 1);
                var col = img.color;
                if (!Mathf.Approximately(col.a, alpha))
                {
                    col.a = alpha;
                    img.color = col;
                }
            }
        }

        public void Show(int[] stops)
        {
            if (stops == null) return;
            for (int r = 0; r < stops.Length && r < 3; r++) Set(r, stops[r], 0);
        }

        /// <summary>Bật khung sáng các ô thắng (mã ô = cuộn * 3 + hàng); null = tắt hết.</summary>
        public void Wins(HashSet<int> on)
        {
            anyWin = false;
            if (wins == null) return;
            for (int i = 0; i < wins.Length; i++)
            {
                if (!wins[i]) continue;
                bool w = on != null && on.Contains(i);
                wins[i].gameObject.SetActive(w);
                anyWin |= w;
            }
        }

        void LateUpdate()
        {
            if (anyWin && wins != null)
            {
                // nhấp nháy hai dáng (không mờ dần): 6 lần mỗi giây
                bool hi = Mathf.FloorToInt(Time.time * 6f) % 2 == 0;
                float s = hi ? 1.06f : 0.97f;
                foreach (var w in wins)
                    if (w && w.gameObject.activeSelf) w.rectTransform.localScale = new Vector3(s, s, 1);
            }
            if (!machine || !root || !machine.Ready()) return;
            if (bFrame == -2)
            {
                bFrame = machine.Asset.FindBone(frameBone);
                bCenter = machine.Asset.FindBone(centerBone);
            }
            if (bFrame < 0 || bCenter < 0) return;
            var pose = machine.State.pose;
            pose.BoneMatrix(bFrame, out float a, out float b, out float c, out float d, out _, out _);
            root.anchoredPosition = pose.BonePos(bCenter) * machine.Scale;
            root.localRotation = Quaternion.Euler(0, 0, Mathf.Atan2(c, a) * Mathf.Rad2Deg - 90f);
            root.localScale = new Vector3(Mathf.Sqrt(b * b + d * d), Mathf.Sqrt(a * a + c * c), 1);
        }
    }
}
