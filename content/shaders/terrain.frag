#version 150

//Fragment


uniform sampler2D p3d_Texture0;
uniform sampler2D p3d_Texture1;
uniform sampler2D p3d_Texture2;
uniform sampler2D p3d_Texture3;
uniform sampler2D Heightmap;

// Input from vertex shader
in vec2 texcoord0;
in vec2 texcoord1;
in vec2 texcoord2;
in vec2 texcoord3;

in vec4 vertex;

// Output to the screen
out vec4 p3d_FragColor;

void main() {
  vec4 color = texture(p3d_Texture2, texcoord2);
  //p3d_FragColor = color.rgba;
  vec4 texel0 = texture2D(p3d_Texture0, texcoord0.st).rgba;
  vec4 texel1 = texture2D(p3d_Texture1, texcoord1.st).rgba;
  vec4 texel2 = texture2D(p3d_Texture2, texcoord2.st).rgba;
  vec4 texel3 = texture2D(p3d_Texture3, texcoord3.st).rgba;
  //vec4 heightMapTexel = texture2D(Heightmap,vertex.xz/(2*500.0)).rgba;
  vec4 heightMapTexel = texture2D(Heightmap,texcoord0.st);

  p3d_FragColor = mix(texel1,texel3,heightMapTexel.b);
}

