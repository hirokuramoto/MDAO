#FreeCADのスプレッドシートへ代入するパラメータ値の設定
import os
import sys
import csv
import numpy as np
from pathlib import Path

from runfoam import RunFoam
from objective_value import ObjectiveValue


def simulate_foam():
    '''OpenFOAMの操作'''
    dir = Path(__file__).parent # extcode_2.pyのあるディレクトリ
    dir /= '../' # 1階層上のディレクトリへ移動
    path = str(dir.resolve()) # 絶対パスの取得

    solver = "simpleFoam"
    r = RunFoam(path, solver)
    r.runfoam()

    #　計算結果のpath
    output_data1 = path + '/optimize/output_MDAO.csv'
    output_data3 = path + '/optimize/constraint.csv'

    # 1個目の目的関数読み取り&書き出し
    #time = 20
    result = ObjectiveValue()
    #data1 = result.flowRatePatch(face, time)
    data1 = result.forceCoeffs()
    np.savetxt(output_data1, data1, fmt="%.4f")

#このpythonファイルを直接呼び出すので、以下は必要
if __name__ == "__main__":
    simulate_foam()
