# kadro.py

### Kadro is currently in active development. No full test coverage yet.

> Kadro means frame in esperanto.

Kadro is a small python package that wraps a little bit of extra functionality around pandas. The goal is to add more functional methods such that you can use pandas in a more composable manner. For example, you may do queries like;

```
(df
 .group_by("c", "d")
 .agg(m_a = lambda _: np.mean(_['a']),
      v_b = lambda _: np.var(_['b']),
      cov_ab = lambda _: np.cov(_['a'], _['b'])[1,1])
 .sort('m_a'))
```

The goal is to have a minimal wrapper that allows for 90% of all dataframe methods to be more expressive by being chainable.

## Philosophy

Data should be a noun and any manipulations on it should be described with verbs. In R it is convenient to have those verbs be functions because the language allows you to write global operators that can chain functions togehter. In python it makes sense to have them wrapped with methods via an object instead.

The idea behind the tool is to have a more minimal api that accomodates 80-90% of the typical dataframe manipulations by attaching a few very useful composable verbs to a wrapped dataframe object. This work is not meant to replace pandas nor is it meant as a python port of popular r-packages (though I'll gladly admit that a lot of ideas are bluntly copied from `tidyr` and `dplyr`).

The goal of this work is to show a proof of concept to demonstrate extra composability and readability for python based data manipulation. Some performance sacrifices will ensue as a result but you will always be able to access the native pandas object.

## Key Differences

When comparing with pandas there are a few notable differences;

- pandas indices are ignored on creation of a kadro frame
- data is immutable, all methods will cause a new datastructure object to be created
- the only way to cache intermediate results is to save the state into a variable