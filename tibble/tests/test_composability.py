import unittest
import numpy as np
import pandas as pd
from tibble import tibble as tb

np.random.seed(42)
n = 20
df = pd.DataFrame({
    'a': np.random.randn(n),
    'b': np.random.randn(n),
    'c': ['foo' if x > 0.5 else 'bar' for x in np.random.rand(n)],
    'd': ['fizz' if x > 0.6 else 'bo' for x in np.random.rand(n)]
})
df = df.sort_values(['c', 'd'])
tf = tb.Tibble(df)

class TestMutate(unittest.TestCase):

    def test_mutate_single(self):
        """Test that you can add a single column."""
        new = tf.mutate(e = lambda _: _['a'] + _['b']*2)
        self.assertEqual(len(new.df.columns), 5)

    def test_mutate_mult1(self):
        """Test that you can add multiple columns."""
        new = (tf
               .mutate(e=lambda _: _['a'] + _['b'] * 2,
                       f=lambda _: np.sqrt(_['e']),
                       q=lambda _: _['a'] / 2))
        self.assertEqual(len(new.df.columns), 7)

    def test_mutate_mult2(self):
        """Test that you can add multiple columns and overwrite."""
        new = (tf
               .mutate(e=lambda _: _['a'] + _['b'] * 2,
                       f=lambda _: np.sqrt(_['e']),
                       a=lambda _: _['a'] / 2))
        self.assertEqual(len(new.df.columns), 6)


if __name__ == '__main__':
    unittest.main()