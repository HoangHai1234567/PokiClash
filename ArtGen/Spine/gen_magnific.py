# -*- coding: utf-8 -*-
"""Gen một file prompt của ArtGen (cùng định dạng với gen.py / Codex) qua MAGNIFIC (connector claude.ai "Magnific", model GPT 2.6), dùng
khi hạn mức Codex hết. Người dùng 2026-11-17 nối connector (gói Plus, ~491k credit; gpt-2-6 ~40 credit / ảnh, 2k ~65).

Phiên Claude Code đang chạy không có công cụ Magnific (connector nạp lúc phiên bắt đầu) nên script gọi một phiên Claude Code CHẠY NGẦM
(`claude.exe -p`, chỉ cho phép đúng các công cụ Magnific cần + curl): tải từng ảnh mẫu lên (request_upload → PUT → finalize_upload),
images_generate với các ảnh mẫu theo ĐÚNG thứ tự "image 1, image 2..." của file prompt, chờ, tải ảnh về chỗ SAVE (trùng tên thì _2, _3...),
rồi đổi cỡ về đúng khung CANVAS của prompt (vd 1536x1024) để các bước sau dùng như ảnh Codex.

    py -3 -I ArtGen/Spine/gen_magnific.py <file prompt> [--mode gpt-2-6] [--res 1k] [--quality high] [--tran 100] [--timeout 1500]

MỨC TRẦN (người dùng 2026-11-17): một ảnh dưới 100 credit; lớn hơn thì BÁO NGƯỜI DÙNG, không gen. Script báo giá (simulate_cost) đúng tham
số trước khi gen (bảng GIA đo bằng simulate_cost; tổ hợp chưa đo thì không gen); quá --tran (mặc định 100) thì dừng, mã thoát 3. Giá GPT 2.6, 3:2, 1 ảnh (đo 2026-11-17): 1k low 15 / medium 40 / high 95;
2k low 30 / medium 65 / high 175. Mặc định 1k high (95 credit): ra đúng 1536x1024 như khung prompt. Lần thử đầu (2k high) đã tốn 175.

Phần prompt gửi Magnific = file prompt bỏ đường dẫn ảnh và mục SAVE (Magnific nhận ảnh mẫu qua references, không mở đường dẫn).
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CLAUDE = [os.path.expanduser(r"~\.vscode\extensions\{}\resources\native-binary\claude.exe".format(d))
          for d in sorted(os.listdir(os.path.expanduser(r"~\.vscode\extensions")), reverse=True) if d.startswith("anthropic.claude-code-")]
# giá đã đo bằng simulate_cost (2026-11-17, 3:2, 1 ảnh, ảnh mẫu không đổi giá): kiểm ngay trong script, không nhờ phiên chạy ngầm đọc số
GIA = {("gpt-2-6", "1k", "low"): 15, ("gpt-2-6", "1k", "medium"): 40, ("gpt-2-6", "1k", "high"): 95,
       ("gpt-2-6", "2k", "low"): 30, ("gpt-2-6", "2k", "medium"): 65, ("gpt-2-6", "2k", "high"): 175}
CONG_CU = ["creations_request_upload", "creations_finalize_upload", "images_generate", "creations_wait", "creations_get", "creation_status"]
TIEN_TO = "mcp__claude_ai_Magnific__"


def doc_prompt(p):
    t = open(p, encoding="utf-8").read().replace("\r\n", "\n")
    lines = t.split("\n")
    anh, giu, save = [], [], None
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^image (\d+) = (.+?\.(?:png|jpg|jpeg|webp)): ?(.*)$", ln, re.I)
        if m:
            anh.append(m.group(2).strip())
            giu.append(f"image {m.group(1)} = {m.group(3)}")
        elif ln.startswith("IMAGES (attached"):
            giu.append("IMAGES (attached as references, in this order):")
        elif ln.startswith("SAVE:"):
            save = ln.split("to", 1)[1].strip()
            # bỏ cả dòng "If a file with that name already exists..." ngay sau
            if i + 1 < len(lines) and lines[i + 1].startswith("If a file"):
                i += 1
        else:
            giu.append(ln)
        i += 1
    if not save:
        raise SystemExit(f"{p}: không có mục SAVE")
    m = re.search(r"CANVAS:[^\n]*?(\d{3,4})\s*x\s*(\d{3,4})", t)
    canvas = (int(m.group(1)), int(m.group(2))) if m else None
    van = re.sub(r"\n{3,}", "\n\n", "\n".join(giu)).strip()
    return anh, save, canvas, van


def ty_le(canvas):
    if not canvas:
        return "auto"
    w, h = canvas
    best = min(["1:1", "3:2", "2:3", "4:3", "3:4", "16:9", "9:16", "2:1", "21:9"],
               key=lambda r: abs(int(r.split(":")[0]) / int(r.split(":")[1]) - w / h))
    return best


def cho_luu(save):
    d, b = os.path.split(save)
    s, e = os.path.splitext(b)
    p, k = save, 2
    while os.path.exists(p):
        p = os.path.join(d, f"{s}_{k}{e}")
        k += 1
    return p


def main(argv):
    a = [x for x in argv if not x.startswith("--")]
    opt = {argv[i][2:]: argv[i + 1] for i in range(len(argv) - 1) if argv[i].startswith("--")}
    if not a:
        print(__doc__)
        return 2
    pf = os.path.abspath(a[0])
    anh, save, canvas, van = doc_prompt(pf)
    for x in anh:
        if not os.path.exists(x):
            raise SystemExit(f"thiếu ảnh mẫu: {x}")
    if not CLAUDE or not os.path.exists(CLAUDE[0]):
        raise SystemExit("không thấy claude.exe của extension Claude Code")
    os.makedirs(os.path.dirname(save), exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="magnific_")
    pt = os.path.join(tmp, "prompt.txt")
    open(pt, "w", encoding="utf-8").write(van)
    tai = os.path.join(tmp, "ket_qua.png")
    mode, res, qual = opt.get("mode", "gpt-2-6"), opt.get("res", "1k"), opt.get("quality", "high")
    tran = int(opt.get("tran", "100"))
    gia0 = GIA.get((mode, res, qual))
    if gia0 is None or gia0 > tran:
        print(f"DỪNG: {mode} {res} {qual} giá {gia0 if gia0 is not None else 'chưa đo'} credit, trần {tran}: không gen, báo người dùng.")
        return 3
    ds = "\n".join(f"  image {i}: {x}  (mimeType {'image/png' if x.lower().endswith('.png') else 'image/jpeg'})" for i, x in enumerate(anh, 1))
    lenh = f"""You are a non-interactive tool runner. Do exactly these steps, nothing else, then print ONE final line.
