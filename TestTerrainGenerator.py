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
                    'example_textures/dirt/Ground042_1K_Color.jpg',
                    'example_textures/grass/Grass003_1K_Color.jpg',
                    'example_textures/rock/Rock050_1K_Color.jpg',
                    'example_textures/snow/Snow006_1K_Color.jpg',
                ]

        #the relative scale factors
        texture_scale_factors = [
                    10,
                    10,
                    10,
                    10
                ]

        #Path to a folder which contains nature objects
        nature_path = 'example_nature'

        TerrainGenerator.generateTerrain(
                                         TerrainGenerator.GENERATORS['FractalCellNoise'],
                                         [TerrainGenerator.MODIFIERS,TerrainGenerator.MODIFIERS['Smooth']],
                                         TerrainGenerator.FINALIZERS['Playability'],
                                         shape,
                                         texture_paths,
                                         texture_scale_factors,
                                         nature_path,
                                         10,
                                         "test", 
                                         force=True
                                        )

        self.terrain, self.tRoot= TerrainGenerator.loadTerrain("test")
        self.tRoot.reparentTo(render)

        self.screenshotReleased = True
        inputState.watchWithModifiers('screenshot','space')
        self.test_var = 10000.0 
        taskMgr.add(self.inputTask,'inputTask')

    def inputTask(self,task):
        if inputState.isSet('screenshot'):
            if self.screenshotReleased:
                self.screenshot(namePrefix='screenshot')
            self.screenshotReleased = False
        else:
            self.screenshotReleased = True


        self.tRoot.setShaderInput('test_var',self.test_var)

        return task.cont


app = TestTerrainGenerator()
app.run()
