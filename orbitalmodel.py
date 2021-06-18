"""
Created Friday June 18, 14:16:05

Author: Ernesto Hof
"""

import numpy as np
import math as m
from commondata import CommonData

class orbit():
    def __init__(self):
        self.data = CommonData()
        self.G = self.data.constants__gravitational_constant     #m3/(kgs2)
        self.g0 = self.data.constants__earth_gravity             #(m/s2)
        self.R_earth = self.data.earth__radius                   #km
        self.R_moon = self.data.moon__vol_mean_radius            #km
        self.M_earth = self.data.earth__mass                     #kg
        self.M_moon = self.data.moon__lunar_mass                  #kg
        self.earth_day = self.data.earth__day*3600               #s
        self.lunar_sid_period = self.data.moon__sidereal_period  #Earth days
        self.lunar_perigee = self.data.moon__perigee              #km
        self.lunar_apogee = self.data.moon__apogee                #km
        self.lunar_orbit_per = self.data.moon__orbital_perimeter #km
        self.LEO_height = self.data.launch_system__starship_leo_height #km
        self.LLO_height = 100 #km

        self.mu_earth = self.G*self.M_earth
        self.mu_moon = self.G*self.M_moon
        self.lunar_mean_motion = 360/(self.lunar_sid_period*self.earth_day*3600) #deg/s
        self.lunar_semi_major_axis = (self.lunar_perigee+self.lunar_apogee)/2    #km
        self.lunar_eccentricity = (self.lunar_apogee-self.lunar_perigee)/(self.lunar_apogee+self.lunar_perigee)
        self.lunar_semi_minor_axis = self.lunar_semi_major_axis*np.sqrt(1-self.lunar_eccentricity**2)

        self.earth_SOI = self.data.earth__average_radius_soi #km
        self.lunar_SOI = self.data.moon__average_radius_soi  #km

        self.LTO_inclination = np.deg2rad(28.58)
        self.LLO_inclination = np.deg2rad(90)

    def orbitcharacteristics(self):
        self.LEO_radius = self.R_earth+self.LEO_height
        self.earth_hohmann_per = self.LEO_radius
        self.earth_hohmann_apo = self.earth_SOI
        self.earth_hohmann_ecc = (self.earth_hohmann_apo-self.earth_hohmann_per)/(self.earth_hohmann_apo+self.earth_hohmann_per)
        self.smajor_earth_hohmann = 0.5 * (self.earth_hohmann_per + self.earth_hohmann_apo)
        self.sminor_earth_hohmann = self.smajor_earth_hohmann*np.sqrt(1-self.earth_hohmann_ecc**2)

        self.LLO_radius = self.R_moon+self.LLO_height
        self.moon_hohmann_per = self.LLO_radius
        self.moon_hohmann_apo = self.lunar_SOI
        self.moon_hohmann_ecc = (self.moon_hohmann_apo-self.moon_hohmann_per)/(self.moon_hohmann_per+self.moon_hohmann_apo)
        self.smajor_moon_hohmann = 0.5*(self.moon_hohmann_apo+self.moon_hohmann_per)
        self.sminor_moon_hohmann = self.smajor_moon_hohmann*np.sqrt(1-self.moon_hohmann_ecc**2)

        self.LEO_velocity = np.sqrt(self.mu_earth/self.LEO_radius)
        self.perigee_velocity = np.sqrt(self.mu_earth*(2/(self.smajor_earth_hohmann*1000)-1/(self.LEO_radius*1000)))
        print(self.perigee_velocity)

Test = orbit()
Test.orbitcharacteristics()







