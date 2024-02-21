import random

class Node:
    name=""
    neighbors=[]
    message=[]
    
    def __init__(self,name):
        self.name=name
        random.seed()

    def reboot(self,connectedNodes):
        self.message=[]
        for i in range(5):
            self.message.append("")
        self.neighbors=connectedNodes

    def tell_message(self):
        tmp=f"[{self.name}]"
        for i in self.message:
            if i == "":
                tmp=tmp+" ???"
            else :
                tmp=tmp+" "+i
        return tmp

    def deliver_message_bit(self,index,message):
        if index-1 >= 0 and index-1 <= len(self.message)-1:
            if self.message[index-1] == "":
                self.message[index-1]=message
                return 0
        return 1

    def send_random_message_bit_to_neighbors(self):
        bits=[]
        for i in range(len(self.message)):
            if self.message[i]!="":
                bits.append((i+1,self.message[i]))
        if len(bits)!=0:
            choice=random.randint(0,len(bits)-1)
            for i in self.neighbors :
                i.deliver_message_bit(bits[choice][0],bits[choice][1])
            return 0
        else :
            return 1
class Simulation:
    nodeCount=None
    connectProbability=None
    crashProbability=None
    def __init__(self,nbNodes,connectProbability,crashProbability):
        self.nodeCount=nbNodes
        self.connectProbability=connectProbability
        self.crashProbability=crashProbability

    
    def reboot_node_with_random_neighbors(self, nodeToReboot, potentialNeighbors):
        neighbors=potentialNeighbors.copy()
        neighbors.remove(nodeToReboot)
        neighbors=list(filter(lambda i:random.random()<=self.connectProbability,neighbors))
        nodeToReboot.reboot(neighbors)

    def run(self,days):
        message=["taking","the","hobbits","to","isengard"]
        nodes=[]
        
        #Initialization day 1
        for i in range(self.nodeCount):
            nodes.append(Node(f"Noeud {i+1}"))
        for i in nodes:
            self.reboot_node_with_random_neighbors(i,nodes)
            i.message=message.copy()            
            
        print("----Start of simulation----")
        for j in nodes:
            print(j.tell_message())
            
        #Starting the simulation
        for i in range(days):
            for j in nodes:
                if random.random()<=self.crashProbability:
                    #print(f"[Day {i+1}] {j.name} has crashed !")
                    self.reboot_node_with_random_neighbors(j,nodes)
                else :
                    j.send_random_message_bit_to_neighbors()

        print("----End of simulation----")
        for j in nodes:
            print(j.tell_message())
    
        
        