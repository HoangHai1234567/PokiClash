// Màn VS đầu trận kiểu trang truyện tranh (người dùng chốt 2026-11-03): nền giấy, hai khung chéo viền mực ngăn bằng khe giấy chéo;
// khung trên là đội địch (đỏ), khung dưới là đội bạn (xanh); trong khung là ô mặt từng tướng (VsFace, mặt địch quay trái, mặt phe mình
// lật quay phải) và viên lực chiến cả đội; chữ VS nổ giữa khe; khung lời dẫn vàng góc trên trái ghi đảo, ải, tên ải.
// Nền trong khung là một ảnh vẽ tay dùng chung cho mọi trận (Resources/BattleIntro/vs_nen, tô màu theo phe); chưa có ảnh thì tia
// tập trung vẽ bằng code. Chữ VS là ảnh vẽ tay Resources/BattleIntro/vs_no nếu có, không thì hình nổ của bộ giấy và chữ. Ảnh gen ở
// ArtGen/BattleIntro. Khung, khe và chỗ đặt tính lúc chạy theo cỡ màn.
// Dựng bằng menu "PokiClash/Prefab/Trận: màn VS truyện tranh" (trong lớp phủ của prefab Screens/Battle, tắt sẵn). BattleController gọi
// Play: khung trượt vào theo đường chéo, mặt bật ra, dấu VS đóng xuống rung màn, giữ một lúc rồi hai khung tách lên xuống. Chạm để bỏ qua.
using System;
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BattleIntro : MonoBehaviour, IPointerClickHandler
    {
        // một phe: gốc (trượt vào, tách ra), viền mực và lòng khung (Mask), nền khung (ảnh hoặc tia), hàng ô mặt, viên lực chiến
        [Serializable]
        public struct Side
        {
            public RectTransform root;
            public PolyGraphic ink, panel;
            public Image art;
            public RayGraphic rays;
            public RectTransform row, power;
            public TextMeshProUGUI powerText;
        }

        // một tướng trên màn VS
        public struct Member
        {
            public HeroDef hero;
            public string name;
            public int star, level;
            public bool boss;
        }

        public const float Margin = 22, Gutter = 15, Border = 8; // lề trang, nửa khe giữa, viền mực khung
        public const float Slope = 0.2f; // khe chéo: y = -Slope·x (trái cao, phải thấp)
        public const string ArtBg = "BattleIntro/vs_nen", ArtVs = "BattleIntro/vs_no";
        const float Gap = 34, BossK = 1.18f;
        static readonly float[] Tilt = { -3, 2.5f, -1.5f, 3, -2 };

        // màu phe: lòng khung, nền ảnh tô (nhân màu), tia, lòng ô mặt
        static readonly Color FoePanel = Theme.Hex("#f6b496"), FoeArt = Theme.Hex("#f59a78"), FoeRays = new Color(0.91f, 0.33f, 0.25f, 0.45f),
            FoeTile = Theme.Hex("#ffe1d2");
        static readonly Color MinePanel = Theme.Hex("#a9cff3"), MineArt = Theme.Hex("#86bdf0"), MineRays = new Color(0.29f, 0.56f, 0.85f, 0.45f),
            MineTile = Theme.Hex("#dcecff");

        [SerializeField] CanvasGroup group;
        [SerializeField] Image page;
        [SerializeField] Side mine, foe;
        [SerializeField] RectTransform caption, vs;
        [SerializeField] TextMeshProUGUI title, sub, vsText;
        [SerializeField] Image burst, vsArt;
        [SerializeField] VsFace facePrefab;

        readonly List<(RectTransform rt, float scale, float delay)> pops = new List<(RectTransform, float, float)>();
        bool skip;

        public RectTransform Rect => (RectTransform)transform;
        // prefab đã dựng màn VS kiểu truyện tranh (menu); chưa thì trận bỏ qua màn VS
        public bool Ready => facePrefab && page && foe.root && mine.root;

        // Dùng khi dựng prefab (Editor).
        public void Setup(CanvasGroup cg, Image pageImg, Side mineSide, Side foeSide, RectTransform captionRt, TextMeshProUGUI titleText,
            TextMeshProUGUI subText, RectTransform vsRt, Image burstImg, TextMeshProUGUI vsLabel, Image vsArtImg, VsFace face)
        {
            group = cg;
            page = pageImg;
            mine = mineSide;
            foe = foeSide;
            caption = captionRt;
            title = titleText;
            sub = subText;
            vs = vsRt;
            burst = burstImg;
            vsText = vsLabel;
            vsArt = vsArtImg;
            facePrefab = face;
        }

        public void OnPointerClick(PointerEventData e) => skip = true;

        public IEnumerator Play(string titleText, string subText, IList<Member> mineTeam, IList<Member> foeTeam, int minePower, int foePower)
        {
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            skip = false;
            title.text = titleText;
            sub.text = subText;
            sub.gameObject.SetActive(!string.IsNullOrEmpty(subText));
            Layout();
            pops.Clear();
            Fill(foe, foeTeam, false, foePower, FoeTile, 0.22f);
            Fill(mine, mineTeam, true, minePower, MineTile, 0.3f);
            Paint();
            yield return Animate();
            gameObject.SetActive(false);
        }

        // ---------- dựng theo cỡ màn ----------

        void Layout()
        {
            var r = Rect.rect;
            float l = -r.width / 2 + Margin, rt = r.width / 2 - Margin, t = r.height / 2 - Margin, b = -r.height / 2 + Margin;
            var top = new[] { new Vector2(l, t), new Vector2(rt, t), new Vector2(rt, Cut(rt) + Gutter), new Vector2(l, Cut(l) + Gutter) };
            var bot = new[] { new Vector2(l, Cut(l) - Gutter), new Vector2(rt, Cut(rt) - Gutter), new Vector2(rt, b), new Vector2(l, b) };
            Shape(foe, top, (t + Gutter) / 2 + 20);
            Shape(mine, bot, (b - Gutter) / 2 - 10);
            Pin(caption, new Vector2(l + 26, t - 26));
            Pin(foe.power, new Vector2(rt - 26, t - 30));
            Pin(mine.power, new Vector2(l + 26, b + 30));
            vs.anchoredPosition = Vector2.zero;
        }

        static float Cut(float x) => -Slope * x;

        static void Pin(RectTransform rt, Vector2 pos) => rt.anchoredPosition = pos;

        // khung một phe: viền mực là đa giác khung, lòng khung co vào một viền; hàng mặt ở rowY; nền ảnh vuông lấy tâm ở hàng mặt
        // (chỗ tia tụ lại), đủ to để phủ kín hộp bao của khung
        static void Shape(Side s, Vector2[] pts, float rowY)
        {
            s.ink.Points = pts;
            s.panel.Points = PolyGraphic.Inset(pts, Border);
            float x0 = float.MaxValue, x1 = float.MinValue, y0 = float.MaxValue, y1 = float.MinValue;
            foreach (var p in pts)
            {
                x0 = Mathf.Min(x0, p.x);
                x1 = Mathf.Max(x1, p.x);
                y0 = Mathf.Min(y0, p.y);
                y1 = Mathf.Max(y1, p.y);
            }
            float side = Mathf.Max(x1 - x0, y1 - y0 + 2 * Mathf.Abs(rowY - (y0 + y1) / 2));
            s.art.rectTransform.sizeDelta = new Vector2(side, side);
            s.art.rectTransform.anchoredPosition = new Vector2(0, rowY);
            s.row.anchoredPosition = new Vector2(0, rowY);
            ((RectTransform)s.rays.transform).anchoredPosition = new Vector2(0, rowY);
        }

        // ô mặt một phe xếp hàng ngang (boss to hơn), cỡ co theo số tướng; mặt bật ra lần lượt từ delay
        void Fill(Side s, IList<Member> team, bool mirror, int power, Color tint, float delay)
        {
            for (int i = s.row.childCount - 1; i >= 0; i--) Destroy(s.row.GetChild(i).gameObject);
            s.powerText.text = TeamPower.Text(power);
            int n = team.Count;
            if (n == 0) return;
            float weights = 0;
            foreach (var m in team) weights += m.boss ? BossK : 1;
            float avail = Rect.rect.width - 2 * Margin - 70;
            float unit = Mathf.Min(VsFace.Size, (avail - Gap * (n - 1)) / weights);
            float total = unit * weights + Gap * (n - 1), x = -total / 2;
            for (int i = 0; i < n; i++)
            {
                var m = team[i];
                float size = unit * (m.boss ? BossK : 1);
                var f = Ui.Spawn(facePrefab, s.row);
                f.Bind(m.hero, m.name, m.star, m.level, m.boss, mirror, tint);
                var rt = f.Rect;
                rt.anchoredPosition = new Vector2(x + size / 2, m.boss ? 14 : 0);
                rt.localEulerAngles = new Vector3(0, 0, Tilt[i % Tilt.Length] * (mirror ? -1 : 1));
                rt.localScale = Vector3.zero;
                pops.Add((rt, size / VsFace.Size, delay + i * 0.07f));
                x += size + Gap;
            }
        }

        // nền khung, dấu VS: ảnh vẽ tay nếu có
        void Paint()
        {
            PaintPanel(foe.panel, foe.art, foe.rays, false);
            PaintPanel(mine.panel, mine.art, mine.rays, true);
            var vsSprite = Resources.Load<Sprite>(ArtVs);
            vsArt.gameObject.SetActive(vsSprite);
            burst.gameObject.SetActive(!vsSprite);
            vsText.gameObject.SetActive(!vsSprite);
            if (vsSprite) Theme.SetSprite(vsArt, vsSprite);
        }

        // Lòng một khung truyện theo phe (dùng chung với dải tuyệt kỹ UltCutIn): màu lòng khung; nền là ảnh vẽ tay dùng chung tô màu phe,
        // chưa có ảnh thì tia tập trung.
        public static void PaintPanel(PolyGraphic panel, Image art, RayGraphic rays, bool mineSide)
        {
            var bg = Resources.Load<Sprite>(ArtBg);
            panel.color = mineSide ? MinePanel : FoePanel;
            art.gameObject.SetActive(bg);
            rays.gameObject.SetActive(!bg);
            rays.color = mineSide ? MineRays : FoeRays;
            if (!bg) return;
            Theme.SetSprite(art, bg);
            art.color = mineSide ? MineArt : FoeArt;
        }

        // lòng ô mặt theo phe
        public static Color FaceTint(bool mineSide) => mineSide ? MineTile : FoeTile;

        // ---------- hoạt cảnh ----------

        IEnumerator Animate()
        {
            const float In = 0.32f, Stamp = 0.44f, Hold = 1.5f, Out = 0.32f;
            var r = Rect.rect;
            var dir = new Vector2(1, -Slope).normalized;
            float far = r.width + 300, lift = r.height * 0.62f;
            var pageCol = page.color;
            float t = 0, tOut = -1, shakeAt = -1;
            vs.localScale = Vector3.zero;
            group.alpha = 1;
            App.Audio.Play("whoosh");
            while (true)
            {
                if (tOut < 0 && (t >= Hold || skip && t > 0.25f)) tOut = t;
                float o = tOut < 0 ? 0 : Mathf.Clamp01((t - tOut) / Out);
                float k = BackOut(Mathf.Clamp01(t / In));
                var shake = Vector2.zero;
                if (shakeAt >= 0 && t - shakeAt < 0.25f)
                {
                    float a = 14 * (1 - (t - shakeAt) / 0.25f);
                    shake = new Vector2(UnityEngine.Random.Range(-a, a), UnityEngine.Random.Range(-a, a));
                }
                foe.root.anchoredPosition = -dir * far * (1 - k) + Vector2.up * lift * o * o + shake;
                mine.root.anchoredPosition = dir * far * (1 - k) - Vector2.up * lift * o * o + shake;
                pageCol.a = Mathf.Clamp01(t / 0.12f) * (1 - o);
                page.color = pageCol;
                foreach (var (rt, scale, delay) in pops) rt.localScale = Vector3.one * scale * Pop(Mathf.Clamp01((t - delay) / 0.24f));
                if (t >= Stamp && shakeAt < 0)
                {
                    shakeAt = t;
                    App.Audio.Play("stamp");
                }
                float v = Mathf.Clamp01((t - Stamp) / 0.18f);
                float vsScale = t < Stamp ? 0 : Mathf.Lerp(2.4f, 1, 1 - (1 - v) * (1 - v)) * (1 - 0.5f * o);
                vs.localScale = Vector3.one * vsScale;
                vs.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(-30, -9, v));
                vs.anchoredPosition = shake * 0.5f;
                group.alpha = 1 - Mathf.Clamp01((o - 0.4f) / 0.6f);
                if (o >= 1) break;
                yield return null;
                t += Time.unscaledDeltaTime;
            }
        }

        // vào nhanh, vượt một chút rồi về
        static float BackOut(float x)
        {
            const float c = 1.4f;
            float y = x - 1;
            return 1 + (c + 1) * y * y * y + c * y * y;
        }

        // bật ra: 0 → 1,12 → 1
        static float Pop(float x) => x <= 0 ? 0 : x < 0.6f ? Mathf.Lerp(0, 1.12f, x / 0.6f) : Mathf.Lerp(1.12f, 1, (x - 0.6f) / 0.4f);
    }
}
