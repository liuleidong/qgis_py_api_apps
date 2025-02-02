from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QAction
from PyQt5.QtCore import QVariant

from qgis.PyQt.QtWidgets import QMainWindow,QMenu, QFileDialog
from qgis.core import (
    QgsProject,QgsLayerTreeModel,QgsVectorLayer,QgsApplication,QgsDataSourceUri,QgsRasterLayer,QgsDataProvider,
    QgsField,QgsFeature,QgsGeometry,QgsPointXY)
from qgis.gui import (
    QgsLayerTreeView,QgsMapCanvas,QgsLayerTreeMapCanvasBridge,
    QgsMapToolPan,QgsMapToolZoom,QgsMapToolIdentifyFeature,QgsMapMouseEvent,
    QgsGui,QgsEditorWidgetRegistry,QgsAttributeDialog,QgsAttributeForm,QgsExpressionSelectionDialog,
    QgsNewMemoryLayerDialog)

from mymenuprovider import MyMenuProvider
from ui.MainWindow import Ui_MainWindow
from rectanglemaptool import RectangleMapTool

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # 初始化图层树
        vl = QVBoxLayout(self.layerTreeDockWidget)
        self.gsLayerTreeView = QgsLayerTreeView(self)
        vl.addWidget(self.gsLayerTreeView)
        # 初始化mapCanvas
        self.gsMapCanvas = QgsMapCanvas(self)
        self.gsMapCanvas.contextMenuAboutToShow.connect(self.populateContextMenu)
        # TODO 设置destcrs 和 extent
        hl = QHBoxLayout(self.mapcanvasWidget)
        hl.setContentsMargins(0,0,0,0)
        hl.addWidget(self.gsMapCanvas)
        # 图层树model
        self.gsLayerTreeModel = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot())
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.ShowLegendAsTree)
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.UseEmbeddedWidgets)
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.UseTextFormatting)
        self.gsLayerTreeModel.setAutoCollapseLegendNodes(10)
        self.gsLayerTreeView.setModel(self.gsLayerTreeModel)
        # synchronise the loaded project with the canvas
        self.gsLayerTreeBridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), self.gsMapCanvas)
        # 添加maptool
        self.gsMapToolPan = QgsMapToolPan(self.gsMapCanvas)
        self.gsMapToolZoomIn = QgsMapToolZoom(self.gsMapCanvas,False)
        self.gsMapToolZoomOut = QgsMapToolZoom(self.gsMapCanvas,True)
        self.gsMapToolIdentifyFeature = QgsMapToolIdentifyFeature(self.gsMapCanvas)
        self.gsMapToolIdentifyFeature.featureIdentified.connect(self.identify_callback)
        self.gsMapToolRectangleMapTool = RectangleMapTool(self.gsMapCanvas)
        self.gsMapCanvas.setMapTool(self.gsMapToolPan)
        # 添加ToolBar用于切换Maptool
        tb_maptool = self.addToolBar('MapTools')
        self.actionPan = QAction(QIcon(':/images/mActionPan.png'),'Pan',self)
        self.actionPan.setCheckable(True)
        self.actionPan.setChecked(True)
        self.actionZoomIn = QAction(QIcon(':/images/mActionZoomIn.png'),'ZoomIn',self)
        self.actionZoomIn.setCheckable(True)
        self.actionZoomOut = QAction(QIcon(':/images/mActionZoomOut.png'),'ZoomOut',self)
        self.actionZoomOut.setCheckable(True)
        self.actionIdentifyFeature = QAction(QIcon(':/images/mActionIdentify.png'),'Identify',self)
        self.actionIdentifyFeature.setCheckable(True)
        self.actionRectangle = QAction(QIcon(':/images/mActionAddBasicRectangle.png'),'Rectangle',self)
        self.actionRectangle.setCheckable(True)

        tb_maptool.addAction(self.actionPan)
        tb_maptool.addAction(self.actionZoomIn)
        tb_maptool.addAction(self.actionZoomOut)
        tb_maptool.addAction(self.actionIdentifyFeature)
        tb_maptool.addAction(self.actionRectangle)
        tb_maptool.actionTriggered[QAction].connect(self.tbmaptoolbtnpressed)

        # 选择工具栏
        tb_selection = self.addToolBar('Selections')
        self.actionSelectAll = QAction(QIcon(':/images/mActionSelectAll.png'),'Select All',self)
        self.actionDeselectAll = QAction(QIcon(':/images/mActionDeselectAll.png'),'Deselect All',self)
        self.actionSelectByValue = QAction(QIcon(':/images/mIconFormSelect.png'),'Select By Value',self)
        self.actionSelectByExpression = QAction(QIcon(':/images/mIconExpressionSelect.png'), 'Select By Expression', self)

        tb_selection.addAction(self.actionSelectAll)
        tb_selection.addAction(self.actionDeselectAll)
        tb_selection.addAction(self.actionSelectByValue)
        tb_selection.addAction(self.actionSelectByExpression)
        tb_selection.actionTriggered[QAction].connect(self.tbselectionbtnpressed)
        # 增加右键菜单
        mymenu = MyMenuProvider(self)
        self.gsLayerTreeView.setMenuProvider(mymenu)

	    # 添加Project菜单
        self.actionNew.triggered.connect(self.project_new)
        self.actionOpen.triggered.connect(self.project_open)
        self.actionClose.triggered.connect(self.project_close)
        self.actionSave.triggered.connect(self.project_save)

        # add vector layer菜单
        self.actionOGR_data_provider_ogr.triggered.connect(self.ogr_addlayer)
        self.actionOGR_data_provider_ogr_Directory.triggered.connect(self.ogr_addlayer_dir)
        self.actionGPX_data_provider_gpx.triggered.connect(self.gpx_addlayer)
        self.actionDelimited_text_file_provider_delimitedtext.triggered.connect(self.csv_addlayer)
        self.actionSpatiaLite_data_provider_spatialite.triggered.connect(self.spatialite_addlayer)
        self.actionMemory_data_provider_memory.triggered.connect(self.memory_addlayer)
        self.actionWFS_web_feature_service_data_provider_wfs.triggered.connect(self.wfs_addlayer)
        # add raster layer菜单
        self.actionGDAL_data_provider_gdal.triggered.connect(self.gdal_addlayer)
        self.actionWMS_data_provider_wms.triggered.connect(self.wms_addlayer)
        QgsGui.editorWidgetRegistry().initEditors()

    def tbmaptoolbtnpressed(self, a):
        self.actionPan.setChecked(False)
        self.actionZoomIn.setChecked(False)
        self.actionZoomOut.setChecked(False)
        self.actionIdentifyFeature.setChecked(False)
        self.actionRectangle.setChecked(False)

        if self.actionPan == a:
            self.actionPan.setChecked(True)
            self.gsMapCanvas.setMapTool(self.gsMapToolPan)
        elif self.actionZoomIn == a:
            self.actionZoomIn.setChecked(True)
            self.gsMapCanvas.setMapTool(self.gsMapToolZoomIn)
        elif self.actionZoomOut == a:
            self.actionZoomOut.setChecked(True)
            self.gsMapCanvas.setMapTool(self.gsMapToolZoomOut)
        elif self.actionIdentifyFeature == a:
            self.actionIdentifyFeature.setChecked(True)
            self.gsMapCanvas.setMapTool(self.gsMapToolIdentifyFeature)
            self.gsMapToolIdentifyFeature.setLayer(self.gsMapCanvas.currentLayer())
        elif self.actionRectangle == a:
            self.actionRectangle.setChecked(True)
            self.gsMapCanvas.setMapTool(self.gsMapToolRectangleMapTool)

    def tbselectionbtnpressed(self, a):
        layer = self.gsMapCanvas.currentLayer()
        if layer is None:
            self.statusbar.showMessage('There is no active layer!!!')
            return
        if self.actionSelectAll == a:
            layer.selectAll()
        elif self.actionDeselectAll == a:
            layer.removeSelection()
        elif self.actionSelectByValue == a:
            self.attribute_form = QgsAttributeForm(layer)
            self.attribute_form.setMode(4)
            self.attribute_form.show()
        elif self.actionSelectByExpression == a:
            ed = QgsExpressionSelectionDialog(layer)
            ed.exec_()

    def identify_callback(self,feature):
        print("You clicked on feature {}".format(feature.id()))
        self.statusbar.showMessage("You clicked on feature {}".format(feature.id()))
        vlayer = self.gsMapCanvas.currentLayer()

        # self.attribute_dialog = QgsAttributeDialog(vlayer,feature,True)
        # self.attribute_dialog.show()
        self.attribute_form = QgsAttributeForm(vlayer,feature)
        self.attribute_form.setMode(0)
        self.attribute_form.show()

    def populateContextMenu(self,menu: QMenu, event: QgsMapMouseEvent):
        subMenu = menu.addMenu('My Menu')
        action = subMenu.addAction('My Action')
        action.triggered.connect(lambda *args:
                                 print(f'Action triggered at {event.x()},{event.y()}'))

    def project_new(self):
        project = QgsProject.instance()
        self.gsMapCanvas.setLayers([])
        self.gsMapCanvas.clearCache()
        project.clear()
        self.statusbar.showMessage("Project New Done!")

    def project_open(self):
        project = QgsProject.instance()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "*.qgs;;*.qgz;;*.qgd")
        project.read(file_path)
        self.statusbar.showMessage("Project read Done!")

    def project_close(self):
        QgsApplication.quit()

    def project_save(self):
        QgsProject.instance().write()
        self.statusbar.showMessage("Project write Done!")

    def ogr_addlayer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Data Source Manager | Vector", "../python_cookbook", "ogr files (*.shp *.gpx *.gpkg *.geojson *.kml *.gml *.dxf)")
        vlayer = QgsVectorLayer(file_path, Path(file_path).stem.__str__(), "ogr")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            subLayers = vlayer.dataProvider().subLayers()
            if len(subLayers) > 1:
                for subLayer in subLayers:
                    name = subLayer.split(QgsDataProvider.SUBLAYER_SEPARATOR)[1]
                    uri = "%s|layername=%s" % (file_path, name,)
                    sub_vlayer = QgsVectorLayer(uri, name, 'ogr')
                    QgsProject.instance().addMapLayer(sub_vlayer)
            else:
                QgsProject.instance().addMapLayer(vlayer)
            self.gsMapCanvas.setCurrentLayer(vlayer)

    def ogr_addlayer_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self,"Data Source Manager | Vector","../python_cookbook")
        vlayer = QgsVectorLayer(dir_path, Path(dir_path).stem.__str__(), "ogr")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)
            self.gsMapCanvas.setCurrentLayer(vlayer)

    def ogr_addlayer_gpkg(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Data Source Manager | Vector", "../python_cookbook",
                                                   "ogr files (*.shp *.gpx *.gpkg *.geojson *.kml *.gml *.dxf)")
        vlayer = QgsVectorLayer(file_path, Path(file_path).stem.__str__(), "ogr")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)
            self.gsMapCanvas.setCurrentLayer(vlayer)

    def gpx_addlayer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Data Source Manager | Gpx", "../python_cookbook", "gpx files (*.gpx)")
        routesLayer = QgsVectorLayer('{}?type=route'.format(file_path), "route", "gpx")
        tracksLayer = QgsVectorLayer('{}?type=track'.format(file_path), "track", "gpx")
        waypointsLayer = QgsVectorLayer('{}?type=waypoint'.format(file_path), "waypoint", "gpx")
        QgsProject.instance().addMapLayers([routesLayer,tracksLayer,waypointsLayer])

    def csv_addlayer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Data Source Manager | Delimitedtext", "../python_cookbook", "Delimitedtext files (*.csv)")
        uri = 'file:///{}?type=csv&xField=longitude&yField=latitude&crs=EPSG:4326'.format(file_path)
        vlayer = QgsVectorLayer(uri, Path(file_path).stem.__str__(), "delimitedtext")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)
            self.gsMapCanvas.setCurrentLayer(vlayer)

    def spatialite_addlayer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Data Source Manager | Delimitedtext", "../python_cookbook",
                                                   "Spatialite files (*.sqlite)")
        uri = QgsDataSourceUri()
        uri.setDatabase(file_path)
        schema = ''
        table = 'landuse'
        geom_column = 'Geometry'
        uri.setDataSource(schema, table, geom_column)

        display_name = 'landuse'
        vlayer = QgsVectorLayer(uri.uri(), display_name, 'spatialite')
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

    def memory_addlayer(self):
        '''
        # create layer
        vl = QgsVectorLayer("Point", "temporary_points", "memory")
        pr = vl.dataProvider()
        # add fields
        pr.addAttributes([QgsField("name", QVariant.String),
                          QgsField("age", QVariant.Int),
                          QgsField("size", QVariant.Double)])
        vl.updateFields()  # tell the vector layer to fetch changes from the provider

        # add a feature
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(10, 10)))
        fet.setAttributes(["Johny", 2, 0.3])
        pr.addFeatures([fet])

        # update layer's extent when new features have been added
        # because change of extent in provider is not propagated to the layer
        vl.updateExtents()
        self.statusbar.showMessage("Layer memory Done!")
        QgsProject.instance().addMapLayer(vl)
        '''
        ml = QgsNewMemoryLayerDialog.runAndCreateLayer()
        if ml is not None:
            QgsProject.instance().addMapLayer(ml)


    def wfs_addlayer(self):
        uri = "https://demo.mapserver.org/cgi-bin/wfs?service=WFS&version=2.0.0&request=GetFeature&typename=ms:cities"
        vlayer = QgsVectorLayer(uri, "my wfs layer", "WFS")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

    def gdal_addlayer(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Data Source Manager | Raster", "../python_cookbook", "gdal files (*.tiff *.tif *.gpkg)")
        rlayer = QgsRasterLayer(file_path, Path(file_path).stem.__str__(), "gdal")
        if not rlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(rlayer)
            self.gsMapCanvas.setCurrentLayer(rlayer)

    def wms_addlayer(self):
        layer_name = 'modis'
        urlWithParams = "crs=EPSG:4326&format=image/png&layers=continents&styles&url=https://demo.mapserver.org/cgi-bin/wms"
        rlayer = QgsRasterLayer(urlWithParams, 'some layer name', 'wms')
        if not rlayer.isValid():
            print("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(rlayer)
