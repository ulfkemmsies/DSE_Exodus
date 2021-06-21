import math as m
import numpy as np
from commondata import CommonData


class Safehouse():

    def __init__(self):
        #Importing the commondata file
        self.data = CommonData()

        #Just as a reminder to me:
        # print(self.data.rassor__capacity) Dont forget!

        #costants
        self.safehouse_radius = 164 # [cm]
        self.safehouse_underground_height = 100 #[cm]
        self.safehouse_bottom_height = 150
        self.safehouse_top_height = 350
        self.safehouse_airlock_covering = 10000 #[cm^2]

        self.thickness_Al = 5 #[cm]
        self.bottom_thickness = 70 #[cm]

        #areas [cm^2]
        self.safehouse_endcaps_area = 2*self.safehouse_radius*self.safehouse_radius*np.pi
        self.safehouse_underground_area = 2*self.safehouse_radius*self.safehouse_underground_height
        self.safehouse_bottom_area = 2 * self.safehouse_radius* self.safehouse_bottom_height - self.safehouse_airlock_covering
        self.safehouse_top_area = 2 * self.safehouse_radius * self.safehouse_top_height

        self.total_calc()


    #weights all in kilograms, input safehouse_water in litres
    def safehouse_weights(self, safehouse_water):
        self.underground_weight = self.safehouse_underground_area*self.thickness_Al*2.2/1000
        self.top_weight = self.safehouse_top_area * self.thickness_Al * 2.2/1000
        self.endcaps_weight = self.safehouse_endcaps_area * self.thickness_Al * 2.2/1000


        self.water_thickness = (safehouse_water*1000 / self.safehouse_bottom_area) #[cm]

        self.bottom_water_weight = self.water_thickness*self.safehouse_bottom_area*0.997/1000
        self.bottom_rigid_weight = (self.bottom_thickness - self.water_thickness)*self.safehouse_bottom_area*2.15/1000

        self.safehouse_total_weight = self.underground_weight+self.top_weight+self.endcaps_weight+self.bottom_rigid_weight+self.bottom_water_weight

        print(self.safehouse_total_weight)
        self.data.habitat__safehouse_mass = self.safehouse_total_weight



    def total_calc(self):
        self.safehouse_weights(1300)


if __name__ == "__main__":
    Test = Safehouse()
    # Test.excavation_time_underneath()





