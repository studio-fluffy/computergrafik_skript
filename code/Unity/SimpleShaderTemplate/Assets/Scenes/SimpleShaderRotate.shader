// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

Shader "Unlit/SimpleShaderRotate"
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
            };


            v2f vert (appdata v)
            {
                v2f o;

                float alpha = 2.0;

                
                float4x4 rotation = float4x4(
                    cos(alpha), 0, -sin(alpha), 0,
                    0, 1, 0, 0,
                    sin(alpha), 0, cos(alpha), 0,
                    0, 0, 0, 1
                );

                v.vertex = mul(rotation, v.vertex);
                
                o.vertex = UnityObjectToClipPos(v.vertex);

                return o;
            }


            fixed4 frag (v2f i) : SV_Target
            {
                return float4(0.0, 0.0, 1.0, 1.0);
            }
            ENDCG
        }
    }
}
