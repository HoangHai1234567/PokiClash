# -*- coding: utf-8 -*-
"""mở xem.html bằng Chrome ngầm, in dòng trạng thái, nút clip và lỗi JS."""
import os
import re
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")
page = sys.argv[1]
CH = [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]
exe = [c for c in CH if os.path.exists(c)][0]
prof = tempfile.mkdtemp(prefix="xem_")
url = "file:///" + page.replace("\\", "/")
r = subprocess.run([exe, "--headless=new", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--user-data-dir=" + prof,
                    "--enable-logging=stderr", "--v=0", "--virtual-time-budget=8000", "--dump-dom", url],
                   capture_output=True, timeout=120)
dom = r.stdout.decode("utf-8", "replace")
err = r.stderr.decode("utf-8", "replace")
print("DOM", len(dom), "ký tự")
m = re.search(r'id="st"[^>]*>([^<]*)', dom)
print("trạng thái:", m.group(1) if m else "(không thấy #st)")
print("nút clip:", re.findall(r'data-clip="([^"]*)"', dom))
for ln in err.splitlines():
    if "CONSOLE" in ln or "Uncaught" in ln or "not found" in ln.lower():
        print("JS:", ln[-300:])
