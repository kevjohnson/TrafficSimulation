import numpy as np
import math
import scipy.stats
import csv
import matplotlib.pyplot as plt


def RNGForTest(n):
    seed = 10
    a = 48271
    q = 44488
    r = 3399
    # m = a * q + r
    m = 2**31 - 1
    # Compute ax mod m without overflow
    # x = []
    c = open("random_number.txt", "w")
    for i in range(0, n):
        t = a * (seed % q) - r * (seed / q)
        if t > 0:
            seed = t
        else:
            seed = t + m
        # print seed
        number = float(seed) / m
        number = str(number)
        # x.append(number)
        c.write(number)
        c.write('\n')
    c.close()
    # return x


def MultipleStreamRN(j, n):
    seed_0 = 1
    a = 48271
    q = 44488
    r = 3399
    # m = a * q + r
    m = 2**31 - 1
    arrivalOrigin = 11
    InitialSeeds = []
    if n >= j:
        return False
    elif n < j:
        for i in range(0, arrivalOrigin):
            seed_0 = (a**j % m) * seed_0 % m
            InitialSeeds.append(seed_0)
    # print InitialSeeds
    i = 0
    dic = {z: [0.0] * n for z in range(0, arrivalOrigin)}
    for seed in InitialSeeds:
        c = open("random_number%i.txt" % i, "w")
        for z in range(0, n):
            t = a * (seed % q) - r * (seed / q)
            if t > 0:
                seed = t
            else:
                seed = t + m
            # print seed
            number = float(seed) / m
            dic[i][z] = str(number)
            c.write(dic[i][z])
            c.write('\n')
        c.close()
        i = i + 1

    # return dic.values()

# def Exponential(rate,n):
# 	interarrival = []
# 	for number in RandomNumberGenerator(n):
# 		deltaT = - math.log(number) / rate
# 		interarrival.append(deltaT)
# 	return interarrival

if __name__ == '__main__':
    MultipleStreamRN(100000, 10000)
    # RNGForTest(100000)
