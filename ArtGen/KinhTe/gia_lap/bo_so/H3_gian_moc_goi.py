# Vòng 1: H2 (giãn sức theo mốc) + cùng gói tướng như H1.
import importlib.util, os


def _load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(os.path.abspath(__file__)), n + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


H1, H2 = _load("H1_goi_khong_gian"), _load("H2_gian_moc")
patch_stages = H2.patch_stages


def patch(b):
    H2.patch(b, H1.GRANTS)
