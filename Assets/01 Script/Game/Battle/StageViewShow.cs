// Trình diễn trận (2026-11-17, đợt "tăng dày nội dung", việc D): chết, ra sân, rút lui, hồi sinh, chuỗi boss tiến hóa. Phần riêng của
// StageView (partial), để file chính (dùng chung với phiên làm hiệu ứng từng tướng) chỉ đổi vài chỗ.
// - Clip chết, ra sân, rút lui chạy theo giờ animation của tướng (tốc độ gốc như đánh, chiêu; người dùng 2026-11-09 "tốc độ animation
//   về gốc"), không theo nhịp sân ×3 như trước: clip chết 2 giây trước đây hết trong 0,66 giây rồi bị tướng kế ra sân cắt ngang.
// - BattlePlayer chờ clip thật (WaitDown, WaitEntered, WaitRetreat) thay cho số chờ cứng; tướng chỉ ra đòn khi clip ra sân xong; bị
//   đánh lúc đang ra sân thì chỉ chớp, bật lùi (StageView.Hurt).
// - Boss tiến hóa (Evolve): dạng cũ diễn clip chết; nền tối dần, gần cuối thân trắng dần nhấp nháy nhanh dần, vệt sáng màu hệ hút vào
//   thân, vòng dưới chân co lại; chớp kem, đổi dạng; sóng toả, tia văng, rung và khựng theo Power; chữ "TIẾN HÓA!" đóng dấu, tên dạng;
//   dạng mới diễn clip ra sân (không có thì bật ra 0,88 → 1,07 → 1), hạt màu hệ bay lên, nền sáng lại. Sàn đấu, mặt boss, tên trên bảng,
//   thanh máu dâng do BattlePlayer làm trong onBurst.
// - Hồi sinh (Revive): tướng nằm xuống theo clip chết rồi được ánh sáng vàng nâng dậy bằng clip ra sân.
// Mọi hình là mục dùng lại của sân (textFx, ringFx, sparkFx) hoặc hạt chồng lớp (HatLua); không sinh đồ vật mới.
using System;
using System.Collections;
using PokiClash.Core;
using PokiClash.UI;
using UnityEngine;
using Random = UnityEngine.Random;

namespace PokiClash
{
    public sealed partial class StageView
    {
        // giây animation: hình không có clip ra sân rơi xuống trong EnterFall; không có clip chết thì khựng, ngã, mờ trong DieFade;
        // rút lui khi đổi tướng RetreatLen
        const float EnterFall = 0.34f, DieFade = 0.6f, RetreatLen = 0.3f;
        // boss tiến hóa: clip chết của dạng cũ chạy tối đa EvoDieCap giây (dài hơn thì ánh sáng biến hình phủ từ đó), thân trắng dần trong
        // EvoGlow giây cuối; chờ clip ra sân của dạng mới tối đa EvoAppearCap giây (phần còn lại chạy tiếp, đòn kế của nó chờ clip xong)
        const float EvoDieCap = 1.6f, EvoGlow = 0.55f, EvoAppearCap = 1.8f;
        static readonly Color Cream = new Color(1f, 0.97f, 0.86f, 1f);
        static readonly Color DimTint = new Color(0.4f, 0.38f, 0.5f, 1f); // nền lúc tối hẳn (nhân màu)
        static readonly Color[] DustStops =
            { new Color32(206, 188, 150, 255), new Color32(222, 208, 178, 255), new Color32(234, 224, 202, 255), new Color32(244, 238, 224, 255) };
        static readonly string[] EnterThuds = { "cham_dat", "dap_dat", "nen", "bam_dat", "go" }; // sự kiện chạm đất của clip ra sân
        static readonly string[] DieThuds = { "nga", "cham_dat", "sap" };                     // của clip chết

        // pha trình diễn đang chạy (menu thử đọc để chụp đúng lúc): "", "evo_chet", "evo_tu", "evo_sang", "evo_ra", "hoi_sinh"
        public string ShowPhase { get; private set; } = "";
        Actor evolving; // dạng cũ đang biến hình: clip chết không thả hạt "linh hồn" bay lên
        float dimK = -1;

