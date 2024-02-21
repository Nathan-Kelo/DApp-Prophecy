from certificate import Certificate

class Block(Certificate):
    certificateList=[]
    indexInBlockchain=None
    parentBlockHash=None

    def __init__(self,issuerPublicKey,indexInBlockChain,parentBlockHash,certList):
        super().__init__(issuerPublicKey)
        self.indexInBlockchain=indexInBlockChain
        self.parentBlockHash=parentBlockHash
        self.certificateList=certList

    def build_payload(self):
        payload=[self.issuerPublicKey,self.timestamp,self.parentBlockHash]+[info for cert in self.certificateList for info in cert.build_payload()]      
        return payload
    
    def is_legit(self):
        if not super().is_legit():
            return False
        for cert in self.certificateList:
            if not cert.is_legit():
                return False
        return True
    
    def display(self):
        super().display()
        dict={}
        dict['Index']=self.indexInBlockchain
        dict['Parent hash']=self.parentBlockHash[:8]
        print(dict)
        print("--Block certs--")
        for cert in self.certificateList:
            cert.display()
        print("----")
            
            