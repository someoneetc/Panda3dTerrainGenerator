#version 150

//Fragment


uniform int TexScaleFactor0;
uniform int TexScaleFactor1;
uniform int TexScaleFactor2;
uniform int TexScaleFactor3;

uniform sampler2D p3d_Texture0;
uniform sampler2D p3d_Texture1;
uniform sampler2D p3d_Texture2;
uniform sampler2D p3d_Texture3;

uniform sampler2D Heightmap;
uniform sampler2D SlopeImage;

// Input from vertex shader
in vec2 texcoord0;
in vec2 texcoord1;
in vec2 texcoord2;
in vec2 texcoord3;

in vec4 vertex;

// Output to the screen
out vec4 p3d_FragColor;

struct TerrainRegion
{
    float min;
    float max;
};

float computeWeight(TerrainRegion terrainRegion, vec4 vertex){
    float regionRange = terrainRegion.max - terrainRegion.min;
    return max(0.0,(regionRange - abs(vertex.z - terrainRegion.max)) / regionRange);
}

void main() {
  vec4 texel0 = texture2D(p3d_Texture0, texcoord0.st * TexScaleFactor0).rgba;
  vec4 texel1 = texture2D(p3d_Texture1, texcoord1.st * TexScaleFactor1).rgba;
  vec4 texel2 = texture2D(p3d_Texture2, texcoord2.st * TexScaleFactor2).rgba;
  vec4 texel3 = texture2D(p3d_Texture3, texcoord3.st * TexScaleFactor3).rgba;

  vec4 heightMapTexel = texture2D(Heightmap,texcoord0.st);
  vec4 slopeImageTexel = texture2D(SlopeImage,texcoord0.st);

  //texel0 = mix(texel0,texel1,heightMapTexel);
  //texel0 = mix(texel0,texel2,slopeImageTexel);

  float scale = 500.0;
  float w0 = 0.0, w1 = 0.0, w2 = 0.0, w3 = 0.0;
  vec4 terrainColor = vec4(0.0,0.0,0.0,0.0);

  TerrainRegion dirtRegion;
  dirtRegion.min = -100.0/scale;
  dirtRegion.max = 0.0/scale;
  w0 = computeWeight(dirtRegion,vertex);

  TerrainRegion grassRegion;
  grassRegion.min = 1.0/scale;
  grassRegion.max = 200.0/scale;
  w1 = computeWeight(grassRegion,vertex);


  TerrainRegion rockRegion;
  rockRegion.min = 201.0/scale;
  rockRegion.max = 400.0/scale;
  w2 = computeWeight(rockRegion,vertex);

  TerrainRegion snowRegion;
  snowRegion.min = 401.0/scale;
  snowRegion.max = 500.0/scale; 
  w3 = computeWeight(snowRegion,vertex);

  terrainColor = texel0 * w0 + texel1 * w1 + texel2 * w2 + texel3 * w3;


  p3d_FragColor = terrainColor; 
}