        bool HasDie(Actor a) => a != null && a.aola != null && a.aola.HasClip(Game.AolaActor.Die);
        bool HasAppear(Actor a) => a != null && a.aola != null && a.aola.HasClip(Game.AolaActor.Appear);
        float DieLen(Actor a) => HasDie(a) ? a.aola.Duration(Game.AolaActor.Die) : DieFade;
        float EnterLen(Actor a) => HasAppear(a) ? a.aola.Duration(Game.AolaActor.Appear) : EnterFall;
        bool Entering(Actor a) => a != null && a.dead <= 0 && a.enter < EnterLen(a);
        bool Busy(Actor a) => a != null && (a.dead > 0 && a.dead < DieLen(a) || Entering(a));
        float Real(float s) => s / Mathf.Max(1, fast); // giây thật của s giây animation (công cụ thử tua nhanh)

        public bool IsDown(int side) => actors[side] != null && actors[side].dead > 0;
        public int FormShown(int side) => actors[side] != null ? actors[side].form : 0; // dạng đang hiện trên sân
        public bool IsEntering(int side) => Entering(actors[side]);

        // giữ nhịp sân ×1 trong s giây sân (như lúc ra đòn): chữ, hạt, chờ của BattlePlayer khớp giờ animation của đoạn trình diễn
        public void HoldPace(float s) => skillHold = Mathf.Max(skillHold, s);

        // thôi giữ nhịp ×1 (đoạn trình diễn xong sớm hơn số đã giữ): sân về nhịp thường mượt trong SlowEase
        public void ReleasePace() => skillHold = Mathf.Min(skillHold, 0.1f);

        // đầu trận (StageView.Init): bỏ nền tối, pha còn sót của trận trước (thoát giữa chừng)
        void ResetShow()
        {
            dimK = -1;
            Dim(0);
            ShowPhase = "";
            evolving = null;
        }

        // ---------- chờ theo clip thật ----------

        // chờ clip chết của bên side chạy xong (cap giây animation, mặc định 2,8; boss 4,2); tướng bị thay hay sân tắt thì thôi chờ
        public IEnumerator WaitDown(int side, float cap = -1)
        {
            var a = actors[side];
            if (a == null || a.dead <= 0) yield break;
            if (cap < 0) cap = a.boss ? 4.2f : 2.8f;
            float end = Time.unscaledTime + Real(cap);
            while (this && isActiveAndEnabled && actors[side] == a && a.dead > 0 && a.dead < DieLen(a) && Time.unscaledTime < end) yield return null;
        }

        // chờ clip ra sân của bên side xong (cap giây animation, mặc định 3,2; boss 5)
        public IEnumerator WaitEntered(int side, float cap = -1)
        {
            var a = actors[side];
            if (!Entering(a)) yield break;
            if (cap < 0) cap = a.boss ? 5f : 3.2f;
            float end = Time.unscaledTime + Real(cap);
            while (this && isActiveAndEnabled && actors[side] == a && Entering(a) && Time.unscaledTime < end) yield return null;
        }

        // chờ tướng bên side lùi khỏi sân (Retreat)
        public IEnumerator WaitRetreat(int side)
        {
            var a = actors[side];
            float end = Time.unscaledTime + Real(RetreatLen + 0.3f);
            while (this && isActiveAndEnabled && a != null && actors[side] == a && a.exit > 0 && a.exit < RetreatLen && Time.unscaledTime < end)
                yield return null;
        }

        // chờ hai bên hết đang chết, đang ra sân (kết trận: con cuối nằm hẳn rồi mới hiện bảng kết quả)
        public IEnumerator WaitSettled(float cap)
        {
            float end = Time.unscaledTime + Real(cap);
            while (this && isActiveAndEnabled && Time.unscaledTime < end && (Busy(actors[0]) || Busy(actors[1]))) yield return null;
        }

        // ---------- gục ----------

        // tướng bên side gục (cú hạ gục, hoặc sự kiện Death): clip chết bắt đầu từ đây, gọi lại không chạy lại từ đầu
        public void KnockDown(int side)
        {
            var a = actors[side];
            if (a == null || a.dead > 0) return;
            a.dead = 0.0001f;
            a.flash = Mathf.Max(a.flash, 0.12f);
        }

