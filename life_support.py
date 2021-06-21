import numpy as np
import unittest
from commondata import CommonData

class Life_Support():
    
    def __init__(self):
        
        self.data = CommonData()
        self.total_calc()
        self.data.code_finisher()

    def water_calc(self):
        self.urine_and_flush_mass = 2.0
        self.total_waste_water = 15.962

        self.water_loss = (1-self.data.water_recovery__upa_recovery/100)*self.urine_and_flush_mass + \
            (1-self.data.water_recovery__wpa_recovery/100)*(self.total_waste_water-self.urine_and_flush_mass+ \
                self.data.water_recovery__upa_recovery/100*self.urine_and_flush_mass)
        self.safety_factor = 1.25
        self.total_water_mass = self.water_loss*4*365*self.safety_factor+self.data.water_recovery__water_reserve_mass
        self.total_water_volume = self.total_water_mass/self.data.constants__water_density
        return self.total_water_mass

    def volume_calc(self):
        return self.data.habitat__inflatable_length*np.pi*(self.data.habitat__inflatable_diameter/2)**2 +\
                    self.data.habitat__rigid_length*np.pi*(self.data.habitat__rigid_diameter/2)**2

    def gas_storage(self):
        self.volume = self.volume_calc()
        self.ox_volume_fill = (101325*self.volume*32)/(self.data.constants__gas_constant*295.15)*0.21/1000
        self.nitro_volume_fill = (101325*self.volume*28.014)/(self.data.constants__gas_constant*295.15)*(1-0.21)/1000
        self.airlock_loss_rate = 0.10
        self.airlock_loss = self.data.habitat__airlock_volume*self.airlock_loss_rate*self.data.gas_storage__airlock_cycles
        self.lost_ox = (101325*self.airlock_loss*32)/(self.data.constants__gas_constant*295.15)*0.21/1000
        self.lost_nitro = (101325*self.airlock_loss*28.014)/(self.data.constants__gas_constant*295.15)*(1-0.21)/1000
        self.ox_mass_ratio = self.ox_volume_fill/(self.ox_volume_fill+self.nitro_volume_fill)
        self.leaked_ox = self.ox_mass_ratio*self.data.gas_storage__leakage_rate*365
        self.leaked_nitro = (1-self.ox_mass_ratio)*self.data.gas_storage__leakage_rate*365
        self.total_ox = (self.ox_volume_fill+self.lost_ox+self.leaked_ox)*1.25
        self.data.total_mass__oxygen_mass = self.total_ox
        self.total_nitro = (self.nitro_volume_fill+self.lost_nitro+self.leaked_nitro)*1.25
        return self.total_ox+self.total_nitro
     

    def total_calc(self):
        self.data.water_recovery__total_water_mass = self.water_calc()
        self.data.gas_storage__total_gas_storage = self.gas_storage()
        self.total_ls_mass = self.data.total_mass__ls_mass_excluding_water_and_gas
        self.total_ls_mass += self.total_water_mass + self.total_ox+self.total_nitro
        print(self.total_ls_mass)
        self.data.total_mass__total_ls_mass = self.total_ls_mass
        self.total_peak_power = 9627
        self.total_peak_power += self.data.power1__comms_peak_power
        print(self.total_peak_power)
        self.data.total_mass__total_ls_power = self.total_peak_power


if __name__ == "__main__":    
    test = Life_Support()