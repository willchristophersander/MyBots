import os
import time
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
from world import WORLD
from robot import ROBOT


class SIMULATION:
    def __init__(self):
        mode = os.environ.get("PYBULLET_MODE", "GUI").upper()
        if mode == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            if self.physicsClient < 0:
                self.physicsClient = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.GRAVITY_X, c.GRAVITY_Y, c.GRAVITY_Z)
        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        for t in range(c.SIMULATION_STEPS):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Act(t)
            time.sleep(c.SIMULATION_SLEEP_TIME)

    def __del__(self):
        p.disconnect()
