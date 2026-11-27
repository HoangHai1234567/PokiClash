// Biển của Nhà theo cách Clash of Critters (GD_Claude/22_Critters_Home.md mục 4), vẽ trên ảnh nền home_base (Image uGUI).
// _SeaTex (ArtGen/Home/sea/make_home_sea.py, cùng khung ảnh nền): R dải mờ rộng, G dải vừa, B dải sắc sát bờ (1 ở bờ), A vùng biển được tô.
// Màu biển: sâu → sóng theo R; dải mép giữa G và B; vân sáng dưới nước (_CausticTex) trôi theo nhiễu; vạch bọt B lệch theo nhiễu nhỏ.
// Nhiễu dòng chảy (_FlowTex) lấy theo uv xoay _Angle, trôi theo thời gian, làm các dải lắc lư và chạy vào bờ.
// Khác Critters: _Crisp cắt bọt và dải mép thành mép sắc (luật UI: không quầng sáng); _Steps chia dải màu thành bậc phẳng (0 = mềm);
// _Grain giữ nét chì của biển vẽ tay (nhân độ sáng ảnh nền chia _PaperLum); đêm (_PokiNight, DayNight đặt) tối dần ra xa bờ.
// Biển như sảnh (người dùng 2026-11-27: nước quanh Nhà phải giống sảnh, đảo Casino cho liền mạch khi đi tàu): _TileMix = 1 lấy màu nước
// từ ảnh biển lát của sảnh (_TileTex = Islands/sanh_bien, lặp _TileST lần trên ảnh nền để vân sóng cùng cỡ như sảnh: ảnh nền
// 6975 x 4198 đơn vị màn, ô lát 1024), bỏ màu tính, vân, nét chì ảnh nền; giữ dải mép sáng (_EdgeCol.a) và vạch bọt sát bờ
// (_FoamAlpha) mảnh, nhạt. Sảnh, đảo Casino (lớp bien_bo dưới các đảo, Editor/ShoreWaveMenu.cs) dùng lại shader này: _TileST.zw lệch ô
// cho khớp lớp biển lát sẵn có của màn.
// Biển chung (người dùng 2026-11-27 "nước của 3 đảo phải liền mạch"; App/SeaAnchor.cs): _TileWorld = 1 thì ô lát lấy theo vị trí thế giới
// với gốc, cỡ ô toàn cục _PokiSeaO (như PokiClash/UISeaWorld của lớp biển mở), bỏ _TileST: biển trong ảnh, sóng bờ, biển mở, chuyến tàu
// cùng một mặt nước.
// Nước trong đảo (_RiverTex, cùng script sinh): vệt bọt trôi theo hướng chảy trên thác, suối vẽ sẵn (thay thác hoạt hình 4 khung của Critters).
Shader "PokiClash/UIHomeSea"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        _Color ("Tint", Color) = (1,1,1,1)
        _SeaTex ("Mặt nạ bờ: R rộng, G vừa, B sắc, A vùng biển", 2D) = "black" {}
        _FlowTex ("Nhiễu dòng chảy (RG, lặp)", 2D) = "gray" {}
        _CausticTex ("Vân sáng dưới nước (G, lặp)", 2D) = "black" {}
        _BaseCol ("Màu nước sâu", Color) = (0.31,0.655,0.89,1)
        _WaveCol ("Màu nước gần bờ", Color) = (0.435,0.788,0.933,1)
        _EdgeCol ("Màu dải mép", Color) = (0.624,0.89,0.949,1)
        _FoamCol ("Màu bọt", Color) = (0.949,0.992,1,1)
        _CausticCol ("Màu vân (cộng thêm)", Color) = (0.06,0.07,0.07,1)
        _Angle ("Góc xoay nhiễu (rad)", Float) = 0.61
        _SpeedX ("Tốc trôi nhiễu X", Float) = 1
        _SpeedY ("Tốc trôi nhiễu Y", Float) = 4
        _FlowScale ("Lặp nhiễu cho dải", Float) = 2
        _FlowFine ("Lặp nhiễu cho bọt (xy)", Vector) = (6,3,0,0)
        _Move ("Lắc dải theo nhiễu", Float) = 0.055
        _FoamMove ("Lắc bọt theo nhiễu", Float) = 0.01
        _CausticST ("Lặp vân (xy)", Vector) = (5,3,0,0)
        _GStr ("Lắc vân theo nhiễu", Float) = 0.3
        _Crisp ("Mép sắc (0 mềm như Critters, 1 sắc)", Range(0,1)) = 1
        _FoamCut ("Ngưỡng vạch bọt", Range(0,1)) = 0.5
        _EdgeCut ("Ngưỡng dải mép", Range(0,1)) = 0.22
        _Steps ("Số bậc màu nước (0 = mềm)", Float) = 0
        _Grain ("Giữ nét chì biển vẽ tay", Range(0,1)) = 0.55
        _PaperLum ("Độ sáng trung bình biển vẽ tay (tuyến tính)", Float) = 0.522
        _RiverTex ("Nước trong đảo: R vùng, GB hướng, A tốc", 2D) = "black" {}
        _TileTex ("Ảnh biển lát như sảnh (Islands/sanh_bien)", 2D) = "white" {}
        _TileST ("Số lần lặp ảnh biển lát trên ảnh (xy), lệch ô (zw)", Vector) = (6.81,4.1,0,0)
        _TileMix ("Dùng ảnh biển lát (0 màu tính, 1 như sảnh)", Range(0,1)) = 1
        _TileWorld ("Ô lát theo thế giới (biển chung _PokiSeaO)", Float) = 0
        _FoamAlpha ("Độ đậm vạch bọt", Range(0,1)) = 0.55
        _RiverSpeed ("Tốc vệt nước chảy (px ảnh nền / giây)", Float) = 70
        _RiverFoam ("Độ đậm vệt nước chảy", Range(0,1)) = 0.6

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
                float2 wpos : TEXCOORD2;
                UNITY_VERTEX_OUTPUT_STEREO
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _Color;
            fixed4 _TextureSampleAdd;
            float4 _ClipRect;
            sampler2D _SeaTex, _FlowTex, _CausticTex, _RiverTex, _TileTex;
            float4 _TileST;
            float _TileMix, _FoamAlpha, _TileWorld;
            float4 _PokiSeaO; // toàn cục (SeaAnchor / chuyến tàu): xy gốc thế giới, zw = 1 / cỡ ô thế giới
            float _RiverSpeed, _RiverFoam;
            float4 _SeaTex_TexelSize;
            half4 _BaseCol, _WaveCol, _EdgeCol, _FoamCol, _CausticCol;
            float _Angle, _SpeedX, _SpeedY, _FlowScale, _Move, _FoamMove, _GStr, _Crisp, _FoamCut, _EdgeCut, _Steps, _Grain, _PaperLum;
            float4 _FlowFine, _CausticST;
            float _PokiNight; // toàn cục, DayNight đặt: 0 ngày, 1 đêm

            v2f vert(appdata_t v)
            {
                v2f OUT;
                UNITY_SETUP_INSTANCE_ID(v);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);
                OUT.worldPosition = v.vertex;
                OUT.vertex = UnityObjectToClipPos(OUT.worldPosition);
                OUT.wpos = mul(unity_ObjectToWorld, v.vertex).xy;
                OUT.texcoord = TRANSFORM_TEX(v.texcoord, _MainTex);
                OUT.color = v.color * _Color;
                return OUT;
            }

            // crisp 0: giữ dải mềm; 1: mép sắc quanh ngưỡng c
            half cut(half x, half c)
            {
                half hard = smoothstep(c - 0.035, c + 0.035, x);
                return lerp(x, hard, _Crisp);
            }

            fixed4 frag(v2f IN) : SV_Target
            {
                half4 color = (tex2D(_MainTex, IN.texcoord) + _TextureSampleAdd) * IN.color;
                float2 uv = IN.texcoord;
                half4 m0 = tex2D(_SeaTex, uv);
                if (m0.a > 0.004)
                {
                    float t = _Time.y / 20.0;
                    float2 tt = t * float2(_SpeedX, _SpeedY);
                    // uv xoay theo _Angle, vuông theo tỉ lệ ảnh (Critters dùng tỉ lệ màn hình cho tấm biển của họ)
                    float2 asp = max(float2(_SeaTex_TexelSize.z / _SeaTex_TexelSize.w, _SeaTex_TexelSize.w / _SeaTex_TexelSize.z), 1.0);
                    float2 c = (uv - 0.5) * asp;
                    float s = sin(_Angle), co = cos(_Angle);
                    float2 rot = float2(co * c.x - s * c.y, s * c.x + co * c.y) + 0.5;
                    half2 nA = tex2D(_FlowTex, uv * _FlowFine.xy + tt).xy - 0.5;
                    half2 nB = tex2D(_FlowTex, rot * _FlowScale + tt).xy - 0.5;

                    half bot0 = tex2D(_SeaTex, uv + nA * _FoamMove).b;   // vạch bọt sát bờ
                    half bot = cut(bot0, _FoamCut);
                    half2 rg = tex2D(_SeaTex, uv + nB * _Move).rg;      // R rộng, G vừa
                    half rw = rg.r;
                    if (_Steps > 0.5)
                    {
                        half k = rw * _Steps;
                        rw = (floor(k) + smoothstep(0.45, 0.55, frac(k))) / _Steps;
                    }
                    half3 sea = lerp(_BaseCol.rgb, _WaveCol.rgb, rw);
                    half edge = cut(saturate(rg.g - bot0), _EdgeCut) * (1.0 - bot);
                    half band2 = saturate(rg.r * rg.r - bot0 - edge);
                    sea = lerp(sea, _EdgeCol.rgb, edge * _EdgeCol.a);
                    half cg = tex2D(_CausticTex, uv * _CausticST.xy + nB.x * _GStr).g;
                    sea += cg * (1.0 - band2) * _CausticCol.rgb;
                    // nét chì của biển vẽ tay: nhân độ sáng ảnh nền so với độ sáng trung bình của biển vẽ
                    half lum = dot(color.rgb, half3(0.3333, 0.3333, 0.3334));
                    sea *= 1.0 + (lum / max(_PaperLum, 0.001) - 1.0) * _Grain;
                    // biển như sảnh: màu từ ảnh biển lát (lặp theo frac, lấy mip theo uv liền để khỏi lộ đường nối), giữ dải mép
                    if (_TileMix > 0.001)
                    {
                        float2 tuv = _TileWorld > 0.5 ? (IN.wpos - _PokiSeaO.xy) * _PokiSeaO.zw : uv * _TileST.xy + _TileST.zw;
                        half3 tile = tex2Dgrad(_TileTex, frac(tuv), ddx(tuv), ddy(tuv)).rgb;
                        sea = lerp(sea, lerp(tile, _EdgeCol.rgb, edge * _EdgeCol.a), _TileMix);
                    }
                    sea = lerp(sea, _FoamCol.rgb, bot * _FoamAlpha);
                    // đêm: tối dần ra xa bờ, sát bờ giữ sáng (như UIInkWater)
                    half3 seaNight = half3(0.56, 0.62, 0.84);
                    #ifndef UNITY_COLORSPACE_GAMMA
                    seaNight = GammaToLinearSpace(seaNight);
                    #endif
                    sea *= lerp(half3(1, 1, 1), seaNight, _PokiNight * (1.0 - rg.g));
                    color.rgb = lerp(color.rgb, sea, m0.a);
                }

                // thác, suối (thay thác 4 khung của Critters): vệt bọt dài trôi theo hướng chảy, mép sắc; lòng hồ (tốc 0) đứng yên
                half4 rv = tex2D(_RiverTex, uv);
                if (rv.r > 0.5 && rv.a > 0.02)
                {
                    float2 d = rv.gb * 2.0 - 1.0;                                 // hướng theo ảnh, y xuống
                    d /= max(length(d), 0.001);
                    float2 pB = float2(uv.x, 1.0 - uv.y) * _SeaTex_TexelSize.zw * 2.0; // px ảnh nền (mặt nạ nửa cỡ)
                    float along = dot(pB, d), across = dot(pB, float2(-d.y, d.x));
                    float tt2 = _Time.y * _RiverSpeed * rv.a;
                    // nhiễu _FlowTex có hạt cỡ 1/5 ô lặp: lặp 40 px ngang dòng, 200 px dọc dòng → vệt rộng khoảng 8 px, dài khoảng 40 px
                    half n1 = tex2D(_FlowTex, float2(across / 40.0, (along - tt2) / 200.0)).r;
                    half n2 = tex2D(_FlowTex, float2(across / 28.0 + 0.37, (along - tt2 * 1.3) / 130.0)).g;
                    half streak = max(smoothstep(0.66, 0.71, n1), smoothstep(0.7, 0.75, n2) * 0.7);
                    color.rgb = lerp(color.rgb, _FoamCol.rgb, streak * _RiverFoam * saturate(rv.a * 3.0));
                }

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
