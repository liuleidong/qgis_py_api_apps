from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMenu, QMessageBox,QAction

from qgis.gui import QgsLayerTreeViewMenuProvider,QgsLayerTreeViewDefaultActions,QgsLayerTreeView,QgsMapCanvas
from qgis.core import QgsLayerTree,QgsLayerTreeGroup,QgsMapLayer,QgsVectorLayer,QgsProject


class MyMenuProvider(QgsLayerTreeViewMenuProvider):
    def __init__(self, MyMainWindow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layerTreeView: QgsLayerTreeView = MyMainWindow.gsLayerTreeView
        self.mapCanvas: QgsMapCanvas = MyMainWindow.gsMapCanvas
        self.myMainWindows = MyMainWindow

    def createContextMenu(self) -> QtWidgets.QMenu:
        try:
            menu = QMenu()
            self.actions: QgsLayerTreeViewDefaultActions = self.layerTreeView.defaultActions()
            idx = self.layerTreeView.currentIndex()
            if not idx.isValid():
                menu.addAction('Expand All', self.layerTreeView.expandAllNodes)
                menu.addAction('Collapse All', self.layerTreeView.collapseAllNodes)
                return menu
            else:
                node = self.layerTreeView.index2node(idx)
                if QgsLayerTree.isGroup(node):  #如果是组，显示对应菜单项目
                    self.actionZoomToGroup = self.actions.actionZoomToGroup(self.mapCanvas,menu)
                    menu.addAction(self.actionZoomToGroup)
                    self.actionRemoveGroupOrLayer = self.actions.actionRemoveGroupOrLayer(menu)
                    menu.addAction(self.actionRemoveGroupOrLayer)
                    self.actionRenameGroupOrLayer = self.actions.actionRenameGroupOrLayer()
                    menu.addAction(self.actionRenameGroupOrLayer)
                    self.actionAddGroup = self.actions.actionAddGroup(menu)
                    menu.addAction(self.actionAddGroup)
                    if self.layerTreeView.selectedNodes(True).count() >= 2:
                        self.actionGroupSelected = self.actions.actionGroupSelected(menu)
                        menu.addAction(self.actionGroupSelected)
                elif QgsLayerTree.isLayer(node):
                    # 如何拿到layer 并转换为vector/raster layer
                    layer: QgsMapLayer = node.layer()
                    if layer.isValid() and layer.isSpatial():
                        self.actionZoomToLayers = self.actions.actionZoomToLayers(self.mapCanvas,menu)
                        menu.addAction(self.actionZoomToLayers) #addAction直接传入self.actions.actionZoomToLayers(self.mapCanvas,menu)还不行，原因未知
                    self.actionRemoveGroupOrLayer = self.actions.actionRemoveGroupOrLayer(menu)
                    menu.addAction(self.actionRemoveGroupOrLayer)                  
                    if isinstance(layer, QgsVectorLayer) is True:
                        self.actionShowFeatureCount = self.actions.actionShowFeatureCount(menu)
                        menu.addAction(self.actionShowFeatureCount)
                return menu

        except:
            print('menu error')

    def updateRasterLayerRenderer(self, widget, layer):
        print("change")
        layer.setRenderer(widget.renderer())
        self.mapCanvas.refresh()

    def deleteSelectedLayer(self):
        deleteRes = QMessageBox.question(self.mainWindows, '信息', "确定要删除所选图层？", QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
        if deleteRes == QMessageBox.Yes:
            layers = self.layerTreeView.selectedLayers()
            for layer in layers:
                self.deleteLayer(layer)

    def deleteAllLayer(self):
        if len(QgsProject.instance().mapLayers().values()) == 0:
            QMessageBox.about(None, '信息', '您的图层为空')
        else:
            deleteRes = QMessageBox.question(self.mainWindows, '信息', "确定要删除所有图层？", QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)
            if deleteRes == QMessageBox.Yes:
                for layer in QgsProject.instance().mapLayers().values():
                    self.deleteLayer(layer)


    def deleteGroup(self, group: QgsLayerTreeGroup):
        deleteRes = QMessageBox.question(self.mainWindows, '信息', "确定要删除组？", QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
        if deleteRes == QMessageBox.Yes:
            layerTreeLayers = group.findLayers()
            for layer in layerTreeLayers:
                self.deleteLayer(layer.layer())
        QgsProject.instance().layerTreeRoot().removeChildNode(group)


    def deleteLayer(self, layer):
        QgsProject.instance().removeMapLayer(layer)
        self.mapCanvas.refresh()
        return 0