Load the tools first with ToolSearch: query "select:{','.join(TIEN_TO + c for c in CONG_CU)}".
1. Upload these local reference images IN THIS ORDER (one creations_request_upload per image, or one call with count={len(anh)}):
{ds}
   For each: call {TIEN_TO}creations_request_upload, then PUT the raw bytes with Bash:
   curl -s -f -X PUT --upload-file "<local path>" -H "Content-Type: <mimeType>" "<presigned url>"
   then {TIEN_TO}creations_finalize_upload (fileName = the file's base name, path = the returned path) to get a creation identifier.
   Keep the identifiers in the same order (image 1 first).
2. Read the prompt text with the Read tool from: {pt}
   Call {TIEN_TO}images_generate with: prompt = that text VERBATIM (do not shorten, translate or rewrite it), mode = "{mode}",
   references = [{{"type": "image", "identifier": <id of image 1>}}, {{"type": "image", "identifier": <id of image 2>}}, ...] in order,
   count = 1, aspectRatio = "{ty_le(canvas)}", resolution = "{res}", extraSettings = {{"quality": "{qual}"}} (exactly the priced settings;
   if the tool rejects them, STOP and print ERROR <reason>; never retry with other settings). If the prompt is rejected as too long, print
   ERROR with the limit; do not cut it.
3. Wait with {TIEN_TO}creations_wait (repeat until finished, up to 20 minutes), then {TIEN_TO}creations_get to get the full-size image url.
4. Download it with Bash: curl -s -f -L -o "{tai}" "<url>"
Final line (exactly one of): SAVED {tai}   |   ERROR <short reason>
"""
    cho_phep = ["ToolSearch", "Read", "Bash(curl:*)"] + [TIEN_TO + c for c in CONG_CU]
    t0 = time.time()
    p = subprocess.run([CLAUDE[0], "-p", lenh, "--allowedTools", ",".join(cho_phep)], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=int(opt.get("timeout", "1500")), cwd=tmp)
    out = (p.stdout or "") + (p.stderr or "")
    gia = gia0
    if not os.path.exists(tai):
        print(out[-3000:])
        print(f"{time.time() - t0:.0f} s, KHÔNG có ảnh")
        return 1
    im = Image.open(tai).convert("RGB")
    goc = im.size
    if canvas and goc != canvas:
        im = im.resize(canvas, Image.LANCZOS)
    dich = cho_luu(save)
    im.save(dich)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{time.time() - t0:.0f} s, 1 ảnh mới (Magnific {mode} {res} {qual}, {gia} credit, {goc[0]}x{goc[1]} → {im.size[0]}x{im.size[1]}):"
          f"\n  {dich}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
