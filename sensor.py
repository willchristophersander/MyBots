import os
import numpy
import pyrosim.pyrosim as pyrosim
import constants as c


class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(c.SIMULATION_STEPS)

    def Get_Value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Save_Values(self):
        os.makedirs("data", exist_ok=True)
        numpy.save("data/" + self.linkName + "SensorValues.npy", self.values)
