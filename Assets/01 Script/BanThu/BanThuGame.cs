// Bản thử 1 đấu 1, màn dọc (GD_Claude/10_BanThu_1v1.md). Tự dựng mọi thứ lúc chạy: camera, sân, bàn, nút.
// Bàn A (xếp khối), A có sập, hoặc C (xếp ngọc) dùng chung trận đánh, để chơi so. Mỗi trận ghi một dòng vào PokiWar/BanThu/tran.csv.
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.InputSystem;

namespace PokiWar.BanThu
{
    public sealed class BanThuGame : MonoBehaviour
    {
        [Tooltip("Thư mục reskin của dự án aola. Hình tướng chỉ dùng trong bản thử.")]
        public string aolaReskin = "E:/ProjectAtomik/aola/reskin";
        [Tooltip("Tự chụp màn hình vào PokiWar/BanThu/ ở menu, đầu trận và cuối trận. F9 chụp tay.")]
        public bool autoShots = true;
        [Tooltip("0 = ngẫu nhiên")]
        public int seed;

        enum Mode { A, ASap, C }
        enum Phase { Menu, Play, Busy, Over }

        // 0 Đỏ đánh, 1 Lam khiên, 2 Lục hồi, 3 Vàng nộ, 4 đá
        static readonly Color[] ActColors =
        {
            new(0.93f, 0.32f, 0.30f), new(0.27f, 0.56f, 0.96f), new(0.33f, 0.80f, 0.40f), new(1f, 0.80f, 0.22f), new(0.50f, 0.47f, 0.44f),
        };
        static readonly string[] ModeNames = { "A · Xếp khối", "A · Xếp khối có sập", "C · Xếp ngọc" };
        static readonly string[] ModeKeys = { "A", "A_sap", "C" };
        // goc_<id>: tướng giữ nguyên hình gốc (aola tools/export_original.py), xếp theo dòng tiến hóa
        static readonly string[] KnownHeroes =
        {
            "monk_2217", "monk_boxer", "monk_500", "monk_2010",
            "goc_1826", "goc_1837", "goc_1831", "goc_1832", "goc_2955", "goc_1319", "goc_1320",
        };
        static readonly Dictionary<string, string> HeroNames = new()
        {
            ["monk_boxer"] = "Võ sư", ["monk_2217"] = "Đại sư cà sa", ["monk_500"] = "Võ tăng Bồ Đề", ["monk_2010"] = "Thiền sư Pháp Luân",
            // 加比, 使者加比, 蓝钧, 万钧, 黑翼·万钧, 小伊, 伊泽 (âm Hán Việt: chữ Hán không có trong phông mặc định)
            ["goc_1826"] = "Gia Bỉ", ["goc_1837"] = "Sứ giả Gia Bỉ", ["goc_1831"] = "Lam Quân", ["goc_1832"] = "Vạn Quân",
            ["goc_2955"] = "Hắc Dực Vạn Quân", ["goc_1319"] = "Tiểu Y", ["goc_1320"] = "Y Trạch",
        };
        static readonly Color Dark = new(0.22f, 0.24f, 0.32f), Gold = new(1f, 0.78f, 0.25f), Grey = new(0.70f, 0.72f, 0.78f);
        const float ContentW = 9f; // bố cục tính trên bề ngang 9 đơn vị

        sealed class Btn
        {
            public Rect Rect;
            public SpriteRenderer Bg;
            public TextMesh Label;
            public Action Click;
            public Color Base;
            public void Select(bool on)
            {
                Bg.color = on ? Gold : Base;
                Label.color = on ? new Color(0.15f, 0.12f, 0.05f) : Color.white;
            }
        }

        sealed class Bar
        {
            public SpriteRenderer Fill;
            public float X0, W, Y, H;
            public void Set(float t)
            {
                t = Mathf.Clamp01(t);
                Fill.transform.position = new Vector3(X0 + W * t / 2, Y, 0);
                Fill.transform.localScale = new Vector3(W * t, H, 1);
            }
        }

        Camera cam;
        float viewH;
        Vector2Int screen;
        Font font;
        Sprite white, blockSprite, gemSprite, roundSprite;
        Transform root;
        string outDir;
        readonly List<Btn> buttons = new();
        Btn pressed;

        Phase phase;
        Mode mode;
        int heroIdx, shots, msgToken;
        readonly List<string> heroes = new();

        Battle battle;
        BlockBoard bb;
        GemBoard gb;
        AolaActor hero, enemy;
        string heroName, enemyName;
        Vector2 heroFeet, enemyFeet;
        float startTime;

        int n;
        float cell, trayCell;
        Vector2 boardTL;
        SpriteRenderer[,] cellR;
        Bar enemyBar, heroBar, rageBar;
        TextMesh enemyHpT, heroHpT, intentT, turnT, msgT;
        Btn skillBtn;
        readonly List<SpriteRenderer>[] trayR = { new(), new(), new() };
        readonly Vector2[] slotPos = new Vector2[3];
        int dragIdx = -1;
        readonly List<SpriteRenderer> dragR = new(), ghostR = new();
        Vector2Int dragTarget, gemDown = new(-1, -1);
        bool dragValid;
        Vector2 gemDownW;

