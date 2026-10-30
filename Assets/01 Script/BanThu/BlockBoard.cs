// Bàn A: xếp khối 8 × 8 kiểu Block Blast, mỗi khối một màu hành động; Gravity bật thì ô rơi sau khi xoá (bản "sập").
using System.Collections.Generic;
using UnityEngine;

namespace PokiWar.BanThu
{
    public sealed class Shape
    {
        public readonly Vector2Int[] Cells;
        public readonly int W, H;

        public Shape(Vector2Int[] cells)
        {
            Cells = cells;
            foreach (var c in cells) { W = Mathf.Max(W, c.x + 1); H = Mathf.Max(H, c.y + 1); }
        }
    }

    public static class Shapes
    {
        // hình gốc, xoay đủ 4 hướng; chữ L 4 ô và chữ Z lấy thêm bản lật
        static readonly (string pattern, bool mirror)[] Bases =
        {
            ("X", false), ("XX", false), ("XXX", false), ("XXXX", false), ("XXXXX", false),
            ("XX/XX", false), ("XXX/XXX/XXX", false), ("XXX/XXX", false),
            ("XX/X.", false), ("XXX/X..", true), ("XXX/.X.", false), ("XX./.XX", true), ("X../X../XXX", false),
        };

        public static readonly List<List<Shape>> Groups = new();
        public static readonly Shape Single;

        static Shapes()
        {
            foreach (var (pattern, mirror) in Bases)
            {
                var cells = Parse(pattern);
                var seen = new HashSet<string>();
                var group = new List<Shape>();
                for (int m = 0; m < (mirror ? 2 : 1); m++)
                {
                    var cur = m == 0 ? cells : Normalize(cells.ConvertAll(c => new Vector2Int(-c.x, c.y)));
                    for (int r = 0; r < 4; r++)
                    {
                        string key = Key(cur);
                        if (seen.Add(key)) group.Add(new Shape(cur.ToArray()));
                        cur = Normalize(cur.ConvertAll(c => new Vector2Int(-c.y, c.x)));
                    }
                }
                Groups.Add(group);
            }
            Single = Groups[0][0];
        }

        public static Shape Random(System.Random rng)
        {
            var g = Groups[rng.Next(Groups.Count)];
            return g[rng.Next(g.Count)];
        }

        static List<Vector2Int> Parse(string p)
        {
            var list = new List<Vector2Int>();
            var rows = p.Split('/');
            for (int y = 0; y < rows.Length; y++)
                for (int x = 0; x < rows[y].Length; x++)
                    if (rows[y][x] == 'X') list.Add(new Vector2Int(x, y));
            return list;
        }

        static List<Vector2Int> Normalize(List<Vector2Int> cells)
        {
            int mx = int.MaxValue, my = int.MaxValue;
            foreach (var c in cells) { mx = Mathf.Min(mx, c.x); my = Mathf.Min(my, c.y); }
            var list = cells.ConvertAll(c => new Vector2Int(c.x - mx, c.y - my));
            list.Sort((a, b) => a.y != b.y ? a.y.CompareTo(b.y) : a.x.CompareTo(b.x));
            return list;
        }

        static string Key(List<Vector2Int> cells) => string.Join(";", cells.ConvertAll(c => c.x + "," + c.y));
    }

    public sealed class Piece
    {
        public Shape Shape;
        public int Color;
        public bool Used;
    }

    public sealed class BlockBoard
    {
        public const int N = 8, Empty = -1, Stone = 4;

        public readonly int[,] Cells = new int[N, N]; // [x, y], y = 0 là hàng trên
        public readonly Piece[] Hand = new Piece[3];
        public readonly bool Gravity;
        public int Combo;
        int dry;
        readonly System.Random rng;

        public BlockBoard(int seed, bool gravity)
        {
            rng = new System.Random(seed);
            Gravity = gravity;
            for (int x = 0; x < N; x++)
                for (int y = 0; y < N; y++)
                    Cells[x, y] = Empty;
            NewHand(false);
        }

        public bool CanPlace(Shape s, int x, int y)
        {
            foreach (var c in s.Cells)
            {
                int cx = x + c.x, cy = y + c.y;
                if (cx < 0 || cy < 0 || cx >= N || cy >= N || Cells[cx, cy] != Empty) return false;
            }
            return true;
        }

        public bool Fits(Shape s)
        {
            for (int y = 0; y <= N - s.H; y++)
                for (int x = 0; x <= N - s.W; x++)
                    if (CanPlace(s, x, y)) return true;
            return false;
        }

        // số hàng + cột đầy nếu đặt khối ở (x, y); dùng cho máy tự chơi
        public int LinesIfPlaced(Shape s, int x, int y)
        {
            var mine = new HashSet<Vector2Int>();
            foreach (var c in s.Cells) mine.Add(new Vector2Int(x + c.x, y + c.y));
            int lines = 0;
            for (int i = 0; i < N; i++)
            {
                bool row = true, col = true;
                for (int k = 0; k < N; k++)
                {
                    row &= Cells[k, i] != Empty || mine.Contains(new Vector2Int(k, i));
                    col &= Cells[i, k] != Empty || mine.Contains(new Vector2Int(i, k));
                }
                if (row) lines++;
                if (col) lines++;
            }
            return lines;
        }

