# -*- coding: utf-8 -*-

'''
=========================================
|                kiterun                |
|		        2017/08/13              |
|	          kiterun@126.com           |
=========================================
'''
from random import random
import math
import sys
import numpy as np
import time
import copy

class SimAnneal(object):
	'''
	Simulated annealing algorithm 
	'''
	def __init__(self, numCity,target_text='min', Markov_chain=1000, 
				 ValueRange=[[0, 2],[0, 2]]):
		self.target_text = target_text
		self.Markov_chain = Markov_chain
		self.ValueRange = ValueRange
		self.nd = len(self.ValueRange)
		self.numCity = numCity

### TSP case
	def iniTSP(self):
		city_pos = dict([[i, [self.mapRange(self.ValueRange[j]) for j in range(len(self.ValueRange))]] for i in range(self.numCity)])
		return city_pos

	def iniTSPcircle(self, R=30):
		radian = np.linspace(0, 2*np.pi, self.numCity)
		xarr = list(np.cos(radian)*R)
		yarr = list(np.sin(radian)*R)
		city_pos = dict([[i, [xarr[i],yarr[i]]] for i in range(self.numCity)])
		return city_pos

	def oldTSP(self):
		oldT = [i for i in range(self.numCity)]
		np.random.shuffle(oldT)
		return oldT

	def newTSP(self, oldList):
		'''
		for TSO question
		:oldList : old path list
		:return : new path list solution
		'''
		length = self.numCity
		x, y = 0, 0
		newList = copy.copy(oldList)
		while x == y:
			x = np.random.randint(0, length)
			y = np.random.randint(0, length)
			if np.random.random() <= 0.5:
				newList[x], newList[y] = newList[y], newList[x]
			else:
				newList[x:(y+1)] = newList[x:(y+1)][::-1]
		return newList

	def mapRange(self, oneDrange):
		return (oneDrange[1]-oneDrange[0])*random() + oneDrange[0]

	def juge(self, func, new, old, T, city_pos):
		'''
		matropolise conditions: to get the maximun or minmun
		:new : new solution data from self.newX
		:old : old solution data
		:T   : current temperature
		
		'''
		dE = func(new, city_pos) - func(old, city_pos) if self.target_text == 'max' else func(old, city_pos) - func(new, city_pos)
		if dE >= 0:
			x, ans = new, func(new, city_pos)
		else:
			if math.exp(dE/T) > random():
				x, ans = new, func(new, city_pos)
			else:
				x, ans = old, func(old, city_pos)
		return [x, ans]


class OptSolution(object):
	'''
	find the optimal solution.

	'''
	def __init__(self, temperature0=100, temDelta=0.98,
				 temFinal=1e-8, Markov_chain=2000, 
				 result=0, val_nd=[0]):
		# initial temperature
		self.temperature0 = temperature0
		# step factor for decreasing temperature
		self.temDelta = temDelta
		# the final temperature
		self.temFinal = temFinal
		# the Markov_chain length (inner loops numbers)
		self.Markov_chain = Markov_chain
		# the final result
		self.result = result
		# the initial coordidate values: 1D [0], 2D [0,0] ...
		self.val_nd = val_nd


	def soulution(self, SA_preV, SA_newV, SA_juge, juge_text, city_p, func, output=[]):
		'''
		calculate the extreme value: max or min value
		:SA_newV : function from class SimAnneal().newVar
		:SA_juge : function from class SimAnneal().juge_*
		:ValueRange : [[],], range of variables, 1D or 2D or 3D...
		:func : target function obtained from user

		'''
		Ti = self.temperature0
		f = max if juge_text=='max' else min
		nf = np.amax if juge_text=='max' else np.amin
		numbers = 0 
		#output = []

		while Ti > self.temFinal:

			res_temp = []
			t0 = time.time()
			preV = SA_preV() if numbers == 0 else output[-1][0]
			
			res_temp = [SA_juge(new=SA_newV(preV), func=func, old=preV, T=Ti, city_pos=city_p) for i in range(self.Markov_chain)]
			# change list to numpy.array
			sol_temp = np.array(res_temp)
			# find the extreme value
			extreme_temp = nf(sol_temp[:, 1])
			# find the row No. and column No. of the extreme value
			re = np.where(sol_temp == extreme_temp)

			result_temp = f(self.result, extreme_temp)

			if result_temp != self.result:
				self.val_nd = sol_temp[re[0][0], 0]
				#print(result_temp)
				#print(sol_temp[re[0][0], 1])
				output.append([self.val_nd, result_temp])
				count = 1
				numbers += 1
			else:
				count += 1

			if count >= 50: break

			self.result = result_temp
			# update the current temperature
			Ti *= self.temDelta
			t1 = time.time()-t0

			print(self.result, t1, Ti)
			print(output[-1], count, numbers)

		return output