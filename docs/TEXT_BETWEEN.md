# TEXT_BETWEEN function
 
Returns the text between two delimiters. You can choose which occurrence of each delimiter to use, counting from the start or the end of the text.
 
## Syntax
 
```
=TEXT_BETWEEN(text, left_del, right_del, [left_del_inst_num], [right_del_inst_num])
```
 
## Arguments
 
| Argument | Required | Description |
| --- | --- | --- |
| `text` | Yes | The text to search. |
| `left_del` | Yes | The delimiter that marks the start of the text to extract. |
| `right_del` | Yes | The delimiter that marks the end of the text to extract. |
| `left_del_inst_num` | No | Which occurrence of `left_del` to use. The default is 1. A negative number counts from the end of `text`: -1 is the last occurrence, -2 the second to last, and so on. |
| `right_del_inst_num` | No | Which occurrence of `right_del` to use. The default is 1. Negative numbers work as for `left_del_inst_num`. |
 
## Remarks
 
- The function is case-sensitive. `"A"` and `"a"` are different delimiters.
- Delimiters are matched exactly as typed. No character has a special meaning, including `\`, `*`, `?`, `~` and `|`.
- All arguments are treated as text, so the function works on numeric columns. Numbers are converted to text with up to 15 significant digits, as Excel does, and TRUE and FALSE become `"TRUE"` and `"FALSE"`.
- The returned text does not include the delimiters.
- Instance numbers are counted separately for each delimiter, across the whole of `text`. Occurrences do not overlap: in `aaaa`, the delimiter `aa` occurs twice.
- The chosen right delimiter must come after the chosen left delimiter. If it does not, the result is `#N/A`.
- When `left_del` and `right_del` are the same, the default instance numbers (1 and 1) select the same character, so the result is `#N/A`. Use a later instance number for `right_del`, for example `=TEXT_BETWEEN(A1, "a", "a", 1, 2)`.
- A decimal instance number is truncated towards zero, not rounded, as in `TEXTBEFORE` and `TEXTAFTER`. For example, 2.9 is treated as 2, and 0.5 is treated as 0.
- Unlike `TEXTBEFORE` and `TEXTAFTER`, which match an empty delimiter immediately, `TEXT_BETWEEN` returns `#VALUE!` for an empty delimiter.
- The function returns Excel errors, not Python errors. See [Errors](#errors).
## Errors
 
| Condition | Result |
| --- | --- |
| `left_del` or `right_del` is an empty string | `#VALUE!` |
| An instance number is not a number | `#VALUE!` |
| An instance number is 0 (after truncation) | `#VALUE!` |
| `left_del` or `right_del` is not found in `text` | `#N/A` |
| An instance number is larger than the number of times that delimiter occurs in `text` | `#N/A` |
| The chosen right delimiter is not after the chosen left delimiter | `#N/A` |
 
The checks run in the order shown, so `#VALUE!` always comes before `#N/A`. For example, `=TEXT_BETWEEN("Hello world", "[", "]", 0, 1)` returns `#VALUE!` even though neither delimiter is in the text.
 
## Examples
 
| Formula | Result | Explanation |
| --- | --- | --- |
| `=TEXT_BETWEEN("Invoice [INV-2041] paid", "[", "]")` | `INV-2041` | Text between the first `[` and the first `]`. |
| `=TEXT_BETWEEN("amina@example.com", "@", ".")` | `example` | Extracts the domain name from an email address. |
| `=TEXT_BETWEEN(12345, 2, 4)` | `3` | Numbers are treated as text. |
| `=TEXT_BETWEEN(1234.5, "1", ".")` | `234` | A decimal number is converted to the text `1234.5`. |
| `=TEXT_BETWEEN("C:\Users\Ada\file", "\", "\", 1, 2)` | `Users` | A backslash is matched as an ordinary character. |
 
### Choosing instances of a repeated delimiter
 
The text in cell `A1` is `aabcaadahyyadf`. The letter `a` occurs six times.
 
| Formula | Result | Explanation |
| --- | --- | --- |
| `=TEXT_BETWEEN(A1, "a", "a", 1, 3)` | `abc` | From the 1st `a` to the 3rd `a`. |
| `=TEXT_BETWEEN(A1, "a", "a", 2, 3)` | `bc` | From the 2nd `a` to the 3rd `a`. |
| `=TEXT_BETWEEN(A1, "a", "a", 3, 5)` | `ad` | From the 3rd `a` to the 5th `a`. |
| `=TEXT_BETWEEN("[a][b][c]", "[", "]", 2, 2)` | `b` | From the 2nd `[` to the 2nd `]`. |
 
### Counting from the end
 
| Formula | Result | Explanation |
| --- | --- | --- |
| `=TEXT_BETWEEN(A1, "a", "a", 1, -1)` | `abcaadahyy` | From the 1st `a` to the last `a`. |
| `=TEXT_BETWEEN(A1, "a", "a", -2, -1)` | `hyy` | From the second-to-last `a` to the last `a`. |
 
### Decimal instance numbers
 
| Formula | Result | Explanation |
| --- | --- | --- |
| `=TEXT_BETWEEN(A1, "a", "a", 2.9, 3)` | `bc` | 2.9 is truncated to 2. |
| `=TEXT_BETWEEN(A1, "a", "a", 1, 3.9)` | `abc` | 3.9 is truncated to 3. |
 
### Errors
 
| Formula | Result | Explanation |
| --- | --- | --- |
| `=TEXT_BETWEEN("Name: Ada", "name", ":")` | `#N/A` | `"name"` is not found because the search is case-sensitive. |
| `=TEXT_BETWEEN(A1, "a", "a")` | `#N/A` | Both delimiters select the 1st `a`. |
| `=TEXT_BETWEEN(A1, "a", "a", 3, 2)` | `#N/A` | The 2nd `a` is before the 3rd `a`. |
| `=TEXT_BETWEEN(A1, "a", "a", 1, 9)` | `#N/A` | `a` occurs only six times. |
| `=TEXT_BETWEEN(A1, "a", "a", -7, -1)` | `#N/A` | There is no seventh `a` from the end. |
| `=TEXT_BETWEEN(A1, "a", "a", 0, 3)` | `#VALUE!` | An instance number cannot be 0. |
| `=TEXT_BETWEEN(A1, "a", "a", 0.5, 3)` | `#VALUE!` | 0.5 is truncated to 0. |
| `=TEXT_BETWEEN("Hello world", "[", "]", 0, 1)` | `#VALUE!` | The instance number is checked before the delimiters are searched for. |
| `=TEXT_BETWEEN("abc", "", "c")` | `#VALUE!` | A delimiter cannot be empty. |
 
## Design notes
 
- **Why instance numbers.** Two delimiters can be ambiguous. In `aabcaadahyyadf`, the text between `a` and `a` could start and end at several places, so each delimiter has its own instance number.
- **Why Excel errors.** An out-of-range instance number returns `#N/A` instead of showing a Python index error, so the result behaves like the results of Excel's own functions and can be handled with `IFERROR` or `IFNA`.
## See also
 
[TEXTBEFORE](https://support.microsoft.com/en-us/excel/functions/textbefore-function), [TEXTAFTER](https://support.microsoft.com/en-us/excel/functions/textafter-function)
 