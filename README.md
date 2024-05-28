# QGIS Python API二次开发示例大全

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
![输入图片说明](https://foruda.gitee.com/images/1716860053922322717/47e9a9fc_1547275.png "屏幕截图")

## using_raster_layers
### 功能截图
![输入图片说明](https://foruda.gitee.com/images/1716862894695413383/d1bbb9e5_1547275.png "屏幕截图")