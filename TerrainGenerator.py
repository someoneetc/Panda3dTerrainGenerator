import math
import json
import random
from PIL import Image
import numpy
import noise
import time

import yaml
import os 


MAPMAKER_PATH = 'mapmaker/build/bin/mapmaker/mapmaker'

def generateTerrain(shape,z_scale,texture_paths,name):
    heightmap_path = os.path.join(name,"heightmap.pnm")
    json_path = os.path.join(name,"map.json")
    if os.path.exists(name):
        print(repr(name), " directory already exists!")
        return
    os.mkdir(name)
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
                'z_scale': z_scale,
                'textures': texture_paths,
            }

    json_file = open(json_path,"w+")
    json_file.write(json.dumps(json_data))
    json_file.close()
