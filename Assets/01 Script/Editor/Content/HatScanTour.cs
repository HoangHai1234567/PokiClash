// Quét ảnh hạt từng tướng dùng (GD_Claude/27, mốc T4: tách atlas hạt theo hệ). Menu "PokiClash/Tải sau/Quét ảnh hạt từng tướng" hoặc
// cờ Temp/hat_scan.flag (Unity không Play thì tự vào Play). Mỗi tướng (sao cuối, đội một mình) vào ải 3: đòn thường, chiêu mana (kèm
// tia), chiêu cuối (kèm UltFx); HatLua.Used ghi mọi tên ảnh được lấy trong lúc tướng đó diễn. Ghi Assets/03 Art/Fx/hat_dung.json
// ({"heroes": {id: [tên ảnh]}}), ContentPackSetup.ApplyHat đọc để chia ảnh: chỉ tướng cùng một hệ (không phải tướng khởi đầu) dùng thì
// vào gói hệ đó; dùng chung, tướng khởi đầu dùng, hoặc chưa thấy ai dùng thì ở bản cài. Sao lưu bản lưu, xong trả lại rồi Stop.
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Core;
using UnityEditor;
using UnityEngine;

namespace PokiClash.EditorTools
{
    public static class HatScanTour
    {
        public const string OutPath = "Assets/03 Art/Fx/hat_dung.json";
        static double nextPoll, tourStart;
        static string Flag => Path.GetFullPath(Path.Combine(Application.dataPath, "../Temp/hat_scan.flag"));

        [MenuItem("PokiClash/Tải sau/Quét ảnh hạt từng tướng (khoảng 10 phút)", priority = 171)]
        static void Run()
        {
            if (EditorApplication.isPlaying)
            {
                if (App.I != null) App.I.StartCoroutine(Tour());
                return;
            }
            File.WriteAllText(Flag, "1");
        }

        [InitializeOnLoadMethod]
        static void Hook() => EditorApplication.update += Poll;

        static void Poll()
        {
            if (EditorApplication.timeSinceStartup < nextPoll) return;
            nextPoll = EditorApplication.timeSinceStartup + 1;
            if (EditorApplication.isCompiling || EditorApplication.isUpdating) return;
            if (!EditorApplication.isPlayingOrWillChangePlaymode)
            {
                if (!File.Exists(Flag)) return;
                File.Delete(Flag);
                SessionState.SetBool("HatScanTour", true);
                tourStart = EditorApplication.timeSinceStartup;
                EditorApplication.isPlaying = true;
                return;
            }
            if (tourStart > 0 && EditorApplication.timeSinceStartup - tourStart > 1500)
            {
                Debug.LogWarning("[Quét hạt] Quá 25 phút: dừng Play.");
                tourStart = 0;
                EditorApplication.isPlaying = false;
                return;
            }
            if (EditorApplication.isPlaying && SessionState.GetBool("HatScanTour", false) && App.I != null && App.Router != null && App.Router.CurrentRoot != null)
            {
                SessionState.SetBool("HatScanTour", false);
                BootTitle.Dismiss();
                App.I.StartCoroutine(Tour());
            }
        }

        static IEnumerator Tour()
        {
            var path = App.Save.FilePath;
            string backup = File.Exists(path) ? File.ReadAllText(path) : null;
            var used = new Dictionary<string, SortedSet<string>>();
            string cur = null;
            HatLua.Used = n =>
            {
                if (cur == null) return;
                if (!used.TryGetValue(cur, out var set)) used[cur] = set = new SortedSet<string>();
                set.Add(n);
            };
            int done = 0, failed = 0;
            try
            {
                var heroes = App.Data.Heroes.Select(h => h.id).ToList();
                foreach (var hero in heroes)
                {
                    var s = App.Save.Data;
                    var hp = s.Hero(hero);
                    if (hp == null) continue;
                    hp.owned = true;
                    hp.star = App.Data.Cfg.maxStar;
                    s.team = new List<string> { hero };
                    if (s.level < 7) s.level = 7;
                    App.Router.Go(SceneIds.Battle, new BattleArgs { stageId = 3 });
                    float t0 = Time.realtimeSinceStartup;
                    yield return null;
                    while ((App.Router.Busy || App.Router.Current != SceneIds.Battle) && Time.realtimeSinceStartup - t0 < 30) yield return null;
                    var ctl = Object.FindAnyObjectByType<BattleController>();
                    var st = Object.FindAnyObjectByType<StageView>();
                    if (!ctl || !st)
                    {
                        Debug.LogWarning($"[Quét hạt] {hero}: không vào được trận");
                        failed++;
                        continue;
                    }
                    st.speed = 1;
                    t0 = Time.realtimeSinceStartup;
                    while (!ctl.WaitingPlayer && Time.realtimeSinceStartup - t0 < 20) yield return null;
                    yield return new WaitForSecondsRealtime(0.4f);
                    cur = hero;
                    st.Play(0, StageView.Attack);
                    yield return new WaitForSecondsRealtime(2.0f);
                    st.Play(0, StageView.Cast, () => st.Beam(0));
                    yield return new WaitForSecondsRealtime(3.0f);
                    st.Play(0, StageView.Skill, () => st.UltFx(0));
                    yield return new WaitForSecondsRealtime(4.2f);
                    cur = null;
                    done++;
                    Debug.Log($"[Quét hạt] {hero}: {(used.TryGetValue(hero, out var u) ? u.Count : 0)} ảnh ({done}/{heroes.Count})");
                }
            }
            finally
            {
                HatLua.Used = null;
                if (backup != null)
                {
                    File.WriteAllText(path, backup);
                    App.Save.Load();
                }
            }
            // ghi JSON (thứ tự cố định để git so được)
            var sb = new StringBuilder("{\n \"heroes\": {\n");
            var ids = used.Keys.OrderBy(k => k).ToList();
            for (int i = 0; i < ids.Count; i++)
                sb.Append($"  \"{ids[i]}\": [{string.Join(", ", used[ids[i]].Select(n => "\"" + n + "\""))}]{(i < ids.Count - 1 ? "," : "")}\n");
            sb.Append(" }\n}\n");
            File.WriteAllText(OutPath, sb.ToString());
            AssetDatabase.ImportAsset(OutPath);
            App.Router.Go(SceneIds.Hub);
            Debug.Log($"[Quét hạt] Xong: {done} tướng, {failed} lỗi, {used.Values.SelectMany(x => x).Distinct().Count()} ảnh khác nhau → {OutPath}");
            tourStart = 0;
            EditorApplication.isPlaying = false;
        }
    }
}
