"""Gọi Codex (codex exec, gói ChatGPT của người dùng) gen ảnh theo một file prompt của ArtGen, rồi kiểm ảnh đã lưu.

Thay việc người dùng dán đường dẫn file prompt vào Codex desktop (người dùng chọn cách này 2026-11-07). File prompt giữ
nguyên luật cũ: mở đầu bằng "image N = <đường dẫn>: ...", có mục SAVE. Script đính các ảnh mẫu đó theo đúng thứ tự
(codex exec -i), chạy trong thư mục gốc PokiClash (sandbox workspace-write), chờ xong rồi liệt kê ảnh PNG mới trong các
thư mục mà file prompt bảo lưu.

    py -3 -I ArtGen/Heroes/tools/gen_codex.py <file prompt> [--steps N02,N06] [--note "câu sửa thêm"] [--timeout 1500]

--steps: với file lượt 2/3 (nhiều bước), vẽ đúng các bước này trong một lượt, mỗi bước một ảnh.
--note: câu dặn thêm (câu sửa nhanh trong HUONG_DAN.md) gửi kèm.
Ghi nhật ký: <thư mục lưu>/../gen_log.jsonl (mỗi lần chạy một dòng). Chạy từng lệnh một, không song song.
"""
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))  # thư mục gốc PokiClash
_CACHE = os.path.join(os.environ.get("TEMP", HERE), "pokiclash_codex_path.txt")


def codex_exe():
    """codex.exe nằm trong gói AppX của Codex desktop; đường dẫn đổi theo phiên bản nên hỏi PowerShell."""
    if os.path.exists(_CACHE):
        p = open(_CACHE, encoding="utf-8").read().strip()
        if os.path.exists(p):
            return p
    loc = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-AppxPackage -Name OpenAI.Codex).InstallLocation"],
                         capture_output=True, text=True).stdout.strip()
    p = os.path.join(loc, "app", "resources", "codex.exe")
    if not loc or not os.path.exists(p):
        sys.exit("Không tìm thấy codex.exe (Codex desktop chưa cài?)")
    open(_CACHE, "w", encoding="utf-8").write(p)
    return p


def parse(prompt_path):
    text = open(prompt_path, encoding="utf-8").read()
    refs = re.findall(r"^image \d+ = (.+?\.(?:png|jpg|jpeg|webp)):", text, re.M | re.I)
    saves = set()
    for m in re.finditer(r"(?:save it as a PNG to|goes into|save it to) ([A-Za-z]:\\[^\s\"']+)", text, re.I):
        p = m.group(1).rstrip(".,;")
        saves.add(p if not p.lower().endswith(".png") else os.path.dirname(p))
    return text, refs, sorted(saves)


def snapshot(dirs):
    out = {}
    for d in dirs:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.lower().endswith(".png"):
                    p = os.path.join(d, f)
                    out[p] = os.path.getmtime(p)
    return out


def main(argv):
    if not argv:
        sys.exit(__doc__)
    prompt = os.path.abspath(argv[0])
    opts = {"steps": None, "note": None, "timeout": 1500}
    i = 1
    while i < len(argv):
        k = argv[i].lstrip("-")
        opts[k] = argv[i + 1]
        i += 2
    text, refs, saves = parse(prompt)
    missing = [r for r in refs if not os.path.exists(r)]
    if missing:
        sys.exit("Thiếu ảnh mẫu: " + ", ".join(missing))
    if not saves:
        sys.exit("File prompt không có mục SAVE")
    msg = [f"Read the prompt file {prompt} and do exactly what it says.",
           f"Its reference images are also attached to this message, in the same order (attached image k = image k "
           f"of the file), so you can see them without opening them.",
           "Generate each image with your image generation tool, then save it exactly where the file says. Do not change, "
           "move or delete any other file. Do not ask questions: work alone until the images are saved."]
    if opts["steps"]:
        steps = opts["steps"].split(",")
        msg.append(f"In this run draw ONLY these steps, one image per step, in this order: {', '.join(steps)}. Ignore the "
                   f"file's ORDER section about waiting for \"next\": draw them all now, save each, then stop.")
    if opts["note"]:
        msg.append("Extra instruction for this run: " + opts["note"])
    exe = codex_exe()
    cmd = [exe, "exec", "-C", PROJECT, "-s", "workspace-write", "--skip-git-repo-check", "--color", "never"]
    for r in refs:
        cmd += ["-i", r]
    last = os.path.join(os.environ.get("TEMP", HERE), f"codex_last_{os.getpid()}.txt")
    cmd += ["-o", last, "--", "\n".join(msg)]
    before = snapshot(saves)
    t0 = time.time()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                            errors="replace")
    try:
        out, _ = proc.communicate(timeout=float(opts["timeout"]))
        code = proc.returncode
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
        out, code = "", "timeout"
    dur = round(time.time() - t0)
    after = snapshot(saves)
    new = sorted(p for p, t in after.items() if before.get(p) != t)
    reply = open(last, encoding="utf-8", errors="replace").read().strip() if os.path.exists(last) else ""
    rec = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "prompt": prompt, "steps": opts["steps"], "note": opts["note"],
           "exit": code, "sec": dur, "new": new, "reply": reply[-600:]}
    for d in saves:
        log = os.path.join(os.path.dirname(d.rstrip("\\/")), "gen_log.jsonl")
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        break
    if code != 0:
        tail = "\n".join(out.splitlines()[-15:]) if out else ""
        print(f"Codex kết thúc lỗi ({code}) sau {dur} s.\n{tail}")
    print(f"{dur} s, {len(new)} ảnh mới:")
    for p in new:
        print("  " + p)
    if not new:
        print("  (không có ảnh mới) Codex trả lời: " + reply[-400:])
    return 0 if new else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
