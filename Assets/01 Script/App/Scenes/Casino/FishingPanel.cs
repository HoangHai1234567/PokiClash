// Bến câu (GD_Claude/32_BenCau_Scene.md; luật câu ở 29_DaoCasino.md mục 6.2). Scene riêng vẽ tay (người dùng 2026-11-26: "gen thẳng 1 scene
// riêng, có người đứng câu cá có animation, có shader nước, thả câu có tương tác"):
// - Cảnh: ảnh nền ben_cau_nen (2:3, phủ kín khung) với shader PokiClash/UIPondWater (lăn tăn, bọt vỗ bờ, vệt sóng, gợn, bóng cá, vùng câu).
//   Cậu thám hiểm (rig AtomSpine cau_ca.bytes, AtomikGraphic) đứng cuối bến; dây câu (FishingLine) võng từ xương dau_can tới phao.
// - Cách chơi như Clash of Critters (người dùng 2026-11-26 "cách chơi phải giống clash of critters", "căn 1 thanh chạy rồi tap đúng
//   lúc"; bản 3: "bỏ phần nâng cấp cần đi, khi thả câu thì cho người chơi thả random trên hồ câu", "có cá thì không cần ấn giật nữa"):
//   chạm nút CÂU (hoặc mặt nước): clip quang, sự kiện "tha" thì phao bay theo cung tới một chỗ ngẫu nhiên trên hồ (phần nhìn thấy,
//   ngoài chỗ người che). Vùng nơi phao rơi (vòng elip quanh chỗ đứng như lam_nuoc.py: Gần bờ / Xa bờ / Rạn đá) là chỗ câu của lõi.
// - Phao 3D: cắt theo mặt nước (phần trên rõ, phần dưới mờ xanh), nhún theo lò xo (rơi chìm sâu rồi nảy, rỉa nhấp, cắn chìm hẳn,
//   kéo nghiêng theo dây); nước quanh phao có vòng bám, gợn toả, vệt rẽ nước khi bị kéo (shader _Bob, _Wake).
// - Chờ: bóng cá bơi lại phao, rỉa (phao nhấp, gợn nhỏ), cắn thì phao chìm, hiện "!" rồi tự vào thanh chạy (không phải chạm giật).
// - Kéo: mọi con đều qua thanh chạy, chạm trúng vùng vàng đủ max(1, Fishing.Ticks) nhịp trong ReelTime giây (cá nhỏ 1 nhịp), trượt
//   mất MissCost giây. Mỗi nhịp trúng: clip nhip, nước bắn ở phao, phao bị kéo lại gần. Trúng: clip trung, sự kiện
//   "ca_len" thì cá vọt khỏi nước bay về đầu cần, rồi thẻ kết quả. Sổng: clip hut, dây chùng, bóng cá lao đi.
// Lõi: Core/Casino/Fishing.cs (mồi, chỗ câu = vùng phao rơi, chọn cá, Sổ Cá, bán cá, Cá Vua; cần câu không còn nâng). Hình 35 con cá
// (30 loài + 5 Cá Vua) ở Assets/03 Art/Casino/BenCau/Ca (GPT 2.6, càng hiếm càng dị): thẻ kết quả, Sổ Cá (chưa bắt: bóng đen), cá vọt. Mọi phần tử dựng sẵn trong
// prefab (menu "PokiClash/Prefab/Đảo Casino/Bến câu: dựng scene"); ở đây không sinh GameObject.
using System;
using System.Collections.Generic;
using System.Linq;
using AtomSpine;
using PokiClash.Core;
using PokiClash.Game;
using PokiClash.UI;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

namespace PokiClash
{
    public sealed class FishingPanel : MonoBehaviour
    {
        [Serializable]
        public struct DexCell
        {
            public Image dot, ring;
            public TextMeshProUGUI name, info;
        }

        [Serializable]
        public struct ReelUi
        {
            public RectTransform panel, bar, zone, needle;
            public Image zoneImg, timerRing;
            public Image[] pips;
            public TextMeshProUGUI timer, penalty, hint;
        }

        [Serializable]
        public struct ResultUi
        {
            public GameObject root;
            public RectTransform card;
            public Image dot, ring, medal;
            public TextMeshProUGUI name, info, rewards;
            public RectTransform banner;
            public TextMeshProUGUI bannerText;
            public SketchButton ok;
        }

        // cảnh: nền + shader nước, người câu, dây, phao, đồ ngắm, giọt nước, cá vọt
        [Serializable]
        public struct SceneUi
        {
            public RectTransform world;
            public Image plate;
            public AimArea aim;
            public AtomikGraphic fisher;
            public FishingLine line;
            public RectTransform bobber, bang;
            public RectTransform bobTop, bobUnder;   // hai bản hình phao: trên mặt nước (cắt theo RectMask2D), dưới nước (mờ xanh)
            public RectTransform[] drops;
            public TextMeshProUGUI hint;
            public Image leapFish;
            public TextAsset rig, water;
        }

        [SerializeField] SceneUi sc;
        [Header("Nút câu")]
        [SerializeField] SketchButton actBtn;
        [SerializeField] HoldArea actTap;
        [Header("Kéo")]
        [SerializeField] ReelUi reel;
        [Header("Trên")]
        [SerializeField] TextMeshProUGUI baitText;
        [Header("Dưới")]
        [SerializeField] SketchButton dexBtn, sellBtn, baitBtn;
        [Header("Kết quả")]
        [SerializeField] ResultUi res;
        [Header("Sổ Cá")]
        [SerializeField] GameObject dex;
        [SerializeField] TextMeshProUGUI dexHead;
        [SerializeField] DexCell[] dexCells;
        [SerializeField] SketchButton dexClose;
        [Header("Hình cá")]
        [SerializeField] Sprite[] fishArt;   // tên sprite = id loài (Assets/03 Art/Casino/BenCau/Ca, ArtGen/Casino/ben_cau/ca/cat_ca.py)

        enum St { Idle, Fly, Wait, Bite, Reel, Pull, Result }

        // ảnh nền gốc và vùng câu (khớp lam_nuoc.py, nuoc.json)
        const float PW = 1024f, PH = 1536f;
        static readonly Vector2 Feet = new Vector2(512, 1405);   // chỗ đứng của rig trên ảnh nền (px, y xuống)
        const float RigK = 610f / 683f;                           // px ảnh nền / đơn vị rig (cao như cảnh A)
        static readonly Vector2 Stand = new Vector2(512, 1300);   // chỗ đứng (tâm vòng vùng câu)
        const float RNear = 400f, RFar = 790f, YS = 1.15f;
        // điểm ngắm mặc định mỗi vùng (ngoài chỗ cậu đứng che); chỗ người che (px ảnh nền) không thả phao được
        static readonly Vector2[] ZoneTarget = { new Vector2(700, 1060), new Vector2(600, 700), new Vector2(470, 560) };
        static readonly Rect Body = new Rect(380, 780, 280, 660);

