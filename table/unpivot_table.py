import xloil
from xloil.pandas import PDFrame
import pandas as pd
from converters import IntOrArrayOfInt, DfWithHeader, ExcelStringType


@xloil.func(name="UNPIVOT_TABLE",
            help="Unpivot a DataFrame from wide to long format",
           args={"array": "Range to unpivot. The first row must contain the column headers",
                 "id_vars_index": "Position of the column(s) to keep as identifiers, counted from 1 (default: none)",
                 "value_vars_index": "Position of the column(s) to unpivot, counted from 1 (default: all columns not in id_vars_index)",
                 "var_name": "Title of the column that holds the old headers (default: variable)",
                 "value_name": "Title of the column that holds the values (default: value)"})
def unpivot_table(array: DfWithHeader,
                  id_vars_index: IntOrArrayOfInt = None,
                  value_vars_index: IntOrArrayOfInt = None,
                  var_name: ExcelStringType = "variable",
                  value_name: ExcelStringType = "value"):
    # reject invalid arguments, whichever arguments were supplied
    for arg in (array, id_vars_index, value_vars_index, var_name, value_name):
        if isinstance(arg, xloil.CellError):
            return xloil.CellError.VALUE
    n = array.shape[1]
    for idx in (id_vars_index, value_vars_index):
        if idx is None:
            continue
        items = idx if isinstance(idx, list) else [idx]
        if any(x == 0 or abs(x) > n for x in items):
            return xloil.CellError.VALUE
    cols_list = [""] + array.columns.tolist()

    def to_names(idx):
        if idx is None:
            return None
        return [cols_list[x] for x in idx] if isinstance(idx, list) else cols_list[idx]

    try:
        return PDFrame(index=False)(array.melt(to_names(id_vars_index),
                                               to_names(value_vars_index),
                                               var_name, value_name))
    except (ValueError, KeyError):
        return xloil.CellError.VALUE

