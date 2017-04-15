import numpy as np
import ode
import schwarzschild as sch
import orbitas as orb
from auxiliar import max
import animator as anim

def main():
    (M,E2,L,t0,r0,phi0,signal_drds) = (0.1 , 2.0, 1.0, 0.0, 5.0, 180, -1.0)

    L = 3.5*M
    h = 0.1
    part = sch.particle(2.0, 1.0, 0.0, 5.0, 180, -1.0)
    f = [part.dtds,part.drds,part.dphids] #Rightside function
    bh = sch.blackhole(M)
    ODE = ode.ode(f,h,r0,t0,1.0)
    orbit = orb.orbit(part,bh,ODE,10)
    ani = anim.orbit_animation(orbit,10)
    ani.show_orbit()
    return

main()
