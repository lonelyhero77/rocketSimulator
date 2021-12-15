from vpython import *

handle = cylinder( size=vector(1,.2,.2), color=vector(0.72,0.42,0) )

head = box( size=vector(.2,.6,.2), pos=vector(1.1,0,0), color=color.gray(.6) )

hammer = compound([handle, head])
hammer.axis = vector(1,0,0)