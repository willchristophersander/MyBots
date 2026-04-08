import math
import numpy

# Simulation
SIMULATION_STEPS = 500
SIMULATION_SLEEP_TIME = 1 / 240.0

# Physics
GRAVITY_X = 0.0
GRAVITY_Y = 0.0
GRAVITY_Z = -9.8

# Motors (position control)
MOTOR_MAX_FORCE = 500
AMPLITUDE = math.pi / 4.0
FREQUENCY = 1.0
PHASE_OFFSET = 0.0
# Keep joint excursions modest to encourage repeatable stepping gaits.
motorJointRange = 0.2

# Evolution (deliverable-quality search preset)
numberOfGenerations = 25
populationSize = 15

# Neural-network dimensions (quadruped)
# Use only lower-leg touch sensors to focus search on contacts that change.
numSensorNeurons = 4
numMotorNeurons = 8

# Final project: Central Pattern Generator (CPG)
# If enabled, one sensor neuron is overwritten with sin(CPG_X * t).
CPG_ENABLED = True
CPG_SENSOR_NEURON = 0
CPG_X = 0.25
