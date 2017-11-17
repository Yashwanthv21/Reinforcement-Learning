import numpy as np
import math,sys,os
import time
import itertools
import random


#Global Variables
alpha=0.3
states=[]
discount = 0.5 #gamma
allstates=[[i,j ]for i in range (1,6) for j in range(1,6) ]
initial_state = [1,5]

pick = [[1,1],[3,3],[5,5],[4,1]]
drop = [[5,1],[4,4]]
global Bank_account
Bank_account=0
Bank=[]
step=1
prev_state=None
Q_values={}

def find_index(target, myList):
    for i in range(len(myList)):
        if myList[i] == target:
            return i



def Reward(variable):
    if(variable == "pick"):
        r=12
    elif(variable == "drop"):
        r=-12
    else:
        r=-1
    return r
 


class States(object):
    def __init__(self, state):
        pick = [[1,1],[3,3],[5,5],[4,1]]
        drop = [[5,1],[4,4]]
        self.name = state
        self.pickup=4
        self.dropoff=0
        self.actions=['e','w','n','s']
        for i in range(len(self.actions)):
            a=self.name[0]
            b=self.name[1]
            key=(a,b,self.actions[i])
            Q_values[key]=0.0




def aplop(state,x,op):
    #print pick
    #print drop
    #print [i,j]
    i=state.name[0]
    j=state.name[1]
    
    if([i,j] in pick):
        var= "pick"
    elif([i,j] in drop):
        var= "drop"
    else:
        var=None
    if(op==0):
        action= PRandom(state)
    elif(op==1):
        action= PExploit(state)
    elif(op==2):
        action= PGreedy(state)
    return var,action
    
def PRandom(state):
    operator = random.choice(state.actions)
    return operator

def PExploit(state):
    m,ind=get_max_value(state)
    if(ind == 0):
        op='e'
    elif(ind==1):
        op='w'
    elif(ind==2):
        op='n'
    else:
        op='s'
    
    seed=random.uniform(0, 1)
    if(seed<0.15):
        operator = random.choice(state.actions)
    else:
        operator=op

    
    return operator
    

def PGreedy(state):
    m,ind=get_max_value(state)
    if(ind == 0):
        operator='e'
    elif(ind==1):
        operator='w'
    elif(ind==2):
        operator='n'
    else:
        operator='s'
    
    return operator
    
    

def apply_op(state,x,option):
    i=state.name[0]
    j=state.name[1]
    var,op=aplop(state,x,option)
    #print op
    rew_this_step=0
    if(var == "pick"):
        rew_this_step+=Reward(var)
        x=1
        state.pickup-=1
        #print Bank_account
    elif((var == "drop")):
        rew_this_step+=Reward(var)
        x=0
        state.dropoff+=1
    
    
    l=len(op)
    rew_this_step+=Reward(op)
        
    
        #print Bank_account
    
    
    #Bank_account+=rew_this_step    #print Bank_account
    return rew_this_step,x,op

def get_max_value(state):
    values=[]
    a=state.name[0]
    b=state.name[1]
    for i in range(4):
        values.append(Q_values[(a,b,state.actions[i])])
    m,ind=max( (values[i],i) for i in xrange(len(values)) )
    return m,ind
    

def get_next_state(state,action):
    x=state.name[0]
    y=state.name[1]
    if(action=='e'):
        next_x=x
        next_y=y+1
    elif(action=='w'):
        next_x=x
        next_y=y-1
    elif(action=='n'):
        next_x=x-1
        next_y=y
    elif(action=='s'):
        next_x=x+1
        next_y=y
    
    new_cord=[next_x,next_y]
    if (new_cord in allstates):
        
        new_index=find_index(new_cord,allstates)
        next_state=states[new_index]
    else:
        next_state=None
        
    return next_state
    


