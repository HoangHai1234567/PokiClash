# Mây chuyển scene (2026-11-24)

Hai nửa mây khép vào giữa khi chuyển scene (`App/CloudCover.cs`, prefab `04 Prefabs/App/App.prefab`, Canvas phủ / Nen / May / trai, phai).

- Gen bằng Magnific (GPT 2.6, 2k high, nền trong suốt, 9:16, 175 credit/ảnh), ảnh mẫu nét: `Assets/03 Art/Islands/land_thuy_may_1.png`.
- `tai_ve/may_1.png`, `tai_ve/may_2.png`: ảnh gốc 1520 x 2688, cụm mây quay sang phải.
- `may_trai.png`, `may_phai.png`: đã cắt lề trong suốt bên phải (mép cụm mây chạm gần mép ảnh), chép vào
  `Assets/03 Art/Kit/may_chuyen_trai.png`, `may_chuyen_phai.png`. Nửa phải trong prefab lật ngang (scale x = -1) nên cụm quay sang trái.
- Đã thử ghép lúc khép kín (mỗi nửa 0,95 bề ngang x 1,15 bề cao màn) ở màn 9:16, 9:20, 3:4: che kín, không lỗ.

Prompt (gửi nguyên văn, count 2):

> A tall vertical column of cartoon cloud for a mobile game screen transition, hand-drawn in the exact same style as reference image 1
> (a small hand-drawn cloud: dark brown-black ink outline, cream fill). Shape: the cloud fills the whole canvas from the very top edge to
> the very bottom edge. Its LEFT side is a straight vertical cut that runs off the left border of the canvas ... Its RIGHT side is a bumpy
> edge made of 8 to 10 big round puffs ... Flat coloring: no shading, no gradient, no highlight, no glow, no drop shadow. Background outside
> the cloud: fully transparent.
