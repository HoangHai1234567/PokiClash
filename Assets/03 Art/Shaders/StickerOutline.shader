// Viền sticker cho tướng aola (bản dev): ảnh tướng render ra RenderTexture, shader lấy mẫu độ phủ 8 hướng để vẽ
// viền trắng rồi viền mực bên ngoài (thay cho drop-shadow của canvas web). _Flash: nháy trắng khi trúng đòn; _Gray: gục.
Shader "PokiClash/StickerOutline"
{
    Properties
    {
        [PerRendererData] _MainTex ("Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _White ("Viền trắng (texel)", Float) = 3
        _Ink ("Viền mực (texel)", Float) = 2.5
        _Flash ("Nháy trắng", Range(0,1)) = 0
        _Gray ("Xám", Range(0,1)) = 0

        _StencilComp ("Stencil Comparison", Float) = 8
        _Stencil ("Stencil ID", Float) = 0
        _StencilOp ("Stencil Operation", Float) = 0
        _StencilWriteMask ("Stencil Write Mask", Float) = 255
        _StencilReadMask ("Stencil Read Mask", Float) = 255
        _ColorMask ("Color Mask", Float) = 15
    }

    SubShader
    {
        Tags { "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent" "PreviewType"="Plane" }
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
            #pragma target 2.0
            #include "UnityCG.cginc"
            #include "UnityUI.cginc"
            #pragma multi_compile_local _ UNITY_UI_CLIP_RECT

            struct appdata_t { float4 vertex : POSITION; float4 color : COLOR; float2 texcoord : TEXCOORD0; };
            struct v2f { float4 vertex : SV_POSITION; fixed4 color : COLOR; float2 uv : TEXCOORD0; float4 wpos : TEXCOORD1; };

            sampler2D _MainTex;
            float4 _MainTex_TexelSize;
            fixed4 _Color;
            float _White, _Ink, _Flash, _Gray;
            float4 _ClipRect;
            fixed4 _PokiInk;

            v2f vert(appdata_t v)
            {
                v2f o;
                o.wpos = v.vertex;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                o.color = v.color * _Color;
                return o;
            }

            float Around(float2 uv, float r)
            {
                float2 t = _MainTex_TexelSize.xy * r;
                float a = 0;
                a = max(a, tex2D(_MainTex, uv + float2( t.x, 0)).a);
                a = max(a, tex2D(_MainTex, uv + float2(-t.x, 0)).a);
                a = max(a, tex2D(_MainTex, uv + float2(0,  t.y)).a);
                a = max(a, tex2D(_MainTex, uv + float2(0, -t.y)).a);
                a = max(a, tex2D(_MainTex, uv + t * 0.7071).a);
                a = max(a, tex2D(_MainTex, uv - t * 0.7071).a);
                a = max(a, tex2D(_MainTex, uv + float2(t.x, -t.y) * 0.7071).a);
                a = max(a, tex2D(_MainTex, uv + float2(-t.x, t.y) * 0.7071).a);
                return a;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                fixed4 c = tex2D(_MainTex, i.uv);
                float aw = Around(i.uv, _White);
                float ai = Around(i.uv, _White + _Ink);
                // màu đã nhân alpha khi render ra RT nền trong suốt: chia lại
                float3 art = c.a > 0.001 ? c.rgb / c.a : c.rgb;
                float g = dot(art, float3(0.299, 0.587, 0.114));
                art = lerp(art, float3(g, g, g) * 0.85, _Gray);
                art = lerp(art, float3(1, 1, 1), _Flash);
                float3 col = lerp(_PokiInk.rgb, float3(1, 1, 1), aw);
                col = lerp(col, art, c.a);
                float a = max(max(ai, aw), c.a);
                fixed4 o = fixed4(col, a) * i.color;
                #ifdef UNITY_UI_CLIP_RECT
                o.a *= UnityGet2DClipping(i.wpos.xy, _ClipRect);
                #endif
                return o;
            }
        ENDCG
        }
    }
}