        const float ZoneScale = 0.6f, NeedleTol = 0.012f, FlyTime = 0.5f, PullTime = 0.55f;

        St st;
        int ticks, hits, spot;
        float t, timeLeft, zoneC, zoneW, needleP, needleDir, needleSpeed, lastTap = -1, shake, flash, penaltyT, resT, nibbleT;
        float relaxT, castFallback = -1, bobY, bobV, bobRest, tilt, wakeK;
        Vector2 bobPrev;
        bool released, castQueued;
        Vector2 target, lastTarget, bob, barBase, flyFrom, flyTo;   // bob, target: px ảnh nền; flyFrom/To: toạ độ world (cục bộ)
        Vector2 bobLocal;
        FishBite bite;
        int resClass;
        string assist;
        Rng rng;
        Action onRefresh;
        Material mat;
        int waterW, waterH;
        byte[] waterMask;
        readonly Vector4[] rip = new Vector4[8];
        int ripNext;
        readonly Vector4[] fishA = new Vector4[6], fishB = new Vector4[6];

        struct Shadow
        {
            public Vector2 pos, to, vel;
            public float len, alpha, phase, speed;
            public bool on;
        }

        readonly Shadow[] fishes = new Shadow[6];       // 0: cá cắn câu; 1..5: cá bơi lững lờ
        Vector2[] dropVel;
        float[] dropLife;
        float leapT = -1;
        Vector2 leapFrom;
        static AtomSpine.AtomikAsset rigAsset;

        static SaveData S => App.Save.Data;
        static GameData D => App.Data;
        static FishingConfig C => D.Cfg.casino.fishing;
        static double Now => SaveService.Now();
        static Sprite Icon(string n) => App.Art ? App.Art.Icon(n) : null;

        public string State => st.ToString();

        // Dùng khi dựng prefab (Editor).
        public void Setup(SceneUi scene, SketchButton act, HoldArea actArea, ReelUi reelUi, TextMeshProUGUI bait,
            SketchButton dexB, SketchButton sellB, SketchButton baitB, ResultUi result, GameObject dexGo,
            TextMeshProUGUI dHead, DexCell[] cells, SketchButton dClose)
        {
            sc = scene; actBtn = act; actTap = actArea; reel = reelUi; baitText = bait;
            dexBtn = dexB; sellBtn = sellB; baitBtn = baitB; res = result; dex = dexGo; dexHead = dHead; dexCells = cells; dexClose = dClose;
        }

        public void Open(Action refresh)
        {
            onRefresh = refresh;
            rng = new Rng(Rng.RandomSeed());
            gameObject.SetActive(true);
            LoadWater();
            if (sc.plate && sc.plate.material)
            {
                mat = new Material(sc.plate.material);
                sc.plate.material = mat;
            }
            LoadRig();
            if (sc.aim) sc.aim.Down = OnDown;
            spot = 0;
            if (actTap) actTap.Down = Act;
            dexBtn.SetOnClick(ShowDex);
            sellBtn.SetOnClick(Sell);
            baitBtn.SetOnClick(BuyBait);
            res.ok.SetOnClick(() => { res.root.SetActive(false); ToIdle(); });
            dexClose.SetOnClick(() => dex.SetActive(false));
            res.root.SetActive(false);
            dex.SetActive(false);
            barBase = reel.bar.anchoredPosition;
            int nd = sc.drops?.Length ?? 0;
            dropVel = new Vector2[nd];
            dropLife = new float[nd];
            foreach (var d in sc.drops) d.gameObject.SetActive(false);
            if (sc.leapFish) sc.leapFish.gameObject.SetActive(false);
            for (int i = 1; i < fishes.Length; i++) SpawnAmbient(i, true);
            fishes[0].on = false;
            ToIdle();
            Render();
        }

        public void Close() => gameObject.SetActive(false);

        // Dùng khi dựng prefab (Editor).
        public void SetFishArt(Sprite[] art) => fishArt = art;

        Sprite FishArt(string id)
        {
            if (fishArt == null || id == null) return null;
            foreach (var a in fishArt)
                if (a && a.name == id) return a;
            return null;
        }

        // hình cá vào một Image: có hình thì hiện hình (chưa biết loài: bóng đen), không có thì chấm màu hệ như cũ
        void ShowFish(Image img, FishDef f, bool known)
        {
            var spr = FishArt(f.id);
            if (spr)
            {
                Theme.SetSprite(img, spr);   // đổi cả material: chấm Sketch cũ dùng material giải mã, giữ lại thì hình cá bị xám
                img.preserveAspect = true;
                img.color = known ? Color.white : new Color(0.13f, 0.11f, 0.1f, 0.78f);
            }
            else img.color = known ? Theme.Of(f.elem) : new Color(0.8f, 0.77f, 0.7f);
        }

        void LoadWater()
        {
            waterMask = null;
            if (!sc.water || sc.water.bytes.Length < 8) return;
            var b = sc.water.bytes;
            waterW = BitConverter.ToInt32(b, 0);
            waterH = BitConverter.ToInt32(b, 4);
            if (waterW <= 0 || waterH <= 0 || b.Length < 8 + waterW * waterH) return;
            waterMask = new byte[waterW * waterH];
            Buffer.BlockCopy(b, 8, waterMask, 0, waterMask.Length);
        }

        void LoadRig()
        {
            if (!sc.fisher || !sc.rig) return;
            if (!rigAsset)
            {
                try { rigAsset = AtomikFile.Load(sc.rig.bytes); }
                catch (Exception e) { Debug.LogWarning("[Bến câu] Không nạp được rig " + sc.rig.name + ": " + e.Message); }
            }
            if (!rigAsset) return;
            sc.fisher.overlayClip = "";
            sc.fisher.asset = rigAsset;
            sc.fisher.EventFired -= OnRigEvent;
            sc.fisher.EventFired += OnRigEvent;
            sc.fisher.CrossFade("idle", 0f, true);
        }

        // ---------- toạ độ: px ảnh nền (y xuống) <-> cục bộ của world (tâm, y lên) ----------

        Vector2 WorldSize => sc.world ? sc.world.rect.size : new Vector2(PW, PH);
        Vector2 PlateToLocal(Vector2 pp) { var s = WorldSize; return new Vector2((pp.x / PW - 0.5f) * s.x, (0.5f - pp.y / PH) * s.y); }
        Vector2 LocalToPlate(Vector2 l) { var s = WorldSize; return new Vector2((l.x / s.x + 0.5f) * PW, (0.5f - l.y / s.y) * PH); }
        float LocalPerPlate => WorldSize.x / PW;
        static Vector2 Sh(Vector2 pp) => new Vector2(pp.x, PH - pp.y);   // sang hệ shader (uv, y lên)

        bool Water(Vector2 pp)
        {
            if (waterMask == null) return pp.y > 330 && pp.y < 1180;
            int x = Mathf.FloorToInt(pp.x / 4f), y = Mathf.FloorToInt(pp.y / 4f);
            if (x < 0 || y < 0 || x >= waterW || y >= waterH) return false;
            return waterMask[y * waterW + x] != 0;
        }

