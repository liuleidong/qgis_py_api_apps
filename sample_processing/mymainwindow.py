from functools import partial
from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QAction

from qgis.PyQt.QtWidgets import QMainWindow,QMenu, QFileDialog
from qgis.core import QgsProject,QgsLayerTreeModel,QgsVectorLayer,QgsApplication,QgsDataSourceUri,QgsRasterLayer
from qgis.core import (
  QgsProcessingContext,
  QgsTaskManager,
  QgsTask,
  QgsProcessingAlgRunnerTask,
  Qgis,
  QgsProcessingFeedback,
  QgsApplication,
  QgsMessageLog,
)
from qgis.gui import QgsLayerTreeView,QgsMapCanvas,QgsLayerTreeMapCanvasBridge,QgsMapToolPan,QgsMapToolZoom,QgsMapToolIdentifyFeature,QgsMapMouseEvent

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
        tb = self.addToolBar('MapTools')
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

        tb.addAction(self.actionPan)
        tb.addAction(self.actionZoomIn)
        tb.addAction(self.actionZoomOut)
        tb.addAction(self.actionIdentifyFeature)
        tb.addAction(self.actionRectangle)
        tb.actionTriggered[QAction].connect(self.toolbtnpressed)

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
        # process
        self.actionrandompointsinextent.triggered.connect(self.process_randompointsinextent)
        self.actionqgis_randompointsinsidepolygons.triggered.connect(self.process_randompointsinsidepolygons)
        self.actiongdal_cliprasterbyextent.triggered.connect(self.process_gdalcliprasterbyextent)

    def toolbtnpressed(self, a):
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

    def process_gdalcliprasterbyextent(self):
        def task_finished(context, successful, results):
            vlayer = QgsRasterLayer(results['OUTPUT'],'raster')
            QgsProject.instance().addMapLayer(vlayer)

        alg = QgsApplication.processingRegistry().algorithmById(
            'gdal:cliprasterbyextent')
        self.context = QgsProcessingContext()
        self.feedback = QgsProcessingFeedback()
        params = {'INPUT':'../python_cookbook/multiband.tif','PROJWIN':'20.434202040,20.457151583,-34.028299615,-34.012483038 [EPSG:4326]','OVERCRS':False,'NODATA':None,'OPTIONS':'','DATA_TYPE':0,'EXTRA':'','OUTPUT':'TEMPORARY_OUTPUT'}
        self.task = QgsProcessingAlgRunnerTask(alg, params, self.context, self.feedback)
        self.task.executed.connect(partial(task_finished, self.context))
        QgsApplication.taskManager().addTask(self.task)

    def process_randompointsinsidepolygons(self):
        MESSAGE_CATEGORY = 'AlgRunnerTask'
        def task_finished(context, successful, results):
            if not successful:
                QgsMessageLog.logMessage('Task finished unsucessfully',
                                         MESSAGE_CATEGORY, Qgis.Warning)
            output_layer = context.getMapLayer(results['OUTPUT'])
            # because getMapLayer doesn't transfer ownership, the layer will
            # be deleted when context goes out of scope and you'll get a
            # crash.
            # takeMapLayer transfers ownership so it's then safe to add it
            # to the project and give the project ownership.
            if output_layer and output_layer.isValid():
                QgsProject.instance().addMapLayer(
                    context.takeResultLayer(output_layer.id()))

        alg = QgsApplication.processingRegistry().algorithmById(
            'qgis:randompointsinsidepolygons')
        self.context = QgsProcessingContext()
        self.feedback = QgsProcessingFeedback()
        params = {'INPUT':'../python_cookbook/protected_areas.shp','STRATEGY':0,'VALUE':10,'MIN_DISTANCE':None,'OUTPUT':'TEMPORARY_OUTPUT'}
        self.task = QgsProcessingAlgRunnerTask(alg, params, self.context, self.feedback)
        self.task.executed.connect(partial(task_finished, self.context))
        QgsApplication.taskManager().addTask(self.task)

    def process_randompointsinextent(self):
        MESSAGE_CATEGORY = 'AlgRunnerTask'
        def task_finished(context, successful, results):
            if not successful:
                QgsMessageLog.logMessage('Task finished unsucessfully',
                                         MESSAGE_CATEGORY, Qgis.Warning)
            output_layer = context.getMapLayer(results['OUTPUT'])
            # because getMapLayer doesn't transfer ownership, the layer will
            # be deleted when context goes out of scope and you'll get a
            # crash.
            # takeMapLayer transfers ownership so it's then safe to add it
            # to the project and give the project ownership.
            if output_layer and output_layer.isValid():
                QgsProject.instance().addMapLayer(
                    context.takeResultLayer(output_layer.id()))

        alg = QgsApplication.processingRegistry().algorithmById(
            'native:randompointsinextent')
        # `context` and `feedback` need to
        # live for as least as long as `task`,
        # otherwise the program will crash.
        # Initializing them globally is a sure way
        # of avoiding this unfortunate situation.
        self.context = QgsProcessingContext()
        self.feedback = QgsProcessingFeedback()
        params = {
            'EXTENT': '0.0,10.0,40,50 [EPSG:4326]',
            'MIN_DISTANCE': 0.0,
            'POINTS_NUMBER': 50000,
            'TARGET_CRS': 'EPSG:4326',
            'OUTPUT': 'memory:My random points'
        }
        self.task = QgsProcessingAlgRunnerTask(alg, params, self.context, self.feedback)
        self.task.executed.connect(partial(task_finished, self.context))
        QgsApplication.taskManager().addTask(self.task)

    def identify_callback(self,feature):
        print("You clicked on feature {}".format(feature.id()))
        self.statusbar.showMessage("You clicked on feature {}".format(feature.id()))

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
        pass

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
