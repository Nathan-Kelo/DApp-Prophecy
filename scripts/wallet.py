from helpers import cryptography

class Wallet:
    publicKey=None
    __privateKey=None

    def __init__(self):
        self.__privateKey=cryptography.generate_random_private_key()
        self.publicKey=cryptography.get_public_key_from_private_key(self.__privateKey)
    
    def sign(self,certificate):
        certificate.signature=cryptography.sign_hash_with_private_key(certificate.hash(),self.__privateKey)
    
    #not going to print private because dosent feel right tbh
    def display(self):
        dict={}
        dict['Public Key']=self.publicKey[:8]
        print(dict)