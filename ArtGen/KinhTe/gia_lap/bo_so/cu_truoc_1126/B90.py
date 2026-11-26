# Bộ B chạy 90 ngày (mốc so cho các bộ làm khó): số y như B_de_xuat.
import importlib.util, os
spec = importlib.util.spec_from_file_location("B", os.path.join(os.path.dirname(os.path.abspath(__file__)), "B_de_xuat.py"))
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)


def patch(b):
    B.patch(b)
