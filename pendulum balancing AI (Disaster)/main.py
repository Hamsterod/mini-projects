import math
import Agent

import pygame
from pygame import Vector2

import PendulumClass
import PendulumPivotClass

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pendulum", "Pendulum")
my_font = pygame.font.SysFont('Roboto MS', 50)
clock = pygame.time.Clock()
running = True

player = PendulumPivotClass.PendulumPivot(0, 0, [-500, 500], 0, 1.03, 50)
pendulum = PendulumClass.Pendulum(Vector2(0, 0), 100, 0, 0, 0.99, math.radians(90))

last_QTable = Agent.QTable

def update():
    player.move(dt, pendulum.update_state(), pendulum)
    pendulum.move(Vector2(player.position, 0), player.acceleration, dt)
    pendulum.update_score(pygame.time.get_ticks())

def render():
    screen.fill("#f5e9d0")

    text_surface3 = my_font.render('"Brain Size": ' + str(len(Agent.QTable)), True, "#e85b3f")
    text_surface2 = my_font.render('Best Score: ' + str(last_score), True, "#e85b3f")
    text_surface1 = my_font.render('Generation: ' + str(generation), True, "#e85b3f")
    text_surface = my_font.render('Score: ' + str(pendulum.score), True, "#e85b3f")
    screen.blit(text_surface3, (Vector2(screen.get_width() / 2 + player.margin[1] - 300, screen.get_height() / 2 - 60)))
    screen.blit(text_surface2, (Vector2(screen.get_width() / 2 + player.margin[0], screen.get_height() / 2 - 30)))
    screen.blit(text_surface1, (Vector2(screen.get_width() / 2 + player.margin[1] - 300, screen.get_height() / 2 - 30)))
    screen.blit(text_surface, (Vector2(screen.get_width()/2 + player.margin[0], screen.get_height()/2 - 60)))

    pygame.draw.line(screen, "#e85b3f", Vector2(screen.get_width()/2 + player.margin[0], screen.get_height()/2),
                     Vector2(screen.get_width()/2 + player.margin[1], screen.get_height()/2), 4)

    pygame.draw.line(screen, "#eba536", Vector2(screen.get_width()/2 + player.position, screen.get_height()/2),
                     Vector2(screen.get_width()/2 + pendulum.position.x,
                             screen.get_height()/2 + pendulum.position.y), 4)
    pygame.draw.circle(screen, "#f58973", Vector2(screen.get_width()/2 + player.position, screen.get_height()/2), 10)
    pygame.draw.circle(screen, "#e85b3f", Vector2(screen.get_width() / 2 + player.position, screen.get_height() / 2),13, 4)
    pygame.draw.circle(screen, "#f5c373", Vector2(screen.get_width()/2 + pendulum.position.x, screen.get_height()/2 + pendulum.position.y), 15)
    pygame.draw.circle(screen, "#eba536", Vector2(screen.get_width() / 2 + pendulum.position.x,screen.get_height() / 2 + pendulum.position.y), 18, 4)

    pygame.display.flip()

# Main Loop
last_reset = 0
last_score = -1000
generation = 0
while running:
    if pygame.time.get_ticks() > last_reset + 10000:

        if pendulum.score > last_score:
            last_QTable = Agent.QTable
            last_score = pendulum.score
        #else:
        #    Agent.QTable = last_QTable


        player.position = 0
        player.velocity = 0
        player.acceleration = 0

        pendulum.score = 0
        pendulum.angular_velocity = 0
        pendulum.angular_acceleration = 0
        pendulum.angle = 90
        pendulum.position = Vector2(0, 0)

        generation += 1
        last_reset = pygame.time.get_ticks()
    dt = clock.tick(60) / 100
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game Loop
    update()
    render()

print(Agent.QTable)
pygame.quit()