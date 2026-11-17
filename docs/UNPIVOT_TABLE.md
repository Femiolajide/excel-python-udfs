# UNPIVOT_TABLE function

Converts a table from wide format to long format. Columns you choose are turned into rows, with one column for the old column headers and one for the values.

## Syntax

```
=UNPIVOT_TABLE(array, [id_vars_index], [value_vars_index], [var_name], [value_name])
```

## Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `array` | Yes | The range to unpivot. The first row must contain the column headers. |
| `id_vars_index` | No | The position of the column, or columns, to keep as identifiers. Their values are repeated on every row of the result. The default is none. |
| `value_vars_index` | No | The position of the column, or columns, to unpivot. The default is every column that is not in `id_vars_index`. |
| `var_name` | No | The title of the column that holds the old column headers. The default is `variable`. |
| `value_name` | No | The title of the column that holds the values. The default is `value`. |

## Returns

A table that spills into the cells below and to the right of the formula. The identifier columns come first, in the order you list them, followed by the `var_name` column and the `value_name` column. The result has one row for each data row of `array` multiplied by the number of columns unpivoted.

## Remarks

### The range

- The first row of `array` must be the header row. Its entries become the values in the `var_name` column.
- If only the header row is selected, the result is a header row with no data.
- Dates in the range are read as Excel serial numbers. Format the result column as a date if you need dates.
- The value column can hold numbers and text together.

### Choosing columns

- `id_vars_index` and `value_vars_index` take column positions, counted from 1 across `array`. The first column of `array` is 1.
- A negative number counts from the end: -1 is the last column, -2 the second to last, and so on. 0 is not valid.
- Each argument accepts a number, a cell that contains a number, a range of cells, or an array constant such as `{1,3,2}`.
- Text that can be read as a number is accepted. In a range or array, text entries must be whole numbers.
- A decimal number is truncated, not rounded. For example, 2.9 is treated as 2, and -2.9 as -2.
- Repeated positions are counted once. Columns appear in the order you list them.
- If you leave out `id_vars_index` and `value_vars_index`, every column is unpivoted and the result has only the `var_name` and `value_name` columns.
- If you give `value_vars_index` but not `id_vars_index`, only the columns you list are unpivoted, and the other columns are not in the result.
- Do not choose the same column in both arguments.

### Naming the new columns

- `var_name` and `value_name` take text. Numbers and TRUE or FALSE are converted to text.
- `value_name` must not be the same as a column header in `array`.

The function uses `pandas.DataFrame.melt()`.

## Errors

| Condition | Result |
| --- | --- |
| `array` is not a range, for example a single cell or text | `#VALUE!` |
| A column position is 0 | `#VALUE!` |
| A column position is larger than the number of columns in `array`, counting from either end | `#VALUE!` |
| A column position is not a number, for example text that is not a number, TRUE or FALSE, or an empty cell in a range | `#VALUE!` |
| `var_name` or `value_name` is a range | `#VALUE!` |
| `value_name` is the same as a column header in `array` | `#VALUE!` |
| The cells where the table would spill are not empty | `#SPILL!` |

## Examples

Cells `A1:D3` contain:

| Name | Jan | Feb | Mar |
| --- | ---: | ---: | ---: |
| Ann | 10 | 20 | 30 |
| Ben | 11 | 21 | 31 |

### Unpivoting with an identifier column

`=UNPIVOT_TABLE(A1:D3, 1)` keeps `Name` and unpivots the other three columns.

| Name | variable | value |
| --- | --- | ---: |
| Ann | Jan | 10 |
| Ben | Jan | 11 |
| Ann | Feb | 20 |
| Ben | Feb | 21 |
| Ann | Mar | 30 |
| Ben | Mar | 31 |

### Naming the new columns

`=UNPIVOT_TABLE(A1:D3, 1, {2,3,4}, "Month", "Sales")` unpivots columns 2 to 4 and renames the new columns.

| Name | Month | Sales |
| --- | --- | ---: |
| Ann | Jan | 10 |
| Ben | Jan | 11 |
| Ann | Feb | 20 |
| Ben | Feb | 21 |
| Ann | Mar | 30 |
| Ben | Mar | 31 |

### Choosing the columns to unpivot

| Formula | Result | Explanation |
| --- | --- | --- |
| `=UNPIVOT_TABLE(A1:D3, 1, {2,3})` | 4 rows: Jan and Feb only | `Mar` is not in the result. |
| `=UNPIVOT_TABLE(A1:D3, 1, {-3,-2,-1})` | The same 6 rows as the first example | -3, -2 and -1 are `Jan`, `Feb` and `Mar`. |
| `=UNPIVOT_TABLE(A1:D3, 1.9)` | The same 6 rows as the first example | 1.9 is truncated to 1. |

### Without an identifier column

`=UNPIVOT_TABLE(A1:D3)` unpivots every column, including `Name`.

| variable | value |
| --- | --- |
| Name | Ann |
| Name | Ben |
| Jan | 10 |
| Jan | 11 |
| Feb | 20 |
| Feb | 21 |
| Mar | 30 |
| Mar | 31 |

### Several identifier columns

Cells `A1:D3` contain:

| Region | Name | Jan | Feb |
| --- | --- | ---: | ---: |
| North | Ann | 10 | 20 |
| South | Ben | 11 | 21 |

`=UNPIVOT_TABLE(A1:D3, {1,2})` keeps `Region` and `Name`.

| Region | Name | variable | value |
| --- | --- | --- | ---: |
| North | Ann | Jan | 10 |
| South | Ben | Jan | 11 |
| North | Ann | Feb | 20 |
| South | Ben | Feb | 21 |

### Errors

Using the first table:

| Formula | Result | Explanation |
| --- | --- | --- |
| `=UNPIVOT_TABLE(A1:D3, 0)` | `#VALUE!` | A column position cannot be 0. |
| `=UNPIVOT_TABLE(A1:D3, 5)` | `#VALUE!` | `A1:D3` has only four columns. |
| `=UNPIVOT_TABLE(A1:D3, TRUE)` | `#VALUE!` | A column position cannot be TRUE or FALSE. |
| `=UNPIVOT_TABLE(A1)` | `#VALUE!` | `A1` is a single cell, not a range. |
| `=UNPIVOT_TABLE(A1:D3, 1, , , "Name")` | `#VALUE!` | `value_name` matches the header `Name`. |

## Design notes

- **Why it exists.** Many analyses and charts need data in long format, with one observation on each row. This function brings the pandas `melt` method into a cell formula, so the result updates when the data change.
- **Why positions.** Columns are chosen by position counting from 1, as Excel does, not from 0 as pandas does, and negative numbers count from the end.

## See also

[`pandas.DataFrame.melt()`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.melt.html)
