import numpy as np
import math as m
import scipy as sp
import scipy.integrate as integrate
import unittest


def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return m.trunc(number)

    factor = 10.0 ** decimals
    return m.trunc(number * factor) / factor


class Crosssection:
    def __init__(self,r,t,d) -> None:
        self.r = r
        self.t = t
        self.d = d

    def calculate_areas(self):
        self.side_big_sector = 0.5 * (self.r + self.t)**2 *(m.pi/2)

        self.side_triangle = 0.5 * ((self.r+self.t)*(m.sqrt(2)/2)+(self.r-self.d))**2

        self.side_segment = 0.5 * (self.r +self.t)**2 * ((m.pi/2)-1)

        self.side_small_triangle = 0.5 * ((m.sqrt(2)/2)*(self.r+self.t)-(self.r-self.d))**2

        self.side_small_sector = 0.5 * (m.pi/2)*(self.r)**2

        self.top_big_sector = 0.5 * (self.r+self.t)**2 * (m.pi/4)

        self.top_small_sector = 0.5 * (self.r)**2 *(m.pi/4)

        if (self.r - self.d) > (m.sqrt(2)/2)*self.r: 
            self.bottom_small_triangle = 0.5 * ((self.r-self.d)-(m.sqrt(2)*0.5*self.r))**2

            x1 = (self.r)*(m.sin(m.acos((self.r-self.d)/self.r)))

            x2 = (m.sqrt(2)/2)*self.r

            self.bottom_zone = abs((integrate.quad(lambda x: (self.r-self.d)-m.sqrt((self.r)**2 -x**2), x1, x2))[0])

        elif (self.r - self.d) < (m.sqrt(2)/2)*self.r:
            self.bottom_small_triangle = 0.5 * (-(self.r-self.d)+(m.sqrt(2)*0.5*self.r))**2

            x2 = (self.r)*(m.sin(m.acos((self.r-self.d)/self.r)))

            x1 = (m.sqrt(2)/2)*self.r

            self.bottom_zone = abs((integrate.quad(lambda x: -(self.r-self.d)+m.sqrt((self.r)**2 -x**2), x1, x2))[0])

        else:
            self.bottom_small_triangle = 0
            self.bottom_zone = 0

    def total_area(self):
        self.calculate_areas()
        self.total_cs_area = 2*(self.side_big_sector + self.side_triangle - self.side_segment - self.side_small_triangle - self.side_small_sector + self.top_big_sector - self.top_small_sector + self.bottom_small_triangle + self.bottom_zone)
        return self.total_cs_area


class CrossSectionTests(unittest.TestCase):

        def setUp(self):
            self.nofloor35 = Crosssection(3,5,0)
            self.nofloor35.total_area()
            self.floor35 = Crosssection(3,5,0.5)
            self.floor35.total_area()
            self.bigfloor35 = Crosssection(3,5,1)
            self.bigfloor35.total_area()

        def test_side_big_sector(self):
           self.assertEqual(truncate(self.nofloor35.side_big_sector,2), 50.26)

        def test_side_triangle(self):
           self.assertEqual(truncate(self.nofloor35.side_triangle,2),37.47)
           self.assertEqual(truncate(self.floor35.side_triangle,2),33.26)
           self.assertEqual(truncate(self.bigfloor35.side_triangle,2),29.31)
        
        def test_side_segment(self):
           self.assertEqual(truncate(self.nofloor35.side_segment,2),18.26)

        def test_side_small_triangle(self):
           self.assertEqual(truncate(self.nofloor35.side_small_triangle,2),3.52)
           self.assertEqual(truncate(self.floor35.side_small_triangle,2),4.98)
           self.assertEqual(truncate(self.bigfloor35.side_small_triangle,2),6.68)

        def test_side_small_sector(self):
           self.assertEqual(truncate(self.nofloor35.side_small_sector,2),7.06)

        def test_top_big_sector(self):
           self.assertEqual(truncate(self.nofloor35.top_big_sector,2),25.13)

        def test_top_small_sector(self):
           self.assertEqual(truncate(self.nofloor35.top_small_sector,2),3.53)

        def test_bottom_small_triangle(self):
           self.assertEqual(truncate(self.nofloor35.bottom_small_triangle,2),0.38)
           self.assertEqual(truncate(self.floor35.bottom_small_triangle,2),0.07)
           self.assertEqual(truncate(self.bigfloor35.bottom_small_triangle,2),0)

        def test_bottom_zone(self):
           self.assertEqual(truncate(self.nofloor35.bottom_zone,2),0.57)
           self.assertEqual(truncate(self.floor35.bottom_zone,2),0.08)
           self.assertEqual(truncate(self.bigfloor35.bottom_zone,2),0)

        def test_total_area(self):
           self.assertEqual(truncate(self.nofloor35.total_cs_area,2),162.87)
           self.assertEqual(truncate(self.floor35.total_cs_area,2),149.93)
           self.assertEqual(truncate(self.bigfloor35.total_cs_area,2),138.34)

if __name__ == "__main__":    

    unittest.main()

    test = Crosssection(3,0.825,1)
    print(test.total_area())