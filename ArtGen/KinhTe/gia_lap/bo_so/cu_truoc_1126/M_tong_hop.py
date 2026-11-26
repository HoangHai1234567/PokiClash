# Bộ M: gộp các đề xuất đo được của GD_Claude/33, 34, 35 (chạy 90 ngày):
# - bộ B (sửa đảo Casino, trứng rương, đánh lại ải, Bỏ quảng cáo, Gói Tiếp Sức) + đường EXP dốc (bộ D);
# - cửa hàng: bỏ Trứng Khá; nạp đầu 3 bậc chọn 1 thay Gói Khởi Hành; gói đá tiến hóa ngày / tuần; Thẻ Phiêu Lưu thêm 1 đá mỗi ngày;
#   gói sự kiện 3 bậc; vật phẩm "x2 EXP máy bi" trong gói bi từ 9,99 USD và gói sự kiện bậc 3; Lọ Bi theo lịch xoay 9 ngày (mở 3 ngày).
# Mua gì là giả định của persona (runner/EconSim.cs, Shopping).
import importlib.util, os
spec = importlib.util.spec_from_file_location("D", os.path.join(os.path.dirname(os.path.abspath(__file__)), "D_exp_doc.py"))
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)


def patch(b):
    D.patch(b)
    sh = b["shop"]
    packs = [p for p in sh["packs"] if p["id"] not in ("egg_1", "launch")]
    def pack(id, name, price, items, **kw):
        d = {"id": id, "name": name, "desc": "", "tab": "offers", "price": price, "scale": True, "sort": 50, "items": items}
        d.update(kw)
        packs.append(d)
    pack("first_1", "Nạp đầu bậc 1", 4.99, [{"k": "balls", "n": 1000}, {"k": "egg", "n": 2, "r": 2}, {"k": "evo", "n": 5}], limit=1)
    pack("first_2", "Nạp đầu bậc 2", 9.99, [{"k": "balls", "n": 3000}, {"k": "egg", "n": 2, "r": 2}, {"k": "egg", "n": 1, "r": 3}, {"k": "evo", "n": 10}], limit=1)
    pack("first_3", "Nạp đầu bậc 3", 19.99, [{"k": "balls", "n": 6400}, {"k": "egg", "n": 3, "r": 3}, {"k": "evo", "n": 20}, {"k": "ticket", "n": 1, "r": 3}], limit=1)
    pack("evo_daily", "Đá tiến hóa hôm nay", 1.99, [{"k": "evo", "n": 5}], limit=1, daily=True)
    pack("evo_week", "Túi đá tuần", 4.99, [{"k": "evo", "n": 15}, {"k": "egg", "n": 1, "r": 3}], limit=1, weekly=True)
    pack("event_1", "Gói sự kiện nhỏ", 1.99, [{"k": "balls", "n": 250}, {"k": "shards", "n": 5, "h": "*feat"}])
    pack("event_2", "Gói sự kiện vừa", 4.99, [{"k": "balls", "n": 700}, {"k": "shards", "n": 10, "h": "*feat"}, {"k": "evo", "n": 2}])
    pack("event_3", "Gói sự kiện lớn", 9.99, [{"k": "balls", "n": 1500}, {"k": "shards", "n": 20, "h": "*feat"}, {"k": "evo", "n": 5}])
    sh["packs"] = packs
    for c in sh["cards"]:
        if c["id"] == "month":
            c["daily"] = c["daily"] + [{"k": "evo", "n": 1}]
    b["sim"]["piggyGapDays"] = 3  # cùng lịch xoay: mỗi đợt mở đập được một lần
    b["sim"]["piggyRotate"] = 9
    b["sim"]["x2Packs"] = ["balls_3", "balls_4", "balls_5", "balls_6", "refill_3", "event_3"]
    b["sim"]["x2Balls"] = 20000
