#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('services.ice --all -I .')
import drobots
import sys, time, random, math
from State import *

class RobotControllerAttackerI(drobots.RobotControllerAttacker):

    def __init__(self, robot, container):
        self.robot = robot
        self.container = container
        self.state = State.MOVING
        self.previous_damage = 0
        self.x = 10
        self.y = 10
        self.shoot_angle = 0
        self.shoots_counter = 0
        self.friends_position = dict()
        self.handlers = {
            State.MOVING : self.move,
            State.SHOOTING : self.shoot,
            State.PLAYING : self.play
        }
        self.velocidad = 0
        self.energia = 0
        
    def setContainer(self, container, current=None):
        self.container = container
    
    def friendPosition(self, point, identifier, current=None):
        self.friends_position[identifier]= point

    def turn(self, current=None):
        try:
            self.handlers[self.state]()
        except drobots.NoEnoughEnergy:
            pass

    def play(self):
        my_location = self.robot.location()    

        for i in range(0,3):
            defender_prx = self.container.getElementAt(i)
            defender = drobots.RobotControllerAttackerPrx.uncheckedCast(defender_prx)
            defender.friendPosition(my_location, i)
            self.state = State.SHOOTING

    def move(self):
        location = self.robot.location()
        delta_x = self.x - location.x
        delta_y = self.y - location.y
        angle = int(round(self.calculate_angle(delta_x, delta_y), 0))

        if(self.velocidad == 0):
            self.robot.drive(random.randint(0,360),100)
            self.velocidad = 100
        elif(location.x > 390):
            self.robot.drive(225, 100)
            self.velocidad = 100
        elif(location.x < 100):
            self.robot.drive(45, 100)
            self.velocidad = 100
        elif(location.y > 390):
            self.robot.drive(315, 100)
            self.velocidad = 100
        elif(location.y < 100):
            self.robot.drive(135, 100)
            self.velocidad = 100

        print ('Moving to x: ' + str(location.x) + ' y: ' + str(location.y) + ' α: ' + str(angle) + 'º')
        self.robot.drive(angle, 100)
        self.state = State.PLAYING

    def shoot(self): 
        MAX_SHOOTS = 20
        if self.shoots_counter <= MAX_SHOOTS:
            angle = self.shoot_angle + random.randint(0, 360)
            distance = (self.shoots_counter + 6) * 20
            self.robot.cannon(angle, distance) 
            self.shoots_counter += 1
            self.state = State.SHOOTING
        else:
            self.shoots_counter = 0
            self.state = State.MOVING 

    def robotDestroyed(self, current=None):
        print 'Destroyed atacant'

    def calculate_angle(self, x, y, current=None):
        if x==0:
            if y>0:
                return 90
            return 270
        if y==0:
            if x>0:
                return 0
            return 180
        elif y>0:
            return 90 - math.degrees(math.atan(float(x)/float(y)))
        else:
            return 270 - math.degrees(math.atan(float(x)/float(y)))