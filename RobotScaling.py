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
        self.bagsize = 40 # [L] bagsize 
        self.underneathhabitat = 83.7*self.data.regolith__density #[m3] volume under habitat
        self.total_calcu

    def rassor_amount_under_habitat(self, time):
        self.robots_needed = m.ceil((self.underneathhabitat / (self.data.rassor__capacity*time))) #number of robots needed for this section

    def rassor_amount_at_excavationloc (self, time):
        self.robots_needed2 = m.ceil((self.data.regolith__total_mass - self.underneathhabitat) / (self.data.rassor__capacity*time))


    def total_calcu(self):
        self.rassor_amount_at_excavationloc(100)
        self.rassor_amount_under_habitat(200)



    
Test = Robots()