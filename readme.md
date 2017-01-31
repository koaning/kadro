# kadro.py

### Kadro is currently in active development. No full test coverage yet.

> Kadro means frame in esperanto.

![Imgur](http://i.imgur.com/Zzru9Qa.png)

Kadro is a small python package that wraps a little bit of extra functionality around pandas. The goal is to add more functional methods such that you can use pandas in a more composable manner. For example, you may do queries like;

```
import kadro as kd

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
- ~~gather/spread~~
- ~~left_join/inner_join~~

## Vignette

Although we also generate some documentation, the best way to understand the library is to read the vignette. In the main of the repo you'll find a notebook containing a demonstration of all the functionality.

## Future

This package is a little bit experimental in nature and was originally meant as a peronsal project. I may extra support if it gets traction. Feel free to notify me of issues.

