import torch
import unittest

import m2s.common.utils as utils

class TestCommonUtils(unittest.TestCase):

    def test_sanitize(self):
    	self.assertTrue(utils.sanitize(1) == 1)
    	self.assertTrue(utils.sanitize(torch.Tensor([1, 2])) == [1, 2])
    	self.assertTrue(utils.sanitize(torch.LongTensor([1, 2])) == [1, 2])
    	self.assertTrue(utils.sanitize(
    		{"abc": torch.LongTensor([1, 2])}) == {"abc": [1, 2]})