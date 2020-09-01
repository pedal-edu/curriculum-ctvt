import unittest
from textwrap import dedent

from pedal.core import *
from pedal.core.report import MAIN_REPORT
from pedal.core.commands import clear_report, suppress, contextualize_report
from pedal.sandbox.commands import get_sandbox
from pedal.source import verify
from pedal.tifa import tifa_analysis
from pedal.resolvers import simple
from pedal.sandbox import commands
from pedal.cait.cait_api import parse_program
from curriculum_ctvt.plotting import assert_one_of_plots
from curriculum_ctvt.iteration_context import plot_group_error
import tate
import matplotlib.pyplot as plt

code_hist_and_plot = ('''
import matplotlib.pyplot as plt
plt.hist([1,2,3])
plt.title("My line plot")
plt.show()
plt.plot([4,5,6])
plt.show()''')[1:]

SUCCESS_MESSAGE = "Complete\nGreat work!"
SUCCESS_TEXT = "Great work!"


class Execution:
    """

    """
    def __init__(self, code, tracer_style='none', old_style_messages=False,
                 run_tifa=True, report=MAIN_REPORT):
        self.code = code
        self.tracer_style = tracer_style
        self.old_style_messages = old_style_messages
        self.report=report
        self.final = None
        self.run_tifa = run_tifa

    def __enter__(self):
        clear_report(report=self.report)
        contextualize_report(self.code, report=self.report)
        verify(report=self.report)
        if self.run_tifa:
            tifa_analysis(report=self.report)
        # TODO: Clean this up
        self.student = get_sandbox(self.report)
        self.student.report_exceptions_mode = True
        self.report['sandbox']['sandbox'].tracer_style = self.tracer_style
        commands.run()
        return self

    def __exit__(self, *args):
        suppress("runtime", "FileNotFoundError", report=self.report)
        self.final = simple.resolve()
        self.feedback = """{title}\n{message}""".format(
            title=self.final.title,
            message=self.final.message
        )


class ExecutionTestCase(unittest.TestCase):
    def assertFeedback(self, execution, feedback_string):
        """

        Args:
            execution:
            feedback_string:

        Returns:

        """
        return self.assertEqual(dedent(feedback_string).lstrip(), execution.feedback)

    def test_check_for_plot_correct_hist(self):
        with Execution(code_hist_and_plot) as e:
            self.assertEqual(assert_one_of_plots('hist', [[1, 2, 3]]), False)
        self.assertFeedback(e, SUCCESS_MESSAGE)

    def test_check_for_plot_correct_hist_alt(self):
        with Execution(code_hist_and_plot) as e:
            self.assertEqual(assert_one_of_plots('hist', [[4, 5, 6], [1, 2, 3]]), False)
        self.assertFeedback(e, SUCCESS_MESSAGE)

        with Execution(code_hist_and_plot) as e:
            self.assertEqual(assert_one_of_plots('hist', [[1, 2, 3], [4, 5, 6]]), False)
        self.assertFeedback(e, SUCCESS_MESSAGE)

        with Execution(code_hist_and_plot) as e:
            self.assertEqual(assert_one_of_plots('hist', [[1, 2, 3], [1, 2, 3, 4]]), False)
        self.assertFeedback(e, SUCCESS_MESSAGE)

        with Execution(code_hist_and_plot) as e:
            self.assertEqual(assert_one_of_plots('hist', [[1, 2, 3, 4], [1, 2, 3]]), False)
        self.assertFeedback(e, SUCCESS_MESSAGE)

    def test_check_for_plot_wrong_hist(self):
        with Execution(code_hist_and_plot) as e:
            assert_one_of_plots('hist', [[1, 2, 3, 4]])
        self.assertFeedback(e, "Plot Data Incorrect\n"
                               "You have created a histogram, but it does not "
                               "have the right data.")

    def test_check_for_plot_wrong_hist_alt(self):
        with Execution(code_hist_and_plot) as e:
            assert_one_of_plots('hist', [[1, 2, 3, 4], [4, 5, 6]])
        self.assertFeedback(e, "Plotting Another Graph\n"
                               "You have created a histogram, but it does not "
                               "have the right data. That data appears to have been plotted in another graph.")

        with Execution(code_hist_and_plot) as e:
            assert_one_of_plots('hist', [[4, 5, 6], [1, 2, 3, 4]])
        self.assertFeedback(e, "Plotting Another Graph\n"
                               "You have created a histogram, but it does not "
                               "have the right data. That data appears to have been plotted in another graph.")

    def test_check_for_plot_correct_plot(self):  # TODO: Write a more complete unit test
        with Execution(code_hist_and_plot) as e:
            self.assertEqual(assert_one_of_plots('line', [[4, 5, 6]]), False)
        self.assertFeedback(e, SUCCESS_MESSAGE)

    def test_check_for_plot_wrong_plot(self):  # TODO: Write a more complete unit test
        with Execution(code_hist_and_plot) as e:
            assert_one_of_plots('line', [[4, 5, 6, 7]])
        self.assertFeedback(e, "Plot Data Incorrect\n"
                               "You have created a line plot, but it does not "
                               "have the right data.")

    def test_assert_one_of_plots_wrong_type_of_plot(self):  # TODO: Write a more complete unit test
        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.plot([1,2,3])
            plt.title("My line plot")
            plt.show()
        ''')
        with Execution(student_code) as e:
            assert_one_of_plots('hist', [[1, 2, 3]])
        self.assertFeedback(e, "Wrong Plot Type\n"
                               "You have plotted the right data, but you appear "
                               "to have not plotted it as a histogram.")

    def test_assert_one_of_plots_wrong_data_place(self):  # TODO: Write a more complete unit test
        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.plot([1,2,3])
            plt.title("Wrong graph with the right data")
            plt.show()
            plt.hist([4,5,6])
            plt.title("Right graph with the wrong data")
            plt.show()
        ''')
        with Execution(student_code) as e:
            assert_one_of_plots('hist', [[1, 2, 3]])
        self.assertFeedback(e, "Plotting Another Graph\n"
                               "You have created a histogram, but it does not "
                               "have the right data. That data appears to have "
                               "been plotted in another graph.")

    def test_assert_one_of_plots_missing_plot_and_data(self):  # TODO: Write a more complete unit test
        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.plot([1,2,3])
            plt.title("My line plot")
            plt.show()
        ''')
        with Execution(student_code) as e:
            assert_one_of_plots('hist', [[4, 5, 6]])
        self.assertFeedback(e, "Missing Plot\n"
                               "You have not created a histogram with the proper data.")

    def test_assert_one_of_plots_empty_scatter(self):  # TODO: Write a more complete unit test
        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.scatter([], [])
            plt.title("Nothingness and despair")
            plt.show()
        ''')
        with Execution(student_code) as e:
            assert_one_of_plots('scatter', [[]])
        self.assertFeedback(e, SUCCESS_MESSAGE)

    def test_assert_one_of_plots_simple_scatter(self):  # TODO: Write a more complete unit test
        student_code = dedent('''
            import matplotlib.pyplot as plt
            plt.scatter([1,2,3], [4,5,6])
            plt.title("Some actual stuff")
            plt.show()
        ''')
        with Execution(student_code) as e:
            assert_one_of_plots('scatter', [[[1, 2, 3], [4, 5, 6]]])
        self.assertFeedback(e, SUCCESS_MESSAGE)