        void Start()
        {
            Application.runInBackground = true; // để máy tự chơi chạy cả khi cửa sổ Unity không được chọn
            font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            white = MakeSprite(4, (x, y) => Color.white);
            blockSprite = MakeSprite(64, BlockPixel);
            gemSprite = MakeSprite(64, GemPixel);
            roundSprite = MakeSprite(64, (x, y) => new Color(1, 1, 1, RoundAlpha(x, y, 64, 20)), 20);
            outDir = Path.GetFullPath(Path.Combine(Application.dataPath, "..", "BanThu"));

            cam = Camera.main;
            if (!cam)
            {
                var go = new GameObject("Main Camera") { tag = "MainCamera" };
                cam = go.AddComponent<Camera>();
            }
            cam.orthographic = true;
            cam.transform.position = new Vector3(0, 0, -10);
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0.10f, 0.11f, 0.16f);

            FindHeroes();
            BuildMenu();
        }

        // ---------- bố cục ----------

        void Layout()
        {
            screen = new Vector2Int(Screen.width, Screen.height);
            float aspect = (float)Screen.width / Mathf.Max(1, Screen.height);
            viewH = Mathf.Max(16f, ContentW / aspect); // máy dài thì cao thêm; màn ngang thì hai bên để trống
            cam.orthographicSize = viewH / 2;
        }

        float Y(float fromTop) => viewH / 2 - fromTop * viewH;

        void Clear()
        {
            StopAllCoroutines();
            if (root) Destroy(root.gameObject);
            root = new GameObject("BanThu_View").transform;
            buttons.Clear();
            pressed = null;
            dragIdx = -1;
            dragR.Clear();
            ghostR.Clear();
            foreach (var t in trayR) t.Clear();
            gemDown = new Vector2Int(-1, -1);
            msgT = null;
        }

        void FindHeroes()
        {
            heroes.Clear();
            if (Directory.Exists(aolaReskin))
                foreach (var d in Directory.GetDirectories(aolaReskin))
                    if (File.Exists(Path.Combine(d, "export", "anim.json"))) heroes.Add(Path.GetFileName(d));
            heroes.Sort((a, b) => Rank(a).CompareTo(Rank(b)));
            if (heroes.Count == 0) heroes.Add("(hình tạm)");
            Debug.Log("[BanThu] Tướng: " + string.Join(", ", heroes));
        }

        static int Rank(string h)
        {
            int i = Array.IndexOf(KnownHeroes, h);
            return i < 0 ? 99 : i;
        }

        static string Name(string h) => HeroNames.TryGetValue(h, out var s) ? s : h;

        // ---------- menu ----------

        void BuildMenu()
        {
            Clear();
            Layout();
            phase = Phase.Menu;
            autoPlay = false;
            Time.timeScale = 1;
            Text("PokiWar", new Vector2(0, Y(.07f)), .9f, Gold);
            Text("Bản thử 1 đấu 1", new Vector2(0, Y(.115f)), .4f, Grey);

            Text("Chọn tướng", new Vector2(0, Y(.18f)), .38f, Color.white);
            // hai cột, để đủ chỗ cho cả các tướng hình gốc
            var heroBtns = new List<Btn>();
            int rows = (heroes.Count + 1) / 2;
            float rowH = Mathf.Min(.055f, .36f / Mathf.Max(1, rows));
            for (int i = 0; i < heroes.Count; i++)
            {
                int k = i;
                float x = heroes.Count == 1 ? 0 : (i % 2 == 0 ? -2.25f : 2.25f);
                heroBtns.Add(Button(Name(heroes[i]), new Vector2(x, Y(.225f + rowH * (i / 2))), new Vector2(4.3f, rowH * .82f * viewH), () =>
                {
                    heroIdx = k;
                    for (int j = 0; j < heroBtns.Count; j++) heroBtns[j].Select(j == k);
                }, Dark, .3f));
            }
            heroIdx = Mathf.Clamp(heroIdx, 0, heroes.Count - 1);
            heroBtns[heroIdx].Select(true);
            if (heroes[0] == "(hình tạm)")
                Text("Không thấy tướng ở " + aolaReskin, new Vector2(0, Y(.29f)), .26f, ActColors[0]);

            float y0 = .225f + rowH * rows + .03f;
            Text("Chọn bàn", new Vector2(0, Y(y0)), .38f, Color.white);
            var modeBtns = new List<Btn>();
            for (int i = 0; i < 3; i++)
            {
                int k = i;
                modeBtns.Add(Button(ModeNames[i], new Vector2(-3f + 3f * i, Y(y0 + .05f)), new Vector2(2.9f, .05f * viewH), () =>
                {
                    mode = (Mode)k;
                    for (int j = 0; j < modeBtns.Count; j++) modeBtns[j].Select(j == k);
                }, Dark, .24f));
            }
            modeBtns[(int)mode].Select(true);

            Text("Màu là hành động:\nĐỏ đánh · Lam khiên · Lục hồi máu · Vàng nộ\nĐủ nộ thì chạm nút CHIÊU", new Vector2(0, Y(.79f)), .28f, Grey);
            Button("BẮT ĐẦU", new Vector2(0, Y(.88f)), new Vector2(5f, .06f * viewH), StartGame, new Color(0.20f, 0.55f, 0.30f), .44f);
            Text("Hình tướng lấy từ dự án aola, chỉ dùng trong bản thử", new Vector2(0, Y(.955f)), .22f, Grey);
            if (autoShots) StartCoroutine(Shot("menu", .6f));
        }

