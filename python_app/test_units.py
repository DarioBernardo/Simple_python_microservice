import unittest
from TimeSeriesModel import TimeSeriesModel

class ModelTest(unittest.TestCase):

    def test_model(self):
        model = TimeSeriesModel()
        model.add_point_to_ts(1, '2017-01-01', 10, 10)
        model.add_point_to_ts(1, '2017-01-02', 11, 11)
        model.add_point_to_ts(1, '2017-01-03', 12, 12)

        accout_empty = model.get_data_for_accout(2)
        accout_true = model.get_data_for_accout(1)

        self.assertEquals(accout_true.cleared_balance.size, 3)
        self.assertEquals(accout_empty.cleared_balance.size, 0)
