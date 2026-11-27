// Một ải trên bản đồ đảo hệ (prefab Assets/04 Prefabs/Items/BeAi, dựng bằng menu "PokiClash/Prefab/Sảnh và đảo/Bệ ải (BeAi)"):
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
        // khung chân dung (gốc ở chân tướng): đảo vùng đất gắn hình tướng chạy rig vào đây rồi ẩn ảnh chân dung
        public RectTransform HeroRect => p.hero.Rect;
        public void ShowPortraitBody(bool show) => p.hero.SetBody(show);

        // đảo vùng đất zoom xa: bảng tên phóng to (huy hiệu, tên, cấp đi theo), lùi ra ngoài cho khỏi đè tướng
        Vector2 plateBase;
        int plateSide = 1;
        RectTransform plateHost; // lớp nút khi bảng tên đã tách khỏi bệ (DetachPlate)
        float plateK = 1;

        // bảng tên đã tách đang bật: khung trong lớp nút (để tránh hai bảng chồng nhau)
        public bool PlateRect(out Rect r)
        {
            var pr = p.plate.rectTransform;
            r = default;
            if (!plateHost || pr.parent != plateHost || !pr.gameObject.activeSelf) return false;
            var size = Vector2.Scale(pr.rect.size, pr.localScale);
            r = new Rect((Vector2)pr.localPosition - size * 0.5f, size);
            return true;
        }

        // đổi bên bảng tên (trái ↔ phải của bệ)
        public void FlipPlate()
        {
            plateSide = -plateSide;
            plateBase.x = -plateBase.x;
            SetPlateZoom(plateK);
        }

        public void SetPlateZoom(float k)
        {
            plateK = k;
            var pr = p.plate.rectTransform;
            var local = plateBase + new Vector2(plateSide * (k - 1) * PlateW * 0.5f, 0);
            if (plateHost && pr.parent == plateHost)
            {
                // bảng đã tách: cỡ bảng không dưới bệ thường (bệ mini boss, boss thu nhỏ hơn làm chữ cấp còn 13 px), mép trong bảng sát mép bệ
                var s = Rect.localScale;
                float ps = Mathf.Max(s.x, MinLandPlate), w = Rect.sizeDelta.x;
                pr.localScale = new Vector3(k * ps, k * ps, 1);
                float x = plateSide * ((w * 0.5f - 18) * s.x + k * ps * PlateW * 0.5f);
                pr.localPosition = Rect.localPosition + new Vector3(x, plateBase.y * s.y, 0);
                return;
            }
            pr.localScale = new Vector3(k, k, 1);
            pr.anchoredPosition = local;
        }

        // đảo vùng đất: bảng tên tách khỏi bệ sang lớp nút, làm con cuối để vẽ trên mọi cờ, rương, tướng (cờ chân thấp vẽ sau từng đè
        // lên bảng tên của bệ phía trên, soát UI 2026-11-23). Bảng vẫn bám bệ (SetPlateZoom tính lại từ bệ), xoá lớp nút là xoá theo.
        public void DetachPlate(RectTransform layer)
        {
            var pr = p.plate.rectTransform;
            if (!layer) return;
            if (pr.parent == layer)
            {
                pr.SetAsLastSibling();
                return;
            }
            plateHost = layer;
            pr.SetParent(layer, false);
            pr.anchorMin = pr.anchorMax = new Vector2(0.5f, 0.5f);
            pr.SetAsLastSibling();
            SetPlateZoom(1);
        }

        // đảo vùng đất: bệ ở vùng boss còn mây phủ ẩn bảng tên (huy hiệu, tên, cấp đi theo) và vầng sáng cho đỡ lệnh vẽ
        public void ShowPlate(bool on)
        {
            p.plate.gameObject.SetActive(on);
            if (!on && p.glow) p.glow.gameObject.SetActive(false);
        }

        // Dùng khi dựng prefab (Editor).
        public void Setup(Parts parts) => p = parts;

        // bề ngang bệ, chiều cao tướng trên bệ
        public static float Width(StageKind k) => k == StageKind.Boss ? 210 : k == StageKind.Mini ? 165 : 136;
        public static float HeroHeight(StageKind k) => k == StageKind.Boss ? 290 : k == StageKind.Mini ? 230 : 190; // khung chân dung có lề, thân tướng chiếm khoảng 60%
        // bảng 250 → 270, chữ to hơn (soát UI 2026-11-23: "Mini boss · Cấp 67" trên đảo vùng đất còn 13 px)
        const float PlateW = 270, PlateH = 86, Badge = 66;
        const float MinLandPlate = 1.8f; // đảo vùng đất: cỡ bảng tên nhỏ nhất (bệ thường 360 / 190 ≈ 1,9)

        // bảng tên vươn ra bao xa so với tâm bệ (để chọn bên cho khỏi lòi ra ngoài màn)
        public static float PlateReach(StageKind k) => Width(k) * 0.5f + PlateW - 18;

        public static Color Fill(StageDef st, bool open, bool cleared) =>
            !open ? Theme.Hex("#d9d2c2") : cleared ? Theme.Hex("#c9eab8") : st.kind == StageKind.Boss ? Theme.Hex("#ffb3a3")
            : st.kind == StageKind.Mini ? Theme.Hex("#ffd9a0") : Theme.Hex("#fff3c4");

        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        // pos: chỗ ải trong khung ảnh đảo (gốc trên trái), là tâm mặt bệ; side: bảng tên bên phải (1) hay trái (-1)
        // shadeLocked: ải chưa mở thì tướng thành bóng sẫm (đảo vùng đất để đủ màu, người dùng chốt 2026-11-13)
        // mystery: boss cuối đảo còn giấu (ZoneHeader.BossHidden): bóng sẫm dù đảo để đủ màu, tên "???"
        public void Bind(StageDef st, HeroDef hero, int formStar, int level, bool open, bool cleared, bool current, Vector2 pos, int side,
            Sprite pedestal, Action onClick, bool shadeLocked = true, bool mystery = false)
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
            p.hero.Bind(hero, hh, (shadeLocked && !open) || mystery, formStar);
            var hr = p.hero.Rect;
            hr.anchorMin = hr.anchorMax = new Vector2(0.5f, 0.5f);
            hr.anchoredPosition = new Vector2(0, 0.04f * ph);
            hr.localScale = Vector3.one;
            p.hit.rectTransform.Place(new Vector2(0.5f, 0.5f), new Vector2(0, hh * 0.4f), new Vector2(w, hh + ph * 0.6f));
            p.hit.canvasRenderer.cullTransparentMesh = true; // vùng chạm trong suốt: vẫn nhận chạm, không vẽ (đỡ một lệnh vẽ mỗi bệ)
            Action tap = () =>
            {
                SketchButton.Sound?.Invoke(open ? "click" : "error"); // huy hiệu là nút kit, tự phát tiếng
                onClick();
            };
            p.hitClick.OnClick = tap;

            // bảng tên
            var pr = p.plate.rectTransform;
            pr.Place(new Vector2(0.5f, 0.5f), new Vector2(side * (w * 0.5f + PlateW * 0.5f - 18), hh * 0.24f), new Vector2(PlateW, PlateH));
            plateBase = pr.anchoredPosition;
            plateSide = side;
            pr.localScale = Vector3.one;
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

            p.heroName.text = mystery ? "???" : hero.Form(App.Data.Cfg.formStars, formStar).name;
            p.heroName.color = open ? Theme.Ink : Theme.Ink3;
            p.level.text = st.kind == StageKind.Boss ? Loc.F("Boss · Cấp {0}", level) : st.kind == StageKind.Mini ? Loc.F("Mini boss · Cấp {0}", level) : Loc.F("Cấp {0}", level);
            p.level.color = open ? Theme.Ink2 : Theme.Ink3;
            float tx = Badge - 4;
            p.heroName.rectTransform.Place(new Vector2(0, 1), new Vector2(tx, -8), new Vector2(PlateW - tx - 12, 38), new Vector2(0, 1));
            p.level.rectTransform.Place(new Vector2(0, 0), new Vector2(tx, 10), new Vector2(PlateW - tx - 12, 30), new Vector2(0, 0));
            p.heroName.fontSizeMax = 30;
            p.heroName.fontSizeMin = 18;
            p.level.fontSizeMax = 25;
            p.level.fontSizeMin = 16;
        }
    }
}
