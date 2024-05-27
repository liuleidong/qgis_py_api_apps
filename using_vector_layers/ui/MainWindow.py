# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/qgis.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mapcanvasWidget = QtWidgets.QWidget(self.centralwidget)
        self.mapcanvasWidget.setObjectName("mapcanvasWidget")
        self.verticalLayout.addWidget(self.mapcanvasWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuAdd_Vector_Layer = QtWidgets.QMenu(self.menubar)
        self.menuAdd_Vector_Layer.setObjectName("menuAdd_Vector_Layer")
        self.menuAdd_Raster_Layer = QtWidgets.QMenu(self.menubar)
        self.menuAdd_Raster_Layer.setObjectName("menuAdd_Raster_Layer")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.layerTreeDockWidget = QtWidgets.QWidget()
        self.layerTreeDockWidget.setObjectName("layerTreeDockWidget")
        self.dockWidget.setWidget(self.layerTreeDockWidget)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionGPX_data_provider_gpx = QtWidgets.QAction(MainWindow)
        self.actionGPX_data_provider_gpx.setObjectName("actionGPX_data_provider_gpx")
        self.actionDelimited_text_file_provider_delimitedtext = QtWidgets.QAction(MainWindow)
        self.actionDelimited_text_file_provider_delimitedtext.setObjectName("actionDelimited_text_file_provider_delimitedtext")
        self.actionSpatiaLite_data_provider_spatialite = QtWidgets.QAction(MainWindow)
        self.actionSpatiaLite_data_provider_spatialite.setObjectName("actionSpatiaLite_data_provider_spatialite")
        self.actionMemory_data_provider_memory = QtWidgets.QAction(MainWindow)
        self.actionMemory_data_provider_memory.setObjectName("actionMemory_data_provider_memory")
        self.actionWFS_web_feature_service_data_provider_wfs = QtWidgets.QAction(MainWindow)
        self.actionWFS_web_feature_service_data_provider_wfs.setObjectName("actionWFS_web_feature_service_data_provider_wfs")
        self.actionOGR_data_provider_ogr = QtWidgets.QAction(MainWindow)
        self.actionOGR_data_provider_ogr.setObjectName("actionOGR_data_provider_ogr")
        self.actionOGR_data_provider_ogr_Directory = QtWidgets.QAction(MainWindow)
        self.actionOGR_data_provider_ogr_Directory.setObjectName("actionOGR_data_provider_ogr_Directory")
        self.actionGDAL_data_provider_gdal = QtWidgets.QAction(MainWindow)
        self.actionGDAL_data_provider_gdal.setObjectName("actionGDAL_data_provider_gdal")
        self.actionWMS_data_provider_wms = QtWidgets.QAction(MainWindow)
        self.actionWMS_data_provider_wms.setObjectName("actionWMS_data_provider_wms")
        self.actionGeoPackage = QtWidgets.QAction(MainWindow)
        self.actionGeoPackage.setObjectName("actionGeoPackage")
        self.menuProject.addAction(self.actionNew)
        self.menuProject.addAction(self.actionOpen)
        self.menuProject.addAction(self.actionSave)
        self.menuProject.addAction(self.actionClose)
        self.menuAdd_Vector_Layer.addAction(self.actionOGR_data_provider_ogr)
        self.menuAdd_Vector_Layer.addAction(self.actionOGR_data_provider_ogr_Directory)
        self.menuAdd_Vector_Layer.addAction(self.actionGPX_data_provider_gpx)
        self.menuAdd_Vector_Layer.addAction(self.actionDelimited_text_file_provider_delimitedtext)
        self.menuAdd_Vector_Layer.addAction(self.actionSpatiaLite_data_provider_spatialite)
        self.menuAdd_Vector_Layer.addAction(self.actionMemory_data_provider_memory)
        self.menuAdd_Vector_Layer.addAction(self.actionWFS_web_feature_service_data_provider_wfs)
        self.menuAdd_Raster_Layer.addAction(self.actionGDAL_data_provider_gdal)
        self.menuAdd_Raster_Layer.addAction(self.actionWMS_data_provider_wms)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuAdd_Vector_Layer.menuAction())
        self.menubar.addAction(self.menuAdd_Raster_Layer.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuProject.setTitle(_translate("MainWindow", "Project"))
        self.menuAdd_Vector_Layer.setTitle(_translate("MainWindow", "Add Vector Layer"))
        self.menuAdd_Raster_Layer.setTitle(_translate("MainWindow", "Add Raster Layer"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionClose.setText(_translate("MainWindow", "Quit"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionGPX_data_provider_gpx.setText(_translate("MainWindow", "GPX data provider(gpx)"))
        self.actionDelimited_text_file_provider_delimitedtext.setText(_translate("MainWindow", "Delimited text file provider(delimitedtext)"))
        self.actionSpatiaLite_data_provider_spatialite.setText(_translate("MainWindow", "SpatiaLite data provider(spatialite)"))
        self.actionMemory_data_provider_memory.setText(_translate("MainWindow", "Memory data provider(memory)"))
        self.actionWFS_web_feature_service_data_provider_wfs.setText(_translate("MainWindow", "WFS(web feature service) data provider(wfs)"))
        self.actionOGR_data_provider_ogr.setText(_translate("MainWindow", "OGR data provider(ogr) | File"))
        self.actionOGR_data_provider_ogr_Directory.setText(_translate("MainWindow", "OGR data provider(ogr) | Directory"))
        self.actionGDAL_data_provider_gdal.setText(_translate("MainWindow", "GDAL data provider(gdal)"))
        self.actionWMS_data_provider_wms.setText(_translate("MainWindow", "WMS data provider(wms)"))
        self.actionGeoPackage.setText(_translate("MainWindow", "OGR data provider(ogr) | GeoPackage"))
import res_rc
