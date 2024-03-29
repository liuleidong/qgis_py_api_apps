import os

from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout

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

        project = QgsProject.instance()
        filepath = os.getcwd() + r'\..\python_cookbook\01_project.qgs'
        project.read(filepath)

        # 4.1
        # 返回的是key:value，其中key是layerid，value是layer指针
        layers = QgsProject.instance().mapLayers()
        print(layers)
        # 所以可以遍历获取layer的信息如id,name等等
        l = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
        print(l)
        country_layer = QgsProject.instance().mapLayersByName("countries")[0]
        print(country_layer)

        # 4.2
        # QgsLayerTreeGroup QgsLayerTreeLayer
        root = QgsProject.instance().layerTreeRoot()
        print(root)
        print(root.children())
        child0 = root.children()[0]
        print(child0)
        ids = root.findLayerIds()
        print(ids)
        l = root.findLayer(ids[0])
        print(l.layerId())
        root.addGroup('testGroup')
        checked_layers = root.checkedLayers()
        print(checked_layers)
        # Explicit addition using the addLayer() or insertLayer() functions:
        layer1 = QgsVectorLayer("path_to_layer", "Layer 1", "memory")
        # root.addLayer(layer1)
        root.insertLayer(5,layer1)

        # 延伸一下 在cpp基础上如何实现py
        node_layer = root.findLayer(ids[0])
        print("Layer node:", node_layer)
        print("Map layer:", node_layer.layer())

        node_group1 = root.addGroup('Simple Group')
        # add a sub-group to Simple Group
        node_subgroup1 = node_group1.addGroup("I'm a sub group")

        # 移动组
        # clone the group
        cloned_group1 = node_group1.clone()
        # move the node (along with sub-groups and layers) to the top
        root.insertChildNode(0, cloned_group1)
        # remove the original node
        root.removeChildNode(node_group1)

        # 移动图层
        # get a QgsVectorLayer
        vl = QgsProject.instance().mapLayersByName("countries")[0]
        # create a QgsLayerTreeLayer object from vl by its id
        myvl = root.findLayer(vl.id())
        # clone the myvl QgsLayerTreeLayer object
        myvlclone = myvl.clone()
        # get the parent. If None (layer is not in group) returns ''
        parent = myvl.parent()
        # move the cloned layer to the top (0)
        parent.insertChildNode(0, myvlclone)
        # remove the original myvl
        root.removeChildNode(myvl)

        # 移动到其他组
        # get a QgsVectorLayer
        vl = QgsProject.instance().mapLayersByName("countries")[0]
        # create a QgsLayerTreeLayer object from vl by its id
        myvl = root.findLayer(vl.id())
        # clone the myvl QgsLayerTreeLayer object
        myvlclone = myvl.clone()
        # create a new group
        group1 = root.addGroup("Group1")
        # get the parent. If None (layer is not in group) returns ''
        parent = myvl.parent()
        # move the cloned layer to the top (0)
        group1.insertChildNode(0, myvlclone)
        # remove the QgsLayerTreeLayer from its parent
        parent.removeChildNode(myvl)

        node_group1 = root.findGroup("Group1")
        # change the name of the group
        node_group1.setName("Group X")
        node_layer2 = root.findLayer(country_layer.id())
        # change the name of the layer
        node_layer2.setName("Layer X")
        # change the visibility of a layer
        node_group1.setItemVisibilityChecked(True)
        node_layer2.setItemVisibilityChecked(False)
        # expand/collapse the group view
        node_group1.setExpanded(True)
        node_group1.setExpanded(False)