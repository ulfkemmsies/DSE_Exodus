import numpy as np
import scipy as sp
import math as m
from area_calc import Crosssection
from commondata import CommonData
import unittest
from area_calc import truncate

class Structure():

    def __init__(self,r,d) -> None:
        
        self.habitat_length = 27
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
        self.kevlar_thickness = self.data.kevlar_safety_factor * self.internal_pressure * self.habitat_radius / (self.data.kevlar_breaking_tenacity *10**(6)) #m

    def kevlar_mass_calc(self):
        self.kevlar_total_volume = (self.habitat_radius * 2 * m.pi * self.kevlar_thickness)*(self.habitat_length-self.habitat_radius) + (self.kevlar_thickness * (m.pi)**2 * 0.5)
        self.kevlar_total_mass = self.kevlar_total_volume * self.data.kevlar_density
        self.kevlar_launch_cost = self.kevlar_total_mass * self.data.launch_cost

    def total_calc(self):
        self.thickness_distributor()
        self.reg_mass_calc()
        self.pressure_calc()
        self.kevlar_mass_calc()

        print("Habitat Radius [m]:",self.habitat_radius)
        print("Habitat Length [m]:",self.habitat_length)
        print("Floor Depth [m]:",self.floor_depth)
        print("Regolith Volume [m3]:",self.regolith_total_volume)
        print("Regolith Mass [kg]:",self.regolith_total_mass)
        print("Regolith Thickness [m]:",self.regolith_thickness)
        print("Kevlar Mass [kg]:",self.kevlar_total_mass)
        print("Kevlar Thickness [mm]:",self.kevlar_thickness*1000)
        print("Kevlar Launch Cost [$]:",self.kevlar_launch_cost)
        print("Highest Pressure [Pa]:",self.internal_pressure)
        print("Lowest Pressure [Pa]:",self.gauge_pressure)
        print("Radiation Attenuation:",self.data.attenuation_needed)


class StructuralTests(unittest.TestCase):

    def setUp(self):
        self.Struct = Structure(3,1)
        self.Struct.total_calc()

    def test_regolith_thickness(self):
        self.assertEqual(truncate(self.Struct.regolith_thickness,2), 0.82)
    
    def test_regolith_volume(self):
        self.assertEqual(truncate(self.Struct.regolith_total_volume,2), )

    def test_regolith_mass(self):
        self.assertEqual(truncate(self.Struct.regolith_total_mass,2), )

    def test_regolith_external_pressure(self):
        self.assertEqual(truncate(self.Struct.external_pressure,2), )

    def test_kevlar_thickness(self):
        self.assertEqual(truncate(self.Struct.kevlar_thickness,2), )

    def test_kevlar_volume(self):
        self.assertEqual(truncate(self.Struct.kevlar_total_volume,2), )

if __name__ == "__main__":    
    test = Structure(3,1)
    test.total_calc()

    