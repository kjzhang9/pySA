# -*- coding: utf-8 -*-

'''
======================================
|           kiterun                  |
|		   2017/08/11                |
|		 kiterun@126.com             |
======================================
'''

from random import random
import math
import sys
from time import time
from simAnneal_TSP import SimAnneal
from simAnneal_TSP import OptSolution
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def func(w):
	x, = w
	fx = x + 10*math.sin(5*x) + 7*math.cos(4*x)
	return fx

def func2(w):
	x, y = w
	fxy = y*np.sin(2*np.pi*x) + x*np.cos(2*np.pi*y)
	return fxy

def funTSP(keylist, city_pos):
	'''
	keylist : shuffle([0,1,2,...,n])
	'''
	queue = np.array([city_pos[i] for i in keylist])
	totalLen = np.sum(np.sqrt(np.sum(np.square(queue[:-1]-queue[1:]), axis=1)))
	return totalLen

#if __name__ == '__main__':
def run_draw():
	#init = -sys.maxsize # for maximun case
	init = sys.maxsize # for minimun case
	Mar_chain = 1000
	xyRange = [[-50, 50], [-50, 50]]
	xRange = [[0, 10]]
	targ = SimAnneal(target_text='min', Markov_chain=Mar_chain, ValueRange=xyRange, numCity=30)
	city_pos = targ.iniTSPcircle(R=40)
	#city_pos = targ.iniTSP()
	t_start = time()

	calculate = OptSolution(temperature0=300, temDelta=0.98, Markov_chain=Mar_chain, result=init, val_nd=[0,0])
	out = []

	out = calculate.soulution(output=out, SA_preV=targ.oldTSP, SA_newV=targ.newTSP, SA_juge=targ.juge, 
							  juge_text='min',city_p=city_pos, func=funTSP)

	with open('out1.dat', 'w') as f:
		for i in range(len(out)):
			f.write(str(out[i]) + '\n')

	with open('citypos0.dat', 'w') as f:
		for i in range(len(city_pos)):
			f.write(str(city_pos[i]) + '\n')

	t_end = time()
	#print(city_pos)
	print('Running %.4f seconds' %(t_end-t_start))
	'''
	# plot animation
	fig = plt.figure()
	ax = Axes3D(fig)
	xv = np.linspace(xyRange[0][0], xyRange[0][1], 200)
	yv = np.linspace(xyRange[1][0], xyRange[1][1], 200)
	xv, yv = np.meshgrid(xv, yv)
	zv = func2([xv, yv])
	ax.plot_surface(xv, yv, zv, rstride=1, cstride=1, cmap='GnBu', alpha=1)
	#dot = ax.scatter(0, 0, 0, 'ro')
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	x, y, z = output[0][0], output[0][1], output[1]
	ax.scatter(x, y, z, c='r', marker='o')

	plt.savefig('SA_min.png')
	plt.show()
	'''

	fig, ax = plt.subplots()
	ax.grid()
	
	line, = ax.plot([], [], 'o-', lw=2)
	length_template = 'length = %.5f'
	length_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

	def init():
		#ax.set_title('TSP path')
		ax.set_xlim(xyRange[0][0]-5, xyRange[0][1]+5)
		ax.set_ylim(xyRange[1][0]-5, xyRange[1][1]+5)
		line.set_data([], [])
		length_text.set_text('')
		return line, length_text

	def update(i):
		newx = [city_pos[j][0] for j in out[i][0]]
		newy = [city_pos[j][1] for j in out[i][0]]
		line.set_data(newx, newy)
		length_text.set_text(length_template %(out[i][1]))
		return line, length_text

	ani = animation.FuncAnimation(fig, update, range(len(out)), init_func=init, repeat=False, interval=200, blit=True)
	#ani.save('circle_tsp.gif', writer='imagemagick')
	ani.save('tsp1.mp4', extra_args=['-vcodec', 'libx264'])

	plt.show()
	
if __name__ == '__main__':
	run_draw()