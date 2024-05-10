from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QAction

from qgis.PyQt.QtWidgets import QMainWindow
from qgis.core import QgsProject,QgsLayerTreeModel,QgsVectorLayer
from qgis.gui import QgsLayerTreeView,QgsMapCanvas,QgsLayerTreeMapCanvasBridge,QgsMapToolPan,QgsMapToolZoom

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
        # 加载测试图层
        vlayer = QgsVectorLayer("../python_cookbook/airports.shp", "airports", "ogr")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)
        # 添加三个maptool
        self.gsMapToolPan = QgsMapToolPan(self.gsMapCanvas)
        self.gsMapToolZoomIn = QgsMapToolZoom(self.gsMapCanvas,False)
        self.gsMapToolZoomOut = QgsMapToolZoom(self.gsMapCanvas,True)
        self.gsMapCanvas.setMapTool(self.gsMapToolPan)
        # 添加ToolBar用于切换Maptool
        tb = self.addToolBar('MapTools')
        self.actionPan = QAction(QIcon(':/images/mActionPan.png'),'Pan',self)
        self.actionZoomIn = QAction(QIcon(':/images/mActionZoomIn.png'),'ZoomIn',self)
        self.actionZoomOut = QAction(QIcon(':/images/mActionZoomOut.png'),'ZoomOut',self)
        tb.addAction(self.actionPan)
        tb.addAction(self.actionZoomIn)
        tb.addAction(self.actionZoomOut)
        tb.actionTriggered[QAction].connect(self.toolbtnpressed)

    def toolbtnpressed(self, a):
        if self.actionPan == a:
            self.gsMapCanvas.setMapTool(self.gsMapToolPan)
        elif self.actionZoomIn == a:
            self.gsMapCanvas.setMapTool(self.gsMapToolZoomIn)
        elif self.actionZoomOut == a:
            self.gsMapCanvas.setMapTool(self.gsMapToolZoomOut)