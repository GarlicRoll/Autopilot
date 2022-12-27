import numpy as np
import pygame as pg
import sys

class Object():
    def __init__(self, postion):
        self.name = "Default"
        self.position = np.array(postion)
        self.velocity = np.array([0, 0])
        self.speed = np.array([0, 0])

        self.maxSpeed = np.array([5, 5])

    def update(self):
        self.position = self.position + self.speed * 1 + self.velocity * self.velocity * 1 / 2
        
        if np.linalg.norm(self.maxSpeed) > np.linalg.norm(self.speed + self.velocity * 1): self.speed = self.maxSpeed
        else: self.speed = self.speed + self.velocity * 1

    def print(self):
        print("{}: X: {}, Y: {}, VelocityX: {}, VelocityY: {}, SpeedX: {}, SpeedY: {}".format(self.name, self.position[0], self.position[1], self.velocity[0], self.velocity[1], self.speed[0], self.speed[1]))

    def pursuit(self, target):
        return (target.position - self.position) * 10

target = Object([10, 10])
target.name = "Target"
object = Object([10, 100])
object.name = "Object"

target.velocity[0] = 1
target.velocity[1] = 1


sc = pg.display.set_mode((1000, 1000))
 

while True:

    for j in pg.event.get():
            if j.type == pg.QUIT:
                sys.exit()

    target.update()
    object.velocity = object.pursuit(target) / 400
    object.update()
    target.print()
    object.print()
    pg.draw.circle(sc, (0, 255, 0), list(target.position), 10)
    pg.draw.circle(sc, (0, 0, 255), list(object.position), 10)
        
    pg.display.update()
    pg.time.delay(300)
    


'''
while 1:
    pg.draw.circle(sc, (0, 0, 0), 
                   target.position, 10)
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
    pg.time.delay(1000)
'''