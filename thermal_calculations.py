import math as m
import numpy as np
from commondata import CommonData

class ThermalControl():

    def __init__(self):
        self.data = CommonData()

        self.power_draw_MMAC = 240


        self.total_calc()
        # self.data.code_finisher()

    def calculate_surface_length(self):

        self.angle_underground = 2 * np.cos(2/3)
        self.angle_exposed = 2 * m.pi - self.angle_underground

        self.l_exposed = self.data.habitat__radius * self.angle_exposed
        self.l_underground = self.data.habitat__radius * self.angle_underground

        self.l_exposed_sunlit = self.l_exposed / 2
        self.l_exposed_shadow = self.l_exposed_sunlit

    def calculate_surface_area(self):

        self.crosssection_underground = 0.5 * pow(self.data.habitat__radius, 2) * \
                                        (self.angle_underground - np.sin(self.angle_underground))

        self.crosssection_exposed = m.pi * pow(self.data.habitat__radius, 2) - self.crosssection_underground

        self.area_exposed = self.l_exposed * self.data.habitat__length + (2 * self.crosssection_exposed)

        self.area_underground = self.l_underground * self.data.habitat__length + 2 * self.crosssection_underground

        self.area_sunlit = self.l_exposed_sunlit * self.data.habitat__length

        self.area_shadow = self.l_exposed_shadow * self.data.habitat__length + 2 * self.crosssection_exposed

    def calculate_temp_differences(self):

        self.dT_day = self.data.moon__incident_temp_day - self.data.habitat__inside_temp
        self.dT_day_shadow = self.data.moon__incident_temp_day - self.data.habitat__inside_temp

        self.dT_night = self.data.moon__incident_temp_night - self.data.habitat__inside_temp

        self.dT_underground = self.data.moon__subsurface_temp - self.data.habitat__inside_temp

    def calculate_conductivity(self):

        self.exposed_conductivity = 1 / \
            (1 / self.data.regolith__heat_radiation_dose + \
            self.data.regolith__thickness / self.data.regolith__thermal_conductivity + \
            self.data.layers__thickness_insulation / self.data.layers__insulation_thermal_conductivity + \
            1 / self.data.habitat__heat_transmission_coefficient)

        self.underground_conductivity = 1 / \
            (1 / self.data.regolith__subsurface_thermal_conductivity + \
            self.data.layers__thickness_insulation / self.data.layers__insulation_thermal_conductivity + \
            1 / self.data.habitat__heat_transmission_coefficient)
        
    def calculate_temperature_gradient(self):

        self.exposed_temperature_day = self.dT_day * self.exposed_conductivity

    def calculate_heat_flow_night(self):

        self.heat_flow_underground = self.underground_conductivity * self.area_underground * self.dT_underground

        self.heat_flow_night = self.exposed_conductivity * self.area_exposed * self.dT_night + \
            self.underground_conductivity * self.area_underground * self.dT_underground

        #print("Heat flow underground = ", self.heat_flow_underground)
        print("Heat flow at night = ", self.heat_flow_night)

    def calculate_heat_flow_day(self):

        self.heat_flow_day = self.exposed_conductivity * self.area_sunlit * self.dT_day + \
            self.exposed_conductivity * self.area_shadow * self.dT_day_shadow + \
            self.underground_conductivity * self.area_underground * self.dT_underground

        print("Heat flow at day = ", self.heat_flow_day)

    def calculate_body_heat(self):

        self.astronaut_body_heat = 250


    def calculate_internal_heatgains(self):

        self.equipment_heat_day = 3800
        self.equipment_heat_night = 4700

        self.internal_heat_day = self.equipment_heat_day + self.astronaut_body_heat * 4
        self.internal_heat_night = self.equipment_heat_night + self.astronaut_body_heat * 4

        print("Internal heat day = ", self.internal_heat_day)
        print("Internal heat night = ", self.internal_heat_night)

    def calculate_total_heat(self):

        self.total_heat_day = self.internal_heat_day + self.heat_flow_day + 4 * self.astronaut_body_heat
        self.total_heat_night = self.internal_heat_night + self.heat_flow_night + 4 * self.astronaut_body_heat

        print("total heat day = ", self.total_heat_day)
        print("total heat night = ", self.total_heat_night)

    def calculate_thermal_power(self):

        self.required_MMAC_units = 2

        self.thermal_power_budget = self.required_MMAC_units * self.power_draw_MMAC
        self.data.thermal__power_draw = self.thermal_power_budget
        #print("thermal power budget =", self.thermal_power_budget)

    def total_calc(self):

        self.calculate_surface_length()
        self.calculate_surface_area()
        self.calculate_temp_differences()
        self.calculate_conductivity()
        self.calculate_temperature_gradient()
        self.calculate_heat_flow_night()
        self.calculate_heat_flow_day()
        self.calculate_body_heat()
        self.calculate_internal_heatgains()
        self.calculate_total_heat()
        self.calculate_thermal_power()


Test = ThermalControl()
#print(Test)