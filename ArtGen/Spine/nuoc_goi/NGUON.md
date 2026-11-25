# Nguồn texture của bộ nước (atlas nuoc_fb.png, nuoc_vet.png)

Người dùng 2026-11-25 cho dùng thẳng texture của hai gói mẫu, có biến đổi (độ sáng → dải màu cel của game + vân chì). Gói SrRubfish "Water - Assets for VFX 02" tải qua Baidu Netdisk, chưa rõ đã mua trên Asset Store: nếu chưa, phải thay các flipbook dưới đây bằng bản tự làm trước khi phát hành (chạy lại dong_goi.py với nguồn mới, giữ mã).

| Mã | Nguồn (Assets/SrRubfish_VFX_02/Textures/) | Khung | Dùng cho |
|---|---|---|---|
| `Xoan` | `Flipbooks/Water/FX_TX_TwirlingWater_2x8_01.png` | 16 | vệt xoắn cuộn quanh thân tia / mũ đầu tia (Water Laser LaserNoise03/05) |
| `NuocNgang` | `Flipbooks/Water/FX_TX_LateralWater_01_3x4.png` | 12 | lá nước xoay ở đầu tia (Laser LaserNoise06) |
| `VongNuoc` | `Flipbooks/Water/FX_TX_TiledWater_3x4_01_SoftRender.png` | 12 | vòng nước nở quanh thân tia / gốc (Laser WaterAOE) |
| `Toe` | `Flipbooks/Water/FX_TX_NormalSplash_4x4_01.png` | 16 | toé thường (Laser Splashes) |
| `ToeNgangA` | `Flipbooks/Water/FX_TX_LateralSplash_2x5_03.png` | 10 | toé ngang có hướng (Laser Impact WaterDirectionalImpact) |
| `ToeNgangB` | `Flipbooks/Water/FX_TX_LateralSplash_2x5_04.png` | 10 | toé ngang có hướng 2 |
| `TruotDat` | `Flipbooks/Water/FX_TX_LateralWaterSlide_4x4_01.png` | 16 | vệt nước loang trượt trên đất (Laser LateralWater_Lingering) |
| `ChamDat` | `Flipbooks/Water/FX_TX_WaterDots_4x4_01.png` | 16 | vòng gợn chấm trên đất (GroundDots) |
| `MuaA` | `Flipbooks/Water/FX_TX_RainSplash_02.png` | 16 | toé hạt mưa trên đất (WaterGround_01) |
| `MuaB` | `Flipbooks/Water/FX_TX_RainSplash_03.png` | 9 | toé hạt mưa 2 (WaterGround_03) |
| `MuaC` | `Flipbooks/Water/FX_TX_RainSplash_01.png` | 12 | toé hạt mưa 3 (WaterGround_04) |
| `MuaD` | `Flipbooks/Water/FX_TX_RainSplash_04.png` | 12 | toé hạt mưa 4 (WaterGround_02) |
| `Giot` | `Shared/FX_TX_FlipbookDots_02.png` | 4 | giọt bắn kéo dài (Dots / DotsDirectional) |
| `BongNho` | `Shared/fx_tx_bubbles_2x2_01.png` | 4 | bong bóng trong lòng tia (DotsDirectionalInside) |
| `GaiTrung` | `Shared/FX_TX_ImpactShapes_Sharp_01.png` | 4 | gai sắc chỗ trúng (Impact LightImpact / ImpactSpikes) |
| `ChopHuong` | `Shared/FX_TX_DirectionalImpact_02.png` | 1 | chớp trúng có hướng (Impact Impact) |
| `ChopTron` | `Shared/FX_TX_Animeimpact_Circular_01.png` | 1 | chớp trúng tròn (Impact CenterImpact) |
| `ToeGiua` | `Flipbooks/Water/FX_TX_SimpleCenterSplash_4x4_01.png` | 16 | toé bung giữa (SimpleSplash) |
| `ToeDon` | `Flipbooks/Water/FX_TX_WaterSimpleSplash_4x4_01.png` | 16 | toé đơn (SimpleWaterImpact) |
| `ToeTrung` | `Flipbooks/Water/FX_TX_SimpleImpactWater_4x4_01.png` | 16 | toé trúng đạn (Water_Impact_01) |
| `ToeVa` | `Flipbooks/Water/FX_TX_ImpactSplash_4x4_01.png` | 16 | toé va (ImpactGround) |
| `CotDung` | `Flipbooks/Water/FX_TX_VerticalSplash_4x4_02.png` | 16 | cột nước dựng (mạch phun / ImpactGround) |
| `ToeDat` | `Flipbooks/Water/FX_TX_GroundWaterSplash_4x4_01.png` | 16 | toé trên đất (Water_ImpactGround) |
| `CauVong` | `Flipbooks/Water/FX_TX_WaterLoop_01.png` | 25 | khối nước cuộn vòng (Orb / StrongProjectile) |
| `BongVo` | `Flipbooks/Water/FX_TX_BubbleExplode_3x3_01.png` | 9 | bong bóng vỡ (Bubble) |
| `BongDon` | `Flipbooks/Water/FX_TX_SmpleBubble_4x4_01.png` | 16 | bong bóng đơn |
| `Chem` | `Flipbooks/Water/FX_TX_MainSlash_4x4_01.png` | 16 | lưỡi chém nước (WaveAttack / Slash) |
| `SongTruot` | `Flipbooks/Water/FX_TX_LateralSplashSlides_4x6_02.png` | 24 | sóng trượt ngang (WaveAttack Projectile) |
| `Roi` | `Flipbooks/Water/FX_TX_WaterWhip_4x4_02.png` | 16 | roi nước (Whip) |
| `GonMua` | `Flipbooks/Water/FX_TX_WaterRipples_4x3_01.png` | 12 | vòng gợn mưa (RainExample) |
| `XoayO` | `Flipbooks/Water/FX_TX_TwirlTiled_4x5_01.png` | 20 | lốc xoáy ô lặp (Buff / whirl) |
| `BotKhoi` | `Flipbooks/Water/FX_TX_FoamSmoke_4x4_01.png` | 16 | khói bọt (FoamImpact) |
| `ChemVong` | `Flipbooks/Water/FX_TX_CicularSlash_4x4_01.png` | 16 | chém vòng tròn (SlashBasic / whirl) |
| `ToeNgangC` | `Flipbooks/Water/FX_TX_WaterLateralImpact_4x3_01.png` | 12 | toé ngang 3 (StrongProjectile Impact) |
| `ToeNho` | `Flipbooks/Water/FX_TX_MiniSplash_2x6_01.png` | 12 | toé nhỏ |
| `ToeGiuaNho` | `Flipbooks/Water/FX_TX_SmallSplashCenter_01_6x8.png` | 41 | toé nhỏ bung giữa (Projectile) |
| `NuocRoi` | `Flipbooks/Water/FX_TX_FallingWater_4x3_01.png` | 12 | nước rơi (FallingWater) |
| `ToeDatLon` | `Flipbooks/Water/FX_TX_GroundSplash_5x5_01.png` | 25 | toé đất lớn (Grenade Explosion) |
| `BotRieng` | `Flipbooks/Water/FX_TX_FoamIndividual_4x4_01.png` | 16 | bọt rời (Waterfall foam) |
| `VetSang` | `Flipbooks/Water/FX_TX_HighlightSlash_2x5_01.png` | 10 | vệt sáng lưỡi chém (Slash highlight) |

Texture lặp `nuoc_vet.png`: R `Shared/FX_TX_WaterNoise_Sharp.png` (Rubfish), G kênh R của `Tex_Water_01.tga` (NamuFX), B `Shared/FX_TX_FlamesNoise_01.png` (Rubfish), A alpha của `Shared/FX_TX_WaterTrail_01.png` (Rubfish).
