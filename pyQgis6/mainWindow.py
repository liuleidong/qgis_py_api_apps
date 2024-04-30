
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout

from qgis.PyQt.QtWidgets import QMainWindow
from qgis.gui import QgsLayerTreeView,QgsMapCanvas,QgsLayerTreeMapCanvasBridge
from qgis.core import (
  QgsApplication,
  QgsDataSourceUri,
  QgsCategorizedSymbolRenderer,
  QgsClassificationRange,
  QgsPointXY,
  QgsProject,
  QgsExpression,
  QgsField,
  QgsFields,
  QgsFeature,
  QgsFeatureRequest,
  QgsFeatureRenderer,
  QgsGeometry,
  QgsGraduatedSymbolRenderer,
  QgsMarkerSymbol,
  QgsMessageLog,
  QgsRectangle,
  QgsRendererCategory,
  QgsRendererRange,
  QgsSymbol,
  QgsVectorDataProvider,
  QgsVectorLayer,
  QgsVectorFileWriter,
  QgsWkbTypes,
  QgsSpatialIndex,
  QgsVectorLayerUtils,
  QgsLayerTreeModel
)

from qgis.core.additions.edit import edit

from qgis.PyQt.QtGui import (
    QColor,
)

from qgis.PyQt.QtGui import (
    QColor,
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


        vlayer = QgsVectorLayer(r"../python_cookbook/airports.shp", "airports", "ogr")
        if not vlayer.isValid():
            print("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)
        # 6.1. Retrieving information about attributes
        for field in vlayer.fields():
            print(field.name(), field.typeName())
        print(vlayer.displayField())

        # 6.2. Iterating over Vector Layer
        features = vlayer.getFeatures()
        for feature in features:
            print("Feature ID:",feature.id())
            geom = feature.geometry()
            geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
            if geom.type() == QgsWkbTypes.PointGeometry:
                # the geometry type can be of single or multi type
                if geomSingleType:
                    x = geom.asPoint()
                    print("Point: ", x)
                else:
                    x = geom.asMultiPoint()
                    print("MultiPoint: ", x)
            elif geom.type() == QgsWkbTypes.LineGeometry:
                if geomSingleType:
                    x = geom.asPolyline()
                    print("Line: ", x, "length: ", geom.length())
                else:
                    x = geom.asMultiPolyline()
                    print("MultiLine: ", x, "length: ", geom.length())
            elif geom.type() == QgsWkbTypes.PolygonGeometry:
                if geomSingleType:
                    x = geom.asPolygon()
                    print("Polygon: ", x, "Area: ", geom.area())
                else:
                    x = geom.asMultiPolygon()
                    print("MultiPolygon: ", x, "Area: ", geom.area())
            else:
                print("Unknown or invalid geometry")
                # fetch attributes
            attrs = feature.attributes()
            # attrs is a list. It contains all the attribute values of this feature
            print(attrs)
            # for this test only print the first feature
            break

        # 6.3.Selecting features
        vlayer.selectAll()
        vlayer.removeSelection()

        vlayer.selectByExpression('"fk_region" >= 18')
        vlayer.removeSelection()

        selected_fid = []
        fi = vlayer.getFeatures()
        selected_fid.append(next(fi).id())
        selected_fid.append(next(fi).id())
        selected_fid.append(next(fi).id())
        vlayer.select(selected_fid)
        # 6.3.1. Accessing attributes
        feature = next(fi)
        print(feature['name'])
        print(feature[1])

        # 6.3.2. Iterating over selected features
        selection = vlayer.selectedFeatures()
        sf = next(iter(selection))
        print(sf[1])

        # 6.3.3. Iterating over a subset of features
        areaOfInterest = QgsRectangle(-1692674, 6619308,-417842,5731479)
        request = QgsFeatureRequest().setFilterRect(areaOfInterest).setFlags(QgsFeatureRequest.ExactIntersect)
        request.setLimit(2)
        for feature in vlayer.getFeatures(request):
            vlayer.select(feature.id())
        vlayer.removeSelection()

        exp = QgsExpression('"fk_region" > 18')
        request = QgsFeatureRequest(exp)

        # 6.4.Modifying Vector Layers
        caps = vlayer.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.DeleteFeatures:
            print('The layer supports DeleteFeatures')

        caps_string = vlayer.dataProvider().capabilitiesString()
        print(caps_string)

        # If caching is enabled, a simple canvas refresh might not be sufficient
        # to trigger a redraw and you must clear the cached image for the layer
        if self.gsMapCanvas.isCachingEnabled():
            vlayer.triggerRepaint()
        else:
            self.gsMapCanvas.refresh()

        # 6.4.1. Add Features
        if caps & QgsVectorDataProvider.AddFeatures:
            feat = QgsFeature(vlayer.fields())
        # 6.4.2. Delete Features
        if caps & QgsVectorDataProvider.DeleteFeatures:
            res = vlayer.dataProvider().deleteFeatures([5, 10])
        # 6.4.3.Modify Features
        fid = 0
        # if caps & QgsVectorDataProvider.ChangeAttributeValues:
        #     attrs = {0: "hello", 1: 123}
        #     vlayer.dataProvider().changeAttributeValues({fid: attrs})
        # if caps & QgsVectorDataProvider.ChangeGeometries:
        #     geom = QgsGeometry.fromPointXY(QgsPointXY(111, 222))
        #     vlayer.dataProvider().changeGeometryValues({fid: geom})

        ### Favor QgsVectorLayerEditUtils class for geometry-only edits
        # 6.4.4.Modifying Vector Layers with an Editing Buffer
        # QgsVectorDataProvider是直接修改数据，而QgsVectorLayer是在buffer中修改，最后commit生效
        # layer.beginEditCommand("Feature triangulation")
        # # ... call layer's editing methods ...
        # if problem_occurred:
        #     layer.destroyEditCommand()
        #     # ... tell the user that there was a problem
        #     # and return
        # # ... more editing ...
        # layer.endEditCommand()
        # 6.4.5.Adding and Removing Fields
        # layer.dataProvider().addAttributes
        # layer.dataProvider().deleteAttributes([0])
        # layer.updateFields()
        # 6.5. Using Spatial Index
        # Think of a layer without a spatial index as a telephone book in which telephone numbers are not ordered or indexed.
        # The only way to find the telephone number of a given person is to read from the beginning until you find it.
        index = QgsSpatialIndex()
        # index.addFeature(feat)
        index.addFeature(vlayer.getFeatures())
        # QgsSpatialIndexKDBush
        # 6.6. The QgsVectorLayerUtils class
        # feat = QgsVectorLayerUtils.createFeature(vlayer)
        # val = QgsVectorLayerUtils.getValues(vlayer, "NAME", selectedOnly=True)
        # 6.7.Creating Vector Layers
        