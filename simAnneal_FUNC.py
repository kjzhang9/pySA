# -*- coding: utf-8 -*-

'''
=========================================
|                kiterun                |
|		        2017/08/11              |
|	          kiterun@126.com           |
=========================================
'''
from random import random
import math
import sys
import numpy as np

class SimAnneal(object):
	'''
	Simulated annealing algorithm 
	'''
	def __init__(self, target_text='min', Markov_chain=1000, 
				 ValueRange=[[0, 2],[0, 2]], numCity=20):
		self.target_text = target_text
		self.Markov_chain = Markov_chain
		self.ValueRange = ValueRange
		self.nd = len(self.ValueRange)
		self.numCity = numCity

### TSP case
	def iniTSP(self):
		city_pos = dict([[i, [[self.mapRange(self.ValueRange[j]), self.mapRange(self.ValueRange[j])] for j in range(self.nd)]] for i in range(self.numCity)])
		return city_pos

	def oldTSP(self):
		oldT = [[i for i in range(self.numCity)] for j in range(self.Markov_chain)]
		for i in range(self.Markov_chain):
			random.shuffle(oldT[i])
		return oldT

	def newTSP(self, oldList):
		'''
		for TSO question
		:oldList : old path list
		:return : new path list solution
		'''
		length = self.numCity
		for i in range(self.Markov_chain):
			x, y = 0, 0
			while x == y:
				x = np.random.randint(0, length)
				y = np.random.randint(0, length)
				oldList[i][x], oldList[i][y] = oldList[i][y], oldList[i][x]
		return oldList

####

	def mapRange(self, oneDrange):
		return (oneDrange[1]-oneDrange[0])*random() + oneDrange[0]

### function extreme value

	def preVar(self):
		preV = [[self.mapRange(self.ValueRange[j]) for i in range(self.Markov_chain)] for j in range(self.nd)]
		return preV

	def newVar(self, oldList):
		'''
		suitable for function extreme value question
		:old : list, from self.preVar return
		:return : list, new solutions based on old solutions
		:T   : current temperature
		'''
		newList = [[i + (random()*2-1) for i in oldList[j]] for j in range(self.nd)]
		return newList
####

	def juge(self, func, new, old, T):
		'''
		matropolise conditions: to get the maximun or minmun
		:new : new solution data from self.newX
		:old : old solution data
		:T   : current temperature
		
		'''
		dE = func(new) - func(old) if self.target_text == 'max' else func(old) - func(new)
		if dE >= 0:
			x, ans = new, func(new)
		else:
			if math.exp(dE/T) > random():
				x, ans = new, func(new)
			else:
				x, ans = old, func(old)
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

	# create unifrom distributed x,y ..., depend on value range
	def mapRange(self, oneDrange):
		return (oneDrange[1]-oneDrange[0])*random() + oneDrange[0]

	def soulution(self, SA_preV, SA_newV, SA_juge, juge_text, ValueRange, func):
		'''
		calculate the extreme value: max or min value
		:SA_newV : function from class SimAnneal().newVar
		:SA_juge : function from class SimAnneal().juge_*
		:ValueRange : [[],], range of variables, 1D or 2D or 3D...
		:func : target function obtained from user

		'''
		Ti = self.temperature0
		ndim = len(ValueRange)
		f = max if juge_text=='max' else min
		nf = np.amax if juge_text=='max' else np.amin
		loops = 0

		while Ti > self.temFinal:
			res_temp = []
			preV = SA_preV() 
			newV = SA_newV(preV)

			for i in range(self.Markov_chain):
				boolV = True
				for j in range(ndim):
					boolV &= (ValueRange[j][0]<= newV[j][i] <= ValueRange[j][1])
				if boolV == True:
					res_temp.append(SA_juge(new=[newV[k][i] for k in range(ndim)], 
									func=func, old=[preV[k][i] for k in range(ndim)], 
									T=Ti))
				else:
					continue
				loops += 1

			# change list to numpy.array
			sol_temp = np.array(res_temp)
			# find the extreme value
			extreme_temp = nf(sol_temp[:, 1])
			# find the row No. and column No. of the extreme value
			re = np.where(sol_temp == extreme_temp)

			result_temp = f(self.result, extreme_temp)
			# update the cooordidate of current extrema value 
			self.val_nd = self.val_nd if result_temp == self.result else sol_temp[re[0][0], 0]
			# update the extreme value
			self.result = result_temp
			# update the current temperature
			Ti *= self.temDelta

		output = [self.val_nd, self.result]
		print(output)
		print('Total loops = %d' %loops)
		return output