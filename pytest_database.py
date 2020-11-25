# coding=UTF-8
import sys
import os
import unittest
from decimal import *
from utils import get_r1_data

class TestFunc(unittest.TestCase):
    def test_get_r1_data(self):
        '''
        Test method get_r1_data()
        '''
        self.assertEqual((('武汉', Decimal('50340')), ('香港', Decimal('5701')), ('孝感', Decimal('3518')), ('黄冈', Decimal('2907')), ('荆州', Decimal('1580'))), get_r1_data())
if __name__ == '__main__':
    unittest.main()

