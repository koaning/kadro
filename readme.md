# kadro.py

### Kadro is currently in active development. No full test coverage yet.

> Kadro means frame in esperanto.

![Imgur](http://i.imgur.com/Zzru9Qa.png)

Kadro is a small python package that wraps a little bit of extra functionality around pandas. The goal is to add more functional methods such that you can use pandas in a more composable manner. For example, you may do queries like;

```
import numpy as np
import pandas as pd
import kadro as kd

df = pd.read_csv(<some_file>)

(kd.Frame(df)
  .mutate(e = lambda _: _.a + _.b,
          f = lambda _: np.sqrt(_.e))
  .group_by('c', 'd')
  .agg(m_e = lambda _: np.mean(_.e),
       v_f = lambda _: np.var(_.f),
       cov_ef = lambda _: np.cov(_.e, _.f)[1,1])
  .sort('m_e'))
```

This statement may feel similar to normal aggregation code from `pandas` combined with some parts from `tidyverse` in R. In steps it does the following;

1. It takes a pandas dataframe and casts it to a `kadro.Frame` object. It is merely a wrapper with some methods attached.
2. It takes the new datastructure and it adds two new columns; `e` and `f`. These columns are based off the columns `a` and `b` and we access these series via lambda functions. These lambda functions assume the original pandas dataframe to be passed.
3. It then groups the datastructure via the columns `c` and `d`.
4. It then aggregates this dataset by calculating the mean value of column `e`, the variance of column `f` and by calculating the covariance between `e` and `f`. Again, we can use any function that is able to aggregate a series object to a singleton value.
5. Finally, it sorts this aggregated datastructure by the newly created column `m_e`, which denotes the calculated mean of `e` that was calculated in the step before.

The statements are readable and may remind you of the original pandas library. Note a few key differences.

- the `mutate` method creates two new columns, one of which is based on a new column created in the same `mutate` call
- the `agg` method can apply different functions on different groups and allows you to immediately name the created columns in one call
- all the verbs are composable in a single chain that you can read from top to bottom, from left to right

## Philosophy

The goal is to have a minimal wrapper that allows most of all dataframe operations to be more expressive by being chainable.

Data should be a noun and any manipulations on it should be described with verbs. In R it is convenient to have those verbs be functions because the language allows you to write global operators that can chain functions togehter. In python it makes sense to have them wrapped with methods via an object instead.

The idea behind the tool is to have a more minimal api that accomodates 80-90% of the typical dataframe manipulations by attaching a few very useful composable verbs to a wrapped dataframe object. This work is not meant to replace pandas nor is it meant as a python port of popular r-packages (though I'll gladly admit that a lot of ideas are bluntly copied from `tidyr` and `dplyr`).

The goal of this work is to show a proof of concept to demonstrate extra composability and readability for python based data manipulation. Some performance sacrifices will ensue as a result but you will always be able to access the native pandas object.

## Key Differences

When comparing with pandas there are a few notable differences;

- pandas indices are ignored on creation of a kadro frame
- data is immutable, all methods will cause a new datastructure object to be created
- the only way to cache intermediate results is to save the state into a variable
- methods tend to be lazy, meaning that the functions of methods like `mutate` are evaluated in order

## Key Verbs

Currently, the following verbs are supported in Kadro;

- mutate
- filter
- head/tail/slice
- select/rename/drop
- group_by/agg/ungroup
- sort
- sample_n
- pipe
- left_join/inner_join
- plot
- ~~gather/spread~~

## Documentation and Vignette

You can find elaborate documentation here; https://koaning.github.io/kadro/.

Instead of mere documentation you fill find that all methods are properly documented with a docstring and that perhaps the best way to understand the library is to read the vignette; a notebook containing a demonstration of all the functionality from a-z. In the main of the repo you'll find a notebook containing a demonstration of all the functionality which can render from github.

## Installation

Pip/Conda support is not fully up. You can use pip to install it via github tho.

```
pip install git+git://github.com/koaning/kadro.git
```


Otherwise, consider downloading and playing with this package by running;

```
python setup.py install
```

## Contributions

Contributions are welcome but the package is to remain minimal. If people want to add some extra tests; thats fine and always welcome. You can run tests via;

```
pytest
```

And you can update the docs by running the following from the `/docs` folder;

```
pdoc --html --overwrite kadro.Frame
cp kadro/Frame.m.html index.html
rm -rf kadro
```


## Future

This package is not much more than an alternative ui in nature. Originally meant as a peronsal project and I don't expect many changes are ever needed. I may extra support if it gets traction but the package is intentionally minimal.

Feel free to notify me of issues.

