
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout

from qgis.PyQt.QtWidgets import QMainWindow
from qgis.gui import QgsLayerTreeView,QgsMapCanvas,QgsLayerTreeMapCanvasBridge
from qgis.core import (
    QgsRasterLayer,
    QgsProject,
    QgsPointXY,
    QgsRaster,
    QgsRasterShader,
    QgsColorRampShader,
    QgsSingleBandPseudoColorRenderer,
    QgsSingleBandColorDataRenderer,
    QgsSingleBandGrayRenderer,
    QgsLayerTreeModel,
    QgsRasterBlock,
    Qgis
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

        path_to_tif = r"../python_cookbook/data/srtm.tif"
        rlayer = QgsRasterLayer(path_to_tif, "SRTM")
        if not rlayer.isValid():
            print("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(rlayer)

        print(rlayer.width(), rlayer.height())
        print(rlayer.extent())
        print(rlayer.extent().toString())
        print(rlayer.rasterType())
        print(rlayer.bandCount())
        print(rlayer.bandName(1))
        print(rlayer.metadata())
        print(rlayer.renderer())
        print(rlayer.renderer().type())

        fcn = QgsColorRampShader()
        fcn.setColorRampType(QgsColorRampShader.Interpolated)
        lst = [QgsColorRampShader.ColorRampItem(0, QColor(0, 255, 0)),
               QgsColorRampShader.ColorRampItem(255, QColor(255, 255, 0))]
        fcn.setColorRampItemList(lst)
        shader = QgsRasterShader()
        shader.setRasterShaderFunction(fcn)
        renderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(), 1, shader)
        rlayer.setRenderer(renderer)
        rlayer.triggerRepaint() #不调用也可以

        rlayer_multi  = QgsRasterLayer(r"../python_cookbook/multiband.tif", "MULTIBAND")
        if not rlayer_multi.isValid():
            print("Layer failed to load!")
        else:
            self.statusbar.showMessage("Layer load Done!")
            QgsProject.instance().addMapLayer(rlayer_multi)

        rlayer_multi.renderer().setGreenBand(1)
        rlayer_multi.renderer().setRedBand(2)

        val, res = rlayer.dataProvider().sample(QgsPointXY(20.50, -34), 1)
        print(f'{val}:{res}')

        ident = rlayer.dataProvider().identify(QgsPointXY(20.5, -34), QgsRaster.IdentifyFormatValue)

        if ident.isValid():
          print(ident.results())

        block = QgsRasterBlock(Qgis.Byte, 2, 2)
        block.setData(b'\xaa\xbb\xcc\xdd')
        provider = rlayer.dataProvider()
        provider.setEditable(True)
        provider.writeBlock(block, 1, 0, 0)
        provider.setEditable(False)
