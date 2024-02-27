from helpers import timestamp
from helpers import cryptography

class Certificate:
    issuerPublicKey=None
    signature=None
    timestamp=None      #this is timestamp of creation

    def __init__(self,issuerPublicKey):
        self.issuerPublicKey=issuerPublicKey
        self.signature=None
        self.timestamp=timestamp.now()

    def build_payload(self):
        return [self.issuerPublicKey,self.timestamp]

    def hash(self):
        tmp=""
        for item in self.build_payload():
            tmp+=str(item)
        return cryptography.hash_string(tmp)

    def equals(self,otherCertificate):
        return self.hash()==otherCertificate.hash()
    
    def __eq__(self, otherCertificate) -> bool:
        return self.equals(otherCertificate)
    
    def __hash__(self) -> int:
        return int(self.hash(),16)
    
    def is_legit(self):
        return cryptography.has_public_key_signed_this_hash(self.issuerPublicKey,self.signature,self.hash())
    
    def display(self):
        dict={}
        dict['Public Key']=self.issuerPublicKey[:8]
        if self.signature == None:
            dict['Signature']="NOT SIGNED YET"
        else:    
            dict['Signature']=self.signature[:8]
        dict['timestamp']=self.timestamp
        dict['type']=type(self)
        print(dict)
        
        
    