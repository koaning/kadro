import numpy as np
import pandas as pd
import itertools as it


class Tibble:
    """
    A datastructure that adds methods on top of pandas.

    Example:
    import numpy as np
    import pandas as pd
    import tibble as tb

    np.random.seed(42)
    n = 40

    df = pd.DataFrame({
        'a': np.random.randn(n),
        'b': np.random.randn(n),
        'c': ['foo' if x > 0.5 else 'bar' for x in np.random.rand(n)],
        'd': ['fizz' if x > 0.5 else 'bo' for x in np.random.rand(n)]
    })

    tf = tb.Tibble(df)
    """
    def __init__(self, df, groups = []):
        self.df = df.copy()
        self.df.index = np.arange(df.shape[0])
        self.groups = groups

    def __repr__(self):
        res = "Pandas derived TibbleFrame Object.\n"
        if len(self.groups) > 0:
            res += "With groups {}\n".format(self.groups)
        return res + "\n" + str(self.df.head(10))

    def _group_mutate(self, **kwargs):
        df_copy = self.df.copy()
        res = []
        grouped = df_copy.groupby(self.groups)
        for key in kwargs.keys():
            new_row = pd.concat([group[1].pipe(kwargs[key]) for group in grouped])
            df_copy[key] = new_row
        return Tibble(df_copy, self.groups[:])

    def show(self, n = 10):
        """
        Shows the `n` top items of a the datastructure.
        """
        res = "Pandas derived TibbleFrame Object.\n"
        if len(self.groups) > 0:
            res += "With groups {}\n".format(self.groups)
        print(res + "\n" + str(self.df.head(n)))

    def plot(self, *args, **kwargs):
        """
        Wrapper around pandas plotting. See pandas documentation.
        """
        return self.df.plot(*args, **kwargs)

    def mutate(self, **kwargs):
        """
        Creates or changes a column. Keeps groups in mind.

        Example:
        tf.mutate(a = lambda _: _['col1'] + _['col2']*2)
        """
        if len(self.groups) != 0:
            return self._group_mutate(**kwargs)
        df_copy = self.df.copy()
        for mut in kwargs.keys():
            df_copy[mut] = kwargs[mut](df_copy)
        return Tibble(df_copy, self.groups[:])

    def filter(self, *args):
        """
        Filter rows to keep.

        Example: Example:
        tf.filter(lambda _: _['col1'] > 20)
        """
        df_copy = self.df.copy()
        for func in args:
            predicate = func(df_copy)
            df_copy = df_copy[predicate]
        return Tibble(df_copy, self.groups[:])

    def select(self, *args):
        """
        Select a subset of the columns.

        Example:
        tf.select("col1", "col2")
        tf.select(["col1", "col2"])
        """
        columns = list(it.chain(*args))
        df_copy = self.df.copy()
        return Tibble(df_copy[columns], self.groups[:])

    def rename(self, rename_dict):
        """
        Renames the dataframe.
        Expects a a dictionary of strings where the keys represent
        the old names and the values represent the new names.

        Example:
        tf.rename({"aa":"a", "bb":"b"})
        """
        df_copy = self.df.copy()
        df_copy = df_copy.rename(index=str, columns = rename_dict)
        return Tibble(df_copy, self.groups[:])


    def set_names(self, names):
        """
        Expects a list of strings and will reset the column names.

        Example:
        tf.set_names(["a", "b", "c", "omg_d")
        """
        df_copy = self.df.copy()
        df_copy.columns = names
        return Tibble(df_copy, self.groups[:])

    def drop(self, *args):
        """
        Drops columns from the dataframe.

        Example:
        tf.drop("col1")
        tf.drop(["col1", "col2"])
        """
        df_copy = self.df.copy()
        columns = [_ for _ in df_copy.columns if _ not in it.chain(*args)]
        return Tibble(df_copy[columns], self.groups[:])

    def sort(self, *args, ascending = True):
        """
        Sort the data structure based on *args passed in.
        Works just like .sort_values in pandas but keeps groups in mind.

        Example:
        tf.sort("col1")
        tf.sort(["col1", "col2"], ascending=[True, False])
        """
        df_copy = self.df.copy()
        sort_cols = self.groups + [arg for arg in args]
        df_sorted = df_copy.sort_values(sort_cols, ascending=ascending)
        return Tibble(df_sorted, self.groups[:])

    def group_by(self, *args):
        """
        Add a group to the datastructure. Will have effect on .agg/.sort/.mutate methods.
        Calling .agg after grouping will remove it. Otherwise you need to call .ungroup
        if you want to remove the grouping on the datastructure.

        Example:
        tf.group_by("col1")
        tf.group_by("col1", "col2")
        """
        group_names = [_ for _ in args]
        if any([_ not in self.df.columns for _ in group_names]):
            raise TibbleError("Wrong column name in .group_by method: does not exist.")
        return Tibble(self.df.copy(), group_names[:])

    def ungroup(self):
        """
        Removes any group from the datastructure.
        """
        return Tibble(self.df.copy(), [])

    def pipe(self, func, *args, **kwargs):
        """
        Pipe the datastructure through a large function. Works just like .pipe in pandas.

        Example:
        def large_function1(frame):
            <stuff>
        def large_function2(frame):
            <stuff>
        tf.pipe(large_function1).pipe(large_function2)
        """
        df_copy = self.df.copy()
        new_df = df_copy.pipe(func, *args, **kwargs)
        return Tibble(new_df, self.groups[:])

    def _agg_nogroups(self, **kwargs):
        new_df = pd.DataFrame({k: v(self.df) for k, v in kwargs.items()}, index = [0])
        return Tibble(new_df, [])

    def agg(self, **kwargs):
        """
        Aggregates the datastructure. Commonly works with .group_by. If no grouping
        is present it will just aggregate the entire table.

        Example:
        tf.group_by("col1").agg(m1 = lambda _: np.mean(_['m1']))

        Example:
        (tf
         .group_by("col1", "col2")
         .agg(m1 = lambda _: np.mean(_['m1']),
              m2 = lambda _: np.mean(_['m2']),
              c = lambda _: np.cov(_['m1'], _['m2'])[1,1]))
        """
        if len(self.groups) == 0:
            return self._agg_nogroups(**kwargs)
        df_copy = self.df.copy()
        grouped = df_copy.groupby(self.groups)
        res = [grouped.apply(kwargs[_]) for _ in kwargs.keys()]
        res = pd.concat(res, axis = 1).reset_index()
        res.columns = self.groups + list(kwargs.keys())
        return Tibble(res, [])

    def gather(self, key = "key", value="value", keep = []):
        """
        Turns a wide dataframe into a long one. Removes any grouping.

        Example:
        df = pd.DataFrame({
            'a': np.random.random(8),
            'b': np.random.random(8)*3,
            'c': 'a,a,a,a,b,b,b,b'.split(',')
        })
        tf = tb.Tibble(df)
        tf.gather("key", "value")
        """
        copy_df = self.df.copy()
        copy_df = pd.melt(copy_df,
                          id_vars = keep,
                          value_vars=[_ for _ in copy_df.columns if _ not in keep])
        return Tibble(copy_df, []).rename({"variable": key, "value": value})

    def spread(self, key = "key", value="key", keep = []):
        """
        Turns a long dataframe into a wide one.

        CURRENTLY UNIMPLEMENTED!
        """
        pass

    def sample_n(self, n_samples, replace = False):
        """
        Samples `n_samples` rows from the datastructure. You can do it with, or without, replacement.

        Example:
        tf.n_sample(100)
        tf.n_sample(1000, replace = True)
        """
        df_copy = self.df.copy()
        idx = np.arange(df_copy.shape[0])
        row_ids = np.random.choice(idx, size = n_samples, replace = replace)
        return Tibble(df_copy.iloc[row_ids], self.groups[:])

    def head(self, n = 5):
        """
        Mimic of pandas head function. Selects `n` top rows.

        Example:
        tf.head(10)
        """
        return Tibble(self.df.copy().head(n), self.groups[:])

    def tail(self, n = 5):
        """
        Mimic of pandas tail function. Selects `n` bottom rows.

        Example:
        tf.tail(10)
        """
        return Tibble(self.df.copy().tail(n), self.groups[:])

    def slice(self, *args):
        """
        Slice away rows of the dataframe based on row number.

        Example:
        tf.slice(1,2,3)
        tf.slice([1,2,3,])
        """
        if len(args) > 1:
            return self.slice(args)
        df_copy = self.df.copy()
        return Tibble(df_copy.iloc[args], self.groups[:])