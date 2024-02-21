from helpers import cryptography
from block import Block

class Blockchain:
    
    def __init__(self):
        self.blockList=[]
        #Add genesis block
        self.blockList.append(Block(cryptography.get_black_hole_public_key(),
                                    0,
                                    "0",
                                    []))

    def get_latest_block(self):
        return self.blockList[-1]
    
    def contains_certificate(self,certificate):
        for block in self.blockList:
            if certificate in block.certificateList:
                return True
        return False
    
    def contains_block(self,block):
        if block in self.blockList:
            return False
        return True
    
    def is_legit(self):        
        for i in range(1,len(self.blockList)):
            #First check if the block themselves are not tampered with
            if self.blockList[i].indexInBlockchain != i:
                print("Index corruption")
                return False

            if not self.blockList[i].is_legit():
                print("Block corruption")
                return False
            
            if i<len(self.blockList)-1:
                if self.blockList[i].hash() != self.blockList[i+1].parentBlockHash:
                    print("Hash corruption")
                    return False
            
            #only one can have the genesis block as a parent maybe ?                
            if i != 0:
                if self.blockList[i].issuerPublicKey == cryptography.get_black_hole_public_key():
                    print("Genisis corruption")
                    return False
        return True
        
    def display(self):
        genisis={}
        genisis['Genesis Key']=self.blockList[0].issuerPublicKey[:8]
        genisis['Genesis Index']=self.blockList[0].indexInBlockchain
        print(genisis)
        for block in self.blockList[1:]:
            block.display()
        