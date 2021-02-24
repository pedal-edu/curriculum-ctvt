from pedal.cait.cait_api import *
from pedal.core.commands import *


def missing_conversion_group():
    missing_conversion_1()
    missing_conversion_2()
    missing_conversion_3()
    missing_conversion_4()


def wrong_conversion_group_int():
    wrong_conversion_int_1()
    wrong_conversion_int_2()


def wrong_conversion_group_float():
    wrong_conversion_float_1()
    wrong_conversion_float_2()


def missing_conversion_1():
    MESSAGE = 'The input is always a string and must be converted to a number before being used in an arithmetic calculation.'
    LABEL = 'miss_conv_1'
    TITLE = 'Missing Conversion.'
    find0 = find_matches("""

_var_ = input()

__expr__""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    within0 = []
    for match in prev_matchset:
        __expr__ = match['__expr__']
        within0.extend(__expr__.find_matches("""_var_ * ___""", use_previous = match))
    prev_matchset = within0
    if within0:
        prev_found_matchset = within0
    where0 = []
    for match in prev_matchset:
        _var_ = match['_var_']
        if not _var_.was_type(float):
            where0.append(match)
    prev_matchset = where0
    if where0:
        prev_found_matchset = where0
    if prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def missing_conversion_2():
    MESSAGE = 'The input is always a string and must be converted to a number before being used in an arithmetic calculation.'
    LABEL = 'miss_conv_2'
    TITLE = 'Missing Conversion.'
    find0 = find_matches("""

_var_ = input()

__expr__""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    within0 = []
    for match in prev_matchset:
        __expr__ = match['__expr__']
        within0.extend(__expr__.find_matches("""_var_  +  ___""", use_previous = match))
    prev_matchset = within0
    if within0:
        prev_found_matchset = within0
    where0 = []
    for match in prev_matchset:
        _var_ = match['_var_']
        if not _var_.was_type(float):
            where0.append(match)
    prev_matchset = where0
    if where0:
        prev_found_matchset = where0
    if prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def missing_conversion_3():
    MESSAGE = 'The input is always a string and must be converted to a number before being used in an arithmetic calculation.'
    LABEL = 'miss_conv_3'
    TITLE = 'Missing Conversion.'
    find0 = find_matches("""

_var_ = input()

__expr__""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    within0 = []
    for match in prev_matchset:
        __expr__ = match['__expr__']
        within0.extend(__expr__.find_matches("""_var_  - ___""", use_previous = match))
    prev_matchset = within0
    if within0:
        prev_found_matchset = within0
    where0 = []
    for match in prev_matchset:
        _var_ = match['_var_']
        if not _var_.was_type(float):
            where0.append(match)
    prev_matchset = where0
    if where0:
        prev_found_matchset = where0
    if prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def missing_conversion_4():
    MESSAGE = 'The input is always a string and must be converted to a number before being used in an arithmetic calculation.'
    LABEL = 'miss_conv_4'
    TITLE = 'Missing Conversion.'
    find0 = find_matches("""

_var_ = input()

__expr__""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    within0 = []
    for match in prev_matchset:
        __expr__ = match['__expr__']
        within0.extend(__expr__.find_matches("""_var_  / ___""", use_previous = match))
    prev_matchset = within0
    if within0:
        prev_found_matchset = within0
    where0 = []
    for match in prev_matchset:
        _var_ = match['_var_']
        if not _var_.was_type(float):
            where0.append(match)
    prev_matchset = where0
    if where0:
        prev_found_matchset = where0
    if prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def wrong_conversion_int_1():
    MESSAGE = 'The input is a number with a decimal point. The conversion should reflect this type of number.'
    LABEL = 'wr_conv_int_1'
    TITLE = 'Wrong Conversion'
    find0 = find_matches("""

_var_ = input()

__expr1__ """)
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    within0 = []
    for match in prev_matchset:
        __expr1__ = match['__expr1__']
        within0.extend(__expr1__.find_matches("""int(_var_) """, use_previous = match))
    prev_matchset = within0
    if within0:
        prev_found_matchset = within0
    if prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def wrong_conversion_int_2():
    MESSAGE = 'The input is a number with a decimal point. The conversion should reflect this type of number.'
    LABEL = 'wr_conv_int_2'
    TITLE = 'Wrong Conversion'
    find0 = find_matches("""int(input()) """)
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    if prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def wrong_conversion_float_1():
    MESSAGE = 'The input is a whole number. The conversion should reflect this type of number.'
    LABEL = 'wr_conv_float_1'
    TITLE = 'Wrong Conversion'
    find0 = find_matches("""

_var_ = input()

__expr1__ """)
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    within0 = []
    for match in prev_matchset:
        __expr1__ = match['__expr1__']
        within0.extend(__expr1__.find_matches("""float(_var_) """, use_previous = match))
    prev_matchset = within0
    if within0:
        prev_found_matchset = within0
    if prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def wrong_conversion_float_2():
    MESSAGE = 'The input is a whole number. The conversion should reflect this type of number.'
    LABEL = 'wr_conv_float_2'
    TITLE = 'Wrong Conversion'
    find0 = find_matches("""___ = float(input()) """)
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    if prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def missing_input():
    MESSAGE = 'The problem requires that a value be input by the user.'
    LABEL = 'miss_input'
    TITLE = 'Missing Input'
    find0 = find_matches("""input()""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    if not prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def missing_inputs():
    MESSAGE = 'The problem requires that two values be input by the user.'
    LABEL = 'miss_inputs'
    TITLE = 'Missing Inputs'
    find0 = find_matches("""

___ = __expr1__

___ = __expr2__ """)
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    within0 = []
    for match in prev_matchset:
        __expr1__ = match['__expr1__']
        within0.extend(__expr1__.find_matches("""input()""", use_previous = match))
    prev_matchset = within0
    if within0:
        prev_found_matchset = within0
    within1 = []
    for match in prev_matchset:
        __expr2__ = match['__expr2__']
        within1.extend(__expr2__.find_matches("""input()""", use_previous = match))
    prev_matchset = within1
    if within1:
        prev_found_matchset = within1
    if not prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def missing_output():
    MESSAGE = 'The problem requires that a value be output by the program.'
    LABEL = 'miss_output'
    TITLE = 'Missing Output'
    find0 = find_matches("""print()""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    if not prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def missing_outputs():
    MESSAGE = 'The problem requires that two values be output by the user.'
    LABEL = 'miss_outputs'
    TITLE = 'Missing Outputs'
    find0 = find_matches("""

print()

print() """)
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    if not prev_matchset:
        if prev_found_matchset:
            return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
        else:
            return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False
