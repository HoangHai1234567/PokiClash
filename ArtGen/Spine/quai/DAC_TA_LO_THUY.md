# Đặc tả lô 10 dòng tướng mới đảo Thủy (2026-11-11)

File chung cho mọi agent của lô. Ai làm phần nào cũng đọc hết file này trước, rồi đọc các skill ở mục 2. Trả lời, ghi chú,
HUONG_DAN bằng tiếng Việt; file prompt gửi GPT bằng tiếng Anh.

## 1. Việc và phân công

Người dùng gửi 9 con gốc của game tham khảo Sword x Staff (bản rút: `D:\RefAnimation\SwordxStaff\web\assets\Monster\monster_<số>\`
gồm `.skel` Spine 4.2, `.atlas`, `.png`; trang xem `http://localhost:8765/index.html` khi server đang chạy) và con Hải Long Ngũ Đầu
đã dựng (`ArtGen/Spine/hai_long.py`, dựa trên `monster_3705`). Đây là 10 tướng mới của đảo Thủy, theo thứ tự ải.

| # | Mã làm việc | Con gốc | Con gốc là | Phải làm | Agent | Thay suất đảo (ải, tướng cũ, độ hiếm cũ) |
|---|---|---|---|---|---|---|
| 1 | `tm01` | monster_3211: giọt nước xanh mập, mắt trắng cau có, hai vây nhỏ, chóp nhọn | dạng 1 | vẽ lại dạng 1, thêm dạng 2 | opus | ải 1, Thủy Long, uncommon, **tướng khởi đầu** |
| 2 | `tm02` | monster_3227: cua mang tảng đá trên lưng, hai càng băng xanh nhạt, một mắt đỏ trong hốc tối | dạng 1 | vẽ lại dạng 1, thêm dạng 2 | opus | ải 5, Tiểu Y, common |
| 3 | `tm03` | monster_3230: nòng nọc/ếch tròn xanh tím, hai tai xoắn ốc, bụng kem, mặt nạ trắng | dạng 1 | vẽ lại dạng 1, thêm dạng 2 | opus | ải 10, Cánh Cụt, common |
| 4 | `tm04` | monster_3233: thú tròn xanh lam, hai lá/ngạnh vàng sau lưng, đuôi ngọn lửa xanh ngọc, mắt to một bên | dạng 1 | vẽ lại dạng 1, thêm dạng 2 | opus | ải 15, Mi Nhi, uncommon |
| 5 | `tm05` | monster_3237: con sò/cầu gai vỏ xanh lam, gai vàng, miệng hồng hé giữa hai mảnh vỏ | dạng 1 | vẽ lại dạng 1, thêm dạng 2 | opus | ải 20, Ma Kết, rare |
| 6 | `tm06` | monster_3241: ếch thủy quái xanh lục cõng thùng gỗ buộc dây đỏ, tóc lá, đĩa trên đầu, mỏ vàng | dạng 1 | vẽ lại dạng 1, thêm dạng 2 | opus | ải 30, Vây Lam, rare |
| 7 | `tm07` | monster_3244: cá voi/kỳ lân biển xanh ngọc, sừng xám, đóa sen hồng trên lưng | dạng 2 | vẽ lại dạng 2, thêm dạng 1 | fable | ải 40, Kuba, epic |
| 8 | `tm08` | monster_3247: rắn rồng con xanh ngọc vân xoắn, bụng hồng kem, vây tai, mắt hồng | dạng 2 | vẽ lại dạng 2, thêm dạng 1 | fable | ải 50, Thương Lam, epic |
| 9 | `tm09` | monster_3281: thú bò sát trắng sừng đen cong, hàm răng to nhe ra, lòng miệng tím, đuôi pha lê tím | dạng 2 | vẽ lại dạng 2, thêm dạng 1 | fable | ải 60, Huyền Vũ, legend |
| 10 | `tm10` (dạng 1, 2), `hai_long` (dạng 3) | monster_3705 qua Hải Long | dạng 3 | thêm dạng 1, 2; **dựng lại dạng 3 với lưới dày hơn** | fable | ải 70, Lam Quân, epic (boss cuối đảo) |

Ảnh chụp người dùng gửi (trang xem, tư thế idle), theo thứ tự dòng 1 → 9:
`C:\Users\ADMIN\AppData\Local\Temp\claude\5e92ce638305c490\7f704dd5-4cf4-4c60-91e3-810a2b39cc4a\images\1.png` … `9.png`.

Kết quả quét xương, lưới, khoá của con gốc (chạy `mo_xe/chay.py`, xong dần): `D:\RefAnimation\SwordxStaff\scan\monster_<số>\info.json,
mesh.json, keys.json`. Đọc bằng Python; `ArtGen/Spine/mo_xe/nhip.py` đọc nhịp từ khoá thật.

Dòng 1–9 có 2 dạng, dòng 10 có 3 dạng. Mỗi dạng đều phải có đủ bộ clip ở mục 5. Hiệu ứng (tia, đạn, vụ nổ) **không nằm trong rig**:
rig chỉ để chỗ bám (xương miệng, sự kiện), lớp VFX trên sân làm sau ở một bước riêng.

## 2. Đọc trước khi làm (bắt buộc)

- `.claude/skills/skill-petclash/SKILL.md` (đọc hết, nhất là mục 7, 14, 15) và `mo_xe_quai_nhieu_dau.md` (đọc hết, nhất là mục
  3b, 6b, 9 và **mọi mục "Lỗi đã gặp"**).
- `.claude/skills/pokiclash-spine-rig/SKILL.md`: mục 0a (tiêu chí bắt buộc), 7 (lỗi), 9 (.atomik, bản 2, bản 3), 11 (tiến hóa nối
  liền), 17 (thân rắn, lò xo bờm, dạng cuối khác hẳn), 18 (chiêu đa dạng, há miệng), 20 (rig dựng bằng mã, toàn bộ).
- `CLAUDE.md` của dự án (luật file prompt `ArtGen/**`, luật hình tướng: nét bút mực + chì sáp, **tô phẳng, không bóng, không ánh
  sáng**, viền trắng giấy xé do game vẽ) và `ArtGen/README.md` mục "Luật chung" (câu dán vào prompt).
- Mẫu đã chạy: `ArtGen/Spine/build_hai_long.py` + `gui_gpt/hai_long/*.txt` (gói prompt), `ArtGen/Spine/hai_long.py` (rig bằng mã).

## 3. Luật thiết kế

- **Thiết kế khác hẳn con gốc.** Chỉ giữ dáng cơ thể và chủ đề (giọt nước, cua đá, ếch tai xoắn...) làm điểm xuất phát; hình, màu,
  chi tiết, diễn xuất là của mình. Con gốc là của nhà phát hành khác: **không đính ảnh con gốc hay ảnh chụp trang xem vào prompt GPT**,
  chỉ tả bằng lời. Ảnh mẫu đính cho GPT chỉ là ảnh của dự án (mục 4).
- Nét của dự án (không phải nét Sword x Staff): bút mực nâu `#2B2118` hơi rung, tô chì màu và sáp màu, mỗi vùng một màu đều, vân chì
  chỉ là vân; không bóng, không điểm sáng (trừ một chấm sáng nhỏ trong mắt), không bóng loáng, không quầng sáng, nền trắng tinh.
- **Chibi chỉ ở dạng 1.** Dạng sau tỉ lệ trưởng thành, dữ, chiến, ngầu và đẹp hơn (đầu nhỏ lại, mắt sắc, nanh, móng, thế đánh).
  **Dạng cuối khác hẳn dạng trước**: đổi màu chủ đạo (đậm hơn), thêm giáp/đồ/phụ kiện, đổi chi tiết đặc trưng và đổi bóng dáng, vẫn
  giữ vài nét nhận ra cùng dòng. Tướng là sinh vật kiểu thú nuôi, mặt quả quyết; không linh vật vui tươi, không đáng sợ.
- Càng gần boss cuối đảo (dòng sau) càng hoành tráng; độ hiếm cột cuối bảng mục 1 cho biết tầm cỡ.
- Hướng: con vật nhìn sang **phải người xem** (như mọi tướng `.atomik`), góc nghiêng 3/4 hoặc nhìn ngang.
- Hệ Thủy: lam, trắng bọt; mỗi dòng một bảng màu riêng, không trùng nhau và không trùng 13 tướng Thủy đang có.

## 4. Pha 1: thiết kế và concept (làm ngay)

1. Xem con gốc: ảnh chụp, atlas `.png` (thấy cách cắt mảnh), và khi có thì `scan/monster_<số>/info.json` (số xương, slot, lưới,
   clip, thời lượng). Ghi nhận: dáng, cách cắt mảnh, bộ phận nào cử động, clip nào có.
2. Thiết kế cả dòng bằng chữ: tên tiếng Việt của dòng (và từng dạng nếu khác), ý lore, bảng màu (mã hex), chi tiết từng dạng, đòn
   đánh / chiêu bắn / chiêu cuối của từng dạng (theo lore và chiêu Pokémon hệ nước; phần lớn đứng tại chỗ; dạng sau mạnh hơn, đổi
   kiểu), bộ phận sẽ tách mảnh ở pha 2.
3. Gói prompt: viết `ArtGen/Spine/build_<mã>.py` (mẫu `build_hai_long.py`) sinh `ArtGen/Spine/gui_gpt/<mã>_<k>/luot_1_concept.txt`
   và `HUONG_DAN.md`; ảnh lưu `ArtGen/Spine/inbox/<mã>_<k>/tai_ve/L1_concept.png`. Luật file prompt theo CLAUDE.md: mở đầu danh
   sách ảnh mẫu đường dẫn **tuyệt đối tính từ chỗ đặt script** (không ghi cứng ổ đĩa), mục SAVE đúng dạng
   `save it as a PNG to <đường dẫn>` (trùng tên thì `_2`, `_3`…, không sửa/dời/xoá file khác), tự đủ, không nhắc tên game nào.
   Ảnh mẫu: `ArtGen/Islands/refs/world_style.png` (nét), một hai concept tướng Thủy đã duyệt của dự án khác loài
   (`ArtGen/Spine/inbox/<dạng>/tai_ve/L1_duyet.png` hoặc `L1_lien.png`), và với dạng thứ hai trở đi: concept dạng đã chọn của dòng.
   Concept là con trọn vẹn một ảnh, nền trắng, dáng dễ tách mảnh (chân tay tách thân, không chéo nhau, miệng hé để thấy lòng miệng).
4. Gen: `py -3 -I ArtGen/Spine/gen.py ArtGen/Spine/gui_gpt/<mã>_<k>/luot_1_concept.txt` (chạy nền; gen.py tự xếp hàng theo khoá
   Codex chung, mỗi lúc một lệnh trên cả máy, khoảng 2 phút một ảnh; thêm `--note "..."` để sửa nhanh). Tự mở ảnh ra xem; lệch
   thiết kế, có bóng, có điểm sáng, sai hướng thì gen lại (tối đa 3 lần mỗi dạng ở pha này). Dạng đầu chọn xong mới dựng prompt dạng sau.
   Hết hạn mức Codex: kiểm theo `pokiclash-spine-rig` mục 2, ghi giờ mở lại vào báo cáo, đừng chờ mù.
5. **Dừng ở đây và báo cáo** (mục 8). Không gen tờ mảnh, không rig trước khi người dùng duyệt concept.

## 5. Pha 2: tờ mảnh, rig, animation, xuất (chỉ làm khi được báo "đã duyệt")

- Cách dựng như Hải Long (`pokiclash-spine-rig` mục 20): GPT vẽ **tờ mảnh rời vẽ đủ phần bị che** (đầu, hàm dưới có lòng miệng,
  mắt nhắm / mí, lưỡi, chi, đuôi, vây, phụ kiện...); cắt mảnh; rig dựng bằng mã ra JSON Spine 4.2 rồi `.atomik`.
- **Cách lai (chuẩn từ 2026-11-11 04:00, sau khi soi dòng 7, 9):** thân hình cong tròn (cá voi, cá sấu, kỳ giông, hà mã, sò...)
  mà dựng từ mảnh GPT thì GPT vẽ thành ống thẳng, ghép lại lộ khúc ống, khe trắng, đầu cụt, IoU kẹt 0,6–0,7 (đúng lỗi người dùng chê
  ngày 11-08). Vì vậy: **mảnh thân chính (và các phần liền với thân, không cần tách) cắt thẳng từ concept** (khớp ~100%, kiểu
  `thuy_long_lien.py`: vùng theo nét mực, hạt giống, nhãn gần nhất); **tờ mảnh GPT chỉ dùng cho phần phải tách hoặc bị che**: hàm
  dưới + lòng miệng + lưỡi, mí, chi/vây phía xa, phụ kiện chồng lớp (sen, bình, giáp rời), và làm **nguồn vẽ bù** vùng thân bị các
  phần tách che (dán hình mảnh GPT đã khớp vào chỗ khuyết thay vì loang màu). Con nhiều cổ / thân rắn dài (dòng 10, 8) giữ dải mảnh
  GPT nếu IoU đạt. Đích IoU khung 0 với concept ≥ 0,9 khi dùng cách lai.
  Dùng thư viện chung `ArtGen/Spine/quai/` (có README) khi nó xong; thiếu gì thì viết trong file riêng của dòng, không sửa thư viện.
- **Lưới dày, mịn, đều** (người dùng yêu cầu chất lượng cao): mọi mảnh mềm là lưới tam giác gần đều cạnh, đỉnh cách nhau đều trên
  viền và bên trong (con số đích ở README thư viện), không tam giác mảnh dài; trọng số trơn (chuỗi: B-spline bậc hai; vùng: hoà theo
  khoảng cách đi trong hình), tối đa 4 xương mỗi đỉnh, không đỉnh nào bám cứng 100% một xương trừ đồ cứng thật (vỏ, sừng, đá).
  Xương đủ để mềm: thân, cổ, đuôi, vây, tai, râu là chuỗi nhiều đốt; phần mềm (râu, bờm, lưỡi, dây) mô phỏng dây rồi nướng.
- Bộ clip mỗi dạng (tên trong file là tên game đọc; nhịp gốc ở `skill-petclash` 7.1 và bảng Hải Long mục 15):

| Clip | Ý | Ghi chú |
|---|---|---|
| `appear` | xuất hiện (như `xuat_hien` của Hải Long) | khung đầu trống hoặc hình tụ lại; kết thúc đúng khung 0 của `idle` |
| `idle` | đứng, lặp liền | thở, phụ kiện lệch pha, điểm phá nhịp (chớp mắt, táp miệng...) |
| `attack` | đòn thường | lấy đà ngược chiều, ra đòn 1–3 khung, giữ có trôi, về; sự kiện `trung` ở khung trúng |
| `cast` | chiêu bắn (như `chieu_phun`) | đứng tại chỗ, há miệng / giơ chỗ phát; sự kiện `phun`, `het_phun`; xương `mieng` (trục x chĩa hướng nhả) |
| `skill` | chiêu cuối (như `chieu` gầm) | tụ lực, bung, giữ rung hai dáng; sự kiện `gam`, `het_gam` hoặc riêng theo chiêu |
| `hit` | trúng đòn | không lấy đà, đỉnh ở 0,07 s, sóng chạy từ ngọn về gốc, mắt nhắm |
| `die` | chết (như `chet`) | giật, nhắm mắt, lả đi giữ một nhịp, đổ, tan; khung cuối trống |
| `evolve` | tiến hóa (mọi dạng trừ dạng cuối) | rig gộp dạng sau (`pokiclash-spine-rig` mục 11), 2,8 s, đổi dạng lúc lốc đậm nhất, khung cuối trùng khung 0 `idle` dạng sau |
| `aura` (tuỳ) | lặp chồng lên mọi clip | thứ bay quanh, nước dưới chân chạy liền qua mọi lần đổi clip |

  Mọi clip không lặp nối về khung 0 `idle` không giật (đo lệch, ghi vào báo cáo). Dạng sau lấy đà dài hơn, ổn định hơn, chiêu dữ hơn.
- Dung lượng: con gốc 0,1–0,3 MB. Đích mỗi dạng dòng 1–9: `.atomik` ≤ 0,3 MB, trần 0,5 MB. Dòng 10: dạng 1–2 ≤ 0,6 MB, dạng 3 giữ
  quanh 1,1 MB dù lưới dày hơn. Cách giữ: atlas bảng 256 màu, cạnh bội 8; lọc khoá RDP; dùng lại hình (lật bằng tỉ lệ âm).
- Ra: `ArtGen/Spine/inbox/<mã>_<k>/rig/`: `<mã>_<k>.json/.atlas/.png`, `<mã>_<k>.atomik`, `<mã>_<k>_game.json`, `xem.html` (trang xem một
  file), `khung_<clip>.png` (12 khung), `luoi.png` (lưới + trọng số), ảnh cận miệng, khớp, `so_sanh.md` (số xương, slot, đỉnh, tam giác,
  khoá, MB so với con gốc), chân dung vuông 512 không bóng. **Không chép vào `Assets/`** (Claude điều phối làm bước vào game).
- Soi trước khi báo (bắt buộc, `skill-petclash` mục 14 và 15 "Kiểm"): tờ khung từng clip, soi cận ở khung nhanh nhất (miệng há to
  nhất, ngửa đầu, khớp, râu), mí phủ kín (in "còn hở 0 px"), lệch khung cuối so với `idle`. Nói rõ cái gì chưa xem ở tốc độ thật.
- **Bài học từ lần soi đầu (dòng 9, 2026-11-11), mọi dòng phải kiểm:**
  - `so_concept.png`: khung t=0 idle đặt cạnh concept cùng tỉ lệ; **bóng dáng phải khớp concept** (sừng, mào, đuôi, vây, tỉ lệ đầu
    thân). Lỗi đã gặp: sừng lớn nằm bẹp sau gáy bị gờ vai che gần hết; đuôi dày trong concept thành cái que mảnh vì GPT vẽ mảnh
    đuôi mảnh mà rig chỉ co dài. Dải lưới có độ dày thay đổi dọc chiều dài, hoặc gen lại mảnh.
  - Đo lệch nối clip **trên đỉnh lưới đã vẽ của mọi slot** (gồm lò xo, dây mềm, độ cong mặc định), không chỉ xương: mọi clip khung 0 =
    khung cuối = khung 0 `idle` thật sự (lỗi đã gặp: attack khung 0 đuôi duỗi thẳng, skill khung 0 đuôi cong vểnh, số đo vẫn báo 0 px).
  - Nhịp đòn đúng chiều: phần nện (đuôi, chùy, nắm đấm) nhấc lên lúc lấy đà, chạm đúng khung `trung`, rồi về; không dựng lên sau cú đánh rồi giữ.
  - **Mật độ lưới theo chiều cao con, không theo pixel cố định** (bài học dòng 1: con cao 380 px dùng bước mặc định 11/15 px chỉ ra
    993 đỉnh, tay 72 đỉnh, tam giác to, không đạt "dày mịn"): bước viền ≈ 1,5% chiều cao con, bước trong ≈ 2% (con cao 380 px:
    khoảng 6 / 8 px). Mỗi mảnh thân, đầu, chi đều thấy lưới đều dày; dạng cuối cỡ vừa thường 2000–4000 đỉnh. Mọi mảnh "hở 0 px"
    (không chấp nhận hở 1–2 px). In số đỉnh / chiều cao vào `so_sanh.md`. Vẫn giữ dung lượng trong đích.
  - Chi vẽ thành nhiều đoạn rời (đùi, ống, bọc) dễ thiếu đoạn hoặc lộ "miệng ống": vẽ chi liền một mảnh từ hông/vai tới cổ chân/cổ
    tay khi được (như `pokiclash-spine-rig` mục 11), không để đoạn nào trông lơ lửng.
  - **Prompt tờ mảnh phải đính concept đã chọn và dặn GPT vẽ từng mảnh đúng hình, đúng tỉ lệ như trên concept** ("same silhouette
    and proportions as in image N", kể cả cổ, họng, ngực, bụng, hàm dưới to bản), chỉ thêm phần bị che. Lỗi đã gặp (dòng 9): tờ thân
    không có cổ, tờ đầu không có họng, hàm nhỏ hơn concept → dò vị trí, tỉ lệ thế nào IoU cũng kẹt ở 0,66, phải gen lại.
  - **Đặt mảnh khớp vào concept bằng dò tự động** (tỉ lệ, góc, vị trí theo mặt nạ: SQDIFF có mặt nạ dò thô rồi tinh như `rig.place`,
    `thuy_long.place`; mảnh vẽ khác concept thì đặt theo hai đầu khớp đọc trên concept), không đoán hệ số tay. Đích: IoU mặt nạ khung
    0 idle với concept ≥ 0,85 (in ra trong `so_concept.png`), trừ chỗ cố ý đổi có ghi rõ. Lỗi đã gặp: thân gầy thấp như thằn lằn trong
    khi concept là thú to ngực sâu; sừng gắn vào cổ thay vì đỉnh sọ; gờ lưng lơ lửng có khe sáng bên dưới (chân gờ phải chồng vào thân).

## 6. An toàn máy và phối hợp (bắt buộc)

- Máy này từng sập cứng khi Chrome ngầm vẽ. **Mọi lệnh mở Chrome/Edge ngầm** (`mo_xe/chay.py`, soi bằng runtime Spine) chạy qua
  `py -3 -I ArtGen/Spine/quai/khoa.py chrome -- <lệnh>` (1 suất cả máy). **Việc Python nặng chạy lâu** (nướng animation, dựng lưới,
  xuất atlas) chạy qua `khoa.py nang -- <lệnh>` (2 suất). Gen ảnh chỉ qua `gen.py` (khoá Codex riêng).
- Không đụng Unity (không MCP Unity, không menu), không sửa `Assets/`, `heroes.json`, `stages.json`. Không chạy lệnh git ghi.
  Không xoá file (ghi đè file do chính mình sinh thì được). Không đăng artifact.
- Chỉ sửa file của mình: `build_<mã>.py`, `<mã>.py` (và module riêng `<mã>_*.py`), thư mục `gui_gpt/<mã>_*`, `inbox/<mã>_*`. Dòng 10
  thêm `build_hai_long.py`, `hai_long.py`, `inbox/hai_long/`, `gui_gpt/hai_long/`. File chung (`beast.py`, `beasts_cfg*.py`,
  `longrig.py`, `atomik.py`, `gen.py`, `mo_xe/*`, `quai/*`) chỉ đọc; cần sửa thì ghi vào báo cáo.
- Python (sửa 2026-11-11 sau khi thư viện xong): `py -3` (3.14) có numpy, Pillow, shapely nhưng **không có cv2**; cv2 chỉ có ở
  `D:/spine-venv/Scripts/python -I` (script cũ như `hai_long.py` chạy bằng venv này). Thư viện `quai/` chỉ dùng numpy + Pillow,
  chạy được cả hai. `-I` không thêm thư mục script vào `sys.path`: script dòng tự `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`
  trước `from quai import ...`. In tiếng Việt `sys.stdout.reconfigure(encoding="utf-8")`. Đầu ra lệnh ngắn (lọc, `tail`). Heredoc
  Bash dài hay bị cắt: viết script bằng Write rồi chạy.
- Thư viện `ArtGen/Spine/quai/` đã xong (đọc `quai/README.md`, mục 5 là mười bước cho agent dòng; con thử `quai/vi_du.py`,
  kết quả `quai/vi_du_ra/`). Sân luôn kéo `attack` lao tới đối thủ trừ khi khai `attack` trong `dung_yen` của `xuat_het`.
  Sóng nước kiểu Hải Long và giải cổ dài chưa có trong thư viện: chép từ `hai_long.py` vào file riêng của dòng.
  Thêm 2026-11-11 04:10: `luoi.luoi_dai(..., mu=True, buoc_theo_cao=H)` (mũ tròn hai đầu, hở 0; bước theo chiều cao con) và
  `luoi.luoi_vung(..., buoc_theo_cao=H)` (viền 1,5% H, trong 2% H). Dùng hai tham số này để đạt luật mật độ ở mục 5.

## 7. Model

Dòng 1–6 do agent Opus làm, dòng 7–10 do agent Fable làm (người dùng chỉ định). Thư viện `quai/` do một agent riêng làm.

## 8. Báo cáo cuối mỗi pha (gửi Claude điều phối, tiếng Việt, gọn)

Pha 1: tên dòng đề xuất, bảng màu, mô tả từng dạng (3–5 dòng), đường dẫn concept đã chọn và các bản khác, khác con gốc ở đâu, dự
kiến tờ mảnh và xương cho pha 2, đòn/chiêu từng dạng, vướng mắc. Pha 2: đường dẫn kết quả, số đo `so_sanh.md`, những gì đã soi và
chưa soi, lỗi còn lại, việc cần Claude làm khi đưa vào game.
