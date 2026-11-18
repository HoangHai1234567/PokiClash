// Sóng đập bờ trên ảnh nền đảo vùng đất (GD_Claude/18, bản thử ArtGen/Islands/land_thuy/concept/song_thu.html).
// _DistTex (ArtGen/Islands/land_thuy/m0/build_land.py): R = khoảng cách tới bờ × 4 (px ảnh gốc, trần 64), G = chỗ được vẽ sóng
// (biển ngoài khơi, không đè mây, thuyền). Vạch bọt trắng có viền mực chạy dần vào bờ, lệch theo nhiễu; sát bờ nước tràn lên rút ra
// theo nhịp; sóng lên cao nhất thì tung bụi nước. Tô phẳng, không quầng sáng (luật UI). Tính theo px ảnh gốc của _DistTex nên
// phóng ảnh nền bao nhiêu thì sóng to theo bấy nhiêu, khớp nét gạch của ảnh.
Shader "PokiClash/UIInkWater"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _DistTex ("Khoảng cách tới bờ (R), chỗ vẽ sóng (G)", 2D) = "black" {}
        _Period ("Khoảng cách hai vạch sóng (px ảnh gốc)", Float) = 22
        _Speed ("Tốc vạch sóng chạy vào (px ảnh gốc / giây)", Float) = 9
        _Reach ("Xa bờ nhất còn vạch sóng (px ảnh gốc)", Float) = 46
        _Wash ("Nước tràn lên bờ xa nhất (px ảnh gốc)", Float) = 14
        _Foam ("Độ đậm bọt", Range(0,1)) = 0.92
        _InkCol ("Màu viền mực vạch sóng", Color) = (0.16,0.42,0.62,1)

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
            fixed4 _Color;
            fixed4 _TextureSampleAdd;
            float4 _ClipRect;
            sampler2D _DistTex;
            float4 _DistTex_TexelSize;
            float _Period, _Speed, _Reach, _Wash, _Foam;
            fixed4 _InkCol;
            float _PokiNight; // toàn cục, DayNight đặt: 0 ngày, 1 đêm

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

            float h21(float2 q) { return frac(sin(dot(q, float2(127.1, 311.7))) * 43758.5453); }
            float vn(float2 q)
            {
                float2 i = floor(q), f = frac(q);
                f = f * f * (3.0 - 2.0 * f);
                return lerp(lerp(h21(i), h21(i + float2(1, 0)), f.x), lerp(h21(i + float2(0, 1)), h21(i + float2(1, 1)), f.x), f.y);
            }

            fixed4 frag(v2f IN) : SV_Target
            {
                half4 color = (tex2D(_MainTex, IN.texcoord) + _TextureSampleAdd) * IN.color;
                float2 m = tex2D(_DistTex, IN.texcoord).rg;
                if (m.g > 0.5)
                {
                    float t = _Time.y;
                    float d = m.r * 64.0;
                    float2 p = IN.texcoord * _DistTex_TexelSize.zw;    // px ảnh gốc
                    float n = (vn(p * 0.018 + float2(t * 0.04, 0)) - 0.5) * 14.0;
                    float f = frac((d + n + t * _Speed) / _Period);
                    float line_ = smoothstep(0.0, 0.04, f) * (1.0 - smoothstep(0.11, 0.19, f));
                    float ink = smoothstep(0.19, 0.22, f) * (1.0 - smoothstep(0.22, 0.28, f));
                    float fade = 1.0 - smoothstep(5.0, _Reach, d);
                    float br = (vn(p * 0.006) - 0.5) * 0.6;
                    float w = 0.5 + 0.5 * sin(t * 1.3 + vn(p * 0.009) * 6.283);   // nhịp đập bờ
                    float reach = 3.0 + w * (_Wash - 3.0);
                    float wash = 1.0 - smoothstep(reach - 1.5, reach + 1.5, d);
                    float washEdge = 1.0 - smoothstep(1.0, 3.2, abs(d - reach));
                    float hatch = 0.72 + 0.28 * step(0.5, frac((p.x + p.y) * 0.22));
                    float spray = step(0.9, h21(floor(p / 3.0) + floor(t * 9.0))) * (1.0 - smoothstep(0.0, 7.0, d)) * smoothstep(0.78, 1.0, w);
                    float foam = max(line_ * fade * (0.9 + br), max(wash * 0.72 * hatch, washEdge));
                    foam = max(foam, spray);
                    color.rgb = lerp(color.rgb, _InkCol.rgb, ink * fade * 0.45);
                    color.rgb = lerp(color.rgb, half3(0.985, 1.0, 1.0), saturate(foam) * _Foam);
                    // đêm (DayNight đặt _PokiNight): biển tối dần theo khoảng cách tới bờ, sát bờ giữ sáng: đảo nổi sáng giữa biển đêm
                    // DayCycle.SeaNight là màu sRGB: dự án render tuyến tính nên đổi sang tuyến tính, cho khớp biển lặp quanh đảo (màu Image)
                    half3 seaNight = half3(0.56, 0.62, 0.84);
                    #ifndef UNITY_COLORSPACE_GAMMA
                    seaNight = GammaToLinearSpace(seaNight);
                    #endif
                    color.rgb *= lerp(half3(1, 1, 1), seaNight, _PokiNight * smoothstep(4.0, 46.0, d));
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
