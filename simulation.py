import time
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
from world import WORLD
from robot import ROBOT


class SIMULATION:
    def __init__(self, directOrGUI, solutionID, label=""):
        self.directOrGUI = directOrGUI
        self.videoLogId = None
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.GRAVITY_X, c.GRAVITY_Y, c.GRAVITY_Z)
        self.world = WORLD()
        self.robot = ROBOT(solutionID)
        if directOrGUI == "GUI":
            self.videoLogId = p.startStateLogging(
                loggingType=p.STATE_LOGGING_VIDEO_MP4,
                fileName="recording_" + str(solutionID) + ".mp4",
            )
        if label:
            p.addUserDebugText(
                text=label,
                textPosition=[1.5, 0, 4.0],
                textColorRGB=[1, 1, 0],
                textSize=1.5,
                lifeTime=0,
            )

    def Run(self):
        for t in range(c.SIMULATION_STEPS):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            if self.directOrGUI == "GUI":
                time.sleep(c.SIMULATION_SLEEP_TIME)

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def __del__(self):
        if self.videoLogId is not None:
            p.stopStateLogging(self.videoLogId)
        p.disconnect()
