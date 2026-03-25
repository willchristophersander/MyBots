import os
import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK


class ROBOT:
    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.bodyId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.bodyId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")
        os.system("rm brain" + str(solutionID) + ".nndf")

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Think(self):
        self.nn.Update()

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                key = jointName if jointName in self.motors else jointName.encode("utf-8")
                self.motors[key].Set_Value(self, desiredAngle)

    def Neuron_Display_Text(self):
        s_vals = "  ".join(
            f"{self.nn.Get_Value_Of(n):+.2f}"
            for n in sorted(self.nn.Get_Neuron_Names())
            if self.nn.neurons[n].Is_Sensor_Neuron()
        )
        m_vals = "  ".join(
            f"{self.nn.Get_Value_Of(n):+.2f}"
            for n in sorted(self.nn.Get_Neuron_Names())
            if self.nn.neurons[n].Is_Motor_Neuron()
        )
        synapses = "  ".join(
            f"({k[0]}->{k[1]}: {self.nn.synapses[k].Get_Weight():+.2f})"
            for k in self.nn.synapses
        ) if self.nn.synapses else "(no synapses)"
        return (
            f"Sensor neurons:  {s_vals}\n"
            f"Motor neurons:   {m_vals}\n"
            f"Synapses: {synapses}"
        )

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.bodyId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        tmpFileName = "tmp" + str(self.solutionID) + ".txt"
        fitnessFileName = "fitness" + str(self.solutionID) + ".txt"
        f = open(tmpFileName, "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()
        os.system("mv " + tmpFileName + " " + fitnessFileName)

    def Save_Values(self):
        for sensor in self.sensors.values():
            sensor.Save_Values()
