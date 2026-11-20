// Một mảnh hình tướng aola (bản dev, AolaActor): màu = ảnh × màu đỉnh (nhân của color transform Flash, alpha) + _Add
// (phần cộng, 0..1), như colorTransform của SWF. _SrcBlend/_DstBlend: thường (SrcAlpha, OneMinusSrcAlpha) hoặc cộng
// (SrcAlpha, One) cho mảnh blend "add"/"screen"; AolaActor giữ hai material, _Add đặt qua MaterialPropertyBlock.
Shader "PokiClash/PetPart"
{
    Properties
    {
        [PerRendererData] _MainTex ("Texture", 2D) = "white" {}
        [PerRendererData] _Add ("Màu cộng", Color) = (0,0,0,0)
        [HideInInspector] _SrcBlend ("Src", Float) = 5
        [HideInInspector] _DstBlend ("Dst", Float) = 10
        [HideInInspector] _SrcBlendA ("Src alpha", Float) = 1
        [HideInInspector] _DstBlendA ("Dst alpha", Float) = 10
    }

    SubShader
    {
        Tags { "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent" "PreviewType"="Plane" }
        Cull Off
        Lighting Off
        ZWrite Off
        // Kênh ALPHA trộn riêng (One, OneMinusSrcAlpha): tướng vẽ ra RenderTexture nền trong suốt rồi shader viền sticker đọc lại. Trộn
        // alpha bằng (SrcAlpha, OneMinusSrcAlpha) như màu thì chỗ một mảnh có điểm nửa trong (mép mờ, khử răng cưa) đè lên mảnh đặc,
        // alpha của RT tụt xuống a*a + (1 - a) < 1: RT "thủng", sticker lấp giấy trắng vào → vệt sáng ở MỌI khớp nối của mọi tướng
        // (người dùng 2026-11-12). Với (One, OneMinusSrcAlpha) alpha = a + dst*(1 - a): đúng độ phủ, màu trong RT là màu đã nhân alpha
        // như StickerOutline giả định. Mảnh blend cộng giữ cách cũ (AolaActor đặt _SrcBlendA/_DstBlendA).
        Blend [_SrcBlend] [_DstBlend], [_SrcBlendA] [_DstBlendA]

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma target 3.5
            #include "UnityCG.cginc"

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
            };

            Texture2D _MainTex;
            SamplerState sampler_MainTex;
            fixed4 _Add;

            // Lọc khi thu nhỏ (người dùng 2026-11-20: tướng ở màn Nhà "bị vỡ"): atlas không có mipmap (nhẹ APK), tướng nhỏ trên màn
            // (màn Nhà ~150 điểm RT cho dáng đứng, atlas tới 800 điểm) thì một lần lấy mẫu song tuyến bỏ sót nét mực, ra lấm tấm, đứt
            // nét. Ô điểm ảnh phủ quá 1,4 điểm atlas thì lấy n x n điểm rải đều trong ô (n <= 4), cộng theo alpha (nhân trước) rồi chia
            // lại. Hình to hơn atlas (sân đấu gần 1:1, xem tướng) thì n = 1, như cũ.
            fixed4 SampleAA(float2 uv)
            {
                float w, h;
                _MainTex.GetDimensions(w, h);
                float2 dx = ddx(uv), dy = ddy(uv);
                float2 sz = float2(w, h);
                float fp = max(length(dx * sz), length(dy * sz)); // điểm atlas trên một điểm ảnh
                int n = (int)clamp(ceil(fp / 1.4), 1, 4);
                if (n == 1) return _MainTex.SampleLevel(sampler_MainTex, uv, 0);
                float4 acc = 0;
                float inv = 1.0 / n;
                [loop] for (int a = 0; a < n; a++)
                {
                    [loop] for (int b = 0; b < n; b++)
                    {
                        float2 o = ((a + 0.5) * inv - 0.5) * dx + ((b + 0.5) * inv - 0.5) * dy;
                        float4 t = _MainTex.SampleLevel(sampler_MainTex, uv + o, 0);
                        acc += float4(t.rgb * t.a, t.a);
                    }
                }
                acc *= inv * inv;
                return fixed4(acc.a > 1e-4 ? acc.rgb / acc.a : 0, acc.a);
            }

            v2f vert(appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                o.color = v.color;
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                fixed4 t = SampleAA(i.uv);
                fixed4 c;
                c.rgb = saturate(t.rgb * i.color.rgb + _Add.rgb);
                c.a = t.a * i.color.a;
                return c;
            }
            ENDCG
        }
    }
}