        // ---------- trận ----------

        void StartGame()
        {
            int s = seed != 0 ? seed : Environment.TickCount;
            battle = new Battle();
            bb = mode == Mode.C ? null : new BlockBoard(s, mode == Mode.ASap);
            gb = mode == Mode.C ? new GemBoard(s) : null;
            heroName = heroes[heroIdx];
            enemyName = heroes.Count > 1 ? heroes[(heroIdx + 1) % heroes.Count] : heroName;
            startTime = Time.time;
            BuildPlay();
            if (autoShots) StartCoroutine(Shot("dau_tran_" + ModeKeys[(int)mode], 1.2f));
        }

        void BuildPlay()
        {
            Clear();
            Layout();
            phase = Phase.Play;

            // sân đấu
            Quad(white, new Vector2(0, Y(.21f)), new Vector2(40, .34f * viewH), new Color(0.15f, 0.20f, 0.22f), -500);
            Quad(white, new Vector2(0, Y(.33f)), new Vector2(40, .14f * viewH), new Color(0.20f, 0.27f, 0.23f), -499);
            enemyFeet = new Vector2(2.2f, Y(.27f));
            heroFeet = new Vector2(-2.1f, Y(.365f));
            enemy = MakeActor(enemyName, enemyFeet, .18f * viewH, true, 100, ActColors[0]);
            hero = MakeActor(heroName, heroFeet, .14f * viewH, false, 300, ActColors[1]);

            // thanh trên
            turnT = Text("", new Vector2(-4.3f, Y(.025f)), .3f, Color.white, TextAnchor.MiddleLeft);
            Text(ModeNames[(int)mode], new Vector2(0, Y(.025f)), .3f, Grey);
            Button("Menu", new Vector2(3.7f, Y(.025f)), new Vector2(1.4f, .034f * viewH), BuildMenu, Dark, .28f);

            // địch
            Text(Name(enemyName) + " (địch)", new Vector2(-4.3f, Y(.055f)), .3f, Color.white, TextAnchor.MiddleLeft);
            enemyBar = MakeBar(-4.3f, 4.6f, Y(.08f), .02f * viewH, ActColors[0]);
            enemyHpT = Text("", new Vector2(-2.0f, Y(.08f)), .26f, Color.white, TextAnchor.MiddleCenter, 1250);
            intentT = Text("", new Vector2(-4.3f, Y(.108f)), .28f, Gold, TextAnchor.MiddleLeft);

            // mình
            heroBar = MakeBar(-4.3f, 4.8f, Y(.4f), .02f * viewH, ActColors[2]);
            heroHpT = Text("", new Vector2(-1.9f, Y(.4f)), .26f, Color.white, TextAnchor.MiddleCenter, 1250);
            skillBtn = Button("", new Vector2(2.85f, Y(.4f)), new Vector2(2.9f, .036f * viewH), OnSkill, Dark, .3f, 1100);
            rageBar = MakeBar(1.4f, 2.9f, Y(.4f), .03f * viewH, new Color(1f, 0.8f, 0.22f, 0.45f), 1101);
            Text("Đỏ đánh · Lam khiên · Lục hồi · Vàng nộ", new Vector2(0, Y(.428f)), .25f, Grey);

            BuildBoard();
            msgT = Text("", new Vector2(0, Y(.64f)), .55f, Color.white, TextAnchor.MiddleCenter, 1400);
            RefreshHud();
        }

        AolaActor MakeActor(string name, Vector2 feet, float height, bool flip, int sorting, Color placeholder)
        {
            var go = new GameObject(name);
            go.transform.SetParent(root, false);
            go.transform.position = feet;
            var a = go.AddComponent<AolaActor>();
            if (!a.Load(Path.Combine(aolaReskin, name), height, flip, sorting)) a.UsePlaceholder(height, placeholder, sorting);
            return a;
        }

