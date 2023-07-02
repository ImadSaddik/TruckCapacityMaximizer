from django.shortcuts import render
from django.contrib import messages

import plotly.graph_objects as go
import plotly.offline as opy

from .solver import Solver
from pulp import *

import numpy as np
import random
import time


def home(request):
    return render(request, "solver/home.html", {})


showInputProducts = False
showInputTruckTypes = False
numberOfProducts = 0
numberOfTruckTypes = 0

productVolumes = []
productDemandQuantity = []
truckTypeCapacities = []
numberOfTrucksPerType = []

def manual(request):
    global showInputProducts
    global showInputTruckTypes
    global numberOfProducts
    global numberOfTruckTypes
    global productVolumes
    global productDemandQuantity
    global truckTypeCapacities
    global numberOfTrucksPerType
    
    if request.POST.get('form_type') == 'PRODUCTS':
        showInputProducts = True
        numberOfProducts = int(request.POST.get('number_of_products'))
        
    if request.POST.get('form_type') == 'TRUCKS':
        showInputTruckTypes = True
        numberOfTruckTypes = int(request.POST.get('number_of_truck_types'))
        
    if request.POST.get('form_type') == 'PRODUCTS_INFORMATION':
        productVolumes = [
            int(request.POST.get(f'product_volume_{i}'))
            for i in range(numberOfProducts)
        ]
        productDemandQuantity = [
            int(request.POST.get(f'product_demand_{i}'))
            for i in range(numberOfProducts)
        ]
        
    if request.POST.get('form_type') == 'TRUCKS_INFORMATION':
        truckTypeCapacities = [
            int(request.POST.get(f'truck_capacity_{i}'))
            for i in range(numberOfTruckTypes)
        ]
        numberOfTrucksPerType = [
            int(request.POST.get(f'truck_number_per_type_{i}'))
            for i in range(numberOfTruckTypes)
        ]
        
    context = {
        'showInputProducts': showInputProducts, 
        'showInputTruckTypes': showInputTruckTypes,
        'numberOfProducts': range(numberOfProducts),
        'numberOfTruckTypes': range(numberOfTruckTypes)
    }
    
    return render(request, "solver/manual.html", context=context)
    

def result(request):
    global numberOfProducts
    global numberOfTruckTypes
    global productVolumes
    global productDemandQuantity
    global truckTypeCapacities
    global numberOfTrucksPerType

    if (productVolumes == [] or productDemandQuantity == [] or truckTypeCapacities == [] or numberOfTrucksPerType == []):
        messages.error(request, "Please fill in all the information")
        return render(request, "solver/manual.html", {})
    
    prob = LpProblem("Truck Loading Problem", LpMinimize)
    solver = Solver(numberOfProducts=numberOfProducts, 
                    numberOfTruckTypes=numberOfTruckTypes,
                    prob=prob,
                    productVolumes=productVolumes,
                    productDemandQuantity=productDemandQuantity,
                    truckTypeCapacities=truckTypeCapacities,
                    numberOfTrucksPerType=numberOfTrucksPerType
                )
    
    solution = solver.getSolution()
    averageFillRate = getAverageFillRate(solution)
    status = LpStatus[prob.status]
    canShowTable = status == 'Optimal'
    trucksUsedBarPlot = getBarChart(solution)
    truckFillRateBarPlot = getFillRateBarChart(solution, solver.getTruckTypeNames())

    context = {
        'solution': solution,
        'averageFillRate': averageFillRate,
        'status': status,
        'numberOfProducts': range(numberOfProducts),
        'canShowTable': canShowTable,
        'trucksUsedBarPlot': trucksUsedBarPlot,
        'truckFillRateBarPlot': truckFillRateBarPlot
    }
    return render(request, "solver/result.html", context=context)


def getAverageFillRate(solution):
    sumOfFillRate = 0
    usedTrucksCount = 0
    
    for value in solution.values():
        sumOfFillRate += max(value[-1], 0)
        usedTrucksCount += 1 if value[-1] > 0 else 0

    return round((sumOfFillRate / usedTrucksCount), 2)


def getBarChart(data):
    x = ['Used', 'Not used']
    usedTrucksCount = sum(1 if value[-1] > 0 else 0 for value in data.values())
    y = [usedTrucksCount, len(data) - usedTrucksCount]
    
    fig = go.Figure(data=go.Bar(x=x, y=y))
    fig.update_layout(
        title='Trucks usage comparison',
        title_x=0.5,
        xaxis_title='Trucks',
        yaxis_title='Number of trucks',
    )
    return opy.plot(fig, auto_open=False, output_type='div')


def getFillRateBarChart(data, truckTypeNames):
    global numberOfTrucksPerType
    x = truckTypeNames
    y = np.zeros(len(truckTypeNames))
    
    for key, value in data.items():
        truckTypeName = key.split("_")[0] + "_" + key.split("_")[1]
        truckTypeIndex = x.index(truckTypeName)
        y[truckTypeIndex] += max(value[-1], 0)
        
    y /= numberOfTrucksPerType
    
    fig = go.Figure(data=go.Bar(x=x, y=y))
    fig.update_layout(
        title='Fill rate average per truck type',
        title_x=0.5,
        xaxis_title='Trucks',
        yaxis_title='Average fill rate',
    )
    return opy.plot(fig, auto_open=False, output_type='div')
        

async def benchmark(request):
    executionTimes = await getExecutionTimes()
    timeComplexityPlot = getTimeComplexityPlot(executionTimes)
    
    context = {
        'timeComplexityPlot': timeComplexityPlot
    }
    return render(request, "solver/benchmark.html", context=context)


async def getExecutionTimes():
    executionTimes = []
    numberOfProducts = 100
    
    for i in range(1, 10):
        startTime = time.time()
        
        prob = LpProblem("Truck Loading Problem", LpMinimize)
        solver = Solver(numberOfProducts=numberOfProducts, 
                        numberOfTruckTypes=i,
                        prob=prob,
                        productVolumes=generateProductVolumes(numberOfProducts),
                        productDemandQuantity=generateProductDemandQuantity(numberOfProducts),
                        truckTypeCapacities=generateTruckTypeCapacities(numberOfTruckTypes=i),
                        numberOfTrucksPerType=generateNumberOfTrucksPerType(numberOfTruckTypes=i)
        )
        _ = solver.getSolution()
        
        endTime = time.time()
        executionTimes.append(round(endTime - startTime, 2))
        
    return executionTimes


def generateProductVolumes(numberOfProducts):
    return [random.random() * 5 for _ in range(numberOfProducts)]


def generateProductDemandQuantity(numberOfProducts):
    return [random.randint(10, 1000) for _ in range(numberOfProducts)]


def generateTruckTypeCapacities(numberOfTruckTypes):
    return [random.randint(50, 300) for _ in range(numberOfTruckTypes)]


def generateNumberOfTrucksPerType(numberOfTruckTypes):
    numberOfTrucksPerType = [5]
    return numberOfTrucksPerType * numberOfTruckTypes


def getTimeComplexityPlot(executionTimes):
    x = list(range(1, len(executionTimes)))
    y = executionTimes
    
    fig = go.Figure(data=go.Scatter(x=x, y=y))
    fig.update_layout(
        title='Execution time as a function of the number of truck types',
        title_x=0.5,
        xaxis_title='Number of truck types',
        yaxis_title='Time (s)',
    )
    return opy.plot(fig, auto_open=False, output_type='div')
