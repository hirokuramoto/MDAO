
import numpy as np
import os


class ReadResult(object):
    ''' postProcess/に作成された結果ファイルを読み込み,
        指定した目的関数値を返す
    '''
    def __init__(self, wd):
        self.wd    = wd   # 結果ファイル保存パス


    def read_value(self):
        '''結果ファイルをnumpy配列として読み込み'''
        self.array = np.loadtxt(self.wd, comments='#')

        return self.array[-1, 1] # 最終行の2列目の値


if __name__ == "__main__":
    path = os.getcwd() + '/postProcessing/flowRatePatch(name=Outlet2)/0/surfaceFieldValue.dat'

    data = ReadResult(path)
    print(data.read_value())
