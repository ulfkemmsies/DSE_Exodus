import math as m
from commondata import CommonData
import unittest
import numpy as np

class PowerRelated():

    def __init__(self):
        self.data = CommonData()

        self.regolith_weight = self.data.regolith__total_mass * self.data.moon__gravity

        self.p_power_required = self.data.habitat__night_avg_power                # [W] Power required from life support Dependent
        self.p_day_sec = 86400                      # [sec]
        self.p_eff_fuel_cell = self.data.power_storage__eff_fuel_cell                 # [] 55% Uncertain!          
        self.p_safety_factor = 1.25                 # [] Safety factor 
        self.p_req_days = 18                        # [days]
        self.p_h2_specific_energy = 120000000       # [J/kg]
        self.p_liquid_h2_density = 71               # [kg/m3]
        self.p_h2_specific_vol_energy = 8520000000  # [J/m3]         
        self.p_liquid_o2_density = 1141             # [kg/m3] 
        self.p_o2_life_support = self.data.total_mass__oxygen_mass                # [kg] From life support Dependent
        self.p_h2_life_support = self.data.power_storage__life_support_h2_needed             # [kg] Dependent
        self.p_h2_o2_ratio = 7.94                   # []
        self.p_h2_tank_ref_propellant_mass = self.data.power_storage__h2_tank_ref_propellant_mass    # [kg] Uncertain
        self.p_h2_tank_ref_mass = self.data.power_storage__h2_tank_ref_mass               # [kg] Uncertain
        self.p_o2_tank_ref_propellant_mass = self.data.power_storage__o2_tank_ref_propellant_mass   # [kg] Uncertain
        self.p_o2_tank_ref_mass = self.data.power_storage__o2_tank_ref                    # [kg] Uncertain
        self.p_tank_topoff_factor = 1.05            # [] You can never fill a tank 100% 
        self.p_inn_tank_radius = 1.0                # [m] Inner tank radius
        self.p_outer_tank_radius = 1.2              # [m] Outer tank radius   

        self.total_calc()
        # self.data.code_finisher()

#calculate the total mass and volume of h2 and o2 needed
    def calculate_hydrogen_energy(self):

        self.energy_needed = self.p_req_days * self.p_day_sec * self.p_power_required * self.p_eff_fuel_cell * self.p_safety_factor
        self.h2_mass_en = self.energy_needed / self.p_h2_specific_energy
        self.h2_mass = self.energy_needed / self.p_h2_specific_energy + self.p_h2_life_support
        self.o2_mass = self.h2_mass_en * self.p_h2_o2_ratio + self.p_o2_life_support
        self.h2_volume = self.h2_mass / self.p_liquid_h2_density
        self.o2_volume = self.o2_mass / self.p_liquid_o2_density

        #print("h2 mass", self.h2_mass, "h2 volume", self.h2_volume)
        #print("o2 mass", self.o2_mass, "o2 volume", self.o2_volume)

        self.data.power_storage__h2_mass  = np.round(self.h2_mass,2)
        self.data.power_storage__o2_mass  = np.round(self.o2_mass,2)

#Calculate the mass of the hydrogen and oxygen tanks based on 1989 nasa study
    def tank_mass(self):
        self.h2_tank_mass = (self.h2_mass * self.p_h2_tank_ref_mass)/ self.p_h2_tank_ref_propellant_mass
        self.o2_tank_mass = (self.o2_mass * self.p_o2_tank_ref_mass)/ self.p_o2_tank_ref_propellant_mass

        #print("h2 tank mass", self.h2_tank_mass)
        #print("o2 tank mass", self.o2_tank_mass)

        self.data.power_storage__h2_tank_mass  = np.round(self.h2_tank_mass,2)
        self.data.power_storage__o2_tank_mass  = np.round(self.o2_tank_mass,2)

# calculate the volume dimension of the h2 and o2 tank
    def calculate_tank_volume(self):
        self.h2_tank_volume = self.h2_volume * self.p_tank_topoff_factor # +5%
        self.o2_tank_volume = self.o2_volume * self.p_tank_topoff_factor # +5%
        self.h2_tank_height = self.h2_tank_volume/(3.1415*self.p_inn_tank_radius**2)
        self.o2_tank_height = self.o2_tank_volume/(3.1415*self.p_inn_tank_radius**2)
        self.h2_tank_volume_total = 3.1415 * self.p_outer_tank_radius**2 * self.h2_tank_height
        self.o2_tank_volume_total = 3.1415 * self.p_outer_tank_radius**2 * self.o2_tank_height
        
        #print("h2 tank height", self.h2_tank_height)
        #print("o2 tank height", self.o2_tank_height)
        #print("tank radius", self.p_outer_tank_radius)
        #print("h2 tank total tank volume", self.h2_tank_volume_total)    
        #print("o2 tank total tank volume", self.o2_tank_volume_total)    

        self.data.power_storage__h2_tank_volume  = np.round(self.h2_tank_volume_total,2)
        self.data.power_storage__o2_tank_volume  = np.round(self.o2_tank_volume_total,2)

    def total_calc(self):
        self.calculate_hydrogen_energy()
        self.tank_mass()
        self.calculate_tank_volume()

        self.data.power_storage__total_mass = self.h2_tank_mass + self.o2_tank_mass + self.h2_mass + self.o2_mass
        self.data.power_storage__total_volume = self.h2_tank_volume + self.o2_tank_volume + self.h2_volume + self.o2_volume
        
if __name__ == "__main__":
    Test = PowerRelated()
