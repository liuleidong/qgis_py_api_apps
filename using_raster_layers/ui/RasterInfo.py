# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RasterInfo.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RasterInfoDialog(object):
    def setupUi(self, RasterInfoDialog):
        RasterInfoDialog.setObjectName("RasterInfoDialog")
        RasterInfoDialog.resize(419, 421)
        self.gridLayout = QtWidgets.QGridLayout(RasterInfoDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(RasterInfoDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_extent = QtWidgets.QLabel(RasterInfoDialog)
        self.label_extent.setText("")
        self.label_extent.setObjectName("label_extent")
        self.gridLayout.addWidget(self.label_extent, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(RasterInfoDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_width = QtWidgets.QLabel(RasterInfoDialog)
        self.label_width.setText("")
        self.label_width.setObjectName("label_width")
        self.gridLayout.addWidget(self.label_width, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(RasterInfoDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_height = QtWidgets.QLabel(RasterInfoDialog)
        self.label_height.setText("")
        self.label_height.setObjectName("label_height")
        self.gridLayout.addWidget(self.label_height, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(RasterInfoDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_rasterType = QtWidgets.QLabel(RasterInfoDialog)
        self.label_rasterType.setText("")
        self.label_rasterType.setObjectName("label_rasterType")
        self.gridLayout.addWidget(self.label_rasterType, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(RasterInfoDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_bandCount = QtWidgets.QLabel(RasterInfoDialog)
        self.label_bandCount.setText("")
        self.label_bandCount.setObjectName("label_bandCount")
        self.gridLayout.addWidget(self.label_bandCount, 4, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(RasterInfoDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_crs = QtWidgets.QLabel(RasterInfoDialog)
        self.label_crs.setText("")
        self.label_crs.setObjectName("label_crs")
        self.gridLayout.addWidget(self.label_crs, 5, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(RasterInfoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)
        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(RasterInfoDialog)
        self.buttonBox.accepted.connect(RasterInfoDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(RasterInfoDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(RasterInfoDialog)

    def retranslateUi(self, RasterInfoDialog):
        _translate = QtCore.QCoreApplication.translate
        RasterInfoDialog.setWindowTitle(_translate("RasterInfoDialog", "Dialog"))
        self.label_2.setText(_translate("RasterInfoDialog", "Extent:"))
        self.label.setText(_translate("RasterInfoDialog", "Width:"))
        self.label_3.setText(_translate("RasterInfoDialog", "Height:"))
        self.label_4.setText(_translate("RasterInfoDialog", "RasterType:"))
        self.label_5.setText(_translate("RasterInfoDialog", "bandCount:"))
        self.label_6.setText(_translate("RasterInfoDialog", "crs:"))
