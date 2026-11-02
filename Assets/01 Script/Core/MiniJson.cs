// Đọc JSON thành Dictionary<string, object> / List<object> / double / string / bool / null, và ghi ngược lại.
// JsonUtility không đọc được mảng lẫn kiểu, nên phần lõi dùng bộ này (chép từ BanThu, thêm phần ghi).
using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Text;

namespace PokiClash.Core
{
    public static class MiniJson
    {
        public static object Parse(string s)
        {
            int i = 0;
            var v = Value(s, ref i);
            Skip(s, ref i);
            if (i < s.Length) throw new FormatException($"JSON thừa ký tự ở vị trí {i}");
            return v;
        }

        static void Skip(string s, ref int i)
        {
            while (i < s.Length && char.IsWhiteSpace(s[i])) i++;
        }

        static char At(string s, int i)
        {
            if (i >= s.Length) throw new FormatException("JSON hết giữa chừng");
            return s[i];
        }

        static object Value(string s, ref int i)
        {
            Skip(s, ref i);
            char c = At(s, i);
            if (c == '{')
            {
                var d = new Dictionary<string, object>();
                i++;
                Skip(s, ref i);
                if (At(s, i) == '}') { i++; return d; }
                while (true)
                {
                    Skip(s, ref i);
                    string key = Str(s, ref i);
                    Skip(s, ref i);
                    if (At(s, i) != ':') throw new FormatException($"Thiếu dấu hai chấm ở vị trí {i}");
                    i++;
                    d[key] = Value(s, ref i);
                    Skip(s, ref i);
                    char e = At(s, i++);
                    if (e == '}') return d;
                    if (e != ',') throw new FormatException($"Thiếu dấu phẩy ở vị trí {i - 1}");
                }
            }
            if (c == '[')
            {
                var l = new List<object>();
                i++;
                Skip(s, ref i);
                if (At(s, i) == ']') { i++; return l; }
                while (true)
                {
                    l.Add(Value(s, ref i));
                    Skip(s, ref i);
                    char e = At(s, i++);
                    if (e == ']') return l;
                    if (e != ',') throw new FormatException($"Thiếu dấu phẩy ở vị trí {i - 1}");
                }
            }
            if (c == '"') return Str(s, ref i);
            if (string.CompareOrdinal(s, i, "true", 0, 4) == 0) { i += 4; return true; }
            if (string.CompareOrdinal(s, i, "false", 0, 5) == 0) { i += 5; return false; }
            if (string.CompareOrdinal(s, i, "null", 0, 4) == 0) { i += 4; return null; }
            int start = i;
            while (i < s.Length && "+-0123456789.eE".IndexOf(s[i]) >= 0) i++;
            if (i == start) throw new FormatException($"Ký tự lạ ở vị trí {i}");
            return double.Parse(s.Substring(start, i - start), NumberStyles.Float, CultureInfo.InvariantCulture);
        }

        static string Str(string s, ref int i)
        {
            if (At(s, i) != '"') throw new FormatException($"Thiếu ngoặc kép ở vị trí {i}");
            var sb = new StringBuilder();
            i++;
            while (At(s, i) != '"')
            {
                char c = s[i++];
                if (c != '\\') { sb.Append(c); continue; }
                char e = At(s, i++);
                switch (e)
                {
                    case 'n': sb.Append('\n'); break;
                    case 't': sb.Append('\t'); break;
                    case 'r': sb.Append('\r'); break;
                    case 'b': sb.Append('\b'); break;
                    case 'f': sb.Append('\f'); break;
                    case 'u': sb.Append((char)int.Parse(s.Substring(i, 4), NumberStyles.HexNumber)); i += 4; break;
                    default: sb.Append(e); break;
                }
            }
            i++;
            return sb.ToString();
        }

        // ---------- ghi ----------

        public static string Write(object v, bool pretty = false)
        {
            var sb = new StringBuilder();
            WriteValue(sb, v, pretty, 0);
            return sb.ToString();
        }

