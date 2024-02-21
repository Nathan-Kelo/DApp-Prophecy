from helpers import cryptography
from json import dumps

class RaffleTicket:

    def __init__(self,ownerPublicKey,number,raffleHash):
        self.ownerPublicKey=ownerPublicKey
        self.number=number
        self.raffleHash=raffleHash

    def build_payload(self):
        payload={}
        payload['PublicKey']=self.ownerPublicKey
        payload['number']=self.number
        payload['raffleHash']=self.raffleHash
        return payload
    
    def hash(self):
        return cryptography.hash_string(dumps(self.build_payload()))