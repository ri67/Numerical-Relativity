import numpy as np
from matplotlib import pyplot as plt
import ode
import auxiliar as aux

'''Library that contains the important elements on Schwarzschild's'''
'''            Spacetime model in General Relativity '''

#******************************************************************************#
#Schwarzschild function
M = 0.1
def hsch(Y):
    return 1 - (2*M/Y[1])

#******************************************************************************#

class particle:

    def __init__(self,E2,L,t0,r0,phi0,signal_drds):
        '''Physical variables '''
        self.E2, self.L,self.signal_drds, = E2, L, signal_drds
        '''Coordinate vector in spacetime, phi0 is in degrees'''
        self.cv = [t0,r0,phi0]
        phi = aux.deg_to_rad(phi0)
        self.px, self.py  = r0*np.cos(phi), r0*np.sin(phi)
        if(pow(L,2)>12*pow(M,2)):
            self.rmax = (pow(L,2) - L*np.sqrt(pow(L,2)-12*pow(M,2)))/(2*M) #argmax(V)
            self.rmin = (pow(L,2) + L*np.sqrt(pow(L,2)-12*pow(M,2)))/(2*M) #argmin local(V)
        return

    ''' Create the graphical properties of the plarticle '''
    ''' body is the graphical element for the particle, a circle '''
    ''' trail is the graphical element to plot the trail '''
    def draw_part(self,ax):
        self.plot_radius = 0.025
        self.body = plt.Circle((self.px, self.py), self.plot_radius, fc='r')
        self.trail, = ax.plot([], [] ,lw=1 )
        self.trail.set_data([],[])
        self.trail_pos_x = []
        self.trail_pos_y = []
        return

    '''Particle equations used on the ode
       Notice that we give an Y that could be different from self.cv
       The reason is that we use those functions on the Runge-Kutta
    G1'''
    def dtds(self,Y,t):
        E2 = self.E2
        return np.sqrt(E2)/hsch(Y)
    '''Energy Equation'''
    def drds(self,Y,t):
        E2, sg = self.E2, self.signal_drds
        return sg*( np.sqrt( np.abs( E2 - self.V(Y)) ) )
    def mdrds(self,Y,t):
        E2, sg = self.E2, self.signal_drds
        return (-1.0)*sg*( np.sqrt( np.abs( E2 - self.V(Y)) ) )
    '''G2'''
    def dphids(self,Y,t):
        L, = self.L,
        return 180*(L/(pow(Y[1],2)))/np.pi
    #Potential Energy
    def V(self,Y):
        L = self.L
        return  (1 +  pow(L/Y[1],2))*hsch(Y)
    ''' Calculates the new position of the particle using RK '''
    '''It updates cv, px,py, trail_pos_x and trail_pos_y '''
    def update_pos(self,ode,t):
        self.cv = ode.RK_step(self.cv,t)
        r0 = self.cv[1]
        phi = aux.deg_to_rad(self.cv[2])
        self.px, self.py  = r0*np.cos(phi), r0*np.sin(phi)
        self.trail_pos_x = self.trail_pos_x + [self.px]
        self.trail_pos_y = self.trail_pos_y + [self.py]
        self.trail.set_data(self.trail_pos_x,self.trail_pos_y)
        return

    def pos(self):
        return [self.px,self.py]

#******************************************************************************#

class blackhole:
    def __init__(self,M):
        self.M = M
        self.draw_bh()
        return

    def draw_bh(self):
        self.body = plt.Circle((0, 0), 2*M, fc = 'k')
        return
