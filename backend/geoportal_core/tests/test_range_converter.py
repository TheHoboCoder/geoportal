from unittest import TestCase
from common.utils import RangeConverter

class TestRangeConverter(TestCase):
    
    def test_simple_ranges(self):
        rangeIn = (1, 5)
        rangeOut = (5, 10)
        r = RangeConverter([(rangeIn, rangeOut)])
        for i in range(0, 2):
            self.assertEquals(r.convert(rangeIn[i]), rangeOut[i])

    def test_ascending(self):
        rangeIn = (1, 5)
        rangeOut = (10, 5)
        r = RangeConverter([(rangeIn, rangeOut)])
        for i in range(0, 2):
            self.assertEquals(r.convert(rangeIn[i]), rangeOut[i])

    def test_ranges(self):
        r = RangeConverter([((1, 5), (5, 9)),
                            ((7, 9), (10, 27))])
        self.assertEquals(r.convert(5), 9)
        self.assertEquals(r.convert(7), 10)

    def test_out_range(self):
        r = RangeConverter([((1, 5), (5, 9)),
                            ((7, 9), (10, 27))])
        self.assertEquals(r.convert(0), 5)
        self.assertEquals(r.convert(10), 27)
        r.min_value = -2
        r.max_value = 30
        self.assertEquals(r.convert(0), -2)
        self.assertEquals(r.convert(10), 30)
