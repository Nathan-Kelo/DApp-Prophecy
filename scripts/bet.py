class SmartContract():
    def __init__(self,ownerPublicKey):
        self.ownerPublicKey=ownerPublicKey
        self.description=None
        self.startTime=None
        self.closingPeriod=None
        #dictionnary of betters with their public key, the amount staked, and the outcome they want
        self.betters=[]
        #list of strings for different outcomes
        self.outcomes=[]
        self.logs=[]
        self.type="BET"

#these two functions are to be called outside blockchain only_______________    
    def display(self,*args):
        print(self.description)
        for i,o in enumerate(self.outcomes):
            print(f'Select {i+1} for {o}')
        print(self.closingPeriod)
        print('Current betters---------')
        total={}
        for b in self.betters:
            print(f"User {b['PublicKey'][256:264]} bet {b['Amount']} on {b['Outcome']}.")
            if b['Outcome'] in total.keys():
                total[b['Outcome']]+=b['Amount']
            else:
                total[b['Outcome']]=b['Amount']
        print(total)
    
    def logDump(self,*args):
        for l in self.logs:
            print(l)
#___________________________________________________________________________
            
    def startBet(self, callerPublicKey,callTimestamp, closingPeriod,description,outcomes):
        if(callerPublicKey != self.ownerPublicKey):
            self.logs.append(f"[ERROR] {callerPublicKey[256:264]} tried modifying contract but is not owner.")
            return
        if(callTimestamp>closingPeriod):
            self.logs.append(f"[ERROR] closing period ends before bet starts.")
            return
        if(self.closingPeriod!=None):
            self.logs.append(f"[ERROR] already started a bet, cannot start again.")
            return
        self.closingPeriod=closingPeriod
        self.description=description

        self.outcomes=outcomes
        self.startTime=callTimestamp
        self.logs.append(f'[BET] Started new bet.')
        print('-------------sfsfs----------------------------',closingPeriod)

    
    def closeBet(self, callerPublicKey, callTimestamp,outcome):
        if callerPublicKey!=self.ownerPublicKey:
            self.logs.append(f"[ERROR] {callerPublicKey[256:264]}")
        self.closingPeriod=-1
        self.logs.append(f'[BET] Redistributing winnings...')
        self.redistributePebbles(outcome)
        self.logs.append(f'[BET] Redistributed winnings.')


    def redistributePebbles(self, winningOutcome):
        if winningOutcome < 1 or winningOutcome>len(self.outcomes):
            self.logs.append(["[ERROR] outcome not in list of possible outcomes."])
            return
        winningstaked=0
        rest=0
        for b in self.betters:
            if b['Outcome']==self.outcomes[winningOutcome-1]:
                winningstaked+=b['Amount']
            else:
                rest+=b['Amount']
        multiplier=rest/winningstaked
        for b in self.betters:
            b['Account'].addPebble(b['Amount'] + b['Amount']*multiplier)
            pass
    

    def addBetter(self,betterPublicKey,callTimestamp,betterAccount,amount,outcome):
        betterPublicKey = betterAccount.issuerPublicKey
        if amount<0:
            self.logs.append(f'[ERROR] cannot stake negative amount.')
        if betterAccount.pebbleAmount<amount:
            self.logs.append(f'[ERROR] {betterPublicKey[256:264]} does not have enough pebbles.')
            return
        if callTimestamp>self.closingPeriod:
            self.logs.append(f"[ERROR] {betterPublicKey[256:264]} tried betting after closing period.")
            return
        for b in self.betters:
            if b['PublicKey']==betterPublicKey and b['Outcome']!=self.outcomes[outcome-1]:
                self.logs.append(f'[ERROR] {betterPublicKey[256:264]} cannot bet on a different outcome.')
                return
            elif b['PublicKey']==betterPublicKey and b['Outcome']==self.outcomes[outcome-1]:
                b['Amount']+=amount
                betterAccount.removePebble(amount)
                print(betterAccount.pebbleAmount)
                self.logs.append(f'[BET] {betterPublicKey[256:264]} added more to his bet.')
                return
        self.betters.append({'PublicKey':betterPublicKey, 'Account': betterAccount,'Amount':amount,'Outcome':self.outcomes[outcome-1]})
        betterAccount.removePebble(amount)
        print(betterAccount.pebbleAmount)
        self.logs.append(f"[BET] Added better {betterPublicKey[256:264]}.")
        return