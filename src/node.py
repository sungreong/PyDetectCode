import pandas as pd
from collections import Counter
from copy import deepcopy

table = pd.DataFrame


def get_error_table(count_table: table, target):
    return count_table.groupby([target]).apply(lambda x: 0 if x.shape[0] == 1 else min(x["Size"]) / sum(x["Size"]))


def get_error_rate(count_table: table, target):

    metric = get_error_table(count_table, target).mean()
    return metric


def make_count_table(df: table, target, by):
    count_table = df.groupby([by, target]).size().reset_index(name="Size")
    return count_table


def get_metric(df: table, target, col):
    count_table = make_count_table(df, target, col)
    metric = get_error_rate(count_table, target=col)
    return metric


def get_min_col(metric_result: dict):
    return min(metric_result.items(), key=lambda x: x[1])[0]


def get_target_prob(data):
    total_n = len(data)
    target_bin_count = dict(Counter(data))
    target_prob = deepcopy(target_bin_count)
    for k, v in target_bin_count.items():
        target_prob[k] = v / total_n
    else:
        return target_prob


def get_gini(prob_dict):
    return sum([v**2 for k, v in prob_dict.items()])


def get_gini_impurity(prob_dict):
    gini = get_gini(prob_dict)
    return 1 - gini


def make_gini_impurity(data):
    prob_dict = get_target_prob(data)
    return get_gini_impurity(prob_dict)


def make_weighted_gini_impurity(data):
    return pd.Series(dict(gini=make_gini_impurity(data), n=len(data)))


def get_weighted_gini_impurity(df: pd.DataFrame, col, target_col):
    summary_df = df.groupby([col]).apply(lambda x: make_weighted_gini_impurity(x[target_col]))
    return (summary_df["gini"] * (summary_df["n"] / sum(summary_df["n"]))).sum()


def make_gini_attributes(df: pd.DataFrame, cols: list, target_col):
    gini_attributes = dict()
    for col in cols:
        gini_attributes[col] = get_weighted_gini_impurity(df=df, col=col, target_col=target_col)
    else:
        return gini_attributes


def get_min_giniattributes(metric_result):
    return min(metric_result.items(), key=lambda x: x[1])
