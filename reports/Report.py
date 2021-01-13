# -*- coding: utf-8 -*-

import sys, os
from qgis.core import *
from qgis.PyQt.QtXml import QDomDocument
from PyQt5.QtCore import *
from PyQt5.QtXml import *
# from PyPDF2 import PdfFileMerger
from qgis.PyQt.QtWidgets import QMessageBox


from . import ReportsDefinitions as RDef

import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import  MMTDefinitions
# reload(sys)
# sys.setdefaultencoding("utf-8")

class Report:
    """
    Brief:
    """

    def __init__(self,
                 iface,
                 pluginPath,
                 dbFileName,
                 reportType,
                 ret,
                 crsEpsgCod,
                 hotspot,
                 referenceLayer,
                 mapPanel):
        self.iface = iface
        self.pluginPath = pluginPath
        self.dbFileName = dbFileName
        self.qmlPath = None
        self.imgPath = None
        self.reportType = reportType
        self.tags = ret[1]
        self.values = ret[2]
        self.crsEpsgCod = str(crsEpsgCod)
        self.qgsCrs = QgsCoordinateReferenceSystem(self.crsEpsgCod)
        self.qptFilePath = None
        self.hotspot = hotspot
        self.referenceLayer = referenceLayer
        self.coordTxt =''
        # self.layout = None
        # self.items = None
        self.strProcessErrors = ''
        self.titleWindow = "Report Tools"
        self.mapPanel = mapPanel
        self.initialize()


    def addFeature(self, lyr, geom, zone=0):
        feature = QgsFeature()
        feature.setGeometry(geom)
        if lyr.name() == "Features Img":
            feature.setFields(lyr.dataProvider().fields())
            feature.setAttribute('zone', zone)
        lyr.startEditing()
        noerrorAdd = lyr.addFeature(feature)
        noerrorCommit = lyr.commitChanges()
        if not noerrorCommit:
            self.strProcessErrors = 'addFeature:Error'
            self.finalize()
        return feature

    def initialize(self):
        if self.reportType != RDef.CONST_REPORT_TYPE_1 \
                and self.reportType != RDef.CONST_REPORT_TYPE_2:
            self.strProcessErrors = 'Report.initialize'
            self.strProcessErrors += '\nReport type not found: ' + self.reportType
            self.finalize()
        if not self.reportType in RDef.qptFiles:
            self.strProcessErrors += 'Report.initialize'
            self.strProcessErrors += '\nReport type not found in qpt files container: ' + self.reportType
            self.finalize()

        # QMessageBox.information(self.iface.mainWindow(), self.titleWindow, self.reportType)
        self.qptFilePath = os.path.normcase(self.pluginPath + RDef.CONST_THIS_PATH + RDef.CONST_TEMPLATE_PATH
                                            + RDef.CONST_QPT_PATH + RDef.qptFiles[self.reportType][0])
        if not QFile.exists(self.qptFilePath):
            self.strProcessErrors = 'Report.initialize'
            self.strProcessErrors += '\nQpt file does not exist:\n' + self.qptFilePath
            self.finalize()

        # self.createLayoutFromQpt()

        self.qmlPath = os.path.normcase(self.pluginPath + RDef.CONST_THIS_PATH + RDef.CONST_TEMPLATE_PATH + RDef.CONST_QML_PATH)
        self.imgPath = self.pluginPath + RDef.CONST_THIS_PATH + RDef.CONST_TEMPLATE_PATH + RDef.CONST_IMG_PATH

        # if self.reportType == RDef.CONST_REPORT_TYPE_1:
        self.initializeHotSpotReport()

    def initializeHotSpotReport(self):
        self.factorLocationMap1 = RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][3]
        self.zoomMap2 = RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][4]
        self.zoomMap3 = RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][5]
        self.idNumZones = RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][6]
        self.idIniZone = RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][7]
        self.numInfoZone = RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][8]
        self.logoFile = self.imgPath+RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][9]
        self.simbMap1 = self.qmlPath+RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][10]
        self.simbMap2 = self.qmlPath+RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][11]
        self.simbMap3 = self.qmlPath+RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][12]
        self.xmlPath = self.pluginPath + RDef.CONST_THIS_PATH + RDef.CONST_TEMPLATE_PATH + RDef.CONST_XML_PATH
        self.xmlFileRampColor = self.xmlPath+RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][13]
        self.legendImg = self.imgPath+RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][14]
        self.simbPanels = self.qmlPath+RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][15]
        self.simbPanel = self.qmlPath+RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][16]
        # self.filenameOutputPrefix = self.values[0] + RDef.CONST_REPORT_TYPE_1
        self.listMaplayers1 = None
        self.listMaplayers2 = None
        self.listMaplayers3 = None
        self.colorRamp=None
        # QMessageBox.information(self.iface.mainWindow(), self.titleWindow, "HotSpotReport Initialized")
        self.createIGHotSpotReport()
        # self.generateHotSpotReport()
        # self.kk()


    def createRampColorFromXML(self):
        # Carga la paleta de colores del xml
        with open(self.xmlFileRampColor) as fColor:
            xmlRampColor = fColor.read()
        docRampColor = QDomDocument()
        docRampColor.setContent(xmlRampColor)
        rampColors = docRampColor.elementsByTagName('colorramp')
        for i in range(len(rampColors)):
            vNode = rampColors.at(i)
            vElement = vNode.toElement()
            if (vElement.attribute('name') == 'Iron'):
                self.colorRamp = QgsSymbolLayerUtils().loadColorRamp(vElement)
            else:
                self.strProcessErrors = 'createRampColorFromXML:Error'
                self.finalize()
        # QMessageBox.information(self.iface.mainWindow(), self.titleWindow, "RampColorFromXML created")

    # def createLayoutFromQpt(self):
    #     p = QgsProject()
    #     self.layout = QgsLayout(p)
    #     self.layout.initializeDefaults()
    #     paperSize = RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][1]
    #     if RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][2] == "Vertical":
    #         self.layout.pageCollection().page(0).setPageSize(paperSize, QgsLayoutItemPage.Orientation.Portrait)
    #     else:
    #         self.layout.pageCollection().page(0).setPageSize(paperSize, QgsLayoutItemPage.Orientation.Landscape)
    #     with open(self.qptFilePath,  'r', encoding='utf-8') as f:
    #         template_content = f.read()
    #     doc = QDomDocument()
    #     doc.setContent(template_content)
    #     # self.items, ok = self.layout.loadFromTemplate(doc, QgsReadWriteContext(), False)
    #     self.items, ok = self.layout.loadFromTemplate(doc, QgsReadWriteContext())
    #     if not ok:
    #         self.strProcessErrors = 'Report.createLayoutFromQpt'
    #         self.strProcessErrors += '\n:Error\n'
    #         self.finalize()
    #     else:
    #         QMessageBox.information(self.iface.mainWindow(), self.titleWindow, "LayoutFromQpt created")


    def createIGHotSpotReport(self):
        # Capa de imagen georeferenciada
        # layerName = "Ortofoto"
        # dirOrto = 'H:/Eiffage/SolarPark/PozoCanada/data/'
        # lyrRaster = QgsRasterLayer(dirOrto + 'ORTO.tif', layerName)
        # QgsProject.instance().addMapLayers([lyrRaster])
        lyrRaster = self.referenceLayer

        # Capa de feature georreferenciado para Mapa 1 y Mapa 2)
        # Capas Mapa 2
        lyrFeatureMap2 = QgsVectorLayer('Point?crs=EPSG:' + self.crsEpsgCod, "Feature Point Map", "memory")
        # QMessageBox.information(self.iface.mainWindow(), self.titleWindow, "IGHotSpotReport "+self.values[3])
        geomPoint = QgsGeometry()
        geomPoint = geomPoint.fromWkt(self.values[3])
        featurePointMap = self.addFeature(lyrFeatureMap2, geomPoint)
        lyrFeatureMap2.loadNamedStyle(self.simbMap2)

        uri = QgsDataSourceUri()
        uri.setDatabase(self.dbFileName)
        schema = ''
        table = MMTDefinitions.CONST_SPATIALITE_LAYERS_PHOTOVOLTAIC_PANELS_TABLE_NAME
        geom_column = MMTDefinitions.CONST_SPATIALITE_LAYERS_PHOTOVOLTAIC_ARRAY_PANELS_TABLE_GEOMETRY_COLUMN
        uri.setDataSource(schema, table, geom_column)
        display_name = 'photovoltaicPanels'
        panelsLayer = QgsVectorLayer(uri.uri(), display_name, 'spatialite')
        panelsLayer.loadNamedStyle(self.simbPanels)
        uri2 = QgsDataSourceUri()
        uri2.setDatabase(self.dbFileName)
        sql = 'ST_contains("'+geom_column + '", GeomFromText("' + self.values[3] + '"))'
        uri2.setDataSource(schema, table, geom_column, sql)
        display_name = 'photovoltaicPanel'
        panelLayer = QgsVectorLayer(uri2.uri(), display_name, 'spatialite')
        panelLayer.loadNamedStyle(self.simbPanel)
        if self.mapPanel:
            self.listMaplayers2 = [lyrFeatureMap2, panelLayer, panelsLayer, lyrRaster]
        else:
            self.listMaplayers2 = [lyrFeatureMap2, lyrRaster]
            # self.listMaplayers2 = [lyrFeatureMap2, panelLayer, lyrRaster]
        self.coordTxt = self.values[3]+'  EPSG: '+ self.crsEpsgCod

        # Capas Mapa 1
        lyrFeatureMap1 = QgsVectorLayer('Polygon?crs=EPSG:' + self.crsEpsgCod, "Extent Map 2", "memory")
        featureZone = self.addFeature(lyrFeatureMap1,
                                 QgsGeometry.fromRect(lyrFeatureMap2.extent().buffered(self.zoomMap2 * self.factorLocationMap1)))
        lyrFeatureMap1.loadNamedStyle(self.simbMap1)
        self.listMaplayers1 = [lyrFeatureMap1, lyrRaster]

        # Capas Mapa 3
        crs = QgsCoordinateReferenceSystem()
        crs.createFromSrid(int(self.crsEpsgCod))
        lyrImg = QgsRasterLayer(self.values[4] + '/' + self.values[5] + '.TIFF', 'image')
        lyrImg.setCrs(crs)
        lyrFeaturesImg = QgsVectorLayer('MultiPolygon?crs=EPSG:' + self.crsEpsgCod + '&field=zone:integer', "Features Img",
                                        "memory")

        for i in range(0, int(self.values[self.idNumZones]), 1):
            geom = QgsGeometry.fromWkt(self.values[self.idIniZone - 1 + self.numInfoZone * i])
            featureImg = self.addFeature(lyrFeaturesImg, QgsGeometry.fromWkt(self.values[self.idIniZone - 1 + self.numInfoZone * i]), i)

        styleLoaded = lyrFeaturesImg.loadNamedStyle(self.simbMap3)
        self.listMaplayers3 = [lyrFeaturesImg, lyrImg]

        if not lyrFeatureMap1.isValid() and lyrFeatureMap2.isValid() and lyrFeaturesImg.isValid():
            self.strProcessErrors = 'Report.createIGHotSpotReport'
            self.strProcessErrors += '\n:Error vectorial layers creation'
            self.finalize()
        if not lyrRaster.isValid() and lyrImg.isValid():
            self.strProcessErrors = 'Report.createIGHotSpotReport'
            self.strProcessErrors += '\n:Error raster layers creation'
            self.finalize()
        # QgsProject.instance().addMapLayers([lyrFeatureMap2, lyrFeaturesImg, lyrRaster, lyrImg])
        # QMessageBox.information(self.iface.mainWindow(), self.titleWindow, "IG HotSpotReport Created")
        self.createHotSpotReport(lyrFeatureMap2, lyrFeaturesImg, lyrRaster, lyrImg)

    def createHotSpotReport(self, lyrFeatureMap2, lyrFeaturesImg, lyrRaster, lyrImg):
        p = QgsProject()
        layout = QgsLayout(p)
        layout.initializeDefaults()
        paperSize = RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][1]
        if RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][2] == "Vertical":
            layout.pageCollection().page(0).setPageSize(paperSize, QgsLayoutItemPage.Orientation.Portrait)
        else:
            layout.pageCollection().page(0).setPageSize(paperSize, QgsLayoutItemPage.Orientation.Landscape)
        with open(self.qptFilePath,  'r', encoding='utf-8') as f:
            template_content = f.read()
        doc = QDomDocument()
        doc.setContent(template_content)
        # self.items, ok = self.layout.loadFromTemplate(doc, QgsReadWriteContext(), False)
        items, ok = layout.loadFromTemplate(doc, QgsReadWriteContext())
        for item in items:
            txt = ''
            itemName = item.displayName()
            if item.displayName() == 'logo':
                item.setPicturePath(self.logoFile)
                continue
            if item.displayName() == 'map1':
                item.setLayers(self.listMaplayers1)
                item.zoomToExtent(lyrRaster.extent())
                continue
            if item.displayName() == 'map2':
                item.setLayers(self.listMaplayers2)
                item.setCrs(self.qgsCrs)
                item.zoomToExtent(lyrFeatureMap2.extent().buffered(self.zoomMap2))
                continue
            if item.displayName() == 'img':
                item.zoomToExtent(lyrFeaturesImg.extent().buffered(self.zoomMap3))
                stats = lyrImg.dataProvider().bandStatistics(1, QgsRasterBandStats.All, item.extent())
                # print(str(stats.minimumValue)+','+str(stats.maximumValue))
                self.createRampColorFromXML()
                colorRampShader = QgsColorRampShader(stats.minimumValue, stats.maximumValue, self.colorRamp.clone(),
                                                     QgsColorRampShader.Interpolated, QgsColorRampShader.Continuous)
                colorRampShader.classifyColorRamp(self.colorRamp.count(), 1, item.extent())
                shader = QgsRasterShader()
                shader.setRasterShaderFunction(colorRampShader)
                renderer = QgsSingleBandPseudoColorRenderer(lyrImg.dataProvider(), 1, shader)
                lyrImg.setRenderer(renderer)
                item.setLayers(self.listMaplayers3)
                item.refresh()
                continue
            if item.displayName() == 'legendImg':
                # QMessageBox.information(self.iface.mainWindow(), self.titleWindow, self.legendImg)
                item.setPicturePath(self.legendImg)
                continue
            if item.displayName() == 'vmin':
                item.setText(str(int(stats.minimumValue * float(self.values[1]) + float(self.values[2]))))
                continue
            if item.displayName() == 'vmax':
                item.setText(str(int(stats.maximumValue * float(self.values[1]) + float(self.values[2]))))
                continue
            if item.displayName() == 'tagsGen':
                txt = 'Hotspot:\n'
                for i in range(5, 13, 1):
                    txt += self.tags[i] + ':\n'
                item.setText(txt)
                continue
            if item.displayName() == 'infoGen':
                txt = self.hotspot + '\n'
                for i in range(5, 13, 1):
                    txt += self.values[i] + '\n'
                item.setText(txt)
                continue
            if item.displayName() == 'tagsZone':
                txt = '\n'
                for i in range(self.idIniZone, self.idIniZone + self.numInfoZone - 1, 1):
                    txt += self.tags[i] + ':\n'
                item.setText(txt)
                continue
            if item.displayName() == 'coord':
                item.setText(self.coordTxt)
                continue
            if item.displayName() == 'info1':
                txt = 'Zona 1\n'
                for i in range(self.idIniZone, self.idIniZone + self.numInfoZone - 1, 1):
                    txt += self.values[i] + '\n'
                item.setText(txt)
                continue
            if item.displayName() == 'info2' and int(self.values[self.idNumZones]) > 1:
                txt = 'Zona 2\n'
                zone = 2
                for i in range(self.idIniZone + self.numInfoZone * (zone - 1),
                               self.idIniZone + self.numInfoZone * (zone - 1) + self.numInfoZone - 1, 1):
                    txt += self.values[i] + '\n'
                item.setText(txt)
                continue
            if item.displayName() == 'info3' and int(self.values[self.idNumZones]) > 2:
                txt = 'Zona 3\n'
                zone = 3
                for i in range(self.idIniZone + self.numInfoZone * (zone - 1),
                               self.idIniZone + self.numInfoZone * (zone - 1) + self.numInfoZone - 1, 1):
                    txt += self.values[i] + '\n'
                item.setText(txt)
                continue
            if item.displayName() == 'info4' and int(self.values[self.idNumZones]) > 3:
                txt = 'Zona 4\n'
                zone = 4
                for i in range(self.idIniZone + self.numInfoZone * (zone - 1),
                               self.idIniZone + self.numInfoZone * (zone - 1) + self.numInfoZone - 1, 1):
                    txt += self.values[i] + '\n'
                item.setText(txt)
                continue
            if item.displayName() == 'info5' and int(self.values[self.idNumZones]) > 4:
                txt = 'Zona 5\n'
                zone = 5
                for i in range(self.idIniZone + self.numInfoZone * (zone - 1),
                               self.idIniZone + self.numInfoZone * (zone - 1) + self.numInfoZone - 1, 1):
                    txt += self.values[i] + '\n'
                item.setText(txt)
                continue
            if item.displayName() == 'info6' and int(self.values[self.idNumZones]) > 5:
                txt = 'Zona 6\n'
                zone = 6
                for i in range(self.idIniZone + self.numInfoZone * (zone - 1),
                               self.idIniZone + self.numInfoZone * (zone - 1) + self.numInfoZone - 1, 1):
                    txt += self.values[i] + '\n'
                item.setText(txt)
                continue
        # QMessageBox.information(self.iface.mainWindow(), self.titleWindow, "HotSpotReport Created")
        exporter = QgsLayoutExporter(layout)
        self.filenameOutput = self.hotspot + '_' + self.values[5] + '.pdf'
        self.fileNamePathOutput = os.path.normcase(os.path.join(self.values[0], self.filenameOutput))
        exportResult = exporter.exportToPdf(self.fileNamePathOutput, QgsLayoutExporter.PdfExportSettings())
        # QMessageBox.information(self.iface.mainWindow(), self.titleWindow, "HotSpotReport Printed ")
        # os.startfile(self.fileNamePathOutput)
        return True
    #
    # def createHotSpotReport(self, lyrFeatureMap2, lyrFeaturesImg, lyrRaster, lyrImg):
    #     p = QgsProject()
    #     layout = QgsLayout(p)
    #     layout.initializeDefaults()
    #     paperSize = RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][1]
    #     if RDef.qptFiles[RDef.CONST_REPORT_TYPE_1][2] == "Vertical":
    #         layout.pageCollection().page(0).setPageSize(paperSize, QgsLayoutItemPage.Orientation.Portrait)
    #     else:
    #         layout.pageCollection().page(0).setPageSize(paperSize, QgsLayoutItemPage.Orientation.Landscape)
    #     with open(self.qptFilePath,  'r', encoding='utf-8') as f:
    #         template_content = f.read()
    #     doc = QDomDocument()
    #     doc.setContent(template_content)
    #     # self.items, ok = self.layout.loadFromTemplate(doc, QgsReadWriteContext(), False)
    #     items, ok = layout.loadFromTemplate(doc, QgsReadWriteContext())
    #
    #     # tagZones = self.tags[self.idIniZone:self.idIniZone + self.numInfoZone - 1]
    #     # maxlen = len(max(tagZones))
    #     # for tagZone in tagZones:
    #     #     for i in range(0, maxlen-len(tagZone), 1):
    #     #         tagZone += ' '
    #     #
    #     # numZones = int(self.values[self.idNumZones])
    #     # txtZones = ''
    #     # for tagZone in tagZones:
    #     #     txtZones += tagZone + '  '
    #     #     for zone in range(1, numZones+1, 1):
    #     #         index = self.idIniZone + self.numInfoZone * (zone - 1)
    #     #         txtZones += self.values[index]
    #     #     txtZones += '\n'
    #
    #     for item in items:
    #         txt = ''
    #         itemName = item.displayName()
    #         if item.displayName() == 'logo':
    #             item.setPicturePath(self.logoFile)
    #             continue
    #         if item.displayName() == 'map1':
    #             item.setLayers(self.listMaplayers1)
    #             item.zoomToExtent(lyrRaster.extent())
    #             continue
    #         if item.displayName() == 'map2':
    #             item.setLayers(self.listMaplayers2)
    #             item.setCrs(self.qgsCrs)
    #             item.zoomToExtent(lyrFeatureMap2.extent().buffered(self.zoomMap2))
    #             continue
    #         if item.displayName() == 'img':
    #             item.zoomToExtent(lyrFeaturesImg.extent().buffered(self.zoomMap3))
    #             stats = lyrImg.dataProvider().bandStatistics(1, QgsRasterBandStats.All, item.extent())
    #             # print(str(stats.minimumValue)+','+str(stats.maximumValue))
    #             self.createRampColorFromXML()
    #             colorRampShader = QgsColorRampShader(stats.minimumValue, stats.maximumValue, self.colorRamp.clone(),
    #                                                  QgsColorRampShader.Interpolated, QgsColorRampShader.Continuous)
    #             colorRampShader.classifyColorRamp(self.colorRamp.count(), 1, item.extent())
    #             shader = QgsRasterShader()
    #             shader.setRasterShaderFunction(colorRampShader)
    #             renderer = QgsSingleBandPseudoColorRenderer(lyrImg.dataProvider(), 1, shader)
    #             lyrImg.setRenderer(renderer)
    #             item.setLayers(self.listMaplayers3)
    #             item.refresh()
    #             continue
    #         if item.displayName() == 'legendImg':
    #             # QMessageBox.information(self.iface.mainWindow(), self.titleWindow, self.legendImg)
    #             item.setPicturePath(self.legendImg)
    #             continue
    #         if item.displayName() == 'vmin':
    #             item.setText(str(int(stats.minimumValue * float(self.values[1]) + float(self.values[2]))))
    #             continue
    #         if item.displayName() == 'vmax':
    #             item.setText(str(int(stats.maximumValue * float(self.values[1]) + float(self.values[2]))))
    #             continue
    #         if item.displayName() == 'tagsGen':
    #             txt = 'Hotspot:\n'
    #             for i in range(5, 13, 1):
    #                 txt += self.tags[i] + ':\n'
    #             item.setText(txt)
    #             continue
    #         if item.displayName() == 'infoGen':
    #             txt = self.hotspot + '\n'
    #             for i in range(5, 13, 1):
    #                 txt += self.values[i] + '\n'
    #             item.setText(txt)
    #             continue
    #         # if item.displayName() == 'infoZone':
    #         #     item.setText(txtZones)
    #         #     continue
    #       # QMessageBox.information(self.iface.mainWindow(), self.titleWindow, "HotSpotReport Created")
    #     exporter = QgsLayoutExporter(layout)
    #     self.filenameOutput = self.hotspot + '_' + self.values[5] + '.pdf'
    #     self.fileNamePathOutput = os.path.normcase(os.path.join(self.values[0], self.filenameOutput))
    #     exportResult = exporter.exportToPdf(self.fileNamePathOutput, QgsLayoutExporter.PdfExportSettings())
    #     # QMessageBox.information(self.iface.mainWindow(), self.titleWindow, "HotSpotReport Printed ")
    #     # os.startfile(self.fileNamePathOutput)
    #     return True

    def finalize(self):
        msg = QMessageBox()
        msg.setWindowTitle(self.titleWindow)
        msg.setIcon(QMessageBox.Warning)
        msg.setText(self.strProcessErrors)
        msg.exec_()
        return False


