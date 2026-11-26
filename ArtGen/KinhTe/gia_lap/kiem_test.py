# Chạy bộ test NUnit của game ngoài Unity, trên Assets hoặc trên một bản nháp (thư mục có Core/, Tests/, Json/, Golden/).
#   py -3 -I kiem_test.py                 -> test trên Assets (mốc)
#   py -3 -I kiem_test.py --nhap <thư mục> [lọc tên test ...]
# File test nào cần UnityEngine / UnityEditor thì tự bị bỏ (in danh sách). TestData của CoreGoldenTests thay bằng bản đọc theo biến môi trường.
import os, sys, re, shutil, subprocess, glob

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build

args = sys.argv[1:]
nhap = None
if "--nhap" in args:
    i = args.index("--nhap")
    nhap = os.path.abspath(args[i + 1])
    del args[i:i + 2]
if nhap:
    CORE, TESTS, JSON, DATA = [os.path.join(nhap, *x) for x in (("Core",), ("Tests",), ("02 Data", "Json"), ("02 Data",))]
else:
    A = os.path.join(build.PROJ, "Assets")
    CORE, TESTS, JSON, DATA = os.path.join(A, "01 Script", "Core"), os.path.join(A, "01 Script", "Tests"), os.path.join(A, "02 Data", "Json"), os.path.join(A, "02 Data")
OUT = os.path.join(HERE, "out", "test")
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)

SHIM = '''using System; using System.IO; using PokiClash.Core;
namespace PokiClash.Tests {
    public static class TestData {
        public const string OldStarter = "ti_tach";
        public static string DataDir => Environment.GetEnvironmentVariable("POKI_TEST_DATA");
        static GameData cached;
        public static string Read(string rel) => rel.StartsWith("Json/")
            ? File.ReadAllText(Path.Combine(Environment.GetEnvironmentVariable("POKI_TEST_JSON"), rel.Substring(5)))
            : File.ReadAllText(Path.Combine(DataDir, rel));
        public static GameData Load() => cached ??= GameData.FromJson(
            Read("Json/heroes.json"), Read("Json/cards.json"), Read("Json/zones.json"), Read("Json/stages.json"), Read("Json/balance.json"));
        public static StageDef AtLevel(StageDef st, int lv) {
            var c = new StageDef { id = st.id, zone = st.zone, idx = st.idx, name = st.name, kind = st.kind, tag = st.tag, chapter = st.chapter, drops = st.drops };
            foreach (var e in st.enemies) c.enemies.Add(new StageEnemy { hero = e.hero, level = lv, boss = e.boss, evo = e.evo, buff = e.buff });
            return c;
        }
    }
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
    return [l for l in (p.stdout + p.stderr).splitlines() if ": error" in l]


core_dll = os.path.join(OUT, "Core.dll")
errs = csc(core_dll, sorted(glob.glob(os.path.join(CORE, "**", "*.cs"), recursive=True)), [], "library")
if errs:
    print("\n".join(errs[:40]))
    print("LỖI BIÊN DỊCH Core:", len(errs))
    sys.exit(1)
nunit = glob.glob(os.path.join(build.PROJ, "Library", "PackageCache", "com.unity.ext.nunit*", "net40", "unity-custom", "nunit.framework.dll"))[0]
shutil.copy2(nunit, OUT)
nunit = os.path.join(OUT, "nunit.framework.dll")
shim = os.path.join(OUT, "Shim.cs")
open(shim, "w", encoding="utf-8").write(SHIM)
runner = os.path.join(build.PROJ, "ArtGen", "Casino", "so_lieu", "nunit_shim", "Runner.cs")
ok, bo = [], []
for f in sorted(glob.glob(os.path.join(TESTS, "*.cs"))):
    t = open(f, encoding="utf-8").read()
    name = os.path.basename(f)
    if name == "CoreGoldenTests.cs":  # bỏ lớp TestData gốc (dùng UnityEngine.Application)
        a = t.index("    public static class TestData")
        b = t.index("    public class CoreGoldenTests")
        t = t[:a] + t[b:]
        t = t.replace("using UnityEngine;\n", "")
    dst = os.path.join(OUT, name)
    open(dst, "w", encoding="utf-8").write(t)
    e = csc(os.path.join(OUT, "thu.dll"), [dst, shim], [core_dll, nunit], "library")
    (bo if e else ok).append(name)
    if e and "UnityEngine" not in " ".join(e) and "UnityEditor" not in " ".join(e):
        print("LỖI BIÊN DỊCH", name, ":", e[0][-300:])
print("file test chạy được ngoài Unity:", len(ok), "| bỏ (cần Unity):", ", ".join(bo))
errs = csc(os.path.join(OUT, "tests.exe"), [os.path.join(OUT, n) for n in ok] + [shim, runner], [core_dll, nunit], "exe")
if errs:
    print("\n".join(errs[:40]))
    sys.exit(1)
env = dict(os.environ, POKI_TEST_JSON=JSON, POKI_TEST_DATA=DATA)
p = subprocess.run([build.MONO, os.path.join(OUT, "tests.exe")] + args, cwd=OUT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
lines = (p.stdout + p.stderr).splitlines()
bad = [l for l in lines if "HỎNG" in l]
print("\n".join(bad[:80]))
print(lines[-1] if lines else "(không có kết quả)")
open(os.path.join(OUT, "ket_qua.txt"), "w", encoding="utf-8").write("\n".join(lines))
