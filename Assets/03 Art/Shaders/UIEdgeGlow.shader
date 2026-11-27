// Viền sáng bám mép nút (người dùng 2026-11-27, màn quà hôm nay: quầng mềm to sau nút ×2 "lố quá, shader bám viền nhẹ nhàng thôi").
// Vẽ trên một Image không ảnh phủ nút, tràn ra mỗi bên _Width px. Hình nút là chữ nhật bo góc: nửa cỡ _Box.xy, lệch tâm _Box.zw (px, mép
// vẽ của ảnh nút lùi vào trong khung). Sáng nhất ngay mép, tắt dần ra ngoài; lấn vài px vào dưới mép nút để mép vẽ tay không hở.
// Một vệt sáng hơn chạy chậm quanh viền (_Sweep, 0 = tắt). Cộng sáng (SrcAlpha, One) như UIAdditive; màu = _Color × màu Image (alpha
// của Image để code cho thở). Code đặt _Box, _Size, _Width theo cỡ nút thật (DailyGiftView.FitGlow).
Shader "PokiClash/UIEdgeGlow"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint (nhân màu Image; a hạ độ sáng chung)", Color) = (1,1,1,0.8)
        _Box ("Nửa cỡ nút xy, lệch tâm zw (px)", Vector) = (292, 61, -3, 4)
        _Size ("Cỡ Image (px)", Vector) = (660, 200, 0, 0)
        _Radius ("Bo góc nút (px)", Float) = 18
        _Width ("Tầm sáng ra ngoài mép (px)", Float) = 30
        _Under ("Lấn vào dưới mép nút (px)", Float) = 10
        _Power ("Độ dốc tắt dần (to = bám mép hơn)", Range(1, 4)) = 2.2
        _Sweep ("Vệt sáng chạy quanh viền", Range(0, 1)) = 0.45
        _SweepLen ("Dài vệt (px)", Float) = 110
        _Speed ("Vòng mỗi giây", Float) = 0.28

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
        Blend SrcAlpha One
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

            struct appdata_t { float4 vertex : POSITION; float4 color : COLOR; float2 texcoord : TEXCOORD0; UNITY_VERTEX_INPUT_INSTANCE_ID };
            struct v2f { float4 vertex : SV_POSITION; fixed4 color : COLOR; float2 uv : TEXCOORD0; float4 worldPosition : TEXCOORD1; UNITY_VERTEX_OUTPUT_STEREO };

            fixed4 _Color;
            float4 _Box, _Size, _ClipRect;
            float _Radius, _Width, _Under, _Power, _Sweep, _SweepLen, _Speed;

            v2f vert(appdata_t v)
            {
                v2f o;
                UNITY_SETUP_INSTANCE_ID(v);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(o);
                o.worldPosition = v.vertex;
                o.vertex = UnityObjectToClipPos(o.worldPosition);
                o.uv = v.texcoord;
                o.color = v.color * _Color;
                return o;
            }

            // khoảng cách có dấu tới chữ nhật bo góc (> 0 ngoài nút), px
            float RoundBox(float2 p, float2 b, float r)
            {
                float2 q = abs(p) - b + r;
                return length(max(q, 0)) + min(max(q.x, q.y), 0) - r;
            }

            // vị trí (px) dọc chu vi chữ nhật nửa cỡ b của điểm gần p nhất, chiều kim đồng hồ từ góc trên trái; liền mạch qua các góc
            float Perim(float2 p, float2 b)
            {
                float2 c = clamp(p, -b, b);
                float2 e = abs(p) - b;
                if (e.y >= e.x) return p.y > 0 ? c.x + b.x : 2 * b.x + 2 * b.y + (b.x - c.x);
                return p.x > 0 ? 2 * b.x + (b.y - c.y) : 4 * b.x + 2 * b.y + (c.y + b.y);
            }

            fixed4 frag(v2f i) : SV_Target
            {
                float2 p = (i.uv - 0.5) * _Size.xy - _Box.zw;
                float d = RoundBox(p, _Box.xy, _Radius);
                float glow = pow(saturate(1 - max(d, 0) / max(_Width, 1)), _Power);
                glow *= saturate(1 + d / max(_Under, 1)); // dưới nút tắt dần, nút che phần này

                // vệt sáng chạy quanh viền
                float per = 4 * (_Box.x + _Box.y);
                float u = frac(Perim(p, _Box.xy) / per - _Time.y * _Speed);
                float k = min(u, 1 - u) * per / max(_SweepLen, 1);
                float sweep = _Sweep * exp(-k * k * 4);

                float a = glow * (0.6 + sweep) * i.color.a;
                #ifdef UNITY_UI_CLIP_RECT
                a *= UnityGet2DClipping(i.worldPosition.xy, _ClipRect);
                #endif
                return fixed4(i.color.rgb, a);
            }
        ENDCG
        }
    }
}