        // thả phao được: có nước và không nằm sau lưng cậu (bị người che)
        bool Castable(Vector2 pp) => Water(pp) && !Body.Contains(pp);

        int ZoneAt(Vector2 pp)
        {
            if (!Castable(pp)) return 0;
            float r = Mathf.Sqrt((pp.x - Stand.x) * (pp.x - Stand.x) + (pp.y - Stand.y) * YS * (pp.y - Stand.y) * YS);
            return r < RNear ? 1 : r < RFar ? 2 : 3;
        }

        Vector2 RandomWater(int zone = 0)
        {
            for (int i = 0; i < 60; i++)
            {
                var p = new Vector2(UnityEngine.Random.Range(60f, PW - 60f), UnityEngine.Random.Range(340f, 1170f));
                if (Water(p) && (zone == 0 || ZoneAt(p) == zone)) return p;
            }
            return ZoneTarget[Mathf.Clamp(zone - 1, 0, 2)];
        }

        Vector2 TipLocal()
        {
            if (sc.fisher && sc.fisher.asset && sc.fisher.TryGetBoneWorld("dau_can", out var w, out _))
                return sc.world.InverseTransformPoint(w);
            return PlateToLocal(new Vector2(680, 900));
        }

        // ---------- trên, dưới ----------

        void Render()
        {
            var s = S;
            var d = D;
            double now = Now;
            int free = Fishing.FreeLeft(s, d, now);
            baitText.text = Loc.F("Mồi: {0} miễn phí · {1} mua", free, Casino.Of(s).bait);
            int v = Fishing.CreelValue(s, d);
            sellBtn.SetText(v > 0 ? Loc.F("Bán cá · {0} bi", NumFmt.Short(v)) : Loc.T("Bán cá"));
            sellBtn.Locked = v <= 0;
            baitBtn.SetText(Loc.F("Mua {0} mồi · {1} bi", C.baitPack, Fishing.BaitCost(s, d)));
            dexBtn.SetText(Loc.F("Sổ Cá {0}/{1}", Casino.Of(s).dex.Count(kv => kv.Value.n > 0 && C.fish.Any(f => f.id == kv.Key)), C.fish.Count));
        }

        void Sell()
        {
            int v = Fishing.SellCreel(S, D);
            if (v <= 0) return;
            App.Save.Save();
            App.Audio.Play("coin");
            App.Toasts.Show(Loc.F("Bán cá được {0} bi", v), Icon("ball"));
            Render();
            onRefresh?.Invoke();
        }

        void BuyBait()
        {
            if (!Fishing.BuyBait(S, D))
            {
                App.Toasts.Show(Loc.T("Không đủ bi"), Icon("ball"));
                return;
            }
            App.Save.Save();
            Render();
            if (st == St.Idle) ToIdle();
        }

        string ZoneName(int zone) => zone >= 1 && zone <= C.spots.Count ? C.spots[zone - 1].Name : "";

        void SetAct()
        {
            switch (st)
            {
                case St.Idle:
                    actBtn.SetRole(BtnColor.Green);
                    actBtn.SetText(Loc.T("Câu"));
                    break;
                case St.Bite:
                    actBtn.SetRole(BtnColor.Purple);
                    actBtn.SetText(Loc.T("Cá cắn!"));
                    break;
                case St.Reel:
                    actBtn.SetRole(BtnColor.Purple);
                    actBtn.SetText(Loc.T("Kéo!"));
                    break;
                case St.Result:
                    actBtn.SetRole(BtnColor.Paper);
                    actBtn.SetText(Loc.T("Câu"));
                    break;
                default:
                    actBtn.SetRole(BtnColor.Paper);
                    actBtn.SetText(Loc.T("Chờ cá..."));
                    break;
            }
        }

        void Clip(string name, bool loop, string then = null)
        {
            if (!sc.fisher || !sc.fisher.asset) return;
            sc.fisher.CrossFade(name, 0.1f, loop);
            sc.fisher.ClearQueue();
            if (then != null) sc.fisher.Queue(then, true);
        }

        // ---------- nhập: chạm, kéo, nhả trên mặt hồ; nút to ----------

        void OnDown(PointerEventData e)
        {
            if (st == St.Idle || st == St.Reel) Act();
        }

        void Act()
        {
            float now = Time.unscaledTime;
            if (now - lastTap < 0.08f) return;
            lastTap = now;
            switch (st)
            {
                case St.Idle: Cast(); break;
                case St.Reel: TryHit(); break;
            }
        }

        // ---------- quăng ----------

        // chỗ phao rơi: ngẫu nhiên trên hồ, trong phần nhìn thấy (màn dài hơn 2:3 thì hai bên nền bị cắt), ngoài chỗ người che;
        // zone > 0 thì chỉ trong vùng đó (lượt câu đầu đời: Gần bờ cho chắc trúng)
        Vector2 CastPoint(int zone)
        {
            float vis = sc.world && sc.world.parent is RectTransform hold ? Mathf.Min(1f, hold.rect.width / WorldSize.x) : 1f;
            float x0 = PW * (0.5f - vis / 2) + 90, x1 = PW * (0.5f + vis / 2) - 90;
            for (int i = 0; i < 120; i++)
            {
                var c = new Vector2(UnityEngine.Random.Range(x0, x1), UnityEngine.Random.Range(420f, 1150f));
                int z = ZoneAt(c);
                if (z > 0 && (zone == 0 || z == zone)) return c;
            }
            return ZoneTarget[Mathf.Clamp(zone - 1, 0, 2)];
        }

        void Cast()
        {
            var s = S;
            var d = D;
            double now = Now;
            bool firstEver = Casino.Of(s).dex.Count == 0;
            target = CastPoint(firstEver ? 1 : 0);
            spot = Mathf.Clamp(ZoneAt(target) - 1, 0, C.spots.Count - 1);
            string why = null;
            bite = firstEver ? Fishing.FirstCast(s, d, now, rng) : Fishing.Cast(s, d, spot, 1, now, rng, out why);
            if (bite == null)
            {
                App.Toasts.Show(why, Icon("lock"));
                return;
            }
            // mọi con đều qua thanh chạy: cá nhỏ (0 nhịp ở lõi) cần trúng 1 nhịp
            ticks = Mathf.Max(1, Fishing.Ticks(bite));
            lastTarget = target;
            App.Save.Save();
            Render();
            st = St.Fly;
            released = false;
            castFallback = 0.3f;   // rig cũ thiếu sự kiện "tha" thì vẫn thả sau 0,3 giây
            Clip("quang", false, "cho");
            sc.hint.text = "";
            SetAct();
        }

        void OnRigEvent(string name, string s)
        {
            if (name == "tha" && st == St.Fly && !released) Release();
            else if (name == "ca_len" && st == St.Pull && leapT < 0) StartLeap();
        }

        void Release()
        {
            released = true;
            App.Audio.Play("whoosh");
            flyFrom = TipLocal();
            flyTo = PlateToLocal(target);
            bobLocal = flyFrom;
            t = 0;
            sc.bobber.gameObject.SetActive(true);
            sc.line.gameObject.SetActive(true);
        }

