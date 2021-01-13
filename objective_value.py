from pathlib import Path
import numpy as np
import os

class ObjectiveValue(object):
    def __init__(self):
        hoge = Path(__file__).parent # extcode_1.pyのあるディレクトリ
        hoge /= '../'
        path = str(hoge.resolve()) + '/postProcessing'
        self.path = path

    def forceCoeffs(self):
        '''揚力・効力係数の抽出
        args
            time(float) : 時刻
        returns
            Cl(float) : 揚力係数(結果ファイルの1列目)
            Cd(float) : 抗力係数(結果ファイルの2列目)
        '''
        # 結果ファイルの場所
        # 1回目は surfaceFieldValue, 2回目以降は surfaceFieldValue_0 が作成される
        path_dir = self.path + '/forceCoeffs1/0'

        if os.path.exists(path_dir + '/coefficient_0.dat'):
            path = path_dir + '/coefficient_0.dat'
        else:
            path = path_dir + '/coefficient.dat'

        # 結果ファイルの2次元配列化
        table = []
        with open(path, mode='r') as f:
            for line in f:
                if line[0] == '#': # コメント行読み飛ばし
                    continue
                temp = line.rstrip('\n').replace(" ", "").split('\t')
                row = [float(s) for s in temp]
                table.append(row)

        table = np.array(table)

        # 定常解析の場合は最終行を出力
        return table[0, 1]# =Cd(2列目は抗力係数)




    def flowRatePatch(self, face, time):
        '''流量データの抽出
        args
            face(str) : 対象とする面の名前
            time(float) : 時刻
        returns
            flowrate(float) : 流量[m3/s]
        '''
        # 結果ファイルの場所
        # 1回目は surfaceFieldValue, 2回目以降は surfaceFieldValue_0 が作成される
        path_dir = self.path + '/flowRatePatch(name=' + face + ')/0'

        if os.path.exists(path_dir + '/surfaceFieldValue_0.dat'):
            path = path_dir + '/surfaceFieldValue_0.dat'
        else:
            path = path_dir + '/surfaceFieldValue.dat'


        # 結果ファイルの2次元配列化
        table = []
        with open(path, mode='r') as f:
            for line in f:
                if line[0] == '#': # コメント行読み飛ばし
                    continue
                temp = line.rstrip('\n').replace(" ", "").split('\t')
                row = [float(s) for s in temp]
                table.append(row)

        table = np.array(table)

        # 指定した時刻があれば、その時刻のデータを返す
        if time in table[:, 0]:
            r = np.where(table[:, 0]==time)
            return table[r, 1]
        # 指定した時刻がないとき（解析失敗のとき）は0を返す
        else:
            return [0]




if __name__ == "__main__":

    test = ObjectiveValue()
    hoge = test.forceCoeffs()
    np.savetxt('test.csv', hoge)
