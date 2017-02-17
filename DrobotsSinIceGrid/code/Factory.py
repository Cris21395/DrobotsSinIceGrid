#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('servicies.ice --all -I .')
import drobots, sys
from RobotControllerAttacker import *
from RobotControllerDefender import *

class FactoryI(drobots.Factory):
    def __init__(self):
        pass

    def make(self, robot, container_robots, key, current=None):
        print '\033[92m\033[1m' + '******** MAKING FACTORY ********' + '\033[0m'       

        if robot.ice_isA("::drobots::Attacker"):
            rc_servant = RobotControllerAttackerI(robot, container_robots)
            rc_proxy = current.adapter.addWithUUID(rc_servant)
            print rc_proxy                  
            container_robots.link(key, rc_proxy)
            rc = drobots.RobotControllerAttackerPrx.uncheckedCast(rc_proxy)

        else:
            rc_servant = RobotControllerDefenderI(robot, container_robots)
            rc_proxy = current.adapter.addWithUUID(rc_servant)
            print rc_proxy            
            container_robots.link(key, rc_proxy)
            rc = drobots.RobotControllerDefenderPrx.uncheckedCast(rc_proxy)

        rc.setContainer(container_robots)    
        return rc

class ServerFactoryApp(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("FactoryAdapter")
        servant = FactoryI()
        proxy = adapter.add(servant, broker.stringToIdentity("factory"))        

        print(proxy)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

if __name__ == '__main__':
    sys.exit(ServerFactoryApp().main(sys.argv))
