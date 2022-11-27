#version 150

//Fragment

uniform int TexScaleFactor0;
uniform int TexScaleFactor1;
uniform int TexScaleFactor2;

uniform sampler2D p3d_Texture0;
uniform sampler2D p3d_Texture1;
uniform sampler2D p3d_Texture2;

uniform sampler2D Heightmap;
uniform sampler2D SlopeImage;

// Input from vertex shader
in vec2 texcoord0;
in vec2 texcoord1;
in vec2 texcoord2;

in vec4 vertex;

// Output to the screen
out vec4 p3d_FragColor;

void main() {
  vec4 texel0 = texture2D(p3d_Texture0, texcoord0.st * TexScaleFactor0).rgba;
  vec4 texel1 = texture2D(p3d_Texture1, texcoord1.st * TexScaleFactor1).rgba;
  vec4 texel2 = texture2D(p3d_Texture2, texcoord2.st * TexScaleFactor2).rgba;
  vec4 heightMapTexel = texture2D(Heightmap,texcoord0.st);
  vec4 slopeImageTexel = texture2D(SlopeImage,texcoord0.st);

  texel0 = mix(texel0,texel1,heightMapTexel.b);
  texel0 = mix(texel0,texel2,slopeImageTexel.b);
  p3d_FragColor = texel0; 
}

