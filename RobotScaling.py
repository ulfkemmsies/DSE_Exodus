# -*- coding: utf-8 -*-
"""
Created on Tue May 18 15:43:41 2021

@author: Lian Greijn
"""
#from DSE_Exodus.commondata import CommonData
import math as m
import numpy as np
from commondata import CommonData

mrego = 1019588             #total kg required for habitat
bagsize = 40                #[L] size of the bags
underneathhabitat = 83.7    #[m3] volume under habitat
class Robots():
    def __init__(self):
        self.data = CommonData()

    def excavation_time_underneath(self):
        print(self.data.rassor__capacity)


    
Test = Robots()
Test.excavation_time_underneath()