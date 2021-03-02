class blockModelData():
    def __init__(self):

        self.textureCount=16

        #print(self.textureWidth)
        print("init")


        self.transparent=["a"]
        #self.blockUVs={"s":[0,(0,0),(0,1),(1,1),(0,1),(0,1),(1,1),(0,0),(1,0),(0,1),(0,0),(1,0),(0,0),(1,0),(1,1),(0,1),(1,1),(1,1),(0,1),(1,0),(0,0),(1,1),(1,0),(0,0),(1,0)]}
        defaultLayouts={
        "allSides":[[0,1],[0,0],[1,0],[0,0],[0,0],[1,0],[0,1],[1,1],[0,0],[0,1],[1,1],[0,1],[1,1],[1,0],[0,0],[1,0],[1,0],[0,0],[1,1],[0,1],[1,0],[1,1],[0,1],[1,1]],
        "topSidesBottom":[[2,1],[0,0],[1,0],[2,0],[0,0],[1,0],[0,1],[1,1],[1,0],[0,1],[1,1],[1,1],[3,1],[1,0],[0,0],[3,0],[1,0],[0,0],[1,1],[0,1],[2,0],[1,1],[0,1],[2,1]],
        "topSidesBottomSame":[[1,1],[0,0],[1,0],[1,0],[0,0],[1,0],[0,1],[1,1],[1,0],[0,1],[1,1],[1,1],[2,1],[1,0],[0,0],[2,0],[1,0],[0,0],[1,1],[0,1],[2,0],[1,1],[0,1],[2,1]]
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
                       "iron":[8,"allSides"],
                       "snow":[13,"topSidesBottom"],
        }
        #                   <      fbl     > <      bbl    >    <      ftl     > <        btl     > <       fbr     ><       bbr      ><        ftr     ><       btr     >
        #print(self.blockUVs)
        self.blocks=list(self.blockUVs.keys())

        for i in list(self.blockUVs.keys()):
            offset=self.blockUVs[i][0]/self.textureCount
            key=self.blockUVs[i][1]
            self.blockUVs[i]=[]
            #print(self.blockUVs)
            for j in range(len(defaultLayouts[key])):
                self.blockUVs[i].append([0,defaultLayouts[key][j][1]])
                self.blockUVs[i][j][0]=defaultLayouts[key][j][0]/self.textureCount+offset
            #print(self.blockUVs[i])
        #print(self.blockUVs)




if __name__ == "__main__":
    b=blockModelData()