def Qlearn(state,x,op):  
    #action = aplop(state,x,op)

    #print state.name,action
    
    #step=step+1
    i=state.name[0]
    j=state.name[1]
    #print i,j
    #x_init=0
    reward,new_x,action=apply_op(state,x,op)
    #print Reward
    next_state=get_next_state(state,action)
    if(next_state==None):
        m=0
    else:
        m,ind=get_max_value(next_state)
   
    
    q=Q_values[(i,j,action)]
    #print q
    #Applying the formula

    
    new_q=(1-alpha)*q + alpha*(reward+ (discount*m))
    #print new_q
    Q_values[(i,j,action)] = new_q
    if(next_state==None):
        next_state=state
    if(state.pickup==0 and state.name in pick):
        #REMOVE ELEMENT FROM PICK
        #print state.name, "pick", pick
        pick.remove(state.name)
        #print "pick now",pick
    if(state.dropoff==8 and state.name in drop):
        drop.remove(state.name)
        print "DRop", drop, state.name
    if not drop:
        #RESET
        print "RESET"
        ini=[1,5]
        ini_ind=find_index(ini,allstates)
        init=states[ini_ind]
        next_state=init
        pick.append([1,1])
        pick.append([3,3])
        pick.append([5,5])
        pick.append([4,1])
        drop.append([5,1])
        drop.append([4,4])
       
    
    Bank.append(reward)
    print new_q, next_state.name
    return next_state,new_x

'''
op= 0 PRandom
op=1 PExploit
op=2 PGreedy
'''
def SARSA(state,x,op):
    i=state.name[0]
    j=state.name[1]
    reward,new_x,action=apply_op(state,x,op)
    next_state=get_next_state(state,action)
    if(next_state==None):
        m=0
    else:
        reward_, new_x_, next_action=apply_op(next_state,x,op)
        ii=next_state.name[0]
        jj=next_state.name[1]
        m=Q_values[(ii,jj,next_action)]

   
    
    q=Q_values[(i,j,action)]
    #Applying the formula
    
    new_q=(1-alpha)*q + alpha*(reward+ (discount*m))
    
    Q_values[(i,j,action)] = new_q
    if(next_state==None):
        next_state=state
    if(state.pickup==0 and state.name in pick):
        #REMOVE ELEMENT FROM PICK
        pick.remove(state.name) 
    if(state.dropoff==8):
        #RESET
        ini=[1,5]
        ini_ind=find_index(ini,allstates)
        init=states[ini_ind]
        next_state=init
        pick.append([1,1])
        pick.append([3,3])
        pick.append([5,5])
        pick.append([4,1])
       
    Bank.append(reward)
    print new_q, next_state.name
    return next_state,new_x


def Experiment1(initial):

 
    num_steps=3000
    print "Experiment1"
    print "-----"
    print "PRANDOM"
    for step in range(1,num_steps):
        if(step==1): 
            agent,x = Qlearn(initial,0,0)
        else:
            agent,x = Qlearn(agent,x,0)
        
        step+=1
    print "-----"
    print "PGREEDY"
    for step in range(1,num_steps):
        if(step==1): 
            agent,x = Qlearn(initial,0,0)
        else:
            agent,x = Qlearn(agent,x,2)
        
        step+=1

def Experiment2(initial):
    
    num_steps=6000
    print "Experiment2"

    print "-----"
    for step in range(1,201):
        if(step==1): 
            agent,x = Qlearn(initial,0,0)
        else:
            agent,x = Qlearn(agent,x,0)
        step+=1

    print "-----"   
    for step in range(201,6000):

        agent,x = Qlearn(agent,x,1)

        step+=1


def Experiment3(initial):
  
    print 'Experiment3:Implementing SARSA'
    for step in range(1,201):
        if(step==1): 
            agent,x = SARSA(initial,0,0)
        else:
            agent,x = SARSA(agent,x,0)
        step+=1

    print "-----"   
    for step in range(201,6000):

        agent,x = SARSA(agent,x,1)

        step+=1


def main():
    for i in range(25):
        states.append(States(allstates[i]))

    ini=[1,5]
    index=find_index(ini,allstates)
    initial=states[index]
    
    Experiment1(initial)
    Bank_account=sum(Bank)
    print "Bank_account",Bank_account
   



if __name__ == "__main__":
    main()


