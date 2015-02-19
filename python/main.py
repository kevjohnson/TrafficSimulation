import TrafficSimulation
import csv


def main():
    flow = 0.5
    period = 30
    with open("data/Arrival Rates.csv") as inFile:
        reader = csv.reader(inFile)
        arrivalRates = {int(rows[0]): float(rows[1]) for rows in reader}
    with open("data/Travel Matrix.csv") as inFile:
        reader = csv.reader(inFile)
        travelMatrix = {int(rows[0]): rows[1:] for rows in reader}
    for key in travelMatrix:
        for index, item in enumerate(travelMatrix[key]):
            travelMatrix[key][index] = float(travelMatrix[key][index])
    with open("data/Capacity.csv") as inFile:
        reader = csv.reader(inFile)
        capacity = {int(rows[0]): int(rows[1]) for rows in reader}
    timeLimit = 60 * 100
    simulation = TrafficSimulation.TrafficSimulation(
        arrivalRates, travelMatrix, capacity, flow, period, timeLimit)
    simulation.run()
    with open("output.txt", 'w') as outFile:
        output = simulation.getOutput()
        for elem in output:
            outFile.write("{}\n".format(elem))

if __name__ == "__main__":
    main()