        void BuildBoard()
        {
            n = bb != null ? BlockBoard.N : GemBoard.W;
            float top = Y(.445f), avail = .39f * viewH;
            cell = Mathf.Min(8.6f / n, avail / n);
            float size = cell * n;
            boardTL = new Vector2(-size / 2, top - (avail - size) / 2);
            Quad(roundSprite, boardTL + new Vector2(size / 2, -size / 2), new Vector2(size + .3f, size + .3f), new Color(0.06f, 0.07f, 0.10f), 1000, true);
            cellR = new SpriteRenderer[n, n];
            for (int y = 0; y < n; y++)
                for (int x = 0; x < n; x++)
                    cellR[x, y] = Quad(white, CellPos(x, y), Vector2.one * cell * .92f, Color.clear, 1010);

            if (bb != null)
            {
                trayCell = Mathf.Min(cell * .55f, .5f, .125f * viewH / 5); // khối 5 ô dựng đứng vẫn nằm gọn dưới bàn
                for (int i = 0; i < 3; i++) slotPos[i] = new Vector2((i - 1) * 3f, Y(.905f));
                RefreshTray();
            }
            else Text("Kéo một viên ngọc sang ô bên cạnh để đổi chỗ", new Vector2(0, Y(.9f)), .28f, Grey);
            RefreshBoard(Snap());
        }

        Vector2 CellPos(int x, int y) => boardTL + new Vector2((x + .5f) * cell, -(y + .5f) * cell);

        Vector2Int CellAt(Vector2 w)
        {
            int x = Mathf.FloorToInt((w.x - boardTL.x) / cell), y = Mathf.FloorToInt((boardTL.y - w.y) / cell);
            return x >= 0 && y >= 0 && x < n && y < n ? new Vector2Int(x, y) : new Vector2Int(-1, -1);
        }

        int[,] Snap() => bb != null ? bb.Snapshot() : gb.Snapshot();

        void RefreshBoard(int[,] g)
        {
            for (int y = 0; y < n; y++)
                for (int x = 0; x < n; x++)
                {
                    var r = cellR[x, y];
                    int v = g[x, y];
                    if (v < 0)
                    {
                        r.sprite = white;
                        r.color = new Color(1, 1, 1, .06f);
                        r.transform.localScale = Vector3.one * cell * .92f;
                    }
                    else
                    {
                        r.sprite = bb != null || v == GemBoard.Stone ? blockSprite : gemSprite;
                        r.color = ActColors[v];
                        r.transform.localScale = Vector3.one * cell * .96f;
                    }
                }
        }

        void RefreshTray()
        {
            for (int i = 0; i < 3; i++)
            {
                foreach (var r in trayR[i]) if (r) Destroy(r.gameObject);
                trayR[i].Clear();
                var p = bb.Hand[i];
                if (p.Used || i == dragIdx) continue;
                DrawPiece(p, slotPos[i], trayCell, bb.Fits(p.Shape) ? 1f : .3f, 1050, trayR[i]);
            }
        }

        void DrawPiece(Piece p, Vector2 center, float c, float alpha, int order, List<SpriteRenderer> into)
        {
            var origin = center + new Vector2(-(p.Shape.W - 1) * c / 2, (p.Shape.H - 1) * c / 2);
            var col = ActColors[p.Color];
            col.a = alpha;
            foreach (var q in p.Shape.Cells)
                into.Add(Quad(blockSprite, origin + new Vector2(q.x * c, -q.y * c), Vector2.one * c * .96f, col, order));
        }

        void RefreshHud()
        {
            enemyBar.Set((float)battle.EnemyHp / Battle.EnemyMaxHp);
            enemyHpT.text = $"{battle.EnemyHp}/{Battle.EnemyMaxHp}";
            heroBar.Set((float)battle.HeroHp / Battle.HeroMaxHp);
            heroHpT.text = battle.Shield > 0 ? $"{battle.HeroHp}/{Battle.HeroMaxHp}  khiên {battle.Shield}" : $"{battle.HeroHp}/{Battle.HeroMaxHp}";
            rageBar.Set(battle.Rage / 100f);
            skillBtn.Label.text = battle.CanCast ? "CHIÊU!" : $"Nộ {battle.Rage}%";
            skillBtn.Bg.color = battle.CanCast ? Gold : Dark;
            turnT.text = $"Lượt {battle.Turns}";
            string act = battle.NextAct == EnemyAct.Attack ? $"Đánh {Battle.EnemyAtk}" : $"Ném {Battle.StoneCount} đá";
            intentT.text = $"{act} sau {battle.Countdown} lượt";
        }

        // ---------- máy tự chơi (menu PokiWar → Tự chơi …): để soi màn hình giữa trận và đo nhanh ----------

        bool autoPlay;
        float autoNext, overAt;
        int autoGamesLeft;
        readonly System.Random autoRng = new();

        // chọn tướng kế tiếp trong danh sách (địch là tướng sau nó); dùng từ menu PokiWar khi đang Play
        public void NextHero()
        {
            if (heroes.Count == 0) FindHeroes();
            heroIdx = (heroIdx + 1) % heroes.Count;
            BuildMenu();
            Debug.Log($"[BanThu] Tướng: {heroes[heroIdx]}, địch: {heroes[(heroIdx + 1) % heroes.Count]}");
        }

        // games trận liên tiếp, chạy nhanh gấp 4; mỗi trận ghi vào tran.csv như người chơi thật
        public void StartAuto(int modeIndex, int games = 3)
        {
            if (heroes.Count == 0) FindHeroes();
            heroIdx = Mathf.Clamp(heroIdx, 0, heroes.Count - 1);
            mode = (Mode)modeIndex;
            autoPlay = true;
            autoGamesLeft = games - 1;
            Time.timeScale = 4;
            StartGame();
        }

