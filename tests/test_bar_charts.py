import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.mistake_test_template import *
from curriculum_ctvt.bar_charts import *
from pedal.resolvers import simple


class DictionaryMistakeTest(MistakeTest):
    def test_parameter_lists(self):
        self.to_source("list1 = [1, 2, 3]\n"
                       "list2 = [1, 2, 3]\n"
                       "list3 = [1, 2, 3]\n"
                       "plt.bar(list1, list2, tick_label=list3)")
        result = parameter_lists()
        self.assertFalse(result, "false positive")

        self.to_source("list1 = 1\n"
                       "list2 = [1, 2, 3]\n"
                       "list3 = [1, 2, 3]\n"
                       "plt.bar(list1, list2, tick_label=list3)")
        result = parameter_lists()
        self.assertTrue("1" in result.message, "false negative")

        self.to_source("list1 = [1, 2, 3]\n"
                       "list2 = 2\n"
                       "list3 = [1, 2, 3]\n"
                       "plt.bar(list1, list2, tick_label=list3)")
        result = parameter_lists()
        self.assertTrue(result, "false negative")
        self.assertTrue("2" in result.message)

        self.to_source("list1 = [1, 2, 3]\n"
                       "list2 = [1, 2, 3]\n"
                       "list3 = 3\n"
                       "plt.bar(list1, list2, tick_label=list3)")
        result = parameter_lists()
        self.assertTrue("3" in result.message, "false negative")

    def test_parameter_types(self):
        self.to_source("list1 = [1, 2, 3]\n"
                       "list2 = [1, 2, 3]\n"
                       "list3 = ['a', 'a', 'a']\n"
                       "plt.bar(list1, list2, tick_label=list3)")
        result = parameter_types()
        self.assertFalse(result, "false positive")

        self.to_source("list1 = ['a', 'a', 'a']\n"
                       "list2 = [1, 2, 3]\n"
                       "list3 = [1, 2, 3]\n"
                       "plt.bar(list1, list2, tick_label=list3)")
        result = parameter_types()
        self.assertTrue(result, "false negative")
        self.assertTrue("1" in result.message)

        self.to_source("list1 = [1, 2, 3]\n"
                       "list2 = [1, 2, 3]\n"
                       "list3 = [1, 2, 3]\n"
                       "plt.bar(list1, list2, tick_label=list3)")
        result = parameter_types()
        self.assertTrue(result, "false negative")
        self.assertTrue("3" in result.message)