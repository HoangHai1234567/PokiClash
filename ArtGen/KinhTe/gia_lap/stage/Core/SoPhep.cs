// Sổ Phép: cây kỹ năng cấp tài khoản của cậu bé thuần thú sư (GD_Claude/28_SoPhep.md; nghiên cứu GD_Claude/reports/Cây kỹ năng cho
// PokiClash.md; người dùng duyệt "Làm theo bạn đề xuất" 2026-11-24). 4 chương × 5 ô, mua bằng nét; ô đổi luật trận (rút, chọn thẻ, đổi
// tướng, khắc hệ, cứu nguy) chứ không cộng % chỉ số, không có ô kinh tế. Ô chốt cuối chương 2–4 tốn thêm đá tiến hóa (đang dư).
// Nét: 3 khi mở sổ (cấp 50) + 1 ở mỗi cấp tận cùng 3, 8 từ 53 tới 198 (30 nét) + EXP thừa sau cấp 200 (27.000 EXP một nét, tối đa 7):
// nét tính lại từ cấp và số nét EXP đã đổi, không lưu. Tẩy sổ miễn phí: hoàn hết nét và đá. Ô chọn đổi mặt bất cứ lúc nào ngoài trận.
// Số trên ô ở balance.json khối "sophep" (BalanceConfig.sophep), chữ mô tả ở Describe. Hiệu ứng trong trận: BattleRules (Battle.cs).
using System;
using System.Collections.Generic;
using System.Linq;

namespace PokiClash.Core
{
    // kind: "lv" ô cấp (giá theo cấp), "one" ô đơn, "pick" ô chọn (hai mặt), "cap" ô chốt (chọn, tốn đá), "elem" chọn 1 trong 5 hệ,
    // "deco" trang trí (không cộng sức)
    [Serializable]
    public class SoPhepNode
    {
        public string id, name, kind, icon; // icon: tên icon trong bộ Fallback/Icons (tạm, chờ icon vẽ tay)
        public int ch; // chương 0..3
        public List<int> cost = new List<int>(); // giá nét theo cấp; ô không phải "lv" chỉ một phần tử
        public int stones; // đá tiến hóa (ô chốt), trả một lần
        public List<string> faces = new List<string>(); // tên hai mặt (pick, cap)
        public List<double> v = new List<double>(); // số của ô (ý nghĩa theo id, xem SoPhep.Rules)

        public string Name => Loc.T(name);
        public int MaxLv => Math.Max(1, cost.Count);
        public bool IsCap => kind == "cap";
        public bool IsElem => kind == "elem";
        public int FaceCount => IsElem ? Elements.All.Length : faces.Count;
        public string FaceName(int i) => IsElem ? Elements.Name(Elements.All[Math.Max(0, Math.Min(i, Elements.All.Length - 1))]) :
            i >= 0 && i < faces.Count ? Loc.T(faces[i]) : "";
    }

    [Serializable]
    public class SoPhepChapter
    {
        public string name;
        public int level, spent; // cổng: cấp người chơi, số nét đã vẽ
        public bool lord; // cổng: đã hạ chúa tể đầu tiên (boss ải cuối một đảo)
        public string Name => Loc.T(name);
    }

    [Serializable]
    public class SoPhepConfig
    {
        public int openLevel = 50, openPoints = 3, fromLevel = 53, toLevel = 198, expPerPoint = 27000, expPoints = 7;
        public int capNeed = 3; // ô chốt cần đã vẽ bấy nhiêu ô khác cùng chương
        public List<int> endDigits = new List<int> { 3, 8 };
        public List<SoPhepChapter> chapters = new List<SoPhepChapter>();
        public List<SoPhepNode> nodes = new List<SoPhepNode>();
        public List<string> path = new List<string>(); // đường gợi ý: "id" vẽ một cấp, "id:mặt" chọn mặt rồi vẽ

        public SoPhepNode Node(string id) => nodes.Find(n => n.id == id);

