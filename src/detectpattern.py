from IPython.display import clear_output
import os, sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)
import pandas as pd
from src.metric import make_gini_attributes, get_min_giniattributes


class DetectionPattern(object):
    def __init__(self):
        self._name = "sepcode"

    def make_where_query(self, condition_list: dict):
        total_q = []
        for k, v in condition_list.items():
            if len(v) == 1:
                q = f"{k} == '{v[0]}'"
            else:
                _comb = list(v)
                q = f"{k} in {_comb}"
            total_q.append(q)
        else:
            total_q = " and ".join([f"({i})" for i in total_q])
        return total_q

    def print_pretty(self, d: dict, indent=0):
        for key, value in d.items():
            print("\t" * indent + str(key))
            if isinstance(value, dict):
                self.print_pretty(value, indent + 1)
            else:
                print("\t" * (indent + 1) + str(value))

    def initialize(self, comb: pd.DataFrame, target_col):
        self._comb = comb
        self._target_real_idx_dict_list = comb.groupby([target_col]).apply(lambda x: x.index.tolist()).to_dict()
        self.collection = []
        del self.collection[:]
        self._target_idx_list = {k: [] for k, v in self._target_real_idx_dict_list.items()}
        self._target_list = comb[target_col].unique().tolist()
        self._is_finished = False

    def check_target_index_equal(self):
        check_target = dict()
        for col in list(self._target_idx_list.keys()):
            check_target[col] = len(self._target_idx_list[col]) == len(self._target_real_idx_dict_list[col])
        else:
            print("check target index")
            self.print_pretty(check_target)
        if any([True for i in list(check_target.values()) if i == False]):
            self._is_finished = False
            raise Exception("해당 컬럼으로 분리할 수 없음")
        else:
            self._is_finished = True

    def completed(self):
        if self._is_finished:
            print("Success")
        else:
            print("Failed")

    def get_condition(self, verbose=True):
        self.check_target_index_equal()

        target_q = {i: [] for i in self._target_list}
        target_q_unique_list = {i: [] for i in self._target_list}
        target_q_unique_list_cond = {i: [] for i in self._target_list}
        for d in self.collection:
            for k, v in d.items():
                target_q[k].append(v)
        for target, v in target_q.items():
            result = []
            for i in v:
                q = self.make_where_query(i)
                target_idx = self._comb.query(q).index.tolist()
                if any([True for i in target_idx if i in target_q_unique_list[target]]):
                    continue
                else:
                    target_q_unique_list_cond[target].append(i)
                    target_q_unique_list[target].extend(target_idx)
        use_col_list = self._find_use_col(target_q_unique_list_cond)
        result = dict(use_col_list=use_col_list, condition=target_q_unique_list_cond)
        if verbose:
            self.print_pretty(result)
        return result

    def _find_use_col(self, target_condition):
        use_col = []
        for k, conds in target_condition.items():
            for cond in conds:
                use_col.extend(list(cond.keys()))
        else:
            use_col = list(set(use_col))
        return use_col

    def fit(self, comb, cols, target_col, previous_condition=[]):
        if len(cols) == 0:
            return print("Failed")
        result = make_gini_attributes(comb, cols=cols, target_col=target_col)

        select_col = get_min_giniattributes(result)[0]
        find_pure_result = dict(filter(lambda x: x[1] == 0.0, result.items()))
        if len(find_pure_result) == 0:
            select_candidate = list(comb[select_col].unique())
            qs = [f"{select_col} == '{i}'" for i in select_candidate]
            qs_dict = [{select_col: [i]} for i in select_candidate]

            _cols = cols
            for idx, q in enumerate(qs):
                _comb = comb.query(q)
                _cols = list(set(_cols).difference(set([select_col])))
                previous_condition.append(qs_dict[idx])
                self.fit(comb=_comb, cols=_cols, target_col=target_col, previous_condition=previous_condition)
        else:
            for select_col, _ in find_pure_result.items():
                r = comb.groupby([target_col]).apply(lambda x: {select_col: list(x[select_col].unique())})

                r = r.to_dict()
                for k, v in r.items():
                    for cond in previous_condition:
                        v.update(cond)
                self.collection.append(r)
                for k, i in r.items():
                    q = self.make_where_query(i)
                    _result = comb.query(q)
                    result: pd.DataFrame = _result.groupby([target_col]).apply(lambda x: x.index.tolist())
                    if result.empty:
                        print("emtpy")
                        continue
                    for k, v in result.to_dict().items():
                        self._target_idx_list[k] = sorted(list(set(v) | set(self._target_idx_list[k])))
            else:
                print("Progress...")
                for k in self._target_list:
                    current = len(self._target_idx_list[k])
                    total = len(self._target_real_idx_dict_list[k])
                    ratio = (current / total) * 100
                    print(f"{k:10s} : {ratio:06.2f}%")
                del previous_condition[-1]
