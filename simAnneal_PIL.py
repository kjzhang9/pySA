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
from PIL import Image, ImageDraw

class SimAnneal(object):
	'''
	Simulated annealing algorithm 
	'''

	def __init__(self, numPatch=30, picture='', target_text='min', Markov_chain=1000):
		self.target_text = target_text
		self.Markov_chain = Markov_chain
		self.numPatch = numPatch
		self.picture = picture

	def tar_pix(self):
		im = Image.open(self.picture)
		#im = im.resize((256, 256))
		self.tar_pixel = [im.getpixel((x, y)) for x in range(0, 256) for y in range(0, 256)]
		return self.tar_pixel

	def colorTriangle(self, size):
		trg_axy = [np.random.randint(0, size[0]), np.random.randint(0, size[1])]
		trg_bxy = [np.random.randint(0, size[0]), np.random.randint(0, size[1])]
		trg_cxy = [np.random.randint(0, size[0]), np.random.randint(0, size[1])]
		clr_rgba = [np.random.randint(0, 255) for i in range(3)] + [np.random.randint(95, 115)]
		return [(trg_axy[0], trg_axy[1]), \
				(trg_bxy[0], trg_bxy[1]), \
				(trg_cxy[0], trg_cxy[1]), \
				(clr_rgba[0], clr_rgba[1], clr_rgba[2], clr_rgba[3])]

	def evolution(self, best_tmp):
		'''
		develop a new solution from previous best solution
		'''
		new_tmp = copy.copy(best_tmp)
		for i in range(6):
			indx = np.random.randint(0, self.numPatch)
			new_tmp[indx][0] = tuple(min(max(0, best_tmp[indx][0][i] + np.random.randint(-10, 10)), 255) for i in range(2))
			new_tmp[indx][1] = tuple(min(max(0, best_tmp[indx][1][i] + np.random.randint(-10, 10)), 255) for i in range(2))
			new_tmp[indx][2] = tuple(min(max(0, best_tmp[indx][2][i] + np.random.randint(-10, 10)), 255) for i in range(2))
			new_tmp[indx][3] = tuple([min(max(0, best_tmp[indx][3][i] + np.random.randint(-15, 15)), 255) for i in range(3)] \
					  		  		+ [np.random.randint(95, 115)])
		return new_tmp

	def draw_single(self, single, size=(256, 256)):
		img_s = Image.new('RGBA', size)
		draw = ImageDraw.Draw(img_s)
		draw.polygon([single[0], single[1], single[2]], fill = single[3])
		return img_s

	def draw_all(self, triangles):
		img_a = Image.new('RGBA', size=(256, 256))
		draw_a = ImageDraw.Draw(img_a)
		draw_a.polygon([(0, 0), (0, 255), (255, 255), (255 ,0)], fill=(255, 255, 255, 255))
		for single in triangles:
			img_a = Image.alpha_composite(img_a, self.draw_single(single))
		pixels = [img_a.getpixel((x, y)) for x in range(0, 256) \
										 for y in range(0, 256)]
		#img_a.save('triangle.jpg', 'jpeg')
		return pixels

	def iniSolution(self):
		iniV = [self.colorTriangle(size=(256, 256)) for j in range(self.numPatch)]
		#print(iniV)
		return iniV

	def newSolution(self, best):
		newT = self.evolution(best)
		return newT

	def juge(self, func, new, old, T):
		'''
		matropolise conditions: to get the maximun or minmun
		:new : new solution data from self.newX
		:old : old solution data
		:T   : current temperature
		
		'''
		newfuc = func(self.tar_pix(), self.draw_all(new))
		oldfuc = func(self.tar_pix(), self.draw_all(old))
		dE = newfuc - oldfuc if self.target_text == 'max' else oldfuc - newfuc
		if dE >= 0:
			x, ans = new, newfuc
		else:
			if math.exp(dE/T) > random():
				x, ans = new, newfuc
			else:
				x, ans = old, oldfuc
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


	def soulution(self, SA_preV, SA_newV, SA_juge, juge_text, func, output=[]):
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
			if numbers == 0:
				preV = SA_preV
				res_temp = [SA_juge(new=SA_newV(preV()), func=func, old=preV(), T=Ti) \
							for i in range(self.Markov_chain)]
			else:
				preV = output[-1][0]
				res_temp = [SA_juge(new=SA_newV(preV), func=func, old=preV, T=Ti) \
							for i in range(self.Markov_chain)]

			# change list to numpy.array
			sol_temp = np.array(res_temp)
			#print(sol_temp)
			print(sol_temp.shape)
			# find the extreme value
			extreme_temp = nf(sol_temp[:, 1])
			# find the row No. and column No. of the extreme value
			re = np.where(sol_temp == extreme_temp)

			result_temp = f(self.result, extreme_temp)

			if result_temp != self.result:
				self.val_nd = sol_temp[re[0][0], 0]
				#print(result_temp)
				#print(sol_temp[re[0][0], 0])
				output.append([self.val_nd, result_temp])
				count = 1
				numbers += 1
			else:
				count += 1

			if count >= 50: break

			self.result = result_temp
			print(result_temp)

			# update the current temperature
			Ti *= self.temDelta
			t1 = time.time()-t0

			#print(t1, Ti)
			#print(count, numbers)

		return output