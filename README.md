# pySA
Simulated Annealing algorithm

Module：simAnneal_FUNC is used to find the maximun or minimun value

Module: simAnneal_TSP is used to figure out the TSP problem, find the shortest path.

### Example 1. Using Module simAnneal_FUNC 

**2D function f(x, y)**:

 $$ f(x,y) = y\ sin(2 \pi x) + x\cos(2\pi y) $$
 
#### 1.1 Find the maximun value

**Step 1. Import modules**
```python
from random import random
from simAnneal_FUNC import SimAnneal, OptSolution
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
```
**Step 2. Define function**
```python
def func(w):
    x, y = w
    fxy = y*np.sin(2*np.pi*x) + x*np.cos(2*np.pi*y)
    return fxy
```
**Step 3. Run and Visulization**
```python
if __name__ == '__main__':

    targ = SimAnneal(target_text='max')
    init = -sys.maxsize # for maximun case
    #init = sys.maxsize # for minimun case
    xyRange = [[-2, 2], [-2, 2]]
    xRange = [[0, 10]]

    calculate = OptSolution(Markov_chain=1000, result=init, val_nd=[0,0])
    output = calculate.soulution(SA_newV=targ.newVar, SA_juge=targ.juge, juge_text='max',ValueRange=xyRange, func=func2)
                        
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
```
![Maximun of SA](https://github.com/kjzhang9/pySA/blob/master/SA_max.png  "Maximun")
![Minimun of SA](https://github.com/kjzhang9/pySA/blob/master/SA_min.png  "Min")

### Example 2. Using Module simAnneal_TSP

**Just run the example.py, to test reliability , we use Module simAnneal_TSP to find the shortest path. As we know, for this case, circumference is the shortest path.**

The followed figure shows dynamic process:

![TSP of SA](https://github.com/kjzhang9/pySA/blob/master/circle_tsp.gif  "TSP")

 