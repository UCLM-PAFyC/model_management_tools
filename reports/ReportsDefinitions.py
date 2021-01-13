# -*- coding: utf-8 -*-
__author__ = 'david.hernandez@uclm.es'

# ICONS: <div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/"             title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/"             title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

CONST_REPORT_TYPE_1 = "PhHotspot"
CONST_REPORT_TYPE_2 = "PwLHazardArea"
CONST_THIS_PATH = "/reports"
CONST_TEMPLATE_PATH = "/templates"
CONST_QPT_PATH = "/qpt/"
CONST_NO_COMBO_SELECT = " ... "
CONST_QML_PATH = "/qml/"
CONST_XML_PATH = "/xml/"
CONST_IMG_PATH = "/img/"

qptFiles={}
#qptFiles[CONST_REPORT_TYPE_1] = [qptFile, paperSize='A4', orientationPage= "Vertical", factorLocationMap1 =1, zoomMap2 =8, zoomMap3 = 10, idNumZones = 13, idIniZone = 15, numInfoZone = 15, logo, )
#simbFeatureLocation, simbFeature, simbFeatureImg, ],

qptFiles[CONST_REPORT_TYPE_1] = ['templateFeatureImgThermal.qpt','A4',"Vertical", 1, 8, 20, 13, 15, 15, 'logo-gran.jpg',
                                 'featureLocation.qml', 'featurePointMap.qml', 'featureImg.qml', 'rampColorIron.xml', 'rampcolor-iron.png', 'PhotovoltaicPanels.qml', 'PhotovoltaicPanel.qml']
# qptFiles[CONST_REPORT_TYPE_2] = ['templateFeatureImgThermal.qpt','A4',CONST_TEMPLATE_VERTICAL]
