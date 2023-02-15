import numpy
import matplotlib.pyplot

# plots a new graph in a new window with curves given
def plotTheseNew(
    xOfCurves: list[numpy.ndarray],
    yOfCurves: list[numpy.ndarray],
    titleOfPlot,
    coloursOfCurves: list[str],
    plt: matplotlib.pyplot,
    nameOfCurves: list[str] = [],
    xLabel: str = "Real axis",
    yLabel: str = "Imaginary axis",
) -> matplotlib.pyplot:
    countOfCurves = len(xOfCurves)
    assert countOfCurves == len(yOfCurves)
    assert nameOfCurves is None or 0 == len(nameOfCurves) or countOfCurves == len(nameOfCurves)
    assert countOfCurves == len(coloursOfCurves)

    minX, maxY = 0, 0
    fig = plt.figure()
    fig.canvas.manager.set_window_title(titleOfPlot)
    for i in range(0, countOfCurves):

        xpoints = xOfCurves[i]
        minX = min(minX, min(xpoints))
        ypoints = yOfCurves[i]
        maxY = max(maxY, max(ypoints))

        plt.plot(
            xpoints,
            ypoints,
            color=coloursOfCurves[i],
            marker=".",
            markersize=10,
            label=nameOfCurves[i] if nameOfCurves is not None and len(nameOfCurves) != 0 else "",
        )
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)

    return plt