        public static SoPhepConfig Parse(Dictionary<string, object> o)
        {
            var c = new SoPhepConfig();
            if (o == null) return c;
            c.openLevel = J.Int(o, "openLevel", c.openLevel);
            c.openPoints = J.Int(o, "openPoints", c.openPoints);
            c.fromLevel = J.Int(o, "fromLevel", c.fromLevel);
            c.toLevel = J.Int(o, "toLevel", c.toLevel);
            c.expPerPoint = J.Int(o, "expPerPoint", c.expPerPoint);
            c.expPoints = J.Int(o, "expPoints", c.expPoints);
            c.capNeed = J.Int(o, "capNeed", c.capNeed);
            if (J.Arr(o, "endDigits") is var ed && ed.Count > 0) c.endDigits = ed.Select(x => (int)(double)x).ToList();
            foreach (var x in J.Arr(o, "chapters"))
            {
                var co = J.Obj(x);
                c.chapters.Add(new SoPhepChapter { name = J.Str(co, "name"), level = J.Int(co, "level"), spent = J.Int(co, "spent"), lord = J.Bool(co, "lord") });
            }
            foreach (var x in J.Arr(o, "nodes"))
            {
                var no = J.Obj(x);
                c.nodes.Add(new SoPhepNode
                {
                    id = J.Str(no, "id"), name = J.Str(no, "name"), kind = J.Str(no, "kind"), icon = J.Str(no, "icon"), ch = J.Int(no, "ch"),
                    stones = J.Int(no, "stones"),
                    cost = J.Arr(no, "cost").Select(v => (int)(double)v).ToList(),
                    faces = J.Arr(no, "faces").Select(v => (string)v).ToList(),
                    v = J.Arr(no, "v").Select(v => (double)v).ToList(),
                });
            }
            c.path = J.Arr(o, "path").Select(v => (string)v).ToList();
            return c;
        }
    }

    // trạng thái lưu (SaveData.sophep; null = chưa đụng tới sổ)
    public sealed class SoPhepState
    {
        public Dictionary<string, int> lv = new Dictionary<string, int>(); // cấp đã vẽ của từng ô
        public Dictionary<string, int> face = new Dictionary<string, int>(); // mặt đang chọn của ô chọn
        public int stones; // đá tiến hóa đã trả (hoàn khi tẩy)
        public int expPoints; // nét đã đổi từ EXP thừa sau cấp 200
        public double expBank; // EXP thừa đang góp cho nét kế

        public static SoPhepState Read(Dictionary<string, object> o)
        {
            if (o == null) return null;
            var s = new SoPhepState { stones = J.Int(o, "stones"), expPoints = J.Int(o, "expPts"), expBank = J.Num(o, "bank") };
            foreach (var kv in J.Obj(o, "lv") ?? new Dictionary<string, object>())
                if (kv.Value is double n) s.lv[kv.Key] = (int)n;
            foreach (var kv in J.Obj(o, "face") ?? new Dictionary<string, object>())
                if (kv.Value is double n) s.face[kv.Key] = (int)n;
            return s;
        }

        public Dictionary<string, object> Write() => new Dictionary<string, object>
        {
            ["lv"] = lv.ToDictionary(kv => kv.Key, kv => (object)(double)kv.Value),
            ["face"] = face.ToDictionary(kv => kv.Key, kv => (object)(double)kv.Value),
            ["stones"] = (double)stones, ["expPts"] = (double)expPoints, ["bank"] = expBank,
        };
    }

    public static class SoPhep
    {
        static SoPhepConfig C(BalanceConfig cfg) => cfg.sophep;

        public static bool Open(SaveData s, BalanceConfig cfg) => C(cfg).nodes.Count > 0 && s.level >= C(cfg).openLevel;

