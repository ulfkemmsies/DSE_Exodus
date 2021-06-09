from tkinter import Label
from matplotlib import scale
from matplotlib.colors import to_rgba_array
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
from commondata import CommonData
import unittest


class NPV():

    def __init__(self,trials):
        self.trials = trials
        self.data = CommonData()
        self.create_distros()
        self.assign_vars()
        # self.print_distro(self.ebp_leo_cost_distro, trials=self.trials)
        # self.print_all_distros(trials)
        self.create_case_array()

    def create_distros(self):
        self.init_hab_investment_distro = stats.lognorm(s=0.3, loc=self.data.habitat__init_investment/2, scale=self.data.habitat__init_investment)
        self.hab_operational_cost_distro = stats.lognorm(s=0.3, loc=self.data.habitat__operational_cost/2, scale=self.data.habitat__operational_cost)
        self.resupply_payload_distro = stats.norm(loc=self.data.habitat__resupply_payload, scale=0.1*self.data.habitat__resupply_payload)
        self.resupply_payload_refuel_distro = stats.norm(loc=self.data.habitat__resupply_payload_refueling, scale=0.1*self.data.habitat__resupply_payload_refueling)

        self.return_prop_distro = stats.norm(loc=self.data.launch_system__return_prop, scale=0.05*self.data.launch_system__return_prop)

        self.leo_init_demand_distro = stats.norm(loc=self.data.leo__init_demand, scale=0.05*self.data.leo__init_demand)
        self.leo_annual_growth_distro = stats.norm(loc=self.data.leo__annual_growth, scale=0.05*self.data.leo__annual_growth)
        self.leo_annual_launch_cost_decrease_distro = stats.norm(loc=self.data.launch_system__annual_cost_decrease, scale=0.05*self.data.launch_system__annual_cost_decrease)

        self.eml1_init_demand_distro = stats.norm(loc=self.data.eml1__init_demand, scale=0.05*self.data.eml1__init_demand)
        self.eml1_annual_growth_distro = stats.norm(loc=self.data.eml1__annual_growth, scale=0.05*self.data.eml1__annual_growth)

        self.lunar_surface_init_demand_distro = stats.norm(loc=self.data.lunar_surface__init_demand, scale=0.05*self.data.lunar_surface__init_demand)
        self.lunar_surface_annual_growth_distro = stats.norm(loc=self.data.lunar_surface__annual_growth, scale=0.05*self.data.lunar_surface__annual_growth)
        self.LS_annual_launch_cost_decrease_distro = stats.norm(loc=self.data.lunar_surface__annual_launch_cost_decrease, scale=0.05*self.data.lunar_surface__annual_launch_cost_decrease)

        self.prop_mine_specific_dev_cost_distro = stats.lognorm(s=0.3, loc=self.data.prop_mine__specific_dev_cost/2, scale=self.data.prop_mine__specific_dev_cost)
        self.prop_mine_specific_operational_cost_distro = stats.lognorm(s=0.3, loc=self.data.prop_mine__specific_operational_cost/2, scale=self.data.prop_mine__specific_operational_cost)
        self.prop_mine_specific_output_distro = stats.norm(loc=self.data.prop_mine__specific_output, scale=0.05*self.data.prop_mine__specific_output)
        self.prop_mine_resupply_payload_distro = stats.lognorm(s=0.3, loc=self.data.prop_mine__resupply_payload/2, scale=self.data.prop_mine__resupply_payload)

        self.equity_percent_distro = stats.uniform()
        self.init_market_share_distro = stats.uniform(loc=0.5, scale=0.5)
        self.market_share_change_distro = stats.norm(loc=self.data.prop_mine__market_share_change_rate, scale=0.05*self.data.prop_mine__market_share_change_rate)
        self.discount_rate_distro = stats.norm(loc=self.data.prop_mine__discount_rate, scale=0.75*self.data.prop_mine__discount_rate)
        self.market_undercut_distro = stats.uniform(loc=0.5, scale=0.5)

        self.ebp_leo_cost_distro = stats.beta(a=1.5, b=3, loc=self.data.ebp__leo_cost/10, scale=self.data.ebp__leo_cost*1.5)
        self.ebp_production_cost_distro = stats.lognorm(s=0.3, loc=self.data.ebp__production_cost/2, scale=self.data.ebp__production_cost)

        self.mbp_production_cost_distro = stats.lognorm(s=0.3, loc=self.data.mbp__production_cost/2, scale=self.data.mbp__production_cost)
        self.mbp_annual_cost_decrease_distro = stats.norm(loc=self.data.mbp__annual_cost_decrease, scale=0.05*self.data.mbp__annual_cost_decrease)

    def assign_vars(self):

        self.init_hab_investment = self.trunc_sample(self.init_hab_investment_distro, min=0)
        self.hab_operational_cost = self.trunc_sample(self.hab_operational_cost_distro)
        self.resupply_payload = self.trunc_sample(self.resupply_payload_distro)
        self.resupply_payload_refuel = self.trunc_sample(self.resupply_payload_refuel_distro)

        self.return_prop_investment = self.trunc_sample(self.return_prop_distro)

        self.leo_init_demand = self.trunc_sample(self.leo_init_demand_distro)
        self.leo_annual_growth = self.trunc_sample(self.leo_annual_growth_distro)
        self.leo_annual_launch_cost_decrease = self.trunc_sample(self.leo_annual_launch_cost_decrease_distro)

        self.eml1_init_demand = self.trunc_sample(self.eml1_init_demand_distro)
        self.eml1_annual_growth = self.trunc_sample(self.eml1_annual_growth_distro)

        self.lunar_surface_init_demand = self.trunc_sample(self.lunar_surface_init_demand_distro)
        self.lunar_surface_annual_growth = self.trunc_sample(self.lunar_surface_annual_growth_distro)
        self.LS_annual_launch_cost_decrease = self.trunc_sample(self.LS_annual_launch_cost_decrease_distro)

        self.prop_mine_specific_dev_cost = self.trunc_sample(self.prop_mine_specific_dev_cost_distro)
        self.prop_mine_specific_operational_cost = self.trunc_sample(self.prop_mine_specific_operational_cost_distro)
        self.prop_mine_specific_output = self.trunc_sample(self.prop_mine_specific_output_distro)
        self.prop_mine_resupply_payload = self.trunc_sample(self.prop_mine_resupply_payload_distro)

        self.equity_percent = self.trunc_sample(self.equity_percent_distro)
        self.init_market_share = self.trunc_sample(self.init_market_share_distro)
        self.market_share_change = self.trunc_sample(self.market_share_change_distro)
        self.discount_rate = self.trunc_sample(self.discount_rate_distro)
        self.market_undercut = self.trunc_sample(self.market_undercut_distro)

        self.ebp_production_cost = self.trunc_sample(self.ebp_production_cost_distro)
        self.ebp_leo_cost = self.trunc_sample(self.ebp_leo_cost_distro) * self.ebp_production_cost
        self.ebp_eml1_cost = 3 * self.ebp_leo_cost
        self.ebp_ls_cost = 12 * self.ebp_leo_cost        

        self.mbp_production_cost = self.trunc_sample(self.mbp_production_cost_distro)
        self.mbp_leo_cost = 6 * self.mbp_production_cost
        self.mbp_leo_cost_aerobraking = 3 * self.mbp_production_cost
        self.mbp_eml1_cost = 2 * self.mbp_production_cost
        self.mbp_annual_cost_decrease = self.trunc_sample(self.mbp_annual_cost_decrease_distro)

    def print_distro(self, distro, trials, min=None, max=None, title=None):
        r = self.trunc_sample(distro=distro, trials=trials, min=min, max=max)
        Q25 = np.percentile(np.sort(r), 25, interpolation = 'midpoint')
        Q75 = np.percentile(np.sort(r), 75, interpolation = 'midpoint')
        mean = np.sort(r).mean()
        std = np.sort(r).std()
        neg = distro.cdf(0).round(5)
        stdcdf = (distro.cdf(mean+std).round(3) - distro.cdf(mean-std).round(3)).round(3)
        stdcdf2 = (distro.cdf(mean+2*std).round(3) - distro.cdf(mean-2*std).round(3)).round(3)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.hist(r, density=True, histtype='stepfilled', alpha=0.4, bins=20)
        ax.plot(np.sort(r), distro.pdf(np.sort(r)), label=f"negative cdf:{neg}")

        ax.axvline(x=Q25, color="green", ls='--', alpha=0.4, label="27/75 percentiles")
        ax.axvline(x=Q75, color="green", ls='--', alpha=0.4)

        ax.axvline(x=mean+std, color="red", ls='--', alpha=0.3, label="1/2 std devs.")
        ax.axvline(x=mean+2*std, color="red", ls='--', alpha=0.2)

        ax.axvline(x=mean-std, color="red", ls='--', alpha=0.3)
        ax.axvline(x=mean-2*std, color="red", ls='--', alpha=0.2)

        ax.axvline(x=mean, color="black", ls='--', alpha=0.4, label="mean")

        plt.text(mean, distro.pdf(mean), f"{mean.round(2)}")
        plt.grid(True, which='both', color='black', linestyle="--", linewidth=0.5, alpha=0.2)
        plt.minorticks_on()
        plt.title(f"{title}\n")
        plt.tight_layout()

        plt.legend()
        plt.savefig(fname=f"distro_plots/{title}.jpeg")
        # plt.show()

        plt.close(fig)
    
    def print_all_distros(self, trials):

        keys = list(self.__dict__.keys())
        filtered = list(filter(lambda item: item not in ['trials', 'data'] ,keys))

        for key in filtered:

            distro = getattr(self, key)
            if type(distro) == stats.distributions.rv_frozen:
                self.print_distro(distro, trials, title=str(key))

    def trunc_sample(self, distro, min=None, max=None, trials=1):
        rv = distro.rvs(size=trials)

        if min == None and max == None:
            if trials == 1:
                return rv[0]
            else:
                return rv

        elif min != None and max != None:
            if trials == 1 and rv >= min and rv <= max:
                return rv[0]

            elif trials == 1 and ((not rv >= min) or (not rv <= max)):
                while ((not rv >= min) or (not rv <= max)):
                    rv = distro.rvs()
                return rv[0]
            
            elif trials > 1:
                trunc = rv[rv<max]
                trunc = trunc[trunc>min]
                print("Truncated sample size: ",trunc.size)
                return trunc

        elif min == None and max != None:
            if trials == 1 and rv <= max:
                return rv[0]

            elif trials == 1 and not rv <= max:
                while not rv <= max:
                    rv = distro.rvs()
                return rv[0]
            
            elif trials > 1:
                trunc = rv[rv<max]
                print("Truncated sample size: ",trunc.size)
                return trunc

        elif min != None and max == None:
            if trials == 1 and rv >= min:
                return rv[0]

            elif trials == 1 and (not rv >= min):
                while (not rv >= min):
                    rv = distro.rvs()
                return rv[0]
            
            elif trials > 1:
                trunc = rv[rv>min]
                print("Truncated sample size: ",trunc.size)
                return trunc

    def create_case_array(self):

        year_index_0 = np.linspace(0,9, 10)
        LEO_demand = np.apply_along_axis(lambda n: self.leo_init_demand * (1+self.leo_annual_growth)**n, 0, year_index_0)
        EML1_demand = np.apply_along_axis(lambda n: self.eml1_init_demand * (1+self.eml1_annual_growth)**n, 0, year_index_0)
        lunar_surface_demand = np.apply_along_axis(lambda n: self.lunar_surface_init_demand * (1+self.lunar_surface_annual_growth)**n, 0, year_index_0)

        total_demand = LEO_demand + EML1_demand + lunar_surface_demand + self.data.launch_system__return_prop/1000
        demand_delta = np.array([total_demand[i] - total_demand[i-1] for i in range(len(total_demand))])
        demand_delta[0] = total_demand[0]

        ebp_leo_cost = np.apply_along_axis(lambda n: self.ebp_leo_cost * (1-self.leo_annual_launch_cost_decrease)**n, 0, year_index_0)
        ebp_eml1_cost = np.apply_along_axis(lambda n: self.ebp_eml1_cost * (1-self.leo_annual_launch_cost_decrease)**n, 0, year_index_0)
        ebp_lunar_surface_cost = np.apply_along_axis(lambda n: self.ebp_ls_cost * (1-self.leo_annual_launch_cost_decrease)**n, 0, year_index_0)

        discounted_ebp_leo_cost = self.discount_rate * ebp_leo_cost
        discounted_ebp_eml1_cost = self.discount_rate * ebp_eml1_cost
        discounted_ebp_lunar_surface_cost = self.discount_rate * ebp_lunar_surface_cost

        mbp_leo_cost = np.apply_along_axis(lambda n: self.mbp_leo_cost * (1-self.LS_annual_launch_cost_decrease)**n, 0, year_index_0)
        mbp_leo_cost_aerobraking = np.apply_along_axis(lambda n: self.mbp_leo_cost_aerobraking * (1-self.LS_annual_launch_cost_decrease)**n, 0, year_index_0)
        mbp_eml1_cost = np.apply_along_axis(lambda n: self.mbp_eml1_cost * (1-self.LS_annual_launch_cost_decrease)**n, 0, year_index_0)
        mbp_lunar_surface_cost = np.apply_along_axis(lambda n: self.mbp_production_cost * (1-self.mbp_annual_cost_decrease)**n, 0, year_index_0)

        market_share = np.apply_along_axis(lambda n: self.init_market_share * (1-self.market_share_change)**n, 0, year_index_0)

        prop_mine_mass = (demand_delta * 1000) / self.prop_mine_specific_output
        total_current_mine_mass = np.array([sum(prop_mine_mass[0:x:1]) for x in range(0, len(prop_mine_mass)+1)][1:])
        total_launch_mass = prop_mine_mass + self.resupply_payload_refuel + self.prop_mine_resupply_payload
        total_launch_mass[0]  = total_launch_mass[0] + self.data.habitat__total_mass

        launch_costs = total_launch_mass * self.ebp_ls_cost
        operational_costs = total_current_mine_mass * self.prop_mine_specific_operational_cost + self.hab_operational_cost
        yearly_costs = launch_costs + operational_costs

        

        # print(self.ebp_leo_cost)
        print(prop_mine_mass)
        print(total_current_mine_mass)
        print(operational_costs)




if __name__ == "__main__":
    test = NPV(50000)