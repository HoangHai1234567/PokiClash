# Mổ xẻ hai gói nước mẫu (2026-11-25)

Người dùng: "làm lại vfx nước của game theo asset này ... quét thật kĩ và lấy cái nào phù hợp, nó có gì mình cũng phải có như vậy";
"đặc biệt là tia nước ở water laser rất đẹp"; "xem rõ cấu trúc từng prefab nó có những gì, particle system thế nào, vẽ thế nào rồi làm".

- **SrRubfish "Water - Assets for VFX 02"** (`Assets/SrRubfish_VFX_02`): 37 prefab, 72 flipbook nước vẽ sẵn (cel anime, lam + trắng),
  12 shader graph URP Unlit, 4 FBX hình dạng (ống tia, xoắn, lưỡi chém, vòng). Không có script.
- **NamuFX "Stylized Water Effect Pack"** (`Assets/NamuFX`): 12 prefab, 1 atlas hạt 8x8 tách kênh (`Tex_Particles_01`), 3 texture mặt
  nước toon tách kênh (`Tex_Water_01..03`: lưới vân / bọt mép), 4 shader graph (hạt có nhiễu méo, mặt nước, Fresnel, vệt đuôi).

Ảnh động từng prefab (chụp trong Unity 24 khung/giây, góc ngang chúc 18°): `xem.html`; tờ 12 khung: `to/`; 4 scene demo của Rubfish:
`gif/demo_*.gif`. Công cụ: `Assets/01 Script/Editor/VfxPackShots.cs` (menu PokiClash/Thử/VFX gói nước: …), `ghep.py`.

## 1. Gói vẽ thế nào (shader)

| Shader (Rubfish) | Cách tô | Dùng cho |
|---|---|---|
| LerpTransparencies | lấy giá trị xám của texture (R) → `lerp(MainColor tối, HighColor sáng)`, alpha = texture × màu đỉnh của hạt × OpacitySaturation; mềm theo độ sâu cảnh | hầu hết flipbook toé, giọt |
| ComplexGradientTransparencies | như trên + **texture trôi theo thời gian** (Panning) + **tan bằng smoothstep** theo alpha hạt (hoặc Custom Data) + lấy alpha theo màu đỉnh | lớp nhiễu tia (LaserNoise), chớp trúng, gai sắc |
| StandardTransparencyShaderFresnel | flipbook × Fresnel (giữa sáng `FresnelHigh`, mép đậm `FresnelLow`) | lõi tia (LaserCore), vòng nước, lá nước trên mesh |
| StandardDissolve | tan theo texture nhiễu riêng (ngưỡng + bậc) | vệt, đuôi |
| Transparencies+Gradient+VertexOffset | tô theo texture gradient + đẩy đỉnh theo mặt nạ | sóng |
| WaterShader_Sphere | Lit, Fresnel nhiễu trôi + đẩy đỉnh + tan | cầu nước (Orb) |
| Water_AnimeCascade | 8 texture: nhiễu cắt trôi, bọt mép, méo sóng, màu đỉnh | thác nước |
| RefractionShader | khúc xạ màn hình (SceneColor) | sóng xung kích (game không dùng: uGUI không có SceneColor, luật không quầng) |

NamuFX: `SH_Particles` (atlas hạt tách kênh R/G/B = ba hình, méo bằng nhiễu `noise11`, tan theo Custom Data), `SH_Water_Base` (mặt nước
toon: lưới vân trôi + bọt mép, trên mesh tròn / ống), `SH_Advanced-Fresnel` (cầu nước), `SH_Trail` (vệt đuôi).

**Rút ra cho game:** toàn bộ màu của gói đến từ một giá trị xám tô qua 2 màu → thay bằng **dải cel 4 màu của game** (tối / lam sâu /
lam sáng / bọt trắng, ranh run nét tay) + **vân chì**; mép cắt sắc bằng ngưỡng alpha; "tan" của gói (smoothstep theo alpha hạt) = ngưỡng
mép dâng theo độ hiện. Đã làm ở `UIWaterFx` chế độ 6 (flipbook) và 7 (ống tia).

## 2. Cách gói ghép một hiệu ứng (particle system)

Mỗi hiệu ứng là một cây ParticleSystem, gốc thường là một hạt mesh / bộ phát rỗng; con là các lớp: **thân** (mesh hoặc flipbook lớn),
**chớp** (1 hạt, 0,1–0,2 s), **toé** (flipbook 4x4 phát 10–35 / s, cỡ 3–6, tốc 12–60), **giọt** (`FlipbookDots` 2x2 kéo dài theo vận tốc,
20–400 / s, đời 0,4–0,6, cỡ 0,15–0,4 → 0), **nền đất** (nhóm `GroundFX`: vệt trượt `LateralWaterSlide`, vòng chấm `WaterDots`, toé mưa
`RainSplash` 01–04, phát 6–23 / s, nằm ngang). Toé / giọt có Size over lifetime (0 → 1 cho toé, 1 → 0 cho giọt), Color over lifetime alpha
0 → 1 ở 0,2 → 0. Bộ phát con (Sub emitter) sinh vòng nước (WaterAOE front + back: hai nửa vòng trước / sau thân).

## 3. Water Laser (người dùng thích nhất)

| Prefab | Lớp chính | Nhịp |
|---|---|---|
| WaterLaser_Cast | LaserCore (mesh ống, 0,4 s), LaserNoise 01–03 (vân sắc trôi, xoắn TwirlingWater 2x8), Splashes, DotsDirectional, WaterAOE | tia MẢNH phóng tới + mũ lưỡi liềm, rồi tan thành bọt |
| WaterLaser_MainLaser | gốc mesh ống (Size curve thở 1 s), LaserCore 01/02, LaserNoise 01–04 (ComplexGradient, vân `WaterNoise_Sharp` trôi), Head: LaserNoise 05 (TwirlingWater trên khối xoắn, 6 / s), 06 (LateralWater 3x4 xoay ±2,15 rad/s, 3 / s), BackHead + WaterTiling 01/02 (sinh WaterAOE 2–4 / s); DotsDirectional + DotsDirectionalInside (bong bóng trôi trong lòng tia 23–40 / s); Dots (20–45 / s); Splashes (10 / s); GroundFX | giữ, bề dày theo đường cong 0,6 → 1 (0,11) → 0,85 → 0,91 → 0,76 → 0,90 → 0,79 → 0,6 mỗi giây |
| WaterLaser_Impact | chớp tròn Animeimpact (0,12–0,2 s, cỡ 6–9), chớp hướng DirectionalImpact (0,13–0,2, cỡ 12–14), LightImpact / DarkImpact / ImpactSpikes (ImpactShapes 2x2, kéo dài, tốc 20, 3–8 cái), WaterDirectionalImpact 1/2 (LateralSplash 2x5, tốc 35), Dots (15–20 + 20 / s), Glow (bỏ), ShockWave khúc xạ (bỏ), GroundFX | lặp mỗi 0,2 s |
| WaterLaser_Burst | như Impact + lớp toé lớn lúc mở | 0,2 s |
| WaterLaser_Dissolve | LaserCore/Noise ngắn (0,2 s), xoắn 0,6 s co 0,8 → 0,2, Splashes, ground đọng lại | tia mảnh lại, vỡ khúc, rơi |

Trong game (`HatNuocGoi.cs`, `NLaser`): ống 4 lớp (vỏ mỏng rách, vỏ ngoài, lõi sáng, vệt bọt trôi; vân sắc kéo dài theo thân trôi
1,3–2,9 / s), bề dày Cast mảnh 0,32 → phình vượt 1,18 trong 0,11 s → thở theo đúng đường cong của gói (kéo về 0,8–1); mũ lưỡi liềm lúc
phóng; đầu nòng: khối nước cuộn `WaterLoop` + lá nước xoay `LateralWater` + vòng nước `TiledWater` chạy ra; xoắn `TwirlingWater` chạy dọc
thân trước / sau (14 / s); bong bóng trong lòng (22 / s); giọt bắn khỏi thân (30 / s); nền đất dọc đường tia (vệt trượt 15 / s, vòng chấm
11 / s, toé mưa 9 / s); chỗ trúng lặp 0,2 s (chớp tròn + chớp hướng + 3–7 gai sắc + toé ngang + toé + giọt); tắt: đuôi chạy, ống vỡ theo
nhiễu, mảnh xoắn / toé rơi.

## 4. Bảng đối chiếu: gói có gì → game làm gì

| Gói | Hiệu ứng | Game (chiêu) |
|---|---|---|
| Rubfish WaterLaser_* | tia | `n_tia` mọi tướng tia (NTiaKhung → NLaser) |
| Rubfish WaterOrb_Charge / Loop / Dissolve, MagicWater_OrbLoop, NamuFX Water_Ball_Explosion | cầu nước tụ, cuộn, vỡ | `n_cau`, `n_ngoc` |
| Rubfish StrongProjectile_Cast / Traveling / Impact, SimpleProjectile_Traveling, Projectile_Cast, SimpleWaterImpact | đạn nước | `n_dan`, `n_thuong`, `n_bong` |
| Rubfish WaveAttack_Cast / Projectile / Burst / Impact | sóng | `n_song` |
| Rubfish RainExample + WaterGround_01, NamuFX ripples | mưa, gợn | `n_mua` |
| Rubfish WaterBuff_Loop | vòng xoáy quanh chân | `n_xoay`, buff / hồi |
| Rubfish Water_Grenade_Preexplosion / Explosion, NamuFX Water_Explosion, Bubble_Explosion | bom nước, bong bóng nổ | `n_bong` (nổ), chiêu cuối |
| Rubfish Water_SlashBasic / LineaSlash | chém nước | đòn thường có vuốt / càng |
| Rubfish Water_Impact_01, ImpactGround, FoamImpact, SimpleSplash; NamuFX Hit_01 / 02, Splash_A / B / Multiple, Water_Impact | trúng, toé | `n_va`, toé dùng chung (NSplash, NTrung, NToe) |
| Rubfish FallingWater, Waterfall_* | thác / cột nước rơi | `n_voi` (mạch phun), chiêu cuối giáng nước |
| NamuFX Bubbles_Burst / Vertical_Loop | bong bóng | idle Thủy, `n_bong` |
| NamuFX Water_Beam | tia nước toon (ống + vòng đất) | tham khảo vòng nước dưới chân tia |

## 5. Phụ lục: từng lớp của từng prefab (tự sinh từ YAML)

Cột: nhịp (`dur`, `delay`, `life`), cỡ (`size`), tốc (`spd`), phát (`rate`, `burst@giây x số`), tờ khung (`sheetCxR`), kiểu vẽ
(billboard / stretched / horizontal / mesh), shader (`S:`), texture (`T:`), module bật (`mods:`).

### FX_PF_FallingWater_01

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| FallingWater_02 | dur5 loop life0.6..1.2 size3..4 spd0 rate=1.5..2 sheet4x4 vertical S:Transparencies_Gradient_Noise_Add T:FX_TX_FallingWater_4x3_02.png mods: |
| GroundGroup/WaterGround_03 | dur100 loop life0.8..0.6 size0.5..1 spd0 rate=2..4 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| GroundGroup/WaterGround_04 | dur100 loop life0.8..0.6 size1..0.5 spd0 rate=2..4 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| GroundGroup/WaterGround_02 | dur100 loop life0.8..0.6 size0.3..0.5 spd0 rate=2..4 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| GroundGroup/Shadow | dur5 loop life2 size20 spd0 rate=1 burst@0x0 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| GroundDots | dur10 loop life0.3..1 size0.1..0.2 spd0..0 rate=12..20 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods: |
| GroundGroup/GroundDots | dur1 loop life0.6..0.8 size0.8..1.5 spd0 rate=5..6 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| FallingWater_01 | dur5 loop life0.6..0.5 size3 spd0 rate=2..3 sheet4x3 vertical S:Transparencies_Gradient_Noise_Add T:FX_TX_FallingWater_4x3_01.png mods: |
| FX_PF_FallingWater_01 | dur5 loop life5 size1 spd5 rate=10 billboard mods: |
| GroundGroup/DistortDots | dur100 loop life1..0.5 size0.5..1.2 spd0 rate=10 S:RefractionShader T:builtin mods:Size,Color,CustomData |
| GroundGroup | dur5 loop life5 size1 spd5 rate=10 billboard mods: |
| GroundGroup/WaterGround_01 | dur100 loop life0.8..0.6 size1..2 spd0 rate=2..4 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |

### FX_PF_Lava_SimpleSplash_01

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| WaterTiled2 | dur1 life0.39 size1..1 spd0 rate=0 burst@0x1 none mods:Color,Sub |
| Glow_Heart | dur1 life0.2 size9.85 spd0 rate=0 burst@0x1 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| WaterTiled2/WaterFront | dur1 life2 size0.6 spd0 rate=0 burst@0x1 sheet3x4 mesh mesh=FX_MS_ExamplesMeshes_01.fbx S:LerpTransparencies T:FX_TX_TiledWater_3x4_01_SoftRender.png mods:Size,Color,CustomData |
| WaterTiled2/WaterBack | dur1 life2 size0.6 spd0 rate=0 burst@0x1 sheet3x4 mesh mesh=FX_MS_ExamplesMeshes_01.fbx S:LerpTransparencies T:FX_TX_TiledWater_3x4_01_SoftRender.png mods:Size,Color,CustomData |
| WaterGround_01 | dur0.65 delay0.25 life0.8..0.6 size1.5 spd0 rate=3..5 sheet4x3 billboard S:LerpTransparencies T:FX_TX_RainSplash_04.png mods: |
| WaterGround_04 | dur0.65 delay0.25 life0.8..0.6 size1 spd0 rate=3..5 sheet4x3 billboard S:LerpTransparencies T:FX_TX_RainSplash_01_Grayscale.png mods: |
| WaterGround_03 | dur0.65 delay0.25 life0.8..0.6 size1 spd0 rate=3..5 sheet3x3 billboard S:LerpTransparencies T:FX_TX_RainSplash_03_Grayscale.png mods: |
| WaterGround_02 | dur0.65 delay0.25 life0.8..0.6 size1 spd0 rate=3..5 sheet4x4 billboard S:LerpTransparencies T:FX_TX_RainSplash_02_Grayscale.png mods: |
| FX_PF_Lava_SimpleSplash_01 | dur1 life5 size1 spd5 rate=10 none S:Transparencies_Gradient_Noise_Add T:FX_TX_SmallSplashCenter_01_6x8.png mods: |
| Dots | dur1 life0.3..1 size0.35..0.2 spd12..60 rate=0 burst@0.06x6..9 stretched(v0 l2) S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Size,InheritVelocity |
| WaterRipplesGround | dur500 life1 size5.33..16 spd0 rate=0 burst@0x1 burst@0.1x0..1 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| CenterSplash | dur0.5 delay0.12 life0.5..0.75 size3.5..5 spd0 rate=0 burst@0x1 sheet6x3 vertical S:LerpTransparencies T:FX_TX_SmallSplashCenter_01_6x8.png mods:Size,Color |
| Shadow | dur1 life0.74 size9.85 spd0 rate=0 burst@0x1 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |

### FX_PF_MagicWater_OrbLoop

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| SparksLoop | dur5000 loop delay0.8 life0.4..1.2 size0.03..0.08 spd3..2 rate=20..30 billboard S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Size,Noise |
| Cast | dur1.2 life0.9 size1.3 spd0 rate=0 burst@0x1 sheet4x6 mesh mesh=builtin S:StandardTransparencyShader T:FX_TX_WaterMask_4x5_SoftRender_Grayscale.png mods:Size,Color,Rotation |
| Cast/Heartlight_Burst | dur12 life1 size6.35 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size |
| Mask | dur5000 delay1 life5000 size6 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| LightSphere | dur5000 loop life1..2 size2..2.8 spd0..0 rate=1..2 sheet2x8 mesh mesh=builtin S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods:Rotation |
| DarkBack | dur5000 loop life1.2..1.5 size2.1 spd0..0 rate=0.8..1 sheet2x8 mesh mesh=builtin S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods: |
| Cast/Heartlight_Impact | dur12 delay0.8 life0.4 size2.34 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| Heartlight | dur5000 loop life1 size2.34 spd0 rate=1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Noise |
| Around | dur5000 loop delay0.2 life1.3..2 size0.8..2 spd0..0 rate=1..2 sheet2x8 mesh S:StandardTransparencyShader T:FX_TX_TwirlingWater_2x8_01.png mods: |
| FX_PF_MagicWater_OrbLoop | dur5000 loop life5 size1 spd5 rate=10 billboard mods: |
| AroundDark | dur5000 loop delay0.2 life1.3..2 size0.8..2 spd0..0 rate=1..2 sheet2x8 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods: |
| Cast/ShockWave | dur5 delay0.8 life0.4 size11.7 spd0 rate=0 burst@0x1 S:RefractionShader T:builtin mods:Size,Color,CustomData |
| HeartCircle | dur5000 loop life1 size1 spd0 rate=1 billboard S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Noise |
| ExtraDots | dur5000 loop life0.3..1 size0.1..0.12 spd1..3 rate=12 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,Color,Rotation,Velocity,Noise |
| DarkSphere | dur5000 loop life1.4..2 size2..2.8 spd0..0 rate=2..3 sheet2x8 mesh mesh=builtin S:StandardTransparencyShader T:FX_TX_TwirlingWater_2x8_01.png mods:Rotation |
| LastLightSphere | dur5000 loop life1.2..1.5 size2.1 spd0..0 rate=0.8..1 sheet2x8 mesh mesh=builtin S:StandardTransparencyShader T:FX_TX_TwirlingWater_2x8_01.png mods: |
| Cast/LightBurst | dur12 delay0.8 life0.4..1.2 size0.05..0.1 spd12..50 rate=0 burst@0x20 billboard S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Size,Noise |
| ShockWave | (1) dur500 delay0.8 life2 size9.69 spd0 rate=1 burst@0x0 S:RefractionShader T:builtin mods:Size,Color,CustomData |
| Cast/'Mask | ' dur5 life1 size6.94 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size |
| Cast/CircleBurst | dur1.2 life1..0.6 size2.1 spd0..0 rate=1 burst@0.4x0 burst@0x1 burst@0.2x1 sheet2x8 mesh mesh=builtin S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods: |
| Glow | dur5000 delay0.85 life5000 size9.3 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Noise |
| Cast/HeartCircle | dur12 loop life1 size1 spd0 rate=0 burst@0x1 billboard S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Size |
| Dots | dur5000 loop life0.5..1 size0.1..0.2 spd1..3 rate=12 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,Color,Rotation,Velocity,Noise |
| SphereNoise | dur5000 loop life1 size0.8 spd0 rate=1 mesh mesh=builtin S:ComplexGradientTransparencies T:FX_TX_FlamesNoise_04.png mods:Noise |
| Cast/CircleBurst | dur1.2 life1..0.6 size2.1 spd0..0 rate=0 burst@0.4x0 burst@0x1 burst@0.2x1 sheet2x8 mesh mesh=builtin S:StandardTransparencyShader T:FX_TX_TwirlingWater_2x8_01.png mods: |
| Cast/RadialImpact | dur12 delay0.8 life0.4 size4 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_RadialBurst_03.psd mods:Size,Color |

