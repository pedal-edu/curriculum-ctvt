from pedal.cait.cait_api import *
from pedal.core.commands import *


def wrong_calculation_61():
    MESSAGE = 'The calculation of miles from kilometers does not seem correct.'
    LABEL = 'wr_cacl_61'
    TITLE = 'Wrong Calculation'
    find0 = find_matches("""
_var1_ = __inexpr__
___ = __expr__ * 0.67 """)
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    within0 = []
    for match in prev_matchset:
        __inexpr__ = match['__inexpr__']
        within0.extend(__inexpr__.find_matches("""input()""", use_previous = match))
    prev_matchset = within0
    if within0:
        prev_found_matchset = within0
    within1 = []
    for match in prev_matchset:
        __expr__ = match['__expr__']
        within1.extend(__expr__.find_matches("""_var1_""", use_previous = match))
    prev_matchset = within1
    if within1:
        prev_found_matchset = within1
    if not prev_matchset:
        return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
    return False


def wrong_output_61():
    MESSAGE = 'The variable used for output does not seem correct.'
    LABEL = 'wr_output_61'
    TITLE = 'Wrong Output'
    find0 = find_matches("""
_var1_ = __inexpr__
_var2_= __expr__ * 0.67
print(__expr2__)""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    within0 = []
    for match in prev_matchset:
        __inexpr__ = match['__inexpr__']
        within0.extend(__inexpr__.find_matches("""input()""", use_previous = match))
    prev_matchset = within0
    if within0:
        prev_found_matchset = within0
    within1 = []
    for match in prev_matchset:
        __expr__ = match['__expr__']
        within1.extend(__expr__.find_matches("""_var1_""", use_previous = match))
    prev_matchset = within1
    if within1:
        prev_found_matchset = within1
    within2 = []
    for match in prev_matchset:
        __expr2__ = match['__expr2__']
        within2.extend(__expr2__.find_matches("""_var2_""", use_previous = match))
    prev_matchset = within2
    if within2:
        prev_found_matchset = within2
    if not prev_matchset:
        return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
    return False


def wrong_calc_62():
    """
    BEGIN wrong_calc_62()
    MESSAGE
    LABEL
    TITLE
    FIND `___ * 1.15`
    IF FOUND GIVE NO FEEDBACK
    FIND `___ * 0.15`
    IF NOT FOUND GIVE FEEDBACK
    END

    """
    message = 'The calculation does not appear to be correct.'
    label = 'wr_calc_62'
    title = 'Wrong Calculation'

    if not find_match("___ * 1.15") and not find_match("___ * 0.15"):
        explain(message, label=label, title=title)


def wrong_calc_cw_6_3_5():
    MESSAGE = 'The calculation of the exchange amount does not appear to be correct.'
    LABEL = 'wr_calc_cw_6_3_5'
    TITLE = 'Wrong Calculation'
    find0 = find_matches("""___ /  ___""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    if prev_matchset:
        return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
    return False


def missing_constant_981():
    MESSAGE = 'Need to use the cost per square yard (9.81) in the cost calculations.'
    LABEL = 'miss_9.81'
    TITLE = 'Missing Cost Factor'
    find0 = find_matches("""9.81""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    if not prev_matchset:
        return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
    return False


def missing_constant_150():
    MESSAGE = 'Need to use the installation cost per square yard (1.50) in the cost calculations.'
    LABEL = 'miss_1.50'
    TITLE = 'Missing Cost Factor'

    find0 = find_matches("""1.50""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    if not prev_matchset:
        return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def missing_area_calc():
    MESSAGE = 'Check that you have calculated correctly the area of the carpet.'
    LABEL = 'miss_area'
    TITLE = 'Missing Area Calculation'

    '''
    find0 = find_matches("""
_var1_ = __expr1__
_var2_ = __expr2__
___ = __expr3__ * _expr4_""")
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
    within2 = []
    for match in prev_matchset:
        __expr3__ = match['__expr3__']
        within2.extend(__expr3__.find_matches("""_var1_""", use_previous = match))
    prev_matchset = within2
    if within2:
        prev_found_matchset = within2
    within3 = []
    for match in prev_matchset:
        __expr4__ = match['__expr4__']
        within3.extend(__expr4__.find_matches("""_var2_""", use_previous = match))
    prev_matchset = within3
    if within3:
        prev_found_matchset = within3
    if not prev_matchset:
        return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False
    '''

    find0 = find_matches("_var1_ = __expr1__\n"
                         "_var2_ = __expr2__\n"
                         "___ = __expr3__ * _expr4_\n")
    for match in find0:
        match0 = find_match("input()")
        match1 = find_match("input()")
        match2 = find_match("_var1_")
        match3 = find_match("_var2_")
        if not (match0 and match1 and match2 and match3):
            return explain(message=MESSAGE, label=LABEL, title=TITLE)


def missing_average_calc():
    MESSAGE = 'Check your calculation to see if both parties pay the same amount.'
    LABEL = 'miss_div_2'
    TITLE = 'Missing part of calculation'
    find0 = find_matches("""
___ = ___ / 2 """)
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    if prev_matchset:
        return explain(message=MESSAGE.format(**prev_found_matchset[0].names()), label=LABEL, title=TITLE)
    return False


def missing_constant_12():
    MESSAGE = 'Be sure that you are representing the positivity rate correctly.'
    LABEL = 'miss_0.12'
    TITLE = 'Missing Positivity Rate'
    find0 = find_matches("""0.12""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    if not prev_matchset:
        return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False


def missing_constant_034():
    MESSAGE = 'Be sure that you are representing the death rate correctly.'
    LABEL = 'miss_0.034'
    TITLE = 'Missing Death Rate'
    find0 = find_matches("""0.034""")
    prev_matchset = find0
    prev_found_matchset = []
    if find0:
        prev_found_matchset = find0
    if not prev_matchset:
        return explain(message=MESSAGE, label=LABEL, title=TITLE)
    return False

