class Account():
    def __init__(self,issuerPublicKey):
        self.pebbleAmount=20
        self.issuerPublicKey=issuerPublicKey
        self.logs=[]

    def log(self,message):
        self.logs.append(f'[ACC {self.issuerPublicKey[256:264]}] {message}')

    def logDump(self):
        for l in self.logs:
            print(l)

    def removePebble(self,amount):
        self.pebbleAmount-=amount
        self.log(f"REMOVED {amount} | NEW BALANCE:{self.pebbleAmount}")
    
    def addPebble(self,amount):
        self.pebbleAmount+=amount
        self.log(f"ADDED {amount} | NEW BALANCE:{self.pebbleAmount}")