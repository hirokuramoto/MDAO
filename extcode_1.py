#FreeCADのスプレッドシートへ代入するパラメータ値の設定
import sys
import subprocess
import csv
from pathlib import Path

import pandas as pd

from param_b import FreecadParams

def cad(input_filename):
    '''FreeCADにパラメータの値を渡してSTEP形式で保存と体積の計算'''

    #input_MDAO.csvからパラメータ読み込み
    with open(input_filename, 'r') as input_file:
        file_contents = input_file.readlines()
    a = [float(f) for f in file_contents]

    dir = Path(__file__).parent # extcode_1.pyのあるディレクトリ
    dir /= '../' # 1階層上のディレクトリへ移動
    path = str(dir.resolve()) # 絶対パスの取得

    # FreeCADの形状データの保存場所の指定
    fcpath = path + '/cad/original_model.FCStd'
    # STEP形式でのファイル保存場所の指定
    stpath = path + '/cad/original_model.step'
    f_params = FreecadParams(fcpath,stpath)
    f_params.import_fcstd()
    f_params.set_value('a', str(a))
    #f_params.set_value('b', str(b))

    # STEP形式で保存
    f_params.export_step()

    # 体積の計算と保存
    v = f_params.volume_cal() #体積
    df = pd.DataFrame([v])
    df.to_csv(path + '/optimize/volume.csv', header=False, index=False)

#このpythonファイルを直接呼び出すので、以下は必要
if __name__ == "__main__":
    input_filename = sys.argv[1]

    cad(input_filename)
