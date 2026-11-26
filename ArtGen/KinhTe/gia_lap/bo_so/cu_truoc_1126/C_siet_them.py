# Bộ số C: bộ B + siết thu nhập bi thụ động khoảng 25% (cây bi 4 -> 3 bi / giờ, chứa 96 -> 72; ruộng Nhà 2 -> 1,5 bi / giờ).
# Để đo: người chơi vừa không trả tiền có bắt đầu gặp tường không, quảng cáo và gói bi có thêm vai trò không.
import importlib.util, os
spec = importlib.util.spec_from_file_location("B", os.path.join(os.path.dirname(os.path.abspath(__file__)), "B_de_xuat.py"))
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)


def patch(b):
    B.patch(b)
    b["trees"]["perHour"] = 3
    b["trees"]["cap"] = 72
    b["farm"]["base"] = 1.5
