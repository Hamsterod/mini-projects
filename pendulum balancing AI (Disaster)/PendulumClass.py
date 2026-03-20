import math

from pygame import Vector2

class Pendulum:
    def __init__(self, position, dist, angular_acceleration, angular_velocity, angular_damp, angle):
        self.position = position
        self.dist = dist
        self.angular_acceleration = angular_acceleration
        self.angular_velocity = angular_velocity
        self.angular_damp = angular_damp
        self.angle = angle
        self.last_update = 0
        self.score = 0

    def move(self, pivot_position, pivot_acceleration, dt):
        self.angular_acceleration = (9.81/self.dist)*math.cos(self.angle) + (pivot_acceleration/self.dist)*math.sin(self.angle)
        self.angular_velocity += self.angular_acceleration * dt
        self.angular_velocity *= self.angular_damp
        self.angle += self.angular_velocity * dt
        self.position = pivot_position + Vector2(math.cos(self.angle), math.sin(self.angle)) * self.dist

    def get_next_state(self, pivot_acceleration, dt):
        next_angular_acceleration = (9.81/self.dist)*math.cos(self.angle) + (pivot_acceleration/self.dist)*math.sin(self.angle)
        next_angular_velocity = self.angular_velocity + next_angular_acceleration * dt
        next_angular_velocity *= self.angular_damp
        next_angle = self.angle + next_angular_velocity * dt

        return str(int(math.degrees(next_angle) % 360)) + "/" + str(int(next_angular_velocity))

    def update_score(self, time):
        if 180 <= math.degrees(self.angle) % 360 <= 360:  # Up
            if time > self.last_update + 100:
                self.score += 2
                self.last_update = time
        elif 45 <= math.degrees(self.angle) % 360 <= 135: # Down
            if time > self.last_update + 100:
                self.score -= 3
                self.last_update = time

    def get_score(self):
        if 180 <= math.degrees(self.angle) % 360 <= 360:  # Up
            return 2
        elif 45 <= math.degrees(self.angle) % 360 <= 135: # Down
            return -3
        else:
            return -1

    def update_state(self):
        state = ""

        state += str(int(math.degrees(self.angle) % 360)) + "/"
        state += str(int(self.angular_velocity))

        return state