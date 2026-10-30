// Bàn C: xếp ngọc 7 × 7 kiểu Pokiwar. Đổi chỗ hai ngọc kề nhau, 3 ngọc cùng màu thẳng hàng thì ghép, ngọc rơi và dây chuyền.
using System.Collections.Generic;
using UnityEngine;

namespace PokiWar.BanThu
{
    public sealed class GemBoard
    {
        public const int W = 7, H = 7, Empty = -1, Stone = 4;

        public readonly int[,] Cells = new int[W, H]; // [x, y], y = 0 là hàng trên
        readonly System.Random rng;

        public GemBoard(int seed)
        {
            rng = new System.Random(seed);
            Fill();
        }

        void Fill()
        {
            do
            {
                for (int y = 0; y < H; y++)
                    for (int x = 0; x < W; x++)
                        Cells[x, y] = FreshColor(x, y);
            } while (!HasMove());
        }

        // màu không tạo sẵn hàng 3 với hai ô bên trái và hai ô bên trên
        int FreshColor(int x, int y)
        {
            int c;
            do c = rng.Next(4);
            while ((x >= 2 && Cells[x - 1, y] == c && Cells[x - 2, y] == c) ||
                   (y >= 2 && Cells[x, y - 1] == c && Cells[x, y - 2] == c));
            return c;
        }

        bool IsGem(int x, int y) => Cells[x, y] >= 0 && Cells[x, y] < 4;

        bool[,] FindMatches(out bool any)
        {
            var m = new bool[W, H];
            any = false;
            for (int y = 0; y < H; y++)
                for (int x = 0; x < W;)
                {
                    int end = x + 1;
                    while (IsGem(x, y) && end < W && Cells[end, y] == Cells[x, y]) end++;
                    if (IsGem(x, y) && end - x >= 3) { for (int k = x; k < end; k++) m[k, y] = true; any = true; }
                    x = end;
                }
            for (int x = 0; x < W; x++)
                for (int y = 0; y < H;)
                {
                    int end = y + 1;
                    while (IsGem(x, y) && end < H && Cells[x, end] == Cells[x, y]) end++;
                    if (IsGem(x, y) && end - y >= 3) { for (int k = y; k < end; k++) m[x, k] = true; any = true; }
                    y = end;
                }
            return m;
        }

        void Swap(Vector2Int a, Vector2Int b) => (Cells[a.x, a.y], Cells[b.x, b.y]) = (Cells[b.x, b.y], Cells[a.x, a.y]);

        static bool Inside(Vector2Int p) => p.x >= 0 && p.y >= 0 && p.x < W && p.y < H;

        // null nếu đổi chỗ không ghép được (không tính lượt)
        public List<Step> TrySwap(Vector2Int a, Vector2Int b)
        {
            if (!Inside(a) || !Inside(b) || Mathf.Abs(a.x - b.x) + Mathf.Abs(a.y - b.y) != 1) return null;
            if (!IsGem(a.x, a.y) || !IsGem(b.x, b.y)) return null;
            Swap(a, b);
            FindMatches(out bool any);
            if (!any) { Swap(a, b); return null; }
            return Resolve();
        }

        List<Step> Resolve()
        {
            var steps = new List<Step>();
            for (int chain = 0; ; chain++)
            {
                var m = FindMatches(out bool any);
                if (!any) break;
                var st = new Step { Chain = chain };
                var gone = new bool[W, H];
                for (int y = 0; y < H; y++)
                    for (int x = 0; x < W; x++)
                    {
                        if (!m[x, y]) continue;
                        st.Counts[Cells[x, y]]++;
                        gone[x, y] = true;
                        // đá bên cạnh ô ghép thì vỡ (không cho gì)
                        foreach (var d in Dirs)
                        {
                            var n = new Vector2Int(x + d.x, y + d.y);
                            if (Inside(n) && Cells[n.x, n.y] == Stone) gone[n.x, n.y] = true;
                        }
                    }
                for (int y = 0; y < H; y++)
                    for (int x = 0; x < W; x++)
                        if (gone[x, y]) { Cells[x, y] = Empty; st.Cleared.Add(new Vector2Int(x, y)); }
                st.Lines = 1;
                Fall();
                st.After = Snapshot();
                steps.Add(st);
            }
            return steps;
        }

        static readonly Vector2Int[] Dirs = { Vector2Int.right, Vector2Int.left, Vector2Int.up, Vector2Int.down };

        void Fall()
        {
            for (int x = 0; x < W; x++)
            {
                int write = H - 1;
                for (int y = H - 1; y >= 0; y--)
                {
                    if (Cells[x, y] == Empty) continue;
                    int v = Cells[x, y];
                    Cells[x, y] = Empty;
                    Cells[x, write--] = v;
                }
                for (int y = write; y >= 0; y--) Cells[x, y] = rng.Next(4);
            }
        }

        public bool HasMove() => Moves(true).Count > 0;

        // các cặp đổi chỗ ghép được; dùng cho máy tự chơi
        public List<(Vector2Int a, Vector2Int b)> Moves(bool firstOnly = false)
        {
            var list = new List<(Vector2Int, Vector2Int)>();
            for (int y = 0; y < H; y++)
                for (int x = 0; x < W; x++)
                    foreach (var d in new[] { Vector2Int.right, Vector2Int.up })
                    {
                        var a = new Vector2Int(x, y);
                        var b = new Vector2Int(x + d.x, y + d.y);
                        if (!Inside(b) || !IsGem(a.x, a.y) || !IsGem(b.x, b.y)) continue;
                        Swap(a, b);
                        FindMatches(out bool any);
                        Swap(a, b);
                        if (!any) continue;
                        list.Add((a, b));
                        if (firstOnly) return list;
                    }
            return list;
        }

        // hết nước đi thì xáo màu ngọc, đá giữ nguyên chỗ
        public void Shuffle()
        {
            for (int tries = 0; tries < 50; tries++)
            {
                for (int y = 0; y < H; y++)
                    for (int x = 0; x < W; x++)
                        if (Cells[x, y] != Stone) Cells[x, y] = FreshColor(x, y);
                if (HasMove()) return;
            }
            Fill();
        }

        public List<Vector2Int> AddStones(int n)
        {
            var gems = new List<Vector2Int>();
            for (int y = 0; y < H; y++)
                for (int x = 0; x < W; x++)
                    if (IsGem(x, y)) gems.Add(new Vector2Int(x, y));
            var put = new List<Vector2Int>();
            for (int i = 0; i < n && gems.Count > 0; i++)
            {
                int k = rng.Next(gems.Count);
                var c = gems[k];
                gems.RemoveAt(k);
                Cells[c.x, c.y] = Stone;
                put.Add(c);
            }
            return put;
        }

        // đá thành ngọc; ngọc mới có thể ghép với ô bên phải hoặc bên dưới, nên trả về các đợt ghép phát sinh
        public List<Step> RemoveStones()
        {
            for (int y = 0; y < H; y++)
                for (int x = 0; x < W; x++)
                    if (Cells[x, y] == Stone) Cells[x, y] = FreshColor(x, y);
            return Resolve();
        }

        public int[,] Snapshot() => (int[,])Cells.Clone();
    }
}