        void Land()
        {
            bob = target;
            st = St.Wait;
            t = 0;
            nibbleT = UnityEngine.Random.Range(0.6f, 1.2f);
            Ripple(bob, 1.2f);
            Splash(bob, 8, 1f);
            bobY = 0;
            bobV = -260f;      // phao cắm xuống rồi nảy lên
            bobRest = 0;
            App.Audio.Play("splash");
            sc.hint.text = Loc.T("Chờ cá cắn câu...");
            // cá cắn câu bơi lại từ một phía
            ref var f = ref fishes[0];
            f.on = true;
            f.len = bite.king ? 190f : ticks == 0 ? 68f : Mathf.Lerp(92f, 150f, ticks / (float)Fishing.MaxTicks);
            float a = UnityEngine.Random.Range(0, Mathf.PI * 2);
            var from = bob + new Vector2(Mathf.Cos(a), Mathf.Sin(a) * 0.6f) * 300f;
            f.pos = Water(from) ? from : RandomWater(spot + 1);
            f.to = bob;
            f.alpha = 0;
            f.phase = UnityEngine.Random.value * 6f;
            SetAct();
        }

        // ---------- cá cắn, kéo ----------

        void ToIdle()
        {
            st = St.Idle;
            bite = null;
            assist = null;
            ticks = hits = 0;
            leapT = -1;
            bobRest = 0;
            wakeK = 0;
            sc.bobber.gameObject.SetActive(false);
            sc.bang.gameObject.SetActive(false);
            sc.line.Clear();
            reel.panel.gameObject.SetActive(false);
            if (sc.leapFish) sc.leapFish.gameObject.SetActive(false);
            sc.hint.text = Fishing.BaitLeft(S, D, Now) > 0 ? Loc.T("Chạm CÂU để thả câu")
                : Loc.T("Hết mồi: mua mồi hoặc làm nhiệm vụ quán trọ");
            if (sc.fisher && sc.fisher.asset && sc.fisher.CurrentClip != "hut") Clip("idle", true);
            SetAct();
        }

        void Hook()
        {
            sc.bang.gameObject.SetActive(false);
            Haptics.Play(Haptic.UiTap);
            App.Audio.Play("whoosh");
            Ripple(bob, 0.9f);
            Splash(bob, 4, 0.7f);
            if (bite.king)
            {
                assist = D.Heroes.Where(h => !h.minion && S.Hero(h.id)?.owned == true && Elements.Beats(h.elem) == bite.fish.elem)
                    .OrderByDescending(h => S.Hero(h.id).star).Select(h => h.id).FirstOrDefault();
                App.Toasts.Show(assist != null ? Loc.F("Cá Vua! {0} phụ kéo", D.Hero(assist).name) : Loc.T("Cá Vua! Không có tướng khắc hệ để phụ kéo"), Icon("star"));
            }
            Clip("giat", false, "keo");
            bobV = 160f;   // giật: phao bật lên
            st = St.Reel;
            zoneW = Mathf.Clamp((float)Fishing.Zone(S, D, bite, assist) * ZoneScale, 0.08f, 0.6f);
            needleP = 0;
            needleDir = 1;
            needleSpeed = 0.6f + 0.2f * (float)bite.pull;
            hits = 0;
            timeLeft = (float)Fishing.ReelTime;
            shake = flash = penaltyT = 0;
            PlaceZone();
            reel.panel.gameObject.SetActive(true);
            for (int i = 0; i < reel.pips.Length; i++)
            {
                reel.pips[i].gameObject.SetActive(i < ticks);
                reel.pips[i].color = new Color(1, 1, 1, 0.35f);
            }
            reel.hint.text = Loc.T("Chạm khi kim vào vùng vàng");
            reel.penalty.alpha = 0;
            sc.hint.text = bite.king ? Loc.T("Cá Vua!") : Loc.T("Cá lớn!");
            StepReelUi(0);
            SetAct();
        }

        void PlaceZone()
        {
            float half = zoneW / 2;
            float c = 0.5f;
            for (int i = 0; i < 10; i++)
            {
                c = UnityEngine.Random.Range(half + 0.02f, 1 - half - 0.02f);
                if (Mathf.Abs(c - needleP) >= 0.25f + half) break;
            }
            zoneC = c;
        }

        void TryHit()
        {
            if (Mathf.Abs(needleP - zoneC) <= zoneW / 2 + NeedleTol)
            {
                hits++;
                if (hits - 1 < reel.pips.Length) reel.pips[hits - 1].color = Theme.Yellow;
                flash = 1;
                Haptics.Play(Haptic.UiTap);
                App.Audio.Play("reel");
                Splash(bob, 5, 0.9f);
                Ripple(bob, 0.9f);
                bobV = 220f;   // giật một nhịp: phao bật lên
                if (hits >= ticks)
                {
                    reel.panel.gameObject.SetActive(false);
                    StartPull(false);
                    return;
                }
                Clip("nhip", false, "keo");
                PlaceZone();
                needleSpeed *= 1.04f;
            }
            else
            {
                timeLeft -= (float)Fishing.MissCost;
                shake = 1;
                penaltyT = 1;
                reel.penalty.text = Loc.F("-{0} giây", Fishing.MissCost);
                App.Audio.Play("error");
                if (timeLeft <= 0) ReelFail();
            }
        }

        void ReelFail()
        {
            reel.panel.gameObject.SetActive(false);
            Haptics.Play(Haptic.Lose);
            Escape(bite.king ? Loc.T("Cá Vua thoát rồi!") : Loc.T("Cá sổng mất"));
        }

        void Escape(string msg)
        {
            App.Toasts.Show(msg, Icon("fish"));
            ref var f = ref fishes[0];
            if (f.on)
            {
                var away = f.pos - Stand;
                f.to = f.pos + (away.sqrMagnitude > 1 ? away.normalized : Vector2.down) * 420f;
                f.speed = 520f;
            }
            Ripple(bob, 0.8f);
            Clip("hut", false, "idle");
            relaxT = 0.6f;   // dây chùng rồi mới thu phao
            st = St.Idle;
            bite = null;
            ticks = hits = 0;
            reel.panel.gameObject.SetActive(false);
            sc.bang.gameObject.SetActive(false);
            sc.hint.text = "";
            SetAct();
        }

        // afterHook: cá nhỏ vừa giật là lên (diễn giat rồi trung); không thì trung ngay sau nhịp cuối
        void StartPull(bool afterHook)
        {
            st = St.Pull;
            t = 0;
            leapT = -1;
            sc.hint.text = "";
            App.Audio.Play("whoosh");
            if (sc.fisher && sc.fisher.asset)
            {
                sc.fisher.CrossFade(afterHook ? "giat" : "trung", 0.1f, false);
                sc.fisher.ClearQueue();
                if (afterHook) sc.fisher.Queue("trung", false);
                sc.fisher.Queue("idle", true);
            }
            castFallback = afterHook ? 0.65f : 0.2f;   // rig thiếu sự kiện "ca_len" thì vẫn cho cá vọt lên
            SetAct();
        }

