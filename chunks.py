from ursina import *
from ursina.shaders import lit_with_shadows_shader
import random
class voxelChunk(Entity):
    def __init__(self,chunkArray,position=Vec3(0,0,0),shader=lit_with_shadows_shader,origin=Vec3(0,0,0)):
        super().__init__(double_sided=False,texture="testStrip",shader=shader,position=position,origin=origin)
        self.texture.filtering='none'
        self.textureCount=13
        self.textureWidth=self.texture.width/self.textureCount
        #print(self.textureWidth)
        self.chunkArray=chunkArray
        self.building=False
        self.chunkDict={}
        self.template=[(0,3,15,12),(13,18,6,1),(2,7,9,4),(16,21,19,14),(5,10,22,17),(20,23,11,8)]
        self.faceNormals=[[0,-1,0],[0,0,-1],[-1,0,0],[1,0,0],[0,0,1],[0,1,0]]
        a=0
        self.transparent=["a"]
        #self.blockUVs={"s":[0,(0,0),(0,1),(1,1),(0,1),(0,1),(1,1),(0,0),(1,0),(0,1),(0,0),(1,0),(0,0),(1,0),(1,1),(0,1),(1,1),(1,1),(0,1),(1,0),(0,0),(1,1),(1,0),(0,0),(1,0)]}
        defaultLayouts={
        "allSides":[[0,0],[0,1],[1,1],[0,1],[0,1],[1,1],[0,0],[1,0],[0,1],[0,0],[1,0],[0,0],[1,0],[1,1],[0,1],[1,1],[1,1],[0,1],[1,0],[0,0],[1,1],[1,0],[0,0],[1,0]],
        "topSidesBottom":[[2,0],[0,1],[1,1],[2,1],[0,1],[1,1],[0,0],[1,0],[1,1],[0,0],[1,0],[1,0],[3,0],[1,1],[0,1],[3,1],[1,1],[0,1],[1,0],[0,0],[2,1],[1,0],[0,0],[2,0]],
        "topSidesBottomSame":[[1,0],[0,1],[1,1],[1,1],[0,1],[1,1],[0,0],[1,0],[1,1],[0,0],[1,0],[1,0],[2,0],[1,1],[0,1],[2,1],[1,1],[0,1],[1,0],[0,0],[2,1],[1,0],[0,0],[2,0]]
        #                     <      fbl     > <      bbl    >    <      ftl     > <        btl     > <       fbr     ><       bbr      ><        ftr     ><       btr     >



        }
        self.blockUVs={"s":[0,"allSides"],
                       "g":[1,"topSidesBottom"],
                       "d":[3,"allSides"],
                       "log":[4,"topSidesBottomSame"],
                       "p":[7,"allSides"],
                       "l":[6,"allSides"],
                       "b":[12,"allSides"],
                       "coal":[11,"allSides"],
                       "diamond":[10,"allSides"],
                       "gold":[9,"allSides"],
                       "iron":[8,"allSides"]
        }
        #                   <      fbl     > <      bbl    >    <      ftl     > <        btl     > <       fbr     ><       bbr      ><        ftr     ><       btr     >



        for i in list(self.blockUVs.keys()):
            offset=self.blockUVs[i][0]/self.textureCount
            key=self.blockUVs[i][1]
            self.blockUVs[i]=[]
            #print(self.blockUVs)
            for j in range(len(defaultLayouts[key])):
                self.blockUVs[i].append([0,defaultLayouts[key][j][1]])
                self.blockUVs[i][j][0]=defaultLayouts[key][j][0]/self.textureCount+offset
            #print(self.blockUVs[i])
        self.vertsChanged=True
        self.normalsChanged=True
        self.trianglesChanged=True
        self.UVsChanged=True

    @property
    def chunkArray(self):
        return self._chunkArray

    @chunkArray.setter
    def chunkArray(self,value):
        #print("setting")
        self._chunkArray=value
        #self.buildChunk()

    @property
    def verts(self):
        return self._verts

    @verts.setter
    def verts(self,value):
        self._verts=value
        self.vertsChanged=True

    @property
    def normals(self):
        return self._normals

    @normals.setter
    def normals(self,value):
        self._normals=value
        self.normalsChanged=True

    @property
    def triangles(self):
        return self._triangles

    @triangles.setter
    def triangles(self,value):
        self._triangles=value
        self.trianglesChanged=True


    @property
    def UVs(self):
        return self._UVs

    @UVs.setter
    def UVs(self,value):
        self._UVs=value
        self.UVsChanged=True


        

    def generateMesh(self):
        if self.vertsChanged:
            print("verts")
            self.model.vertices=self.verts#.copy()
            self.vertsChanged=False
        if self.normalsChanged:
            self.model.normals=self.normals#.copy()
            self.normalsChanged=False
        if self.trianglesChanged:
            self.model.triangles=self.faces#.copy()
            self.trianglesChanged=False
        if self.UVsChanged:
            self.model.uvs=self.UVs#.copy()
            self.UVsChanged=False
        self.model.generate()
    def buildChunk(self):
        #print("building")
        #print(self.chunkArray)
        self.verts=[]
        self.faces=[]
        self.normals=[]
        self.UVs=[]
        #self.norms=[]
        width=len(self.chunkArray)
        height=len(self.chunkArray[0])
        depth=len(self.chunkArray[0][0])
        #print(width,height,depth)
        for i in range(width):
            #print(i)
            for j in range(height):
                #print(j)
                for k in range(depth):
                    self.addBlock(position=(i,j,k),block=self.chunkArray[i][j][k],generate=False,checkOthers=False)
        self.model=Mesh(vertices=self.verts,normals=self.normals,triangles=self.faces,uvs=self.UVs,thickness=4,static=True)
        self.model.generate()







    def resetChunk(self): 
        self.building=True
        self.buildingI=0
        self.buildingJ=0
        self.buildingK=0
    def update(self):
        if self.building:
            width=len(self.chunkArray)
            height=len(self.chunkArray[0])
            depth=len(self.chunkArray[0][0])
            self.addBlock(position=(self.buildingI,self.buildingJ,self.buildingK),block=self.chunkArray[self.buildingI][self.buildingJ][self.buildingK],generate=False,checkOthers=False)
            self.buildingK+=1
            if self.buildingK==depth:
                self.buildingK=0
                self.buildingJ+=1
            if self.buildingJ == height:
                self.buildingJ=0
                self.buildingI+=1
            if self.buildingI == width:
                print(self.buildingI)
                self.building=False
                self.model=Mesh(vertices=self.verts,normals=self.normals,triangles=self.faces,uvs=self.UVs,thickness=4,static=True)
                self.model.generate()
                
    def fill(self,startPosition,endPosition,block="s",replace="",generate=True,checkOthers=True):
        for i in range(startPosition[0],endPosition[0]+1):
            for j in range(startPosition[1],endPosition[1]+1):
                for k in range(startPosition[2],endPosition[2]+1):
                    if self.chunkArray[i][j][k] == replace or replace=="":
                        self.addBlock(position=(i,j,k),block=block,generate=False)
        self.generateMesh()
                

    def removeBlock(self,position,generate=True):
        i,j,k=position[0],position[1],position[2]
        chunkKey=str(i)+":"+str(j)+":"+str(k)
        self.chunkArray[i][j][k]="a"
        width=len(self.chunkArray)
        height=len(self.chunkArray[0])
        depth=len(self.chunkArray[0][0])
        show=False
        normals=self.faceNormals


        
        

        






        if self.chunkArray[i][j][k] == "a" and chunkKey in list(self.chunkDict.keys()):
            fStart=self.chunkDict[chunkKey][1]
            template=self.template

            for l in range(6):
                    self.faces[fStart+l]=[]



        
        for l in range(6):
                        #print(normals[l])
            if i+normals[l][0] >=width or i+normals[l][0] < 0 or j+normals[l][1] >=height or j+normals[l][1] < 0 or k+normals[l][2] >=depth or k+normals[l][2] < 0 or self.chunkArray[i+normals[l][0]][j+normals[l][1]][k+normals[l][2]] =="a":                                                                #doesn't display hidden faces
                pass
            else:
                self.addBlock(position=(i+normals[l][0],j+normals[l][1],k+normals[l][2]),block=chunkArray[i+normals[l][0]][j+normals[l][1]][k+normals[l][2]],generate=False)
        if generate:
            self.generateMesh()
    
    def addBlock(self,position,block="s",generate=True,checkOthers=True):
        i,j,k=position[0],position[1],position[2]
        chunkKey=str(i)+":"+str(j)+":"+str(k)
        self.chunkArray[i][j][k]=block
        width=len(self.chunkArray)
        height=len(self.chunkArray[0])
        depth=len(self.chunkArray[0][0])
        show=False
        normals=self.faceNormals
        for l in range(6):
                        
            if i+normals[l][0] >=width or i+normals[l][0] < 0 or j+normals[l][1] >=height or j+normals[l][1] < 0 or k+normals[l][2] >=depth or k+normals[l][2] < 0 or self.chunkArray[i+normals[l][0]][j+normals[l][1]][k+normals[l][2]] in self.transparent:                                                                #doesn't display hidden faces
                show=True
                break
        #print(show)
        if self.chunkArray[i][j][k] != "a" and show:
            if chunkKey in list(self.chunkDict.keys()):
                vStart=self.chunkDict[chunkKey][0]
                fStart=self.chunkDict[chunkKey][1]

                






                if self.chunkArray[i][j][k] != "a":
                    for l in range(24):
                        self.UVs[vStart+l]=self.blockUVs[self.chunkArray[i][j][k]][l]
                    template=self.template
                    normals=self.faceNormals
                    for l in range(6):
                        #print(normals[l])
                        if i+normals[l][0] >=width or i+normals[l][0] < 0 or j+normals[l][1] >=height or j+normals[l][1] < 0 or k+normals[l][2] >=depth or k+normals[l][2] < 0 or self.chunkArray[i+normals[l][0]][j+normals[l][1]][k+normals[l][2]] in self.transparent:                                                                #doesn't display hidden faces
                            
                            #print(start)
                            #print((start,start,start,start)+(template[l]))
                            add=[]
                            for m in template[l]:
                                add.append(vStart+m)
                            self.faces[fStart+l]=add
                            #print(add)
                            
                            
                        else:
                            self.faces[fStart+l]=([])
                            if checkOthers and str(i+normals[l][0])+":"+str(j+normals[l][1])+":"+str(k+normals[l][2]) in list(self.chunkDict.keys()):
                                self.faces[self.chunkDict[str(i+normals[l][0])+":"+str(j+normals[l][1])+":"+str(k+normals[l][2])][1]+ (5-l)]=([])

   



                
            else:
                
                


                if self.chunkArray[i][j][k] != "a":
                    self.chunkDict[str(i)+":"+str(j)+":"+str(k)]=[len(self.verts),len(self.faces)]
                    for l in range(24):
                        self.UVs.append(self.blockUVs[self.chunkArray[i][j][k]][l])
                        #print(self.blockUVs[self.chunkArray[i][j][k]][l])
                    #self.UVs+=self.blockUVs[self.chunkArray[i][j][k]]
                    



                    for l in range(8):
                        
                        key=str(bin(l))
                        key="0"*(3-len(key[2:]))+key[2:]
                        vertex=Vec3(i,j,k)
                        #normal=Vec3(-0.5,-0.5,-0.5)
                        normal=Vec3(-0.5,-0.5,-0.5)+Vec3(int(key[0]),int(key[1]),int(key[2]))
                        normal=(normal[0],normal[1],normal[2])
                        
                        #print(normal)
                        for m in range(3):
                            vertex[m]=vertex[m]+int(key[m])
                        #normal=normal+vertex
                        for n in range(3):
                            self.verts.append(vertex)
                            self.normals.append(normal)
                    #template=[(0,1,5,4),(2,3,7,6),(0,2,6,4),(1,3,7,5),(0,2,3,1),(4,6,7,5)]
                    #normals=[[0,-1,0],[0,1,0],[0,0,-1],[0,0,1],[-1,0,0],[1,0,0]]

                    template=self.template
                    normals=self.faceNormals
                    for l in range(6):
                        #print(normals[l])
                        #if i+normals[l][0] >=width or i+normals[l][0] < 0 or j+normals[l][1] >=height or j+normals[l][1] < 0 or k+normals[l][2] >=depth or k+normals[l][2] < 0:
                            #print(([i+normals[l][0]],[j+normals[l][1]],[k+normals[l][2]]))
            
                        if i+normals[l][0] >=width or i+normals[l][0] < 0 or j+normals[l][1] >=height or j+normals[l][1] < 0 or k+normals[l][2] >=depth or k+normals[l][2] < 0 or self.chunkArray[i+normals[l][0]][j+normals[l][1]][k+normals[l][2]] in self.transparent:                                                                #doesn't display hidden faces
                            start=self.chunkDict[str(i)+":"+str(j)+":"+str(k)][0]
                            #print(start)
                            #print((start,start,start,start)+(template[l]))
                            add=[]
                            for m in template[l]:
                                add.append(start+m)
                            self.faces.append(add)
                            #print(add)
                            
                            
                        else:
                            self.faces.append([])
                            if checkOthers and str(i+normals[l][0])+":"+str(j+normals[l][1])+":"+str(k+normals[l][2]) in list(self.chunkDict.keys()):
                                self.faces[self.chunkDict[str(i+normals[l][0])+":"+str(j+normals[l][1])+":"+str(k+normals[l][2])][1]+ (5-l)]=([])
                                
            
            
    ###


            
            if generate:

                self.generateMesh()


        



