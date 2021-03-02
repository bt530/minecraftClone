from math import inf,nan
from ursina import *
from numpy import dot,cross
from hit_info import HitInfo


#fix bug where ray starts right from face boundary

class voxelcaster():
    def __init__(self,chunks,size=16):
        self.chunks=chunks
        self.size=size
        self.cubeTemplate=[[[0,0,0],[0,0,1],[1,0,0]],[[0,0,0],[1,0,0],[1,1,0]],[[0,0,0],[0,0,1],[0,1,1]],[[1,0,0],[1,0,1],[1,1,1]],[[0,0,1],[0,1,1],[1,1,1]],[[0,1,0],[1,1,0],[1,1,1]]]
        self.faceNormals=[[0,-1,0],[0,0,-1],[-1,0,0],[1,0,0],[0,0,1],[0,1,0]]

    def voxelcast(self,origin,direction,maxDistance=inf,debug=False):

        origin=Vec3(*origin)
        direction=Vec3(*direction)
        #position=Vec3(*origin)
        point=origin
        normal=Vec3(0,1,0)
        oldNormal=None
        currentDistance=0
        currentWorldCube=Vec3(origin[0]//1,origin[1]//1,origin[2]//1)
        #print(direction)
        while currentDistance < maxDistance:
            
            
            cubeType,currentChunk,currentCube=self.getCube(currentWorldCube)
            #print(cubeType)
            if cubeType != "a" and cubeType != None:
                return self.createHitInfo(hit=True,point=point,normal=-normal,currentChunk=currentChunk,currentCube=currentCube,cubeType=cubeType,distance=currentDistance)###
                
            else:
                error=True
                for i in range(6):
                    start=Vec3(self.cubeTemplate[i][0][0],self.cubeTemplate[i][0][1],self.cubeTemplate[i][0][2])+currentWorldCube
                    normal=Vec3(self.faceNormals[i][0],self.faceNormals[i][1],self.faceNormals[i][2])
                    divider=dot(direction,self.faceNormals[i])
                    if divider != 0:
                        scalar=(dot(start,self.faceNormals[i])-dot(origin,self.faceNormals[i]))/divider
                        #print(scalar)
                        if scalar != nan and scalar != inf and scalar >=0:

                            point=Vec3(origin+scalar*direction)
                            if debug:
                                e=Entity(model="cube", scale=0.1,position=point)
                                destroy(e,delay=1)
                                e.fade_out(duration=1)

                            relPoint=point-currentWorldCube
                            #print(relPoint)
                            ##print(oldPoint,point)
                            ######switch to basing it off face rather than old point/new point to reduce issues with floating point arithmetic
                            if relPoint[0] >=0 and relPoint[0] <=1 and relPoint[1] >=0 and relPoint[1] <=1 and relPoint[2] >=0 and relPoint[2] <=1 and oldNormal != -normal and scalar >=0:
                                ##print(oldPoint,point)
                                oldNormal=normal
                                currentWorldCube=currentWorldCube+normal
                                currentDistance=distance(origin,point)
                                ##print(currentDistance)
                                error=False
                                break
                if error:
                    print("breaking")
                    #print(0/0)
                    break
                
        return self.createHitInfo()###
                        
                    
                    
                    
            
            
            


    def createHitInfo(self,hit=False,point=None,normal=None,currentChunk=None,currentCube=None,cubeType=None,distance=None):
        hit=HitInfo(hit=hit)
        hit.point=point
        hit.normal=normal
        hit.currentChunk=currentChunk
        hit.currentCube=currentCube
        hit.cubeType=cubeType
        hit.distance=distance
        return hit
        

    def getCube(self,position):    
        currentChunk=Vec3(0,0,0)
        currentCube=Vec3(0,0,0)
        for i in range(3):
            currentChunk[i]=round(position[i]//self.size * self.size)
            currentCube[i]=round(position[i] % self.size)
        try:
            chunkArray=self.getChunkArray(currentChunk)
        
            return chunkArray[round(currentCube[0])][round(currentCube[1])][round(currentCube[2])],currentChunk,currentCube
        except Exception as e: ##
            #print(e)
            return "b",None,None





    def getChunkArray(self,chunk):##
        return self.chunks[str(round(chunk[0]))+":"+str(round(chunk[1]))+":"+str(round(chunk[2]))].chunkArray

if __name__ == "__main__":
    from worldGeneration import chunkGenerator
    from chunks import voxelChunk
    import random
    app=Ursina()
    
    Texture.default_filtering = None
    Sky()
    generator=chunkGenerator(seed=21)
    count=0
    chunksDict={}
    caster=voxelcaster(chunks=chunksDict)
    for i in range(1):
        for j in range(4):
            for k in range(1):
                count+=1
                print("\n"*10+"▓"*round(count/2)+"░"*round((256-count)/2))
                x,y,z=i*16,j*16,k*16
                chunk=generator.generateChunkArrayNew(position=Vec3(x,y,z))
                chunk=voxelChunk(position=Vec3(x,y,z),chunkArray=chunk)
                chunk.buildChunk()
                chunksDict[str(x)+":"+str(y)+":"+str(z)]=chunk
    #print("hit start")
    for i in range(100):
        ##print(i)
        hitTest=caster.voxelcast(origin=Vec3(random.randint(0,1599)/100,50,random.randint(0,1599)/100),direction=Vec3(0,-1,0),maxDistance=50)
        #print(hitTest.currentChunk)
        #print(hitTest.currentCube)
        #print(hitTest.normal)
        Entity(model="cube",scale=0.1,position=hitTest.point,color=color.black)
    #print("hit end")
    EditorCamera()
    
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
    window.fullscreen=True
    app.run()
