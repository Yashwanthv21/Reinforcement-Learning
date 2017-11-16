from qlearn import QLearn


class State:
   def __init__(self,x,y,pickup=False,dropoff=False):
       # actions = ["N","E","W","S"]
       # self.actions = actions
       self.pickup = pickup
       self.dropoff = dropoff
       self.blocks = 0
       if pickup:
           self.blocks = 4
       self.locationX = x
       self.locationY = y



def nextState(action,state):
    x = state.locationX
    y = state.locationY
    print (x,y)
    if action == "E":
        if y < 5:
            y += 1
    elif action == "W":
        if y > 1:
            y -= 1
    elif action == "N":
        if x > 1:
            x -= 1
    elif action == "S":
        if x < 5:
            x += 1

    reward = -1
    print ("after",x,y)
    return next((s for s in states if s.locationX == x and s.locationY == y), None),reward

states = []

states.append(State(1,1,True))
states.append(State(1,2))
states.append(State(1,3))
states.append(State(1,4))
states.append(State(1,5))

states.append(State(2,1))
states.append(State(2,2))
states.append(State(2,3))
states.append(State(2,4))
states.append(State(2,5))

states.append(State(3,1))
states.append(State(3,2))
states.append(State(3,3,True))
states.append(State(3,4))
states.append(State(3,5))

states.append(State(4,1,True))
states.append(State(4,2))
states.append(State(4,3))
states.append(State(4,4,dropoff=True))
states.append(State(4,5))

states.append(State(5,1,dropoff=True))
states.append(State(5,2))
states.append(State(5,3))
states.append(State(5,4))
states.append(State(5,5,True))



bankAccount = 0

# Initial state is 1,5
Q = QLearn(["N","E","W","S"])

# https://stackoverflow.com/questions/7125467/find-object-in-list-that-has-attribute-equal-to-some-value-that-meets-any-condi
initialState = next((x for x in states if x.locationX == 1 and x.locationY == 5), None)

action = Q.chooseAction((initialState.locationX,initialState.locationY))

state, reward = nextState(action,initialState)

bankAccount += reward

Q.learn(initialState,action,reward,state)

i = 0
while i < 1000:
    i+=1

    action = Q.chooseAction((state.locationX, state.locationY))
    state1, reward = nextState(action, state)

    bankAccount += reward

    Q.learn(state, action, reward, state1)
    state = state1

print(Q.q)


