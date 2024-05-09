from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout

from qgis.PyQt.QtWidgets import QMainWindow
from qgis.core import QgsProject,QgsLayerTreeModel,QgsVectorLayer
from qgis.gui import QgsLayerTreeView,QgsMapCanvas,QgsLayerTreeMapCanvasBridge

from ui.MainWindow import Ui_MainWindow


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
        self.gsLayerTreeBridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), self.gsMapCanvas)

        vlayer = QgsVectorLayer("../python_cookbook/airports.shp", "airports", "ogr")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)