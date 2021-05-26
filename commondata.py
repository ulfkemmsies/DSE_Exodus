import pandas as pd
from csv import writer
import csv


class CommonData():

    
    def __init__(self) -> None:
        
        self.read_csv('data.csv')
        self.df_tab_organizer()

        self.launch_cost = 250000 #$/kg

        self.moon_gravity = 1.625

        self.allowable_radiation = 99
        self.total_radiation = 100
        self.attenuation_needed = self.allowable_radiation/self.total_radiation

        self.regolith_density = 1500 #kg/m3
        self.regolith_porosity = 45 #%
        self.regolith_cohesion = 2.35 
        self.regolith_internal_friction_angle = 18.5 #deg
        self.regolith_bearing_capacity = 31
        self.regolith_thermal_conductivity = 1
        self.regolith_specific_heat = 800
        self.regolith_specific_area = 0.9
        self.regolith_dose_reduction = 0.8 #% per g/cm2
        
        self.kevlar_youngs_modulus = 179 #GPa
        self.kevlar_ultimate_tensile = 3450 #MPa
        self.kevlar_breaking_tenacity = 3000 #MPa
        self.kevlar_dose_reduction = 5.5 #% per g/cm2
        self.kevlar_thermal_conductivity = 0.04 #W/mK
        self.kevlar_density = 1470 #kg/m3
        self.kevlar_safety_factor = 4 

    def read_csv(self, file_name):
        self.df = pd.read_csv(file_name)

    def append_to_df(self, new_row):
        self.df = self.df.append(new_row, ignore_index=True)

    def df_to_csv(self, file_name):
        out_file = self.df.to_csv(file_name, index=False)

    def df_tab_organizer(self):
        self.tab_names = self.df.group.unique()

    def df_subtab_creator(self,tab_name):
        self.subtabs = self.df.loc[self.df['group']== tab_name].object.unique()

    def param_getter(self, tab_name, subtab_name):
        filtered = self.df.loc[(self.df['group']== tab_name) & (self.df['object']== subtab_name)]
        return filtered

    def add_row(self, tab_name, subtab_name, param, value, unit):
        new_row = {'group':tab_name, 'object':subtab_name, 'param':param, 'value':value, 'units':unit}
        self.df = self.df.append(new_row, ignore_index=True)

    def get_tab_from_subtab(self, subtab_name):
        filtered = self.df.loc[self.df['object']== subtab_name]
        return filtered.group.values[0]

    def reverse_name_cleaner(self, entry):
        out = entry.replace(" ", "_")
        out = out.lower()
        return out