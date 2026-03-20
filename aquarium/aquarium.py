import py5
from py5 import *

#Utility Functions
def rotate_position(pos, ang):
    position_rotated = [pos[0]*cos(ang) - pos[1]*sin(ang), pos[0]*sin(ang) + pos[1]*cos(ang)]
    
    return position_rotated

def fancy_ellipse(pos, rad, ang):
    begin_closed_shape()
    for i in range(0, 360, 25):
        i_rad = radians(i)
        
        point_position = [rad[0]/2*cos(i_rad), rad[1]/2*sin(i_rad)]
        rotated = rotate_position(point_position, ang)
        
        vertex(rotated[0] + pos[0], rotated[1] + pos[1])
    end_shape()

def draw_background():
    for row in range(canvas_height):
        blend_colour = row / canvas_height
        stroke(18, 110 + 60 * blend_colour, 170 + 40 * blend_colour)
        line(0, row, canvas_width, row)

    no_stroke()
    fill(19, 120, 90)
    rect(0, canvas_height - 38, canvas_width, 38)

    fill(204, 182, 112)
    rect(0, canvas_height - 14, canvas_width, 14)

def sort_by_proximity(arr, pos):
    arr.sort(key = lambda p: (p.position[0] - pos[0])**2 + (p.position[1] - pos[1])**2)
    
    return arr

def get_angle(pos1, pos2):
    angle = atan2(pos2[1]-pos1[1], pos2[0]-pos1[0])
    
    return angle

def get_distance(pos1, pos2):
    return sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)

#Classes
class Fish():
    def __init__(self, position, fish_size, rotation, fish_colour, tail_colour, fish_speed, target_angle):
        self.position = position
        self.fish_size = fish_size
        self.rotation = rotation
        self.fish_colour = fish_colour
        self.tail_colour = tail_colour
        self.fish_speed = fish_speed
        self.target_angle = target_angle
    
    def draw(self):
        fill(self.tail_colour)
        
        tail_animation_x = sin(py5.frame_count*self.fish_speed/5)*self.fish_size[0]/40
        tail_animation_y = sin(py5.frame_count*self.fish_speed/10)*self.fish_size[1]/20
        
        position_offset = sin(self.position[1]*0.1)*5 + cos(self.position[0]*0.1)*5
        
        tailpoint1 = [-self.fish_size[0]/3, 0]
        tailpoint2 = [-self.fish_size[0] + tail_animation_x, -self.fish_size[1]/2 + tail_animation_y + position_offset]
        tailpoint3 = [-self.fish_size[0] + tail_animation_x,  self.fish_size[1]/2 - tail_animation_y + position_offset]
        
        tailpoint1_rotated = rotate_position(tailpoint1, self.rotation - self.target_angle*0.03)
        tailpoint2_rotated = rotate_position(tailpoint2, self.rotation - self.target_angle*0.03)
        tailpoint3_rotated = rotate_position(tailpoint3, self.rotation - self.target_angle*0.03)
        
        triangle(tailpoint1_rotated[0]+self.position[0], tailpoint1_rotated[1]+self.position[1],
                 tailpoint2_rotated[0]+self.position[0], tailpoint2_rotated[1]+self.position[1],
                 tailpoint3_rotated[0]+self.position[0], tailpoint3_rotated[1]+self.position[1])
        
        fill(self.fish_colour)
        
        fancy_ellipse(self.position, self.fish_size, self.rotation)   
        
        eye_position = [self.fish_size[0]/3, 0]
        eye_position_rotated = rotate_position(eye_position, self.rotation)
        
        fill(0)
        circle(eye_position_rotated[0] + self.position[0], eye_position_rotated[1] + self.position[1], self.fish_size[0]/12)
    
    def move(self):
        move_x = cos(self.rotation)*self.fish_speed
        move_y = sin(self.rotation)*self.fish_speed
        
        if self.position[0]+move_x > canvas_width+70 or self.position[0]+move_x < -70:
            move_x = -move_x
            move_y /= 5
            self.rotation = atan2(move_y, move_x)
        if self.position[1]+move_y > canvas_height or self.position[1]+move_y < 0:
            move_y = -move_y
            self.rotation = atan2(move_y, move_x)
        
        self.target_angle = 0
        
        if len(food_list) > 0:
            closest_food = sort_by_proximity(food_list, self.position)[0]
            
            angle_difference = get_angle(self.position, closest_food.position) - self.rotation
            
            while angle_difference > PI: angle_difference -= TWO_PI
            while angle_difference < -PI: angle_difference += TWO_PI
            
            self.target_angle = angle_difference
            
            self.rotation += angle_difference*0.01
            
            if get_distance(self.position, closest_food.position) < self.fish_size[1]/2:
                food_list.remove(closest_food)
        self.rotation += sin(self.position[1]*0.1)*0.01 + cos(self.position[0]*0.1)*0.01
        self.position = [self.position[0]+move_x, self.position[1]+move_y]
        

