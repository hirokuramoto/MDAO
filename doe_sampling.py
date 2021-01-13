import openmdao.api as om

from externalcode import ExternalCode
import sql2csv

class LHS(object):
    def __init__(self, num, filename, design_name, design_init, lower, upper):
        '''LHSに基づく解析の実行'''
        self.num         = num          # sample数
        self.filename    = filename     # sqlファイル名(str)
        self.design_name = design_name  # 設計変数名(list)
        self.design_init = design_init  # 設計変数の初期値(list)
        self.lower       = lower        # 設計変数の下限値(list)
        self.upper       = upper        # 設計変数の上限値(list)

    def compute(self):
        prob = om.Problem()
        model = prob.model

        n = len(self.design_name)

        # モデルの構築
        list=['f_xy1', 'f_xy2', 'f_xy3']
        for i in range(n):
            model.add_subsystem('p{k}'.format(k=i), om.IndepVarComp(self.design_name[i], self.design_init[i]), promotes=[self.design_name[i]])
            list.append(self.design_name[i])

        model.add_subsystem('p', ExternalCode(), promotes=list)

        for i in range(n):
            model.add_design_var(self.design_name[i], lower=self.lower[i], upper=self.upper[i])

        model.add_objective('f_xy1') # 出口流量
        model.add_objective('f_xy2') # 配管重量
        model.add_objective('f_xy3') # 最大流速

        # ドライバーの設定
        driver = prob.driver = om.DOEDriver(om.LatinHypercubeGenerator(self.num))

        # レコーダの設定
        driver.recording_options['includes'] = ['*']
        driver.recording_options['record_objectives'] = True
        driver.recording_options['record_inputs'] = True
        driver.recording_options['record_outputs'] = True
        driver.recording_options['record_residuals'] = False

        recorder = om.SqliteRecorder(self.filename)
        driver.add_recorder(recorder)

        # 問題の構築とドライバー実行
        prob.setup()
        prob.run_driver()
        prob.cleanup()

        # 結果の書き出し
        column = n + 3
        sql2csv.convert(column, self.filename, self.design_name)