        // nhịp của clip ra sân: chạm đất thì rung, bụi; gầm thì rung đều; hình rơi xuống thì rung nhẹ, bụi lúc chạm (gọi từ Update)
        void EnterBeats(Actor a, float e0)
        {
            if (e0 > EnterLen(a)) return; // ra sân xong (a.enter còn chạy tới 9)
            if (HasAppear(a))
            {
                foreach (var n in EnterThuds)
                {
                    float tl = a.aola.EventTime(Game.AolaActor.Appear, n);
                    if (tl < 0 || e0 >= tl || a.enter < tl) continue;
                    AddTrauma(n == "cham_dat" ? 0.35f : 0.28f);
                    Dust(a.side, 1f);
                }
                float tg = a.aola.EventTime(Game.AolaActor.Appear, "gam");
                if (tg >= 0 && e0 < tg && a.enter >= tg) AddTrauma(0.18f + 0.15f * Power(a.side));
            }
            else if (e0 < EnterFall && a.enter >= EnterFall)
            {
                AddTrauma(0.14f);
                Dust(a.side, 0.75f);
            }
        }

        // nhịp của clip chết: thân chạm đất thì thịch nhẹ, bụi; hơn nửa clip thì vài hạt màu hệ bay lên (vfx-petclash mục 12 "Chết")
        void DieBeats(Actor a, float d0)
        {
            if (d0 > DieLen(a)) return; // clip chết xong (a.dead còn chạy)
            if (HasDie(a))
                foreach (var n in DieThuds)
                {
                    float tl = a.aola.EventTime(Game.AolaActor.Die, n);
                    if (tl < 0 || d0 >= tl || a.dead < tl) continue;
                    AddTrauma(0.14f + 0.12f * Power(1 - a.side));
                    Dust(a.side, 1f);
                }
            else if (d0 < DieFade * 0.75f && a.dead >= DieFade * 0.75f) Dust(a.side, 0.8f);
            float tm = DieLen(a) * 0.6f;
            if (a != evolving && d0 < tm && a.dead >= tm) Motes(a.side, Color.Lerp(Theme.Of(a.hero.elem), Color.white, 0.3f), 6, 0.6f, BodyNow(a) - Body(a.side));
        }

        // ---------- hồi sinh ----------

        // Bị động hồi sinh: tướng đang nằm (clip chết từ cú hạ gục) chờ tới khi gần nằm hẳn (tối đa 1,1 giây), thân trắng dần, chớp vàng,
        // vòng sáng, hạt vàng bay lên; rồi clip ra sân (không có thì bật lên). onLight: lúc chớp (chữ, tiếng, thanh máu dâng).
        public IEnumerator Revive(int side, Action onLight)
        {
            var a = actors[side];
            if (a == null)
            {
                onLight?.Invoke();
                yield break;
            }
            ShowPhase = "hoi_sinh";
            HoldPace(3);
            var gold = Theme.Hex("#f7c948");
            if (a.dead > 0)
            {
                float until = Mathf.Min(DieLen(a) * 0.75f, 1.1f);
                float guard = Time.unscaledTime + Real(until + 1.5f);
                while (this && isActiveAndEnabled && actors[side] == a && a.dead < until && Time.unscaledTime < guard)
                {
                    float g = Mathf.Clamp01((a.dead - (until - 0.35f)) / 0.35f);
                    if (g > 0) a.flash = 0.2f * g + 0.02f;
                    yield return null;
                }
            }
            if (!this || !isActiveAndEnabled || actors[side] != a)
            {
                onLight?.Invoke();
                ShowPhase = "";
                yield break;
            }
            Flash(new Color(1, 0.93f, 0.66f, 0.8f));
            a.dead = 0;
            a.recoil = -1;
            a.clip = Idle;
            a.loop = true;
            a.t = 0;
            if (HasAppear(a)) a.enter = 0;
            else
            {
                a.enter = 9;
                StartCoroutine(Pop(a, 0.8f));
            }
            a.flash = 0.32f;
            BigRing(Body(side), gold, a.H * 1.7f, 0, 0.5f);
            FloorRing(Pos[side], gold, a.H * 0.3f, a.H * 1.8f, 0, 0.5f);
            Motes(side, Color.Lerp(gold, Color.white, 0.3f), 12, 0.7f);
            AddTrauma(0.22f);
            onLight?.Invoke();
            yield return WaitEntered(side, 2.2f);
            ReleasePace();
            ShowPhase = "";
        }

        // ---------- boss tiến hóa ----------

