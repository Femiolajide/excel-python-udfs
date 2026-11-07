import xloil 
# safe string conversion
@xloil.converter()
def ExcelStringType(val):
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    else:
        return str(val)


@xloil.func(name="TEXT_BETWEEN",
            help="Extracts the text between two delimiters",
            args={"text":"The text to extract from",
                  "left_del":"The left delimiter",
                  "right_del":"The right delimiter",
                  "left_del_inst_num":"The instance number of the first delimiter",
                  "right_del_inst_num":"The instance number of the second delimiter",
                  },
                  group="MY TEXT FUNCTIONS")
def text_between(text:ExcelStringType,
                 left_del:ExcelStringType,
                 right_del:ExcelStringType,
                 left_del_inst_num=1,
                 right_del_inst_num=1,
                 ) -> str | xloil.CellError:
    left_del_inst_num = int(left_del_inst_num)
    right_del_inst_num = int(right_del_inst_num)
    if left_del == "" or right_del == "":
        return ""
    if left_del_inst_num == 0 or right_del_inst_num == 0:
        return xloil.CellError.VALUE
    if left_del not in text or right_del not in text:
        return xloil.CellError.NA
    if abs(left_del_inst_num) > text.count(left_del):
        return xloil.CellError.NA
    if abs(right_del_inst_num) > text.count(right_del):
        return xloil.CellError.NA
    right_del_occr = text.count(right_del)
    right_del_occr = right_del_occr + 1
    right_del_occr = -1 * right_del_occr
    if right_del_inst_num > 0:
        right_del_inst_num = right_del_occr + right_del_inst_num
    # inner function to find the index number of a string 
    # this custom function supports instance number
    def find(text:str, x:str, occr=1) -> int:
        def sep_list(text:str,sep:str)->list:
            text = str(text)
            sep = str(sep)
            splited = text.split(sep)
            good_sep = []
            for y,x in enumerate(splited,1):
                good_sep.append(x)
                if y != len(splited):
                    good_sep.append(sep)
            return good_sep
        split_list = sep_list(text,x)
        text_dict = {k:v for k,v in 
                    enumerate(split_list)}
        search_dict = {k:v for k,v in 
                    text_dict.items()
                    if v == x}
        search_list = [*search_dict.items()]
        if occr > 0:
            index = search_list[int(occr) - 1][0]
            return index,split_list
        elif occr < 0:
            index = search_list[int(occr)][0]
            return index,split_list
    try:
        index_1, text_list_1 = find(text,
                                    left_del,
                                    left_del_inst_num)
        text_2 = "".join(text_list_1[index_1 + 1:])
        index_2, text_list_2 = find(text_2,
                                    right_del,
                                    right_del_inst_num)
        res = "".join(text_list_2[:index_2])
        return res
    except IndexError:
        return xloil.CellError.NA
