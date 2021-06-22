"""
Created Friday June 18, 14:16:05

Author: Ernesto Hof
"""

import numpy as np
import math as m
from commondata import CommonData
import matplotlib.pyplot as plt

class orbit():
    def __init__(self):
        self.data = CommonData()
        self.G = self.data.constants__gravitational_constant            #m3/(kgs2)
        self.g0 = self.data.earth__gravity                              #(m/s2)
        self.R_earth = self.data.earth__radius                          #km
        self.R_moon = self.data.moon__vol_mean_radius                   #km
        self.M_earth = self.data.earth__mass                            #kg
        self.M_moon = self.data.moon__mass                              #kg
        self.earth_day = self.data.earth__day*3600                      #s
        self.lunar_sid_period = self.data.moon__sidereal_period         #Earth days
        self.lunar_perigee = self.data.moon__perigee                    #km
        self.lunar_apogee = self.data.moon__apogee                      #km
        self.lunar_orbit_per = self.data.moon__orbital_perimeter        #km
        self.LEO_height = self.data.launch_system__starship_leo_height  #km
        self.LLO_height = self.data.launch_system__llo_height           #km

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
        self.earth_rot_velocity = 0

        self.starshipdry = self.data.launch_system__starship_dry_mass
        self.superheavydry = self.data.launch_system__superheavy_dry_mass
        self.starshipfuel = self.data.launch_system__starship_prop_capacity
        self.superheavyfuel = self.data.launch_system__superheavy_prop_capacity
        self.starship_PL = 57597
        self.methaneIsp = self.data.launch_system__ch4_specific_impulse_vac
        self.hydrogenIsp = self.data.launch_system__lh2lox_specific_impulse_vac

        self.ariane_PL = self.data.launch_system__ariane_pl_mass
        self.ariane_structural_coeff = 3

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

        self.LEO_velocity = np.sqrt(self.mu_earth/(self.LEO_radius*1000))
        self.perigee_velocity = np.sqrt(self.mu_earth*(2/(self.LEO_radius*1000)-1/(self.smajor_earth_hohmann*1000)))
        self.apogee_velocity = np.sqrt(self.mu_earth*(2/(self.earth_SOI*1000)-1/(self.smajor_earth_hohmann*1000)))

        self.LLO_velocity = np.sqrt(self.mu_moon/(self.LLO_radius*1000))
        self.periselene_velocity = np.sqrt(self.mu_moon*(2/(self.LLO_radius*1000)-1/(self.smajor_moon_hohmann*1000)))
        self.aposelene_velocity = np.sqrt(self.mu_moon*(2/(self.lunar_SOI*1000)-1/(self.smajor_moon_hohmann*1000)))

    def deltaV(self):
        self.orbitcharacteristics()
        self.deltaV_earth_launch = 0 #by defintion
        self.deltaV_earth_exit = self.perigee_velocity-self.LEO_velocity
        self.deltaV_lunar_entry = self.apogee_velocity-self.aposelene_velocity
        self.deltaV_lunar_inclination = np.sqrt(2*self.aposelene_velocity**2*(1-np.cos(self.LLO_inclination)))
        self.deltaV_LLO_circulization = np.abs(self.periselene_velocity-self.LLO_velocity)
        self.deltaV_lunar_landing = self.LLO_velocity
        self.total_deltaV = 1.1*(self.deltaV_earth_launch+self.deltaV_earth_exit+self.deltaV_lunar_entry+\
            self.deltaV_lunar_inclination+self.deltaV_LLO_circulization+self.deltaV_lunar_landing)

    def propellantmass(self, starship, ariane):
        if starship == True:
            self.dry = self.starshipdry
            self.PL = self.starship_PL
            self.Isp = self.methaneIsp

        else:
            self.PL = 1225
            self.dry = self.ariane_structural_coeff*self.PL
            self.Isp = self.hydrogenIsp

        self.Epropmass_lunar_landing = m.exp(self.deltaV_lunar_landing/(self.g0*self.Isp))*\
            (self.dry+self.PL)-self.dry-self.PL
        self.Epropmass_LLO_circulization = m.exp(self.deltaV_LLO_circulization/(self.g0*self.Isp))*\
            (self.dry+self.PL+self.Epropmass_lunar_landing)-\
            self.dry-self.PL-self.Epropmass_lunar_landing
        self.Epropmass_LLO_inclination = m.exp(self.deltaV_lunar_inclination/(self.g0*self.Isp))*\
            (self.dry+self.PL+self.Epropmass_lunar_landing+self.Epropmass_LLO_circulization)-\
            self.dry-self.PL-self.Epropmass_lunar_landing-self.Epropmass_LLO_circulization
        self.Epropmass_moon_entry = m.exp(self.deltaV_lunar_entry/(self.g0*self.Isp))*\
            (self.dry+self.PL+self.Epropmass_lunar_landing+self.Epropmass_LLO_circulization+self.Epropmass_LLO_inclination)-\
            self.dry-self.PL-self.Epropmass_lunar_landing-self.Epropmass_LLO_circulization-self.Epropmass_LLO_inclination
        self.Epropmass_earth_exit = m.exp(self.deltaV_earth_exit/(self.g0*self.Isp))*\
            (self.dry+self.PL+self.Epropmass_lunar_landing+self.Epropmass_LLO_circulization+self.Epropmass_LLO_inclination+self.Epropmass_moon_entry)-\
            self.dry-self.PL-self.Epropmass_lunar_landing-self.Epropmass_LLO_circulization-self.Epropmass_LLO_inclination-self.Epropmass_moon_entry

        self.totalpropmass_moon_journey = self.Epropmass_lunar_landing+self.Epropmass_LLO_circulization+self.Epropmass_LLO_inclination+\
            self.Epropmass_moon_entry+self.Epropmass_earth_exit
        self.additionalfuel_moon_journey = self.totalpropmass_moon_journey*0.1
        self.totalpropmass_moon_journey += self.additionalfuel_moon_journey

        self.Lpropmass_earth_entry = m.exp(self.deltaV_earth_exit/(self.g0*self.Isp))*\
                                     (self.dry+self.PL)-self.dry-self.PL
        self.Lpropmass_moon_exit = m.exp(self.deltaV_lunar_entry/(self.g0*self.Isp))*\
            (self.dry+self.PL+self.Lpropmass_earth_entry)-self.dry-self.PL-self.Lpropmass_earth_entry
        self.Lpropmass_LLO_inclination = m.exp(self.deltaV_lunar_inclination/(self.g0*self.Isp))*\
            (self.dry+self.PL+self.Lpropmass_earth_entry+self.Lpropmass_moon_exit)-\
            self.dry-self.PL-self.Lpropmass_earth_entry-self.Lpropmass_moon_exit
        self.Lpropmass_lunarhohmann = m.exp(self.deltaV_LLO_circulization/(self.g0*self.Isp))*\
            (self.dry+self.PL+self.Lpropmass_earth_entry+self.Lpropmass_moon_exit+self.Lpropmass_LLO_inclination)-\
            self.dry-self.PL-self.Lpropmass_earth_entry-self.Lpropmass_moon_exit-self.Lpropmass_LLO_inclination
        self.Lpropmass_lunar_launch = m.exp(self.deltaV_lunar_landing/(self.g0*self.Isp))*\
            (self.dry+self.Isp+self.Lpropmass_earth_entry+self.Lpropmass_moon_exit+self.Lpropmass_LLO_inclination+self.Lpropmass_lunarhohmann)-\
            self.dry-self.Isp-self.Lpropmass_earth_entry-self.Lpropmass_moon_exit-self.Lpropmass_LLO_inclination-self.Lpropmass_lunarhohmann

        self.totalpropmass_earth_journey = self.Lpropmass_earth_entry+self.Lpropmass_moon_exit+self.Lpropmass_LLO_inclination+\
            self.Lpropmass_lunarhohmann+self.Lpropmass_lunar_launch
        self.additionalfuel_earth_journey = 0.1*self.totalpropmass_earth_journey

        return self.totalpropmass_earth_journey

    def transfertime(self):
        self.LEO_period = 2*np.pi*np.sqrt((self.LEO_radius*1000)**3/self.mu_earth)/60
        self.LEO_revolutions = m.ceil(self.totalpropmass_moon_journey/self.data.launch_system__max_payload_mass)+1
        self.total_LEO_time = self.LEO_revolutions*self.LEO_period

        self.earth_hohmann_period = np.pi*np.sqrt((self.smajor_earth_hohmann*1000)**3/self.mu_earth)/60

        self.moon_hohmann_period = np.pi*np.sqrt((self.smajor_moon_hohmann*1000)**3/self.mu_moon)/60

        self.LLO_period = 2*np.pi*np.sqrt((self.LLO_radius*1000)**3/self.mu_moon)/60
        self.LLO_revolutions = 1

        self.total_LLO_time = self.LLO_period*self.LLO_revolutions

        self.total_transfer_time = self.total_LEO_time+self.earth_hohmann_period+self.moon_hohmann_period+self.total_LLO_time

    def program(self, starship, ariane):
        self.orbitcharacteristics()
        self.deltaV()
        self.propellantmass(starship, ariane)
        self.transfertime()

        if starship==True:
            print("---------------------------STARSHIP---------------------------------------")
        elif ariane==True:
            print("---------------------------Ariane 64----------------------------------\n")

        print("---------------------------Orbital Parameters-----------------------------\n",
              "LEO Height: ", self.LEO_height, "km"
              "\nLEO Radius: ", self.LEO_radius, "km",
              "\nEarth Hohmann Perigee: ", self.earth_hohmann_per, "km",
              "\nEarth Hohmann Apogee: ", self.earth_hohmann_apo, "km",
              "\nEarth Hohmann Semi-major Axis: ", self.smajor_earth_hohmann, "km",
              "\nMoon Hohmann Perigee: ", self.moon_hohmann_per, "km",
              "\nMoon Hohmann Apogee: ", self.moon_hohmann_apo, "km",
              "\nMoon Hohmann Semi-major Axis: ", self.smajor_moon_hohmann, "km",
              "\nLLO Height: ", self.LLO_height, "km",
              "\nLLO Radius: ", self.LLO_radius, "km",
              "\n-------------------------------DeltaV------------------------------------\n",
              "\n Payload Mass: ", self.PL, "kg",
              "\n Earth Exit: ", self.deltaV_earth_exit, "m/s",
              "\n Propellant Needed: ", self.Epropmass_earth_exit, "kg",
              "\n Lunar SOI Entry: ", self.deltaV_lunar_entry, "m/s",
              "\n Propellant Needed: ", self.Epropmass_moon_entry, "kg"
              "\n Lunar Inclination Change: ", self.deltaV_lunar_inclination, "m/s",
              "\n Propellant Needed: ", self.Epropmass_LLO_inclination, "kg"
              "\n LLO Circulization: ", self.deltaV_LLO_circulization, "m/s",
              "\n Propellant Needed: ", self.Epropmass_LLO_circulization, "kg"
              "\n Lunar Landing: ", self.deltaV_lunar_landing, "m/s",
              "\n Propellant Needed: ", self.Epropmass_lunar_landing, "kg",
              "\n-------------------------------------------------------------------------\n",
              "\n Total Mission DeltaV Budget: ", self.total_deltaV, "m/s",
              "\n Total Propellant Required (Refuel in LEO): ", self.totalpropmass_moon_journey, "kg",
              "\n Additional Fuel for ContingencyL ", self.additionalfuel_moon_journey, "kg",
              "\n Total Transfer Time: ", self.total_transfer_time, "min or", self.total_transfer_time/(24*60), "days")
        if starship==True:
            print("Number of Refills Needed in LEO: ", self.LEO_revolutions-1)

Test = orbit()
Test.program(False, True)







