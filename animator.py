import numpy as np
import ode
import schwarzschild as sch
import time
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Slider, Button, RadioButtons
from auxiliar import max as max
from auxiliar import deg_to_rad as deg_to_rad
import orbitas as orb

''' The main objective of this library is to create the animation class, which we
    will use to draw the orbit'''
#******************************************************************************#


class orbit_animation:
    def __init__(self,orbit,lim):
        self.orbit = orbit
        self.fig = plt.figure(figsize=(15,10))
        self.ax = self.fig.add_axes([0.025, 0.375, 0.8, 0.60])
        plt.axis("equal")
        self.orbit.part.draw_part(self.ax)
        self.ax.set_xlim((-lim,lim))
        self.ax.set_ylim((-lim,lim))
        self.stop = False
        self.n_of_frames = 60 #The time variable will have values module n
        self.init_text_variables()
        self.energy_Diagram()
        self.sliders()
        self.buttons()
        self.redraw = False
        return

    '''Text dinamical variables for the plot'''
    def init_text_variables(self):
        ax = self.ax
        self.Radius_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
        self.Phi_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)
        self.V_text = ax.text(0.02, 0.80, '', transform=ax.transAxes )
        self.time_text = ax.text(0.02, 0.75, '', transform=ax.transAxes )
        self.proper_time_text = ax.text(0.02, 0.70, '', transform=ax.transAxes )
        self.drds_text = ax.text(0.02, 0.65, '', transform=ax.transAxes )
        self.valid = ax.text(0.375, 0.45, '', transform=ax.transAxes )
        self.valid.set_text('Parameters violate the Energy Equation')
        return

    ''' Creates the object to draw the energy diagram '''
    def energy_Diagram(self):
        part = self.orbit.part
        bh = self.orbit.bh
        L, E2, M = part.L , part.E2, bh.M
        self.ED = self.fig.add_axes([0.025, 0.1, 0.8, 0.15])
        self.ED.set_xlabel('radius')
        self.ED.set_ylabel('E^2')
        self.ED.set_xlim((2*(M),10))
        self.V_pot, = self.ED.plot([], [], 'o-',lw=4 )
        ''' Verifies if rmax exists and set ylim as E2+1 or V(rmax)+1 '''
        if(pow(L,2)>12*pow(M,2)):
            lim_supy = max(E2+1,1 + part.V([0,part.rmax,0]))
            self.ED.set_ylim((0,lim_supy))
        else:
            self.ED.set_ylim((0,E2+1))
    '''Draws the potential, the energy lines '''
    def draw_ED(self):
        bh = self.orbit.bh
        part = self.orbit.part
        L, E2, M = part.L , part.E2, bh.M
        r_vec = np.linspace(2*M,10,500)
        self.potential_plot, = self.ED.plot([],[],color='b')
        self.energy_plot, = self.ED.plot([],[],color='r')
        self.rmax_plot, = self.ED.plot([],[],color='g')
        self.rmin_plot, = self.ED.plot([],[],color='y')
        if(pow(L,2)>12*pow(M,2)):
            r_vec = np.linspace(2*M,part.rmin + 1,500) #New limit if the minimum radius exists
        pot = []
        energ = []
        for i in range(0,len(r_vec)):
            pot = pot + [part.V([0,r_vec[i]])]
            energ = energ + [E2]
        self.potential_plot.set_data(r_vec,pot)
        self.energy_plot.set_data(r_vec,energ)
        if(pow(L,2)>12*pow(M,2)):
            self.ED.set_xlim((2*(M),part.rmin + 1))
            m = max(E2+1,1 + part.V([0,part.rmax,0]))
            energ_vec = np.linspace(0,m,2)
            rmax_vec = []
            rmin_vec = []
            for i in range(0,len(energ_vec)):
                rmax_vec = rmax_vec + [part.rmax]
                rmin_vec = rmin_vec + [part.rmin]
            self.rmax_plot.set_data(rmax_vec,energ_vec)
            self.rmin_plot.set_data(rmin_vec,energ_vec)
        return

