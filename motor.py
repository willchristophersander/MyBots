import os
import numpy
import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c


class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.AMPLITUDE
        self.frequency = c.FREQUENCY
        self.offset = c.PHASE_OFFSET
        # One motor oscillates at half the frequency (per "Flexing" instructions).
        try:
            j = self.jointName.decode() if isinstance(self.jointName, bytes) else self.jointName
        except Exception:
            j = str(self.jointName)
        if "FrontLeg" in j:
            self.frequency = c.FREQUENCY * 0.5
        self.motorValues = self.amplitude * numpy.sin(
            self.frequency * numpy.linspace(0, 2 * numpy.pi, c.SIMULATION_STEPS) + self.offset
        )

    def Set_Value(self, robot, t):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot.bodyId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=self.motorValues[t],
            maxForce=c.MOTOR_MAX_FORCE,
        )

    def Save_Values(self):
        os.makedirs("data", exist_ok=True)
        name = self.jointName.decode() if isinstance(self.jointName, bytes) else str(self.jointName)
        numpy.save("data/" + name + "MotorValues.npy", self.motorValues)
