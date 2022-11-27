import math
import shutil
import json
import random
from PIL import Image
import numpy
import noise
import time

import yaml
import os 

from panda3d.core import GeoMipTerrain, TextureStage, TexGenAttrib, Shader, Texture, Vec3, CollisionRay, CollisionTraverser, CollisionHandlerQueue, CollisionNode, NodePath

def loadTerrain(path):

    #load terrain data
    terrain_file = open(os.path.join(path,'map.json'))
    terrain_data = json.loads(terrain_file.read())
    terrain_file.close()

    #Generate the terrain using GeoMipTerrain
    terrain = GeoMipTerrain('terrain')
    terrain.setHeightfield(terrain_data['heightmap'])
    #terrain.setBruteforce(True)
    tRoot = terrain.getRoot()

    tRoot.setSz(100)

    #Textures setup
    ts_idx = 0
    
    for tex in terrain_data['textures']:
        ts = TextureStage('gnd' + str(ts_idx))
        ts.setSort(ts_idx)
        texture = loader.loadTexture(tex)
        tRoot.setTexture(ts,texture)
        ts_idx+=1

    
    terrain.generate()

    #Generate slope image
    slope_img = Texture()
    slope_img.load(terrain.makeSlopeImage())

    #shaders
    tRoot.setShaderInput("Heightmap",loader.loadTexture(terrain_data['heightmap']))
    tRoot.setShaderInput("SlopeImage",slope_img)
    tRoot.setShaderInput("TexScaleFactor0",terrain_data['texture_scale_factors'][0])
    tRoot.setShaderInput("TexScaleFactor1",terrain_data['texture_scale_factors'][1])
    tRoot.setShaderInput("TexScaleFactor2",terrain_data['texture_scale_factors'][2])

    shader = Shader.load(vertex=terrain_data['vertex_shader'],
                         fragment=terrain_data['fragment_shader'],
                         lang=Shader.SL_GLSL)

    tRoot.setShader(shader)



    terrain.update()

    #Load nature
    for nat_obj in terrain_data['object_positions']:
        for pos in terrain_data['object_positions'][nat_obj]:

            mod = loader.loadModel(nat_obj)
            bounds = mod.getTightBounds()
            mod_height = abs(bounds[0].z - bounds[1].z)

            #mod.setScale(10)
            z_pos = terrain.getElevation(pos[0],pos[1]) * tRoot.get_sz()
            mod.setPos(Vec3(pos[0],pos[1],z_pos))
            mod.reparentTo(render)

    return terrain, tRoot


MAPMAKER_PATH = 'mapmaker/build/bin/mapmaker/mapmaker'
SHADERS = 'shaders'

def find_biggest(natural_objects):
    max_size = (0.0,0.0)
    for obj in natural_objects:
        mod = loader.loadModel(obj)
        bounds = mod.getTightBounds()
        b_x = abs(bounds[0].x - bounds[1].x)
        b_y = abs(bounds[0].y - bounds[1].y)
        if b_x * b_y > max_size[0] * max_size[1]:
            max_size = (b_x,b_y)
    return max_size 

def generateTerrain(shape,texture_paths,texture_scale_factors,nature_path,natural_objects_count,path,force=False):
    heightmap_path = os.path.join(path,"heightmap.pnm")
    json_path = os.path.join(path,"map.json")
    if os.path.exists(path):
        if force:
            shutil.rmtree(path)
        else:
            print(path, " already exists!")
            return
    os.mkdir(path)
    with open('tmp.yml','w+') as inputFile:
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

    #generate nature
    terrain = GeoMipTerrain('terrain')
    terrain.setHeightfield(heightmap_path)
    slopeImg = terrain.makeSlopeImage()
    #nature = list(filter(lambda x: x.endswith('.obj'),os.listdir(nature_path)))
    nature = list(map(lambda x: os.path.join(nature_path,x),os.listdir(nature_path)))
    max_size = find_biggest(nature)

    object_positions = {}
    for obj in nature:
        object_positions[obj] = []


    
    count = 0

    x_cells_count = slopeImg.getReadXSize() / max_size[0]
    y_cells_count = slopeImg.getReadYSize() / max_size[1]

    while(count < natural_objects_count):
        pt = (random.uniform(0,slopeImg.getReadXSize()),
              random.uniform(0,slopeImg.getReadYSize()))

        rand_obj = random.randrange(0,len(nature)) 
        object_positions[nature[rand_obj]] += [pt]

        count += 1

         
    #print(biggest_natural_object)
    #print(slopeImg.getReadXSize(),slopeImg.getReadYSize())



    #generate json
    json_data = {
                'heightmap': heightmap_path,
                'shape': shape,
                'textures': texture_paths,
                'texture_scale_factors': texture_scale_factors,
                'vertex_shader': os.path.join(SHADERS,'terrain.vert'),
                'fragment_shader': os.path.join(SHADERS,'terrain.frag'),
                'object_positions': object_positions
            }

    json_file = open(json_path,"w+")
    json_file.write(json.dumps(json_data,indent=4))
    json_file.close()
