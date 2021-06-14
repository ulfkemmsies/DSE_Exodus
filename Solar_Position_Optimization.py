"""
Created on Fri May 28 2021

@author: Ernesto Hof
"""

#importing packages
import numpy as np
import matplotlib.pyplot as plt
from commondata import CommonData
import math as m

class PVArrays():
    def __init__(self):
        # Importing the commondata file
        self.data = CommonData()

        self.longest_illumination = 233 #days
        self.longest_darkness = 4.5 #days
        self.design_longest_darkness = 8 #days
        self.illumination_2m = 88 #percent of lunar year
        self.illumination_10m = 92 #percent of lunar year

        self.tower_height = 10 #m
        self.tower_width = 2 #m
        self.ground_clearance = 2 #m
        self.outer_support_beam_thickness = 20 #mm
        self.inner_support_beam_thickness = 10 #mm
        self.support_material_density = 2810 #kg/m3

        self.cable_density = 5  #kg/m

        self.voltage_required = 600 #V DC

        self.power_required_nominal = 20 #kW
        self.power_required_manufacturing = 75 #kW
        self.power_required = max(self.power_required_nominal,self.power_required_manufacturing)

        self.distance_landing_habitat = 1.9 #km
        self.distance_habitat_solar = 1.9 #km
        self.actual_distance_landing_habitat = 2.5 #km\

    def shadow(self,maxmin):
        self.inclination = np.deg2rad(5)  # radians
        #maxmin is false when the minimum solar inclination is required
        if maxmin == 'min':
            self.inclination = np.deg2rad(0.01)  # radians
        self.shadow_radius = self.tower_height/np.tan(self.inclination)
        self.shadow_diameter = 2*self.shadow_radius
        self.shadow_area = np.pi*self.shadow_radius**2

        print("Radius of solar tower shadow cone: ", self.shadow_radius, "m")

    def power(self, inclination):
        #if inclination is true, this means the solar arrays are inclined to receive perpendicular solar rays
        self.area_per_tower = (self.tower_height-self.ground_clearance)*self.tower_width
        if inclination == True:
            self.area_required = self.power_required*1000/(self.data.moon__solar_constant*
                                                      self.data.solar__cell_absorptivity*0.01*self.data.solar__cell_avg_efficiency_bol)
            self.number_of_towers = m.ceil(self.area_required/self.area_per_tower)
            self.power_per_tower = self.area_per_tower*self.data.moon__solar_constant*\
                            self.data.solar__cell_absorptivity*0.01*self.data.solar__cell_avg_efficiency_bol

        else:
            self.area_required = self.power_required*1000/(self.data.moon__solar_constant*
            self.data.solar__cell_absorptivity*0.01*self.data.solar__cell_avg_efficiency_bol*np.cos(self.inclination))

            self.number_of_towers = m.ceil(self.area_required/self.area_per_tower)
            self.power_per_tower = self.area_per_tower * self.data.moon__solar_constant*\
                            self.data.solar__cell_absorptivity * 0.01 * self.data.solar__cell_avg_efficiency_bol*np.cos(self.inclination)

        self.total_power = self.number_of_towers*self.power_per_tower

        print("Total area needed: ",self.area_required, "m2")
        print("Total number of towers: ", self.number_of_towers)
        print("Power produced per tower: ", self.power_per_tower, "W")
        print("Total power produced: ", self.total_power, "W")


    def gridfinding(self, numberoftowers):
        self.grid = [0,0]
        self.current_min = 2*self.shadow_radius*(self.number_of_towers+1)*self.shadow_radius
        for i in range(1,numberoftowers+1):
            N = i
            M = numberoftowers/i
            if M.is_integer()==True:
                self.area = (N+1)*self.shadow_radius*(M+1)*self.shadow_radius
                #print(self.area)
                #print(N,"x", M)
            if self.area < self.current_min:
                self.current_min = self.area
                self.grid = [int(N),int(M)]
        return self.grid, self.area

    def optimallayout(self):
        self.grid = self.gridfinding(self.number_of_towers)[0]
        if sum(self.grid)==0:
            self.grid1, areacheck1 = self.gridfinding(self.number_of_towers+1)
            self.grid2, areacheck2 = self.gridfinding(self.number_of_towers-1)
            if areacheck1<areacheck2:
                self.grid1 = self.grid
            else:
                self.grid2 = self.grid
            # residual gives how much towers you are missing or have too much in the current grid, so if its negative
            # it means your current grid contains too few towers compared to the number you need for your power requirement
            self.residual = self.grid[0]*self.grid[1]-self.number_of_towers


    def towerposition(self):
        self.xboundary = -0.5*(self.grid[1]-1)*self.shadow_radius
        self.yboundary = 0.5*(self.grid[0]-1)*self.shadow_radius
        self.xcoordinates = [self.xboundary]
        self.ycoordinates = [self.yboundary]
        self.coordinates = []
        for i in range(self.grid[1]-1):
            self.xcoordinates.append(self.xcoordinates[i]+self.shadow_radius)
        for j in range(self.grid[0]-1):
            self.ycoordinates.append(self.ycoordinates[j]-self.shadow_radius)
        for k in range(len(self.ycoordinates)):
            for n in range(len(self.xcoordinates)):
                self.coordinates.append([self.xcoordinates[n],self.ycoordinates[k]])
        if self.residual < 0:
            towerdirection = min(self.grid[0],self.grid[1])

    def PVelectricalsetup(self):
        self.number_of_cells_x = m.floor(self.tower_width/(self.data.solar__cell_xdimension/1000))
        self.number_of_cells_y = m.floor((self.tower_height-self.ground_clearance)/(self.data.solar__cell_ydimension/1000))
        self.total_number_of_cells = self.number_of_cells_x*self.number_of_cells_y

        self.number_of_cells_series = self.voltage_required/(self.data.solar__cell_maxpower_voltage_bol/1000)
        self.number_of_cells_series = m.ceil(self.number_of_cells_series)
        self.voltage_supply = self.number_of_cells_series*self.data.solar__cell_maxpower_voltage_bol/1000

        self.number_of_cells_parallel = m.floor(self.total_number_of_cells/self.number_of_cells_series)
        self.current_supply = self.number_of_cells_parallel*self.data.solar__cell_maxpower_current_bol/1000

        self.actual_number_of_cells = self.number_of_cells_parallel*self.number_of_cells_series
        self.actual_cell_width = self.number_of_cells_x*self.data.solar__cell_xdimension/1000
        self.actual_cell_height = (self.actual_number_of_cells/self.number_of_cells_x)*self.data.solar__cell_ydimension/1000

        print("Total number of solar cells per tower: ", self.actual_number_of_cells)
        print("Voltage supply per tower: ", self.voltage_supply, "V")
        print("Current supply per tower: ", self.current_supply, "A")

    def cablelength(self):
        length = 0
        for i in range(len(self.coordinates)):
            length += (self.coordinates[i][0] ** 2 + self.coordinates[i][1] ** 2) ** (0.5)
        self.cable_weight = length * self.cable_density
        print("Total High-Power cable length: ", length, " m")
        print("Total cable weight: ", self.cable_weight, "kg")

    def PVmass(self):
        self.cell_weight = self.data.solar__cell_area*self.data.solar__average_cell_weight/1000

        self.tower_cell_weight= self.actual_number_of_cells*self.cell_weight/1000
        self.outer_support_weight = (2*self.actual_cell_width*(self.outer_support_beam_thickness/1000)**2\
        +2*self.actual_cell_height*(self.outer_support_beam_thickness/1000)**2)*self.support_material_density
        print(self.outer_support_weight)


    def plotting(self):
        fig,ax = plt.subplots()
        for i in range(len(self.coordinates)):
            plt.plot(self.coordinates[i][0],self.coordinates[i][1],'c',marker="X", ms=10)
            plt.plot([self.coordinates[i][0],0],[self.coordinates[i][1],0],'b')

        #circle = plt.Circle((self.coordinates[0][0], self.coordinates[0][1]),
                            #self.shadow_radius, color='gray', label='Shadow Cone')
        #ax.add_patch(circle)
        plt.plot(0,0,'r',marker="H", ms=25, label="Habitat")
        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.title("Solar Tower Grid (Habitat in Origin)")
        plt.legend(loc='best')
        plt.show()
        plt.close()

    def runprogram(self,maxmin,inclination):
        self.shadow(maxmin)
        self.power(inclination)
        self.optimallayout()
        self.towerposition()
        self.cablelength()
        self.plotting()
        self.PVelectricalsetup()
        self.PVmass()

Test = PVArrays()
Test.runprogram('max',False)