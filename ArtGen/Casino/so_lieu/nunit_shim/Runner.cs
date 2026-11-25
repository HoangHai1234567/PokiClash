// Bộ chạy NUnit tối giản ngoài Unity: tìm lớp có hàm [Test] trong assembly này, chạy từng hàm, in đạt / hỏng.
using System;
using System.Linq;
using System.Reflection;
using NUnit.Framework;

static class TestRunner
{
    static int Main(string[] args)
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;
        int pass = 0, fail = 0;
        foreach (var t in Assembly.GetExecutingAssembly().GetTypes().OrderBy(x => x.Name))
        {
            var tests = t.GetMethods().Where(m => m.GetCustomAttributes(typeof(TestAttribute), false).Length > 0).ToList();
            if (tests.Count == 0) continue;
            foreach (var m in tests)
            {
                string name = t.Name + "." + m.Name;
                if (args.Length > 0 && !args.Any(a => name.Contains(a))) continue;
                var inst = m.IsStatic ? null : Activator.CreateInstance(t);
                var sw = System.Diagnostics.Stopwatch.StartNew();
                try
                {
                    m.Invoke(inst, null);
                    pass++;
                    Console.WriteLine($"  ĐẠT  {name} ({sw.ElapsedMilliseconds} ms)");
                }
                catch (TargetInvocationException e)
                {
                    fail++;
                    var ie = e.InnerException;
                    Console.WriteLine($"  HỎNG {name}: {ie?.GetType().Name}: {ie?.Message}");
                    if (!(ie is AssertionException)) Console.WriteLine(ie?.StackTrace);
                }
            }
        }
        Console.WriteLine($"{pass} đạt, {fail} hỏng");
        return fail > 0 ? 1 : 0;
    }
}
