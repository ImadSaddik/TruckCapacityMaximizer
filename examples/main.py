from ..solver.solver import Solver
from pulp import *


# Define the problem
prob = LpProblem("Truck Loading Problem", LpMinimize)

# instantiate the solver
numberOfProducts = 3
numberOfTruckTypes = 2
productVolumes = [1.2, 0.3, 0.5]
productDemandQuantity = [129, 32, 300]
truckTypeCapacities = [120, 210]
numberOfTrucksPerType = [15, 10]

solver = Solver(numberOfProducts=numberOfProducts, 
                    numberOfTruckTypes=numberOfTruckTypes,
                    prob=prob,
                    productVolumes=productVolumes,
                    productDemandQuantity=productDemandQuantity,
                    truckTypeCapacities=truckTypeCapacities,
                    numberOfTrucksPerType=numberOfTrucksPerType
                )

# Solve the problem
solution = solver.getSolution()
solution = solver.pretifySolution(solution)
print("___________________________")
print(solution)