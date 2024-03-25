import os

from qgis.PyQt.QtWidgets import QMainWindow,QMessageBox
from qgis.core import QgsProject,QgsLayerTreeModel,QgsVectorLayer,QgsDataSourceUri,QgsRasterLayer
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
        self.actionSpatiaLite.triggered.connect(self.spatiaLite)
        self.actionMySQL.triggered.connect(self.mysql)
        self.actionWFS.triggered.connect(self.wfs)
        self.actionTif.triggered.connect(self.tiff)
        self.actionGeopackage.triggered.connect(self.gpkg)
        self.actionPostGIS.triggered.connect(self.raster_postgis)
        self.actionWCS.triggered.connect(self.wcs)

    def iface(self):
        # iface只能在QGis中使用
        QMessageBox.information(self, r'Tip', r'iface只能在QGis中使用',
                                QMessageBox.Yes)  # 2
        # TypeError: qgis._gui.QgisInterface represents a C++ abstract class and cannot be instantiated
        # iface = QgisInterface()
        # vlayer = iface.addvectorLayer("../python_cookbook/airports.shp", "airports", "ogr")
        # if not vlayer:
        #     self.statusbar.showMessage("Layer failed to load!")
        # else:
        #     self.statusbar.showMessage("Layer load Done!")
    #     QgsProject.instance().addMapLayer(vlayer)

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

        QMessageBox.information(self, r'Tip', r'修改数据库ip等信息才能正常显示',
                                QMessageBox.Yes)  # 2
        # 需要实际数据库才能正常显示
        uri = QgsDataSourceUri()
        # set host name, port, database name, username and password
        uri.setConnection("localhost", "5432", "dbname", "johny", "xxx")
        # set database schema, table name, geometry column and optionally
        # subset (WHERE clause)
        uri.setDataSource("public", "roads", "the_geom", "cityid = 2643", "primary_key_field")
        vlayer = QgsVectorLayer(uri.uri(False), "postgis", "postgres")
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
        vlayer = QgsVectorLayer(uri, "csv", "delimitedtext")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

    def gpx(self):
        # 使用type区分不同类型
        # type可取值：track waypoint route
        uri = r'..\python_cookbook\layers.gpx?type=track'
        vlayer = QgsVectorLayer(uri, "gpx", "gpx")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

    def spatiaLite(self):
        uri = QgsDataSourceUri()
        uri.setDatabase(r'..\python_cookbook\landuse.sqlite')
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

    def mysql(self):

        QMessageBox.information(self, r'Tip', r'修改数据库ip等信息才能正常显示',
                                QMessageBox.Yes)  # 2
        # uri = "MySQL:dbname,host=localhost,port=3306,user=root,password=xxx|layername=my_table"
        # vlayer = QgsVectorLayer(uri, "my table", "ogr")
        # if not vlayer:
        #     self.statusbar.showMessage("Layer failed to load!")
        # else:
        #     self.statusbar.showMessage("Layer load Done!")
        #     QgsProject.instance().addMapLayer(vlayer)

    def wfs(self):
        uri = "https://demo.mapserver.org/cgi-bin/wfs?service=WFS&version=2.0.0&request=GetFeature&typename=ms:cities"
        vlayer = QgsVectorLayer(uri, "my wfs layer", "WFS")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

    def tiff(self):
        # get the path to a tif file  e.g. /home/project/data/srtm.tif
        path_to_tif = r"../python_cookbook/data/srtm.tif"
        rlayer = QgsRasterLayer(path_to_tif, "SRTM layer name")
        if not rlayer.isValid():
            print("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(rlayer)

    def gpkg(self):
        # get the path to a geopackage  e.g. /home/project/data/data.gpkg
        path_to_gpkg = os.getcwd() + r'\..\python_cookbook\sublayers.gpkg'
        gpkg_raster_layer = "GPKG:" + path_to_gpkg + ":srtm"
        rlayer = QgsRasterLayer(gpkg_raster_layer, "gpkg", "gdal")
        if not rlayer.isValid():
            print("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(rlayer)

    def raster_postgis(self):
        QMessageBox.information(self, r'Tip', r'修改数据库ip等信息才能正常显示',
                                QMessageBox.Yes) 
        # uri_config = {
        #     # database parameters
        #     'dbname': 'gis_db',  # The PostgreSQL database to connect to.
        #     'host': 'localhost',  # The host IP address or localhost.
        #     'port': '5432',  # The port to connect on.
        #     'sslmode': QgsDataSourceUri.SslDisable,  # SslAllow, SslPrefer, SslRequire, SslVerifyCa, SslVerifyFull
        #     # user and password are not needed if stored in the authcfg or service
        #     'authcfg': 'QconfigId',  # The QGIS athentication database ID holding connection details.
        #     'service': None,  # The PostgreSQL service to be used for connection to the database.
        #     'username': None,  # The PostgreSQL user name.
        #     'password': None,  # The PostgreSQL password for the user.
        #     # table and raster column details
        #     'schema': 'public',  # The database schema that the table is located in.
        #     'table': 'my_rasters',  # The database table to be loaded.
        #     'geometrycolumn': 'rast',  # raster column in PostGIS table
        #     'sql': None,  # An SQL WHERE clause. It should be placed at the end of the string.
        #     'key': None,  # A key column from the table.
        #     'srid': None,  # A string designating the SRID of the coordinate reference system.
        #     'estimatedmetadata': 'False',  # A boolean value telling if the metadata is estimated.
        #     'type': None,  # A WKT string designating the WKB Type.
        #     'selectatid': None,  # Set to True to disable selection by feature ID.
        #     'options': None,  # other PostgreSQL connection options not in this list.
        #     'enableTime': None,
        #     'temporalDefaultTime': None,
        #     'temporalFieldIndex': None,
        #     'mode': '2',
        #     # GDAL 'mode' parameter, 2 unions raster tiles, 1 adds tiles separately (may require user input)
        # }
        # # remove any NULL parameters
        # uri_config = {key: val for key, val in uri_config.items() if val is not None}
        # # get the metadata for the raster provider and configure the URI
        # md = QgsProviderRegistry.instance().providerMetadata('postgresraster')
        # uri = QgsDataSourceUri(md.encodeUri(uri_config))
        #
        # # the raster can then be loaded into the project
        # rlayer = iface.addRasterLayer(uri.uri(False), "raster layer name", "postgresraster")

    def wcs(self):
        layer_name = 'modis'
        url = "https://demo.mapserver.org/cgi-bin/wcs?identifier={}".format(layer_name)
        rlayer = QgsRasterLayer(url, 'my wcs layer', 'wcs')
        if not rlayer.isValid():
            print("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(rlayer)