        // nét từ cấp: số cấp từ fromLevel tới min(level, toLevel) có chữ số tận cùng thuộc endDigits
        public static int LevelPoints(SoPhepConfig c, int level)
        {
            int n = 0;
            for (int l = c.fromLevel; l <= Math.Min(level, c.toLevel); l++)
                if (c.endDigits.Contains(l % 10)) n++;
            return n;
        }

        public static int Earned(SaveData s, BalanceConfig cfg)
        {
            if (!Open(s, cfg)) return 0;
            var c = C(cfg);
            return c.openPoints + LevelPoints(c, s.level) + Math.Min(c.expPoints, s.sophep?.expPoints ?? 0);
        }

        public static int Total(BalanceConfig cfg) => C(cfg).nodes.Sum(n => n.cost.Sum());
        public static int TotalStones(BalanceConfig cfg) => C(cfg).nodes.Sum(n => n.stones);
        public static int MaxPoints(BalanceConfig cfg) => C(cfg).openPoints + LevelPoints(C(cfg), C(cfg).toLevel) + C(cfg).expPoints;

        public static int Lv(SaveData s, string id) => s.sophep != null && s.sophep.lv.TryGetValue(id, out var v) ? v : 0;
        public static int Face(SaveData s, string id) => s.sophep != null && s.sophep.face.TryGetValue(id, out var v) ? v : 0;

        public static int Spent(SaveData s, BalanceConfig cfg)
        {
            int n = 0;
            foreach (var nd in C(cfg).nodes)
            {
                int l = Math.Min(Lv(s, nd.id), nd.MaxLv);
                for (int i = 0; i < l && i < nd.cost.Count; i++) n += nd.cost[i];
            }
            return n;
        }

        public static int Free(SaveData s, BalanceConfig cfg) => Math.Max(0, Earned(s, cfg) - Spent(s, cfg));

        // đã hạ chúa tể đầu tiên: xong ải cuối của một đảo bất kỳ
        public static bool LordBeaten(SaveData s) => Elements.All.Any(z => s.zones[(int)z] >= Islands.Size(z));

        public static bool ChapterOpen(SaveData s, BalanceConfig cfg, int ch)
        {
            var c = C(cfg);
            if (!Open(s, cfg) || ch < 0 || ch >= c.chapters.Count) return false;
            var cp = c.chapters[ch];
            return s.level >= cp.level && Spent(s, cfg) >= cp.spent && (!cp.lord || LordBeaten(s));
        }

        // điều kiện mở chương (chữ trên trang khoá)
        public static string ChapterNeed(BalanceConfig cfg, int ch)
        {
            var cp = C(cfg).chapters[ch];
            var parts = new List<string>();
            if (cp.lord) parts.Add(Loc.T("hạ một chúa tể"));
            else if (cp.level > 0) parts.Add(Loc.F("cấp {0}", cp.level));
            if (cp.spent > 0) parts.Add(Loc.F("đã vẽ {0} nét", cp.spent));
            return string.Join(" · ", parts);
        }

        static int OthersDone(SaveData s, BalanceConfig cfg, SoPhepNode n) =>
            C(cfg).nodes.Count(x => x.ch == n.ch && x != n && !x.IsCap && Lv(s, x.id) > 0);

        // lý do chưa vẽ được (rỗng là vẽ được)
        public static string Block(SaveData s, BalanceConfig cfg, string id)
        {
            var n = C(cfg).Node(id);
            if (n == null) return "?";
            if (!Open(s, cfg)) return Loc.F("Mở ở cấp {0}", C(cfg).openLevel);
            if (Lv(s, id) >= n.MaxLv) return Loc.T("Đã vẽ đủ");
            if (!ChapterOpen(s, cfg, n.ch)) return Loc.F("Chương mở khi {0}", ChapterNeed(cfg, n.ch));
            if (n.IsCap && OthersDone(s, cfg, n) < C(cfg).capNeed) return Loc.F("Vẽ {0} ô khác trong chương trước", C(cfg).capNeed);
            if (Free(s, cfg) < n.cost[Math.Min(Lv(s, id), n.cost.Count - 1)]) return Loc.T("Chưa đủ nét");
            if (n.stones > 0 && Lv(s, id) == 0 && s.evoStones < n.stones) return Loc.T("Chưa đủ đá tiến hóa");
            return "";
        }

