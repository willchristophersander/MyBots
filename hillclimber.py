import copy
import constants as c
from solution import SOLUTION


class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()

    def Evolve(self):
        # Show and record the initial random solution.
        self.parent.Evaluate("GUI", "Initial random robot", "recording_initial.mp4")
        self.initialFitness = self.parent.fitness
        self.fitnessLog = [(self.initialFitness, self.initialFitness)]
        # Evolve blindly.
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Show_Best(self):
        label = (
            f"Hill Climber  |  {c.numberOfGenerations} generations\n"
            f"Initial fitness: {self.initialFitness:.3f}\n"
            f"Final fitness:   {self.parent.fitness:.3f}"
        )
        self.parent.Evaluate("GUI", label, "recording_final.mp4")

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate("DIRECT")
        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child

    def Print(self):
        print(self.parent.fitness, self.child.fitness)
