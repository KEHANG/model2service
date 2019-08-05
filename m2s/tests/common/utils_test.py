import torch
import numpy
import unittest
import pandas as pd

import m2s.common.utils as utils

class DataTypeFoo(object):

    def __init__(self, value):

        self.value = value

class TestCommonUtils(unittest.TestCase):

    def test_sanitize(self):
        self.assertTrue(utils.sanitize(None) == 'None')
        self.assertTrue(utils.sanitize(1) == 1)
        self.assertTrue(utils.sanitize(numpy.int64(1)) == 1)
        self.assertTrue(utils.sanitize([1, 2]) == [1, 2])
        self.assertTrue(utils.sanitize(numpy.array([1, 2])) == [1, 2])
        self.assertTrue(utils.sanitize(torch.Tensor([1, 2])) == [1, 2])
        self.assertTrue(utils.sanitize(torch.LongTensor([1, 2])) == [1, 2])

        # test pandas data type which has to_json()
        df = pd.DataFrame([{"col 1":"a","col 2":"b"},
                           {"col 1":"c","col 2":"d"}])
        df_json = '{"col 1":{"0":"a","1":"c"},"col 2":{"0":"b","1":"d"}}'
        self.assertTrue(utils.sanitize(df) == df_json)
        self.assertTrue(utils.sanitize(
            {"abc": torch.LongTensor([1, 2])}) == {"abc": [1, 2]})

        # test sanitizing custom data type that has no to_json()
        with self.failUnlessRaises(ValueError):
            utils.sanitize(DataTypeFoo(10))