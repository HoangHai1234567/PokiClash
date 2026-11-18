// Tia nắng dịu cho lớp sáng tối (DayNight): các dải sáng ấm chéo từ góc trên trái, trôi rất chậm, mạnh ở phía trên, nhạt dần xuống
// dưới; cộng sáng nhẹ (Blend One One). Độ mạnh theo alpha của màu Image, màu nắng nhân với rgb của nó (DayNight).
// Dải nắng tính theo toạ độ CỦA ẢNH (uv nhân cỡ ảnh theo đơn vị canvas, cỡ suy từ đạo hàm màn hình), không theo toạ độ canvas: kéo bản đồ
// thì nắng đi theo bản đồ, phóng to thì dải to theo (người dùng báo 2026-11-18: trước đây nắng đứng yên như UI khi kéo, ở mọi màn).
// Đảo, sảnh: ảnh nắng là RawImage tràn ra ngoài ảnh, DayNight đặt uvRect để uv 0..1 trùng khung ảnh, phần tràn có uv ngoài 0..1:
// dải chạy tiếp, fade kẹp 0..1, nên kéo / zoom ra rìa không lộ mép chữ nhật sáng.
Shader "PokiClash/UISunRays"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _Warm ("Màu nắng", Color) = (1, 0.9, 0.66, 1)
        _Strength ("Độ sáng tối đa", Range(0, 1)) = 0.32
        _Scale ("(cũ, không dùng) Bề rộng dải theo canvas", Float) = 420
        _Bands ("Mật độ dải theo chiều cao ảnh", Float) = 5.5
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
        Blend One One
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

            struct appdata_t { float4 vertex : POSITION; float4 color : COLOR; float2 texcoord : TEXCOORD0; UNITY_VERTEX_INPUT_INSTANCE_ID };
            struct v2f { float4 vertex : SV_POSITION; fixed4 color : COLOR; float2 uv : TEXCOORD0; float4 worldPosition : TEXCOORD1; UNITY_VERTEX_OUTPUT_STEREO };

            fixed4 _Color, _Warm;
            float _Strength, _Scale, _Bands;
            float4 _ClipRect;

            v2f vert(appdata_t v)
            {
                v2f OUT;
                UNITY_SETUP_INSTANCE_ID(v);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);
                OUT.worldPosition = v.vertex;
                OUT.vertex = UnityObjectToClipPos(OUT.worldPosition);
                OUT.uv = v.texcoord;
                OUT.color = v.color * _Color;
                return OUT;
            }

            fixed4 frag(v2f IN) : SV_Target
            {
                float t = _Time.y;
                // tỉ lệ khung ảnh = (độ dời canvas trên một đơn vị u) / (trên một đơn vị v); không đổi khi kéo hay phóng (Image không xoay)
                float2 dPx = ddx(IN.worldPosition.xy), dPy = ddy(IN.worldPosition.xy);
                float2 dUx = ddx(IN.uv), dUy = ddy(IN.uv);
                float sx = length(float2(dPx.x, dPy.x)) / max(length(float2(dUx.x, dUy.x)), 1e-6);
                float sy = length(float2(dPx.y, dPy.y)) / max(length(float2(dUx.y, dUy.y)), 1e-6);
                float2 p = float2(IN.uv.x * sx / max(sy, 1e-6), IN.uv.y) * _Bands; // toạ độ trong ảnh: dời và phóng cùng bản đồ
                float2 dir = normalize(float2(0.55, -0.83));   // nắng rọi từ trên trái xuống dưới phải
                float u = dot(p, float2(-dir.y, dir.x));       // ngang qua các dải
                float band = smoothstep(0.55, 1.0, 0.5 + 0.5 * sin(u * 3.1 + t * 0.12));
                band += 0.6 * smoothstep(0.62, 1.0, 0.5 + 0.5 * sin(u * 5.3 - t * 0.09 + 1.7));
                band += 0.35 * smoothstep(0.7, 1.0, 0.5 + 0.5 * sin(u * 8.9 + t * 0.07 + 4.1));
                float fade = saturate(IN.uv.y * 1.25 - 0.15);   // mạnh ở phía trên ảnh
                float k = (band * fade * 0.8 + 0.12) * _Strength * IN.color.a;
                #ifdef UNITY_UI_CLIP_RECT
                k *= UnityGet2DClipping(IN.worldPosition.xy, _ClipRect);
                #endif
                return fixed4(_Warm.rgb * IN.color.rgb * k, 0); // màu Image nhuộm nắng (chạng vạng: cam)
            }
        ENDCG
        }
    }
}
