import random
import json

from direct.showbase.ShowBase import ShowBase
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import GeoMipTerrain, TextureStage, LMatrix4f, LVecBase4f, GeomVertexWriter, PNMImage, GeomVertexReader, HeightfieldTesselator, TexGenAttrib, GeomVertexRewriter, LVecBase3f, Texture, AmbientLight, DirectionalLight, Shader



import TerrainGenerator



class TestTerrainGenerator(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        #Generate terrain
        shape = (1025,1025)
        z_scale = 100
        texture_paths = [
                    'example_textures/grass.JPG',
                    'example_textures/snow.JPG'
                ]

        TerrainGenerator.generateTerrain(shape,z_scale,texture_paths,"test")

        terrain, tRoot = TerrainGenerator.loadTerrain("test")
        tRoot.reparentTo(render)
        

app = TestTerrainGenerator()
app.run()
