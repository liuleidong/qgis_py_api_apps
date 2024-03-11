import os

from qgis.PyQt.QtWidgets import QMainWindow
from qgis.core import QgsProject,QgsLayerTreeModel,QgsVectorLayer,QgsDataSourceUri
from qgis.gui import QgsLayerTreeView,QgsMapCanvas,QgsLayerTreeMapCanvasBridge,QgisInterface
from ui.MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout


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
        self.gsLayerTreeBridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), self.gsMapCanvas, self)
        # connect actions to slot
        self.actionQgisInterface.triggered.connect(self.iface)
        self.actionShapefile.triggered.connect(self.gdal_shapefile)
        self.actiondxf.triggered.connect(self.gdal_dxf)
        self.actiongeopackage.triggered.connect(self.gdal_geopackage)
        self.actionpostgis.triggered.connect(self.postgis)
        self.actioncsv.triggered.connect(self.csv)
        self.actiongpx.triggered.connect(self.gpx)

    def iface(self):
        # iface只能在QGis中使用
        # TypeError: qgis._gui.QgisInterface represents a C++ abstract class and cannot be instantiated
        iface = QgisInterface()
        vlayer = iface.addvectorLayer("../python_cookbook/airports.shp", "airports", "ogr")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

    def gdal_shapefile(self):
        vlayer = QgsVectorLayer("../python_cookbook/airports.shp", "airports", "ogr")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

    def gdal_dxf(self):
        # sample.dxf包含的集合类型是LineString,官方教程写的是Polygon，不能示
        # uri = "../python_cookbook/sample.dxf|layername=entities|geometrytype=Polygon"
        # 改成geometrytype=LineString后，可以正常显示
        # uri = "../python_cookbook/sample.dxf|layername=entities|geometrytype=LineString"
        # sample.dxf似乎会默认显示第一个图层
        uri = "../python_cookbook/sample.dxf"
        vlayer = QgsVectorLayer(uri, "sample", "ogr")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

    def gdal_geopackage(self):
        # 如果直接传，只能显示第一个图层
        # uri = r'../python_cookbook/network.gpkg'
        # 通过layername参数指定加载图层
        uri = r'../python_cookbook/network.gpkg|layername=network_points'
        vlayer = QgsVectorLayer(uri, "network", "ogr")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

    def postgis(self):
        # 需要实际数据库才能正常显示
        uri = QgsDataSourceUri()
        # set host name, port, database name, username and password
        uri.setConnection("localhost", "5432", "dbname", "johny", "xxx")
        # set database schema, table name, geometry column and optionally
        # subset (WHERE clause)
        uri.setDataSource("public", "roads", "the_geom", "cityid = 2643", "primary_key_field")
        vlayer = QgsVectorLayer(uri.uri(False), "layer name you like", "postgres")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

    def csv(self):
        # 注意file:///，三个斜杠
        filepath = os.getcwd() + r'\..\python_cookbook\delimited_xy.csv'
        uri = "file:///{}?delimiter={}&xField={}&yField={}".format(filepath, ";", "x", "y")
        print(uri)
        vlayer = QgsVectorLayer(uri, "layer name you like", "delimitedtext")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

    def gpx(self):
        # 使用type区分不同类型
        # type可取值：track waypoint route
        uri = r'..\python_cookbook\layers.gpx?type=track'
        vlayer = QgsVectorLayer(uri, "layer name you like", "gpx")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)
