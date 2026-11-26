// Scene Trường đua của đảo Casino (GD_Claude/29_DaoCasino.md mục 6.3; mỗi trò một scene). Prefab Screens/CasinoRace (menu
// "PokiClash/Prefab/Đảo Casino/Trường đua: dựng scene"). Lõi: Core/Casino/Race.cs; sân: RaceStadium.
// Người dùng 2026-11-25: "random 3-5 tướng mỗi lane chạy đua nhau, trên đường chạy tướng có thể đánh nhau cho vui vui, có tướng bị
// choáng stun, nó cũng kiểu random ai về nhất cho vui thôi". Người dùng 2026-11-26: "sáng tạo hơn ở màn đua, thiết kế track đua như
// kiểu sân vận động 2 bên có khán giả".
// Người dùng 2026-11-26 (lượt hai): "cho trường đua fullscreen, khi đua bỏ mấy cái cúp, khi đua xong có 1 màn nhận thưởng đứng podium".
// - Sân phủ kín màn hình. Trên cùng: thanh đường hôm nay (3 chặng tô màu hệ, tên hệ; lúc đua là bản đồ nhỏ, mỗi tướng một chấm) và
//   bảng treo. Chưa đua: tấm sảnh ở đáy màn (5 hạng cúp, dòng điểm cúp tuần + lượt có thưởng, Nhận quà tuần, tướng đang chọn, Chọn
//   tướng, Đua); bấm Đua thì cả tấm sảnh ẩn đi, chỉ còn nút Cổ vũ.
// - Đua xong: lễ trao giải. Màn tối lại, bục 3 bậc trồi lên, ba tướng về đầu lần lượt nhảy lên bục (hạng ba trước, hạng nhất sau
//   cùng), hoa giấy; rồi hiện hạng của mình (cúp / nơ bạc / nơ đồng), thưởng, bảng xếp hạng cả đoàn, Đua lại / Xong.
// - Sân vận động (RaceStadium): máy quay bám tướng mình, thế giới cuộn ngang; khán đài mái sọc phía xa, hàng cổ động viên quay lưng phía
//   gần, cổng chặng theo hệ, vạch đích ca rô. Số làn = số tướng (3–5). Tướng ra khỏi khung thì có thẻ nhỏ ở mép báo cách mấy mét.
// - Hình tướng là RIG THẬT (AolaSticker như màn Nhà; người dùng 2026-11-26: "sao không lấy thẳng animation walk của tướng ra"): chạy
//   bằng clip walk (nhanh chậm theo tốc độ), đứng ở vạch và về đích bằng idle, húc bằng clip đánh, bị choáng bằng clip trúng đòn rồi
//   đứng xám; trên bục nhận thưởng cũng là rig idle. Rig của phần lớn tướng nằm trong gói nội dung nạp sau: hỏi AolaActor.Ready mỗi
//   khung tới khi sẵn rồi mới dựng (mỗi khung một con); đếm ngược chờ cả đoàn có rig (tối đa RigWaitMax giây). Bản đầu coi lần hỏi
//   đầu chưa sẵn là "không có rig" nên cả đoàn chạy bằng chân dung (người dùng 2026-11-26: "sao tôi chưa thấy các tướng play
//   animation walk"). Dạng chưa nhập rig hoặc chưa có clip walk thì giữ chân dung / dáng đứng nhảy cóc như trước. Trước khi đua (vừa vào màn) hàng tướng mẫu ở vạch cũng là rig diễn idle,
//   ba đối thủ bí ẩn tô sẫm; rig chưa sẵn thì để trống rồi bật ra, không hiện chân dung tĩnh (người dùng 2026-11-26: "play animation idle
//   cho chúng, không để icon tĩnh nhìn bị vỡ"). Rig của tướng còn có mặt được giữ lại và chuyển làn khi bấm Đua / về sảnh. Kèm: số hạng đang giữ, bụi dưới chân, vụt nổ, sao choáng, chữ nổi.
//   Không hiện tên tướng trên đường đua (người dùng 2026-11-26: "bỏ tên của tướng đi"); tướng mình có vòng vàng xoay dưới chân.
//   Rig chụp ở cỡ gấp đôi rồi thu lại và không xoay nghiêng (người dùng: "nhìn tướng hơi mờ").
// - Diễn: đếm ngược 3-2-1 trước khi chạy; bảng treo giữa khán đài hiện mặt tướng dẫn đầu + lời tường thuật; đổi ngôi đầu, va chạm thì
//   khán giả chỗ đó bật dậy; 20% cuối "Nước rút!" cả sân nhảy, sóng người; hai tướng đầu sát nhau trước vạch đích thì quay chậm
//   "Sát nút!"; về nhất chớp trắng, hoa giấy.
// - Dưới: tướng đang chọn, Chọn tướng, Đua (lệ phí; hết lượt có thưởng là đua tập), Cổ vũ (vòng sáng co về khớp nút: Tuyệt / Tốt / Hụt;
//   Tuyệt có khiên né đòn ngắn; trúng nhịp thì hàng cổ động viên của mình nhảy theo).
// - Kết quả: hạng, bi, điểm cúp; bảng xếp hạng cả đoàn (trúng / bị choáng); Đua lại / Xong.
// Luật cược (người dùng 2026-11-26, lượt cược): "đặt 1 trong 5 con kiểu tap vào 1 trong 5 con rồi hiện lên nút đặt cược, đặt max là 500
// bóng ... về nhất x3, về nhì x2, về 3 thì hòa tiền, 4, 5 mất tiền. 1 ngày được chơi 5 lần"; "chọn 1 trong ... con này chứ không phải
// chọn tướng, thêm nhân vật đen vào đây, thiết kế lại phần dưới chỗ các button".
// - Chưa đua: 5 con của lượt đua kế đứng ở vạch (Race.Lineup), đủ màu, diễn idle. Chạm vào đường đua thì con GẦN chỗ chạm nhất được
//   chọn (một vùng chạm chung, không phải ô riêng từng con: các con đứng chéo che nhau nên ô riêng dễ chọn nhầm; người dùng
//   2026-11-26: "phần tap vào nhân vật chưa đúng lắm và có chỗ hơi khó tap"); con được chọn to lên, có vòng vàng dưới chân, các con
//   khác tối bớt. Không còn chọn tướng của mình, không còn hàng cúp (điểm cúp tuần tính cho hạng cúp cao nhất đã mở).
// - Lão Mực đứng sau quầy làm chủ quầy cược (người dùng: "thêm Lão Mực làm chủ quầy cược"; rig DealerRig dùng chung với lều Đêm
//   Bài): chào khi vào màn, ngó khi mình chọn con, mừng / hoà / tiếc theo kết quả lượt vừa đua khi quay lại quầy.
// - Quầy cược ở đáy màn: vé lượt còn lại hôm nay, điểm cúp tuần (+ Nhận quà tuần), dải băng báo con đang chọn, bảng trả thưởng, 4 đồng
//   chip mức cược, nút Đặt cược (chỉ hiện sau khi chạm chọn một con). Hết lượt thì nút thành Đua thử (không cược).
// - Lúc đua: nút Cổ vũ chỉ để khán đài hò reo (kết quả do lõi định theo mức cược, Core/Casino/Race.cs).
// Mọi vật dựng sẵn trong prefab (5 làn), không sinh lúc chạy.
using System.Collections.Generic;
using System.Linq;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class RaceScene : SceneRoot
    {
        [System.Serializable]
        public struct Lane
        {
            public RectTransform token, body, stars, spin; // token: chân tướng trên làn; stars: chỗ sao choáng, spin: vòng sao xoay
            public HeroPortrait portrait;
            public Image face, burst, badge; // face: ảnh chân dung (tối đi khi choáng)
            public TextMeshProUGUI pop, badgeText;
            public RectTransform mark, markSpin; // vòng vàng dưới chân tướng của mình (mark dẹt thành elip, markSpin xoay)
            public RectTransform line; // vạch kẻ trên làn (làn đầu không có)
            public RectTransform edge; // thẻ ở mép khung khi tướng ra ngoài tầm nhìn
            public HeroPortrait edgeFace;
            public TextMeshProUGUI edgeText;
            public RectTransform chip; // chấm trên bản đồ nhỏ
            public Image chipFill;
            public Image[] dust; // bụi dưới chân
            public RectTransform rig; // chỗ gắn rig tướng (AolaSticker), gốc ở chân
        }

        [System.Serializable]
        public struct PodSlot
        {
            public RectTransform root, body; // root: chỗ đứng trên bậc; body: khung nhún của tướng
            public HeroPortrait portrait;
            public Image tag; // thẻ tên dưới chân bục
            public TextMeshProUGUI name;
        }

        enum Phase { Idle, Count, Run }

        [SerializeField] RaceTap[] chips; // đồng chip mức cược (RaceConfig.chips)
        [SerializeField] TextMeshProUGUI[] chipTexts, legend; // số trên chip; bảng trả thưởng nhất / nhì / ba
        [SerializeField] RectTransform chipRing; // vòng sáng quanh chip đang chọn
        [SerializeField] Image[] tickets; // vé lượt hôm nay
        [SerializeField] Sprite ticketOn, ticketOff;
        [SerializeField] RaceTap trackTap; // vùng chạm chung trên đường đua (chọn con gần chỗ chạm nhất)
        [SerializeField] DealerRig dealer; // Lão Mực sau quầy cược
        [SerializeField] TextMeshProUGUI info, track, talk;
        [SerializeField] SketchButton claim;
        [SerializeField] RectTransform field, map;
        [SerializeField] RaceStadium stadium;
        [SerializeField] Image[] segs;
        [SerializeField] TextMeshProUGUI[] segNames;
        [SerializeField] Lane[] lanes;
        [SerializeField] HeroPortrait boardFace;
        [SerializeField] TextMeshProUGUI big;
        [SerializeField] TextMeshProUGUI hero;
        [SerializeField] SketchButton go, cheer;
        [SerializeField] TextMeshProUGUI cheerText;
        [SerializeField] GameObject result;
        [SerializeField] TextMeshProUGUI resTitle, resInfo;
        [SerializeField] TextMeshProUGUI[] resRows;
        [SerializeField] SketchButton resAgain, resDone;
        [SerializeField] GameObject lobby, hud; // lobby: tấm sảnh ở đáy màn (ẩn khi đua); hud: thanh đường + bảng treo (ẩn khi trao giải)
        [SerializeField] GameObject podium; // lễ trao giải (trong khung sân, dưới lớp hoa giấy)
        [SerializeField] RectTransform podRise; // bục + tướng, trồi từ dưới lên
        [SerializeField] Image podDim, resIcon;
        [SerializeField] PodSlot[] podSlots;
        [SerializeField] Sprite[] resIcons; // cúp, nơ bạc, nơ đồng

        public override string Title => Loc.T("Trường đua");
        public override string BackTo => SceneIds.Casino;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static RaceConfig C => D.Cfg.casino.race;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        int cup; // hạng cúp của tuần (cao nhất đã mở)
        string mine; // con mình đặt cược
        List<string> lineup = new List<string>(); // 5 con của lượt đua kế
        int pick = -1, bet; // con đang chọn (−1: chưa), mức cược đang chọn
        float cheerCool;
        int lastPlace = -1; // hạng lượt vừa đua có cược (−1: chưa có), để Lão Mực phản ứng khi quay lại quầy
        const float TapReach = 260; // chạm cách tâm con gần nhất xa hơn chừng này thì không chọn
        RaceGame game;
        float acc;
        int evSeen;
        Rng rng;
        Phase phase;
        const float PopSec = 1.1f, CountSec = 2.6f, DustSec = 0.45f, BigSec = 1.25f;
        const float StartPad = 0.3f, StretchAt = 0.8f, PhotoZone = 7f, PhotoGap = 2.6f, CoastUnits = 11f;
        // diễn theo làn: lao (đích, còn bao lâu), vụt nổ, chữ nổi, nhịp chạy, bụi, lúc về đích, số hạng / số mét đang hiện
        readonly float[] lungeT = new float[5], burstT = new float[5], popT = new float[5], runPh = new float[5], finAt = new float[5], rankPop = new float[5];
        readonly Vector2[] lungeDir = new Vector2[5];
        readonly float[,] dustT = new float[5, 2], dustX = new float[5, 2];
        readonly int[] rankNow = new int[5], edgeNow = new int[5], dustNext = new int[5], placeOf = new int[5];
        float count, cam, camBias, slow = 1, shake, bigT, bigDur = 1, leadSaid, endHold;
        int leader = -1, countShown;
        bool stretch, photo, firstIn;
        Vector2 fieldHome, podHome;
        bool homeSet;
        float podT, seenH;
        int podStage;
        // rig tướng theo làn (AolaSticker): dựng dần sau khi bấm Đua, huỷ khi rời cuộc đua
        const float RigK = 0.74f; // dáng đứng của rig so với khung chân dung
        const float RigWaitMax = 6f; // chờ gói nội dung / đọc rig lâu nhất bấy nhiêu giây, quá thì chạy bằng chân dung
        const float RigSS = 2f; // rig chụp ở cỡ gấp đôi rồi thu lại: ảnh 1024 cho mọi cỡ tướng, không mờ trên máy nét
        readonly AolaSticker[] rigs = new AolaSticker[5];
        readonly bool[] rigFailed = new bool[5], rigWalk = new bool[5], onPod = new bool[5];
        readonly float[] rigH = new float[5], clipT = new float[5], atkT = new float[5], rigWait = new float[5];
        // tướng đang đứng ở từng làn (hàng mẫu trước khi đua hoặc đoàn đua), làn nào tô sẫm (đối thủ bí ẩn), rig của tướng nào, cỡ lúc dựng
        readonly string[] laneHero = new string[5], rigHero = new string[5];
        readonly bool[] laneDark = new bool[5];
        readonly float[] rigBase = new float[5], rigPop = new float[5];
        int laneCount;
        float startHold; // đã ghìm đếm ngược bao lâu để chờ rig
        readonly string[] clipNow = new string[5];
        readonly int[] podRunner = { -1, -1, -1 }; // tướng (làn) đứng ở từng bậc bục
        static readonly float[] PodHeight = { 250, 215, 205 };
        static readonly float[] PodMarks = { 0.77f, 1.07f, 1.37f, 1.8f }; // ba tướng chạm bục, rồi hiện bảng thưởng
        string boardHero;

        public RaceGame Game => game;

        // soi (lượt chụp của Editor): từng làn đang dùng rig hay chân dung, có clip walk không, đang phát clip gì
        public string RigReport()
        {
            var sb = new System.Text.StringBuilder();
            for (int i = 0; game != null && i < game.runners.Count && i < rigs.Length; i++)
                sb.Append($"lan {i} {game.runners[i].hero}: rig={(rigs[i] != null)} hong={rigFailed[i]} walk={rigWalk[i]} clip={clipNow[i]} t={clipT[i]:F2}\n");
            return sb.ToString();
        }

        // Dùng khi dựng prefab (Editor).
        public void Setup(TextMeshProUGUI infoText, TextMeshProUGUI trackText, TextMeshProUGUI talkText, SketchButton claimBtn,
            RectTransform fieldRt, RaceStadium stadiumView, RectTransform mapRt, Image[] segImgs, TextMeshProUGUI[] segTexts, Lane[] laneList,
            HeroPortrait boardPortrait, TextMeshProUGUI bigText, TextMeshProUGUI heroText, SketchButton goBtn, SketchButton cheerBtn,
            TextMeshProUGUI cheerLabel, GameObject res, TextMeshProUGUI rTitle, TextMeshProUGUI rInfo, TextMeshProUGUI[] rRows,
            SketchButton rAgain, SketchButton rDone, GameObject lobbyGo, GameObject hudGo, GameObject podiumGo, RectTransform podiumRise,
            Image podiumDim, PodSlot[] podiumSlots, Image rIcon, Sprite[] rIcons, RaceTap[] chipTaps, TextMeshProUGUI[] chipLabels,
            RectTransform chipSel, TextMeshProUGUI[] legendTexts, Image[] ticketImgs, Sprite ticketFull, Sprite ticketUsed, RaceTap trackTapArea,
            DealerRig dealerRig)
        {
            trackTap = trackTapArea; dealer = dealerRig;
            lobby = lobbyGo; hud = hudGo; podium = podiumGo; podRise = podiumRise; podDim = podiumDim; podSlots = podiumSlots; resIcon = rIcon; resIcons = rIcons;
            info = infoText; track = trackText; talk = talkText; claim = claimBtn; field = fieldRt; stadium = stadiumView; map = mapRt;
            segs = segImgs; segNames = segTexts; lanes = laneList; boardFace = boardPortrait; big = bigText;
            hero = heroText; go = goBtn; cheer = cheerBtn; cheerText = cheerLabel; result = res; resTitle = rTitle;
            resInfo = rInfo; resRows = rRows; resAgain = rAgain; resDone = rDone;
            chips = chipTaps; chipTexts = chipLabels; chipRing = chipSel; legend = legendTexts; tickets = ticketImgs; ticketOn = ticketFull; ticketOff = ticketUsed;
        }

        public override void Enter(object args)
        {
            rng = new Rng(Rng.RandomSeed());
            trackTap.onTap = null;
            trackTap.onTapAt = TapAt;
            for (int i = 0; i < chips.Length; i++)
            {
                chips[i].index = i;
                chips[i].onTap = PickChip;
            }
            go.SetOnClick(StartRace);
            cheer.SetOnClick(Cheer);
            claim.SetOnClick(ClaimWeek);
            resAgain.SetOnClick(BackToLobby);
            resDone.SetOnClick(BackToLobby);
            if (!homeSet) podHome = podRise.anchoredPosition;
            ClosePodium();
            game = null;
            phase = Phase.Idle;
            if (!homeSet)
            {
                fieldHome = field.anchoredPosition;
                homeSet = true;
            }
            cheerText.text = "";
            big.gameObject.SetActive(false);
            lastPlace = -1;
            NewLineup();
            Render();
            // Lão Mực sau quầy cược: lần đầu ông dẫn luật cược (câu đầu đã chào), không thì chào như thường
            Guide.MucActor = dealer;
            if (!CasinoGuide.Race() && dealer) dealer.Play("greet");
        }

        int bonk; // hai tiếng húc phát xen kẽ

        // lượt đua kế: 5 con mới, chưa chọn con nào; mức cược mặc định là chip thứ hai nếu đủ bi
        void NewLineup()
        {
            lineup = Race.Lineup(D, C, (uint)(rng.Next() * uint.MaxValue));
            pick = -1;
            mine = null;
            int balls = S.balls;
            if (bet <= 0 || bet > balls)
            {
                bet = 0;
                for (int i = 0; i < C.chips.Length; i++)
                    if (C.chips[i] <= balls && (bet == 0 || i <= 1)) bet = C.chips[i];
            }
            talk.text = Loc.T("Chạm vào một con để đặt cược. Về nhất, nhì thì thắng lớn!");
        }

        void BackToLobby()
        {
            ClosePodium();
            game = null;
            phase = Phase.Idle;
            NewLineup();
            Render();
            // Lão Mực phản ứng theo lượt vừa xong: khách thắng lớn / thắng / hoà / thua
            if (dealer && lastPlace >= 0) dealer.Play(lastPlace == 0 ? "react_win_big" : lastPlace == 1 ? "react_win_small" : lastPlace == 2 ? "react_push" : "react_lose");
            lastPlace = -1;
        }

        // lượt chụp của Editor chọn con thay ngón tay
        public void PickRunner(int i) => Tap(i);

        // chạm vào đường đua: chọn con có tâm hình gần chỗ chạm nhất (trong tầm TapReach)
        void TapAt(Vector2 screen)
        {
            if (game != null || lineup.Count == 0) return;
            if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(field, screen, PokiCanvas.UiCamera, out var lp)) return;
            // đổi sang toạ độ của các làn: x từ mép trái khung, y từ mép trên khung xuống
            float x = lp.x + field.rect.width * field.pivot.x, y = field.rect.height * (1 - field.pivot.y) - lp.y;
            int n = lineup.Count, best = -1;
            float bestD = TapReach;
            for (int i = 0; i < n && i < lanes.Length; i++)
            {
                var at = lanes[i].token.anchoredPosition; // (x, −y chân)
                float cx = at.x, cy = -at.y - FigureH(i, n) * 0.5f;
                float d = Mathf.Sqrt((x - cx) * (x - cx) + (y - cy) * (y - cy));
                if (d < bestD) { bestD = d; best = i; }
            }
            if (best >= 0) Tap(best);
        }

        // chạm một con ở vạch xuất phát: chọn con đó để cược
        void Tap(int i)
        {
            if (game != null || i < 0 || i >= lineup.Count) return;
            pick = i;
            mine = lineup[i];
            App.Audio.Play("pick");
            Haptics.Play(Haptic.UiTap);
            var h = D.Hero(mine);
            talk.text = Loc.F("Bạn chọn {0}. Chọn mức cược rồi bấm Đặt cược!", h != null ? h.name : mine);
            stadium.Pulse(stadium.ViewX(0), 500, 14);
            if (dealer && dealer.IsIdle) dealer.Play("bet_watch");
            Render();
        }

        void PickChip(int i)
        {
            if (game != null || i < 0 || i >= C.chips.Length) return;
            if (C.chips[i] > S.balls)
            {
                App.Toasts.Show(Loc.T("Không đủ bi"), Icon("lock"));
                App.Audio.Play("error");
                return;
            }
            bet = C.chips[i];
            App.Audio.Play("bet");
            Render();
        }

        void OnDestroy() => ClearRigs();

        void ClearRigs()
        {
            for (int i = 0; i < rigs.Length; i++)
            {
                rigs[i]?.Destroy();
                rigs[i] = null;
                rigHero[i] = laneHero[i] = null;
                rigFailed[i] = rigWalk[i] = onPod[i] = laneDark[i] = false;
                clipNow[i] = null;
                clipT[i] = atkT[i] = rigWait[i] = rigPop[i] = 0;
            }
            laneCount = 0;
            for (int k = 0; k < podRunner.Length; k++) podRunner[k] = -1;
        }

        // Đặt tướng cho n làn (hàng mẫu trước khi đua, hoặc đoàn đua). Rig đã dựng của tướng còn có mặt thì giữ lại và chuyển sang làn
        // mới (tướng mình không chớp mất khi bấm Đua / về sảnh); rig thừa thì huỷ; làn chưa có rig sẽ được Update dựng dần.
        void SetLaneHeroes(string[] heroes, bool[] dark, int n)
        {
            var keep = new AolaSticker[5];
            var keepBase = new float[5];
            var keepWalk = new bool[5];
            var keepT = new float[5];
            var used = new bool[5];
            for (int i = 0; i < n && i < 5; i++)
                for (int j = 0; j < 5; j++)
                {
                    if (used[j] || rigs[j] == null || rigHero[j] != heroes[i]) continue;
                    used[j] = true;
                    keep[i] = rigs[j];
                    keepBase[i] = rigBase[j];
                    keepWalk[i] = rigWalk[j];
                    keepT[i] = clipT[j];
                    break;
                }
            for (int j = 0; j < 5; j++)
                if (rigs[j] != null && !used[j]) rigs[j].Destroy();
            laneCount = Mathf.Min(n, 5);
            for (int i = 0; i < 5; i++)
            {
                bool has = i < laneCount;
                rigs[i] = has ? keep[i] : null;
                rigBase[i] = keepBase[i];
                rigWalk[i] = keepWalk[i];
                laneHero[i] = has ? heroes[i] : null;
                rigHero[i] = rigs[i] != null ? heroes[i] : null;
                laneDark[i] = has && dark != null && dark[i];
                rigFailed[i] = onPod[i] = false;
                clipNow[i] = null;
                clipT[i] = keepT[i];
                atkT[i] = rigWait[i] = rigPop[i] = 0;
                lanes[i].rig.localScale = Vector3.one;
                if (rigs[i] != null) PlaceRig(i, laneCount);
            }
            for (int k = 0; k < podRunner.Length; k++) podRunner[k] = -1;
        }

        // gắn rig của làn i vào đúng làn, đúng cỡ theo số làn; dời sao choáng, vụt nổ, số hạng theo chiều cao rig
        void PlaceRig(int i, int n)
        {
            var ln = lanes[i];
            var s = rigs[i];
            var h = D.Hero(laneHero[i]);
            var form = h != null ? HeroArt.FormOf(h) : null;
            // cỡ theo dạng như trên sân đấu nhưng nén lại cho vừa làn
            rigH[i] = PortraitH(n) * RigK * Mathf.Clamp(form != null ? (float)form.size : 1f, 0.82f, 1.22f);
            s.Rect.SetParent(ln.rig, false);
            s.Rect.anchoredPosition = Vector2.zero;
            float sc = rigH[i] / Mathf.Max(1, rigBase[i]) / RigSS;
            s.Rect.localScale = new Vector3(sc, sc, 1);
            s.Tint = laneDark[i] ? 0.55f : 1f; // con không được chọn: tối bớt
            float top = rigH[i] * 1.1f;
            ln.stars.anchoredPosition = new Vector2(0, top);
            ln.burst.rectTransform.anchoredPosition = new Vector2(top * 0.3f, top * 0.55f);
            ln.badge.rectTransform.anchoredPosition = new Vector2(-top * 0.62f, top * 0.8f);
        }

        // Dựng rig cho làn i; true: vừa dựng xong một con (mỗi khung tối đa một con: dựng prefab + RenderTexture tốn). Rig chưa sẵn (gói
        // nội dung đang nạp, anim đang đọc ở luồng phụ): chưa dựng, khung sau hỏi lại; chờ quá RigWaitMax hoặc dạng chưa nhập rig thì dùng
        // chân dung.
        bool BuildRig(int i, int n, float dt)
        {
            var ln = lanes[i];
            var h = D.Hero(laneHero[i]);
            var form = h != null ? HeroArt.FormOf(h) : null;
            if (form == null || string.IsNullOrEmpty(form.aola))
            {
                rigFailed[i] = true;
                return false;
            }
            if (!AolaActor.Ready(form.aola))
            {
                rigWait[i] += dt;
                if (rigWait[i] > RigWaitMax) rigFailed[i] = true;
                return false;
            }
            float baseH = PortraitH(n) * RigK * Mathf.Clamp((float)form.size, 0.82f, 1.22f);
            var s = AolaSticker.TryCreate(ln.rig, h, form.aola, baseH * RigSS, false);
            if (s == null)
            {
                rigFailed[i] = true;
                return false;
            }
            s.MaxFollowX = 0.45f; // clip đánh tự lao: giữ thân gần chỗ đứng, phần lao do màn đua lái
            rigs[i] = s;
            rigHero[i] = laneHero[i];
            rigBase[i] = baseH;
            rigWalk[i] = s.HasClip(AolaSticker.Walk);
            clipNow[i] = null;
            rigPop[i] = 0.22f; // bật ra từ nhỏ tới đủ cỡ
            PlaceRig(i, n);
            return true;
        }

        // mỗi khung: dựng dần rig còn thiếu (tối đa một con); chân dung chỉ hiện khi làn đó chịu không có rig; rig vừa dựng bật ra
        void TendRigs(float dt)
        {
            bool built = false;
            for (int i = 0; i < laneCount; i++)
            {
                var ln = lanes[i];
                if (rigs[i] == null && !rigFailed[i] && !built && AolaSticker.CanBuildNow) built = BuildRig(i, laneCount, dt);
                bool portrait = rigs[i] == null && rigFailed[i];
                if (ln.portrait.gameObject.activeSelf != portrait) ln.portrait.gameObject.SetActive(portrait);
                if (rigPop[i] > 0)
                {
                    rigPop[i] = Mathf.Max(0, rigPop[i] - dt);
                    float k = Mathf.Lerp(1f, 0.55f, rigPop[i] / 0.22f);
                    ln.rig.localScale = new Vector3(k, k, 1);
                }
            }
        }

        // cả đoàn đã có rig hoặc đã chịu dùng chân dung
        bool RigsSettled()
        {
            for (int i = 0; i < laneCount; i++)
                if (rigs[i] == null && !rigFailed[i]) return false;
            return true;
        }

        // chiều cao hình đang hiện của làn i (rig thấp hơn khung chân dung)
        float FigureH(int i, int n) => rigs[i] != null ? rigH[i] * 1.1f : PortraitH(n);

        public override void Exit()
        {
            ClearRigs();
            if (homeSet) field.anchoredPosition = fieldHome;
            if (game == null || game.done || game.bet <= 0) { game = null; return; }
            Race.Run(C, game);
            var res = Race.Finish(S, D, game, Now);
            App.Save.Save();
            App.Toasts.Show(Loc.F("Trường đua: về thứ {0}/{1}, nhận {2} bi", res.place + 1, res.runners, res.balls), Icon("ball"));
            game = null;
        }

        void Render()
        {
            var s = S;
            var d = D;
            double now = Now;
            cup = Race.WeekCup(s, d);
            var tr = game != null ? game.terrain : Race.TrackOf(C, Casino.Today(now));
            track.text = Loc.T("Đường hôm nay");
            for (int i = 0; i < segs.Length; i++)
            {
                bool has = i < tr.Length;
                segs[i].gameObject.SetActive(has);
                if (!has) continue;
                segs[i].color = Color.Lerp(Theme.Of(tr[i]), Theme.Paper, 0.45f);
                if (i < segNames.Length) segNames[i].text = Elements.Name(tr[i]);
            }
            int pts = Race.Points(s, d, cup, now);
            int left = Casino.PlaysLeft(s, d, Casino.Race, now);
            double mult = Casino.RaceMult(d, now);
            info.text = Loc.F("Cúp tuần {0}/{1}", pts, C.weekPts) + (mult > 1 ? " · " + Loc.F("Lễ Hội Đua ×{0}", mult.ToString("0.#")) : "");
            claim.gameObject.SetActive(Race.WeekReady(s, d, cup, now));
            claim.SetText(Loc.T("Nhận quà tuần"));
            for (int i = 0; i < tickets.Length; i++)
            {
                tickets[i].gameObject.SetActive(i < C.daily);
                tickets[i].sprite = i < left ? ticketOn : ticketOff;
            }
            for (int i = 0; i < legend.Length; i++)
            {
                double k = i < C.pay.Length ? C.pay[i] : 0;
                legend[i].text = k > 1 ? Loc.F(i == 0 ? "Nhất ×{0}" : i == 1 ? "Nhì ×{0}" : "Ba ×{0}", k.ToString("0.#"))
                    : k == 1 ? Loc.T(i == 0 ? "Nhất: hoàn tiền" : i == 1 ? "Nhì: hoàn tiền" : "Ba: hoàn tiền") : "";
            }
            var h = pick >= 0 ? d.Hero(mine) : null;
            hero.text = Loc.T("Chạm vào một con để đặt cược");
            bool racing = game != null && !game.done;
            lobby.SetActive(game == null);
            trackTap.gameObject.SetActive(game == null);
            hud.SetActive(!podium.activeSelf);
            cheer.gameObject.SetActive(racing && phase == Phase.Run);
            // chip mức cược: chip đang chọn có vòng sáng, chip quá túi tiền thì mờ; hết lượt thì cả hàng mờ (đua thử không cược)
            bool chosen = false;
            for (int i = 0; i < chips.Length; i++)
            {
                bool has = i < C.chips.Length;
                chips[i].gameObject.SetActive(has);
                if (!has) continue;
                chipTexts[i].text = C.chips[i].ToString();
                bool can = left > 0 && C.chips[i] <= s.balls;
                var img = chips[i].GetComponent<Image>();
                if (img) img.color = can ? Color.white : new Color(1, 1, 1, 0.45f);
                bool sel = left > 0 && C.chips[i] == bet && can;
                chips[i].transform.localScale = Vector3.one * (sel ? 1.12f : 1f);
                if (sel)
                {
                    chosen = true;
                    chipRing.SetParent(chips[i].transform, false);
                    chipRing.anchoredPosition = Vector2.zero;
                    chipRing.SetAsFirstSibling();
                }
            }
            chipRing.gameObject.SetActive(chosen);
            // nút Đặt cược chỉ hiện sau khi chạm chọn một con
            go.gameObject.SetActive(game == null && pick >= 0);
            hero.transform.parent.gameObject.SetActive(pick < 0); // dải băng nhắc chạm chọn nằm đúng chỗ nút Đặt cược
            go.SetText(left > 0 ? Loc.F("Đặt cược · {0} bi", bet) : Loc.T("Đua thử (hết lượt hôm nay)"));
            go.Locked = left > 0 && (!chosen || bet > s.balls);
            if (game == null) Preview();
        }

        // chưa đua: 5 con của lượt đua kế đứng ở vạch, diễn idle; con đang chọn sáng màu có vòng vàng, các con khác là bóng đen
        void Preview()
        {
            int n = lineup.Count;
            stadium.SetTrack(Race.TrackOf(C, Casino.Today(Now)), C.seg);
            stadium.Calm();
            stadium.Mood = 0.15f;
            cam = -stadium.Width * StartPad;
            stadium.SetCamera(cam);
            SetLanes(n);
            var dark = new bool[n];
            for (int i = 0; i < lanes.Length; i++)
            {
                var ln = lanes[i];
                ln.token.gameObject.SetActive(i < n);
                HideFx(ln);
                if (i >= n) continue;
                dark[i] = pick >= 0 && i != pick; // đã chọn một con thì các con khác tối bớt
                ln.token.anchoredPosition = new Vector2(stadium.ViewX(0) + Stagger(i, n, 0), -stadium.LaneY(i, n));
                ln.body.anchoredPosition = Vector2.zero;
                ln.body.localScale = Vector3.one * (i == pick ? 1.14f : 1f);
                ln.body.localEulerAngles = Vector3.zero;
                var show = D.Hero(lineup[i]);
                ln.portrait.gameObject.SetActive(false); // chân dung chỉ hiện khi không dựng được rig (TendRigs)
                if (show != null) BindPortrait(ln, show, n);
                SetMark(ln, i == pick, PortraitH(n) * 0.9f);
            }
            SetLaneHeroes(lineup.ToArray(), dark, n);
            BindBoard(pick >= 0 ? D.Hero(mine) : null);
        }

        void HideFx(Lane ln)
        {
            ln.stars.gameObject.SetActive(false);
            ln.burst.gameObject.SetActive(false);
            ln.pop.gameObject.SetActive(false);
            ln.badge.gameObject.SetActive(false);
            ln.edge.gameObject.SetActive(false);
            ln.chip.gameObject.SetActive(false);
            foreach (var d in ln.dust) d.enabled = false;
        }

        // tướng cao theo bề cao làn (màn dài thì làn rộng, tướng to hơn)
        float PortraitH(int n) => Mathf.Clamp(stadium.LaneGap(n) * 1.3f, 150, 215);

        // xếp hàng chéo ở vạch xuất phát (làn xa đứng trên, làn gần lùi lại) cho các tướng khỏi che nhau; chạy được vài mét thì hết lệch
        float Stagger(int i, int n, float pos) => ((n - 1) * 0.5f - i) * PortraitH(n) * 0.6f * (1 - Mathf.Clamp01(pos / 8f));

        // chân dung cao theo số làn, chân trùng gốc token; sao choáng trên đầu, vụt nổ giữa thân
        void BindPortrait(Lane ln, HeroDef h, int n, bool silhouette = false)
        {
            float ph = PortraitH(n);
            ln.portrait.Bind(h, ph, silhouette);
            ln.portrait.Rect.anchoredPosition = new Vector2(0, -ph * HeroArt.FootY);
            ln.stars.anchoredPosition = new Vector2(0, ph * 0.95f);
            ln.burst.rectTransform.anchoredPosition = new Vector2(ph * 0.25f, ph * 0.5f);
            ln.badge.rectTransform.anchoredPosition = new Vector2(-ph * 0.46f, ph * 0.78f);
        }

        // vòng vàng dưới chân: chỉ tướng của mình
        static void SetMark(Lane ln, bool on, float width)
        {
            ln.mark.gameObject.SetActive(on);
            if (on) ln.mark.sizeDelta = new Vector2(width, width);
        }

        void BindBoard(HeroDef h)
        {
            boardFace.gameObject.SetActive(h != null);
            if (h == null || boardHero == h.id) return;
            boardHero = h.id;
            boardFace.Bind(h, 88);
        }

        // vạch kẻ làn theo số tướng
        void SetLanes(int n)
        {
            for (int i = 0; i < lanes.Length; i++)
            {
                var line = lanes[i].line;
                if (!line) continue;
                line.gameObject.SetActive(i > 0 && i < n);
                line.anchoredPosition = new Vector2(0, -stadium.LaneLineY(i, n));
            }
        }

        void ClaimWeek()
        {
            var r = Race.ClaimWeek(S, D, cup, Now, rng);
            if (r.Count == 0) return;
            App.Save.Save();
            App.Audio.Play("chest");
            App.Toasts.Show(Loc.T("Quà tuần: ") + CasinoUi.Rewards(r), Icon("star"));
            Render();
        }

        void StartRace()
        {
            if (pick < 0 || pick >= lineup.Count) return;
            int stake = Casino.PlaysLeft(S, D, Casino.Race, Now) > 0 ? bet : 0; // hết lượt: đua thử, không cược
            var g = Race.Start(S, D, lineup, pick, stake, Now, rng, out var why);
            if (g == null)
            {
                App.Toasts.Show(why, Icon("lock"));
                return;
            }
            if (stake > 0) App.Audio.Play("bet");
            App.Save.Save();
            game = g;
            acc = 0;
            evSeen = 0;
            slow = 1;
            shake = 0;
            camBias = 0;
            leader = -1;
            leadSaid = -10;
            stretch = photo = firstIn = false;
            endHold = 0;
            for (int i = 0; i < 5; i++)
            {
                lungeT[i] = burstT[i] = popT[i] = rankPop[i] = 0;
                runPh[i] = i * 1.7f;
                finAt[i] = -1;
                rankNow[i] = edgeNow[i] = -1;
                dustNext[i] = 0;
                dustT[i, 0] = dustT[i, 1] = 0;
            }
            int n = g.runners.Count;
            stadium.SetTrack(g.terrain, C.seg);
            stadium.Calm();
            stadium.Mood = 0.45f;
            cam = -stadium.Width * StartPad;
            stadium.SetCamera(cam);
            SetLanes(n);
            var d = D;
            for (int i = 0; i < lanes.Length; i++)
            {
                var ln = lanes[i];
                bool has = i < n;
                ln.token.gameObject.SetActive(has);
                HideFx(ln);
                if (!has) continue;
                var r = g.runners[i];
                var h = d.Hero(r.hero);
                ln.portrait.gameObject.SetActive(false); // chân dung chỉ hiện khi không dựng được rig (TendRigs)
                ln.body.localScale = Vector3.one;
                ln.body.localEulerAngles = Vector3.zero;
                if (h != null)
                {
                    BindPortrait(ln, h, n);
                    ln.edgeFace.Bind(h, 54);
                }
                SetMark(ln, r.player, PortraitH(n) * 0.8f);
                ln.chip.gameObject.SetActive(true);
                ln.chip.localScale = Vector3.one * (r.player ? 1.35f : 1f);
                ln.chipFill.color = r.player ? Theme.Yellow : Theme.Of(r.elem);
                if (r.player) ln.chip.SetAsLastSibling();
            }
            SetLaneHeroes(g.runners.Select(x => x.hero).ToArray(), null, n);
            BindBoard(d.Hero(mine));
            talk.text = Loc.F("{0} tướng vào vạch xuất phát!", n);
            cheerText.text = "";
            phase = Phase.Count;
            count = CountSec;
            countShown = -1;
            startHold = 0;
            // xin nạp rig của cả đoàn ngay (gói theo hệ, đọc anim ở luồng phụ); Update hỏi lại mỗi khung
            foreach (var r in g.runners)
            {
                var rh = d.Hero(r.hero);
                var rf = rh != null ? HeroArt.FormOf(rh) : null;
                if (rf != null && !string.IsNullOrEmpty(rf.aola)) AolaActor.Ready(rf.aola);
            }
            App.Audio.Play("whoosh");
            Render();
        }

        // cổ vũ: chỉ để khán đài hò reo cho con mình (kết quả do lõi định, không đổi theo lần bấm)
        void Cheer()
        {
            if (game == null || game.done || phase != Phase.Run || cheerCool > 0) return;
            cheerCool = 0.45f;
            var me = game.Player;
            Haptics.Play(Haptic.UiTap);
            stadium.CheerJump(34);
            if (me != null)
            {
                float x = Mathf.Clamp(stadium.ViewX(me.pos), 80, stadium.Width - 80);
                stadium.Pulse(x, 420, 16);
                stadium.Burst(new Vector2(x, stadium.Height - 380), 6, Theme.Yellow, Theme.Of(me.elem));
                var h = D.Hero(me.hero);
                cheerText.text = Loc.F("Cố lên, {0}!", h != null ? h.name : me.hero);
            }
        }

        void Update()
        {
            if (!field || !stadium) return;
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.1f);
            if (game == null)
            {
                // khung đổi cỡ (lần đầu dàn màn, xoay máy): xếp lại hàng tướng mẫu theo chiều cao mới
                if (Mathf.Abs(stadium.Height - seenH) > 0.5f)
                {
                    seenH = stadium.Height;
                    Preview();
                }
                stadium.SetCamera(cam);
                stadium.Tick(dt);
                TendRigs(dt);
                for (int i = 0; i < laneCount; i++)
                {
                    if (rigs[i] == null) continue;
                    clipT[i] += dt;
                    rigs[i].Show(StageView.Idle, clipT[i] + i * 0.31f, true, 1, false, 0);
                }
                return;
            }
            if (phase == Phase.Count) Countdown(dt);
            else if (!game.done)
            {
                Direct(dt);
                acc += dt * slow;
                cheerCool = Mathf.Max(0, cheerCool - dt);
                while (acc >= Race.Dt && !game.done)
                {
                    acc -= (float)Race.Dt;
                    Race.Step(C, game);
                }
            }
            // rig tướng: mỗi khung dựng tối đa một con (trong lúc đếm ngược là đủ cả đoàn)
            if (!podium.activeSelf) TendRigs(dt);
            ConsumeEvents();
            Draw(dt);
            if (podium.activeSelf) AnimatePodium(dt);
            else if (game.done && evSeen >= game.events.Count)
            {
                endHold += dt;
                if (endHold > 0.9f) Finish();
            }
        }

        // đếm ngược trước khi chạy
        void Countdown(float dt)
        {
            // chờ cả đoàn có rig rồi mới đếm (gói nội dung nạp sau): tướng đứng idle ở vạch, không đổi hình giữa chừng
            if (countShown == -1 && !RigsSettled() && startHold < RigWaitMax)
            {
                startHold += dt;
                return;
            }
            count -= dt;
            int n = Mathf.CeilToInt((count - 0.5f) / 0.7f); // 3, 2, 1 mỗi số 0,7 giây; 0,5 giây cuối là "Chạy!"
            if (n != countShown)
            {
                countShown = n;
                ShowBig(n > 0 ? n.ToString() : Loc.T("Chạy!"), Theme.Yellow, n > 0 ? 0.7f : BigSec);
                App.Audio.Play(n > 0 ? "peg" : "whoosh");
                if (n <= 0) stadium.Wave();
            }
            if (count > 0) return;
            phase = Phase.Run;
            stadium.Mood = 0.55f;
            talk.text = Loc.T("Xuất phát! Cả đoàn lao khỏi vạch!");
            Render();
        }

        void ShowBig(string text, Color c, float sec)
        {
            big.text = text;
            big.color = c;
            bigT = bigDur = sec;
            big.rectTransform.localScale = new Vector3(1.6f, 1.6f, 1);
            big.alpha = 1;
            big.gameObject.SetActive(true);
        }

        // đạo diễn: ngôi đầu, nước rút, sát nút
        void Direct(float dt)
        {
            double len = game.Length(C);
            int a = -1, b = -1;
            for (int i = 0; i < game.runners.Count; i++)
            {
                double x = game.runners[i].pos;
                if (a < 0 || x > game.runners[a].pos) { b = a; a = i; }
                else if (b < 0 || x > game.runners[b].pos) b = i;
            }
            if (a < 0) return;
            var lead = game.runners[a];
            // đổi ngôi đầu (bỏ qua vài giây đầu còn chen nhau)
            if (a != leader && game.t > 2.5 && lead.finishT < 0 && (leader < 0 || lead.pos - game.runners[leader].pos > 0.8))
            {
                bool first = leader < 0;
                leader = a;
                BindBoard(D.Hero(lead.hero));
                if (game.t - leadSaid > 1.6)
                {
                    leadSaid = (float)game.t;
                    talk.text = first ? Loc.F("{0} đang dẫn đầu!", NameOf(a)) : Loc.F("{0} vượt lên dẫn đầu!", NameOf(a));
                    stadium.Pulse(stadium.ViewX(lead.pos), 320, 20);
                }
            }
            if (!stretch && lead.pos >= len * StretchAt)
            {
                stretch = true;
                stadium.Mood = 1f;
                stadium.Wave();
                ShowBig(Loc.T("Nước rút!"), Theme.Yellow, BigSec);
                talk.text = Loc.T("Nước rút! Cả khán đài đứng hết dậy!");
                App.Audio.Play("level", 0.6f);
            }
            // hai tướng đầu sát nhau ngay trước vạch đích: quay chậm
            bool close = !firstIn && b >= 0 && lead.pos >= len - PhotoZone && lead.pos - game.runners[b].pos <= PhotoGap;
            if (close && !photo)
            {
                photo = true;
                ShowBig(Loc.T("Sát nút!"), Theme.Paper, BigSec);
                talk.text = Loc.F("{0} và {1} sát nút nhau!", NameOf(a), NameOf(b));
            }
            slow = Mathf.MoveTowards(slow, close ? 0.35f : 1f, dt * (close ? 6f : 2.5f));
        }

        string NameOf(int i) => i >= 0 && i < game.runners.Count ? D.Hero(game.runners[i].hero)?.name ?? game.runners[i].hero : "";

        // sự kiện mới của lõi → diễn trên sân, tường thuật
        void ConsumeEvents()
        {
            for (; evSeen < game.events.Count; evSeen++)
            {
                var e = game.events[evSeen];
                int me = game.PlayerIndex;
                float ax = e.a >= 0 && e.a < game.runners.Count ? stadium.ViewX(game.runners[e.a].pos) : 0;
                switch (e.kind)
                {
                    case RaceEv.Hit:
                        Lunge(e.a, e.b);
                        if (e.b >= 0 && e.b < 5) burstT[e.b] = 0.38f;
                        Pop(e.b, Loc.T("Choáng!"), Theme.RedD);
                        talk.text = e.a >= 0 ? Loc.F("{0} húc {1} choáng váng!", NameOf(e.a), NameOf(e.b)) : Loc.F("{0} vấp ngã!", NameOf(e.b));
                        ax = e.b >= 0 && e.b < game.runners.Count ? stadium.ViewX(game.runners[e.b].pos) : ax;
                        App.Audio.Play(bonk++ % 2 == 0 ? "raceBonk1" : "raceBonk2", 0.85f); // húc (gen Magnific)
                        stadium.Pulse(ax, 300, 22);
                        if (e.b == me)
                        {
                            Haptics.Play(Haptic.UiError);
                            shake = 12;
                        }
                        else if (e.a == me)
                        {
                            Haptics.Play(Haptic.UiTap);
                            shake = 7;
                        }
                        break;
                    case RaceEv.Trip:
                        Lunge(e.a, e.b);
                        Pop(e.a, Loc.T("Vấp!"), Theme.Orange);
                        talk.text = Loc.F("{0} lao vào {1} nhưng hụt, vấp ngã!", NameOf(e.a), NameOf(e.b));
                        stadium.Pulse(ax, 220, 12);
                        break;
                    case RaceEv.Dodge:
                        Lunge(e.a, e.b);
                        Pop(e.b, Loc.T("Né!"), Theme.BlueD);
                        Pop(e.a, Loc.T("Vấp!"), Theme.Orange, false);
                        talk.text = Loc.F("{0} né gọn cú húc của {1}!", NameOf(e.b), NameOf(e.a));
                        stadium.Pulse(ax, 260, 18);
                        break;
                    case RaceEv.Gust:
                        Pop(e.a, Loc.T("Bứt tốc!"), Theme.GreenD);
                        talk.text = Loc.F("{0} bứt tốc vọt lên!", NameOf(e.a));
                        App.Audio.Play("raceDash", e.a == me ? 0.9f : 0.5f); // vọt lên (gen Magnific)
                        stadium.Pulse(ax, 260, 16);
                        if (e.a == me) Haptics.Play(Haptic.UiTap);
                        break;
                    case RaceEv.Finish:
                        int place = Race.Order(game).IndexOf(e.a);
                        if (e.a >= 0 && e.a < 5) finAt[e.a] = Time.unscaledTime;
                        if (place == 0)
                        {
                            firstIn = true;
                            slow = 1;
                            talk.text = Loc.F("{0} về nhất!", NameOf(e.a));
                            BindBoard(D.Hero(game.runners[e.a].hero));
                            var c = Theme.Of(game.runners[e.a].elem);
                            stadium.Flash(photo ? 0.85f : 0.5f);
                            stadium.Burst(new Vector2(stadium.ViewX(game.Length(C)), stadium.LaneY(e.a, game.runners.Count) - 60), 16, Theme.Yellow, c);
                            stadium.Rain(2.6f, Theme.Yellow, c);
                            stadium.Wave();
                            stadium.Mood = 1f;
                            shake = 6;
                            App.Audio.Play("stamp", 1f, 0.9f);
                        }
                        else if (e.a == me) stadium.Pulse(ax, 400, 20);
                        break;
                }
            }
        }

        void Lunge(int a, int b)
        {
            if (a < 0 || a >= 5 || b < 0 || b >= game.runners.Count) return;
            float dx = (float)(game.runners[b].pos - game.runners[a].pos) * RaceStadium.K;
            float dy = lanes[b].token.anchoredPosition.y - lanes[a].token.anchoredPosition.y;
            lungeDir[a] = new Vector2(Mathf.Clamp(dx * 0.7f, -240, 240) + Mathf.Sign(dx) * 20, Mathf.Clamp(dy * 0.5f, -90, 90));
            lungeT[a] = 0.28f;
            if (rigs[a] != null && rigs[a].HasClip(StageView.Attack)) atkT[a] = Mathf.Min(rigs[a].Duration(StageView.Attack), 0.8f);
        }

        void Pop(int i, string text, Color c, bool replace = true)
        {
            if (i < 0 || i >= 5) return;
            if (!replace && popT[i] > 0) return;
            var ln = lanes[i];
            ln.pop.text = text;
            ln.pop.color = c;
            bool left = ln.token.anchoredPosition.x > field.rect.width * 0.68f;
            ln.pop.rectTransform.pivot = new Vector2(left ? 1 : 0, 0.5f);
            ln.pop.alignment = left ? TextAlignmentOptions.MidlineRight : TextAlignmentOptions.MidlineLeft;
            popT[i] = PopSec;
        }

        // vị trí để vẽ: về đích rồi thì chạy trớn thêm một đoạn rồi dừng
        float DrawPos(int i, double len)
        {
            var r = game.runners[i];
            if (r.finishT < 0 || finAt[i] < 0) return (float)r.pos;
            return (float)len + CoastUnits * (1 - Mathf.Exp(-1.3f * (Time.unscaledTime - finAt[i])));
        }

        void Draw(float dt)
        {
            float w = stadium.Width;
            int n = game.runners.Count;
            float hh = PortraitH(n);
            double len = game.Length(C);
            float tNow = Time.unscaledTime;
            float anim = dt * slow; // quay chậm thì nhịp chạy cũng chậm theo
            int me = game.PlayerIndex;
            // máy quay bám tướng mình, lệch về phía đối thủ gần nhất (đang bị đuổi thì hé phía sau, đang đuổi thì hé phía trước);
            // đầu và cuối đường thì đứng lại
            float mePx = me >= 0 ? DrawPos(me, len) * RaceStadium.K : 0, near = float.MaxValue;
            for (int i = 0; i < n; i++)
            {
                if (i == me) continue;
                float gapPx = DrawPos(i, len) * RaceStadium.K - mePx;
                if (Mathf.Abs(gapPx) < Mathf.Abs(near)) near = gapPx;
            }
            float bias = near == float.MaxValue ? 0 : Mathf.Clamp(near * 0.4f, -w * 0.2f, w * 0.12f);
            camBias = Mathf.Lerp(camBias, bias, 1 - Mathf.Exp(-2.5f * dt));
            float target = mePx - w * 0.4f + camBias;
            target = Mathf.Clamp(target, -w * StartPad, (float)len * RaceStadium.K - w * 0.45f);
            cam = phase == Phase.Count ? target : Mathf.Lerp(cam, target, 1 - Mathf.Exp(-7f * dt));
            stadium.SetCamera(cam);
            stadium.Tick(dt);
            if (shake > 0.1f)
            {
                shake = Mathf.MoveTowards(shake, 0, dt * 40);
                field.anchoredPosition = fieldHome + new Vector2(Mathf.Sin(tNow * 71) * shake, Mathf.Cos(tNow * 57) * shake * 0.6f);
            }
            else field.anchoredPosition = fieldHome;
            if (bigT > 0)
            {
                bigT -= dt;
                float k = 1 - Mathf.Clamp01(bigT / bigDur);
                float s = k < 0.15f ? Mathf.Lerp(1.6f, 1f, k / 0.15f) : 1 + k * 0.08f;
                big.rectTransform.localScale = new Vector3(s, s, 1);
                big.alpha = Mathf.Clamp01(bigT / 0.25f);
                if (bigT <= 0) big.gameObject.SetActive(false);
            }
            // hạng đang giữ: về đích trước xếp trước, còn chạy thì ai xa hơn xếp trước
            for (int i = 0; i < n && i < 5; i++)
            {
                var ri = game.runners[i];
                int ahead = 0;
                for (int j = 0; j < n; j++)
                {
                    if (j == i) continue;
                    var rj = game.runners[j];
                    bool before = ri.finishT >= 0
                        ? rj.finishT >= 0 && (rj.finishT < ri.finishT || rj.finishT == ri.finishT && j < i)
                        : rj.finishT >= 0 || rj.pos > ri.pos || rj.pos == ri.pos && j < i;
                    if (before) ahead++;
                }
                placeOf[i] = ahead;
            }
            float mapW = map ? map.rect.width : 0;
            for (int i = 0; i < n && i < lanes.Length; i++)
            {
                var ln = lanes[i];
                var r = game.runners[i];
                bool run = phase == Phase.Run;
                bool stunned = run && r.Stunned(game.t) && r.finishT < 0;
                bool coasting = r.finishT >= 0 && tNow - finAt[i] < 1.6f;
                bool moving = run && !stunned && (r.finishT < 0 || coasting);
                float pos = DrawPos(i, len);
                float x = pos * RaceStadium.K - cam + Stagger(i, n, pos);
                float laneY = stadium.LaneY(i, n);
                float fh = FigureH(i, n); // chiều cao hình đang hiện (rig thấp hơn khung chân dung)
                // lao vào đánh: ra rồi về
                Vector2 lunge = Vector2.zero;
                if (lungeT[i] > 0)
                {
                    lungeT[i] -= dt;
                    float k = Mathf.Sin(Mathf.Clamp01(1 - lungeT[i] / 0.28f) * Mathf.PI);
                    lunge = lungeDir[i] * k;
                }
                ln.token.anchoredPosition = new Vector2(x + lunge.x, -laneY);
                // nhảy cóc: nhịp theo tốc độ, chúi về trước, bóp giãn lúc chạm đất; mỗi lần chạm đất tung bụi
                float v = moving ? (r.finishT < 0 ? (float)Race.Speed(C, game, r) : 6f) : 0;
                if (moving) runPh[i] += anim * (5.5f + 0.4f * v);
                float ph = runPh[i];
                float up = Mathf.Abs(Mathf.Sin(ph));
                var rig = rigs[i];
                bool walks = rig != null && rigWalk[i]; // rig có clip walk tự bước: không nhảy cóc, không bóp giãn bằng code
                float hop = moving && !walks ? up * (rig != null ? 12f : 20f) : 0;
                float squash = moving && rig == null ? 1 + (up < 0.25f ? -0.09f : 0.035f) : 1;
                bool boosted = moving && r.finishT < 0 && game.t < r.gustUntil;
                ln.body.anchoredPosition = new Vector2(0, hop + lunge.y);
                ln.body.localScale = new Vector3(2 - squash, squash, 1);
                float lean = rig != null ? 0 // rig không xoay nghiêng: xoay ảnh chụp làm nét mờ
                    : stunned ? Mathf.Sin(tNow * 18 + i) * 10 : moving ? -(boosted ? 11 : 5) + Mathf.Sin(ph) * 3 : 0;
                ln.body.localEulerAngles = new Vector3(0, 0, lean);
                if (ln.face) ln.face.color = stunned ? new Color(0.68f, 0.68f, 0.76f) : Color.white;
                if (rig != null && !onPod[i])
                {
                    // clip của rig: đang húc → đánh; choáng → trúng đòn rồi đứng xám; chạy → walk theo tốc độ; còn lại đứng
                    atkT[i] = Mathf.Max(0, atkT[i] - dt);
                    string clip = atkT[i] > 0 ? StageView.Attack : stunned ? StageView.Hit : moving && walks ? AolaSticker.Walk : StageView.Idle;
                    if (clip != clipNow[i])
                    {
                        clipNow[i] = clip;
                        clipT[i] = 0;
                    }
                    float rate = clip == AolaSticker.Walk ? Mathf.Clamp(v / 10f, 0.6f, 1.5f) * 1.7f : 1f;
                    clipT[i] += anim * rate;
                    bool once = clip == StageView.Attack || clip == StageView.Hit;
                    bool held = clip == StageView.Hit && clipT[i] >= rig.Duration(StageView.Hit); // hết clip trúng đòn mà còn choáng: đứng lắc
                    if (x > -260 && x < w + 260)
                        rig.Show(held ? StageView.Idle : clip, clipT[i], !once || held, 1, stunned, burstT[i] > 0 ? burstT[i] / 0.38f : 0);
                    else rig.Hold();
                }
                if (moving)
                {
                    int step = Mathf.FloorToInt(ph / Mathf.PI);
                    if (step != dustNext[i])
                    {
                        dustNext[i] = step;
                        int k = step & 1;
                        dustT[i, k] = DustSec;
                        dustX[i, k] = pos * RaceStadium.K - 26;
                    }
                }
                for (int k = 0; k < ln.dust.Length && k < 2; k++)
                {
                    var d = ln.dust[k];
                    if (dustT[i, k] <= 0)
                    {
                        if (d.enabled) d.enabled = false;
                        continue;
                    }
                    dustT[i, k] -= dt;
                    float q = 1 - Mathf.Clamp01(dustT[i, k] / DustSec);
                    d.enabled = true;
                    var c = Color.Lerp(stadium.SegColor(stadium.SegAt(dustX[i, k])), Color.white, 0.45f);
                    d.color = new Color(c.r, c.g, c.b, 0.85f * (1 - q));
                    d.rectTransform.anchoredPosition = new Vector2(dustX[i, k] - cam - q * 26, -laneY + 6 + q * 14);
                    float s = Mathf.Lerp(0.45f, 1.15f, q) * (boosted ? 1.3f : 1f);
                    d.rectTransform.localScale = new Vector3(s, s, 1);
                }
                if (ln.mark.gameObject.activeSelf) ln.markSpin.localEulerAngles = new Vector3(0, 0, -tNow * 70f);
                // sao choáng xoay trên đầu
                ln.stars.gameObject.SetActive(stunned);
                if (stunned)
                    for (int k = 0; k < ln.spin.childCount; k++)
                    {
                        float a = tNow * 5.5f + k * Mathf.PI * 2 / ln.spin.childCount;
                        var st = (RectTransform)ln.spin.GetChild(k);
                        st.anchoredPosition = new Vector2(Mathf.Cos(a) * fh * 0.32f, Mathf.Sin(a) * fh * 0.11f);
                        float s = 0.75f + 0.3f * Mathf.Sin(a);
                        st.localScale = new Vector3(s, s, 1);
                        st.localEulerAngles = new Vector3(0, 0, tNow * 200f);
                    }
                // vụt nổ chỗ trúng
                if (burstT[i] > 0)
                {
                    burstT[i] -= dt;
                    float k = 1 - burstT[i] / 0.38f;
                    ln.burst.gameObject.SetActive(true);
                    float s = k < 0.4f ? Mathf.Lerp(0.3f, 1.4f, k / 0.4f) : Mathf.Lerp(1.4f, 0.6f, (k - 0.4f) / 0.6f);
                    ln.burst.rectTransform.localScale = new Vector3(s, s, 1);
                    ln.burst.color = new Color(1f, 0.85f, 0.25f, 1 - Mathf.Clamp01((k - 0.5f) * 2));
                }
                else ln.burst.gameObject.SetActive(false);
                // chữ nổi bay lên, mờ dần
                if (popT[i] > 0)
                {
                    popT[i] -= dt;
                    float k = 1 - popT[i] / PopSec;
                    ln.pop.gameObject.SetActive(true);
                    float side = ln.pop.rectTransform.pivot.x > 0.5f ? -1 : 1;
                    ln.pop.rectTransform.anchoredPosition = new Vector2(side * (fh * 0.42f + 6 + k * 10), fh * 0.5f + k * 26);
                    var c = ln.pop.color;
                    ln.pop.color = new Color(c.r, c.g, c.b, 1 - Mathf.Clamp01((k - 0.6f) / 0.4f));
                }
                else ln.pop.gameObject.SetActive(false);
                // số hạng đang giữ (bật nhẹ khi đổi hạng)
                int place = placeOf[i];
                if (run)
                {
                    if (place != rankNow[i])
                    {
                        if (rankNow[i] >= 0 && place < rankNow[i]) rankPop[i] = 0.3f;
                        rankNow[i] = place;
                        ln.badgeText.text = (place + 1).ToString();
                        ln.badge.color = place == 0 ? Theme.Yellow : Theme.Paper2;
                    }
                    ln.badge.gameObject.SetActive(true);
                    rankPop[i] = Mathf.Max(0, rankPop[i] - dt);
                    float s = 1 + Mathf.Sin(rankPop[i] / 0.3f * Mathf.PI) * 0.45f;
                    ln.badge.rectTransform.localScale = new Vector3(s, s, 1);
                }
                // ra khỏi khung: thẻ ở mép báo cách tướng mình mấy mét
                bool off = run && (x < -36 || x > w + 36);
                if (ln.edge.gameObject.activeSelf != off) ln.edge.gameObject.SetActive(off);
                if (off)
                {
                    ln.edge.anchoredPosition = new Vector2(x < 0 ? 78 : w - 78, -laneY + fh * 0.42f);
                    int gap = me >= 0 ? Mathf.RoundToInt(Mathf.Abs(pos - DrawPos(me, len))) : 0;
                    if (gap != edgeNow[i])
                    {
                        edgeNow[i] = gap;
                        ln.edgeText.text = gap + "m";
                    }
                }
                // bản đồ nhỏ
                if (mapW > 0) ln.chip.anchoredPosition = new Vector2(mapW * Mathf.Clamp01((float)(r.pos / len)), ln.chip.anchoredPosition.y);
            }
        }

        void ClosePodium()
        {
            podium.SetActive(false);
            result.SetActive(false);
        }

        // đua xong: tính thưởng rồi mở lễ trao giải
        void Finish()
        {
            var res = Race.Finish(S, D, game, Now);
            App.Save.Save();
            cheerText.text = "";
            big.gameObject.SetActive(false);
            stadium.Mood = res.place < 3 ? 1f : 0.6f;
            resTitle.text = res.place == 0 ? Loc.T("Về nhất!") : Loc.F("Về thứ {0}/{1}", res.place + 1, res.runners);
            string money = game.bet <= 0 ? Loc.T("Đua thử: không cược, không thưởng.")
                : res.balls > game.bet ? Loc.F("Thắng cược! Đặt {0} bi, nhận về {1} bi", game.bet, res.balls)
                : res.balls == game.bet ? Loc.F("Hoà tiền: nhận lại {0} bi", res.balls)
                : res.balls > 0 ? Loc.F("Đặt {0} bi, nhận về {1} bi", game.bet, res.balls) : Loc.F("Thua cược: mất {0} bi", game.bet);
            lastPlace = game.bet > 0 ? res.place : -1;
            resInfo.text = money + (res.points > 0 ? "\n" + Loc.F("+{0} điểm cúp tuần", res.points) + (res.weekReady ? " · " + Loc.T("Đủ điểm: nhận quà tuần!") : "") : "");
            bool medal = res.place < 3 && resIcons != null && res.place < resIcons.Length && resIcons[res.place];
            resIcon.gameObject.SetActive(medal);
            if (medal) resIcon.sprite = resIcons[res.place];
            var order = Race.Order(game);
            for (int i = 0; i < resRows.Length; i++)
            {
                bool has = i < order.Count;
                resRows[i].gameObject.SetActive(has);
                if (!has) continue;
                var r = game.runners[order[i]];
                resRows[i].text = Loc.F("{0}. {1} · húc trúng {2} · bị choáng {3}", i + 1, NameOf(order[i]), r.hits, r.stuns);
                resRows[i].color = r.player ? Theme.RedD : Theme.Ink;
            }
            for (int k = 0; k < podSlots.Length; k++)
            {
                var sl = podSlots[k];
                bool has = k < order.Count;
                var r = has ? game.runners[order[k]] : null;
                var h = has ? D.Hero(r.hero) : null;
                sl.root.gameObject.SetActive(false); // AnimatePodium bật khi tới lượt nhảy lên
                sl.tag.gameObject.SetActive(h != null);
                podRunner[k] = -1;
                if (h == null) continue;
                float podH = PodHeight[Mathf.Min(k, PodHeight.Length - 1)];
                int lane = order[k];
                var rig = lane < rigs.Length ? rigs[lane] : null;
                sl.portrait.gameObject.SetActive(rig == null);
                if (rig != null)
                {
                    // rig của tướng rời làn lên đứng bục (phóng theo cỡ bục), diễn idle
                    podRunner[k] = lane;
                    onPod[lane] = true;
                    rig.Rect.SetParent(sl.body, false);
                    rig.Rect.anchoredPosition = Vector2.zero;
                    float sc = podH * RigK / Mathf.Max(1, rigBase[lane]) / RigSS;
                    rig.Rect.localScale = new Vector3(sc, sc, 1);
                }
                sl.portrait.Bind(h, podH);
                sl.portrait.Rect.anchoredPosition = new Vector2(0, -sl.portrait.Rect.sizeDelta.y * HeroArt.FootY);
                sl.name.text = h.name;
                sl.tag.color = r.player ? Theme.Yellow : Theme.Paper;
            }
            podT = 0;
            podStage = 0;
            podium.SetActive(true);
            result.SetActive(false);
            AnimatePodium(0);
            Haptics.Play(res.place == 0 ? Haptic.Win : Haptic.UiTap);
            Render();
        }

        // lễ trao giải: tối màn, bục trồi lên, hạng ba / nhì / nhất lần lượt nhảy lên bục, rồi hiện thưởng
        void AnimatePodium(float dt)
        {
            podT += dt;
            podDim.color = new Color(0.1f, 0.08f, 0.06f, 0.6f * Mathf.Clamp01(podT / 0.3f));
            float u = Mathf.Clamp01(podT / 0.45f) - 1;
            float rise = 1 + 2.2f * u * u * u + 1.2f * u * u; // trồi quá đà một chút rồi về
            podRise.anchoredPosition = new Vector2(podHome.x, podHome.y - 900 * (1 - rise));
            for (int k = 0; k < podSlots.Length; k++)
            {
                var sl = podSlots[k];
                if (!sl.tag.gameObject.activeSelf) continue; // không có tướng hạng này
                float tt = podT - (0.55f + (podSlots.Length - 1 - k) * 0.3f);
                if (sl.root.gameObject.activeSelf != tt >= 0) sl.root.gameObject.SetActive(tt >= 0);
                if (tt < 0) continue;
                float fall = Mathf.Clamp01(tt / 0.22f);
                float drop = 320 * (1 - fall * fall);
                float land = tt - 0.22f;
                float sq = land >= 0 && land < 0.18f ? 1 - 0.2f * Mathf.Sin(land / 0.18f * Mathf.PI) : 1;
                float hop = land <= 0.3f ? 0 : k == 0 ? Mathf.Abs(Mathf.Sin((land - 0.3f) * 5.2f)) * 28 : Mathf.Max(0, Mathf.Sin((land - 0.3f) * 4f + k * 1.9f)) * 9;
                sl.body.anchoredPosition = new Vector2(0, drop + hop);
                sl.body.localScale = new Vector3(2 - sq, sq, 1);
                int lane = podRunner[k];
                if (lane >= 0 && rigs[lane] != null) rigs[lane].Show(StageView.Idle, podT + k * 0.37f, true, 1, false, 0);
            }
            // mốc: từng tướng chạm bục; hạng nhất chạm bục thì hoa giấy; rồi hiện bảng thưởng
            while (podStage < PodMarks.Length && podT >= PodMarks[podStage])
            {
                if (podStage < 2) App.Audio.Play("land", 0.7f);
                else if (podStage == 2)
                {
                    var win = game.runners[Race.Order(game)[0]];
                    stadium.Rain(4.5f, Theme.Yellow, Theme.Of(win.elem));
                    stadium.Wave();
                    stadium.Flash(0.3f);
                    App.Audio.Play(Race.PlaceOf(game) == 0 ? "win" : "stamp");
                }
                else result.SetActive(true);
                podStage++;
            }
            if (result.activeSelf)
            {
                float k = Mathf.Clamp01((podT - PodMarks[3]) / 0.25f);
                float sc = Mathf.Lerp(1.5f, 1f, k);
                resTitle.rectTransform.localScale = new Vector3(sc, sc, 1);
                if (resIcon.gameObject.activeSelf) resIcon.rectTransform.localEulerAngles = new Vector3(0, 0, Mathf.Sin(podT * 2.4f) * 6);
            }
        }
    }
}
