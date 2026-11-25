// Tranh chì của tướng trên trang sổ (màn mở khoá tướng, HeroUnlockView; người dùng 2026-11-24: bút chì vẽ hình tướng lên trang giấy
// rồi tướng bật ra). Lấy ảnh tướng (RenderTexture của rig hoặc ảnh chân dung) làm nguồn:
//   - nét chì: đường biên độ sáng trong hình (lấy mẫu theo điểm ảnh màn hình nên nét dày đều) + gạch chéo ở chỗ tối;
//   - gạch chì hiện dần theo đường zích zắc từng hàng từ trên xuống (bút chì trên màn đi đúng đường này, cùng công thức);
//   - sáp màu tô tràn chéo từ trên trái xuống, mép tô có sọc sáp; tô xong là màu thật của hình, nét chì còn nhạt bên trên.
// Tham số theo màu đỉnh (không cần bản sao material lúc chạy): r = tiến độ gạch chì, g = tiến độ tô màu (0–1, gửi theo gamma, shader
// đổi lại khi dự án ở không gian tuyến tính), b = 1 nếu nguồn là RenderTexture màu đã nhân alpha, a = độ đục chung.
// uv 0–1 của ảnh là hộp quanh hình (RawImage.uvRect cắt sẵn), nên hàng zích zắc trải đúng trên tướng.
Shader "PokiClash/UIPencilDraw"
{
    Properties
    {
        [PerRendererData] _MainTex ("Texture", 2D) = "white" {}
        _Rows ("Số hàng gạch zích zắc", Float) = 7
        _Graphite ("Màu chì", Color) = (0.24, 0.2, 0.17, 1)

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
            #pragma target 3.0
            #include "UnityCG.cginc"
            #include "UnityUI.cginc"
            #pragma multi_compile_local _ UNITY_UI_CLIP_RECT

            struct appdata_t { float4 vertex : POSITION; float4 color : COLOR; float2 texcoord : TEXCOORD0; };
            struct v2f { float4 vertex : SV_POSITION; float4 color : COLOR; float2 uv : TEXCOORD0; float4 wpos : TEXCOORD1; };

            sampler2D _MainTex;
            float _Rows;
            fixed4 _Graphite;
            float4 _ClipRect;

            v2f vert(appdata_t v)
            {
                v2f o;
                o.wpos = v.vertex;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                o.color = v.color;
                #ifndef UNITY_COLORSPACE_GAMMA
                o.color.rg = LinearToGammaSpace(float3(v.color.rg, 0)).rg; // canvas đổi màu đỉnh sang tuyến tính: đổi lại
                #endif
                return o;
            }

            // độ sáng của điểm, nền trong suốt coi như giấy trắng (biên hình cũng ra nét)
            float Lum(float2 uv, float premul)
            {
                fixed4 c = tex2D(_MainTex, uv);
                float3 art = premul > 0.5 && c.a > 0.001 ? c.rgb / c.a : c.rgb;
                float l = dot(art, float3(0.299, 0.587, 0.114));
                return lerp(1, l, c.a);
            }

            fixed4 frag(v2f i) : SV_Target
            {
                float hatchP = i.color.r, colP = i.color.g, premul = i.color.b;
                fixed4 c = tex2D(_MainTex, i.uv);
                float3 art = premul > 0.5 && c.a > 0.001 ? c.rgb / c.a : c.rgb;
                float a = c.a;

                // nét chì: biên độ sáng, bước lấy mẫu 1,5 điểm ảnh màn hình
                float2 fw = max(fwidth(i.uv), 1e-6);
                float2 dx = float2(fw.x * 1.5, 0), dy = float2(0, fw.y * 1.5);
                float g = abs(Lum(i.uv + dx, premul) - Lum(i.uv - dx, premul)) + abs(Lum(i.uv + dy, premul) - Lum(i.uv - dy, premul));
                float edge = smoothstep(0.1, 0.3, g);
                // gạch chéo ở chỗ tối (toạ độ điểm ảnh màn hình)
                float2 pix = i.uv / fw;
                float L = dot(art, float3(0.299, 0.587, 0.114));
                float hatch = smoothstep(0.6, 0.72, frac((pix.x + pix.y) / 9.0)) * saturate((0.78 - L) * 1.8);
                float sketch = saturate(edge + hatch * 0.6);

                // gạch chì hiện theo zích zắc: hàng từ trên xuống, hàng chẵn trái → phải, hàng lẻ phải → trái
                float row = floor((1 - i.uv.y) * _Rows);
                float xr = fmod(row, 2) < 0.5 ? i.uv.x : 1 - i.uv.x;
                float o = (row + xr) / _Rows;
                float rev = saturate((hatchP - o) * _Rows * 6);

                // sáp màu tô tràn chéo, mép có sọc sáp
                float oc = saturate(i.uv.x * 0.35 + (1 - i.uv.y) * 0.65);
                float stripe = frac((pix.x - pix.y * 0.6) / 11.0);
                float cov = colP >= 0.999 ? 1 : saturate((colP * 1.3 - oc) * 5 + (stripe - 0.5) * 0.9) * step(0.001, colP);

                float3 col = lerp(_Graphite.rgb, art, cov);
                col = lerp(col, _Graphite.rgb, edge * 0.2 * cov);
                float alpha = a * max(sketch * rev * 0.9, cov);
                fixed4 res = fixed4(col, alpha * i.color.a);
                #ifdef UNITY_UI_CLIP_RECT
                res.a *= UnityGet2DClipping(i.wpos.xy, _ClipRect);
                #endif
                return res;
            }
        ENDCG
        }
    }
}
