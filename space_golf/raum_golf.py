#Classen
class GolfBall():
    def __init__(self, pos, vel, dur, col):
        self.pos = pos
        self.vel = vel
        self.dur = dur
        self.col = col
    
    def physik(self):
        self.pos += self.vel
        
        if started:
            for s in schwarzlöcher:
                self.vel += (s.mas/(s.pos-self.pos).mag**2)*(s.pos-self.pos).normalize()
                
                if (s.pos-self.pos).mag-self.dur/2 < s.dur/2: #Kollision
                    self.vel = Py5Vector(0, 0)
                    Restart()
    
    def render_objekt(self):
        if started:
            schwanz.append(Py5Vector(self.pos.x, self.pos.y))
            for p in range(len(schwanz)):
                if p > 1:
                    stroke(255)
                    stroke_weight(p*self.dur/len(schwanz)/1.5)
                    line(schwanz[p-1].x, schwanz[p-1].y, schwanz[p].x, schwanz[p].y)
            if len(schwanz) > 300:
                schwanz.pop(0)
                
        no_stroke()
        fill(self.col)
        circle(self.pos.x, self.pos.y, self.dur)

class Schwarzloch():
    def __init__(self, pos, dur, mas):
        self.pos = pos
        self.dur = dur
        self.mas = mas

#Setup
def setup():
    global test_ball, zielend, stä, richtung, started, score, ziel_pos, ziel_dur, schwarzlöcher, schwanz
    size(900, 500)
    
    #Variabeln
    started = False
    zielend = False
    stä = 0
    richtung = Py5Vector(0, 0)
    score = 0
    ziel_pos = Py5Vector(width-150, height/2)
    ziel_dur = 50
    
    #Objekte
    test_ball = GolfBall(Py5Vector(150, height/2), Py5Vector(0, 0), 15, "#E07C34")
    schwanz = [Py5Vector(150, height/2)]
    
    schwarzlöcher = []
        
#Funktionen
def Physik():
    global zielend, started
    
    if zielend and not is_mouse_pressed:
        test_ball.vel = -richtung*stä/20
        zielend = False
        started = True
    
    test_ball.physik()

def Render():
    global richtung, stä, zielend, started, ziel_pos, ziel_dur, score
    background("#DBC190")
        
    if is_mouse_pressed and not started:
        #Richtungslinie
        stroke(255)
        stroke_weight(5)
        richtung = (Py5Vector(mouse_x, mouse_y) - test_ball.pos).normalize()
        stä = min(100, (Py5Vector(mouse_x, mouse_y) - test_ball.pos).mag)
        line(test_ball.pos.x, test_ball.pos.y, test_ball.pos.x + richtung.x * stä, test_ball.pos.y + richtung.y * stä)
    
        #Text
        fill(255)
        text_size(15)
        text_align(CENTER)
        text(int(stä), test_ball.pos.x, test_ball.pos.y+test_ball.dur+10) #Stärke
        zielend = True

    #Objekte
    no_stroke()
    fill("#E07C34")
    circle(ziel_pos.x, ziel_pos.y, ziel_dur)
    fill(30)
    circle(ziel_pos.x, ziel_pos.y, ziel_dur/1.5)
    test_ball.render_objekt()
    
    for s in schwarzlöcher:
        fill(40)
        circle(s.pos.x, s.pos.y, s.dur)
    
    fill(255)
    text_size(30)
    text_align(LEFT, TOP)
    text(score, 10, 10)

def Restart():
    global schwanz, started
    started = False
    test_ball.pos = Py5Vector(150, height/2)
    test_ball.vel = Py5Vector(0, 0)
    schwanz = [test_ball.pos]
    
#Gameloop
def draw():
    global ziel_pos, ziel_dur, score, started, schwanz, schwarzlöcher
    
    Physik()
    Render()
    if (test_ball.pos-ziel_pos).mag < ziel_dur/2:
        Restart()
        schwarzlöcher.clear()
        score += 1
        for i in range(min(score, random_int(1, 4))):
            rmasse = random(10, 50)
                        
            schwarzlöcher.append(Schwarzloch(Py5Vector(width*random(0.3, 0.75), height*random(0.1, 0.9)), rmasse, rmasse*20))
    
    if is_key_pressed:
        if key in ['r', 'R']:
           Restart()