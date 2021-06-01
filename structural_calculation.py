import numpy as np
import scipy as sp
import math as m
from area_calc import Crosssection
from commondata import CommonData
import unittest
from area_calc import truncate


class Structure():

    def __init__(self, Datahandler=None) -> None:
        
        if Datahandler == None:
            self.data = CommonData()
        else:
            self.data = Datahandler
            
        self.total_calc()
        self.data.attributes_to_df()
        # self.data.code_finisher()

    def thickness_distributor(self):
        self.data.regolith__thickness = (self.data.habitat__radiation_attenuation_needed / ((self.data.regolith__radiation_dose_reduction/100) * (self.data.regolith__density /1000)))/100 #m
        self.Cross_section = Crosssection(self.data.habitat__radius,self.data.regolith__thickness,self.data.habitat__floor_depth)

    def reg_mass_calc(self):
        self.regolith_cs_area = self.Cross_section.total_area()
        self.data.regolith__total_volume = self.regolith_cs_area * (self.data.habitat__length - self.data.habitat__radius) + 0.5 * m.pi * self.regolith_cs_area
        self.data.regolith__total_mass = self.data.regolith__total_volume * self.data.regolith__density

    def pressure_calc(self):
        self.external_pressure = self.data.regolith__thickness * self.data.regolith__density * self.data.moon__gravity #Pa
        self.gauge_pressure = self.data.habitat__internal_pressure - self.external_pressure
        self.data.kevlar__thickness = self.data.habitat__structural_safety_factor * self.data.habitat__internal_pressure * self.data.habitat__radius / (self.data.kevlar__breaking_tenacity *10**(6)) #m

    def kevlar_mass_calc(self):
        self.kevlar_total_volume = (self.data.habitat__radius * 2 * m.pi * self.data.kevlar__thickness)*(self.data.habitat__length-self.data.habitat__radius) + (self.data.kevlar__thickness * (m.pi)**2 * 0.5)
        self.data.kevlar__total_mass = self.kevlar_total_volume * self.data.kevlar__density
        self.kevlar_launch_cost = self.data.kevlar__total_mass * self.data.launch_system__launch_cost

    def total_calc(self):
        self.thickness_distributor()
        self.reg_mass_calc()
        self.pressure_calc()
        self.kevlar_mass_calc()

        # print("Habitat Radius [m]:",self.data.habitat__radius)
        # print("Habitat Length [m]:",self.data.habitat__length)
        # print("Floor Depth [m]:",self.data.habitat__floor_depth)
        # print("Regolith Volume [m3]:",self.data.regolith__total_volume)
        # print("Regolith Mass [kg]:",self.data.regolith__total_mass)
        # print("Regolith Thickness [m]:",self.data.regolith__thickness)
        # print("Kevlar Mass [kg]:",self.data.kevlar__total_mass)
        # print("Kevlar Thickness [mm]:",self.data.kevlar__thickness*1000)
        # print("Kevlar Launch Cost [$]:",self.kevlar_launch_cost)
        # print("Highest Pressure [Pa]:",self.data.habitat__internal_pressure)
        # print("Lowest Pressure [Pa]:",self.gauge_pressure)
        # print("Radiation Attenuation:",self.data.habitat__radiation_attenuation_needed)


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
    test = Structure()
    


    