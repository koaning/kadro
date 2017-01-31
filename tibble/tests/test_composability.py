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

class Composables(unittest.TestCase):

    def test_compose1(self):
        """Test that grouping has an effect on mutate."""
        new = (tf
               .group_by('c', 'd')
               .mutate(e = lambda _: _['a'].shift())
               .ungroup())
        print(new)
        self.assertEqual(len(new.groups), 0)
        self.assertEqual(new.df.iloc[0]['a'], new.df.iloc[1]['e'])
        self.assertEqual(np.isnan(new.df.iloc[0]['e']), True)


if __name__ == '__main__':
    unittest.main()