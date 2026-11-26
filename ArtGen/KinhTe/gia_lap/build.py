# Giả lập kinh tế (GD_Claude/33_CanBangKinhTe.md): biên dịch Core đúng như trên đĩa (không overlay, không patch) + runner/*.cs ngoài
# Unity, rồi chạy. Không đụng Assets, không cần Unity Editor.
#   py -3 -I build.py build                 -> out/Core.dll, out/sim.exe, out/data/<bộ số>/*.json
#   py -3 -I build.py run <tham số runner>  -> build rồi chạy một tiến trình
# Bộ số: "goc" là balance.json đang có; mỗi file bo_so/<tên>.py (hàm patch(b) sửa dict balance) sinh thêm out/data/<tên>/.
import os, sys, shutil, subprocess, glob, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.environ.get("POKI_PROJ") or os.path.abspath(os.path.join(HERE, "..", "..", ".."))
U = r"C:\Program Files\Unity\Hub\Editor\6000.0.73f1\Editor\Data"
DOTNET = os.path.join(U, "NetCoreRuntime", "dotnet.exe")
CSC = os.path.join(U, "DotNetSdkRoslyn", "csc.dll")
MONO = os.path.join(U, "MonoBleedingEdge", "bin", "mono.exe")
API = os.path.join(U, "MonoBleedingEdge", "lib", "mono", "4.7.1-api")
OUT = os.path.join(HERE, "out")
STAGE = os.path.join(HERE, "stage")


def csc(out, files, refs, target="library"):
    rsp = out + ".rsp"
    with open(rsp, "w", encoding="utf-8") as f:
        f.write("-nologo -nostdlib -optimize+ -langversion:9.0 -nowarn:1701,1702,0414,0649,0169,0219,0162 -target:%s\n" % target)
        f.write('-out:"%s"\n' % out)
        for r in [os.path.join(API, x) for x in ("mscorlib.dll", "System.dll", "System.Core.dll")] + refs:
            f.write('-r:"%s"\n' % r)
        for x in files:
            f.write('"%s"\n' % x)
    p = subprocess.run([DOTNET, CSC, "@" + rsp], capture_output=True, text=True, encoding="utf-8", errors="replace")
    errs = [l for l in (p.stdout + p.stderr).splitlines() if ": error" in l]
    if errs:
        print("\n".join(errs[:60]))
        print("LOI BIEN DICH:", len(errs), out)
        sys.exit(1)


def cs_files(d):
    return sorted(glob.glob(os.path.join(d, "**", "*.cs"), recursive=True))


def data():
    src = os.path.join(PROJ, "Assets", "02 Data", "Json")
    base = os.path.join(OUT, "data", "goc")
    os.makedirs(base, exist_ok=True)
    for f in glob.glob(os.path.join(src, "*.json")):
        shutil.copy2(f, base)
    with open(os.path.join(base, "balance.json"), encoding="utf-8") as f:
        bal = f.read()
    for py in sorted(glob.glob(os.path.join(HERE, "bo_so", "*.py"))):
        name = os.path.splitext(os.path.basename(py))[0]
        spec = importlib.util.spec_from_file_location(name, py)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        b = json.loads(bal)
        mod.patch(b)
        dd = os.path.join(OUT, "data", name)
        os.makedirs(dd, exist_ok=True)
        for f in glob.glob(os.path.join(base, "*.json")):
            if os.path.basename(f) != "balance.json":
                shutil.copy2(f, dd)
        if hasattr(mod, "patch_stages"):  # bộ số sửa cả ải (ví dụ địch mạnh dần theo mốc)
            with open(os.path.join(base, "stages.json"), encoding="utf-8") as f:
                stg = json.load(f)
            mod.patch_stages(stg)
            with open(os.path.join(dd, "stages.json"), "w", encoding="utf-8") as f:
                json.dump(stg, f, ensure_ascii=False)
        with open(os.path.join(dd, "balance.json"), "w", encoding="utf-8") as f:
            json.dump(b, f, ensure_ascii=False)


def stage_patch():
    """Vá BẢN SAO Core trong stage/ (không đụng Assets) để thử luật chưa có trong game: hệ số sức theo từng tướng
    (HeroStats.HeroMult). Mặc định HeroMult = null: mọi số y như game."""
    def sub(rel, pairs):
        f = os.path.join(STAGE, "Core", rel)
        with open(f, encoding="utf-8") as fh:
            t = fh.read()
        for a, b in pairs:
            assert a in t, (rel, a)
            t = t.replace(a, b)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(t)
    sub("HeroStats.cs", [
        ("using System;", "using System;\nusing System.Collections.Generic;"),
        ("        public static double PowerOf(Rarity r) => RarityPower[(int)r];",
         "        public static double PowerOf(Rarity r) => RarityPower[(int)r];\n"
         "        public static Dictionary<string, double> HeroMult;\n"
         "        public static double PowerOfHero(HeroDef h) => HeroMult != null && HeroMult.TryGetValue(h.id, out var v) ? v : RarityPower[(int)h.rarity];"),
        ("double m = RarityPower[(int)h.rarity] * LevelMult", "double m = PowerOfHero(h) * LevelMult"),
    ])
    sub("Islands.cs", [("HeroStats.PowerOf(NormRarity) / HeroStats.PowerOf(h.rarity)", "HeroStats.PowerOf(NormRarity) / HeroStats.PowerOfHero(h)")])
    sub("Badges.cs", [("HeroStats.PowerOf(Islands.NormRarity) / HeroStats.PowerOf(h.rarity)", "HeroStats.PowerOf(Islands.NormRarity) / HeroStats.PowerOfHero(h)")])


def build():
    os.makedirs(OUT, exist_ok=True)
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    shutil.copytree(os.path.join(PROJ, "Assets", "01 Script", "Core"), os.path.join(STAGE, "Core"), ignore=shutil.ignore_patterns("*.meta"))
    stage_patch()
    csc(os.path.join(OUT, "Core.dll"), cs_files(os.path.join(STAGE, "Core")), [])
    csc(os.path.join(OUT, "sim.exe"), cs_files(os.path.join(HERE, "runner")), [os.path.join(OUT, "Core.dll")], target="exe")
    data()
    print("build OK")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    build()
    if cmd == "run":
        sys.exit(subprocess.run([MONO, os.path.join(OUT, "sim.exe")] + sys.argv[2:], cwd=OUT).returncode)
