import os, sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.sepcode import SeperateCode
from src.gene_data import make_gene
from IPython.display import clear_output
import pandas as pd

attribute_names = ["age", "income", "student", "credit_rate"]
class_name = "default"
data1 = {
    "age": [
        "youth",
        "youth",
        "middle_age",
        "senior",
        "senior",
        "senior",
        "middle_age",
        "youth",
        "youth",
        "senior",
        "youth",
        "middle_age",
        "middle_age",
        "senior",
    ],
    "income": [
        "high",
        "high",
        "high",
        "medium",
        "low",
        "low",
        "low",
        "medium",
        "low",
        "medium",
        "medium",
        "medium",
        "high",
        "medium",
    ],
    "student": ["no", "no", "no", "no", "yes", "yes", "yes", "no", "yes", "yes", "yes", "no", "yes", "no"],
    "credit_rate": [
        "fair",
        "excellent",
        "fair",
        "fair",
        "fair",
        "excellent",
        "excellent",
        "fair",
        "fair",
        "fair",
        "excellent",
        "excellent",
        "fair",
        "excellent",
    ],
    "default": ["no", "no", "yes", "yes", "yes", "no", "yes", "no", "yes", "yes", "yes", "yes", "yes", "no"],
}
df1 = pd.DataFrame(data1, columns=data1.keys())
if __name__ == "__main__":
    comb = make_gene()
    cols = ["cola", "colb", "colc", "cold"]
    target_col = "target"
    sc = SeperateCode()
    print("exp 1th")
    sc.initialize(comb, target_col)
    sc.fit(comb, cols, target_col, [])
    clear_output(wait=True)
    _ = sc.get_condition()
    sc.completed()

    print("exp 2th")
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
