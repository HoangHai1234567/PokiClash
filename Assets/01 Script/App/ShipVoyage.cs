// Chuyến tàu qua mây (người dùng 2026-11-19, làm lại 2026-11-27): chuyển giữa sảnh, Nhà, đảo Casino và màn tải lúc mở game.
// Người dùng: "tưởng tượng 3 đảo trong 1 map to, chỉ cần follow cam theo thuyền và tách mây cho mượt", "nước của 3 đảo phải liền mạch".
// Mọi thứ nằm trên một dải thế giới dọc theo hướng đi, camera chỉ trượt dọc dải, bám theo tàu:
//   [ảnh chụp màn cũ] → [dải mây trên biển] → [ảnh chụp màn mới]
// - Biển chung (App/SeaAnchor.cs): ảnh chụp màn, biển của dải, màn thật cùng vẽ một ảnh biển lát ghim theo thế giới. Biển của dải ghim
//   theo ảnh màn cũ; trước khi chụp màn mới, gốc biển của màn mới được dời (SeaAnchor.Match) cho trùng đúng chỗ biển của dải lúc camera
//   tới nơi, nên không còn đường nối giữa ảnh chụp và biển. Cỡ ô hai màn lệch nhau (màn cũ đang phóng) thì đổi cỡ dần giữa dải mây.
// - Đóng (Close): camera màn cũ lướt tới bến, giao diện cố định của màn (SceneRoot.Chrome) mờ đi; chụp màn cũ (không tàu, không mây
//   vành), tàu của lớp này đứng thay tàu của màn ở chỗ đậu. Màn đứng yên trong lúc SceneRouter gỡ màn cũ, nạp màn mới (máy khựng lúc nạp
//   chỉ thấy như tàu đứng chờ ở bến, không giật giữa đường).
// - Mở (Open): màn mới đặt camera ở chỗ đậu, tàu của màn ẩn; chụp màn mới, đặt sau dải mây. Rồi tàu chạy MỘT đường liền: đường ra khơi
//   của bến cũ → đường cong qua dải mây → đường vào bến mới tới tận chỗ đậu; tốc độ tăng dần khi rời bến, hãm dần khi cập bến (hồ sơ tốc
//   độ tính trước theo cả đường). Camera trượt theo tàu (SmoothDamp, đi trước tàu một đoạn theo tốc độ), bắt đầu và dừng đúng hai ảnh
//   màn; mây ở mép màn cũ khép từ hai bên khi tàu rời bến, mây ở mép màn mới dạt ra khi camera tới nơi; giữa dải mây toả quanh tàu và
//   khép sau đuôi. Dải mây nằm giữa hai đảo (bắt đầu ngoài mép màn), không đè lên đảo.
// - Ảnh màn gồm cả phần đảo ngoài khung (người dùng 2026-11-27 "khi tàu rời bến thì phần đảo nằm ngoài cam bị cắt đi"): ngoài ô chính,
//   chụp thêm các ô kề cỡ màn mà camera sẽ quét qua (dời lớp kéo của bản đồ, SeaAnchor.Map), nửa độ phân giải; xem Capture. Tàu đậu xong thì lớp này tắt (màn thật y như ảnh), tàu của màn hiện đúng chỗ đậu (PierShip.DockedFrom), giao diện
//   cố định hiện lại. Không chuyền tàu qua lại giữa màn và lớp này giữa đường như bản cũ.
// - Hướng đi trên màn (người dùng 2026-11-27): sảnh → Nhà thẳng lên (về thẳng xuống), Nhà → đảo Casino sang trái (về sang phải),
//   sảnh → Casino chéo lên trái, Casino → sảnh chéo xuống phải; màn tải đi lên. Dải thế giới nằm dọc theo hướng đi ax (đi chéo: bề
//   dài / bề ngang dải là hình chiếu của màn lên hướng đi / hướng vuông góc).
// - Mây vành rời của màn (CloudRing) không nằm trong ảnh chụp: lớp này mang từng đám sang dải thế giới đúng chỗ, đúng độ toả, để chúng
//   tiếp tục toả quanh tàu; lúc tới thì trả độ toả về mây của màn mới.
// - Màn tải (App gọi BeginBoot khi mở thẳng vào sảnh): biển mở, tàu đi lên, logo, thanh tải, mẹo. Tải xong (đủ 2,4 giây) thì dải mây
//   hiện ra phía trước, tàu đi qua rồi vào bến sảnh như trên.
// Theo giờ (DayCycle, như sảnh, đảo; người dùng 2026-11-19 "mây và thời tiết ở loading cũng phải đổi theo giờ"): lớp nhuộm
// (day_multiply) và tia nắng (day_rays) phủ biển, dưới ảnh chụp màn (ảnh đã nhuộm sẵn); biển tối thêm về đêm (DayCycle.SeaNight);
// mây nhân CloudTint × màu cảnh như mây sảnh; tàu nhân màu cảnh, đêm thắp đèn lồng.
// Canvas riêng thứ tự 9 (dưới thanh trên 10: thanh trên, kệ chung đứng yên như giao diện, thế giới trôi); màn tải 15 (che thanh trên).
// SceneRouter dùng lớp này thay màn mây CloudCover khi Takes(cũ, mới) đúng. Không sinh GameObject lúc chạy: mây, bọt là ảnh dựng sẵn
// trong prefab (menu "PokiClash/Prefab/Sảnh và đảo/Bến tàu: tàu sảnh, chuyến tàu qua mây, màn tải", Editor/ShipBuild.cs); lớp biển của
// prefab đổi sang vật liệu biển chung (Resources/SeaWorld.mat, shader PokiClash/UISeaWorld) lúc chạy, nét sóng rời của bản cũ tắt.
using System.Collections;
using System.Collections.Generic;
using PokiClash.Core;
using TMPro;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class ShipVoyage : MonoBehaviour, ISceneCover
    {
        const float Cruise = 1700; // tốc độ giữa biển (đơn vị/giây)
        const float BootSpeed = 460; // màn tải: đi chậm trên biển
        const float Accel = 1100, Decel = 1250; // giữa biển
        const float AccelDock = 380, DecelDock = 330; // sát bến: rời bến, cập bến êm
        const float NearK = 1.5f; // trần tốc gần bến: tốc bến + NearK × khoảng tới bến (đơn vị/giây trên mỗi đơn vị)
        const float CamLead = 0.18f; // camera đi trước tàu 0,18 bề dài màn khi chạy hết tốc
        const float CamLag = 0.42f; // độ trễ camera (giây, SmoothDamp)
        // dải mây bắt đầu ngay ngoài mép trước màn cũ, hết trước mép sau màn mới 0,15 bề dài màn: mây nằm giữa các đảo, không đè lên đảo
        // (ảnh màn đã có phần đảo ngoài khung, biển chung không còn đường nối phải giấu như bản phủ lấn 0,3 vào màn)
        const float BandOut = 0.15f;
        const float Edge = 0.3f; // vùng mây khép / dạt ở mép dải (bề dài màn, cộng 260)
        const float Gap = 2400; // khoảng biển mây tối thiểu giữa hai màn (đơn vị)
        const float Step = 10; // bước lấy mẫu đường đi
        const float BootMin = 2.4f;
        const int OrderVoyage = 9, OrderBoot = 15;

        static readonly string[] Tips =
        {
            "Thủy khắc Hỏa, Hỏa khắc Kim, Kim khắc Mộc, Mộc khắc Thổ, Thổ khắc Thủy.",
            "Đánh vào hệ mình khắc: sát thương ×1,5. Bị khắc thì chỉ còn ×0,75.",
            "Mỗi lượt chọn 5 lần, mỗi lần 1 trong 3 thẻ.",
            "Chiêu và Tuyệt kỹ không tốn lần chọn, chỉ tốn mana và nộ.",
            "Ải đã qua tự đánh ra bi khi bạn vắng mặt.",
            "Cấp người chơi cũng là cấp của mọi tướng.",
            "Nút Nhà ở hàng dưới sảnh đưa bạn về Nhà.",
        };

        [SerializeField] PokiCanvas view;
        [SerializeField] RectTransform area; // phủ kín màn (Nen của canvas)
        [SerializeField] Image blocker;
        [SerializeField] RectTransform sea; // lớp biển (vật liệu biển chung), phủ kín màn
        [SerializeField] Image[] waves = new Image[0]; // nét sóng rời của bản cũ: tắt (ảnh biển lát đã có sóng)
        [SerializeField] Image tint; // lớp nhuộm theo giờ (day_multiply), trên biển, dưới ảnh chụp màn
        [SerializeField] RawImage rays; // tia nắng (day_rays)
        [SerializeField] RawImage oldShot, newShot; // ảnh chụp màn cũ / mới, cỡ bằng màn
        [SerializeField] ShipLook look;
        [SerializeField] Image[] clouds = new Image[0];
        [SerializeField] Image[] carry = new Image[0]; // mây vành của màn mang sang dải (CloudRing)
        [SerializeField] float holeRadius = 290;
        [Tooltip("Vật liệu biển chung (shader PokiClash/UISeaWorld); trống thì nạp Resources/SeaWorld")]
        [SerializeField] Material seaMat;
        [Header("Màn tải")]
        [SerializeField] CanvasGroup bootUi;
        [SerializeField] RectTransform logo;
        [SerializeField] Image barFill;
        [SerializeField] RectTransform barPencil;
        [SerializeField] TextMeshProUGUI pct, tip;

        public static ShipVoyage I { get; private set; }
        public static bool Booting => I && I.booting;

        public bool Closed { get; private set; }

        Vector2 ax = Vector2.up; // hướng đi trên màn hình (vector đơn vị)
        static readonly Vector2 UpLeft = new Vector2(-1, 1).normalized;
        // toạ độ dải thế giới: x ngang (theo Lat, vuông góc hướng đi), q dọc theo hướng đi; màn hình = Lat * x + ax * (q - qc)
        Vector2 Lat => new Vector2(ax.y, -ax.x);
        float qc; // camera (VoyageSeason đọc tên trường này)
        Vector2 sp; // tàu (x, q)
        float speed, targetSpeed, followX;
        bool follow, running, booting, loaded;
        float bandA = float.PositiveInfinity, bandB = float.PositiveInfinity, kA = 1, kB = 1; // dải mây [A, B]; độ khép mây ở hai mép
        float qNew = float.PositiveInfinity; // tâm ảnh màn mới
        RenderTexture rtOld, rtNew;
        // ô chụp kề ảnh màn cũ / mới (Capture): phần đảo ngoài khung lúc camera trượt đi / tới
        sealed class Tile
        {
            public RawImage img;
            public RenderTexture rt;
            public Vector2 off; // lệch so với tâm ảnh chính (toạ độ màn, bội số cỡ màn)
            public bool arrival;
        }
        readonly List<Tile> tiles = new List<Tile>();
        readonly List<RawImage> tilePool = new List<RawImage>(); // RawImage nhân từ oldShot lần đầu cần, giữ lại dùng tiếp
        float bootT0, tipT;
        int tipIdx;
        Vector2 lastSize, logoPos;
        Vector2[] cBase, cOff;
        float[] cW;
        float period;
        float[] cJit;
        bool seaOn;
        // mây mang: vị trí gốc (x, q), độ toả, chỉ số trong CloudRing của màn mới (-1: mây màn cũ)
        Vector2[] kBase, kOff;
        int[] kRing;
        int kCount, kArr;
        CloudRing ringNew, ringOld;
        // màn cũ (huỷ chuyến khi màn mới không nạp được: SceneRouter mở lại màn cũ)
        SceneRoot oldRoot;
        PierShip fromPier;

        // ---- biển chung: điểm biển giữa màn u(qc) = u0 + ax · I(qc), cỡ ô T(qc) (đơn vị local của area) ----
        Vector2 seaU0;
        float seaTa = SeaWorld.Tile, seaTb = SeaWorld.Tile, seaQ1, seaQ2;
        float[] seaInt; // I(q) = ∫ dq / T(q) lấy mẫu đều trên [0, qNew]
        bool seaBlend;

        // ---- đường đi một mạch (toạ độ dải) ----
        readonly List<Vector2> depart = new List<Vector2>(), arrive = new List<Vector2>();
        readonly List<Vector2> path = new List<Vector2>();
        readonly List<float> pathV = new List<float>(); // trần tốc từng điểm (hồ sơ tốc độ)
        float pathLen, ps, sDep, sArr, qc0, d0, camV, tripT, partT = -1, turnT;
        float sizeFrom = 1.1f, sizeTo = 1.1f, vFrom, vTo;
        bool trip, tripDone, endPier;
        Vector2 dockFace = Vector2.up; // hướng mũi lúc đậu (màn hình)

        // Dùng khi dựng prefab (Editor).
        public void Setup(PokiCanvas canvas, RectTransform areaRt, Image block, RectTransform seaRt, Image[] waveImgs, Image tintImg,
            RawImage raysImg, RawImage oldImg,
            RawImage newImg, ShipLook ship, Image[] cloudImgs, Image[] carryImgs, CanvasGroup boot, RectTransform logoRt, Image fill,
            RectTransform pencil, TextMeshProUGUI pctText, TextMeshProUGUI tipText)
        {
            carry = carryImgs;
            view = canvas;
            area = areaRt;
            blocker = block;
            sea = seaRt;
            waves = waveImgs;
            tint = tintImg;
            rays = raysImg;
            oldShot = oldImg;
            newShot = newImg;
            look = ship;
            clouds = cloudImgs;
            bootUi = boot;
            logo = logoRt;
            barFill = fill;
            barPencil = pencil;
            pct = pctText;
            tip = tipText;
        }

        void Awake()
        {
            I = this;
            logoPos = logo ? logo.anchoredPosition : Vector2.zero;
            // lớp biển: vật liệu biển chung (lấy ô lát theo thế giới), một tấm phủ kín màn; nét sóng rời của bản cũ tắt
            if (!seaMat) seaMat = Resources.Load<Material>("SeaWorld");
            var img = sea ? sea.GetComponent<Image>() : null;
            if (img && seaMat)
            {
                img.material = seaMat;
                img.type = Image.Type.Simple;
            }
            foreach (var w in waves)
                if (w)
                    w.gameObject.SetActive(false);
            Hide();
        }

        void OnDestroy()
        {
            if (I == this)
            {
                I = null;
                SeaWorld.Held = false;
            }
            Release();
        }

        Vector2 Size
        {
            get
            {
                var s = area.rect.size;
                return s.x > 1 ? s : new Vector2(PokiCanvas.RefW, PokiCanvas.RefH);
            }
        }

        float H => Size.y;
        // khoảng giữa tâm hai ảnh màn trên dải (biết trước lúc chụp màn cũ: Close chụp phần đảo ngoài khung tới giữa đường)
        float Span => L + Mathf.Max(1.1f * L, Gap);
        // bề dài của màn theo hướng đi / bề ngang vuông góc (đi chéo: hình chiếu của màn)
        float L => Mathf.Abs(ax.x) * Size.x + Mathf.Abs(ax.y) * Size.y;
        float Wd => Mathf.Abs(ax.y) * Size.x + Mathf.Abs(ax.x) * Size.y;
        // điểm trên màn (so với tâm) -> toạ độ dải, khi tâm màn ở q0; hướng trên màn -> hướng trong dải
        Vector2 ToBand(Vector2 sc, float q0) => new Vector2(Vector2.Dot(sc, Lat), q0 + Vector2.Dot(sc, ax));
        Vector2 Dirs(Vector2 v) => new Vector2(Vector2.Dot(v, Lat), Vector2.Dot(v, ax));
        Vector2 ScreenDir(Vector2 b) => Lat * b.x + ax * b.y;

        // ---------- SceneRouter ----------

        // chuyến này có đi tàu không (và hướng đi)
        public bool Takes(string from, string to)
        {
            if (booting && to == SceneIds.Hub)
            {
                ax = Vector2.up;
                return true;
            }
            // sảnh → Nhà thẳng lên, về thẳng xuống
            if (from == SceneIds.Hub && to == SceneIds.Home) ax = Vector2.up;
            else if (from == SceneIds.Home && to == SceneIds.Hub) ax = Vector2.down;
            // đảo Casino (GD_Claude/29_DaoCasino.md): từ sảnh chéo lên trái, về sảnh chéo xuống phải
            else if (from == SceneIds.Hub && to == SceneIds.Casino) ax = UpLeft;
            else if (from == SceneIds.Casino && to == SceneIds.Hub) ax = -UpLeft;
            // Nhà → Casino sang trái, về sang phải
            else if (from == SceneIds.Home && to == SceneIds.Casino) ax = Vector2.left;
            else if (from == SceneIds.Casino && to == SceneIds.Home) ax = Vector2.right;
            else return false;
            return true;
        }

        public void Block(bool on)
        {
            if (blocker) blocker.raycastTarget = on;
        }

        void Show(int order)
        {
            running = true;
            gameObject.SetActive(true);
            if (view && view.Canvas) view.Canvas.sortingOrder = order;
            Block(true);
        }

        void Hide()
        {
            running = false;
            Closed = false;
            follow = trip = tripDone = false;
            SeaWorld.Held = false;
            if (look) look.Show(false);
            if (bootUi) bootUi.alpha = 0;
            Release();
            gameObject.SetActive(false);
        }

        void Release()
        {
            foreach (var rt in new[] { rtOld, rtNew })
                if (rt)
                {
                    rt.Release();
                    Destroy(rt);
                }
            rtOld = rtNew = null;
            if (oldShot) oldShot.texture = null;
            if (newShot) newShot.texture = null;
            foreach (var t in tiles)
            {
                if (t.rt)
                {
                    t.rt.Release();
                    Destroy(t.rt);
                }
                if (t.img)
                {
                    t.img.texture = null;
                    t.img.gameObject.SetActive(false);
                }
            }
            tiles.Clear();
        }

        void Restart()
        {
            seaOn = false;
            kCount = 0;
            followX = 0;
            ringNew = ringOld = null;
            oldRoot = null;
            fromPier = null;
            foreach (var c in carry)
                if (c) c.gameObject.SetActive(false);
            qc = qc0 = 0;
            shotsNewTop = false;
            follow = trip = tripDone = false;
            bandA = bandB = qNew = float.PositiveInfinity;
            kA = kB = 1;
            partT = -1;
            seaBlend = false;
            seaU0 = Vector2.zero;
            seaTa = seaTb = SeaWorld.Tile;
            depart.Clear();
            arrive.Clear();
            Release();
            if (look) look.Show(false);
            if (bootUi) bootUi.alpha = 0;
        }

        // rời màn cũ: camera lướt tới bến, giao diện mờ; chụp màn cũ làm nền, tàu của lớp này đứng ở chỗ đậu. Trả về khi màn cũ gỡ được
        // (màn đứng yên tới khi Open: lúc nạp màn mới máy có khựng cũng chỉ thấy tàu chờ ở bến)
        public IEnumerator Close()
        {
            if (Closed)
            {
                Block(true);
                yield break;
            }
            Show(OrderVoyage);
            Restart();
            Daylight();
            Layout(0);
            bool north = ax.y > 0.01f; // rời bến theo đường ra khơi bắc / nam (đi ngang: theo đường ngang của bến)
            bool flat = Mathf.Abs(ax.y) < 0.01f;
            var root = App.Router ? App.Router.CurrentRoot : null;
            oldRoot = root;
            if (root) root.Chrome(false, true);
            var from = PierShip.Active;
            if (from && root && from.gameObject.scene != root.gameObject.scene) from = null;
            if (from) from.UseSide(flat ? (ax.x < 0 ? -1 : 1) : 0);
            bool pier = from && from.isActiveAndEnabled && from.Has(north);
            if (pier)
            {
                from.Ready(north);
                if (from.Glide != null) yield return from.Glide(from.FocusFor(north)); // cùng lúc giao diện mờ đi
                else yield return new WaitForSecondsRealtime(0.25f);
            }
            else yield return new WaitForSecondsRealtime(0.25f);
            if (root) root.Chrome(false, false);
            yield return null; // một khung cho camera, bố cục đứng yên
            float lossy = Mathf.Max(1e-5f, look.transform.lossyScale.x);
            Vector2 face = ax;
            if (pier)
            {
                fromPier = from;
                foreach (var w in from.WorldLine(north)) depart.Add(ToBand(Local(w), 0));
                sizeFrom = from.ShipRect.lossyScale.x / lossy;
                vFrom = Mathf.Max(160, from.Speed * from.Look.transform.lossyScale.x / lossy);
                face = from.Look.Heading;
                from.Look.Show(false);
            }
            else
            {
                // màn cũ không có bến: tàu từ mép sau màn chạy vào
                depart.Add(new Vector2(0, -L / 2 - 260));
                depart.Add(new Vector2(0, -L / 2 - 100));
                sizeFrom = 1.1f;
                vFrom = 600;
            }
            ringOld = CloudRing.Active;
            if (ringOld && root && ringOld.gameObject.scene != root.gameObject.scene) ringOld = null;
            // gốc biển của màn cũ (biển của dải ghim theo ảnh chụp này)
            var anchor = SeaAnchor.Active;
            if (anchor && root && anchor.gameObject.scene != root.gameObject.scene) anchor = null;
            float al = Mathf.Max(1e-5f, area.lossyScale.x);
            if (anchor)
            {
                anchor.Apply();
                seaTa = anchor.TileWorld / al;
                seaU0 = -Local(anchor.OriginWorld) / seaTa;
            }
            else
            {
                seaTa = SeaWorld.Tile;
                seaU0 = Vector2.zero;
            }
            seaTb = seaTa;
            // chụp màn cũ và phần đảo ngoài khung theo hướng camera sẽ trượt (như một bản đồ liền)
            rtOld = Capture(anchor, ringOld, 0, false, ax);
            if (oldShot) oldShot.texture = rtOld;
            SeaWorld.Held = true;
            seaOn = true;
            sp = depart[0];
            look.Size = sizeFrom;
            look.Pos = Screen_(sp);
            look.Face(face, true);
            look.ClearFoam();
            look.Show(true);
            bandA = L / 2 + BandOut * L;
            kA = 0;
            Layout(0);
            Closed = true;
        }

        // tới màn mới: đặt camera màn mới ở bến, chụp, nối sau dải mây; tàu chạy một mạch từ chỗ đậu cũ tới chỗ đậu mới; tắt lớp
        public IEnumerator Open()
        {
            if (booting) yield return BootEnd();
            var root = App.Router ? App.Router.CurrentRoot : null;
            if (!booting && root == oldRoot)
            {
                Cancel(); // màn mới không nạp được (gói tải lỗi): ở lại màn cũ
                yield break;
            }
            bool fromNorth = ax.y < -0.01f; // cập bến theo đường vào bắc / nam (đi ngang: theo đường ngang của bến)
            bool flat = Mathf.Abs(ax.y) < 0.01f;
            var to = PierShip.Active;
            if (to && root && to.gameObject.scene != root.gameObject.scene) to = null;
            if (root) root.Chrome(false, false);
            if (to) to.UseSide(flat ? (ax.x < 0 ? 1 : -1) : 0); // đi sang trái thì vào bến từ bên phải
            bool pier = to && to.isActiveAndEnabled && to.Has(fromNorth);
            if (pier)
            {
                to.Park();
                to.Frame?.Invoke(to.FocusFor(fromNorth), World(Vector2.zero)); // giữa chỗ đậu và điểm vào bến ra giữa màn (camera tự kẹp)
                to.HoldAtExit(fromNorth);
            }
            // chờ camera, bố cục màn mới đứng yên rồi mới chụp
            for (int f = 0; f < 3; f++) yield return null;
            yield return new WaitForSecondsRealtime(0.12f);
            // màn mới đặt sau dải mây: mép gần cách mép trước màn cũ (hoặc chỗ camera màn tải) một khoảng biển mây
            qc0 = qc;
            qNew = qc0 + Span;
            float lossy = Mathf.Max(1e-5f, look.transform.lossyScale.x);
            arrive.Clear();
            endPier = pier;
            if (pier)
            {
                var line = to.WorldLine(fromNorth); // chỗ đậu → điểm ra khơi
                for (int i = line.Count - 1; i >= 0; i--) arrive.Add(ToBand(Local(line[i]), qNew));
                sizeTo = to.ShipRect.lossyScale.x / lossy;
                vTo = Mathf.Max(160, to.Speed * to.Look.transform.lossyScale.x / lossy);
                var fw = (Vector2)area.InverseTransformVector(to.DockFaceWorld(fromNorth));
                dockFace = fw.sqrMagnitude > 1e-6f ? fw.normalized : ax;
            }
            else
            {
                // màn mới không có bến: tàu đi khuất phía trước
                arrive.Add(ToBand(ax * (L / 2 - 200), qNew));
                arrive.Add(ToBand(ax * (L / 2 + 320), qNew));
                sizeTo = 1.1f;
                vTo = Cruise;
                dockFace = ax;
            }
            ringNew = CloudRing.Active;
            if (ringNew && root && ringNew.gameObject.scene != root.gameObject.scene) ringNew = null;
            kArr = kCount;
            // biển màn mới: cỡ ô thật của màn mới; gốc dời cho trùng biển của dải lúc camera tới qNew
            var anchor = SeaAnchor.Active;
            if (anchor && root && anchor.gameObject.scene != root.gameObject.scene) anchor = null;
            float al = Mathf.Max(1e-5f, area.lossyScale.x);
            seaTb = anchor ? anchor.TileWorld / al : seaTa;
            BuildSea();
            if (anchor)
            {
                var o = SeaAt(qNew, out float t);
                anchor.Match(World(o), t * al);
                anchor.Apply();
            }
            // chụp màn mới và phần đảo ngoài khung phía camera tới (ngược hướng đi)
            rtNew = Capture(anchor, ringNew, qNew, true, -ax);
            ApplySea();
            Restack(false); // đầu chuyến ảnh màn cũ nằm trên (ô kề màn mới vừa chèn vào dưới ảnh màn cũ)
            if (newShot) newShot.texture = rtNew;
            bandB = qNew - L / 2 - BandOut * L;
            kB = 1;
            if (!follow) System.GC.Collect(); // dọn rác lúc màn còn đứng yên (tàu chờ ở bến), khỏi khựng giữa đường
            BuildTrip();
            App.Audio?.Play("whoosh");
            follow = false;
            tripT = 0;
            partT = -1;
            turnT = 0;
            tripDone = false;
            trip = true;
            while (!tripDone) yield return null;
            // tàu đã đậu, camera đứng đúng ảnh màn mới, mây mép đã dạt: trả mây vành, tàu của màn hiện ở chỗ đậu, tắt lớp (màn thật y như ảnh)
            trip = false;
            qc = qNew;
            HandBack();
            if (pier) to.DockedFrom(fromNorth);
            Hide();
            if (to) to.UseSide(0);
            if (root) root.Chrome(true, true);
            booting = false;
        }

        // màn mới không nạp được: trả màn cũ như trước chuyến
        void Cancel()
        {
            if (fromPier)
            {
                fromPier.Look.Show(true);
                fromPier.Park();
                fromPier.UseSide(0);
            }
            if (ringOld) ringOld.Show(true);
            foreach (var c in carry)
                if (c) c.gameObject.SetActive(false);
            kCount = 0;
            var root = oldRoot;
            Hide();
            if (root) root.Chrome(true, true);
        }

        // ---------- màn tải ----------

        // mở game thẳng vào sảnh: che màn bằng biển có tàu đi lên, logo, thanh tải (App gọi trước Router.Go(Hub))
        public void BeginBoot()
        {
            booting = true;
            loaded = false;
            Show(OrderBoot);
            ax = Vector2.up;
            Restart();
            seaOn = true;
            SeaWorld.Held = true;
            seaU0 = Vector2.zero;
            seaTa = seaTb = SeaWorld.Tile;
            sp = new Vector2(0, -H * 0.16f);
            speed = targetSpeed = BootSpeed;
            follow = true;
            look.Size = 1.1f;
            sizeFrom = 1.1f;
            look.Pos = Screen_(sp);
            look.Face(Vector2.up, true);
            look.Show(true);
            bootT0 = Time.unscaledTime;
            tipIdx = Random.Range(0, Tips.Length);
            ShowTip();
            if (bootUi) bootUi.alpha = 1;
            SetBar(0);
            Closed = true;
            Daylight(); // nhuộm theo giờ ngay khung đầu
            Layout(0);
        }

        IEnumerator BootEnd()
        {
            loaded = true;
            while (Time.unscaledTime - bootT0 < BootMin) yield return null;
            SetBar(1);
            yield return new WaitForSecondsRealtime(0.2f);
            // dải mây hiện ra ngay trước mặt, tàu tăng tốc đi vào
            bandA = qc + H / 2 + 40;
            kA = 1;
            targetSpeed = Cruise;
            App.Audio?.Play("whoosh");
            for (float t = 0; t < 0.4f; t += Dt)
            {
                if (bootUi) bootUi.alpha = 1 - Smooth(t / 0.4f);
                yield return null;
            }
            if (bootUi) bootUi.alpha = 0;
            if (view && view.Canvas) view.Canvas.sortingOrder = OrderVoyage; // thanh trên của sảnh hiện trên mây
        }

        void SetBar(float v)
        {
            if (!barFill) return;
            v = Mathf.Clamp01(v);
            barFill.fillAmount = v;
            if (barPencil)
            {
                float w = barFill.rectTransform.rect.width;
                var pp = barPencil.anchoredPosition;
                barPencil.anchoredPosition = new Vector2(-w / 2 + w * v + 18, pp.y);
            }
            if (pct) pct.text = $"{Mathf.RoundToInt(v * 100)}%";
        }

        void ShowTip()
        {
            if (!tip) return;
            tip.text = Loc.F("<color=#b8382a><b>Mẹo:</b></color> {0}", Loc.T(NextTip()));
            tipIdx++;
        }

        // người mới chỉ thấy câu về vòng chơi; các câu khác hiện khi đã học tới phần đó (GD_Claude/25_FTUE.md bước A1, mục 6)
        string NextTip()
        {
            var s = App.Save?.Data;
            if (s == null || Tutorial.IsLegacy(s)) return Tips[tipIdx % Tips.Length];
            if (!Tutorial.CoreDone(s)) return "Thắng ải lấy bi, thả bi vào máy để mạnh lên.";
            for (int k = 0; k < Tips.Length; k++)
            {
                int i = (tipIdx + k) % Tips.Length;
                if (TipOpen(s, i))
                {
                    tipIdx += k;
                    return Tips[i];
                }
            }
            return "Thắng ải lấy bi, thả bi vào máy để mạnh lên.";
        }

        // thứ tự như Tips: khắc hệ ×2, lượt đánh, chiêu và tuyệt kỹ, AFK, cấp chung, tàu về Nhà
        static bool TipOpen(SaveData s, int i)
        {
            switch (i)
            {
                case 0:
                case 1: return Tutorial.Done(s, Tutorial.Counter);
                case 2: return Tutorial.Done(s, Tutorial.RunQueue);
                case 3: return Tutorial.Done(s, Tutorial.Ult);
                case 4: return Tutorial.Done(s, Tutorial.AfkBtn);
                case 5: return Tutorial.Done(s, Tutorial.Exp);
                case 6: return Home.Open(s, GameData.Current.Cfg);
                default: return true;
            }
        }

        // ---------- đường đi một mạch ----------

        // đường ra khơi bến cũ → đường cong qua dải mây → đường vào bến mới; lấy mẫu đều Step; hồ sơ tốc độ: trần theo khoảng tới bến,
        // tăng tốc / hãm có giới hạn (êm hơn sát bến), xuất phát từ tốc hiện tại, dừng hẳn ở chỗ đậu mới
        void BuildTrip()
        {
            var ctrl = new List<Vector2>();
            bool boot = follow; // màn tải: tàu đang chạy, đường bắt đầu từ chỗ tàu
            if (boot) ctrl.Add(sp);
            else ctrl.AddRange(depart);
            float depLen = boot ? 0 : PolyLen(depart);
            float arrLen = PolyLen(arrive);
            var p0 = ctrl[ctrl.Count - 1];
            var t0 = !boot && depart.Count >= 2 ? (depart[depart.Count - 1] - depart[depart.Count - 2]).normalized : Vector2.up;
            var p3 = arrive[0];
            var t3 = arrive.Count >= 2 ? (arrive[1] - arrive[0]).normalized : Vector2.up;
            // không quay ngược hướng đi: hai tiếp tuyến luôn có phần tiến theo dải
            if (t0.y < 0.25f) t0 = (t0 + Vector2.up * (0.25f - t0.y) * 2).normalized;
            if (t3.y < 0.25f) t3 = (t3 + Vector2.up * (0.25f - t3.y) * 2).normalized;
            float D = Vector2.Distance(p0, p3);
            var p1 = p0 + t0 * D * 0.35f;
            var p2 = p3 - t3 * Mathf.Min(D * 0.35f, 900);
            const int N = 64;
            for (int i = 1; i < N; i++)
            {
                float t = i / (float)N, s = 1 - t;
                ctrl.Add(s * s * s * p0 + 3 * s * s * t * p1 + 3 * s * t * t * p2 + t * t * t * p3);
            }
            ctrl.AddRange(arrive);
            // lấy mẫu đều
            path.Clear();
            pathV.Clear();
            path.Add(ctrl[0]);
            float carryLen = 0;
            for (int i = 1; i < ctrl.Count; i++)
            {
                var a = ctrl[i - 1];
                var b = ctrl[i];
                float seg = Vector2.Distance(a, b);
                if (seg < 1e-4f) continue;
                float at = Step - carryLen;
                while (at <= seg)
                {
                    path.Add(Vector2.Lerp(a, b, at / seg));
                    at += Step;
                }
                carryLen = seg - (at - Step);
            }
            if (Vector2.Distance(path[path.Count - 1], ctrl[ctrl.Count - 1]) > 0.5f) path.Add(ctrl[ctrl.Count - 1]);
            int n = path.Count;
            pathLen = (n - 1) * Step;
            sDep = boot ? Mathf.Min(600, pathLen * 0.3f) : Mathf.Max(depLen, 1);
            sArr = Mathf.Max(arrLen, 1);
            // trần tốc
            float v0 = boot ? speed : 0;
            float vEnd = endPier ? 0 : Cruise * 0.6f;
            var v = new float[n];
            for (int i = 0; i < n; i++)
            {
                float s = i * Step, rest = Mathf.Max(0, pathLen - s);
                float lim = Cruise;
                if (!boot) lim = Mathf.Min(lim, vFrom + NearK * s);
                if (endPier) lim = Mathf.Min(lim, vTo + NearK * rest);
                v[i] = lim;
            }
            v[0] = Mathf.Min(v[0], v0);
            for (int i = 1; i < n; i++)
            {
                float s = i * Step;
                float a = boot ? Accel : Mathf.Lerp(AccelDock, Accel, Smooth(s / 500f));
                v[i] = Mathf.Min(v[i], Mathf.Sqrt(v[i - 1] * v[i - 1] + 2 * a * Step));
            }
            v[n - 1] = Mathf.Min(v[n - 1], vEnd);
            for (int i = n - 2; i >= 0; i--)
            {
                float rest = Mathf.Max(0, pathLen - i * Step);
                float d = endPier ? Mathf.Lerp(DecelDock, Decel, Smooth(rest / 500f)) : Decel;
                v[i] = Mathf.Min(v[i], Mathf.Sqrt(v[i + 1] * v[i + 1] + 2 * d * Step));
            }
            pathV.AddRange(v);
            ps = 0;
            // camera: bắt đầu đúng chỗ đang đứng (bến cũ: tâm ảnh màn cũ; màn tải: đang bám tàu)
            d0 = path[0].y + Lead(v[0]) - qc;
            camV = boot ? speed : 0;
        }

        // camera đi trước tàu bao nhiêu khi tàu chạy tốc v: bù độ trễ của SmoothDamp (v × CamLag) cộng phần nhìn trước theo tốc độ
        float Lead(float v) => v * CamLag + CamLead * L * Mathf.Clamp01(v / Cruise);

        static float PolyLen(List<Vector2> pts)
        {
            float len = 0;
            for (int i = 1; i < pts.Count; i++) len += Vector2.Distance(pts[i - 1], pts[i]);
            return len;
        }

        Vector2 PathAt(float s)
        {
            int n = path.Count;
            if (n == 0) return sp;
            float f = Mathf.Clamp(s, 0, pathLen) / Step;
            int i = Mathf.Min(n - 2, (int)f);
            if (i < 0) return path[0];
            return Vector2.Lerp(path[i], path[i + 1], f - i);
        }

        float SpeedAt(float s)
        {
            int n = pathV.Count;
            if (n == 0) return Cruise;
            float f = Mathf.Clamp(s, 0, pathLen) / Step;
            int i = Mathf.Min(n - 2, (int)f);
            if (i < 0) return pathV[0];
            return Mathf.Lerp(pathV[i], pathV[i + 1], f - i);
        }

        // ---------- biển chung ----------

        // cỡ ô đổi dần (chỉ khi hai màn lệch cỡ) giữa dải mây, lúc cả hai ảnh màn gần như khuất; lập bảng I(q) = ∫ dq / T(q)
        void BuildSea()
        {
            seaBlend = Mathf.Abs(seaTb - seaTa) > 0.5f;
            seaQ1 = qc0 + 0.75f * L;
            seaQ2 = Mathf.Max(seaQ1 + 1, qNew - 0.75f * L);
            const int M = 256;
            seaInt = new float[M + 1];
            float span = Mathf.Max(1, qNew - qc0);
            float acc = 0;
            for (int i = 0; i <= M; i++)
            {
                if (i > 0)
                {
                    float qa = qc0 + span * (i - 1) / M, qb = qc0 + span * i / M;
                    acc += (qb - qa) * 0.5f * (1 / TileAt(qa) + 1 / TileAt(qb));
                }
                seaInt[i] = acc;
            }
        }

        float TileAt(float q) => seaBlend ? Mathf.Lerp(seaTa, seaTb, Smooth(Mathf.InverseLerp(seaQ1, seaQ2, q))) : seaTa;

        float SeaIntegral(float q)
        {
            if (!seaBlend || seaInt == null) return q / seaTa;
            float span = Mathf.Max(1, qNew - qc0);
            if (q <= qc0) return qc0 / seaTa + (q - qc0) / seaTa;
            float baseI = qc0 / seaTa;
            if (q >= qNew) return baseI + seaInt[seaInt.Length - 1] + (q - qNew) / seaTb;
            float f = (q - qc0) / span * (seaInt.Length - 1);
            int i = Mathf.Min(seaInt.Length - 2, (int)f);
            return baseI + Mathf.Lerp(seaInt[i], seaInt[i + 1], f - i);
        }

        // gốc biển (local của area) và cỡ ô khi camera ở q: điểm biển giữa màn u = u0 + ax · I(q), gốc = −u · T
        Vector2 SeaAt(float q, out float t)
        {
            t = TileAt(q);
            var u = seaU0 + ax * SeaIntegral(q);
            return -u * t;
        }

        void ApplySea()
        {
            if (!seaOn) return;
            var o = SeaAt(qc, out float t);
            SeaWorld.Set(World(o), t * Mathf.Max(1e-5f, area.lossyScale.x));
        }

        // ---------- mỗi khung ----------

        static float Dt => Mathf.Min(Time.unscaledDeltaTime, 0.05f);

        // màu theo giờ: biển, nhuộm, nắng, mây, tàu (gọi mỗi khung; giờ đổi chậm nên rẻ)
        void Daylight()
        {
            float hr = DayCycle.Hour, night = DayCycle.Night(hr), sun = DayCycle.Sun(hr), dusk = DayCycle.Dusk(hr) * (1 - night);
            var tintC = DayCycle.Tint(hr);
            if (sea)
            {
                var img = sea.GetComponent<Image>();
                if (img) img.color = Color.Lerp(Color.white, DayCycle.SeaNight, night);
            }
            if (tint)
            {
                bool on = seaOn && (tintC.r < 0.995f || tintC.g < 0.995f || tintC.b < 0.995f);
                if (tint.enabled != on) tint.enabled = on;
                if (on) tint.color = tintC;
            }
            if (rays)
            {
                float k = Mathf.Max(sun, dusk * 0.3f);
                bool on = seaOn && k > 0.01f;
                if (rays.enabled != on) rays.enabled = on;
                if (on)
                {
                    rays.color = new Color(1, Mathf.Lerp(1, 0.66f, dusk), Mathf.Lerp(1, 0.42f, dusk), k);
                    // dải nắng cố định trong thế giới: trôi theo camera
                    rays.uvRect = new Rect(ax.x * qc / Mathf.Max(1, Size.x), ax.y * qc / Mathf.Max(1, H), 1, 1);
                }
            }
            var ct = DayCycle.CloudTint(hr) * tintC;
            foreach (var c in clouds)
                if (c && c.gameObject.activeSelf) c.color = new Color(ct.r, ct.g, ct.b, 1);
            for (int k = 0; k < kCount; k++) carry[k].color = new Color(ct.r, ct.g, ct.b, 1);
            if (look)
            {
                look.SetTint(tintC);
                look.Night(night);
            }
        }

        void Update()
        {
            if (!running) return;
            float dt = Dt;
            if (dt <= 0) return;
            Daylight();
            var prev = sp;
            float prevQc = qc;
            float v = 0;
            if (trip) v = Trip(dt);
            else if (follow)
            {
                // màn tải: tàu đi thẳng lên, camera theo sau, không lùi
                speed = Mathf.MoveTowards(speed, targetSpeed, Accel * dt);
                sp = new Vector2(Mathf.Lerp(sp.x, followX, 1 - Mathf.Exp(-1.6f * dt)), sp.y + speed * dt);
                float want = sp.y + CamLead * L * Mathf.Clamp01(speed / Cruise);
                qc = Mathf.Max(qc, Mathf.Lerp(qc, want, 1 - Mathf.Exp(-2.6f * dt)));
                v = speed;
            }
            float camSpeed = (qc - prevQc) / dt;
            look.Pos = Screen_(sp);
            if (follow && !trip)
            {
                var d = ScreenDir(sp - prev);
                if (d.sqrMagnitude > 0.01f) look.Face(d);
            }
            look.Flow = -ax * camSpeed; // bọt nằm trong thế giới
            look.Tick(dt, v);
            Layout(dt);
            if (booting && bootUi && bootUi.alpha > 0)
            {
                float e = Time.unscaledTime - bootT0;
                SetBar(loaded ? Mathf.Min(1, e / BootMin) : Mathf.Min(0.9f, e / BootMin));
                tipT += dt;
                if (tipT > 2.6f)
                {
                    tipT = 0;
                    ShowTip();
                }
                if (logo) logo.anchoredPosition = logoPos + new Vector2(0, Mathf.Sin(e * 1.6f) * 6);
            }
        }

        // một khung của chuyến: tàu theo đường với hồ sơ tốc độ, camera trượt theo, mây hai mép; trả tốc độ tàu
        float Trip(float dt)
        {
            tripT += dt;
            float before = ps;
            if (ps < pathLen)
            {
                float vs = Mathf.Max(SpeedAt(ps), endPier ? 26 : 80);
                ps = Mathf.Min(pathLen, ps + vs * dt);
            }
            float vNow = (ps - before) / dt;
            sp = PathAt(ps);
            // hướng mũi theo đường; đậu rồi thì quay theo hướng đậu
            if (ps < pathLen - 0.5f)
            {
                var d = ScreenDir(PathAt(Mathf.Min(pathLen, ps + 16)) - sp);
                if (d.sqrMagnitude > 0.01f) look.Face(d);
            }
            else if (endPier) look.Face(dockFace);
            // cỡ tàu đổi dần giữa đường
            float mid = Mathf.Max(1, pathLen - sDep - sArr);
            look.Size = Mathf.Lerp(sizeFrom, sizeTo, Smooth((ps - sDep) / mid));
            // camera: đi trước tàu theo tốc độ (bù độ trễ SmoothDamp, nên lúc chạy đều tàu nằm sau tâm màn 0,18 bề dài); đầu chuyến bắt
            // đầu đúng chỗ cũ, cuối chuyến dừng đúng tâm màn mới
            float lead = Lead(SpeedAt(ps));
            float target = sp.y + lead - d0 * (1 - Smooth(ps / sDep));
            target = Mathf.Lerp(target, qNew, Smooth((ps - (pathLen - sArr)) / sArr));
            target = Mathf.Clamp(target, qc0, qNew);
            float nq = Mathf.SmoothDamp(qc, target, ref camV, CamLag, Mathf.Infinity, dt);
            qc = Mathf.Clamp(Mathf.Max(qc, nq), qc0, qNew);
            if (qNew - qc < 0.5f && ps >= pathLen - 0.5f)
            {
                qc = qNew;
                camV = 0;
            }
            // mây mép màn cũ khép lại từ hai bên khi tàu rời bến; mép màn mới dạt ra khi camera tới nơi
            if (!booting) kA = Smooth(tripT / 0.8f);
            if (partT < 0 && qNew - qc < 0.08f * L) partT = 0;
            if (partT >= 0)
            {
                partT += dt;
                kB = 1 - Smooth(partT / 0.55f);
            }
            if (ps >= pathLen - 0.5f && qc >= qNew && kB <= 0.001f)
            {
                turnT += dt;
                if (turnT >= 0.3f) tripDone = true; // quay mũi theo hướng đậu xong
            }
            return vNow;
        }

        void Build(Vector2 size)
        {
            lastSize = size;
            int n = clouds.Length;
            const int cols = 6;
            int rows = Mathf.Max(1, Mathf.CeilToInt(n / (float)cols));
            float margin = 260;
            float dx = (size.x + margin * 2) / cols, dy = (size.y + margin * 2) / rows;
            float cdx = (Mathf.Min(size.x, Size.x) + margin * 2) / cols; // cỡ mây theo bề ngang màn thật (đi ngang, chéo: dải rộng hơn màn)
            period = rows * dy;
            cBase = new Vector2[n];
            cOff = new Vector2[n];
            cW = new float[n];
            cJit = new float[n];
            var rng = new System.Random(19);
            for (int i = 0; i < n; i++)
            {
                int r = i / cols, c = i % cols;
                float x = -size.x / 2 - margin + (c + 0.5f + (r % 2 == 0 ? -0.25f : 0.25f)) * dx + (float)(rng.NextDouble() - 0.5) * dx * 0.35f;
                float q = (r + 0.5f) * dy + (float)(rng.NextDouble() - 0.5) * dy * 0.4f;
                cBase[i] = new Vector2(x, q);
                cW[i] = cdx * (1.9f + (float)rng.NextDouble() * 0.5f);
                cJit[i] = ((float)rng.NextDouble() - 0.5f) * 0.32f * size.y; // mép dải so le, không thẳng như bức tường
                var crt = clouds[i].rectTransform;
                float aspect = clouds[i].sprite ? clouds[i].sprite.rect.height / clouds[i].sprite.rect.width : 0.5f;
                crt.sizeDelta = new Vector2(cW[i], cW[i] * aspect);
                crt.localScale = new Vector3(rng.NextDouble() < 0.5 ? -1 : 1, 1, 1);
            }
            var real = Size; // size là cỡ dải (ngang, dọc theo hướng đi); biển và ảnh chụp theo màn thật
            if (sea)
            {
                sea.anchorMin = sea.anchorMax = new Vector2(0.5f, 0.5f);
                sea.anchoredPosition = Vector2.zero;
                sea.sizeDelta = new Vector2(real.x + 512, real.y + 512);
            }
            foreach (var shot in new[] { oldShot, newShot })
                if (shot) shot.rectTransform.sizeDelta = real;
        }

        // vị trí lặp gần camera của một vật cố định trong thế giới (chu kỳ p)
        float Near(float q, float p) => qc + Mathf.Repeat(q - qc + p / 2, p) - p / 2;

        // biển, ảnh màn cũ / mới, mây theo camera; mây ở mép ảnh khép / dạt theo kA / kB, toả quanh tàu
        void Layout(float dt)
        {
            var size = Size;
            var band = new Vector2(Wd, L);
            if (cBase == null || band != lastSize) Build(band);
            if (sea && sea.gameObject.activeSelf != seaOn) sea.gameObject.SetActive(seaOn);
            ApplySea();
            Place(oldShot, rtOld, 0);
            Place(newShot, rtNew, qNew);
            // ảnh đảo gần camera nằm trên: nửa đường đầu ảnh màn cũ (và ô kề của nó) trên ảnh màn mới, qua giữa đường thì ngược lại; đổi lúc
            // camera ở giữa dải mây
            bool newTop = rtNew && qc > (qc0 + qNew) * 0.5f;
            if (newTop != shotsNewTop) Restack(newTop);
            // ô kề của ảnh màn: cùng chỗ trong thế giới với ảnh chính, lệch đúng bội số cỡ màn
            foreach (var t in tiles)
            {
                var p = ax * ((t.arrival ? qNew : 0) - qc) + t.off;
                bool on = t.rt && Mathf.Abs(p.x) < size.x && Mathf.Abs(p.y) < size.y;
                if (t.img.gameObject.activeSelf != on) t.img.gameObject.SetActive(on);
                if (!on) continue;
                t.img.rectTransform.sizeDelta = size;
                t.img.rectTransform.anchoredPosition = p;
            }
            float Wh = band.x / 2 + 220;
            float edge = Edge * band.y + 260; // vùng mây khép / dạt ở mép dải
            // mọi đám mây còn thấy được trên ảnh màn cũ / mới đều khép / dạt theo kA / kB (không đám nào hiện sẵn trên màn lúc tàu còn đậu)
            float seenA = qc0 + band.y / 2 + 400, seenB = qNew - band.y / 2 - 400;
            // vùng toả: quanh thân tàu; mây dạt ngang hai bên, mở trước mũi, khép lại đúng chỗ sau đuôi (người dùng: thấy rõ thuyền,
            // mây không lùi lại)
            float lsz = look ? look.Size : 1;
            var center = Screen_(sp) + new Vector2(0, 110 * lsz);
            var head = look ? look.Heading : Vector2.up;
            float R = holeRadius * (look ? Mathf.Max(0.7f, look.Size) : 1), R2 = R * 2.6f;
            for (int i = 0; i < clouds.Length; i++)
            {
                var img = clouds[i];
                float q = Near(cBase[i].y, period);
                float a0 = bandA + cJit[i], b0 = bandB - cJit[i];
                bool on = q >= a0 && q <= b0;
                float kk = 1;
                if (on && q < Mathf.Max(a0 + edge, seenA)) kk = Mathf.Min(kk, kA);
                if (on && q > Mathf.Min(b0 - edge, seenB)) kk = Mathf.Min(kk, kB);
                on &= kk > 0.002f;
                if (img.gameObject.activeSelf != on) img.gameObject.SetActive(on);
                if (!on)
                {
                    cOff[i] = Vector2.zero;
                    continue;
                }
                float x = cBase[i].x, absX = Mathf.Abs(x);
                float g = (1 - kk) * Wh;
                float xd = Mathf.Sign(x == 0 ? 1 : x) * (g + absX * (1 - g / Wh) + Mathf.Pow(1 - kk, 2) * cW[i] * 0.62f);
                var p = Lat * xd + ax * (q - qc);
                cOff[i] = Part(p, center, head, R, R2, cOff[i], dt, i);
                img.rectTransform.anchoredPosition = p + cOff[i];
            }
            // mây vành mang theo: cố định trong thế giới; toả quanh tàu khi tàu chạy (lúc tàu còn chờ ở bến giữ nguyên như trên màn)
            for (int k = 0; k < kCount; k++)
            {
                var img = carry[k];
                var p = Screen_(kBase[k]);
                bool on = Mathf.Abs(p.x) < size.x * 0.5f + 400 && Mathf.Abs(p.y) < size.y * 0.5f + 400;
                if (img.gameObject.activeSelf != on) img.gameObject.SetActive(on);
                if (trip && dt > 0) kOff[k] = Part(p, center, head, R, R2, kOff[k], dt, k);
                if (on) img.rectTransform.anchoredPosition = p + kOff[k];
            }
        }

        // độ toả một đám mây quanh tàu: nhanh lúc toả, chậm lúc khép
        static Vector2 Part(Vector2 p, Vector2 center, Vector2 head, float R, float R2, Vector2 cur, float dt, int i)
        {
            var target = Side(p, center, head, R, R2, i);
            float rate = target.sqrMagnitude > cur.sqrMagnitude ? 24f : 3.2f;
            return dt > 0 ? Vector2.Lerp(cur, target, 1 - Mathf.Exp(-rate * dt)) : target;
        }

        // đích dạt của một đám mây khi tàu chạy qua: chỉ dạt NGANG (vuông góc hướng đi), mạnh khi gần đường tàu; cửa sổ dọc đường đi mở
        // trước mũi tới 2,4R và khép sau đuôi từ -0,6R tới -1,8R, nên mây dạt ra rồi về đúng chỗ, không bị đẩy lùi theo tàu
        public static Vector2 Side(Vector2 p, Vector2 center, Vector2 head, float R, float R2, int i)
        {
            var d = p - center;
            var h = head.sqrMagnitude > 1e-4f ? head.normalized : Vector2.up;
            var n = new Vector2(-h.y, h.x);
            float along = Vector2.Dot(d, h), lat = Vector2.Dot(d, n), al = Mathf.Abs(lat);
            if (al >= R2) return Vector2.zero;
            float g = along > 1.2f * R ? 1 - Mathf.InverseLerp(1.2f * R, 2.4f * R, along)
                : along < -0.6f * R ? 1 - Mathf.InverseLerp(-0.6f * R, -1.8f * R, along) : 1;
            g = Smooth(g);
            if (g <= 0) return Vector2.zero;
            float k = 1 - al / R2;
            float s = al > 1 ? Mathf.Sign(lat) : (i % 2 == 0 ? 1 : -1);
            return n * (s * R * k * k * g);
        }

        // mang mây vành của màn (đang đúng chỗ trên màn hình) sang dải thế giới (ToBand, tâm màn ở q0): đám trong vùng chụp (màn và các ô
        // kề offs, nới một dải), gần tâm màn trước; kho có hạn, đám không mang được thì vẽ luôn vào ảnh chụp. keep: chỉ số đã mang
        void Carry(CloudRing ring, float q0, bool arrival, List<Vector2> offs, List<int> keep)
        {
            if (kBase == null || kBase.Length != carry.Length)
            {
                kBase = new Vector2[carry.Length];
                kOff = new Vector2[carry.Length];
                kRing = new int[carry.Length];
            }
            if (!arrival) kCount = 0;
            float al = Mathf.Max(1e-5f, area.lossyScale.x);
            float layer = ring.Layer.lossyScale.x / al;
            var half = Size / 2;
            var order = new List<(float d, int i, Vector2 s)>();
            for (int i = 0; i < ring.Count; i++)
            {
                var s1 = Local(ring.Layer.TransformPoint(ring.Home(i)));
                float ex = Mathf.Max(0, Mathf.Abs(s1.x) - half.x), ey = Mathf.Max(0, Mathf.Abs(s1.y) - half.y);
                bool near = ex <= 420 && ey <= 700;
                for (int k = 0; !near && k < offs.Count; k++)
                    near = Mathf.Abs(s1.x - offs[k].x) <= half.x + 300 && Mathf.Abs(s1.y - offs[k].y) <= half.y + 300;
                if (!near) continue;
                order.Add((s1.magnitude, i, s1));
            }
            order.Sort((x, y) => x.d.CompareTo(y.d));
            // màn cũ lấy tối đa 55% kho, phần còn lại để dành cho màn mới
            int cap = arrival ? carry.Length : Mathf.RoundToInt(carry.Length * 0.55f);
            foreach (var (_, i, s0) in order)
            {
                if (kCount >= cap) break;
                keep.Add(i);
                var src = ring.Cloud(i);
                var img = carry[kCount];
                img.sprite = src.sprite;
                var srt = src.rectTransform;
                float sc = srt.lossyScale.y / al;
                img.rectTransform.sizeDelta = srt.rect.size * sc;
                img.rectTransform.localScale = new Vector3(Mathf.Sign(srt.localScale.x), 1, 1);
                kBase[kCount] = ToBand(s0, q0);
                kOff[kCount] = ring.Offset(i) * layer;
                kRing[kCount] = arrival ? i : -1;
                kCount++;
            }
        }

        // trả độ toả mây mang về mây vành của màn mới, ẩn mây mang
        void HandBack()
        {
            float al = Mathf.Max(1e-5f, area.lossyScale.x);
            for (int k = 0; k < kCount; k++)
            {
                if (ringNew && kRing[k] >= 0) ringNew.SetOffset(kRing[k], kOff[k] / (ringNew.Layer.lossyScale.x / al));
                carry[k].gameObject.SetActive(false);
            }
            kCount = 0;
            if (ringNew) ringNew.Show(true);
            ringNew = null;
        }

        bool shotsNewTop;

        // xếp lại thứ tự vẽ khối ảnh chụp (ô kề + ảnh chính của màn cũ, của màn mới): nhóm nằm trên vẽ sau
        void Restack(bool newTop)
        {
            shotsNewTop = newTop;
            if (!oldShot || !newShot) return;
            var list = new List<Transform>();
            void Group(bool arrival)
            {
                foreach (var t in tiles)
                    if (t.arrival == arrival && t.img)
                        list.Add(t.img.transform);
                list.Add((arrival ? newShot : oldShot).transform);
            }
            Group(!newTop); // nhóm dưới trước
            Group(newTop);
            int at = int.MaxValue;
            foreach (var tr in list) at = Mathf.Min(at, tr.GetSiblingIndex());
            for (int k = 0; k < list.Count; k++) list[k].SetSiblingIndex(at + k);
        }

        void Place(RawImage shot, RenderTexture rt, float q)
        {
            if (!shot) return;
            bool on = rt && Mathf.Abs(q - qc) < L * 1.05f;
            if (shot.gameObject.activeSelf != on) shot.gameObject.SetActive(on);
            if (on) shot.rectTransform.anchoredPosition = ax * (q - qc);
        }

        // ---------- chụp màn ----------

        // chụp màn và các ô kề theo hướng camera sẽ trượt (dir: hướng camera đi trên màn, so với tâm ảnh màn này), như một bản đồ liền
        // (người dùng 2026-11-27: "khi tàu rời bến thì phần đảo nằm ngoài cam bị cắt đi ... mô phỏng thật như 3 đảo trong cùng 1 map"):
        // ô chính đủ nét; ô kề dời lớp kéo của bản đồ (SeaAnchor.Map) đúng một màn rồi chụp, thu nửa độ phân giải (chỉ thấy lúc camera
        // đang trượt, phần lớn dưới mây). Mây vành của màn: đám trong vùng chụp mang sang dải (toả quanh tàu), đám còn lại vẽ vào ảnh.
        // Gọi lúc màn đứng yên (tàu chờ ở bến), mọi lần chụp trong cùng một khung nên màn không kịp nhúc nhích.
        RenderTexture Capture(SeaAnchor anchor, CloudRing ring, float q0, bool arrival, Vector2 dir)
        {
            var size = Size;
            var map = anchor ? anchor.Map : null;
            var offs = map ? TileOffsets(dir, size) : new List<Vector2>();
            var keep = new List<int>();
            if (ring)
            {
                Carry(ring, q0, arrival, offs, keep);
                ring.Show(true);
                foreach (int i in keep) ring.Cloud(i).enabled = false;
            }
            if (anchor) anchor.Apply();
            var main = Snap();
            Dump(main, arrival ? "toi_chinh" : "di_chinh");
            if (offs.Count > 0)
            {
                // mặt nạ cắt khung bản đồ (RectMask2D) đã bỏ khỏi lượt vẽ (cull) mọi hình nằm hẳn ngoài khung, và chỉ dời lớp kéo trong cùng
                // một khung thì nó chưa tính lại: ô kề mất hết đảo, chỉ còn biển (người dùng 2026-11-27 "vẫn bị cắt"). Bật vẽ lại tạm thời
                // (vùng cắt của mặt nạ vẫn giữ), chụp xong trả đúng như cũ
                // Hình bị bỏ từ lúc nạp màn (phần bản đồ chưa từng hiện trên màn) còn chưa dựng lưới (Graphic.Rebuild bỏ qua hình đang bị bỏ),
                // nên phải đánh dấu dựng lại, không thì bật vẽ cũng trống ("vẫn bị cắt ở đây", góc chưa kéo tới)
                var culled = new List<CanvasRenderer>();
                foreach (var cr in map.GetComponentsInChildren<CanvasRenderer>())
                    if (cr.cull)
                    {
                        cr.cull = false;
                        culled.Add(cr);
                        var g = cr.GetComponent<Graphic>();
                        if (g)
                        {
                            g.SetVerticesDirty();
                            g.SetMaterialDirty();
                        }
                    }
                var tmp = NewShot(1, 24);
                var home = map.anchoredPosition;
                var parent = map.parent;
                foreach (var o in offs)
                {
                    var w = area.TransformVector(-o);
                    map.anchoredPosition = home + (parent ? (Vector2)parent.InverseTransformVector(w) : (Vector2)w);
                    if (anchor) anchor.Apply();
                    Render(tmp);
                    var rt = NewShot(0.5f, 0);
                    Graphics.Blit(tmp, rt);
                    AddTile(rt, o, arrival);
                    Dump(rt, (arrival ? "toi" : "di") + $"_{o.x / size.x:0}_{o.y / size.y:0}");
                }
                map.anchoredPosition = home;
                if (anchor) anchor.Apply();
                foreach (var cr in culled)
                    if (cr)
                        cr.cull = true;
                tmp.Release();
                Destroy(tmp);
            }
            if (ring)
            {
                foreach (int i in keep) ring.Cloud(i).enabled = true;
                ring.Show(false);
            }
            return main;
        }

        // các ô kề (bội số cỡ màn, toạ độ màn) mà khung nhìn quét qua khi trượt từ tâm theo dir một đoạn 0,9 bề dài màn + 400: khung lệch
        // dir·t giao ô (i, j) khi |dir.x·t − i·W| < W và |dir.y·t − j·H| < H; bỏ ô chỉ chạm sát mép, tối đa 6 ô, gần trước
        List<Vector2> TileOffsets(Vector2 dir, Vector2 size)
        {
            // mỗi đảo chỉ chụp tới quá giữa đường một chút (phần giữa là dải mây): hai đảo chụp chồng lên nhau thì đảo này che mất đảo kia
            // (người dùng 2026-11-27 "vẫn bị đúng chỗ đấy ... hoặc do bị cái gì đè lên": ô biển của đảo Casino đè lên đảo Hỏa)
            float D = Mathf.Min(0.9f * L + 400, Span / 2 - L / 2 + 0.2f * L);
            const float Pad = 80;
            var found = new List<(float t, Vector2 o)>();
            for (int i = -3; i <= 3; i++)
            for (int j = -2; j <= 2; j++)
            {
                if (i == 0 && j == 0) continue;
                float lo = 0, hi = D;
                if (!Cross(dir.x, i * size.x, size.x - Pad, ref lo, ref hi) || !Cross(dir.y, j * size.y, size.y - Pad, ref lo, ref hi)) continue;
                found.Add((lo, new Vector2(i * size.x, j * size.y)));
            }
            found.Sort((a, b) => a.t.CompareTo(b.t));
            var list = new List<Vector2>();
            for (int k = 0; k < found.Count && k < 6; k++) list.Add(found[k].o);
            return list;
        }

        // khoảng t có |a·t − c| < r, giao vào [lo, hi]; còn chỗ thì đúng
        static bool Cross(float a, float c, float r, ref float lo, ref float hi)
        {
            if (Mathf.Abs(a) < 1e-4f) return Mathf.Abs(c) < r && hi > lo;
            float t1 = (c - r) / a, t2 = (c + r) / a;
            if (t1 > t2) (t1, t2) = (t2, t1);
            lo = Mathf.Max(lo, t1);
            hi = Mathf.Min(hi, t2);
            return hi > lo;
        }

        // soi lỗi (chỉ Editor, khi có cờ Temp/chuyen_tau_dump.on): lưu từng ảnh chụp ra Temp/PokiShots/chuyen_tau/<tên>.png
        static void Dump(RenderTexture rt, string name)
        {
#if UNITY_EDITOR
            if (!rt) return;
            string root = System.IO.Path.GetFullPath(System.IO.Path.Combine(Application.dataPath, ".."));
            if (!System.IO.File.Exists(System.IO.Path.Combine(root, "Temp/chuyen_tau_dump.on"))) return;
            string dir = System.IO.Path.Combine(root, "Temp/PokiShots/chuyen_tau");
            System.IO.Directory.CreateDirectory(dir);
            var prev = RenderTexture.active;
            RenderTexture.active = rt;
            var tex = new Texture2D(rt.width, rt.height, TextureFormat.RGBA32, false);
            tex.ReadPixels(new Rect(0, 0, rt.width, rt.height), 0, 0);
            tex.Apply();
            RenderTexture.active = prev;
            System.IO.File.WriteAllBytes(System.IO.Path.Combine(dir, name + ".png"), tex.EncodeToPNG());
            Destroy(tex);
            Debug.Log($"[Chuyến tàu] chụp {name} {rt.width}x{rt.height}");
#endif
        }

        void AddTile(RenderTexture rt, Vector2 off, bool arrival)
        {
            int k = tiles.Count;
            while (tilePool.Count <= k)
            {
                var img = Instantiate(oldShot, oldShot.transform.parent);
                img.name = "chup_ke_" + tilePool.Count;
                img.texture = null;
                img.raycastTarget = false;
                img.transform.SetSiblingIndex(oldShot.transform.GetSiblingIndex()); // dưới ảnh chính, dưới mây
                img.gameObject.SetActive(false);
                tilePool.Add(img);
            }
            var t = new Tile { img = tilePool[k], rt = rt, off = off, arrival = arrival };
            t.img.texture = rt;
            tiles.Add(t);
        }

        RenderTexture NewShot(float scale, int depth) =>
            new RenderTexture(Mathf.Max(16, Mathf.RoundToInt(Screen.width * scale)), Mathf.Max(16, Mathf.RoundToInt(Screen.height * scale)), depth,
                RenderTextureFormat.ARGB32) { name = "chuyen_tau_chup" };

        // chụp màn hiện tại qua camera UI (không lớp này, không thanh trên) vào ảnh cỡ màn
        RenderTexture Snap()
        {
            var rt = PokiCanvas.UiCamera ? NewShot(1, 24) : null;
            if (rt) Render(rt);
            return rt;
        }

        void Render(RenderTexture rt)
        {
            var cam = PokiCanvas.UiCamera;
            if (!cam || !rt) return;
            var own = view ? view.Canvas : null;
            bool ownOn = own && own.enabled;
            if (own) own.enabled = false;
            var bars = App.Bars ? App.Bars.GetComponentInParent<Canvas>() : null;
            bool barsOn = bars && bars.enabled;
            if (bars) bars.enabled = false;
            Canvas.ForceUpdateCanvases();
            var req = new RenderPipeline.StandardRequest { destination = rt };
            if (RenderPipeline.SupportsRenderRequest(cam, req)) RenderPipeline.SubmitRenderRequest(cam, req);
            else
            {
                var prev = cam.targetTexture;
                cam.targetTexture = rt;
                cam.Render();
                cam.targetTexture = prev;
            }
            if (own) own.enabled = ownOn;
            if (bars) bars.enabled = barsOn;
        }

        // ---------- toạ độ ----------

        Vector2 Screen_(Vector2 p) => Lat * p.x + ax * (p.y - qc);

        Vector2 Local(Vector3 world) => area.InverseTransformPoint(world);

        Vector3 World(Vector2 local) => area.TransformPoint(local);

        static float Smooth(float u)
        {
            u = Mathf.Clamp01(u);
            return u * u * (3 - 2 * u);
        }
    }
}
