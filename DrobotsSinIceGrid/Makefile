#!/usr/bin/make -f
# -*- mode:makefile -*-

.PHONY: all run-player run-player2 run-container clean run-all-factories

SERVER = drobots7

all:
	gnome-terminal --tab -e "make run-all-factories"
	gnome-terminal --tab -e "make run-container"
	gnome-terminal --tab -e "make run-player2"
	make run-player

run-player:
	python code/Player.py --Ice.Config=locator.config $(SERVER)

run-player2:
	python code/Player2.py --Ice.Config=locator.config $(SERVER)

run-factory1:
	python code/Factory.py --Ice.Config=Factory1.config

run-factory2:
	python code/Factory.py --Ice.Config=Factory2.config

run-factory3:
	python code/Factory.py --Ice.Config=Factory3.config

run-factory4:
	python code/Factory.py --Ice.Config=Factory4.config

run-all-factories:
	make -j run-factory1 run-factory2 run-factory3 run-factory4

run-container:
	python code/Container.py --Ice.Config=Container.config

clean:
	sudo rm -f code/*.pyc
	sudo killall -q -9 python