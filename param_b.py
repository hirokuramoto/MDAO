import sys

FREECADPATH = "/usr/lib/freecad-python3/lib"
sys.path.append(FREECADPATH)
import FreeCAD
import Import

class FreecadParams:
    """FreeCADで寸法値の変更とSTEP形式で保存"""
    def __init__(self, fc, st):
        self.fcpath = fc
        self.stpath = st

    def import_fcstd(self):
        FreeCAD.open(self.fcpath)

    def set_value(self, params, value):
        FreeCAD.setActiveDocument("original_model")
        FreeCAD.ActiveDocument.Spreadsheet.set(params, value)
        FreeCAD.ActiveDocument.recompute()
        __objs__=[]
        __objs__.append(FreeCAD.getDocument("original_model").getObject("Pad"))
        del __objs__

    def export_step(self):
        __objs__=[]
        __objs__.append(FreeCAD.getDocument("original_model").getObject("Pad"))
        Import.export(__objs__, self.stpath)
        del __objs__

    def volume_cal(self):
        FreeCAD.setActiveDocument("original_model")
        volume = FreeCAD.ActiveDocument.getObject("Pad").Shape.Volume
        return volume

#if __name__ == '__main__':
#    import os
#    path = os.getcwd()
#    fcpath = path + '/cad/original_model.fcstd'
#    stpath = path + '/cad/original_model.step'

#    f = FreecadParams(fcpath,stpath)
#    f.import_fcstd()
#    f.set_value('a', '89')
#    f.set_value('b', '9')
#    f.export_step()
