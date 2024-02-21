#used for cleaner prints can get rid of it after testing
import math

def best_profit(history):
    holding=0
    investement=1
    sens=None
    i=0
    buy_points=[]
    while i < len(history)-1:
        if history[i+1]<history[i]and(sens=="asc"or sens==None):
            investement=history[i]*holding
            buy_points.append((i,history[i]))
            sens="desc"
        elif history[i+1]>history[i]and(sens=="desc"or sens==None):
            holding=investement/history[i]
            sens="asc"
            buy_points.append((i,history[i]))
        #Comme le point final n'a pas de point suivant pour rentrer dans les conditions, on n'ajoute une condition
        if(i==len(history)-2):
            if sens=="asc":
                investement=history[i+1]*holding
                buy_points.append((i+1,history[i+1]))
        #si le dernier point fait partie d'une d'un segment decroissant, on n'a pas a besoin de faire qlq chose           
        #print(f"{i} :({math.trunc(history[i]*1e3)/1e3},{math.trunc(history[i+1]*1e3)/1e3}) sens: {sens} \tholding({math.trunc(holding*1e3)/1e3})profit: {math.trunc(investement*1e3)/1e3}")
        i=i+1    
    return investement,buy_points
    