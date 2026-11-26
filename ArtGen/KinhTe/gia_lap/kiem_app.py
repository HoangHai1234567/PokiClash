# Biên dịch thử assembly Game và Editor của game ngoài Unity với một bản nháp (thư mục có Core/ và tuỳ ý App/, Game/, UI/, Editor/ đè
# lên file cùng đường dẫn trong Assets/01 Script). Dùng lại ArtGen/Casino/so_lieu/kiem_bien_dich.py (đọc csproj Unity sinh).
#   py -3 -I kiem_app.py --nhap <thư mục nháp>        (không --nhap: biên dịch đúng Assets hiện tại)
import os, sys, glob, shutil, subprocess

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build

sys.path.insert(0, os.path.join(build.PROJ, "ArtGen", "Casino", "so_lieu"))
import kiem_bien_dich as kb

args = sys.argv[1:]
nhap = os.path.abspath(args[args.index("--nhap") + 1]) if "--nhap" in args else None
SCRIPT = os.path.join(build.PROJ, "Assets", "01 Script")
WORK = os.path.join(HERE, "out", "app")
shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(os.path.join(WORK, "out"))
os.makedirs(os.path.join(WORK, "overlay"))
if nhap:
    for d in ("App", "Game", "UI", "Editor"):
        if os.path.isdir(os.path.join(nhap, d)):
            shutil.copytree(os.path.join(nhap, d), os.path.join(WORK, "overlay", d))
core_src = os.path.join(nhap, "Core") if nhap else os.path.join(SCRIPT, "Core")
core = os.path.join(WORK, "out", "Core.dll")
rsp = core + ".rsp"
with open(rsp, "w", encoding="utf-8") as f:
    f.write("-nologo -nostdlib -langversion:9.0 -nowarn:1701,1702,0414,0649,0169,0219,0162,0618 -target:library\n-out:\"%s\"\n" % core)
    for r in ("mscorlib.dll", "System.dll", "System.Core.dll"):
        f.write('-r:"%s"\n' % os.path.join(build.API, r))
    for x in sorted(glob.glob(os.path.join(core_src, "**", "*.cs"), recursive=True)):
        f.write('"%s"\n' % x)
p = subprocess.run([build.DOTNET, build.CSC, "@" + rsp], capture_output=True, text=True, encoding="utf-8", errors="replace")
errs = [l for l in (p.stdout + p.stderr).splitlines() if ": error" in l]
if errs:
    print("\n".join(errs[:30]))
    sys.exit(1)
kb.HERE, kb.OUT = WORK, os.path.join(WORK, "out")
for k in ("game", "editor"):
    kb.build(k)
