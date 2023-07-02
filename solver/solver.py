from pulp import *
from tabulate import tabulate


class Solver():
    def __init__(self, numberOfProducts, numberOfTruckTypes, prob, productVolumes, 
                 productDemandQuantity, truckTypeCapacities, numberOfTrucksPerType):
        self.prob = prob
        self.numberOfProducts = numberOfProducts
        self.numberOfTruckTypes = numberOfTruckTypes
        self.productVolumes = productVolumes
        self.productDemandQuantity = productDemandQuantity
        self.truckTypeCapacities = truckTypeCapacities
        self.numberOfTrucksPerType = numberOfTrucksPerType
        
    
    def getProductNames(self):
        productNames = []
        for i in range(self.numberOfProducts):
            productName = f"Product_{str(i + 1)}"
            productNames.append(productName)
            
        return productNames
    
    
    def getTruckTypeNames(self):
        truckTypeNames = []
        for i in range(self.numberOfTruckTypes):
            truckTypeName = f"Truck_{str(i + 1)}"
            truckTypeNames.append(truckTypeName)
            
        return truckTypeNames
    
    
    def getTrucksPerTypeNames(self):
        trucksPerTypeNames = []
        for i in range(self.numberOfTruckTypes):
            for j in range(self.numberOfTrucksPerType[i]):
                truckPerTypeName = f"Truck_{str(i + 1)}_{str(j + 1)}"
                trucksPerTypeNames.append(truckPerTypeName)
                
        return trucksPerTypeNames
        

    def getSolution(self):
        x, y = self.setDecisionVariables()
        self.prob += (lpSum([y[truckPerType] for truckPerType in self.getTrucksPerTypeNames()]), "number_of_trucks_used")
        self.setConstraints(x=x, y=y)
        self.prob.solve()

        status = LpStatus[self.prob.status]
        canShowTable = status == 'Optimal'

        return self.prepareSolution(x=x) if canShowTable else None
        
    
    def setDecisionVariables(self):
        x = LpVariable.dicts("X", (self.getProductNames(), self.getTrucksPerTypeNames()), 0, None, LpInteger)
        y = LpVariable.dicts("Y", self.getTrucksPerTypeNames(), 0, 1, LpBinary)
        
        return x, y
        
        
    def setConstraints(self, x, y):
        for truckPerType in self.getTrucksPerTypeNames():
            truckTypeName = truckPerType.split("_")[0] + "_" + truckPerType.split("_")[1]
            self.prob += (
                lpSum(self.getTruckLoad(x, truckPerType)) <= self.getTruckCapacityIfUsed(y, truckTypeName, truckPerType),
                f"Capacity_of_{truckPerType}"
            )
            
        for (productIndex, product) in enumerate(self.getProductNames()):
            self.prob += (
                lpSum(self.getProductQuantity(x, product)) == self.productDemandQuantity[productIndex],
                f"sum_of_trucks_for_{product}"
            )
            
            
    def getTruckLoad(self, x, truckPerType):
        return [(x[product][truckPerType] * self.productVolumes[productIndex]) for (productIndex, product) in enumerate(self.getProductNames())]
    
    
    def getTruckCapacityIfUsed(self, y, truckTypeName, truckPerType):
        return self.truckTypeCapacities[self.getTruckTypeIndex(truckTypeName)] * y[truckPerType]
        
    
    def getTruckTypeIndex(self, truckTypeName):
        return self.getTruckTypeNames().index(truckTypeName)
        
        
    def getProductQuantity(self, x, product):
        return [x[product][truckPerType] for truckPerType in self.getTrucksPerTypeNames()]
        
        
    def prepareSolution(self, x):
        table = []
        for truck in self.getTrucksPerTypeNames():
            truckInventory = [truck]
            transportedVolume = 0

            for (productIndex, product) in enumerate(self.getProductNames()):
                truckInventory.append(value(x[product][truck]))
                transportedVolume += value(x[product][truck]) * self.productVolumes[productIndex]

            truckTypeName = truck.split("_")[0] + "_" + truck.split("_")[1]
            truckLoad = transportedVolume / self.truckTypeCapacities[self.getTruckTypeIndex(truckTypeName)]
            truckInventory.append(round(truckLoad * 100, 2))
            table.append(truckInventory)

        table = sorted(table, key=lambda x: x[-1], reverse=True)
        return {row[0]: row[1:] for row in table}
    
    
    def pretifySolution(self, solution):
        pretifiedSolution = []
        for truck, values in solution.items():
            values.insert(0, truck)
            pretifiedSolution.append(values)

        headers = ['Truck']
        headers.extend(iter(self.getProductNames()))
        headers.append('Capacity %')

        return tabulate(pretifiedSolution, headers=headers, floatfmt=".2f")
