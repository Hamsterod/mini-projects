import math
import random

import Agent

learning_rate = 0.1
discount_factor = 0.1

class PendulumPivot:
    def __init__(self, position, velocity, margin, acceleration, damp, speed):
        self.position = position
        self.velocity = velocity
        self.margin = margin
        self.acceleration = acceleration
        self.damp = damp
        self.speed = speed

    def move(self, dt, state, pendulum):
        if Agent.QTable.get(state) is None:
            Agent.QTable.update({state: [random.randrange(-1,1), random.randrange(-1,1)]})
        if Agent.QTable.get(pendulum.get_next_state(self.acceleration, dt)) is None:
            Agent.QTable.update({pendulum.get_next_state(self.acceleration, dt): [random.randrange(-1, 1), random.randrange(-1, 1)]})

        Agent.QTable[state][0 if Agent.QTable[state][0] > Agent.QTable[state][1] else 1] = (1 - learning_rate) * Agent.QTable[state][0 if Agent.QTable[state][0] > Agent.QTable[state][1] else 1] + learning_rate * (pendulum.get_score() + discount_factor  * max(Agent.QTable[pendulum.get_next_state(self.acceleration, dt)]))
        print(Agent.QTable[state][0 if Agent.QTable[state][0] > Agent.QTable[state][1] else 1] - (1 - learning_rate) * Agent.QTable[state][0 if Agent.QTable[state][0] > Agent.QTable[state][1] else 1] + learning_rate * (pendulum.get_score() + discount_factor  * max(Agent.QTable[pendulum.get_next_state(self.acceleration, dt)])))

        if Agent.QTable[state][0] > Agent.QTable[state][1]:
            self.acceleration = -self.speed
        if Agent.QTable[state][0] < Agent.QTable[state][1]:
            self.acceleration = self.speed

        self.velocity += self.acceleration * dt

        if self.position <= self.margin[0]:
            self.velocity = math.fabs(self.velocity) * 0.8
        if self.position >= self.margin[1]:
            self.velocity = -math.fabs(self.velocity) * 0.8

        self.position += self.velocity * dt
        self.velocity /= self.damp