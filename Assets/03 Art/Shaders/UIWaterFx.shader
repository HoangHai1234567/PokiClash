// HIỆU ỨNG NƯỚC TRONG TRẬN BẰNG SHADER (người dùng 2026-11-24 chọn "c": toàn bộ bộ nước chạy bằng shader thay khung vẽ sẵn; lốc nước
// giữ khung). Học shader repo abitofgamedev/water_vfx (skill vfx-petclash/hoc_water_vfx_abitofgamedev.md): mọi hình tan theo
// step(ngưỡng, mặt_nạ_mềm × nhiễu), tia ống dùng HAI NGƯỠNG trên một dải dọc ống, cầu rung theo nhiễu. Chất nước là bộ nước v2 đã duyệt
// (blender_anime_fx.md mục 13c): lam nhạt + bọt trắng, dải màu PHẲNG, không quầng sáng, không chuyển màu (luật UI).
// Bản 2 (người dùng xem tour: "cần nổi khối hơn chút và có chút texture kiểu vẽ tay"):
//  - NỔI KHỐI kiểu cel: theo pháp tuyến giả của hình, mặt hướng sáng (trên trái) thành MẢNG SÁNG trắng, mặt khuất thành MẢNG TỐI lam
//    sâu (_ColShade), mép lam sâu; ranh các mảng run nhẹ theo nhiễu mịn (nét tay, không thẳng tắp); cầu có chấm sáng nhỏ trên trái;
//  - VÂN CHÌ vẽ tay: A của _MainTex là nét gạch chéo ~−38° đứt quãng (ArtGen/Spine/nuoc_shader/tao_texture.py), lấy theo toạ độ màn hình
//    (nét giữ cỡ, góc khi hình xoay), nhân tối nhẹ màu (_Hatch); mảng bọt nhạt hơn;
//  - mép hình run theo nhiễu mịn; vân nước kéo tương phản (_Contrast) cho đủ mảng sâu / bọt.
// Một lưới uGUI (HatNuocFx) chứa mọi hình nước của một lớp hạt; mỗi đỉnh mang tham số của hình nó (không tạo material lúc chạy):
//   TEXCOORD0.xy = toạ độ trong hình (theo loại)
//   TEXCOORD1    = (loại, ngưỡng tan, p1, p2)                 — Canvas của lớp hạt phải bật kênh TexCoord1, TexCoord2 (menu NuocFxMenu)
//   TEXCOORD2    = (giờ sân, hạt giống, p3, p4)
//   COLOR        = nhân màu, a = độ hiện
// Loại: 0 CẦU  uv ∈ [-1,1]²; p1 = độ rung, p2 = tốc xoay vệt
//       1 DẢI  uv.x = quãng dọc (đơn vị UI / 100), uv.y = ngang [-1,1]; p1 = ngưỡng đầu, p2 = ngưỡng đuôi, p3 = quãng 0..1,
//              p4 = phần sáng theo hướng ngang (pháp tuyến trụ giả); ngưỡng tan > 0,5: dải BỌT trắng rách (mào sóng)
//       2 MẶT NẠ uv ∈ [0,1]²; p1 = ô atlas, p2 = dải mép bọt, p3 = 1 phẳng / 0 vòm, p4 = cỡ nhiễu
//       3 QUẠT (vương miện) uv = (x ∈ [-1,1], y ∈ [0,1]), gốc quạt ở (0,0); p1 = ô atlas (ngón), p2 = nửa góc mở (rad),
//              p3 = số lần lặp ngón, p4 = bán kính trong
//       4 VÀNH (loang trên đất) uv ∈ [-1,1]²; p1 = ô atlas, p2 = bán kính trong, p3 = lặp quanh vành, p4 = nửa vẽ (+1 trước, −1 sau, 0 cả)
//       5 CHẤM (giọt) uv ∈ [-1,1]²; p1 = tông (0 sâu, 1 sáng, 2 bọt)
// Bản 3 (người dùng 2026-11-25: "làm lại vfx nước của game theo asset này ... dùng thẳng nhưng nên thay đổi đi chút"; gói SrRubfish Water
// VFX 02 + NamuFX Stylized Water, nguồn ở ArtGen/Spine/nuoc_goi/NGUON.md). Gói tô flipbook bằng LERP giá trị xám giữa MainColor và
// HighColor (LerpTransparencies), tia là mesh Fresnel + vân nhiễu trôi + tan smoothstep theo alpha hạt. Ở đây giữ dáng + nhịp của gói,
// đổi chất: giá trị → DẢI MÀU CEL lam nhạt / bọt của game (ranh dải run nét tay), mép cắt sắc (alpha qua ngưỡng), tan = ngưỡng mép
// dâng theo độ hiện (ăn mòn như gói), phủ vân chì như mọi hình nước.
//       6 FLIPBOOK uv0.xy = uv khung A trong _FbTex, uv0.zw = uv khung B (chồng mờ); p1 = ngưỡng mép, p2 = cặp kênh (0 RG, 1 BA),
//              thr = tỉ lệ khung B; p3 = nâng giá trị (+ sáng hơn), p4 = kiểu (0 thường, 1 nền đất phẳng tối hơn, 2 toàn bọt trắng)
//       7 ỐNG TIA uv.x = quãng dọc (UI / 100), uv.y = ngang [-1,1]; thr = ngưỡng tan (vỡ), p1 = tốc trôi vân, p2 = lớp (0 vỏ ngoài,
//              1 lõi sáng, 2 vệt bọt trôi, 3 vỏ mỏng rách), p3 = quãng 0..1, p4 = phần sáng theo hướng ngang
Shader "PokiClash/UIWaterFx"
{
    Properties
    {
        [PerRendererData] _MainTex ("Nhiễu lặp (R mượt, G vừa, B mịn, A vân chì)", 2D) = "gray" {}
        _MaskTex ("Mặt nạ mềm (atlas 4x4)", 2D) = "black" {}
        _FbTex ("Flipbook nước (RG cặp 0, BA cặp 1: giá trị, alpha)", 2D) = "black" {}
        _VetTex ("Vân lặp (R vân sắc, G lưới toon, B nhiễu tan, A vệt đuôi)", 2D) = "gray" {}
        _FbStops ("Ngưỡng dải flipbook (x tối, y sâu, z sáng→bọt)", Vector) = (0.2, 0.42, 0.74, 0)
        _ColShade ("Mảng tối", Color) = (0.373, 0.761, 0.925, 1)
        _ColDeep ("Lam sâu", Color) = (0.494, 0.851, 0.965, 1)
        _ColBody ("Lam sáng", Color) = (0.576, 0.910, 1, 1)
        _ColFoam ("Bọt trắng", Color) = (0.918, 0.984, 1, 1)
        _Stops ("Ngưỡng ramp (x sâu-sáng, y sáng-bọt)", Vector) = (0.36, 0.66, 0, 0)
        _Light ("Hướng sáng (x trái-phải, y lên, z ra máy)", Vector) = (-0.45, 0.55, 0.75, 0)
        _VolK ("Độ khối cel (vân)", Float) = 0.14
        _Hi ("Ngưỡng mảng sáng", Float) = 0.62
        _Lo ("Ngưỡng mảng tối", Float) = -0.05
        _Rim ("Mép lam sâu (bán kính bắt đầu)", Float) = 0.84
        _Contrast ("Tương phản vân", Float) = 1.6
        _Hatch ("Độ đậm vân chì", Float) = 0.5
        _HatchPx ("Cỡ ô vân chì (px UI)", Float) = 110

        _StencilComp ("Stencil Comparison", Float) = 8
        _Stencil ("Stencil ID", Float) = 0
        _StencilOp ("Stencil Operation", Float) = 0
        _StencilWriteMask ("Stencil Write Mask", Float) = 255
        _StencilReadMask ("Stencil Read Mask", Float) = 255
        _ColorMask ("Color Mask", Float) = 15
        [Toggle(UNITY_UI_ALPHACLIP)] _UseUIAlphaClip ("Use Alpha Clip", Float) = 0
    }

    SubShader
    {
        Tags { "Queue" = "Transparent" "IgnoreProjector" = "True" "RenderType" = "Transparent" "PreviewType" = "Plane" "CanUseSpriteAtlas" = "True" }
        Stencil
        {
            Ref [_Stencil]
            Comp [_StencilComp]
            Pass [_StencilOp]
            ReadMask [_StencilReadMask]
            WriteMask [_StencilWriteMask]
        }
        Cull Off
        Lighting Off
        ZWrite Off
        ZTest [unity_GUIZTestMode]
        Blend SrcAlpha OneMinusSrcAlpha
        ColorMask [_ColorMask]

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma target 3.0
            #include "UnityCG.cginc"
            #include "UnityUI.cginc"
            #pragma multi_compile_local _ UNITY_UI_CLIP_RECT
            #pragma multi_compile_local _ UNITY_UI_ALPHACLIP

            struct appdata
            {
                float4 vertex : POSITION;
                float4 color : COLOR;
                float4 uv0 : TEXCOORD0;
                float4 uv1 : TEXCOORD1;
                float4 uv2 : TEXCOORD2;
            };

            struct v2f
            {
                float4 pos : SV_POSITION;
                fixed4 color : COLOR;
                float4 uv0 : TEXCOORD0;
                float4 uv1 : TEXCOORD1;
                float4 uv2 : TEXCOORD2;
                float4 wpos : TEXCOORD3;
            };

            sampler2D _MainTex, _MaskTex, _FbTex, _VetTex;
            fixed4 _ColShade, _ColDeep, _ColBody, _ColFoam;
            float4 _Stops, _Light, _ClipRect, _FbStops;
            float _VolK, _Hi, _Lo, _Rim, _Contrast, _Hatch, _HatchPx;

            v2f vert(appdata v)
            {
                v2f o;
                o.wpos = v.vertex;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.color = v.color;
                o.uv0 = v.uv0;
                o.uv1 = v.uv1;
                o.uv2 = v.uv2;
                return o;
            }

            float3 Ramp(float f) { return f < _Stops.x ? _ColDeep.rgb : (f < _Stops.y ? _ColBody.rgb : _ColFoam.rgb); }
            float NR(float2 uv) { return saturate((tex2D(_MainTex, uv).r - 0.5) * _Contrast + 0.5); }
            float NG(float2 uv) { return tex2D(_MainTex, uv).g; }
            float NB(float2 uv) { return tex2D(_MainTex, uv).b; }
            // ô atlas 4x4 (ô 0 ở góc TRÊN trái ảnh; v = 0 là đáy ô)
            float Mask(float idx, float2 uv)
            {
                idx = round(idx);
                float cx = fmod(idx, 4), ry = floor(idx / 4);
                uv = clamp(uv, 0.004, 0.996);
                return tex2D(_MaskTex, (float2(cx, 3 - ry) + uv) * 0.25).r;
            }
            float Cover(float d) { return saturate(d / max(fwidth(d), 1e-4) + 0.5); }
            float3 L3() { return normalize(_Light.xyz); }
            // NỔI KHỐI: d = độ hướng sáng (−1..1) + run nét tay → mảng tối / giữ màu vân / mảng sáng trắng
            float3 Cel(float3 col, float d, float2 wob)
            {
                d += (NB(wob) - 0.5) * 0.16;
                col = d < _Lo ? _ColShade.rgb : col;
                col = d > _Hi ? _ColFoam.rgb : col;
                return col;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                int mode = (int)round(i.uv1.x);
                float thr = i.uv1.y, p1 = i.uv1.z, p2 = i.uv1.w;
                float time = i.uv2.x, seed = i.uv2.y, p3 = i.uv2.z, p4 = i.uv2.w;
                float3 col = _ColBody.rgb;
                float a = 1;
                float foamy = 0; // 1: vùng này là bọt → vân chì nhạt hơn
                if (mode == 0) // ---------------- CẦU
                {
                    float2 p = i.uv0.xy;
                    float r = length(p);
                    float ang = atan2(p.y, p.x);
                    float wob = (NG(float2(ang * 0.159 + seed, time * 0.35)) - 0.5) * 2 * p1 + (NB(p * 0.9 + seed) - 0.5) * 0.04;
                    float rr = r - wob;
                    a = Cover(1 - rr);
                    float nz = sqrt(saturate(1 - min(dot(p, p), 0.999)));
                    float3 n = float3(p, nz);
                    float lon = atan2(p.x, nz) / 3.1416 + time * p2 + seed;
                    float lat = asin(clamp(p.y, -1, 1)) / 3.1416;
                    float v = NR(float2(lon * 0.9, lat * 2.2 + seed * 0.37));
                    float d = dot(n, L3());
                    col = Cel(Ramp(v + _VolK * d), d * 0.8, p * 1.3 + seed); // cầu: mảng sáng gọn thành lưỡi liềm trên trái (d × 0,8)
                    float2 hp = p - float2(-0.42, 0.44); // chấm sáng nhỏ trên trái
                    col = dot(hp, hp) < 0.024 ? _ColFoam.rgb : col;
                    col = rr > _Rim ? _ColDeep.rgb : col;
                    foamy = d * 0.8 > _Hi ? 1 : 0;
                    if (thr > 0.001) a *= Cover(NB(p * 1.7 + seed) - thr);
                }
                else if (mode == 1) // ---------------- DẢI (tia, ống, đuôi, mũi thương, sóng)
                {
                    float along = i.uv0.x, ac = i.uv0.y;
                    float edge = 1 - abs(ac) + (NB(float2(along * 0.9 + seed, ac * 0.3)) - 0.5) * 0.08;
                    a = Cover(edge);
                    float nz = sqrt(saturate(1 - ac * ac));
                    float d = ac * p4 + nz * L3().z * 0.55;
                    float v = NR(float2(along * 0.38 - time * 1.6 + seed, ac * 0.55 + seed * 0.71));
                    col = Cel(Ramp(v + _VolK * d), d * 1.25, float2(along * 0.7 + seed, ac * 0.4));
                    col = abs(ac) > _Rim ? _ColDeep.rgb : col;
                    foamy = d * 1.25 > _Hi ? 1 : 0;
                    float m = p3 + (NG(float2(along * 0.8 + seed, ac * 0.5)) - 0.5) * 0.12;
                    a *= Cover(m - p2) * Cover(p1 - m);
                    if (thr > 0.5) // dải BỌT (mào sóng): trắng, rách lỗ theo nhiễu
                    {
                        col = _ColFoam.rgb;
                        foamy = 1;
                        a *= Cover(NG(float2(along * 1.4 + seed, ac * 0.7 + seed)) - (thr - 0.5));
                    }
                }
                else if (mode == 2) // ---------------- MẶT NẠ MỀM (chấm toé, vũng)
                {
                    float2 uv = i.uv0.xy;
                    float m = Mask(p1, uv);
                    float nn = saturate((NG(uv * p4 + seed) - 0.3) / 0.4);
                    float vv = m * (0.35 + 0.65 * nn);
                    float dd = vv - thr;
                    a = Cover(dd + (NB(uv * 2.3 + seed) - 0.5) * 0.03);
                    float2 c2 = uv * 2 - 1;
                    float3 n = normalize(float3(c2 * 0.8, sqrt(saturate(1 - dot(c2, c2)))));
                    float v = NR(uv * 1.3 + seed + float2(time * 0.2, 0));
                    float d = dot(n, L3());
                    col = Ramp(v + (1 - p3) * _VolK * d);
                    if (p3 < 0.5) col = Cel(col, d, uv * 1.7 + seed); // chấm toé nổi khối; vũng (phẳng) giữ dải vân
                    col = dd < p2 ? _ColFoam.rgb : col;
                    foamy = dd < p2 ? 1 : 0;
                }
                else if (mode == 3) // ---------------- QUẠT (vương miện ngửa)
                {
                    float2 q = i.uv0.xy;
                    float r = length(q);
                    float th = atan2(q.x, q.y);
                    float u = th / max(p2, 0.05) * 0.5 + 0.5;
                    float v = (r - p4) / max(1 - p4, 0.05);
                    a = Cover(min(min(u, 1 - u) * 6, min(v, 1 - v) * 6));
                    float m = Mask(p1, float2(frac(u * p3 + seed), v));
                    float nn = saturate((NG(float2(u * 2 + seed, v * 0.8)) - 0.3) / 0.4);
                    float vv = m * (0.55 + 0.45 * nn);
                    float dd = vv - thr;
                    a *= Cover(dd + (NB(q * 1.9 + seed) - 0.5) * 0.03);
                    // mỗi ngón là một trụ dọc bán kính: pháp tuyến ngang theo vị trí trong ngón (frac của ô lặp) → mép ngón tối / sáng
                    float fu = frac(u * p3 * 7 + seed) * 2 - 1;
                    float3 n = normalize(float3(sin(th) * 0.6 + fu * 0.5, cos(th) * 0.45, 0.6));
                    float w = NR(float2(u * 3 + seed, v * 1.2 - time * 0.8));
                    float d = dot(n, L3());
                    col = Cel(Ramp(w + _VolK * d), d, q * 1.4 + seed);
                    col = dd < 0.05 ? _ColFoam.rgb : col;
                    foamy = (dd < 0.05 || d > _Hi) ? 1 : 0;
                }
                else if (mode == 4) // ---------------- VÀNH loang trên đất
                {
                    float2 q = i.uv0.xy;
                    float r = length(q);
                    float u = atan2(q.y, q.x) / 6.2832 + 0.5;
                    float v = (r - p2) / max(1 - p2, 0.05);
                    a = Cover(min(v, 1 - v) * 8);
                    a *= p4 > 0.5 ? Cover(-q.y * 20) : (p4 < -0.5 ? Cover(q.y * 20) : 1);
                    float m = Mask(p1, float2(frac(u * p3 + seed), v * 0.91));
                    float nn = saturate((NG(float2(u * 4 + seed, v)) - 0.3) / 0.4);
                    float vv = m * (0.35 + 0.65 * nn);
                    float dd = vv - thr;
                    a *= Cover(dd);
                    float w = NR(float2(u * 6 + seed, v * 1.3 - time * 0.6));
                    col = Ramp(w + _VolK * (0.6 - v));
                    col = v > 0.72 ? _ColShade.rgb : col; // mép ngoài vành tối hơn: vành có bề dày
                    col = dd < 0.035 ? _ColFoam.rgb : col;
                    foamy = dd < 0.035 ? 1 : 0;
                }
                else if (mode == 6) // ---------------- FLIPBOOK của gói (giá trị → dải cel của game)
                {
                    float4 A = tex2D(_FbTex, i.uv0.xy), B = tex2D(_FbTex, i.uv0.zw);
                    float2 va = p2 < 0.5 ? A.rg : A.ba, vb = p2 < 0.5 ? B.rg : B.ba;
                    float v = lerp(va.x, vb.x, thr), al = lerp(va.y, vb.y, thr);
                    float2 sp = i.wpos.xy / 160 + seed;
                    // mép cắt sắc; mờ dần = ngưỡng mép dâng (ăn mòn từ chỗ mỏng như gói tan theo alpha hạt)
                    float cut = p1 + (1 - i.color.a) * (0.95 - p1);
                    a = Cover(al - cut + (NB(sp) - 0.5) * 0.05);
                    float vv = v + p3 + (NB(sp * 1.7) - 0.5) * 0.09;
                    col = vv < _FbStops.x ? _ColShade.rgb : (vv < _FbStops.y ? _ColDeep.rgb : (vv < _FbStops.z ? _ColBody.rgb : _ColFoam.rgb));
                    foamy = vv >= _FbStops.z ? 1 : 0;
                    if (p4 > 1.5) { col = _ColFoam.rgb; foamy = 1; }
                    else if (p4 > 0.5) col = vv >= _FbStops.z ? _ColBody.rgb : (vv < _FbStops.y ? _ColShade.rgb : _ColDeep.rgb); // nền đất: phẳng, tối hơn
                    a *= saturate(i.color.a * 3); // gần hết đời: tắt hẳn (không còn lõi lấm tấm)
                    i.color.a = 1; // độ hiện đã vào ngưỡng mép
                }
                else if (mode == 7) // ---------------- ỐNG TIA kiểu Water Laser (vỏ / lõi / vệt bọt trôi), vân sắc kéo dài theo thân
                {
                    float x = i.uv0.x, ac = i.uv0.y;
                    float sc = p1;
                    float s = tex2D(_VetTex, float2(x * 0.075 - time * sc * 0.5, ac * 0.36 + seed)).r;  // vân nước sắc, kéo dài dọc ống
                    float s2 = tex2D(_VetTex, float2(x * 0.11 - time * sc * 0.7 + 0.37, ac * 0.3 - seed)).r;
                    float rag = (tex2D(_VetTex, float2(x * 0.42 - time * sc * 0.8, seed * 1.7)).b - 0.5);
                    float nz = sqrt(saturate(1 - ac * ac));
                    float d = ac * p4 + nz * 0.5;
                    if (p2 < 0.5) // vỏ ngoài: mép rách gợn trôi, lam sâu → lam, vệt sáng dọc theo pháp tuyến
                    {
                        a = Cover(1 - abs(ac) - rag * 0.22);
                        float w = nz * 0.75 + (s - 0.5) * 0.35 + d * 0.2;                      // trụ: giữa sáng, hai mép lam sâu → tối
                        col = w < 0.42 ? _ColShade.rgb : (w < 0.66 ? _ColDeep.rgb : _ColBody.rgb);
                        col = abs(ac) > 0.84 - rag * 0.16 ? _ColShade.rgb : col;
                    }
                    else if (p2 < 1.5) // lõi sáng: lam sáng, sọc bọt theo vân trôi
                    {
                        a = Cover(1 - abs(ac) - rag * 0.12);
                        float w = nz * 0.5 + s2 * 0.55 + d * 0.15;
                        col = w < 0.5 ? _ColDeep.rgb : (w < 0.82 ? _ColBody.rgb : _ColFoam.rgb);
                        foamy = w >= 0.82 ? 1 : 0;
                    }
                    else if (p2 < 2.5) // vệt bọt trôi (sọc trắng chạy dọc thân)
                    {
                        a = Cover(1 - abs(ac) - 0.15) * Cover(s2 - 0.68);
                        col = _ColFoam.rgb;
                        foamy = 1;
                    }
                    else // vỏ mỏng rách: mảng lam sâu loang lổ (lớp xoắn ngoài cùng)
                    {
                        a = Cover(1 - abs(ac) - rag * 0.3) * Cover(s - 0.3) * 0.85;
                        col = s > 0.8 ? _ColBody.rgb : _ColDeep.rgb;
                    }
                    if (thr > 0.001) a *= Cover(tex2D(_VetTex, float2(x * 0.5 + seed, ac * 0.5)).b - thr); // vỡ / tan
                }
                else // ---------------- CHẤM (giọt): nửa dưới phải tối, chấm sáng trên trái
                {
                    float2 p = i.uv0.xy;
                    a = Cover(1 - length(p));
                    col = p1 < 0.5 ? _ColDeep.rgb : (p1 < 1.5 ? _ColBody.rgb : _ColFoam.rgb);
                    float d = dot(float3(p, sqrt(saturate(1 - dot(p, p)))), L3());
                    col = (p1 < 1.5 && d < 0.1) ? _ColShade.rgb : col;
                    col = (p1 < 1.5 && d > 0.8) ? _ColFoam.rgb : col;
                }
                // VÂN CHÌ vẽ tay theo toạ độ màn hình (bọt nhạt hơn)
                float h = tex2D(_MainTex, i.wpos.xy / _HatchPx).a;
                col *= lerp(1, h, _Hatch * (1 - 0.6 * foamy));
                fixed4 o = fixed4(col * i.color.rgb, a * i.color.a);
                #ifdef UNITY_UI_CLIP_RECT
                o.a *= UnityGet2DClipping(i.wpos.xy, _ClipRect);
                #endif
                #ifdef UNITY_UI_ALPHACLIP
                clip(o.a - 0.001);
                #endif
                return o;
            }
            ENDCG
        }
    }
}
