import numpy as np

'''Auxiliar functions Library'''

#******************************************************************************#

#gets the maximum
def max(a,b):
    if(a > b):
        return a
    else:
        return b

#Returns a vectorial function evaluated on x,t
def ev(f,x,t):
    a = []
    for i in range(0,len(f)):
        a = a + [f[i](x,t)]
    return a
#Converts degrees to radians in [0,2pi]
def deg_to_rad(a):
    theta = np.radians(a)
    while(theta >= 2*np.pi):
        theta = theta - 2*np.pi
    while(theta <= -2*np.pi):
        theta = theta + 2*np.pi
    return theta
