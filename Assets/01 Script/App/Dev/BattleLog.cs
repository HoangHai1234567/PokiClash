#if UNITY_EDITOR || DEVELOPMENT_BUILD
// Ghi trận (chỉ Editor và bản Development): mỗi trận kết thúc thêm một dòng vào Logs/tran.csv.
// Editor: thư mục Logs của project (ngoài Assets); máy thật: persistentDataPath/Logs. Bản phát hành không có lớp này.
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using PokiClash.Core;
using UnityEngine;

namespace PokiClash
{
    public static class BattleLog
    {
        const string Header = "thoi_diem,dao,ai,ten_ai,doi,cap,ket_qua,hiep,giay,mau_con_pct,tu_choi";

        public static string FilePath =>
            Application.isEditor ? Path.GetFullPath(Path.Combine(Application.dataPath, "../Logs/tran.csv"))
                : Path.Combine(Application.persistentDataPath, "Logs", "tran.csv");

        static string Q(string s) => "\"" + s.Replace("\"", "\"\"") + "\"";

        // result: "thang", "thua" hoặc "bo" (bỏ trận); hpPct: tổng máu còn / tổng máu tối đa của đội người chơi, 0..100
        public static void Write(ZoneDef zone, StageDef stage, IEnumerable<string> team, int level, string result, int rounds, float seconds, double hpPct, bool auto)
        {
            try
            {
                var path = FilePath;
                Directory.CreateDirectory(Path.GetDirectoryName(path));
                bool fresh = !File.Exists(path);
                var line = string.Join(",",
                    DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture), Keys.Of(zone.id), stage.idx, Q(stage.name),
                    Q(string.Join(" + ", team)), level, result, rounds, seconds.ToString("0.0", CultureInfo.InvariantCulture),
                    hpPct.ToString("0", CultureInfo.InvariantCulture), auto ? 1 : 0);
                File.AppendAllText(path, (fresh ? Header + "\n" : "") + line + "\n", new UTF8Encoding(fresh));
            }
            catch (Exception e)
            {
                Debug.LogWarning("[Ghi trận] " + e.Message);
            }
        }

        public static double HpPct(Battle b)
        {
            var fs = b.sides[0].fighters;
            double max = fs.Sum(f => f.maxHp);
            return max > 0 ? fs.Sum(f => Math.Max(0, f.hp)) / max * 100 : 0;
        }
    }
}
#endif