        public static int CostOf(SaveData s, BalanceConfig cfg, SoPhepNode n) => n.cost[Math.Min(Lv(s, n.id), n.cost.Count - 1)];

        public static bool Buy(SaveData s, BalanceConfig cfg, string id)
        {
            if (Block(s, cfg, id) != "") return false;
            var n = C(cfg).Node(id);
            s.sophep ??= new SoPhepState();
            if (n.stones > 0 && Lv(s, id) == 0)
            {
                s.evoStones -= n.stones;
                s.sophep.stones += n.stones;
            }
            s.sophep.lv[id] = Lv(s, id) + 1;
            return true;
        }

        public static void SetFace(SaveData s, BalanceConfig cfg, string id, int face)
        {
            var n = C(cfg).Node(id);
            if (n == null || n.FaceCount <= 1) return;
            s.sophep ??= new SoPhepState();
            s.sophep.face[id] = Math.Max(0, Math.Min(face, n.FaceCount - 1));
        }

        // tẩy sổ: hoàn hết nét (tự tính lại) và đá; giữ mặt đã chọn
        public static void Reset(SaveData s)
        {
            if (s.sophep == null) return;
            s.evoStones += s.sophep.stones;
            s.sophep.stones = 0;
            s.sophep.lv.Clear();
        }

        // EXP thừa sau cấp tối đa (Progress.AddExp): góp vào nét, tối đa expPoints nét; đủ thì EXP thừa bỏ như cũ
        public static void Bank(SaveData s, BalanceConfig cfg, double over)
        {
            var c = C(cfg);
            if (over <= 0 || !Open(s, cfg) || c.expPerPoint <= 0) return;
            s.sophep ??= new SoPhepState();
            var st = s.sophep;
            if (st.expPoints >= c.expPoints)
            {
                st.expBank = 0;
                return;
            }
            st.expBank += over;
            while (st.expBank >= c.expPerPoint && st.expPoints < c.expPoints)
            {
                st.expBank -= c.expPerPoint;
                st.expPoints++;
            }
            if (st.expPoints >= c.expPoints) st.expBank = 0;
        }

        // đường gợi ý: vẽ theo thứ tự path từ chỗ đang dừng; dừng ở bước đầu tiên chưa vẽ được (giữ thứ tự). Trả số ô vừa vẽ.
        public static int AutoBuy(SaveData s, BalanceConfig cfg)
        {
            int n = 0;
            var want = new Dictionary<string, int>();
            foreach (var step in C(cfg).path)
            {
                var parts = step.Split(':');
                string id = parts[0];
                var node = C(cfg).Node(id);
                if (node == null) continue;
                want[id] = want.TryGetValue(id, out var w) ? w + 1 : 1;
                if (parts.Length > 1 && int.TryParse(parts[1], out var f) && Lv(s, id) == 0) SetFace(s, cfg, id, f);
                if (Lv(s, id) >= want[id]) continue;
                if (!Buy(s, cfg, id)) break;
                n++;
            }
            return n;
        }

        // dấu của sổ đang vẽ (khoá bộ nhớ đệm tỉ lệ thắng của ProgressSim)
        public static string Key(SaveData s) => s.sophep == null || s.sophep.lv.Count == 0 ? "" :
            string.Join(",", s.sophep.lv.OrderBy(kv => kv.Key, StringComparer.Ordinal).Select(kv => kv.Key + kv.Value + "/" + Face(s, kv.Key)));

        public static bool HasCover(SaveData s, BalanceConfig cfg) =>
            C(cfg).nodes.Any(nd => nd.kind == "deco" && Lv(s, nd.id) > 0);

