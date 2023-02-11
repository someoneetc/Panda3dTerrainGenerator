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

def _typeCheck(args,types):
    for arg,a_type in zip(args,types):
        if not isinstance(arg,a_type):
            return (type(arg),a_type)
    return None

def getHeightmap(path):
    terrain_data = json.loads(terrain_file.read())
    terrain_file.close()
    return terrain_data['heightmap']


def loadTerrain(path):

    tc = _typeCheck([path],[str])
    if tc:
        raise ValueError('Expected ',repr(tc[1]), ' but got ', repr(tc[0]))

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

    """
    test = terrain.makeSlopeImage()
    test.write('test.pnm')
    for i in range (0,test.getReadXSize()):
        for j in range(0,test.getReadYSize()):
            print(test.getXelVal(i,j))
    """

    #shaders
    tRoot.setShaderInput("Heightmap",loader.loadTexture(terrain_data['heightmap']))
    tRoot.setShaderInput("SlopeImage",slope_img)
    tRoot.setShaderInput("TexScaleFactor0",terrain_data['texture_scale_factors'][0])
    tRoot.setShaderInput("TexScaleFactor1",terrain_data['texture_scale_factors'][1])
    tRoot.setShaderInput("TexScaleFactor2",terrain_data['texture_scale_factors'][2])
    tRoot.setShaderInput("TexScaleFactor3",terrain_data['texture_scale_factors'][3])


    terrainGeneratorPath = os.path.dirname(__file__)
    shader = Shader.load(vertex=os.path.join(os.path.join(terrainGeneratorPath,'shaders'),terrain_data['vertex_shader']),
                         fragment=os.path.join(os.path.join(terrainGeneratorPath,'shaders'),terrain_data['fragment_shader']),
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


SHADERS = 'shaders'

def find_biggest(natural_objects):
    max_size = (1.0,1.0)
    for obj in natural_objects:
        mod = loader.loadModel(obj)
        bounds = mod.getTightBounds()
        b_x = abs(bounds[0].x - bounds[1].x)
        b_y = abs(bounds[0].y - bounds[1].y)
        if b_x * b_y > max_size[0] * max_size[1]:
            max_size = (b_x,b_y)
    return max_size 


GENERATORS = {
        "DiamondSquare": 0,
        "MidpointDisplacement": 1,
        "FractalValueNoise": 2,
        "FractalGradientNoise": 3,
        "FractalSimplexNoise": 4,
        "FractalCellNoise": 5,
        "Hills": 6,
        }


MODIFIERS = {
        "ThermalErosion": 0,
        "HydraulicErosion": 1,
        "FastErosion": 2,
        "Islandize": 3,
        "Gaussize": 4,
        "Flatten": 5,
        "Smooth": 6,
        }

FINALIZERS = {
            "ErosionScore": 0,
            "Playability": 1
        }

def generateCfg(generator,modifiers,finalizer,inputFile,shape,output):
    generator_cfg = {}
    modifier_cfg = {}
    finalizer_cfg = {}

    #GENERATOR
    if generator == GENERATORS['DiamondSquare']:
        generator_cfg = {
                    'name': 'diamond-square',
                    'parameters': {
                        'values': [0, 100, 200, 300]
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
                        'filename': output 
                    }
                }

    elif generator == GENERATORS["MidpointDisplacement"]:
        generator_cfg = {
                    'name': 'midpoint-displacement',
                    'parameters': {
                        'values': [0, 100, 200, 300]
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
                        'filename': output 
                    }
                }
    elif generator == GENERATORS["FractalValueNoise"]:
        generator_cfg = {
                    'name': 'fractal',
                    'parameters': {
                        'noise': 'value',
                        'noise_parameters':{
                            'curve': 'cubic'
                        },
                        'scale': 1.0,
                        'octaves': 10,
                        'lacunarity': 2.0,
                        'persistence': 0.5,

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
                        'filename': output 
                    }
                }
    elif generator == GENERATORS["FractalGradientNoise"]:
        generator_cfg = {
                    'name': 'fractal',
                    'parameters': {
                        'noise': 'gradient',
                        'noise_parameters':{
                            'curve': 'quintic'
                        },
                        'scale': 1.0,
                        'octaves': 10,
                        'lacunarity': 2.0,
                        'persistence': 0.5,

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
                        'filename': output 
                    }
                }

    elif generator == GENERATORS["FractalSimplexNoise"]:
        generator_cfg = {
                    'name': 'fractal',
                    'parameters': {
                        'noise': 'simplex',
                        'scale': 1.0,
                        'octaves': 10,
                        'lacunarity': 2.0,
                        'persistence': 0.5,

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
                        'filename': output 
                    }
                }
 
    elif generator == GENERATORS["FractalCellNoise"]:
        generator_cfg = {
                    'name': 'fractal',
                    'parameters': {
                        'noise': 'cell',
                        'noise_parameters': {
                                'count': 32,
                                'distance': 'euclidean',
                                'coeffs': [-1,1]
                            },
                        'scale': 1.0,
                        'octaves': 1,
                        'lacunarity': 2.0,
                        'persistence': 0.5,

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
                        'filename': output 
                    }
                }
    elif generator == GENERATORS["Hills"]:
        generator_cfg = {
                    'name': 'hills',
                    'parameters': {
                        'count': 100,
                        'radius_min': 0.3,
                        'radius_max': 0.6,

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
                        'filename': output 
                    }
                }


        



    #MODIFIERS
    modifiers_cfg = []

    for mod in modifiers:
        if mod == MODIFIERS['ThermalErosion']:
            modifiers_cfg += [
                        {    
                            'name': 'thermal-erosion',
                            'parameters':{
                                    'iterations': 50,
                                    'talus': 4,
                                    'fraction': 0.5
                                }
                        }
                    ]
        elif mod == MODIFIERS['HydraulicErosion']:
            modifiers_cfg += [
                        {    
                            'name': 'hydraulic-erosion',
                            'parameters':{
                                    'iterations': 100,
                                    'rain_amount': 0.01,
                                    'solubility': 0.01,
                                    'evaporation': 0.5,
                                    'capacity': 0.01
                                }
                        }
                    ]

        elif mod == MODIFIERS['FastErosion']:
            modifiers_cfg += [
                        {    
                            'name': 'fast-erosion',
                            'parameters':{
                                    'iterations': 100,
                                    'talus': 8,
                                    'fraction': 0.5,
                                }
                        }
                    ]

        
        elif mod == MODIFIERS['Islandize']:
            modifiers_cfg += [
                                {'name': 'islandize',
                                    'parameters':{
                                        'border': 0.15
                                    }
                                }
                            ]
        elif mod == MODIFIERS['Gaussize']:
            modifiers_cfg += [
                        {    
                            'name': 'gaussize',
                            'parameters':{
                                    'spread': 0.3,
                                }
                        }
                    ]

        elif mod == MODIFIERS['Flatten']:
            modifiers_cfg += [
                        {    
                            'name': 'flatten',
                            'parameters':{
                                    'factor': 2.0,
                                }
                        }
                    ]
        elif mod == MODIFIERS['Smooth']:
            modifiers_cfg += [
                        {    
                            'name': 'smooth',
                            'parameters':{
                                    'iterations': 10,
                                }
                        }
                    ]




    if finalizer == FINALIZERS['Playability']:
        finalizer_cfg = {
                    'name': 'playability',
                    'parameters':{
                        'sea_level': 0.5,
                        'unit_size': 1,
                        'building_size': 9,
                        'unit_talus': 8.0,
                        'building_talus': 2.0,
                        'output_intermediates': False,
                    }
                }
    elif finalizer == FINALIZERS['ErosionScore']:
        finalizer_cfg = {
                    'name': 'erosion-score'
                }

    cfg = {
            'generator': generator_cfg,
            'modifiers': modifiers_cfg,
            'finalizer': finalizer_cfg
          }
    inputFile.write(yaml.dump(yaml.safe_load(str(cfg))))


def generateTerrain(generator,modifiers,finalizer,shape,texture_paths,texture_scale_factors,nature_path,natural_objects_count,path,force=False):
    MAPMAKER_PATH = os.path.join(os.path.dirname(__file__),'mapmaker/build/bin/mapmaker/mapmaker')
    tc = _typeCheck(
                    [
                        generator,
                        modifiers,
                        finalizer,
                        shape,
                        texture_paths,
                        texture_scale_factors,
                        nature_path,
                        natural_objects_count,
                        path,
                        force
                     ],
                    [
                        int,
                        list,
                        int,
                        tuple,
                        list,
                        list,
                        str,
                        int,
                        str,
                        bool
                     ]
                    )
    if tc:
        raise ValueError('Expected ',repr(tc[1]), ' but got ', repr(tc[0]))

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
        """cfg = {
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
        }"""
        #inputFile.write(yaml.dump(yaml.safe_load(str(cfg))))
        generateCfg(generator,modifiers,finalizer,inputFile,shape,heightmap_path)
    os.system(MAPMAKER_PATH + ' ./tmp.yml')

    #generate nature
    terrain = GeoMipTerrain('terrain')
    terrain.setHeightfield(heightmap_path)
    slopeImg = terrain.makeSlopeImage()
    #nature = list(filter(lambda x: x.endswith('.obj'),os.listdir(nature_path)))
    if nature_path == "":
        nature = []
        natural_objects_count = 0
    else:
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
                'vertex_shader': 'terrain.vert',
                'fragment_shader': 'terrain.frag',
                'object_positions': object_positions
            }

    json_file = open(json_path,"w+")
    json_file.write(json.dumps(json_data,indent=4))
    json_file.close()