### FX_PF_Poison_SimpleSplash_01

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Shadow | dur1 life0.74 size9.85 spd0 rate=0 burst@0x1 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| FX_PF_Poison_SimpleSplash_01 | dur1 life5 size1 spd5 rate=10 none S:Transparencies_Gradient_Noise_Add T:FX_TX_SmallSplashCenter_01_6x8.png mods: |
| WaterTiled2/WaterFront | dur1 life1.5 size1 spd0 rate=0 burst@0x1 sheet3x4 mesh S:LerpTransparencies T:FX_TX_TiledWater_3x4_01_SoftRender.png mods:Size,Color,CustomData |
| Glow_Heart | dur1 life0.2 size9.85 spd0 rate=0 burst@0x1 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| WaterTiled2/WaterBack | dur1 life1.5 size1 spd0 rate=0 burst@0x1 sheet3x4 mesh S:LerpTransparencies T:FX_TX_TiledWater_3x4_01_SoftRender.png mods:Size,Color,CustomData |
| WaterGround_01 | dur0.65 delay0.32 life1..1.2 size1.5 spd0 rate=3..5 sheet4x4 billboard S:LerpTransparencies T:FX_TX_RainSplash_02.png mods: |
| WaterRipplesGround | dur500 life1 size5.33..16 spd0 rate=0 burst@0x1 burst@0.1x0..1 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| CenterSplash | dur0.5 life0.785..0.9 size5..5 spd0 rate=0 burst@0x1 sheet6x3 vertical S:LerpTransparencies T:FX_TX_SmallSplashCenter_01_6x8.png mods:Size,Color |
| WaterGround_03 | dur0.65 delay0.32 life1..1.2 size1 spd0 rate=3..5 sheet3x3 billboard S:LerpTransparencies T:FX_TX_RainSplash_03_Grayscale.png mods: |
| Dots | dur1 life0.3..1 size0.35..0.2 spd12..35 rate=0 burst@0.06x12..15 stretched(v0 l2) S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Size,InheritVelocity |
| WaterGround_02 | dur0.65 delay0.32 life1..1.2 size1 spd0 rate=3..5 sheet4x4 billboard S:LerpTransparencies T:FX_TX_RainSplash_02_Grayscale.png mods: |
| WaterTiled2 | dur1 life0.5 size1.2..1.2 spd0 rate=0 burst@0x1 none mods:Color,Sub |
| WaterGround_04 | dur0.65 delay0.32 life1..1.2 size1 spd0 rate=3..5 sheet4x3 billboard S:LerpTransparencies T:FX_TX_RainSplash_01_Grayscale.png mods: |

### FX_PF_RainExample

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| GroundsRadials | dur1 loop life0.5..1 size0.5..1 spd0 rate=123 sheet4x4 S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size |
| DistortRadialGround | dur500 loop life0.4..0.8 size1..2 spd0 rate=500 burst@0x1 S:RefractionShader T:builtin mods:Size,Color,CustomData |
| FX_PF_RainExample | dur123 loop life0.6..0.8 size0.3..1.2 spd0 rate=200 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| DebrisGround_01 | dur123 loop life0.6..0.8 size0.3..1.2 spd0 rate=20..50 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| RainDetail | dur1 loop life2..1 size0.12..0.2 spd12..10 rate=300 stretched(v0 l1) S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods:Size,Collision |
| DebrisGround_03 | dur123 loop life0.6..0.8 size0.45..0.8 spd0 rate=20..50 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_05.png mods: |
| DebrisGround_02 | dur123 loop life0.6..0.8 size0.3..1.2 spd0 rate=20..50 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| DebrisGround_04 | dur123 loop life0.6..0.8 size0.7..1.3 spd0 rate=20..50 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_05.png mods: |
| RainLong | dur1 loop life2..1 size0.03..0.012 spd12..10 rate=123 stretched(v0 l1) S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Size |

