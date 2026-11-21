// Tên trong dữ liệu theo ngôn ngữ (2026-11-21): GameDb.Build gọi khi không phải tiếng Việt, thay tướng, thẻ, đảo, ải bằng bản sao
// đã dịch tên (bản gốc nằm trong ScriptableObject, không được sửa: Play trong Editor sẽ ghi đè asset). Bảng dịch là Loc (tra theo
// chính chuỗi tiếng Việt). Tên trong cấu hình cân bằng (công trình Nhà, tầng Hang, bậc huy hiệu...) dịch lúc hiện bằng Loc.T.
using System.Collections.Generic;

namespace PokiClash.Core
{
    public static class LocData
    {
        public static HeroDef Hero(HeroDef h)
        {
            var c = h.Copy();
            c.name = Loc.T(h.name);
            c.title = Loc.T(h.title);
            c.line = Loc.T(h.line);
            if (h.forms != null)
            {
                c.forms = new HeroForm[h.forms.Length];
                for (int i = 0; i < h.forms.Length; i++)
                {
                    c.forms[i] = h.forms[i].Copy();
                    c.forms[i].name = Loc.T(h.forms[i].name);
                }
            }
            return c;
        }

        public static CardDef Card(CardDef d)
        {
            var c = d.Copy();
            c.name = Loc.T(d.name);
            c.flavor = Loc.T(d.flavor);
            return c;
        }

        public static ZoneDef Zone(ZoneDef z)
        {
            var c = z.Copy();
            c.name = Loc.T(z.name);
            c.sub = Loc.T(z.sub);
            return c;
        }

        public static StageDef Stage(StageDef s)
        {
            var c = s.Copy();
            c.name = Loc.T(s.name);
            return c;
        }

        public static List<T> All<T>(IEnumerable<T> src, System.Func<T, T> f)
        {
            var l = new List<T>();
            foreach (var x in src) l.Add(Loc.Lang == Loc.Vi ? x : f(x));
            return l;
        }
    }
}