        static double V(SoPhepNode n, int i) => i >= 0 && i < n.v.Count ? n.v[i] : 0;

        // luật trận của sổ đang vẽ; null nếu chưa vẽ ô nào có tác dụng trong trận
        public static BattleRules Rules(SaveData s, BalanceConfig cfg)
        {
            if (s.sophep == null || s.sophep.lv.Count == 0) return null;
            var r = new BattleRules();
            bool any = false;
            foreach (var n in C(cfg).nodes)
            {
                int lv = Math.Min(Lv(s, n.id), n.MaxLv);
                if (lv <= 0 || n.kind == "deco") continue;
                int f = Face(s, n.id);
                any = true;
                switch (n.id)
                {
                    case "lat_trang": r.rerolls = (int)V(n, lv - 1); break;
                    case "rong_don":
                        if (f == 0) r.firstOfferAdd = (int)V(n, 0);
                        else r.groupWeight = V(n, 1);
                        break;
                    case "giu_net": r.holds = (int)V(n, 0); break;
                    case "mat_tinh": r.rareWeight = V(n, 0); break;
                    case "chot_1":
                        r.picks = (int)V(n, f == 0 ? 0 : 2);
                        r.offer = (int)V(n, f == 0 ? 1 : 3);
                        break;
                    case "muc_cho": r.benchMana = V(n, lv - 1); break;
                    case "vao_rut":
                        if (f == 0) r.swapInShield = V(n, 0);
                        else r.swapOutHeal = V(n, 1);
                        break;
                    case "tiep_suc": r.manaCarry = V(n, 0); break;
                    case "tiep_noi": r.koRage = V(n, 0); break;
                    case "chot_2":
                        if (f == 0) r.midSwaps = (int)V(n, 0);
                        else r.assist = V(n, 1);
                        break;
                    case "mui_la":
                        if (f == 0) r.advAdd = V(n, 0);
                        else r.disAdd = V(n, 1);
                        break;
                    case "chua_te": r.bossRerolls = (int)V(n, lv - 1); break;
                    case "net_cuu":
                        r.lowAt = V(n, 0);
                        r.lowHeal = V(n, 1);
                        break;
                    case "tinh_tao": r.stunGuard = (int)V(n, 0); break;
                    case "chot_3":
                        if (f == 0) r.revivePct = V(n, 0);
                        else
                        {
                            r.thornsAt = V(n, 1);
                            r.thorns = V(n, 2);
                        }
                        break;
                    case "but_chi":
                        r.elemExtra = (int)Elements.All[Math.Max(0, Math.Min(f, Elements.All.Length - 1))];
                        r.elemExtraN = (int)V(n, 0);
                        break;
                    case "trang_cuoi": r.lastOffer = (int)V(n, 0); break;
                    case "net_ket": r.executeBelow = V(n, 0); break;
                    case "chot_4":
                        if (f == 0) r.ultDiscount = V(n, 0);
                        else r.doubleFirst = true;
                        break;
                }
            }
            return any ? r : null;
        }

        static string Pct(double v) => Js.RoundInt(v * 100) + "%";