        void StartLeap()
        {
            leapT = 0;
            leapFrom = PlateToLocal(bob);
            Splash(bob, 8, 1.1f);
            Ripple(bob, 1.2f);
            App.Audio.Play("splash");
            fishes[0].on = false;
            sc.bobber.gameObject.SetActive(false);
            if (sc.leapFish)
            {
                sc.leapFish.gameObject.SetActive(true);
                var spr = FishArt(bite.fish.id);
                if (spr)
                {
                    Theme.SetSprite(sc.leapFish, spr);
                    sc.leapFish.color = Color.white;
                    sc.leapFish.preserveAspect = true;
                    sc.leapFish.rectTransform.sizeDelta = new Vector2(150, 150 * spr.rect.height / Mathf.Max(1, spr.rect.width));
                }
                else sc.leapFish.color = Color.Lerp(Theme.Of(bite.fish.elem), Color.white, 0.25f);
                float s = Mathf.Lerp(0.8f, 1.5f, Mathf.Clamp01(fishes[0].len / 190f)) * LocalPerPlate;
                sc.leapFish.rectTransform.localScale = new Vector3(s, s, 1);
            }
        }

        void LandFish()
        {
            var s = S;
            var d = D;
            var c = Fishing.Land(s, d, bite, Now, rng);
            App.Save.Save();
            App.Audio.Play(bite.fish.rar >= Rarity.Epic || bite.king ? "win" : "coin");
            Haptics.Play(bite.fish.rar >= Rarity.Rare ? Haptic.Win : Haptic.UiTap);
            st = St.Result;
            reel.panel.gameObject.SetActive(false);
            sc.bobber.gameObject.SetActive(false);
            sc.line.Clear();
            if (sc.leapFish) sc.leapFish.gameObject.SetActive(false);
            sc.hint.text = "";
            SetAct();
            res.root.SetActive(true);
            resT = 0;
            resClass = Fishing.SizeClass(c.fish, c.size);
            ShowFish(res.dot, c.fish, true);
            res.ring.color = Theme.Of(c.fish.rar);
            res.medal.color = MedalColor(resClass, 0);
            res.name.text = c.fish.Name;
            res.info.text = string.Join(" · ", new List<string> { Elements.RarityName(c.fish.rar), Loc.F("{0} cm", c.size.ToString("0.#")), ClassName(resClass) });
            string banner = c.king ? Loc.T("Cá Vua!") : c.first ? Loc.T("Loài mới!") : c.record ? Loc.T("Kỷ lục mới!") : null;
            res.banner.gameObject.SetActive(banner != null);
            if (banner != null) res.bannerText.text = banner.ToUpperInvariant();
            string rw = CasinoUi.Rewards(c.rewards);
            if (c.setDone is Elem e) rw = Loc.F("Đủ 6 loài hệ {0}!", Elements.Name(e)) + (rw.Length > 0 ? "\n" + rw : "");
            if (!c.king) rw = (rw.Length > 0 ? rw + "\n" : "") + Loc.F("Vào giỏ, bán ở đây được {0} bi", Fishing.Price(d, new CaughtFish { id = c.fish.id, size = c.size }));
            res.rewards.text = rw;
            StepResult(0);
            Render();
            onRefresh?.Invoke();
        }

        // ---------- mỗi khung ----------

        void Update()
        {
            if (!sc.world) return;
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            if (sc.fisher) sc.fisher.pixelScale = LocalPerPlate * RigK;
            float wig = Time.unscaledTime;
            if (castFallback > 0)
            {
                castFallback -= dt;
                if (castFallback <= 0)
                {
                    if (st == St.Fly && !released) Release();
                    else if (st == St.Pull && leapT < 0) StartLeap();
                }
            }
            switch (st)
            {
                case St.Fly:
                    if (!released) break;
                    t += dt / FlyTime;
                    {
                        float k = Mathf.Clamp01(t);
                        float h = Vector2.Distance(flyFrom, flyTo) * 0.28f + 40f;
                        bobLocal = Vector2.Lerp(flyFrom, flyTo, k) + Vector2.up * Mathf.Sin(k * Mathf.PI) * h;
                    }
                    if (t >= 1) Land();
                    break;
                case St.Wait: StepWait(dt); break;
                case St.Bite:
                    t += dt;
                    if (t >= 0.35f) Hook();
                    break;
                case St.Reel: StepReel(dt); break;
                case St.Pull:
                    t += dt;
                    if (leapT >= 0) StepLeap(dt);
                    break;
                case St.Result: StepResult(dt); break;
            }
            if (relaxT > 0)
            {
                relaxT -= dt;
                if (relaxT <= 0 && st == St.Idle) ToIdle();
            }
            StepFish(dt);
            StepDrops(dt);
            DrawBobberAndLine(wig);
            PushShader();
        }

        void StepWait(float dt)
        {
            t += dt;
            ref var f = ref fishes[0];
            f.alpha = Mathf.MoveTowards(f.alpha, 1, dt * 2);
            f.to = bob + new Vector2(-f.len * 0.35f, f.len * 0.12f);
            f.speed = Mathf.Max(40f, Vector2.Distance(f.pos, f.to) / Mathf.Max(0.3f, (float)bite.wait - t));
            // rỉa mồi: phao nhấp, gợn nhỏ
            nibbleT -= dt;
            if (nibbleT <= 0 && t < bite.wait - 0.3f && Vector2.Distance(f.pos, f.to) < 60f)
            {
                nibbleT = UnityEngine.Random.Range(0.5f, 1.1f);
                Ripple(bob, 0.45f);
                bobV = -130f;   // rỉa: phao nhấp
                App.Audio.Play("plop");
            }
            if (t >= bite.wait)
            {
                st = St.Bite;
                t = 0;
                sc.bang.gameObject.SetActive(true);
                Haptics.Play(Haptic.UiTap);
                App.Audio.Play("bloop");
                Ripple(bob, 1.2f);
                Splash(bob, 5, 0.8f);
                bobV = -320f;
                bobRest = -24f;   // cắn: phao chìm hẳn, hiện "!" rồi tự vào thanh chạy
                sc.hint.text = Loc.T("Cá cắn câu!");
                SetAct();
            }
        }


        void StepReel(float dt)
        {
            timeLeft -= dt;
            needleP += needleDir * needleSpeed * dt;
            if (needleP > 1) { needleP = 2 - needleP; needleDir = -1; }
            if (needleP < 0) { needleP = -needleP; needleDir = 1; }
            StepReelUi(dt);
            // phao bị kéo dần về bến theo số nhịp, cá giãy
            float prog = hits / (float)Mathf.Max(1, ticks);
            var shore = new Vector2(lastTarget.x >= Body.center.x ? Body.xMax + 50 : Body.xMin - 50, 1060);
            var dest = Vector2.Lerp(lastTarget, shore, 0.6f * prog);
            if (!Castable(dest)) dest = bob;
            bob = Vector2.MoveTowards(bob, dest, 120f * dt);
            ref var f = ref fishes[0];
            float w = Time.unscaledTime;
            f.to = bob + new Vector2(Mathf.Sin(w * 3.1f) * f.len * 0.4f, Mathf.Cos(w * 2.3f) * f.len * 0.2f);
            f.speed = 260f;
            if (UnityEngine.Random.value < dt * 1.5f) Ripple(bob, 0.45f);
            if (timeLeft <= 0) ReelFail();
        }

