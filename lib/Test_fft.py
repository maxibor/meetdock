#!/usr/bin/env python3
import fft
import random as rand
import pandas
    
def test_distance():
	"""Test dist_cal function assert that the distance returned by the dist_cal
	fonction is alway positive"""
	for i in range(10**6):
		x1 = rand.uniform(-100,100)
		y1 = rand.uniform(-100,100)
		z1 = rand.uniform(-100,100)
		x2 = rand.uniform(-100,100)
		y2 = rand.uniform(-100,100)
		z2 = rand.uniform(-100,100)
		assert fft.dist_cal(x1, y1, z1, x2, y2, z2) > 0

def test_init_grid():
	"""Test init_grid function :  assert that number of columns is 4 
	whatever the number input and rows exists"""
	for essais in range(10**3):
		i = rand.randint(0,1000)
		mygrid = fft.init_grid(1)
		assert mygrid.shape[1] == 4 and mygrid.shape[0] != 0