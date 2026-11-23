// Một vùng đảo trên sảnh (prefab mục Items/BangVung; năm bản sao đặt sẵn theo toạ độ ảnh trong Screens/Hub): vùng chạm tròn,
// bảng tên (icon hệ, tên, nhãn độ khó, cấp đề nghị và tiến độ, thanh tiến độ), mũi tên nhún khi là đảo nên đánh.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class HubZone : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Elem zone;
            public Image hit, plaque, icon;
            public ClickCatcher hitClick, plaqueClick;
            public TextMeshProUGUI name, level;
            public DifficultyTag difficulty;
            public ZoneProgressBar bar;
            public GameObject arrow;
        }

        [SerializeField] Parts p;

        public Elem Zone => p.zone;

        // Dùng khi nướng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        // Dùng khi nướng prefab (Editor): icon hệ của vùng (cố định theo vùng).
        public void SetIcon(Sprite s) => p.icon.sprite = s;

        // prog: số ải đã qua; next: cấp địch ải kế tiếp (0: đã qua hết); recommended: đảo nên đánh (hiện mũi tên).
        // 5 đảo chơi song song (2026-11-05) nên bảng ghi cấp ải kế tiếp thay cho khoảng cấp của đảo.
        public void Bind(ZoneDef z, int prog, int next, Progress.Difficulty df, bool recommended)
        {
            p.zone = z.id;
            string key = Keys.Of(z.id);
            name = "o_vung_" + key;
            p.hit.name = "vung_" + key;
            p.plaque.name = "bang_" + key;
            p.plaque.rectTransform.localEulerAngles = new Vector3(0, 0, (z.order % 2 == 1 ? -1 : 1) * 1.5f);
            p.name.text = z.name;
            p.difficulty.Set(df);
            // tên đảo co trong phần bên trái nhãn độ khó (soát UI 2026-11-23: "Đã chinh phục" đè chữ "Thủy")
            var tr = p.difficulty.Rect;
            var nr = p.name.rectTransform;
            float room = p.plaque.rectTransform.rect.width + tr.anchoredPosition.x - tr.rect.width - nr.anchoredPosition.x - 6;
            if (room > 60) nr.sizeDelta = new Vector2(room, nr.sizeDelta.y);
            if (!p.name.enableAutoSizing)
            {
                p.name.fontSizeMax = p.name.fontSize;
                p.name.fontSizeMin = Mathf.Round(p.name.fontSize * 0.7f);
                p.name.enableAutoSizing = true;
            }
            p.level.text = (next > 0 ? Loc.F("Ải kế cấp {0}", next) : Loc.F("Boss cấp {0}", z.levelMax)) + Loc.F(" · {0}/{1} ải", prog, Islands.Size(z.id));
            p.bar.Set(Theme.Of(z.id), prog / (float)Islands.Size(z.id));
            p.arrow.SetActive(recommended);
        }

        public void SetOnClick(Action open)
        {
            p.hitClick.OnClick = open;
            p.plaqueClick.OnClick = open;
        }

        // bảng tên né mép màn, cột thẻ công trình và hàng nút đáy khi kéo bản đồ (soát UI 2026-11-23: nhãn đảo bị cột nút phải che,
        // cắt mép trái). safe, block: khung trên màn (điểm ảnh); bảng dời tối đa maxShift (điểm ảnh màn), xa hơn thì mờ đi.
        Vector2 plaqueBase, plaqueOff;
        bool plaqueBaseSet;
        static readonly Vector3[] Corners = new Vector3[4];

        public void KeepInView(Rect safe, Rect block, float maxShift, float dt)
        {
            var pr = p.plaque.rectTransform;
            if (!plaqueBaseSet)
            {
                plaqueBase = pr.anchoredPosition;
                plaqueBaseSet = true;
            }
            if (!p.plaque.gameObject.activeInHierarchy || !p.plaque.canvas) return;
            var root = p.plaque.canvas.rootCanvas;
            var cam = root.renderMode == RenderMode.ScreenSpaceOverlay ? null : root.worldCamera;
            pr.GetWorldCorners(Corners);
            float x0 = float.MaxValue, y0 = float.MaxValue, x1 = float.MinValue, y1 = float.MinValue;
            foreach (var w in Corners)
            {
                var sp = RectTransformUtility.WorldToScreenPoint(cam, w);
                x0 = Mathf.Min(x0, sp.x);
                x1 = Mathf.Max(x1, sp.x);
                y0 = Mathf.Min(y0, sp.y);
                y1 = Mathf.Max(y1, sp.y);
            }
            var r = Rect.MinMaxRect(x0, y0, x1, y1);
            var d = Vector2.zero;
            if (r.xMin < safe.xMin) d.x = safe.xMin - r.xMin;
            else if (r.xMax > safe.xMax) d.x = safe.xMax - r.xMax;
            if (r.yMin < safe.yMin) d.y = safe.yMin - r.yMin;
            else if (r.yMax > safe.yMax) d.y = safe.yMax - r.yMax;
            var m = new Rect(r.position + d, r.size);
            if (block.width > 0 && m.Overlaps(block))
            {
                // né cột: đường ngắn nhất (sang trái, xuống dưới hay lên trên cột) mà vẫn trong khung an toàn
                float best = block.xMin - m.xMax;
                bool horiz = true;
                float down = block.yMin - m.yMax, up = block.yMax - m.yMin;
                if (Mathf.Abs(down) < Mathf.Abs(best) && m.yMin + down >= safe.yMin)
                {
                    best = down;
                    horiz = false;
                }
                if (Mathf.Abs(up) < Mathf.Abs(best) && m.yMax + up <= safe.yMax)
                {
                    best = up;
                    horiz = false;
                }
                if (horiz) d.x += best;
                else d.y += best;
            }
            // điểm ảnh màn → đơn vị khung của cha bảng tên (bản đồ có zoom nên giới hạn dời tính theo điểm ảnh màn)
            var parent = (RectTransform)pr.parent;
            RectTransformUtility.ScreenPointToLocalPointInRectangle(parent, r.center, cam, out var a);
            RectTransformUtility.ScreenPointToLocalPointInRectangle(parent, r.center + d, cam, out var b);
            RectTransformUtility.ScreenPointToLocalPointInRectangle(parent, r.center + new Vector2(maxShift, 0), cam, out var e);
            float maxLocal = Mathf.Abs(e.x - a.x);
            var need = plaqueOff + (b - a);
            bool far = Mathf.Abs(need.x) > maxLocal * 1.02f || Mathf.Abs(need.y) > maxLocal * 1.02f;
            var want = new Vector2(Mathf.Clamp(need.x, -maxLocal, maxLocal), Mathf.Clamp(need.y, -maxLocal, maxLocal));
            plaqueOff = Vector2.Lerp(plaqueOff, want, 1 - Mathf.Exp(-12f * dt));
            pr.anchoredPosition = plaqueBase + plaqueOff;
            // đảo trôi quá xa (phải dời hơn giới hạn): bảng mờ đi thay vì nằm dở dưới thanh trên, cột nút
            float alpha = Mathf.MoveTowards(plaqueAlpha, far ? 0 : 1, dt * 6);
            if (!Mathf.Approximately(alpha, plaqueAlpha))
            {
                plaqueAlpha = alpha;
                if (plaqueGraphics == null) plaqueGraphics = p.plaque.GetComponentsInChildren<Graphic>(true);
                foreach (var g in plaqueGraphics)
                    if (g) g.canvasRenderer.SetAlpha(alpha);
                p.plaque.raycastTarget = alpha > 0.5f;
            }
        }

        float plaqueAlpha = 1;
        Graphic[] plaqueGraphics;
    }
}