        // Chuỗi tiến hóa (EvType.Evolve): chết → biến hình → ra sân. Đúng cả khi boss tiến hóa lúc máu về 0 (cú hạ gục đã gọi KnockDown,
        // clip chết đang chạy thì chạy tiếp) lẫn khi tiến hóa dưới ngưỡng máu (còn đứng: bắt đầu clip chết từ đây). Tổng khoảng 2,5–3,5
        // giây (clip chết ≤ 1,6 + ra sân ≤ 1,8), theo giờ animation nên công cụ thử tua nhanh cũng nhanh theo.
        // onCharge: lúc bắt đầu tụ sáng (tiếng); onBurst: lúc chớp đổi dạng (sàn đấu, mặt boss, tên, thanh máu, tiếng, rung tay).
        public IEnumerator Evolve(int side, HeroDef hero, bool boss, int star, string formName, Action onCharge, Action onBurst)
        {
            var a = actors[side];
            float pw = Power(side);
            var col = Color.Lerp(Theme.Of(hero.elem), Color.white, 0.2f);
            ShowPhase = "evo_chet";
            HoldPace(8);
            if (a != null)
            {
                evolving = a;
                KnockDown(side);
                // cửa sổ chết: trọn clip chết (dài hơn EvoDieCap thì tới đó); sáng lên trong EvoGlow giây cuối của cửa sổ
                float win = HasDie(a) ? Mathf.Min(DieLen(a), EvoDieCap) : DieFade;
                float glow0 = Mathf.Max(0.12f, win - EvoGlow), glowLen = win - glow0;
                // chưa sáng xong mà clip sắp hết (chuỗi bắt đầu trễ): giữ ở khung còn thân, đừng để clip chạy tới khung trống
                float hold = HasDie(a) ? Mathf.Max(glow0, Mathf.Min(win, DieLen(a) - 0.12f)) : win;
                float g = -1; // tiến độ sáng 0..1 (-1: chưa sáng)
                float guard = Time.unscaledTime + Real(win + glowLen + 2f);
                while (this && isActiveAndEnabled && actors[side] == a && Time.unscaledTime < guard)
                {
                    if (g < 1 && a.dead > hold) a.dead = hold;
                    float d = a.dead;
                    if (g < 0 && d >= glow0)
                    {
                        g = 0;
                        ShowPhase = "evo_tu";
                        onCharge?.Invoke();
                        Charge(a, col, pw, glowLen, BodyNow(a)); // tụ vào chỗ thân đang nằm (clip chết hay dời thân khỏi chỗ đứng)
                    }
                    else if (g >= 0) g = Mathf.Min(1, g + Time.unscaledDeltaTime * Mathf.Max(1, fast) / Mathf.Max(0.05f, glowLen));
                    float prog = Mathf.Clamp01((d - 0.1f) / Mathf.Max(0.2f, win - 0.1f));
                    if (g >= 0) prog = Mathf.Max(prog, Mathf.Lerp(glow0 / win, 1, g));
                    Dim(Mathf.SmoothStep(0, 1, prog) * 0.85f);
                    // thân trắng dần (shader sticker _Flash tối đa 0,65), nhấp nháy nhanh dần
                    if (g >= 0) a.flash = 0.2f * g * (0.78f + 0.22f * Mathf.Sin(d * (16 + 34 * g) + g * 20)) + 0.02f;
                    if (g >= 1 && d >= win) break;
                    yield return null;
                }
                // khựng: một nhịp nín thở trước chớp (giờ animation)
                for (float t = 0; t < 0.12f && this && isActiveAndEnabled; t += Time.unscaledDeltaTime * Mathf.Max(1, fast))
                {
                    if (actors[side] == a) a.flash = 0.22f;
                    yield return null;
                }
            }
            if (!this || !isActiveAndEnabled) yield break;

            // chớp kem che lúc đổi hình
            ShowPhase = "evo_sang";
            Flash(Cream);
            SetActor(side, hero, boss, true, star);
            evolving = null;
            var b = actors[side];
            bool rig = HasAppear(b);
            if (!rig)
            {
                b.enter = 9; // không rơi từ trời xuống: bật ra từ ánh sáng
                StartCoroutine(Pop(b));
            }
            b.flash = 0.34f;
            EvoBurst(b, col, pw);
            // chữ đóng dấu sát bảng thông tin của boss (dải trời trên bảng; bảng vẽ trên lớp hiệu ứng nên không đặt đè lên bảng): không che
            // dạng mới đang hiện, không đè tướng bên kia
            float ts = 40 * (1 + 0.2f * pw);
            bool named = !string.IsNullOrEmpty(formName);
            if (TitleSpots(side, ts, 25, out var tw, out var nw))
            {
                Title("TIẾN HÓA!", Theme.Hex("#ffe08a"), ts, Vector2.zero, 0, 1.5f, tw);
                if (named) Title(formName, Theme.Hex("#fff6c8"), 25, Vector2.zero, 0.14f, 1.36f, nw);
            }
            else
            {
                var at = new Vector2(SW * 0.5f, 60);
                Title("TIẾN HÓA!", Theme.Hex("#ffe08a"), ts, at, 0, 1.5f);
                if (named) Title(formName, Theme.Hex("#fff6c8"), 25, at + new Vector2(0, 38), 0.14f, 1.36f);
            }
            Motes(side, col, Mathf.RoundToInt(Mathf.Lerp(8, 14, pw)), 0.9f);
            onBurst?.Invoke();

            // dạng mới ra sân, nền sáng lại
            ShowPhase = "evo_ra";
            float cap = rig ? Mathf.Min(EnterLen(b), EvoAppearCap) : 0.5f;
            float t0 = Time.unscaledTime;
            while (this && isActiveAndEnabled && actors[side] == b)
            {
                float k = rig ? b.enter : (Time.unscaledTime - t0) * Mathf.Max(1, fast);
                Dim(0.85f * (1 - Mathf.SmoothStep(0, 1, k / 0.6f)));
                if (k >= cap || Time.unscaledTime - t0 > Real(cap + 1f)) break;
                yield return null;
            }
            Dim(0);
            ReleasePace();
            ShowPhase = "";
        }

