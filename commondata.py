class CommonData():
    
    def __init__(self) -> None:
        
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
        self.kevlar_density = 1.47 #kg/m3
        self.kevlar_safety_factor = 1.5 