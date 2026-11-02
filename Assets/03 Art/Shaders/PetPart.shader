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
    }

    SubShader
    {
        Tags { "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent" "PreviewType"="Plane" }
        Cull Off
        Lighting Off
        ZWrite Off
        Blend [_SrcBlend] [_DstBlend]

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
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

            sampler2D _MainTex;
            fixed4 _Add;

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
                fixed4 t = tex2D(_MainTex, i.uv);
                fixed4 c;
                c.rgb = saturate(t.rgb * i.color.rgb + _Add.rgb);
                c.a = t.a * i.color.a;
                return c;
            }
            ENDCG
        }
    }
}
