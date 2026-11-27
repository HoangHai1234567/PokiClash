// Màn VS đầu trận. Kiểu trang truyện tranh (người dùng chốt 2026-11-03), làm lại 2026-11-27 (người dùng: "làm nó epic hơn nữa, các icon
// mặt tướng làm thật đẹp và to hơn, nền trắng đổi sang tối màu, 2 ô xanh đỏ lao chéo từ góc phải trên chéo xuống và từ góc trái dưới chéo
// lên. Khi vào giữa thì chậm lại rồi hiện chữ vs sau đó lại move nhanh ra ngoài màn, chữ vs bay ra rồi chuyển mượt vào màn đấu"):
// - nền tối (mực tím than) thay nền giấy, vệt tốc độ chéo bay theo hướng hai khung lao (nhanh lúc lao, chậm lúc trôi);
// - hai khung chéo viền giấy kem ngăn bằng khe chéo: khung trên đội địch (đỏ tươi), khung dưới đội bạn (xanh tươi). Đường chạy song song
//   với khe giữa hai khung (người dùng sửa cùng ngày: "ô đỏ phải move từ góc trái trên xuống, ô xanh từ góc phải dưới lên", "đường chạy nó
//   sẽ song song với line giữa 2 ô", "bị nhanh quá"): khung đỏ vào từ trái (cao) trượt xuống phải, khung xanh vào từ phải (thấp) trượt
//   lên trái; tới giữa thì trôi chậm (khoảnh khắc chậm), dấu VS đóng xuống: rung màn,
//   sao nổ loang ra, mảnh văng, số lực chiến đếm lên. Hết lúc chậm thì hai khung tăng tốc lao tiếp ra khỏi màn theo hướng cũ, chữ VS phóng
//   to bay ra và mờ dần, nền tối tan dần lộ sân đấu (tướng ra sân từ lúc hai khung bắt đầu lao ra: OnSplit);
// - không còn ô mặt (người dùng cùng ngày: "thay vì icon 2 con cho luôn 2 con nhân vật play animation idle, khi đang ở giữa màn thì play
//   animation tấn công"): mỗi tướng đứng cả thân trong khung phe mình (rig vector AolaSticker, cao 560 khi một tướng, 420 khi hai, vừa bề
//   ngang khi ba), đứng thở; tới giữa màn (lúc trôi chậm) cả hai ra đòn tấn công rồi về dáng đứng; ô tên và cấp dưới chân, nhãn BOSS.
//   Rig chưa có (dạng chưa nhập, gói tải sau chưa về) thì chân dung trọn con. Địch quay trái, phe mình lật quay phải.
// Nền trong khung là ảnh vẽ tay dùng chung (Resources/BattleIntro/vs_nen, tô màu phe); chữ VS là ảnh vẽ tay vs_no (không thì hình nổ + chữ).
// Ảnh gen ở ArtGen/BattleIntro. Khung, khe và chỗ đặt tính lúc chạy theo cỡ màn; vệt tốc độ, sao nổ, mảnh văng dựng lúc chạy lần đầu.
// Dựng bằng menu "PokiClash/Prefab/Trận/Trận: màn VS truyện tranh" (trong lớp phủ của prefab Screens/Battle, tắt sẵn). BattleController gọi
// Play. Chạm để bỏ qua (nhảy tới lúc lao ra).
using System;
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class BattleIntro : MonoBehaviour, IPointerClickHandler
    {
        // một phe: gốc (lao vào, lao ra), viền và lòng khung (Mask), nền khung (ảnh hoặc tia), hàng ô mặt, viên lực chiến
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

        public const float Margin = 22, Gutter = 15, Border = 8; // lề trang, nửa khe giữa, viền khung
        public const float Slope = 0.2f; // khe chéo: y = -Slope·x (trái cao, phải thấp)
        public const string ArtBg = "BattleIntro/vs_nen", ArtVs = "BattleIntro/vs_no";
        const float Gap = 34, BossK = 1.18f;
        static readonly float[] Tilt = { -3, 2.5f, -1.5f, 3, -2 };

        // màu phe cho dải tuyệt kỹ (UltCutIn, PaintPanel): lòng khung, nền ảnh tô (nhân màu), tia, lòng ô mặt
        static readonly Color FoePanel = Theme.Hex("#f6b496"), FoeArt = Theme.Hex("#f59a78"), FoeRays = new Color(0.91f, 0.33f, 0.25f, 0.45f),
            FoeTile = Theme.Hex("#ffe1d2");
        static readonly Color MinePanel = Theme.Hex("#a9cff3"), MineArt = Theme.Hex("#86bdf0"), MineRays = new Color(0.29f, 0.56f, 0.85f, 0.45f),
            MineTile = Theme.Hex("#dcecff");

        // màn VS bản tối (2026-11-27): nền mực, khung đỏ / xanh tươi viền giấy kem, ô mặt sáng hơn khung một bậc
        static readonly Color Dark = new Color(0.075f, 0.063f, 0.141f, 0.97f), Rim = Theme.Hex("#fdf5e7");
        static readonly Color FoeHot = Theme.Hex("#e8473a"), FoeHotArt = Theme.Hex("#ff6650"), FoeHotRays = new Color(0.55f, 0.08f, 0.1f, 0.5f),
            FoeHotTile = Theme.Hex("#ffd6c8");
        static readonly Color MineHot = Theme.Hex("#3a7fe0"), MineHotArt = Theme.Hex("#5596ff"), MineHotRays = new Color(0.07f, 0.2f, 0.55f, 0.5f),
            MineHotTile = Theme.Hex("#d4e6ff");
        static readonly Color[] ChipColors = { Theme.Hex("#ffd23f"), Theme.Hex("#fdf5e7"), Theme.Hex("#ff6650"), Theme.Hex("#5596ff") };

        // ô đứng lớn nhất của một tướng theo số tướng một phe (ba tướng thì vừa bề ngang)
        static float MaxFace(int n) => n <= 1 ? 560 : n == 2 ? 420 : VsFace.Size;

        // nhịp (giây): nền tối hiện, hai khung lao vào, trôi chậm (dấu VS đóng ngay đầu lúc chậm), lao ra, nền tan. Bản đầu 0,34 / 1,15 /
        // 0,3 s bị chê nhanh quá; bản 0,6 / 1,8 / 0,5 s thì người dùng dặn "làm tốc độ lao vào nhanh hơn lao ra cũng nhanh hơn sẽ tạo
        // feel tốt hơn": lao vào, lao ra gắt (lao vào hãm kiểu luỹ thừa 4, lao ra tăng tốc luỹ thừa 3), giữ khoảng chậm ở giữa
        const float FadeIn = 0.16f, DashStart = 0.06f, DashIn = 0.3f, Slow = 1.7f, DashOut = 0.26f, BgOut = 0.5f, VsOut = 0.55f;
        const float Drift = 44; // quãng trôi chậm mỗi bên tâm (đơn vị canvas)
        const float RigFrame = 2.2f; // khung chụp rig (chiều cao dáng đứng): đủ cho dáng đứng, đòn đánh vươn xa thì AolaSticker tự nới
        const float AttackLag = 0.18f; // phe mình ra đòn trễ hơn phe địch một nhịp
        // chữ VS (người dùng 2026-11-27: "chữ VS to hơn và có hiệu ứng rung mạnh hơn"): cỡ đứng gấp VsBig lần cỡ dựng sẵn; dấu đóng rung
        // màn mạnh, lâu (boss mạnh hơn); trong lúc chậm chữ run liên tục (xê dịch, xoay nhẹ) như chữ VS truyện tranh
        const float VsBig = 1.5f, StampShake = 0.5f, VsJitter = 6, VsJitterRot = 2.2f;

        // chỗ xuất phát của khung đỏ so với chỗ đứng (khung xanh ngược lại): song song với khe giữa (y = −Slope·x), bên trái phía trên;
        // lao ra thì đi tiếp sang phải phía dưới. Đủ xa để cả khung khuất màn
        Vector2 Far
        {
            get
            {
                float d = Rect.rect.width + 80;
                return new Vector2(-d, d * Slope);
            }
        }

        [SerializeField] CanvasGroup group;
        [SerializeField] Image page;
        [SerializeField] Side mine, foe;
        [SerializeField] RectTransform caption, vs;
        [SerializeField] TextMeshProUGUI title, sub, vsText;
        [SerializeField] Image burst, vsArt;
        [SerializeField] VsFace facePrefab;

        readonly List<(RectTransform rt, float scale, float delay)> pops = new List<(RectTransform, float, float)>();
        bool skip;

        // rig của từng tướng: dựng dần mỗi khung một cái (AolaSticker.CanBuildNow), xoá khi màn VS xong
        struct RigSlot
        {
            public VsFace face;
            public Member member;
            public bool mineSide;
            public float scale; // tỉ lệ ô trên màn (cỡ ô / VsFace.Size)
            public AolaSticker sticker;
            public float born;
            public bool tried;
        }

        readonly List<RigSlot> rigs = new List<RigSlot>();

        // vệt tốc độ, sao nổ, mảnh văng (dựng lúc chạy lần đầu)
        RectTransform streakLayer, fxLayer;
        readonly List<(RectTransform rt, Image img, Vector2 pos, float speed, int side)> streaks = new List<(RectTransform, Image, Vector2, float, int)>();
        Image ring;
        readonly List<(RectTransform rt, Image img, Vector2 vel, float spin)> chips = new List<(RectTransform, Image, Vector2, float)>();
        CanvasGroup vsGroup;
        int minePower, foePower;

        // gọi một lần lúc hai khung bắt đầu lao ra (BattleController cho hai tướng ra sân đúng lúc này, sân lộ dần sau màn VS); tự xoá sau khi gọi
        public Action OnSplit;

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

        void OnDisable() => ClearRigs();

        public IEnumerator Play(string titleText, string subText, IList<Member> mineTeam, IList<Member> foeTeam, int minePower, int foePower)
        {
            gameObject.SetActive(true);
            transform.SetAsLastSibling();
            skip = false;
            title.text = titleText;
            sub.text = subText;
            sub.gameObject.SetActive(!string.IsNullOrEmpty(subText));
            this.minePower = minePower;
            this.foePower = foePower;
            Layout();
            pops.Clear();
            ClearRigs();
            Fill(foe, foeTeam, false, FoeHotTile, 0.16f);
            Fill(mine, mineTeam, true, MineHotTile, 0.22f);
            Paint();
            BuildFx();
            yield return Animate();
            ClearRigs();
            gameObject.SetActive(false);
            var late = OnSplit; // bị tắt giữa chừng: vẫn cho tướng ra sân
            OnSplit = null;
            late?.Invoke();
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

        // khung một phe: viền là đa giác khung, lòng khung co vào một viền; hàng mặt ở rowY; nền ảnh vuông lấy tâm ở hàng mặt
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
        void Fill(Side s, IList<Member> team, bool mirror, Color tint, float delay)
        {
            for (int i = s.row.childCount - 1; i >= 0; i--) Destroy(s.row.GetChild(i).gameObject);
            s.powerText.text = "0";
            int n = team.Count;
            if (n == 0) return;
            float weights = 0;
            foreach (var m in team) weights += m.boss ? BossK : 1;
            float avail = Rect.rect.width - 2 * Margin - 70;
            float unit = Mathf.Min(MaxFace(n), (avail - Gap * (n - 1)) / weights);
            float total = unit * weights + Gap * (n - 1), x = -total / 2;
            for (int i = 0; i < n; i++)
            {
                var m = team[i];
                float size = unit * (m.boss ? BossK : 1);
                var f = Ui.Spawn(facePrefab, s.row);
                f.Bind(m.hero, m.name, m.star, m.level, m.boss, mirror, tint);
                f.Body(m.hero, m.star);
                var rt = f.Rect;
                rt.anchoredPosition = new Vector2(x + size / 2, m.boss ? 14 : 0);
                rt.localEulerAngles = new Vector3(0, 0, Tilt[i % Tilt.Length] * (mirror ? -1 : 1));
                rt.localScale = Vector3.zero;
                pops.Add((rt, size / VsFace.Size, DashStart + delay + i * 0.09f));
                rigs.Add(new RigSlot { face = f, member = m, mineSide = mirror, scale = size / VsFace.Size });
                x += size + Gap;
            }
        }

        // nền khung, dấu VS: ảnh vẽ tay nếu có; bản tối: khung đỏ / xanh tươi, viền giấy kem, nền trang mực
        void Paint()
        {
            PaintPanel(foe.panel, foe.art, foe.rays, false);
            PaintPanel(mine.panel, mine.art, mine.rays, true);
            Hot(foe, FoeHot, FoeHotArt, FoeHotRays);
            Hot(mine, MineHot, MineHotArt, MineHotRays);
            var c = Dark;
            c.a = 0;
            page.color = c;
            var vsSprite = Resources.Load<Sprite>(ArtVs);
            vsArt.gameObject.SetActive(vsSprite);
            burst.gameObject.SetActive(!vsSprite);
            vsText.gameObject.SetActive(!vsSprite);
            if (vsSprite) Theme.SetSprite(vsArt, vsSprite);
        }

        static void Hot(Side s, Color panel, Color art, Color rays)
        {
            s.panel.color = panel;
            s.art.color = art;
            s.rays.color = rays;
            s.ink.color = Rim;
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

        // ---------- rig cả thân ----------

        // dựng rig một tướng: đứng cả thân trong ô đứng (đỉnh hình gần mép trên, chân trên ô tên), hình rộng thì không phóng quá bề ngang ô
        // nhiều. Ảnh chụp theo cỡ trên màn (rồi thu lại bằng localScale) cho nét. Không mặt nạ: đòn đánh vươn ra ngoài ô thoải mái.
        static AolaSticker BuildRig(RigSlot r)
        {
            var form = HeroArt.FormOf(r.member.hero, r.member.star).aola;
            if (string.IsNullOrEmpty(form) || !AolaActor.Ready(form)) return null;
            var art = r.face.ArtRect;
            var box = r.face.ArtBox;
            float k = Mathf.Max(0.2f, r.scale);
            float shotH = box.y * 0.9f * k; // cỡ chụp ước lượng (đơn vị màn), chỉnh tỉ lệ sau khi đọc khung bao dáng đứng
            var s = AolaSticker.TryCreate(art, r.member.hero, form, shotH, false, 1024, RigFrame);
            if (s == null) return null;
            s.HideShadow();
            float top = 1, mx = 0.45f;
            if (s.Extent(StageView.Idle, out float emx, out float etop, out _) && etop > 0.2f)
            {
                top = etop;
                mx = Mathf.Max(0.1f, emx);
            }
            float want = Mathf.Min(0.9f * box.y / Mathf.Max(1, top), 0.62f * box.x / mx); // chiều cao dáng đứng trong ô (đơn vị ô)
            s.Rect.localScale = Vector3.one * (want / shotH);
            s.Rect.anchoredPosition = new Vector2(0, FootLift);
            r.face.UseRig(true);
            return s;
        }

        const float FootLift = 22; // chân cao hơn đáy vùng hình một chút, khỏi lấp ô tên

        // dáng đứng; tới attackAt (giữa màn) ra đòn tấn công một lượt rồi về dáng đứng
        void TickRigs(float t, float attackAt)
        {
            bool built = false;
            for (int i = 0; i < rigs.Count; i++)
            {
                var r = rigs[i];
                if (!r.tried && !built && AolaSticker.CanBuildNow)
                {
                    r.tried = true;
                    built = true;
                    r.sticker = BuildRig(r);
                    r.born = t;
                    rigs[i] = r;
                }
                if (r.sticker == null) continue;
                float at = attackAt + (r.mineSide ? AttackLag : 0), since = t - at;
                if (since >= 0 && since < r.sticker.Duration(StageView.Attack))
                    r.sticker.Show(StageView.Attack, since, false, 1, false, 0);
                else r.sticker.Show(StageView.Idle, t - r.born + i * 0.37f, true, 1, false, 0);
            }
        }

        void ClearRigs()
        {
            foreach (var r in rigs) r.sticker?.Destroy();
            rigs.Clear();
        }

        // ---------- vệt tốc độ, sao nổ, mảnh văng ----------

        void BuildFx()
        {
            if (!vsGroup)
            {
                vsGroup = vs.GetComponent<CanvasGroup>();
                if (!vsGroup) vsGroup = vs.gameObject.AddComponent<CanvasGroup>();
                vsGroup.blocksRaycasts = false;
            }
            if (!streakLayer)
            {
                streakLayer = NewLayer("vet_toc_do", page.transform.GetSiblingIndex() + 1);
                for (int i = 0; i < 18; i++)
                {
                    var img = NewImage(streakLayer, "vet", Rim);
                    streaks.Add((img.rectTransform, img, Vector2.zero, 0, i % 2));
                }
            }
            if (!fxLayer)
            {
                fxLayer = NewLayer("no_vs", vs.GetSiblingIndex());
                ring = NewImage(fxLayer, "sao_loang", Rim);
                Theme.SetSprite(ring, Sketch.Burst);
                ring.preserveAspect = false;
                ring.rectTransform.sizeDelta = new Vector2(520, 360);
                for (int i = 0; i < 16; i++)
                {
                    var img = NewImage(fxLayer, "manh", ChipColors[i % ChipColors.Length]);
                    chips.Add((img.rectTransform, img, Vector2.zero, 0));
                }
            }
            // vệt: rải khắp màn, nghiêng theo hướng lao (dọc khe giữa); nửa trên đi theo khung đỏ (sang phải), nửa dưới theo khung xanh (sang trái)
            var r = Rect.rect;
            var path = Far;
            float ang = Mathf.Atan2(path.y, path.x) * Mathf.Rad2Deg;
            for (int i = 0; i < streaks.Count; i++)
            {
                var s = streaks[i];
                float len = UnityEngine.Random.Range(160f, 520f), w = UnityEngine.Random.Range(5f, 12f);
                s.rt.sizeDelta = new Vector2(len, w);
                s.rt.localEulerAngles = new Vector3(0, 0, ang);
                float y = s.side == 0 ? UnityEngine.Random.Range(0f, r.height / 2) : UnityEngine.Random.Range(-r.height / 2, 0f);
                s.pos = new Vector2(UnityEngine.Random.Range(-r.width / 2, r.width / 2), y);
                s.speed = UnityEngine.Random.Range(0.75f, 1.25f);
                s.img.color = Fade(Rim, 0);
                streaks[i] = s;
            }
            ring.color = Fade(Rim, 0);
            foreach (var c in chips) c.img.color = Fade(c.img.color, 0);
        }

        RectTransform NewLayer(string name, int sibling)
        {
            var rt = (RectTransform)new GameObject(name, typeof(RectTransform)).transform;
            rt.SetParent(transform, false);
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = rt.offsetMax = Vector2.zero;
            rt.SetSiblingIndex(Mathf.Clamp(sibling, 0, transform.childCount - 1));
            return rt;
        }

        static Image NewImage(Transform parent, string name, Color c)
        {
            var img = new GameObject(name, typeof(RectTransform), typeof(Image)).GetComponent<Image>();
            img.transform.SetParent(parent, false);
            img.raycastTarget = false;
            img.color = c;
            return img;
        }

        static Color Fade(Color c, float a)
        {
            c.a = a;
            return c;
        }

        void Shatter()
        {
            ring.rectTransform.localScale = Vector3.one * 0.6f;
            ring.color = Fade(Rim, 0.9f);
            for (int i = 0; i < chips.Count; i++)
            {
                var c = chips[i];
                float a = (i / (float)chips.Count + UnityEngine.Random.Range(-0.03f, 0.03f)) * Mathf.PI * 2;
                c.vel = new Vector2(Mathf.Cos(a), Mathf.Sin(a)) * UnityEngine.Random.Range(900f, 1600f);
                c.spin = UnityEngine.Random.Range(-720f, 720f);
                c.rt.anchoredPosition = Vector2.zero;
                c.rt.sizeDelta = new Vector2(UnityEngine.Random.Range(14f, 26f), UnityEngine.Random.Range(28f, 46f));
                c.rt.localEulerAngles = new Vector3(0, 0, a * Mathf.Rad2Deg);
                c.img.color = Fade(ChipColors[i % ChipColors.Length], 1);
                chips[i] = c;
            }
        }

        void TickFx(float dt, float since, float streakSpeed, float streakAlpha)
        {
            // sao nổ loang ra rồi mờ trong 0,4 giây
            if (since >= 0)
            {
                float u = Mathf.Clamp01(since / 0.4f);
                ring.rectTransform.localScale = Vector3.one * VsBig * Mathf.Lerp(0.6f, 2.6f, 1 - (1 - u) * (1 - u));
                ring.color = Fade(Rim, 0.9f * (1 - u));
                float fade = Mathf.Clamp01(1 - (since - 0.25f) / 0.35f);
                for (int i = 0; i < chips.Count; i++)
                {
                    var c = chips[i];
                    c.vel *= Mathf.Exp(-4.5f * dt);
                    c.rt.anchoredPosition += c.vel * dt;
                    c.rt.localEulerAngles += new Vector3(0, 0, c.spin * dt);
                    c.img.color = Fade(c.img.color, fade);
                    chips[i] = c;
                }
            }
            // vệt tốc độ: bay theo hướng lao, quấn quanh màn
            var r = Rect.rect;
            var dir = Far.normalized;
            float wrapX = r.width / 2 + 300, wrapY = r.height / 2 + 300;
            for (int i = 0; i < streaks.Count; i++)
            {
                var s = streaks[i];
                var v = (s.side == 0 ? -dir : dir) * streakSpeed * s.speed;
                s.pos += v * dt;
                if (s.pos.x < -wrapX) s.pos.x += 2 * wrapX;
                if (s.pos.x > wrapX) s.pos.x -= 2 * wrapX;
                if (s.pos.y < -wrapY) s.pos.y += 2 * wrapY;
                if (s.pos.y > wrapY) s.pos.y -= 2 * wrapY;
                s.rt.anchoredPosition = s.pos;
                s.img.color = Fade(Rim, streakAlpha * (0.6f + 0.4f * s.speed));
                streaks[i] = s;
            }
        }

        // ---------- hoạt cảnh ----------

        IEnumerator Animate()
        {
            // khung đỏ vào từ trái phía trên, ra ở phải phía dưới (dọc khe giữa); khung xanh ngược lại
            var far = Far;
            var drift = far.normalized * Drift;
            float slowAt = DashStart + DashIn, stampAt = slowAt + 0.04f;
            bool boss = false;
            foreach (var rg in rigs) boss |= rg.member.boss;
            float shakeAmp = boss ? 44 : 32;
            float t = 0, tOut = -1, shakeAt = -1, stampT = -1;
            vs.localScale = Vector3.zero;
            vsGroup.alpha = 1;
            group.alpha = 1;
            App.Audio.Play("whoosh");
            while (true)
            {
                float dt = Time.unscaledDeltaTime;
                if (tOut < 0 && (t >= slowAt + Slow || skip && t > 0.25f))
                {
                    tOut = Mathf.Max(t, slowAt);
                    App.Audio.Play("whoosh");
                    var split = OnSplit;
                    OnSplit = null;
                    split?.Invoke();
                }
                TickRigs(t, slowAt);

                // vị trí khung đỏ trên đường chéo; khung xanh đối xứng qua tâm
                Vector2 red;
                float streakSpeed, streakAlpha;
                if (t < slowAt)
                {
                    float u = Mathf.Clamp01((t - DashStart) / DashIn);
                    red = Vector2.Lerp(far, drift, 1 - Mathf.Pow(1 - u, 4));
                    streakSpeed = 3600;
                    streakAlpha = 0.32f * Mathf.Clamp01(t / FadeIn);
                }
                else if (tOut < 0)
                {
                    red = Vector2.Lerp(drift, -drift, Mathf.Clamp01((t - slowAt) / Slow));
                    streakSpeed = 220;
                    streakAlpha = 0.12f;
                }
                else
                {
                    float w = Mathf.Clamp01((t - tOut) / DashOut);
                    var from = Vector2.Lerp(drift, -drift, Mathf.Clamp01((tOut - slowAt) / Slow));
                    red = Vector2.Lerp(from, -far * 1.05f, w * w * w);
                    streakSpeed = 4000;
                    streakAlpha = 0.3f * (1 - Mathf.Clamp01((t - tOut - 0.1f) / 0.35f));
                }

                // dấu VS đóng: rung màn, sao loang, mảnh văng
                if (t >= stampAt && shakeAt < 0)
                {
                    shakeAt = t;
                    stampT = t;
                    App.Audio.Play("stamp");
                    Haptics.Play(Haptic.Stamp);
                    Shatter();
                }
                var shake = Vector2.zero;
                if (shakeAt >= 0 && t - shakeAt < StampShake)
                {
                    float k = 1 - (t - shakeAt) / StampShake;
                    float a = shakeAmp * k * k;
                    shake = new Vector2(UnityEngine.Random.Range(-a, a), UnityEngine.Random.Range(-a, a));
                }
                foe.root.anchoredPosition = red + shake;
                mine.root.anchoredPosition = -red + shake;

                // nền tối: hiện nhanh, tan sau khi hai khung lao ra (lộ sân đấu)
                float bgOut = tOut < 0 ? 0 : Mathf.Clamp01((t - tOut - 0.08f) / BgOut);
                page.color = Fade(Dark, Dark.a * Mathf.Clamp01(t / FadeIn) * (1 - bgOut * bgOut * (3 - 2 * bgOut)));

                foreach (var (rt, scale, delay) in pops) rt.localScale = Vector3.one * scale * Pop(Mathf.Clamp01((t - delay) / 0.24f));

                // số lực chiến đếm lên từ lúc dấu VS đóng
                if (stampT >= 0)
                {
                    float c = Mathf.Clamp01((t - stampT) / 0.6f);
                    c = 1 - (1 - c) * (1 - c);
                    foe.powerText.text = NumFmt.Short(Mathf.RoundToInt(foePower * c));
                    mine.powerText.text = NumFmt.Short(Mathf.RoundToInt(minePower * c));
                }

                // chữ VS: đóng xuống (to, xoay → vừa), thở nhẹ lúc chậm; lao ra thì phóng to bay ra, mờ dần
                if (t < stampAt) vs.localScale = Vector3.zero;
                else
                {
                    float v = Mathf.Clamp01((t - stampAt) / 0.16f);
                    float s = VsBig * Mathf.Lerp(2.4f, 1, 1 - (1 - v) * (1 - v)) * (1 + 0.04f * Mathf.Sin((t - stampAt) * 9f) * v);
                    float rot = Mathf.Lerp(-30, -9, v);
                    if (tOut < 0 && v >= 1) rot += VsJitterRot * 2 * (Mathf.PerlinNoise(t * 22f, 7.3f) - 0.5f);
                    float a = 1;
                    if (tOut >= 0)
                    {
                        float o = Mathf.Clamp01((t - tOut) / VsOut);
                        s *= Mathf.Lerp(1, 3.6f, o * o);
                        rot += 14 * o;
                        a = 1 - o;
                    }
                    vs.localScale = Vector3.one * s;
                    vs.localEulerAngles = new Vector3(0, 0, rot);
                    vsGroup.alpha = a;
                }
                var jitter = stampT >= 0 && tOut < 0
                    ? VsJitter * 2 * new Vector2(Mathf.PerlinNoise(t * 26f, 1.1f) - 0.5f, Mathf.PerlinNoise(3.7f, t * 26f) - 0.5f)
                    : Vector2.zero;
                vs.anchoredPosition = shake * 0.7f + jitter;
                TickFx(dt, stampT < 0 ? -1 : t - stampT, streakSpeed, streakAlpha);

                if (tOut >= 0 && t - tOut >= Mathf.Max(DashOut, BgOut + 0.08f, VsOut)) break;
                yield return null;
                t += dt;
            }
        }

        // bật ra: 0 → 1,12 → 1
        static float Pop(float x) => x <= 0 ? 0 : x < 0.6f ? Mathf.Lerp(0, 1.12f, x / 0.6f) : Mathf.Lerp(1.12f, 1, (x - 0.6f) / 0.4f);
    }
}
