# OpenFOAMで計算実行
import subprocess
import os
from pathlib import Path

class RunFoam(object):
    '''OpenFOAMの実行と結果のcsv保存'''
    def __init__(self, workdir, solver):
        '''args
            workdir : ワークディレクトリのパス(str)
            solver  : 選択したソルバー(str)
        '''
        self.workdir = workdir
        self.solver  = solver

    def runfoam(self):
        cmd0 = "salome -t" # Salome-Mecaをターミナルモードで起動
        cmd1 = "salome shell step2unv.py" # meshを作成(Salome-Mecaのマクロ機能を利用)
        cmd2 = "salome killall" # Salome-Mecaを閉じる
        cmd3 = "ideasUnvToFoam Mesh_1.unv"
        cmd4 = self.solver

        subprocess.run(cmd0.split())
        subprocess.run(cmd1.split())
        subprocess.run(cmd2.split())
        subprocess.run(cmd3.split(), cwd=self.workdir)
        self._change_wall() # boundaryファイルの境界タイプを書き換え
        subprocess.run(cmd4.split(), cwd=self.workdir)


    def _change_wall(self):
        '''ideasUnvToFoamで作成したメッシュの壁面条件のタイプを
           patch から wall に変更
        '''

        path = self.workdir + '/constant/polyMesh/boundary'

        with open(path, mode='r+') as f:
            line_list = f.readlines()

            for index,line in enumerate(line_list): # インデックス番号(行数), 要素の順に取得
                if line[0:8] == "    Wall":
                    del line_list[index+2]
                    line_list.insert(index+2, "        type            wall;\n")

        with open(path, mode='w') as f:
            f.writelines(line_list)

if __name__ == "__main__":

    dir = Path(__file__).parent # extcode_1.pyのあるディレクトリ
    dir /= '../' # 1階層上のディレクトリへ移動
    path = str(dir.resolve()) # 絶対パスの取得

    solver = "simpleFoam"
    r = RunFoam(path, solver)
    r.runfoam()
