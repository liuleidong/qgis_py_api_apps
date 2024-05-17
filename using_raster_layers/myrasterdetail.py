from PyQt5.QtWidgets import QDialog

from qgis.core import QgsRasterLayer

from ui.RasterInfo import Ui_RasterInfoDialog


class MyRasterDetail(QDialog,Ui_RasterInfoDialog):
    def __init__(self,rlayer):
        super(QDialog, self).__init__()
        self.setupUi(self)
        self.rlayer = rlayer
        self.label_extent.setText(rlayer.extent().toString())
        self.label_width.setText(str(rlayer.width()))
        self.label_height.setText(str(rlayer.height()))
        self.label_rasterType.setText(str(rlayer.rasterType()))
        self.label_bandCount.setText(str(rlayer.bandCount()))
        self.label_crs.setText(rlayer.crs().authid())