// Chỗ phát sáng của đảo trên bản đồ sảnh về đêm (người dùng 2026-11-20: "buổi đêm các đảo sáng lên", chọn cách mặt nạ phát sáng).
// Ảnh là phần đảo vốn là nguồn sáng (dung nham, mặt trời vàng, chuông, xoáy nước, đèn: ArtGen/Islands/sanh_moi/den_dem.py), vẽ TRÊN lớp
// nhuộm đêm nên giữ màu gốc giữa cảnh đã tối; cộng thêm sáng theo màu của Image (màu hệ), chập chờn bằng nhiễu trôi lên; không quầng nhoè.
// Độ đêm đọc biến toàn cục _PokiNight (DayNight đặt mỗi khung theo giờ máy): ban ngày tắt hẳn, chạng vạng hiện dần.
// Trộn premultiplied: phần màu gốc trộn thường, phần sáng thêm vượt alpha nên thành cộng sáng.
Shader "PokiClash/UIIslandEmit"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _Boost ("Sáng thêm", Float) = 0.6
        _Shimmer ("Chập chờn", Range(0,1)) = 0.45
        _NoiseScale ("Cỡ vệt chập chờn", Float) = 7
        _Speed ("Tốc độ trôi", Float) = 0.5
        _NightGain ("Hệ số đêm (sáng đủ sớm hơn)", Float) = 1.6

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
            #pragma target 2.0

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
            fixed4 _Color;
            float4 _ClipRect;
            float _Boost, _Shimmer, _NoiseScale, _Speed, _NightGain;
            float _PokiNight; // toàn cục (DayNight)

            float hash21(float2 p) { return frac(sin(dot(p, float2(127.1, 311.7))) * 43758.5453); }
            float vnoise(float2 p)
            {
                float2 i = floor(p), f = frac(p);
                float2 u = f * f * (3.0 - 2.0 * f);
                return lerp(lerp(hash21(i), hash21(i + float2(1, 0)), u.x), lerp(hash21(i + float2(0, 1)), hash21(i + 1), u.x), u.y);
            }

            v2f vert(appdata_t v)
            {
                v2f OUT;
                UNITY_SETUP_INSTANCE_ID(v);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);
                OUT.worldPosition = v.vertex;
                OUT.vertex = UnityObjectToClipPos(OUT.worldPosition);
                OUT.texcoord = v.texcoord;
                OUT.color = v.color * _Color;
                return OUT;
            }

            fixed4 frag(v2f IN) : SV_Target
            {
                fixed4 tex = tex2D(_MainTex, IN.texcoord);
                float n = saturate(_PokiNight * _NightGain);
                n = n * n * (3.0 - 2.0 * n);
                // chập chờn: hai lớp nhiễu trôi lên, lệch hướng nhau
                float t = _Time.y * _Speed;
                float2 p = IN.texcoord * _NoiseScale;
                float s = vnoise(p + float2(0, -t)) * 0.65 + vnoise(p * 2.3 + float2(t * 0.7, -t * 1.6)) * 0.35;
                float flick = 1.0 + _Shimmer * (s * 2.0 - 1.0);
                float a = tex.a * n * IN.color.a;
                float3 rgb = tex.rgb + tex.rgb * IN.color.rgb * _Boost * flick;
                fixed4 o = fixed4(rgb * a, a);

                #ifdef UNITY_UI_CLIP_RECT
                o *= UnityGet2DClipping(IN.worldPosition.xy, _ClipRect);
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
