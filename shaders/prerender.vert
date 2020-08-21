#version 120

varying vec3 normal;
varying vec3 position;
varying vec4 color;
varying float depth;
uniform vec4 osg_MaterialDiffuseColor;
uniform vec4 osg_MaterialAmbientColor;

void main()
{
    color = osg_MaterialDiffuseColor + osg_MaterialAmbientColor;
    normal = normalize((gl_ModelViewMatrix * vec4(gl_Normal.xyz,0)).xyz);
    vec4 inPos = vec4(gl_Vertex.xyz, 1);
    position = (gl_ModelViewMatrix * inPos).xyz;
    depth = -position.z;

    // Calculate vertex position in clip coordinates
    gl_Position = gl_ModelViewProjectionMatrix * inPos;
}