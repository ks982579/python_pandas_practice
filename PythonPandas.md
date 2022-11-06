# Pandas in Python

## Sources
- [ ] [Pandas Data Analysis in Python](https://www.youtube.com/playlist?list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS) Youtube series by _Corey Schafer_
- [ ] [Pandas Reference for API](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.casefold.html#pandas.Series.str.casefold)

## Getting Started

Pandas is a data analysis library that allows us to read and work with different types of data. It has great performance because it is built on top of Numpy. 

Installation is in the README.md for project. 

Jupyter makes viewing data easy. The instructor uses [Stack Overflow Survey](https://insights.stackoverflow.com/survey) data to provide real world results for analysis. Get this or other data and then create a directory with the data inside. Start a notebook within that directory. 

When you create a new notebook, you should rename it because they are named "untitled". Start the notebook with the following. 

```python
import pandas as pd
pd.__version__
```

Then, you can read in data, such as csv. 

```python
df = pd.read_csv('survey_results_public.csv')
```

This creates a **data-frame**, which can be thought of as a table or spreadsheet with rows and columns. 

To get information regarding the dataframe, you can run the following. 

```python
df.shape
df.info()
```

## DataFrame and Series

Data Frames are (basically) tables, like rows and columns. They are also referred to as a "2 dimensional data structure". In a pythonic format, you might think of it like a dictionary, with column titles as the keys, and the values for each key is a list of values.

```python
people = {
	"first": ["John", "Courtney"],
	"last": ["Doe", "Smith"],
}
```

You can actually call the column of a data-frame just like you would the key to a dictionary, and it returns a list of its values. And you can create a data-frame from a dictionary by passing it in as the argument the the class.

```python
import pandas as pd
new_df = pd.DataFrame(people)
``` 

The difference between our dictionary and a data-frame is that the dictionary is composed of lists, where a data-frame consists of **Series**. You can think of a series like a row in a table. See a list of columns by calling the _columns_ **attribute**.

```python
df.columns
```
You can also lookup multiple columns at once by passing in a list of column names.

```python
lookup_list = ['Employment', 'RemoteWork', 'CodingActivities', 'EdLevel', 'LearnCode', 'LearnCodeOnline']
df[lookup_list]
```

We need to talk about accessing rows now. There are two methods, one for "integer-location", and the other for just "location". Think of the former like accessing an array, starting at 0 and going to $n-1$. The latter involves passing in the reference to an index, which by default is a 0 based list. 

Remember, if you pass in a single value then you are returned a series. If you pass in a list of values, you are returned another data-frame. The idea sounds like overriding methods.

```python
df.iloc[0]
df.iloc[[0,2,5], [1,2,4]]
df.loc["honda"]
```

You can also pass in a second argument that specifies the columns you want back. For `iloc`, the columns must also be integers. You can pass in a list of strings for the column names for `loc`. 

You can use the `range()`method if you want to get multiple rows without explicitly defining them. You can also use the slice/splice syntax without the square brackets. 

```python
df.loc[ 1:12 , 'LanguageHaveWorkedWith':'DatabaseWantToWorkWith']
```

For the columns, yes you can slice with their string names. And note that the end value is **inclusive**, which is not typical of the ordinary slice methodology. But it would be a pain to find the next column string name... 

## Indexes - How to Set, Reset, and Use

Consider something like...
```python
people = {
    "first": ["Kevin", "Megan", "Sean", "Melody"],
    "last": ["Penmark", "Mikeson", "Hemingway", "Mistress"],
    "email": ['KevinPenmark@example.com', 'MeganMikeson@example.com', 'SeanHemingway@example.com', 'MelodyMistress@example.com'],
}
simple_df = pd.DataFrame(people)
simple_df.set_index('email', inplace=True)
```

That will set the index to be the emails, which is usually a good idea since emails are unique. Note we must set `inplace=True`. You can also reassign over the data-frame, but Pandas typically won't save over information unless you tell it to. 

```python
print(simple_df.index)
simple_df.loc["MelodyMistress@example.com"]
```

Note that you can see all of the indexes with the `index` attribute, which can be helpful on a small data-frame like this. And we can use the `loc` indexer now with the index email values. You can also pass in the column names as the second argument. 

Now, what if we aren't happy with our decision to set the index? We can reset it. Now, you can reassign the reset data-frame to itself or use the `inplace=True` argument, or assign the data-frame to a new variable name and have a new one!

```python
df.reset_index(inplace=True)
```

We can also assign an index out of the gate. Say our CSV has an column for an index already. You can just add an argument to specify which column it is like so:

```python
df = pd.read_csv('survey_results_public.csv', index_col="ResponseId")
```

Remember, this won't have an impact on using the `iloc` indexer. 

If your indexes are sting values, it might make sense to sort them alphabetically. You can call a `sort_index()` method similar to a list. Note that by default `ascending=True`, meaning it sorts a-z. 

```python
df.sort_index(ascending=False, inplace=True)
```

Also, don't forget to specify `inplace=True` if you want changes to stick. 

## Filtering 
### Using Conditionals to Filter Rows and Columns

~~This is part 4 in the series...~~
Filtering is very important to almost every project and is usually done at the beginning. We typically filter the data that we want from what we have, leaving behind what we don't want. We can perform some basic comparisons within our dataframe. 

```python
people = {
    "first": ["Kevin", "Megan", "Sean", "Melody", "Joseph"],
    "last": ["Penmark", "Mikeson", "Hemingway", "Mistress", "Penmark"],
    "email": ['KevinPenmark@example.com', 'MeganMikeson@example.com', 'SeanHemingway@example.com', 'MelodyMistress@example.com', 'JoePen@example.com'],
}
df = pd.DataFrame(people)
df["last"] == "Penmark"
```

The last statement will return a _series_ of index values and booleans

| email | Bool |
|  :---: | :---: |
| KevinPenmark@example.com | True |
| MeganMikeson@example.com |  False |
| SeanHemingway@example.com |    False |
| MelodyMistress@example.com |   False |
| JoePen@example.com |            True |
Name: last, dtype: bool

The statement `df["last"] == "Penmark"` creates a **filter mask**, which when applied to a _DataFrame_, gives you the rows that meet the criteria. 

Let us now apply this filter to our _DataFrame_ by assigning it to a variable. You do this by passing the filter mask into the _DataFrame_.

```python
my_filter = df["last"] == "Penmark"
df[my_filter]
```

This returns only the values that are `True`. You can also create the filter mask directly in the _DataFrame_, skipping the variable assignment step. However, you may notice it is harder to read. Another way to generate the same _DataFrame_ is with the `loc` indexer. 

```python
my_filter = df["last"] == "Penmark"
df.loc[my_filter]
```

This is what makes **Pandas** a little confusing, being able to do the same thing multiple ways. However, the `loc` method is great because you can also pass in column titles that you also want. 

Using conditional _and_ and _or_ statements in Pandas is different that regular python. We use the `&` and `|` operators. 

```python
filt2 = (simple_df["first"] == "Kevin") | (simple_df["last"] == "Mistress")
simple_df.loc[filt2]
```

Note that it was necessary for the parentheses. Without them, I think the _or_ operator was trying to grab the string "Kevin", instead of the who Boolean value. 

We can also negate an entire filter with the tilde. 

```python
simple_df.loc[~filt2]
```

The above will return everything that failed the filter. 

Here's another example with our actual data set

```python
high_salary = (df["CompTotal"] > 75000)
df.loc[high_salary, ["CodingActivities", "EdLevel", "YearsCodePro", "LanguageHaveWorkedWith"]]
```

Now, let's filter by certain countries. I created a set to filter out any duplicates firstly. That way, I could see my options. Then, create a list and use it to create a filter mask.

```python
country_set = set(df["Country"])
countries = ["United States of America", "Ireland", "Denmark"]
country_filter = df["Country"].isin(countries)
df.loc[country_filter, "Country"]
```

Apply the filter mask to your _DataFrame_ to get a new _DataFrame_ (or *Series*). 

We can also use string methods for filtering data. In our _DataFrame_, the `df["LanguageHaveWorkedWith"]` column is comprised of semi-colon separated values. [Here is](https://pandas.pydata.org/docs/user_guide/text.html#method-summary) a list of methods that you can use. I tried to add the `casefold()`, but that returns a *Series* object, which does not have the same methods as the _DataFrame_. 

```python
language_filter = df["LanguageHaveWorkedWith"].str.contains("rust", case=False, na=False)
df.loc[language_filter, "LanguageHaveWorkedWith"]
```

The `casefold` workaround is to specify `case=False` in the arguments. The `na=False` is also necessary because our data contains some `NaN` values. This basically removes them through the filter mask. 

There are so many more string methods for _DataFrame_ objects. It might be worth looking over the reference manual. 

## Updating Rows and Columns
### Modifying Data within _DataFrame_ objects

We start with updating column names. Simply reassign the column list.

```python
simple_df.columns = ["first_name", "last_name"]
```

You might not want to change all of the columns like this, but you can use the list itself to create a new one. You can also use **list comprehension** to create a new list for column titles. 

```python
simple_df.columns = simple_df.columns.str.replace(" ", "_")
```

The above will replace spaces with underscores, which helps if you like using dot notation. 

You can also use the [`rename()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html) method on a _DataFrame_, which has quite a few arguments to choose from. 

```python
new_df= simple_df.rename(columns={"first": "first_name"})
```

You pass in dictionaries to change names. The keys are the old names and the values are the new names. This returns a _DataFrame_ object. You can overwrite the old one, pass in the `inplace` argument, or assign to a new variable name. 

To update rows and such, we can grab a row with the `loc` or`iloc` indexers, and assign it a new list of values. 

```python
new_df.loc["JoePen@example.com"] = ["Joe", "Penmark"]
```

This seems simple enough, but imagine our actual dataset that has 79 columns. We don't want to update all 79 at once. Remember that with the indexers, we can pass in a second argument to specify columns.

```python
new_df.loc["JoePen@example.com", "fn"] = "Joe"
``` 

Notice that we didn't need to use lists here because we were only adjusting one value of one column. Actually, passing in a list of values would cause a small problem, Pandas would save the value as a list rather than a string. 

An equivalent expression is as follows:

```python
new_df.loc["JoePen@example.com", ["fn"]] = ["Joe"]
``` 

By passing in a list for the columns, Pandas can then accept a list for the values. 

For single value changes, Pandas has a [_DataFrame_.at](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.at.html) indexer, which basically takes in the index and the column name, and returns its value. It has a similar _DataFrame_.iat indexer as well. 

```python
new_df.at["JoePen@example.com", "fn"] = "Joe"
``` 

The `loc` indexers have a bit of overhead to determine what you are asking. As such, using the `at` indexers for scalar values can be much quicker. 

**Note**, you may think you can create a filter to find a value and then pull out what you need and change it. But you will receive a "Setting WithCopyWarning" exception. The difference involves Pandas returning a [**View** vs. a **Copy**](https://pandas.pydata.org/docs/user_guide/indexing.html#returning-a-view-versus-a-copy).  If you attempt the filter reassignment approach, you will begin using "chained indexing" which also has expensive overhead. Basically, Pandas can't guarantee the value will be changed on the actual object, or just a copy that is immediately discarded. 

The correct way to use a filter to change values is within a `loc` indexer. 

```python
my_filter = (df['email'] == 'user@example.com')
df.loc[my_filter, 'last_name'] = "Smith"
```

That's not completely practical, the above example. But the idea can lead to changing multiple values in a column. You can reassign a column to a modified version of itself. 

```python
df["last_name"] = df["last_name"].str.upper()
```

There are 4 similar methods for making changes to _DataFrame_ or _Series_ objects. They are: `apply`, `map`, `applymap`, `replace`. 

The [`Series.apply(func, convert_dtype=True, args=(), **kwargs)`](https://pandas.pydata.org/docs/reference/api/pandas.Series.apply.html) works differently on a _Series_ than a _DataFrame_. On a _Series_, the method invokes a function on values of the _Series_. 

I am switching gears in the example to be...

```python
import random
import pandas as pd

rang_val = 10

# Generate Dates list
rang_val = 10
random_times = []
for _x in range(rang_val):
    random_times.append(pd.Timestamp(2022, 9, random.randint(1,30), random.randint(0,23)))

# Generate random endpoints
random_endpoints = []
eps = ["user", "friends", "tweets"]
for _x in range(rang_val):
    random_endpoints.append(f"/api/{random.choice(eps)}")

api_calls = {
    "date": random_times,
    "request": random_endpoints,
}
req_df = pd.DataFrame(api_calls)

req_df['request'].apply(len)
```

The last line actually used the `apply()` method. It is applying the `len()` function on each element of the _Series_ returned. You can create your own functions that are more advanced than this. 

```python
def convert_date_to_julian(val):
    return math.trunc(val.to_julian_date()-0.5)
    # subtract 0.5 because Julian starts at noon...

req_df['julian_date'] = req_df['date'].apply(convert_date_to_julian)
```

The above example changes the dates to [Julian](https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.to_julian_date.html) values, starting on 1 Jan 4,713 BC at noon. Remember that you only pass in a reference to the function that changes values. And you must reassign the _Series_ as Pandas will does not work _in-place_. 

You can also use `lambda` functions, which are Python's anonymous functions. 

```python
req_df['date'] = req_df['date'].apply(lambda val: math.trunc(val.to_julian_date()-0.5))
```

The [`DataFrame.apply(func, axis=0, raw=False, result_type=None, args=(), **kwargs)`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html) applies a function along an axis of the _DataFrame_. That means it applies to function to the entire row, or column, of the _DataFrame_ at a time. 

```python
req_df.apply(len)
```

This simple example is quite powerful. You should get back a series of the lengths of each column. Since each column has the same number of rows, the answers are all the same. 

To apply the function to each **row**, instead of each column, we must specify the `axis=1`.

```python
req_df.apply(len, axis=1)
```

You can also use the string 'columns', but that seems a little backwards to me. So, `axis=0` is default, and same as specifying 'rows'. And `axis=1` is the same as 'columns', but applies the function to each row. I guess you can think of it like, what values are passed into the function? When you specify 'columns' you get the values in each column, per row. The other way around is getting the values in each row, per column. 

When is the default better? Probably when you are comparing all of the values in that column. 

```python
req_df.apply(pd.Series.min)
req_df.apply(lambda x: x.min())
```

The above gives the minimum value in each column. The latter seems to make more sense since what is being passed in is a _Series_ object. However, it appears you can pass an actual series into this `@classmethod` as well. 

The [`DataFrame.applymap()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.applymap.html) method only works on a _DataFrame_, there is no _Series_ equivalent. it takes in a function, and you can also pass in an argument of `na_action="ignore"` to propagate NaN values without passing them through the function. 

```python
req_df.applymap(len)
```

This applies the function to each value, or in other terms, to each cell of our spreadsheet / each element of our _DataFrame_. This method seems hard to apply because, for instance, you cannot run string methods on numerical data types. Easy to raise exceptions. 

The [`Series.map()`] method only works on _Series_ objects, and substitutes values in a _Series_ object with one specified in the argument. The argument can be a function, dictionary, or _Series_. 

```python
df["first_name"].map(lambda val: f"My name is {val}.")
```

You can also pass in a _dict_, whcih substitutes the values in for any key that it finds. For example, passing in `{"kevin": "kev"}` will substitute all values of "kevin" with "kev". However, any values not converted per the dictionary are converted to "NaN". Even passing in the `na_action="ignore"` won't fix this issue, that only works on already existing `NaN` values.

The proper method is probably [`Series.replace()`](https://pandas.pydata.org/docs/reference/api/pandas.Series.replace.html). Passing in a dictionary here only replaces matches, and does not `NaN` non-matches. 

```python
req_df["request"].replace({"/api/tweets": "Twitter sucks"})
```

To make the changes stick here, you must assign to itself, or set `inplace=True`. 

An interesting thought is using `map` to change `{"Yes": True, "No": False}`. 

## Add/Remove Rows and Columns from _DataFrame_ Objects

We can create a new _Series_ by manipulating existing _Series_ objects. 

```python
df["full_name"] = df["first"] + " " + df["last"]
```

The above will create a _Series_ object of, say, first and last names, and saves it to a new column called "full_name". You could also use the `apply()` method as I believe I did in a previous example. 

**Note**, you must use the bracket notation when creating a new column. If you try for dot-notation, Python will think you are trying to assign the object a new attribute instead of a new column. 

Suppose now we are happy with just the "full_name" and want to remove the others. We can call the `DataFrame.drop()` method to remove columns.

```python
df.drop(columns=["first", "last"], inplace=True)
```

If we were unhappy that the names came together, we can split them.

```python
df[["first", "last"]] = df["full_name"].str.split(" ", expand=True)
```

The `DataFrame.str.split()` method splits strings into a list based on a separator. We pass in `expand=True` to tell Pandas we are actually trying to get additional columns out of this. Then, we can assign the new columns almost like we are performing array [destructuring](https://blog.teclado.com/destructuring-in-python/). 

How about adding new rows? it's a little complicated because our added row should have an index. However, we can tell Pandas to ignore the index. We would use the [`DataFrame.append()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.append.html) method, but it has been put on the **Deprecated** list since 22 January 2022. Use the [`pandas.concat()`](https://pandas.pydata.org/docs/reference/api/pandas.concat.html#pandas.concat) method instead, which is a library **General Function**, and not a _DataFrame_ method. 

```python
new_row = pd.Series({"request": "/home", "julian_date": 10})
req_df = pd.concat([req_df, new_row.to_frame().T], ignore_index=True)
```

The process is a bit harder than it needs to be. Basically, you must convert the _Series_ object to a _DataFrame_ with the [`Series.to_frame()`](https://pandas.pydata.org/docs/reference/api/pandas.Series.to_frame.html) method to concatenate it to the existing _DataFrame_ object. But you also must refer to the [`DataFrame.T`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.T.html) property when concatenating or the new value will be concatenated into a new row, which wouldn't make sense. 

What's the difference? Think of the `DataFrame.T` like the **transpose** of our _DataFrame_. Initially, the keys of our _dict_ are the indexes, and the values are aligned in a column titled "0". 

| index | 0 |
| :--: | :--: |
| request | /home |
| julian_date | 10 |

However, calling `DataFrame.T` fixes that with a transpose:

| index | request | julian_date |
| :--: | :--: | :--: |
| 0 | /home | 10  |

Then, all that is left to do is `ingnore_index=True` so the _DataFame_ can assign it a new index. You would keep the default `False` if you were using something like email addresses as the index. 

Note, this is also how to append _DataFrame_ objects together as well. Also note that the `concat()` method does not have an `inplace` argument, and is not an in-place method. 

What if we don't want a row in our table? We can [`DataFrame.drop(index=?)`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html) the value. 

```python
req_df.drop(index=10, inplace=True)
```

The index can be whatever the value is, string, int, or pass in a tuple for multiple rows. If you pass in both an index and a column, it will remove both the index and the column, not the one element they both point to. 

To drop multiple rows at once, you can also use a filter. 

```python
drop_filter = df["last"] == "Doe"
df.drop(index=df[ drop_filter ].index, inplace=True)
```

Be sure to call the `index` property on the _DataFrame_ object since that is what the method is expecting. 

## Sorting Data

~~Part 7~~
