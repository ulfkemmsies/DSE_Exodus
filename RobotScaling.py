# -*- coding: utf-8 -*-
"""
Created on Tue May 18 15:43:41 2021

@author: Lian Greijn
"""
#from DSE_Exodus.commondata import CommonData
import math as m
import numpy as np
from commondata import CommonData
import unittest

class Robots():
    def __init__(self, tunder, texcavation, tcrane, ttransport, tbagging):
        #Importing the commondata file
        self.data = CommonData()
        self.t1 = tunder        #Time planned for excavation of the trench underneath the habitat
        self.t2 = texcavation   #Time planned for excavation at the excavation site
        self.t3 = tcrane        #Time planned for the crane to lift the bags
        self.t4 = ttransport    #Time planned for transportation
        self.t5 = tbagging      #Time planned for the bagging process
        #Just as a reminder to me:
        # print(self.data.rassor__capacity) Dont forget!

        #place holder values required
        self.bagsize = 500 # [L] bagsize 
        self.underneathhabitat = 150.366*self.data.regolith__density #[m3] volume under habitat
        self.number_of_trips_2habitat = 100
        self.safetyfactor_underhabitat = 0.5
        self.safetyfactor_at_excavation = 0.6
        #Running the actual calculation
        self.total_calc()
        self.data.code_finisher()

    #Calculations for the rassor
    def rassor_amount_under_habitat(self):
        self.rassor_uh_robots_needed = m.ceil((self.underneathhabitat / (self.data.rassor__capacity*self.safetyfactor_underhabitat*self.t1))) #number of robots needed for this section
        self.keepvalue = self.rassor_uh_robots_needed
        self.data.rassor__number_needed = self.rassor_uh_robots_needed + 1
        print("number of robots under habitat", self.rassor_uh_robots_needed)

    def rassor_amount_at_excavationloc (self):
        self.rassor_ae_robots_needed = m.ceil((self.data.regolith__total_mass - self.underneathhabitat) / (self.data.rassor__capacity*self.safetyfactor_at_excavation*self.t2))
        if self.rassor_ae_robots_needed >= self.keepvalue:
            self.data.rassor__number_needed = self.rassor_ae_robots_needed + 1
        print("number of robots for other excavation", self.rassor_ae_robots_needed)

    #Calculations Crane
    def crane_calculations(self):
        self.bag_number_required = (self.data.regolith__total_volume*1000) / self.bagsize
        self.cranes_needed = m.ceil((self.data.crane__operating_speed * self.bag_number_required)/(self.t3*16*3600))
        if self.cranes_needed <= 2:
            self.data.crane__number_needed = 2

        else: 
            self.data.crane__number_needed = self.cranes_needed 
        print("number of cranes needed", self.cranes_needed)

    #Calculations Transporter
    def transporter_calculations(self):
        self.transport_time_total = (self.data.athlete__distance/self.data.athlete__velocity)*self.number_of_trips_2habitat*2
        self.transporters_needed = m.ceil(self.transport_time_total/(self.t4*(16*3600)))
        if self.transporters_needed <= 2:
            self.data.athlete__number_needed = 2

        else: 
            self.data.athlete__number_needed = self.transporters_needed 

        print("Number of transporters required", self.transporters_needed)

    #Calculations bagging system
    def bagging_calculations(self):
        self.number_of_bags = (self.data.regolith__total_volume*1000) / self.bagsize
        self.bagging_needed = m.ceil(self.number_of_bags/(self.data.bagging__filling_capacity * self.t5))
        self.data.bagging__number_needed = self.bagging_needed
        print("number of bagging robots needed", self.bagging_needed)

    def main_outputs(self):
        self.data.all_logistics__power_draw = self.data.bagging__number_needed * self.data.bagging__power_draw + self.data.athlete__number_needed * self.data.athlete__power_draw + self.data.crane__number_needed * self.data.crane__power_draw + self.data.rassor__number_needed * self.data.rassor__power_draw + self.data.nipper__number_needed * self.data.nipper__power_draw + self.data.robotarm__number_needed * self.data.robotarm__power_draw
        self.data.all_logistics__total_mass = self.data.bagging__number_needed * self.data.bagging__mass + self.data.athlete__number_needed * self.data.athlete__mass + self.data.crane__number_needed * self.data.crane__mass + self.data.rassor__number_needed * self.data.rassor__mass + self.data.nipper__number_needed * self.data.nipper__mass + self.data.robotarm__number_needed * self.data.robotarm__mass
        self.data.all_logistics__total_volume = self.data.bagging__number_needed * self.data.bagging__volume + self.data.athlete__number_needed * self.data.athlete__volume + self.data.crane__number_needed * self.data.crane__volume + self.data.rassor__number_needed * self.data.rassor__volume + self.data.nipper__number_needed * self.data.nipper__volume + self.data.robotarm__number_needed * self.data.robotarm__volume

    #To run all calculations, fill in the brackets for the time required: add all defs here
    def total_calc(self):
        self.rassor_amount_under_habitat()
        self.rassor_amount_at_excavationloc()
        self.crane_calculations()
        self.transporter_calculations()
        self.bagging_calculations()


class Robottests(unittest.TestCase):

    def setUp(self):
        self.example = Robots(10,10,1,10,1)
        
    def test_inflatable_thickness(self):
        self.assertAlmostEqual(self.example.rassor_uh_robots_needed, 10)
        self.assertAlmostEqual(self.example.rassor_ae_robots_needed, 59)
        self.assertAlmostEqual(self.example.cranes_needed, 2)
        self.assertAlmostEqual(self.example.bagging_needed, 27)

if __name__ == "__main__":
    RunProgramm = Robots(84,317,350,10,118)
    
    # unittest.main()
    # Test.excavation_time_underneath()

    #print(Test.bagsize)


