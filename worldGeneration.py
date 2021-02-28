#https://pypi.org/project/perlin-noise/#history
from ursina import *
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from chunks import voxelChunk
import copy
import random

class chunkGenerator():
    def __init__(self,
                 octaveDepth=2,
                 square=[0.005,0.007],
                 seed=2,
                 terrainScale=[50,10],
                 terrainOffset=[16,16],
                 chunkSize=16,
                 oreRules={0:{"diamond":2,"iron":20,"coal":25,"gold":10},
                           1:{"diamond":1,"iron":30,"coal":30,"gold":3},
                           2:{"diamond":0,"iron":10,"coal":50,"gold":0},
                           3:{"diamond":0,"iron":5,"coal":60,"gold":0},



                           }
                 ):


        
        
        self.oreRules=oreRules
        self.octaveDepth=octaveDepth
        self.square=square
        self.seed=seed
        self.noise=[]
        self.terrainScale=terrainScale
        self.terrainOffset=terrainOffset
        self.size=chunkSize
        self.templateAir=[]
        self.templateStone=[]
        for i in range(self.size):
            layerAir=[]
            layerStone=[]
            for j in range(self.size):
                lineAir=[]
                lineStone=[]
                for k in range(self.size):
                    lineAir.append("a")
                    lineStone.append("s")
                    
                layerAir.append(lineAir)
                layerStone.append(lineStone)
                #print(line)
            self.templateAir.append(layerAir)
            self.templateStone.append(layerStone)
        for i in range(2,self.octaveDepth+2):
            self.noise.append(PerlinNoise(octaves=2**i, seed=self.seed))
    def generateChunkArray(self,position,size=16):
        chunkArray=[]
        for i in range(size):
            layer=[]
            for j in range(size):
                line=[]
                for k in range(size):
                    x=position[0]+i
                    y=position[1]+j
                    z=position[2]+k

                    #xmapped=x*self.square
                    #zmapped=z*self.square
                    
                    surface=0
                    for l in range(len(self.noise)):
                        surface +=  (self.noise[l]([x*self.square[l],z*self.square[l]]))*self.terrainScale[l]+self.terrainOffset[l]
                    surface=round(surface)
                    #surface=round(surface*self.terrainScale+self.terrainOffset)
                    
                    if y < surface-3:
                        line.append("s")
                    elif y >= surface-3 and y<surface:
                        line.append("d")
                    elif y== surface:
                        line.append("g")
                    else:
                        line.append("a")
                    
                layer.append(line)
                #print(line)
            chunkArray.append(layer)
        #print(chunkArray)
        return chunkArray              
        pass

    def generateChunkArrayNew(self,position):
        size=self.size
        x=position[0]
        
        z=position[2]
        surface=0
        stonePresent=False
        for l in range(len(self.noise)):
            surface +=  (self.noise[l]([x*self.square[l],z*self.square[l]]))*self.terrainScale[l]+self.terrainOffset[l]
        surface=round(surface)
        if surface >position[1]+size:
            chunkArray=copy.deepcopy(self.templateAir)
            air=True
            #print("air")
        else:
            chunkArray=copy.deepcopy(self.templateStone)
            air=False
            stonePresent=True
            #print("stone")
        
        #print(chunkArray)
        for i in range(size):
            for k in range(size):
                x=position[0]+i
                
                z=position[2]+k
                surface=0
                for l in range(len(self.noise)):
                    surface +=  (self.noise[l]([x*self.square[l],z*self.square[l]]))*self.terrainScale[l]+self.terrainOffset[l]
                surface=round(surface)

                #xmapped=x*self.square
                #zmapped=z*self.square
                

                #surface=round(surface*self.terrainScale+self.terrainOffset)
                if air:
                    for j in range(size):
                        y=position[1]+j
                        if y < surface-3:
                            chunkArray[i][j][k]="s"
                            stonePresent=True
                        elif y >= surface-3 and y<surface:
                            chunkArray[i][j][k]="d"
                        elif y== surface:
                            chunkArray[i][j][k]="g"
                        elif y==0:
                            chunkArray[i][j][k]="b"
                        else:
                            break
                else:
                    for l in range(size):
                        j=size-l-1
                        y=position[1]+j
                        if y > surface:
                            chunkArray[i][j][k]="a"
                        elif y >= surface-3 and y<surface:
                            chunkArray[i][j][k]="d"
                        elif y== surface:
                            chunkArray[i][j][k]="g"
                        elif y==0:
                            chunkArray[i][j][k]="b"
                        else:
                            
                            break
            if stonePresent:
                for i in list(self.oreRules[round(position[1]/size)].keys()):
                    for j in range(self.oreRules[round(position[1]/size)][i]):
                        x=random.randint(0,size-1)
                        y=random.randint(0,size-1)
                        z=random.randint(0,size-1)
                        if chunkArray[x][y][z]=="s":
                            chunkArray[x][y][z]=i
        



                        #line.append("a")

        #ore generation

                
                
                    

        #print(chunkArray)
        return chunkArray              
        pass


    def loadChunkArray(self,position):
        pass
        
        










if __name__ == "__main__":
    app=Ursina()
    Texture.default_filtering = None
    Sky()
    generator=chunkGenerator()
    count=0
    for i in range(8):
        for j in range(4):
            for k in range(8):
                count+=1
                print("\n"*100+"|"+"count)
                x,y,z=i*16,j*16,k*16
                chunk=generator.generateChunkArrayNew(position=Vec3(x,y,z))
                chunk=voxelChunk(position=Vec3(x,y,z),chunkArray=chunk)
                chunk.buildChunk()
    EditorCamera()
    Entity(model="cube",scale_y=2,position=(-1,-1,-1))
    """
    pivot=Entity(rotation_z=0,rotation_x=30,rotation_y=0,y=32)
    s=DirectionalLight(scale=-30, shadows=False)
    s._light.show_frustum()
    """


    sun = DirectionalLight(y=10, rotation=(90+40,45,0))
    #sun._light.show_frustum()
    sun._light.set_shadow_caster(True, 4096, 4096)
    #sun._light.show_frustum()
    # sun._light.set_shadow_caster(True, 4096, 4096)
    #bmin, bmax = scene.get_tight_bounds(chunk)
    lens = sun._light.get_lens()
    lens.set_near_far(0, 10)
    # lens.set_film_offset((bmin.xy + bmax.xy) * .5)
    lens.set_film_size(0)

    app.run()
                
                


    """
    seed=1
    noise = []

    depth=2
    for i in range(1,depth+1):
        noise.append(PerlinNoise(octaves=2**i, seed=seed))
    xpix, ypix = 100, 100


    pic=[]
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val=0
            for k in range(len(noise)):
                noise_val +=         noise[k]([1*i/xpix, 1*j/ypix])/2**k
            row.append(noise_val)
        pic.append(row)
    plt.imshow(pic, cmap='gray')
    plt.show()
    """
