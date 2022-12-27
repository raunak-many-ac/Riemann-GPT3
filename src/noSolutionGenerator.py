# Note: - It is an incomplete file
# Generate prompts that have "No Solution" in hypothesized Inverse of Riemann Zeta Function
import random
import numpy
import mpmath
import matplotlib.pyplot as plotter

from src.constants import Constants

def generateNoSolutionDataPoints(dataPoints):

    pass

def generateNoSolutionFor(fixedImag):
    hundredMillion = 1000
    interval = 4/hundredMillion
    realPart = -2

    inputReal = []
    zetaReal = []
    dataPoints = []

    while realPart < 2:
        inputOfZeta = mpmath.mpc(realPart, fixedImag)

        outputOfZeta = mpmath.zeta(inputOfZeta)

        inputReal.append(realPart)
        zetaReal.append(outputOfZeta.real)
        dataPoints.append((inputOfZeta, outputOfZeta))
        realPart += interval

    plotter.plot(numpy.array(inputReal), numpy.array(zetaReal))
    plotter.show(block=True)

    generateNoSolutionDataPoints(dataPoints=dataPoints)


# constReal = random.randrange(start=-2, stop=2) * random.random()

constImag = random.randrange(start=Constants.NEGATIVE_INFINITE, stop=Constants.INFINITE) * random.random()

generateNoSolutionFor(constImag)
