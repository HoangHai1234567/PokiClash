# Bộ L9_moc9_ngay7: K0 + giả lập gói tướng đi trước xa: mốc 6 ngày 2, mốc 9 (11 sao, thẻ cấp 4) ngày 7
import importlib.util, os
spec = importlib.util.spec_from_file_location("K0", os.path.join(os.path.dirname(os.path.abspath(__file__)), "K0_gian_moc.py"))
K0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K0)
patch_stages = K0.patch_stages


def patch(b):
    K0.patch(b, [{'day': 2, 'moc': 6, 'star': 6, 'card': 3}, {'day': 7, 'moc': 9, 'star': 11, 'card': 4}])
