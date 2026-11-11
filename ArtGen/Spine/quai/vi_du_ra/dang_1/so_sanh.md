# vi_du_1: so với con gốc monster_3211

| | của mình | con gốc |
|---|---|---|
| Xương | 48 | 15 |
| Slot | 23 | 7 |
| Đỉnh lưới | 2101 | 81 |
| Tam giác | 3383 | 68 |
| Khoá | 3650 | 973 |
| MB | 0.08 (.atomik; json 273 KB + png 9 KB) | 0.12 (.skel + .atlas + .png) |
| Clip | appear 1.20s, idle 2.00s, attack 0.90s, cast 1.00s, skill 1.80s, hit 0.60s, die 1.60s, evolve 2.80s, aura 2.00s | block_01 0.50s, die_01 1.00s, floating_01 1.50s, hit_01 0.50s, hit_02 0.67s, idle_01 1.33s, run_01 0.57s, skill_01 1.00s, skill_02 1.17s, stun_01 1.33s |
| Lưới / mảnh cứng (gốc) |  | 5 / 4, tối đa 3 xương mỗi đỉnh, IK 0, transform 0, deform 0 timeline |

## Nối clip (khung cuối so với khung 0 idle)

- appear: khung cuối lệch khung 0 idle 0.00 px; khung đầu trống
- idle: bước khép vòng 0.49 px (bước thường 3.30)
- attack: khung cuối lệch khung 0 idle 0.00 px
- cast: khung cuối lệch khung 0 idle 0.00 px
- skill: khung cuối lệch khung 0 idle 0.00 px
- hit: khung cuối lệch khung 0 idle 0.00 px
- die: khung cuối trống
- evolve: khung cuối lệch khung 0 idle dạng sau 0.00 px; slot dạng cũ còn hiện: không (dạng sau co 0.853 trong rig gộp)

Lệch .atomik nạp lại so với bộ vẽ Python: khung 0 0.044 px (toạ độ gắn); giữa clip 1.20 px (lược khoá RDP).