#Resets the energy diagram for slider changes
    def ED_reset(self):
        bh = self.orbit.bh
        part = self.orbit.part
        self.rmax_plot.set_data([],[]) #avoid to plot max and min if thet don't exist
        self.rmin_plot.set_data([],[])
        L, E2, M = part.L , part.E2, bh.M
        lim_supx = max(10,part.rmin + 1)
        r_vec = np.linspace(2*M,lim_supx,20*lim_supx)
        pot = []
        energ = []
        for i in range(0,len(r_vec)):
            pot = pot + [part.V([0,r_vec[i]])]
            energ = energ + [E2]
        self.potential_plot.set_data(r_vec,pot)
        self.energy_plot.set_data(r_vec,energ)
        self.ED.set_xlim((2*(M),lim_supx))
        if(pow(L,2)>12*pow(M,2)):
            lim_supy = max(E2+1,1 + part.V([0,part.rmax,0]))
            self.ED.set_ylim((0,lim_supy))
            energ_vec = np.linspace(0,lim_supy,2)
            rmax_vec = []
            rmin_vec = []
            for i in range(0,len(energ_vec)):
                rmax_vec = rmax_vec + [part.rmax]
                rmin_vec = rmin_vec + [part.rmin]
            self.rmax_plot.set_data(rmax_vec,energ_vec)
            self.rmin_plot.set_data(rmin_vec,energ_vec)
        else:
            self.ED.set_ylim((0,E2+1))
        return

    '''Updates the text variable on the animation '''
    def update_orbit_text(self):
        bh = self.orbit.bh
        part = self.orbit.part
        ode = self.orbit.ode
        time = part.cv[0]
        tau = self.orbit.proper_time
        r = part.cv[1]
        phi = part.cv[2]
        X = part.cv
        drds = ode.F[1](part.cv,tau)
        self.Radius_text.set_text('r = %.3f' % r)
        self.Phi_text.set_text('Phi = %.3f ' % deg_to_rad(phi) )
        self.V_text.set_text('V(r) = %.3f' % part.V(X) )
        self.time_text.set_text('t = %.3f' % time )
        self.proper_time_text.set_text('tau = %.3f' % tau )
        self.drds_text.set_text('drds = %.7f' % drds )
        self.V_pot.set_data([r],[part.V(X)])
        return

#####################################################################################################
#Widgets to enhance user interacvity
    '''Create sliders to make inputs easier '''
    def sliders(self):
        part = self.orbit.part
        r0, phi0 = part.cv[1], part.cv[2]
        bh = self.orbit.bh
        self.E2_slider_ax = self.fig.add_axes([0.86, 0.94, 0.10, 0.03], facecolor = 'g')
        self.E2_slider =  Slider(self.E2_slider_ax, 'E^2', 0.0, 2*part.E2, valinit = part.E2)
        self.L_slider_ax = self.fig.add_axes([0.86, 0.90, 0.10, 0.03], facecolor = 'g')
        self.L_slider =  Slider(self.L_slider_ax, 'L', 0, 2*part.L, valinit = part.L)
        self.r0_slider_ax = self.fig.add_axes([0.86, 0.86, 0.10, 0.03], facecolor = 'g')
        self.r0_slider =  Slider(self.r0_slider_ax, 'r0', 2*bh.M, 10.0*r0, valinit = r0)
        self.phi0_slider_ax = self.fig.add_axes([0.86, 0.82, 0.10, 0.03], facecolor = 'g')
        self.phi0_slider =  Slider(self.phi0_slider_ax, 'phi0', 0, 360, valinit = phi0)
        self.scale_slider_ax = self.fig.add_axes([0.86, 0.50, 0.10, 0.03], facecolor = 'g')
        self.scale_slider =  Slider(self.scale_slider_ax, 'Scale', r0 + 2, 10*r0, valinit = 10.0)
        return

    '''Rescale the orbit plot '''
    def scale_change(self,val):
        lim = self.scale_slider.val
        self.ax.set_xlim((-lim,lim))
        self.ax.set_ylim((-lim,lim))
        return

    ''' Reset orbit variables when sliders are changed '''
    def sliders_update(self,val):
        self.redraw = True
        return

    def buttons(self):
        self.restart_button_ax = self.fig.add_axes([0.86, 0.75, 0.1, 0.04])
        self.restart_button = Button(self.restart_button_ax, 'Restart', color='w', hovercolor='0.975')
        self.direction_button_ax = self.fig.add_axes([0.86, 0.60, 0.1, 0.1], facecolor = 'w' )
        self.direction_button = RadioButtons(self.direction_button_ax, ('ingoing', 'outgoing'), active=0)
        return

    ''' Resets orbit to time zero  maintaining the current parameters '''
    def restart_button_click(self,mouse_event):
        self.redraw = True
        return

    ''' Chooses between ingoing and outgoing directions '''
    def dir_button_click(self,label):
        part = self.orbit.part
        if(label == 'outgoing'):
            part.signal_drds = 1.0
        else:
            part.signal_drds = -1.0
        self.redraw = True
        return

    def redraw_orbit(self,val):
        part = self.orbit.part
        ode = self.orbit.ode
        self.orbit.reverse = False
        part.reset_particle( self.E2_slider.val, self.L_slider.val, 0.0,  self.r0_slider.val,
                                         self.phi0_slider.val, self.orbit.part.signal_drds)
        f = [part.dtds,part.drds,part.dphids] #Rightside function
        ode.change_F(f)
        self.stop = False
        self.ED_reset()
        self.orbit.proper_time = self.orbit.part.cv[0]
        self.redraw = False
        return

