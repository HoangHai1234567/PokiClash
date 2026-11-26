# Biên dịch lõi (Assets/01 Script/Core + bản nháp trong so_lieu/overlay/Core nếu có) + Harness.cs rồi chạy ngoài Unity.
# py -3 -I chay.py [stats | dump <ô> <hạt giống>]
import glob, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
U = r"C:\Program Files\Unity\Hub\Editor\6000.0.73f1\Editor\Data"
DOTNET, CSC = os.path.join(U, "NetCoreRuntime", "dotnet.exe"), os.path.join(U, "DotNetSdkRoslyn", "csc.dll")
MONO = os.path.join(U, "MonoBleedingEdge", "bin", "mono.exe")
API = os.path.join(U, "MonoBleedingEdge", "lib", "mono", "4.7.1-api")
core = os.path.join(PROJ, "Assets", "01 Script", "Core")
files = {os.path.relpath(f, core).replace("\\", "/"): f for f in glob.glob(os.path.join(core, "**", "*.cs"), recursive=True)}
ov = os.path.join(PROJ, "ArtGen", "Casino", "so_lieu", "overlay", "Core")
for f in glob.glob(os.path.join(ov, "**", "*.cs"), recursive=True):
    files[os.path.relpath(f, ov).replace("\\", "/")] = f
out = os.path.join(HERE, "out")
os.makedirs(out, exist_ok=True)
rsp = os.path.join(out, "h.rsp")
with open(rsp, "w", encoding="utf-8") as f:
    f.write("-nologo -nostdlib -langversion:9.0 -optimize+ -nowarn:1701,1702,0414,0649,0169,0219 -target:exe\n")
    f.write('-out:"%s"\n' % os.path.join(out, "h.exe"))
    for r in ("mscorlib.dll", "System.dll", "System.Core.dll"):
        f.write('-r:"%s"\n' % os.path.join(API, r))
    for x in list(files.values()) + [os.path.join(HERE, "Harness.cs")]:
        f.write('"%s"\n' % x)
p = subprocess.run([DOTNET, CSC, "@" + rsp], capture_output=True, text=True, encoding="utf-8", errors="replace")
errs = [l for l in (p.stdout + p.stderr).splitlines() if ": error" in l]
if errs:
    print("\n".join(errs[:40]))
    sys.exit(1)
sys.exit(subprocess.run([MONO, os.path.join(out, "h.exe")] + sys.argv[1:], cwd=out).returncode)
