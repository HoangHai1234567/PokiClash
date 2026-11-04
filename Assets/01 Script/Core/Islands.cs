// Hệ thống 70 ải (chép Web/src/core/data/islands.ts, minions.ts và phần ải của stages.ts, progression.ts):
// - cỡ đảo, ải mini boss đầu, rương mốc theo đảo (zoneSize, zoneMiniAt, ZONE_CHESTS); GameData.Index() điền lại từ danh sách ải;
// - phần cộng của địch trong ải (enemyMods): cường hóa của ải, độ yếu của lính; đảo 70 ải còn quy độ hiếm của địch về Khá
//   và giảm máu, công của mini boss, boss (nếu không, từ ải 20 tướng Hiếm, Sử thi, Huyền thoại thắng gần như mọi trận).
// Đảo có ải mang kiểu (StageDef.tag) là đảo 70 ải (hiện chỉ Đảo Thủy, danh sách ải nằm sẵn trong stages.json); đảo khác 8 ải.
// Thiết kế và số đo: GD_Claude/14_HeThongAi.md.
using System.Linq;

namespace PokiClash.Core
{
    public static class Islands
    {
        // lính yếu hơn tướng cùng cấp (MINION_POWER)
        public const double MinionHp = 0.85, MinionAtk = 0.9, MinionDef = 0.9;

        // đảo 70 ải: địch mọi độ hiếm có sức như tướng Khá; máu mini boss ×0,95, boss cuối đảo (tiến hóa) ×0,7, công của cả hai ×0,95
        // (ENEMY_NORM; miniAtk của web không dùng tới)
        public const Rarity NormRarity = Rarity.Uncommon;
        public const double MiniHp = 0.95, BossHp = 0.7, BossAtk = 0.95;

        // đảo 70 ải, thang cấp 200 (2026-11-04): địch có sao và cấp thẻ như người chơi bình thường cùng cấp (Teams.EnemyStar, EnemyCard),
        // nên Máu, Công nhân thêm hệ số này để % cường hóa từng kiểu ải giữ như thiết kế mà tỉ lệ thắng vẫn đạt mục tiêu
        public const double LevelNorm = 0.8;

        static readonly string[] TagNames = { "", "Tướng mới", "Bầy lính", "Cường hóa", "Tướng và lính", "Hai tướng", "Lính tinh nhuệ", "Cửa ải" };
        public static string TagName(StageTag t) => TagNames[(int)t];

        static readonly int[] OldChests = { 4, 8 };
        static int[] size = { 8, 8, 8, 8, 8 };
        static int[] miniAt = { 4, 4, 4, 4, 4 };
        static bool[] isLong = new bool[5];
        static int[][] chests = { OldChests, OldChests, OldChests, OldChests, OldChests };

        // điền cỡ đảo, mini boss đầu, rương mốc từ danh sách ải (GameData.Index gọi)
        public static void Bind(GameData d)
        {
            foreach (var e in Elements.All)
            {
                var st = d.ZoneStages(e).ToList();
                int i = (int)e;
                size[i] = st.Count;
                miniAt[i] = st.FirstOrDefault(x => x.kind == StageKind.Mini)?.idx ?? 4;
                isLong[i] = st.Any(x => x.tag != StageTag.None);
                chests[i] = isLong[i] ? st.Where(x => x.idx % 10 == 0).Select(x => x.idx).ToArray() : OldChests;
            }
        }

        // số ải của đảo (70 hoặc 8)
        public static int Size(Elem z) => size[(int)z];

        // ải mini boss đầu tiên (Đền Huy Hiệu mở dãy của hệ khi qua ải này)
        public static int MiniAt(Elem z) => miniAt[(int)z];

        // đảo 70 ải (màn đảo vẽ đường mòn có mốc và chấm)
        public static bool IsLong(Elem z) => isLong[(int)z];

        // số ải phải qua để mở từng rương mốc: đảo 8 ải 4 và 8; đảo 70 ải mỗi 10 ải (7 rương)
        public static int[] Chests(Elem z) => chests[(int)z];

        // phần cộng của địch e trong ải (long: ải của đảo 70 ải); không có gì thì null (để số khớp bản web từng bit)
        public static StatMods EnemyMods(GameData d, StageEnemy e, bool @long)
        {
            var h = d.Hero(e.hero);
            double b = e.buff;
            double hp = 1 + b, atk = 1 + b, def = 1 + b / 2;
            if (h.minion)
            {
                hp *= MinionHp;
                atk *= MinionAtk;
                def *= MinionDef;
            }
            if (@long)
            {
                double r = HeroStats.PowerOf(NormRarity) / HeroStats.PowerOf(h.rarity);
                hp *= r * (e.boss ? (e.evo ? BossHp : MiniHp) : 1) * LevelNorm;
                atk *= r * (e.boss ? BossAtk : 1) * LevelNorm;
                def *= r;
            }
            if (hp == 1 && atk == 1 && def == 1) return null;
            return new StatMods { hpPct = hp - 1, atkPct = atk - 1, defPct = def - 1, spd = 0 };
        }
    }
}