#####################################################################################################
    ''' initialization function: plot the background of each frame
        Set the ODE we want to solve
        Returns the variables that need to be redrawn'''
    def init(self):
        self.draw_ED()
        self.orbit.part.body.center = (self.orbit.part.px, self.orbit.part.py)
        self.ax.add_patch(self.orbit.part.body)
        self.ax.add_artist(self.orbit.bh.body) #Draw the BH

        return  (self.orbit.part.body, self.Radius_text, self.Phi_text, self.V_text,
                self.V_pot, self.time_text , self.proper_time_text, self.orbit.part.trail,
                self.energy_plot,self.potential_plot,self.rmax_plot,self.rmin_plot,
                self.drds_text,)

    # animation function.  This is called sequentially
    #For each time t it evolves one step in the RK and use that value to draw
    #Return the variables that need to be redrawn
    ''' Dinamics of the animation
        Returns the variables that need to be redrawn'''

    def animate(self,t):
        part = self.orbit.part
        bh = self.orbit.bh
        E2 = self.orbit.part.E2
        h = self.orbit.ode.step_h
        '''restart and update orbit if any slider or button is pressed'''
        self.E2_slider.on_changed(self.sliders_update)
        self.L_slider.on_changed(self.sliders_update)
        self.r0_slider.on_changed(self.sliders_update)
        self.phi0_slider.on_changed(self.sliders_update)
        self.scale_slider.on_changed(self.scale_change)
        self.restart_button.on_clicked(self.restart_button_click)
        self.direction_button.on_clicked(self.dir_button_click)
        if(self.redraw == True):
            self.redraw_orbit(True)

        if( (part.E2 - part.V(part.cv) >= 0.0)  ):
            self.valid.set_visible(False)
            time = (self.orbit.proper_time)
            time = time + h
            if(self.stop == False):
                self.orbit.update_orbit(time*h)
                self.update_orbit_text()
            self.orbit.proper_time = time

            #Stop refreshing if we have a collision
            if((np.sqrt(pow(part.px,2)+pow(part.py,2))) <= 2*bh.M + part.plot_radius ):
                self.stop = True
        else:
            self.valid.set_visible(True)
            self.stop = True

        return  (self.orbit.part.body, self.Radius_text, self.Phi_text, self.V_text,
                self.V_pot, self.time_text , self.proper_time_text, self.orbit.part.trail,
                self.energy_plot,self.potential_plot,self.rmax_plot,self.rmin_plot,self.valid,
                self.drds_text,)


    ''' call the animator.  blit=True means only re-draw the parts that have changed'''
    def show_orbit(self):
        part = self.orbit.part
        E2 , X = part.E2, part.cv
        fig = self.fig
        animate = self.animate
        init = self.init
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                            frames=self.n_of_frames, interval=20, blit=True)
        plt.show()
        return
