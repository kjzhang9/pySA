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
from simAnneal_PIL import SimAnneal
from simAnneal_PIL import OptSolution
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def funPixel(target, tmp):
	'''
	target: the pixels of target picture
	tmp   : the pixels of current picture
	'''
	delta_total = 0
	for i in range(len(target)):
		delta_r = tmp[i][0] - target[i][0]
		delta_g = tmp[i][1] - target[i][1]
		delta_b = tmp[i][2] - target[i][2]
		delta_total += delta_r**2 + delta_g**2 + delta_b**2
	return delta_total

#if __name__ == '__main__':
def run_draw():
	#init = -sys.maxsize # for maximun case
	init = sys.maxsize # for minimun case
	Mar_chain = 100
	targ = SimAnneal(target_text='min', Markov_chain=Mar_chain, numPatch=30, picture='fire.jpg')

	t_start = time()

	calculate = OptSolution(temperature0=300, temDelta=0.98, Markov_chain=Mar_chain, result=init, val_nd=[0,0])
	out = []

	out = calculate.soulution(output=out, SA_preV=targ.iniSolution, SA_newV=targ.newSolution, SA_juge=targ.juge, 
							  juge_text='min',func=funPixel)


	t_end = time()
	#print(city_pos)
	print('Running %.4f seconds' %(t_end-t_start))

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
	'''
if __name__ == '__main__':
	run_draw()