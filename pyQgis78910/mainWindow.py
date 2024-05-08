import os

from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout

from qgis.PyQt.QtWidgets import QMainWindow
from qgis.core import QgsProject,QgsLayerTreeModel,QgsVectorLayer
from qgis.gui import QgsLayerTreeView,QgsMapCanvas,QgsLayerTreeMapCanvasBridge

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsVectorLayer,
    QgsPoint,
    QgsPointXY,
    QgsProject,
    QgsGeometry,
    QgsWkbTypes,
    QgsGeometry,
    QgsMapSettings,
    QgsPrintLayout,
    QgsMapSettings,
    QgsMapRendererParallelJob,
    QgsLayoutItemLabel,
    QgsLayoutItemLegend,
    QgsLayoutItemMap,
    QgsLayoutItemPolygon,
    QgsLayoutItemScaleBar,
    QgsLayoutExporter,
    QgsLayoutItem,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsUnitTypes,
    QgsProject,
    QgsFillSymbol,
    QgsAbstractValidityCheck,
    check,
)

from qgis.gui import (
    QgsMapCanvas,
    QgsRubberBand,
)

from qgis.PyQt.QtGui import (
    QPolygonF,
    QColor,
)

from qgis.PyQt.QtCore import (
    QPointF,
    QRectF,
    QSize,
)

from ui.MainWindow import Ui_MainWindow
from rightClickContextMenu import menuProvider


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
        #
        self.rightMenu = menuProvider(self)
        self.gsLayerTreeView.setMenuProvider(self.rightMenu)

        vlayer = QgsVectorLayer("../python_cookbook/airports.shp", "airports", "ogr")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)

        # Sometimes one geometry is actually a collection of simple (single-part) geometries. Such a geometry is called a multi-part geometry.
        # If it contains just one type of simple geometry, we call it multi-point, multi-linestring or multi-polygon.

        # 7.1.Geometry Construction
        gPnt = QgsGeometry.fromPointXY(QgsPointXY(1, 1))
        print(gPnt)
        gLine = QgsGeometry.fromPolyline([QgsPoint(1, 1), QgsPoint(2, 2)])
        print(gLine)
        gPolygon = QgsGeometry.fromPolygonXY([[QgsPointXY(1, 1),
                                               QgsPointXY(2, 2), QgsPointXY(2, 1)]])
        print(gPolygon)
        # A Polygon is represented by a list of linear rings (i.e. closed linestrings). The first ring is the outer ring (boundary), optional subsequent rings are holes in the polygon.
        geom = QgsGeometry.fromWkt("POINT(3 4)")
        print(geom)
        g = QgsGeometry()
        wkb = bytes.fromhex("010100000000000000000045400000000000001440")
        g.fromWkb(wkb)

        # print WKT representation of the geometry
        print(g.asWkt())

        # 7.2. Access to Geometry
        if gPnt.wkbType() == QgsWkbTypes.Point:
            print(gPnt.wkbType())
            # output: 1 for Point
        if gLine.wkbType() == QgsWkbTypes.LineString:
            print(gLine.wkbType())
            # output: 2 for LineString
        if gPolygon.wkbType() == QgsWkbTypes.Polygon:
            print(gPolygon.wkbType())
            # output: 3 for Polygon

        # 7.3. Geometry Predicates and Operations

        # 8.1.Coordinate reference systems
        # Note that for initialization of spatial reference systems QGIS needs to look up appropriate values in its internal database srs.db.
        # Thus in case you create an independent application you need to set paths correctly with QgsApplication.setPrefixPath()
        crs = QgsCoordinateReferenceSystem("EPSG:4326")

        print("QGIS CRS ID:", crs.srsid())
        print("PostGIS SRID:", crs.postgisSrid())
        print("Description:", crs.description())
        print("Projection Acronym:", crs.projectionAcronym())
        print("Ellipsoid Acronym:", crs.ellipsoidAcronym())
        print("Proj String:", crs.toProj())
        # check whether it's geographic or projected coordinate system
        print("Is geographic:", crs.isGeographic())
        # check type of map units in this CRS (values defined in QGis::units enum)
        print("Map units:", crs.mapUnits())
        # 9. Using the Map Canvas
        # The layers are rendered to an image (using the QgsMapRendererJob class) and that image is displayed on the canvas.
        # 9.1.Embedding Map Canvas
        # 9.2.Rubber Bands and Vertex Markers
        r = QgsRubberBand(self.gsMapCanvas, QgsWkbTypes.PolygonGeometry)  # polygon
        points = [[QgsPointXY(-100, 35), QgsPointXY(10, 50), QgsPointXY(120, 35)]]
        r.setToGeometry(QgsGeometry.fromPolygonXY(points), None)
        self.gsMapCanvas.scene().removeItem(r)
        # 9.3. Using Map Tools with Canvas

        # 10. Map Rendering and Printing
        # 10.1. Simple Rendering
        image_location = os.path.join(QgsProject.instance().homePath(), "myrender.png")

        settings = QgsMapSettings()
        settings.setLayers([vlayer])
        settings.setBackgroundColor(QColor(255, 255, 255))
        settings.setOutputSize(QSize(800, 600))
        settings.setExtent(vlayer.extent())

        render = QgsMapRendererParallelJob(settings)

        def finished():
            img = render.renderedImage()
            # save the image; e.g. img.save("/Users/myuser/render.png","png")
            img.save(image_location, "png")

        render.finished.connect(finished)

        # Start the rendering
        render.start()

        # The following loop is not normally required, we
        # are using it here because this is a standalone example.
        from qgis.PyQt.QtCore import QEventLoop
        loop = QEventLoop()
        render.finished.connect(loop.quit)
        loop.exec_()

        # 10.3.Output using print layout
        # TODO 先学习一下C++部分的代码，py可以作为提纲