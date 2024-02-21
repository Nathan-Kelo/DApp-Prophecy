from stake import StakingOperation
from math import trunc
from ticket import RaffleTicket
from helpers import cryptography

class ProofOfStake:
    
    def __init__(self,defaultForgerPublicKey):
        self.defaultForgerPublicKey=defaultForgerPublicKey
    
    def hash_distance(self,hash1,hash2):
        return abs(int(hash1,16)-int(hash2,16))
    
    def get_next_forger_public_key(self,blockList):
        if(blockList[-1].issuerPublicKey==cryptography.get_black_hole_public_key()):
            return self.defaultForgerPublicKey

        accounts=StakingOperation.build_staking_accounts(blockList)
        if len(accounts)==0:
            return self.defaultForgerPublicKey
        
        raffle={}
        for pKey in accounts.keys():
            distances=[]
            for nb in range(trunc(accounts[pKey])):
                distances.append(self.hash_distance(RaffleTicket(pKey,nb+1,blockList[-1].hash()).hash(),blockList[-1].hash()))
            raffle[pKey]=min(distances)
        return min(raffle,key=raffle.get)
        
    def is_next_block_forger_legit(self,blockList,nextBlock):
        return nextBlock.issuerPublicKey==self.get_next_forger_public_key(blockList)

    def is_blockchain_legit(self,blockchain):
        chain=blockchain.blockList       
        if chain[1].issuerPublicKey!=self.defaultForgerPublicKey:
            return False
        for i in range(2,len(chain)):
            if not self.is_next_block_forger_legit(chain[:i-1],chain[i]):
                return False
        return True