        void StepReelUi(float dt)
        {
            float w = reel.bar.rect.width;
            reel.needle.anchoredPosition = new Vector2(needleP * w, reel.needle.anchoredPosition.y);
            reel.zone.anchoredPosition = new Vector2(zoneC * w, reel.zone.anchoredPosition.y);
            reel.zone.sizeDelta = new Vector2(zoneW * w, reel.zone.sizeDelta.y);
            float left = Mathf.Max(0, timeLeft);
            reel.timer.text = Mathf.CeilToInt(left).ToString();
            reel.timerRing.fillAmount = left / (float)Fishing.ReelTime;
            reel.timerRing.color = left <= 8 ? Theme.Red : Theme.Yellow;
            flash = Mathf.Max(0, flash - dt * 4);
            reel.zoneImg.color = Color.Lerp(Theme.Yellow, Color.white, flash);
            shake = Mathf.Max(0, shake - dt * 3);
            reel.bar.anchoredPosition = barBase + new Vector2(Mathf.Sin(Time.unscaledTime * 60) * 16 * shake, 0);
            penaltyT = Mathf.Max(0, penaltyT - dt * 1.2f);
            reel.penalty.alpha = Mathf.Clamp01(penaltyT * 1.6f);
            reel.penalty.rectTransform.anchoredPosition = new Vector2(reel.penalty.rectTransform.anchoredPosition.x, 70 + (1 - penaltyT) * 50);
        }

        void StepLeap(float dt)
        {
            leapT += dt / PullTime;
            float k = Mathf.Clamp01(leapT);
            var tip = TipLocal();
            float h = Vector2.Distance(leapFrom, tip) * 0.35f + 80f;
            var p = Vector2.Lerp(leapFrom, tip, Mathf.SmoothStep(0, 1, k)) + Vector2.up * Mathf.Sin(k * Mathf.PI) * h;
            if (sc.leapFish)
            {
                sc.leapFish.rectTransform.anchoredPosition = p;
                sc.leapFish.rectTransform.localEulerAngles = new Vector3(0, 0, Mathf.Lerp(40, -30, k) + Mathf.Sin(k * 30) * 12);
            }
            bobLocal = p;
            if (leapT >= 1.25f) LandFish();
        }

        void StepResult(float dt)
        {
            resT += dt;
            float k = Mathf.Clamp01(resT / 0.3f);
            float pop = 1 + Mathf.Sin(k * Mathf.PI) * 0.08f;
            res.card.localScale = Vector3.one * Mathf.Lerp(0.7f, 1, Mathf.SmoothStep(0, 1, k)) * pop;
            float kb = Mathf.Clamp01((resT - 0.2f) / 0.35f);
            res.banner.localScale = Vector3.one * (kb <= 0 ? 0 : Mathf.Lerp(0.3f, 1, Mathf.SmoothStep(0, 1, kb)) * (1 + Mathf.Sin(kb * Mathf.PI) * 0.15f));
            res.medal.color = MedalColor(resClass, resT);
        }

        // ---------- bóng cá, giọt nước, gợn ----------

        void SpawnAmbient(int i, bool anywhere)
        {
            ref var f = ref fishes[i];
            f.on = true;
            f.pos = RandomWater();
            f.to = RandomWater();
            f.len = UnityEngine.Random.Range(55f, 95f);
            f.speed = UnityEngine.Random.Range(28f, 60f);
            f.alpha = anywhere ? 1 : 0;
            f.phase = UnityEngine.Random.value * 6f;
        }

        void StepFish(float dt)
        {
            for (int i = 0; i < fishes.Length; i++)
            {
                ref var f = ref fishes[i];
                if (!f.on)
                {
                    fishB[i] = Vector4.zero;
                    continue;
                }
                var d = f.to - f.pos;
                if (i > 0 && d.magnitude < 20f)
                {
                    f.to = RandomWater();
                    f.speed = UnityEngine.Random.Range(28f, 60f);
                }
                var step = Vector2.ClampMagnitude(d, f.speed * dt);
                var next = f.pos + step;
                if (i == 0 || Water(next)) f.pos = next;
                else f.to = RandomWater();
                if (step.sqrMagnitude > 0.0001f) f.vel = Vector2.Lerp(f.vel, step / Mathf.Max(dt, 1e-4f), 0.15f);
                if (i > 0) f.alpha = Mathf.MoveTowards(f.alpha, 1, dt);
                else if (st != St.Wait && st != St.Bite && st != St.Reel && st != St.Pull) // sổng: lao đi rồi tắt
                {
                    f.alpha = Mathf.MoveTowards(f.alpha, 0, dt * 1.6f);
                    if (f.alpha <= 0) f.on = false;
                }
                var ps = Sh(f.pos);
                var vs = new Vector2(f.vel.x, -f.vel.y);
                float ang = vs.sqrMagnitude > 1 ? -Mathf.Atan2(vs.y, vs.x) : 0;
                fishA[i] = new Vector4(ps.x, ps.y, ang, f.len);
                fishB[i] = new Vector4(f.alpha * (i == 0 ? 1f : 0.75f), f.phase, 0, 0);
            }
        }

        void Ripple(Vector2 pp, float strength)
        {
            var s = Sh(pp);
            rip[ripNext] = new Vector4(s.x, s.y, Time.time, strength);
            ripNext = (ripNext + 1) % rip.Length;
        }

        void Splash(Vector2 pp, int n, float power)
        {
            var at = PlateToLocal(pp);
            int made = 0;
            for (int i = 0; i < sc.drops.Length && made < n; i++)
            {
                if (dropLife[i] > 0) continue;
                made++;
                dropLife[i] = 1;
                var d = sc.drops[i];
                d.gameObject.SetActive(true);
                d.anchoredPosition = at;
                float a = UnityEngine.Random.Range(-1.1f, 1.1f);
                dropVel[i] = new Vector2(Mathf.Sin(a), Mathf.Cos(a) * 1.4f) * UnityEngine.Random.Range(160f, 300f) * power * LocalPerPlate;
                float s = UnityEngine.Random.Range(0.7f, 1.2f) * LocalPerPlate * 1.3f;
                d.localScale = new Vector3(s, s, 1);
            }
        }

