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
debug = False
orbitDrawing = False
# Time Settings
dt = 10 # [sec]
freq = 1000 # [Hz]
warp = False

"""
Rocket Variables
"""
engine = False # Rocket Engine Logic Trigger
propulsion = False # True: Reverse, False: Forward
initialRocketVel = vec(0, 0, -1395)
initialRocketMass = 4500
initialRocketPos = vec(Rem/1.1, 0, 0)

"""
Planetary Variables
"""
initialEarthPos = vector(0, 0, 0) # or vec(0, 0, 0)
initialEarthVel = vector(0, 0, 0)
initialMoonPos = vector(Rem, 0, 0)
initialMoonVel = vec(0, 0, -1022)

"""
Planetary and Rocket Configuration
"""
earth = sphere(radius = Re*10, color = color.white, make_trail=orbitDrawing, trail_color=color.white, texture=textures.earth)
earth.mass = Me
earth.pos = initialEarthPos
earth.vel = initialEarthVel

moon = sphere(radius = Rm*10, color = color.white, make_trail=False, texture=textures.rough, retain=10)
moon.mass = Mm
moon.pos = initialMoonPos
moon.vel = initialMoonVel

shaft = cylinder(size=vector(3, .3, .3), color=color.white)
head = cone(size=vector(3.6, .3, .3), pos=vector(3,0,0), color=color.gray(.5) )
thruster = cone(size=vector(2, .2, .2), pos=vector(-1, 0, 0), color=color.gray(.3))
flame = cylinder(size=vector(0.3, .15, .15), pos=vector(-1.2, 0, 0), color=color.red)
rocket = compound([shaft, head, thruster, flame], make_trail=True, color= color.white, trail_color = color.yellow)
rocket.size = vector(1.4e7, 0.8e7, 0.8e7)
rocket.mass = initialRocketMass
rocket.pos = initialRocketPos
rocket.vel = initialRocketVel

"""
System Force Calculation and Application
"""
system = [
    [earth, moon],
    [earth, rocket],
    [moon, rocket]
    ]    
planets = (earth, moon, rocket)

def calculateVelocity(planet1, planet2):
    R = planet1.pos - planet2.pos
    F = G * planet1.mass * planet2.mass * R.norm() / R.mag2 # norm = u /|u|
    planet1.vel = planet1.vel - (F / planet1.mass) * dt
    planet2.vel = planet2.vel + (F / planet2.mass) * dt
    
def calculatePosition(planet):
    planet.pos = planet.pos + planet.vel * dt

"""
Rocket Sequence Configuration
"""
def switchEngine(b):
    global engine
    engine = not engine
    if engine:
        b.text = "Engine OFF"
        rocket.trail_color = color.orange
    else:
        b.text = "Engine ON"
        rocket.trail_color = color.yellow

def switchPropulsion(p):
    global propulsion
    propulsion = not propulsion
    if not propulsion: p.text = "MODE: FORWARD"
    else: p.text = "MODE: REVERSE"

"""
Simulation Environment and Loop Configuration
"""
#Environment Initialization
def init():
    global mt, maxSpeed
    #Set every variables to initial values
    rocket.pos = initialRocketPos
    rocket.vel = initialRocketVel
    rocket.clear_trail()
    earth.pos = initialEarthPos
    earth.vel = initialEarthVel
    moon.pos = initialMoonPos
    moon.vel = initialMoonVel
    mt = 0
    maxSpeed = 0

#Record Settings
mt = 0
maxSpeed = 0

# Scene Settings
def setspeed(s):
    global dt, warp
    warp = not warp
    if warp:
        s.text = "STOP WARPING"
        dt = 1000
    else:
        s.text = "WARP" 
        dt= 10
        
scene.camera.follow(rocket)
scene.title = "<b>System Simulation @ Initial dt[sec]={}, Frequency[Hz]={}, Initial Rocket Velocity={}</b>\n\
    ENGINE MODE | PROPULSION MODE | TIME WARP\n\
    "\
    .format(dt, freq, rocket.vel)
button(text="Turn Engine On", pos=scene.title_anchor, bind=switchEngine)
button(text="MODE: FORWARD", pos=scene.title_anchor, bind=switchPropulsion)
button(text="WARP", pos=scene.title_anchor, bind=setspeed)
button(text="RESET", pos=scene.title_anchor, bind=init)

# Loop
while True:
    rate(freq) # rate(frequency), halts computations until 1.0/freq seconds after the previous call to rate()
    
    for planet1, planet2 in system:
        calculateVelocity(planet1, planet2)

    # Engine Propulsion System
    if engine:
        if propulsion: rocket.vel = rocket.vel + 0.4 * -rocket.vel.norm()
        else: rocket.vel = rocket.vel + 0.4 * +rocket.vel.norm()
    
    for planet in planets:
        calculatePosition(planet)

    rocket.axis = rocket.vel.norm()

    mt += dt
    d = ((mt / 60) / 60 ) // 24

    curSpeed = round(rocket.vel.mag)
    if maxSpeed < curSpeed:
        maxSpeed = curSpeed  

    msg = ("<h3>Mission Time    {}s / {}m / {}d \n |v|= {spd} m/s, |v_max|= {maxspd} m/s</h3>"\
        .format(mt, mt//60, d, vel=rocket.vel, spd=curSpeed, maxspd=maxSpeed))
    if debug: print(msg)
    scene.caption = msg
   
    # Stop when collision between rocket and earth or rocket and moon has occurred
    if mag2(rocket.pos-earth.pos) <= (Re+Rr)**2:
        msg = "\n <h1>Mission completed!</h1>"
        scene.append_to_caption(msg)
        scene.pause()
        init()

    if mag2(rocket.pos-moon.pos) <= (Rm+Rr)**2:
        msg = "\n <h1>Collision occured!</h1>"
        scene.append_to_caption(msg)
        scene.pause()
        init()