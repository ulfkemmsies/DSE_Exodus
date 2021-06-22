import numpy as np
from numpy.core.fromnumeric import var
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
from commondata import CommonData
from NPV_calc import discrete_cdf
import unittest
from bisect import bisect_left
import time

#import other modules
from RobotScaling import Robots
from Solar_Position_Optimization import PVArrays
from structural_calculation import Structure
from life_support import Life_Support
from Safehouse import Safehouse
from structural_v2 import StressRelated
from thermal_calculations import ThermalControl
from Power import PowerRelated



class Anal_Sensitivity():
    def __init__(self):
        self.data = CommonData()

        self.df = self.data.df
        self.get_vars()

        self.var_list = ['water_recovery__upa_recovery', 'water_recovery__wpa_recovery','gas_storage__airlock_cycles' ,'gas_storage__leakage_rate' , 'total_mass__ls_mass_excluding_water_and_gas', 'total_mass__total_ls_power', 'habitat__day_peak_power','habitat__night_avg_power','habitat__airlock_volume','habitat__safehouse_mass','habitat__safehouse_volume','habitat__extra_cargo_volume','habitat__extra_cargo_mass','rassor__power_draw','athlete__power_draw','robotarm__power_draw','bagging__power_draw', 'nipper__power_draw','solar__average_cell_weight', 'cell_avg_efficiency', 'power_storage__eff_fuel_cell', 'power_storage__life_support_h2_needed', 'power_storage__h2_tank_ref_propellant_mass', 'power_storage__h2_tank_ref_mass', 'power_storage__o2_tank_ref_propellant_mass', 'power_storage__o2_tank_ref', 'habitat__cylinders_mass', 'all_logistics__docking_station', 'all_logistics__internal_transporter_mass', 'habitat__cylinders_volume' , 'all_logistics__internal_transporter_volume']

        self.mass_var_list = ['total_mass__total_ls_mass', 'habitat__inflatable_mass', 'all_logistics__total_mass', 'solar__total_mass', 'power_storage__total_mass', 'total_mass__total_ls_mass', 'habitat__safehouse_mass', 'habitat__extra_cargo_mass', 'habitat__cylinders_mass', 'all_logistics__docking_station', 'all_logistics__internal_transporter_mass']
        self.volume_var_list = ['habitat__airlock_volume', 'habitat__safehouse_volume', 'habitat__inflatable_volume', 'all_logistics__total_volume', 'solar__total_volume', 'power_storage__total_volume', 'total_mass__total_volume', 'habitat__extra_cargo_volume', 'habitat__cylinders_volume' , 'all_logistics__internal_transporter_volume']
        self.power_var_list = ['all_logistics__power_draw']

        self.trials = 500
        
        self.total_calc()

    def get_vars(self, key_list=None):
        keys = list(self.data.__dict__.keys())
        filtered = list(filter(lambda item: item not in ['df', 'tab_names', 'subtabs', 'missing_keys'] ,keys))
        if key_list != None:
            filtered = list(filter(lambda item: item in key_list ,filtered))
        # print(filtered)
        return filtered
        
    def vars_to_pdf(self, vars_list, uncertainty=0.2):
        for var in vars_list:
            value = getattr(self.data, var)
            distro_name = f"{var}_distro"
            distro = stats.norm(loc=value, scale=uncertainty*value)

            setattr(self, distro_name, distro)

    def sample_from_pdfs(self):
        keys = list(self.__dict__.keys())

        for key in keys:

            distro = getattr(self, key)
            if type(distro) == stats.distributions.rv_frozen:
                non_distro_var_name = key.replace("_distro", "")
                setattr(self.data, non_distro_var_name, distro.rvs(size=1)[0])
                # print(str(non_distro_var_name),": ",getattr(self, non_distro_var_name))

    def sample_calc(self, var_list=None):

        self.vars_to_pdf(self.get_vars(var_list))
        self.sample_from_pdfs()

        # self.print_all_distros(self.trials)
        self.total_runner()

        return self.outputs_calc()

    def outputs_calc(self):
        
    
        total_mass = sum([float(getattr(self.data, key)) for key in self.mass_var_list])
        total_volume = sum(list(float(getattr(self.data, key)) for key in self.volume_var_list))
        max_power = sum(list(float(getattr(self.data, key)) for key in self.power_var_list))

        print("Total Mass: ",total_mass)
        print("Total volume: ",total_volume)
        print("Construction Power Draw: ",max_power)

        return total_mass, total_volume, max_power

    def converger(self, var_list=None):
        
        self.attributes_to_converge_arr(var_list=None, arr_name="init_value_array", local=False)

        # self.total_runner(arr_name="constant_filter_array", var_list=var_list)

        # print("Init values: ", self.init_value_array[:,1])
        # print("Variables: " ,self.constant_filter_array[:,1])

        # bool_mask = np.not_equal(self.init_value_array[:,1], self.constant_filter_array[:,1])

        # print(bool_mask)

        # non_constants = self.init_value_array[:,0]


        max_delta = 1

        while max_delta > 0.01:

            self.attributes_to_converge_arr(var_list=var_list, arr_name="before_arr", local=False)

            self.total_runner(arr_name="after_arr", var_list=var_list)

            max_delta = self.arr_delta(self.before_arr, self.after_arr)
        
        print("Maximum Delta: ", max_delta)

    def arr_delta(self, arr1, arr2):
        
        # print(arr1[:5,0])
        # print(arr2[:5,0])
        # names_same = np.equal(arr1[:,0], arr2[:,0])
        vals1 = arr1[:,1][arr1[:,0] == arr2[:,0]].astype(float)
        vals2 = arr2[:,1][arr1[:,0] == arr2[:,0]].astype(float)
        
        ratios = np.abs(vals1/vals2)

        print(ratios)
        largest_delta = np.amax((ratios/vals1))
        return largest_delta

    def total_runner(self):
        Structure()
        StressRelated()
        ThermalControl()
        Robots(50,317,350,10,277)
        Life_Support()
        PVArrays()
        Safehouse()
        PowerRelated()

    def attributes_to_converge_arr(self, var_list, arr_name, local=False):
        
        keys = self.get_vars(var_list)
        arr_out = np.array(keys)

        if local:
            values = np.array([float(getattr(self, key)) for key in keys])

        elif not local:
            values = np.array([float(getattr(self.data, key)) for key in keys])

        length = len(list(arr_out))
        arr_out = np.reshape(arr_out, (length,1))
        values = np.reshape(values, (length,1))        
        values = values.astype(float)

        arr_out = np.hstack((arr_out, values))
        setattr(self, arr_name, arr_out)

    def print_all_distros(self, trials):

        keys = list(self.__dict__.keys())

        for key in keys:

            distro = getattr(self, key)
            if type(distro) == stats.distributions.rv_frozen:
                self.print_distro(trials, distro, title=str(key), x_axis="test", y_axis="Relative Frequency")
                
    def print_distro(self, trials, distro=None, title=None, x_axis=None, y_axis=None):
                
        r = np.sort(distro.rvs(size=trials))

        fig = plt.figure()
        ax = fig.add_subplot(111)

        # Adjust the subplots region to leave some space for the sliders and buttons
        # fig.subplots_adjust(left=0.25, bottom=0.25)

        #calculate interquartile range, mean and standard deviations
        # Q25 = np.percentile(np.sort(r), 25, interpolation = 'midpoint').round(2)
        # Q75 = np.percentile(np.sort(r), 75, interpolation = 'midpoint').round(2)
        # IQR = Q75 - Q25
        mean = np.sort(r).mean().round(2)
        std = np.sort(r).std().round(2)

        # Define an axes area and draw a slider in it
        # amp_slider_ax  = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=axis_color)
        # amp_slider = Slider(amp_slider_ax, 'Amp', 0.1, 10.0, valinit=amp_0)

        # Draw another slider
        # freq_slider_ax = fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=axis_color)
        # freq_slider = Slider(freq_slider_ax, 'Freq', 0.1, 30.0, valinit=freq_0)


        #if plotting pure distribution, calculate CDF of negative values and plot PDF
        neg = distro.cdf(0).round(5)

        ax.plot(np.sort(r), distro.pdf(np.sort(r)))
        plt.text(mean, distro.pdf(mean), f"{format(mean,'.1E')}")

        if x_axis !=None and y_axis != None:
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)

        # ax.axvline(x=Q25, color="green", ls='--', alpha=0.4, label=f"27/75 percentiles\nIQR: {format(IQR,'.1E')}")
        # ax.axvline(x=Q75, color="green", ls='--', alpha=0.4)

        ax.axvline(x=mean+std, color="red", ls='--', alpha=0.3, label=f"1/2 std devs.\n Std. Dev.: {format(std,'.1E')}")
        ax.axvline(x=mean+2*std, color="red", ls='--', alpha=0.2)

        ax.axvline(x=mean-std, color="red", ls='--', alpha=0.3)
        ax.axvline(x=mean-2*std, color="red", ls='--', alpha=0.2)

        ax.axvline(x=mean, color="black", ls='-', alpha=0.5, label=f"Mean: {format(mean,'.1E')}")

        # if distro == None and in_arr != None:
        #     cdf = discrete_cdf(np.sort(r))
        #     cdf_vals = [cdf(point) for point in np.sort(r)]
        #     billionyearlygain = np.round(cdf(1000000000),4)
        #     billionyearlygain2 = cdf(2000000000)
        #     billionyearlygain3 = cdf(3000000000)
        #     neg = cdf(0)
        #     billionyearlycost = cdf(-1000000000)
        #     billionyearlycost2 = cdf(-2000000000)
        #     billionyearlycost3 = cdf(-3000000000)
        #     billionyearlycost4 = cdf(-4000000000)
        #     billionyearlycost5 = cdf(-5000000000)
        #     ax.axvline(x=1000000000, ls='--', alpha=0.3, label=f"1+B€ Profit Prob: {np.round(1-billionyearlygain, 4)}\n2+B€ Profit Prob: {np.round(1-billionyearlygain2, 4)}\n3+B€ Profit Prob: {np.round(1-billionyearlygain3,4)}")
        #     ax.axvline(x=-1000000000, ls='--', alpha=0.3, label=f"1-B€ Costs Prob: {np.round(1-billionyearlycost,4)}\n2-B€ Costs Prob: {np.round(1-billionyearlycost2,4)}\n3-B€ Costs Prob: {np.round(1-billionyearlycost3,4)}\n4-B€ Costs Prob: {np.round(1-billionyearlycost4,4)}\n5-B€ Costs Prob: {np.round(1-billionyearlycost5,4)}")
        #     ax.axvline(x=0, ls='-', alpha=0.3, label=f"Negative NPV Prob: {np.round(neg,4)}")


        ax.hist(r, density=True, histtype='stepfilled', alpha=0.5, bins=100, label=f"{trials} samples")

        plt.grid(True, which='both', color='black', linestyle="--", linewidth=0.5, alpha=0.2)
        plt.minorticks_on()

        # title = name_cleaner(title)
        plt.title(f"{title}\n")

        plt.tight_layout()

        plt.legend()
        # plt.savefig(fname=f"distro_plots/{title}.jpeg", dpi=300)
        plt.show()
        

        plt.close(fig)

    def total_calc(self):
        
        mass_results = np.zeros(self.trials)
        volume_results = np.zeros(self.trials)
        power_results = np.zeros(self.trials)

        t0 = time.time()

        for i in range(self.trials):

            total_mass, total_volume, max_power = self.sample_calc(self.var_list)

            mass_results[i] = total_mass
            volume_results[i] = total_volume
            power_results[i] = max_power

            print(f"Successfully calculated {i}-th sample!")

        mass_results = mass_results[mass_results != 0]
        volume_results = volume_results[volume_results != 0]
        power_results = power_results[power_results != 0]

        print(time.time() - t0, "seconds")

        self.print_output(mass_results, title="Total Mass Probability Distribution", x_axis="kg", y_axis="Relative Frequency", min= 70000, max= 100000)
        self.print_output(volume_results, title="Total Volume Probability Distribution", x_axis="m3", y_axis="Relative Frequency", min= 250, max=650)
        self.print_output(power_results, title="Maximum Power Probability Distribution", x_axis="W", y_axis="Relative Frequency", min= 20000, max= 60000)

    def print_output(self, in_arr, title=None, x_axis=None, y_axis=None, min=None, max=None):

        r = in_arr
        r = np.sort(r)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        #calculate interquartile range, mean and standard deviations
        Q25 = np.percentile(np.sort(r), 25, interpolation = 'midpoint').round(2)
        Q75 = np.percentile(np.sort(r), 75, interpolation = 'midpoint').round(2)
        IQR = Q75 - Q25
        mean = np.sort(r).mean().round(2)
        std = np.sort(r).std().round(2)

        if x_axis !=None and y_axis != None:
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)

        ax.axvline(x=Q25, color="green", ls='--', alpha=0.4, label=f"27/75 percentiles\nIQR: {format(IQR,'.1E')}")
        ax.axvline(x=Q75, color="green", ls='--', alpha=0.4)

        ax.axvline(x=mean+std, color="red", ls='--', alpha=0.3, label=f"1/2 std devs.\n Std. Dev.: {format(std,'.1E')}")
        ax.axvline(x=mean+2*std, color="red", ls='--', alpha=0.2)

        ax.axvline(x=mean-std, color="red", ls='--', alpha=0.3)
        ax.axvline(x=mean-2*std, color="red", ls='--', alpha=0.2)

        ax.axvline(x=mean, color="black", ls='-', alpha=0.5, label=f"Mean: {format(mean,'.1E')}")

        cdf = discrete_cdf(np.sort(r))
        cdf_vals = [cdf(point) for point in np.sort(r)]

        # neg = cdf(0)
        # ax.axvline(x=0, ls='-', alpha=0.3, label=f"Negative NPV Prob: {np.round(neg,4)}")

        if min != None:
            ax.axvline(x=min, color="black", ls='-', alpha=0.8, label=f"Minimum: {format(min,'.1E')}\nMin CDF: {format(cdf(min),'.1E')}")

        if max != None:
            ax.axvline(x=max, color="black", ls='-', alpha=0.8, label=f"Maximum: {format(max,'.1E')}\nMax CDF: {format(cdf(max),'.1E')}")

        ax.hist(r, density=True, histtype='stepfilled', alpha=0.5, bins=100, label=f"{self.trials} samples\nBounded Prob. {cdf(max)-cdf(min)}")

        plt.grid(True, which='both', color='black', linestyle="--", linewidth=0.5, alpha=0.2)
        plt.minorticks_on()

        plt.title(f"{title}\n")

        plt.tight_layout()

        plt.legend()
        # plt.savefig(fname=f"sensitivity_analysis_plots/{title}.jpeg", dpi=300)
        plt.show()
        

        plt.close(fig)


if __name__ == "__main__":
    test = Anal_Sensitivity()