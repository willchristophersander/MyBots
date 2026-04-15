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
        self._textId = None
        self._label = label
        if directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.GRAVITY_X, c.GRAVITY_Y, c.GRAVITY_Z)
        self.world = WORLD()
        self.robot = ROBOT(solutionID)
        if directOrGUI == "GUI":
            p.resetDebugVisualizerCamera(
                cameraDistance=5,
                cameraYaw=50,
                cameraPitch=-25,
                cameraTargetPosition=[0.0, 0.0, 1.0],
            )
            self.videoLogId = p.startStateLogging(
                loggingType=p.STATE_LOGGING_VIDEO_MP4,
                fileName="recording_" + str(solutionID) + ".mp4",
            )
            initialText = (label + "\n") if label else ""
            self._textId = p.addUserDebugText(
                text=initialText + "Initialising...",
                # Put overlay near the robot so it's on-screen by default.
                textPosition=[0.0, 0.0, 2.0],
                textColorRGB=[1, 1, 0],
                textSize=1.6,
                lifeTime=0,
            )

    def Run(self):
        for t in range(c.SIMULATION_STEPS):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think(t)
            self.robot.Act(t)
            if self.directOrGUI == "GUI":
                if self._textId is not None:
                    prefix = (self._label + "\n") if self._label else ""
                    p.addUserDebugText(
                        text=prefix + self.robot.Neuron_Display_Text(),
                        textPosition=[0.0, 0.0, 2.0],
                        textColorRGB=[1, 1, 0],
                        textSize=1.6,
                        lifeTime=0,
                        replaceItemUniqueId=self._textId,
                    )
                time.sleep(c.SIMULATION_SLEEP_TIME)

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def __del__(self):
        if self.videoLogId is not None:
            p.stopStateLogging(self.videoLogId)
        p.disconnect()
