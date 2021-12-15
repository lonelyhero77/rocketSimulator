from vpython import *
#mks unit
# Re = 1
# Rm = 273e-3
# Rem = 60
# G = 1.04e-17
# Me = 9.37e17
# Mm = 1.15e16
# Rr = Rm*5
"""
Constants
"""
Re = 6.37e6
Rm = 1.74e6
Rem = 0.384e9
G = 6.67e-11
Me = 5.97e24
Mm = 7.35e22
Rr = Rm*5

"""
Planetary and Rocket Settings
"""
earth = sphere(radius = Re*10, color = color.white, make_trail=True, texture=textures.earth)
earth.mass = Me
earth.pos = vec(0, 0, 0)
earth.vel = vec(0, 0, 0)

moon = sphere(radius = Rm*10, color = color.white, make_trail=True, texture=textures.rough)
moon.mass =Mm
moon.pos = vec(Rem, 0, 0)
moon.vel = vec(0, 0, -1022)


handle = cylinder( size=vector(1e8,.2e8,.2e8), color=vector(0.72,0.42,0) )
head = box( size=vector(.2e8,.6e8,.2e8), pos=vector(1.1,0,0), color=color.gray(.6))
hammer = compound([handle, head], make_trail=True, color= color.white, trail_color = color.green)
# hammer.axis = vector(1,0,0)

rocket = hammer
# rocket = sphere(radius = Rr, color = color.red, make_trail=True)
rocket.mass = 4500
rocket.pos = vec(Rem/1.2, 0, 0)
rocket.vel = vec(0, 0, -1000)



"""
System force calculation and application
"""
system = [
    [earth, moon],
    [earth, rocket],
    [moon, rocket]
    ]
    
planets = (earth, moon, rocket)

def calculateVelocity(obj1, obj2):
    R = obj1.pos - obj2.pos
    F = G * obj1.mass * obj2.mass * R.norm() / R.mag2 #norm = u / |u
    obj1.vel = obj1.vel - (F / obj1.mass) * dt
    obj2.vel = obj2.vel + (F / obj2.mass) * dt
    
def calculatePosition(obj):
    obj.pos = obj.pos + obj.vel * dt


"""
Loop
"""
#time settings
dt = 100
mt = 0

while True:
    rate(2000)
    
    for planet1, planet2 in system:
        calculateVelocity(planet1, planet2)
    
    for planet in planets:
        calculatePosition(planet)

    rocket.axis = rocket.pos.norm()

    mt += dt
    d = ((mt / 60) / 60 ) // 24

    print("Mission Time    {}s / {}m / {}d".format(mt, mt//60, d))
    # print(rocket.pos)
    # print(rocket.vel)

    #stop when collision between rocket and earth occurred
    if mag2(rocket.pos-earth.pos) <= (Re+Rr)**2: 
        break

    #stop when collision between rocket and moon occurred
    if mag2(rocket.pos-moon.pos) <= (Rm+Rr)**2:
        break