from vpython import *

# handle = cylinder( size=vector(1,.2,.2), color=vector(0.72,0.42,0) )

#x y z x: length, y,z area(size)
shaft = cylinder(size=vector(3, .3, .3), color=color.white)
head = cone(size=vector(3.6, .3, .3), pos=vector(3,0,0), color=color.gray(.5) )
thruster = cone(size=vector(2, .2, .2), pos=vector(-1, 0, 0), color=color.gray(.3))
flame = cylinder(size=vector(0.3, .1, .1), pos=vector(-2, 0, 0), color=color.red)
rocket = compound([shaft, head, thruster, flame])
rocket.size = vector(1.4e7, 0.8e7, 0.8e7)
rocket.axis = vector(1,1,0)

scene.pause()