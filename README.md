# PyQGIS二次开发示例大全

| 名称 | 描述 |
|--|--|
| sample_qgs_vector_raster | qgs、矢量图层、栅格图层的加载示例 |
| sample_mapcanvas_maptool_layertree | mapcanvas、maptools、layertree、右键菜单等示例 |
| using_raster_layers | 栅格图层的使用示例 |
| using_vector_layers | 矢量图层的使用示例 |
| sample_diagrams | 地图图表示例 |
| sample_processing | native,qgis,gdal算法使用示例 |
| hellopyqgis | 基于pyqt5Widget调用QGis库，获取QGis的发行名称示例 |
| basepyqgis | 基础程序，以上示例程序都基于此程序修改 |

# 项目特性
- 基于QGis3.28 
- Apache 协议开源
- [QGIS Python API documentation](https://qgis.org/pyqgis/master/index.html)
- [pyqgis_developer_cookbook](https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/index.html)

# 社群
## 公众号
![输入图片说明](https://foruda.gitee.com/images/1697077286578350399/c111e1c7_1547275.jpeg "qrcode_for_gh_5fe62453ec05_258.jpg")
- 请关注微信公众号获取最新消息推送
## QQ群
![输入图片说明](https://foruda.gitee.com/images/1699751451905542002/42412fe3_1547275.png "屏幕截图")
- 加入qq群
## 知识星球
![输入图片说明](https://foruda.gitee.com/images/1697160230025579811/496ec4a9_1547275.png "屏幕截图")
- 加入知识星球有偿咨询

# 源码说明
## sample_qgs_vector_raster
### 功能截图
- [x] 加载各种格式数据
    - [x] qgis项目文件
    - [x] shapefile
    - [x] gpx
    - [x] gpkg
    - [x] geojson
    - [x] gml
    - [x] kml
    - [x] dxf
    - [x] coverage目录
    - [x] csv
    - [x] spalialite数据库
    - [x] memory
    - [x] wfs
    - [x] raster栅格
    - [x] wms
- 加载qgs(qgis项目文件)
![输入图片说明](https://foruda.gitee.com/images/1716798528404642956/1b8d887e_1547275.png "屏幕截图")
- 加载矢量图层(按照Data Provider分类：Ogr,Gpx,Delimitedtext,Spatialite,Memory)
![输入图片说明](https://foruda.gitee.com/images/1716799103538354990/ebd0554b_1547275.png "屏幕截图")
    - shapefile
![输入图片说明](https://foruda.gitee.com/images/1716799139522917348/21388b75_1547275.png "屏幕截图")
    - gpx
![输入图片说明](https://foruda.gitee.com/images/1716799187481445852/d36af863_1547275.png "屏幕截图")
    - csv
![输入图片说明](https://foruda.gitee.com/images/1716859294147911386/fbfac846_1547275.png "屏幕截图")
    - Spatialite
![输入图片说明](https://foruda.gitee.com/images/1716859412080284053/e0b28343_1547275.png "屏幕截图")
    - Memory
![输入图片说明](https://foruda.gitee.com/images/1716859473405484194/85c031fe_1547275.png "屏幕截图")
    - Wfs
![输入图片说明](https://foruda.gitee.com/images/1716859542571317785/6ad7ea6c_1547275.png "屏幕截图")
- 加载栅格图层(按照Data Provider分类：Gdal,Wms)
![输入图片说明](https://foruda.gitee.com/images/1716859648562875414/03701d25_1547275.png "屏幕截图")
    - Gdal
![输入图片说明](https://foruda.gitee.com/images/1716859701161849546/e9b8aad7_1547275.png "屏幕截图")
    - Wms
![输入图片说明](https://foruda.gitee.com/images/1716859757502377427/85d4d902_1547275.png "屏幕截图")

## sample_mapcanvas_maptool_layertree
### 功能截图
- [x] mapcanvas
- [x] maptool
- [x] layertree
- [x] layertree右键菜单
- [x] mapcanvas右键菜单
![输入图片说明](https://foruda.gitee.com/images/1716860053922322717/47e9a9fc_1547275.png "屏幕截图")
![输入图片说明](https://foruda.gitee.com/images/1716944627713788445/da543c99_1547275.gif "maptool.gif")

## using_raster_layers
### 功能截图
- [x] 栅格图层属性显示
- [x] 栅格图层属性自定义显示
- [x] 栅格图层符号系统
![输入图片说明](https://foruda.gitee.com/images/1716862894695413383/d1bbb9e5_1547275.png "屏幕截图")
    - QGis栅格图层属性框
![输入图片说明](https://foruda.gitee.com/images/1716944864077672171/32b6784a_1547275.gif "rasterqgisproperty.gif")
    - 栅格图层自定义属性框
![输入图片说明](https://foruda.gitee.com/images/1716944904009711546/45855420_1547275.gif "rastercustomproperty.gif")
    - 代码设置符号系统
![输入图片说明](https://foruda.gitee.com/images/1716944944631402762/099a14a7_1547275.gif "rastersinglegray.gif")
![输入图片说明](https://foruda.gitee.com/images/1716946233834224530/da03512b_1547275.gif "rastersinglePseudo.gif")
![输入图片说明](https://foruda.gitee.com/images/1716945079913198979/ca62255b_1547275.gif "rastersinglemulti.gif")
![输入图片说明](https://foruda.gitee.com/images/1716945032755943982/de9e68b7_1547275.gif "hillshade.gif")
![输入图片说明](https://foruda.gitee.com/images/1716945057021565954/cdb7c8bf_1547275.gif "courd.gif")
    - gui设置符号系统
![输入图片说明](https://foruda.gitee.com/images/1716863698103137896/1be44c6f_1547275.png "屏幕截图")

## using_vector_layers
### 功能截图
- [x] 显示图层所有字段
- [x] 显示图层属性表
- [x] 选择feature
- [x] 图层属性、设置符号系统等
- [x] 代码设置图层符号：点符号、线符号和面符号

    - `QgsFieldComboBox`显示图层字段Fields
![输入图片说明](https://foruda.gitee.com/images/1716945893836059738/3f639010_1547275.gif "vectorshowfields.gif")
    - 使用`QgsAttributeTableModel,QgsAttributeTableView`显示属性表
![输入图片说明](https://foruda.gitee.com/images/1716945911471790958/487a6353_1547275.gif "vectorshowattribute.gif")
    - 图层属性
    ![输入图片说明](https://foruda.gitee.com/images/1716892465795361062/1cc2705f_1547275.png "屏幕截图")
    - 单一符号-简单点符号
![输入图片说明](https://foruda.gitee.com/images/1716945979515771384/2b65cfaa_1547275.gif "vectorsymbolsimplemarker.gif")
    - 单一符号-svg点符号
![输入图片说明](https://foruda.gitee.com/images/1716945993774522985/997f2f62_1547275.gif "vectorsymbolsvgmarker.gif")
    - 分类符号
![输入图片说明](https://foruda.gitee.com/images/1716946010850094180/98fd8952_1547275.gif "vectorsymbolcatotry.gif")
    - 分级符号
![输入图片说明](https://foruda.gitee.com/images/1716946023336028520/01bf40fc_1547275.gif "vectorsymbolgradute.gif")
    - 单一符号-插值线符号
![输入图片说明](https://foruda.gitee.com/images/1716946039141671027/88d1a91a_1547275.gif "vectorsymbolline.gif")
    - 单一符号-svg面填充符号
![输入图片说明](https://foruda.gitee.com/images/1716946050959929571/9f280ff8_1547275.gif "vectorsymbolpolygon.gif")
    - feature全选取消
    ![输入图片说明](https://foruda.gitee.com/images/1716946172217442153/ca8939ed_1547275.gif "vectorselectall.gif")
    - select by value
    ![输入图片说明](https://foruda.gitee.com/images/1716946189954097816/759a53e2_1547275.gif "vectorselectbyvalue.gif")
    - select by expression
    ![输入图片说明](https://foruda.gitee.com/images/1716946215307849464/9fba1b58_1547275.gif "vectorselectbyexpression.gif")
## sample_diagrams
### 功能截图
- [x] 饼图(Pie Diagram)
- [x] 文本图(Text Diagram)
- [x] 直方图(Histogram)
- [x] 分段条形图(StackedBar Diagram)

![输入图片说明](https://foruda.gitee.com/images/1716892945098854624/03025491_1547275.png "屏幕截图")
![输入图片说明](https://foruda.gitee.com/images/1716892879909004470/62ba8b6b_1547275.png "屏幕截图")
![输入图片说明](https://foruda.gitee.com/images/1716892892247028335/01ba89c4_1547275.png "屏幕截图")
![输入图片说明](https://foruda.gitee.com/images/1716892904158196463/87fa500e_1547275.png "屏幕截图")
![输入图片说明](https://foruda.gitee.com/images/1716892914758183357/3c5203e8_1547275.png "屏幕截图")

## sample_processing
### 功能截图
- [x] native:randompointsinextents算法使用示例
- [x] qgis:randompointsinsidepolygons算法使用示例
- [x] gdal:cliprasterbyextent算法使用示例

    - 在extent中生成随机点
![输入图片说明](https://foruda.gitee.com/images/1716893153774439791/3565daa1_1547275.png "屏幕截图")
    - 在polygons生成随机点
![输入图片说明](https://foruda.gitee.com/images/1716893247555728292/ab9bca60_1547275.png "屏幕截图")
    - 栅格图层裁剪
![输入图片说明](https://foruda.gitee.com/images/1716893378757029904/85bd12a5_1547275.png "屏幕截图")

## hellopyqgis
### 功能截图
- [x] hello pyqgis
![输入图片说明](https://foruda.gitee.com/images/1716893457142151737/8a7e4934_1547275.png "屏幕截图")

# 参考资料
- [pyqgis_developer_cookbook](https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook)
- [QGIS Python API](https://qgis.org/pyqgis/master/index.html)
- [pyqgis-samples](https://github.com/webgeodatavore/pyqgis-samples/)
- [pyqgis二次开发专栏](https://www.zhihu.com/column/c_1641448508350812161)