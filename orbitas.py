import numpy as np
import ode
import schwarzschild as sch


#Class which contain the orbit structure and the position recalculation method
class orbit:
    def __init__(self,part,bh,ode):
        self.part = part
        self.bh = bh
        self.ode = ode
        self.proper_time = part.cv[0] #global iterator
        return

    def update_orbit(self,time):
        rev_radius = self.part.cv[1]
        self.part.update_pos(self.ode,self.proper_time)
        if( (self.part.E2 - self.part.V(self.part.cv) <= 0) ):
            if(self.ode.F[1].__name__ == 'drds'):
                f = [self.part.dtds,self.part.mdrds,self.part.dphids] #Rightside function
            else:
                f = [self.part.dtds,self.part.drds,self.part.dphids] #Rightside function
            self.ode.change_F(f)
            self.part.cv[1] = rev_radius
        self.part.body.center = (self.part.px,self.part.py)
        self.part.trail.set_data(self.part.trail_pos_x,self.part.trail_pos_y)
        return
