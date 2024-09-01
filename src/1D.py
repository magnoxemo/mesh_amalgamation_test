import numpy as np
import matplotlib.pyplot as plt


def slab_source(Nx,Sig_s,Sig_a,thickness,N,Q,isotropic=False, implicit_capture = True):
     

    '''this code is adapted from Computational Nuclear Engineering and Radiological Science Using Python book '''

    dx = thickness/Nx
    X = np.linspace(dx*0.5, thickness - 0.5*dx,Nx)
    scalar_flux = np.zeros(Nx)
    scalar_flux_tl = np.zeros(Nx)
    Sig_t = Sig_a + Sig_s
    leak_left = 0.0
    leak_right = 0
    N = int(N)
    for i in range(N):
        if (isotropic):
            mu = np.random.uniform(-1,1,1)
        else:
            mu = 1.0
        x = np.random.random(1)*thickness
        alive = 1
        weight = Q*thickness/N
        #which cell am I in
        cell = np.argmin(np.abs(X-x))
        while (alive):
            if (implicit_capture):
                #get distance to collision
                if (Sig_s > 0):
                    l = -np.log(1-np.random.random(1))/Sig_s 
                else:
                    l = 10.0*thickness/np.abs(mu) #something that will make it through
            else:
                #get distance to collision
                l = -np.log(1-np.random.random(1))/Sig_t
            #compare distance to collision to distance to cell edge
            distance_to_edge = ((mu > 0.0)*( (cell+1)*dx - x) + 
                                (mu<0.0)*( x - cell*dx) + 1.0e-8)/np.abs(mu)
            if (distance_to_edge < l):
                l = distance_to_edge
                collide = 0
            else:
                collide = 1
            #move particle
            x += l*mu
            #score track length tally
            if (implicit_capture):
                scalar_flux_tl[cell] += weight*(1.0 - np.exp(-l*Sig_a))/(Sig_a + 1.0e-14)
            else:
                scalar_flux_tl[cell] += weight*l
            if (implicit_capture):
                if not(l>=0):
                    print(l,x,mu,cell,distance_to_edge)
                assert(l>=0)
                weight_old = weight
                weight *= np.exp(-l*Sig_a)
            #still in the slab?
            if (np.abs(x-thickness) < 1.0e-14) or (x > thickness):
                leak_right += weight
                alive = 0
            elif (x<= 1.0e-14):
                alive = 0
                leak_left += weight
            else:
                #compute cell particle collision is in
                cell= np.argmin(np.abs(X-x))
                if (implicit_capture):
                    if (collide):
                        mu = np.random.uniform(-1,1,1)
                    scalar_flux[cell] += weight/Sig_s/dx
                else:
                    #scatter or absorb
                    scalar_flux[cell] += weight/Sig_t/dx
                    if (collide) and (np.random.random(1) < Sig_s/Sig_t): 
                        #scatter, pick new mu
                        mu = np.random.uniform(-1,1,1)
                    elif (collide): #absorbed
                        alive = 0
            #print(x,mu,alive,l*mu,weight*l)
    return scalar_flux, scalar_flux_tl/dx, X


flux,flux1,x=(slab_source(100,Sig_s=1,Sig_a=.1,thickness=3,N=1000,Q=1,isotropic=True,implicit_capture=True))
plt.figure(figsize=(10,10))
plt.plot(x,flux)
plt.show()


