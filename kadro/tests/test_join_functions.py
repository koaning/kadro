import unittest
import numpy as np
import pandas as pd
from kadro import Frame as kd

df_age = pd.DataFrame({
    'name': ['vincent', 'tim', 'anna'],
    'age': [28, 30, 25]
})

df_length = pd.DataFrame({
    'name': ['vincent', 'tim'],
    'length': [188, 172]
})

kd_age = kd.Frame(df_age)
kd_length = kd.Frame(df_length)

class TestJoin(unittest.TestCase):

    def test_inner_join(self):
        kd_joined_inner = kd_age.inner_join(kd_length)
        self.assertEqual(kd_joined_inner.shape[0], 2)

    def test_left_join1(self):
        kd_joined_inner = kd_age.left_join(kd_length)
        self.assertEqual(kd_joined_inner.shape[0], 3)

    def test_left_join2(self):
        kd_joined_inner = kd_length.left_join(kd_age)
        self.assertEqual(kd_joined_inner.shape[0], 2)

if __name__ == '__main__':
    unittest.main()