import math
import json
import random
from PIL import Image
import numpy
import noise
import time

import yaml
import os 

from panda3d.core import GeoMipTerrain, TextureStage, TexGenAttrib, Shader

def loadTerrain(path):

    #load terrain data
    terrain_file = open(os.path.join(path,'map.json'))
    terrain_data = json.loads(terrain_file.read())
    terrain_file.close()

    #Generate the terrain using GeoMipTerrain
    terrain = GeoMipTerrain('terrain')
    terrain.setHeightfield(terrain_data['heightmap'])
    terrain.setBruteforce(True)
    tRoot = terrain.getRoot()
    tRoot.setTexGen(TextureStage.getDefault(),TexGenAttrib.MWorldPosition)
    tRoot.setTexScale(TextureStage.getDefault(),1.0/terrain_data['shape'][0],1.0/terrain_data['shape'][1])
    tRoot.setScale(1,1,terrain_data["z_scale"])
    terrain.generate()

    ts_idx = 0
    for texture in terrain_data['textures']:
        ts = TextureStage('gnd' + str(ts_idx))
        ts.setSort(ts_idx)
        tRoot.setTexture(ts,loader.loadTexture(terrain_data['textures'][ts_idx]))
        ts_idx+=1


    tRoot.setShaderInput("Heightmap",loader.loadTexture(terrain_data['heightmap']))
    shader = Shader.load(vertex=terrain_data['vertex_shader'],
                         fragment=terrain_data['fragment_shader'],
                         lang=Shader.SL_GLSL)

    tRoot.setShader(shader)
    terrain.update()

    return terrain, tRoot


MAPMAKER_PATH = 'mapmaker/build/bin/mapmaker/mapmaker'
SHADERS = 'shaders'

def generateTerrain(shape,z_scale,texture_paths,path):
    heightmap_path = os.path.join(path,"heightmap.pnm")
    json_path = os.path.join(path,"map.json")
    if os.path.exists(path):
        print(repr(path), " directory already exists!")
        return
    os.mkdir(path)
    with open('tmp.yml','w+') as inputFile:
        """
        cfg = {
            'seed': int(time.time()),
            'generator': {
                'name': "fractal",
                'parameters':{
                    'noise': 'gradient',
                    'noise_parameters':{
                        'curve': 'cubic'
                    },
                    'scale': 1,
                    'octaves': 10,
                    'lacunarity': 2.0,
                    'persistence': 0.5
                },
                'size': {
                    'width': shape[0]+1,
                    'height': shape[1]+1
                },
                'output':{
                    'type': 'grayscale',
                    'parameters':{
                        'sea_level': 0.5,
                        'shaded': False 
                    },
                    'filename': heightmap_path 
                },
                'finalizer':{
                    'name': 'playability',
                    'parameters':{
                        'sea_level': 0.5,
                        'unit_size': 1,
                        'building_size': 9,
                        'unit_talus': 8.0,
                        'building_talus': 2.0,
                        'output_intermediates': False
                    }
                }
            }
        }"""
        cfg = {
            'generator': {
                'name': 'diamond-square',
                'parameters': {
                    'values': [0,20,40,100]
                },
                'size':{
                    'width': shape[0],
                    'height': shape[1]
                },
                'output':{
                    'type': 'grayscale',
                    'parameters':{
                        'sea_level': 0,
                        'shaded': False 
                    },
                    'filename': heightmap_path 
                },

            }
        }
        inputFile.write(yaml.dump(yaml.safe_load(str(cfg))))
    os.system(MAPMAKER_PATH + ' ./tmp.yml')

    #generate json
    json_data = {
                'heightmap': heightmap_path,
                'shape': shape,
                'z_scale': z_scale,
                'textures': texture_paths,
                'vertex_shader': os.path.join(SHADERS,'terrain.vert'),
                'fragment_shader': os.path.join(SHADERS,'terrain.frag'),
            }

    json_file = open(json_path,"w+")
    json_file.write(json.dumps(json_data,indent=4))
    json_file.close()
