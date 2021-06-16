import numpy as np
import unittest
from commondata import CommonData

class Life_Support():
    
    def __init__(self, Datahandler=None) -> None:
        
        if Datahandler == None:
            self.data = CommonData()
        else:
            self.data = Datahandler
            
        self.total_calc()

    def water_calc(self):
        self.water_loss = (1-self.data.water_recovery__upa_recovery/100)*self.data.water_recovery__urine_and_flush_mass + \
            (1-self.data.water_recovery__wpa_recovery/100)*(self.data.water_recovery__total_waste_water-self.data.water_recovery__urine_and_flush_mass+ \
                self.data.water_recovery__upa_recovery/100*self.data.water_recovery__urine_and_flush_mass)
        self.safety_factor = 1.25
        self.total_water_mass = self.water_loss*4*365*self.safety_factor+self.data.water_recovery__water_reserve_mass
        self.total_water_volume = self.total_water_mass/self.data.constants__water_density
        print(self.total_water_mass)
        print(self.total_water_volume)


        

    def total_calc(self):
        self.water_calc()

if __name__ == "__main__":    
    test = Life_Support()