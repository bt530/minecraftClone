#https://pypi.org/project/perlin-noise/
from ursina import *
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from chunks import voxelChunk
import copy
import random
import time as t

class chunkGenerator():
    def __init__(self,
                 octaveDepth=2,
                 square=[0.005,0.007],
                 seed=2,
                 snowHeight=48,
                 terrainScale=[50,10],
                 terrainOffset=[16,16],
                 chunkSize=16,
                 oreRules={0:{"diamond":2,"iron":20,"coal":25,"gold":10},
                           1:{"diamond":1,"iron":30,"coal":30,"gold":3},
                           2:{"diamond":0,"iron":10,"coal":50,"gold":0},
                           3:{"diamond":0,"iron":5,"coal":60,"gold":0},



                           },
                 spawnRules={0:{"tree":1},
                           1:{"tree":10},
                           2:{"tree":10},
                           3:{"tree":5},



                           },
                 treeTemplate=[["l",[[[-1,3,-1],[1,5,1]]]],
                               ["log",[[[0,1,0],[0,4,0]]]],
                               ["a",[[[-1,5,-1],[-1,5,-1]],[[1,5,-1],[1,5,-1]],[[1,5,1],[1,5,1]],[[-1,5,1],[-1,5,1]]]]

                               ]
                 ):

        self.spawnRules=spawnRules
        self.treeTemplate=treeTemplate
        self.snowHeight=snowHeight
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
        grassPresent=False
        for l in range(len(self.noise)):
            surface +=  (self.noise[l]([x*self.square[l],z*self.square[l]]))*self.terrainScale[l]+self.terrainOffset[l]
        surface=round(surface)
        if surface >position[1]+size:
            chunkArray=copy.deepcopy(self.templateStone)
            air=False
            stonePresent=True
            #print("air")
        else:
            chunkArray=copy.deepcopy(self.templateAir)
            air=True
            
            #print("stone")
        
        #print(chunkArray)
        s=self.seed+position[0]+position[1]+position[2]
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
                            if y > self.snowHeight and random.randint(0,y-self.snowHeight)!=0:
                                s+=10
                                random.seed(s)
                                chunkArray[i][j][k]="snow"

                            else:
                                chunkArray[i][j][k]="g"
                                grassPresent=True

                        else:
                            break
                    if position[1]==0:
                        chunkArray[i][0][k]="b"

                    if position[1]==3 and chunkArray[i][size-1][k] != "a":
                        chunkArray[i][0][k]="snow"
                else:
                    for m in range(size):

                        j=size-m-1
                        y=position[1]+j


                        if y > surface:
                            chunkArray[i][j][k]="a"
                        elif y >= surface-3 and y<surface:
                            chunkArray[i][j][k]="d"
                        elif y== surface:
                            if y > self.snowHeight and random.randint(0,y-self.snowHeight)!=0:
                                s+=10
                                random.seed(s)
                                chunkArray[i][j][k]="snow"

                            else:
                                chunkArray[i][j][k]="g"
                                grassPresent=True

                        else:
                            
                            break
                    if position[1]==0:
                        chunkArray[i][0][k]="b"
                    if position[1]==3 and chunkArray[i][size-1][k] != "a":
                        chunkArray[i][0][k]="snow"
                        
            if stonePresent:
                s=self.seed+position[0]+position[1]+position[2]
                for i in list(self.oreRules[round(position[1]/size)].keys()):
                    for j in range(self.oreRules[round(position[1]/size)][i]):
                        s+=10
                        random.seed(s)
                        x=random.randint(0,size-1)
                        y=random.randint(0,size-1)
                        z=random.randint(0,size-1)
                        if chunkArray[x][y][z]=="s":
                            chunkArray[x][y][z]=i
            if grassPresent:
                s=self.seed+position[0]+position[1]+position[2]
                #print(self.oreRules[round(position[1]/size)])
                for j in range(self.spawnRules[round(position[1]/size)]["tree"]):
                    s+=10
                    random.seed(s)
                    x=random.randint(2,size-3)
                    y=random.randint(0,size-7)
                    z=random.randint(2,size-3)
                    if chunkArray[x][y][z]=="g":
                        for i in self.treeTemplate:
                            for k in i[1]:
                                for a in range(k[0][0]+x,k[1][0]+1+x):
                                    for b in range(k[0][1]+y,k[1][1]+1+y):
                                        for c in range(k[0][2]+z,k[1][2]+1+z):
                                            #print(a,b,c)
                                            try:
                                                if chunkArray[a][b][c]=="a" or chunkArray[a][b][c]=="l":
                                                    
                                                    chunkArray[a][b][c]=i[0]
                                            except:
                                                print(a,b,c)
                                                print(0/0)
                                                #print( chunkArray[a][b][c])
        
        


                        #line.append("a")

        #ore generation

                
                
                    

        #print(chunkArray)
        return chunkArray              
        pass


    def loadChunkArray(self,position):
        pass
        
        










if __name__ == "__main__":
    app=Ursina()
    window.fullscreen=True
    Texture.default_filtering = None
    Sky()
    generator=chunkGenerator(seed=round(t.time()))
    count=0
    for i in range(8):
        for j in range(4):
            for k in range(8):
                count+=1
                print("\n"*10+"▓"*round(count/2)+"░"*round((256-count)/2))
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
