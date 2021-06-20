# -*- coding: utf-8 -*-
"""
Created on Tue May 18 15:43:41 2021

@author: Lian Greijn
"""
#from DSE_Exodus.commondata import CommonData
import math as m
import numpy as np
from commondata import CommonData

class Robots():
    def __init__(self):
        #Importing the commondata file
        self.data = CommonData()

        #Just as a reminder to me:
        # print(self.data.rassor__capacity) Dont forget!

        #place holder values required
        self.bagsize = 50 # [L] bagsize 
        self.underneathhabitat = 83.7*self.data.regolith__density #[m3] volume under habitat
        self.number_of_trips_2habitat = 100
        self.safetyfactor_underhabitat = 0.5
        self.safetyfactor_at_excavation = 0.8
        #Running the actual calculation
        self.total_calc()

    #Calculations for the rassor
    def rassor_amount_under_habitat(self, time):
        self.robots_needed = m.ceil((self.underneathhabitat / (self.data.rassor__capacity*self.safetyfactor_underhabitat*time))) #number of robots needed for this section
        print("number of robots under habitat", self.robots_needed)

    def rassor_amount_at_excavationloc (self, time):
        self.robots_needed = m.ceil((self.data.regolith__total_mass - self.underneathhabitat) / (self.data.rassor__capacity*self.safetyfactor_at_excavation*time))
        print("number of robots for other excavation", self.robots_needed)

    #Calculations Crane
    def crane_calculations(self, time):
        self.bag_number_required = (self.data.regolith__total_volume*1000) / self.bagsize
        self.cranes_needed = m.ceil((self.data.crane__operating_speed * self.bag_number_required)/(time*16*3600))*()
        print("number of cranes needed", self.cranes_needed)

    #Calculations Transporter
    def transporter_calculations(self, time):
        self.transport_time_total = (self.data.athlete__distance/self.data.athlete__velocity)*self.number_of_trips_2habitat*2
        self.transporters_needed = m.ceil(self.transport_time_total/(time*(16*3600)))
        print("Number of tranpsorters required", self.transporters_needed)

    #To run all calculations, fill in the brackets for the time required: add all defs here
    def total_calc(self):
        self.rassor_amount_under_habitat(60)
        self.rassor_amount_at_excavationloc(330)
        self.crane_calculations(350)
        self.transporter_calculations(10)

if __name__ == "__main__":
    Test = Robots()
    # Test.excavation_time_underneath()

    print(Test.bagsize)