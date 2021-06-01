import pandas as pd
from csv import writer
import csv
from area_calc import truncate
import os

class CommonData():

    
    def __init__(self) -> None:
        
        self.read_csv('data.csv')
        self.df_tab_organizer()
        self.csv_to_attributes()

        # print(list(filter(lambda item: item not in ['df', 'tab_names', 'subtabs'] , list(self.__dict__.keys()))))

    def read_csv(self, file_name):
        dir_path = os.getcwd()
        csv_path = dir_path+"\\data.csv"
        self.df = pd.read_csv(csv_path)

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
        new_row = {'group':tab_name, 'object':subtab_name, 'param':param, 'value':float(value), 'units':unit}
        self.df = self.df.append(new_row, ignore_index=True)

    def get_tab_from_subtab(self, subtab_name):
        filtered = self.df.loc[self.df['object']== subtab_name]
        return filtered.group.values[0]

    def reverse_name_cleaner(self, entry):
        out = entry.replace(" ", "_")
        out = out.lower()
        return out

    def csv_to_attributes(self):
        self.read_csv('data.csv')
        objects = list(self.df.object.values)
        params = list(self.df.param.values)
        values = list(self.df.value.values)

        for i in range(len(objects)):
            attr_name = f"{objects[i]}__{params[i]}"
            setattr(self, attr_name, values[i])

    def attributes_to_df(self):
        keys = list(self.__dict__.keys())
        filtered = list(filter(lambda item: item not in ['df', 'tab_names', 'subtabs', 'missing_keys'] ,keys))
        self.missing_keys = []

        for key in filtered:

            value = getattr(self, key)
            key = key.split("__")
            object = key[0]
            param = key[1]

            if self.df.loc[(self.df['object']==object) & (self.df['param']==param)].size > 0:
                row = self.df.index[(self.df['object']==object) & (self.df['param']==param)].tolist()[0]
                self.df.iat[row, 3] = truncate(value, decimals=3)

            else:
                self.missing_keys.append(key)
        
        if len(self.missing_keys) > 0:
            print("Missing following parameters in csv:\n", *self.missing_keys)

    def code_finisher(self):
        self.attributes_to_df()
        if len(self.missing_keys) == 0:
            print("All keys found! Writing results to csv.")
            self.df_to_csv('data.csv')