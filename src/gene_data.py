from sklearn.model_selection import ParameterGrid
import pandas as pd 
def make_gene() :
    ASET = dict(
        cola = ["A"],
        colb = [1,2,3],
        colc = ["a","c"],
        cold = ["#","###"]
    )
    BSET = dict(
        cola = ["A"],
        colb = [2,3,4,5],
        colc = ["b","d"],
            cold = ["#","###"]

    )
    CSET = dict(
        cola = ["C"],
        colb = [1,4],
        colc = ["a","b"],
            cold = ["#","###"]

    )
    DSET = dict(
        cola = ["B"],
        colb = [1,2],
        colc = ["e","b"],
        cold = ["#","###"]

    )
    ESET = dict(
        cola = ["B"],
        colb = [3,4],
        colc = ["a","b"],
        cold = ["#","###"]

    )


    RESULT = []
    RESULT.extend(list(ParameterGrid(ASET)))
    RESULT.extend(list(ParameterGrid(BSET)))
    RESULT.extend(list(ParameterGrid(CSET)))
    RESULT.extend(list(ParameterGrid(DSET)))
    RESULT.extend(list(ParameterGrid(ESET)))
    # def find_unique_dict(RESULT) :
    #     RESULT = list(map(dict, set(tuple(sorted(d.items())) for d in RESULT)))
    #     return RESULT
    # assert len(find_unique_dict(RESULT)) == len(RESULT)
    comb = pd.DataFrame()
    df = pd.DataFrame(list(ParameterGrid(ASET)))
    df["target"] = "aa"
    comb = pd.concat([comb,df],axis=0)
    df = pd.DataFrame(list(ParameterGrid(BSET)))
    df["target"] = "bb"
    comb = pd.concat([comb,df],axis=0)
    df = pd.DataFrame(list(ParameterGrid(CSET)))
    df["target"] = "cc"
    comb = pd.concat([comb,df],axis=0)
    df = pd.DataFrame(list(ParameterGrid(DSET)))
    df["target"] = "dd"
    comb = pd.concat([comb,df],axis=0)
    df = pd.DataFrame(list(ParameterGrid(ESET)))
    df["target"] = "ee"
    comb = pd.concat([comb,df],axis=0)
    comb = comb.reset_index(drop=True)
    return comb