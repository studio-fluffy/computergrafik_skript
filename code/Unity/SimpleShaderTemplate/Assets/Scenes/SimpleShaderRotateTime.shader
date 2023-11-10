Shader "Unlit/SimpleShaderRotateTime"
{
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
            };

            struct v2f
            {
                float4 vertex : SV_POSITION;
                fixed2 uv: TEXCOORD0;
            };

            static const float PI = 3.14159265f;
            uniform float _time;


            v2f vert (appdata v)
            {
                v2f o;
                o.uv.x = 0.5;
                o.uv.y = 1.0;

                float alpha = fmod(_time, PI * 2);

                
                float4x4 rotation = float4x4(
                    cos(alpha), 0, -sin(alpha), 0,
                    0, 1, 0, 0,
                    sin(alpha), 0, cos(alpha), 0,
                    0, 0, 0, 1
                );

                v.vertex = mul(alpha, v.vertex);
                
                o.vertex = UnityObjectToClipPos(v.vertex);

                return o;
            }


            fixed4 frag (v2f i) : SV_Target
            {
                
                return float4(i.uv.x, 0.0, 0.0, 1.0);
            }
            ENDCG
        }
    }
}
