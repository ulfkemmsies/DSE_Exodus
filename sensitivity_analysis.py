import numpy as np
from numpy.core.fromnumeric import var
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
from commondata import CommonData
from RobotScaling import Robots
from Solar_Position_Optimization import PVArrays
from structural_calculation import Structure
from life_support import Life_Support
from NPV_calc import discrete_cdf
import unittest
from bisect import bisect_left
import time

class Anal_Sensitivity():
    def __init__(self):
        self.data = CommonData()

        self.df = self.data.df
        self.get_vars()

        self.var_list = []

        self.mass_var_list = ['total_mass__total_ls_mass']
        self.volume_var_list = ['habitat__airlock_volume']
        self.power_var_list = ['power1__comms_peak_power']
        self.time_var_list = []

        self.trials = 50
        # self.vars_to_pdf()
        # self.sample_from_pdfs()
        # self.print_all_distros(50000)

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
                setattr(self, non_distro_var_name, distro.rvs(size=1)[0])
                # print(str(non_distro_var_name),": ",getattr(self, non_distro_var_name))

    def sample_calc(self, var_list):

        self.vars_to_pdf(self.get_vars(var_list))
        self.sample_from_pdfs()

        self.converger(var_list)

        return self.outputs_calc()

    def outputs_calc(self):
        
        total_mass = sum(list(lambda key: float(getattr(self.data, key)) for key in self.mass_var_list))
        total_volume = sum(list(lambda key: float(getattr(self.data, key)) for key in self.volume_var_list))
        max_power = sum(list(lambda key: float(getattr(self.data, key)) for key in self.power_var_list))
        total_time = sum(list(lambda key: float(getattr(self.data, key)) for key in self.time_var_list))

        return total_mass, total_volume, max_power, total_time

    def converger(self, var_list):
        
        self.attributes_to_converge_arr(var_list=None, arr_name="init_value_array", local=False)

        self.total_runner(arr_name="constant_filter_array")

        non_constants = self.init_value_array[:,0][np.not_equal(self.init_value_array[:,1], self.constant_filter_array[:,1])]


        max_delta = 1

        while max_delta > 0.01:

            self.attributes_to_converge_arr(var_list=non_constants, arr_name="before_arr", local=False)

            self.total_runner(arr_name="after_arr")

            max_delta = self.arr_delta(self.before_arr, self.after_arr)

    def arr_delta(self, arr1, arr2):
        
        names_same = np.equal(arr1[:,0], arr2[:,0])
        vals1 = arr1[:,1][names_same]
        vals2 = arr2[:,1][names_same]

        largest_delta = np.amax((np.abs(vals1-vals2)/vals1))
        return largest_delta

    def total_runner(self):
        pass

    def attributes_to_converge_arr(self, var_list, arr_name, local=False):
        
        keys = self.get_vars(var_list)
        arr_out = np.array(keys)

        def getlocal(key):
            return float(getattr(self, key))

        def getabroad(key):
            return float(getattr(self.data, key))

        if local:
            vectorizedget = np.vectorize(getlocal)
            values = vectorizedget(arr_out)
        elif not local:
            vectorizedget = np.vectorize(getabroad)
            values = vectorizedget(arr_out)

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
        
        mass_results = np.zeros((1,self.trials))
        volume_results = np.zeros((1,self.trials))
        power_results = np.zeros((1,self.trials))
        time_results = np.zeros((1,self.trials))

        t0 = time.time()

        for i in range(self.trials):

            total_mass, total_volume, max_power, total_time = self.sample_calc(self.var_list)

            mass_results[i] = total_mass
            volume_results[i] = total_volume
            power_results[i] = max_power
            time_results[i] = total_time

            print(f"Successfully calculated {i}-th sample!")

        print(time.time() - t0, "seconds")

        self.print_output(mass_results, title="Total Mass Probability Distribution", x_axis="kg", y_axis="Relative Frequency")
        self.print_output(volume_results, title="Total Volume Probability Distribution", x_axis="m3", y_axis="Relative Frequency")
        self.print_output(power_results, title="Maximum Power Probability Distribution", x_axis="W", y_axis="Relative Frequency")
        self.print_output(time_results, title="Total Construction Time Probability Distribution", x_axis="days", y_axis="Relative Frequency")

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

        neg = cdf(0)
        ax.axvline(x=0, ls='-', alpha=0.3, label=f"Negative NPV Prob: {np.round(neg,4)}")

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