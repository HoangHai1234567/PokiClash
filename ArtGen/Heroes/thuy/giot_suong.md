# Giọt Sương: tướng Thủy đầu tiên (dòng 3 dạng)

Dòng khởi đầu hệ Nước của aola: #7 滴滴 → #8 露滴 → #9 露西亚. Cả ba đều là con vector, nên thay tạo hình mà giữ được animation. Quy trình chung: [../QUY_TRINH.md](../QUY_TRINH.md).

Mỗi dạng một file, có đủ bảng giải phẫu, prompt concept và 8 prompt nhóm mảnh:

| Dạng | aola | File | Rig | Gen khi nào |
|---|---|---|---|---|
| 1 | #7 滴滴 (đứng hai chân) | [giot_suong_1.md](giot_suong_1.md) | `<aola>/reskin/pet7_parts`, `thuy_7` | **gen thử ngay** |
| 2 | #8 露滴 (đứng hai chân, tay vây, đuôi dài) | [giot_suong_2.md](giot_suong_2.md) | `<aola>/reskin/pet8_parts`, `thuy_8` | sau khi duyệt concept dạng 1 |
| 3 | #9 露西亚 (bốn chân, cổ dài) | [giot_suong_3.md](giot_suong_3.md) | `<aola>/reskin/pet9_parts`, `thuy_9` | sau khi duyệt concept dạng 2 |

Dạng nào ứng với sao nào chưa chốt (việc dữ liệu, xem `GD_Claude/13_DanhSachTuong.md`).

## Hướng thiết kế cả dòng

Do Claude đề xuất, duyệt ở bước concept. Một con **kỳ giông sen** lớn dần:

1. **Bé kỳ giông:** đầu bè, hai chùm mang ba nhánh, nụ sen trên đỉnh, yếm lá sen, đuôi vây.
2. **Kỳ giông non:** bốn chùm mang dày, hoa sen hé nở, tay thành vây màng, đuôi dài có quạt cánh sen.
3. **Thủy long sen:** cổ dài, bốn chân, mặt hiền kiểu kỳ giông, ba chùm mang lông vũ, chuỗi hạt sen, quạt đuôi cánh sen to.

Giữ xuyên suốt: da xanh da trời, bụng kem, mang hồng san hô, chi tiết sen xanh lá và dây đỏ. Concept dạng sau đính kèm concept dạng trước để vẫn là một con.

Dáng ngoài đổi cho khác bản gốc (đầu, mang, mào, thùy đuôi); thân, tay, chân giữ viền để khớp rig.

## Thứ tự gen

1. Concept dạng 1 → Claude duyệt → 8 nhóm dạng 1 → Claude ghép.
2. Concept dạng 2 (đính concept dạng 1) → duyệt → 8 nhóm → ghép.
3. Concept dạng 3 (đính concept dạng 2) → duyệt → 8 nhóm → ghép.

Nhóm mảnh của một dạng gen được ngay khi concept của dạng đó đã duyệt, không cần chờ ghép dạng trước.
