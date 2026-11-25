// Một dòng chỉ số tướng: chữ trái, 5 nấc hình bình hành nền trắng, số phải (người dùng 2026-11-24: "để các thanh nền trắng, hình bình
// hành, máu fill xanh lá, công đỏ, thủ xanh dương"). Dùng ở màn chọn tướng khởi đầu (StarterDialog) và màn mở khoá tướng
// (HeroUnlockView). Mỗi nấc: ảnh nền trắng viền mực (03 Art/Kit/nac_binh_hanh) và con là lớp màu (nac_binh_hanh_mau, gạch sáp chéo, màu
// đặt sẵn trong prefab theo chỉ số). Dựng bằng StatPipsBuild (Editor). Set: các nấc đầy lần lượt từ trái, mỗi nấc mọc ngang trong
// 0,08 giây, cách nhau 0,05 giây.
using PokiClash.Core;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class StatPips : MonoBehaviour
    {
        public TextMeshProUGUI label, value;
        public Image[] fills; // lớp màu của từng nấc, gốc ở mép trái

        const float Gap = 0.05f, Grow = 0.08f;
        int want;
        float t = 99, delay;

        public void Set(string text, int n, float delay = 0)
        {
            if (value) value.text = text;
            want = Mathf.Clamp(n, 0, fills.Length);
            this.delay = delay;
            t = 0;
            Apply();
        }

        void Update()
        {
            if (t > delay + fills.Length * Gap + Grow) return;
            t += Time.unscaledDeltaTime;
            Apply();
        }

        void Apply()
        {
            for (int j = 0; j < fills.Length; j++)
            {
                float k = j < want ? Mathf.Clamp01((t - delay - j * Gap) / Grow) : 0;
                fills[j].enabled = k > 0;
                fills[j].rectTransform.localScale = new Vector3(k, 1, 1);
            }
        }

        // nấc 1–5 của Máu, Công, Thủ theo thứ hạng trong các tướng thu phục được cùng độ hiếm (cấp 1, 1 sao): đứng nhóm 20% thấp nhất
        // 1 nấc, nhóm 20% cao nhất 5 nấc (bằng nhau thì tính nửa). Cùng độ hiếm để thanh cho thấy nét riêng (con khiên nhiều Thủ, con
        // đánh nhiều Công); xếp cả dàn thì độ hiếm lấn hết (Thường toàn 1–2 nấc, Huyền thoại 5/5/5). Độ hiếm đã có viên riêng.
        public static int[] RarityPips(GameData d, HeroDef h)
        {
            var me = HeroStats.Compute(d.Cfg, h, 1, 1);
            double[] mine = { me.hp, me.atk, me.def };
            var res = new int[3];
            var below = new float[3];
            int n = 0;
            foreach (var o in d.Heroes)
            {
                if (o.rarity != h.rarity) continue;
                var s = HeroStats.Compute(d.Cfg, o, 1, 1);
                double[] v = { s.hp, s.atk, s.def };
                for (int k = 0; k < 3; k++) below[k] += v[k] < mine[k] ? 1 : v[k] == mine[k] ? 0.5f : 0;
                n++;
            }
            for (int k = 0; k < 3; k++) res[k] = n == 0 ? 3 : Mathf.Clamp(1 + Mathf.FloorToInt(5 * below[k] / n), 1, 5);
            return res;
        }
    }
}
