// Đuốc thắp trên các đảo bản đồ sảnh (người dùng 2026-11-20: "thêm những điểm sáng kiểu ngọn đuốc được thắp trên các đảo", chọn cách
// ngọn lửa bằng shader). Vẽ hết trong một ô chữ nhật (Image không ảnh), toạ độ tính theo bề ngang ô (ngang 1, cao _Aspect):
// - torch (màu Image.g = 1): cột gỗ + chậu sắt có nét mực nâu (luôn hiện, ban ngày là đuốc tắt), lửa giọt nước 3 bậc màu + nét mực đỏ
//   nâu, đung đưa theo nhiễu, nhảy khung 9 hình/giây cho giống vẽ tay; chạng vạng lửa nhú dần lên từ chậu;
// - lamp (màu Image.g = 0): chỉ đốm lửa trong đèn có sẵn trong tranh (đèn lồng, hải đăng);
// - vùng sáng quanh lửa: hai vòng tách bậc (không chuyển màu mượt), cộng sáng ấm, phập phồng theo lửa.
// Màu Image.r = hạt giống lệch nhịp từng đuốc, Image.a = độ hiện. Độ đêm đọc _PokiNight (DayNight đặt theo giờ máy).
// Chân đuốc (torch) ở y = 0.22, tâm lửa đèn (lamp) ở y = 0.62 (đơn vị bề ngang ô): menu đặt pivot theo đó.
Shader "PokiClash/UITorch"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Aspect ("Cao / ngang của ô", Float) = 1.4
        _Ink ("Nét mực", Color) = (0.23,0.13,0.08,1)
        _FlameInk ("Nét lửa", Color) = (0.45,0.12,0.04,1)
        _Outer ("Lửa ngoài", Color) = (0.98,0.42,0.10,1)
        _Mid ("Lửa giữa", Color) = (1.0,0.76,0.20,1)
        _Core ("Lõi lửa", Color) = (1.0,0.96,0.72,1)
        _Halo ("Màu vùng sáng", Color) = (1.0,0.70,0.32,1)
        _HaloA ("Độ sáng vùng sáng", Float) = 0.13
        _InkPx ("Nét mực (px màn)", Float) = 1.6
        _NightGain ("Hệ số đêm (thắp sớm hơn)", Float) = 1.6

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
        Tags
        {
            "Queue"="Transparent"
            "IgnoreProjector"="True"
            "RenderType"="Transparent"
            "PreviewType"="Plane"
            "CanUseSpriteAtlas"="True"
        }

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
        Blend One OneMinusSrcAlpha
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
            #pragma multi_compile_local _ UNITY_UI_ALPHACLIP

            struct appdata_t
            {
                float4 vertex   : POSITION;
                float4 color    : COLOR;
                float2 texcoord : TEXCOORD0;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };

            struct v2f
            {
                float4 vertex   : SV_POSITION;
                float4 color    : COLOR;
                float2 texcoord : TEXCOORD0;
                float4 worldPosition : TEXCOORD1;
                UNITY_VERTEX_OUTPUT_STEREO
            };

            float4 _ClipRect, _Ink, _FlameInk, _Outer, _Mid, _Core, _Halo;
            float _Aspect, _HaloA, _InkPx, _NightGain;
            float _PokiNight; // toàn cục (DayNight)

            float hash21(float2 p) { return frac(sin(dot(p, float2(127.1, 311.7))) * 43758.5453); }
            float vnoise(float2 p)
            {
                float2 i = floor(p), f = frac(p);
                float2 u = f * f * (3.0 - 2.0 * f);
                return lerp(lerp(hash21(i), hash21(i + float2(1, 0)), u.x), lerp(hash21(i + float2(0, 1)), hash21(i + 1), u.x), u.y);
            }

            // nửa bề ngang của giọt lửa ở độ cao y (đáy tròn bán kính r, vuốt nhọn tới đỉnh h); < 0 ngoài khoảng
            float flameHalf(float y, float r, float h)
            {
                if (y < 0 || y > h) return -1;
                if (y < r) return sqrt(max(0, r * r - (r - y) * (r - y)));
                return r * pow(saturate(1.0 - (y - r) / max(h - r, 1e-4)), 1.25);
            }

            // khoảng cách (âm: bên trong) tới giọt lửa, đo ngang, cộng phần vượt đáy / đỉnh
            float flameDist(float2 q, float r, float h)
            {
                float hw = flameHalf(clamp(q.y, 0, h), r, h);
                float d = abs(q.x) - max(hw, 0);
                return max(d, max(-q.y, q.y - h));
            }

            void over(inout float4 dst, float3 c, float a)
            {
                dst.rgb = c * a + dst.rgb * (1 - a);
                dst.a = a + dst.a * (1 - a);
            }

            // tô hình có nét mực: d < 0 bên trong, nét dày ink (đơn vị ô), px: cỡ 1 px màn
            void shape(inout float4 dst, float d, float3 fill, float3 ink, float w, float px)
            {
                float outA = saturate(0.5 - (d - w) / px);  // cả nét lẫn ruột
                float inA = saturate(0.5 - d / px);
                over(dst, lerp(ink, fill, inA), outA);
            }

            v2f vert(appdata_t v)
            {
                v2f OUT;
                UNITY_SETUP_INSTANCE_ID(v);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);
                OUT.worldPosition = v.vertex;
                OUT.vertex = UnityObjectToClipPos(OUT.worldPosition);
                OUT.texcoord = v.texcoord;
                OUT.color = v.color;
                return OUT;
            }

            float4 frag(v2f IN) : SV_Target
            {
                float seed = IN.color.r;
                bool torch = IN.color.g > 0.5;
                float2 P = float2(IN.texcoord.x - 0.5, IN.texcoord.y * _Aspect);
                float px = max(fwidth(P.x), 1e-5);
                float w = _InkPx * px;

                float n = saturate(_PokiNight * _NightGain);
                n = n * n * (3.0 - 2.0 * n);
                // nhảy khung kiểu vẽ tay, mỗi đuốc lệch nhịp
                float tq = floor(_Time.y * 9.0 + seed * 7.0) / 9.0;
                float fl = vnoise(float2(tq * 3.1, seed * 17.0));        // 0..1
                float fl2 = vnoise(float2(tq * 5.3 + 11.0, seed * 29.0));

                float4 S = float4(0, 0, 0, 0);
                float2 c; // tâm vùng sáng
                float haloR;

                if (torch)
                {
                    // cột gỗ (thon dần xuống chân), sọc sáng bên trái
                    float y0 = 0.22, y1 = 0.50;
                    float k = saturate((P.y - y0) / (y1 - y0));
                    float hw = lerp(0.017, 0.025, k);
                    float dPole = max(abs(P.x) - hw, max(y0 - P.y, P.y - y1));
                    float3 wood = (P.x < -hw * 0.25) ? float3(0.72, 0.47, 0.26) : float3(0.55, 0.33, 0.18);
                    shape(S, dPole, wood, _Ink.rgb, w, px);

                    // lửa: đáy trong chậu, nhú lên theo độ đêm
                    float grow = n;
                    float base = 0.53;
                    float h = 0.25 * (0.88 + 0.24 * fl) * grow;
                    float r = 0.068 * (0.92 + 0.12 * fl2) * lerp(0.6, 1.0, grow);
                    float2 q = P - float2(0, base);
                    float up = saturate(q.y / max(h, 1e-3));
                    q.x -= (vnoise(float2(q.y * 11.0 + seed * 5.0, tq * 4.0)) - 0.5) * 0.07 * up;
                    q.x -= sin(tq * 2.3 + seed * 6.3) * 0.025 * up * up;
                    if (grow > 0.01)
                    {
                        shape(S, flameDist(q, r, h), _Outer.rgb, _FlameInk.rgb, w * 0.9, px);
                        float2 q2 = q - float2(0, 0.012);
                        float in2 = saturate(0.5 - flameDist(q2, r * 0.62, h * 0.66) / px);
                        over(S, _Mid.rgb, in2);
                        float2 q3 = q - float2(0, 0.02);
                        float in3 = saturate(0.5 - flameDist(q3, r * 0.34, h * 0.38) / px);
                        over(S, _Core.rgb, in3);
                    }

                    // chậu sắt loe miệng, viền miệng sáng hơn (che chân lửa)
                    float b0 = 0.48, b1 = 0.565;
                    float kb = saturate((P.y - b0) / (b1 - b0));
                    float bw = lerp(0.034, 0.074, kb * kb * 0.4 + kb * 0.6);
                    float dBowl = max(abs(P.x) - bw, max(b0 - P.y, P.y - b1));
                    float3 iron = P.y > b1 - 0.018 ? float3(0.50, 0.40, 0.33) : float3(0.33, 0.27, 0.25);
                    shape(S, dBowl, iron, _Ink.rgb, w, px);

                    c = float2(0, base + h * 0.42);
                    haloR = 0.36;
                }
                else
                {
                    // đốm lửa trong đèn có sẵn: bầu dục ấm, phập phồng
                    c = float2(0, 0.62);
                    float rr = (0.026 + 0.008 * fl) * n;
                    float d = length((P - c) / float2(0.8, 1.0)) - rr;
                    over(S, lerp(_Mid.rgb, _Core.rgb, 0.6), saturate(0.5 - d / px) * step(0.01, n));
                    haloR = 0.26;
                }

                // vùng sáng hai bậc, mép hơi lượn, to nhỏ theo lửa
                float R = haloR * (0.94 + 0.12 * fl) * n;
                float2 dv = P - c;
                float ang = atan2(dv.y, dv.x);
                float dist = length(dv) * (1.0 + 0.04 * (vnoise(float2(ang * 2.0 + seed * 9.0, tq * 1.5)) - 0.5));
                float b1a = saturate(0.5 - (dist - R) / (px * 1.5));
                float b2a = saturate(0.5 - (dist - R * 0.58) / (px * 1.5));
                float haloA = (b1a + b2a) * _HaloA * (0.85 + 0.3 * fl) * n;
                float3 halo = _Halo.rgb * haloA;

                float4 o = float4(S.rgb + halo * (1 - S.a), S.a);
                o *= IN.color.a;

                #ifdef UNITY_UI_CLIP_RECT
                o *= UnityGet2DClipping(IN.worldPosition.xy, _ClipRect);
                #endif
                #ifdef UNITY_UI_ALPHACLIP
                clip(o.a + dot(o.rgb, 1) - 0.001);
                #endif
                return o;
            }
        ENDCG
        }
    }
}
