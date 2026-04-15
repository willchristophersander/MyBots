import os
import sys
import time
import random
import numpy
import pyrosim.pyrosim as pyrosim
import constants as c


class SOLUTION:
    def __init__(self, myID):
        self.myID = myID
        self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
        self.cpg_x = random.uniform(c.CPG_X_MIN, c.CPG_X_MAX)

    def Set_ID(self, myID):
        self.myID = myID

    def Start_Simulation(self, directOrGUI, label=""):
        # world.sdf/body.urdf are static for all solutions; generate once elsewhere
        # to avoid parallel write races during DIRECT batch evaluation.
        self.Create_Brain()
        import shlex
        cmd = ("env CPG_X=" + str(self.cpg_x) + " " + sys.executable + " simulate.py " + directOrGUI
               + " " + str(self.myID)
               + " " + shlex.quote(label))
        if directOrGUI == "DIRECT":
            cmd += " &"
        os.system(cmd)

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system("rm " + fitnessFileName)

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1
        if random.random() < c.CPG_X_MUTATION_PROB:
            self.cpg_x += random.gauss(0, c.CPG_X_MUTATION_SIGMA)
            self.cpg_x = max(c.CPG_X_MIN, min(c.CPG_X_MAX, self.cpg_x))

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="GroundBlock", pos=[0, -2, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])
        pyrosim.Send_Joint(
            name="Torso_BackLeg", parent="Torso", child="BackLeg",
            type="revolute", position=[0, -0.5, 1], jointAxis="1 0 0",
        )
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(
            name="Torso_FrontLeg", parent="Torso", child="FrontLeg",
            type="revolute", position=[0, 0.5, 1], jointAxis="1 0 0",
        )
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(
            name="Torso_LeftLeg", parent="Torso", child="LeftLeg",
            type="revolute", position=[0.5, 0, 1], jointAxis="0 1 0",
        )
        pyrosim.Send_Cube(name="LeftLeg", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])

        pyrosim.Send_Joint(
            name="Torso_RightLeg", parent="Torso", child="RightLeg",
            type="revolute", position=[-0.5, 0, 1], jointAxis="0 1 0",
        )
        pyrosim.Send_Cube(name="RightLeg", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])

        pyrosim.Send_Joint(
            name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg",
            type="revolute", position=[0, 1, 0], jointAxis="1 0 0",
        )
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(
            name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg",
            type="revolute", position=[0, -1, 0], jointAxis="1 0 0",
        )
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(
            name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg",
            type="revolute", position=[1, 0, 0], jointAxis="0 1 0",
        )
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])

        pyrosim.Send_Joint(
            name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg",
            type="revolute", position=[-1, 0, 0], jointAxis="0 1 0",
        )
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2, 0.2, 1])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        sensorLinks = [
            "FrontLowerLeg",
            "BackLowerLeg",
            "LeftLowerLeg",
            "RightLowerLeg",
        ]
        motorJoints = [
            "Torso_BackLeg",
            "Torso_FrontLeg",
            "Torso_LeftLeg",
            "Torso_RightLeg",
            "FrontLeg_FrontLowerLeg",
            "BackLeg_BackLowerLeg",
            "LeftLeg_LeftLowerLeg",
            "RightLeg_RightLowerLeg",
        ]

        for neuronName, linkName in enumerate(sensorLinks):
            pyrosim.Send_Sensor_Neuron(name=neuronName, linkName=linkName)
        for motorOffset, jointName in enumerate(motorJoints):
            pyrosim.Send_Motor_Neuron(
                name=c.numSensorNeurons + motorOffset,
                jointName=jointName,
            )

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow,
                    targetNeuronName=currentColumn + c.numSensorNeurons,
                    weight=self.weights[currentRow][currentColumn],
                )
        pyrosim.End()
