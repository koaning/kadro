import unittest
import numpy as np
import pandas as pd
import kadro as kd

np.random.seed(42)
n = 20
df = pd.DataFrame({
    'a': np.random.randn(n),
    'b': np.random.randn(n),
    'c': ['foo' if x > 0.5 else 'bar' for x in np.random.rand(n)],
    'd': ['fizz' if x > 0.6 else 'bo' for x in np.random.rand(n)]
})
df = df.sort_values(['c', 'd'])
kf = kd.Frame(df)

class TestMutate(unittest.TestCase):

    def test_mutate_single(self):
        new = kf.mutate(e = lambda _: _['a'] + _['b']*2)
        self.assertEqual(len(new.df.columns), 5)

    def test_mutate_mult1(self):
        new = (kf
               .mutate(e=lambda _: _['a'] + _['b'] * 2,
                       f=lambda _: np.sqrt(_['e']),
                       q=lambda _: _['a'] / 2))
        self.assertEqual(len(new.df.columns), 7)

    def test_mutate_mult2(self):
        new = (kf
               .mutate(e=lambda _: _['a'] + _['b'] * 2,
                       f=lambda _: np.sqrt(_['e']),
                       a=lambda _: _['a'] / 2))
        self.assertEqual(len(new.df.columns), 6)


class TestFilter(unittest.TestCase):

    def test_filter_single(self):
        new = kf.filter(lambda _: _['a'] > 1000)
        self.assertEqual(new.df.shape[0], 0)

    def test_filter_mult(self):
        new = (kf
                 .filter(lambda _: _['a'] > 0,
                         lambda _: _['b'] > 0))
        self.assertEqual(new.df.shape[0], 3)


class TestSlice(unittest.TestCase):

    def test_slice1(self):
        self.assertEquals(kf.slice(2, 3, 10).df.shape[0], 3)

    def test_slice2(self):
        self.assertEquals(kf.slice([1, 2, 3, 10]).df.shape[0], 4)


class TestAgg(unittest.TestCase):

    def test_agg_nogroup(self):
        new = (kf.agg(m_a=lambda _: np.mean(_['a']),
                     v_b=lambda _: np.var(_['b']),
                     cov_ab=lambda _: np.cov(_['a'], _['b'])[1, 1]))
        self.assertEquals(new.shape[0], 1)
        self.assertEquals(new.shape[1], 3)

    def test_agg_group(self):
        new = (kf
                 .group_by("c", "d")
                 .agg(m_a=lambda _: np.mean(_['a']),
                      v_b=lambda _: np.var(_['b']),
                      cov_ab=lambda _: np.cov(_['a'], _['b'])[1, 1]))
        self.assertEquals(new.shape[0], 4)
        self.assertEquals(new.shape[1], 5)

class TestSamplers(unittest.TestCase):

    def test_sampler1(self):
        new = kf.sample_n(10)
        self.assertEquals(new.shape[0], 10)

    def test_sampler2(self):
        new = kf.sample_n(10000, replace=True).sort("a").head(5)
        self.assertEquals(new.shape[0], 5)
        self.assertEquals(new.df.iloc[0]['a'], new.df.iloc[2]['a'])

if __name__ == '__main__':
    unittest.main()