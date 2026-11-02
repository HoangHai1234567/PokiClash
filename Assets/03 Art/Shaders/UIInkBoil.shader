// Nét mực rung cho UI (thay 3 filter SVG boil0..2 của bản web): dời UV theo texture nhiễu toàn cục _PokiNoise,
// 3 bộ dời thay nhau 6 lần mỗi giây; _PokiBoil = 0 thì đứng yên ở bộ đầu.
// _Encoded = 1: sprite vẽ bằng code (Sketch.cs) mã hoá kênh: R = độ sáng phần tô, G = mực, B = vùng gạch sáp, A = độ phủ.
// Màu tô lấy từ màu của Image, mực lấy từ _PokiInk, nên đổi màu nút không làm đổi màu viền.
Shader "PokiClash/UIInkBoil"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _Encoded ("Sprite mã hoá kênh (Sketch)", Float) = 1
        _BoilAmp ("Biên độ rung (texel)", Float) = 1.6

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
            float4 _MainTex_ST;
            float4 _MainTex_TexelSize;
            fixed4 _Color;
            fixed4 _TextureSampleAdd;
            float4 _ClipRect;
            float _Encoded;
            float _BoilAmp;

            sampler2D _PokiNoise;
            float _PokiBoil;
            fixed4 _PokiInk;

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

            fixed4 frag(v2f IN) : SV_Target
            {
                float set = _PokiBoil > 0.5 ? floor(fmod(_Time.y * 6.0, 3.0)) : 0.0;
                float2 n = tex2D(_PokiNoise, IN.worldPosition.xy / 56.0 + set * float2(0.37, 0.61)).rg * 2.0 - 1.0;
                float2 uv = IN.texcoord + n * _BoilAmp * _MainTex_TexelSize.xy;
                half4 t = tex2D(_MainTex, uv) + _TextureSampleAdd;

                half4 color;
                if (_Encoded > 0.5)
                {
                    half3 fill = IN.color.rgb * t.r;
                    // gạch sáp: B ~ 1 vệt sáng (-55°), B ~ 0,5 vệt tối mảnh
                    float s = frac(dot(IN.worldPosition.xy, float2(0.574, 0.819)) / 18.0);
                    half light = t.b > 0.75 ? step(s, 0.33) * 0.22 : 0.0;
                    half dark = (t.b > 0.25 && t.b <= 0.75) ? step(s, 0.22) * 0.07 : 0.0;
                    fill = lerp(fill, half3(1, 1, 1), light);
                    fill *= 1.0 - dark;
                    color.rgb = lerp(fill, _PokiInk.rgb, t.g);
                    color.a = t.a * IN.color.a;
                }
                else
                {
                    color = t * IN.color;
                }

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
