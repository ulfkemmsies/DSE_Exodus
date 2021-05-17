import numpy as np
import scipy as sp
import math as m
from area_calc import Crosssection

class CommonData():
    
    def __init__(self) -> None:
        
        self.launch_cost = 250000 #$/kg

        self.moon_gravity = 1.625

        self.allowable_radiation = 99
        self.total_radiation = 100
        self.attenuation_needed = self.allowable_radiation/self.total_radiation

        self.regolith_density = 1500 #kg/m3
        self.regolith_porosity = 45 #%
        self.regolith_cohesion = 2.35 
        self.regolith_internal_friction_angle = 18.5 #deg
        self.regolith_bearing_capacity = 31
        self.regolith_thermal_conductivity = 1
        self.regolith_specific_heat = 800
        self.regolith_specific_area = 0.9
        self.regolith_dose_reduction = 0.8 #% per g/cm2
        
        self.kevlar_youngs_modulus = 179 #GPa
        self.kevlar_ultimate_tensile = 3450 #MPa
        self.kevlar_breaking_tenacity = 3000 #MPa
        self.kevlar_dose_reduction = 5.5 #% per g/cm2
        self.kevlar_thermal_conductivity = 0.04 #W/mK
        self.kevlar_density = 1.47 #kg/m3
        self.kevlar_safety_factor = 1.5 

class Structure():

    def __init__(self,r,d) -> None:
        
        self.habitat_length = 30
        self.data = CommonData()
        self.habitat_radius = r
        self.floor_depth = d
        
    
    def thickness_distributor(self):
        self.regolith_thickness = (self.data.attenuation_needed / ((self.data.regolith_dose_reduction/100) * (self.data.regolith_density /1000)))/100 #m
        self.Cross_section = Crosssection(self.habitat_radius,self.regolith_thickness,self.floor_depth)

    def reg_mass_calc(self):
        self.regolith_cs_area = self.Cross_section.total_area()
        self.regolith_total_volume = self.regolith_cs_area * (self.habitat_length - self.habitat_radius) + 0.5 * m.pi * self.regolith_cs_area
        self.regolith_total_mass = self.regolith_total_volume * self.data.regolith_density

    def pressure_calc(self):
        self.internal_pressure = 101325 #Pa
        self.external_pressure = self.regolith_thickness * self.data.regolith_density * self.data.moon_gravity #Pa
        self.gauge_pressure = self.internal_pressure - self.external_pressure
        self.kevlar_thickness = self.data.kevlar_safety_factor * self.gauge_pressure * self.habitat_radius / (self.data.kevlar_breaking_tenacity *10**(6)) #m

    def kevlar_mass_calc(self):
        self.kevlar_total_volume = self.habitat_radius * 2 * m.pi * self.kevlar_thickness + self.kevlar_thickness * (m.pi)**2 * 0.5
        self.kevlar_total_mass = self.kevlar_total_volume * self.data.kevlar_density
        self.kevlar_launch_cost = self.kevlar_total_mass * self.data.launch_cost

    def total_calc(self):
        self.thickness_distributor()
        self.reg_mass_calc()
        self.pressure_calc()
        self.kevlar_mass_calc()

        print("Habitat Radius:",self.habitat_radius)
        print("Habitat Length:",self.habitat_length)
        print("Floor Depth:",self.floor_depth)
        print("Regolith Mass:",self.regolith_total_mass)
        print("Regolith Thickness:",self.regolith_thickness)
        print("Kevlar Mass:",self.kevlar_total_mass)
        print("Kevlar Thickness:",self.kevlar_thickness)
        print("Kevlar Launch Cost:",self.kevlar_launch_cost)
        print("Highest Pressure:",self.external_pressure)
        print("Lowest Pressure:",self.gauge_pressure)
        print("Radiation Attenuation:",self.data.attenuation_needed)

    
test = Structure(3,0)
test.total_calc()