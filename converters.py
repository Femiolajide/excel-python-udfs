import xloil 
import pandas as pd
from xloil.pandas import PDFrame
import datetime as dt
import numpy as np

# kind of string imput I want 
@xloil.converter()
def ExcelStringType(val):    
    if val is None:
        return ""
    elif isinstance(val, xloil.ExcelArray):
        return xloil.CellError.VALUE
    elif isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    elif isinstance(val, float) and val.is_integer():
        return str(int(val))
    else:
        return str(val)

# Kind of dataframe I prefer  df with headers

@xloil.converter()
def DfWithHeader(rng):
    if isinstance(rng, xloil.ExcelArray):
        data = rng.to_numpy()
        return pd.DataFrame(data[1:],columns=data[0])
    else:
        return xloil.CellError.VALUE

# Integer input or array of integers

@ xloil.converter()
def IntOrArrayOfInt(val):
    try:
        if isinstance(val, bool):
            return xloil.CellError.VALUE
        elif isinstance(val, xloil.ExcelArray):
            out = val.to_numpy().astype(int).flatten().tolist()
            return list(dict.fromkeys(out))
        elif val is None:
            return None
        else:
            return int(float(str(val)))
    except:
        return xloil.CellError.VALUE


