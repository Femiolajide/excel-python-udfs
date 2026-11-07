# excel-python-udfs
 
Excel functions written in Python and powered by [xlOil](https://xloil.readthedocs.io), for data problems that Excel's built-in functions handle badly or not at all. Each function is documented like a native Excel function, tested on awkward inputs, and returns proper Excel errors.
 
## Why this exists
 
Excel has many built-in functions, and they handle most data tasks well. Some tasks they cannot handle. Others need so many nested functions that the formula becomes hard to write, read and check. I write my logic in Python, not VBA, so when Excel runs out of options I build the missing function in Python and call it from a cell.
 
The aim is more than cleaning, reshaping or analysing data once. It is to build reusable tools that give the same result every time, so that anyone can run them and trust the output.
 
## Where the functions come from
 
- Real problems I have faced in my own data analysis work.
- Features I wish Excel had.
- Ideas I think are useful in data analysis generally.
It is also practice. Each function means turning a problem into clear logic, then turning that logic into working Python.
 
## What every function includes
 
- **A documentation page** in the style of Excel's own function pages: syntax, arguments, remarks, errors and examples.
- **Defined behaviour for awkward input,** such as blanks, numbers entered as text, upper and lower case, and values out of range.
- **Excel errors, not Python errors.** Bad input returns `#N/A` or `#VALUE!`, so the result works with `IFERROR` and `IFNA`.
- **Examples that have been run in Excel,** with the results shown on the page.
- **A repeatable result.** The same input always gives the same output.
I explain the thinking behind individual functions in my [LinkedIn posts](https://www.linkedin.com/in/olajide-atanda-084756239).
 
## Functions
 
The [function index](docs/index.md) lists every function with a one-line description and its status. Each function has its own page in the `docs` folder.
 

## Requirements
 
- Microsoft Excel for Windows
- Python
- xlOil
## Installation
 
See the [xlOil documentation](https://xloil.readthedocs.io) for how to install xlOil and load Python modules.
 

## Using a function
 
After installation, the functions appear in Excel's function list under their group name, and you use them like any other function. Open the function's page in `docs` for its syntax and examples.
 

## Feedback
 
If a function gives a result you did not expect, please open an issue with the formula, the input and the result you expected. Do not include real or confidential data. Use made-up examples.

 
## About
- [LinkedIn](https://www.linkedin.com/in/olajide-atanda-084756239)