        void AutoMove()
        {
            if (battle.Turns == 8) StartCoroutine(Shot("giua_tran_" + ModeKeys[(int)mode], .2f));
            if (battle.CanCast) { StartCoroutine(CastSkill()); return; }
            if (bb != null)
            {
                int bi = -1, bx = 0, by = 0, best = int.MinValue;
                for (int i = 0; i < 3; i++)
                {
                    var p = bb.Hand[i];
                    if (p.Used) continue;
                    for (int y = 0; y < BlockBoard.N; y++)
                        for (int x = 0; x < BlockBoard.N; x++)
                        {
                            if (!bb.CanPlace(p.Shape, x, y)) continue;
                            int score = bb.LinesIfPlaced(p.Shape, x, y) * 100 + y * 2 + autoRng.Next(6); // dồn xuống đáy, ưu tiên xoá
                            if (score > best) { best = score; bi = i; bx = x; by = y; }
                        }
                }
                if (bi < 0) return;
                var steps = bb.Place(bi, bx, by, out var placed);
                RefreshTray();
                StartCoroutine(Turn(placed, steps));
            }
            else
            {
                var moves = gb.Moves();
                if (moves.Count == 0) return;
                var (a, b) = moves[autoRng.Next(moves.Count)];
                TrySwap(a, b);
            }
        }

        // ---------- nhập ----------

        void Update()
        {
            if (cam == null) return;
            if (autoPlay && phase == Phase.Play && Time.time >= autoNext)
            {
                autoNext = Time.time + .45f;
                AutoMove();
            }
            if (autoPlay && phase == Phase.Over && Time.time > overAt + 1.5f)
            {
                if (autoGamesLeft-- > 0) StartGame();
                else { autoPlay = false; Time.timeScale = 1; }
            }
            if (Screen.width != screen.x || Screen.height != screen.y)
            {
                if (phase == Phase.Menu) BuildMenu();
                else if (phase == Phase.Play) BuildPlay();
                else Layout();
            }
            if (Keyboard.current != null && Keyboard.current.f9Key.wasPressedThisFrame) StartCoroutine(Shot("f9_" + ++shots, 0));

            var p = Pointer.current;
            if (p == null) return;
            Vector2 w = cam.ScreenToWorldPoint(p.position.ReadValue());
            if (p.press.wasPressedThisFrame) Down(w);
            else if (p.press.isPressed) Drag(w);
            if (p.press.wasReleasedThisFrame) Up(w);
        }

        void Down(Vector2 w)
        {
            pressed = null;
            foreach (var b in buttons)
                if (b.Rect.Contains(w)) { pressed = b; return; }
            if (phase != Phase.Play) return;
            if (bb != null)
            {
                for (int i = 0; i < 3; i++)
                    if (!bb.Hand[i].Used && Mathf.Abs(w.x - slotPos[i].x) < 1.45f && Mathf.Abs(w.y - slotPos[i].y) < 1.3f)
                    {
                        StartDrag(i, w);
                        return;
                    }
            }
            else
            {
                var c = CellAt(w);
                if (c.x >= 0) { gemDown = c; gemDownW = w; }
            }
        }

        void Drag(Vector2 w)
        {
            if (dragIdx >= 0) MoveDrag(w);
            else if (gemDown.x >= 0)
            {
                var d = w - gemDownW;
                if (d.magnitude < cell * .45f) return;
                var dir = Mathf.Abs(d.x) > Mathf.Abs(d.y) ? new Vector2Int(d.x > 0 ? 1 : -1, 0) : new Vector2Int(0, d.y > 0 ? -1 : 1);
                var a = gemDown;
                gemDown = new Vector2Int(-1, -1);
                TrySwap(a, a + dir);
            }
        }

        void Up(Vector2 w)
        {
            if (pressed != null)
            {
                var b = pressed;
                pressed = null;
                if (b.Rect.Contains(w)) b.Click();
                return;
            }
            if (dragIdx >= 0) EndDrag();
            gemDown = new Vector2Int(-1, -1);
        }

        void StartDrag(int i, Vector2 w)
        {
            dragIdx = i;
            RefreshTray();
            var p = bb.Hand[i];
            DrawPiece(p, w, cell, 1f, 1150, dragR);
            var col = ActColors[p.Color];
            col.a = .35f;
            foreach (var _ in p.Shape.Cells)
            {
                var g = Quad(blockSprite, Vector2.zero, Vector2.one * cell * .96f, col, 1020);
                g.enabled = false;
                ghostR.Add(g);
            }
            MoveDrag(w);
        }

