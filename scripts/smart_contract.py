from certificate import Certificate
from json import dumps
from helpers import cryptography, timestamp

class SmartContractDefinition(Certificate):

    def __init__(self,issuerPublicKey,sourceCode):
        super().__init__(issuerPublicKey)
        self.sourceCode=sourceCode

    def build_payload(self):
        payload={}
        payload['SourceCode']=self.sourceCode
        payload['Timestamp']=timestamp.now()
        payload['issuerPublicKey']=self.issuerPublicKey
        return payload
    
    def hash(self):
        tmp=""
        for item in self.build_payload():
            tmp+=str(item)
        tmp+=str(self.timestamp)
        return cryptography.hash_string(tmp)
    
    def instantiate_contract(self):
        exec(self.sourceCode)
        return locals()['SmartContract'](self.issuerPublicKey)
    
    @staticmethod
    def get_smart_contract_at_current_state(blockchain,targetSmartContractHash):
        history=[]
        for b in blockchain.blockList:
            for c in b.certificateList:
                if isinstance(c,SmartContractDefinition):
                    if c.hash()==targetSmartContractHash:
                        history.append(c)
                elif isinstance(c,SmartContractWritingOperation):
                    if c.targetSmartContractHash==targetSmartContractHash:
                        history.append(c)
        history=sorted(history,key=lambda x:x.timestamp)
        contract=history[0].instantiate_contract()
        for c in history[1:]:
            c.apply_on_contract(contract)
        return contract

    @staticmethod
    def find_trending_bets(blockchain):
        bet_totals = []
        encountered_contracts = set()
    
        for block in blockchain.blockList:
            for cert in block.certificateList:
                if isinstance(cert, SmartContractDefinition):
                    contract = SmartContractDefinition.get_smart_contract_at_current_state(blockchain, cert.hash())
                
                    if contract.type == "BET":
                        total_mises = sum(bet['Amount'] for bet in contract.betters)
                    
                        if contract.description not in encountered_contracts:
                            bet_totals.append({'contract_Owner': contract.ownerPublicKey[256:264] ,'contract_desc': contract.description, 'total_mises': total_mises})
                            encountered_contracts.add(contract.description)

        bet_totals = sorted(bet_totals, key=lambda x: x['total_mises'], reverse=True)
        return bet_totals

    
class SmartContractWritingOperation(Certificate):

    def __init__(self, issuerPublicKey,targetSmartContractHash,targetFunctionName,functionArgumentList):
        super().__init__(issuerPublicKey)
        self.targetSmartContractHash=targetSmartContractHash
        self.targetFunctionName=targetFunctionName
        self.functionArgumentList=functionArgumentList

    def build_payload(self):
        payload={}
        payload['issuerPublicKey']=self.issuerPublicKey
        payload['Timestamp']=self.timestamp
        payload['targetFunctionName']=self.targetFunctionName
        payload['targetContractHash']=self.targetSmartContractHash
        #payload['functionArgumentList']=dumps(self.functionArgumentList)
        return payload
    
    def hash(self):
        return cryptography.hash_string(dumps(self.build_payload()))

    
    def apply_on_contract(self,contractPythonObject):
        args=self.functionArgumentList[:]
        args.insert(0,self.timestamp)
        args.insert(0,self.issuerPublicKey)
        getattr(contractPythonObject,self.targetFunctionName)(*args)

    
