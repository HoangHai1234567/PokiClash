# Bộ K6t_chi_mo_khoa: K0 + giả lập gói tướng trọn bộ: chỉ mở khoá (1 sao, thẻ cấp 1): mốc 3 ngày 2, mốc 6 ngày 7
import importlib.util, os
spec = importlib.util.spec_from_file_location("K0", os.path.join(os.path.dirname(os.path.abspath(__file__)), "K0_gian_moc.py"))
K0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K0)
patch_stages = K0.patch_stages


def patch(b):
    K0.patch(b, [{'day': 2, 'moc': 3, 'star': 1, 'card': 1}, {'day': 7, 'moc': 6, 'star': 1, 'card': 1}])