        void StepDrops(float dt)
        {
            for (int i = 0; i < sc.drops.Length; i++)
            {
                if (dropLife[i] <= 0) continue;
                dropLife[i] -= dt / 0.55f;
                dropVel[i] += Vector2.down * 900f * LocalPerPlate * dt;
                var d = sc.drops[i];
                d.anchoredPosition += dropVel[i] * dt;
                d.localEulerAngles = new Vector3(0, 0, Mathf.Atan2(dropVel[i].y, dropVel[i].x) * Mathf.Rad2Deg - 90);
                if (dropLife[i] <= 0) d.gameObject.SetActive(false);
            }
        }

        // phao: lò xo dọc (cm ảnh nền), nghiêng theo vận tốc và dây; hai bản hình cắt theo mặt nước
        void DrawBobberAndLine(float wig)
        {
            float dt = Mathf.Min(Time.unscaledDeltaTime, 0.05f);
            var tip = TipLocal();
            bool showBob = st == St.Fly && released || st == St.Wait || st == St.Bite || st == St.Reel || st == St.Pull && leapT < 0
                           || st == St.Idle && relaxT > 0;
            float s = LocalPerPlate;
            if (st == St.Reel) bobRest = -9f + Mathf.Sin(wig * 9f) * 3f;
            else if (st != St.Bite) bobRest = 0;
            // lò xo: k = 70, cản 7; thêm sóng nhẹ khi nổi yên
            float acc = (bobRest - bobY) * 70f - bobV * 7f;
            bobV += acc * dt;
            bobY += bobV * dt;
            float idleBob = st == St.Wait || st == St.Idle ? Mathf.Sin(wig * 2.6f) * 2.2f + Mathf.Sin(wig * 4.1f + 1.3f) * 1.1f : 0f;
            float y = bobY + idleBob;
            if (showBob)
            {
                Vector2 water;   // điểm phao chạm mặt nước (cục bộ)
                if (st == St.Fly)
                {
                    water = bobLocal;
                    y = 0;
                }
                else water = PlateToLocal(bob);
                // nghiêng: lắc theo sóng + theo vận tốc nhún + theo dây khi căng
                var toTip = tip - water;
                float pull = st == St.Reel || st == St.Bite ? Mathf.Clamp(Mathf.Atan2(toTip.x, toTip.y) * Mathf.Rad2Deg * 0.35f, -25f, 25f) : 0f;
                float targetTilt = (st == St.Fly ? Mathf.Sin(wig * 12f) * 25f : Mathf.Sin(wig * 1.7f) * 6f) - bobV * 0.02f - pull;
                tilt = Mathf.Lerp(tilt, targetTilt, 1 - Mathf.Exp(-dt * 10f));
                sc.bobber.gameObject.SetActive(true);
                sc.bobber.anchoredPosition = water;
                sc.bobber.localScale = Vector3.one;
                bool under = st != St.Fly;
                var offs = new Vector3(0, y * s * 1.15f, 0);
                var rot = Quaternion.Euler(0, 0, tilt);
                foreach (var b in new[] { sc.bobTop, sc.bobUnder })
                {
                    if (!b) continue;
                    b.localPosition = offs;
                    b.localRotation = rot;
                    b.localScale = new Vector3(s * 1.15f, s * 1.15f, 1);
                }
                // bay: không cắt theo mặt nước (mask phần trên mở rộng xuống), cả hình hiện
                if (sc.bobTop && sc.bobTop.parent && sc.bobTop.parent.GetComponent<RectMask2D>() is RectMask2D rm) rm.enabled = under;
                if (sc.bobUnder) sc.bobUnder.gameObject.SetActive(under);
                sc.bang.anchoredPosition = water + new Vector2(0, 86 * s);
                // dây buộc vào đầu que phao (đỉnh hình, xoay theo phao)
                var stick = water + (Vector2)(rot * new Vector3(0, (44f + y * 1.15f) * s, 0));
                if (st != St.Fly) stick.y = water.y + (44f * Mathf.Cos(tilt * Mathf.Deg2Rad) + y * 1.15f) * s;
                float len = Vector2.Distance(tip, stick);
                float sag = st == St.Reel || st == St.Bite ? len * 0.015f
                    : st == St.Fly ? len * 0.06f
                    : st == St.Idle ? len * 0.22f : len * 0.1f;
                float side = st == St.Reel ? Mathf.Sin(wig * 13) * 4f * s : 0f;
                sc.line.gameObject.SetActive(true);
                sc.line.SetCurve(tip, stick, sag, side);
                // vệt rẽ nước khi phao bị kéo đi
                if (st != St.Fly)
                {
                    float sp = (bob - bobPrev).magnitude / Mathf.Max(dt, 1e-4f);
                    wakeK = Mathf.Lerp(wakeK, Mathf.Clamp01(sp / 60f), 1 - Mathf.Exp(-dt * 4f));
                }
                bobPrev = bob;
            }
            else if (st == St.Pull && leapT >= 0 && sc.leapFish)
            {
                sc.line.SetCurve(tip, sc.leapFish.rectTransform.anchoredPosition, 0f);
                wakeK = 0;
            }
            else
            {
                sc.bobber.gameObject.SetActive(false);
                if (st != St.Pull) sc.line.Clear();
                wakeK = 0;
            }
        }

        void PushShader()
        {
            if (!mat) return;
            Push(mat);
            // material đang vẽ có thể là bản sao (bộ sửa material của uGUI): ghi cả vào đó
            var rm = sc.plate ? sc.plate.materialForRendering : null;
            if (rm && rm != mat) Push(rm);
        }

        void Push(Material mat)
        {
            mat.SetFloat("_Now", Time.time);
            mat.SetVectorArray("_Rip", rip);
            mat.SetVectorArray("_Fish", fishA);
            mat.SetVectorArray("_FishB", fishB);
            bool floating = sc.bobber && sc.bobber.gameObject.activeSelf && st != St.Fly;
            var b = Sh(bob);
            float sink = Mathf.Clamp01(-bobY / 24f);
            mat.SetVector("_Bob", floating ? new Vector4(b.x, b.y, sink, 1) : Vector4.zero);
            // vệt rẽ nước: hướng phao đang chạy (lúc kéo: về phía bến); cá cắn câu giãy cũng tạo vệt
            var dir = st == St.Reel ? (Vector2)(new Vector2(Body.center.x, 1060) - bob) : fishes[0].vel;
            var ds = new Vector2(dir.x, -dir.y);
            float ang = ds.sqrMagnitude > 0.01f ? Mathf.Atan2(ds.y, ds.x) : 0f;
            float wk = floating ? Mathf.Max(wakeK, st == St.Reel ? 0.55f : 0f) : 0f;
            mat.SetVector("_Wake", new Vector4(b.x, b.y, ang, wk));
        }

        static Color MedalColor(int k, float time)
        {
            switch (k)
            {
                case 0: return Theme.Hex("#c98a4b");
                case 1: return Theme.Hex("#b9c6cf");
                case 2: return Theme.Yellow;
                default: return Color.HSVToRGB(Mathf.Repeat(time * 0.35f, 1), 0.55f, 1);
            }
        }

