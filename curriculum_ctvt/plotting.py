from pedal import Feedback, CompositeFeedbackFunction
from pedal.assertions import ensure_function_call, prevent_function_call
from pedal.core.feedback import FeedbackResponse
from pedal.core.report import MAIN_REPORT
from pedal.types.builtin import BUILTIN_MODULES
from pedal.types.definitions import ModuleType, FunctionType, NoneType
from pedal.cait.find_node import function_is_called
from pedal.cait.cait_api import parse_program, def_use_error
from pedal.sandbox.commands import get_sandbox
from pedal.extensions.plotting import other_plt, wrong_plt_data, wrong_plt_type, no_plt, GRAPH_TYPES, compare_data
from collections import namedtuple


@CompositeFeedbackFunction(other_plt, wrong_plt_data, wrong_plt_type, no_plt)
def assert_one_of_plots(plt_type, data_plots, **kwargs):
    """
    Check whether a plot with the given ``plt_type`` and one of``data`` exists.
    If the plot was found successfully, returns False.
    Otherwise, returns the feedback that was detected.

    Args:
        plt_type (str): Either 'line', 'hist', or 'scatter'
        data (list): The expected data to check in the plots in osurce code. Each item in the
                    list should either be a list of numbers or a tuple of two lists (for scatter/line plots)
    """
    report = kwargs.get("report", MAIN_REPORT)
    # Allow instructor to use "plot" instead of "line" as type
    if plt_type == 'plot':
        plt_type = 'line'
    # Check the plots to see if there is a plot with the data
    type_found = False
    data_found = False
    plots = get_sandbox(report=report).modules.plotting.plots
    for graph in plots:
        for a_plot in graph['data']:
            data_found_here = False
            for data in data_plots:
                data_found_here = compare_data(plt_type, data, a_plot)
                if data_found_here:
                    break
            if a_plot['type'] == plt_type and data_found_here:
                return False
            if a_plot['type'] == plt_type:
                type_found = True
            if data_found_here:
                data_found = data_found_here
    # Figure out what kind of mistake was made.
    data = data_plots[-1]
    plt_type = GRAPH_TYPES.get(plt_type, plt_type)
    if type_found and data_found:
        return other_plt(plt_type, data, data_found)
    elif type_found:
        return wrong_plt_data(plt_type, data, data_found)
    elif data_found:
        return wrong_plt_type(plt_type, data, data_found)
    else:
        return no_plt(plt_type, data, data_found)
