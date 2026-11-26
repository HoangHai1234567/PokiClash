// Mặt hồ của scene Bến câu (GD_Claude/32_BenCau_Scene.md mục 3), vẽ trên ảnh nền ben_cau_nen (Image uGUI, material riêng của màn).
// Bản 2 (người dùng 2026-11-26: "nước quá tĩnh, không có tương tác với mồi câu / dây câu"): mặt nước động rõ, phao và cá làm nước động.
// _WaterTex (ArtGen/Casino/ben_cau/nuoc/lam_nuoc.py, cùng khung ảnh nền 1024 x 1536): R = mặt nước, G = khoảng cách tới bờ / 48 px.
// Chỉ vẽ trong nước; tính theo px ảnh nền gốc (p = uv × _PlateSize, y lên). Lớp, từ dưới lên:
//  1. nền lăn tăn hai tầng sóng (_Wobble px), quanh phao thêm vòng khúc xạ lan ra;
//  2. vệt sáng chì màu chạy theo sóng (dải sin uốn theo nhiễu, đứt khúc), màu _LightCol;
//  3. bóng cá (_Fish[i] = x, y, góc, dài; _FishB[i].x = độ đậm, .y = pha quẫy), đuôi quẫy, màu _ShadowCol nhân lên nước;
//  4. vệt sóng trắng trôi, hiện rồi tan;
//  5. bọt vỗ bờ quanh bờ, đá, lá súng, cọc bến;
//  6. phao (_Bob = x, y, độ chìm 0..1, bật): mảng nước sẫm dưới phao, vòng nước bám quanh thân phao, gợn tròn toả đều liên tục;
//  7. vệt rẽ nước chữ V sau vật đang chạy (_Wake = x, y, góc chạy radian, độ mạnh): phao bị kéo, cá giãy;
//  8. gợn tròn sự kiện (_Rip[i] = x, y, lúc bắt đầu theo _Now, độ mạnh), 8 nguồn: phao rơi, cá rỉa, cắn, giật, nhịp kéo, cá vọt.
// Đêm chưa làm (cần lớp đêm cho cả cảnh, không chỉ nước). Tô phẳng, mép cứng, không quầng sáng, không chuyển màu mềm
// (luật UI); màu lấy từ thuộc tính (Unity đổi sang tuyến tính), hằng màu viết tay đổi bằng GammaToLinearSpace.
Shader "PokiClash/UIPondWater"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _WaterTex ("Nước (R), khoảng cách bờ (G)", 2D) = "black" {}
        _FoamCol ("Màu bọt, gợn", Color) = (0.97,0.99,1,1)
        _LightCol ("Màu vệt sáng", Color) = (0.72,0.93,1,1)
        _ShadowCol ("Màu bóng cá (nhân)", Color) = (0.16,0.32,0.55,1)
        _Wobble ("Lăn tăn (px)", Float) = 2.6
        _PlateSize ("Cỡ ảnh nền gốc (px)", Vector) = (1024,1536,0,0)
        _Now ("Đồng hồ gợn (giây, code đặt)", Float) = 0

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
            sampler2D _WaterTex;
            float4 _WaterTex_TexelSize;
            fixed4 _FoamCol, _LightCol, _ShadowCol;
            float _Wobble, _Now;
            float4 _PlateSize;
            float4 _Rip[8];
            float4 _Fish[6];
            float4 _FishB[6];
            float4 _Bob;
            float4 _Wake;

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
            // vạch mép cứng quanh d = r, dày w px (khử răng cưa 1 px)
            float band(float d, float r, float w) { return 1.0 - smoothstep(w * 0.5 - 0.6, w * 0.5 + 0.6, abs(d - r)); }

            fixed4 frag(v2f IN) : SV_Target
            {
                // cỡ ảnh nền gốc cố định (không lấy _WaterTex_TexelSize: Unity có thể giãn ảnh lên lũy thừa 2 khi nhập)
                float2 size = _PlateSize.xy;
                float2 p = IN.texcoord * size;          // px ảnh nền gốc
                float4 m = tex2D(_WaterTex, IN.texcoord);
                float water = saturate((m.r - 0.35) / 0.3);
                float d = m.g * 48.0;
                float t = _Time.y;

                // 1. lăn tăn hai tầng + khúc xạ quanh phao
                float2 uv = IN.texcoord;
                float2 qb = (p - _Bob.xy) * float2(1.0, 1.0 / 0.55);
                float db = length(qb);
                if (water > 0.0)
                {
                    float calm = smoothstep(5.0, 18.0, d) * water;
                    float2 o1 = float2(vn(p * 0.022 + float2(t * 0.35, 0)), vn(p * 0.022 + float2(7.3, -t * 0.3))) - 0.5;
                    float2 o2 = float2(vn(p * 0.07 + float2(-t * 0.8, 3.1)), vn(p * 0.07 + float2(1.7, t * 0.9))) - 0.5;
                    float2 off = (o1 * 1.6 + o2 * 0.7) * _Wobble;
                    if (_Bob.w > 0.0 && db < 70.0)
                    {
                        float k = sin(db * 0.32 - t * 6.0) * (1.0 - db / 70.0) * 2.2;
                        off += normalize(qb + 0.001) * k;
                    }
                    uv += off * calm / size;
                }
                half4 color = (tex2D(_MainTex, uv) + _TextureSampleAdd) * IN.color;
                if (water <= 0.0)
                {
                    #ifdef UNITY_UI_CLIP_RECT
                    color.a *= UnityGet2DClipping(IN.worldPosition.xy, _ClipRect);
                    #endif
                    return color;
                }

                // 2. vệt sáng chạy theo sóng
                {
                    float warp = vn(p * 0.008 + float2(t * 0.05, 0)) * 7.0 + vn(p * 0.02) * 2.0;
                    float s1 = sin(p.y * 0.075 + warp + t * 1.3);
                    float s2 = sin(p.y * 0.11 - p.x * 0.02 + warp * 1.3 - t * 0.9);
                    float br = step(0.42, vn(p * float2(0.03, 0.09) + float2(t * 0.25, 0)));
                    float streak = max(step(0.955, s1), step(0.965, s2) * 0.8) * br * smoothstep(10.0, 22.0, d);
                    color.rgb = lerp(color.rgb, _LightCol.rgb, streak * 0.55);
                }

                // 3. bóng cá
                float sh = 0.0;
                [unroll] for (int i = 0; i < 6; i++)
                {
                    float a = _FishB[i].x;
                    if (a <= 0.001) continue;
                    float L = max(_Fish[i].w, 1.0);
                    float2 q = p - _Fish[i].xy;
                    q.y /= 0.8;
                    float cs = cos(_Fish[i].z), sn = sin(_Fish[i].z);
                    float2 l = float2(q.x * cs - q.y * sn, q.x * sn + q.y * cs);
                    float tailK = saturate(-l.x / (0.5 * L));
                    l.y -= sin(t * 7.0 + _FishB[i].y + l.x * 0.07) * 0.07 * L * tailK;
                    float body = length(float2(l.x / (0.5 * L), l.y / (0.2 * L)));
                    float bodyA = 1.0 - smoothstep(1.0 - 1.2 / L, 1.0 + 1.2 / L, body);
                    float tx = -l.x - 0.42 * L;
                    float tailA = step(0.0, tx) * step(tx, 0.34 * L) * (1.0 - smoothstep(-0.8, 0.8, abs(l.y) - (0.12 * L + tx * 0.75)));
                    sh = max(sh, max(bodyA, tailA) * a);
                }
                color.rgb = lerp(color.rgb, color.rgb * _ShadowCol.rgb, saturate(sh) * 0.55 * water);

                float foam = 0.0;
                // 4. vệt sóng trôi (ô 80 x 52 px)
                {
                    float2 cell = float2(80.0, 52.0);
                    float2 pp = p + float2(t * 9.0, sin(t * 0.7) * 3.0);
                    float2 id = floor(pp / cell);
                    float2 lc = pp - id * cell - (0.25 + 0.5 * float2(h21(id), h21(id + 17.0))) * cell;
                    float s = frac(t * 0.22 + h21(id + 5.0));
                    float vis = step(s, 0.7) * smoothstep(0.0, 0.07, s) * (1.0 - smoothstep(0.55, 0.7, s));
                    float len = 12.0 + 9.0 * h21(id + 9.0);
                    float y = sin(lc.x * 0.28 + t * 2.0) * 2.6;
                    float mark = step(abs(lc.x), len) * (1.0 - smoothstep(0.8, 1.8, abs(lc.y - y)));
                    foam = max(foam, mark * vis * 0.85 * smoothstep(12.0, 20.0, d));
                }
                // 5. bọt vỗ bờ
                {
                    float w = 0.5 + 0.5 * sin(t * 1.6 + vn(p * 0.012) * 6.283);
                    float reach = 3.0 + w * 9.0;
                    float edge = band(d, reach, 2.8) * step(0.3, vn(p * 0.06 + float2(t * 0.06, 0)));
                    float wash = (1.0 - smoothstep(reach - 0.8, reach + 0.8, d)) * 0.5 * (0.7 + 0.3 * step(0.5, frac((p.x + p.y) * 0.2)));
                    float outer = band(d, reach + 10.0, 2.0) * step(0.5, vn(p * 0.05 - float2(t * 0.05, 0))) * 0.65;
                    foam = max(foam, max(edge, max(wash, outer)));
                }
                // 6. phao: nước sẫm dưới phao, vòng nước bám, gợn toả liên tục
                if (_Bob.w > 0.0)
                {
                    float sink = _Bob.z;
                    float rr = 15.0 + sink * 5.0;
                    color.rgb = lerp(color.rgb, color.rgb * _ShadowCol.rgb, (1.0 - smoothstep(rr - 1.0, rr + 1.0, db)) * 0.35 * _Bob.w);
                    foam = max(foam, band(db, rr + 1.5, 3.0) * 0.95 * _Bob.w);
                    [unroll] for (int j = 0; j < 3; j++)
                    {
                        float f = frac(t * 0.5 + j / 3.0);
                        float r = rr + 6.0 + f * 78.0;
                        foam = max(foam, band(db, r, 2.2) * (1.0 - f) * 0.75 * _Bob.w);
                    }
                }
                // 7. vệt rẽ nước chữ V sau vật đang chạy
                if (_Wake.w > 0.0)
                {
                    float2 q = p - _Wake.xy;
                    q.y /= 0.6;
                    float cs = cos(-_Wake.z), sn = sin(-_Wake.z);
                    float2 l = float2(q.x * cs - q.y * sn, q.x * sn + q.y * cs);   // trục x theo hướng chạy
                    float back = -l.x;
                    if (back > 0.0 && back < 170.0)
                    {
                        float fade = (1.0 - back / 170.0) * _Wake.w;
                        float wob = sin(back * 0.18 - t * 9.0) * 1.5;
                        float arm = band(abs(l.y) + wob, back * 0.42 + 4.0, 2.6);
                        float arm2 = band(abs(l.y) - wob, back * 0.25 + 2.0, 2.0) * step(20.0, back) * 0.7;
                        foam = max(foam, max(arm, arm2) * fade);
                    }
                }
                // 8. gợn tròn sự kiện
                [unroll] for (int k = 0; k < 8; k++)
                {
                    float age = _Now - _Rip[k].z;
                    if (_Rip[k].w <= 0.0 || age < 0.0 || age > 1.8) continue;
                    float2 q = p - _Rip[k].xy;
                    q.y /= 0.55;
                    float dd = length(q);
                    float r = 10.0 + age * 70.0 * (0.7 + 0.3 * _Rip[k].w);
                    float fade = (1.0 - age / 1.8) * saturate(_Rip[k].w);
                    float ring = max(band(dd, r, 3.0), band(dd, r * 0.62, 2.2) * step(0.2, age) * 0.85);
                    ring = max(ring, band(dd, r * 0.35, 1.8) * step(0.45, age) * 0.6);
                    foam = max(foam, ring * fade);
                }
                color.rgb = lerp(color.rgb, _FoamCol.rgb, saturate(foam) * water);

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
