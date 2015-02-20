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
	c = open("random_number_test.txt","w")
	for i in range(0,n):
		t = a * (seed % q) - r * (seed / q)
		if t > 0:
			seed = t
		else:
			seed = t + m
		number = float (seed)/m
		number = str(number)
		c.write(number)
		c.write('\n')
	c.close()	
def MultipleStreamRN(j,n):
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
		for i in range(0,arrivalOrigin):
			seed_0 = (a**j % m) * seed_0 % m
			InitialSeeds.append(seed_0)

	dic = {y:[0]*arrivalOrigin for y in range(0,n)}
	for i in range(0,n):
		c = open("random_number_0%i.txt" %i,"w")
		for s in range(len(InitialSeeds)):
			if i == 0:
				dic[i][s] = InitialSeeds[s]
			else:
				t = a * (dic[i-1][s] % q) - r * (dic[i-1][s] / q)
				if t > 0:
					dic[i][s] = t
				else:
					dic[i][s] = t + m
			number = float (dic[i][s])/m
			rdnumber = str(number)
			c.write(rdnumber)
			c.write('\n')
		c.close()
	
	
if __name__ == '__main__':
    MultipleStreamRN(100000,10)
    # RNGForTest(100000)