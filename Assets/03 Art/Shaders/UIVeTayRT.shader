// HIỆN HIỆU ỨNG PREFAB GỐC CÓ CHẤT VẼ TAY (2026-11-25; người dùng: "làm theo hướng A, dùng thẳng prefab của gói, nhưng nên sửa lại 1 chút để
// nó có chất vẽ tay hơn"). Prefab ParticleSystem của gói (vd. FX_PF_MagicWater_OrbLoop) chạy ở góc xa thế giới, camera riêng chụp vào
// RenderTexture (CauMaRig); RawImage trên lớp hạt của sân (CauMaHien) vẽ texture đó qua shader này:
//  - màu: độ sáng của ảnh gốc → 4 DẢI PHẲNG (tối / sâu / sáng / kem; 2026-11-25 người dùng đổi sang xanh biển hơi sẫm), ranh dải run theo
//    nhiễu (nét tay); trộn lại một phần sắc gốc (_GiuGoc) đã xoay sắc (_DoiSac) cho khỏi mất khối;
//  - độ hiện: hai bậc phẳng (mờ / đặc) thay cho mờ dần mịn, mép run theo nhiễu;
//  - VÂN CHÌ gạch chéo theo toạ độ màn hình (A của nuoc_nhieu.png), nhạt ở vùng kem;
//  - QUẦNG (NGOẠI LỆ người dùng cho riêng cầu ma thủy): phần cộng sáng của gói (rgb vượt alpha trong ảnh premultiplied) giữ lại thành quầng
//    mềm cộng dồn màu _ColQuang, không bị dồn dải.
// Ảnh RenderTexture là premultiplied (xoá về 0,0,0,0, hạt trộn alpha / cộng sáng lên) → trộn One / OneMinusSrcAlpha.
Shader "PokiClash/UIVeTayRT"
{
    Properties
    {
        [PerRendererData] _MainTex ("Ảnh RenderTexture", 2D) = "black" {}
        _NoiseTex ("Nhiễu lặp (B mịn, A vân chì)", 2D) = "gray" {}
        _ColShade ("Tối", Color) = (0.059, 0.208, 0.471, 1)
        _ColDeep ("Sâu", Color) = (0.094, 0.333, 0.678, 1)
        _ColBody ("Sáng", Color) = (0.216, 0.51, 0.86, 1)
        _ColFoam ("Kem", Color) = (0.8, 0.9, 1.0, 1)
        _ColQuang ("Quầng", Color) = (0.6, 0.82, 1.0, 1)
        _DoiSac ("Xoay sắc màu gốc (độ; 26: xanh ngọc của gói → xanh biển)", Float) = 26
        _SacSang ("Độ sáng màu gốc (vùng tối, giữ sáng ở vùng kem)", Range(0.4, 1.2)) = 0.8
        _DamSac ("Độ đậm màu gốc sau khi xoay", Range(0, 2)) = 1.35
        _Bands ("Ngưỡng dải độ sáng (x tối, y sâu, z sáng→kem)", Vector) = (0.16, 0.34, 0.62, 0)
        _AlphaLo ("Ngưỡng hiện mờ", Float) = 0.1
        _AlphaHi ("Ngưỡng hiện đặc", Float) = 0.42
        _AlphaMid ("Độ hiện bậc mờ", Float) = 0.55
        _AlphaMax ("Độ hiện tối đa (khối phủ đối thủ trong mờ)", Range(0, 1)) = 0.85
        _GiuGoc ("Giữ sắc gốc", Range(0, 1)) = 0.55
        _Phang ("Độ dồn bậc độ hiện (0 giữ mờ gốc, 1 hai bậc phẳng)", Range(0, 1)) = 0.45
        _RunCo ("Cỡ ô nhiễu run (px UI)", Float) = 260
        _Quang ("Độ quầng", Float) = 1.1
        _Run ("Độ run mép / ranh", Float) = 0.09
        _Hatch ("Độ đậm vân chì", Float) = 0.4
        _HatchPx ("Cỡ ô vân chì (px UI)", Float) = 110

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
        Tags { "Queue" = "Transparent" "IgnoreProjector" = "True" "RenderType" = "Transparent" "PreviewType" = "Plane" "CanUseSpriteAtlas" = "True" }
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
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma target 3.0
            #include "UnityCG.cginc"
            #include "UnityUI.cginc"
            #pragma multi_compile_local _ UNITY_UI_CLIP_RECT
            #pragma multi_compile_local _ UNITY_UI_ALPHACLIP

            struct appdata
            {
                float4 vertex : POSITION;
                float4 color : COLOR;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float4 pos : SV_POSITION;
                fixed4 color : COLOR;
                float2 uv : TEXCOORD0;
                float4 wpos : TEXCOORD1;
            };

            sampler2D _MainTex, _NoiseTex;
            fixed4 _ColShade, _ColDeep, _ColBody, _ColFoam, _ColQuang;
            float4 _Bands, _ClipRect;
            float _DoiSac, _SacSang, _DamSac, _AlphaMax, _AlphaLo, _AlphaHi, _AlphaMid, _GiuGoc, _Phang, _RunCo, _Quang, _Run, _Hatch, _HatchPx;

            // xoay sắc quanh trục xám (giữ độ sáng gần đúng)
            float3 XoaySac(float3 c, float deg)
            {
                float a = radians(deg), cs = cos(a), sn = sin(a);
                const float3 k = float3(0.57735, 0.57735, 0.57735);
                return c * cs + cross(k, c) * sn + k * dot(k, c) * (1 - cs);
            }

            v2f vert(appdata v)
            {
                v2f o;
                o.wpos = v.vertex;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.color = v.color;
                o.uv = v.uv;
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                float4 s = tex2D(_MainTex, i.uv);
                float a = saturate(s.a);
                float3 goc = a > 0.004 ? saturate(s.rgb / a) : float3(0, 0, 0);       // màu gốc bỏ premultiply
                // dự án màu Linear: ảnh RT đọc ra là giá trị tuyến tính (teal tầm trung ~0,07) → đổi về gamma rồi mới chia dải, không thì
                // gần hết vỏ xoáy rơi vào dải tối thành mảng sẫm đặc
                float lum = dot(LinearToGammaSpace(goc), float3(0.3, 0.59, 0.11));
                float2 sp = i.wpos.xy / max(20, _RunCo);
                float run = (tex2D(_NoiseTex, sp).r - 0.5) * 2 * _Run;                  // run nét tay cho ranh dải và mép (kênh R mượt, không lấm tấm)
                float l = lum + run;
                float3 col = l < _Bands.x ? _ColShade.rgb : (l < _Bands.y ? _ColDeep.rgb : (l < _Bands.z ? _ColBody.rgb : _ColFoam.rgb));
                // màu gốc của gói (xanh ngọc) xoay sang màu nước của chiêu, hạ sáng vùng tối; dải độ sáng vẫn theo ảnh gốc
                float3 gg = XoaySac(LinearToGammaSpace(goc), _DoiSac);
                float gl = dot(gg, float3(0.3, 0.59, 0.11));
                gg = (gl + (gg - gl) * _DamSac) * lerp(_SacSang, 1, smoothstep(0.6, 0.95, lum));   // xoay xong hơi xỉn: đẩy đậm lại
                col = lerp(col, GammaToLinearSpace(saturate(gg)), _GiuGoc);
                float aa = a + run * 0.5;
                float ab = step(_AlphaLo, aa) * lerp(_AlphaMid, 1, step(_AlphaHi, aa)); // hai bậc độ hiện
                ab = lerp(a, ab, _Phang);                                                // chỉ dồn bậc một phần: giữ độ trong của vỏ xoáy gốc
                ab = min(ab, _AlphaMax);                                                 // khối nước phủ lên đối thủ: trong mờ, vẫn thấy con bị trúng
                // vân chì (nhạt ở vùng kem)
                float h = tex2D(_NoiseTex, i.wpos.xy / _HatchPx).a;
                float kem = l >= _Bands.z ? 1 : 0;
                col *= lerp(1, h, _Hatch * (1 - 0.6 * kem));
                // quầng (ngoại lệ): phần cộng sáng vượt alpha giữ lại thành quầng mềm, cộng dồn (premultiplied, không thêm alpha)
                float du = saturate(dot(s.rgb, float3(0.3, 0.59, 0.11)) - a * 0.55);
                float3 quang = _ColQuang.rgb * du * _Quang;
                float A = ab * i.color.a;
                fixed4 o = fixed4(col * A + quang * i.color.a, A);
                #ifdef UNITY_UI_CLIP_RECT
                o *= UnityGet2DClipping(i.wpos.xy, _ClipRect);
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
