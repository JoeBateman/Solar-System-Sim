from vpython import *
import numpy as np
import time

G = 6.67*10**(-11)
AU = 1.496*10**11
HOUR = 3600
DAY = 86400
YEAR = 3.154*10**7

### Defining planetary data to be used
mercury_data = [0.39*AU, 48236, 3.3*10**23]
venus_data = [0.723*AU, 35008, 4.87*10**24]
earth_data = [AU, 29784, 5.98*10**24]
mars_data = [1.524*AU, 24134, 6.42*10**23]
jupiter_data = [5.203*AU, 13072, 1.90*10**27]
saturn_data = [9.539*AU, 9651, 5.69*10**26]
uranus_data = [19.18*AU, 6799, 8.68*10**25]
neptune_data = [30.06*AU, 5435, 1.02*10**26]


def angular_speed(mass, radius):
    # Function to determine the angular speed of an orbiting object
    return np.sqrt(G*mass/r**3)
           
### Creating visible axes for the simulation to help the user orientate
### themselves
xaxis=cylinder(pos=vector(-2*AU,0,0), axis=vector(4*AU,0,0), radius=0.01*AU)
yaxis=cylinder(pos=vector(0,-2*AU,0), axis=vector(0,4*AU,0), radius=xaxis.radius)
zaxis=cylinder(pos=vector(0,0,-2*AU), axis=vector(0,0,4*AU), radius=xaxis.radius)
scene.background = color.black
[distant_light(direction=vector( 0.22,  0.44,  0.88),       color=color.gray(0.8)),
 distant_light(direction=vector(-0.88, -0.22, -0.44),       color=color.gray(0.3))]
local_light(pos=vector(0,0,0), color=color.yellow)
scene.range=5*AU


### Defining 1 solar mass, and the position of the sun
MASS= 1.988*10**(30)
MASS_POS = np.array([0,0,0])

def force_grav(mass, pos):
    # Calculating a vector force on an object due to the graviational force of
    # another object
    distance = np.sqrt((pos.x-MASS_POS[0])**2 + (pos.y-MASS_POS[1])**2 + (pos.z-MASS_POS[2])**2)#np.linalg.norm(np.asarray(pos)-np.asarray(MASS_POS))
    force = -G*MASS*mass/(distance)**2
    return force*(pos.x/distance), force*(pos.y/distance), force*(pos.z/distance)


def pos_change(mass, v_0, pos_0, step):
    # Function used to numerically calculate the change in position and velocity
    # due to the forces acting upon it. 
    a = np.asarray(force_grav(mass, pos_0))/mass
    v_0.x = v_0.x + step*a[0]
    pos_0.x = pos_0.x + step * v_0.x
    v_0.y = v_0.y + step*a[1]
    pos_0.y = pos_0.y + step * v_0.y
    v_0.z = v_0.z + step*a[2]
    pos_0.z = pos_0.z + step * v_0.z 

    
    return pos_0, v_0

### Ratio of radii of planets to radius of earth, as well as scale value for
### visualisation
radii = [0.3779527559055118, 0.952755905511811, 1, 0.5275590551181103, 11.181102362204726, 9.448818897637796, 4.015748031496063, 3.7795275590551185]
sun_rad = 1 #  actually 109.2983833, but will obscure other planets of used 
scale = 0.05

### Creating objects for the sun & planets, as well as relative size and colour
sun = sphere(pos=vector(MASS_POS[0],MASS_POS[1], MASS_POS[2]), radius=sun_rad*scale*AU, color=color.yellow)
mercury = sphere(pos=vector(mercury_data[0],0,0), radius=radii[0]*scale*AU, color=color.gray(0.8))
mercury.velocity = vector(0,0,mercury_data[1])
venus = sphere(pos=vector(venus_data[0],0,0), radius=radii[1]*scale*AU, color=color.yellow)
venus.velocity = vector(0,0,venus_data[1])
earth = sphere(pos=vector(earth_data[0],0,0), radius=radii[2]*scale*AU, color=color.green)
earth.velocity = vector(0,0,earth_data[1])
mars = sphere(pos=vector(mars_data[0],0,0), radius=radii[3]*scale*AU, color=color.red)
mars.velocity = vector(0,0,mars_data[1])
jupiter = sphere(pos=vector(jupiter_data[0],0,0), radius=radii[4]*scale*AU, color=color.orange)
jupiter.velocity = vector(0,0,jupiter_data[1])
saturn = sphere(pos=vector(saturn_data[0],0,0), radius=radii[5]*scale*AU, color=color.yellow)
saturn.velocity = vector(0,0,saturn_data[1])
uranus = sphere(pos=vector(uranus_data[0],0,0), radius=radii[6]*scale*AU, color=color.white)
uranus.velocity = vector(0,0,uranus_data[1])
neptune = sphere(pos=vector(neptune_data[0],0,0), radius=radii[7]*scale*AU, color=color.blue)
neptune.velocity = vector(0,0,neptune_data[1])

### Creating lists of planet names and data
planets = (mercury,venus,earth,mars,jupiter,saturn,uranus,neptune)
planet_data = (mercury_data,venus_data,earth_data,mars_data,jupiter_data,saturn_data,uranus_data,neptune_data)

### Creating a while loop for the simulation to run, and an end condition
time=0
while time < 50000:
    rate(50)
    step = 84600
    for i, planet in enumerate(planets):

        planet.pos, planet.velocity = pos_change(planet_data[i][2], planet.velocity, planet.pos, step)