        // chữ hiệu ứng của ô ở cấp lv (ô cấp) hoặc mặt face (ô chọn); lv ≤ 0 thì tả cấp 1
        public static string Describe(SoPhepNode n, int face, int lv)
        {
            int l = Math.Max(1, Math.Min(lv, n.MaxLv));
            switch (n.id)
            {
                case "lat_trang": return Loc.F("Mỗi trận được đổi cả bộ thẻ đang chọn {0} lần.", (int)V(n, l - 1));
                case "rong_don":
                    return face == 0 ? Loc.F("Lần chọn đầu mỗi lượt hiện thêm {0} thẻ.", (int)V(n, 0))
                        : Loc.F("Thẻ cùng nhóm (Công, Thủ, Hồi) với thẻ vừa chọn dễ ra gấp {0} lần ở lần rút kế.", V(n, 1));
                case "giu_net": return Loc.T("Một lần mỗi trận: thẻ hiếm nhất bạn bỏ qua ở lần chọn cuối được giữ sang lần chọn đầu lượt sau.");
                case "mat_tinh": return Loc.F("Thẻ Hiếm trở lên dễ ra gấp {0} lần.", V(n, 0));
                case "chot_1":
                    return face == 0 ? Loc.F("Mỗi lượt chọn {0} lần, mỗi lần {1} thẻ.", (int)V(n, 0), (int)V(n, 1))
                        : Loc.F("Mỗi lượt chọn {0} lần, mỗi lần {1} thẻ.", (int)V(n, 2), (int)V(n, 3));
                case "muc_cho": return Loc.F("Tướng dự bị nhận thêm {0} mana mỗi lượt.", (int)V(n, l - 1));
                case "vao_rut":
                    return face == 0 ? Loc.F("Tướng vừa vào sân có khiên bằng {0} máu tối đa.", Pct(V(n, 0)))
                        : Loc.F("Tự đổi tướng thì tướng vừa rút ra hồi {0} máu tối đa.", Pct(V(n, 1)));
                case "tiep_suc": return Loc.F("Tự đổi tướng thì tướng vào nhận {0} mana của tướng ra.", Pct(V(n, 0)));
                case "tiep_noi": return Loc.F("Tướng gục thì tướng ra thay có sẵn {0} nộ.", (int)V(n, 0));
                case "chot_2":
                    return face == 0 ? Loc.F("Mỗi trận được đổi tướng {0} lần cả khi đã chọn thẻ.", (int)V(n, 0))
                        : Loc.F("Tướng chính tung Tuyệt kỹ thì mỗi tướng dự bị đánh phụ {0} Công của nó.", Pct(V(n, 1)));
                case "mui_la":
                    return face == 0 ? Loc.F("Đánh hệ mình khắc: hệ số khắc hệ cộng thêm {0}.", V(n, 0))
                        : Loc.F("Đánh hệ khắc mình: bớt thiệt {0} hệ số.", V(n, 1));
                case "chua_te": return Loc.F("Trận có boss hoặc mini boss: thêm {0} lần đổi cả bộ thẻ.", (int)V(n, l - 1));
                case "net_cuu": return Loc.F("Lần đầu một tướng xuống dưới {0} máu mỗi trận, hồi {1} máu tối đa.", Pct(V(n, 0)), Pct(V(n, 1)));
                case "tinh_tao": return Loc.T("Hết choáng thì miễn choáng tới hết lượt sau của tướng.");
                case "chot_3":
                    return face == 0 ? Loc.F("Một lần mỗi trận, tướng gục được vẽ lại với {0} máu, mất lượt kế.", Pct(V(n, 0)))
                        : Loc.F("Lần đầu xuống dưới {0} máu, phản lại {1} sát thương nhận tới hết trận.", Pct(V(n, 1)), Pct(V(n, 2)));
                case "but_chi": return Loc.F("Đánh địch hệ {0}: mỗi lần chọn hiện thêm {1} thẻ.", n.FaceName(face), (int)V(n, 0));
                case "trang_cuoi": return Loc.F("Lần chọn cuối mỗi lượt hiện {0} thẻ.", (int)V(n, 0));
                case "net_ket": return Loc.F("Đòn của bạn để địch (không phải boss) dưới {0} máu thì kết liễu luôn.", Pct(V(n, 0)));
                case "bia_so": return Loc.T("Nét vẽ tướng mới mang màu hệ của tướng. Không cộng sức mạnh.");
                case "chot_4":
                    return face == 0 ? Loc.F("Tuyệt kỹ đầu tiên mỗi trận bớt {0} nộ.", Pct(V(n, 0))) : Loc.T("Thẻ chọn đầu tiên mỗi trận chạy hai lần.");
            }
            return "";
        }
    }
}
