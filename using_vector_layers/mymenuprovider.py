from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMenu, QMessageBox, QAction, QDialog, QFormLayout,QTableView
from PyQt5.QtGui import QColor

from qgis.gui import (
    QgsLayerTreeViewMenuProvider,QgsLayerTreeViewDefaultActions,QgsLayerTreeView,QgsMapCanvas,
    QgsMapLayerComboBox,QgsFieldComboBox,QgsAttributeTableModel,QgsAttributeTableFilterModel,QgsAttributeTableView,
    QgsVectorLayerProperties)
from qgis.core import (QgsApplication,
    QgsLayerTree,QgsLayerTreeGroup,QgsMapLayer,QgsVectorLayer,QgsProject,QgsMapLayerProxyModel,
    QgsVectorLayerCache,QgsWkbTypes,QgsSymbol,QgsLineSymbol,QgsFillSymbol,
    QgsSingleSymbolRenderer,QgsSvgMarkerSymbolLayer,QgsMarkerSymbol,
    QgsCategorizedSymbolRenderer,QgsRendererCategory,
    QgsGraduatedSymbolRenderer,QgsRendererRange,
    QgsInterpolatedLineSymbolLayer,QgsSVGFillSymbolLayer)


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
                        menu.addAction('Show Symbology Dialog',self.showSymbologyDialog)
                        if layer.geometryType() == QgsWkbTypes.GeometryType.PointGeometry:
                            menu.addAction('Single Symbol - Simple Marker', self.symbol_single_simple_marker)
                            menu.addAction('Single Symbol - Svg Marker', self.symbol_single_svg_marker)
                            menu.addAction('Categorized Symbol',self.symbol_categorized)
                            menu.addAction('Graduated Symbol', self.symbol_graduated)
                        elif layer.geometryType() == QgsWkbTypes.GeometryType.LineGeometry:
                            menu.addAction('Single Symbol - Interpolated Line',self.symbol_single_interpolated_line)
                        elif layer.geometryType() == QgsWkbTypes.GeometryType.PolygonGeometry:
                            menu.addAction('Single Symbol - Svg Fill', self.symbol_single_svg_fill)
                return menu

        except:
            print('menu error')

    def savefeatureas(self):
        vlayer = self.mapCanvas.currentLayer()
        # QgsVectorLayerSaveAsDialog 这是一个问题，文档上有，但是实际调用却不行
        print(vlayer.geometryType())

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

    def showSymbologyDialog(self):
        vlayer = self.layerTreeView.currentLayer()
        if vlayer:
            prop = QgsVectorLayerProperties(self.mapCanvas,None,vlayer)
            prop.exec()

    def symbol_single_simple_marker(self):
        vlayer = self.layerTreeView.currentLayer()
        if vlayer:
            symbol = QgsMarkerSymbol.createSimple({'name': 'square', 'color': 'red'})
            vlayer.renderer().setSymbol(symbol)
            # show the change
            vlayer.triggerRepaint()

    def symbol_single_svg_marker(self):
        vlayer = self.layerTreeView.currentLayer()
        if vlayer:
            svgpath = '../python_cookbook/test.svg'
            # svglayer = QgsSvgMarkerSymbolLayer(svgpath,size=12)
            self.svglayer = QgsSvgMarkerSymbolLayer.create({'name':svgpath,'size':'12','outline_color':'red'})
            symbol = QgsMarkerSymbol([self.svglayer])
            vlayer.renderer().setSymbol(symbol)
            # show the change
            vlayer.triggerRepaint()

    def symbol_categorized(self):
        vlayer = self.layerTreeView.currentLayer()
        if vlayer:
            self.svglayer1 = QgsSvgMarkerSymbolLayer.create({'name': "../python_cookbook/svg/airport.svg", 'size': '4'})
            self.symbol1 = QgsMarkerSymbol([self.svglayer1])
            self.svglayer2 = QgsSvgMarkerSymbolLayer.create({'name': "../python_cookbook/svg/airport1.svg", 'size': '4'})
            self.symbol2 = QgsMarkerSymbol([self.svglayer2])
            self.svglayer3 = QgsSvgMarkerSymbolLayer.create({'name': "../python_cookbook/svg/airport3.svg", 'size': '4'})
            self.symbol3 = QgsMarkerSymbol([self.svglayer3])
            self.svglayer4 = QgsSvgMarkerSymbolLayer.create({'name': "../python_cookbook/svg/airport2.svg", 'size': '4'})
            self.symbol4 = QgsMarkerSymbol([self.svglayer4])

            cat1 = QgsRendererCategory('Civilian/Public', self.symbol1, 'Civilian/Public')
            cat2 = QgsRendererCategory('Joint Military/Civilian', self.symbol2, 'Joint Military/Civilian')
            cat3 = QgsRendererCategory('Military', self.symbol3, 'Military')
            cat4 = QgsRendererCategory('Other', self.symbol4, 'Other')

            categorized_renderer = QgsCategorizedSymbolRenderer()
            categorized_renderer.setClassAttribute("USE")
            categorized_renderer.addCategory(cat1)
            categorized_renderer.addCategory(cat2)
            categorized_renderer.addCategory(cat3)
            categorized_renderer.addCategory(cat4)
            vlayer.setRenderer(categorized_renderer)
            vlayer.triggerRepaint()

    def symbol_graduated(self):
        vlayer = self.layerTreeView.currentLayer()
        if vlayer:
            myTargetField = 'ELEV'
            myRangeList = []
            myOpacity = 1
            # Make our first symbol and range...
            myMin = 0.0
            myMax = 50.0
            myLabel = 'Group 1'
            myColour = QColor('#ffee00')
            mySymbol1 = QgsSymbol.defaultSymbol(vlayer.geometryType())
            mySymbol1.setColor(myColour)
            mySymbol1.setOpacity(myOpacity)
            myRange1 = QgsRendererRange(myMin, myMax, mySymbol1, myLabel)
            myRangeList.append(myRange1)
            # now make another symbol and range...
            myMin = 50.1
            myMax = 100
            myLabel = 'Group 2'
            myColour = QColor('#00eeff')
            mySymbol2 = QgsSymbol.defaultSymbol(vlayer.geometryType())
            mySymbol2.setColor(myColour)
            mySymbol2.setOpacity(myOpacity)
            myRange2 = QgsRendererRange(myMin, myMax, mySymbol2, myLabel)
            myRangeList.append(myRange2)
            myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
            myClassificationMethod = QgsApplication.classificationMethodRegistry().method("EqualInterval")
            myRenderer.setClassificationMethod(myClassificationMethod)
            myRenderer.setClassAttribute(myTargetField)

            vlayer.setRenderer(myRenderer)
            vlayer.triggerRepaint()

    def symbol_single_interpolated_line(self):
        vlayer = self.layerTreeView.currentLayer()
        if vlayer:
            self.interpolLayer = QgsInterpolatedLineSymbolLayer.create({'single_color':'black'})
            symbol = QgsLineSymbol([self.interpolLayer])
            vlayer.renderer().setSymbol(symbol)
            vlayer.triggerRepaint()

    def symbol_single_svg_fill(self):
        vlayer = self.layerTreeView.currentLayer()
        if vlayer:
            svgpath = '../python_cookbook/test.svg'
            self.svgLayer = QgsSVGFillSymbolLayer.create({'svgFile':svgpath})
            symbol = QgsFillSymbol([self.svgLayer])
            vlayer.renderer().setSymbol(symbol)
            vlayer.triggerRepaint()

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