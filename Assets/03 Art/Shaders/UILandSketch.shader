// Bản phác chì của vùng boss chưa mở trên đảo vùng đất (ZoneSceneLand; người dùng 2026-11-18: "kết hợp cả A và B, mây tan ra, có bút chì
// vào tô màu section mới"; phủ đen trước đó bị chê). Ảnh này trùng khung ảnh đảo (cùng sprite, cùng uv), nằm ngay trên ảnh đảo, dưới hiệu
// ứng, sáng tối, cờ, tướng; mây phủ nằm trên cùng. Chỗ thuộc vùng chưa mở (trường vùng _SecTex: R = chỉ số vùng × 25 làm mềm, G = đất)
// hiện bản phác dựng từ chính ảnh đảo (cùng công thức tờ xem trước ArtGen/Islands/land_thuy/m0/xem_khoa.py): nét mực nâu theo độ tối cục
// bộ và nét viền sẵn có, phần tô thành giấy kem có vân chì gạch chéo theo độ đậm, hạt giấy. Ngoài vùng khoá trong suốt.
// Biến toàn cục (ZoneSceneLand đặt): _PokiLandOpened = số vùng đã mở. Bút chì tô màu vùng vừa mở: _PokiLandRevealSec (vùng k, -1: tắt),
// _PokiLandRevealN, _PokiLandReveal[i] (xy: tâm vệt tô theo uv ảnh đảo, z: bán kính theo bề ngang ảnh), _PokiLandRevealFade (0..1: tô
// nốt phần còn lại của vùng k). Project màu Linear: tính trên giá trị gamma rồi đổi lại (đúng như tờ xem trước).
// Tô bằng bút chì màu như màn mở khoá tướng (người dùng 2026-11-27: "phần tô màu section đảo khi unlock làm giống với phần tô màu khi
// unlock tướng", cùng công thức với UIPencilDraw): _PokiLandUseCover = 1 thì bỏ vệt tròn, _PokiLandCover là ảnh phủ trải trên khung
// vùng _PokiLandCoverBox (uv ảnh đảo: x, y, rộng, cao), mỗi kênh RGBA là chỗ bút của một nhóm màu (_PokiLandC0.._C3, gamma, w = 1 nếu
// có; Core/CrayonPlan) đã gạch qua. Mỗi điểm lấy kênh của nhóm có màu gần nhất nên màu không lem sang vùng khác; nét mực, mảng tối (dưới
// _PokiLandDarkL) bút nào qua cũng tô. Vệt sáp có vân chéo và hạt giấy, lực nhẹ thì còn lộ bản phác.
Shader "PokiClash/UILandSketch"
{
    Properties
    {
        [PerRendererData] _MainTex ("Ảnh đảo", 2D) = "white" {}
        _SecTex ("Trường vùng (R: vùng × 25, G: đất)", 2D) = "black" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _Paper ("Màu giấy", Color) = (0.955, 0.925, 0.855, 1)
        _Ink ("Màu mực", Color) = (0.36, 0.27, 0.20, 1)
        _Hatch ("Tần số gạch chì (theo điểm ảnh ảnh đảo)", Float) = 0.42
        _Tap ("Khoảng lấy mẫu dò nét (điểm ảnh)", Float) = 3
        _StencilComp ("Stencil Comparison", Float) = 8
        _Stencil ("Stencil ID", Float) = 0
        _StencilOp ("Stencil Operation", Float) = 0
        _StencilWriteMask ("Stencil Write Mask", Float) = 255
        _StencilReadMask ("Stencil Read Mask", Float) = 255
        _ColorMask ("Color Mask", Float) = 15
    }

    SubShader
    {
        Tags { "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent" "PreviewType"="Plane" "CanUseSpriteAtlas"="True" }
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
            Name "Default"
        CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma target 3.0
            #include "UnityCG.cginc"
            #include "UnityUI.cginc"
            #pragma multi_compile_local _ UNITY_UI_CLIP_RECT

            struct appdata_t { float4 vertex : POSITION; float4 color : COLOR; float2 texcoord : TEXCOORD0; UNITY_VERTEX_INPUT_INSTANCE_ID };
            struct v2f { float4 vertex : SV_POSITION; fixed4 color : COLOR; float2 uv : TEXCOORD0; float4 worldPosition : TEXCOORD1; UNITY_VERTEX_OUTPUT_STEREO };

            sampler2D _MainTex, _SecTex;
            float4 _MainTex_TexelSize;
            fixed4 _Color, _Paper, _Ink;
            float _Hatch, _Tap;
            float4 _ClipRect;
            float _PokiLandOpened, _PokiLandRevealSec, _PokiLandRevealN, _PokiLandRevealFade;
            float4 _PokiLandReveal[24];
            sampler2D _PokiLandCover;
            float4 _PokiLandCoverBox, _PokiLandC0, _PokiLandC1, _PokiLandC2, _PokiLandC3;
            float _PokiLandUseCover, _PokiLandDarkL;

            v2f vert(appdata_t v)
            {
                v2f OUT;
                UNITY_SETUP_INSTANCE_ID(v);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);
                OUT.worldPosition = v.vertex;
                OUT.vertex = UnityObjectToClipPos(OUT.worldPosition);
                OUT.uv = v.texcoord;
                OUT.color = v.color * _Color;
                return OUT;
            }

            float Lum(float2 uv) { return dot(LinearToGammaSpace(tex2D(_MainTex, uv).rgb), float3(0.3, 0.59, 0.11)); }
            float Hash(float2 p) { return frac(sin(dot(p, float2(12.9898, 78.233))) * 43758.5453); }

            // nhiễu giá trị của vân sáp (cùng hàm với UIPencilDraw để vệt sáp trông như màn mở khoá tướng)
            float HashW(float2 p)
            {
                p = frac(p * float2(123.34, 456.21));
                p += dot(p, p + 45.32);
                return frac(p.x * p.y);
            }

            float VNoise(float2 p)
            {
                float2 i = floor(p), f = frac(p);
                f = f * f * (3 - 2 * f);
                return lerp(lerp(HashW(i), HashW(i + float2(1, 0)), f.x), lerp(HashW(i + float2(0, 1)), HashW(i + 1), f.x), f.y);
            }

            // bình phương khoảng cách màu tới nhóm (nhóm không dùng: rất xa)
            float D(float3 g, float4 c) { float3 d = g - c.rgb; return c.w > 0.5 ? dot(d, d) : 1e4; }

            fixed4 frag(v2f IN) : SV_Target
            {
                float2 uv = IN.uv;
                float4 f = tex2D(_SecTex, uv);
                float v = f.r * (255.0 / 25.0);
                // vùng chỉ số >= số vùng đã mở thì khoá (trường làm mềm: mép phác / màu mềm)
                float lk = smoothstep(_PokiLandOpened - 0.72, _PokiLandOpened - 0.28, v);
                float2 px = uv * _MainTex_TexelSize.zw;
                float2 pix = uv / max(fwidth(uv), 1e-7); // toạ độ điểm ảnh màn hình (vân sáp dày đều theo màn như bên tướng)
                if (_PokiLandRevealSec >= 0)
                {
                    float k = _PokiLandRevealSec;
                    float mk = 1 - smoothstep(k + 0.28, k + 0.72, v); // thuộc vùng k (vùng sau vẫn khoá)
                    float carve = _PokiLandRevealFade;
                    if (_PokiLandUseCover > 0.5)
                    {
                        // bút chì màu: kênh của nhóm màu gần nhất; nét mực, mảng tối lấy kênh lớn nhất
                        float2 lu = (uv - _PokiLandCoverBox.xy) / max(_PokiLandCoverBox.zw, 1e-5);
                        float inb = step(0, lu.x) * step(0, lu.y) * step(lu.x, 1) * step(lu.y, 1);
                        float4 cv = tex2D(_PokiLandCover, saturate(lu)) * inb;
                        float3 gm = LinearToGammaSpace(tex2D(_MainTex, uv).rgb);
                        float4 d = float4(D(gm, _PokiLandC0), D(gm, _PokiLandC1), D(gm, _PokiLandC2), D(gm, _PokiLandC3));
                        float m = min(min(d.x, d.y), min(d.z, d.w));
                        float4 sel = step(d, m.xxxx);
                        float own = max(max(cv.x * sel.x, cv.y * sel.y), max(cv.z * sel.z, cv.w * sel.w));
                        float anyc = max(max(cv.x, cv.y), max(cv.z, cv.w));
                        float kc = dot(gm, float3(0.299, 0.587, 0.114)) < _PokiLandDarkL ? anyc : own;
                        // vân sáp: sợi chéo theo hướng gạch + hạt giấy; lực nhẹ, mép vệt thì còn lộ bản phác
                        float2 q = float2(dot(pix, float2(0.82, 0.57)), dot(pix, float2(-0.57, 0.82)));
                        float fiber = VNoise(float2(q.x / 7.0, q.y / 1.6));
                        float tooth = VNoise(pix / 2.2 + 17.0);
                        float lay = saturate((kc - fiber * 0.45) * 2.6);
                        carve = max(carve, lay * (0.84 + 0.16 * tooth));
                    }
                    else
                    {
                        float asp = _MainTex_TexelSize.w / _MainTex_TexelSize.z;
                        float wob = (sin(px.x * 0.031 + px.y * 0.017) + sin(px.x * 0.013 - px.y * 0.041)) * 0.0045; // mép tô như nét chì
                        for (int i = 0; i < 24; i++)
                        {
                            if (i >= (int)_PokiLandRevealN) break;
                            float4 r = _PokiLandReveal[i];
                            float2 dd = (uv - r.xy) * float2(1, asp);
                            carve = max(carve, 1 - smoothstep(r.z * 0.72, r.z, length(dd) + wob));
                        }
                    }
                    lk *= 1 - mk * carve;
                }
                float a = f.g * lk * IN.color.a;
                #ifdef UNITY_UI_CLIP_RECT
                a *= UnityGet2DClipping(IN.worldPosition.xy, _ClipRect);
                #endif
                if (a < 0.002) return fixed4(0, 0, 0, 0);

                // bản phác: nét mực (tối hơn xung quanh, hoặc nét viền đậm sẵn có), giấy có vân chì theo độ đậm, hạt giấy
                float2 t = _MainTex_TexelSize.xy * _Tap;
                float g = Lum(uv);
                float gm = (Lum(uv + float2(t.x, 0)) + Lum(uv - float2(t.x, 0)) + Lum(uv + float2(0, t.y)) + Lum(uv - float2(0, t.y))
                    + Lum(uv + t * 0.7) + Lum(uv - t * 0.7) + Lum(uv + float2(t.x, -t.y) * 0.7) + Lum(uv + float2(-t.x, t.y) * 0.7)) * 0.125;
                float ink = saturate((gm - g - 0.025) * 14);
                ink = max(ink, saturate((0.3 - g) * 6));
                float hatch = step(0.55, sin((px.x + px.y * 1.4) * _Hatch)) * min(saturate((0.85 - g) * 1.1), 0.7);
                float grain = Hash(floor(px * 0.5));
                float3 paper = LinearToGammaSpace(_Paper.rgb);
                float3 inkc = LinearToGammaSpace(_Ink.rgb);
                float3 fill = paper * (1 - 0.32 * hatch) * (0.97 + 0.06 * grain);
                float3 col = fill * (1 - ink * 0.85) + inkc * ink * 0.85;
                return fixed4(GammaToLinearSpace(col) * IN.color.rgb, a);
            }
        ENDCG
        }
    }
}
