from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QAction

from qgis.PyQt.QtWidgets import QMainWindow,QMenu
from qgis.core import QgsProject,QgsLayerTreeModel,QgsVectorLayer
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
        # 加载测试图层
        vlayer = QgsVectorLayer("../python_cookbook/airports.shp", "airports", "ogr")
        if not vlayer:
            self.statusbar.showMessage("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(vlayer)
            self.gsMapCanvas.setCurrentLayer(vlayer)
        # 添加三个maptool
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

    def toolbtnpressed(self, a):
        self.actionPan.setChecked(False)
        self.actionZoomOut.setChecked(False)
        self.actionZoomIn.setChecked(False)
        self.actionIdentifyFeature.setChecked(False)
        if self.actionPan == a:
            self.gsMapCanvas.setMapTool(self.gsMapToolPan)
        elif self.actionZoomIn == a:
            self.gsMapCanvas.setMapTool(self.gsMapToolZoomIn)
        elif self.actionZoomOut == a:
            self.gsMapCanvas.setMapTool(self.gsMapToolZoomOut)
        elif self.actionIdentifyFeature == a:
            self.gsMapCanvas.setMapTool(self.gsMapToolIdentifyFeature)
            self.gsMapToolIdentifyFeature.setLayer(self.gsMapCanvas.currentLayer())
        elif self.actionRectangle == a:
            self.gsMapCanvas.setMapTool(self.gsMapToolRectangleMapTool)

    def identify_callback(self,feature):
        print("You clicked on feature {}".format(feature.id()))
        self.statusbar.showMessage("You clicked on feature {}".format(feature.id()))

    def populateContextMenu(self,menu: QMenu, event: QgsMapMouseEvent):
        subMenu = menu.addMenu('My Menu')
        action = subMenu.addAction('My Action')
        action.triggered.connect(lambda *args:
                                 print(f'Action triggered at {event.x()},{event.y()}'))