def addRandom():
    #return
    #chunk.model.generate()
    chunk.addBlock((random.randint(0,15),random.randint(0,15),random.randint(0,15)),block="l")
    invoke(addRandom,delay=0.5)
    
if __name__=="__main__":
    app=Ursina()
    Texture.default_filtering = None
    Sky()
    
    chunkArray1=[]
    for x in range(16):
        layer=[]
        for y in range(16):
            line=[]
            for z in range(16):

                    line.append("s")

            layer.append(line)
        chunkArray1.append(layer)
    chunkArray1[0][0][0]="s"
    



    chunkArray2=[]
    for x in range(16):
        layer=[]
        for y in range(16):
            line=[]
            for z in range(16):
                #line.append("s")
                
                if y < 8:
                    line.append("s")
                elif y == 8 and random.randint(0,1)==0:
                    line.append("s")
                elif y==8:
                    line.append("d")
                elif y >8 and y <10:
                    line.append("d")
                elif y==10:
                    line.append("g")
                else:
                    line.append("a")

                

                    

            layer.append(line)
        chunkArray2.append(layer)
    #chunkArray[0][0][0]="s"


    
    #print(chunkArray)
    total=0
    for i in range(1):
        for j in range(1):
            for k in range(1):
                total+=1
                print(total)
                if j ==0:
                    chunk=voxelChunk(chunkArray2,position=(i*16,j*16,k*16))
                else:
                    chunk=voxelChunk(chunkArray1,position=(i*16,j*16,k*16))
                chunk.buildChunk()
    
    #test=Entity(model="cube")

    #addRandom()
    chunk.addBlock((5,11,5),block="log")
    chunk.addBlock((5,12,5),block="log")
    chunk.addBlock((5,13,5),block="log")
    chunk.addBlock((5,14,5),block="log")
    chunk.addBlock((5,15,5),block="log")


    chunk.fill((4,13,4),(6,14,6),block="l",replace="a")


    chunk.fill((5,15,4),(5,15,6),block="l")
    chunk.fill((4,15,5),(6,15,5),block="l")

    
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
    bmin, bmax = scene.get_tight_bounds(chunk)
    lens = sun._light.get_lens()
    lens.set_near_far(0, 10)
    # lens.set_film_offset((bmin.xy + bmax.xy) * .5)
    lens.set_film_size(0)

    app.run()
            
        
