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
                    'example_textures/grass/Grass003_1K_Color.jpg',#base texture
                    'example_textures/snow/Snow006_1K_Color.jpg',#this depends on height
                    'example_textures/rock/Rock050_1K_Color.jpg'#this depends on slope
                ]

        #the relative scale factors
        texture_scale_factors = [
                    10,
                    10,
                    10
                ]

        #Path to a folder which contains nature objects
        nature_path = 'example_nature'

        TerrainGenerator.generateTerrain(shape,
                                         texture_paths,
                                         texture_scale_factors,
                                         nature_path,
                                         1000,
                                         "test", 
                                         force=True)

        self.terrain, self.tRoot= TerrainGenerator.loadTerrain("test")
        self.tRoot.reparentTo(render)

        self.screenshotReleased = True
        inputState.watchWithModifiers('screenshot','space')
        taskMgr.add(self.inputTask,'inputTask')

    def inputTask(self,task):
        if inputState.isSet('screenshot'):
            if self.screenshotReleased:
                self.screenshot(namePrefix='screenshot')
            self.screenshotReleased = False
        else:
            self.screenshotReleased = True
        return task.cont


app = TestTerrainGenerator()
app.run()
