import numpy as np
import pandas as pd
import sqlitedict

import openmdao.api as om

def convert(dimension, filename, design_name):
    '''SQLファイルから結果をcsvに書き出し'''

    case_reader = om.CaseReader(filename)

    # 計算回数を取得
    driver_cases = case_reader.list_cases('driver')

    # 結果を2次元配列化
    res = np.array([[0. for i in range(dimension)]] * len(driver_cases))
    for i in range(len(driver_cases)):
        case = case_reader.get_case(driver_cases[i])
        res[i,0] = case.get_objectives()['f_xy1']
        res[i,1] = case.get_objectives()['f_xy2']
        res[i,2] = case.get_objectives()['f_xy3']
        for j in range(len(design_name)):
            res[i,3+j] = case.get_design_vars()[design_name[j]]

        # 制約条件がある場合は以下を追加
        # res[] = case.get_constraints()[]

    list =['phi', 'weight', 'velocity']
    for i in range(len(design_name)):
        list.append(design_name[i])

    df = pd.DataFrame(res, columns=list)
    df.to_csv("result.csv", index=False)


if __name__ == '__main__':
    convert(5, 'doe_sampling.sql', ['a', 'b'])
