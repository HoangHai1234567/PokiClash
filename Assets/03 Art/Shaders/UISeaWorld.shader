// Biển mở chung của sảnh, Nhà, đảo Casino và chuyến tàu (App/SeaAnchor.cs): ảnh biển lát (_SeaTile = Islands/sanh_bien) lấy theo vị trí
// thế giới của điểm ảnh, gốc và cỡ ô là biến toàn cục _PokiSeaO (xy gốc thế giới, zw = 1 / cỡ ô thế giới) do SeaAnchor của màn hoặc chuyến
// tàu ghi; không dùng uv của Image, nên mọi lớp biển ở mọi canvas (cùng camera UI) là một mặt nước liền, không lộ đường nối.
// Màu Image (DayNight làm tối biển về đêm) nhân vào như ảnh thường.
Shader "PokiClash/UISeaWorld"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _SeaTile ("Ảnh biển lát (Islands/sanh_bien)", 2D) = "white" {}

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
                float4 worldPosition : TEXCOORD1;
                float2 wpos : TEXCOORD2;
                UNITY_VERTEX_OUTPUT_STEREO
            };

            sampler2D _SeaTile;
            fixed4 _Color;
            float4 _ClipRect;
            float4 _PokiSeaO; // toàn cục: xy gốc thế giới, zw = 1 / cỡ ô thế giới

            v2f vert(appdata_t v)
            {
                v2f OUT;
                UNITY_SETUP_INSTANCE_ID(v);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);
                OUT.worldPosition = v.vertex;
                OUT.vertex = UnityObjectToClipPos(v.vertex);
                OUT.wpos = mul(unity_ObjectToWorld, v.vertex).xy;
                OUT.color = v.color * _Color;
                return OUT;
            }

            fixed4 frag(v2f IN) : SV_Target
            {
                float2 tuv = (IN.wpos - _PokiSeaO.xy) * _PokiSeaO.zw;
                // lặp theo frac, lấy mip theo uv liền để khỏi lộ đường nối ô (như UIHomeSea)
                half4 color = tex2Dgrad(_SeaTile, frac(tuv), ddx(tuv), ddy(tuv));
                color.a = 1;
                color *= IN.color;

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