        public bool AnyFits()
        {
            foreach (var p in Hand)
                if (!p.Used && Fits(p.Shape)) return true;
            return false;
        }

        // đặt khối; placed = bàn ngay sau khi đặt (trước khi xoá), để hiện cho người chơi thấy
        public List<Step> Place(int handIndex, int x, int y, out int[,] placed)
        {
            var p = Hand[handIndex];
            foreach (var c in p.Shape.Cells) Cells[x + c.x, y + c.y] = p.Color;
            p.Used = true;
            placed = Snapshot();

            var steps = Resolve();
            if (steps.Count > 0) { Combo++; dry = 0; }
            else if (++dry >= 3) { Combo = 0; dry = 0; } // ba lượt liền không xoá thì mất combo, như Block Blast

            if (Hand[0].Used && Hand[1].Used && Hand[2].Used) NewHand(false);
            return steps;
        }

        List<Step> Resolve()
        {
            var steps = new List<Step>();
            for (int chain = 0; ; chain++)
            {
                var full = new bool[N, N];
                int lines = 0;
                for (int y = 0; y < N; y++)
                {
                    bool row = true;
                    for (int x = 0; x < N && row; x++) row = Cells[x, y] != Empty;
                    if (!row) continue;
                    lines++;
                    for (int x = 0; x < N; x++) full[x, y] = true;
                }
                for (int x = 0; x < N; x++)
                {
                    bool col = true;
                    for (int y = 0; y < N && col; y++) col = Cells[x, y] != Empty;
                    if (!col) continue;
                    lines++;
                    for (int y = 0; y < N; y++) full[x, y] = true;
                }
                if (lines == 0) break;

                var st = new Step { Lines = lines, Chain = chain };
                for (int y = 0; y < N; y++)
                    for (int x = 0; x < N; x++)
                    {
                        if (!full[x, y]) continue;
                        int v = Cells[x, y];
                        if (v >= 0 && v < 4) st.Counts[v]++;
                        Cells[x, y] = Empty;
                        st.Cleared.Add(new Vector2Int(x, y));
                    }
                if (Gravity) Fall();
                st.After = Snapshot();
                steps.Add(st);
                if (!Gravity) break; // không sập thì xoá xong là bàn đứng yên
            }
            return steps;
        }

        // từng ô rơi thẳng xuống tới khi chạm đáy hoặc chạm ô khác
        void Fall()
        {
            for (int x = 0; x < N; x++)
            {
                int write = N - 1;
                for (int y = N - 1; y >= 0; y--)
                {
                    if (Cells[x, y] == Empty) continue;
                    int v = Cells[x, y];
                    Cells[x, y] = Empty;
                    Cells[x, write--] = v;
                }
            }
        }

        // rescue: cả 3 khối đều phải đặt được (tay "cứu" sau khi choáng)
        public void NewHand(bool rescue)
        {
            for (int i = 0; i < 3; i++)
                Hand[i] = new Piece { Shape = Shapes.Random(rng), Color = rng.Next(4) };
            for (int i = 0; i < (rescue ? 3 : 1); i++)
            {
                int tries = 0;
                while (!Fits(Hand[i].Shape) && tries++ < 40) Hand[i].Shape = Shapes.Random(rng);
                if (!Fits(Hand[i].Shape)) Hand[i].Shape = Shapes.Single;
            }
            int j = rng.Next(3); // khối chắc chắn đặt được không phải lúc nào cũng ở ô đầu
            (Hand[0], Hand[j]) = (Hand[j], Hand[0]);
        }

        // hết chỗ: nổ vùng 4 × 4 giữa bàn, ra tay mới đặt được
        public void Stun()
        {
            for (int y = 2; y < 6; y++)
                for (int x = 2; x < 6; x++)
                    Cells[x, y] = Empty;
            NewHand(true);
        }

        public List<Vector2Int> AddStones(int n)
        {
            var empty = new List<Vector2Int>();
            for (int y = 0; y < N; y++)
                for (int x = 0; x < N; x++)
                    if (Cells[x, y] == Empty) empty.Add(new Vector2Int(x, y));
            var put = new List<Vector2Int>();
            for (int i = 0; i < n && empty.Count > 0; i++)
            {
                int k = rng.Next(empty.Count);
                var c = empty[k];
                empty.RemoveAt(k);
                Cells[c.x, c.y] = Stone;
                put.Add(c);
            }
            return put;
        }

        public void RemoveStones()
        {
            for (int y = 0; y < N; y++)
                for (int x = 0; x < N; x++)
                    if (Cells[x, y] == Stone) Cells[x, y] = Empty;
        }

        public int[,] Snapshot() => (int[,])Cells.Clone();
    }
}
