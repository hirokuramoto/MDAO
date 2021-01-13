import os
import time

from doe_sampling import LHS
from kriging_surrogate import KrigingSurrogate

def main():
    '''メインファイル'''

    # パラメータの設定
    file  = 'doe_sampling.sql'  # 結果ファイル名
    name  = ['a']          # 設計変数名
    init  = [10.0]       # 設計変数の初期値
    lower = [ 0.0]        # 設計変数の下限値
    upper = [75.0]       # 設計変数の上限値
    num   = 200                 # 初期サンプル数

    # LHSによるサンプリングとOpenFOAM実行
    sampling = LHS(num ,file, name, init, lower, upper)
    sampling.compute()

    # FEM結果を用いてKrigingモデルの構築とパレート解集合の獲得
    surrogate = KrigingSurrogate(num ,file, name, init, lower, upper)
    surrogate.modeling()
    surrogate.nsga2()

t1 = time.time()

main()

t2 = time.time()
elapsed_time = t2 - t1
print(("elapsed_time:{0}".format(elapsed_time)+"{sec}"))
