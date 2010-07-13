import numpy as nu
import galpy.util.bovy_plot as plot
from Potential import PotentialError
class linearPotential:
    """Class representing 1D potentials"""
    def __init__(self,amp=1.):
        self._amp= amp
        self.dim= 1
        return None

    def __call__(self,x):
        """
        NAME:
           __call__
        PURPOSE:
           evaluate the potential
        INPUT:
           x
        OUTPUT:
           Phi(x)
        HISTORY:
           2010-07-12 - Written - Bovy (NYU)
        """
        try:
            return self._amp*self._evaluate(x)
        except AttributeError:
            raise PotentialError("'_evaluate' function not implemented for this potential")

    def force(self,x):
        """
        NAME:
           force
        PURPOSE:
           evaluate the force
        INPUT:
           x
        OUTPUT:
           F(x)
        HISTORY:
           2010-07-12 - Written - Bovy (NYU)
        """
        try:
            return self._amp*self._force(x)
        except AttributeError:
            raise PotentialError("'_force' function not implemented for this potential")

    def plot(self,min=-15.,max=15,ns=21,savefilename=None):
        """
        NAME:
           plot
        PURPOSE:
           plot the potential
        INPUT:
           min - minimum x
           max - maximum x
           ns - grid in x
           savefilename - save to or restore from this savefile (pickle)
        OUTPUT:
           plot to output device
        HISTORY:
           2010-07-13 - Written - Bovy (NYU)
        """
        if not savefilename == None and os.path.exists(savefilename):
            print "Restoring savefile "+savefilename+" ..."
            savefile= open(savefilename,'rb')
            potx= pickle.load(savefile)
            xs= pickle.load(savefile)
            savefile.close()
        else:
            xs= nu.linspace(min,max,ns)
            potx= nu.zeros(ns)
            for ii in range(ns):
                potx[ii]= self._evaluate(xs[ii])
            if not savefilename == None:
                print "Writing savefile "+savefilename+" ..."
                savefile= open(savefilename,'wb')
                pickle.dump(potx,savefile)
                pickle.dump(xs,savefile)
                savefile.close()
        return plot.bovy_plot(xs,potx,
                              xlabel=r"$x/x_0$",ylabel=r"$\Phi(x)$",
                              xrange=[min,max])
    
def evaluatePotentials(x,Pot):
    """
    NAME:
       evaluatePotentials
    PURPOSE:
       evaluate the sum of a list of potentials
    INPUT:
       x - evaluate potentials at this position
       Pot - (list of) linearPotential instance(s)
    OUTPUT:
       pot(x)
    HISTORY:
       2010-07-13 - Written - Bovy (NYU)
    """
    if isinstance(Pot,list):
        sum= 0.
        for pot in Pot:
            sum+= pot(x)
        return sum
    elif isinstance(Pot,linearPotential):
        return Pot(x)
    else:
        raise PotentialError("Input to 'evaluatePotentials' is neither a linearPotential-instance or a list of such instances")

def evaluateForces(x,Pot):
    """
    NAME:
       evaluateForces
    PURPOSE:
       evaluate the forces due to a list of potentials
    INPUT:
       x - evaluate forces at this position
       Pot - (list of) linearPotential instance(s)
    OUTPUT:
       force(x)
    HISTORY:
       2010-07-13 - Written - Bovy (NYU)
    """
    if isinstance(Pot,list):
        sum= 0.
        for pot in Pot:
            sum+= pot.force(x)
        return sum
    elif isinstance(Pot,linearPotential):
        return Pot.force(x)
    else:
        raise PotentialError("Input to 'evaluateForces' is neither a linearPotential-instance or a list of such instances")

def plotPotentials(Pot,min=-15.,max=15,ns=21,savefilename=None):
    """
    NAME:
       plotPotentials
    PURPOSE:
       plot a combination of potentials
    INPUT:
       min - minimum x
       max - maximum x
       ns - grid in x
       savefilename - save to or restore from this savefile (pickle)
    OUTPUT:
       plot to output device
    HISTORY:
       2010-07-13 - Written - Bovy (NYU)
    """
    if not savefilename == None and os.path.exists(savefilename):
        print "Restoring savefile "+savefilename+" ..."
        savefile= open(savefilename,'rb')
        potx= pickle.load(savefile)
        xs= pickle.load(savefile)
        savefile.close()
    else:
        xs= nu.linspace(min,max,ns)
        potx= nu.zeros(ns)
        for ii in range(ns):
            potx[ii]= evaluatePotentials(xs[ii],Pot)
        if not savefilename == None:
            print "Writing savefile "+savefilename+" ..."
            savefile= open(savefilename,'wb')
            pickle.dump(potx,savefile)
            pickle.dump(xs,savefile)
            savefile.close()
    return plot.bovy_plot(xs,potx,
                          xlabel=r"$x/x_0$",ylabel=r"$\Phi(x)$",
                          xrange=[min,max])

