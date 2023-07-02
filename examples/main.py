from ..solver.solver import Solver
from pulp import *


# Remove unwanted output from PuLP
pulp.LpSolverDefault.msg = False

# Define the problem
prob = LpProblem("Truck_Loading_Problem", LpMinimize)

# instantiate the solver
numberOfProducts = 3
numberOfTruckTypes = 2
productVolumes = [1.2, 0.3, 0.5]
productDemandQuantity = [1290, 302, 300]
truckTypeCapacities = [120, 210]
numberOfTrucksPerType = [5, 10]

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

# Print the status of the solution
print(f"Status: {LpStatus[solver.prob.status]}")

# Pretify the solution using tabulate
if solution is not None:
    solution = solver.pretifySolution(solution)

    # Print the solution
    print(solution)
