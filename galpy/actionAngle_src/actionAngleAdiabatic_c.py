import os
import ctypes
import ctypes.util
import numpy
from numpy.ctypeslib import ndpointer
from galpy import potential, potential_src
from galpy.orbit_src.integrateFullOrbit import _parse_pot
#Find and load the library
_lib = None
_libname = ctypes.util.find_library('galpy_actionAngle_c')
if _libname:
    _lib = ctypes.CDLL(_libname)
if _lib is None:
    import sys
for path in sys.path:
    try:
        _lib = ctypes.CDLL(os.path.join(path,'galpy_actionAngle_c.so'))
    except OSError:
        _lib = None
    else:
        break
if _lib is None:
    raise IOError('galpy actionAngle_c module not found')

def actionAngleAdiabatic_c(pot,gamma,R,vR,vT,z,vz):
    """
    NAME:
       actionAngleAdiabatic_c
    PURPOSE:
       Use C to calculate actions using the adiabatic approximation
    INPUT:
       pot - Potential or list of such instances
       gamma - as in Lz -> Lz+\gamma * J_z
       R, vR, vT, z, vz - coordinates (arrays)
    OUTPUT:
       (jr,jz,err)
       jr,jz : array, shape (len(R))
       err - non-zero if error occured
    HISTORY:
       2012-12-10 - Written - Bovy (IAS)
    """
    #Parse the potential
    npot, pot_type, pot_args= _parse_pot(pot)

    #Set up result arrays
    jr= numpy.empty(len(R))
    jz= numpy.empty(len(R))
    err= ctypes.c_int(0)

    #Set up the C code
    ndarrayFlags= ('C_CONTIGUOUS','WRITEABLE')
    actionAngleAdiabatic_actionsFunc= _lib.actionAngleAdiabatic_actions
    actionAngleAdiabatic_actionsFunc.argtypes= [ctypes.c_int,
                                                ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                                                ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                                                ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                                                ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                                                ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                                                ctypes.c_int,
                                                ndpointer(dtype=numpy.int32,flags=ndarrayFlags),
                                                ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                                                ctypes.c_double,
                                                ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                                                ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                                                ctypes.POINTER(ctypes.c_int)]

    #Array requirements, first store old order
    f_cont= [R.flags['F_CONTIGUOUS'],
             vR.flags['F_CONTIGUOUS'],
             vT.flags['F_CONTIGUOUS'],
             z.flags['F_CONTIGUOUS'],
             vz.flags['F_CONTIGUOUS']]
    R= numpy.require(R,dtype=numpy.float64,requirements=['C','W'])
    vR= numpy.require(vR,dtype=numpy.float64,requirements=['C','W'])
    vT= numpy.require(vT,dtype=numpy.float64,requirements=['C','W'])
    z= numpy.require(z,dtype=numpy.float64,requirements=['C','W'])
    vz= numpy.require(vz,dtype=numpy.float64,requirements=['C','W'])
    jr= numpy.require(jr,dtype=numpy.float64,requirements=['C','W'])
    jz= numpy.require(jz,dtype=numpy.float64,requirements=['C','W'])

    #Run the C code
    actionAngleAdiabatic_actionsFunc(len(R),
                                     R,
                                     vR,
                                     vT,
                                     z,
                                     vz,
                                     ctypes.c_int(npot),
                                     pot_type,
                                     pot_args,
                                     ctypes.c_double(gamma),
                                     jr,
                                     jz,
                                     ctypes.byref(err))

    #Reset input arrays
    if f_cont[0]: R= numpy.asfortranarray(R)
    if f_cont[1]: vR= numpy.asfortranarray(vR)
    if f_cont[2]: vT= numpy.asfortranarray(vT)
    if f_cont[3]: z= numpy.asfortranarray(z)
    if f_cont[4]: vz= numpy.asfortranarray(vz)

    return (jr,jz,err.value)

def actionAngleStaeckel_calcu0(E,Lz,pot,delta):
    """
    NAME:
       actionAngleStaeckel_calcu0
    PURPOSE:
       Use C to calculate u0 in the Staeckel approximation
    INPUT:
       E, Lz - energy and angular momentum
       pot - Potential or list of such instances
       delta - focal length of prolate spheroidal coordinates
    OUTPUT:
       (u0,err)
       u0 : array, shape (len(E))
       err - non-zero if error occured
    HISTORY:
       2012-12-03 - Written - Bovy (IAS)
    """
    #Parse the potential
    npot, pot_type, pot_args= _parse_pot(pot)

    #Set up result arrays
    u0= numpy.empty(len(E))
    err= ctypes.c_int(0)

    #Set up the C code
    ndarrayFlags= ('C_CONTIGUOUS','WRITEABLE')
    actionAngleStaeckel_actionsFunc= _lib.calcu0
    actionAngleStaeckel_actionsFunc.argtypes= [ctypes.c_int,
                               ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                               ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                               ctypes.c_int,
                               ndpointer(dtype=numpy.int32,flags=ndarrayFlags),
                               ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                               ctypes.c_double,
                               ndpointer(dtype=numpy.float64,flags=ndarrayFlags),
                               ctypes.POINTER(ctypes.c_int)]

    #Array requirements, first store old order
    f_cont= [E.flags['F_CONTIGUOUS'],
             Lz.flags['F_CONTIGUOUS']]
    E= numpy.require(E,dtype=numpy.float64,requirements=['C','W'])
    Lz= numpy.require(Lz,dtype=numpy.float64,requirements=['C','W'])
    u0= numpy.require(u0,dtype=numpy.float64,requirements=['C','W'])

    #Run the C code
    actionAngleStaeckel_actionsFunc(len(E),
                                    E,
                                    Lz,
                                    ctypes.c_int(npot),
                                    pot_type,
                                    pot_args,
                                    ctypes.c_double(delta),
                                    u0,
                                    ctypes.byref(err))

    #Reset input arrays
    if f_cont[0]: E= numpy.asfortranarray(E)
    if f_cont[1]: Lz= numpy.asfortranarray(Lz)

    return (u0,err.value)
