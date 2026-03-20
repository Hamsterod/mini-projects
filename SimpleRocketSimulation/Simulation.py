import matplotlib.pyplot as plt

import PhysicalBody as pb

#Graph Parameters
y = []
t = []

#Simulation Parameters
simulation_time = 30
simulation_step = 0.001

#Simulation Constants
g = 9.81
d = 1.225

#CreatingObjects
rock1 = pb.PhysicalBody([0, 0], [0, 0], 0.73, 0.7, 0.005)

apogee = 0
step = 0
while step <= simulation_time:

    rock1.updatePhysics([0, -g + max(-(step**(2)*0.05)+15, 0)], simulation_step, d)
    print(str(rock1.position)+str("%.3f" % step))
    #Getting Apogee
    if apogee < rock1.position[1]:
        apogee = rock1.position[1]
    #Updating Graph
    t.append(step)
    y.append(rock1.position[1])
    
    step += simulation_step
plt.plot(t, y)
plt.show()
print("%.2f" % apogee)