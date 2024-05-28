from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMenu, QMessageBox
from PyQt5.QtGui import QColor

from qgis.gui import (
    QgsLayerTreeViewMenuProvider,QgsLayerTreeViewDefaultActions,QgsLayerTreeView,QgsMapCanvas,
    QgsRasterLayerProperties,QgsMultiBandColorRendererWidget)
from qgis.core import (
QgsLayerTree,QgsLayerTreeGroup,QgsMapLayer,QgsVectorLayer,QgsProject,
QgsRasterLayer,QgsColorRampShader,QgsRasterShader,QgsSingleBandPseudoColorRenderer,QgsSingleBandGrayRenderer,
QgsMultiBandColorRenderer,QgsHillshadeRenderer,QgsRasterContourRenderer)

from myrasterdetail import MyRasterDetail


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
                        menu.addAction(self.actionZoomToLayers)
                    self.actionRemoveGroupOrLayer = self.actions.actionRemoveGroupOrLayer(menu)
                    menu.addAction(self.actionRemoveGroupOrLayer)
                    if isinstance(layer,QgsVectorLayer) is True:
                        self.actionShowFeatureCount = self.actions.actionShowFeatureCount(menu)
                        menu.addAction(self.actionShowFeatureCount)
                    elif isinstance(layer,QgsRasterLayer) is True:
                        menu.addAction('QGis Properties',self.rasterlayerProperties)
                        menu.addAction('Custom Properties', self.rasterCustomProperties)
                        menu.addAction('SingleBandGrayRenderer',self.rasterSingleBandGrayRenderer)
                        menu.addAction('SingleBandPseudoColorRenderer',self.rasterSingleBandRenderer)
                        menu.addAction('MultiBandColorRenderer',self.rasterMultiBandColorRenderer)
                        menu.addAction('HillshadeRenderer',self.rasterHillshadeRenderer)
                        menu.addAction('ContourRenderer',self.rasterContourRenderer)
                        menu.addAction('Symbology Dialog',self.rasterShowSymbolWidget)
                return menu

        except:
            print('menu error')

    def rasterlayerProperties(self):
        layer = self.layerTreeView.currentLayer()
        if layer:
            prop = QgsRasterLayerProperties(layer,self.mapCanvas)
            prop.exec()


    def rasterCustomProperties(self):
        layer = self.layerTreeView.currentLayer()
        if layer:
            detail = MyRasterDetail(layer)
            detail.exec_()

    def rasterSingleBandGrayRenderer(self):
        rlayer = self.layerTreeView.currentLayer()
        if rlayer:
            grayBand = 1;
            renderer = QgsSingleBandGrayRenderer(rlayer.dataProvider(), grayBand );
            rlayer.setRenderer(renderer)
            rlayer.triggerRepaint()

    def rasterSingleBandRenderer(self):
        rlayer = self.layerTreeView.currentLayer()
        if rlayer:
            fcn = QgsColorRampShader()
            fcn.setColorRampType(QgsColorRampShader.Interpolated)
            lst = [QgsColorRampShader.ColorRampItem(0, QColor(0, 255, 0)),
                   QgsColorRampShader.ColorRampItem(255, QColor(255, 255, 0))]
            fcn.setColorRampItemList(lst)
            shader = QgsRasterShader()
            shader.setRasterShaderFunction(fcn)
            renderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(), 1, shader)
            rlayer.setRenderer(renderer)
            rlayer.triggerRepaint()

    def rasterMultiBandColorRenderer(self):
        rlayer = self.layerTreeView.currentLayer()
        if rlayer:
            renderer = QgsMultiBandColorRenderer(rlayer.dataProvider(),1,2,3)
            rlayer.setRenderer(renderer)
            rlayer.triggerRepaint()

    def rasterHillshadeRenderer(self):
        rlayer = self.layerTreeView.currentLayer()
        if rlayer:
            renderer = QgsHillshadeRenderer(rlayer.dataProvider(), 1,45,315)
            rlayer.setRenderer(renderer)
            rlayer.triggerRepaint()

    def rasterContourRenderer(self):
        rlayer = self.layerTreeView.currentLayer()
        if rlayer:
            renderer = QgsRasterContourRenderer(rlayer.dataProvider())
            renderer.setInputBand(1);
            renderer.setContourInterval(100.00);
            renderer.setContourIndexInterval(500.00);
            renderer.setDownscale(4.00);
            rlayer.setRenderer(renderer)
            rlayer.triggerRepaint()

    def rasterShowSymbolWidget(self):
        rlayer = self.layerTreeView.currentLayer()
        if rlayer:
            prop = QgsRasterLayerProperties(rlayer,self.mapCanvas)
            prop.exec()

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