class Food():
    def __init__(self, position, velocity, food_size):
        self.position = position
        self.velocity = velocity
        self.food_size = food_size
    
    def draw(self):
        fill("#e26951")
        circle(self.position[0], self.position[1], self.food_size)
    
    def fall(self, g):
        self.velocity += g
        self.velocity *= 0.9*(self.food_size/10) + cos(self.position[1]*0.1)*0.01
        self.position[1] += self.velocity
        self.position[0] += sin(self.position[1]*0.1)*(0.1*self.food_size) + cos(self.position[0]*0.1)*0.01

class Bubble:
    def __init__(self, position, bubble_size):
        self.position = position
        self.bubble_size = bubble_size
    
    def draw(self):
        stroke(255, 255, 255, 100)
        fill(0, 0, 0, 0)
        circle(self.position[0], self.position[1], self.bubble_size)
    
    def rise(self):
        self.position[1] -= sin(self.position[0])*0.5 + ((self.bubble_size-10)/10) + 1
        self.position[0] += sin(self.position[1]*0.01*cos(self.position[1]*0.05))
        if self.position[1] < -50:
            self.position = [random(0, canvas_width), canvas_height+50]
            self.bubble_size = random(10, 20)

class Seaweed():
    def __init__(self, position):
        self.position = position
        
    def draw(self):
        stroke(19, 120, 90)
        
        res = 10
        for i in range(res):
            stroke_weight((i+1)*2)
            
            weed_point1 = [self.position + sin((py5.frame_count + self.position + i*res)*0.05)*(res-i),
                            canvas_height*0.4*(i/res) + canvas_height*0.5]
            weed_point2 = [self.position + sin((py5.frame_count + self.position + (i+1)*res)*0.05)*(res-i+1),
                            canvas_height*0.4*((i+1)/res) + canvas_height*0.5]
            
            line(weed_point1[0], weed_point1[1], weed_point2[0], weed_point2[1])
        stroke_weight(1)
        no_stroke()

#Setup
def settings():
    global canvas_width, canvas_height

    canvas_width = 800
    canvas_height = 400

    py5.size(canvas_width, canvas_height)

def setup():
    global fish_list, food_list, bubble_list, seaweed_list

    background(255)
    no_stroke()
    fill(0)
    
    fish_list = []
    
    for i in range(30):
        r = random(0, 255)
        g = random(0, 255)
        b = random(0, 255)
        fish_colour 	= color(r, g, b)
        tail_colour 	= color(r-10, g-20, b-30)
        position 		= [random(0.1*canvas_width, 0.9*canvas_width), random(0.1*canvas_height, 0.9*canvas_height)]
        fish_speed 		= random(0.5, 2)
        fish_rotation 	= random(TWO_PI)
        fish_size 		= random(30, 50)
        fish_list.append(Fish(position, [fish_size, fish_size/2], fish_rotation, fish_colour, tail_colour, fish_speed, 0))
    
    food_list = []
    bubble_list = []

    for i in range(25):
        bubble_pos = [random(0, canvas_width), random(0, canvas_height)]
        bubble_size = random(10, 20)
        bubble_list.append(Bubble(bubble_pos, bubble_size))
    
    seaweed_list = []

    for i in range(20):
        position = canvas_width/20*i
        
        seaweed_list.append(Seaweed(position))

#Main
def draw():
    draw_background()
    
    for seaweed in seaweed_list:
        seaweed.draw()
    
    for food in food_list:
        food.fall(0.098)
        food.draw()
        if food.position[1] > canvas_height or -50 > food.position[0] or canvas_width + 50 < food.position[0]:
            food_list.remove(food)
    
    for fish in fish_list:
        fish.move()
        fish.draw()
        
    for bubble in bubble_list:
        bubble.rise()
        bubble.draw()
    
    if py5.is_mouse_pressed:
        food_size = random(5, 10)
        food_velocity = random(1, 25)
        food_list.append(Food([py5.mouse_x+random(-20, 20), 1], food_velocity, food_size))

run_sketch()