        void MoveDrag(Vector2 w)
        {
            var p = bb.Hand[dragIdx];
            // khối nhấc lên trên ngón tay để ngón không che chỗ đặt
            var center = w + new Vector2(0, cell * 1.8f + (p.Shape.H - 1) * cell / 2);
            var origin = center + new Vector2(-(p.Shape.W - 1) * cell / 2, (p.Shape.H - 1) * cell / 2);
            for (int k = 0; k < p.Shape.Cells.Length; k++)
                dragR[k].transform.position = origin + new Vector2(p.Shape.Cells[k].x * cell, -p.Shape.Cells[k].y * cell);
            dragTarget = new Vector2Int(Mathf.RoundToInt((origin.x - boardTL.x) / cell - .5f), Mathf.RoundToInt((boardTL.y - origin.y) / cell - .5f));
            dragValid = bb.CanPlace(p.Shape, dragTarget.x, dragTarget.y);
            for (int k = 0; k < ghostR.Count; k++)
            {
                ghostR[k].enabled = dragValid;
                if (dragValid) ghostR[k].transform.position = CellPos(dragTarget.x + p.Shape.Cells[k].x, dragTarget.y + p.Shape.Cells[k].y);
            }
        }

        void EndDrag()
        {
            int i = dragIdx;
            dragIdx = -1;
            foreach (var r in dragR) if (r) Destroy(r.gameObject);
            foreach (var r in ghostR) if (r) Destroy(r.gameObject);
            dragR.Clear();
            ghostR.Clear();
            if (!dragValid) { RefreshTray(); return; }
            var steps = bb.Place(i, dragTarget.x, dragTarget.y, out var placed);
            RefreshTray();
            StartCoroutine(Turn(placed, steps));
        }

        void TrySwap(Vector2Int a, Vector2Int b)
        {
            var before = gb.Snapshot();
            var steps = gb.TrySwap(a, b);
            if (steps == null) { Message("Không ghép được"); return; }
            (before[a.x, a.y], before[b.x, b.y]) = (before[b.x, b.y], before[a.x, a.y]);
            StartCoroutine(Turn(before, steps));
        }

        void OnSkill()
        {
            if (phase == Phase.Play && battle.CanCast) StartCoroutine(CastSkill());
        }

        // ---------- lượt ----------

        IEnumerator Turn(int[,] first, List<Step> steps)
        {
            phase = Phase.Busy;
            RefreshBoard(first);
            yield return new WaitForSeconds(.08f);
            yield return PlaySteps(steps);
            if (battle.Over) { End(); yield break; }

            var act = battle.EndTurn();
            RefreshHud();
            if (act == EnemyAct.Attack)
            {
                enemy.Play(AolaActor.Attack);
                yield return new WaitForSeconds(.35f);
                var (lost, blocked) = battle.EnemyAttack();
                hero.Play(AolaActor.Hit);
                Float(lost > 0 ? $"-{lost}" : "Chặn hết", heroFeet + new Vector2(0, 2.4f), ActColors[0]);
                if (blocked > 0) Float($"khiên chặn {blocked}", heroFeet + new Vector2(1.6f, 1.6f), ActColors[1]);
                RefreshHud();
                yield return new WaitForSeconds(.3f);
            }
            else if (act == EnemyAct.Stones)
            {
                enemy.Play(AolaActor.Skill);
                Message("Địch ném đá!");
                yield return new WaitForSeconds(.4f);
                if (bb != null) bb.AddStones(Battle.StoneCount);
                else gb.AddStones(Battle.StoneCount);
                RefreshBoard(Snap());
                RefreshHud();
                yield return new WaitForSeconds(.25f);
            }
            if (battle.Over) { End(); yield break; }

            if (bb != null)
            {
                if (!bb.AnyFits())
                {
                    Message("Hết chỗ! Choáng");
                    yield return new WaitForSeconds(.5f);
                    int lost = battle.Stun();
                    hero.Play(AolaActor.Hit);
                    Float($"-{lost}", heroFeet + new Vector2(0, 2.4f), ActColors[0]);
                    bb.Stun();
                    RefreshBoard(bb.Snapshot());
                    RefreshHud();
                    if (battle.Over) { End(); yield break; }
                }
                RefreshTray();
            }
            else if (!gb.HasMove())
            {
                Message("Hết nước, xáo bàn");
                gb.Shuffle();
                RefreshBoard(gb.Snapshot());
            }
            phase = Phase.Play;
        }

        IEnumerator PlaySteps(List<Step> steps)
        {
            foreach (var st in steps)
            {
                foreach (var c in st.Cleared) cellR[c.x, c.y].color = Color.white;
                yield return new WaitForSeconds(.13f);
                var g = battle.Apply(st.Counts, Mult(st));
                ShowGain(g, st);
                RefreshBoard(st.After);
                RefreshHud();
                yield return new WaitForSeconds(.18f);
            }
        }

        // Mỗi lượt bàn C ra nhiều ô hơn bàn A (lượt nào cũng ghép, lại hay dây chuyền), bàn sập cũng hơn A thường.
        // Máy tự chơi (30/10): C thắng sau 8–19 lượt, A sập 19–29, A 27–43. Hệ số dưới kéo ba bàn về cùng độ dài trận.
        const float GemValue = .4f, SapValue = .75f;

