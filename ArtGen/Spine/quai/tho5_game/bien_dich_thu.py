# -*- coding: utf-8 -*-
"""Biên dịch thử PokiClash.Core + PokiClash.Game bằng Roslyn đi kèm Unity, KHÔNG đụng Unity đang mở: đọc danh sách file + tham chiếu từ
.csproj, thay các file có trong thư mục <thay> (bản đã sửa), thêm file mới trong đó. In lỗi (bỏ cảnh báo).

    py -3 -I ArtGen/Spine/quai/tho5_game/bien_dich_thu.py <thư mục thay>
"""
import os
import re
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
THAY = os.path.abspath(sys.argv[1])
UNITY = r"C:\Program Files\Unity\Hub\Editor\6000.0.73f1\Editor\Data"
DOTNET = os.path.join(UNITY, "NetCoreRuntime", "dotnet.exe")
CSC = os.path.join(UNITY, "DotNetSdkRoslyn", "csc.dll")
OUT = tempfile.mkdtemp(prefix="pc_csc_")


def doc_csproj(ten):
    t = open(os.path.join(ROOT, ten), encoding="utf-8").read()
    files = [os.path.join(ROOT, f) for f in re.findall(r'<Compile Include="([^"]+)"', t)]
    refs = re.findall(r"<HintPath>([^<]+)</HintPath>", t)
    defs = re.search(r"<DefineConstants>([^<]*)</DefineConstants>", t).group(1)
    unsafe = "<AllowUnsafeBlocks>True" in t
    return files, refs, defs, unsafe


def chay(ten, out_dll, them_ref=()):
    files, refs, defs, unsafe = doc_csproj(ten)
    moi = {f.lower(): os.path.join(THAY, f) for f in os.listdir(THAY) if f.endswith(".cs")}
    dung, da = [], set()
    for f in files:
        b = os.path.basename(f).lower()
        if b in moi:
            dung.append(moi[b])
            da.add(b)
        else:
            dung.append(f)
    for b, p in moi.items():                                     # file mới: *Tour.cs vào Editor, còn lại vào Game
        if b not in da and (("editor" in ten.lower()) == b.endswith("tour.cs")) and "core" not in ten.lower():
            dung.append(p)
            print("  thêm", p)
    rsp = os.path.join(OUT, os.path.basename(out_dll) + ".rsp")
    with open(rsp, "w", encoding="utf-8") as w:
        w.write("-nologo -nostdlib+ -noconfig -target:library -langversion:9.0 -nowarn:CS0618,CS0649,CS0414,CS0169,CS0219,CS0162,CS0168\n")
        w.write(f"-out:\"{out_dll}\"\n-define:{defs}\n")
        if unsafe:
            w.write("-unsafe\n")
        for r in list(refs) + list(them_ref):
            w.write(f"-r:\"{r}\"\n")
        for f in dung:
            w.write(f"\"{f}\"\n")
    p = subprocess.run([DOTNET, CSC, "@" + rsp], capture_output=True, text=True, encoding="utf-8", errors="replace")
    loi = [ln for ln in p.stdout.splitlines() if ": error " in ln]
    print(f"{ten}: {len(dung)} file, mã thoát {p.returncode}, {len(loi)} lỗi")
    for ln in loi[:40]:
        print("   ", ln.replace(ROOT, "").strip())
    return p.returncode == 0


core = os.path.join(OUT, "PokiClash.Core.dll")
game = os.path.join(OUT, "PokiClash.Game.dll")
if chay("PokiClash.Core.csproj", core) and chay("PokiClash.Game.csproj", game, [core]):
    chay("PokiClash.Editor.csproj", os.path.join(OUT, "PokiClash.Editor.dll"), [core, game])
