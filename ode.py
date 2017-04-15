import numpy as np
import auxiliar as aux

'''Library to solve X' = F(X) using'''

#Returns the evaluated vector of a list of functions
ev = aux.ev

#******************************************************************************#

# ODE finite difference variables#
class ode:
    """ Sets the initial conditions and functions for the Ode """
    def __init__(self,f,h,x0,T0,TF):
        self.F, self.step_h, self.n_eq = f, h, len(f)
        self.X0, self.t0, self.tf = x0, T0, TF
        return

    """Changes the ODE Rightside without changing the rest of the ODE"""
    def change_F(self,f):
        if(len(f) != self.n_eq ):
            self.F = f
            return

    """Calculates x_(n+1) using the Runge-Kutta method
    np.multiply multiplies an array by an float value
    To sum two arrays we need the np.add functions, so we need extra careful"""
    def RK_step(self,X,t):
        #Runge-Kutta F's
        F, h = self.F, self.step_h
        F1 = ev(F,X,t)
        F2 = ev(F, np.add(X, np.multiply(F1,h/2.0)), t + (h/2.0))
        F3 = ev(F, np.add(X, np.multiply(F2,h/2.0)), t + (h/2.0))
        F4 = ev(F, np.add(X, np.multiply(F3,h)), t + (h))
        A = np.add(np.add(np.add(F1, np.multiply(F2,2.0)), np.multiply(F3,2.0)),F4)
        return  np.add(X, np.multiply(A,h/6.0))

    """Solves the ODE using Runge-Kutta Method
    It returns a list which each the n-th element is X_n
    We don't need this on the Orbitas program"""
    def RK(self):
        Tf, T0, X0, h = self.tf, self.t0, self.X0, self.step_h
        y = np.array([X0])
        N = int((Tf-T0)/h)
        X = X0
        for i in range(0,N):
            X = Ode.RK_step(X,i*h)
            y = np.append(y,[X],axis = 0)
        return y
