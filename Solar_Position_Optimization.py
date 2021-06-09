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
        self.number_of_towers = 6
        self.tower_panel_area = self.data.solar__maximum_area/self.number_of_towers

    def shadow(self):
        self.shadow_radius_min = self.tower_height/np.tan(self.inclination_max)
        self.shadow_radius_max = self.tower_height/np.tan(self.inclination_min)
        self.shadow_diameter_min = 2*self.shadow_radius_min
        self.shadow_diameter_max = 2*self.shadow_radius_max
        self.shadow_area_min = np.pi*self.shadow_radius_min**2
        self.shadow_area_max = np.pi*self.shadow_radius_max**2

    def power():
        self.power_vertical = self.data.moon__solar_constant*self.data.solar__maximum_area*self.data.power__PV_efficiency