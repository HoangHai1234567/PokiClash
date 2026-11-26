# Bộ K3_goi_moc3: K0 + giả lập gói tướng trọn bộ: mốc 3 (3 sao, thẻ cấp 2) ngày 2
import importlib.util, os
spec = importlib.util.spec_from_file_location("K0", os.path.join(os.path.dirname(os.path.abspath(__file__)), "K0_gian_moc.py"))
K0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K0)
patch_stages = K0.patch_stages


def patch(b):
    K0.patch(b, [{'day': 2, 'moc': 3, 'star': 3, 'card': 2}])
