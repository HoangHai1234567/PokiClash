// Vòng thử trình diễn trận (2026-11-17, việc D của đợt "tăng dày nội dung"): chụp chuỗi khung để soi chết, biến hình, ra sân.
// 1. Boss tiến hóa: ải đầu tiên có boss "evo" (đảo Thủy ải 70 nếu có), đến lượt mình thì ép boss còn 1 máu rồi chọn thẻ; cú đánh hạ boss
//    → clip chết → tụ sáng → chớp đổi dạng → clip ra sân của dạng mới. Đúng với cả luật cũ (tiến hóa dưới 25% máu: còn 1 máu là tiến hóa)
//    lẫn luật mới (tiến hóa lúc máu về 0). Ảnh Temp/PokiShots/evo_seq_###.png.
// 2. Tướng thường gục: ải có 2 địch trở lên, không boss: ép địch đang ra sân còn 1 máu → clip chết trọn → tướng kế diễn clip ra sân,
//    thanh máu dâng. Ảnh Temp/PokiShots/ko_seq_###.png.
// 3. Tướng mình gục: ép tướng mình còn 1 máu, bật tự chơi (máy tự chọn tướng thay) → clip chết → tướng thay ra sân.
//    Ảnh Temp/PokiShots/own_ko_seq_###.png.
// Mỗi khung ghi giờ, pha trình diễn (StageView.ShowPhase), bên nào đang chết / đang ra sân, clip đang chạy vào Temp/PokiShots/trinh_dien.txt.
// Chạy khi đang Play từ Boot; bản lưu được trả lại như trước khi thử.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class BattleShowTour
    {
        static string Dir => PlayTour.ShotDir;
        static string LogPath => Path.Combine(Dir, "trinh_dien.txt");

        static void Log(string s)
        {
            Debug.Log("[Thử] " + s);
            File.AppendAllText(LogPath, s + System.Environment.NewLine);
        }

        [MenuItem("PokiClash/Thử/Trận/Trình diễn trận: boss tiến hóa (chết, biến hình, ra sân), tướng gục, tướng kế ra sân (đang Play)", priority = 125)]
        static void Try()
        {
            if (!EditorApplication.isPlaying || App.I == null)
            {
                Debug.LogWarning("[Thử] Mở Boot.unity và bấm Play trước.");
                return;
            }
            App.I.StartCoroutine(Run(7));
        }

        [MenuItem("PokiClash/Thử/Trận/Trình diễn trận: chỉ boss tiến hóa (đang Play)", priority = 126)]
        static void TryEvo()
        {
            if (EditorApplication.isPlaying && App.I != null) App.I.StartCoroutine(Run(1));
        }

        [MenuItem("PokiClash/Thử/Trận/Trình diễn trận: độc, phản đòn (đang Play)", priority = 128)]
        static void TryPoison()
        {
            if (EditorApplication.isPlaying && App.I != null) App.I.StartCoroutine(Run(4));
        }

        [MenuItem("PokiClash/Thử/Trận/Trình diễn trận: chỉ tướng gục, tướng kế ra sân (đang Play)", priority = 127)]
        static void TryKo()
        {
            if (EditorApplication.isPlaying && App.I != null) App.I.StartCoroutine(Run(2));
        }

        // which (cờ): 1 boss tiến hóa, 2 tướng gục (địch, mình), 4 độc + phản đòn
        static IEnumerator Run(int which)
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            Directory.CreateDirectory(Dir);
            foreach (var f in Directory.GetFiles(Dir, "*_seq_*.png")) File.Delete(f);
            File.WriteAllText(LogPath, "");
            try
            {
                var d = App.Data;
                var evos = d.Stages.Where(s => s.enemies.Count > 0 && s.enemies[0].evo && d.Hero(s.enemies[0].hero).forms.Length > 1).OrderBy(s => s.id).ToList(); // boss đứng đầu (ra sân trước)
                // ca thường: boss tiến hóa đầu tiên (clip chết, ra sân dài vừa); ca dài: boss cuối đảo Thủy (Hải Long: chết 4 giây, ra sân
                // 4,8 giây, chuỗi phải cắt ở EvoDieCap và chờ ra sân tối đa EvoAppearCap)
                var evo = evos.FirstOrDefault();
                var evoLong = evos.FirstOrDefault(s => s.zone == Elem.Thuy && s.idx == Islands.Size(Elem.Thuy));
                if ((which & 1) != 0 && evo != null) yield return EvoCase(evo, "evo_seq");
                else if ((which & 1) != 0) Log("Không có ải boss tiến hóa (evo)");
                if ((which & 1) != 0 && evoLong != null && evoLong != evo) yield return EvoCase(evoLong, "evo_seq_dai");

                var two = d.Stages.FirstOrDefault(s => s.enemies.Count >= 2 && !s.enemies.Any(e => e.boss || e.evo));
                if ((which & 2) != 0 && two != null) yield return KoCase(two, false, "ko_seq");
                else if ((which & 2) != 0) Log("Không có ải 2 địch không boss");
                if ((which & 2) != 0 && two != null) yield return KoCase(two, true, "own_ko_seq");
                if ((which & 4) != 0 && two != null) yield return PoisonCase(two, "doc_seq");
            }
            finally
            {
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            App.Router.Go(SceneIds.Hub);
            Log("Xong trình diễn trận: ảnh và nhật ký trong " + Dir);
        }

        // đội 3 tướng đủ mạnh để sống qua lượt địch (cấp người chơi tạm nâng; bản lưu trả lại sau)
        static void Team(int minLevel = 40) // cấp 60 mở ô đội thứ 2 (Progress.SlotLevels)
        {
            var s = App.Save.Data;
            var ids = s.team != null && s.team.Count > 0 ? s.team.ToList() : new List<string>();
            // đủ 3 tướng (ca tướng mình gục cần tướng thay)
            foreach (var h in App.Data.Heroes)
            {
                if (ids.Count >= 3) break;
                if (!ids.Contains(h.id)) ids.Add(h.id);
            }
            foreach (var id in ids) s.Hero(id).owned = true;
            s.team = ids;
            if (s.level < minLevel) s.level = minLevel;
        }

        static IEnumerator Enter(StageDef st)
        {
            // trận trước còn trên màn (Battle → Battle): chờ có BattleController mới, đừng bắt nhầm sân cũ
            var old = Object.FindAnyObjectByType<BattleController>();
            App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = st.id });
            float t0 = Time.realtimeSinceStartup;
            while ((App.Router.Busy || App.Router.Current != SceneIds.Battle || Object.FindAnyObjectByType<BattleController>() == old && old) &&
                   Time.realtimeSinceStartup - t0 < 30) yield return null;
            yield return new WaitForSecondsRealtime(0.3f);
        }

        static IEnumerator Until(System.Func<bool> ok, float max)
        {
            float t0 = Time.realtimeSinceStartup;
            while (!ok() && Time.realtimeSinceStartup - t0 < max) yield return null;
        }

        // chọn thẻ tới khi hết lượt chọn (thẻ đầu mỗi lượt chia)
        static IEnumerator PickAll(BattleController ctl)
        {
            int guard = 0;
            while (ctl.Battle.phase == Phase.Picking && ctl.Battle.turn.side == 0 && guard++ < 12)
            {
                ctl.TestPick(0);
                yield return new WaitForSecondsRealtime(0.18f);
            }
        }

        static IEnumerator EvoCase(StageDef st, string tag)
        {
            Team();
            yield return Enter(st);
            var ctl = Object.FindAnyObjectByType<BattleController>();
            var sv = Object.FindAnyObjectByType<StageView>();
            if (!ctl || !sv)
            {
                Log("Không thấy BattleController / StageView");
                yield break;
            }
            yield return Until(() => ctl.WaitingPlayer, 45);
            var side = ctl.Battle.sides[1];
            var boss = side.fighters[side.active];
            Log($"{tag}: boss tiến hóa ải {st.idx} đảo {st.zone}, {boss.hero.id} dạng {boss.form + 1}/{boss.hero.forms.Length}, Epic {sv.Epic:0.00}, Power {sv.Power(1):0.00}");
            int form0 = boss.form;
            boss.hp = 1;
            boss.shield = 0;
            // chụp từ cú hạ gục (boss ngã) tới khi chuỗi qua pha "evo_ra" và dạng mới diễn xong clip ra sân; logic trận đi trước hoạt cảnh
            // nên không canh boss.form
            var rec = App.I.StartCoroutine(Record(sv, tag, 16f, () => sv.IsDown(1) || sv.ShowPhase != "" || Seen.Contains("evo_ra") && sv.IsEntering(1),
                () => Seen.Contains("evo_ra") && sv.ShowPhase == "" && !sv.IsEntering(1)));
            yield return PickAll(ctl);
            yield return rec;
            Log($"Boss sau chuỗi: dạng {boss.form + 1}, máu {boss.hp:0}/{boss.maxHp:0}, phase trận {ctl.Battle.phase}");
        }

        static IEnumerator KoCase(StageDef st, bool own, string tag)
        {
            Team(own ? 60 : 40);
            yield return Enter(st);
            var ctl = Object.FindAnyObjectByType<BattleController>();
            var sv = Object.FindAnyObjectByType<StageView>();
            if (!ctl || !sv) yield break;
            yield return Until(() => ctl.WaitingPlayer, 45);
            int s = own ? 0 : 1;
            var team = ctl.Battle.sides[s];
            int act0 = team.active;
            var f = team.fighters[act0];
            Log($"{tag}: ải {st.idx} đảo {st.zone}, {(own ? "tướng mình" : "địch")} {f.hero.id} còn 1 máu; đội mình " +
                $"{string.Join(",", ctl.Battle.sides[0].fighters.Select(x => x.hero.id))} (bản lưu {string.Join(",", App.Save.Data.team)}, cấp {App.Save.Data.level})");
            f.hp = 1;
            f.shield = 0;
            if (own)
            {
                // địch không gục được trong lúc chờ nó đánh hạ tướng mình
                var foe = ctl.Battle.ActiveOf(1);
                foe.maxHp = foe.hp = 1e7;
            }
            bool down = false;
            var rec = App.I.StartCoroutine(Record(sv, tag, own ? 40f : 16f, () => (down |= sv.IsDown(s)) && (sv.IsDown(s) || sv.IsEntering(s)),
                () => team.active != act0 && !sv.IsDown(s) && !sv.IsEntering(s)));
            if (own)
            {
                // tướng mình hút máu, hồi máu lại trong lượt mình: tới lượt địch mới ép còn 1 máu; máy tự chọn tướng thay
                ctl.SetAuto(true);
                float tw = Time.realtimeSinceStartup;
                while (ctl.Battle.turn.side != 1 && ctl.Battle.phase != Phase.Over && Time.realtimeSinceStartup - tw < 30) yield return null;
                f.hp = 1;
                f.shield = 0;
                Log($"{tag}: tới lượt địch, tướng mình còn 1 máu");
            }
            else yield return PickAll(ctl);
            yield return rec;
            if (own) ctl.SetAuto(false);
            Log($"{tag}: tướng ra sân sau {team.fighters[team.active].hero.id} (trước {f.hero.id}), phase trận {ctl.Battle.phase}");
        }

        // Độc và phản đòn: địch đang ra sân bị tẩm 3 lớp độc (mất máu đầu lượt nó) và có phản đòn 50% (đòn của mình dội lại mình);
        // chụp 9 giây từ lúc chọn thẻ
        static IEnumerator PoisonCase(StageDef st, string tag)
        {
            Team();
            yield return Enter(st);
            var ctl = Object.FindAnyObjectByType<BattleController>();
            var sv = Object.FindAnyObjectByType<StageView>();
            if (!ctl || !sv) yield break;
            yield return Until(() => ctl.Battle.phase == Phase.Picking && ctl.Battle.turn.side == 0, 45);
            var foe = ctl.Battle.ActiveOf(1);
            foe.maxHp = foe.hp = 1e6;
            foe.statuses.RemoveAll(x => x.id == StatusId.Poison);
            foe.statuses.Add(new StatusInst { id = StatusId.Poison, left = 3, stacks = 3, v = 60 });
            foe.buffs.Add(new Buff { stat = Stat.Thorns, v = 0.5, left = 99, until = PokiClash.Core.Until.Start });
            Log($"{tag}: ải {st.idx}, địch {foe.hero.id}: độc 3 lớp, phản đòn 50%");
            var rec = App.I.StartCoroutine(Record(sv, tag, 9f, () => true, () => false));
            ctl.SetAuto(true);
            yield return rec;
            ctl.SetAuto(false);
        }

        static readonly HashSet<string> Seen = new HashSet<string>(); // các pha trình diễn đã thấy trong lần chụp đang chạy

        // chữ trên hai thanh máu (bảng phe mình / địch)
        static string HpLabels()
        {
            var bars = Object.FindObjectsByType<UI.UiBar>(FindObjectsSortMode.None).Where(b => b.Type == UI.UiBar.Kind.Hp && b.isActiveAndEnabled && b.Label)
                .Select(b => b.Label.text);
            return string.Join(" | ", bars);
        }

        // chụp mỗi khoảng 0,12 giây khi `on` đúng, dừng khi `done` đúng (sau khi đã chụp) hoặc quá max giây; ghi nhật ký từng khung
        static IEnumerator Record(StageView sv, string tag, float max, System.Func<bool> on, System.Func<bool> done)
        {
            float t0 = Time.realtimeSinceStartup, last = -1, first = -1;
            int n = 0;
            string phase0 = null;
            Seen.Clear();
            while (Time.realtimeSinceStartup - t0 < max)
            {
                if (!sv) yield break;
                if (sv.ShowPhase != phase0)
                {
                    Log($"  {tag} t={Time.realtimeSinceStartup - t0:0.00}s pha '{phase0}' → '{sv.ShowPhase}'");
                    phase0 = sv.ShowPhase;
                    Seen.Add(phase0);
                }
                bool active = on();
                if (active && first < 0) first = Time.realtimeSinceStartup;
                if (active && Time.realtimeSinceStartup - last >= 0.12f)
                {
                    last = Time.realtimeSinceStartup;
                    yield return new WaitForEndOfFrame();
                    var tex = ScreenCapture.CaptureScreenshotAsTexture();
                    if (tex)
                    {
                        File.WriteAllBytes(Path.Combine(Dir, $"{tag}_{n:000}.png"), tex.EncodeToPNG());
                        Object.DestroyImmediate(tex);
                    }
                    Log($"  {tag}_{n:000} t={last - t0:0.00}s pha='{sv.ShowPhase}' chết={sv.IsDown(0)}/{sv.IsDown(1)} " +
                        $"ra sân={sv.IsEntering(0)}/{sv.IsEntering(1)} clip={sv.ClipOf(0)}/{sv.ClipOf(1)} máu: {HpLabels()}");
                    n++;
                    continue;
                }
                if (first >= 0 && done())
                {
                    Log($"  {tag}: xong sau {Time.realtimeSinceStartup - first:0.00}s từ lúc bắt đầu chụp, {n} khung");
                    yield return new WaitForSecondsRealtime(0.4f);
                    yield break;
                }
                yield return null;
            }
            Log($"  {tag}: hết {max} giây, {n} khung (chưa thấy kết thúc: soi nhật ký)");
        }
    }
}
