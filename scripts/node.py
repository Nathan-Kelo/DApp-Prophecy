from network import Node
from blockchain import Blockchain
from block import Block
from certificate import Certificate

class BlockchainNode(Node):

    #This is shared between all of the nodes so i dont need to broadcast a clear signal to all
    

    def __init__(self,wallet,consensusAlgorithm):
        super().__init__(wallet.publicKey)
        self.wallet=wallet
        self.consensusAlgorithm=consensusAlgorithm
        self.blockchain=Blockchain()
        self.__certificateBox=set()
        
#____________________________________communication protocol____________________________________
        
    def receive_object_from_node(self, obj, senderNodeIdentifier):
        if isinstance(obj,Block):
            self.new_block(obj)
            self.print(f"\"{self.formatIdentifier(senderNodeIdentifier)}\" sent me a new a new block")
        elif isinstance(obj,Certificate):
            self.new_certificate(obj)
            self.print(f"\"{self.formatIdentifier(senderNodeIdentifier)}\" sent me a certificate")
        else:
            self.print(f'I dont know what I received.')

    def print(self,message):
        print(f'[{self.formatIdentifier(self.nodeIdentifier)}] {message}')

    def send_object_to_node(self, obj, nodeIdentifier):
        self.print(f"I am sending the data \"{obj}\" to \"{self.formatIdentifier(nodeIdentifier)}\"")
        super().send_object_to_node(obj, nodeIdentifier)
    
    def formatIdentifier(self,nodeIdentifier):
        numbers=4
        middle=int(len(nodeIdentifier)/2)
        return f'node {nodeIdentifier[:numbers]}.{nodeIdentifier[middle-numbers:middle]}.{nodeIdentifier[len(nodeIdentifier)-numbers:]}'
            
            
    def broadcast_object(self, obj):
        self.print(f"I am sending the data \"{obj}\" to EVERYBODY!")
        super().broadcast_object(obj)
    
#_________________________________________________________________________________________________
    def try_forge_block(self):
        if(len(self.__certificateBox)==5):
            block=Block(self.wallet.publicKey,self.blockchain.get_latest_block().indexInBlockchain+1,self.blockchain.get_latest_block().hash(),list(self.__certificateBox.copy()))
            if self.consensusAlgorithm.is_next_block_forger_legit(self.blockchain.blockList,block):
                self.wallet.sign(block)                
                self.new_block(block)
                self.__certificateBox=set()
                self.broadcast_object(block)
                return True
        else:
            return False        
        
    def new_certificate(self,certificate):
        
        if not certificate.is_legit():
            self.print(1)
            return False
        if self.blockchain.contains_certificate(certificate):
            self.print(2)
            return False
        if certificate in self.__certificateBox:
            self.print('3 :')
            certificate.display()
            return False
        
        self.print('Adding')
        certificate.display()
        self.__certificateBox.add(certificate)
        if not self.try_forge_block():
            self.broadcast_object(certificate)
        
    
    
    def new_block(self,block):
        if not self.blockchain.contains_block(block):
            return
        if not self.consensusAlgorithm.is_next_block_forger_legit(self.blockchain.blockList,block):
            return
        if not block.is_legit():
            return
        if block.indexInBlockchain != self.blockchain.get_latest_block().indexInBlockchain+1:
            return
        for c in block.certificateList:
            if self.blockchain.contains_certificate(c):
                return
        if len(block.certificateList)<5:
           return
        if self.blockchain.get_latest_block().hash() != block.parentBlockHash:
            return 
        
        #All good so we append to blockchain
        self.blockchain.blockList.append(block)
        for certificate in block.certificateList:
            if certificate in self.__certificateBox:
                self.__certificateBox.remove(certificate) 
        self.broadcast_object(block)
        self.try_forge_block()

    def print_certbox(self):
        print(f'--CERTBOX {len(self.__certificateBox)} certs--')
        for cert in self.__certificateBox:
            cert.display()
        print('----')
        
            