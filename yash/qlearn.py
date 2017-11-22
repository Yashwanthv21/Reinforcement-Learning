import random


class QLearn:
    def __init__(self, actions, alpha=0.3, gamma=0.5):
        self.q = {}

        self.alpha = alpha      # discount constant
        self.gamma = gamma
        self.actions = actions

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)
        # return self.q.get((state, action), 1.0)

    def learnQ(self, state, action, reward, value):
        '''
        Q-learning:
            Q(s, a) += alpha * (reward(s,a) + max(Q(s') - Q(s,a))
        '''
        oldv = self.q.get((state, action), None)
        if oldv is None:
            # self.q[(state, action)] = reward
            self.q[(state, action)] = self.alpha * value
        else:
            # self.q[(state, action)] = oldv + self.alpha * (value - oldv)
            self.q[(state, action)] = (1-self.alpha)*oldv + self.alpha*value

    def chooseActionGreedy(self, state):

        q = [self.getQ(state, a) for a in self.actions]
        maxQ = max(q)
        count = q.count(maxQ)
        # In case there're several state-action max values
        # we select a random one among them
        if count > 1:
            best = [i for i in range(len(self.actions)) if q[i] == maxQ]
            i = random.choice(best)
        else:
            i = q.index(maxQ)

        action = self.actions[i]
        return action

    def chooseActionEploit(self, state):
        if random.random() <= 0.85:
            return self.chooseActionGreedy(state)
        else:
            return self.chooseActionRandom(state)

    def chooseActionRandom(self, state):
        action = random.choice(self.actions)
        return action

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)
