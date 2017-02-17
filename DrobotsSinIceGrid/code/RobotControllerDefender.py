#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('servicies.ice --all -I .')
import drobots
import sys, time, random, math
from State import *

class RobotControllerDefenderI(drobots.RobotControllerDefender):

    def __init__(self, robot, container):
        self.robot = robot
        self.container = container
        self.state = State.MOVING
        self.previous_damage = 0
        self.friends_position = dict()
        self.x = 390
        self.y = 390
        self.Allangles = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]
        self.angles_left_to_scan = self.Allangles[:]
        random.shuffle(self.angles_left_to_scan)

        self.handlers = {
            State.MOVING : self.move,
            State.SCANNING : self.scan,
            State.PLAYING : self.play
        }

    def setContainer(self, container, current=None):
        self.container = container

    def turn(self, current=None):
        try:
            self.handlers[self.state]()
        except drobots.NoEnoughEnergy:
            pass

    def play(self):
        my_location = self.robot.location()    

        for i in range(2,4):
            attacker_prx = self.container.getElementAt(i)
            attacker = drobots.RobotControllerAttackerPrx.uncheckedCast(attacker_prx)
            attacker.friendPosition(my_location, i)


    def friendPosition(self, point, identifier, current=None):
        self.friends_position[identifier] = point

    def move(self):
        location = self.robot.location()
        delta_x = self.x - location.x
        delta_y = self.y - location.y
        angle = int(round(self.calculate_angle(delta_x, delta_y), 0))
        self.robot.drive(angle, 100)
        self.state = State.PLAYING


    def scan(self): 
        amplitude = 20        
        try:
            current_angle = self.angles_left_to_scan.pop()
        except IndexError:
            self.angles_left_to_scan = self.Allangles[:]
            random.shuffle(self.angles_left_to_scan)
            current_angle = self.angles_left_to_scan.pop()            
            
        detected_enemies = self.robot.scan(current_angle, amplitude)
        if  detected_enemies != 0:
            self.robot.drive(0, 0)
            self.shoot_angle = current_angle
            self.state = State.SHOOTING
 
    def robotDestroyed(self, current=None):
        print 'Destroyed defender'

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