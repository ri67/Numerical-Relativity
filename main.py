import numpy as np
import ode
import schwarzschild as sch
import orbitas as orb
from auxiliar import max
from auxiliar import inlist as inlist
import animator as anim
import time

'''Given the initial conditions generates the animation for the orbit path '''
def play(E2 = 2.0, L = 0.75, r0 = 1.0, M = 0.1,t0 = 0.0 ,signal_drds = -1.0, phi0 = 0.0):
    h = 0.005
    part = sch.particle(E2,L,t0,r0,phi0,signal_drds)
    if(E2 - part.V([t0,r0,phi0]) >= 0.0):
        f = [part.dtds,part.drds,part.dphids] #Rightside function
        bh = sch.blackhole(M)
        ODE = ode.ode(f,h,r0,t0,1.0)
        orbit = orb.orbit(part,bh,ODE)
        ani = anim.orbit_animation(orbit,10)
        ani.show_orbit()
    else:
        print('Error! Values violate the energy equation!')
    return

def messages():
    print('Welcome! Type \'help\' to see the commands!')
    print('Type exit if you want to exit')
    return

def help_message():
    print('Commands available: exit, examples,help,input')
    print('In examples, type the number of the orbit you want to see ')
    print('In input,type the value you want for the following variables:')
    print('[E2 = 2.0, L = 0.75, r0 = 1.0, M = 0.1,t0 = 0.0 ,signal_drds = -1.0, phi0 = 0.0]')
    print('where the default is specified on the rightside of the equalities')
    return

def examples():
    ex_list = ['1','1a','2','3','4','5','6','7','8','9','10','11','12']
    print('Types of orbits: Bound orbit - B), Crash orbit - C), Escape orbit - E), Flyby - F)')
    print('After the number we display the type with ingoing and outgoing, always starting with ingoing')
    print('M = 0.1, phi0 = 0, t0 = 0')

    '''Case I)L² < 12M²'''
    #a)E² < 1
    print('1: C/C) E2 = 0.90, L = 0.316, r0 = 0.30 ')
    #b)E² >= 1
    print('2: C/E) E2 = 2.00, L = 0.316, r0 = 2.00 ')

    '''Case II) 12M² < L² < 16M² '''
    #a)E² < V(rmax) , r0 < rmax
    print('3: C/C) E2 = 0.895, L = 0.3535, r0 = 0.40 ')
    #b)V(rmin)< E² < V(rmax), r0 > rmax
    print('4: B/B) E2 = 0.91, L = 0.3605, r0 = 0.60 ')
    #c)V(rmax)< E²
    print('5: C/C) E2 = 0.95, L = 0.3605, r0 = 0.60 ')
    #d)E² >= 1
    print('6: C/E) E2 = 2.00, L = 0.3872, r0 = 0.60 ')

    print('1: F) E2 = 2.00, L = 1.00, r0 = 1.00')
    print('2: C) E2 = 0.90, L = 0.32, r0 = 0.30')

    val = input('Type the orbit number:')
    print(val)
    while(not inlist(val,ex_list)):
        val = input('Error!Type a valid example number:')

    if(val == '1'):
        play(0.90,0.316,.30)
    if(val == '1a'):
        play(0.90,0.1,.30)
    if(val == '2'):
        play(2.00,0.316,2.00)
    if(val == '3'):
        play(0.895,0.3535,0.40)
    if(val == '4'):
        play(0.91,0.3605,0.60)
    if(val == '5'):
        play(0.95,0.3605,0.60)
    if(val == '6'):
        play(2.00,0.3872,0.60)


    else:
        return
    return

def main():
    done = False
    messages()
    while(not done):
        word = input('cmd:')
        while( (word != 'examples') and (word != 'exit') and (word != 'help') and (word != 'input') ):
                print('Error! Unknown command! Type \'help\' to see the commands!')
                word = input('cmd:')
        if(word == 'help'):
            help_message()
        if(word == 'examples'):
            examples()
        if(word == 'exit'):
            done = True
    return

if __name__ == "__main__":
    main()
