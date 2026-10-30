// Trận 1 đấu 1 dùng chung cho bàn khối (A) và bàn ngọc (C). Màu là hành động: 0 Đỏ đánh, 1 Lam khiên, 2 Lục hồi, 3 Vàng nộ.
using UnityEngine;

namespace PokiWar.BanThu
{
    public enum EnemyAct { Attack, Stones }

    public struct Gain
    {
        public int Damage, Shield, Heal, Rage;
    }

    public sealed class Battle
    {
        // số đề xuất ban đầu (GD_Claude/10_BanThu_1v1.md), chỉnh khi chơi thử
        public const int HeroMaxHp = 400, EnemyMaxHp = 600, EnemyAtk = 55, EnemyEvery = 3, StoneCount = 3;
        public const int RedDamage = 10, BlueShield = 6, GreenHeal = 5, YellowRage = 10, SkillDamage = 150;
        public const int ShieldCap = 40; // khiên không cộng dồn mãi, nếu không tướng gần như bất tử
        public const float StunHpPart = 0.2f;

        public int HeroHp = HeroMaxHp, EnemyHp = EnemyMaxHp, Shield, Rage, Countdown = EnemyEvery, Turns;
        int enemyActions;

        public bool Over => HeroHp <= 0 || EnemyHp <= 0;
        public bool Won => EnemyHp <= 0;
        public bool CanCast => Rage >= 100 && !Over;
        // địch: đánh, đánh, ném đá, lặp lại; luôn báo trước
        public EnemyAct NextAct => enemyActions % 3 == 2 ? EnemyAct.Stones : EnemyAct.Attack;

        public Gain Apply(int[] counts, float mult)
        {
            var g = new Gain
            {
                Damage = Mathf.RoundToInt(counts[0] * RedDamage * mult),
                Shield = Mathf.Min(ShieldCap - Shield, Mathf.RoundToInt(counts[1] * BlueShield * mult)),
                Heal = Mathf.Min(HeroMaxHp - HeroHp, Mathf.RoundToInt(counts[2] * GreenHeal * mult)),
                Rage = Mathf.Min(100 - Rage, Mathf.RoundToInt(counts[3] * YellowRage * mult)),
            };
            EnemyHp = Mathf.Max(0, EnemyHp - g.Damage);
            Shield += g.Shield;
            HeroHp += g.Heal;
            Rage += g.Rage;
            return g;
        }

        public int Cast()
        {
            Rage = 0;
            int d = Mathf.Min(EnemyHp, SkillDamage);
            EnemyHp -= d;
            return d;
        }

        // hết một lượt của người chơi; trả về hành động của địch nếu tới lượt nó
        public EnemyAct? EndTurn()
        {
            Turns++;
            if (Over || --Countdown > 0) return null;
            Countdown = EnemyEvery;
            var act = NextAct;
            enemyActions++;
            return act;
        }

        // trả về (máu mất, phần khiên chặn)
        public (int lost, int blocked) EnemyAttack()
        {
            int blocked = Mathf.Min(Shield, EnemyAtk);
            Shield = 0;
            int lost = Mathf.Min(HeroHp, EnemyAtk - blocked);
            HeroHp -= lost;
            return (lost, blocked);
        }

        public int Stun()
        {
            int lost = Mathf.Min(HeroHp, Mathf.RoundToInt(HeroMaxHp * StunHpPart));
            HeroHp -= lost;
            return lost;
        }
    }

    // một đợt xoá trên bàn (xoá đường ở A, ghép ở C); bàn sập hay dây chuyền thì có nhiều đợt, Chain tăng dần
    public sealed class Step
    {
        public readonly System.Collections.Generic.List<Vector2Int> Cleared = new();
        public readonly int[] Counts = new int[4];
        public int Lines, Chain;
        public int[,] After;
    }
}
