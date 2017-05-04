import numpy as np

def exmaker():
    M = 0.1
    L2 = float(input('L2 = '))
    L = np.sqrt(L2)
    E2 = 2.00
    r0 = 0.60
    if(L2>12*pow(M,2)):
        rmax = (L2 - L*np.sqrt(L2-12*pow(M,2)))/(2*M) #argmax(V)
        rmin = (L2 + L*np.sqrt(L2-12*pow(M,2)))/(2*M) #argmin local(V)
        Vmax = (1 +  pow(L/rmax,2))*(1 - (2*M/rmax))
        Vmin = (1 +  pow(L/rmin,2))*(1 - (2*M/rmin))
        V = (1 +  pow(L/r0,2))*(1 - (2*M/r0))
        print('rmax = ',rmax)
        print('rmin = ',rmin)
        print('Vmax = ',Vmax)
        print('Vmin = ',Vmin)
        print('L = ',L)
        print('drts2 = ', E2 - V )
    return

if __name__ == "__main__":
    exmaker()
