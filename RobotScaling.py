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
        self.bagsize = 500 # [L] bagsize 
        self.underneathhabitat = 83.7*self.data.regolith__density #[m3] volume under habitat
        self.number_of_trips_2habitat = 100
        self.safetyfactor_underhabitat = 0.5
        self.safetyfactor_at_excavation = 0.6
        #Running the actual calculation
        self.total_calc()
        self.data.code_finisher()

    #Calculations for the rassor
    def rassor_amount_under_habitat(self, time):
        self.robots_needed = m.ceil((self.underneathhabitat / (self.data.rassor__capacity*self.safetyfactor_underhabitat*time))) #number of robots needed for this section
        self.keepvalue = self.robots_needed
        self.data.rassor__number_needed = self.robots_needed + 1
        print("number of robots under habitat", self.robots_needed)

    def rassor_amount_at_excavationloc (self, time):
        self.robots_needed = m.ceil((self.data.regolith__total_mass - self.underneathhabitat) / (self.data.rassor__capacity*self.safetyfactor_at_excavation*time))
        if self.robots_needed >= self.keepvalue:
            self.data.rassor__number_needed = self.robots_needed + 1
        print("number of robots for other excavation", self.robots_needed)

    #Calculations Crane
    def crane_calculations(self, time):
        self.bag_number_required = (self.data.regolith__total_volume*1000) / self.bagsize
        self.cranes_needed = m.ceil((self.data.crane__operating_speed * self.bag_number_required)/(time*16*3600))
        if self.cranes_needed <= 2:
            self.data.crane__number_needed = 2

        else: 
            self.data.crane__number_needed = self.cranes_needed 
        print("number of cranes needed", self.cranes_needed)

    #Calculations Transporter
    def transporter_calculations(self, time):
        self.transport_time_total = (self.data.athlete__distance/self.data.athlete__velocity)*self.number_of_trips_2habitat*2
        self.transporters_needed = m.ceil(self.transport_time_total/(time*(16*3600)))
        if self.transporters_needed <= 2:
            self.data.athlete__number_needed = 2

        else: 
            self.data.athlete__number_needed = self.transporters_needed 

        print("Number of transporters required", self.transporters_needed)

    #Calculations bagging system
    def bagging_calculations(self, time):
        self.number_of_bags = (self.data.regolith__total_volume*1000) / self.bagsize
        self.bagging_needed = m.ceil(self.number_of_bags/(self.data.bagging__filling_capacity * time))
        self.data.bagging__number_needed = self.bagging_needed
        print("number of bagging robots needed", self.bagging_needed)

    #To run all calculations, fill in the brackets for the time required: add all defs here
    def total_calc(self):
        self.rassor_amount_under_habitat(50)
        self.rassor_amount_at_excavationloc(277)
        self.crane_calculations(350)
        self.transporter_calculations(10)
        self.bagging_calculations(277)

if __name__ == "__main__":
    Test = Robots()
    # Test.excavation_time_underneath()

    #print(Test.bagsize)

