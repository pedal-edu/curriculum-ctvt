from pedal.cait.cait_api import *
from pedal.environments.quick import *
from pedal.sandbox.commands import *
import importlib.util
import numpy as np
import pandas as pd
import time
import importlib
import sys
import os
import re
import itertools as it
from scipy import stats
import math
import traceback
from tqdm import tqdm


def setup(student_code, input_vals):
    """
    Clears MAIN_REPORT, sets source, and runs TIFA
    Args:
        student_code: String of student code
        input_vals: list of inputs to be queued.
    Returns:
        None
    """
    contextualize_report(student_code)
    tifa_analysis()
    if len(input_vals) != 0:
        queue_input(*input_vals)
    # run(threaded=True)
    return get_sandbox()


def process(student_code1, module, ins_code, report, input_vals=None, codestate=-1):
    # student_code1 = file.read()
    student_run = setup(student_code1, input_vals)  # setup returns a sandbox object
    student_run.allowed_time = 10
    student_run.run(threaded=True)
    # student_run.run()
    module.loader.exec_module(ins_code)
    feedback = report.feedback
    feedback_set = []
    label_set = set()
    for item in feedback:
        if item.label not in label_set:
            label_set.add(item.label)
            feedback_set.append(item)
    return {"feedback": feedback_set, "codestate": codestate}


def assignment_process(df, assignment, progs2_dir, ins_dir, main_file):
    asid = assignment['asid']
    ins_code = assignment['ins_code']
    test_in = assignment["inputs"]
    feedback_code = ins_dir + ins_code
    # Grabbing Module "name"
    ins_mod = ins_code[:-3]
    my_spec = importlib.util.spec_from_file_location(ins_mod, feedback_code)
    module = importlib.util.module_from_spec(my_spec)
    assignment["module"] = module
    # Yes: I realize we are iterating through the df multiple times.
    # instead of more efficiently running through the df sequentially
    total_iterations = 0
    student_feedback = []
    pass_count = 0
    t0 = time.time()
    label_set = {}
    for index, row in tqdm(df.iterrows(), total=len(df)):
        row_asid = int(row["AssignmentID"])
        if row_asid == asid or row_asid == -1:
            total_iterations += 1
            codestate_id = int(row['CodeStateID'])
            main_file_revamp = main_file
            if main_file is None:
                main_file_revamp = row["CodeStateSection"]
            code_f = progs2_dir + "CodeStates/" + str(codestate_id) + "/" + main_file_revamp
            try:
                with open(code_f) as code:
                    code_extracted = code.read(20000)
                feedback_result = process(code_extracted, my_spec, module, MAIN_REPORT, input_vals=test_in,
                                          codestate=codestate_id)
                feedback_result["row"] = index
                student_feedback.append(feedback_result)
                score = 0.0
                mistake_index = len(feedback_result['feedback'])
                # TODO: Get rid of these items in pedal v3
                # if "module_not_found" in feedback_result['feedback']:
                #    feedback_result['feedback'].remove("module_not_found")
                # if "unused_returned_value" in feedback_result['feedback']:
                #    feedback_result['feedback'].remove("unused_returned_value")
                if len(feedback_result['feedback']) == 1 and feedback_result['feedback'][0].label == "set_success":
                    score = 1.0
                    mistake_index -= 1.0
                    pass_count += 1
                df.at[index, 'Score'] = score
                df.at[index, 'mistake index'] = mistake_index
                for feedback in feedback_result['feedback']:
                    if feedback.label in label_set.keys():
                        label_set[feedback.label] += 1
                    else:
                        label_set[feedback.label] = 1
            except Exception as inst:
                # print(type(inst))
                # print(inst.args)
                # track = traceback.format_exc()
                # print(track)
                traceback.print_tb(inst.__traceback__)

            # if total_iterations >= 10:  # TODO: Remove this
            #     break
            # if total_iterations % 20 == 0:  # TODO: Remove this
            #    print(total_iterations)

    t1 = time.time()
    time_elapsed = t1 - t0
    print("asid: {}, time: {}".format(asid, time_elapsed))
    return {
        "pass_count": pass_count,
        "total submissions": total_iterations,
        "time_elapsed": time_elapsed,
        "label_set": label_set,
        "student_feedback": student_feedback
    }