        // A: combo theo lượt liền nhau, nhiều đường một lúc, dây chuyền khi sập. C: dây chuyền.
        float Mult(Step st)
        {
            if (gb != null) return (1 + .25f * st.Chain) * GemValue;
            float combo = 1 + .25f * Mathf.Max(0, bb.Combo - 1);
            return combo * (1 + .3f * (st.Lines - 1)) * (1 + .5f * st.Chain) * (bb.Gravity ? SapValue : 1);
        }

        void ShowGain(Gain g, Step st)
        {
            if (g.Damage > 0)
            {
                hero.Play(AolaActor.Attack);
                StartCoroutine(Later(.25f, () => enemy.Play(AolaActor.Hit)));
                Float($"-{g.Damage}", enemyFeet + new Vector2(0, .15f * viewH * .8f), ActColors[0]);
            }
            if (g.Shield > 0) Float($"+{g.Shield} khiên", heroFeet + new Vector2(1.7f, 1.9f), ActColors[1]);
            if (g.Heal > 0) Float($"+{g.Heal} máu", heroFeet + new Vector2(1.7f, 1.3f), ActColors[2]);
            if (g.Rage > 0) Float($"+{g.Rage} nộ", heroFeet + new Vector2(1.7f, 2.5f), ActColors[3]);
            string tag = st.Chain > 0 ? $"Dây chuyền {st.Chain + 1}" : bb != null && bb.Combo > 1 ? $"Combo x{bb.Combo}" : "";
            if (tag != "") Message(tag);
        }

        IEnumerator CastSkill()
        {
            phase = Phase.Busy;
            hero.Play(AolaActor.Skill);
            Message("Tung chiêu!");
            yield return new WaitForSeconds(Mathf.Clamp(hero.Duration(AolaActor.Skill) * .6f, .3f, .9f));
            int d = battle.Cast();
            enemy.Play(AolaActor.Hit);
            Float($"-{d}", enemyFeet + new Vector2(0, .15f * viewH * .8f), Gold);
            List<Step> extra = null;
            if (bb != null) bb.RemoveStones();
            else extra = gb.RemoveStones();
            RefreshBoard(Snap());
            RefreshHud();
            if (extra != null && extra.Count > 0) yield return PlaySteps(extra);
            if (bb != null) RefreshTray();
            if (battle.Over) { End(); yield break; }
            phase = Phase.Play;
        }

        void End()
        {
            phase = Phase.Over;
            overAt = Time.time;
            float secs = Time.time - startTime;
            (battle.Won ? hero : enemy).Play(AolaActor.Skill);
            Log(secs);

            Quad(white, Vector2.zero, new Vector2(40, 40), new Color(0, 0, 0, .78f), 1500);
            Text(battle.Won ? "THẮNG!" : "THUA", new Vector2(0, Y(.44f)), 1.1f, battle.Won ? Gold : ActColors[0], TextAnchor.MiddleCenter, 1510);
            Text($"{ModeNames[(int)mode]}\n{battle.Turns} lượt · {secs:0} giây", new Vector2(0, Y(.52f)), .38f, Color.white, TextAnchor.MiddleCenter, 1510);
            Button("Chơi lại", new Vector2(-2.2f, Y(.61f)), new Vector2(3.8f, .055f * viewH), StartGame, new Color(0.20f, 0.55f, 0.30f), .36f, 1520);
            Button("Menu", new Vector2(2.2f, Y(.61f)), new Vector2(3.8f, .055f * viewH), BuildMenu, Dark, .36f, 1520);
            if (autoShots) StartCoroutine(Shot("ket_" + ModeKeys[(int)mode], .8f));
        }

        void Log(float secs)
        {
            try
            {
                Directory.CreateDirectory(outDir);
                string f = Path.Combine(outDir, "tran.csv");
                string head = File.Exists(f) ? "" : "thoi_diem,ban,tuong,dich,ket_qua,luot,giay,mau_con,mau_dich_con,may_tu_choi\n";
                File.AppendAllText(f, head + $"{DateTime.Now:yyyy-MM-dd HH:mm:ss},{ModeKeys[(int)mode]},{heroName},{enemyName}," +
                                      $"{(battle.Won ? "thang" : "thua")},{battle.Turns},{secs:0},{battle.HeroHp},{battle.EnemyHp},{(autoPlay ? 1 : 0)}\n");
            }
            catch (Exception e)
            {
                Debug.LogWarning("[BanThu] Không ghi được tran.csv: " + e.Message);
            }
        }

        // ---------- hiển thị ----------

        void Message(string s)
        {
            if (!msgT) return;
            msgT.text = s;
            int token = ++msgToken;
            StartCoroutine(Later(1f, () => { if (token == msgToken && msgT) msgT.text = ""; }));
        }

        void Float(string s, Vector2 pos, Color c)
        {
            var t = Text(s, pos, .42f, c, TextAnchor.MiddleCenter, 1300);
            StartCoroutine(FloatUp(t));
        }

