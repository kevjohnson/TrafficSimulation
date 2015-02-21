import TrafficSimulation
import csv


def main():
    flow = 1.5
    synchronous = True
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
    with open("data/Signal Timings.csv") as inFile:
        reader = csv.reader(inFile)
        signalTimings = {int(rows[0]): rows[1:] for rows in reader}
    for key in signalTimings:
        for index, item in enumerate(signalTimings[key]):
            signalTimings[key][index] = int(signalTimings[key][index])
    timeLimit = 60 * 150
    seed = 123
    simulation = TrafficSimulation.TrafficSimulation(
        arrivalRates, travelMatrix, capacity, flow, signalTimings,
        timeLimit, synchronous, seed)
    simulation.run()
    with open("output.txt", 'w') as outFile:
        output = simulation.getOutput()
        writer = csv.writer(outFile)
        for elem in output:
            writer.writerow(elem)

if __name__ == "__main__":
    main()
