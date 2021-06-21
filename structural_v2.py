import math as m
from commondata import CommonData
import unittest

class StressRelated():

    def __init__(self):
        self.data = CommonData()

        self.regolith_weight = self.data.regolith__total_mass * self.data.moon__gravity

        self.t_insulation = 0.005
        self.t_bladder = 0.001
        self.t_lining = 0.0004
        self.t_radiation = 0.02
        self.t_restraint = 0.0002

        self.safety_factor = 4

        self.total_calc()
        self.data.code_finisher()

    def calculate_inflatable_properties(self):

        self.strain_insulation = self.data.layers__emod_insulation / self.data.layers__tensile_insulation
        self.strain_bladder = self.data.layers__emod_bladder / self.data.layers__tensile_bladder
        self.strain_lining = self.data.layers__emod_lining / self.data.layers__tensile_lining
        self.strain_radiation = self.data.layers__emod_radiation / self.data.layers__tensile_radiation
        self.strain_restraint = self.data.layers__emod_restraint / self.data.layers__tensile_restraint

        self.inflatable_thickness = \
            self.t_insulation + self.t_bladder * 3 + self.t_lining + self.t_radiation + self.t_restraint

        print("inflatable thickness", self.inflatable_thickness)

        self.t_ratio_insulation = self.t_insulation / self.inflatable_thickness
        self.t_ratio_bladder = self.t_bladder * 3 / self.inflatable_thickness
        self.t_ratio_lining = self.t_lining / self.inflatable_thickness
        self.t_ratio_radiation = self.t_radiation / self.inflatable_thickness
        self.t_ratio_restraint = self.t_restraint / self.inflatable_thickness

        self.inflatable_tensile_strength = \
            self.data.layers__tensile_insulation * self.t_ratio_insulation + \
            self.data.layers__tensile_bladder * self.t_ratio_bladder + \
            self.data.layers__tensile_lining * self.t_ratio_lining + \
            self.data.layers__tensile_restraint * self.t_ratio_restraint + \
            self.data.layers__tensile_radiation * self.t_ratio_radiation

        print(self.inflatable_tensile_strength)

    def calculate_stress(self):

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

        self.volume_insulation = self.dimension * self.t_insulation
        self.volume_bladder = self.dimension * self.t_bladder
        self.volume_lining = self.dimension * self.t_lining 
        self.volume_radiation = self.dimension * self.t_radiation
        self.volume_restraint = self.dimension * self.t_restraint

        self.inflatable_mass = self.mass_insulation + self.mass_lining + self.mass_bladder + self.mass_restraint + \
            self.mass_radiation

        self.data.habitat__inflatable_volume = self.volume_insulation + self.volume_lining + self.volume_bladder + self.volume_restraint + \
        self.volume_radiation

        self.data.habitat__inflatable_mass = self.inflatable_mass

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