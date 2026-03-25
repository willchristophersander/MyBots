import sys
from simulation import SIMULATION

directOrGUI = sys.argv[1]
solutionID   = sys.argv[2]
label        = sys.argv[3] if len(sys.argv) > 3 else ""

simulation = SIMULATION(directOrGUI, solutionID, label)
simulation.Run()
simulation.Get_Fitness()
