# Bộ D: B + đường EXP dốc dần. EXP lên cấp = 9 × cấp^1,54 (hiện 45 × cấp): 20 cấp đầu nhanh bằng hoặc hơn hiện nay,
# cấp 100 tốn gấp 2,4, cấp 200 gấp 3,5; tổng EXP tới cấp 200 gấp khoảng 2,7.
import importlib.util, os
spec = importlib.util.spec_from_file_location("B", os.path.join(os.path.dirname(os.path.abspath(__file__)), "B_de_xuat.py"))
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)


def patch(b):
    B.patch(b)
    b["progression"]["expBase"] = 9
    b["progression"]["expPow"] = 1.54
