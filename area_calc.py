import numpy as np
import math as m
import scipy as sp
import scipy.integrate as integrate

class Crosssection:
    def __init__(self,r,t,d) -> None:
        self.r = r
        self.t = t
        self.d = d

    def calculate_areas(self):
        self.side_big_sector = 0.5 * (self.r + self.t)**2 *(m.pi/2)
        # print("Side Big Sector:", self.side_big_sector)

        self.side_triangle = 0.5 * ((self.r+self.t)*(m.sqrt(2)/2)+(self.r-self.d))**2
        # print("Side Triangle:", self.side_triangle)

        self.side_segment = 0.5 * (self.r +self.t)**2 * ((m.pi/2)-1)
        # print("Side Side Segment:", self.side_segment)

        self.side_small_triangle = 0.5 * ((m.sqrt(2)/2)*(self.r+self.t)-(self.r-self.d))**2
        # print("Side Small Triangle:", self.side_small_triangle)

        self.side_small_sector = 0.5 * (m.pi/2)*(self.r)**2
        # print("Side Small Sector:", self.side_small_sector)

        self.top_big_sector = 0.5 * (self.r+self.t)**2 * (m.pi/4)
        # print("Top Big Sector:", self.top_big_sector)

        self.top_small_sector = 0.5 * (self.r)**2 *(m.pi/4)
        # print("Top Small Sector:", self.top_small_sector)

        if (self.r - self.d) > (m.sqrt(2)/2)*self.r: 
            self.bottom_small_triangle = 0.5 * ((self.r-self.d)-(m.sqrt(2)*0.5*self.r))**2
            # print("Bottom Small Triangle:", self.bottom_small_triangle)

            x1 = (self.r)*(m.sin(m.acos((self.r-self.d)/self.r)))
            # print("First Integration Limit:",x1)
            x2 = (m.sqrt(2)/2)*self.r
            # print("Second Integration Limit:",x2)
            self.bottom_zone = abs((integrate.quad(lambda x: (self.r-self.d)-m.sqrt((self.r)**2 -x**2), x1, x2))[0])
            # print("Small Bottom Zone:", self.bottom_zone)
        else:
            self.bottom_small_triangle = 0
            self.bottom_zone = 0

    def total_area(self):
        self.calculate_areas()
        self.total_area = 2*(self.side_big_sector + self.side_triangle - self.side_segment - self.side_small_triangle - self.side_small_sector + self.top_big_sector - self.top_small_sector + self.bottom_small_triangle + self.bottom_zone)
        # print("Total Area:",self.total_area)
        return self.total_area