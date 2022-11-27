#version 150

//Fragment


uniform sampler2D p3d_Texture0;
uniform sampler2D p3d_Texture1;
uniform sampler2D Heightmap;

// Input from vertex shader
in vec2 texcoord0;
in vec2 texcoord1;

in vec4 vertex;

// Output to the screen
out vec4 p3d_FragColor;

void main() {
  vec4 texel0 = texture2D(p3d_Texture0, texcoord0.st).rgba;
  vec4 texel1 = texture2D(p3d_Texture1, texcoord1.st).rgba;
  vec4 heightMapTexel = texture2D(Heightmap,texcoord0.st);

  p3d_FragColor = mix(texel0,texel1,heightMapTexel.b);
}