        // tâm thân đang hiện (đơn vị sân): đo khung bao hình của rig, không đo được thì chỗ thân lúc đứng
        Vector2 BodyNow(Actor a) => a.aola != null && a.aola.Center(out var c) ? Pos[a.side] + c : Body(a.side);

        // tụ sáng trong dur giây quanh thân (body: tâm thân đang nằm): vệt sáng màu hệ hút vào tâm (nhanh dần), vòng sáng co lại quanh
        // thân, vòng dưới chân co lại
        void Charge(Actor a, Color c, float pw, float dur, Vector2 body)
        {
            var feet = new Vector2(body.x, Pos[a.side].y);
            float H = a.H;
            int n = Mathf.RoundToInt(Mathf.Lerp(14, 24, pw));
            for (int i = 0; i < n; i++)
            {
                float ang = (i + Random.value * 0.6f) / n * Mathf.PI * 2;
                float r = H * Random.Range(0.8f, 1.2f);
                var from = body + new Vector2(Mathf.Cos(ang) * r, Mathf.Sin(ang) * r * 0.85f);
                float life = Random.Range(0.3f, 0.44f);
                float delay = Random.Range(0, Mathf.Max(0.05f, dur - life));
                Streak(from, body + Random.insideUnitCircle * H * 0.08f, Color.Lerp(c, Cream, Random.Range(0.2f, 0.8f)), delay, life, Random.Range(9f, 13f));
            }
            BigRing(body, Cream, H * 1.9f, 0, dur + 0.05f, true);
            BigRing(body, c, H * 1.5f, dur * 0.35f, dur * 0.65f + 0.05f, true);
            FloorRing(feet, c, H * 1.6f, H * 0.2f, 0, dur + 0.05f);
            FloorRing(feet, Cream, H * 1.2f, H * 0.15f, dur * 0.4f, dur * 0.6f + 0.05f);
        }

