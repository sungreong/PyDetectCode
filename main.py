import os, sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.detectpattern import DetectionPattern
from src.gene_data import make_gene, make_gene_v2
from IPython.display import clear_output
import pandas as pd


if __name__ == "__main__":
    comb = make_gene()
    cols = ["cola", "colb", "colc", "cold"]
    target_col = "target"
    sc = DetectionPattern()
    print("exp 1th")
    sc.initialize(comb, target_col)
    sc.fit(comb, cols, target_col, [])
    clear_output(wait=True)
    _ = sc.get_condition()
    sc.completed()

    print("exp 2th")
    df1 = make_gene_v2()
    attribute_names = ["age", "income", "student", "credit_rate"]
    class_name = "default"
    sc.initialize(df1, class_name)
    sc.fit(df1, attribute_names, class_name, [])
    clear_output(wait=True)
    _ = sc.get_condition()
    sc.completed()
    print("exp 3th")
    attribute_names = ["default", "student", "credit_rate"]
    class_name = "age"
    sc.initialize(df1, class_name)
    sc.fit(df1, attribute_names, class_name, [])
    print(sc.get_condition())
    sc.completed()