        static string ClassName(int k)
        {
            switch (k)
            {
                case 0: return Loc.T("Hạng Đồng");
                case 1: return Loc.T("Hạng Bạc");
                case 2: return Loc.T("Hạng Vàng");
                default: return Loc.T("Hạng Cầu vồng");
            }
        }

        // ---------- Sổ Cá ----------

        void ShowDex()
        {
            var s = S;
            var st2 = Casino.Of(s);
            var fish = C.fish;
            for (int i = 0; i < dexCells.Length; i++)
            {
                var cell = dexCells[i];
                bool has = i < fish.Count;
                cell.dot.transform.parent.gameObject.SetActive(has);
                if (!has) continue;
                var f = fish[i];
                bool caught = st2.dex.TryGetValue(f.id, out var rec) && rec.n > 0;
                ShowFish(cell.dot, f, caught);
                cell.ring.color = caught ? Theme.Of(f.rar) : new Color(0.7f, 0.66f, 0.6f);
                cell.name.text = caught ? f.Name : "???";
                cell.info.text = caught ? Loc.F("×{0} · {1} cm", rec.n, rec.best.ToString("0.#")) : (f.night ? Loc.T("cắn ban đêm") : Elements.RarityName(f.rar));
            }
            var king = Fishing.KingOf(D, Now);
            dexHead.text = Loc.F("Đã bắt {0}/{1} loài · đủ bộ hệ: {2}", st2.dex.Count(kv => kv.Value.n > 0 && fish.Any(f => f.id == kv.Key)), fish.Count,
                               st2.sets.Count == 0 ? "—" : string.Join(", ", st2.sets.Select(k => Elements.Name(Keys.ToElem(k))))) +
                           (king != null ? "\n" + Loc.F("Cá Vua tuần này: {0} ({1}) ở {2}", king.Name, Elements.Name(king.elem),
                               C.spots[C.spots.Count - 1].Name) : "");
            dex.SetActive(true);
        }

        public void ShowDexForTest() => ShowDex();

        // cho lượt chụp thử: ngắm vùng zone (1..3), thả, giật, tự chạm khi kim trong vùng vàng (cố trượt một lần) tới khi xong
        public System.Collections.IEnumerator AutoCast(int zone, Action<string> shot)
        {
            if (st != St.Idle) yield break;
            yield return new WaitForSecondsRealtime(0.3f);
            lastTap = -1;
            Act();
            if (st != St.Fly) yield break;
            yield return new WaitForSecondsRealtime(0.5f);
            shot?.Invoke("bay");
            while (st == St.Fly) yield return null;
            yield return new WaitForSecondsRealtime(0.15f);
            shot?.Invoke("roi");
            yield return new WaitForSecondsRealtime(0.9f);
            shot?.Invoke("noi");
            while (st == St.Wait) yield return null;
            yield return null;
            shot?.Invoke("can_cau");
            while (st == St.Bite) yield return null;
            float t0 = Time.realtimeSinceStartup;
            bool missed = false, shotReel = false;
            while (st == St.Reel && Time.realtimeSinceStartup - t0 < 40)
            {
                float gap = Mathf.Abs(needleP - zoneC);
                if (!missed && hits >= 1 && gap > zoneW / 2 + 0.2f)
                {
                    lastTap = -1;
                    Act();
                    missed = true;
                    yield return null;
                    shot?.Invoke("truot");
                }
                else if (gap <= zoneW / 2 - 0.01f)
                {
                    lastTap = -1;
                    Act();
                }
                if (!shotReel && st == St.Reel && Time.realtimeSinceStartup - t0 > 0.9f)
                {
                    shotReel = true;
                    shot?.Invoke("keo");
                }
                yield return null;
            }
            float tl = Time.realtimeSinceStartup;
            bool shotLeap = false;
            while (st == St.Pull && Time.realtimeSinceStartup - tl < 4)
            {
                if (!shotLeap && leapT > 0.45f)
                {
                    shotLeap = true;
                    shot?.Invoke("ca_vot");
                }
                yield return null;
            }
            yield return new WaitForSecondsRealtime(0.6f);
            shot?.Invoke("ket_qua");
        }
    }

    // chữ thưởng của đảo (ô thưởng đẹp dùng chung để C8)
    public static class CasinoUi
    {
        public static string Rewards(List<Reward> rs)
        {
            if (rs == null || rs.Count == 0) return "";
            var d = App.Data;
            var parts = new List<string>();
            foreach (var r in rs)
                switch (r.k)
                {
                    case RewardKind.Balls: parts.Add(Loc.F("+{0} bi", r.n)); break;
                    case RewardKind.Bait: parts.Add(Loc.F("+{0} mồi", r.n)); break;
                    case RewardKind.Deco: parts.Add(Loc.F("+{0} {1} (vào túi Nhà)", r.n, d.Cfg.home.Def(r.id)?.Name ?? r.id)); break;
                    case RewardKind.Shards:
                        string h = r.res?.hero ?? r.hero;
                        parts.Add(Loc.F("+{0} mảnh {1}", r.res?.n ?? r.n, h != null ? d.Hero(h)?.name : "")); break;
                    case RewardKind.EvoStones: parts.Add(Loc.F("+{0} đá tiến hóa", r.n)); break;
                    case RewardKind.Stones: parts.Add(Loc.F("+{0} đá tiềm năng", r.n)); break;
                    case RewardKind.Crystal: parts.Add(Loc.F("+{0} đá tinh", r.n)); break;
                    case RewardKind.Card: parts.Add(Loc.T("+1 bản sao thẻ")); break;
                    case RewardKind.Egg: parts.Add(Loc.F("+{0} trứng", r.n)); break;
                    case RewardKind.Exp: parts.Add(Loc.F("+{0} EXP", r.n)); break;
                    default: parts.Add("+" + r.n); break;
                }
            return string.Join(" · ", parts);
        }

        // chữ món thưởng của đảo trước khi nhận (bi nhân bậc cấp như Casino.Grant)
        public static string Items(IEnumerable<CasinoItem> items)
        {
            var s = App.Save.Data;
            var d = App.Data;
            var parts = new List<string>();
            foreach (var it in items)
            {
                if (it == null) continue;
                switch (it.k)
                {
                    case "balls": parts.Add(Loc.F("+{0} bi", Shop.RoundBalls(it.n * Casino.Band(s, d)))); break;
                    case Casino.Bait: parts.Add(Loc.F("+{0} mồi", it.n)); break;
                    case "stones": parts.Add(Loc.F("+{0} đá tiềm năng", it.n)); break;
                    case "evo": parts.Add(Loc.F("+{0} đá tiến hóa", it.n)); break;
                    case "crystal": parts.Add(Loc.F("+{0} đá tinh", it.n)); break;
                    case "shards": parts.Add(Loc.F("+{0} mảnh tướng", it.n)); break;
                    case "copies": parts.Add(Loc.F("+{0} bản sao thẻ", it.n)); break;
                    default: parts.Add("+" + it.n + " " + it.k); break;
                }
            }
            return string.Join(" · ", parts);
        }
    }
}
