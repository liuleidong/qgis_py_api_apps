
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout

import os

from qgis.core import (
qgsDoubleToString,
    Qgis,
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

from qgis.PyQt.QtGui import (
    QPolygonF,
    QColor,
)

from qgis.PyQt.QtCore import (
    QPointF,
    QRectF,
    QSize,
)

from qgis.PyQt.QtWidgets import QMainWindow
from qgis.core import QgsProject,QgsLayerTreeModel,QgsVectorLayer
from qgis.gui import QgsLayerTreeView,QgsMapCanvas,QgsLayerTreeMapCanvasBridge

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

        project = QgsProject.instance()
        layout = QgsPrintLayout(project)
        layout.initializeDefaults()
        layout.setName("MyLayout")
        project.layoutManager().addLayout(layout)

        map = QgsLayoutItemMap(layout)
        # Set map item position and size (by default, it is a 0 width/0 height item placed at 0,0)
        map.attemptMove(QgsLayoutPoint(5, 5, QgsUnitTypes.LayoutMillimeters))
        map.attemptResize(QgsLayoutSize(200, 200, QgsUnitTypes.LayoutMillimeters))
        # Provide an extent to render
        map.zoomToExtent(self.gsMapCanvas.extent())
        layout.addLayoutItem(map)

        label = QgsLayoutItemLabel(layout)
        label.setText("Hello world")
        label.adjustSizeToText()
        layout.addLayoutItem(label)
        #
        # base_path = os.path.join(QgsProject.instance().homePath())
        # pdf_path = os.path.join(base_path, "output.pdf")
        #
        # exporter = QgsLayoutExporter(layout)
        # exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())
        print(Qgis.releaseName())
        print(Qgis.version())
        print(Qgis.devVersion())
        print(Qgis.MessageLevel.Info)
        print(qgsDoubleToString(1.66666666))