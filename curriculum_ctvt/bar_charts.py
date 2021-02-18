from pedal.cait.cait_api import (parse_program, find_match, find_matches,
                                 find_expr_sub_matches, data_state,
                                 def_use_error)
from pedal.core.commands import gently, explain
from pedal.types.definitions import *
"""
2. 

3. 

4. 
"""


def bar_group():
    parameter_lists()
    parameter_types()


def parameter_lists():
    """
        Each of the three parameters is a list (feedback: parameters n should be a list)
        Returns:

    """
    message = 'Parameter {_list_} should be a list'
    code = "non_list_bar"
    tldr = "Non-List Passed to Bar"
    matches = find_matches("plt.bar(_list1_, _list2_, tick_label=_list3_)")
    for match in matches:
        list_var = [match["_list1_"], match["_list2_"], match["_list3_"]]
        count = 0
        while count < 3:
            if not list_var[count].was_type('list'):
                return explain(message.format(_list_=count + 1), label=code, title=tldr)
            count += 1
    return False


def parameter_types():
    """
        the first two lists have values that are ints or floats (feedback: parameter n must be a number type)
        Returns:

    """
    message = 'Parameter {} must be a {} type'
    code = "wrong_bar_types"
    tldr = "Bar Chart Parameter(s) Incorrect"
    matches = find_matches("plt.bar(_list1_, _list2_, tick_label=_list3_)")
    for match in matches:
        _list1_ = match["_list1_"]
        _list2_ = match["_list2_"]
        _list3_ = match["_list3_"]
        if _list1_.was_type('list'):
            if not type(data_state(_list1_).type.subtype) == NumType:
                return explain(message.format(1, "number"), label=code, title=tldr)
        if _list2_.was_type('list'):
            if not type(data_state(_list2_).type.subtype) == NumType:
                return explain(message.format(2, "number"), label=code, title=tldr)
        if _list3_.was_type('list'):
            if not type(data_state(_list3_).type.subtype) == StrType:
                return explain(message.format(3, "string"), label=code, title=tldr)
    return False
