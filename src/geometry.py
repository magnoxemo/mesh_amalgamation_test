import numpy as np
import matplotlib.pyplot as plt 
from math import *


class Zcylinder():
    
    def __init__(self,x0:float,y0:float,radius:float):
        """
        (x0,y0)---> center of the pincell. It is recomended that not putting the center at the origin which will break the mesh tracking script.  """
        self.x0=x0
        self.y0=y0
        self.r=radius
        self.tolerance=10**-6
        
    def particle_position_confirm(self,x,y):     
        ''' 
        this function will confirm that if the particle is with in the cylinder or outside of it.

        if val is negative--> then inside 
        if val is positive--> then outside
        if val=0 then on the surface.
        
        '''   
        val=(x-self.x0)**2+(y-self.y0)**2-self.r**2
        return val
    
    def plot_data(self):

        x=np.linspace(self.x0-self.r,self.x0+self.r,num=100)
        y=self.y0+np.sqrt(self.r*self.r-(x-self.x0)**2)

        return x,y,-y
    


        

class Plane():
    def __init__(self,a:float,b:float,c:float,d:float):
        '''
        rather than indiviual Xplane, Yplane I can create a class for the generalized plane.
        But I will have to put c=0 other wise it will crate a 3D surface.

        '''
        self.a=a
        self.b=b
        self.c=c
        self.d=d

    def particle_position_confirm(self,x,y):     
        ''' 
        this function will confirm that if the particle's side of the plane.

        if val is negative--> then right side of the plane
        if val is positive--> then left side
        if val=0 then on the plane.
        
        val=ax+by+cz-d

        please don't put both of the co-efficients (a,b) equal to zero :)
        '''   
        val=self.a*x+self.b*y-self.d
        return val
    
    def plot_data(self,min:float,max:float,color='blue'):

        '''
        min and max--> from min position to max position will be plotted 
        '''
        x=np.linspace(min,max,num=100)
        if self.b!=0:
            y=(self.d-self.a*x)/self.b
        elif (self.a!=0):
            y=x
            x=(self.d-self.b*y)/self.a

        return x,y 
    

        


class  Cell():
    def __init__(self,surface_array:list,indicator_array:list):
        """
           surface array will contain object of surface class.
           indicator array will contain logic like : insidegit,outside and on_the_surface. 
           the suface and the indicator array needs to be in the same order.     
        """
        self.surfaces=surface_array
        self.logic_array=indicator_array
        self.cell_id_number=self.logic_array_to_id_number()

    def logic_array_to_id_number(self):
        #id number will follow a three digit indicator 
        # 1 outside 
        # 0 inside and on the surface 
        id=[]
        for i in self.logic_array:
            if i=='inside' or i=='on_the_surface':
                id.append(0)
            elif i=='outside':
                id.append(1)

        return id 

    def particle_within_this_cell(self,r:list):

        ''' same as the def particle_position_confirm() method [that returns the positive, negative or zero value ] but this particle_within_this_cell function 
            can check inbetween different layers. I think when we do finally define the amalgamation region, from coding perspective I can treat them as a cell. 
            I will have to ask Paul about it.
            
            but what is the on the fly least_gradient_mesh_finder() finds only two mesh rather than a single layer? [#I need to code it first]
        '''
        x=r[0]
        y=r[1]
        #z=r[2] only 

        generated_id_number=[]

        for _ in self.surfaces:
            ''' searching all the '''
            if _.particle_position_confirm(x,y)<0 or _.particle_position_confirm(x,y)==0:
                generated_id_number.append(0)
            elif _.particle_position_confirm(x,y,z)>0:
                generated_id_number.append(1)

        """ 
        here we need a converter program which will tell us if the co ordinate is inside or outside 
        after reading the generated number 
        """
        if generated_id_number==self.cell_id_number:
            print("particle is found in this cell ") 
            return 1

        else:
            print("particle is not found in this cell ") 
            return 0
        

'''
cylinder=Zcylinder(x0=0,y0=0,radius=12)
x,y,y_=cylinder.plot_data()

plt.figure(figsize=(10,10))
plt.plot(x,y,color='red')
plt.plot(x,y_,color='red')
X_plane=Plane(a=1,b=0,c=0,d=12)
x,y=X_plane.plot_data(min=-10,max=10)
plt.plot(x,y,color='blue')
plt.show()  

'''