        // lúc đổi dạng: sóng kem và sóng màu hệ toả, vòng sóng dưới chân (hạt chồng lớp có viền mực nếu có), tia văng, rung, khựng theo Power
        void EvoBurst(Actor b, Color c, float pw)
        {
            var body = Body(b.side);
            var feet = Pos[b.side];
            float H = b.H;
            BigRing(body, Cream, H * 2.3f, 0, 0.5f);
            BigRing(body, c, H * 1.7f, 0.07f, 0.45f);
            FloorRing(feet, c, H * 0.3f, H * 2.6f, 0, 0.55f);
            Spark(b.side, Cream, Mathf.RoundToInt(Mathf.Lerp(12, 22, pw)), 1.2f + 0.4f * pw);
            Spark(b.side, c, Mathf.RoundToInt(Mathf.Lerp(6, 12, pw)), 0.9f + 0.3f * pw);
            var h = Hat;
            if (h != null) h.Ring(feet + new Vector2(0, 2), 0.5f, 0.2f * H, 1.5f * H, c);
            AddTrauma(Mathf.Lerp(0.45f, 0.85f, pw));
            Freeze(Mathf.Lerp(0.06f, 0.12f, pw));
        }

        // bật ra 0,88 → 1,07 → 1 quanh chân (dạng không có clip ra sân)
        IEnumerator Pop(Actor a, float s0 = 0.88f)
        {
            if (a.aola == null) yield break;
            var rt = a.body;
            for (float t = 0; t < 0.36f; t += Time.unscaledDeltaTime * Mathf.Max(1, fast))
            {
                if (!rt || actors[a.side] != a) yield break;
                float s = t < 0.2f ? Mathf.Lerp(s0, 1.07f, Out01(t / 0.2f)) : Mathf.Lerp(1.07f, 1f, Mathf.SmoothStep(0, 1, (t - 0.2f) / 0.16f));
                rt.localScale = new Vector3(s, s, 1);
                yield return null;
            }
            if (rt) rt.localScale = Vector3.one;
        }

        // nền (ảnh sàn, trời, phần động) tối đi theo k 0..1; tướng, hạt, chữ giữ sáng. Nhân màu ở CanvasRenderer nên không đụng màu
        // phủ của sàn đấu (ApplyArena) và đổi nền giữa chừng vẫn giữ độ tối.
        void Dim(float k)
        {
            k = Mathf.Clamp01(k);
            if (Mathf.Abs(k - dimK) < 0.002f) return;
            dimK = k;
            var c = Color.Lerp(Color.white, DimTint, k);
            if (bg) bg.canvasRenderer.SetColor(c);
            if (sky) sky.canvasRenderer.SetColor(c);
            if (arena) arena.Dim(c);
        }

        // ---------- hình nhỏ dùng lại ----------

        // số liền nhau trên cùng một con (trong 0,45 giây): so le phải trái, nâng dần (đơn vị sân, y lên)
        readonly float[] numAt = { -9, -9 };
        readonly int[] numIdx = new int[2];

        Vector2 NumberStack(int side)
        {
            float now = Time.unscaledTime;
            numIdx[side] = now - numAt[side] < Real(0.45f) ? Mathf.Min(numIdx[side] + 1, 4) : 0;
            numAt[side] = now;
            int i = numIdx[side];
            return i == 0 ? Vector2.zero : new Vector2((i % 2 == 1 ? 1 : -1) * (34 + 10 * i), 24 * i);
        }

        // chữ đóng dấu (tiến hóa): to 2,2 lần rồi nện về, nảy nhẹ, giữ, mờ và trôi lên ở 25% cuối; delay, life giây sân
        // Chỗ (toạ độ thế giới) của chữ "TIẾN HÓA!" và tên dạng: trên bảng thông tin của bên side (bảng địch là bảng nằm cao hơn) nếu dải
        // trời trên bảng đủ chỗ, không thì ngay dưới bảng. false: không thấy bảng.
        bool TitleSpots(int side, float titleSize, float nameSize, out Vector3 title, out Vector3 name)
        {
            title = name = Vector3.zero;
            BattlePlate best = null;
            if (plateLayer)
                foreach (var pl in plateLayer.GetComponentsInChildren<BattlePlate>())
                    if (best == null || (side == 1 ? pl.Rect.position.y > best.Rect.position.y : pl.Rect.position.y < best.Rect.position.y))
                        best = pl;
            if (!best) return false;
            float th = titleSize * K, nh = nameSize * K; // cao chữ (đơn vị UI)
            var c = new Vector3[4];
            best.Rect.GetWorldCorners(c); // 0 dưới trái, 1 trên trái, 2 trên phải, 3 dưới phải
            var top = fxLayer.InverseTransformPoint((c[1] + c[2]) * 0.5f);
            var bottom = fxLayer.InverseTransformPoint((c[0] + c[3]) * 0.5f);
            float roof = float.MaxValue;
            if (transform.parent is RectTransform area)
            {
                var ac = new Vector3[4];
                area.GetWorldCorners(ac);
                roof = fxLayer.InverseTransformPoint(ac[1]).y;
            }
            const float gap = 8;
            Vector3 tl, nl;
            if (roof - top.y >= th + nh + 3 * gap)
            {
                nl = new Vector3(top.x, top.y + gap + nh * 0.5f, 0);
                tl = new Vector3(top.x, nl.y + nh * 0.5f + gap + th * 0.5f, 0);
            }
            else
            {
                tl = new Vector3(bottom.x, bottom.y - gap - th * 0.5f, 0);
                nl = new Vector3(bottom.x, tl.y - th * 0.5f - gap - nh * 0.5f, 0);
            }
            title = fxLayer.TransformPoint(tl);
            name = fxLayer.TransformPoint(nl);
            return true;
        }

