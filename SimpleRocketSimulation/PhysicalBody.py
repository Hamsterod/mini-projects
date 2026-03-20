class PhysicalBody:
    def __init__(self, position, velocity, mass, drag_coefficient, reference_area):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.drag_coefficient = drag_coefficient
        self.reference_area = reference_area
    
    def updatePhysics(self, a, step, d):
        speed = (self.velocity[0]**2 + self.velocity[1]**2)**0.5
        if speed != 0:
            drag_mag = (((0.5*d)*(speed**2)*self.drag_coefficient*self.reference_area)/self.mass)
            drag = [-(self.velocity[0]/speed) * drag_mag,
                    -(self.velocity[1]/speed) * drag_mag]
        else:
            drag = [0, 0]
        self.velocity = [
            self.velocity[0] + ((a[0] + drag[0]) * step),
            self.velocity[1] + ((a[1] + drag[1]) * step)]
        self.position = [self.position[0] + (self.velocity[0]*step),
                         self.position[1] + (self.velocity[1]*step)]