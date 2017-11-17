from qlearn import QLearn


class State:
   def __init__(self,x,y,pickup=False,dropoff=False):
       # actions = ["N","E","W","S"]
       # self.actions = actions
       self.pickup = pickup
       self.dropoff = dropoff
       if pickup:
           self.pblocks = 4
       if dropoff:
           self.dblocks = 0
       self.locationX = x
       self.locationY = y

class Agent:
    def __init__(self):
        self.hasBlock = False

def nextState(action,state):
    x = state.locationX
    y = state.locationY
    # print (x,y)
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

    # print ("after",x,y)
    return next((s for s in states if s.locationX == x and s.locationY == y), None)


def printData(state,reward,act,bank,iter):
    print(iter,"Pos:",state.locationX,state.locationY,"action:",act,"reward:",reward,"Bank:",bank)


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

agent = Agent()

bankAccount = 0

# Initial state is 1,5
Q = QLearn(["N","E","W","S"])


def startSolver():
    # global dropCount,bankAccount
    bankAccount = 0

    initialState = next((x for x in states if x.locationX == 1 and x.locationY == 5), None)
    action = Q.chooseActionGreedy((initialState.locationX, initialState.locationY))
    state = nextState(action, initialState)
    reward = -1
    bankAccount += reward
    Q.learn(initialState, action, reward, state)
    dropCount = 0
    i = 0
    while i < 3000 and dropCount < 16:
        i += 1
        reward = -1
        a = 0
        if state.pickup and not agent.hasBlock and state.pblocks >= 1:
            state.pblocks -= 1
            reward = 12
            agent.hasBlock = True
            a = 1
        elif state.dropoff and agent.hasBlock and state.dblocks < 8:
            state.dblocks += 1
            reward = 12
            agent.hasBlock = False
            dropCount += 1
            a = 2

        action = Q.chooseActionGreedy((state.locationX, state.locationY))
        state1 = nextState(action, state)

        bankAccount += reward

        printData(state, reward, a, bankAccount, i)
        Q.learn(state, action, reward, state1)
        state = state1


# https://stackoverflow.com/questions/7125467/find-object-in-list-that-has-attribute-equal-to-some-value-that-meets-any-condi



startSolver()

print(Q.q)





