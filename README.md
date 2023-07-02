# Maximization of Truck Capacity Utilization

## Description
This project aims to address the optimization problem of maximizing truck capacity utilization. The problem involves a fleet of trucks, each with a specific capacity for transporting goods. Additionally, there are various products, each with its own volume. The objective is to efficiently allocate products to trucks in a way that maximizes the overall utilization of truck capacities.

We have approached this optimization problem using the PulP library, a popular linear programming tool in Python. By formulating the problem as a linear programming model and leveraging the capabilities of PulP, we were able to find an optimal solution that optimizes the allocation of products to trucks.

## Key Features
- Efficiently allocates products to trucks based on their respective volumes
- Maximizes the overall utilization of truck capacities
- Provides an optimal solution to the truck capacity utilization problem
- Implemented using the PulP library for linear programming in Python

## Getting Started
To get started with this project, follow these steps:

1. Clone the repository: `git clone https://github.com/ImadSaddik/TruckCapacityMaximizer.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Make sure to navigate to the folder that contains: `manage.py`
4. Run this command: `python manage.py runserver`

## Usage
This Django application allows you to interact with the code through a web interface, enabling you to input the number of trucks and products for your specific problem and obtain the optimal solution. If you prefer using the solver in your terminal, navigate to the 'solver' folder and import the `solver.py` file. This file implements the optimization model using PulP. Inside the script, you can easily modify the input data, such as truck capacities and product weights, to experiment with different scenarios.

To learn how to use the Solver class, follow these steps:

1. Navigate to the directory where you copied this repository. In my case, I renamed the copied folder to "optimization." If you have a different folder name, make sure to adjust it in the next step as well.
2. Execute the following command: `python -m optimization.examples.main`, optimization refers to the name of the folder that contains the whole project
3. The content of the `main.py` script is displayed below:


```python
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
```
