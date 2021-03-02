from ursina import *
#credit to pokepetter for the basis of the first person script
from voxelcaster import voxelcaster
from blockModel import blockModelData
from ursina.shaders import lit_with_shadows_shader
class FirstPersonController(Entity):
    def __init__(self,blockModel=None, **kwargs):
        super().__init__()
        self.speed = 5
        self.origin_y = -.5
        self.camera_pivot = Entity(parent=self, y=1.9)
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = True
        self.grounded = False
        self.jump_height = 2
        self.jump_duration = .5
        self.jumping = False
        self.air_time = 0
        self.chunksDict=chunksDict
        self.caster=voxelcaster(chunks=self.chunksDict)
        self.size=16


        for key, value in kwargs.items():
            setattr(self, key ,value)



        if blockModel==None:
            blockModel=blockModelData()
        self.template=[(0,3,15,12),(13,18,6,1),(2,7,9,4),(16,21,19,14),(5,10,22,17),(20,23,11,8)]
        self.faceNormals=[[0,-1,0],[0,0,-1],[-1,0,0],[1,0,0],[0,0,1],[0,1,0]]
        self.blockUVs=blockModel.blockUVs
        self.blocks=blockModel.blocks

        





        #set up hand held cube
        
        self.cube=Entity(parent=camera,texture="testStrip",position=(0.5,-0.5,1),scale=0.4,rotation=(-50,45,20),always_on_top=True,shader=lit_with_shadows_shader)
        self.cube.texture.filtering=None
        self.cube.verts=[]
        self.cube.normals=[]
        
        self.cube.faces=self.template
        self.cube.block=1
        self.cube.UVs=[]
        
        for l in range(8):
                        
            key=str(bin(l))
            key="0"*(3-len(key[2:]))+key[2:]
            vertex=Vec3(0,0,0)
            #normal=Vec3(-0.5,-0.5,-0.5)
            normal=Vec3(-0.5,-0.5,-0.5)+Vec3(int(key[0]),int(key[1]),int(key[2]))
            normal=(normal[0],normal[1],normal[2])
            
            #print(normal)
            for m in range(3):
                vertex[m]=vertex[m]+int(key[m])
            #normal=normal+vertex
            for n in range(3):
                self.cube.verts.append(vertex)
                self.cube.normals.append(normal)
        self.setBlockTexture(generate=False)
        
        


    def setBlockTexture(self,generate=True):
        self.cube.UVs=[]
        
        for l in range(24):
            self.cube.UVs.append(self.blockUVs[self.blocks[self.cube.block]][l])
        #print(self.cube.UVs)
        self.cube.model=Mesh(vertices=self.cube.verts,normals=self.cube.normals,triangles=self.cube.faces,uvs=self.cube.UVs)
        self.cube.model.generate()
    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
            ).normalized()

        origin = self.world_position + (self.up*1)+ self.direction * self.speed * time.dt
        if distance(self.direction,Vec3(0,0,0)) != 0:
            hit_info = self.caster.voxelcast(origin , self.down, maxDistance=1)
            if not hit_info.hit:
                self.position += self.direction * self.speed * time.dt


        if self.gravity:
            # # gravity
            ray = self.caster.voxelcast(self.world_position+(0,2,0), self.down)
            #wtp(ray.hit)
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=(self,))
            if ray.hit:
                if ray.distance <= 2.1:
                    if not self.grounded:
                        self.land()
                    self.grounded = True
                    # make sure it's not a wall and that the point is not too far up
                    if ray.normal.y > .7 and ray.point[1] - self.world_y < .5: # walk up slope
                        self.y = ray.point[1]
                    return
                else:
                    self.grounded = False

                # if not on ground and not on way up in jump, fall
                self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
                self.air_time += time.dt * .25 * self.gravity


    def input(self, key):
        if key == 'space':
            self.jump()
        if key == 'scroll up' or key == 'up arrow down':
            self.cube.block=(self.cube.block+1)%len(self.blocks)
            self.setBlockTexture()
        if key == 'scroll down' or key == 'down arrow down':
            self.cube.block=(self.cube.block-1)%len(self.blocks)
            self.setBlockTexture()
        if key == 'right mouse down':
            ray=self.caster.voxelcast(self.camera_pivot.world_position,self.camera_pivot.forward)
            if ray.hit:
                try:
                    #print(ray.currentChunk)
                    #print(ray.normal)
                    #print(ray.currentCube)

                    
                    pos=Vec3(ray.currentCube)+Vec3(ray.normal)
                    for i in range(3):
                        if pos[i] < 0:
                            pos[i]=15
                            ray.currentChunk[i] -= self.size
                        elif pos[i] > 15:
                            pos[i]=0
                            ray.currentChunk[i] += self.size
                    key=str(round(ray.currentChunk[0]))+":"+str(round(ray.currentChunk[1]))+":"+str(round(ray.currentChunk[2]))
                    self.chunksDict[key].addBlock(position=[round(pos[0]),round(pos[1]),round(pos[2])],block=self.blocks[self.cube.block])
                except Exception as e:
                    #print(e)
                    #print(ray.currentCube)
                    pass
        if key == 'left mouse down':
            ray=self.caster.voxelcast(self.camera_pivot.world_position,self.camera_pivot.forward)
            if ray.hit:
                try:
                    #print(ray.currentChunk)
                    #print(ray.normal)
                    #print(ray.currentCube)

                    
                    pos=Vec3(ray.currentCube)

                    key=str(round(ray.currentChunk[0]))+":"+str(round(ray.currentChunk[1]))+":"+str(round(ray.currentChunk[2]))
                    self.chunksDict[key].removeBlock(position=[round(pos[0]),round(pos[1]),round(pos[2])])
                except Exception as e:
                    #print(e)
                    #print(ray.currentCube)
                    pass
            

    def jump(self):
        if not self.grounded:
            return

        self.grounded = False
        self.animate_y(self.y+self.jump_height, self.jump_duration, resolution=int(1//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.jump_duration)


    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # #wtp('land')
        self.air_time = 0
        self.grounded = True
def fs():
    window.fullscreen=True
    window.position=(0,0)
    player.y=60

if __name__ == '__main__':



    from worldGeneration import chunkGenerator
    from chunks import voxelChunk
    import random
    import time as t
    blockModel=blockModelData()
    app=Ursina()
    window.fullscreen=True
    Texture.default_filtering = None
    Sky()
    generator=chunkGenerator(seed=round(t.time()))
    count=0
    chunksDict={}
    caster=voxelcaster(chunks=chunksDict)
    for i in range(8):
        for j in range(4):
            for k in range(8):
                count+=1
                print("\n"*10+"▓"*round(count/2)+"░"*round((256-count)/2))
                x,y,z=i*16,j*16,k*16
                chunk=generator.generateChunkArrayNew(position=Vec3(x,y,z))
                chunk=voxelChunk(position=Vec3(x,y,z),chunkArray=chunk,blockModel=blockModel)
                chunk.buildChunk()
                chunksDict[str(x)+":"+str(y)+":"+str(z)]=chunk
    #wtp("hit start")
    for i in range(0):
        #wtp(i)
        hitTest=caster.voxelcast(origin=Vec3(random.randint(0,1599)/100,50,random.randint(0,1599)/100),direction=Vec3(0,-1,0),maxDistance=50)
        #wtp(hitTest.currentChunk)
        #wtp(hitTest.currentCube)
        #wtp(hitTest.normal)
        Entity(model="cube",scale=0.1,position=hitTest.point,color=color.black)
    #wtp("hit end")
    player = FirstPersonController( position=(15.5,40,15.5), origin_y=-.5,chunksDict=chunksDict,blockModel=blockModel)
    
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
    invoke(fs,delay=10)

    app.run()







    
