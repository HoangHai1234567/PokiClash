// Một ải trên bản đồ đảo hệ (prefab Assets/04 Prefabs/Items/BeAi, dựng bằng menu "PokiClash/Prefab/Bệ ải (BeAi)"):
// - bệ đất theo đảo (Islands/be_<hệ>, boss: be_<hệ>_boss), tướng chính của ải đứng trên bệ (chưa mở: bóng sẫm);
// - bảng tên bên cạnh: huy hiệu số ải (khoá khi chưa mở, dấu qua khi đã qua, cam là mini boss, đỏ là boss, vương miện trên
//   huy hiệu ải đặc biệt), tên tướng, cấp;
// - vầng sáng nhịp dưới bệ ở ải đang đánh. Chạm bệ, tướng hay bảng tên đều mở ải.
// Mọi phần có sẵn trong prefab; Bind đặt cỡ theo kiểu ải, bật tắt và gán.
using System;
using PokiClash.Core;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ZoneNode : MonoBehaviour
    {
        [Serializable]
        public struct Parts
        {
            public Image glow, pedestal, hit, plate, crown, check, lockIcon;
            public Pulse glowPulse;
            public HeroPortrait hero;
            public SketchButton badge;
            public TextMeshProUGUI heroName, level;
            public ClickCatcher hitClick, plateClick;
        }

        [SerializeField] Parts p;

        public RectTransform Rect => (RectTransform)transform;

        // Dùng khi dựng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        // bề ngang bệ, chiều cao tướng trên bệ
        public static float Width(StageKind k) => k == StageKind.Boss ? 210 : k == StageKind.Mini ? 165 : 136;
        public static float HeroHeight(StageKind k) => k == StageKind.Boss ? 290 : k == StageKind.Mini ? 230 : 190; // khung chân dung có lề, thân tướng chiếm khoảng 60%
        const float PlateW = 250, PlateH = 86, Badge = 66;

        // bảng tên vươn ra bao xa so với tâm bệ (để chọn bên cho khỏi lòi ra ngoài màn)
        public static float PlateReach(StageKind k) => Width(k) * 0.5f + PlateW - 18;

        public static Color Fill(StageDef st, bool open, bool cleared) =>
            !open ? Theme.Hex("#d9d2c2") : cleared ? Theme.Hex("#c9eab8") : st.kind == StageKind.Boss ? Theme.Hex("#ffb3a3")
            : st.kind == StageKind.Mini ? Theme.Hex("#ffd9a0") : Theme.Hex("#fff3c4");

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // pos: chỗ ải trong khung ảnh đảo (gốc trên trái), là tâm mặt bệ; side: bảng tên bên phải (1) hay trái (-1)
        public void Bind(StageDef st, HeroDef hero, int formStar, int level, bool open, bool cleared, bool current, Vector2 pos, int side,
            Sprite pedestal, Action onClick)
        {
            name = "ai_" + st.idx;
            float w = Width(st.kind), hh = HeroHeight(st.kind);
            var rt = Rect;
            rt.anchorMin = rt.anchorMax = new Vector2(0, 1);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = pos;
            rt.sizeDelta = new Vector2(w, w * 0.5f);

            // bệ: tâm elip mặt trên (38% từ đỉnh ảnh) trùng tâm nút
            float ph = pedestal ? w * pedestal.rect.height / pedestal.rect.width : w * 0.625f;
            Theme.SetSprite(p.pedestal, pedestal);
            p.pedestal.enabled = pedestal;
            p.pedestal.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -0.12f * ph), new Vector2(w, ph));
            p.glow.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, -0.1f * ph), new Vector2(w * 1.45f, w * 0.75f));
            p.glow.gameObject.SetActive(current);
            p.glowPulse.enabled = current;

            // tướng đứng giữa mặt bệ (gốc ảnh chân dung ở chân)
            p.hero.Bind(hero, hh, !open, formStar);
            var hr = p.hero.Rect;
            hr.anchorMin = hr.anchorMax = new Vector2(0.5f, 0.5f);
            hr.anchoredPosition = new Vector2(0, 0.04f * ph);
            hr.localScale = Vector3.one;
            p.hit.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, hh * 0.4f), new Vector2(w, hh + ph * 0.6f));
            Action tap = () =>
            {
                SketchButton.Sound?.Invoke(open ? "click" : "error"); // huy hiệu là nút kit, tự phát tiếng
                onClick();
            };
            p.hitClick.OnClick = tap;

            // bảng tên
            var pr = p.plate.rectTransform;
            pr.Place(new Vector2(0.5f, 0.5f), new Vector2(side * (w * 0.5f + PlateW * 0.5f - 18), hh * 0.24f), new Vector2(PlateW, PlateH));
            p.plate.color = open ? Theme.CardFill : new Color(0.93f, 0.9f, 0.84f, 0.92f);
            p.plateClick.OnClick = tap;
            var br = p.badge.Rect;
            br.Place(new Vector2(0, 0.5f), new Vector2(-14, 0), new Vector2(Badge, Badge), new Vector2(0, 0.5f));
            p.badge.SetText(open ? st.idx.ToString() : "");
            p.badge.SetColor(Fill(st, open, cleared));
            p.badge.Label.color = Theme.Ink;
            p.badge.SetOnClick(onClick);
            p.badge.ClickSound = open ? "click" : "error";
            p.lockIcon.gameObject.SetActive(!open);
            Theme.SetSprite(p.lockIcon, Icon("lock"));
            p.lockIcon.rectTransform.Place(new Vector2(0.5f, 0.5f), Vector2.zero, new Vector2(Badge * 0.5f, Badge * 0.5f));
            p.check.gameObject.SetActive(cleared);
            Theme.SetSprite(p.check, Icon("check"));
            p.check.rectTransform.Place(new Vector2(1, 0), new Vector2(6, -6), new Vector2(34, 34), new Vector2(0.5f, 0.5f));
            bool special = st.kind != StageKind.Normal;
            p.crown.gameObject.SetActive(special);
            if (special)
            {
                Theme.SetSprite(p.crown, Icon(st.kind == StageKind.Boss ? "boss" : "crownSm"));
                p.crown.rectTransform.Place(new Vector2(0.5f, 1), new Vector2(0, 26), new Vector2(46, 46), new Vector2(0.5f, 0.5f));
            }

            p.heroName.text = hero.Form(App.Data.Cfg.formStars, formStar).name;
            p.heroName.color = open ? Theme.Ink : Theme.Ink3;
            p.level.text = st.kind == StageKind.Boss ? $"Boss · Cấp {level}" : st.kind == StageKind.Mini ? $"Mini boss · Cấp {level}" : $"Cấp {level}";
            p.level.color = open ? Theme.Ink2 : Theme.Ink3;
            float tx = Badge - 4;
            p.heroName.rectTransform.Place(new Vector2(0, 1), new Vector2(tx, -8), new Vector2(PlateW - tx - 12, 38), new Vector2(0, 1));
            p.level.rectTransform.Place(new Vector2(0, 0), new Vector2(tx, 10), new Vector2(PlateW - tx - 12, 30), new Vector2(0, 0));
        }
    }
}