### FX_PF_SimpleWaterImpact_01

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| FX_PF_SimpleWaterImpact_01 | dur1 life5 size1 spd5 rate=10 none S:LerpTransparencies T:FX_TX_ImpactSplash_4x4_01.png mods: |
| WaterDirectionalImpact | dur1 life0.2 size1.75 spd35 rate=0 burst@0x1 sheet2x5 S:LerpTransparencies_WithNoise T:FX_TX_LateralSplash_2x5_05.png mods:Sub |
| Dots | dur1 delay0.03 life0.3..0.6 size0.2..0.4 spd12..50 rate=0 burst@0x8..12 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| Impact | dur1 delay0.05 life0.2 size8.19 spd0 rate=0 burst@0x1 billboard S:ComplexGradientTransparencies T:FX_TX_DirectionalImpact_02.png mods:Size,Color |
| WaterImpact | dur1 delay0.05 life0.3 size8 spd0 rate=0 burst@0x1 sheet4x4 billboard S:LerpTransparencies T:FX_TX_ImpactSplash_4x4_01.png mods:Sub |
| Glow | dur1 life0.1 size8.38 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| FoamImpact | (3) dur1 life0.12..0.5 size0.69..0.32 spd23..55.57 rate=0 burst@0x4 sheet2x2 stretched(v-0.03 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| FoamImpact | (2) dur0.3 delay0.03 life0.2 size2.85 spd20 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| Impact | (1) dur1 life0.2 size4.03 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_ImpactSimpleCurvy_01.png mods:Size,Color |
| GlowSecond | dur1 delay0.05 life0.2 size8.38 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| FoamImpact | (1) dur0.3 delay0.03 life0.2 size2.17 spd20 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |

### FX_PF_WaterBuff_Loop

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Cast/Glow | dur1 life0.6 size10 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| Cast/ImpactSpikes | dur0.3 delay0.2 life0.2..0.25 size0.56..2.28 spd1..22.18 rate=0 burst@0x4..7 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| Cast | dur5 loop life5 size1 spd5 rate=10 billboard mods: |
| Cast/GroundCast | dur5 life0.3 size1.84 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_DenseNoise_01.png mods:Size |
| Cast/Dots | dur0.2 delay0.3 life0.45..0.8 size0.45..0.19 spd35..80 rate=0 burst@0x20..30 sheet2x2 stretched(v0 l1) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size |
| Cast/Glow_Heart | dur1 delay0.2 life0.45 size18.24 spd0 rate=0 burst@0x1 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| GlowADD | dur5 delay0.4 life500 size24.1 spd0 rate=0 burst@0x1 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Rotation |
| Cast/Radial | dur1 life0.2 size12 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_RadialBurst_01.psd mods:Size,Color |
| Cast/Foam | dur1 delay0.2 life0.3 size6.14 spd0 rate=0 burst@0x1 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_SimpleCenterSplash_4x4_01.png mods:Size,Color,CustomData |
| Cast/DistortWave | dur5 life0.4 size12 spd0 rate=0 burst@0x1 horizontal S:RefractionShader T:builtin mods:Size,Color,CustomData |
| GroundDots | dur500 delay0.4 life0.3..0.6 size0.1..0.3 spd40..120 rate=40..60 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,Velocity,Noise |
| SecondaryWater_Cast | dur500 delay0.3 life0.3..0.4 size1.6..1.5 spd0..0 rate=0 burst@0x3 sheet2x5 mesh S:StandardTransparencyShader T:FX_TX_LateralSplash_2x5_05.png mods:Size |
| WaterRipplesGround | dur500 delay0.4 life1..1.65 size18..14 spd0 rate=2 burst@0x1 sheet4x3 horizontal S:StandardTransparencyShader T:FX_TX_WaterRipples_4x3_01.png mods:Size,Color |
| GlowMovement | dur5 delay0.4 life500 size1.84 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_DenseNoise_01.png mods: |
| GoingUp | dur500 delay0.3 life0.65..0.85 size2.2..2.5 spd0..0 rate=3 burst@0x1 sheet2x6 mesh S:StandardTransparencyShader T:FX_TX_LateralSplash_2x6_07.png mods:Color |
| Cast/GroundCaustics | dur5 delay0.2 life0.7 size1.6 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_CausticNoise_01_Aberration.psd mods:Size,Color |
| Cast/GlowCast | dur1 delay0.2 life0.2 size3 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_VerticalImpact_01.png mods:Size |
| LoopGroundSpiral | dur500 delay0.3 life0.4..0.65 size1.6..1.8 spd0..0 rate=0 burst@0x2 sheet4x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods:Size |
| GlowShadow | dur5 delay0.4 life500 size17.35 spd0 rate=0 burst@0x1 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| FX_PF_WaterBuff_Loop | dur100 loop delay0.36 life2 size2.2..2 spd0..0 rate=1 burst@0x1 sheet5x5 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_5x5_01.png mods: |
| GroundSpiral | dur500 delay0.5 life0.4..0.65 size2..1.5 spd0..0 rate=4..6 burst@0x1 sheet4x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods:Size |
| Cast/RadialAoE | dur1 delay0.3 life0.5 size18.33 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_RadialBurst_03.psd mods:Size,Color |
| GlowShadow | dur5 delay0.4 life500 size12.1 spd0 rate=0 burst@0x1 horizontal S:ComplexGradientTransparencies T:FX_TX_CircleGround_Buff_01.png mods:Rotation |
| SecondaryWater_Cast | dur500 delay0.3 life0.3..0.4 size1.6..1.5 spd0..0 rate=0 burst@0x3 sheet3x4 mesh S:StandardTransparencyShader T:FX_TX_LateralSplash_3x4_02.png mods:Size |

### FX_PF_WaterGround_01

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| WaterTiled2/WaterBack | dur1 life1 size0.5 spd0 rate=0 burst@0x1 sheet4x5 mesh mesh=FX_MS_ExamplesMeshes_01.fbx S:Transparencies+Gradient+VertexOffset T:FX_TX_TiledWater_4x5_02.png mods:Size,CustomData |
| GroundFoam/GroundRadial | dur0.3 life1.19..0.45 size9..12 spd0 rate=9 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| GroundFoam | dur0.3 life0.3..0.92 size8.14..12.43 spd0 rate=6 sheet4x3 horizontal S:StandardTransparencyShader T:FX_TX_WaterRipples_4x3_01.png mods:Size,Color |
| SparksGravity_Center | dur1 delay0.1 life1..0.5 size0.49..0.2 spd20..45 rate=0 burst@0x8..9 sheet2x2 stretched(v0 l1) S:LerpTransparencies T:FX_TX_FlipbookDots_01.png mods:Size |
| GroundSplash_04 | dur0.5 delay0.4 life0.8..0.6 size1 spd0 rate=10 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| FX_PF_WaterGround_01 | dur1 life5 size1 spd5 rate=10 billboard mods: |
| WaterTiled/WaterFront | dur1 life1 size0.5 spd0 rate=0 burst@0x1 sheet4x5 mesh mesh=FX_MS_ExamplesMeshes_01.fbx S:Transparencies+Gradient+VertexOffset T:FX_TX_TiledWater_4x5_02.png mods:Size,CustomData |
| GroundSplash_03 | dur0.65 delay0.4 life0.8..0.6 size2 spd0 rate=5 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| GroundSplash_02 | dur0.5 delay0.4 life0.8..0.6 size1 spd0 rate=10 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| SparksGravity | dur1 life1..0.5 size0.45..0.3 spd18..35 rate=0 burst@0x20..12 sheet2x2 stretched(v0 l1) S:LerpTransparencies T:FX_TX_FlipbookDots_01.png mods:Size |
| GroundSplash_01 | dur0.5 delay0.4 life0.8..0.6 size1 spd0 rate=10 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| WaterTiled/WaterBack | dur1 life1 size0.5 spd0 rate=0 burst@0x1 sheet4x5 mesh mesh=FX_MS_ExamplesMeshes_01.fbx S:Transparencies+Gradient+VertexOffset T:FX_TX_TiledWater_4x5_02.png mods:Size,CustomData |
| WaterTiled | dur1 delay0.05 life1 size1.2..0.8 spd0 rate=0 burst@0x1 none mods:Color,Sub |
| WaterTiled2/WaterFront | dur1 life1 size0.5 spd0 rate=0 burst@0x1 sheet4x5 mesh mesh=FX_MS_ExamplesMeshes_01.fbx S:Transparencies+Gradient+VertexOffset T:FX_TX_TiledWater_4x5_02.png mods:Size,CustomData |
| WaterTiled2 | dur1 life0.39 size0.6..0.8 spd0 rate=0 burst@0x1 none mods:Color,Sub |

### FX_PF_WaterLaser_Burst

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| DotsDirectional | dur0.2 life0.4..0.6 size0.4..0.2 spd10..35 rate=400..300 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,Color,Velocity |
| GroundFX | (1)/WaterGround_03 dur0.2 loop delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| GroundFX | (1)/LateralWater_Lingering_02 dur0.12 life0.45..0.58 size14.52..5 spd0 rate=30 burst@0x0 sheet4x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| GroundFX | (1)/WaterGround_02 dur0.2 loop delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| WaterTiling | (1) dur0.23 life0.6..0.8 size3 spd0 rate=0 burst@0x1 none mods:Sub |
| LaserNoise | (6) dur1 life0.45..0.52 size2 spd0 rate=0 burst@0x2 sheet3x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWater_01_3x4.png mods:Color,Rotation |
| LaserCore | dur1 life0.12 size1 spd0 rate=0 burst@0x1 mesh S:StandardTransparencyShaderFresnel mods:Size |
| WaterTiling | (1)/WaterAOE_Waterback dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| ShockWave_Radial  | dur0.2 life0.3 size20 spd0 rate=0 burst@0x1 S:RefractionShader T:builtin mods:Size,Color,CustomData |
| GroundFX | (1)/GroundDots dur0.2 loop delay0.2 life0.6..0.8 size1.3..2.5 spd0 rate=12..20 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| GroundFX | (1) dur0.2 life5 size1 spd5 rate=10 billboard mods: |
| LaserNoise02 | dur1 life0.12 size1.1 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_WaterNoise_Sharp.png mods:Size |
| GroundFX | (1)/WaterGround_01 dur0.2 loop delay0.2 life0.8..0.6 size2 spd0 rate=6..10 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| GroundFX | (1)/LateralWater_Lingering_01 dur0.12 life0.45..0.58 size14.52..5 spd0 rate=30 burst@0x0 sheet4x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| Splashes | dur0.2 life0.35..0.45 size6.32..3.66 spd12..60 rate=35 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_NormalSplash_4x4_01_Alpha.png mods:Size,Color |
| Dots | dur0.2 life0.4..0.6 size0.15..0.35 spd2..23 rate=60..100 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| FX_PF_WaterLaser_Burst | dur1 life1 size1 spd0 rate=0 burst@0x1 mesh S:StandardTransparencyShaderFresnel mods:Size |
| LaserNoise01 | dur1 life0.12 size1 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_WaterNoise_Sharp.png mods:Size |
| GroundFX | (1)/WaterGround_04 dur0.2 loop delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| WaterTiling | (1)/WaterAOE_Waterfront dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| LaserNoise03 | dur1 life0.2 size2 spd0 rate=0 burst@0x1 sheet2x8 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods:Size,Rotation |

### FX_PF_WaterLaser_Cast

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| LaserNoise | 01 dur1 life0.4 size1 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_WaterNoise_Sharp.png mods:Size |
| WaterTiling02/WaterAOE_Waterfront | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| Dots | dur0.2 life0.4..0.6 size0.15..0.35 spd2..23 rate=60..100 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| LaserNoise | 02 dur1 life0.4 size1.1 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_WaterNoise_Sharp.png mods:Size |
| LaserNoise | 03 dur1 life0.5 size0.8..0.6 spd0 rate=0 burst@0x2 sheet2x8 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods:Size,Rotation |
| LaserCore | dur1 life0.4 size1 spd0 rate=0 burst@0x1 mesh S:StandardTransparencyShaderFresnel mods:Size |
| WaterTiling02/WaterAOE_Waterback | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| WaterTiling02 | dur0.23 life0.6..0.8 size0.7..1 spd0 rate=6..12 none mods:Sub |
| Splashes | dur0.45 life0.6..0.8 size3..5 spd12..60 rate=10 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_NormalSplash_4x4_01_Alpha.png mods:Size |
| DotsDirectional | dur0.45 delay0.3 life0.4..0.6 size0.4..0.2 spd10..35 rate=23..40 sheet2x2 stretched(v0 l1) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,Color,Velocity |
| FX_PF_WaterLaser_Cast | dur1 loop life1 size1 spd0 rate=0 burst@0x1 mesh S:StandardTransparencyShaderFresnel mods:Size |

### FX_PF_WaterLaser_Dissolve

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| LaserNoise01 | dur1 life0.2 size1 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_WaterNoise_Sharp.png mods:Size |
| GroundFX | dur0.2 loop life5 size1 spd5 rate=10 billboard mods: |
| GroundFX/GroundDots | dur0.45 delay0.2 life0.6..0.8 size1.3..2.5 spd0 rate=12..20 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| DotsDirectional | dur0.3 delay0.12 life0.4..0.6 size0.4..0.2 spd10..35 rate=45..60 sheet2x2 stretched(v0 l1) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,Color,Velocity |
| LaserNoise03 | dur1 life0.6 size0.8..0.2 spd0 rate=0 burst@0x2 sheet2x8 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods:Size,Rotation |
| GroundFX/WaterGround_02 | dur0.45 delay0.45 life0.8..0.6 size1 spd0 rate=10..16 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| GroundFX/WaterGround_01 | dur0.45 delay0.45 life0.8..0.6 size2 spd0 rate=10..16 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| GroundFX/LateralWater_Lingering_01 | dur0.4 delay0.3 life0.4..0.6 size2.2..5 spd0 rate=13..20 burst@0x0 sheet4x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| WaterTiling02 | dur0.23 life1 size1.2 spd0 rate=6..12 none mods:Sub |
| LaserCore | dur1 life0.2 size1 spd0 rate=0 burst@0x1 mesh S:StandardTransparencyShaderFresnel mods:Size |
| Splashes | dur0.2 life0.6..0.8 size3..5 spd12..60 rate=20 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_NormalSplash_4x4_01_Alpha.png mods:Size,Velocity |
| WaterTiling02/WaterAOE_Waterback | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| FX_PF_WaterLaser_Dissolve | dur1 loop life1 size1 spd0 rate=0 burst@0x1 mesh S:StandardTransparencyShaderFresnel mods:Size |
| LaserNoise02 | dur1 life0.2 size1.1 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_WaterNoise_Sharp.png mods:Size |
| GroundFX/WaterGround_03 | dur0.45 delay0.45 life0.8..0.6 size1 spd0 rate=10..16 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| GroundFX/WaterGround_04 | dur0.45 delay0.45 life0.8..0.6 size1 spd0 rate=10..16 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| WaterTiling02/WaterAOE_Waterfront | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| GroundFX/LateralWater_Lingering_02 | dur0.4 delay0.3 life0.4..0.6 size2.2..5 spd0 rate=13..20 burst@0x0 sheet4x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |

### FX_PF_WaterLaser_Impact

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| OrientatedBaseDirection/Radial | dur0.2 loop life0.19 size7 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_RadialBurst_03.psd mods:Size,Color |
| OrientatedBaseDirection/Glow_Heart | dur0.2 loop life0.12 size10.4 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| OrientatedBaseDirection/GlowSecond | dur0.2 loop delay0.05 life0.2 size10.36 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| OrientatedBaseDirection/LightImpact | dur0.2 loop delay0.03 life0.2 size3.2..4.36 spd20 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| OrientatedBaseDirection/CenterImpact | dur0.2 loop life0.12..0.2 size6..9 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_Animeimpact_Circular_01.png mods:Size,Color |
| OrientatedBaseDirection/ShockWave_Radial | dur0.2 loop life0.3 size33.7 spd0 rate=0 burst@0x1 billboard S:RefractionShader T:builtin mods:Size,Color,CustomData |
| OrientatedBaseDirection/WaterDirectionalImpact | dur0.2 loop delay0.1 life0.2 size7.14 spd35 rate=0 burst@0x0..1 sheet2x5 S:LerpTransparencies T:FX_TX_LateralSplash_2x5_03.png mods:Sub |
| OrientatedBaseDirection | dur0.2 loop life5 size1 spd5 rate=10 billboard mods: |
| OrientatedBaseDirection/Dots | dur0.2 loop life0.4..0.6 size0.16..0.3 spd12..50 rate=20 burst@0x15..20 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| OrientatedBaseDirection/Glow | dur0.2 loop life0.4 size13.2 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| OrientatedBaseDirection/Impact | dur0.2 loop life0.2..0.13 size12..14.19 spd0 rate=0 burst@0x1 billboard S:ComplexGradientTransparencies T:FX_TX_DirectionalImpact_02.png mods:Size,Color |
| GroundFX/LateralWater_Lingering_02 | dur0.2 loop life0.4..0.6 size4.72..4.07 spd0 rate=0 burst@0x1 sheet4x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| OrientatedBaseDirection/WaterTiling/WaterAOE_Waterback | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| GroundFX/LateralWater_Lingering_01 | dur0.2 loop life0.4..0.6 size4.72..4.07 spd0 rate=0 burst@0x1 sheet4x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| GroundFX/WaterGround_03 | dur0.2 loop delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| OrientatedBaseDirection/WaterDirectionalImpact2 | dur0.2 loop delay0.1 life0.2 size7.14 spd35 rate=0 burst@0x0..1 sheet2x5 S:LerpTransparencies T:FX_TX_LateralSplash_2x5_04.png mods:Sub |
| GroundFX/WaterGround_04 | dur0.2 loop delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| OrientatedBaseDirection/DarkImpact | dur0.2 loop delay0.03 life0.2 size6 spd20 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| GroundFX/GroundDots | dur0.2 loop delay0.2 life0.6..0.8 size1.3..2.5 spd0 rate=12..20 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| GroundFX | dur0.2 loop life5 size1 spd5 rate=10 billboard mods: |
| OrientatedBaseDirection/WaterTiling/WaterAOE_Waterfront | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| GroundFX/WaterGround_02 | dur0.2 loop delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| OrientatedBaseDirection/WaterTiling | dur0.2 loop life0.7..1.2 size1.4..2 spd0 rate=2..3 none mods:Sub |
| GroundFX/WaterGround_01 | dur0.2 loop delay0.2 life0.8..0.6 size2 spd0 rate=6..10 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| OrientatedBaseDirection/GlowMask | dur0.2 loop life0.3 size14.93 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| FX_PF_WaterLaser_Impact | dur0.2 loop life5 size1 spd5 rate=10 billboard mods: |
| OrientatedBaseDirection/ImpactSpikes | dur0.2 loop life0.2..0.25 size1.5..2.5 spd1..22.18 rate=0 burst@0x3..8 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| ANIM/DIRECTOR | comp class 95 tren ? mods: |

### FX_PF_WaterLaser_MainLaser

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Splashes | dur5 loop life0.5..0.65 size3..5 spd12..60 rate=10 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_NormalSplash_4x4_01_Alpha.png mods:Size |
| Head/BackHead/WaterTiling02/WaterAOE_Waterback | dur1 life0.6 size1 spd0..0 rate=0..0 burst@0x1 sheet4x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_NormalSplash_4x4_01.png mods: |
| GroundFX/WaterGround_02 | dur0.2 loop delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| Head | dur5 life5 size1 spd5 rate=10 billboard mods: |
| Head/BackHead | dur5 loop life5 size1 spd5 rate=10 billboard mods: |
| WaterTiling | dur1 loop life1..1.2 size1.8..1.6 spd0 rate=4 none mods:Sub |
| Head/LaserNoise | 04 dur1 loop life1 size1.1 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_WaterNoise_Sharp.png mods:Size |
| DotsDirectional | dur1 loop life0.4..0.6 size0.4..0.2 spd10..35 rate=23..40 sheet2x2 stretched(v0 l1) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,Color,Velocity |
| WaterTiling/WaterAOE_Waterfront | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| GroundFX/WaterGround_01 | dur0.2 loop delay0.2 life0.8..0.6 size2 spd0 rate=6..10 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| Head/LaserNoise | 02 dur1 loop life1 size1.1 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_WaterNoise_Sharp.png mods:Size |
| WaterTiling/WaterAOE_Waterback | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| WaterTiling02 | dur1 loop life1..1.2 size1.4..1.2 spd0 rate=2..3 none mods:Sub |
| DotsDirectionalInside | dur1 loop life0.4..0.6 size0.76..0.4 spd10..35 rate=23..40 sheet2x2 stretched(v0 l1) S:LerpTransparencies T:fx_tx_bubbles_2x2_01.png mods:Size,Color |
| Head/BackHead/WaterTiling02/WaterAOE_Waterfront | dur1 life0.6 size1 spd0..0 rate=0..0 burst@0x1 sheet4x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_NormalSplash_4x4_01.png mods: |
| GroundFX/GroundDots | dur0.2 loop delay0.2 life0.6..0.8 size1.3..2.5 spd0 rate=12..20 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| GroundFX/LateralWater_Lingering_02 | dur1 loop life0.4..0.6 size2.2..5 spd0 rate=23 burst@0x0 sheet4x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| GroundFX | dur0.2 loop life5 size1 spd5 rate=10 billboard mods: |
| Head/LaserNoise | 03 dur1 loop life1 size1 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_WaterNoise_Sharp.png mods:Size |
| Head/LaserNoise | 06 dur1 loop life0.45..0.6 size1.4..1.1 spd0 rate=3 sheet3x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWater_01_3x4.png mods:Rotation |
| Head/BackHead/WaterTiling01/WaterAOE_Waterfront | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| Head/LaserNoise | 05 dur1 loop life0.6..1.2 size1.4..1.8 spd0 rate=6 sheet2x8 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods:Size,Rotation |
| Head/BackHead/WaterTiling02 | dur1 loop life0.9..1.2 size1.4..1.5 spd0 rate=2..3 none mods:Sub |
| GroundFX/LateralWater_Lingering_01 | dur1 loop life0.4..0.6 size2.2..5 spd0 rate=23 burst@0x0 sheet4x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| WaterTiling02/WaterAOE_Waterback | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| GroundFX/WaterGround_04 | dur0.2 loop delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| Head/BackHead/WaterTiling01/WaterAOE_Waterback | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| Head/BackHead/WaterTiling01 | dur1 loop life0.6..1.2 size1.4..2 spd0 rate=2..3 none mods:Sub |
| GroundFX/WaterGround_03 | dur0.2 loop delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| Head/LaserNoise | 01 dur1 loop life1 size1 spd0 rate=0 burst@0x1 mesh S:ComplexGradientTransparencies T:FX_TX_WaterNoise_Sharp.png mods:Size |
| FX_PF_WaterLaser_MainLaser | dur1 loop life1 size1 spd0 rate=0 burst@0x1 mesh S:StandardTransparencyShaderFresnel mods:Size |
| WaterTiling02/WaterAOE_Waterfront | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| Head/LaserCore | 02 dur1 loop life1 size1 spd0 rate=0 burst@0x1 mesh S:StandardTransparencyShaderFresnel mods:Size |
| Head/LaserCore | 01 dur1 loop life1 size1 spd0 rate=0 burst@0x1 mesh S:StandardTransparencyShaderFresnel mods:Size |
| Dots | dur1 loop life0.4..0.6 size0.15..0.35 spd15..35 rate=20..45 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| ANIM/DIRECTOR | comp class 95 tren ? mods: |

### FX_PF_WaterOrb_Charge

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| ImpactFlipbook | dur1 life0.13 size3.43 spd0 rate=0 burst@0x1 billboard S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Size,Color |
| Glow | dur1 life0.6 size10 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| FX_PF_WaterOrb_Charge | dur5 loop life5 size1 spd5 rate=10 billboard mods: |
| ImpactSpikes | dur0.3 life0.2..0.25 size0.56..2.28 spd1..22.18 rate=0 burst@0x4..7 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| Glow_Heart | dur1 life0.12 size6.87 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| Radial | dur1 life0.19 size7.43 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_RadialBurst_03.psd mods:Size,Color |
| Dots | dur0.2 life0.4..0.6 size0.16..0.3 spd3..22 rate=100 burst@0x15..20 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| DistortWave | dur5 life0.4 size12 spd0 rate=0 burst@0x1 billboard S:RefractionShader T:builtin mods:Size,Color,CustomData |
| Foam | dur1 life0.3 size5 spd0 rate=0 burst@0x1 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_SimpleCenterSplash_4x4_01.png mods:Size,Color,CustomData |

### FX_PF_WaterOrb_Dissolve

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| GroundGround/WaterGround_04 | dur0.4 delay0.45 life0.8..0.6 size1..0.5 spd0 rate=6..9 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| GroundGround/GroundDots | dur0.6 delay0.5 life0.6..0.8 size0.8..1.5 spd0 rate=20..30 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| GroundGround/WaterGround_02 | dur0.4 delay0.45 life0.8..0.6 size0.3..0.5 spd0 rate=6..9 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| Radial | dur1 life0.19 size5.57 spd0 rate=0 burst@0x1 billboard S:ComplexGradientTransparencies T:FX_TX_CircleImpact_01.png mods:Size,Color,Rotation |
| FallingWater | dur1 life0.3 size3.13 spd0 rate=0 burst@0x1 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_SimpleImpactWater_4x4_01.png mods:Size,Color,CustomData |
| Dots | dur0.2 life0.4..1 size0.16..0.3 spd3..12 rate=100 burst@0x15..12 sheet2x2 stretched(v0 l1) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,Velocity |
| Distort | dur5 life0.4 size12 spd0 rate=0 burst@0x1 billboard S:RefractionShader T:builtin mods:Size,Color,CustomData |
| Glow_Heart | dur1 life0.12 size6.87 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| GroundGround/Shadow | dur5 delay0.3 life0.5 size8 spd0 rate=0 burst@0x1 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| Glow | dur1 life0.6 size10 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| FX_PF_WaterOrb_Dissolve | dur5 loop life5 size1 spd5 rate=10 billboard mods: |
| Opaque | dur3 life0.7 size0.9 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:WaterShader_Sphere T:FX_TX_WaterNoise_Sharp.png mods:Size,Color |
| GroundGround/WaterGround_03 | dur0.4 delay0.45 life0.8..0.6 size0.5..1 spd0 rate=6..9 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| GroundGround/DistortDots | dur0.3 delay0.3 life0.5..0.7 size0.5..1.2 spd0 rate=20..30 S:RefractionShader T:builtin mods:Size,Color,CustomData |
| GroundGround/WaterGround_01 | dur0.4 delay0.45 life0.8..0.6 size1..2 spd0 rate=6..9 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| Water | dur1 life0.5 size5 spd0 rate=0 burst@0x1 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_SimpleCenterSplash_4x4_01.png mods:Size,Color,CustomData |
| GroundGround | dur5 life5 size1 spd5 rate=10 billboard mods: |
| ImpactSpikes | dur0.3 life0.2..0.25 size0.56..2.28 spd1..22.18 rate=0 burst@0x4..7 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |

### FX_PF_WaterOrb_Loop

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| AroundShapes_Waterup_00 | dur3 life0.6 size2 spd0..0 rate=0 burst@0x1 sheet2x8 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods: |
| FallingWater02 | dur100 delay0.5 life0.8..1 size0.7..0.8 spd0..0 rate=2..4 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods:Rotation |
| AroundShapes_Waterup_01 | dur3 delay0.1 life0.6 size2 spd0..0 rate=0 burst@0x1 sheet2x8 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods: |
| GroundGroup/GroundDots | dur0.1 life1.19..0.45 size9..12 spd0 rate=9 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| BaseHighlight | dur3 delay0.3 life0.65 size1.1 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_CausticNoise_01.psd mods:Size,Color |
| GroundGroup/GroundDots | dur0.3 delay0.2 life1 size0.1..0.2 spd5..12 rate=80..120 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Velocity |
| GroundGroup/Foam | dur0.3 life1..0.9 size2..3 spd8..12 rate=5 burst@0x12 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_FoamSmoke_4x4_01.png mods:Size,Color,Rotation,Velocity |
| FX_PF_WaterOrb_Loop | dur5 life5 size1 spd5 rate=10 billboard S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods: |
| GroundGroup/WaterGround_01 | dur100 delay0.2 life0.8..0.6 size1..2 spd0 rate=3..5 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| Glow_AB_Loop | dur1 delay0.9 life100 size6 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| GroundGroup/WaterRipplesGround | dur0.15 delay0.08 life0.3..0.92 size8.14..12.43 spd0 rate=6 burst@0x1 sheet4x3 horizontal S:StandardTransparencyShader T:FX_TX_WaterRipples_4x3_01.png mods:Size,Color |
| DarkGlow | dur5 delay0.5 life100 size6 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| AroundShapes_Waterup_06 | dur3 delay0.34 life0.65 size1.5 spd0..0 rate=0 burst@0x1 sheet2x8 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods: |
| GroundGroup | dur5 life5 size1 spd5 rate=10 billboard mods: |
| Glow_AB_Burst | dur1 delay0.1 life0.85 size6 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| BaseOpenWater | dur3 delay0.2 life0.6 size1 spd0 rate=0 burst@0x1 sheet4x6 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:Transparencies_Gradient_Noise_Add T:FX_TX_WaterMask_4x5_SoftRender_Grayscale.png mods:Size,Color |
| FallingWater | dur100 delay0.5 life0.6..0.3 size0.7..0.8 spd0..0 rate=2..4 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods:Rotation |
| AroundShapes | dur100 delay0.3 life1.2..1.6 size3..2.8 spd0..0 rate=1..2 sheet4x6 mesh mesh=builtin S:Transparencies_Gradient_Noise_Add T:FX_TX_TwirlTiled_4x5_01.png mods:Color,Rotation |
| GroundGroup/WaterGround_02 | dur100 delay0.2 life0.8..0.6 size0.3..0.5 spd0 rate=3..5 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| AroundShapes_Waterup_02 | dur3 delay0.2 life0.6 size2 spd0..0 rate=0 burst@0x1 sheet2x8 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods: |
| LoopSphere | dur3 delay1.1 life100 size0.95 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:WaterShader_Sphere T:FX_TX_WaterNoise_Sharp.png mods:Noise |
| GroundSpiral | dur0.2 delay0.12 life0.4..0.65 size2..1.5 spd0..0 rate=7 burst@0x1 sheet4x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| CastingWaterDots | dur1 delay0.2 life0.4..0.6 size0.1..0.2 spd3..8 rate=12 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| AroundShapes_Waterup_04 | dur3 delay0.2 life0.6 size1.5 spd0..0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardDissolve T:FX_TX_WaterTrail_02.png mods:Size,Color,Rotation |
| Glow_Add_Loop | dur1 delay0.9 life100 size5 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| GroundGroup/ShockWave_Radial | dur5 life0.7 size5.82 spd0 rate=0 burst@0x1 S:RefractionShader T:builtin mods:Size,Color,CustomData |
| GroundGroup/Shadow | dur5 delay0.3 life100 size8 spd0 rate=0 burst@0x1 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| GroundGroup/DistortDots | dur100 life0.5..0.7 size0.5..1.2 spd0 rate=12 S:RefractionShader T:builtin mods:Size,Color,CustomData |
| GroundGroup/WaterGround_03 | dur100 delay0.2 life0.8..0.6 size0.5..1 spd0 rate=3..5 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| GroundGroup/GroundDots | dur1 delay0.2 life0.6..0.8 size0.8..1.5 spd0 rate=20..30 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| AroundShapes_Waterup_05 | dur3 delay0.4 life0.8 size1.5 spd0..0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardDissolve T:FX_TX_WaterTrail_02.png mods:Size,Color,Rotation |
| GroundGroup/WaterGround_04 | dur100 delay0.2 life0.8..0.6 size1..0.5 spd0 rate=3..5 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| Glow_Add_Burst | dur1 delay0.1 life0.85 size5 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| DotsLoop | dur100 delay0.2 life0.6..0.8 size0.1..0.2 spd0 rate=20..35 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Velocity |
| AroundShapes_Waterup_03 | dur3 delay0.3 life0.6 size1.5 spd0..0 rate=0 burst@0x1 sheet2x8 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods: |
| BaseOpaque | dur3 delay0.4 life0.7 size0.9 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:WaterShader_Sphere T:FX_TX_WaterNoise_Sharp.png mods:Size,Color |

### FX_PF_WaterSimpleProjectile_Traveling

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Lingering | dur5 life5 size1 spd5 rate=10 billboard mods: |
| Lingering/Splashes | dur1 loop life0.4..0.5 size1.5..2 spd5..12 rate=12..80 burst@0x0 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_NormalSplash_4x4_01_Alpha.png mods:Size,Color |
| Main | dur5 life5 size1 spd5 rate=10 billboard mods: |
| Lingering/SparksGravity | dur1 loop life0.6..0.5 size0.3..0.69 spd20..50 rate=23..50 sheet2x2 stretched(v0 l1) S:LerpTransparencies T:fx_tx_bubbles_2x2_01.png mods:Size,Color,Noise |
| Main/Glow | dur1 loop life1 size4.9 spd0.003 rate=1 stretched(v0 l2) S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| Main/Head | dur1 loop life1 size2 spd0.003 rate=1 stretched(v0 l2) S:ComplexGradientTransparencies T:FX_TX_TrailHead.png mods: |
| FX_PF_WaterSimpleProjectile_Traveling | dur5 loop life1 size5.37 spd0.003 rate=1 stretched(v0 l2) S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| Lingering/WaterTrail | dur1 loop life0.6 size1 spd-16 rate=60 none S:StandardDissolve T:FX_TX_WaterTrail_01.png mods:Color,Trail |
| Main/HeadGlow | dur1 loop life1 size2.69 spd0.003 rate=1 stretched(v0 l2) S:StandardTransparencyShader T:FX_TX_TrailHead_Glow.png mods: |
| ANIM/DIRECTOR | comp class 95 tren ? mods: |

### FX_PF_Water_FoamImpact

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Foam | dur1 life0.3..0.3 size3.21..2.9 spd0.05 rate=0 burst@0x4 sheet6x4 stretched(v0 l-2) S:StandardTransparencyShader T:FX_TX_LateralImpactComposed_4x6_01.png mods:Size,Color,CustomData |
| Radial | dur1 life0.19 size7 spd0 rate=0 burst@0x1 billboard S:ComplexGradientTransparencies T:FX_TX_CircleImpact_01.png mods:Size,Color,Rotation |
| Glow_Heart | dur1 life0.12 size6.87 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| Dots | dur1 life0.4..0.6 size0.16..0.3 spd5..25 rate=0 burst@0x15..20 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| FX_PF_Water_FoamImpact | dur5 loop life5 size1 spd5 rate=10 billboard mods: |
| ImpactSpikes | dur0.3 life0.2..0.25 size0.56..2.28 spd1..22.18 rate=0 burst@0x4..7 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| ImpactFlipbook | dur1 life0.13 size3.43 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_Animeimpact_Circular_01.png mods:Size,Color |
| Glow | dur1 life0.6 size15 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |

### FX_PF_Water_Grenade_Explosion

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| GroundGroup/WaterGround_04 | dur0.6 delay0.2 life0.8..0.6 size1 spd0 rate=6 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| SmallSplashes | dur1 delay0.05 life0.4..0.5 size5.1..3 spd12..63.88 rate=0 burst@0x4 sheet4x4 billboard S:LerpTransparencies T:FX_TX_NormalSplash_4x4_01.png mods:Rotation,Velocity |
| MainGlow | dur1 life0.12 size31.52 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| GroundGroup/GroundRadial | dur0.1 life1.19..0.45 size9..12 spd0 rate=9 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| RadialSecond | dur1 delay0.08 life0.12 size51.56 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_RadialBurst_01.psd mods:Size,Color |
| GroundGroup/GroundFoam | dur0.15 delay0.08 life0.3..0.92 size8.14..12.43 spd0 rate=6 burst@0x1 sheet4x3 horizontal S:StandardTransparencyShader T:FX_TX_WaterRipples_4x3_01.png mods:Size,Color |
| AroundShape_First | dur1 life0.44 size6.22 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:WaterShader_Sphere T:FX_TX_WaterNoise_Sharp.png mods:Size,Color |
| GroundGroup | dur5 life5 size1 spd5 rate=10 billboard mods: |
| Radial | dur1 delay0.08 life0.12 size81.4 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_RadialBurst_03.psd mods:Size,Color |
| GroundGroup/WaterGround_01 | dur0.6 delay0.2 life0.8..0.6 size2 spd0 rate=6 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| Circle | dur1 life0.35 size4.34 spd0 rate=0 burst@0x1 billboard S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Size,Color |
| AroundShape | dur1 life0.4 size3.47 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:WaterShader_Sphere T:FX_TX_WaterNoise_Sharp.png mods:Size,Color |
| Impact | dur1 life0.2..0.2 size2..2.5 spd3..12 rate=0 burst@0x2 burst@0.12x0 burst@0.05x0 sheet2x5 S:StandardTransparencyShader T:FX_TX_LateralSplash_2x5_04.png mods:Sub |
| FX_PF_Water_Grenade_Explosion | dur5 loop life5 size1 spd5 rate=10 billboard mods: |
| CircleCenter | dur1 life0.4 size1 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel mods:Size,Color |
| ImpactAround | dur0.3 life0.25..0.2 size0.84..3.82 spd1..12 rate=0 burst@0x6 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| Around | dur1 life0.4..0.55 size3..3.2 spd0 rate=0 burst@0x2 sheet3x5 mesh mesh=?4b35ee S:StandardTransparencyShaderFresnel T:FX_TX_SlashNoisy_3x5_01.png mods:Size,Color,Rotation |
| GroundGroup/GroundRadialDots | dur1 delay0.2 life0.6..0.8 size0.8..1.5 spd0 rate=20..30 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| GroundGroup/WaterGround_03 | dur0.6 delay0.2 life0.8..0.6 size1 spd0 rate=6 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| GroundGroup/WaterGround_02 | dur0.6 delay0.2 life0.8..0.6 size1 spd0 rate=6 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| GroundGroup/ShockWave_Radial | dur5 life0.7 size14 spd0 rate=0 burst@0x1 S:RefractionShader T:builtin mods:Size,Color,CustomData |
| ShockWave | dur5 life0.4 size55.8 spd0 rate=0 burst@0x1 billboard S:RefractionShader T:builtin mods:Size,Color,CustomData |
| FoamShapes | dur0.3 life0.25..0.2 size0.84..3.82 spd1..22.18 rate=0 burst@0x12 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| ImpactGlow | dur1 life0.8 size13.71 spd0 rate=0 burst@0x2 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| GlowContrast | dur1 life0.3 size25.94 spd0 rate=0 burst@0x1 vertical S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| VerticalSplash | dur0.2 life0.4 size14.84..15.3 spd0 rate=0 burst@0x1 sheet4x4 vertical S:Transparencies_Gradient_Noise_Add T:FX_TX_SimpleImpactWater_4x4_01.png mods: |
| Dots | dur1 life0.8..1 size0.16..0.3 spd55..82.9 rate=0 burst@0x60 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |

### FX_PF_Water_Grenade_Preexplosion

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Dots | dur1 life0.3..0.5 size0.1..0.3 spd5..12 rate=0 burst@0x8 burst@0.2x12 burst@0.4x12 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| BaseOpaque | dur1 life0.65 size1 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel mods:Size |
| TiledAround | dur1 delay0.1 life0.6 size1.05 spd0 rate=0 burst@0x1 sheet2x8 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods: |
| FX_PF_Water_Grenade_Preexplosion | dur5 loop life5 size1 spd5 rate=10 billboard mods: |
| ExtraBeams | dur1 delay0.48 life0.15..0.1 size0.3..0.5 spd0 rate=0 burst@0x1 burst@0.05x1 burst@0.08x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel mods:Size,Noise |
| MaskGlow | dur1 life0.6 size8.34 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size |
| ADD | dur1 life0.6 size8.34 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size |
| Smalwhip | dur1 delay0.4 life0.2 size6 spd0 rate=0 burst@0x1 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_WaterWhip_4x4_02.png mods:Sub |
| BaseHighlight | dur1 life0.65 size1.1 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_CausticNoise_01.psd mods:Size,Color |
| BaseOverload | dur1 life0.65 size1 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_WaterNoise_02.png mods:Size |
| TiledAround2 | dur1 life0.45 size1.05 spd0 rate=0 burst@0x1 sheet2x8 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TwirlingWater_2x8_01.png mods: |

### FX_PF_Water_ImpactGround

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| WaterTiling | dur1 life1 size1 spd0 rate=0 burst@0x1 none mods:Sub |
| VerticalImpact | dur0.1 life0.2 size5.28 spd0 rate=0 burst@0x1 sheet3x3 vertical S:LerpTransparencies T:FX_TX_VerticalSplash_3x3_01.png mods: |
| FoamShapes | dur0.3 life0.25..0.2 size0.84..0.52 spd1..22.18 rate=0 burst@0x5 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Water_01.png mods:Size,Color |
| ShockWave | dur5 life0.4 size25 spd0 rate=0 burst@0x1 S:RefractionShader T:builtin mods:Size,Color,CustomData |
| WaterGround_01 | dur0.6 delay0.2 life0.8..0.6 size2 spd0 rate=6 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| ImpactGlow | dur1 life0.1 size24.82 spd0 rate=0 burst@0x2 vertical S:StandardTransparencyShader T:FX_TX_VerticalGlow_01.png mods:Size,Color |
| OpenWave | dur1 life0.5 size7.62 spd0 rate=0..0 burst@0x1 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_SmallWaterGroundSplash_01_4x4.png mods:Sub |
| Dots | dur1 life0.3..1 size0.16..0.51 spd5..100 rate=0 burst@0x23 burst@0.02x23 burst@0.06x3 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| VerticalSplash | dur0.2 life1..1 size14.84..15.3 spd0 rate=0 burst@0x1 sheet5x5 vertical S:Transparencies_Gradient_Noise_Add T:FX_TX_GroundSplash_5x5_01.png mods: |
| WaterGround_03 | dur0.6 delay0.2 life0.8..0.6 size1 spd0 rate=6 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| GlowContrast | dur1 life0.4 size42.3 spd0 rate=0 burst@0x1 vertical S:ComplexGradientTransparencies T:FX_TX_VerticalGlow_01.png mods:Size,Color |
| ShockWave_Radial | dur5 life0.4 size5.13 spd0 rate=0 burst@0x1 S:RefractionShader T:builtin mods:Size,Color,CustomData |
| FX_PF_Water_ImpactGround | dur5 life5 size1 spd5 rate=10 billboard S:Transparencies_Gradient_Noise_Add T:FX_TX_VerticalSplash_4x4_02_Grayscale.png mods: |
| WaterTiling/WaterAOE_Waterback | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh mesh=FX_MS_ExamplesMeshes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| GroundWave_02 | dur5 life0.66 size9.1 spd0 rate=0 burst@0x1 sheet4x4 S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color,CustomData |
| WaterGround_04 | dur0.6 delay0.2 life0.8..0.6 size1 spd0 rate=6 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| WaterTiling/WaterAOE_Waterfront | dur1 life0.35 size1 spd0..0 rate=0..0 burst@0x1 sheet3x4 mesh mesh=FX_MS_ExamplesMeshes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods: |
| FoamImpact | dur0.3 life0.12 size2.56 spd1..12 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Water_01.png mods:Size,Color |
| FoamContrast | dur0.3 life0.1 size3.81 spd1..12 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Water_01.png mods:Size,Color |
| WaterGround_02 | dur0.6 delay0.2 life0.8..0.6 size1 spd0 rate=6 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| GroundWave_01 | dur5 life1 size17.5 spd0 rate=0 burst@0x1 sheet4x4 S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color,CustomData |

### FX_PF_Water_Impact_01

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Glow | dur1 life0.12 size8 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| WaterImpact | dur1 life0.3 size5.63 spd0 rate=0 burst@0x1 sheet4x4 billboard S:LerpTransparencies T:FX_TX_ImpactSplash_4x4_01.png mods:Sub |
| WaterDirectionalImpact | dur1 life0.35..0.55 size2..2.5 spd3..12 rate=0 burst@0x2 burst@0.12x0 burst@0.05x0 sheet2x5 S:StandardTransparencyShader T:FX_TX_LateralSplash_2x5_04.png mods:Sub |
| Dots | dur1 life0.3..1 size0.1..0.3 spd5..35 rate=0 burst@0x8 burst@0.05x0 burst@0.12x6 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| FX_PF_Water_Impact_01 | dur1 life5 size1 spd5 rate=10 none S:LerpTransparencies T:FX_TX_ImpactSplash_4x4_01.png mods: |
| Impact | dur1 life0.12 size12.99 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_DirectionalImpact_01.png mods:Size,Color |

### FX_PF_Water_LineaSlash_01

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| LightSlash | dur0.63 life0.25 size1 spd0 rate=0..0 burst@0x1 sheet2x5 mesh S:LerpTransparencies T:FX_TX_HighlightSlash_2x5_01.png mods:Size,Color,Velocity |
| Glow | dur0.63 life0.8 size1 spd0 rate=0..0 burst@0x1 mesh S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color,Velocity |
| Dots_02 | dur0.12 delay0.1 life0.3..0.6 size0.4..0.8 spd0..2 rate=20..12 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,Velocity,Noise |
| Dots_01 | dur0.12 delay0.05 life0.3..1.2 size0.12..0.2 spd0..2 rate=35..50 burst@0x3..8 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,Velocity,Noise |
| FX_PF_Water_LineaSlash_01 | dur1 life5 size1 spd5 rate=10 billboard S:Transparencies_Gradient_Noise_Add T:FX_TX_MainSlash_4x4_01_Grayscale.psd mods: |
| SlashLinear | dur0.63 delay0.02 life0.6 size1 spd0 rate=0..0 burst@0x1 sheet4x4 mesh S:Transparencies_Gradient_Noise_Add T:FX_TX_MainSlash_4x4_01_Grayscale.psd mods:Color,Velocity |

### FX_PF_Water_Projectile_Cast

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Father3DShapes/WaterAOE_Waterback | dur1 life0.3 size1 spd0..0 rate=0..0 burst@0x1 sheet2x6 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_MiniSplash_2x6_01.png mods: |
| Father3DShapes/WaterAOE_Waterfront | dur1 life0.3 size1 spd0..0 rate=0..0 burst@0x1 sheet2x6 mesh S:StandardTransparencyShaderFresnel T:FX_TX_MiniSplash_2x6_01.png mods: |
| Dots | dur1 loop delay0.03 life0.2..0.4 size0.2..0.4 spd12..50 rate=0 burst@0x8..12 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| WaterDirectionalImpact | dur1 loop life0.2 size1.75 spd35 rate=0 burst@0x1 sheet3x3 S:LerpTransparencies T:FX_TX_VerticalSplash_3x3_01.png mods:Sub |
| FX_PF_Water_Projectile_Cast | dur1 life5 size1 spd5 rate=10 none S:LerpTransparencies T:FX_TX_ImpactSplash_4x4_01.png mods: |
| DirectionalFoam | dur0.3 delay0.03 life0.2 size2.17 spd20 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| GlowSecond | dur1 loop delay0.05 life0.32 size8.38 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| Impact | dur1 loop life0.2 size4.03 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_ImpactSimpleCurvy_01.png mods:Size,Color |
| DirectionalFoamDark | dur0.3 delay0.03 life0.2 size2.85 spd20 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| Glow | dur1 loop life0.35 size8.38 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| Father3DShapes | dur1 loop life0.2 size1.57 spd0 rate=0 burst@0x1 billboard mods:Sub |
| WaterImpact | dur1 loop delay0.05 life0.3 size8 spd0 rate=0 burst@0x1 sheet4x4 billboard S:LerpTransparencies T:FX_TX_ImpactSplash_4x4_01.png mods:Sub |

### FX_PF_Water_SimpleSplash_01

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| WaterTiled2/WaterBack | dur1 life2 size0.8 spd0 rate=0 burst@0x1 sheet4x5 mesh mesh=FX_MS_ExamplesMeshes_01.fbx S:Transparencies+Gradient+VertexOffset T:FX_TX_TiledWater_4x5_02.png mods:Size,Color,CustomData |
| WaterGround_04 | dur0.4 delay0.2 life0.8..0.6 size1 spd0 rate=3..5 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| FX_PF_Water_SimpleSplash_01 | dur1 life5 size1 spd5 rate=10 none S:Transparencies_Gradient_Noise_Add T:FX_TX_SmallSplashCenter_01_6x8.png mods: |
| WaterGround_02 | dur0.4 delay0.2 life0.8..0.6 size1 spd0 rate=3..5 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| WaterGround_03 | dur0.4 delay0.2 life0.8..0.6 size1 spd0 rate=3..5 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| Dots | dur1 life0.3..1 size0.35..0.5 spd12..60 rate=0 burst@0.06x6..9 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| WaterGround_01 | dur0.4 delay0.2 life0.8..0.6 size1.5 spd0 rate=3..5 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| WaterRipplesGround | dur500 life0.5..1 size5.33..16 spd0 rate=0 burst@0x1 burst@0.1x0..1 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| CenterSplash | dur0.5 delay0.12 life0.5..0.75 size3.5..5 spd0 rate=0 burst@0x1 sheet6x3 vertical S:Transparencies_Gradient_Noise_Add T:FX_TX_SmallSplashCenter_01_6x8.png mods:Size,Color |
| Shadow | dur1 life0.74 size9.85 spd0 rate=0 burst@0x1 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| WaterTiled2 | dur1 life0.39 size1..1 spd0 rate=0 burst@0x1 none mods:Color,Sub |
| Glow_Heart | dur1 life0.2 size9.85 spd0 rate=0 burst@0x1 horizontal S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Size,Color |
| WaterTiled2/WaterFront | dur1 life2 size0.8 spd0 rate=0 burst@0x1 sheet4x5 mesh mesh=FX_MS_ExamplesMeshes_01.fbx S:Transparencies+Gradient+VertexOffset T:FX_TX_TiledWater_4x5_02.png mods:Size,Color,CustomData |

### FX_PF_Water_SlashBasic_01

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Slash_Water_Secondary_01 | dur1 delay0.05 life0.25 size1.37 spd0 rate=0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShader T:FX_TX_LateralWater_01_3x4.png mods: |
| GlowMas | dur1 life0.5 size1.73 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_Slashes_01.fbx S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color,Rotation |
| SparksGravity | dur0.2 delay0.05 life0.3..1.2 size0.12..0.2 spd0..0 rate=35..50 burst@0x3..8 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_01.png mods:Size,Velocity,Noise |
| SparksGravity_02 | dur0.2 delay0.1 life0.3..0.6 size0.3..0.5 spd0..0 rate=20..12 sheet2x2 billboard S:LerpTransparencies T:FX_TX_FlipbookDots_01.png mods:Size,Velocity,Noise |
| FX_PF_Water_SlashBasic_01 | dur5 loop life5 size1 spd5 rate=10 billboard S:LerpTransparencies T:FX_TX_HighlightSlash_2x5_01.png mods: |
| Slash_Water_Main | dur1 delay0.05 life0.5 size1.5 spd0 rate=0 burst@0x1 sheet2x5 mesh mesh=FX_MS_Slashes_01.fbx S:StandardTransparencyShader T:FX_TX_LateralSplash_2x5_04.png mods:Color |
| Slash_Highlight | dur1 life0.3 size1.5 spd0 rate=0 burst@0x1 sheet2x5 mesh mesh=FX_MS_Slashes_01.fbx S:LerpTransparencies T:FX_TX_HighlightSlash_2x5_01.png mods:Color |

### FX_PF_Water_StrongProjectile_Cast

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Father3DShapes | dur1 delay0.1 life0.2 size3 spd0 rate=0 burst@0x1 billboard mods:Velocity,Sub |
| Father3DShapes/WaterAOE_Waterback | dur1 life0.3 size1 spd0 rate=0..0 burst@0x1 sheet2x6 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_MiniSplash_2x6_01.png mods:Velocity |
| DirectionalFoamDark | dur0.3 delay0.03 life0.2 size2.85 spd20 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| Glow | dur1 life0.35 size8.38 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| Father3DShapes/WaterAOE_Waterfront | dur1 life0.3 size1 spd0 rate=0..0 burst@0x1 sheet2x6 mesh S:StandardTransparencyShaderFresnel T:FX_TX_MiniSplash_2x6_01.png mods:Velocity |
| WaterDirectionalImpact | dur1 life0.2 size2.17 spd35 rate=0 burst@0x1 sheet3x3 S:LerpTransparencies T:FX_TX_VerticalSplash_3x3_01.png mods:Sub |
| Dots | dur1 delay0.03 life0.2..0.4 size0.2..0.4 spd12..120 rate=0 burst@0x8..12 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| GlowSecond | dur1 delay0.05 life0.32 size8.38 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| Father3DShapes2 | dur1 life0.2 size2 spd0 rate=0 burst@0x1 billboard mods:Velocity,Sub |
| Father3DShapes2/WaterAOE_Waterfront | dur1 life0.3 size1 spd0 rate=0..0 burst@0x1 sheet2x6 mesh S:StandardTransparencyShaderFresnel T:FX_TX_WaterWhip_2x6_01.png mods:Velocity |
| FX_PF_Water_StrongProjectile_Cast | dur1 life5 size1 spd5 rate=10 none S:LerpTransparencies T:FX_TX_ImpactSplash_4x4_01.png mods: |
| Father3DShapes2/WaterAOE_Waterback | dur1 life0.3 size1 spd0 rate=0..0 burst@0x1 sheet2x6 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_WaterWhip_2x6_01.png mods:Velocity |
| Impact | dur1 life0.2 size10.04 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_ImpactSimpleCurvy_01.png mods:Size,Color |
| DirectionalFoam | dur0.3 delay0.03 life0.2 size4.9 spd20 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |

### FX_PF_Water_StrongProjectile_Impact

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Aroundshape | dur1 delay0.05 life0.3 size4 spd0 rate=0 burst@0x1 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods:Rotation |
| WaterDirectionalImpact | dur1 delay0.1 life0.2 size1.95 spd35 rate=0 burst@0x1 sheet2x5 S:LerpTransparencies_WithNoise T:FX_TX_LateralSplash_2x5_05.png mods:Sub |
| Lightimapct | dur0.3 delay0.03 life0.2 size5.4 spd20 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| ShockWave_Radial | dur5 life0.27 size6.67 spd0 rate=0 burst@0x1 billboard S:RefractionShader T:builtin mods:Size,Color,CustomData |
| FX_PF_Water_StrongProjectile_Impact | dur1 life1 size1 spd5 rate=10 none S:LerpTransparencies T:FX_TX_ImpactSplash_4x4_01.png mods: |
| Glow | dur1 life0.1 size8.38 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| DarkImpact | dur0.3 delay0.03 life0.2 size7.45 spd20 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| GlowSecond | dur1 delay0.05 life0.2 size10.36 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| Impact | dur1 delay0.05 life0.2 size16 spd0 rate=0 burst@0x1 billboard S:ComplexGradientTransparencies T:FX_TX_DirectionalImpact_02.png mods:Size,Color |
| MainImpact | dur1 life0.2 size9 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_Animeimpact_Circular_01.png mods:Size,Color |
| SmallSparks | dur1 life0.12..0.5 size0.69..0.32 spd23..55.57 rate=0 burst@0x4 sheet2x2 stretched(v-0.03 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| Dots | dur1 delay0.05 life0.3..1 size0.12..0.4 spd0..120 rate=0 burst@0x12..20 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |

### FX_PF_Water_StrongProjectile_Traveling

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Lingering/AroundShape_Linger | dur1 loop life0.23..0.3 size2..2.3 spd0..0 rate=12..23 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods:Rotation |
| Lingering/WaterTrail | dur1 loop life0.8 size3.18 spd-16 rate=60 none S:StandardDissolve T:FX_TX_WaterTrail_01.png mods:Color,Trail |
| Lingering/Splashes | dur1 loop life0.4..0.5 size1.5..2 spd5..12 rate=12..80 burst@0x0 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_NormalSplash_4x4_01_Alpha.png mods:Size,Color |
| Main/Aroundshape | dur1 loop life0.35..0.5 size2..2.3 spd0..0 rate=2..5 sheet3x4 mesh S:StandardTransparencyShaderFresnel T:FX_TX_TiledWater_3x4_01_SoftRender.png mods:Rotation |
| Lingering/LinearSplash | 2 dur5 loop life0.3..0.4 size2..1 spd5..12 rate=5 sheet2x5 stretched(v0 l-2) S:LerpTransparencies T:FX_TX_LateralSplash_2x5_04.png mods: |
| Lingering/Bubble | dur1 loop life0.2..0.4 size0.2..0.35 spd5..12 rate=60 sheet2x2 billboard S:LerpTransparencies T:fx_tx_bubbles_2x2_01.png mods:Size,Rotation,Velocity,Noise,Sub |
| Lingering/LinearSplash | dur5 loop life0.3..0.4 size2..1 spd5..12 rate=5 sheet2x5 stretched(v0 l-2) S:LerpTransparencies T:FX_TX_LateralSplash_2x5_04.png mods: |
| Lingering/LinearSplash | 3 dur5 loop life0.3..0.4 size4..3 spd5..12 rate=3 sheet2x5 stretched(v0 l-2) S:LerpTransparencies T:FX_TX_LateralSplash_2x6_06.png mods:Size |
| Main/LoopFace | dur12 life12 size2.86 spd0.0005 rate=0 burst@0x1 sheet5x5 S:StandardTransparencyShader T:FX_TX_WaterLoop_01.png mods:Size,Noise |
| Lingering | dur5 life5 size23 spd5 rate=10 billboard mods: |
| Lingering/SparksGravity | dur1 loop life0.6..0.5 size1..1.91 spd20..50 rate=23..50 sheet2x2 stretched(v0 l1) S:LerpTransparencies T:fx_tx_bubbles_2x2_01.png mods:Size,Color,Noise |
| Main/WaterTrail | dur1 loop life0.8 size3.18 spd-16 rate=60 none S:StandardDissolve T:FX_TX_WaterTrail_01.png mods:Color,Trail |
| Main/GlowMask | dur1 loop life1 size12 spd0 rate=1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| Main/Glow | dur1 loop life1 size4.9 spd0.003 rate=1 stretched(v0 l2) S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| Lingering/Bubble/DestroyBubbles02 | dur1 life0.4..0.3 size1..1.4 spd0 rate=0 burst@0x1 sheet3x4 billboard S:LerpTransparencies T:FX_TX_WaterSmallSplash_3x4_01.png mods:Size |
| Main/HeadGlow | dur1 loop life1 size2.13 spd0.003 rate=1 stretched(v0 l2) S:StandardTransparencyShader T:FX_TX_TrailHead_Glow.png mods: |
| FX_PF_Water_StrongProjectile_Traveling | dur5 loop life5 size1 spd5 rate=10 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| Lingering/Bubble/DestroyBubbles | dur1 life0.4..0.3 size2 spd0 rate=0 burst@0x1 sheet3x3 billboard S:LerpTransparencies T:FX_TX_BubbleExplode_3x3_01.png mods:Size,Rotation |
| Main | dur5 life5 size1 spd5 rate=10 billboard mods: |
| ANIM/DIRECTOR | comp class 95 tren ? mods: |

### FX_PF_Waterfall_MainFoam

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| FoamSmoke | dur1 loop life0.8..2 size12..15 spd0..1 rate=3..3 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_FoamSmoke_4x4_01.png mods:Size,Color |
| FoamFill_01 | dur1 loop life1..0.5 size8..5 spd0 rate=0..2 sheet4x4 vertical S:StandardTransparencyShader T:FX_TX_FoamIndividual_4x4_02.png mods: |
| BackFoam | dur1 loop life2..1.5 size22.88..17.79 spd0 rate=1 sheet4x8 vertical S:StandardTransparencyShader T:FX_TX_FoamLoop_4x6_01.png mods: |
| FX_PF_Waterfall_MainFoam | dur5 loop life5 size1 spd5 rate=10 none S:StandardTransparencyShader T:FX_TX_FoamLoop_4x6_01.png mods: |
| FoamFill_02 | dur1 loop life1..0.5 size7..4 spd0 rate=1..2 sheet4x4 vertical S:StandardTransparencyShader T:FX_TX_FoamIndividual_4x4_01.png mods: |
| GroundWater | dur1 loop life1..0.3 size2..0.5 spd0 rate=12 sheet4x3 vertical S:StandardTransparencyShader T:FX_TX_RainSplash_05.png mods: |
| Dots | dur5 loop life1..0.6 size0.1..0.3 spd12..20 rate=50 billboard S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Size |
| MainFoam | dur1 loop life2..1.5 size6..4 spd0 rate=1 sheet4x8 mesh S:StandardTransparency_OffsetGrad T:FX_TX_FoamLoop_4x6_01.png mods: |

### FX_PF_Waterfall_SingleFoam_01

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| MainFoamLoop | dur1 loop life2..1.5 size5.43..5.01 spd0 rate=1 sheet4x8 vertical S:StandardTransparencyShader T:FX_TX_FoamLoop_4x6_01.png mods: |
| Dots | dur5 loop life1..0.6 size0.1..0.3 spd8..20 rate=23 billboard S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Size |
| FoamFill_01 | dur1 loop life1..0.5 size6.5..4 spd0 rate=0..2 sheet4x4 vertical S:StandardTransparencyShader T:FX_TX_FoamIndividual_4x4_02.png mods: |
| FX_PF_Waterfall_SingleFoam_01 | dur5 loop life5 size1 spd5 rate=10 none S:StandardTransparencyShader T:FX_TX_FoamLoop_4x6_01.png mods: |

### FX_PF_Waterfall_SingleFoam_02

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| MainFoamLoop | dur1 loop life2..1.5 size5.43..5.01 spd0 rate=1 sheet4x8 vertical S:StandardTransparencyShader T:FX_TX_FoamLoop_4x6_01.png mods: |
| FoamFill_01 | dur1 loop life1..0.5 size6.5..4 spd0 rate=0..2 sheet4x4 vertical S:StandardTransparencyShader T:FX_TX_FoamIndividual_4x4_02.png mods: |
| FX_PF_Waterfall_SingleFoam_02 | dur5 loop life5 size1 spd5 rate=10 none S:StandardTransparencyShader T:FX_TX_FoamLoop_4x6_01.png mods: |
| Dots | dur5 loop life1..0.6 size0.1..0.3 spd8..20 rate=23 billboard S:ComplexGradientTransparencies T:FX_TX_Circle_01_Dissolve.png mods:Size |
| FoamFill_02 | dur1 loop life1..0.8 size5..3 spd0 rate=0..1 sheet4x4 vertical S:StandardTransparencyShader T:FX_TX_FoamIndividual_4x4_01.png mods: |

### FX_PF_Waterfall_UnderwaterFoam

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| FX_PF_Waterfall_UnderwaterFoam | dur5 loop life5 size1 spd5 rate=10 none S:StandardTransparencyShader T:FX_TX_FoamLoop_4x6_01.png mods: |
| GroundFoam | dur1 loop life1 size13.95 spd0 rate=1 sheet4x8 S:StandardTransparencyShader T:FX_TX_GroundFoam_4x8_01.png mods: |
| GroundFoamDark | dur1 loop life1 size15.47 spd0 rate=1 sheet4x8 S:StandardTransparencyShader T:FX_TX_GroundFoam_4x8_01.png mods: |

### FX_PF_WaveAttack_Burst

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Dots | dur1 life0.4..0.6 size0.15..0.35 spd15..35 rate=0 burst@0x15..20 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| HeadGlow | dur5 life0.3 size4.24 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel mods:Size,Color |
| BurstFlipbook | dur5 life0.3 size5.04 spd0 rate=0 burst@0x1 sheet2x5 mesh S:LerpTransparencies T:FX_TX_LateralSplash_2x5_03.png mods:Size |
| BurstWaves | dur5 life0.3 size5.82 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_FlamesNoise_01.png mods:Size,Color |
| Head_Burst | dur5 life0.3 size4.8 spd0 rate=0 burst@0x1 sheet2x5 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:LerpTransparencies T:FX_TX_LateralSplash_2x5_04.png mods: |
| FX_PF_WaveAttack_Burst | dur5 life5 size1 spd5 rate=10 billboard S:LerpTransparencies T:FX_TX_LateralSplash_2x5_03.png mods: |

### FX_PF_WaveAttack_Cast

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| LateralWater_Lingering_01 | dur1 life0.5..0.6 size4.72..4.07 spd0 rate=0 burst@0x1 sheet4x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| Dots | dur1 life0.4..0.6 size0.15..0.35 spd15..35 rate=0 burst@0x22..30 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| Head_Core_Burst | dur5 life0.3 size4.24 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel mods:Size,Color |
| FoamSmoke | dur1 life0.8..1.5 size4..6 spd0..0.5 rate=0 burst@0x5..8 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_FoamSmoke_4x4_01.png mods:Size,Color |
| FX_PF_WaveAttack_Cast | dur5 life5 size1 spd5 rate=10 billboard S:LerpTransparencies T:FX_TX_LateralSplash_2x5_03.png mods: |
| Head_Front_Burst | dur5 life0.3 size5.82 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_FlamesNoise_01.png mods:Size,Color |
| LateralWater_Lingering_02 | dur1 life0.5..0.6 size4.72..4.07 spd0 rate=0 burst@0x1 sheet4x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| Head_Front_ExtraBurst | dur5 life0.3 size4.8 spd0 rate=0 burst@0x1 sheet2x5 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:LerpTransparencies T:FX_TX_LateralSplash_2x5_04.png mods: |

### FX_PF_WaveAttack_Impact

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| OrientatedBaseDirection/Impact | dur1 life0.13 size14.19 spd0 rate=0 burst@0x1 billboard S:ComplexGradientTransparencies T:FX_TX_DirectionalImpact_02.png mods:Size,Color |
| OrientatedBaseDirection/Glow | dur1 life0.4 size13.2 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| OrientatedBaseDirection/ImpactSpikes | dur0.3 life0.2..0.25 size2.62..2.28 spd1..22.18 rate=0 burst@0x4..7 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| FX_PF_WaveAttack_Impact | dur5 loop life5 size1 spd5 rate=10 billboard mods: |
| GroundFX/LateralWater_Lingering_01 | dur1 life0.4..0.6 size4.72..4.07 spd0 rate=0 burst@0x1 sheet4x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| OrientatedBaseDirection/ShockWave_Radial | dur5 life0.3 size33.7 spd0 rate=0 burst@0x1 billboard S:RefractionShader T:builtin mods:Size,Color,CustomData |
| GroundFX/LateralWater_Lingering_02 | dur1 life0.4..0.6 size4.72..4.07 spd0 rate=0 burst@0x1 sheet4x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| OrientatedBaseDirection/CenterImpact | dur1 life0.12 size1.71 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_Animeimpact_Circular_01.png mods:Size |
| OrientatedBaseDirection | dur5 life5 size1 spd5 rate=10 billboard mods: |
| GroundFX/WaterGround_01 | dur0.4 delay0.2 life0.8..0.6 size2 spd0 rate=6..10 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| GroundFX | dur5 life5 size1 spd5 rate=10 billboard mods: |
| OrientatedBaseDirection/WaterDirectionalImpact | dur1 delay0.1 life0.2 size7.14 spd35 rate=0 burst@0x1 sheet2x5 S:LerpTransparencies T:FX_TX_LateralSplash_2x5_03.png mods:Sub |
| GroundFX/WaterGround_02 | dur0.4 delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| OrientatedBaseDirection/GlowSecond | dur1 delay0.05 life0.2 size10.36 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| GroundFX/WaterGround_03 | dur0.4 delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| GroundFX/GroundDots | dur0.6 delay0.2 life0.6..0.8 size1.3..2.5 spd0 rate=12..20 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| GroundFX/FrontImpact | dur5 life0.3 size4.53 spd0 rate=0 burst@0x1 sheet3x4 mesh S:LerpTransparencies T:FX_TX_LateralWater_01_3x4.png mods:Size |
| OrientatedBaseDirection/LightImpact | dur0.3 delay0.03 life0.2 size4.36 spd20 rate=0 burst@0x1 sheet2x2 stretched(v0 l-2) S:ComplexGradientTransparencies T:FX_TX_ImpactShapes_Sharp_01.png mods:Size,Color |
| GroundFX/WaterGround_04 | dur0.4 delay0.2 life0.8..0.6 size1 spd0 rate=6..10 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| OrientatedBaseDirection/Dots | dur1 life0.4..0.6 size0.16..0.3 spd5..27.89 rate=0 burst@0x15..20 sheet2x2 stretched(v0 l2) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| OrientatedBaseDirection/Radial | dur1 life0.19 size7 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_TX_RadialBurst_03.psd mods:Size,Color |
| OrientatedBaseDirection/Glow_Heart | dur1 life0.12 size6.87 spd0 rate=0 burst@0x1 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |

### FX_PF_WaveAttack_Projectile

| Lớp | Nhịp / cỡ / phát / dạng vẽ / shader / texture |
|---|---|
| Head/GroundFront | dur1 life50 size5.23 spd0 rate=0 burst@0x1 S:LerpTransparencies_WithNoise T:FX_TX_FrontWave_01.png mods: |
| LingeringGround/WaterGround_04 | dur50 life0.8..0.6 size1 spd0 rate=12 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_01.png mods: |
| Head | dur1 life5 size1 spd5 rate=10 billboard mods: |
| Head/Head_Foam | dur5 life30 size5.76 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_DenseNoise_01.png mods: |
| Head/LateralWaves_02 | dur50 loop life1..1.5 size2..4.8 spd0 rate=0.8..1.5 sheet5x5 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_5x5_01.png mods: |
| Head/GlowGround | dur1 life50 size12.94 spd0 rate=10 S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| LingeringGround | dur5 life5 size1 spd5 rate=10 billboard mods: |
| Lingering | dur5 life5 size1 spd5 rate=10 billboard mods: |
| Head/AddGlow | dur1 life50 size22.03 spd0 rate=10 billboard S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods: |
| LingeringGround/WaterGround_02 | dur50 life0.8..0.6 size1 spd0 rate=12 sheet4x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_04.png mods: |
| Lingering/GlowLingering | dur50 life0.8..1.1 size8..6 spd0 rate=15..25 S:StandardTransparencyShader T:FX_MT_GlowAlpha_01.png mods:Color |
| Lingering/FoamSmoke | dur1 loop life0.8..1.5 size4..6 spd0..0.5 rate=12..20 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_FoamSmoke_4x4_01.png mods:Size,Color |
| Head/Head_SharpNoise | dur5 life30 size5 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_WaterNoise_Sharp.png mods: |
| Head/Head_Caustic | dur5 life30 size5.5 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_CausticNoise_01_Aberration.psd mods: |
| Head/Head_Waves | dur5 life30 size7.27 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_FlamesNoise_01.png mods: |
| Head/Dots | dur50 life0.4..0.6 size0.15..0.35 spd15..35 rate=50 sheet2x2 stretched(v0 l1) S:LerpTransparencies T:FX_TX_FlipbookDots_02.png mods:Size,InheritVelocity |
| Head/Head_FrontLight | dur5 life30 size10.58 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_WaterNoise_02.png mods: |
| Head/LateralWaves_Front_02 | dur50 loop life0.5..0.6 size3..5 spd0 rate=3..4 sheet4x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| FX_PF_WaveAttack_Projectile | dur5 loop life20 size4.8 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_FlamesNoise_01.png mods: |
| Head/LateralWaves_01 | dur50 loop life1..1.5 size2..4.8 spd0 rate=0.8..1.5 sheet5x5 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_5x5_01.png mods: |
| LingeringGround/Main | dur50 life0.6..1 size2..3 spd0 rate=8..12 sheet2x5 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:LerpTransparencies T:FX_TX_LateralSplash_2x5_04.png mods:Size,Color |
| LingeringGround/WaterGround_03 | dur50 life0.8..0.6 size1 spd0 rate=12 sheet3x3 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_03.png mods: |
| Head/Head_Front | dur5 life30 size5.82 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:ComplexGradientTransparencies T:FX_TX_CausticNoise_01_Aberration.psd mods: |
| LingeringGround/WaterGround_01 | dur50 life0.8..0.6 size2 spd0 rate=12 sheet4x4 billboard S:StandardTransparencyShader T:FX_TX_RainSplash_02.png mods: |
| Lingering/LateralWater_Lingering_01 | dur50 loop life0.5..0.6 size2..2.58 spd0 rate=10..17 sheet4x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| Head/GroundFoamDark | dur1 life1 size5.68 spd0 rate=0 burst@0x1 sheet4x8 S:Transparencies_Gradient_Noise_Add T:FX_TX_GroundFoam_4x8_01.png mods: |
| Lingering/LateralWater_Lingering_02 | dur50 loop life0.5..0.6 size2..2.58 spd0 rate=10..17 sheet4x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| LingeringGround/GroundDots | dur12 life0.6..0.8 size1.3..2.5 spd0 rate=12..20 sheet4x4 horizontal S:StandardTransparencyShader T:FX_TX_WaterDots_4x4_01.png mods:Size,Color |
| Lingering/WaterLingering | dur5 loop life0.3..0.5 size2..4 spd15..35 rate=25..35 sheet4x4 billboard S:LerpTransparencies T:FX_TX_NormalSplash_4x4_01.png mods:Size |
| Head/Head_Core | dur5 life30 size4.24 spd0 rate=0 burst@0x1 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel mods: |
| Head/LateralWaves_Front_01 | dur50 loop life0.5..0.6 size3..5 spd0 rate=3..4 sheet4x4 mesh mesh=FX_MS_WaterGeneralShapes_01.fbx S:StandardTransparencyShaderFresnel T:FX_TX_LateralWaterSlide_4x4_01.png mods: |
| ANIM/DIRECTOR | comp class 95 tren ? mods: |

## 6. Phụ lục: đường cong theo tuổi hạt (Size / Color / UV / Sub …)

### Ground


### FX_PF_FallingWater_01

- FallingWater_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- Shadow · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.50:1.00 1.00:0.00
- GroundDots · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- GroundDots · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- FallingWater_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x3 anim0 cyc1
- DistortDots · Size: curve=[0.00:0.00 0.30:0.80 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1

### FX_PF_Lava_SimpleSplash_01

- WaterTiled2 · Color: mau 0.00#FFFFFF 0.99#C23F3F | alpha 0.41:1.00 1.00:0.84 · Sub: 2 sub 0 0
- Glow_Heart · Size: curve=[0.00:0.48 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.26:0.31 1.00:0.00
- WaterFront · Size: curve=[0.00:0.65 1.00:1.00] · UV: frameOverTime=[0.00:0.00 0.40:0.45 1.00:1.00] tiles3x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.15:1.00 1.00:0.79 · CustomData: mode0=1 
- WaterBack · Size: curve=[0.00:0.65 1.00:1.00] · UV: frameOverTime=[0.00:0.00 0.40:0.45 1.00:1.00] tiles3x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.15:1.00 1.00:0.79 · CustomData: mode0=1 
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · InheritVelocity: 
- WaterRipplesGround · Size: curve=[0.00:0.41 0.36:0.88 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.36:1.00
- CenterSplash · Size: curve=[0.00:0.75 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles6x3 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.22
- Shadow · Size: curve=[0.00:0.48 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.59:0.42 1.00:0.00

### FX_PF_MagicWater_OrbLoop

- SparksLoop · Size: curve=[0.00:0.00 0.30:1.00 1.00:0.00] · Noise: strength=[2.2]
- Cast · Size: curve=[0.01:1.00 0.26:1.00 0.70:0.89 1.00:0.39] · Rotation: curve=[0.20944] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x6 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.71:1.00 1.00:0.00
- Heartlight_Burst · Size: curve=[0.00:0.58 1.00:0.20]
- LightSphere · Rotation:  · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- DarkBack · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- Heartlight_Impact · Size: curve=[0.00:0.58 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.25:0.31 1.00:0.00
- Heartlight · Noise: strength=[2.2]
- Around · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- AroundDark · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- ShockWave · Size: curve=[0.00:0.40 0.21:0.93 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.26:0.21 1.00:0.00 · CustomData: mode0=1 
- HeartCircle · Noise: strength=[2.2]
- ExtraDots · Size: curve=[0.72:1.00 1.00:0.00] · Rotation: curve=[rand 0.00:2.09 1.00:2.09] · Velocity:  · Noise:  · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- DarkSphere · Rotation:  · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- LastLightSphere · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- LightBurst · Size: curve=[0.00:3.00 0.11:3.00 0.28:1.02 1.00:0.00] · Noise: strength=[2.2]
- ShockWave (1) · Size: curve=[0.00:0.40 0.21:0.93 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.51:1.00 1.00:0.00 · CustomData: mode0=1 
- 'Mask ' · Size: curve=[0.00:0.00 1.00:1.00]
- CircleBurst · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- Glow · Noise: strength=[2.2]
- HeartCircle · Size: curve=[0.00:0.58 1.00:1.00]
- Dots · Size: curve=[0.72:1.00 1.00:0.00] · Rotation: curve=[rand 0.00:2.09 1.00:2.09] · Velocity:  · Noise:  · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- SphereNoise · Noise: strength=[2.2]
- CircleBurst · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- RadialImpact · Size: curve=[0.00:0.58 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.25:0.31 1.00:0.00

### FX_PF_Poison_SimpleSplash_01

- Shadow · Size: curve=[0.00:0.48 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.59:0.42 1.00:0.00
- WaterFront · Size: curve=[0.00:0.59 1.00:1.00] · UV: frameOverTime=[0.00:0.00 0.40:0.45 1.00:1.00] tiles3x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.15:1.00 1.00:0.79 · CustomData: mode0=1 
- Glow_Heart · Size: curve=[0.00:0.48 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.26:0.31 1.00:0.00
- WaterBack · Size: curve=[0.00:0.59 1.00:1.00] · UV: frameOverTime=[0.00:0.00 0.40:0.45 1.00:1.00] tiles3x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.15:1.00 1.00:0.79 · CustomData: mode0=1 
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- WaterRipplesGround · Size: curve=[0.00:0.41 0.36:0.88 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.36:1.00
- CenterSplash · Size: curve=[0.00:0.75 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles6x3 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.22
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · InheritVelocity: 
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- WaterTiled2 · Color: mau 0.00#FFFFFF 0.99#C23F3F | alpha 0.41:1.00 1.00:0.84 · Sub: 2 sub 0 0
- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1

### FX_PF_RainExample

- GroundsRadials · Size: curve=[0.00:0.18 0.33:0.88 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- DistortRadialGround · Size: curve=[0.00:0.00 0.30:0.80 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- FX_PF_RainExample · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x3 anim0 cyc1
- DebrisGround_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x3 anim0 cyc1
- RainDetail · Size: curve=[0.00:1.00 1.00:0.00]
- DebrisGround_03 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x3 anim0 cyc1
- DebrisGround_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x3 anim0 cyc1
- DebrisGround_04 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x3 anim0 cyc1
- RainLong · Size: curve=[0.00:1.00 1.00:0.00]

### FX_PF_SimpleWaterImpact_01

- WaterDirectionalImpact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1 · Sub: 1 sub 0
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- Impact · Size: curve=[0.00:0.46 1.00:1.00] · Color: mau 0.00#98EFFF 0.49#007AA6 1.00#00184F | alpha 0.00:1.00 0.30:0.24 0.73:0.17 1.00:0.00
- WaterImpact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Sub: 1 sub 0
- Glow · Color: mau 0.00#FFFFFF 1.00#002F5B | alpha 0.13:1.00 1.00:0.00
- FoamImpact (3) · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00
- FoamImpact (2) · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00
- Impact (1) · Size: curve=[0.00:0.57 1.00:0.00] · Color: mau 0.00#FFFFFF 0.45#31566C | alpha 0.00:1.00 0.35:1.00 1.00:0.65
- GlowSecond · Color: mau 0.00#FFFFFF 0.16#002F5B | alpha 0.13:1.00 0.33:0.17 1.00:0.00
- FoamImpact (1) · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00

### FX_PF_WaterBuff_Loop

- Glow · Color: mau 0.05#0D82A1 0.99#0037FF | alpha 0.00:1.00 1.00:0.00
- ImpactSpikes · Size: curve=[0.00:1.00 1.00:0.82] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.45 1.00:0.00
- GroundCast · Size: curve=[0.00:0.40 1.00:1.00]
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- Glow_Heart · Size: curve=[0.00:0.48 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.26:0.31 1.00:0.00
- GlowADD · Rotation: curve=[-6.54149]
- Radial · Size: curve=[0.00:1.00 1.00:0.00] · Color: mau 0.00#FFFFFF 1.00#000873 | alpha 0.00:0.00 1.00:0.53
- Foam · Size: curve=[0.00:0.57 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.55 · CustomData: mode0=1 
- DistortWave · Size: curve=[0.00:0.40 0.21:0.93 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- GroundDots · Size: curve=[0.00:0.77 0.24:1.00 1.00:0.00] · Velocity: x=[0.00:0.00 1.00:0.00] y=[0.00:8.00 1.00:0.00] z=[0.00:1.00 1.00:1.00] · Noise: strength=[rand 0.00:1.00 1.00:1.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- SecondaryWater_Cast · Size: curve=[0.00:0.87 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1
- WaterRipplesGround · Size: curve=[0.00:0.41 0.28:0.92 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x3 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.36:1.00
- GoingUp · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x6 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 1.00:1.00
- GroundCaustics · Size: curve=[0.00:0.64 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.38:1.00 1.00:0.00
- GlowCast · Size: curve=[0.00:0.57 1.00:0.00]
- LoopGroundSpiral · Size: curve=[0.00:0.80 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- FX_PF_WaterBuff_Loop · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles5x5 anim0 cyc1
- GroundSpiral · Size: curve=[0.00:1.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- RadialAoE · Size: curve=[0.00:0.76 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#000873 | alpha 0.00:1.00 0.29:0.45 1.00:0.00
- GlowShadow · Rotation: curve=[-6.54149]
- SecondaryWater_Cast · Size: curve=[0.00:0.87 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1

### FX_PF_WaterGround_01

- WaterBack · Size: curve=[0.00:1.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x5 anim0 cyc1 · CustomData: mode0=1 
- GroundRadial · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- GroundFoam · Size: curve=[0.00:0.62 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x3 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- SparksGravity_Center · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- GroundSplash_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterFront · Size: curve=[0.00:1.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x5 anim0 cyc1 · CustomData: mode0=1 
- GroundSplash_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- GroundSplash_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- SparksGravity · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- GroundSplash_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterBack · Size: curve=[0.00:1.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x5 anim0 cyc1 · CustomData: mode0=1 
- WaterTiled · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.41:1.00 1.00:0.00 · Sub: 2 sub 0 0
- WaterFront · Size: curve=[0.00:1.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x5 anim0 cyc1 · CustomData: mode0=1 
- WaterTiled2 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.41:1.00 1.00:0.00 · Sub: 2 sub 0 0

### FX_PF_WaterLaser_Burst

- DotsDirectional · Size: curve=[0.00:1.00 1.00:0.00] · Velocity:  · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.21:1.00 1.00:0.00
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- LateralWater_Lingering_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterTiling (1) · Sub: 2 sub 0 0
- LaserNoise (6) · Rotation: curve=[rand 0.00:2.15 1.00:2.15] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- LaserCore · Size: curve=[0.01:1.24 1.00:1.24]
- WaterAOE_Waterback · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- 'ShockWave_Radial ' · Size: curve=[0.00:0.00 0.30:0.80 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- GroundDots · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- LaserNoise02 · Size: curve=[0.01:1.24 1.00:1.24]
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- LateralWater_Lingering_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- Splashes · Size: curve=[0.00:0.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.53
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- FX_PF_WaterLaser_Burst · Size: curve=[0.00:1.00 0.11:0.87 0.32:1.00 0.49:0.86 0.72:0.96 0.92:0.93 1.00:1.00]
- LaserNoise01 · Size: curve=[0.01:1.24 1.00:1.24]
- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterAOE_Waterfront · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- LaserNoise03 · Size: curve=[0.00:1.00 0.11:0.87 0.32:1.00 0.49:0.86 0.72:0.96 0.92:0.93 1.00:1.00] · Rotation: curve=[rand 0.00:2.15 1.00:2.15] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1

### FX_PF_WaterLaser_Cast

- LaserNoise 01 · Size: curve=[0.00:0.00 0.12:0.17 0.28:0.03 0.44:0.18 0.64:0.05 0.80:0.44 1.00:0.24]
- WaterAOE_Waterfront · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- LaserNoise 02 · Size: curve=[0.00:0.00 0.12:0.17 0.28:0.03 0.44:0.18 0.64:0.05 0.80:0.44 1.00:0.24]
- LaserNoise 03 · Size: curve=[0.00:1.00 0.11:0.87 0.32:1.00 0.49:0.86 0.72:0.96 0.92:0.93 1.00:1.00] · Rotation: curve=[rand 0.00:2.15 1.00:2.15] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- LaserCore · Size: curve=[0.00:0.00 0.12:0.17 0.28:0.03 0.44:0.18 0.64:0.05 0.80:0.44 1.00:0.24]
- WaterAOE_Waterback · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- WaterTiling02 · Sub: 2 sub 0 0
- Splashes · Size: curve=[0.00:0.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- DotsDirectional · Size: curve=[0.00:1.00 1.00:0.00] · Velocity:  · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.21:1.00 1.00:0.00
- FX_PF_WaterLaser_Cast · Size: curve=[0.00:1.00 0.11:0.87 0.32:1.00 0.49:0.86 0.72:0.96 0.92:0.93 1.00:1.00]

### FX_PF_WaterLaser_Dissolve

- LaserNoise01 · Size: curve=[0.00:0.38 0.44:0.39 1.00:0.00]
- GroundDots · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- DotsDirectional · Size: curve=[0.00:1.00 1.00:0.00] · Velocity:  · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.21:1.00 1.00:0.00
- LaserNoise03 · Size: curve=[0.00:1.00 0.11:0.87 0.32:1.00 0.49:0.86 0.72:0.96 0.92:0.93 1.00:1.00] · Rotation: curve=[rand 0.00:2.15 1.00:2.15] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- LateralWater_Lingering_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- WaterTiling02 · Sub: 2 sub 0 0
- LaserCore · Size: curve=[0.00:0.38 0.44:0.39 1.00:0.00]
- Splashes · Size: curve=[0.00:0.00 1.00:1.00] · Velocity: x=[rand 0.00:0.00 1.00:0.00] y=[rand 0.00:0.00 1.00:0.00] z=[rand 0.00:0.00 1.00:0.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- WaterAOE_Waterback · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- FX_PF_WaterLaser_Dissolve · Size: curve=[0.00:1.00 0.11:0.87 0.32:1.00 0.49:0.86 0.72:0.96 0.92:0.93 1.00:1.00]
- LaserNoise02 · Size: curve=[0.00:0.38 0.44:0.39 1.00:0.00]
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterAOE_Waterfront · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- LateralWater_Lingering_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1

### FX_PF_WaterLaser_Impact

- Radial · Size: curve=[0.00:0.41 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.20:0.24 1.00:0.00
- Glow_Heart · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.26:0.31 1.00:0.00
- GlowSecond · Color: mau 0.00#FFFFFF 0.16#002F5B | alpha 0.13:1.00 0.33:0.17 1.00:0.00
- LightImpact · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00
- CenterImpact · Size: curve=[0.00:1.00 1.00:0.00] · Color: mau 0.00#FFFFFF 0.41#47637A 1.00#23327A | alpha 0.00:1.00 1.00:1.00
- ShockWave_Radial · Size: curve=[0.00:0.00 0.30:0.80 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- WaterDirectionalImpact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1 · Sub: 1 sub 0
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- Glow · Color: mau 0.05#0D82A1 0.99#0037FF | alpha 0.00:1.00 0.19:0.19 1.00:0.00
- Impact · Size: curve=[0.00:0.71 1.00:1.00] · Color: mau 0.00#79E0FF 1.00#002E86 | alpha 0.00:1.00 0.33:0.42 1.00:0.00
- LateralWater_Lingering_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- WaterAOE_Waterback · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- LateralWater_Lingering_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- WaterDirectionalImpact2 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1 · Sub: 1 sub 0
- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- DarkImpact · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00
- GroundDots · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- WaterAOE_Waterfront · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterTiling · Sub: 2 sub 0 0
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- GlowMask · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.09:1.00 0.26:0.31 1.00:0.00
- ImpactSpikes · Size: curve=[0.00:1.00 1.00:0.82] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.45 1.00:0.00

### FX_PF_WaterLaser_MainLaser

- Splashes · Size: curve=[0.00:0.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- WaterAOE_Waterback · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterTiling · Sub: 2 sub 0 0
- LaserNoise 04 · Size: curve=[0.00:0.60 0.11:1.00 0.26:0.85 0.41:0.91 0.59:0.76 0.71:0.90 0.83:0.79 1.00:0.60]
- DotsDirectional · Size: curve=[0.00:1.00 1.00:0.00] · Velocity:  · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.21:1.00 1.00:0.00
- WaterAOE_Waterfront · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- LaserNoise 02 · Size: curve=[0.00:0.60 0.11:1.00 0.26:0.85 0.41:0.91 0.59:0.76 0.71:0.90 0.83:0.79 1.00:0.60]
- WaterAOE_Waterback · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- WaterTiling02 · Sub: 2 sub 0 0
- DotsDirectionalInside · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.21:1.00 1.00:0.00
- WaterAOE_Waterfront · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- GroundDots · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- LateralWater_Lingering_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- LaserNoise 03 · Size: curve=[0.00:0.60 0.11:1.00 0.26:0.85 0.41:0.91 0.59:0.76 0.71:0.90 0.83:0.79 1.00:0.60]
- LaserNoise 06 · Rotation: curve=[rand 0.00:2.15 1.00:2.15] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- WaterAOE_Waterfront · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- LaserNoise 05 · Size: curve=[0.00:1.00 0.11:0.87 0.32:1.00 0.49:0.86 0.72:0.96 0.92:0.93 1.00:1.00] · Rotation: curve=[rand 0.00:2.15 1.00:2.15] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- WaterTiling02 · Sub: 2 sub 0 0
- LateralWater_Lingering_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- WaterAOE_Waterback · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterAOE_Waterback · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- WaterTiling01 · Sub: 2 sub 0 0
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- LaserNoise 01 · Size: curve=[0.00:0.60 0.11:1.00 0.26:0.85 0.41:0.91 0.59:0.76 0.71:0.90 0.83:0.79 1.00:0.60]
- FX_PF_WaterLaser_MainLaser · Size: curve=[0.00:1.00 0.11:0.87 0.32:1.00 0.49:0.86 0.72:0.96 0.92:0.93 1.00:1.00]
- WaterAOE_Waterfront · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- LaserCore 02 · Size: curve=[0.00:0.60 0.11:1.00 0.26:0.85 0.41:0.91 0.59:0.76 0.71:0.90 0.83:0.79 1.00:0.60]
- LaserCore 01 · Size: curve=[0.00:0.60 0.11:1.00 0.26:0.85 0.41:0.91 0.59:0.76 0.71:0.90 0.83:0.79 1.00:0.60]
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 

### FX_PF_WaterOrb_Charge

- ImpactFlipbook · Size: curve=[0.00:1.00 1.00:0.00] · Color: mau 0.00#79A5FF 1.00#0063FF | alpha 0.00:1.00 0.89:1.00
- Glow · Color: mau 0.05#0D82A1 0.99#0037FF | alpha 0.00:1.00 1.00:0.00
- ImpactSpikes · Size: curve=[0.00:1.00 1.00:0.82] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.45 1.00:0.00
- Glow_Heart · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.26:0.31 1.00:0.00
- Radial · Size: curve=[0.00:0.52 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.28:0.45 1.00:0.00
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- DistortWave · Size: curve=[0.00:0.40 0.21:0.93 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- Foam · Size: curve=[0.00:0.57 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.55 · CustomData: mode0=1 

### FX_PF_WaterOrb_Dissolve

- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- GroundDots · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- Radial · Size: curve=[0.00:0.33 1.00:1.00] · Rotation: curve=[1.0472] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- FallingWater · Size: curve=[0.00:0.57 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.55 · CustomData: mode0=1 
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · Velocity: y=[3] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- Distort · Size: curve=[0.00:0.40 0.21:0.93 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- Glow_Heart · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.26:0.31 1.00:0.00
- Shadow · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.26:0.17 1.00:0.00
- Glow · Color: mau 0.05#0D82A1 0.99#0037FF | alpha 0.00:1.00 1.00:0.00
- Opaque · Size: curve=[0.00:0.97 0.32:1.25 1.00:1.40] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.09:0.61 1.00:0.00
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- DistortDots · Size: curve=[0.00:0.00 0.30:0.80 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- Water · Size: curve=[0.00:0.57 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.55 · CustomData: mode0=1 
- ImpactSpikes · Size: curve=[0.00:1.00 1.00:0.82] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.45 1.00:0.00

### FX_PF_WaterOrb_Loop

- AroundShapes_Waterup_00 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- FallingWater02 · Rotation: curve=[rand 0.00:0.61 1.00:0.61] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- AroundShapes_Waterup_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- GroundDots · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- BaseHighlight · Size: curve=[0.00:0.34 0.17:0.40 0.29:0.67 0.41:0.30 0.56:0.78 0.84:0.93 0.98:0.07] · Color: mau 0.50#000000 0.56#FFFFFF | alpha 0.62:0.00 0.69:1.00
- GroundDots · Velocity:  · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- Foam · Size: curve=[0.00:0.20 0.16:0.92 1.00:1.00] · Rotation: curve=[rand 0.00:0.21 1.00:0.21] · Velocity: x=[rand 0.00:0.00 1.00:0.00] y=[rand 0.00:0.00 1.00:0.00] z=[rand 0.00:0.00 1.00:0.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.11:1.00 1.00:0.42
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- WaterRipplesGround · Size: curve=[0.00:0.79 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x3 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- AroundShapes_Waterup_06 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- Glow_AB_Burst · Size: curve=[0.00:0.23 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 1.00:1.00
- BaseOpenWater · Size: curve=[0.00:0.50 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x6 anim0 cyc1 · Color: mau 0.00#00FFF4 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- FallingWater · Rotation: curve=[rand 0.00:0.61 1.00:0.61] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- AroundShapes · Rotation:  · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x6 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- AroundShapes_Waterup_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- LoopSphere · Noise: strength=[5]
- GroundSpiral · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- CastingWaterDots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- AroundShapes_Waterup_04 · Size: curve=[0.00:1.00 1.00:1.00] · Rotation: curve=[-1.13446] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.00
- ShockWave_Radial · Size: curve=[0.00:0.00 0.30:0.80 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- DistortDots · Size: curve=[0.00:0.00 0.30:0.80 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- GroundDots · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- AroundShapes_Waterup_05 · Size: curve=[0.00:1.00 1.00:1.00] · Rotation: curve=[-0.610865] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.00
- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- Glow_Add_Burst · Size: curve=[0.00:0.23 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 1.00:1.00
- DotsLoop · Velocity: x=[rand 0.00:0.00 1.00:0.00] y=[rand 0.00:0.00 1.00:0.00] z=[rand 0.00:0.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- AroundShapes_Waterup_03 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- BaseOpaque · Size: curve=[0.00:0.26 0.30:0.68 0.53:0.87 0.72:0.84 1.00:1.00] · Color: mau 0.00#00FFF4 1.00#FFFFFF | alpha 0.00:1.00 1.00:1.00

### FX_PF_WaterSimpleProjectile_Traveling

- Splashes · Size: curve=[0.00:0.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.52
- SparksGravity · Size: curve=[0.00:0.30 0.08:1.00 0.27:0.31 1.00:0.00] · Noise: strength=[0.00:0.00 1.00:5.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#174171 | alpha 0.00:1.00 0.34:0.58
- WaterTrail · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.23:0.16 1.00:0.00 · Trail: widthOverTrail=[0.00:0.52 1.00:1.00]

### FX_PF_Water_FoamImpact

- Foam · Size: curve=[0.00:0.57 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles6x4 anim1 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.55 · CustomData: mode0=1 
- Radial · Size: curve=[0.00:0.41 1.00:1.00] · Rotation: curve=[1.0472] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- Glow_Heart · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.26:0.31 1.00:0.00
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- ImpactSpikes · Size: curve=[0.00:1.00 1.00:0.82] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.45 1.00:0.00
- ImpactFlipbook · Size: curve=[0.00:1.00 1.00:0.00] · Color: mau 0.00#79A5FF 0.38#002E86 1.00#0063FF | alpha 0.00:1.00 0.89:1.00
- Glow · Color: mau 0.05#0D82A1 0.99#0037FF | alpha 0.00:1.00 0.19:0.19 1.00:0.00

### FX_PF_Water_Grenade_Explosion

- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- SmallSplashes · Rotation: curve=[rand 0.00:-0.52 1.00:-0.52] · Velocity: x=[rand 0.00:0.00 1.00:0.00] y=[rand 0.00:0.00 1.00:0.00] z=[rand 0.00:0.00 1.00:0.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- MainGlow · Size: curve=[0.00:0.54 0.14:0.80 1.00:1.00] · Color: mau 0.00#00A1FF 0.44#005E95 1.00#000F2D | alpha 0.12:1.00 0.30:0.16 1.00:0.00
- GroundRadial · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- RadialSecond · Size: curve=[0.00:0.54 0.14:0.80 1.00:1.00] · Color: mau 0.00#00A1FF 0.44#005E95 1.00#000F2D | alpha 0.12:1.00 1.00:0.00
- GroundFoam · Size: curve=[0.00:0.62 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x3 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- AroundShape_First · Size: curve=[0.00:0.74 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.17:0.90 0.25:0.47 1.00:0.00
- Radial · Size: curve=[0.00:0.68 0.13:0.92 1.00:1.00] · Color: mau 0.00#00A1FF 0.44#005E95 1.00#000F2D | alpha 0.00:1.00 0.20:0.35 1.00:0.00
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- Circle · Size: curve=[0.00:0.63 0.13:1.00 0.30:0.22 1.00:0.00] · Color: mau 0.00#FFF9C1 0.15#F7A56C 0.17#0DB0FF 0.61#2967C5 1.00#052D69 | alpha 0.00:1.00 1.00:1.00
- AroundShape · Size: curve=[0.00:0.74 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.17:0.90 0.25:0.47 1.00:0.00
- Impact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1 · Sub: 1 sub 0
- CircleCenter · Size: curve=[0.00:0.63 0.13:1.00 0.30:0.22 1.00:0.00] · Color: mau 0.00#FFA652 0.14#FF6800 0.16#0DB0FF 0.61#2967C5 1.00#052D69 | alpha 0.00:1.00 1.00:1.00
- ImpactAround · Size: curve=[0.00:1.00 1.00:0.82] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.35:0.49 1.00:0.00
- Around · Size: curve=[0.00:0.20 0.33:0.92 1.00:1.00] · Rotation: curve=[0.00:-10.47 0.85:-0.50] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x5 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.42:1.00 1.00:0.24
- GroundRadialDots · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- ShockWave_Radial · Size: curve=[0.00:0.00 0.30:0.80 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- ShockWave · Size: curve=[0.00:0.40 0.21:0.93 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- FoamShapes · Size: curve=[0.00:1.00 1.00:0.82] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.17:1.00 1.00:0.00
- ImpactGlow · Size: curve=[0.00:1.00 0.60:0.29] · Color: mau 0.00#0084FF 0.46#000E21 1.00#000000 | alpha 0.00:1.00 0.35:1.00 1.00:0.00
- GlowContrast · Size: curve=[0.00:0.63 1.00:1.00] · Color: mau 0.00#A2FFF3 0.31#5293A1 1.00#00184F | alpha 0.00:1.00 0.35:1.00 1.00:0.00
- VerticalSplash · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 

### FX_PF_Water_Grenade_Preexplosion

- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- BaseOpaque · Size: curve=[0.00:0.34 0.17:0.40 0.29:0.67 0.41:0.30 0.56:0.78 0.84:0.93 0.98:0.07]
- TiledAround · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1
- ExtraBeams · Size: curve=[0.00:0.56 0.36:1.00 1.00:0.00] · Noise: strength=[4]
- MaskGlow · Size: curve=[0.00:0.34 0.17:0.40 0.29:0.67 0.41:0.30 0.56:0.78 0.84:0.93 0.98:0.07]
- ADD · Size: curve=[0.00:0.34 0.17:0.40 0.29:0.67 0.41:0.30 0.56:0.78 0.84:0.93 0.98:0.07]
- Smalwhip · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Sub: 1 sub 0
- BaseHighlight · Size: curve=[0.00:0.34 0.17:0.40 0.29:0.67 0.41:0.30 0.56:0.78 0.84:0.93 0.98:0.07] · Color: mau 0.50#000000 0.56#FFFFFF | alpha 0.62:0.00 0.69:1.00
- BaseOverload · Size: curve=[0.00:0.34 0.17:0.40 0.29:0.67 0.41:0.30 0.56:0.78 0.84:0.93 0.98:0.07]
- TiledAround2 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x8 anim0 cyc1

### FX_PF_Water_ImpactGround

- WaterTiling · Sub: 2 sub 0 0
- VerticalImpact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x3 anim0 cyc1
- FoamShapes · Size: curve=[0.00:1.00 1.00:0.82] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.17:1.00 1.00:0.00
- ShockWave · Size: curve=[0.00:0.40 0.21:0.93 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- ImpactGlow · Size: curve=[0.00:1.00 0.33:0.55] · Color: mau 0.00#A2FFF3 0.72#0070FF 1.00#00184F | alpha 0.00:1.00 0.35:1.00 1.00:1.00
- OpenWave · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Sub: 1 sub 0
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- VerticalSplash · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles5x5 anim0 cyc1
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- GlowContrast · Size: curve=[0.00:0.63 1.00:1.00] · Color: mau 0.00#A2FFF3 0.31#5293A1 1.00#00184F | alpha 0.00:1.00 0.35:1.00 1.00:0.00
- ShockWave_Radial · Size: curve=[0.00:0.00 0.30:0.80 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- WaterAOE_Waterback · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- GroundWave_02 · Size: curve=[0.00:0.72 1.00:1.00] · UV: frameOverTime=[0.00:0.31 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterAOE_Waterfront · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- FoamImpact · Size: curve=[0.00:1.00 1.00:0.82] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.17:1.00 1.00:0.00
- FoamContrast · Size: curve=[0.00:1.00 1.00:0.82] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 1.00:0.00
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- GroundWave_01 · Size: curve=[0.00:0.72 1.00:1.00] · UV: frameOverTime=[0.00:0.39 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 

### FX_PF_Water_Impact_01

- Glow · Color: mau 0.00#FF7D00 0.33#800011 1.00#540009 | alpha 0.00:1.00 0.35:1.00 1.00:1.00
- WaterImpact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Sub: 1 sub 0
- WaterDirectionalImpact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1 · Sub: 1 sub 0
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- Impact · Size: curve=[0.00:1.00 1.00:0.00] · Color: mau 0.00#14CDFF 0.31#5293A1 1.00#00184F | alpha 0.00:1.00 0.35:1.00 1.00:1.00

### FX_PF_Water_LineaSlash_01

- LightSlash · Size: curve=[0.00:1.00 0.18:0.88] · Velocity: x=[90] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.61:1.00 1.00:0.00
- Glow · Size: curve=[0.00:0.35 0.05:1.45] · Velocity: x=[12] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- Dots_02 · Size: curve=[0.00:1.00 0.27:0.40 1.00:0.00] · Velocity: x=[rand 0.00:0.00 1.00:0.00] y=[rand 0.00:0.00 1.00:0.00] z=[rand 0.00:0.00 1.00:0.00] · Noise: strength=[0.00:0.00 1.00:1.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- Dots_01 · Size: curve=[0.00:1.00 0.27:0.40 1.00:0.00] · Velocity: x=[rand 0.00:0.00 1.00:0.00] y=[rand 0.00:0.00 1.00:0.00] z=[rand 0.00:0.00 1.00:0.00] · Noise: strength=[0.00:0.00 1.00:1.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- SlashLinear · Velocity: x=[20.08] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 0.22#5C7384 | alpha 0.61:1.00 1.00:0.00

### FX_PF_Water_Projectile_Cast

- WaterAOE_Waterback · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x6 anim0 cyc1
- WaterAOE_Waterfront · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x6 anim0 cyc1
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- WaterDirectionalImpact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x3 anim0 cyc1 · Sub: 1 sub 0
- DirectionalFoam · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00
- GlowSecond · Color: mau 0.00#FFFFFF 0.16#002F5B | alpha 0.13:1.00 0.33:0.17 1.00:0.00
- Impact · Size: curve=[0.00:0.57 1.00:0.00] · Color: mau 0.00#FFFFFF 0.45#31566C | alpha 0.00:1.00 0.35:1.00 1.00:0.65
- DirectionalFoamDark · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00
- Glow · Color: mau 0.00#FFFFFF 1.00#002F5B | alpha 0.13:1.00 1.00:0.00
- Father3DShapes · Sub: 2 sub 0 0
- WaterImpact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Sub: 1 sub 0

### FX_PF_Water_SimpleSplash_01

- WaterBack · Size: curve=[0.00:0.65 1.00:1.00] · UV: frameOverTime=[0.00:0.00 0.40:0.45 1.00:1.00] tiles4x5 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.15:1.00 0.59:0.00 · CustomData: mode0=1 
- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- WaterRipplesGround · Size: curve=[0.00:0.41 0.36:0.88 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.36:1.00
- CenterSplash · Size: curve=[0.00:0.75 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles6x3 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.22
- Shadow · Size: curve=[0.00:0.48 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.59:0.42 1.00:0.00
- WaterTiled2 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.41:1.00 1.00:0.00 · Sub: 2 sub 0 0
- Glow_Heart · Size: curve=[0.00:0.48 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.26:0.31 1.00:0.00
- WaterFront · Size: curve=[0.00:0.65 1.00:1.00] · UV: frameOverTime=[0.00:0.00 0.40:0.45 1.00:1.00] tiles4x5 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.15:1.00 0.59:0.00 · CustomData: mode0=1 

### FX_PF_Water_SlashBasic_01

- Slash_Water_Secondary_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- GlowMas · Rotation: curve=[0.00:-4.22 1.00:-0.54] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.22 0.19:0.97 0.36:0.22 1.00:0.00
- SparksGravity · Size: curve=[0.00:1.00 0.27:0.40 1.00:0.00] · Velocity:  · Noise: strength=[0.00:0.00 1.00:1.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- SparksGravity_02 · Size: curve=[0.00:1.00 0.27:0.40 1.00:0.00] · Velocity:  · Noise: strength=[0.00:0.00 1.00:1.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1
- Slash_Water_Main · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1 · Color: mau 0.16#FFFFFF 0.64#FFFFFF 1.00#4A69F2 | alpha 0.67:1.00 1.00:0.00
- Slash_Highlight · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1 · Color: mau 0.00#576895 0.18#7B9EFF 0.27#FFFFFF 0.61#FFFFFF 1.00#142C6E | alpha 0.00:1.00 1.00:1.00

### FX_PF_Water_StrongProjectile_Cast

- Father3DShapes · Velocity: x=[1233] · Sub: 2 sub 0 0
- WaterAOE_Waterback · Velocity: z=[3] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x6 anim0 cyc1
- DirectionalFoamDark · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00
- Glow · Color: mau 0.00#FFFFFF 1.00#002F5B | alpha 0.13:1.00 1.00:0.00
- WaterAOE_Waterfront · Velocity: z=[3] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x6 anim0 cyc1
- WaterDirectionalImpact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x3 anim0 cyc1 · Sub: 1 sub 0
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- GlowSecond · Color: mau 0.00#FFFFFF 0.16#002F5B | alpha 0.13:1.00 0.33:0.17 1.00:0.00
- Father3DShapes2 · Velocity: x=[1233] · Sub: 2 sub 0 0
- WaterAOE_Waterfront · Velocity: z=[3] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x6 anim0 cyc1
- WaterAOE_Waterback · Velocity: z=[3] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x6 anim0 cyc1
- Impact · Size: curve=[0.00:0.57 1.00:0.00] · Color: mau 0.00#FFFFFF 0.45#31566C | alpha 0.00:1.00 0.35:1.00 1.00:0.65
- DirectionalFoam · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00

### FX_PF_Water_StrongProjectile_Impact

- Aroundshape · Rotation:  · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- WaterDirectionalImpact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1 · Sub: 1 sub 0
- Lightimapct · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00
- ShockWave_Radial · Size: curve=[0.00:0.00 0.30:0.80 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- Glow · Color: mau 0.00#FFFFFF 1.00#002F5B | alpha 0.13:1.00 1.00:0.00
- DarkImpact · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.16:0.53 1.00:0.00
- GlowSecond · Color: mau 0.00#FFFFFF 0.16#002F5B | alpha 0.13:1.00 0.33:0.17 1.00:0.00
- Impact · Size: curve=[0.00:0.46 1.00:1.00] · Color: mau 0.00#98EFFF 0.49#007AA6 1.00#00184F | alpha 0.00:1.00 0.30:0.24 0.73:0.17 1.00:0.00
- MainImpact · Size: curve=[0.00:0.68 0.09:1.00 0.21:0.14 1.00:0.00] · Color: mau 0.00#FFFFFF 0.45#31566C | alpha 0.00:1.00 0.35:1.00 1.00:0.65
- SmallSparks · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 

### FX_PF_Water_StrongProjectile_Traveling

- AroundShape_Linger · Rotation:  · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- WaterTrail · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.23:0.16 1.00:0.00 · Trail: widthOverTrail=[0.00:0.52 1.00:1.00]
- Splashes · Size: curve=[0.00:0.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.52
- Aroundshape · Rotation:  · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- LinearSplash 2 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1
- Bubble · Size: curve=[0.00:2.00 0.13:0.92 0.34:1.19 0.51:0.68 0.74:1.12 1.00:0.79] · Rotation: curve=[rand 0.00:0.35 1.00:0.35] · Velocity:  · Noise:  · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · Sub: 2 sub 2 2
- LinearSplash · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1
- LinearSplash 3 · Size: curve=[0.00:1.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1
- LoopFace · Size: curve=[0.00:2.00 0.01:1.22] · Noise: strength=[0.5] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles5x5 anim0 cyc1
- SparksGravity · Size: curve=[0.00:0.30 0.08:1.00 0.27:0.31 1.00:0.00] · Noise: strength=[0.00:0.00 1.00:5.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#174171 | alpha 0.00:1.00 0.34:0.58
- WaterTrail · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.23:0.16 1.00:0.00 · Trail: widthOverTrail=[0.00:0.52 1.00:1.00]
- DestroyBubbles02 · Size: curve=[0.00:0.68 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- DestroyBubbles · Size: curve=[0.00:0.68 1.00:1.00] · Rotation: curve=[rand 0.00:-0.52 1.00:-0.52] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x3 anim0 cyc1

### FX_PF_Waterfall_MainFoam

- FoamSmoke · Size: curve=[0.00:0.57 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.55
- FoamFill_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- BackFoam · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x8 anim0 cyc1
- FoamFill_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- GroundWater · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x3 anim0 cyc1
- Dots · Size: curve=[0.58:1.00 1.00:0.00]
- MainFoam · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x8 anim0 cyc1

### FX_PF_Waterfall_SingleFoam_01

- MainFoamLoop · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x8 anim0 cyc1
- Dots · Size: curve=[0.58:1.00 1.00:0.00]
- FoamFill_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1

### FX_PF_Waterfall_SingleFoam_02

- MainFoamLoop · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x8 anim0 cyc1
- FoamFill_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- Dots · Size: curve=[0.58:1.00 1.00:0.00]
- FoamFill_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1

### FX_PF_Waterfall_UnderwaterFoam

- GroundFoam · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x8 anim0 cyc1
- GroundFoamDark · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x8 anim0 cyc1

### FX_PF_WaveAttack_Burst

- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- HeadGlow · Size: curve=[0.00:1.15 1.00:2.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- BurstFlipbook · Size: curve=[0.00:0.64 0.13:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1
- BurstWaves · Size: curve=[0.00:1.15 1.00:2.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- Head_Burst · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1

### FX_PF_WaveAttack_Cast

- LateralWater_Lingering_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- Head_Core_Burst · Size: curve=[0.00:1.15 1.00:2.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- FoamSmoke · Size: curve=[0.00:0.57 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.55
- Head_Front_Burst · Size: curve=[0.00:1.15 1.00:2.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- LateralWater_Lingering_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- Head_Front_ExtraBurst · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1

### FX_PF_WaveAttack_Impact

- Impact · Size: curve=[0.00:0.71 1.00:1.00] · Color: mau 0.00#79E0FF 1.00#002E86 | alpha 0.00:1.00 0.33:0.42 1.00:0.00
- Glow · Color: mau 0.05#0D82A1 0.99#0037FF | alpha 0.00:1.00 0.19:0.19 1.00:0.00
- ImpactSpikes · Size: curve=[0.00:1.00 1.00:0.82] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.45 1.00:0.00
- LateralWater_Lingering_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- ShockWave_Radial · Size: curve=[0.00:0.00 0.30:0.80 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00 · CustomData: mode0=1 
- LateralWater_Lingering_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- CenterImpact · Size: curve=[0.00:1.00 1.00:0.00]
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- WaterDirectionalImpact · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1 · Sub: 1 sub 0
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- GlowSecond · Color: mau 0.00#FFFFFF 0.16#002F5B | alpha 0.13:1.00 0.33:0.17 1.00:0.00
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- GroundDots · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- FrontImpact · Size: curve=[0.00:0.64 0.13:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles3x4 anim0 cyc1
- LightImpact · Size: curve=[0.00:1.00 1.00:0.00] · UV: tiles2x2 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#0052AA | alpha 0.00:1.00 0.19:0.53 1.00:0.00
- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- Radial · Size: curve=[0.00:0.41 1.00:1.00] · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.20:0.24 1.00:0.00
- Glow_Heart · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.26:0.31 1.00:0.00

### FX_PF_WaveAttack_Projectile

- WaterGround_04 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- LateralWaves_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles5x5 anim0 cyc1
- WaterGround_02 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x3 anim0 cyc1
- GlowLingering · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 1.00:0.00
- FoamSmoke · Size: curve=[0.00:0.57 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:1.00 0.35:1.00 1.00:0.55
- Dots · Size: curve=[0.00:1.00 1.00:0.00] · UV: frameOverTime=[rand 0.00:0.00 1.00:1.00] tiles2x2 anim0 cyc1 · InheritVelocity: 
- LateralWaves_Front_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- LateralWaves_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles5x5 anim0 cyc1
- Main · Size: curve=[0.00:0.64 0.13:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles2x5 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.01:0.00 0.56:1.00
- WaterGround_03 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles3x3 anim0 cyc1
- WaterGround_01 · UV: frameOverTime=[0.00:0.00 1.00:0.99] tiles4x4 anim0 cyc1
- LateralWater_Lingering_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- GroundFoamDark · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x8 anim0 cyc1
- LateralWater_Lingering_02 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- GroundDots · Size: curve=[0.00:0.39 0.45:0.90 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1 · Color: mau 0.00#FFFFFF 1.00#FFFFFF | alpha 0.00:0.00 0.31:1.00
- WaterLingering · Size: curve=[0.00:0.00 1.00:1.00] · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1
- LateralWaves_Front_01 · UV: frameOverTime=[0.00:0.00 1.00:1.00] tiles4x4 anim0 cyc1