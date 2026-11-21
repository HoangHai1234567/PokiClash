// Vật đang chọn ở màn Nhà (người dùng 2026-11-22: "chọn vật chưa thể hiện kĩ là vừa chọn ... hơi sáng nhẹ bằng shader").
// Như UIPlain (ảnh thường × màu Image) rồi kéo màu về phía trắng giấy theo độ sáng _HomeSel (biến toàn cục, HomeScene đặt mỗi khung:
// loé lên lúc vừa chọn rồi thở nhẹ trong lúc còn chọn). Chỉ sáng trong hình (theo alpha của ảnh), không viền, không quầng
// (người dùng ghét quầng, 2026-11-20). Kéo về trắng (screen) chứ không cộng nên nét mực nâu vẫn rõ, màu chì sáp không cháy.
Shader "PokiClash/UIHomeSelect"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _Lift ("Sáng tối đa (về trắng)", Range(0,1)) = 0.34
        _Warm ("Ấm (màu sáng)", Color) = (1, 0.97, 0.88, 1)

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
            fixed4 _Color;
            fixed4 _TextureSampleAdd;
            float4 _ClipRect;
            float _Lift;
            fixed4 _Warm;
            float _HomeSel; // toàn cục (HomeScene): 0 = như thường, 1 = loé lúc vừa chọn

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
                half4 color = (tex2D(_MainTex, IN.texcoord) + _TextureSampleAdd) * IN.color;
                // kéo về trắng ấm: vùng tối (nét mực) sáng ít hơn vùng tô (nhân thêm độ sáng) để viền vẫn đọc được
                half lum = dot(color.rgb, half3(0.299, 0.587, 0.114));
                half k = saturate(_HomeSel) * _Lift * lerp(0.45, 1.0, lum);
                color.rgb = lerp(color.rgb, _Warm.rgb, k);

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
