# -*- coding: utf-8 -*-
"""
Created on Tue May 18 15:43:41 2021

@author: Lian Greijn
"""
#from DSE_Exodus.commondata import CommonData
import math as m
import numpy as np
'''
class Robots():
    def __init__(self, time):
        self.data = CommonData()
        self.excavation_time = time
    
    def truetime_Collecting(self):
        self.true_time = self.excavation_time - (2*self.distance_hab2exc*)
        print(Result)
'''

#Calculations for RASSOR
mras = 66
D2es = 100  #[m] Distance to excavation site
Vras = 1.5  #[m/s] average velocity of the RASSOR
Cr = 2700   #[kg]/day = capacity RASSOR to scoop regalith dust
Sr = 1      #Safety factor on actual performance of RASSOR
Crt = Cr/Sr #True capacity of RASSOR
Mreq = 1019588  #[kg] required amount of regolith for the habitat
Dcol = 100      #Number of days spent collecting
Ntrips = 10     #Number of trips to excavation site
Dcoltrue = Dcol - (2*D2es*Vras*Ntrips)  #Last part can be removed in case of hopper at excavation site
Nras = Mreq/(Crt*Dcol)
Nrasround = m.ceil(Nras) #Number of required RASSOR robots to complete task


#Calculations for ATHLETE
Dl2h = 1000  #[m] Distance between landing site and the habitat
Dl2p = 1000  #[m] Distance between landing site and the solar farm
Vath = 9/3.6 #[m/s] Average speed of Athlete
N2h = 10    #Number of required trips to the habitat site
N2p = 10    #Number of required trips to the power site
Ddriv = 10 #Number of days that can be used to drive items
mathl = 2340 

#Crane
"""
Speed unknown, number of cargo units unknown 

"""


Nath = ((Dl2h/Vath)*N2h + (Dl2p/Vath)*N2p)/(Ddriv*24*3600)
Nathround = m.ceil(Nath)


mtotrob = Nathround*mathl + mras*Nrasround #Total weight of the robots
print("Number of RASSOR robots required", Nrasround)
print('Number of ATHLETE robots required', Nathround)
print('In total these robot weigh:', mtotrob, 'kg')

