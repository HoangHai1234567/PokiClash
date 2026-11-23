// Nước chảy trên bản đồ sảnh (người dùng 2026-11-23: "nước suối vẫn hơi tĩnh, học Kingdom Rush 5"; ArtGen/Islands/sanh_moi/nuoc_dong.py).
// Ảnh phủ sanh_nuoc_<đảo> nằm đè đúng chỗ trên ảnh đảo: A = mặt nạ nước (RGB không dùng). Nét vẽ nền giữ nguyên, shader chỉ vẽ nét bọt
// chồng lên, như KR5:
// - sông (KR5 WavesRiver): vệt bọt trắng nằm ngang dòng trôi xuôi, đứt khúc, hiện rồi tan; viền lam đậm phía sau vệt (KR5: mép hiệu ứng
//   là màu đậm hơn của chính nó, không viền mực). Pha dải lấy từ _FlowTex (R, G = cos, sin của khoảng cách đi theo lòng nước / _Period)
//   nên vệt luôn nằm ngang dòng ở mọi khúc cong;
// - thác (B của _FlowTex = 1; KR5 thác: vệt sáng trôi xuống): vệt dọc trắng và lam đậm trôi nhanh xuống.
// Tô phẳng, không quầng sáng (luật UI). Công thức giữ khớp hàm shade() trong nuoc_dong.py (bản xem trước GIF).
Shader "PokiClash/UIFlowWater"
{
    Properties
    {
        [PerRendererData] _MainTex ("Ảnh phủ (A = mặt nạ nước)", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _FlowTex ("Trường dòng chảy: RG pha theo dòng, B thác", 2D) = "black" {}
        _Period ("Khoảng hai dải bọt sông (px ảnh nới)", Float) = 15
        _RiverSpeed ("Tốc vệt bọt sông (px ảnh nới / giây)", Float) = 13
        _FallSpeed ("Tốc vệt thác (px ảnh nới / giây)", Float) = 42
        _Scale ("px ảnh phủ / px ảnh nới", Float) = 2
        _Foam ("Độ đậm nét bọt", Range(0,1)) = 1
        _Deep ("Màu vệt lam đậm", Color) = (0.15,0.47,0.84,1)

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
                fixed4 color    : COLOR;
                float2 texcoord : TEXCOORD0;
                float4 worldPosition : TEXCOORD1;
                UNITY_VERTEX_OUTPUT_STEREO
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            float4 _MainTex_TexelSize;
            fixed4 _Color;
            fixed4 _TextureSampleAdd;
            float4 _ClipRect;
            sampler2D _FlowTex;
            float _Period, _RiverSpeed, _FallSpeed, _Scale, _Foam;
            fixed4 _Deep;

            v2f vert(appdata_t v)
            {
                v2f OUT;
                UNITY_SETUP_INSTANCE_ID(v);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);
                OUT.worldPosition = v.vertex;
                OUT.vertex = UnityObjectToClipPos(OUT.worldPosition);
                OUT.texcoord = TRANSFORM_TEX(v.texcoord, _MainTex);
                OUT.color = v.color * _Color;
                return OUT;
            }

            float h21(float2 q) { return frac(sin(q.x * 127.1 + q.y * 311.7) * 43758.5453); }
            float vn(float2 q)
            {
                float2 i = floor(q), f = frac(q);
                f = f * f * (3.0 - 2.0 * f);
                float a = h21(i), b = h21(i + float2(1, 0)), c = h21(i + float2(0, 1)), d = h21(i + float2(1, 1));
                return lerp(lerp(a, b, f.x), lerp(c, d, f.x), f.y);
            }

            fixed4 frag(v2f IN) : SV_Target
            {
                float mask = (tex2D(_MainTex, IN.texcoord).a + _TextureSampleAdd.a);
                if (mask < 0.01) discard;
                float3 fl = tex2D(_FlowTex, IN.texcoord).rgb;
                float ph = atan2(fl.g * 2.0 - 1.0, fl.r * 2.0 - 1.0) * 0.15915494;
                float fall = fl.b;
                float2 p = IN.texcoord * _MainTex_TexelSize.zw; // px ảnh phủ, y lên
                float t = _Time.y;
                float inner = smoothstep(0.55, 0.95, mask);

                // sông: dải bọt ngang dòng trôi xuôi, lệch pha theo nhiễu (cong, so le), đứt khúc theo nhiễu trôi chậm
                float k = ph - t * _RiverSpeed / _Period + (vn(p * 0.035) - 0.5) * 0.7;
                float band = frac(k);
                float stroke = smoothstep(0.0, 0.06, band) * (1.0 - smoothstep(0.13, 0.2, band));
                float under = smoothstep(0.2, 0.24, band) * (1.0 - smoothstep(0.24, 0.3, band));
                float dash = smoothstep(0.42, 0.52, vn(float2(p.x * 0.06 + 3.7, p.y * 0.06 - t * 0.35)));
                float rw = stroke * dash * inner * (1.0 - fall);
                float rd = under * dash * inner * (1.0 - fall) * 0.45;

                // thác: vệt dọc trắng / lam đậm trôi xuống (y lên nên cộng thời gian)
                float sy = p.y + t * _FallSpeed * _Scale;
                float n1 = vn(float2(p.x * 0.30, sy * 0.05));
                float n2 = vn(float2(p.x * 0.24 + 7.3, sy * 0.035 + 3.1));
                float fw = smoothstep(0.66, 0.70, n1) * fall * inner;
                float fd = (1.0 - smoothstep(0.26, 0.30, n2)) * fall * inner * 0.6;

                float aw = max(rw, fw);
                float ad = max(rd, fd) * (1.0 - aw);
                float a = saturate(aw + ad);
                half3 rgb = (half3(0.985, 1.0, 1.0) * aw + _Deep.rgb * ad) / max(a, 1e-4);
                half4 color = half4(rgb * IN.color.rgb, a * mask * _Foam * IN.color.a);

                #ifdef UNITY_UI_CLIP_RECT
                color.a *= UnityGet2DClipping(IN.worldPosition.xy, _ClipRect);
                #endif

                #ifdef UNITY_UI_ALPHACLIP
                clip(color.a - 0.001);
                #endif

                return color;
            }
        ENDCG
        }
    }
}
