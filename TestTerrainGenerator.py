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

        #textures should be put in the following order according with
        #their role(for the time being only 3 textures are supported)
        texture_paths = [
                    'example_textures/grass.JPG',#base texture
                    'example_textures/snow.JPG',#this depends on height
                    'example_textures/rock.JPG'#this depends on slope
                ]

        #Path to a folder which contains nature objects
        nature_path = 'example_nature'

        TerrainGenerator.generateTerrain(shape,texture_paths,nature_path,1000,"test", force=True)

        self.terrain, self.tRoot, diobestia = TerrainGenerator.loadTerrain("test")
        self.tRoot.reparentTo(render)

        camera.setPos(diobestia.getPos() + (100,0,0))
        camera.lookAt(diobestia.getPos())



app = TestTerrainGenerator()
app.run()
