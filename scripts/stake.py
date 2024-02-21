from certificate import Certificate

class StakingOperation(Certificate):

    def __init__(self,issuerPublicKey,tokenAmount):
        super().__init__(issuerPublicKey)
        self.tokenAmount=tokenAmount
        
    def build_payload(self):
        return [self.issuerPublicKey,self.timestamp,self.tokenAmount]
        
    
    @staticmethod
    def build_staking_accounts(blockList):
        dict={}
        for block in blockList:
            for cert in block.certificateList:
                if isinstance(cert,StakingOperation):
                    if(cert.issuerPublicKey in dict.keys()):
                        dict[cert.issuerPublicKey]+=cert.tokenAmount
                    else :
                        dict[cert.issuerPublicKey]=cert.tokenAmount
        return dict

    def display(self):
        dict={}
        dict['Public key']=self.issuerPublicKey[:8]     
        dict['Tokens']=self.tokenAmount
        dict['timestamp']=self.timestamp
        print(dict)