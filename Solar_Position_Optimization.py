"""
Created on Fri May 28 2021

@author: Ernesto Hof
"""

#importing packages
import numpy as np
import matplotlib.pyplot as plt
from commondata import CommonData
import math as m

class PVArrays():
    def __init__(self):
        # Importing the commondata file
        self.data = CommonData()

        self.longest_illumination = 233 #days
        self.longest_darkness = 4.5 #days
        self.design_longest_darkness = 8 #days
        self.illumination_2m = 88 #percent of lunar year
        self.illumination_10m = 92 #percent of lunar year

        self.tower_height = 10 #m
        self.tower_width = 2 #m
        self.ground_clearance = 2 #m
        self.number_of_panels_per_tower = 8

        self.outer_support_beam_thickness = 20 #mm #square shape
        self.inner_support_beam_width = 5 #mm
        self.inner_support_beam_thickness = 2 #mm
        self.front_cover_thickness = 6.5 #mm
        self.back_cover_thickness = 5 #mm

        self.solarflower_rhombus_width = 3.5 #m
        self.solarflower_tube_radius = 15 #mm
        self.solarflower_tube_thickness = 5 #mm

        self.safety_factor_structures = 1.5
        self.safety_factor_energy = 2.5

        self.support_material_density = 2810 #kg/m3 #aluminium
        self.back_cover_material_density = 2000 #kg/m3 #CFPR
        self.front_cover_material_density = 2500 #kg/m3 #Tempered glass

        self.cable_density = 1.4  #km/m, from submarine cables (1400 kg per 1000 m)
        self.resistivity_silver = 15.87*10**(-9) #Ohm*meter
        self.cable_radius = 5 #mm

        self.voltage_required = 600 #V DC

        self.power_required_nominal = self.data.habitat__day_peak_power / 1000
        self.power_required_manufacturing = (self.data.all_logistics__power_draw/(1-0.02)**2)/1000 #kW #taking into account a 2% degradation over two years #GET FROM GUI
        self.power_required = max(self.power_required_nominal,self.power_required_manufacturing)

        self.distance_landing_habitat = 1.9 #km
        self.distance_habitat_solar = 1.9 #km
        self.actual_distance_landing_habitat = 2.5 #km\

        self.deployment_time_panels = 60 #s
        self.deployment_time_sunflower = 60 #s
        self.box_dimensions = [3.5,2,0.5]

        self.runprogram('max',False)
        self.data.code_finisher()

    def shadow(self,maxmin):
        self.inclination = np.deg2rad(5)  # radians
        #maxmin is false when the minimum solar inclination is required
        if maxmin == 'min':
            self.inclination = np.deg2rad(0.01)  # radians
        self.shadow_radius = self.tower_height/np.tan(self.inclination)
        self.shadow_diameter = 2*self.shadow_radius
        self.shadow_area = np.pi*self.shadow_radius**2

        #print("Radius of solar tower shadow cone: ", self.shadow_radius, "m")

    def power(self, inclination):
        #if inclination is true, this means the solar arrays are inclined to receive perpendicular solar rays
        self.area_per_tower = (self.tower_height-self.ground_clearance)*self.tower_width
        if inclination == True:
            self.area_required = self.power_required*1000/(self.data.moon__solar_constant*
                                                      self.data.solar__cell_absorptivity*0.01*self.data.solar__cell_avg_efficiency_bol)
            self.number_of_towers = m.ceil(self.area_required/self.area_per_tower)
            self.power_per_tower = self.area_per_tower*self.data.moon__solar_constant*\
                            self.data.solar__cell_absorptivity*0.01*self.data.solar__cell_avg_efficiency_bol

        else:
            self.area_required = self.power_required*1000/(self.data.moon__solar_constant*
            self.data.solar__cell_absorptivity*0.01*self.data.solar__cell_avg_efficiency_bol*np.cos(self.inclination))

            self.number_of_towers = m.ceil(self.area_required/self.area_per_tower)
            self.power_per_tower = self.area_per_tower * self.data.moon__solar_constant*\
                            self.data.solar__cell_absorptivity * 0.01 * self.data.solar__cell_avg_efficiency_bol*np.cos(self.inclination)

        self.total_power = self.number_of_towers*self.power_per_tower

        #print("Total area needed: ",self.area_required, "m2")
        #print("Total number of towers: ", self.number_of_towers)
        #print("Power produced per tower: ", self.power_per_tower, "W")
        #print("Total power produced: ", self.total_power, "W")


    def gridfinding(self, numberoftowers):
        self.grid = [0,0]
        self.current_min = 2*self.shadow_radius*(self.number_of_towers+1)*self.shadow_radius
        for i in range(1,numberoftowers+1):
            N = i
            M = numberoftowers/i
            if M.is_integer()==True:
                self.area = (N+1)*self.shadow_radius*(M+1)*self.shadow_radius
                ##print(self.area)
                ##print(N,"x", M)
            if self.area < self.current_min:
                self.current_min = self.area
                self.grid = [int(N),int(M)]
        return self.grid, self.area

    def optimallayout(self):
        self.grid = self.gridfinding(self.number_of_towers)[0]
        if sum(self.grid)==0:
            self.grid1, areacheck1 = self.gridfinding(self.number_of_towers+1)
            self.grid2, areacheck2 = self.gridfinding(self.number_of_towers-1)
            if areacheck1<areacheck2:
                self.grid1 = self.grid
            else:
                self.grid2 = self.grid
            # residual gives how much towers you are missing or have too much in the current grid, so if its negative
            # it means your current grid contains too few towers compared to the number you need for your power requirement
            self.residual = self.grid[0]*self.grid[1]-self.number_of_towers
            if self.residual !=0:
                print("GRID DOES NOT CONTAIN ALL SOLAR TOWERS, MISSING", -1*self.residual,"TOWER")

    def towerposition(self):
        self.xboundary = -0.5*(self.grid[1]-1)*self.shadow_radius
        self.yboundary = 0.5*(self.grid[0]-1)*self.shadow_radius
        self.xcoordinates = [self.xboundary]
        self.ycoordinates = [self.yboundary]
        self.coordinates = []
        for i in range(self.grid[1]-1):
            self.xcoordinates.append(self.xcoordinates[i]+self.shadow_radius)
        for j in range(self.grid[0]-1):
            self.ycoordinates.append(self.ycoordinates[j]-self.shadow_radius)
        for k in range(len(self.ycoordinates)):
            for n in range(len(self.xcoordinates)):
                self.coordinates.append([self.xcoordinates[n],self.ycoordinates[k]])
        #if (self.residual < 0)==True:
            #towerdirection = min(self.grid[0],self.grid[1])

    def PVelectricalsetup(self):
        self.number_of_cells_x = m.floor(self.tower_width/(self.data.solar__cell_xdimension/1000))
        self.number_of_cells_y = m.floor((self.tower_height-self.ground_clearance)/(self.data.solar__cell_ydimension/1000))
        self.total_number_of_cells = self.number_of_cells_x*self.number_of_cells_y

        self.number_of_cells_series = self.voltage_required/(self.data.solar__cell_maxpower_voltage_bol/1000)
        self.number_of_cells_series = self.number_of_cells_series
        self.voltage_supply = self.number_of_cells_series*self.data.solar__cell_maxpower_voltage_bol/1000

        self.number_of_cells_parallel = self.total_number_of_cells/self.number_of_cells_series
        self.current_supply = self.number_of_cells_parallel*self.data.solar__cell_maxpower_current_bol/1000
        self.actual_number_of_cells = self.number_of_cells_parallel*self.number_of_cells_series
        self.actual_cell_width = self.number_of_cells_x*self.data.solar__cell_xdimension/1000
        self.actual_cell_height = self.number_of_cells_y*self.data.solar__cell_ydimension/1000

        #print("Total number of solar cells per tower: ", self.actual_number_of_cells)
        #print("Voltage supply per tower: ", self.voltage_supply, "V")
        #print("Current supply per tower: ", self.current_supply, "A")

    def cablelength(self):
        self.PVelectricalsetup()
        self.internal_length = 0
        self.transmission_loss = 0
        self.minimum_list = []
        for i in range(len(self.coordinates)):
            self.cable_length = (self.coordinates[i][0] ** 2 + self.coordinates[i][1] ** 2) ** (0.5)
            self.internal_length += self.cable_length
            self.wire_resistance = self.resistivity_silver*self.cable_length/(np.pi*(self.cable_radius/1000)**2)
            self.transmission_loss += self.wire_resistance*self.current_supply**2
            self.minimum_list.append(self.cable_length)

        self.total_length = self.internal_length+self.distance_habitat_solar*1000
        self.cable_weight = self.total_length * self.cable_density
        self.cable_volume = (25/2000)**2*np.pi*self.total_length
        self.internal_cable_weight = (self.total_length-self.distance_habitat_solar*1000)*self.cable_density
        self.habitatsolar_cable_weight = self.distance_habitat_solar*1000*self.cable_density
        self.habitatsolar_cable_volune = self.distance_habitat_solar*1000*(25/2000)**2*np.pi
        #if self.residual != 0:
            ##print("ADD FINAL CABLE MANUALLY TO MASS AND VOLUME")
            
        #print("Total High-Power cable length: ", self.total_length, " m")
        #print("Total cable weight: ", self.cable_weight, "kg") #ADD TO GUI
        self.data.solar__total_cable_mass = self.cable_weight
        #print("Total cable volume: ", self.cable_volume, "m3") #ADD TO GUI
        self.data.solar__total_cable_volume = self.cable_volume
        #print("Total transmission losses: ", self.transmission_loss, "W")

    def PVmass(self):
        self.cell_mass = self.data.solar__cell_area*self.data.solar__average_cell_weight/1000
        self.tower_cell_mass= self.actual_number_of_cells*self.cell_mass/1000

        self.outer_support_volume = (2*self.actual_cell_width*(self.outer_support_beam_thickness/1000)**2\
        +2*self.actual_cell_height*(self.outer_support_beam_thickness/1000)**2)
        self.outer_support_mass = self.outer_support_volume*self.support_material_density
        self.inner_support_volume = self.inner_support_beam_width*self.inner_support_beam_thickness/(1000**2)\
        *((self.number_of_cells_x-1)*self.actual_cell_height+(self.number_of_cells_y-1)*self.actual_cell_width)
        self.inner_support_mass = self.inner_support_volume*self.support_material_density

        self.front_cover_volume = self.actual_cell_width*self.actual_cell_height*self.front_cover_thickness/1000
        self.front_cover_mass = self.front_cover_volume*self.front_cover_material_density

        self.back_cover_volume = self.actual_cell_width*self.actual_cell_height*self.back_cover_thickness/1000
        self.back_cover_mass = self.back_cover_volume*self.back_cover_material_density
        self.panel_assembly_mass_total = self.tower_cell_mass+self.outer_support_mass+self.inner_support_mass\
        +self.front_cover_mass+self.back_cover_mass
        self.hinge_mass = 0.1*self.panel_assembly_mass_total
        self.panel_assembly_mass_total = self.panel_assembly_mass_total+self.hinge_mass

        self.panel_assembly_volume_total = self.outer_support_volume+self.inner_support_volume+\
            self.front_cover_volume+self.back_cover_volume
        self.cell_volume = 0.1*self.panel_assembly_volume_total
        self.panel_assembly_volume_total = self.panel_assembly_volume_total+self.cell_volume
        #print(self.panel_assembly_volume_total)

        #assume solar flower is scissor like structure made from CFPR
        self.solarflower_rhombus_height = self.actual_cell_height/self.number_of_panels_per_tower
        self.solarflower_tube_length = (self.solarflower_rhombus_height+self.solarflower_rhombus_width+\
                                       4*np.sqrt((0.5*self.solarflower_rhombus_height)**2+(0.5*self.solarflower_rhombus_width)**2))\
                                       *self.number_of_panels_per_tower
        self.solarflower_tube_area = (m.pi*self.solarflower_tube_radius**2-m.pi*\
                                     (self.solarflower_tube_radius-self.solarflower_tube_thickness)**2)/(1000**2)

        self.solarflower_volume = self.solarflower_tube_length*self.solarflower_tube_area

        self.solarflower_mass = self.solarflower_volume*self.back_cover_material_density
        self.solarflower_aux_system_mass = 0.1*self.solarflower_mass
        self.solarflower_mass = self.solarflower_mass+self.solarflower_aux_system_mass
        self.solartower_total_mass = (self.solarflower_mass+self.panel_assembly_mass_total)*self.safety_factor_structures
        self.solartower_total_volume = (self.solarflower_volume+self.panel_assembly_volume_total)*self.safety_factor_structures

        self.total_solarfarm_mass = self.solartower_total_mass*self.number_of_towers+self.internal_cable_weight
        self.total_solarfarm_volume = self.box_dimensions[0]*self.box_dimensions[1]*self.box_dimensions[2]*self.number_of_towers

        #print("Total mass of single solar tower: ", self.solartower_total_mass, "kg")
        #print("Total volume of single solar tower: ", self.solartower_total_volume, "m3")
        print("Total mass of entire solar farm: ", self.total_solarfarm_mass, "kg") #ADD TO GUI
        self.data.solar__total_farm_mass = self.total_solarfarm_mass
        # print("Total volume of entire solar farm: ", self.total_solarfarm_volume, "m3") #ADD TO GUI
        self.data.solar__total_farm_volume = self.total_solarfarm_volume
        print("Habitat-Solar Cable Weight: ", self.habitatsolar_cable_weight, "kg")
        print("Habitat-Solar Cable Volume: ", self.habitatsolar_cable_volune, "kg")
        print("ONLY THIS MASS AND VOLUME IS EXCLUDED IN THE TOTAL SOLAR FARM MASS AS IT'S PACKED SEPERATELY IN THE LV")

        self.data.solar__total_mass = self.total_solarfarm_mass + self.habitatsolar_cable_weight
        self.data.solar__total_volume = self.total_solarfarm_volume + self.habitatsolar_cable_volune

    def PVsetupenergy(self):
        self.number_of_trips = max(m.ceil((self.total_solarfarm_mass+self.cable_weight)/self.data.athlete__mass_capacity)/2,1)
        self.travel_time = (self.distance_habitat_solar+self.distance_landing_habitat)*1000\
        /(self.data.athlete__velocity/4)+(min(self.minimum_list)/self.data.athlete__velocity/4)

        self.energy_req_landing_solar_farm = self.travel_time*self.data.athlete__power_draw*2

        #energy required for the erection of the solarflower
        self.energy_req_solarflower = self.solarflower_mass*self.data.moon__gravity*(self.tower_height/2)*self.safety_factor_energy
        #energy required for the erection of the solar panels
        self.energy_req_solarpanels = self.panel_assembly_mass_total*self.data.moon__gravity*\
                                      (self.ground_clearance+(self.tower_height-self.ground_clearance)/2)*self.safety_factor_energy
        self.energy_req_crane = self.data.crane__power_draw*(self.deployment_time_panels+self.deployment_time_sunflower)

        #power required for solarflower erection
        self.power_req_solarflower = self.energy_req_solarflower/self.deployment_time_sunflower
        #power required for solar panels erection
        self.power_req_solarpanels = self.energy_req_solarpanels/self.deployment_time_panels

        self.total_solarfarm_set_up_time = self.travel_time+self.internal_length/(self.data.athlete__velocity/4)+\
            self.number_of_towers*(self.deployment_time_panels+self.deployment_time_sunflower)*2

        self.total_power_needed = self.data.athlete__power_draw*2+self.data.crane__power_draw+\
        self.power_req_solarpanels+self.power_req_solarflower

        self.total_energy_needed = self.energy_req_landing_solar_farm+self.energy_req_solarpanels+self.energy_req_solarflower+\
            self.energy_req_crane

        #print("Total travel time from landing site to solar farm position: ", self.travel_time/60, "minutes")
        #print("Power required for solar tower erection: ",self.total_power_needed) 
        #print("Total time to set up the solar farm: ", self.total_solarfarm_set_up_time/60, "minutes") #ADD TO GUI
        self.data.solar__farm_setup_time = self.total_solarfarm_set_up_time/60
        #print("Energy needed for the erection of one solar tower: ", self.energy_req_solarpanels+self.energy_req_solarpanels+self.energy_req_crane, "J")
        #print("Total energy needed to set up solar farm before being self-sustaining: ", self.total_energy_needed/1000, "kJ")
        #print("Power required to set up solar farm: ", 4000+self.power_req_solarflower+self.power_req_solarpanels, "W") #ADD TO GUI
        self.data.solar__farm_setup_power = 4000+self.power_req_solarflower+self.power_req_solarpanels


    def plotting(self):
        fig,ax = plt.subplots()
        for i in range(len(self.coordinates)):
            plt.plot(self.coordinates[i][0],self.coordinates[i][1],'c',marker="X", ms=10)
            plt.plot([self.coordinates[i][0],0],[self.coordinates[i][1],0],'b')

        circle = plt.Circle((self.coordinates[0][0], self.coordinates[0][1]),
                            self.shadow_radius, color='gray', label='Shadow Cone')
        ax.add_patch(circle)
        plt.plot(0,0,'r',marker="H", ms=25, label="Power Accumulation Point")
        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.title("Solar Tower Grid")
        plt.legend(loc='best')
        #plt.show
        plt.close()

    def cablefitting(self):
        self.radius = 1
        self.cable_perimeter = 0
        while self.radius > 0:
            self.cable_perimeter += 2 * np.pi * self.radius
            self.radius -= 25 / 1000
        #print(self.cable_perimeter)

    def runprogram(self,maxmin,inclination):
        self.shadow(maxmin)
        self.power(inclination)
        self.optimallayout()
        self.towerposition()
        self.cablelength()
        self.plotting()
        self.PVelectricalsetup()
        self.PVmass()
        self.PVsetupenergy()
        self.cablefitting()


if __name__ == "__main__":
    Test = PVArrays()
    # Test.runprogram('max',False)