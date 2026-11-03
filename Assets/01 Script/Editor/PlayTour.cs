// Thử nhanh khi đang Play từ Boot: đi Hub → mọi scene con → quay lại, mở hộp thoại và thông báo, thử xếp hàng chuyển scene,
// rồi chụp Game view ở 3 khung (1080×1920, 1080×2400, 1536×2048) vào thư mục Temp/PokiShots của project (không vào Assets).
using System.Collections;
using System.IO;
using System.Linq;
using PokiClash.Core;
using PokiClash.UI;
using Progress = PokiClash.Core.Progress;
using Object = UnityEngine.Object;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class PlayTour
    {
        public static string ShotDir => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/PokiShots"));
        static int shot;

        // Chụp đứng hình: tắt nét rung đúng lúc chụp, để so ảnh trước và sau một thay đổi theo từng điểm ảnh.
        const string StillMenu = "PokiClash/Thử/Chụp đứng hình (tắt nét rung khi chụp)";

        static bool Still
        {
            get => EditorPrefs.GetBool("PokiClash.ShotStill", false);
            set => EditorPrefs.SetBool("PokiClash.ShotStill", value);
        }

        [MenuItem(StillMenu, priority = 99)]
        static void ToggleStill()
        {
            Still = !Still;
            Menu.SetChecked(StillMenu, Still);
        }

        [MenuItem(StillMenu, true)]
        static bool ToggleStillCheck()
        {
            Menu.SetChecked(StillMenu, Still);
            return true;
        }

        // Chụp các hộp thoại mà các vòng thử chưa chụp tới (ảnh "x_<tên>.png" trong cùng thư mục, không đổi số thứ tự ảnh khác).
        [MenuItem("PokiClash/Thử/Chụp hộp thoại phụ (đang Play)", priority = 99)]
        static void TryExtra()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunExtra());
        }

        static IEnumerator RunExtra()
        {
            // Sổ thẻ: chi tiết thẻ chưa mở (thẻ cuối) và thẻ đã mở (thẻ đầu)
            yield return Go(SceneIds.Cards);
            var cards = Object.FindObjectsByType<UiCard>(FindObjectsSortMode.None).OrderBy(c => c.transform.GetSiblingIndex()).ToList();
            foreach (var (card, tag) in new[] { (cards.First(), "the_dau"), (cards.Last(), "the_cuoi") })
            {
                card.OnPointerClick(null);
                yield return new WaitForSecondsRealtime(0.6f);
                yield return ExtraShot("chi_tiet_" + tag);
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.3f);
            }
            yield return Go(SceneIds.Hub);
            Debug.Log($"[Thử] Xong hộp thoại phụ: {ShotDir}");
        }

        static IEnumerator ExtraShot(string name)
        {
            bool still = Still;
            if (still)
            {
                Theme.SetBoil(false);
                yield return null;
            }
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(ShotDir, $"x_{name}_{tex.width}x{tex.height}.png"), tex.EncodeToPNG());
            Object.Destroy(tex);
            if (still) App.ApplySettings();
        }

        [MenuItem("PokiClash/Thử/Đi một vòng các scene (đang Play)", priority = 100)]
        static void Tour()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Run());
        }

        [MenuItem("PokiClash/Thử/Chụp 3 khung màn hình (đang Play)", priority = 101)]
        static void Frames()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunFrames());
        }

        [MenuItem("PokiClash/Thử/Đánh thử ải 1 (đang Play)", priority = 102)]
        static void TryBattle()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunBattle(1, false)));
        }

        [MenuItem("PokiClash/Thử/Đánh thử boss Đảo Thủy (ải 70), đội 3 tướng (đang Play)", priority = 104)]
        static void TryBattle8()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunBattle(Islands.Size(Elem.Thuy), true)));
        }

        [MenuItem("PokiClash/Thử/Đánh thử ải 7, đội 3 tướng (đang Play)", priority = 103)]
        static void TryBattle7()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunBattle(7, true)));
        }

        [MenuItem("PokiClash/Thử/Boss tiến hóa: đảo Thủy, hộp chuẩn bị, trận ải cuối (đang Play)", priority = 105)]
        static void TryBossEvo()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunBossEvo()));
        }

        // Ải cuối Đảo Thủy (boss một mình, dòng 3 dạng): chụp đảo (tướng trên nút ải), hộp chuẩn bị (các dạng), rồi mỗi lần boss lên
        // dạng thì chụp liền lúc tên dạng mới hiện ra (logic tính trước cả lượt, nên canh chữ trên màn chứ không canh f.form)
        static IEnumerator RunBossEvo()
        {
            shot = 180;
            var sv = App.Save.Data;
            foreach (var id in new[] { "giot_suong", "vo_su", "nu_hoa" }) sv.Hero(id).owned = true;
            sv.team = new System.Collections.Generic.List<string> { "giot_suong", "vo_su", "nu_hoa" };
            sv.level = 10;
            sv.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy) - 1;
            App.Save.Save();
            yield return Go(SceneIds.Zone, Elem.Thuy);
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot("dao_thuy_truoc_boss");
            StagePrep.Open(App.Data.Stages.First(st => st.zone == Elem.Thuy && st.idx == Islands.Size(Elem.Thuy)).id);
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("chuan_bi_boss");
            App.Modals.CloseAll();
            yield return Go(SceneIds.Battle, new BattleArgs { stageId = 8 });
            var ctl = Object.FindAnyObjectByType<BattleController>();
            if (!ctl)
            {
                Debug.LogError("[Thử] Không thấy BattleController");
                yield break;
            }
            var boss = ctl.Battle.sides[1].fighters[0];
            yield return new WaitForSecondsRealtime(1.5f);
            yield return Shot("boss_dang1");
            ctl.SetAuto(true);
            ctl.SetSpeed(3);
            int seen = 0;
            float t0 = Time.realtimeSinceStartup;
            while (ctl.Battle.phase != Phase.Over || seen < boss.form)
            {
                if (Time.realtimeSinceStartup - t0 > 240) break;
                if (seen < boss.form)
                {
                    string next = boss.hero.forms[seen + 1].name;
                    if (Object.FindObjectsByType<TMPro.TextMeshProUGUI>(FindObjectsSortMode.None).Any(t => t.isActiveAndEnabled && t.text == next))
                    {
                        seen++;
                        yield return Shot($"tien_hoa_{seen}_a");
                        yield return new WaitForSecondsRealtime(0.25f);
                        yield return Shot($"tien_hoa_{seen}_b");
                        continue;
                    }
                }
                yield return null;
            }
            Debug.Log($"[Thử] Boss tiến hóa: {(ctl.Battle.winner == 0 ? "thắng" : "thua")} sau {ctl.Battle.round} hiệp; boss lên {boss.form} lần " +
                      $"(thấy trên màn {seen}), máu tối đa dạng cuối {boss.maxHp:0}");
            yield return Until(() => App.Modals.Count > 0, 30);
            yield return new WaitForSecondsRealtime(1.2f);
            yield return Shot("boss_ket_qua");
            Debug.Log($"[Thử] Xong boss tiến hóa: ảnh trong {ShotDir}");
        }

        [MenuItem("PokiClash/Thử/Sàn đấu đảo Thủy: chụp nền từng chặng, mini boss, boss (đang Play)", priority = 106)]
        static void TryArenas()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunArenas()));
        }

        // Mỗi sàn đấu một trận (ArtGen/BattleBG/build_thuy.py): chụp lúc chờ chọn thẻ, rồi 0,8 s sau (phần động đã đổi chỗ)
        static IEnumerator RunArenas()
        {
            shot = 400;
            foreach (int idx in new[] { 1, 5, 10, 15, 20, 25, 30, 40, 50, 60, 65, 70 })
            {
                var st = App.Data.Stages.FirstOrDefault(s => s.zone == Elem.Thuy && s.idx == idx);
                if (st == null) continue;
                yield return Go(SceneIds.Battle, new BattleArgs { stageId = st.id });
                var ctl = Object.FindAnyObjectByType<BattleController>();
                if (ctl) yield return Until(() => ctl.WaitingPlayer, 30);
                yield return new WaitForSecondsRealtime(0.5f);
                yield return Shot($"san_dau_{idx:00}");
                yield return new WaitForSecondsRealtime(0.8f);
                yield return Shot($"san_dau_{idx:00}_b");
            }
            yield return Go(SceneIds.Hub);
            Debug.Log($"[Thử] Xong sàn đấu đảo Thủy: ảnh trong {ShotDir}");
        }

        [MenuItem("PokiClash/Thử/Trận nhiều địch: mặt địch góc trên, dấu X tướng gục (đang Play)", priority = 107)]
        static void TryFoeRow()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunFoeRow()));
        }

        [MenuItem("PokiClash/Thử/Sàn đấu boss ải 70: nền đổi theo dạng tiến hóa (đang Play)", priority = 108)]
        static void TryBossArena()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunBossArena()));
        }

        // Ải 70 đảo Thủy, đội 3 tướng cấp 10, tự đánh: chụp đầu trận, rồi mỗi lần tên dạng mới của boss hiện trên màn (nền vừa đổi
        // trong chớp trắng) chụp 2 ảnh cách 1,2 s (thấy mưa, xoáy quay nhanh hơn).
        static IEnumerator RunBossArena()
        {
            shot = 470;
            var st = App.Data.Stages.FirstOrDefault(s => s.zone == Elem.Thuy && s.idx == Islands.Size(Elem.Thuy));
            if (st == null) yield break;
            var sv = App.Save.Data;
            foreach (var id in new[] { "giot_suong", "vo_su", "nu_hoa" }) sv.Hero(id).owned = true;
            sv.team = new System.Collections.Generic.List<string> { "giot_suong", "vo_su", "nu_hoa" };
            sv.level = 10;
            yield return Go(SceneIds.Battle, new BattleArgs { stageId = st.id });
            var ctl = Object.FindAnyObjectByType<BattleController>();
            if (!ctl) yield break;
            var boss = ctl.Battle.sides[1].fighters[0];
            yield return Until(() => ctl.WaitingPlayer, 30);
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot("boss70_dang1");
            ctl.SetAuto(true);
            ctl.SetSpeed(3);
            int seen = 0;
            float t0 = Time.realtimeSinceStartup;
            while (Time.realtimeSinceStartup - t0 < 240 && (ctl.Battle.phase != Phase.Over || seen < boss.form))
            {
                if (seen < boss.form && seen + 1 < boss.hero.forms.Length)
                {
                    string next = boss.hero.forms[seen + 1].name;
                    if (Object.FindObjectsByType<TMPro.TextMeshProUGUI>(FindObjectsSortMode.None).Any(t => t.isActiveAndEnabled && t.text == next))
                    {
                        seen++;
                        yield return new WaitForSecondsRealtime(0.4f);
                        yield return Shot($"boss70_dang{seen + 1}");
                        yield return new WaitForSecondsRealtime(1.2f);
                        yield return Shot($"boss70_dang{seen + 1}_b");
                        continue;
                    }
                }
                yield return null;
            }
            yield return Until(() => App.Modals.Count > 0, 30);
            Debug.Log($"[Thử] Xong sàn đấu boss ải 70: boss lên {boss.form} lần, thấy trên màn {seen}; " +
                      $"{(ctl.Battle.winner == 0 ? "thắng" : "thua")}; ảnh trong {ShotDir}");
            yield return Go(SceneIds.Hub);
        }

        // Ải Thủy đầu tiên từ ải 20 có 3 địch, đội mình 3 tướng cấp vừa: hai bên đều có tướng gục. Tự đánh, 3 s chụp một ảnh.
        static IEnumerator RunFoeRow()
        {
            shot = 440;
            var st = App.Data.Stages.FirstOrDefault(s => s.zone == Elem.Thuy && s.idx >= 20 && s.enemies.Count >= 3);
            if (st == null)
            {
                Debug.LogError("[Thử] Không có ải 3 địch");
                yield break;
            }
            var sv = App.Save.Data;
            foreach (var id in new[] { "giot_suong", "vo_su", "nu_hoa" }) sv.Hero(id).owned = true;
            sv.team = new System.Collections.Generic.List<string> { "giot_suong", "vo_su", "nu_hoa" };
            sv.level = 4;
            yield return Go(SceneIds.Battle, new BattleArgs { stageId = st.id });
            var ctl = Object.FindAnyObjectByType<BattleController>();
            if (!ctl) yield break;
            yield return Until(() => ctl.WaitingPlayer, 30);
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot($"nhieu_dich_ai{st.idx}_dau");
            ctl.SetAuto(true);
            ctl.SetSpeed(2);
            float t0 = Time.realtimeSinceStartup;
            for (int k = 0; k < 14 && ctl.Battle.phase != Phase.Over && Time.realtimeSinceStartup - t0 < 120; k++)
            {
                yield return new WaitForSecondsRealtime(3f);
                yield return Shot($"nhieu_dich_ai{st.idx}_{k:00}");
            }
            yield return Until(() => App.Modals.Count > 0, 60);
            Debug.Log($"[Thử] Xong trận nhiều địch (ải {st.idx}, {st.enemies.Count} địch): " +
                      $"{(ctl.Battle.winner == 0 ? "thắng" : "thua")}; ảnh trong {ShotDir}");
            yield return Go(SceneIds.Hub);
        }

        // Chạy lần lượt mọi menu thử (trừ "Người chơi mới đi trọn Đảo Thủy" vì lâu), ảnh dồn vào một thư mục, đánh số liên tiếp.
        // Dùng để so ảnh trước và sau một thay đổi lớn (bật "Chụp đứng hình" trước).
        [MenuItem("PokiClash/Thử/Chạy mọi menu thử, chụp ảnh (đang Play)", priority = 98)]
        static void TryAll()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(RunAll());
        }

        static IEnumerator RunAll()
        {
            float t0 = Time.realtimeSinceStartup;
            yield return Run();
            yield return WithSaveBackup(RunBattle(1, false));
            yield return WithSaveBackup(RunBattle(7, true));
            yield return WithSaveBackup(RunBattle(8, true));
            yield return WithSaveBackup(RunHeroes());
            yield return WithSaveBackup(RunMachine());
            yield return WithSaveBackup(RunAfk());
            yield return WithSaveBackup(RunDevTools());
            yield return WithSaveBackup(RunBadges());
            yield return WithSaveBackup(RunPotential());
            yield return WithSaveBackup(RunFarm());
            yield return WithSaveBackup(RunPacks());
            yield return WithSaveBackup(RunMapShots());
            yield return RunFrames();
            Debug.Log($"[Thử] Xong mọi menu thử: {shot} ảnh trong {ShotDir} ({Time.realtimeSinceStartup - t0:0} giây)");
        }

        // giữ bản lưu trước khi thử, xong thì trả lại (thử không làm đổi tiến trình)
        static IEnumerator WithSaveBackup(IEnumerator inner)
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            yield return inner;
            if (backup != null)
            {
                File.WriteAllText(path, backup);
                App.Save.Load();
                App.Bars.Refresh();
                Debug.Log("[Thử] Đã trả lại bản lưu như trước khi thử.");
            }
        }

        [MenuItem("PokiClash/Thử/Tướng: nâng thẻ, tiến hóa (đang Play)", priority = 110)]
        static void TryHeroes()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunHeroes()));
        }

        // bấm nút có chữ (in hoa) trong lớp hộp thoại
        static bool ClickButton(string label)
        {
            foreach (var b in Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None))
                if (b.Label && b.Label.text == label.ToUpperInvariant() && b.isActiveAndEnabled)
                {
                    b.SimulateClick();
                    return true;
                }
            Debug.LogWarning($"[Thử] Không thấy nút '{label}'");
            return false;
        }

        static IEnumerator RunHeroes()
        {
            shot = 60;
            var s = App.Save.Data;
            var d = App.Data;
            yield return Go(SceneIds.Notebook);
            yield return Shot("so_tay_bang_thu");
            ClickButton("+500 XP");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("len_cap");
            App.Modals.CloseAll();
            ClickButton("+5 bản sao");
            Progress.UnlockHero(s, "vo_su");
            Progress.UnlockHero(s, "giot_suong"); // bản lưu trước v4 có Tiểu Y khởi đầu, chưa có Giọt Sương
            App.Save.Save();
            yield return Go(SceneIds.Hub);
            yield return Shot("sanh_viec_cho");
            yield return Go(SceneIds.Heroes);
            yield return Shot("tuong_luoi");
            HeroDetail.Open("giot_suong");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("tuong_chi_tiet");
            ClickButton("Lên cấp 2");
            yield return new WaitForSecondsRealtime(0.4f);
            ClickButton("Lên cấp 2");
            yield return new WaitForSecondsRealtime(0.4f);
            ClickButton("Lên cấp 2");
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot("tuong_nang_the");
            ClickButton("Tiến hóa");
            yield return new WaitForSecondsRealtime(0.35f);
            yield return Shot("tuong_tien_hoa");
            var p = s.Hero("giot_suong");
            Debug.Log($"[Thử] Giọt Sương: thẻ {p.skill.lv}/{p.ult.lv}/{p.passive.lv}, sao {p.star}, cấp người chơi {s.level}");
            // chỉ số trong trận phải khớp màn Tướng
            var st = HeroStats.Compute(d.Cfg, d.Hero("giot_suong"), s.level, p.star);
            var b = Battle.Create(d, Teams.Player(s), Teams.Enemy(d.Stage(1), d), 1);
            var f = b.ActiveOf(0);
            bool same = f.maxHp == st.hp && f.atk == st.atk && f.def == st.def && f.spd == st.spd;
            if (same) Debug.Log($"[Thử] Chỉ số trong trận khớp màn Tướng: máu {st.hp}, công {st.atk}, thủ {st.def}, tốc {st.spd}");
            else Debug.LogError($"[Thử] Lệch chỉ số: màn Tướng {st.hp}/{st.atk}/{st.def}, trận {f.maxHp}/{f.atk}/{f.def}");
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.3f);
            HeroDetail.Open("huyen_vu");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("tuong_chua_co");
            App.Modals.CloseAll();
            yield return Go(SceneIds.Cards);
            yield return Shot("so_the");
            yield return Go(SceneIds.Hub);
            Debug.Log("[Thử] Xong vòng Tướng.");
        }

        [MenuItem("PokiClash/Thử/Máy bi: thả ×1 và ×3, mở rương (đang Play)", priority = 111)]
        static void TryMachine()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunMachine()));
        }

        // đóng lần lượt mọi hộp (rương, Huyền thoại, lên cấp) tới khi máy rảnh; chụp vài hộp đầu
        static IEnumerator SettleMachine(MachineScene m, string tag, int shots, bool log = true)
        {
            float t0 = Time.realtimeSinceStartup;
            int boxes = 0;
            while ((!m.Idle || App.Modals.Count > 0) && Time.realtimeSinceStartup - t0 < 90)
            {
                if (App.Modals.Count > 0)
                {
                    yield return new WaitForSecondsRealtime(1.1f);
                    if (boxes < shots) yield return Shot($"{tag}_hop{boxes}");
                    boxes++;
                    App.Modals.Back();
                    yield return new WaitForSecondsRealtime(0.3f);
                }
                yield return null;
            }
            if (log) Debug.Log($"[Thử] {tag}: đóng {boxes} hộp; cấp {App.Save.Data.level}, {App.Save.Data.balls} bi, đã tiêu {App.Save.Data.ballsSpent}, rương chờ {App.Save.Data.chests.Count}");
        }

        static IEnumerator RunMachine()
        {
            shot = 80;
            var s = App.Save.Data;
            var d = App.Data;
            foreach (var id in new[] { "giot_suong", "vo_su", "nu_hoa" }) s.Hero(id).owned = true;
            s.level = 5;
            s.exp = Progress.ExpToNext(5, App.Data.Cfg) - 40;
            s.balls = 400;
            s.ballsSpent = 270;
            s.legendDone = false;
            s.chests.Clear();
            s.chests.Add(new PendingChest { kind = "chest_silver", x = 1 });
            App.Save.Save();
            yield return Go(SceneIds.Machine);
            var m = Object.FindAnyObjectByType<MachineScene>();
            if (!m)
            {
                Debug.LogError("[Thử] Không thấy MachineScene");
                yield break;
            }
            yield return Shot("may_bi");
            ClickButton("Tỉ lệ");
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("ti_le");
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.3f);
            ClickButton("×1");
            int spent = s.ballsSpent;
            ClickButton("Thả liền 20");
            yield return new WaitForSecondsRealtime(1.6f);
            yield return Shot("tha_x1");
            yield return Until(() => m.Session >= 20, 10);
            Debug.Log($"[Thử] ×1: thả {m.Session} bi, tốn {s.ballsSpent - spent}");
            yield return SettleMachine(m, "x1", 3);

            ClickButton("×3");
            spent = s.ballsSpent;
            ClickButton("Thả liền 20");
            yield return new WaitForSecondsRealtime(1.6f);
            yield return Shot("tha_x3");
            yield return Until(() => m.Session >= 20, 10);
            Debug.Log($"[Thử] ×3: thả {m.Session} lần, tốn {s.ballsSpent - spent} bi; Cà Sa {(s.Hero(d.LegendMilestoneHero).owned ? "đã có" : "chưa có")}");
            yield return SettleMachine(m, "x3", 9);
            yield return Shot("sau_x3");

            // 3 rương vàng ×10 trong khay: chạm khay để mở (nửa số lần ra 30 thẻ, gộp bản sao)
            for (int i = 0; i < 3; i++) s.chests.Add(new PendingChest { kind = "chest_gold", x = 10 });
            App.Save.Save();
            yield return new WaitForSecondsRealtime(0.3f);
            GameObject.Find("khay_chest_gold").GetComponent<SketchButton>().SimulateClick();
            yield return SettleMachine(m, "khay", 3);

            // rời máy khi bi còn lăn: mỗi bi tính như ô giữa
            ClickButton("Thả liền 20");
            yield return new WaitForSecondsRealtime(1.2f);
            int rolling = Object.FindAnyObjectByType<MachineBoard>().Board.balls.Count;
            int lv = s.level, exp = s.exp;
            yield return Go(SceneIds.Hub);
            Debug.Log($"[Thử] Rời máy khi {rolling} bi ×3 đang lăn: cấp {lv}→{s.level}, EXP {exp}→{s.exp}; rương chờ giữ lại {s.chests.Count}");
            yield return Shot("sanh_sau_may");
            Debug.Log($"[Thử] Xong máy bi: ảnh trong {ShotDir}");
        }

        [MenuItem("PokiClash/Thử/AFK và cây bi: tua giờ, hái, mảnh, rương, tăng tốc (đang Play)", priority = 112)]
        static void TryAfk()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunAfk()));
        }

        static bool ClickByName(string name)
        {
            // GameObject.Find không thấy đối tượng dưới App (DontDestroyOnLoad): tìm theo SketchButton
            var b = Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).FirstOrDefault(x => x.name == name && x.isActiveAndEnabled);
            if (b == null)
            {
                Debug.LogWarning($"[Thử] Không thấy nút '{name}'");
                return false;
            }
            b.SimulateClick();
            return true;
        }

        static IEnumerator RunAfk()
        {
            shot = 110;
            const double H = 3600000;
            var s = App.Save.Data;
            s.zones = new int[5];
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            s.zones[(int)Elem.Hoa] = 2; // xong Thủy, 2 ải Hỏa: 2 cây bi
            double now = PokiClash.Game.SaveService.Now();
            s.afk = new AfkState { lastTick = now };
            s.afkSince = (long)now;
            s.trees = null;
            s.ads = null;
            s.ent = null;
            Trees.Tick(s, App.Data.Cfg, now);
            s.intro = true;
            App.Save.Save();
            yield return Go(SceneIds.Hub);

            Afk.Travel(s, 0.5 * H);
            Trees.Travel(s, 0.5 * H);
            App.Bars.Refresh();
            yield return Shot("sanh_afk_30phut");
            Afk.Travel(s, 0.5 * H);
            Trees.Travel(s, 0.5 * H);
            App.OpenAfk();
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("afk_1gio");
            int b0 = s.balls;
            ClickButton("Nhận mảnh");
            yield return new WaitForSecondsRealtime(0.5f);
            Debug.Log($"[Thử] AFK 1 giờ, nhận mảnh: bi không đổi {s.balls - b0 == 0}, giờ AFK còn {s.afk.hours}");

            Afk.Travel(s, 8 * H);
            Trees.Travel(s, 8 * H);
            App.Router.CurrentRoot.Refresh();
            App.Bars.Refresh();
            yield return new WaitForSecondsRealtime(0.4f);
            yield return Shot("sanh_cay_bi");
            ClickNamed("cay_bi");
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("cay_bi_9gio");
            b0 = s.balls;
            int ripe = Trees.Stock(s, App.Data.Cfg, PokiClash.Game.SaveService.Now());
            ClickByName("cay_hai_x2");
            yield return new WaitForSecondsRealtime(1.2f);
            yield return Shot("quang_cao_gia");
            ClickButton("Bỏ qua");
            yield return new WaitForSecondsRealtime(0.5f);
            Debug.Log($"[Thử] Cây bi 9 giờ (2 cây): {ripe} bi (đợi 90); bỏ quảng cáo giữa chừng: +{s.balls - b0} bi (đợi 0)");
            ClickByName("cay_hai_x2");
            yield return new WaitForSecondsRealtime(3.8f);
            yield return Shot("cay_bi_da_hai");
            Debug.Log($"[Thử] Hái ×2 xem hết quảng cáo: +{s.balls - b0} bi (đợi 180), lượt tree_double còn {AdGate.Left(s, App.Data.Cfg, Afk.Today(PokiClash.Game.SaveService.Now()), AdGate.TreeDouble)}");
            App.Modals.CloseAll();

            Afk.Travel(s, 14 * H);
            App.Bars.Refresh();
            yield return new WaitForSecondsRealtime(0.3f);
            yield return Shot("sanh_afk_day");
            App.OpenAfk();
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("afk_day_khay");
            Debug.Log($"[Thử] AFK 22 giờ: {s.afk.hours} giờ, {s.afk.chests.Count} rương, mở được {Afk.ReadyChests(s, App.Data.Cfg, PokiClash.Game.SaveService.Now())}");
            int lv = s.level, exp = s.exp, opened = 0;
            // mở hết rương đã tới giờ (rương đầu khay trước); mở xong khi khay đầy thì rương mới vào khay và bắt đầu đếm
            while (Afk.ReadyChests(s, App.Data.Cfg, PokiClash.Game.SaveService.Now()) > 0 && opened < 6)
            {
                ClickByName("afk_ruong_0");
                yield return new WaitForSecondsRealtime(1.3f);
                if (opened++ == 0) yield return Shot("ruong_afk");
                while (App.Modals.Count > 1)
                {
                    App.Modals.Back();
                    yield return new WaitForSecondsRealtime(0.4f);
                }
                yield return new WaitForSecondsRealtime(0.6f);
            }
            yield return Shot("afk_sau_mo");
            Debug.Log($"[Thử] Mở {opened} rương AFK: còn {s.afk.chests.Count} (đang đếm); cấp {lv}→{s.level}, EXP {exp}→{s.exp}");

            if (ClickByName("afk_mo_ngay"))
            {
                yield return new WaitForSecondsRealtime(4.6f);
                yield return Shot("mo_ngay");
                while (App.Modals.Count > 1)
                {
                    App.Modals.Back();
                    yield return new WaitForSecondsRealtime(0.4f);
                }
            }
            ClickButton("Nhận mảnh");
            yield return new WaitForSecondsRealtime(0.5f);
            App.OpenAfk();
            yield return new WaitForSecondsRealtime(0.6f);
            ClickByName("afk_tang_toc");
            yield return new WaitForSecondsRealtime(4.2f);
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("tang_toc");
            Debug.Log($"[Thử] Sau mở ngay và tăng tốc: rương {s.afk.chests.Count}, lượt mở ngay đã dùng {AdGate.Used(s, Afk.Today(PokiClash.Game.SaveService.Now()), AdGate.AfkChestOpen)}, tăng tốc còn {(s.afk.boostUntil - PokiClash.Game.SaveService.Now()) / H:0.00} giờ");
            App.Modals.CloseAll();
            Debug.Log("[Thử] Xong AFK.");
        }

        [MenuItem("PokiClash/Thử/Sổ tay bản dev: chỉnh số, máy tự chơi, ghi trận (đang Play)", priority = 113)]
        static void TryDevTools()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunDevTools()));
        }

        static IEnumerator RunDevTools()
        {
            shot = 130;
            var s = App.Save.Data;
            s.intro = true;
            App.Save.Save();
            yield return Go(SceneIds.Notebook);
            var sr = Object.FindAnyObjectByType<UnityEngine.UI.ScrollRect>();
            yield return Shot("so_tay_dau");
            sr.verticalNormalizedPosition = 0.45f;
            yield return new WaitForSecondsRealtime(0.3f);
            yield return Shot("so_tay_chinh_so");
            int mana0 = App.Data.Cfg.manaPerTurn;
            ClickByName("them_manaPerTurn");
            ClickByName("them_manaPerTurn");
            Debug.Log($"[Thử] Chỉnh số: mana mỗi lượt {mana0} → {App.Data.Cfg.manaPerTurn}");
            sr.verticalNormalizedPosition = 0f;
            yield return new WaitForSecondsRealtime(0.3f);
            float t0 = Time.realtimeSinceStartup;
            ClickByName("may_tu_choi");
            Debug.Log($"[Thử] Máy tự chơi 100 trận: {Object.FindObjectsByType<TMPro.TextMeshProUGUI>(FindObjectsSortMode.None).FirstOrDefault(t => t.text.StartsWith("Thắng"))?.text} ({Time.realtimeSinceStartup - t0:0.00} giây)");
            yield return new WaitForSecondsRealtime(0.3f);
            yield return Shot("so_tay_may_tu_choi");

            // trận với mana mỗi lượt đã chỉnh, tự chơi ×3; xong thì Logs/tran.csv có dòng mới
            var log = BattleLog.FilePath;
            int before = File.Exists(log) ? File.ReadAllLines(log).Length : 0;
            yield return Go(SceneIds.Battle, new BattleArgs { stageId = 1 });
            var ctl = Object.FindAnyObjectByType<BattleController>();
            yield return Until(() => ctl.WaitingPlayer, 30);
            Debug.Log($"[Thử] Đầu lượt 1, mana tướng ra trận: {ctl.Battle.ActiveOf(0).mana} (đợi {App.Data.Cfg.manaPerTurn})");
            ctl.SetSpeed(3);
            ctl.SetAuto(true);
            yield return Until(() => ctl.Battle.phase == Phase.Over, 120);
            yield return Until(() => App.Modals.Count > 0, 10);
            yield return new WaitForSecondsRealtime(0.5f);
            var lines = File.Exists(log) ? File.ReadAllLines(log) : new string[0];
            Debug.Log($"[Thử] Ghi trận: {lines.Length - before} dòng mới trong {log}: {lines.LastOrDefault()}");
            App.Modals.CloseAll();
            yield return Go(SceneIds.Notebook);
            Object.FindAnyObjectByType<UnityEngine.UI.ScrollRect>().verticalNormalizedPosition = 0.3f;
            yield return new WaitForSecondsRealtime(0.2f);
            ClickButton("Về số gốc");
            Debug.Log($"[Thử] Về số gốc: mana mỗi lượt {App.Data.Cfg.manaPerTurn}");
            yield return Go(SceneIds.Hub);
            Debug.Log("[Thử] Xong Sổ tay bản dev.");
        }

        [MenuItem("PokiClash/Thử/Đền Huy Hiệu: đánh trọn bậc Đồng hệ Thủy (đang Play)", priority = 114)]
        static void TryBadges()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunBadges()));
        }

        static IEnumerator RunBadges()
        {
            shot = 140;
            var s = App.Save.Data;
            var d = App.Data;
            s.intro = true;
            s.zones = new int[5];
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            s.zones[(int)Elem.Hoa] = 4;
            foreach (var bp in s.badges)
            {
                bp.tier = 0;
                bp.won = 0;
            }
            foreach (var id in new[] { "giot_suong", "vo_su", "nu_hoa", "ca_ngua" }) s.Hero(id).owned = true;
            s.level = 9;
            s.team = new System.Collections.Generic.List<string> { "vo_su", "nu_hoa", "ca_ngua" };
            App.Save.Save();
            var ty = d.Hero("giot_suong");
            var before = HeroStats.Compute(d.Cfg, ty, s.level, s.Hero("giot_suong").star, false, Badges.Mods(s, d.Cfg, ty.elem));

            yield return Go(SceneIds.Hub);
            yield return Shot("sanh_den_mo");
            yield return Go(SceneIds.Badges);
            yield return Shot("den_huy_hieu");
            ClickByName("thu_thach_thuy");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("den_danh_sach");
            ClickByName("danh_tran");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("den_chuan_bi");
            ClickButton("Xuất trận!");
            int fights = 0, wins = 0;
            while (s.badges[(int)Elem.Thuy].tier < 1 && fights < 14)
            {
                yield return WaitScene(SceneIds.Battle);
                var ctl = Object.FindAnyObjectByType<BattleController>();
                ctl.SetSpeed(3);
                ctl.SetAuto(true);
                yield return Until(() => ctl.Battle.phase == Phase.Over, 180);
                bool win = ctl.Battle.winner == 0;
                fights++;
                if (win) wins++;
                yield return Until(() => App.Modals.Count > 0, 10);
                yield return new WaitForSecondsRealtime(0.9f);
                if (fights == 1) yield return Shot("den_ket_qua");
                if (s.badges[(int)Elem.Thuy].tier >= 1) break;
                if (!ClickButton(win ? "Trận tiếp »" : "Đánh lại")) break;
            }
            Debug.Log($"[Thử] Đền: {fights} trận, thắng {wins}; Thủy bậc {s.badges[(int)Elem.Thuy].tier}, {s.balls} bi");
            // hộp huy hiệu rồi rương
            yield return Until(() => Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).Any(b => b.name == "mo_ruong_huy_hieu"), 5);
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("den_huy_hieu_dong");
            ClickByName("mo_ruong_huy_hieu");
            yield return new WaitForSecondsRealtime(1.4f);
            yield return Shot("den_ruong");
            ClickButton("Nhận");
            yield return new WaitForSecondsRealtime(0.5f);
            App.Modals.CloseAll();
            var after = HeroStats.Compute(d.Cfg, ty, s.level, s.Hero("giot_suong").star, false, Badges.Mods(s, d.Cfg, ty.elem));
            Debug.Log($"[Thử] Giọt Sương: máu {before.hp}→{after.hp} ({after.hp / before.hp - 1:P1}), công {before.atk}→{after.atk}, thủ {before.def}→{after.def}");
            yield return Go(SceneIds.Badges);
            yield return Shot("den_sau_dong");
            yield return Go(SceneIds.Heroes);
            yield return Shot("tuong_co_huy_hieu");
            HeroDetail.Open("giot_suong");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("tieu_y_huy_hieu");
            App.Modals.CloseAll();
            yield return Go(SceneIds.Hub);
            Debug.Log("[Thử] Xong Đền Huy Hiệu.");
        }

        [MenuItem("PokiClash/Thử/Tiềm năng: đá từ máy bi, khai phá, Hang (đang Play)", priority = 115)]
        static void TryPotential()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunPotential()));
        }

        static IEnumerator RunPotential()
        {
            shot = 160;
            var s = App.Save.Data;
            var d = App.Data;
            s.intro = true;
            s.zones = new int[5];
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            s.zones[(int)Elem.Hoa] = 4;
            foreach (var id in new[] { "giot_suong", "vo_su", "nu_hoa", "ca_ngua" }) s.Hero(id).owned = true;
            s.level = 9;
            s.Hero("giot_suong").star = 3;
            s.Hero("giot_suong").potential = new PotLine[4];
            s.team = new System.Collections.Generic.List<string> { "vo_su", "nu_hoa", "ca_ngua" };
            s.potentialStones = 0;
            s.cave = null;
            s.chests.Clear();
            for (int i = 0; i < 20; i++) s.chests.Add(new PendingChest { kind = "chest_gold", x = 1 });
            App.Save.Save();

            // đá từ rương vàng máy bi
            yield return Go(SceneIds.Machine);
            ClickByName("khay_chest_gold");
            var mm = Object.FindAnyObjectByType<MachineScene>();
            int boxes = 0;
            float t0 = Time.realtimeSinceStartup;
            while ((!mm.Idle || App.Modals.Count > 0) && Time.realtimeSinceStartup - t0 < 120)
            {
                if (App.Modals.Count > 0)
                {
                    yield return new WaitForSecondsRealtime(1.0f);
                    if (boxes == 0 || (boxes < 6 && s.potentialStones > 0 && !shotStones))
                    {
                        if (s.potentialStones > 0) shotStones = true;
                        yield return Shot(s.potentialStones > 0 ? "ruong_ra_da" : "ruong_vang");
                    }
                    boxes++;
                    App.Modals.Back();
                    yield return new WaitForSecondsRealtime(0.25f);
                }
                yield return null;
            }
            Debug.Log($"[Thử] Mở {boxes} hộp rương vàng: có {s.potentialStones} đá tiềm năng");
            if (s.potentialStones < 20) s.potentialStones += 20;
            App.Save.Save();

            // khai phá Giọt Sương (3 sao: 3 ô mở)
            yield return Go(SceneIds.Heroes);
            HeroDetail.Open("giot_suong");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("chi_tiet_dai_tiem_nang");
            ClickByName("mo_tiem_nang");
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot("tiem_nang_trong");
            int st0 = s.potentialStones;
            ClickByName("khai_pha");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("tiem_nang_so_sanh");
            ClickByName("giu_moi");
            yield return new WaitForSecondsRealtime(0.4f);
            Debug.Log($"[Thử] Khai phá lần 1: tốn {st0 - s.potentialStones} đá (đợi 3); giữ mới: {PotentialPanel.TotalsText(d.Cfg, s.Hero("giot_suong").potential)}");
            ClickByName("khoa_0");
            yield return new WaitForSecondsRealtime(0.3f);
            yield return Shot("tiem_nang_khoa");
            var keep = s.Hero("giot_suong").potential.Select(x => x == null ? "-" : $"{x.k}{x.r}").ToArray();
            st0 = s.potentialStones;
            ClickByName("khai_pha");
            yield return new WaitForSecondsRealtime(0.6f);
            ClickByName("giu_cu");
            yield return new WaitForSecondsRealtime(0.4f);
            var after = s.Hero("giot_suong").potential.Select(x => x == null ? "-" : $"{x.k}{x.r}").ToArray();
            Debug.Log($"[Thử] Khai phá lần 2 có khoá ô 1: tốn {st0 - s.potentialStones} đá (đợi 2 + 2 = 4); giữ cũ: {(keep.SequenceEqual(after) ? "dòng không đổi" : "LỖI: dòng đổi")}");
            var m = Teams.MemberOf(s, "giot_suong", d);
            Debug.Log($"[Thử] Giọt Sương vào trận: mods {(m.mods == null ? "không" : $"máu {m.mods.hpPct:P0} công {m.mods.atkPct:P0} thủ {m.mods.defPct:P0} tốc {m.mods.spd}")}, đầu trận {(m.start == null ? "không" : $"mana {m.start.mana} nộ {m.start.rage} chí mạng {m.start.crit:P0} hút máu {m.start.lifesteal:P0}")}");
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.3f);
            HeroDetail.Open("giot_suong");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("chi_tiet_co_tiem_nang");
            App.Modals.CloseAll();

            // Hang tầng Dễ
            yield return Go(SceneIds.Cave);
            int day = Afk.Today(PokiClash.Game.SaveService.Now());
            if (Potential.CaveElem(s, d.Cfg, day) == null) ClickByName("chon_kim");
            yield return new WaitForSecondsRealtime(0.4f);
            yield return Shot("hang");
            int stones = s.potentialStones, left = Potential.CaveLeft(s, d.Cfg, day);
            ClickByName("vao_tang_0");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("hang_chuan_bi");
            ClickButton("Xuất trận!");
            yield return WaitScene(SceneIds.Battle);
            var ctl = Object.FindAnyObjectByType<BattleController>();
            ctl.SetSpeed(3);
            ctl.SetAuto(true);
            yield return Until(() => ctl.Battle.phase == Phase.Over, 180);
            yield return Until(() => App.Modals.Count > 0, 10);
            yield return new WaitForSecondsRealtime(0.9f);
            yield return Shot("hang_ket_qua");
            Debug.Log($"[Thử] Hang tầng Dễ: {(ctl.Battle.winner == 0 ? "thắng" : "thua")}, đá {stones}→{s.potentialStones}, lượt {left}→{Potential.CaveLeft(s, d.Cfg, day)}");
            App.Modals.CloseAll();
            yield return Go(SceneIds.Hub);
            Debug.Log("[Thử] Xong tiềm năng.");
        }

        static bool shotStones;

        [MenuItem("PokiClash/Thử/Trang trại: tự xếp, tua giờ, thu hoạch, đổi ca (đang Play)", priority = 116)]
        static void TryFarm()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunFarm()));
        }

        static IEnumerator RunFarm()
        {
            shot = 180;
            const double H = 3600000;
            var s = App.Save.Data;
            var d = App.Data;
            s.intro = true;
            foreach (var h in d.Heroes) s.Hero(h.id).owned = false;
            foreach (var id in new[] { "giot_suong", "vo_su", "nu_hoa", "ca_ngua", "bo_de" }) s.Hero(id).owned = true;
            s.team = new System.Collections.Generic.List<string> { "giot_suong", "vo_su", "nu_hoa" };
            s.level = 9;
            s.farm = null;
            App.Save.Save();
            yield return Go(SceneIds.Hub);
            yield return Shot("sanh_trang_trai");
            yield return Go(SceneIds.Farm);
            yield return Shot("trang_trai_trong");
            ClickByName("tu_xep");
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot("trang_trai_tu_xep");
            Debug.Log("[Thử] Tự xếp: " + string.Join(", ", s.farm.spots.Select((sp, i) => $"{d.Cfg.farm.spots[i].name}: {sp.hero ?? "-"}")));
            Farm.Travel(s, 3 * H);
            App.Router.CurrentRoot.Refresh();
            yield return new WaitForSecondsRealtime(0.4f);
            yield return Shot("trang_trai_3_gio");
            int b0 = s.balls;
            ClickByName("thu_hoach");
            yield return new WaitForSecondsRealtime(0.4f);
            Debug.Log($"[Thử] Sau 3 giờ: thu hoạch {s.balls - b0} bi; còn lẻ {string.Join(", ", s.farm.spots.Select(sp => sp.stock.ToString("0.00")))}");
            // đổi ca ở Ao vịt: rút tướng hết sức, đưa tướng rảnh vào
            string before = s.farm.spots[0].hero;
            ClickNamed("cho_0");
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot("chon_tuong");
            ClickByName("rut_ra");
            yield return new WaitForSecondsRealtime(0.5f);
            var free = d.Heroes.Select(h => h.id).FirstOrDefault(id => Farm.Free(s, s.farm, id, PokiClash.Game.SaveService.Now()));
            if (free != null) ClickByName("dat_" + free);
            else App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.5f);
            Debug.Log($"[Thử] Đổi ca Ao vịt: {before} → {s.farm.spots[0].hero ?? "-"}; {before} nghỉ còn {Farm.RestLeft(s.farm, before, PokiClash.Game.SaveService.Now()) / 60000:0} phút; vẫn trong đội: {s.team.Contains(before)}");
            ClickByName("farm_x2");
            yield return new WaitForSecondsRealtime(4.2f);
            yield return Shot("trang_trai_x2");
            Debug.Log($"[Thử] Năng suất ×2: {(Farm.Boosting(s.farm, PokiClash.Game.SaveService.Now()) ? "đang bật" : "không bật")}");
            yield return Go(SceneIds.Hub);
            Debug.Log("[Thử] Xong trang trại.");
        }

        [MenuItem("PokiClash/Thử/Gói hỗ trợ: Thẻ Phiêu Lưu, hết lượt quảng cáo, Bỏ quảng cáo (đang Play)", priority = 117)]
        static void TryPacks()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunPacks()));
        }

        static IEnumerator RunPacks()
        {
            shot = 190;
            const double H = 3600000;
            var s = App.Save.Data;
            var cfg = App.Data.Cfg;
            double Now() => PokiClash.Game.SaveService.Now();
            s.intro = true;
            s.zones = new int[5];
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            s.afk = new AfkState { lastTick = Now() };
            s.afkSince = (long)Now();
            s.ads = null;
            s.ent = null;
            s.trees = null;
            Trees.Tick(s, cfg, Now());
            App.Save.Save();

            // như bản phát hành chưa gắn SDK: nút quảng cáo và mục gói phải ẩn
            var (ads, store) = (Ads.Current, Store.Current);
            (Ads.Current, Store.Current) = (null, null);
            yield return Go(SceneIds.Hub);
            Afk.Travel(s, 4 * H);
            App.OpenAfk();
            yield return new WaitForSecondsRealtime(0.6f);
            bool Shown(string n) => Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).Any(b => b.name == n && b.isActiveAndEnabled);
            string afkShown = $"Tăng tốc hiện {Shown("afk_tang_toc")}, Mở ngay hiện {Shown("afk_mo_ngay")}";
            App.Modals.CloseAll();
            TreePanel.Open();
            yield return new WaitForSecondsRealtime(0.6f);
            Debug.Log($"[Thử] Chưa có SDK: Hái ×2 hiện {Shown("cay_hai_x2")}, {afkShown}");
            App.Modals.CloseAll();
            yield return Go(SceneIds.Notebook);
            Debug.Log($"[Thử] Chưa có cửa hàng: mục gói hiện {Shown("mua_adventure_pass")}");
            (Ads.Current, Store.Current) = (ads, store);
            yield return Go(SceneIds.Hub);
            yield return Go(SceneIds.Notebook);
            yield return Shot("so_tay_goi");
            ClickByName("mua_adventure_pass");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("so_tay_da_mua_the");
            Debug.Log($"[Thử] Mua Thẻ Phiêu Lưu: còn thẻ {AdGate.PassActive(s, Now())}, còn {(s.ent.passUntil - Now()) / 86400000:0.0} ngày; khay {Afk.Slots(s, cfg, Now())} ô, rương mở {Afk.OpenH(s, cfg, Now())} giờ");

            yield return Go(SceneIds.Hub);
            Afk.Travel(s, 12 * H);
            Trees.Travel(s, 12 * H);
            App.OpenAfk();
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("afk_the_phieu_luu");
            Debug.Log($"[Thử] AFK 12 giờ có thẻ: {s.afk.chests.Count} rương, ô khay hiện {Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).Count(b => b.name.StartsWith("afk_ruong_"))}");
            App.Modals.CloseAll();
            TreePanel.Open();
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("cay_bi_the_phieu_luu");
            int b0 = s.balls;
            ClickByName("cay_hai");
            yield return new WaitForSecondsRealtime(0.4f);
            Debug.Log($"[Thử] Cây bi 12 giờ có thẻ (2 cây, chứa {Trees.Cap(s, cfg, Now())}): hái +{s.balls - b0} bi (đợi 150, không thẻ 100)");
            App.Modals.CloseAll();
            int day = Afk.Today(Now());
            for (int i = 0; i < 3; i++) AdGate.Use(s, cfg, day, AdGate.AfkBoost);
            Afk.Travel(s, 2 * H);
            Trees.Travel(s, 2 * H);
            App.OpenAfk();
            yield return new WaitForSecondsRealtime(0.7f);
            yield return Shot("afk_het_luot_tang_toc");
            var boost = Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).FirstOrDefault(b => b.name == "afk_tang_toc");
            Debug.Log($"[Thử] Hết 3/3 lượt tăng tốc: nút '{boost?.Label.text}', bấm được {boost?.Interactable}");
            App.Modals.CloseAll();

            yield return Go(SceneIds.Notebook);
            ClickByName("mua_no_ads");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("so_tay_bo_quang_cao");
            yield return Go(SceneIds.Hub);
            TreePanel.Open();
            yield return new WaitForSecondsRealtime(0.7f);
            b0 = s.balls;
            ClickByName("cay_hai_x2");
            yield return new WaitForSecondsRealtime(0.5f);
            Debug.Log($"[Thử] Bỏ quảng cáo, Hái ×2 (2 giờ, 2 cây, có thẻ): +{s.balls - b0} bi ngay (đợi 60), hộp đang mở {App.Modals.Count}, lượt tree_double đã dùng {AdGate.Used(s, day, AdGate.TreeDouble)}");
            App.Modals.CloseAll();

            // Hang hết lượt thắng: "+1 lượt" (cave_extra, 1 lần mỗi ngày)
            s.zones[(int)Elem.Hoa] = 4;
            s.cave = new CaveDay { day = day, wins = cfg.cave.winsPerDay, pick = Elem.Kim };
            yield return Go(SceneIds.Cave);
            yield return Shot("hang_het_luot");
            int c0 = Potential.CaveLeft(s, cfg, day);
            ClickByName("hang_them_luot");
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("hang_them_luot");
            var again = Object.FindObjectsByType<SketchButton>(FindObjectsSortMode.None).Any(b => b.name == "hang_them_luot" && b.isActiveAndEnabled);
            Debug.Log($"[Thử] Hang: lượt {c0} → {Potential.CaveLeft(s, cfg, day)}; cave_extra đã dùng {AdGate.Used(s, day, AdGate.CaveExtra)}; nút +1 lượt còn hiện: {again}");
            yield return Go(SceneIds.Hub);
            yield return new WaitForSecondsRealtime(0.3f);
            Debug.Log("[Thử] Xong gói hỗ trợ.");
        }

        [MenuItem("PokiClash/Thử/Người chơi mới đi trọn Đảo Thủy (đang Play)", priority = 120)]
        static void TryThuy()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunThuy()));
        }

        [MenuItem("PokiClash/Thử/Chụp sảnh và đảo với tiến độ giả (đang Play)", priority = 121)]
        static void TryMapShots()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunMapShots()));
        }

        [MenuItem("PokiClash/Thử/Đảo 70 ải: đường mòn, bảng chặng, hộp chuẩn bị, trận có lính (đang Play)", priority = 122)]
        static void TryIslandLong()
        {
            if (!EditorApplication.isPlaying || App.I == null) return;
            App.I.StartCoroutine(WithSaveBackup(RunIslandLong()));
        }

        // Đảo Thủy 70 ải: màn đảo ở 0, 23, 69 ải đã qua; bảng chặng của chấm ải 24; hộp chuẩn bị các kiểu ải (bóng tướng khởi đầu,
        // bầy lính, nhóm 3 con, cửa ải, mini boss, boss); trận ải 3 (hai lính)
        static IEnumerator RunIslandLong()
        {
            shot = 300;
            var d = App.Data;
            var s = App.Save.Data;
            s.intro = true;
            s.level = 4;
            foreach (var id in new[] { "giot_suong", "vo_su", "nu_hoa" }) s.Hero(id).owned = true;
            foreach (int prog in new[] { 0, 23, 69 })
            {
                s.zones[(int)Elem.Thuy] = prog;
                s.zoneChests[(int)Elem.Thuy] = prog >= 10 ? 1 : 0;
                App.Save.Save();
                yield return Go(SceneIds.Zone, Elem.Thuy);
                yield return new WaitForSecondsRealtime(0.6f);
                yield return Shot("dao70_" + prog);
                if (prog != 23) continue;
                ClickNamed("cham_24"); // chạm chấm mở thẳng hộp chuẩn bị của ải đó (bảng chặng bỏ 2026-11-03)
                yield return new WaitForSecondsRealtime(0.6f);
                yield return Shot("chuan_bi_24");
                App.Modals.CloseAll();
            }
            int Id(int idx) => d.ZoneStages(Elem.Thuy).First(st => st.idx == idx).id;
            var group3 = d.ZoneStages(Elem.Thuy).First(st => st.enemies.Count == 3);
            var gate = d.ZoneStages(Elem.Thuy).First(st => st.tag == StageTag.Gate);
            foreach (var (idx, name) in new[] { (1, "bong"), (2, "bay_linh"), (group3.idx, "nhom_3"), (gate.idx, "cua_ai"), (20, "mini_boss"), (70, "boss") })
            {
                StagePrep.Open(Id(idx));
                yield return new WaitForSecondsRealtime(0.6f);
                yield return Shot($"chuan_bi_{idx}_{name}");
                App.Modals.CloseAll();
                yield return new WaitForSecondsRealtime(0.2f);
            }
            yield return RunBattle(Id(3), false);
            App.Modals.CloseAll();
            yield return Go(SceneIds.Hub);
            yield return Shot("sanh_70");
            Debug.Log($"[Thử] Xong đảo 70 ải: ảnh trong {ShotDir}");
        }

        static IEnumerator RunMapShots()
        {
            shot = 100;
            var s = App.Save.Data;
            s.intro = true;
            s.level = 5;
            s.zones[(int)Elem.Thuy] = Islands.Size(Elem.Thuy);
            s.zones[(int)Elem.Hoa] = 5;
            s.zoneChests[(int)Elem.Thuy] = Islands.Chests(Elem.Thuy).Length;
            Progress.UnlockHero(s, "vo_su");
            Progress.UnlockHero(s, "nu_hoa");
            App.Save.Save();
            yield return Go(SceneIds.Hub);
            yield return Shot("sanh_tien_do");
            yield return Go(SceneIds.Zone, Elem.Hoa);
            yield return new WaitForSecondsRealtime(0.4f);
            yield return Shot("dao_hoa_5");
            yield return Go(SceneIds.Zone, Elem.Kim);
            yield return Shot("dao_kim_0");
            yield return Go(SceneIds.Hub);
        }

        static bool ClickNamed(string name)
        {
            var go = GameObject.Find(name);
            if (go == null)
                foreach (var c in Object.FindObjectsByType<ClickCatcher>(FindObjectsSortMode.None))
                    if (c.name == name)
                    {
                        go = c.gameObject;
                        break;
                    }
            var cc = go ? go.GetComponent<ClickCatcher>() : null;
            if (cc == null)
            {
                Debug.LogWarning($"[Thử] Không thấy '{name}'");
                return false;
            }
            cc.OnClick?.Invoke();
            return true;
        }

        static IEnumerator RunThuy()
        {
            shot = 80;
            var d = App.Data;
            App.Save.Reset();
            yield return Go(SceneIds.Hub);
            yield return Until(() => App.Modals.Count > 0, 3);
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot("gioi_thieu");
            ClickButton("Bắt đầu!");
            // hộp chọn tướng khởi đầu (15_TuongKhoiDau.md): chụp rồi chọn Giọt Sương
            yield return Until(() => Object.FindAnyObjectByType<StarterDialog>() != null, 3);
            yield return new WaitForSecondsRealtime(0.6f);
            yield return Shot("chon_tuong_khoi_dau");
            App.Save.Data.ChooseStarter("giot_suong");
            App.Save.Save();
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot("sanh_nguoi_moi");
            yield return Go(SceneIds.Zone, Elem.Thuy);
            yield return Shot("dao_thuy_dau");
            int wins = 0, losses = 0, guard = 0;
            var log = new System.Text.StringBuilder();
            // đảo 70 ải: đánh 12 ải đầu (bóng tướng khởi đầu, tặng Võ Sư ở ải 3, Tiểu Y ải 5, Cánh Cụt ải 10, rương ải 10)
            const int Upto = 12;
            while (App.Save.Data.zones[(int)Elem.Thuy] < Upto && guard++ < 40)
            {
                var s = App.Save.Data;
                var next = Progress.NextStage(s, d, Elem.Thuy);
                // tướng mới được tặng: cho vào đội nếu còn ô đội mở (chạm ô đội mở bể tướng, chọn, "Xong")
                StagePrep.Open(next.id);
                yield return new WaitForSecondsRealtime(0.4f);
                if (Progress.TeamSlots(s) > 1)
                {
                    ClickNamed("o_doi_0");
                    yield return new WaitForSecondsRealtime(0.4f);
                    foreach (var id in new[] { "vo_su", "nu_hoa" })
                        if (s.Hero(id).owned && !s.team.Contains(id))
                        {
                            ClickNamed("kho_" + id);
                            yield return new WaitForSecondsRealtime(0.2f);
                        }
                    ClickButton("Xong");
                    yield return new WaitForSecondsRealtime(0.3f);
                }
                if (next.idx == 1 || next.idx == 3 || next.idx == 10) yield return Shot("chuan_bi_ai_" + next.idx);
                ClickButton("Xuất trận!");
                yield return WaitScene(SceneIds.Battle);
                var ctl = Object.FindAnyObjectByType<BattleController>();
                ctl.SetSpeed(3);
                ctl.SetAuto(true);
                yield return Until(() => ctl.Battle.phase == Phase.Over, 300);
                yield return Until(() => App.Modals.Count > 0, 30);
                yield return new WaitForSecondsRealtime(0.6f);
                bool won = ctl.Battle.winner == 0;
                if (won) wins++;
                else losses++;
                log.Append($"ải {next.idx} cấp {App.Save.Data.level}: {(won ? "thắng" : "thua")} ({ctl.Battle.round} hiệp); ");
                if (next.idx == 10 && won) yield return Shot("ket_qua_ai_10");
                App.Modals.CloseAll();
                // thả hết bi ở máy bi thật (×1, "Thả liền"), mở rương, đóng hộp lên cấp
                yield return Go(SceneIds.Machine);
                var mm = Object.FindAnyObjectByType<MachineScene>();
                ClickButton("×1");
                int guardM = 0;
                while (App.Save.Data.balls > 0 && guardM++ < 40)
                {
                    ClickButton($"Thả liền {d.Cfg.MaxPerDrop(App.Save.Data.level)}");
                    yield return Until(() => mm.Session > 0, 2);
                    yield return SettleMachine(mm, "thuy", 0, false);
                }
                yield return Go(SceneIds.Zone, Elem.Thuy);
                if (Progress.ZoneChestReady(App.Save.Data, Elem.Thuy) == 0)
                {
                    yield return Shot("dao_thuy_ruong");
                    ClickNamed("ruong_0");
                    yield return new WaitForSecondsRealtime(0.6f);
                    yield return Shot("ruong_ai_10");
                    App.Modals.CloseAll();
                }
            }
            yield return new WaitForSecondsRealtime(0.4f);
            yield return Shot("dao_thuy_" + Upto);
            yield return Go(SceneIds.Hub);
            yield return Shot("sanh_sau_" + Upto + "_ai");
            var sv = App.Save.Data;
            Debug.Log($"[Thử] Đảo Thủy {Upto} ải đầu: {wins} thắng, {losses} thua; cấp {sv.level}; đã thả {sv.ballsSpent} bi, còn {sv.balls}; tướng có: " +
                      string.Join(", ", d.Heroes.Where(h => sv.Hero(h.id).owned).Select(h => $"{h.name} ({sv.Hero(h.id).shards} mảnh)")) +
                      $"; mảnh Mập Răng Cưa {sv.Hero("map_rang").shards}; rương {sv.zoneChests[(int)Elem.Thuy]}/{Islands.Chests(Elem.Thuy).Length}; đảo gợi ý {Progress.RecommendedZone(sv, d).name}\n{log}");
        }

        static IEnumerator Until(System.Func<bool> cond, float timeout)
        {
            float t0 = Time.realtimeSinceStartup;
            while (!cond() && Time.realtimeSinceStartup - t0 < timeout) yield return null;
        }

        static IEnumerator RunBattle(int stageId, bool bigTeam)
        {
            shot = 20 * stageId;
            if (bigTeam)
            {
                var sv = App.Save.Data;
                foreach (var id in new[] { "giot_suong", "vo_su", "nu_hoa" }) sv.Hero(id).owned = true;
                sv.team = new System.Collections.Generic.List<string> { "giot_suong", "vo_su", "nu_hoa" };
                sv.level = 7;
            }
            yield return Go(SceneIds.Battle, new BattleArgs { stageId = stageId });
            var ctl = Object.FindAnyObjectByType<BattleController>();
            if (!ctl)
            {
                Debug.LogError("[Thử] Không thấy BattleController");
                yield break;
            }
            string tag = "tran" + stageId;
            yield return Shot(tag + "_vs");
            yield return Until(() => ctl.WaitingPlayer, 30);
            yield return new WaitForSecondsRealtime(0.8f);
            yield return Shot(tag + "_chon_the");
            ctl.TestPick(0);
            yield return new WaitForSecondsRealtime(0.15f);
            yield return Shot(tag + "_bay_the");
            yield return Until(() => ctl.WaitingPlayer, 5);
            ctl.TestPick(1);
            yield return Until(() => ctl.WaitingPlayer, 5);
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot(tag + "_hang_the");
            ctl.SetSpeed(1);
            ctl.SetAuto(true);
            yield return new WaitForSecondsRealtime(2.2f);
            yield return Shot(tag + "_chay_the");
            yield return new WaitForSecondsRealtime(0.9f);
            yield return Shot(tag + "_danh");
            ctl.SetSpeed(3);
            float t0 = Time.realtimeSinceStartup;
            yield return Until(() => ctl.Battle.phase == Phase.Over, 240);
            var tt = ctl.PlayerTurnSeconds;
            Debug.Log($"[Thử] Ải {stageId}: trận xong sau {Time.realtimeSinceStartup - t0:0.0} giây (×3), {ctl.Battle.round} hiệp, " +
                      $"{(ctl.Battle.winner == 0 ? "thắng" : "thua")}; phần ra đòn một lượt người chơi ở ×1: " +
                      $"trung bình {(tt.Count > 0 ? tt.Average() : 0):0.0} giây ({tt.Count} lượt)");
            yield return Until(() => App.Modals.Count > 0, 30);
            yield return new WaitForSecondsRealtime(1.2f);
            yield return Shot(tag + "_ket_qua");
            Debug.Log($"[Thử] Xong trận thử: ảnh trong {ShotDir}");
        }

        static IEnumerator WaitScene(string scene)
        {
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != scene) && Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(0.3f);
        }

        static IEnumerator Go(string scene, object args = null)
        {
            App.Router.Go(scene, args);
            yield return WaitScene(scene);
            Debug.Log($"[Thử] Đang ở {scene} (thanh trên: {App.Router.CurrentRoot?.Bar})");
        }

        static IEnumerator Shot(string name)
        {
            bool still = Still;
            if (still)
            {
                Theme.SetBoil(false);
                yield return null;
            }
            yield return new WaitForEndOfFrame();
            Directory.CreateDirectory(ShotDir);
            var tex = ScreenCapture.CaptureScreenshotAsTexture();
            var path = Path.Combine(ShotDir, $"{shot++:00}_{name}_{tex.width}x{tex.height}.png");
            File.WriteAllBytes(path, tex.EncodeToPNG());
            Object.Destroy(tex);
            if (still) App.ApplySettings();
        }

        static IEnumerator Run()
        {
            shot = 0;
            if (Directory.Exists(ShotDir)) Directory.Delete(ShotDir, true);
            yield return Go(SceneIds.Hub);
            yield return Shot("hub");
            yield return Go(SceneIds.Zone, Elem.Thuy);
            yield return Shot("zone_thuy");
            yield return Go(SceneIds.Battle, 8);
            yield return Shot("battle");
            App.Router.CurrentRoot.OnBack();
            yield return WaitScene(SceneIds.Zone);
            yield return Go(SceneIds.Zone, Elem.Hoa);
            yield return Shot("zone_hoa");
            App.Router.CurrentRoot.OnBack();
            yield return WaitScene(SceneIds.Hub);

            // xếp hàng: hai yêu cầu chồng lên nhau khi đang chuyển, chỉ giữ yêu cầu mới nhất
            App.Router.Go(SceneIds.Heroes);
            yield return null;
            App.Router.Go(SceneIds.Machine);
            App.Router.Go(SceneIds.Cards);
            yield return WaitScene(SceneIds.Cards);
            Debug.Log($"[Thử] Xếp hàng: cuối cùng ở {App.Router.Current} (cần Cards)");
            yield return Shot("cards");

            yield return Go(SceneIds.Heroes);
            yield return Shot("heroes");
            yield return Go(SceneIds.Machine);
            int before = App.Save.Data.balls;
            App.Save.Data.balls--;
            PokiClash.Core.Progress.AddExp(App.Save.Data, 10, App.Data.Cfg);
            App.Save.Save();
            App.Toasts.Show("+10 EXP (thử)", App.Art.Icon("exp"));
            yield return new WaitForSecondsRealtime(0.4f);
            yield return Shot("machine_toast");
            App.Save.Data.balls = before;
            App.Save.Save();

            yield return Go(SceneIds.Notebook);
            yield return Shot("notebook");
            App.Modals.Confirm("Xoá dữ liệu?", "Mọi tiến trình mất hết: về cấp 1, 10 bi, chỉ có Giọt Sương.", "Xoá", () => { });
            yield return new WaitForSecondsRealtime(0.5f);
            yield return Shot("notebook_confirm");
            App.Modals.CloseAll();
            yield return new WaitForSecondsRealtime(0.3f);

            App.Back();
            yield return WaitScene(SceneIds.Hub);
            yield return Shot("hub_back");
            Debug.Log($"[Thử] Xong vòng: {shot} ảnh trong {ShotDir}");
        }

        static IEnumerator RunFrames()
        {
            foreach (var f in GameViewSizes.Frames)
            {
                GameViewSizes.Select(f.x, f.y);
                yield return new WaitForSecondsRealtime(0.6f);
                yield return Go(SceneIds.Hub);
                yield return Shot($"khung_hub");
                yield return Go(SceneIds.Zone, Elem.Kim);
                yield return Shot($"khung_zone");
                yield return Go(SceneIds.Cards);
                yield return Shot($"khung_cards");
            }
            GameViewSizes.Select(1080, 1920);
            yield return Go(SceneIds.Hub);
            Debug.Log($"[Thử] Xong chụp khung: {ShotDir}");
        }
    }
}
