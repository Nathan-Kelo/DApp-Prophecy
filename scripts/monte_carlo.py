import random

def rain_drop(seed=True):
    if(seed):
        random.seed()
    return random.random(),random.random()

def calculate_pi(iterations):
    random.seed()
    in_cercle=0
    for i in range(iterations):
        x,y=rain_drop(False)
        if (x-0.5)**2+(y-0.5)**2-0.25 <=0:
            in_cercle=in_cercle+1
    return in_cercle/iterations*4