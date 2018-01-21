__author__ = 'yashwanth'
import World
import threading
import time
import random
import optparse
import matplotlib.pyplot as plt

discount = 0.5
alpha = 0.3
iters = 3000
actions = World.actions
states = []
Q = World.Q
first = -1
title = ""
sarsa = False
graph_iters = 0
chooseAction = lambda state: chooseActionEploit(state)

for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

for state in states:
    for action in actions:
        World.set_cell_score(state, action, Q.get((state,action,False),0.0))


def do_action(action):
    s = World.player
    # r = -World.score
    World.currCost = 0
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r = World.currCost
    if r == 0:
        r = -1
    return s, action, r, s2

def Sarsa(s, a, alpha, reward, inc):
    val = World.playerHasBlock
    if reward == 12:
        val = not val
    Q[(s, a, val)] = Q.get((s, a, val),0.0) * (1 - alpha)
    Q[(s, a, val)] = float(Q.get((s, a, val),0.0)) + (alpha * inc)
    World.set_cell_score(s, a, Q.get((s, a, val)))

def chooseActionGreedy(s,sarsa=False):
    val = World.playerHasBlock
    q = [Q.get((s, a, val), 0.0) for a in actions]
    maxQ = max(q)
    count = q.count(maxQ)
    # In case there're several state-action max values
    # we select a random one among them
    if count > 1:
        best = [i for i in range(len(actions)) if q[i] == maxQ]
        i = random.choice(best)
    else:
        i = q.index(maxQ)
    act = actions[i]
    return act, Q.get((s, act, val), 0.0)

def chooseActionEploit(state,sarsa=False):
    if random.random() <= 0.85:
        return chooseActionGreedy(state,sarsa)
    else:
        return chooseActionRandom(state,sarsa)

def chooseActionRandom(state,sarsa=False):
    val = World.playerHasBlock
    action = random.choice(actions)
    if sarsa:
        return action, Q.get((state, action, val), 0.0)
    q = max([Q.get((state, a, val), 0.0) for a in actions])
    return action, q

def inc_Q(s, a, alpha, reward, inc):
    val = World.playerHasBlock
    if reward == 12:
        val = not val
    Q[(s, a, val)] = Q.get((s, a, val),0.0) * (1 - alpha)
    Q[(s, a, val)] = float(Q.get((s, a, val),0.0)) + (alpha * inc)
    World.set_cell_score(s, a, Q.get((s, a, val)))


def printQvalues():
    for i in sorted(Q):
        # print (i, Q.get(i))
        print(i)
        print('\t'*4+str(Q.get(i)))
    print ("------------------------------------------------------------")
    print ("Bank account: ",World.score)



def run():
    global discount,alpha, iters, first, title, graph_iters
    time.sleep(1)
    t = 1
    while True and iters >= 0:
        while first >= 0:
            iters -= 1
            first -= 1
            s = World.player
            act, val = chooseActionRandom(s)
            (s, a, r, s2) = do_action(act)

            # Update Q
            act, val = chooseActionRandom(s2)
            Learn(s, a, alpha, r, r + discount * val)

            # Check if the game has restarted
            t += 1.0
            if World.has_restarted():
                printQvalues()
                World.restart_game()
                time.sleep(0.01)
                t = 1.0
            time.sleep(0.01)

        # Continue Normal
        iters -= 1
        s = World.player
        act, val = chooseAction(s)
        (s, a, r, s2) = do_action(act)

        # Update Q
        act, val = chooseAction(s2)
        Learn(s, a, alpha, r,r + discount * val)

        # Check if the game has restarted
        t += 1.0
        if World.has_restarted():
            printQvalues()
            World.restart_game()
            time.sleep(0.01)
            t = 1.0

        # Speed of player
        time.sleep(0.01)

    printQvalues()
    fig = plt.figure()
    graph_iters = [a for a in range(len(World.bank))]
    plt.plot(graph_iters, World.bank)
    plt.title(title)
    fig.savefig(title+".png")


def parseOptions():
    optParser = optparse.OptionParser()
    optParser.add_option('-e', '--experiment',action='store',
                         type='int',dest='experiment',default=1,
                         metavar="E", help='Experiment number 1, 2 or 3')


    opts, args = optParser.parse_args()
    return opts

if __name__ == '__main__':

    opts = parseOptions()
    print ("Running Experiment ",opts.experiment)
    if opts.experiment == 1:
        chooseAction = lambda s: chooseActionGreedy(s)
        Learn = lambda state, action, alpha, reward, i: inc_Q(state, action, alpha, reward, i)
        iters = 3000
        first = 3000
        title = "Experiment1"
        graph_iters = iters
    elif opts.experiment == 2:
        chooseAction = lambda s: chooseActionEploit(s)
        Learn = lambda state, action, alpha, reward, i: inc_Q(state, action, alpha, reward, i)
        iters = 6000
        first = 200
        title = "Experiment2"
        graph_iters = iters
    elif opts.experiment == 3:
        chooseAction = lambda s: chooseActionEploit(s,sarsa=True)
        Learn = lambda state, action, alpha, reward, i: Sarsa(state, action, alpha, reward, i)
        iters = 6000
        sarsa = True
        first = 200
        title = "Experiment3"
        graph_iters = iters

    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    World.start_game()
    printQvalues()