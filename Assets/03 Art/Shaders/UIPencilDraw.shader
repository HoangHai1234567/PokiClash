// Tranh chì của tướng trên trang sổ (màn mở khoá tướng, HeroUnlockView; người dùng 2026-11-24: bút chì vẽ hình tướng lên trang giấy
// rồi tướng bật ra). Lấy ảnh tướng (RenderTexture của rig hoặc ảnh chân dung) làm nguồn:
//   - nét chì: đường biên độ sáng trong hình (lấy mẫu theo điểm ảnh màn hình nên nét dày đều) + gạch chéo ở chỗ tối;
//   - gạch chì hiện dần theo đường zích zắc từng hàng từ trên xuống (bút chì trên màn đi đúng đường này, cùng công thức);
//   - tô màu, hai cách:
//     * bút chì màu (người dùng 2026-11-25: "làm nhiều bút chì màu khác nhau tô các phần cùng lúc cho thật hơn", _UseCover = 1):
//       _CoverTex là ảnh phủ phủ đúng hộp, mỗi kênh RGBA là chỗ bút của một nhóm màu (_C0.._C3, gamma) đã gạch qua (Core/CrayonPlan).
//       Mỗi điểm ảnh lấy kênh của nhóm có màu gần nhất nên màu không lem sang vùng khác; nét mực, mảng tối (dưới _DarkL) bút nào qua
//       cũng tô. Vệt sáp có vân chéo và hạt giấy, lực tay nhẹ thì lộ giấy; g (tiến độ) là lớp tô kín cuối cùng;
//     * không có kế hoạch (máy không đọc được ảnh): sáp màu tô tràn chéo từ trên trái xuống, mép tô có sọc sáp (g = tiến độ).
//   Tô xong là màu thật của hình, nét chì còn nhạt bên trên.
// Tham số theo màu đỉnh: r = tiến độ gạch chì, g = tiến độ tô màu (0–1, gửi theo gamma, shader đổi lại khi dự án ở không gian tuyến
// tính), b = 1 nếu nguồn là RenderTexture màu đã nhân alpha, a = độ đục chung. Theo material (bản sao lúc chạy): _Box = hộp quanh hình
// trên ảnh nguồn (RawImage.uvRect), _CoverTex, _UseCover, _C0.._C3.
Shader "PokiClash/UIPencilDraw"
{
    Properties
    {
        [PerRendererData] _MainTex ("Texture", 2D) = "white" {}
        _Rows ("Số hàng gạch zích zắc", Float) = 7
        _Graphite ("Màu chì", Color) = (0.24, 0.2, 0.17, 1)
        _Box ("Hộp quanh hình trên ảnh nguồn (x, y, rộng, cao)", Vector) = (0, 0, 1, 1)
        [NoScaleOffset] _CoverTex ("Ảnh phủ bút chì màu (kênh = nhóm màu)", 2D) = "black" {}
        _UseCover ("Tô bằng bút chì màu", Float) = 0
        _C0 ("Màu nhóm 0 (gamma, w = 1 nếu có)", Vector) = (0, 0, 0, 0)
        _C1 ("Màu nhóm 1", Vector) = (0, 0, 0, 0)
        _C2 ("Màu nhóm 2", Vector) = (0, 0, 0, 0)
        _C3 ("Màu nhóm 3", Vector) = (0, 0, 0, 0)
        _DarkL ("Ngưỡng tối (CrayonPlan.DarkL)", Float) = 0.27

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
            sampler2D _CoverTex;
            float _Rows, _UseCover, _DarkL;
            float4 _Box, _C0, _C1, _C2, _C3;
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

            float Hash(float2 p)
            {
                p = frac(p * float2(123.34, 456.21));
                p += dot(p, p + 45.32);
                return frac(p.x * p.y);
            }

            float VNoise(float2 p)
            {
                float2 i = floor(p), f = frac(p);
                f = f * f * (3 - 2 * f);
                return lerp(lerp(Hash(i), Hash(i + float2(1, 0)), f.x), lerp(Hash(i + float2(0, 1)), Hash(i + 1), f.x), f.y);
            }

            // bình phương khoảng cách màu tới nhóm (nhóm không dùng: rất xa)
            float D(float3 g, float4 c) { float3 d = g - c.rgb; return c.w > 0.5 ? dot(d, d) : 1e4; }

            fixed4 frag(v2f i) : SV_Target
            {
                float hatchP = i.color.r, colP = i.color.g, premul = i.color.b;
                fixed4 c = tex2D(_MainTex, i.uv);
                float3 art = premul > 0.5 && c.a > 0.001 ? c.rgb / c.a : c.rgb;
                float a = c.a;
                float2 lu = (i.uv - _Box.xy) / max(_Box.zw, 1e-5); // uv 0–1 trong hộp quanh hình

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
                float row = floor((1 - lu.y) * _Rows);
                float xr = fmod(row, 2) < 0.5 ? lu.x : 1 - lu.x;
                float o = (row + xr) / _Rows;
                float rev = saturate((hatchP - o) * _Rows * 6);

                float cov;
                if (_UseCover > 0.5)
                {
                    // bút chì màu: kênh của nhóm màu gần nhất; nét mực, mảng tối lấy kênh lớn nhất
                    float3 gm = art;
                    #ifndef UNITY_COLORSPACE_GAMMA
                    gm = LinearToGammaSpace(art);
                    #endif
                    float4 cv = tex2D(_CoverTex, saturate(lu));
                    float4 d = float4(D(gm, _C0), D(gm, _C1), D(gm, _C2), D(gm, _C3));
                    float m = min(min(d.x, d.y), min(d.z, d.w));
                    float4 sel = step(d, m.xxxx);
                    float own = max(max(cv.x * sel.x, cv.y * sel.y), max(cv.z * sel.z, cv.w * sel.w));
                    float anyc = max(max(cv.x, cv.y), max(cv.z, cv.w));
                    float k = dot(gm, float3(0.299, 0.587, 0.114)) < _DarkL ? anyc : own;
                    // vân sáp: sợi chéo theo hướng gạch + hạt giấy (toạ độ điểm ảnh màn hình); lực nhẹ, mép vệt thì lộ giấy
                    float2 q = float2(dot(pix, float2(0.82, 0.57)), dot(pix, float2(-0.57, 0.82)));
                    float fiber = VNoise(float2(q.x / 7.0, q.y / 1.6));
                    float tooth = VNoise(pix / 2.2 + 17.0);
                    float lay = saturate((k - fiber * 0.45) * 2.6);
                    cov = max(lay * (0.84 + 0.16 * tooth), colP);
                }
                else
                {
                    // sáp màu tô tràn chéo, mép có sọc sáp
                    float oc = saturate(lu.x * 0.35 + (1 - lu.y) * 0.65);
                    float stripe = frac((pix.x - pix.y * 0.6) / 11.0);
                    cov = colP >= 0.999 ? 1 : saturate((colP * 1.3 - oc) * 5 + (stripe - 0.5) * 0.9) * step(0.001, colP);
                }

                // nét chì đè lên lớp màu (dưới màu chỉ còn nhạt)
                float sk = sketch * rev * 0.9 * (1 - 0.8 * cov);
                float A = sk + cov * (1 - sk);
                float3 col = (_Graphite.rgb * sk + art * cov * (1 - sk)) / max(A, 1e-4);
                fixed4 res = fixed4(col, a * A * i.color.a);
                #ifdef UNITY_UI_CLIP_RECT
                res.a *= UnityGet2DClipping(i.wpos.xy, _ClipRect);
                #endif
                return res;
            }
        ENDCG
        }
    }
}
