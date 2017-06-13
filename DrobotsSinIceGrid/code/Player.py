#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('services.ice --all -I .')
import drobots
import sys, time, random 

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
        print ('Proxy game: ' + str(proxy_game))
        gameFact = drobots.GameFactoryPrx.uncheckedCast(proxy_game)
        game = gameFact.makeGame("FactoryRobots", 2)
        print "game factory: " + str(game)

        try:
            print ('Trying to do login...')
            game.login(player, 'Cris' + str(random.randint(0,99)))
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
        self.counter = 0
        self.container_factories = self.createContainerFactories()
        self.container_robots = self.createContainerControllers()

    def createContainerFactories(self):
        string_prx = 'container -t -e 1.1:tcp -h localhost -p 9190 -t 60000'
        container_proxy = self.broker.stringToProxy(string_prx)
        factories_container = drobots.ContainerPrx.checkedCast(container_proxy)
        factories_container.setType("ContainerFactories")
        print '\033[92m\033[1m' + '******** CREATING FACTORIES ********' + '\033[0m'
        for i in range(0,4):
            string_prx = 'factory -t -e 1.1:tcp -h localhost -p 909'+str(i)+' -t 60000'
            factory_proxy = self.broker.stringToProxy(string_prx)
            print factory_proxy
            factory = drobots.FactoryPrx.checkedCast(factory_proxy)
            
            if not factory:
                raise RuntimeError('Invalid factory '+str(i)+' proxy')
        
            factories_container.link(i, factory_proxy)
        
        return factories_container

    def createContainerControllers(self):
        container_proxy = self.broker.stringToProxy('container -t -e 1.1:tcp -h localhost -p 9190 -t 60000')
        controller_container = drobots.ContainerPrx.checkedCast(container_proxy)
        controller_container.setType("ContainerController")

        if not controller_container:
            raise RuntimeError('Invalid factory proxy')
        
        return controller_container


    def makeController(self, robot, current=None):
        if self.counter == 0 :
            print '\033[92m\033[1m' + '******** CREATING CONTROLLERS ********' + '\033[0m'

        i = self.counter % 4
        print ('Making a robot controller at the factory ' + str(i))
        factory_proxy = self.container_factories.getElementAt(i)
        print factory_proxy
        factory = drobots.FactoryPrx.checkedCast(factory_proxy)
        rc = factory.make(robot, self.container_robots, self.counter)
        self.counter += 1
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

if __name__ == '__main__':
    sys.exit(PlayerApp().main(sys.argv))