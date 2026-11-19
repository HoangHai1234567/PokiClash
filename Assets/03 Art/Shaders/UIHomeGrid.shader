// Lưới thoi phát sáng của chế độ xây màn Nhà (người dùng dặn 2026-11-19: "khi xây / đặt vị trí các building phải nhìn thấy grid kiểu
// ánh sáng glowing"; học Clash of Clans, Clash of Critters). Một ảnh phủ cả bản đồ, nằm trên ô lát, dưới công trình:
// - nét lưới theo ô (gx, gy) tính từ toạ độ ảnh: lõi sáng mảnh (theo px màn, zoom nào cũng mảnh như nhau) + quầng mềm cộng sáng;
// - chỉ trên ô rừng đã mở (_Lots, 1 = mở), mờ dần ra xa chỗ đang đặt (_Ghost) để mắt tập trung;
// - chân thoi công trình đang đặt: phủ màu (xanh đặt được / đỏ không), viền chân thoi sáng, nhịp phập phồng;
// - _Fade: hiện / ẩn dần khi vào, ra chế độ xây.
// Trộn premultiplied: nét, quầng cộng sáng (alpha 0), phủ chân thoi trộn thường.
Shader "PokiClash/UIHomeGrid"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _LineCol ("Màu nét", Color) = (0.8,1,0.95,0.55)
        _GlowCol ("Màu quầng", Color) = (0.45,0.95,1,0.35)
        _GhostCol ("Màu chân thoi", Color) = (0.35,1,0.45,1)
        _GridTop ("Góc trên ô (0,0), px bản đồ", Vector) = (0,0,0,0)
        _Cell ("Ô: ngang, dọc (px)", Vector) = (96,48,0,0)
        _Size ("Cỡ bản đồ (px)", Vector) = (1000,1000,0,0)
        _Grid ("Cạnh lưới (ô)", Float) = 72
        _Lot ("Cạnh ô rừng (ô)", Float) = 12
        _LotsSide ("Số ô rừng mỗi cạnh", Float) = 6
        _Ghost ("Chân thoi đang đặt: gx, gy, cạnh, bật", Vector) = (0,0,0,0)
        _Fade ("Hiện", Range(0,1)) = 1

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
                fixed4 color    : COLOR;
                float2 texcoord : TEXCOORD0;
                float4 worldPosition : TEXCOORD1;
                UNITY_VERTEX_OUTPUT_STEREO
            };

            fixed4 _Color, _LineCol, _GlowCol, _GhostCol;
            float4 _ClipRect, _GridTop, _Cell, _Size, _Ghost;
            float _Grid, _Lot, _LotsSide, _Fade;
            float _Lots[64]; // ô rừng đã mở (i * cạnh + j), tối đa 8 x 8

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
                // px bản đồ (gốc trên trái, y xuống) → toạ độ ô liên tục
                float2 px = float2(IN.texcoord.x * _Size.x, (1.0 - IN.texcoord.y) * _Size.y);
                float u = (px.x - _GridTop.x) / (_Cell.x * 0.5);
                float v = (px.y - _GridTop.y) / (_Cell.y * 0.5);
                float2 g = float2((u + v) * 0.5, (v - u) * 0.5);
                float2 fw = max(fwidth(g), 1e-5);
                if (g.x < 0 || g.y < 0 || g.x > _Grid || g.y > _Grid) return fixed4(0, 0, 0, 0);

                // ô rừng đã mở mới có lưới
                int li = (int)floor(min(g.x, _Grid - 0.001) / _Lot), lj = (int)floor(min(g.y, _Grid - 0.001) / _Lot);
                float open = _Lots[li * (int)_LotsSide + lj];

                // khoảng cách tới nét gần nhất, đổi ra px màn
                float2 f = abs(frac(g + 0.5) - 0.5) / fw;
                float dl = min(f.x, f.y);
                float core = 1.0 - smoothstep(0.55, 1.5, dl);
                float halo = exp(-dl * 0.45);

                // chân thoi đang đặt
                bool on = _Ghost.w > 0.5;
                float n = max(_Ghost.z, 1);
                float2 c = _Ghost.xy + n * 0.5;
                float2 q = abs(g - c) - n * 0.5;           // < 0 trong chân thoi
                float inside = (on && q.x < 0 && q.y < 0) ? 1.0 : 0.0;
                float edge = on ? max(q.x / fw.x, q.y / fw.y) : 1e4; // px tới viền chân thoi (âm: bên trong)
                float rim = on ? exp(-abs(edge) * 0.18) : 0;
                float pulse = 0.78 + 0.22 * sin(_Time.y * 5.0);

                // mờ dần ra xa chỗ đang đặt (vẫn thấy cả lưới đất đã mở)
                float dist = on ? length(g - c) : 0;
                float near = saturate(1.0 - (dist - n * 0.5 - 2.0) / 7.0);
                float focus = on ? lerp(0.14, 1.0, near * near) : 0.45;

                float k = open * focus * _Fade;
                float3 add = (_LineCol.rgb * core * _LineCol.a + _GlowCol.rgb * halo * _GlowCol.a * (on ? near : 0.3)) * k;
                // chân thoi: nét, quầng theo màu xanh / đỏ, viền sáng phập phồng, phủ trộn thường
                float3 gc = _GhostCol.rgb;
                add = lerp(add, (gc * core + gc * halo * 0.45) * _Fade, inside);
                add += gc * rim * 0.9 * pulse * _Fade;
                float fillA = inside * 0.26 * pulse * _Fade;
                float3 rgb = add + gc * fillA;
                fixed4 o = fixed4(rgb, fillA) * IN.color.a;

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