        static IEnumerator FloatUp(TextMesh t)
        {
            var p0 = t.transform.position;
            for (float k = 0; k < .9f; k += Time.deltaTime)
            {
                if (!t) yield break;
                t.transform.position = p0 + Vector3.up * k * 1.2f;
                var c = t.color;
                c.a = 1 - k / .9f;
                t.color = c;
                yield return null;
            }
            if (t) Destroy(t.gameObject);
        }

        static IEnumerator Later(float s, Action a)
        {
            yield return new WaitForSeconds(s);
            a();
        }

        IEnumerator Shot(string tag, float delay)
        {
            yield return new WaitForSeconds(delay);
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(outDir);
            string path = Path.Combine(outDir, $"shot_{tag}.png");
            ScreenCapture.CaptureScreenshot(path);
            Debug.Log("[BanThu] Chụp " + path);
        }

        SpriteRenderer Quad(Sprite s, Vector2 pos, Vector2 size, Color c, int order, bool sliced = false)
        {
            var go = new GameObject("o");
            go.transform.SetParent(root, false);
            go.transform.position = pos;
            var sr = go.AddComponent<SpriteRenderer>();
            sr.sprite = s;
            sr.color = c;
            sr.sortingOrder = order;
            if (sliced) { sr.drawMode = SpriteDrawMode.Sliced; sr.size = size; }
            else go.transform.localScale = new Vector3(size.x, size.y, 1);
            return sr;
        }

        TextMesh Text(string s, Vector2 pos, float height, Color c, TextAnchor anchor = TextAnchor.MiddleCenter, int order = 1200)
        {
            var go = new GameObject("chu");
            go.transform.SetParent(root, false);
            go.transform.position = pos;
            var tm = go.AddComponent<TextMesh>();
            tm.font = font;
            tm.fontSize = 64;
            tm.characterSize = height * 10f / 64f; // chiều cao một dòng ≈ fontSize × characterSize / 10
            tm.anchor = anchor;
            tm.alignment = anchor == TextAnchor.MiddleLeft || anchor == TextAnchor.UpperLeft ? TextAlignment.Left : TextAlignment.Center;
            tm.color = c;
            tm.text = s;
            var mr = go.GetComponent<MeshRenderer>();
            mr.sharedMaterial = font.material;
            mr.sortingOrder = order;
            return tm;
        }

        Btn Button(string label, Vector2 center, Vector2 size, Action click, Color bg, float textH, int order = 1100)
        {
            var b = new Btn
            {
                Rect = new Rect(center - size / 2, size),
                Bg = Quad(roundSprite, center, size, bg, order, true),
                Label = Text(label, center, textH, Color.white, TextAnchor.MiddleCenter, order + 2),
                Click = click,
                Base = bg,
            };
            buttons.Add(b);
            return b;
        }

        Bar MakeBar(float x0, float w, float y, float h, Color c, int order = 1100)
        {
            Quad(white, new Vector2(x0 + w / 2, y), new Vector2(w + .08f, h + .08f), new Color(0, 0, 0, .55f), order - 1);
            var bar = new Bar { Fill = Quad(white, new Vector2(x0, y), new Vector2(0, h), c, order), X0 = x0, W = w, Y = y, H = h };
            bar.Set(1);
            return bar;
        }

        static Sprite MakeSprite(int size, Func<float, float, Color> pixel, float border = 0)
        {
            var t = new Texture2D(size, size, TextureFormat.RGBA32, false) { wrapMode = TextureWrapMode.Clamp, filterMode = FilterMode.Bilinear };
            var px = new Color[size * size];
            for (int y = 0; y < size; y++)
                for (int x = 0; x < size; x++)
                    px[y * size + x] = pixel(x + .5f, y + .5f);
            t.SetPixels(px);
            t.Apply();
            return Sprite.Create(t, new Rect(0, 0, size, size), new Vector2(.5f, .5f), size, 0, SpriteMeshType.FullRect, Vector4.one * border);
        }

        static float RoundAlpha(float x, float y, float size, float r)
        {
            float dx = Mathf.Max(r - x, x - (size - r), 0), dy = Mathf.Max(r - y, y - (size - r), 0);
            return Mathf.Clamp01(r - Mathf.Sqrt(dx * dx + dy * dy) + .5f);
        }

        static Color BlockPixel(float x, float y)
        {
            float edge = Mathf.Min(Mathf.Min(x, y), Mathf.Min(64 - x, 64 - y));
            float v = edge < 5 ? .7f : y > 48 ? 1f : .9f; // viền tối, dải sáng phía trên
            return new Color(v, v, v, RoundAlpha(x, y, 64, 10));
        }

        static Color GemPixel(float x, float y)
        {
            float d = Vector2.Distance(new Vector2(x, y), new Vector2(32, 32));
            float shine = Mathf.Clamp01(1 - Vector2.Distance(new Vector2(x, y), new Vector2(24, 42)) / 14);
            float v = d > 26 ? .68f : .86f + .14f * shine;
            return new Color(v, v, v, Mathf.Clamp01(30 - d + .5f));
        }
    }
}
