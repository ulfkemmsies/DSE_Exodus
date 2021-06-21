import math as m
from commondata import CommonData
import unittest

class PowerRelated():

    def __init__(self):
        self.data = CommonData()

        self.regolith_weight = self.data.regolith__total_mass * self.data.moon__gravity

        self.p_power_required = 6.3                 # [kW] Power required from life support
        self.p_day_sec = 86400                      # [sec]
        self.p_eff_fuel_cell = 1.81                 # [] Uncertain!          
        self.p_safety_factor = 1.25                 # [] Safety factor 
        self.p_req_days = 18                        # [days]
        self.p_h2_specific_energy = 120000000       # [J/kg]
        self.p_liquid_h2_density = 71               # [kg/m3]
        self.p_h2_specific_vol_energy = 8520000000  # [J/m3]         
        self.p_liquid_o2_density = 1141             # [kg/m3] From life support
        self.p_o2_life_support = 495                # [kg] From life support
        self.p_h2_life_support = 267.47             # [kg]
        self.p_h2_o2_ratio = 7.94                   # []
        
        
        self.total_calc()

    def calcucalculate_hydrogen_energy(self):

        self.energy_needed = self.p_req_days * self.p_day_sec * self.p_power_required * self.p_eff_fuel_cell * self.p_safety_factor
        self.h2_mass = self.energy_needed / self.p_h2_specific_energy + self.p_h2_life_support
        self.o2_mass = self.h2_mass * self.p_h2_o2_ratio + self.p_o2_life_support
        self.h2_volume = self.h2_mass / self.p_liquid_h2_density
        self.o2_volume = self.o2_mass / self.p_liquid_o2_density

        print("h2 mass", self.h2_mass, "h2 volume", self.h2_volume)
        print("o2 mass", self.o2_mass, "o2 volume", self.o2_volume)

    def tank_mass (self):

        self.radial_stress = self.data.habitat__internal_pressure * self.data.habitat__radius / self.inflatable_thickness
        self.longitudinal_stress = self.radial_stress / 2
        self.shear_stress = self.radial_stress / 4

        self.stress_safety = self.radial_stress * self.safety_factor
        print("shear", self.shear_stress)
        print(self.stress_safety)

    def calculate_inflatable_mass(self):

        self.dimension = 2 * m.pi * self.data.habitat__radius * self.data.habitat__length + \
            2 * m.pi * (self.data.habitat__radius) ** 2

        self.mass_insulation = self.dimension * self.t_insulation * self.data.layers__density_insulation
        self.mass_bladder = self.dimension * self.t_bladder * self.data.layers__density_bladder
        self.mass_lining = self.dimension * self.t_lining * self.data.layers__density_lining
        self.mass_radiation = self.dimension * self.t_radiation * self.data.layers__density_radiation
        self.mass_restraint = self.dimension * self.t_restraint * self.data.layers__density_restraint

        self.inflatable_mass = self.mass_insulation + self.mass_lining + self.mass_bladder + self.mass_restraint + \
            self.mass_radiation

        print("Inflatable mass:", self.inflatable_mass)

    def total_calc(self):
        self.calculate_inflatable_properties()
        self.calculate_stress()
        self.calculate_inflatable_mass()


Test = StressRelated()
print(Test)

# class UnitTest(unittest.TestCase):

    #def SetUp(self):
    #    self.Test_Struc = set up unit value scenario

    #def test_inflatable_thickness(self):
        #self.assertEqual(truncate(self.Test_Struc.inflatable_thickness, 2), 0.010)

#if __name__ == '__main__':
#    unittest.main()