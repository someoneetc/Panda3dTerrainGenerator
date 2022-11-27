import TerrainGenerator
import random

"""terrain = TerrainGenerator.generateTerrain(0.7,20)
file = open("gplot.dat","w+")
for pt in terrain:
    file.write(str(pt[0]) + "    " + str(pt[1]) + "\n")
file.close()
"""

from direct.showbase.ShowBase import ShowBase
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import GeoMipTerrain, TextureStage, LMatrix4f, LVecBase4f, GeomVertexWriter, PNMImage, GeomVertexReader, HeightfieldTesselator, TexGenAttrib, GeomVertexRewriter, LVecBase3f, Texture, AmbientLight, DirectionalLight, Shader


HEIGHTMAP_SCALE = 2.0


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)


        shape = (1025,1025)
        z_scale = 100
        texture_paths = [
                    'content/textures/grass.JPG',
                    'content/textures/snow.JPG'
                ]
        TerrainGenerator.generateTerrain(shape,z_scale,texture_paths,"test")
        exit(0)

        """self.terrain = GeoMipTerrain('terrain')
        self.terrain.setHeightfield('test.pnm')
        #self.terrain.setBlockSize(32)
        #self.terrain.setNear(0)
        #self.terrain.setFar(100)
        #self.terrain.setFocalPoint(base.camera)
        self.terrain.setBruteforce(True)
        self.tRoot = self.terrain.getRoot()
        self.tRoot.reparentTo(render)
        self.tRoot.setTexture(loader.loadTexture('test.pnm'))
        self.terrain.generate()
        self.terrain.update()

        self.printVerticesPositions()
        """

        """self.terrain = HeightfieldTesselator('hfield')
        self.terrain.setHeightfield('test.pnm')
        self.terrain.setHorizontalScale(1)
        self.terrain.setVerticalScale(129)
        self.tRoot = self.terrain.generate()
        

        
        self.tRoot.reparentTo(self.render)
        """
        self.terrain = GeoMipTerrain('terrain')
        self.terrain.setHeightfield('test.pnm')
        self.terrain.setBruteforce(True)
        self.tRoot = self.terrain.getRoot()
        self.tRoot.reparentTo(render)
        self.tRoot.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.tRoot.setTexScale(TextureStage.getDefault(), 1.0/shape[0], 1.0/shape[1])
        #self.tRoot.setTexture(loader.loadTexture('resources/textures/barren1/color.jpg'))
        #ts1.setCombineRgb(TextureStage.CMModulate, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSPrimaryColor, TextureStage.COSrcColor)
        #ts2.setCombineRgb(TextureStage.CMModulate, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSPrimaryColor, TextureStage.COSrcColor)

        
                

        self.tRoot.setScale(1,1,100)
        
        self.terrain.generate()



        ts1 = TextureStage('gnd1')
        ts2 = TextureStage('gnd2')
        ts3 = TextureStage('gnd3')
        ts4 = TextureStage('gnd4')

        ts1.setSort(0)
        ts2.setSort(1)
        ts3.setSort(2)
        ts4.setSort(3)

        self.tRoot.setTexture(ts1,loader.loadTexture('content/textures/dirt.JPG'))
        self.tRoot.setTexture(ts2,loader.loadTexture('content/textures/grass.JPG'))
        self.tRoot.setTexture(ts3,loader.loadTexture('content/textures/rock.JPG'))
        self.tRoot.setTexture(ts4,loader.loadTexture('content/textures/snow.JPG'))

    
        self.tRoot.setShaderInput("Heightmap",loader.loadTexture('test.pnm'))

        shader = Shader.load(vertex='content/shaders/terrain.vert',fragment='content/shaders/terrain.frag',lang=Shader.SL_GLSL)
        self.tRoot.setShader(shader)

        
        self.terrain.update()


        
        #self.tRoot.setPos(0,0,0)
        #bounds = self.tRoot.getTightBounds()
        #self.tRoot.setPos(abs(bounds[0][0]-bounds[1][0])/2,abs(bounds[0][1]-bounds[1][1])/2,0)
       # self.tRoot.setH(90)
       

        

        
    def printVData(self,vdata):
        vertex = GeomVertexReader(vdata, 'vertex')
        texcoord = GeomVertexReader(vdata, 'texcoord')
        normal = GeomVertexReader(vdata,'normal')
        while not vertex.isAtEnd():
            v = vertex.getData3()
            t = texcoord.getData2()
            n = normal.getData3() 
            print("v = %s, t = %s, n = %s" % (repr(v), repr(t), repr(n)))

    def printVerticesPositions(self):
        for geomNode in self.tRoot.node().getChildren():
            for geom in geomNode.getGeoms():
                vData = geom.getVertexData()
                self.printVData(vData)
            


app = Game()
app.run()
