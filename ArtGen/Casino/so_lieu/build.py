# Biên dịch Core (+ Tests, + runner) ngoài Unity. Bản nháp trong overlay/ đè lên bản ở Assets (cùng đường dẫn tương đối "Core/...", "Tests/...").
# py -3 -I build.py core            -> out/Core.dll
# py -3 -I build.py run             -> Core.dll + runner/*.cs -> out/run.exe, chạy
# py -3 -I build.py tests [Lọc]     -> Core.dll + Tests (chỉ file chỉ định trong TESTS) + nunit runner nhỏ, chạy
import os, sys, shutil, subprocess, glob

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = r"C:\Atomik\PokiWar"
U = r"C:\Program Files\Unity\Hub\Editor\6000.0.73f1\Editor\Data"
DOTNET = os.path.join(U, "NetCoreRuntime", "dotnet.exe")
CSC = os.path.join(U, "DotNetSdkRoslyn", "csc.dll")
MONO = os.path.join(U, "MonoBleedingEdge", "bin", "mono.exe")
API = os.path.join(U, "MonoBleedingEdge", "lib", "mono", "4.7.1-api")
OUT = os.path.join(HERE, "out")
STAGE = os.path.join(HERE, "stage")
os.makedirs(OUT, exist_ok=True)


def stage():
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    shutil.copytree(os.path.join(PROJ, "Assets", "01 Script", "Core"), os.path.join(STAGE, "Core"))
    shutil.copytree(os.path.join(PROJ, "Assets", "01 Script", "Tests"), os.path.join(STAGE, "Tests"))
    if os.environ.get('BASELINE'):
        return
    sys.path.insert(0, HERE)
    import patches
    patches.apply(STAGE)
    ov = os.path.join(HERE, "overlay")
    if os.path.isdir(ov):
        for root, _, files in os.walk(ov):
            for f in files:
                src = os.path.join(root, f)
                rel = os.path.relpath(src, ov)
                dst = os.path.join(STAGE, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)


def csc(out, files, refs, target="library", defines=None):
    rsp = out + ".rsp"
    with open(rsp, "w", encoding="utf-8") as f:
        f.write("-nologo -nostdlib -langversion:9.0 -nowarn:1701,1702,0414,0649,0169,0219 -target:%s\n" % target)
        f.write('-out:"%s"\n' % out)
        if defines:
            f.write("-define:%s\n" % ";".join(defines))
        for r in [os.path.join(API, "mscorlib.dll"), os.path.join(API, "System.dll"), os.path.join(API, "System.Core.dll")] + refs:
            f.write('-r:"%s"\n' % r)
        for x in files:
            f.write('"%s"\n' % x)
    p = subprocess.run([DOTNET, CSC, "@" + rsp], capture_output=True, text=True, encoding="utf-8", errors="replace")
    msg = (p.stdout + p.stderr).strip()
    errs = [l for l in msg.splitlines() if ": error" in l]
    warns = [l for l in msg.splitlines() if ": warning" in l]
    if errs:
        print("\n".join(errs[:60]))
        print("LOI BIEN DICH:", len(errs), out)
        sys.exit(1)
    return warns


def cs_files(d):
    return sorted(glob.glob(os.path.join(d, "**", "*.cs"), recursive=True))


def core():
    stage()
    w = csc(os.path.join(OUT, "Core.dll"), cs_files(os.path.join(STAGE, "Core")), [])
    print("Core.dll OK", ("(%d canh bao)" % len(w)) if w else "")


def data():
    dd = os.path.join(OUT, "data")
    os.makedirs(dd, exist_ok=True)
    for f in glob.glob(os.path.join(PROJ, "Assets", "02 Data", "Json", "*.json")):
        shutil.copy2(f, dd)
    if not os.environ.get('BASELINE'):
        subprocess.run([sys.executable, "-I", os.path.join(HERE, "gen_casino.py"), "--apply", os.path.join(dd, "balance.json")], check=True)


def run(args):
    core()
    data()
    files = cs_files(os.path.join(HERE, "runner"))
    csc(os.path.join(OUT, "run.exe"), files, [os.path.join(OUT, "Core.dll")], target="exe")
    p = subprocess.run([MONO, os.path.join(OUT, "run.exe")] + args, cwd=OUT)
    sys.exit(p.returncode)


def tests(args):
    core()
    data()
    nunit = glob.glob(os.path.join(PROJ, "Library", "PackageCache", "com.unity.ext.nunit*", "net40", "unity-custom", "nunit.framework.dll"))[0]
    shutil.copy2(nunit, OUT)
    want = [a for a in args if a.endswith(".cs")]
    filt = [a for a in args if not a.endswith(".cs")]
    tdir = os.path.join(STAGE, "Tests")
    files = [os.path.join(tdir, f) for f in want] + [os.path.join(HERE, "nunit_shim", "Shim.cs"), os.path.join(HERE, "nunit_shim", "Runner.cs")]
    # TestData (CoreGoldenTests.cs) dùng UnityEngine.Application: shim thay bằng TestDataShim
    csc(os.path.join(OUT, "tests.exe"), files, [os.path.join(OUT, "Core.dll"), os.path.join(OUT, "nunit.framework.dll")], target="exe")
    p = subprocess.run([MONO, os.path.join(OUT, "tests.exe")] + filt, cwd=OUT)
    sys.exit(p.returncode)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "core"
    if cmd == "core":
        core()
    elif cmd == "run":
        run(sys.argv[2:])
    elif cmd == "tests":
        tests(sys.argv[2:])
