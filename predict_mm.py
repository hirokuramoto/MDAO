import pickle
import itertools

import numpy as np

import openmdao.api as om

class Predict(om.ExplicitComponent):
    """read and write csv data for openMDAO """
    def setup(self):
        # input
        self.add_input('a',      val=1.0)
        self.add_input('b',      val=1.0)
        #output
        self.add_output('f_xy1', val=0.0)
        self.add_output('f_xy2', val=0.0)
        self.add_output('f_xy3', val=0.0)

    def compute(self, inputs, outputs):
        a = inputs['a']
        b = inputs['b']

        arr = np.ravel(np.array([a, b])) # 1次元配列にして渡す

        f = open("./kriging_model_1", "rb")
        r = pickle.load(f)
        f.close()
        outputs['f_xy1'] = np.ravel(r.predict(arr)) # 2次元→１次元配列に変換

        f = open("./kriging_model_2", "rb")
        r = pickle.load(f)
        f.close()
        outputs['f_xy2'] = np.ravel(r.predict(arr))

        f = open("./kriging_model_3", "rb")
        r = pickle.load(f)
        f.close()
        outputs['f_xy3'] = np.ravel(r.predict(arr))
