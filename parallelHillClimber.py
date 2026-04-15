import copy
import os
import constants as c
from solution import SOLUTION


class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm -f brain*.nndf")
        os.system("rm -f fitness*.txt tmp*.txt")
        # Generate static assets exactly once to prevent parallel workers from
        # clobbering body.urdf/world.sdf while simulations are starting.
        bootstrap = SOLUTION(-1)
        bootstrap.Create_World()
        bootstrap.Create_Body()
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents, "DIRECT")
        self.initialBestFitness = min(s.fitness for s in self.parents.values())
        self.fitnessLog = []
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Show_Best(self):
        bestParent = min(self.parents.values(), key=lambda s: s.fitness)
        finalBest  = bestParent.fitness
        cpg_x = getattr(bestParent, "cpg_x", os.environ.get("CPG_X", str(getattr(c, "CPG_X", "unset"))))
        cpg_enabled = str(getattr(c, "CPG_ENABLED", False))
        label = (
            f"Marching to the beat (CPG)\n"
            f"CPG_ENABLED: {cpg_enabled}  CPG_X: {cpg_x}\n"
            f"PHC  Population: {c.populationSize}  Generations: {c.numberOfGenerations}\n"
            f"Initial best fitness: {self.initialBestFitness:.3f}\n"
            f"Final best fitness:   {finalBest:.3f}"
        )
        bestParent.Start_Simulation("GUI", label)

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children, "DIRECT")
        self.Print()
        self.Select()

    def Evaluate(self, solutions, directOrGUI):
        for key in solutions:
            solutions[key].Start_Simulation(directOrGUI)
        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()
        # Useful milestone-2 evidence: show evolved CPG_X values.
        if getattr(c, "CPG_ENABLED", False):
            xs = [getattr(solutions[k], "cpg_x", None) for k in solutions if hasattr(solutions[k], "cpg_x")]
            if xs:
                print("CPG_X values:", " ".join(f"{x:.3f}" for x in xs), flush=True)

    def Spawn(self):
        self.children = {}
        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for key in self.children:
            self.children[key].Mutate()

    def Select(self):
        for key in self.parents:
            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        print("")
        for key in self.parents:
            print(self.parents[key].fitness, self.children[key].fitness)
        print("")
