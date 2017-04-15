import numpy as np
import ode
import schwarzschild as sch
from matplotlib import pyplot as plt
from matplotlib import animation
from auxiliar import max as max
from auxiliar import deg_to_rad as deg_to_rad
import orbitas as orb
from auxiliar import max

class orbit_animation:
    def __init__(self,orbit,lim):
        self.orbit = orbit
        self.fig = plt.figure(figsize=(15,10))
        self.ax = self.fig.add_axes([0.1, 0.30, 0.8, 0.60])
        plt.axis("equal")
        self.orbit.part.draw_part(self.ax)
        self.ax.set_xlim((-lim,lim))
        self.ax.set_ylim((-lim,lim))
        self.stop = False
        self.n_of_frames = 200 #The time variable will have values module n
        self.init_text_variables()
        self.energy_Diagram()
        return

    '''Text dinamical variables for the plot'''
    def init_text_variables(self):
        ax = self.ax
        self.Radius_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
        self.Phi_text = ax.text(0.02, 0.80, '', transform=ax.transAxes)
        self.V_text = ax.text(0.02, 0.70, '', transform=ax.transAxes )
        self.time_text = ax.text(0.02, 0.60, '', transform=ax.transAxes )
        self.proper_time_text = ax.text(0.02, 0.50, '', transform=ax.transAxes )
        return

    ''' Creates the object to draw the energy diagram '''
    def energy_Diagram(self):
        part = self.orbit.part
        bh = self.orbit.bh
        L, E2, M = part.L , part.E2, bh.M
        self.ED = self.fig.add_axes([0.1, 0.1, 0.8, 0.15])
        self.ED.set_xlim((2*(M),10))
        self.ED.set_xlabel('radius')
        self.ED.set_ylabel('E^2')
        self.V_pot, = self.ED.plot([], [], 'o-',lw=4 )
        ''' Verifies if rmax exists and set ylim as E2+1 or V(rmax)+1 '''
        if(pow(L,2)>12*pow(M,2)):
            m = max(E2+1,1 + part.V([0,part.rmax,0]))
            self.ED.set_ylim((0,m))
        else:
            self.ED.set_ylim((0,E2+1))
    '''Draws the potential, the energy lines '''
    def draw_ED(self):
        bh = self.orbit.bh
        part = self.orbit.part
        L, E2, M = part.L , part.E2, bh.M
        r_vec = np.linspace(2*M,10,1000)
        pot = []
        energ = []
        for i in range(0,len(r_vec)):
            pot = pot + [part.V([0,r_vec[i]])]
            energ = energ + [E2]
        self.ED.plot(r_vec,pot)
        self.ED.plot(r_vec,energ,color = 'r')
        if(pow(L,2)>12*pow(M,2)):
            m = max(E2+1,1 + part.V([0,part.rmax,0]))
            energ_vec = np.linspace(0,m,1000)
            rmax_vec = []
            rmin_vec = []
            for i in range(0,len(energ_vec)):
                rmax_vec = rmax_vec + [part.rmax]
                rmin_vec = rmin_vec + [part.rmin]
            self.ED.plot(rmax_vec,energ_vec, color = 'y')
            self.ED.plot(rmin_vec,energ_vec,color = 'g')
        return

    def update_orbit_text(self):
        time = self.orbit.time
        bh = self.orbit.bh
        part = self.orbit.part
        ode = self.orbit.ode
        tau = part.cv[0]*ode.step_h
        r = part.cv[1]
        phi = part.cv[2]
        X = part.cv
        self.Radius_text.set_text('r = %.3f' % r)
        self.Phi_text.set_text('Phi = %.3f ' % deg_to_rad(phi) )
        self.V_text.set_text('V(r) = %.3f' % part.V(X) )
        self.time_text.set_text('t = %.3f' % time )
        self.proper_time_text.set_text('tau = %.3f' % tau )
        self.V_pot.set_data([r],[part.V(X)])
        return
    ''' initialization function: plot the background of each frame
        Set the ODE we want to solve
        Returns the variables that need to be redrawn'''

    def init(self):
        self.draw_ED()
        self.orbit.part.body.center = (self.orbit.part.px, self.orbit.part.py)
        self.ax.add_patch(self.orbit.part.body)
        self.ax.add_artist(self.orbit.bh.body) #Draw the BH

        return  (self.orbit.part.body, self.Radius_text, self.Phi_text, self.V_text,
                self.V_pot, self.time_text , self.proper_time_text, self.orbit.part.trail,)

    # animation function.  This is called sequentially
    #For each time t it evolves one step in the RK and use that value to draw
    #Return the variables that need to be redrawn

    def animate(self,t):
        part = self.orbit.part
        bh = self.orbit.bh
        E2 = self.orbit.part.E2
        h = self.orbit.ode.step_h
        time = (self.orbit.time)
        time = time + h
        part = self.orbit.part
        if(self.stop == False):
            self.orbit.update_orbit(time*h)
            self.update_orbit_text()

        #Stop refreshing if we have a collision
        if((np.sqrt(pow(part.px,2)+pow(part.py,2))) <= 2*bh.M + part.plot_radius ):
            self.stop = True

        self.orbit.time = time
        return  (self.orbit.part.body, self.Radius_text, self.Phi_text, self.V_text,
                self.V_pot, self.time_text , self.proper_time_text, self.orbit.part.trail,)


    ''' call the animator.  blit=True means only re-draw the parts that have changed'''
    def show_orbit(self):
        part = self.orbit.part
        E2 , X = part.E2, part.cv
        if( (E2 - self.orbit.part.V(X) <= 0.01)  ):
            print('Valor de E2 e r0 viola a equacao de energia!\n')
        else:
            fig = self.fig
            animate = self.animate
            init = self.init
            anim = animation.FuncAnimation(fig, animate, init_func=init,
                                                frames=self.n_of_frames, interval=20, blit=True)
            plt.show()
        return
