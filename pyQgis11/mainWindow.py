from functools import partial

from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout

from qgis.PyQt.QtWidgets import QMainWindow
from qgis.core import QgsProject,QgsLayerTreeModel,QgsVectorLayer
from qgis.core import (
    edit,
    QgsExpression,
    QgsExpressionContext,
    QgsFeature,
    QgsFeatureRequest,
    QgsField,
    QgsFields,
    QgsVectorLayer,
    QgsPointXY,
    QgsGeometry,
    QgsProject,
    QgsExpressionContextUtils
)
from qgis.core import (
  QgsProcessingContext,
  QgsTaskManager,
  QgsTask,
  QgsProcessingAlgRunnerTask,
  Qgis,
  QgsProcessingFeedback,
  QgsApplication,
  QgsMessageLog,
)
from qgis.gui import QgsLayerTreeView,QgsMapCanvas,QgsLayerTreeMapCanvasBridge
from qgis.PyQt.QtCore import QVariant
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

        # 11. Expressions, Filtering and Calculating Values
        # QGIS has some support for parsing of SQL-like expressions.Only a small subset of SQL syntax is supported.
        # number string column referenc
        # 11.1.Parsing Expressions
        exp = QgsExpression('1 + 1 = 2')
        assert (not exp.hasParserError())
        exp = QgsExpression('2 * 3')
        print(exp)
        print(exp.evaluate())
        # 11.2.2. Expressions with features
        # To evaluate an expression against a feature, a QgsExpressionContext object has to be created and passed to the evaluate function in order to allow the expression to access the feature’s field values.
        fs = vlayer.getFeatures()
        f = (next(fs))
        print(f.id())
        exp = QgsExpression('"ELEV"')
        context = QgsExpressionContext()
        context.setFeature(f)
        print(exp.evaluate(context))

        # create a vector layer
        vl = QgsVectorLayer("Point", "Companies", "memory")
        pr = vl.dataProvider()
        pr.addAttributes([QgsField("Name", QVariant.String),
                          QgsField("Employees", QVariant.Int),
                          QgsField("Revenue", QVariant.Double),
                          QgsField("Rev. per employee", QVariant.Double),
                          QgsField("Sum", QVariant.Double),
                          QgsField("Fun", QVariant.Double)])
        vl.updateFields()

        # add data to the first three fields
        my_data = [
            {'x': 0, 'y': 0, 'name': 'ABC', 'emp': 10, 'rev': 100.1},
            {'x': 1, 'y': 1, 'name': 'DEF', 'emp': 2, 'rev': 50.5},
            {'x': 5, 'y': 5, 'name': 'GHI', 'emp': 100, 'rev': 725.9}]

        for rec in my_data:
            f = QgsFeature()
            pt = QgsPointXY(rec['x'], rec['y'])
            f.setGeometry(QgsGeometry.fromPointXY(pt))
            f.setAttributes([rec['name'], rec['emp'], rec['rev']])
            pr.addFeature(f)

        vl.updateExtents()
        QgsProject.instance().addMapLayer(vl)

        # The first expression computes the revenue per employee.
        # The second one computes the sum of all revenue values in the layer.
        # The final third expression doesn’t really make sense but illustrates
        # the fact that we can use a wide range of expression functions, such
        # as area and buffer in our expressions:
        expression1 = QgsExpression('"Revenue"/"Employees"')
        expression2 = QgsExpression('sum("Revenue")')
        expression3 = QgsExpression('area(buffer($geometry,"Employees"))')

        # QgsExpressionContextUtils.globalProjectLayerScopes() is a convenience
        # function that adds the global, project, and layer scopes all at once.
        # Alternatively, those scopes can also be added manually. In any case,
        # it is important to always go from “most generic” to “most specific”
        # scope, i.e. from global to project to layer
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(vl))
        # QgsExpressionContextUtils不知道干什么用的，似乎在声明变量周期
        with edit(vl):
            for f in vl.getFeatures():
                context.setFeature(f)
                f['Rev. per employee'] = expression1.evaluate(context)
                f['Sum'] = expression2.evaluate(context)
                f['Fun'] = expression3.evaluate(context)
                vl.updateFeature(f)

        print(f['Sum'])

        # params = dict()
        # context = QgsProcessingContext()
        # feedback = QgsProcessingFeedback()
        #
        # buffer_alg = QgsApplication.instance().processingRegistry().algorithmById('native:buffer')
        # task = QgsProcessingAlgRunnerTask(buffer_alg, params, context,
        #                                   feedback)

        MESSAGE_CATEGORY = 'AlgRunnerTask'

        def task_finished(context, successful, results):
            if not successful:
                QgsMessageLog.logMessage('Task finished unsucessfully',
                                         MESSAGE_CATEGORY, Qgis.Warning)
            output_layer = context.getMapLayer(results['OUTPUT'])
            # because getMapLayer doesn't transfer ownership, the layer will
            # be deleted when context goes out of scope and you'll get a
            # crash.
            # takeMapLayer transfers ownership so it's then safe to add it
            # to the project and give the project ownership.
            if output_layer and output_layer.isValid():
                QgsProject.instance().addMapLayer(
                    context.takeResultLayer(output_layer.id()))

        alg = QgsApplication.processingRegistry().algorithmById(
            'qgis:randompointsinextent')
        # `context` and `feedback` need to
        # live for as least as long as `task`,
        # otherwise the program will crash.
        # Initializing them globally is a sure way
        # of avoiding this unfortunate situation.
        context = QgsProcessingContext()
        feedback = QgsProcessingFeedback()
        params = {
            'EXTENT': '0.0,10.0,40,50 [EPSG:4326]',
            'MIN_DISTANCE': 0.0,
            'POINTS_NUMBER': 50000,
            'TARGET_CRS': 'EPSG:4326',
            'OUTPUT': 'memory:My random points'
        }
        task = QgsProcessingAlgRunnerTask(alg, params, context, feedback)
        task.executed.connect(partial(task_finished, context))
        QgsApplication.taskManager().addTask(task)
        # TODO 为什么task不能执行
        # Network analysis library 需要学会Graph怎么用