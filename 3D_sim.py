from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

cube = Entity(model='cube', color=hsv(300,1,1), scale=2, collider='box')

# create camera and player graphic
cam = FirstPersonController()

player = Entity(model='cube',
                origin = (0, 0, -2),
                parent = cam)

# run
app.run()