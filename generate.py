import random
import pyrosim.pyrosim as pyrosim


def Create_World():
    """Generate a minimal world with a single block placed out of the robot's way."""
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="GroundBlock", pos=[0, -2, 0.5], size=[1, 1, 1])
    pyrosim.End()


def Generate_Body():
    """Generate the 3-link robot: Torso with BackLeg and FrontLeg as in the diagram."""
    pyrosim.Start_URDF("body.urdf")

    # Torso (root) placed absolutely at x=1.5, z=1.5 with size 1x1x1.
    pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[1, 1, 1])

    # Back leg: joint at torso's back-bottom corner (absolute x=1, z=1), leg centered at (0.5, 0, 0.5).
    pyrosim.Send_Joint(
        name="Torso_BackLeg",
        parent="Torso",
        child="BackLeg",
        type="revolute",
        position=[1.0, 0, 1.0],
    )
    # Leg geometry is offset from its joint so its bottom sits on z=0 and spans x in [0,1].
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])

    # Front leg: joint at torso's front-bottom corner (absolute x=2, z=1), leg centered at (2.5, 0, 0.5).
    pyrosim.Send_Joint(
        name="Torso_FrontLeg",
        parent="Torso",
        child="FrontLeg",
        type="revolute",
        position=[2.0, 0, 1.0],
    )
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])

    pyrosim.End()


def Generate_Brain():
    """Generate the neural network: sensor neurons for each link, motor neurons for each joint."""
    pyrosim.Start_NeuralNetwork("brain.nndf")

    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

    for sensorNeuronName in range(3):
        for motorNeuronName in range(2):
            pyrosim.Send_Synapse(
                sourceNeuronName=sensorNeuronName,
                targetNeuronName=motorNeuronName + 3,
                weight=random.random() * 2 - 1,
            )

    pyrosim.End()


if __name__ == "__main__":
    Create_World()
    Generate_Body()
    Generate_Brain()
