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
        self.data = CommonData()
        print(self.data.rassor__capacity)

        #place holders required
        self.bagsize = 40 # [L] bagsize 
        self.underneathhabitat = 83.7*self.data.regolith__density #[m3] volume under habitat

        self.total_calc()

    #Calculations for the rassor
    def rassor_amount_under_habitat(self, time):
        self.robots_needed = m.ceil((self.underneathhabitat / (self.data.rassor__capacity*time))) #number of robots needed for this section
        print("number of robots under habitat", self.robots_needed)

    def rassor_amount_at_excavationloc (self, time):
        self.robots_needed = m.ceil((self.data.regolith__total_mass - self.underneathhabitat) / (self.data.rassor__capacity*time))
        print("number of robots for other excavation", self.robots_needed)

    #Calculations Crane
    def crane_calculations(self, time):
        self.bag_number_required = self.data.regolith__total_volume / self.bagsize
        self.cranes_needed = m.ceil((self.data.crane__operating_speed * self.bag_number_required)/(time))
        print("number of cranes needed", self.cranes_needed)

    def total_calc(self):
        self.rassor_amount_under_habitat(100)
        self.rassor_amount_at_excavationloc(200)
        self.crane_calculations(100)

    #Calculations Transporter
Test = Robots()