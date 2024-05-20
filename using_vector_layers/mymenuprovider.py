from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMenu, QMessageBox, QAction, QDialog, QFormLayout,QTableView

from qgis.gui import (
    QgsLayerTreeViewMenuProvider,QgsLayerTreeViewDefaultActions,QgsLayerTreeView,QgsMapCanvas,
    QgsMapLayerComboBox,QgsFieldComboBox,QgsAttributeTableModel,QgsAttributeTableFilterModel,QgsAttributeTableView)
from qgis.core import (
    QgsLayerTree,QgsLayerTreeGroup,QgsMapLayer,QgsVectorLayer,QgsProject,QgsMapLayerProxyModel,
    QgsVectorLayerCache)


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
                        menu.addAction('Show Fields', self.showlayerfields)
                        menu.addAction('Open Attribute Table',self.showlayertableview)
                        menu.addAction('Save Feature As...',self.savefeatureas)
                return menu

        except:
            print('menu error')

    def savefeatureas(self):
        vlayer = self.mapCanvas.currentLayer()


    def showlayertableview(self):
        vlayer = self.mapCanvas.currentLayer()
        self.vector_layer_cache = QgsVectorLayerCache(vlayer, 10000)
        self.attribute_table_model = QgsAttributeTableModel(self.vector_layer_cache)
        self.attribute_table_model.loadLayer()

        self.attribute_table_filter_model = QgsAttributeTableFilterModel(
            self.mapCanvas,
            self.attribute_table_model
        )
        self.attribute_table_view = QgsAttributeTableView()
        self.attribute_table_view.setModel(self.attribute_table_filter_model)
        self.attribute_table_view.show()

    def showlayerfields(self):
        # Create dialog
        new_dialog = QDialog()
        # Add combobox for layer and field
        map_layer_combo_box = QgsMapLayerComboBox()
        map_layer_combo_box.setCurrentIndex(-1)
        map_layer_combo_box.setFilters(QgsMapLayerProxyModel.VectorLayer)
        field_combo_box = QgsFieldComboBox()

        # Create a form layout and add the two combobox
        layout = QFormLayout()
        layout.addWidget(map_layer_combo_box)
        layout.addWidget(field_combo_box)

        # Add signal event
        map_layer_combo_box.layerChanged.connect(field_combo_box.setLayer)  # setLayer is a native slot function

        def on_field_changed(fieldName):
            print(fieldName)
            print("Layer field changed")

        field_combo_box.fieldChanged.connect(on_field_changed)

        new_dialog.setLayout(layout)
        new_dialog.exec_()
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