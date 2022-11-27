import math
import random
from PIL import Image
import numpy
import noise
import time

from panda3d.core import PNMImage

MAPMAKER_PATH = 'mapmaker/build/bin/mapmaker/mapmaker'

class TerrainRegion():
    def __init__(self,minimum,maximum,texture,textureObject):
        self.minimum = minimum
        self.maximum = maximum
        self.texture = texture
        self.textureObject = textureObject        

def writeHeightmap(terrain,path):
    img = Image.fromarray(terrain,mode='L')
    img.save(path)



def distance(pt_a,pt_b):
    if pt_a == None or pt_b == None:
        return -1
    dist = math.sqrt(pow((pt_a[0]-pt_b[0]),2)+pow((pt_a[1]-pt_b[1]),2))
    return dist

import yaml
import os 
from queue import PriorityQueue

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: float 
    payload: Any=field(compare=False)

#Vertex class used by the generateRoadMap function.
#pos := position in the npm grid
#dist := distance from the starting point
#prev := previous vertex in the path
#qPos := position in the priority queue
#inQueue := equals True if the vertex is in the priority queue
#NOTE: each node is considered to be linked to the adjacent ones on the npm
class Vertex:
    def __init__(self,pos,dist,prev,qPos):
        self.pos = pos
        self.dist = dist
        self.prev = prev
        self.qPos = qPos
        self.inQueue = True

    def __lt__(a,b):
        return a.dist < b.dist

    def __gt__(a,b):
        return a.dist > b.dist

    def __str__(self):
        return '[' + str(self.pos) + ', ' + str(self.dist) + ']' 




def generateVersor(a,b):
    v = (b[0] - a[0], b[1] - a[1])
    mod = math.sqrt(pow(v[0],2) + pow(v[1],2))
    versor = (v[0]/mod,v[1]/mod)
    #print(math.sqrt(pow(versor[0],2) + pow(versor[1],2)))
    return versor 

grammar = {
    'A': 'AF++--A+',
    'F': 'F+A--+AF-+F'
}

def generateRoad(pnm,center):
    max_i = 10
    pattern = 'A'
    curr = center
    rows = pnm.getReadXSize()
    cols = pnm.getReadYSize()
    path = []
    #pnm.setXel(curr[0],curr[1],(0,10.0,pnm.getXel(curr[0],curr[1])))
    for i in range(max_i):
        new_p = ''
        for c in pattern:
            if c in grammar:
                new_p += grammar[c]
        pattern = new_p
    print(pattern)
    old_curr = curr
    for i in pattern:
        if curr[0] >= rows or curr[1] >= cols:
            curr = old_curr
        pnm.setXel(curr[0],curr[1],0.0)
        old_curr = curr
        if i == 'A':
            curr = (curr[0]+1,curr[1])
        elif i == 'F':
            curr = (curr[0]-1,curr[1])
        elif i == '+':
            curr = (curr[0],curr[1]+1)
        else:
            curr = (curr[0],curr[1]-1)
    return pnm
            

def generateRoadMap(path):
    pnm = PNMImage()
    pnm.read(path)
    pnm = generateRoad(pnm,(500,500))
    pnm.write(path)


def generateTerrain(settlement_max_diameter,shape,min_height,max_height,roughness,path):
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
                    'filename': path
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
                    'filename': path
                },

            }
        }
        inputFile.write(yaml.dump(yaml.safe_load(str(cfg))))
    os.system(MAPMAKER_PATH + ' ./tmp.yml')
    #generateRoadMap(path)
    #generateCentralPlain(path)
    #generatePlains(path,3)
