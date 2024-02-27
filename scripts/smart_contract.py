from certificate import Certificate
from json import dumps
from helpers import cryptography

class SmartContractDefinition(Certificate):

    def __init__(self,issuerPublicKey,sourceCode):
        super().__init__(issuerPublicKey)
        self.sourceCode=sourceCode

    def build_payload(self):
        payload={}
        payload['SourceCode']=self.sourceCode
        payload['Timestamp']=self.timestamp
        payload['issuerPublicKey']=self.issuerPublicKey
        return payload
    
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
