import pickle

import numpy as np
import pandas as pd
import sqlitedict
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import openmdao.api as om

from predict_mm import Predict

class KrigingSurrogate(object):
    '''GPRに基づくKrigingモデルの作成'''
    def __init__(self, num, filename, design_name, design_init, lower, upper):
        self.num         = num          # サンプル数
        self.filename    = filename     # sqlファイル名(str)
        self.design_name = design_name  # 設計変数名(list)
        self.design_init = design_init  # 設計変数の初期値(list)
        self.lower       = lower        # 設計変数の下限値(list)
        self.upper       = upper        # 設計変数の上限値(list)

    def modeling(self):
        '''FEM結果を使ったKrigingモデルの訓練'''
        # ドライバーに接続されたレコーダの読み込み
        cr = om.CaseReader(self.filename)

        # 計算回数を取得
        driver_cases = cr.list_cases('driver')

        # FEM結果を2次元配列化
        res = np.array([[0. for i in range(self.num)]] * len(driver_cases))
        for i in range(len(driver_cases)):
            case = cr.get_case(driver_cases[i])
            res[i,0] = case.get_objectives()['f_xy1']
            res[i,1] = case.get_objectives()['f_xy2']
            res[i,2] = case.get_objectives()['f_xy3']
            for j in range(len(self.design_name)):
                res[i,3+j] = case.get_design_vars()[self.design_name[j]]

        # 解析に失敗したデータを削除
        if 0.0 in res[:, 0]:
            row = np.where(res[:, 0]==0.0)
            res = np.delete(res, row, axis=0)


        prob = om.Problem()
        model = prob.model

        # モデルの構築
        for i in range(len(self.design_name)):
            model.add_subsystem('p{k}'.format(k=i), om.IndepVarComp(self.design_name[i], self.design_init[i]), promotes=[self.design_name[i]])

        MetaModel = om.MetaModelUnStructuredComp()
        for i in range(len(self.design_name)):
            MetaModel.add_input(self.design_name[i], self.design_init[i])
        MetaModel.add_output('f_xy1', 0., surrogate=om.KrigingSurrogate())
        MetaModel.add_output('f_xy2', 0., surrogate=om.KrigingSurrogate())
        MetaModel.add_output('f_xy3', 0., surrogate=om.KrigingSurrogate())
        prob.model.add_subsystem('MM', MetaModel)
        prob.model.connect('a', 'MM.a')
        prob.model.connect('b', 'MM.b')

        # 問題の構築
        prob.setup()
        MetaModel.options['train:f_xy1'] = res[:,0]
        MetaModel.options['train:f_xy2'] = res[:,1]
        MetaModel.options['train:f_xy3'] = res[:,2]
        for i,j in enumerate(self.design_name): # for (インデックス, 要素) in enumerate(リスト):
            MetaModel.options['train:{k}'.format(k=j)] = res[:,3+i]

        prob.run_model()
        prob.cleanup()

        # プライベートクラス関数(_metadata)にアクセスして、Metamodelに設置されているsurrogateモデルを読み込む
        sg_1 = MetaModel._metadata('f_xy1').get('surrogate')
        sg_2 = MetaModel._metadata('f_xy2').get('surrogate')
        sg_3 = MetaModel._metadata('f_xy3').get('surrogate')

        # 近似モデルの保存
        f = open("./kriging_model_1", "wb")
        pickle.dump(sg_1, f)
        f.close()

        f = open("./kriging_model_2", "wb")
        pickle.dump(sg_2, f)
        f.close()

        f = open("./kriging_model_3", "wb")
        pickle.dump(sg_3, f)
        f.close()


    def nsga2(self):
        '''鍛えたサロゲートモデルを使ってパレート解を求める'''

        prob = om.Problem()
        model = prob.model

        n = len(self.design_name)

        # モデルの構築
        list=['f_xy1', 'f_xy2', 'f_xy3']
        for i in range(n):
            model.add_subsystem('p{k}'.format(k=i), om.IndepVarComp(self.design_name[i], self.design_init[i]), promotes=[self.design_name[i]])
            list.append(self.design_name[i])
        model.add_subsystem('p' , Predict(), promotes=list)

        for i in range(n):
            model.add_design_var(self.design_name[i], lower=self.lower[i], upper=self.upper[i])
        model.add_objective('f_xy1') # コンプライアンス
        model.add_objective('f_xy2') # 重量
        model.add_constraint('f_xy3', upper=300*10**6) # NSGA2のときに有効にする

        driver = prob.driver = om.pyOptSparseDriver()#optimizer='NSGA2')
        driver.options['optimizer'] = 'NSGA2'
        driver.opt_settings['PopSize'] = 100
        driver.opt_settings['maxGen'] = 200

        prob.set_solver_print(level=0)
        prob.setup(check=True)
        prob.run_driver()
        prob.cleanup()


if __name__ == '__main__':
    file = 'doe_sampling.sql'
    design = ['a', 'b']
    init = [45.0,  6.5]
    lower       = [45.0,  6.0]
    upper       = [85.0, 10.0]
    test = KrigingSurrogate(5, file, design, init, lower, upper)
    test.modeling()
    test.nsga2()
