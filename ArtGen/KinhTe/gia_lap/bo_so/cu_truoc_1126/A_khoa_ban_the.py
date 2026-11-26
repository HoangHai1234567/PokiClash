# Bộ số A: y như game hiện tại, chỉ tắt "thu mua thẻ thừa" ở Chợ đen (vòng lặp bi vô hạn) để soi các dòng còn lại của đảo Casino.
def patch(b):
    b["casino"]["market"]["copySell"] = 0
