# Biên dịch thử assembly Game / Editor ngoài Unity theo csproj Unity sinh (Compile, HintPath, DefineConstants) + Library/ScriptAssemblies.
# Bản nháp trong overlay/ (App/, Game/, UI/, Editor/) đè hoặc thêm vào danh sách file. Core lấy từ out/Core.dll (build.py core).
# py -3 -I kiem_bien_dich.py game|editor
import os, re, sys, glob, subprocess, xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
# thư mục project tính từ chỗ đặt script (hai máy khác ổ); đặt POKI_PROJ để chỉ chỗ khác
PROJ = os.environ.get("POKI_PROJ") or os.path.abspath(os.path.join(HERE, "..", "..", ".."))
U = r"C:\Program Files\Unity\Hub\Editor\6000.0.73f1\Editor\Data"
DOTNET = os.path.join(U, "NetCoreRuntime", "dotnet.exe")
CSC = os.path.join(U, "DotNetSdkRoslyn", "csc.dll")
OUT = os.path.join(HERE, "out")
SCRIPT = os.path.join(PROJ, "Assets", "01 Script")


def read_proj(name):
    t = open(os.path.join(PROJ, name), encoding="utf-8").read()
    t = re.sub(r'xmlns="[^"]+"', "", t, count=1)
    root = ET.fromstring(t)
    comp = [c.get("Include") for c in root.iter("Compile")]
    hints = [h.text for h in root.iter("HintPath")]
    defs = ";".join(d.text for d in root.iter("DefineConstants") if d.text)
    langv = next((d.text for d in root.iter("LangVersion")), "9.0")
    return comp, hints, defs, langv


def build(kind):
    proj = "PokiClash.Game.csproj" if kind == "game" else "PokiClash.Editor.csproj"
    comp, hints, defs, langv = read_proj(proj)
    files = {}
    for c in comp:
        p = os.path.join(PROJ, c)
        rel = os.path.relpath(p, SCRIPT).replace("\\", "/")
        files[rel] = p
    ov = os.path.join(HERE, "overlay")
    pref = ("App/", "Game/", "UI/") if kind == "game" else ("Editor/",)
    # file mới (phiên khác vừa thêm) chưa có trong csproj Unity sinh: lấy hết .cs trong thư mục của assembly
    for d in pref:
        for root, _, fs in os.walk(os.path.join(SCRIPT, d)):
            for f in fs:
                if f.endswith(".cs"):
                    src = os.path.join(root, f)
                    rel = os.path.relpath(src, SCRIPT).replace("\\", "/")
                    files.setdefault(rel, src)
    for root, _, fs in os.walk(ov):
        for f in fs:
            if not f.endswith(".cs"):
                continue
            src = os.path.join(root, f)
            rel = os.path.relpath(src, ov).replace("\\", "/")
            if rel.startswith(pref):
                files[rel] = src
    refs = []
    for h in hints:
        if not h:
            continue
        b = os.path.basename(h)
        if b.startswith("PokiClash.") :
            continue
        refs.append(h if os.path.isabs(h) else os.path.join(PROJ, h))
    for d in glob.glob(os.path.join(PROJ, "Library", "ScriptAssemblies", "*.dll")):
        b = os.path.basename(d)
        if b.startswith("PokiClash.") or b.startswith("Assembly-CSharp"):
            continue
        if not any(os.path.basename(r) == b for r in refs):
            refs.append(d)
    refs.append(os.path.join(OUT, "Core.dll"))
    if kind == "editor":
        refs.append(os.path.join(OUT, "PokiClash.Game.dll"))
    out = os.path.join(OUT, "PokiClash.Game.dll" if kind == "game" else "PokiClash.Editor.dll")
    rsp = out + ".rsp"
    with open(rsp, "w", encoding="utf-8") as f:
        f.write("-nologo -nostdlib -noconfig -target:library -langversion:%s -nowarn:0169,0414,0649,0219,1701,1702,0618,0672,0067 -unsafe\n" % (langv or "9.0"))
        f.write('-out:"%s"\n' % out)
        f.write("-define:%s\n" % defs)
        for r in refs:
            f.write('-r:"%s"\n' % r)
        for p in files.values():
            f.write('"%s"\n' % p)
    p = subprocess.run([DOTNET, CSC, "@" + rsp], capture_output=True, text=True, encoding="utf-8", errors="replace")
    msg = (p.stdout + p.stderr)
    errs = [l for l in msg.splitlines() if ": error" in l]
    if errs:
        print("\n".join(errs[:50]))
        print("LOI", len(errs), kind)
        sys.exit(1)
    print(kind, "OK", len(files), "file")


if __name__ == "__main__":
    for k in (sys.argv[1:] or ["game", "editor"]):
        build(k)
