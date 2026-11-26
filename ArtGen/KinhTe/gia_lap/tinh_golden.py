# Tính lại golden "theo tướng mẫu của test" (rương máy bi, AFK, trang trại, tiềm năng, đền, thẻ rơi) ngoài Unity, bằng đúng mã của menu
# Editor/GoldenFixtureMenu.cs (biên dịch kèm vài lớp giả cho UnityEngine / UnityEditor). Dùng sau khi đổi luật hoặc số làm lệch các golden đó.
#   py -3 -I tinh_golden.py --nhap <thư mục có Core/ và "02 Data/">     (mặc định: Assets, tức sửa thẳng golden của game)
import os, sys, subprocess, glob, shutil

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build

args = sys.argv[1:]
A = os.path.join(build.PROJ, "Assets")
if "--nhap" in args:
    nhap = os.path.abspath(args[args.index("--nhap") + 1])
    CORE, DATAPATH = os.path.join(nhap, "Core"), nhap
else:
    CORE, DATAPATH = os.path.join(A, "01 Script", "Core"), A
ED = os.path.join(A, "01 Script", "Editor")
OUT = os.path.join(HERE, "out", "golden")
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

SHIM = '''using System;
namespace UnityEngine {
    public static class Application { public static string dataPath => Environment.GetEnvironmentVariable("POKI_DATAPATH"); }
    public static class Debug { public static void Log(object o) => Console.WriteLine(o); public static void LogWarning(object o) => Console.WriteLine(o); public static void LogError(object o) => Console.WriteLine(o); }
}
namespace UnityEditor {
    public static class AssetDatabase { public static void Refresh() { } }
    [AttributeUsage(AttributeTargets.Method, AllowMultiple = true)]
    public sealed class MenuItem : Attribute { public int priority; public MenuItem(string s) { } public MenuItem(string s, bool v) { } public MenuItem(string s, bool v, int p) { } }
}
static class GoldenMain {
    static int Main() { Console.OutputEncoding = System.Text.Encoding.UTF8; PokiClash.EditorTools.GoldenFixtureMenu.Run(); return 0; }
}
'''


def csc(out, files, refs, target):
    rsp = out + ".rsp"
    with open(rsp, "w", encoding="utf-8") as f:
        f.write("-nologo -nostdlib -langversion:9.0 -nowarn:1701,1702,0414,0649,0169,0219,0162,0618 -target:%s\n-out:\"%s\"\n" % (target, out))
        for r in [os.path.join(build.API, x) for x in ("mscorlib.dll", "System.dll", "System.Core.dll")] + refs:
            f.write('-r:"%s"\n' % r)
        for x in files:
            f.write('"%s"\n' % x)
    p = subprocess.run([build.DOTNET, build.CSC, "@" + rsp], capture_output=True, text=True, encoding="utf-8", errors="replace")
    errs = [l for l in (p.stdout + p.stderr).splitlines() if ": error" in l]
    if errs:
        print("\n".join(errs[:30]))
        sys.exit(1)


core = os.path.join(OUT, "Core.dll")
csc(core, sorted(glob.glob(os.path.join(CORE, "**", "*.cs"), recursive=True)), [], "library")
shim = os.path.join(OUT, "Shim.cs")
open(shim, "w", encoding="utf-8").write(SHIM)
csc(os.path.join(OUT, "golden.exe"), [os.path.join(ED, "GoldenFixtureMenu.cs"), os.path.join(ED, "IslandGen.cs"), shim], [core], "exe")
p = subprocess.run([build.MONO, os.path.join(OUT, "golden.exe")], env=dict(os.environ, POKI_DATAPATH=DATAPATH), capture_output=True, text=True, encoding="utf-8", errors="replace")
print((p.stdout + p.stderr).strip()[-1500:])
sys.exit(p.returncode)