        // world: đặt theo toạ độ thế giới (TitleSpots) thay cho điểm sân at
        void Title(string text, Color color, float size, Vector2 at, float delay, float life, Vector3? world = null)
        {
            var item = FxText(text, color, size);
            var rt = item.Rect;
            if (world.HasValue)
            {
                // giữ cả chữ (kể cả lúc nảy 1,1 lần) trong bề ngang lớp hiệu ứng
                var lp = fxLayer.InverseTransformPoint(world.Value);
                float hw = item.Label.preferredWidth * 0.55f + 16 * K;
                var fr = fxLayer.rect;
                lp.x = fr.width > 2 * hw ? Mathf.Clamp(lp.x, fr.xMin + hw, fr.xMax - hw) : fr.center.x;
                rt.position = fxLayer.TransformPoint(lp);
            }
            else rt.anchoredPosition = P(at);
            rt.localEulerAngles = new Vector3(0, 0, Random.Range(-4f, 4f));
            AddFx(item, textFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    f.rt.localScale = Vector3.zero;
                    return;
                }
                float u = t / life;
                float s = t < 0.14f ? Mathf.Lerp(1.7f, 0.94f, Out01(t / 0.14f)) : t < 0.24f ? Mathf.Lerp(0.94f, 1f, (t - 0.14f) / 0.1f) : 1;
                f.rt.localScale = new Vector3(s, s, 1);
                f.cg.alpha = Mathf.Min(1, t / 0.05f) * (u > 0.75f ? 1 - (u - 0.75f) / 0.25f : 1);
                f.rt.anchoredPosition = f.basePos + new Vector2(0, u > 0.75f ? (u - 0.75f) * 60 * K : 0);
            });
        }

        // vệt sáng bay từ from tới to (đơn vị sân), nhanh dần, dài dần theo tốc độ, mờ ở hai đầu
        void Streak(Vector2 from, Vector2 to, Color c, float delay, float life, float thick)
        {
            if (!sparkFx) return;
            var item = Take(sparkFx);
            item.Image.color = c;
            var rt = item.Rect;
            var d = to - from;
            rt.localEulerAngles = new Vector3(0, 0, Mathf.Atan2(-d.y, d.x) * Mathf.Rad2Deg);
            rt.anchoredPosition = P(from);
            AddFx(item, sparkFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life;
                f.rt.anchoredPosition = P(Vector2.LerpUnclamped(from, to, u * u));
                f.rt.sizeDelta = new Vector2((14 + 46 * u) * K, thick * (1 - 0.45f * u) * K);
                f.cg.alpha = Mathf.Min(1, u / 0.15f) * Mathf.Min(1, (1 - u) / 0.2f);
            });
        }

        // vòng toả quanh at (đơn vị sân), nở từ 0,2 tới size, mờ dần
        // contract: co từ size về 0,15 (tụ sáng), không thì nở từ 0,2 tới size (sóng toả)
        void BigRing(Vector2 at, Color c, float size, float delay, float life, bool contract = false)
        {
            if (!ringFx) return;
            var item = Take(ringFx);
            item.Image.color = c;
            var rt = item.Rect;
            rt.anchoredPosition = P(at);
            AddFx(item, ringFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life, s = contract ? Mathf.Lerp(1, 0.15f, u * u) : Mathf.Lerp(0.2f, 1, Out01(u));
                f.rt.sizeDelta = new Vector2(size * s, size * s * 0.8f) * K;
                f.cg.alpha = contract ? Mathf.Min(1, u / 0.2f) * (u > 0.85f ? (1 - u) / 0.15f : 1) : u < 0.4f ? 1 : 1 - (u - 0.4f) / 0.6f;
            });
        }

        // vòng dẹt dưới chân: bề ngang từ d0 tới d1 (d0 > d1 là co lại), mờ ở 30% cuối
        void FloorRing(Vector2 feet, Color c, float d0, float d1, float delay, float life)
        {
            if (!ringFx) return;
            var item = Take(ringFx);
            item.Image.color = c;
            var rt = item.Rect;
            rt.anchoredPosition = P(feet);
            AddFx(item, ringFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life, w = Mathf.Lerp(d0, d1, d1 > d0 ? Out01(u) : u * u);
                f.rt.sizeDelta = new Vector2(w, w * 0.3f) * K;
                f.cg.alpha = u < 0.7f ? Mathf.Min(1, u / 0.1f) : 1 - (u - 0.7f) / 0.3f;
            });
        }

        // bụi tròn nhạt ở chân (chạm đất): vòng dẹt và vài cụm bụi lăn ra hai bên, nằm sau tướng
        void Dust(int side, float scale)
        {
            var a = actors[side];
            float H = a != null ? a.H : Height[side];
            var feet = Pos[side];
            FloorRing(feet, new Color(0.9f, 0.85f, 0.74f, 0.9f), H * 0.3f, H * 1.1f * scale, 0, 0.4f);
            var h = Hat;
            if (h == null) return;
            for (int i = 0; i < 4; i++)
            {
                float dir = i % 2 == 0 ? -1 : 1;
                var p = h.Smoke(feet + new Vector2(dir * Random.Range(0.1f, 0.35f) * H, -2), new Vector2(dir * Random.Range(40f, 90f), -Random.Range(10f, 30f)),
                    Random.Range(0.5f, 0.75f), 4, Random.Range(9f, 14f) * scale, HatLua.Back, "dark", 0);
                p.stops = DustStops;
            }
        }

        // n hạt màu c bay lên quanh thân bên side, rải trong spread giây (hạt chồng lớp nếu có, không thì vệt sáng nhỏ của sân)
        void Motes(int side, Color c, int n, float spread, Vector2 shift = default)
        {
            var a = actors[side];
            float H = a != null ? a.H : Height[side];
            var feet = Pos[side] + shift;
            var h = Hat;
            for (int i = 0; i < n; i++)
            {
                var at = feet + new Vector2(Random.Range(-0.4f, 0.4f) * H, -Random.Range(0.1f, 0.8f) * H);
                float delay = Random.value * spread;
                var vel = new Vector2(Random.Range(-20f, 20f), -Random.Range(60f, 110f));
                float life = Random.Range(0.7f, 1.1f), size = Random.Range(6f, 10f);
                if (h != null)
                    h.At(delay, () =>
                    {
                        var p = h.Ember(at, vel, life, size, HatLua.Front);
                        p.col = c;
                    });
                else Rise(at, c, delay, life, size);
            }
        }

        // vệt sáng nhỏ đứng thẳng trôi lên rồi mờ (thay hạt chồng lớp khi sân chưa có lớp hạt)
        void Rise(Vector2 at, Color c, float delay, float life, float size)
        {
            if (!sparkFx) return;
            var item = Take(sparkFx);
            item.Image.color = c;
            var rt = item.Rect;
            rt.localEulerAngles = new Vector3(0, 0, 90);
            rt.anchoredPosition = P(at);
            float up = Random.Range(50f, 80f);
            AddFx(item, sparkFx, delay + life, (f, k) =>
            {
                float t = k * (delay + life) - delay;
                if (t < 0)
                {
                    f.cg.alpha = 0;
                    return;
                }
                float u = t / life;
                f.rt.anchoredPosition = P(at - new Vector2(0, up * Out01(u)));
                f.rt.sizeDelta = new Vector2(size * 1.6f * K, size * 0.6f * (1 - 0.5f * u) * K);
                f.cg.alpha = Mathf.Min(1, u / 0.15f) * (u > 0.6f ? (1 - u) / 0.4f : 1);
            });
        }
    }
}
