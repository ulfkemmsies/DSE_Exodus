"""
Created on Fri May 28 2021

@author: Ernesto Hof
"""

#importing packages
import numpy as np
import matplotlib.pyplot as plt
from commondata import CommonData

class PVArrays():
    def __init__(self):
        # Importing the commondata file
        self.data = CommonData()

        self.inclination_min = np.deg2rad(0.01) #radians
        self.inclination_max = np.deg2rad(5) #radians
        self.longest_illumination = 233 #days
        self.longest_darkness = 4.5 #days
        self.design_longest_darkness = 8 #days
        self.illumination_2m = 88 #percent of lunar year
        self.illumination_10m = 92 #percent of lunar year

        self.tower_height = 10 #m
        self.number_of_towers = 100
        self.tower_panel_area = self.data.solar__maximum_area/self.number_of_towers
        print("Total number of solar towers: ", self.number_of_towers)
        print("Height of each solar tower: ", self.tower_height)
        print("Solar panel area per tower: ", round(self.data.solar__maximum_area/self.number_of_towers,4), "m2")

        self.voltage_required = 124.5 #V DC

    def shadow(self):
        self.shadow_radius_min = self.tower_height/np.tan(self.inclination_max)
        self.shadow_radius_max = self.tower_height/np.tan(self.inclination_min)
        self.shadow_diameter_min = 2*self.shadow_radius_min
        self.shadow_diameter_max = 2*self.shadow_radius_max
        self.shadow_area_min = np.pi*self.shadow_radius_min**2
        self.shadow_area_max = np.pi*self.shadow_radius_max**2

        print("Radius of solar tower shadow cone: ", self.shadow_radius_min, "m")

    def power(self):
        self.power_vertical = self.data.moon__solar_constant*self.data.solar__maximum_area*0.01*self.data.solar__cell_avg_efficiency_bol\
        *self.data.solar__cell_absorptivity*np.cos(self.inclination_max)
        self.power_rotated = self.power_vertical/np.cos(self.inclination_max)
        self.power_per_tower_vertical = self.power_vertical/self.number_of_towers
        self.power_per_tower_rotated = self.power_rotated/self.number_of_towers

        print("Power produced per tower without inclining the solar panels: ",
              round((self.power_vertical/self.number_of_towers)/1000,4), "kW")
        print("Total power produced without inclining the solar panels: ",
              round(self.power_vertical / 1000, 4), "kW")
        print("Power produced per tower with inclination mechanism in place: ",
              round((self.power_rotated/self.number_of_towers)/1000,4), "kW")
        print("Total power produced with inclination mechanism in place: ",
              round(self.power_rotated/1000,4), 'kW')

    def optimallayout(self):
        #self.shadow()
        self.current_min = 2*self.shadow_radius_min*(self.number_of_towers+1)*self.shadow_radius_min
        for i in range(1,self.number_of_towers+1):
            N = i
            M = self.number_of_towers/i
            if M.is_integer()==True:
                self.area = (N+1)*self.shadow_radius_min*(M+1)*self.shadow_radius_min
                #print(self.area)
                #print(N,"x", M)
            if self.area < self.current_min:
                self.current_min = self.area
                self.grid = [int(N),int(M)]

    def towerposition(self):
        #self.optimallayout()
        self.xboundary = -0.5*(self.grid[1]-1)*self.shadow_radius_min
        self.yboundary = 0.5*(self.grid[0]-1)*self.shadow_radius_min
        self.xcoordinates = [self.xboundary]
        self.ycoordinates = [self.yboundary]
        self.coordinates = []
        for i in range(self.grid[1]-1):
            self.xcoordinates.append(self.xcoordinates[i]+self.shadow_radius_min)
        for j in range(self.grid[0]-1):
            self.ycoordinates.append(self.ycoordinates[j]-self.shadow_radius_min)
        for k in range(len(self.ycoordinates)):
            for n in range(len(self.xcoordinates)):
                self.coordinates.append([self.xcoordinates[n],self.ycoordinates[k]])

    def cablelength(self):
        #self.towerposition()
        length = 0
        for i in range(len(self.coordinates)):
            length += (self.coordinates[i][0]**2+self.coordinates[i][1]**2)**(0.5)
        print("Total High-Power cable length: ", length, " m")

    def plotting(self):
        #self.shadow()
        #self.power()
        #self.optimallayout()
        #self.towerposition()
        #self.cablelength()
        fig,ax = plt.subplots()
        for i in range(len(self.coordinates)):
            plt.plot(self.coordinates[i][0],self.coordinates[i][1],'c',marker="X", ms=10)
            plt.plot([self.coordinates[i][0],0],[self.coordinates[i][1],0],'b')

        plt.plot(0,0,'r',marker="H", ms=25, label="Habitat")
        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.title("Solar Tower Grid (Habitat in Origin)")
        plt.legend(loc='best')
        plt.show()

    def PVelectricalsetup(self):
        self.tower_current_draw = self.power_per_tower_vertical/self.voltage_required
        self.number_of_cells_series = self.voltage_required/(self.data.solar__cell_maxpower_voltage_bol/1000)
        self.number_of_cells_parallel = self.tower_current_draw/(self.data.solar__cell_maxpower_current_bol/1000)

        print(self.number_of_cells_series)
        print(self.number_of_cells_parallel)


    def runprogram(self):
        self.shadow()
        self.power()
        self.optimallayout()
        self.towerposition()
        self.cablelength()
        self.plotting()
        self.PVelectricalsetup()

Test = PVArrays()
Test.runprogram()