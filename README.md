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

Here is an example of how to use the solver:

```python
# Example usage code snippet
from optimization import optimize_truck_utilization

# Define your input data
truck_capacities = [100, 150, 200]  # Capacities of the trucks
product_weights = [50, 75, 100, 125, 150]  # Weights of the products

# Run the optimization
solution = optimize_truck_utilization(truck_capacities, product_weights)

# Print the results
print("Optimal allocation of products to trucks:")
for truck, products in solution.items():
    print(f"Truck {truck}: {products}")