def semester_process(assignments, progs2_dir, ins_dir, main_file, main_table="MainTable-2.csv"):
    """

    Args:
        assignments (list|dict): Assignments to process, the dictionary should provide
                                the assignment ids, the name of the instructor grading script,
                                as well as the inputs required for the student code. This establishes
                                a mapping from the assignments to the relevant instructor scripts
            feedback_map = [{"asid": 409, "ins_code": "name_of_instructor_script1.py", "inputs": []},
                            {"asid": 410, "ins_code": "name_of_instructor_script2.py", "inputs": []},
                            {"asid": 411, "ins_code": "name_of_instructor_script3.py", "inputs": []},
                            {"asid": 412, "ins_code": "name_of_instructor_script4.py", "inputs": []},
                            ...]
        progs2_dir (str): This should be the file path of the progsnap directory
        ins_dir (str): This should be the directory path to where all your instructor are in, such that
                            ins_dir + ins_code == the full path of the instructor script (note that ins_dir should
                            have a slash at the end of the string).
        main_file (str):  This should be the name of the student's "main" program file that should be run.
        main_table (str): Should be the name of the file that is the main table. Right now it defaults to
                            MainTable-2.csv for my own convenience, but really it should be MainTable.csv.

    Returns:
        This returns a list of dictionaries as follows:
            [{"asid": 409,
              "results": {'pass_count': 0, # how many people passed
                          'total submissions': 100, # number of submissions processed
                          'time_elapsed': 45.10},# how many second it took to run all the code
              "label_set": {"initialization_problem": 12,
                            "blank_source": 2,
                            ...},#A dictionary containing feedback labels as keys, and their counts as values
              "student_feedback": {"feedback": [Feedback(), Feedback(),...],#list of feedback generated
                                   "codestate": 22402, # code state id
                                   "row": 0} #the row in the main table that this feedback was generated for
              }
            ...]
    """
    df = pd.read_csv(progs2_dir + main_table)
    index = df.columns.get_loc("Score")
    df.insert(index, "mistake index", 0.0)
    results = []
    # Compile each module and store it for reloading
    for assignment in assignments:
        asid = assignment['asid']
        # TODO: Figure out how to add the directory to the namespace
        result = assignment_process(df, assignment, progs2_dir, ins_dir, main_file)
        results.append({"asid": asid, "result": result})
    return {"data_frame": df, "tests": results}


def get_all_feedback(results):
    all_labels = set()
    for test in results:
        key_set = test['result']['label_set'].keys()
        for key in key_set:
            all_labels.add(key)
    return all_labels


def add_feedback(data_frame, tests, all_feedback):
    df = data_frame
    for label in all_feedback:
        df[label] = 0

    for test in tests:
        student_list = test['result']['student_feedback']
        for student in student_list:
            feedback = student['feedback']
            student_labels = []
            for item in feedback:
                student_labels.append(item.label)
            df.loc[student['row'], student_labels] = 1


def compile_signatures(data_frame, table_len):
    comp_mist = {}
    result_rows = data_frame.iterrows()
    for index, row in result_rows:
        str_array = []
        sub_row = row[table_len:]
        # Get binary signature
        for item in sub_row:
            str_array.append(str(item))
        sig_part2 = ''.join(str_array)

        # Get assignment id
        sig_part1 = str(row['AssignmentID'])

        # combine both of them
        signature = ','.join([sig_part1, sig_part2])

        columns = sub_row[sub_row == 1]
        human = ','.join(columns.keys())
        if signature in comp_mist.keys():
            comp_mist[signature]['count'] += 1
        else:
            comp_mist[signature] = {"sig_human": human, "asid": sig_part1, 'count': 1, "sig_10": int(sig_part2, 2), "sig_2": "'" + sig_part2}
            comp_mist[signature].update(sub_row.to_dict())
    return list(comp_mist.values())


def mist_comb(results, combo_len):
    all_feedback = list(results['comp_mist_df']['sig_human'].drop_duplicates())
    combos = []
    for feedback in all_feedback:
        split_feedback = feedback.split(",")
        if len(split_feedback) >= combo_len:
            combos += it.combinations(split_feedback, combo_len)
    combo_dict_list = {}
    result_rows = results['comp_mist_df'].iterrows()
    for index, row in result_rows:
        for combo in combos:
            uncombo = list(combo)
            if (row[uncombo] == 1).all():
                sig_part1 = row['asid']
                sig_part2 = ','.join(uncombo)
                signature = ','.join([sig_part1, sig_part2])
                if signature in combo_dict_list:
                    combo_dict_list[signature]['count'] += 1
                else:
                    combo_dict_list[signature] = {"sig_human": sig_part2, "asid": sig_part1, 'count': 1}
    return list(combo_dict_list.values())


def occurrences(results, has_feedbacks=None, miss_feedbacks=None, asid = -1):
    has_feedbacks = [] if not has_feedbacks else has_feedbacks
    miss_feedbacks = [] if not miss_feedbacks else miss_feedbacks
    df = results['data_frame']
    df_result = df
    # finds list of rows that have 1 in columns listed by has_feedbacks (str)
    for feedback in has_feedbacks:
        df_result = df_result.loc[df_result[feedback] == 1]
    # finds list of rows that have 0 in columns listed by miss_feedbacks (str)
    for feedback in miss_feedbacks:
        df_result = df_result.loc[df_result[feedback] != 1]
    if asid != -1:
        df_result = df_result.loc[df_result["AssignmentID"] == asid]
    return df_result


