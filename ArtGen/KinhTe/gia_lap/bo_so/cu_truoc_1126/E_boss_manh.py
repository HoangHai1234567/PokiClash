# Bộ E: D + mini boss / boss mạnh hơn (máu x1,8 -> x2,3; công x1,1 -> x1,25). Đã đo 2026-11-26: gần như không đổi thời gian phá đảo
# (GD_Claude/34 mục 1.4), nên không đề xuất. Giữ file để chạy lại.
import importlib.util, os
spec = importlib.util.spec_from_file_location("D", os.path.join(os.path.dirname(os.path.abspath(__file__)), "D_exp_doc.py"))
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)


def patch(b):
    D.patch(b)
    b["cfg"]["bossHp"] = 2.3
    b["cfg"]["bossAtk"] = 1.25
