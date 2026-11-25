// Viền độ hiếm quanh thẻ chọn trong trận (người dùng 2026-11-25: "thẻ rare (xanh dương) đến legend vàng cam có shader bao xung quanh
// màu thẻ đó, càng hiếm shader càng epic"). Vẽ trên một Image phủ thẻ, tràn ra mỗi bên (_Size − cỡ thẻ) / 2 px; DraftDeck đặt Image
// này ở lớp riêng sau mọi thẻ và cho nó bám theo thẻ (vị trí, góc, cỡ, cả lúc lật).
// Hình: các dải màu PHẲNG (ngoài màu độ hiếm, giữa nhạt hơn, trong gần kem), mép ngoài có nét sẫm như nét mực, vân chì gạch chéo −38 độ;
// mép dải là lưỡi lửa bốc lên (nhiễu cuộn lên trên, lửa cạnh trên cao hơn) — không quầng mềm, không cộng sáng.
// Mỗi bậc hiếm một material (DraftDeck tạo từ Resources/the_aura): Hiếm viền mỏng gợn nhẹ; Sử thi dày, lửa vừa, sao chạy quanh;
// Huyền thoại dày nhất, lửa cao, nhiều sao, tia nắng gãy khúc xoay chậm sau thẻ.
// Dữ liệu riêng từng thẻ đi qua màu đỉnh của Image (UI không đổi màu đỉnh sang Linear): r = pha bung lúc lật (0..1, ngoài khoảng là
// tắt), a = độ hiện.
Shader "PokiClash/UICardAura"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _C1 ("Màu ngoài (màu độ hiếm)", Color) = (0.953, 0.604, 0.176, 1)
        _C2 ("Màu giữa", Color) = (1, 0.79, 0.29, 1)
        _C3 ("Màu trong", Color) = (1, 0.95, 0.77, 1)
        _CInk ("Nét mép ngoài", Color) = (0.55, 0.33, 0.1, 1)
        _Card ("Nửa cỡ thẻ xy, lệch tâm zw (px)", Vector) = (151, 224, -3, 2)
        _Size ("Cỡ ảnh viền (px)", Vector) = (512, 656, 0, 0)
        _Radius ("Bo góc thẻ (px)", Float) = 18
        _Width ("Bề dày viền (px)", Float) = 20
        _Amp ("Độ lửa (0 = viền đều)", Range(0, 1)) = 0.7
        _Top ("Lửa cạnh trên cao thêm", Range(0, 2)) = 0.6
        _Rise ("Tốc độ lửa bốc", Float) = 1
        _Freq ("Tần số lửa (x, y)", Vector) = (0.05, 0.022, 0, 0)
        _Spark ("Số sao chạy quanh", Range(0, 8)) = 3
        _Rays ("Tia sau thẻ", Range(0, 1)) = 0
        _InkW ("Bề dày nét mép (px)", Float) = 2.5
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

            struct appdata_t { float4 vertex : POSITION; float4 color : COLOR; float2 texcoord : TEXCOORD0; UNITY_VERTEX_INPUT_INSTANCE_ID };
            struct v2f { float4 vertex : SV_POSITION; fixed4 color : COLOR; float2 uv : TEXCOORD0; float4 worldPosition : TEXCOORD1; UNITY_VERTEX_OUTPUT_STEREO };

            fixed4 _Color, _C1, _C2, _C3, _CInk;
            float4 _Card, _Size, _Freq, _ClipRect;
            float _Radius, _Width, _Amp, _Top, _Rise, _Spark, _Rays, _InkW;

            v2f vert(appdata_t v)
            {
                v2f OUT;
                UNITY_SETUP_INSTANCE_ID(v);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);
                OUT.worldPosition = v.vertex;
                OUT.vertex = UnityObjectToClipPos(OUT.worldPosition);
                OUT.uv = v.texcoord;
                OUT.color = v.color; // dữ liệu, không nhân _Color
                return OUT;
            }

            float Hash21(float2 p)
            {
                p = frac(p * float2(123.34, 456.21));
                p += dot(p, p + 45.32);
                return frac(p.x * p.y);
            }

            float Noise(float2 p)
            {
                float2 i = floor(p), f = frac(p);
                float2 u = f * f * (3 - 2 * f);
                return lerp(lerp(Hash21(i), Hash21(i + float2(1, 0)), u.x), lerp(Hash21(i + float2(0, 1)), Hash21(i + float2(1, 1)), u.x), u.y);
            }

            // khoảng cách có dấu tới chữ nhật bo góc (> 0 ngoài thẻ), px
            float RoundBox(float2 p, float2 b, float r)
            {
                float2 q = abs(p) - b + r;
                return length(max(q, 0)) + min(max(q.x, q.y), 0) - r;
            }

            // điểm thứ s (0..1) trên chu vi chữ nhật nửa cỡ h, chạy theo chiều kim đồng hồ từ góc trên trái
            float2 Perim(float s, float2 h)
            {
                float u = s * 4 * (h.x + h.y);
                if (u < 2 * h.x) return float2(-h.x + u, h.y);
                u -= 2 * h.x;
                if (u < 2 * h.y) return float2(h.x, h.y - u);
                u -= 2 * h.y;
                if (u < 2 * h.x) return float2(h.x - u, -h.y);
                u -= 2 * h.x;
                return float2(-h.x, -h.y + u);
            }

            // 1 khi x < 0, mép khử răng cưa rộng w (một điểm ảnh)
            float Inside(float x, float w) { return saturate(0.5 - x / max(w, 1e-4)); }

            fixed4 frag(v2f IN) : SV_Target
            {
                float t = _Time.y;
                float2 p = (IN.uv - 0.5) * _Size.xy;
                float2 q = p - _Card.zw;
                float d = RoundBox(q, _Card.xy, _Radius);
                float fw = max(fwidth(d), 0.5);
                float burst = IN.color.r;
                float bursting = step(0.004, burst) * step(burst, 0.996);

                // ---------- dải viền: lưỡi lửa bốc lên ----------
                float up = saturate(q.y / _Card.y);
                float2 nf = q * _Freq.xy + float2(0, -t * _Rise);
                float n = Noise(nf) * 0.65 + Noise(nf * 2.13 + 7.31) * 0.35;
                float pulse = 1 + 0.07 * sin(t * 2.6);
                float w = _Width * pulse * (1 - _Amp * 0.5 + _Amp * n) * (1 + _Top * up * up);
                w *= 1 + 0.35 * bursting * (1 - burst) * (1 - burst); // bung: viền phồng nhẹ rồi về (vòng lan ra mới là chính)
                float mOut = Inside(d - w, fw);
                float mMid = Inside(d - w * 0.64, fw);
                float mIn = Inside(d - w * 0.3, fw);
                float under = 1 - Inside(d + 6, fw); // lấn 6 px vào dưới mép thẻ (mép giấy vẽ tay không trùng hẳn chữ nhật)
                float3 c = lerp(_C1.rgb, _C2.rgb, mMid);
                c = lerp(c, _C3.rgb, mIn);
                float ink = mOut * (1 - Inside(d - (w - _InkW), fw));
                c = lerp(c, _CInk.rgb, ink);
                float hatch = step(0.55, frac(dot(p, float2(0.788, -0.616)) / 7.0)); // vân chì −38 độ
                c *= lerp(1, 0.9, hatch * (1 - mIn));
                float a = mOut * under;

                // ---------- tia nắng gãy khúc sau thẻ (Huyền thoại) ----------
                if (_Rays > 0.01)
                {
                    float ang = atan2(q.y, q.x) / 6.28318 + t * 0.025;
                    float idx = floor(ang * 16);
                    float ray = step(0.5, frac(ang * 16));
                    float len = (_Size.x * 0.5 - _Card.x) * lerp(0.55, 0.92, Hash21(float2(idx, 3.7)));
                    float ra = ray * Inside(d - len, fw) * step(0, d) * (1 - mOut) * 0.42 * _Rays;
                    c = lerp(_C2.rgb, c, a);
                    a = max(a, ra);
                }

                // ---------- sao bốn cánh chạy quanh mép ----------
                float2 hs = _Card.xy + _Width * 0.85;
                [loop] for (int i = 0; i < 8; i++)
                {
                    float fi = i;
                    if (fi >= _Spark) break;
                    float dir = fmod(fi, 2) < 0.5 ? 1 : -0.75;
                    float s = frac(fi / max(_Spark, 1) + t * 0.05 * dir + fi * 0.13);
                    float2 pos = Perim(s, hs);
                    float tw = 0.55 + 0.45 * sin(t * 4.2 + fi * 2.3);
                    float sz = (9 + _Width * 0.45) * tw;
                    float2 r = abs(q - pos) / sz;
                    float st = sqrt(r.x) + sqrt(r.y); // < 1: trong hình sao (astroid)
                    float inS = Inside((st - 1) * sz, fw * 1.2);
                    float fill = Inside((st - 0.82) * sz, fw * 1.2); // trong nét viền sẫm
                    float core = Inside((st - 0.45) * sz, fw * 1.2);
                    c = lerp(c, lerp(lerp(_CInk.rgb, _C2.rgb, fill), _C3.rgb, core), inS);
                    a = max(a, inS);
                }

                // ---------- bung lúc lật: vòng theo dáng thẻ lan ra + chấm bắn theo tia ----------
                if (bursting > 0.5)
                {
                    float e = 1 - (1 - burst) * (1 - burst);
                    float reach = (_Size.x * 0.5 - _Card.x) * 0.95;
                    float R = e * reach;
                    float th = lerp(16, 3, burst);
                    float ring = Inside(abs(d - R) - th * 0.5, fw);
                    float ang = atan2(q.y, q.x) / 6.28318;
                    float sector = floor(ang * 12 + 0.5);
                    float local = (ang * 12 - sector) * 6.28318 / 12 * length(q); // dời ngang tia (px)
                    float dotR = e * reach * 1.1 + 10;
                    float dsz = lerp(9, 2, burst);
                    float dotM = Inside(length(float2(local, d - dotR)) - dsz, fw);
                    c = lerp(c, _C3.rgb, ring);
                    c = lerp(c, _C2.rgb, dotM * (1 - ring));
                    a = max(a, max(ring, dotM) * (1 - burst * 0.4));
                }

                a *= IN.color.a;
                #ifdef UNITY_UI_CLIP_RECT
                a *= UnityGet2DClipping(IN.worldPosition.xy, _ClipRect);
                #endif
                return fixed4(c * a, a);
            }
        ENDCG
        }
    }
}
