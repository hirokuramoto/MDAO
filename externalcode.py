# 問題をコンポーネントとして定義
import os
import csv
import subprocess

import pandas as pd
import openmdao.api as om

class ExternalCode(om.ExternalCodeComp):
    """read and write csv data for openMDAO """
    def setup(self):
        self.add_input('a',      val=0.0)
        #self.add_input('b',      val=0.0)
        self.add_output('f_xy1', shape=1)
        self.add_output('f_xy2', shape=1)
        self.add_output('f_xy3', shape=1)

        path = os.getcwd()
        self.input_filepath   = path + '/input_MDAO.csv'
        self.output_filepath1 = path + '/output_MDAO.csv'
        self.output_filepath2 = path + '/volume.csv'
        self.output_filepath3 = path + '/constraint.csv'
        self.options['external_input_files'] = [self.input_filepath]
        self.options['external_output_files'] = [self.output_filepath1]
        self.options['command'] = ['python3', 'extcode.py', self.input_filepath]

    def compute(self, inputs, outputs):
        a = inputs['a']
        #b = inputs['b']

        # Generate the input file for the paraboloid external code
        with open(self.input_filepath, 'w') as input_file:
            input_file.write('%f\n' % (a))
        super(ExternalCode, self).compute(inputs, outputs)

        # Parse the output file from the external code and set the value of f_xy
        with open(self.output_filepath1, 'r') as output_file1:
            f_xy1 = float(output_file1.read())
        outputs['f_xy1'] = f_xy1

        with open(self.output_filepath2, 'r') as output_file2:
            f_xy2 = float(output_file2.read())
        outputs['f_xy2'] = f_xy2

        with open(self.output_filepath3, 'r') as output_file3:
            f_xy3 = float(output_file3.read())
        outputs['f_xy3'] = f_xy3
