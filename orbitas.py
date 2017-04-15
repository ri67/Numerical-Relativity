import numpy as np
import ode
import schwarzschild as sch
#******************************************************************************#

# Class that creates the animation #
class orbit:
    def __init__(self,part,bh,ode,lim):
        self.part = part
        self.bh = bh
        self.ode = ode
        self.time = 0 #global iterator
        return

    def update_orbit(self,time):
        Rev_rad = self.part.cv[1] #makes the orbit go back one radius value if energy bound has been reached
        self.part.update_pos(self.ode,self.time)
        if( (self.part.E2 - self.part.V(self.part.cv) <= 0.01)  ):
            f = [self.part.dtds,self.part.mdrds,self.part.dphids] #Rightside function
            self.ode.change_F(f)
            self.part.cv[1] = Rev_rad
        self.part.body.center = (self.part.px,self.part.py)
        self.part.trail.set_data(self.part.trail_pos_x,self.part.trail_pos_y)
        return