        static void Indent(StringBuilder sb, bool pretty, int depth)
        {
            if (!pretty) return;
            sb.Append('\n');
            sb.Append(' ', depth * 2);
        }

        static void WriteValue(StringBuilder sb, object v, bool pretty, int depth)
        {
            switch (v)
            {
                case null: sb.Append("null"); return;
                case string s: WriteStr(sb, s); return;
                case bool b: sb.Append(b ? "true" : "false"); return;
                case double d: WriteNum(sb, d); return;
                case float f: WriteNum(sb, f); return;
                case int n: sb.Append(n.ToString(CultureInfo.InvariantCulture)); return;
                case long n: sb.Append(n.ToString(CultureInfo.InvariantCulture)); return;
                case uint n: sb.Append(n.ToString(CultureInfo.InvariantCulture)); return;
                case IDictionary<string, object> d:
                {
                    sb.Append('{');
                    bool first = true;
                    foreach (var kv in d)
                    {
                        if (!first) sb.Append(',');
                        first = false;
                        Indent(sb, pretty, depth + 1);
                        WriteStr(sb, kv.Key);
                        sb.Append(pretty ? ": " : ":");
                        WriteValue(sb, kv.Value, pretty, depth + 1);
                    }
                    if (!first) Indent(sb, pretty, depth);
                    sb.Append('}');
                    return;
                }
                case IEnumerable e:
                {
                    sb.Append('[');
                    bool first = true;
                    foreach (var x in e)
                    {
                        if (!first) sb.Append(',');
                        first = false;
                        WriteValue(sb, x, false, depth + 1);
                    }
                    sb.Append(']');
                    return;
                }
                default:
                    if (v is Enum) { WriteStr(sb, v.ToString()); return; }
                    throw new ArgumentException($"MiniJson không ghi được kiểu {v.GetType().Name}");
            }
        }

        static void WriteNum(StringBuilder sb, double d)
        {
            if (double.IsNaN(d) || double.IsInfinity(d)) { sb.Append("null"); return; }
            sb.Append(Js.Num(d));
        }

        static void WriteStr(StringBuilder sb, string s)
        {
            sb.Append('"');
            foreach (char c in s)
            {
                switch (c)
                {
                    case '"': sb.Append("\\\""); break;
                    case '\\': sb.Append("\\\\"); break;
                    case '\n': sb.Append("\\n"); break;
                    case '\r': sb.Append("\\r"); break;
                    case '\t': sb.Append("\\t"); break;
                    default:
                        if (c < 0x20) sb.Append("\\u").Append(((int)c).ToString("x4"));
                        else sb.Append(c);
                        break;
                }
            }
            sb.Append('"');
        }
    }

    // Đọc tiện từ cây JSON (thiếu khoá thì trả mặc định).
    public static class J
    {
        public static Dictionary<string, object> Obj(object v) => v as Dictionary<string, object>;
        public static List<object> Arr(object v) => v as List<object> ?? new List<object>();

        public static object Get(Dictionary<string, object> o, string k) =>
            o != null && o.TryGetValue(k, out var v) ? v : null;

        public static bool Has(Dictionary<string, object> o, string k) => Get(o, k) != null;
        public static double Num(Dictionary<string, object> o, string k, double def = 0) => Get(o, k) is double d ? d : def;
        public static double? NumOpt(Dictionary<string, object> o, string k) => Get(o, k) is double d ? d : (double?)null;
        public static int Int(Dictionary<string, object> o, string k, int def = 0) => Get(o, k) is double d ? (int)d : def;
        public static int? IntOpt(Dictionary<string, object> o, string k) => Get(o, k) is double d ? (int)d : (int?)null;
        public static string Str(Dictionary<string, object> o, string k, string def = null) => Get(o, k) as string ?? def;
        public static bool Bool(Dictionary<string, object> o, string k, bool def = false) => Get(o, k) is bool b ? b : def;
        public static List<object> Arr(Dictionary<string, object> o, string k) => Arr(Get(o, k));
        public static Dictionary<string, object> Obj(Dictionary<string, object> o, string k) => Obj(Get(o, k));
    }
}
