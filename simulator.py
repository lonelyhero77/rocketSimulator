from vpython import *

"""
Constants
"""
#mks unit
# Re = 1
# Rm = 273e-3
# Rem = 60
# G = 1.04e-17
# Me = 9.37e17
# Mm = 1.15e16
# Rr = Rm*5
Re = 6.37e6
Rm = 1.74e6
Rem = 0.384e9
G = 6.67e-11
Me = 5.97e24
Mm = 7.35e22
Rr = Rm*5

"""
General Variables
"""
orbitDrawing = False
# Time Settings
dt = 10 # [sec]
freq = 1000 # [Hz]
initialMoonVelocity = vec(0, 0, -1022)
warp = False

"""
Rocket Variables
"""
engine = False # Rocket Engine Logic Trigger
propulsion = True # True: Forward, False: Reverse
initialRocketVelocity = vec(0, 0, -1395)


"""
Planetary and Rocket Configuration
"""
earth = sphere(radius = Re*10, color = color.white, make_trail=orbitDrawing, trail_color=color.white, texture=textures.earth)
earth.mass = Me
earth.pos = vec(0, 0, 0)
earth.vel = vec(0, 0, 0)

moon = sphere(radius = Rm*10, color = color.white, make_trail=False, texture=textures.rough, retain=10)
moon.mass =Mm
moon.pos = vec(Rem, 0, 0)
moon.vel = initialMoonVelocity

shaft = cylinder(size=vector(3, .3, .3), color=color.white)
head = cone(size=vector(3.6, .3, .3), pos=vector(3,0,0), color=color.gray(.5) )
thruster = cone(size=vector(2, .2, .2), pos=vector(-1, 0, 0), color=color.gray(.3))
flame = cylinder(size=vector(0.3, .15, .15), pos=vector(-1.2, 0, 0), color=color.red)
rocket = compound([shaft, head, thruster, flame], make_trail=True, color= color.white, trail_color = color.yellow)
rocket.size = vector(1.4e7, 0.8e7, 0.8e7)

rocket.mass = 4500
rocket.pos = vec(Rem/1.1, 0, 0)
rocket.vel = initialRocketVelocity

"""
System Force Calculation and Application
"""
system = [
    [earth, moon],
    [earth, rocket],
    [moon, rocket]
    ]    
planets = (earth, moon, rocket)

def calculateVelocity(obj1, obj2):
    R = obj1.pos - obj2.pos
    F = G * obj1.mass * obj2.mass * R.norm() / R.mag2 # norm = u /|u|
    obj1.vel = obj1.vel - (F / obj1.mass) * dt
    obj2.vel = obj2.vel + (F / obj2.mass) * dt
    
def calculatePosition(obj):
    obj.pos = obj.pos + obj.vel * dt

"""
Rocket Sequence Configuration
"""
def switchEngine(b):
    global engine
    engine = not engine
    if engine:
        b.text = "Engine OFF"
    else:
        b.text = "Engine ON"

def switchPropulsion(p):
    global propulsion
    propulsion = not propulsion
    
    if propulsion:
        p.text = "REVERSE"
    else:
        p.text = "FORWARD"

"""
Simulation Environment and Loop Configuration
"""
#Record Settings
mt = 0
maxSpeed = 0

# Scene Settings
def setspeed(s):
    global dt, warp
    warp = not warp
    if warp:dt = 1000
    else: dt= 10
    # scene.title = "<b>System Simulation @ dt[sec]={}, Frequency[Hz]={}, Initial Rocket Velocity={}</b>".format(dt, freq, rocket.vel)

scene.camera.follow(rocket)
scene.title = "<b>System Simulation @ dt[sec]={}, Frequency[Hz]={}, Initial Rocket Velocity={}</b>".format(dt, freq, rocket.vel)
button(text="Turn Engine On", pos=scene.title_anchor, bind=switchEngine)
button(text="FORWARD", pos=scene.title_anchor, bind=switchPropulsion)
button(text="WARP", pos=scene.title_anchor, bind=setspeed)

# Loop
while True:
    rate(freq) # rate(frequency), halts computations until 1.0/freq seconds after the previous call to rate()
    
    for planet1, planet2 in system:
        calculateVelocity(planet1, planet2)

    # Engine Propulsion System
    if engine:
        if propulsion:
            rocket.vel = rocket.vel + 0.4 * -rocket.vel.norm()
        else:
            rocket.vel = rocket.vel + 0.4 * +rocket.vel.norm()
    
    for planet in planets:
        calculatePosition(planet)

    rocket.axis = rocket.vel.norm()

    mt += dt
    d = ((mt / 60) / 60 ) // 24
    curSpeed = round(rocket.vel.mag)
    if maxSpeed < curSpeed:
        maxSpeed = curSpeed  
    msg = ("Mission Time    {}s / {}m / {}d \n Current Rocket Speed |v|={spd}, Maximum Rocket Speed |v_max|={maxspd}"\
        .format(mt, mt//60, d, vel=rocket.vel, spd=curSpeed, maxspd=maxSpeed))
    # print(msg)
    scene.caption = msg
   
    # Stop when collision between rocket and earth or rocket and moon has occurred
    if mag2(rocket.pos-earth.pos) <= (Re+Rr)**2:
        msg = "\n <h1>Mission completed!</h1>"
        scene.append_to_caption(msg)
        scene.pause()

    if mag2(rocket.pos-moon.pos) <= (Rm+Rr)**2:
        msg = "\n <h1>Collision occured!</h1>"
        scene.append_to_caption(msg)
        scene.pause()