def intersection(df_list):
    df_base = df_list[0]
    for df in df_list:
        df_base = df_base[df['EventID'].isin(df_base)]


def feedback_set(df, col_offset):
    # ignores the first col_offset columns and returns the columns with non-zero values
    df1 = df.iloc[:,0:col_offset]
    df2 = df.iloc[:,col_offset:]
    df2 = df2.loc[:, df2.sum(axis=0) > 0]
    return df1.join(df2)


def mann_u_assignment(df1, df2, asid, param):
    result = {}
    if asid == -1:
        df1_vals = df1[param]
        df2_vals = df2[param]
    else:
        df1_vals = df1.loc[df1['AssignmentID'] == asid][param]
        df2_vals = df2.loc[df2['AssignmentID'] == asid][param]
    try:
        result["statistic"], result['pvalue'] = stats.mannwhitneyu(df1_vals, df2_vals)
        result['count_1'] = df1_vals.agg(['count'])['count']
        result['count_2'] = df2_vals.agg(['count'])['count']
    except ValueError:
        result["statistic"], result['pvalue'] = (-1, 0)
        result['count_1'] = df1_vals.agg(['count'])['count']
        result['count_2'] = df2_vals.agg(['count'])['count']
    return result


def mann_u_effect(df1, df2, asid, param, mannu_res):
    if asid == -1:
        n1 = len(df1[param])
        n2 = len(df2[param])
        return 1 - (2*mannu_res.statistic)/(n1*n2)
    else:
        n1 = len(df1.loc[df1['AssignmentID'] == asid][param])
        n2 = len(df2.loc[df2['AssignmentID'] == asid][param])
        return 1 - (2*mannu_res.statistic)/(n1*n2)


def agg_scores(df, asids, agg_param):
    df_agg = df.filter(['SubjectID', 'AssignmentID', agg_param])
    first = True
    for asid in asids:
        if first:
            asid_filter = df_agg['AssignmentID'] == asid
            first = False
        else:
            asid_filter = asid_filter | (df_agg['AssignmentID'] == asid)
    df_agg = df_agg[asid_filter]
    df_agg = df_agg.groupby('SubjectID')
    return df_agg.agg('mean')


def print_stats(mann_u_result, agg_c, agg_t, label):
    statistic = mann_u_result['statistic']
    pvalue = mann_u_result['pvalue']
    count1 = mann_u_result['count_1']
    count2 = mann_u_result['count_2']
    avg_c = agg_c['mean']
    std_c = agg_c['std']
    avg_t = agg_t['mean']
    std_t = agg_t['std']

    print("{label}: statistic={w:.4f}, pvalue={p:.4f}, "
          "avg is {avg_c:.4f}({c1},+-{std_c:.4f}) vs {avg_t:.4f}({c2},+-{std_t:.4f})".format(
           label=label, w=statistic, p=pvalue, avg_c=avg_c, std_c=std_c, avg_t=avg_t, std_t=std_t, c1=count1,
           c2=count2))


def filter_df(df, keys, values):
    """
    assembled new data frame of rows whose column (denoted by keys) value matches the corresponding value in values

    :param df: data frame
    :type df: data frame
    :param key: Columns to filter_df by
    :type key: ??
    :param value: value to be equal to
    :type value: ??
    :return: filtered data frame
    :rtype:
    """
    if type(keys) != list and type(values) != list:
        keys = [keys]
        values = [values]
    df_ret = df
    for key, value in zip(keys, values):
        df_ret = df_ret.loc[df[key] == value]
    return df_ret


def feedback_mann_u(feedback_array, df1, df2, asid):
    feedback_mann_dict = {}
    cols1 = df1.columns
    cols2 = df2.columns
    for feedback in feedback_array:
        if feedback in cols1 and feedback in cols2:
            try:
                feedback_mann_dict[feedback] = mann_u_assignment(df1, df2, asid, feedback)
            except ValueError:
                continue
    return pd.DataFrame.from_dict(feedback_mann_dict)


def test_func():
    print("11")


# TODO: Figure out why we need this...
try:
    setup(("import matplotlib.pyplot as plt\n"
           "plt.hist([12, 13, 15, 9, 8, 8, 4, 4])\n"
           "plt.show()\n"), [])
except:
    setup(("import matplotlib.pyplot as plt\n"
           "plt.hist([12, 13, 15, 9, 8, 8, 4, 4])\n"
           "plt.show()\n"), [])