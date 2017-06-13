#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('services.ice --all -I .')
import drobots
import sys, time, random
from RobotControllerAttacker import *
from RobotControllerDefender import *

class PlayerApp(Ice.Application): 
    def run(self, argv):

        broker = self.communicator()
        adapter = broker.createObjectAdapter('PlayerAdapter')
        adapter.activate()

        player_servant = PlayerI(broker, adapter)
        proxy_player = adapter.add(player_servant, broker.stringToIdentity('player'))
        print ('Proxy player: ' +str(proxy_player))
        player = drobots.PlayerPrx.checkedCast(proxy_player)

        proxy_game = broker.stringToProxy(argv[1]) 
        print ('Proxy game: ' +str(proxy_game))
        gameFact = drobots.GameFactoryPrx.checkedCast(proxy_game)
        game = gameFact.makeGame("FactoryRobots", 2)
        print "game factory: " + str(game)

        try:
            print ('Trying to do login...')
            game.login(player, 'Pedro' + str(random.randint(0,99)))
            print ('Waiting to receive the robot controllers')
        except drobots.GameInProgress:
            print '\033[91m\033[1m' + "\nGame in progress. Try it again" + '\033[0m'
            return 1
        except drobots.InvalidProxy:
            print '\033[91m\033[1m' + "\nInvalid proxy" + '\033[0m'
            return 2
        except drobots.InvalidName, e:
            print '\033[91m\033[1m' + "\nInvalid name. It is possible that other person be using your name" + '\033[0m'
            print str(e.reason)
            return 3
        except drobots.BadNumberOfPlayers:
            print '\033[91m\033[1m' + "\nBad number of players" + '\033[0m'
            return 4           
        
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

class PlayerI(drobots.Player):
    def __init__(self, broker, adapter):
        self.broker = broker
        self.adapter = adapter    
        self.rc_counter = 0
        self.container_robots = self.createContainerControllers()

    def makeController(self, robot, adapter, current=None): 
        print ('Making a robot controller...')
        name = 'rc' + str(self.rc_counter)
        self.rc_counter += 1

        if robot.ice_isA("::drobots::Attacker"):
            rc_servant = RobotControllerAttackerI(robot, self.container_robots)
        else:
            rc_servant = RobotControllerDefenderI(robot, self.container_robots)
 
        rc_proxy = self.adapter.add(rc_servant, self.broker.stringToIdentity(name))

        rc = drobots.RobotControllerPrx.checkedCast(rc_proxy)
        return rc             
    
    def win(self, current=None): 
        print '\033[93m\033[1m' + "We have won!" + '\033[0m'
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print '\033[91m\033[1m' + "We have lost!" + '\033[0m'
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current=None):
        print '\033[91m\033[1m' + 'Game aborted. Exiting' + '\033[0m'
        current.adapter.getCommunicator().shutdown()

    def createContainerControllers(self):
        container_proxy = self.broker.stringToProxy('container -t -e 1.1:tcp -h localhost -p 9190 -t 60000')
        controller_container = drobots.ContainerPrx.checkedCast(container_proxy)
        controller_container.setType("ContainerController")

        if not controller_container:
            raise RuntimeError('Invalid factory proxy')
        
        return controller_container

if __name__ == '__main__':
	sys.exit(PlayerApp().main(sys.argv))